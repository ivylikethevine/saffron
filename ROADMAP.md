# Saffron Roadmap

Potential improvements, upgrades, and nice-to-haves, roughly ordered by
impact vs. effort. This is a planning document, not a commitment — pick
items up as they become relevant.

## ✓ Completed (2026-08-16)

These have been implemented:

- **Pin image versions** — All floating `:latest`/`:develop`/`:nightly` tags pinned to specific releases (profilarr 2.1.0, byparr v3.0.3, prowlarr nightly-2.6.2.5548-ls10, homeassistant 2026.8.0). `pull_policy` flipped to `missing` for pinned services. See commit 532cba4.
- **Add healthchecks** — Added HTTP healthcheck to qbittorrent (wget on port 8080). Converted portcheck's `depends_on` from list to mapping form with `condition: service_healthy`.
- **Add resource limits** — Added `deploy.resources.limits.memory` to 24 services across 13 stacks (512M for medium-weight, 256M for lightweight UI, 1G for browser-backed, 128M for portcheck). Memory-only per initial scope.
- **Reconcile `pull_policy`** — All pinned services now use `pull_policy: missing`; floating-tag services (portcheck) remain `always`.
- **Network topology diagram** — Added Mermaid diagram to CLAUDE.md showing servarr_bridge, VPN-routed services (bitmagnet-gluetun, qbittorrentvpn), and host-mode services. Created `resources/generate-topology.py` to regenerate diagram programmatically. See commit 700d2fe.
- **Multi-arch verification in CI** — Added `multi-arch-verify` job to `.github/workflows/compose-validate.yml` that checks ARM64 image availability for linuxserver, qmcgaw, and GHCR images via Docker Hub registry API. Verifies all multi-arch images support both linux/amd64 and linux/arm64v8. See commit ebf07f5.

- **Automated dependency updates** — Added `.github/dependabot.yml`
  (`github-actions` ecosystem, monthly, grouped) plus
  `.github/workflows/image-freshness.yml` and
  `resources/check-image-freshness.py`, which compare every pinned `image:`
  tag against upstream and report into the CI job summary. Runs monthly and
  on demand; always exits 0, since a stale upstream release is information,
  not a build failure.

  Two constraints worth remembering, both learned the hard way:

  1. **Dependabot cannot watch these files.** Its `docker` ecosystem only
     matches `Dockerfile` and `docker-compose.yml`/`.yaml`, and every stack
     here uses `compose.yaml`. A `docker` block would not error — it would
     just silently never open a PR. Hence the custom checker.
  2. **GHCR's `tags/list` returns tags oldest-first.** Page 1 of
     home-assistant is 2021 dev builds; the current release sits thousands
     of pages deep, so forward pagination finds old tags, not new ones. The
     script uses the GitHub releases API (newest-first) _merged_ with a
     bounded tag-list walk, because the releases API alone lags the registry
     — bitmagnet ships a `v0.10.1` image tag with no matching release.

  Tag comparison is shape-aware (`nightly-…-ls10` is only compared against
  the same shape) and major-version bumps are reported separately from
  routine ones, so a Postgres 16 → 18 jump is never presented as a pin edit.

## Now (high impact, low-to-medium effort)

Real gaps for consideration:

- **Bump the images the freshness check found stale.** First run of
  `resources/check-image-freshness.py` surfaced four: bitmagnet
  `v0.9.5 → v0.10.1`, home-assistant `2026.8.0 → 2026.8.2`, seerr
  `v3.0.1 → v3.4.1`, and postgres `16.15-alpine → 18.6-alpine`. The first
  three are routine pin edits. **Postgres is not** — 16 → 18 needs a data
  migration for the bitmagnet database, so treat it as its own piece of
  work rather than a tag swap.

- **Log rotation defaults.** `grep -c "logging:" -r stacks/` returns zero
  matches across all 21 stacks, so every container runs on Docker's default
  json-file driver with no size cap — a slow-motion disk-fill on a box that
  stays up for months. Add `logging.options.max-size` / `max-file` once to
  `base-settings` in `stacks/common.yaml.public` so stacks inherit it
  through the existing `extends` pattern instead of repeating it 24 times.
  Known limit: not every service extends `common.yaml` — host-mode and
  VPN-routed services (plex, homeassistant, watchyourlan, the gluetun
  containers) need checking individually, so this is one edit plus an
  audit, not a pure one-liner.

