# Roadmap

Potential improvements, upgrades, and nice-to-haves, ranked by impact against
effort. This is a planning document, not a commitment — pick items up as they
become relevant. Sizes: S an hour or two, M a session, L more.

## Where it stands

As of 2026-11-17, branch `dev`.

- bitmagnet's database is still `postgres:16.15-alpine` (1).
- 21 stacks have no "WebUI Dashboard" section (8): the 20 listed there, plus
  docsify, added since.
- Not run for this update: `compose-validate.yml`, `image-freshness.yml`, or
  any stack.
- Open question: whether bitmagnet v0.10.1 supports Postgres 18 (1).

## Order of work

- 1, the Postgres bump, its own piece of work.
- 4, the CI smoke test, before the larger changes it would guard.
- 2 with 3: the proxy first, then auth at it.
- Later items as they become relevant.

## Now

### 1. Postgres major bump (M)

postgres `16.15-alpine → 18.6-alpine` for bitmagnet needs a `pg_dumpall` from
the old container and a restore into the new one; confirm bitmagnet v0.10.1
supports 18 first.

### 2. Reverse proxy and TLS (L)

Nothing in the repo terminates TLS or provides a single entry point; every
service is its own `host:port`. A `traefik` or `caddy` stack with automatic
Let's Encrypt (or self-signed for pure-LAN use) would let services be reached
at `sonarr.saffron.local` instead of `:8989`, and is the prerequisite for
safely exposing anything beyond the LAN.

### 3. Auth in front of unauthenticated UIs (M)

Dockge, Dozzle, and several other UIs have no login by default — fine for a
single trusted LAN, risky the moment the host is reachable from anywhere else
(guest wifi, VPN clients, etc.). Pair with 2: forward-auth or basic-auth at the
proxy layer covers everything at once instead of per-service.

### 4. Smoke-test the CI workflow, not just syntax (M)

`compose-validate.yml` checks compose syntax, READMEs and the stack index,
`.env.public` completeness and `version:` keys — it never actually starts a
container. A follow-up job that spins up one or two low-risk stacks
(`docker compose up -d && curl healthcheck`) would catch breakage the static
checks can't.

## On hold

Nothing waiting.

## Later

### 5. Backup restore drills (M)

`backrest` is documented for backups, but nothing verifies a restore actually
works. A periodic (manual or scripted) "restore into a scratch dir and diff"
check would turn "we have backups" into "we know the backups work."

### 6. One shared VPN stack (M)

torrent and bitmagnet each run their own gluetun; sharerr already rides
torrent's (`container:qbittorrentvpn`) and slskd rides bitmagnet's
(`container:bitmagnet-gluetun`), so cross-stack startup order is already a
dependency. A single `vpn` stack that every consumer joins with
`network_mode: container:gluetun` halves credentials and config.

### 7. ARM64 verification (S)

Nothing checks that pinned images publish an arm64 manifest. Only needed if
Saffron runs on ARM hardware; the check belongs in `check-image-freshness.py`,
which already talks to both registries.

### 8. Screenshots for the stacks without one (S)

backrest, bitmagnet, dapsync, degoog, diun, docsify, esphome, freshrss, gotify,
homepage, indexing, instadroid, lan-orangutan, lidarr, navidrome, profilarr,
rsshub, sharerr, slskd, ustreamer and watchyourlan skip the "WebUI Dashboard"
section — cosmetic, but matches the pattern the rest of the wiki uses. Three
are already in `resources/screenshots/` but sit in the wrong README or none:
`prowlarr.webp` is in torrent's (belongs in indexing), `lidarr.webp` in
servarr's (belongs in lidarr), and `navidrome.webp` is unused. plex's README
links `plex.webp`, which doesn't exist.

### 9. Candidate services

- **Media**: Jellyfin (open alternative to Plex), Tautulli (Plex stats),
  Audiobookshelf, Unpackerr and Cleanuparr (arr queue hygiene), Recyclarr if
  profilarr proves heavy.
- **Ops**: Uptime Kuma (same author as Dockge), Beszel (lightweight host and
  container metrics), Scrutiny (disk SMART health, pairs with backrest).
- **Network and auth**: Caddy with Tinyauth or Authelia for 2 and 3, Pi-hole
  or AdGuard Home, Vaultwarden.
- **Photos**: Immich.

## Decisions

Out of scope, for now:

- **Orchestration beyond Compose** (Kubernetes, Nomad, Swarm). Saffron's whole
  value proposition is "static YAML, no cluster to operate." Revisit only if
  running across multiple physical hosts becomes a real need.
- **Built-in image signing/verification.** Worth knowing about but adds real
  friction for a homelab; not worth doing until there's a specific threat this
  is defending against.
- **Secrets management beyond `.env`** (git-crypt, a secrets store), decided
  2026-10-25. The `.env.public` → gitignored `.env` model covers a
  single-owner homelab.
- **Git hooks**, a `docker compose config` lint and the webp conversion the
  install script once linked included, decided 2026-10-25. CI already runs the
  lint on every push; lints are run by hand before committing, and a
  screenshot is converted by hand (`cwebp -q 50 IN -o OUT.webp`).

## Done

- 2026-08-16: image versions pinned, `pull_policy: missing` for pinned
  services (`532cba4`).
- 2026-08-16: healthchecks on qbittorrent, and portcheck's `depends_on` waits
  on `service_healthy`.
- 2026-08-16: memory limits on 24 services across 13 stacks.
- 2026-08-16: the network topology diagram, now `resources/generate-topology.py`
  (`700d2fe`).
- 2026-08-16: a multi-arch CI job (`ebf07f5`), removed 2026-10-17; 7 replaces
  it.
- 2026-08-16: Dependabot for GitHub Actions, and `image-freshness.yml` with
  `resources/check-image-freshness.py` for the compose pins Dependabot cannot
  watch.
- 2026-10-17: all 17 non-major pin bumps in one batch.
- 2026-10-17: log rotation and `no-new-privileges` on `base-settings`.
- 2026-10-17: the homepage stack on port 82.
- 2026-10-17: CI checks for `.env.public` completeness and the
  `stacks/README.md` index.
- 2026-10-17: a consistency pass: floating tags pinned, `version:` keys
  dropped, readarr swapped for bookshelf, watchtower for diun, healthchecks on
  every service with a verified binary, `/etc/localtime` as the one timezone
  source.
- 2026-10-17: template consolidation into `base-settings`, with the checkout
  path read from `PWD`/`SAFFRON_DIR`.
- 2026-10-17: `homepage.*` labels on all 26 UI services.
- 2026-10-17: dozzle v10 → v11.
- 2026-10-25: homepage discovery through a read-only socket proxy.
