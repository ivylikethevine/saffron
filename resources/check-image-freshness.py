#!/usr/bin/env python3
"""Report Saffron images whose pinned tag is behind the newest upstream tag.

Saffron pins every image to a specific release (see ROADMAP.md, "Pin image
versions"), which stops surprise breakage but means nothing notices when
upstream ships a new version. Watchtower updates running containers, not the
committed YAML, so `compose.yaml` drifts silently.

Dependabot can't cover this: its docker ecosystem only matches `Dockerfile`
and `docker-compose.yml`/`.yaml`, and every stack here uses `compose.yaml`.
So this script does the equivalent check directly against the registries.

Best-effort by design — it never exits non-zero for a stale image. Network
failures, rate limits, and unparseable tags are reported as "skipped", not
treated as findings.

Usage:
    python3 resources/check-image-freshness.py
    python3 resources/check-image-freshness.py --markdown   # for CI summaries
"""

import argparse
import json
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

import yaml

TIMEOUT = 15
USER_AGENT = "saffron-image-freshness/1.0"

# GHCR paginates 100 tags at a time and orders them by upload date, so real
# version tags can sit several pages deep behind signature artifacts.
GHCR_MAX_PAGES = 5
LINK_NEXT_RE = re.compile(r'<(?P<url>[^>]+)>;\s*rel="next"')

# Tags that are floating on purpose — upstream publishes no useful semver, so
# `pull_policy: always` is doing the work instead. Nothing to compare against.
FLOATING = {"latest", "nightly", "develop", "stable", "main", "edge"}

# A tag we can reason about: an optional prefix, a dotted numeric core, and an
# optional suffix. Comparisons only happen between tags with an identical
# prefix and suffix, so `nightly-2.6.2.5548-ls10` is never compared against a
# plain `2.7.0`, and `16.15-alpine` stays in the alpine track.
TAG_RE = re.compile(r"^(?P<prefix>[a-zA-Z-]*?)(?P<core>\d+(?:\.\d+)*)(?P<suffix>.*)$")

# Suffixes whose trailing digits are themselves a version to compare
# (linuxserver's `-ls10` build number). Everything else is matched literally.
SUFFIX_BUILD_RE = re.compile(r"^(?P<label>-[a-zA-Z]+)(?P<build>\d+)$")


def parse_tag(tag):
    """Split a tag into (prefix, numeric tuple, suffix-label, build number).

    Returns None if the tag has no numeric core to compare.
    """
    match = TAG_RE.match(tag)
    if not match:
        return None
    core = tuple(int(part) for part in match.group("core").split("."))
    suffix = match.group("suffix")
    build_match = SUFFIX_BUILD_RE.match(suffix)
    if build_match:
        return (match.group("prefix"), core, build_match.group("label"),
                int(build_match.group("build")))
    return (match.group("prefix"), core, suffix, 0)


def fetch(url, headers=None):
    payload, _ = fetch_with_headers(url, headers)
    return payload


def fetch_with_headers(url, headers=None):
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT,
                                                   **(headers or {})})
    with urllib.request.urlopen(request, timeout=TIMEOUT) as response:
        return json.loads(response.read()), response.headers


def split_image(image):
    """Split `image:tag` into (registry, repository, tag)."""
    repo, sep, tag = image.rpartition(":")
    # No colon at all, or a colon that's part of a registry host:port rather
    # than a tag separator (`host:5000/repo`) — the image is untagged.
    if not sep or "/" in tag:
        repo, tag = image, "latest"
    if repo.startswith("ghcr.io/"):
        return "ghcr.io", repo[len("ghcr.io/"):], tag
    if "/" not in repo:
        return "docker.io", f"library/{repo}", tag
    return "docker.io", repo, tag


def docker_hub_tags(repo):
    url = (f"https://hub.docker.com/v2/repositories/{repo}/tags"
           f"?page_size=100&ordering=last_updated")
    return [item["name"] for item in fetch(url).get("results", [])]


def ghcr_tags(repo):
    """Candidate version tags for a GHCR image.

    Merges two sources, because each misses things the other catches.

    The GitHub releases API (`ghcr.io/OWNER/REPO` almost always maps to
    `github.com/OWNER/REPO`) returns newest-first in one request, but can lag
    the registry — bitmagnet publishes a `v0.10.1` image tag with no matching
    GitHub release.

    GHCR's own `tags/list` catches those, but cannot be relied on alone: it
    returns tags in *ascending upload order*, so page 1 holds the oldest tags
    (home-assistant's page 1 is 2021 dev builds) and the current release sits
    at the very end, potentially thousands of pages deep. Walking forward from
    page 1 finds old tags, not new ones — which is why the page-budget walk is
    a supplement here, not the primary source.
    """
    return list(dict.fromkeys(github_release_tags(repo) + ghcr_tag_list(repo)))


def github_release_tags(repo):
    """Release tag names from the GitHub repo backing a GHCR image."""
    url = f"https://api.github.com/repos/{repo}/releases?per_page=100"
    headers = {"Accept": "application/vnd.github+json"}
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        # Lifts the unauthenticated 60 req/hr rate limit; CI sets this.
        headers["Authorization"] = f"Bearer {token}"
    try:
        payload = fetch(url, headers)
    except (urllib.error.URLError, json.JSONDecodeError, OSError):
        return []
    if not isinstance(payload, list):
        return []
    return [release["tag_name"] for release in payload
            if not release.get("draft") and release.get("tag_name")]