## Next (real gaps, more design work)

- **Reverse proxy + TLS.** Nothing in the repo terminates TLS or provides a
  single entry point; every service is its own `host:port`. A `traefik` or
  `caddy` stack with automatic Let's Encrypt (or self-signed for pure-LAN
  use) would let services be reached at `sonarr.saffron.local` instead of
  `:8989`, and is the prerequisite for safely exposing anything beyond the
  LAN.
- **Auth in front of unauthenticated UIs.** Dockge, Dozzle, and several
  other UIs have no login by default — fine for a single trusted LAN, risky
  the moment the host is reachable from anywhere else (guest wifi, VPN
  clients, etc.). Pair with the reverse-proxy work above: forward-auth or
  basic-auth at the proxy layer covers everything at once instead of
  per-service.
- **Secrets management beyond `.env`.** Current model (`.env.public`
  template → user-created `.env`, gitignored) is fine for solo use. If this
  ever becomes a team/multi-host setup, revisit git-crypt or a small
  secrets store rather than hand-copying `.env` files during migration (see
  `UPGRADE.md`).
- **Smoke-test the CI workflow, not just syntax.** `compose-validate.yml`
  currently checks YAML validity, README presence, and a few string
  patterns — never actually starts a container. A follow-up job that spins
  up one or two low-risk stacks (`docker compose up -d && curl healthcheck`)
  would catch breakage the static checks can't.

## Later (bigger investments, optional)

- **Backup restore drills.** `backrest` is documented for backups, but
  nothing verifies a restore actually works. A periodic (manual or
  scripted) "restore into a scratch dir and diff" check would turn "we have
  backups" into "we know the backups work."
- **Pre-commit hook auto-install.** `resources/pre-commit` (webp
  conversion) has to be manually copied into `.git/hooks/`. A one-line
  step in `install-saffron.sh` (`ln -sf` or `git config core.hooksPath`)
  would make it opt-out instead of easy-to-forget.
- **Smoke-test CI builds.** The `multi-arch-verify` job now checks ARM64
  availability, but doesn't actually build containers on ARM. A follow-up
  could add experimental `runs-on: ubuntu-latest-arm64` jobs to catch ARM-
  specific breakage, though this is expensive and only needed if Saffron
  actually runs on ARM hardware (Raspberry Pi, etc.).

## Nice-to-haves (low priority, quality-of-life)

- **Heimdall/dashboard auto-population.** Heimdall is included but each
  service still has to be added by hand; a documented "add your new stack
  here too" step (or a script that reads `stacks/*/compose.yaml` ports and
  proposes entries) would keep the dashboard from drifting out of sync the
  way `stacks/README.md` did.
- **`docker compose config` lint in the pre-commit hook**, not just CI —
  catches YAML mistakes before they're even committed, not just before
  merge.
- **Per-stack `.env.public` completeness check in CI.** Right now CI
  checks for `version:`, `pull_policy:`, and README presence; it could also
  flag any `${VAR}` used in a `compose.yaml` that has no corresponding line
  in that stack's `.env.public`, catching the exact gap that bitmagnet and
  speedtest-tracker had before this round of fixes.
- **`stacks/README.md` drift check in CI.** CI checks that each stack
  directory _has_ a README, but never that the index in `stacks/README.md`
  actually lists every stack — CLAUDE.md claims "must be kept in sync (CI
  checks this)", which is not currently true. Extend the existing "Check
  for required documentation" step in `compose-validate.yml`: it already
  loops `stacks/*/` with the right `README.md`/`common.yaml.public` skip
  logic, so it just needs a second assertion per directory.
- **Screenshots for the 9 newly-documented stacks.** backrest, bitmagnet,
  gotify, indexing, lidarr, navidrome, profilarr, slskd, and watchyourlan
  currently skip the "WebUI Dashboard" section since no screenshot exists
  in `resources/screenshots/` — cosmetic, but matches the pattern the rest
  of the wiki uses.

## Explicitly out of scope (for now)

- **Orchestration beyond Compose** (Kubernetes, Nomad, Swarm). Saffron's
  whole value proposition is "static YAML, no cluster to operate." Revisit
  only if running across multiple physical hosts becomes a real need.
- **Built-in image signing/verification.** Worth knowing about (see
  `SECURITY.md`) but adds real friction for a homelab; not worth doing
  until there's a specific threat this is defending against.
