# Next

Candidate changes not yet on [ROADMAP.md](ROADMAP.md). Grouped by kind, not
priority.

## Inconsistencies

Done, pending review:

- Pinned bitmagnet `v0.10.1`, byparr `3.0.4` (upstream never published a
  `v3.0.3` image tag; the `v`-less tag is the real one) and dockge `1.5.0`.
- Dropped the obsolete `version:` key from every compose file; CI now
  rejects it instead of requiring it.
- Replaced readarr with bookshelf `softcover-v0.4.21.182`. The volume stays
  at `/containers/readarr`, so existing data is used in place.
- Removed bazarr from the docs; it left the compose file in commit 5427722.
- `stacks/README.md` now says seerr. The seerr volume stays at
  `/containers/overseerr` so existing data is untouched.
- `restart: unless-stopped` on every stack service (dockge stays `always`).
- Every service mounts `/etc/localtime:ro`, including the ones that don't
  extend common.yaml; the hardcoded `TZ=America/Los_Angeles` vars in gotify,
  backrest and watchyourlan are gone.
- Healthchecks on 17 more services, each using a binary verified in the
  upstream Dockerfile. Inherited from the image: esphome, gotify, byparr,
  slskd, profilarr, dockge, gluetun. Still none: ustreamer (buster-slim, no
  curl or wget), portcheck, docsify, diun (no HTTP endpoint).
- Watchtower replaced by diun `4.33.0`: with every tag pinned, watchtower
  updated nothing. Diun watches each image's repo for newer tags and posts
  to gotify through `host.docker.internal`; the token goes in
  `stacks/diun/.env`.

## Simplifications

- **One shared VPN stack.** torrent and bitmagnet each run their own
  gluetun. A single `vpn` stack with consumers on
  `network_mode: container:gluetun` halves credentials and config, at the
  cost of a cross-stack startup-order dependency.
- **Root compose hardcodes `/home/$USER/saffron`.** Have
  `install-saffron.sh` write the real path into a `.env` beside it.
- Done: `no-new-privileges` and 10m × 3 log rotation on `base-settings`,
  repeated on the six services that don't extend it.
- Done: homepage stack on port 82 beside heimdall, with `homepage.*` labels
  on every UI service.

## Related services

- **Media**: Jellyfin (open alternative to Plex), Tautulli (Plex stats),
  Audiobookshelf, Unpackerr and Cleanuparr (arr queue hygiene), Recyclarr
  if profilarr proves heavy.
- **Ops**: Uptime Kuma (same author as Dockge), Beszel (lightweight host and
  container metrics), Scrutiny (disk SMART health, pairs with backrest).
- **Network and auth**: Caddy with Tinyauth or Authelia for the proxy and
  login roadmap items, Pi-hole or AdGuard Home, Vaultwarden.
- **Photos**: Immich.

## Upgrades pending

- Postgres 16 to 18 for bitmagnet: dump and restore, not a tag edit.
