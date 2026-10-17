# Saffron Roadmap

Potential improvements, upgrades, and nice-to-haves, roughly ordered by
impact vs. effort. This is a planning document, not a commitment — pick
items up as they become relevant.

## ✓ Completed (2026-08-16)

These have been implemented:

- **Pin image versions** — All floating `:latest`/`:develop`/`:nightly` tags pinned to specific releases (profilarr 2.1.0, byparr 3.0.4, prowlarr nightly-2.6.2.5548-ls10, homeassistant 2026.8.0). `pull_policy` flipped to `missing` for pinned services. See commit 532cba4.
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

## ✓ Completed (2026-10-17)

- **Routine pin bumps** from `check-image-freshness.py`, all 17 non-major
  ones in one batch.
- **Log rotation and `no-new-privileges`** on `base-settings` in
  `common.yaml.public` (10m × 3 json-file), repeated directly on the six
  services that don't extend it: bitmagnet's three, ustreamer, watchyourlan
  and dockge.
- **Homepage stack** on port 82 beside heimdall, with the docker socket
  mounted read-only for label discovery.
- **CI: `.env.public` completeness and `stacks/README.md` index checks.**
- **Consistency pass**: every floating tag pinned (bitmagnet, byparr,
  dockge), obsolete `version:` keys dropped, retired readarr swapped for
  bookshelf (data stays in `/containers/readarr`), stale bazarr docs
  removed, watchtower replaced by diun, healthchecks on every service with
  a verified binary, `/etc/localtime` as the one timezone source.
- **Template consolidation**: `restart`, `pull_policy`, hardening, log
  rotation, healthcheck timings and the timezone mount live in
  `base-settings` and every service extends it. The root compose and the
  two stacks that need the checkout path read it from `PWD`/`SAFFRON_DIR`
  instead of `/home/$USER/saffron`. The pre-commit hook is linked by the
  install script. The multi-arch CI job, which only ever checked ghcr images
  and skipped those unconditionally, and the Jekyll build of a docsify site
  are gone.
- **`homepage.*` labels on all 26 UI services**, grouped Media, Media
  Management, Indexing, Downloads, Home and Infrastructure; links use
  `HOMEPAGE_HOST`, passed down from dockge.
- **dozzle v10 → v11.** No config changes; everyone is signed out once.

## Now (high impact, low-to-medium effort)

- **Postgres major bump**, its own piece of work:
  - **postgres `16.15-alpine → 18.6-alpine`** for bitmagnet needs a
    `pg_dumpall` from the old container and a restore into the new one;
    confirm bitmagnet v0.10.1 supports 18 first.

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
- **One shared VPN stack.** torrent and bitmagnet each run their own
  gluetun. A single `vpn` stack with consumers on
  `network_mode: container:gluetun` halves credentials and config, at the
  cost of a cross-stack startup-order dependency.
- **ARM64 verification.** Nothing checks that pinned images publish an
  arm64 manifest. Only needed if Saffron runs on ARM hardware; the check
  belongs in `check-image-freshness.py`, which already talks to both
  registries.

## Nice-to-haves (low priority, quality-of-life)

- **`docker compose config` lint in the pre-commit hook**, not just CI —
  catches YAML mistakes before they're even committed, not just before
  merge.
- **Screenshots for the 9 newly-documented stacks.** backrest, bitmagnet,
  gotify, indexing, lidarr, navidrome, profilarr, slskd, and watchyourlan
  currently skip the "WebUI Dashboard" section since no screenshot exists
  in `resources/screenshots/` — cosmetic, but matches the pattern the rest
  of the wiki uses.

## Candidate services

- **Media**: Jellyfin (open alternative to Plex), Tautulli (Plex stats),
  Audiobookshelf, Unpackerr and Cleanuparr (arr queue hygiene), Recyclarr
  if profilarr proves heavy.
- **Ops**: Uptime Kuma (same author as Dockge), Beszel (lightweight host and
  container metrics), Scrutiny (disk SMART health, pairs with backrest).
- **Network and auth**: Caddy with Tinyauth or Authelia for the proxy and
  login items above, Pi-hole or AdGuard Home, Vaultwarden.
- **Photos**: Immich.

## Explicitly out of scope (for now)

- **Orchestration beyond Compose** (Kubernetes, Nomad, Swarm). Saffron's
  whole value proposition is "static YAML, no cluster to operate." Revisit
  only if running across multiple physical hosts becomes a real need.
- **Built-in image signing/verification.** Worth knowing about (see
  `SECURITY.md`) but adds real friction for a homelab; not worth doing
  until there's a specific threat this is defending against.
