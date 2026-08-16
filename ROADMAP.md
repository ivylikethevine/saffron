# Saffron Roadmap

Potential improvements, upgrades, and nice-to-haves, roughly ordered by
impact vs. effort. This is a planning document, not a commitment — pick
items up as they become relevant.

## Now (high impact, low-to-medium effort)

These fix real gaps found by auditing the current `stacks/` directory.

- **Pin image versions.** Nearly every stack runs `:latest`, `:develop`
  (prowlarr), or `:nightly` (lidarr, readarr). A bad upstream release breaks
  the stack with no warning and no easy rollback. Pin to a known-good tag per
  stack, and let `watchtower`/`pull_policy` handle *intentional* upgrades
  instead of every restart pulling whatever landed on `latest`.
- **Add healthchecks.** Only `bitmagnet-postgres` has one. Without
  healthchecks, `depends_on` can't actually wait for a dependency to be
  *ready* (e.g. profilarr's `parser` dependency, prowlarr before sonarr).
  Add basic HTTP/TCP healthchecks to the services other stacks depend on.
- **Add resource limits.** No stack sets `deploy.resources.limits`. A single
  runaway container (Plex transcode, bitmagnet indexing) can starve the
  whole host. Start with soft memory limits on the heavier services (plex,
  bitmagnet, homeassistant) and expand from there.
- **Reconcile `pull_policy: always` with pinned versions.** Once tags are
  pinned (above), `pull_policy: always` mostly just re-pulls the same digest
  on every start — harmless but pointless. Revisit whether it should stay
  `always` (fine for `:latest`-style tags you intentionally keep floating)
  or move to `missing`/`if_not_present` for pinned stacks.

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
- **Multi-arch verification.** READMEs show ARM64 badges for several
  images, but nothing in CI actually builds/tests on ARM. Only worth doing
  if Saffron is actually being run on ARM hardware (Raspberry Pi, etc.).
- **Pre-commit hook auto-install.** `resources/pre-commit` (webp
  conversion) has to be manually copied into `.git/hooks/`. A one-line
  step in `install-saffron.sh` (`ln -sf` or `git config core.hooksPath`)
  would make it opt-out instead of easy-to-forget.
- **Network topology diagram.** The VPN-sharing relationships (bitmagnet ↔
  slskd via one gluetun; torrent's own gluetun; `servarr_bridge` linking
  servarr/indexing/torrent) are only describable in prose right now. A
  small diagram in `CLAUDE.md` would make the bridge/VPN routing much
  faster to reason about when adding a new stack.

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