def ghcr_tag_list(repo):
    """Paginated GHCR tag list, minus cosign artifacts."""
    token = fetch(f"https://ghcr.io/token?scope=repository:{repo}:pull")["token"]
    headers = {"Authorization": f"Bearer {token}"}
    url = f"https://ghcr.io/v2/{repo}/tags/list?n=100"
    tags = []
    for _ in range(GHCR_MAX_PAGES):
        payload, response_headers = fetch_with_headers(url, headers)
        tags.extend(tag for tag in (payload.get("tags") or [])
                    if not tag.startswith("sha256-"))
        link = response_headers.get("Link")
        if not link:
            break
        match = LINK_NEXT_RE.search(link)
        if not match:
            break
        url = urllib.parse.urljoin("https://ghcr.io", match.group("url"))
    return tags


def newest_comparable(tags, current_parsed):
    """Newest upstream tags sharing the current tag's prefix and suffix shape.

    Returns (same_major, newer_major), either of which may be None.

    The split matters because a major bump is rarely a tag swap — moving
    `postgres:16.15-alpine` to `18.6-alpine` needs a data migration, not an
    edit. So the same-major result is the actionable upgrade, and a newer
    major is reported separately as information.
    """
    prefix, current_core, suffix_label, _ = current_parsed
    current_major = current_core[0]
    same_major, newer_major = [], []
    for tag in tags:
        parsed = parse_tag(tag)
        if not parsed or parsed[0] != prefix or parsed[2] != suffix_label:
            continue
        major = parsed[1][0]
        if major == current_major:
            same_major.append((parsed, tag))
        elif major > current_major:
            newer_major.append((parsed, tag))
    newest = lambda group: (max(group, key=lambda item: (item[0][1], item[0][3]))
                            if group else None)
    return newest(same_major), newest(newer_major)


def collect_images():
    """Map each `image:tag` to the compose files that use it."""
    images = {}
    roots = sorted(Path("stacks").glob("*/compose.yaml"))
    if Path("compose.yaml").exists():
        roots.append(Path("compose.yaml"))
    for compose_file in roots:
        try:
            data = yaml.safe_load(compose_file.read_text())
        except yaml.YAMLError:
            continue
        if not isinstance(data, dict):
            continue
        for service in (data.get("services") or {}).values():
            if not isinstance(service, dict):
                continue
            image = service.get("image")
            if image:
                images.setdefault(image, []).append(str(compose_file))
    return images


def check(image):
    """Return (status, detail) for one image. Status: ok/outdated/skipped."""
    registry, repo, tag = split_image(image)
    if tag in FLOATING:
        return "skipped", "floating tag, pinned by pull_policy instead"
    current = parse_tag(tag)
    if current is None:
        return "skipped", f"tag {tag!r} has no comparable version"
    try:
        tags = ghcr_tags(repo) if registry == "ghcr.io" else docker_hub_tags(repo)
    except (urllib.error.URLError, KeyError, json.JSONDecodeError, OSError) as err:
        return "skipped", f"registry lookup failed ({type(err).__name__})"
    same_major, newer_major = newest_comparable(tags, current)
    if same_major is None and newer_major is None:
        return "skipped", "no upstream tags matched this tag's shape"
    if same_major is not None:
        parsed, newest_tag = same_major
        if (parsed[1], parsed[3]) > (current[1], current[3]):
            return "outdated", newest_tag
    if newer_major is not None:
        # Current within its own major, but upstream has moved on a major.
        # Reported, not recommended — a major bump usually needs a migration.
        return "major", newer_major[1]
    return "ok", tag


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--markdown", action="store_true",
                        help="emit a Markdown table for a CI job summary")
    args = parser.parse_args()

    images = collect_images()
    outdated, major, skipped, ok = [], [], [], []
    buckets = {"outdated": outdated, "major": major,
               "skipped": skipped, "ok": ok}
    for image in sorted(images):
        status, detail = check(image)
        buckets[status].append((image, detail, images[image]))

    if args.markdown:
        print("## Image freshness\n")
        print(f"Checked {len(images)} images — **{len(outdated)} outdated**, "
              f"{len(major)} with a newer major, {len(ok)} current, "
              f"{len(skipped)} skipped.\n")
        if outdated:
            print("### Outdated\n")
            print("| Image | Newest upstream | Used by |")
            print("| --- | --- | --- |")
            for image, newest, files in outdated:
                print(f"| `{image}` | `{newest}` | {', '.join(files)} |")
            print()
        if major:
            print("### Newer major available\n")
            print("Current within its own major. A major bump usually needs a "
                  "migration — review before changing the pin.\n")
            print("| Image | Newest major | Used by |")
            print("| --- | --- | --- |")
            for image, newest, files in major:
                print(f"| `{image}` | `{newest}` | {', '.join(files)} |")
            print()
        if skipped:
            print("<details><summary>Skipped "
                  f"({len(skipped)})</summary>\n")
            for image, reason, _ in skipped:
                print(f"- `{image}` — {reason}")
            print("\n</details>")
    else:
        for image, newest, files in outdated:
            print(f"OUTDATED {image} -> {newest} ({', '.join(files)})")
        for image, newest, files in major:
            print(f"MAJOR    {image} -> {newest} ({', '.join(files)})")
        for image, reason, _ in skipped:
            print(f"SKIPPED  {image} ({reason})")
        print(f"\n{len(outdated)} outdated, {len(major)} newer major, "
              f"{len(ok)} current, {len(skipped)} skipped, "
              f"{len(images)} total")

    # Always succeed: a stale upstream release is information, not a failure.
    return 0


if __name__ == "__main__":
    sys.exit(main())
