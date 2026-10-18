# sharerr

Shares the media library with friends: a private tracker, a Torznab feed and `.torrent` files built from Sonarr/Radarr content tagged `sharerr`, seeded by qBittorrent. Experimental until v1.0.0.

<https://github.com/ivylikethevine/sharerr-rs>

<https://github.com/ivylikethevine/sharerr-rs/pkgs/container/sharerr-rs>

sharerr joins the [torrent](../torrent/README.md) stack's gluetun namespace (`network_mode: container:qbittorrentvpn`), so it announces from the same tunnel address as qBittorrent's swarm traffic. Start the torrent stack first, and restart sharerr whenever `qbittorrentvpn` is recreated.

## Setup

1. Create the config and data directories (the image runs as uid 1000) and copy the config template:

   ```bash
   mkdir -p /containers/sharerr/config /containers/sharerr/data
   cp stacks/sharerr/sharerr.toml.public /containers/sharerr/config/sharerr.toml
   chown -R 1000:1000 /containers/sharerr
   ```

   Set `tracker.advertised_host` there.

2. In this stack's `.env`, set `SHARERR_MASTER_KEY` (`openssl rand -base64 32`) and `MEDIA_PATH` (your `DATA_DIR`).

3. In the torrent stack's `.env`:
   - `LAN_SUBNETS=172.16.0.0/12`, so sharerr can reach Sonarr and Radarr through `host.docker.internal`. It must not overlap the tunnel's `ADDRESSES`.
   - Add `8477` to `PORTS`, so friends reach sharerr through the tunnel. A provider that forwards a single port can only give it to qBittorrent (`TRACKER_PORT=8999`) or sharerr (`TRACKER_PORT=8477`).

4. Give sharerr a key for gluetun's control server. Generate one with `docker run --rm qmcgaw/gluetun:v3.41.3 genkey` and add a role for it to `/containers/gluetun/config.toml`:

   ```toml
   [[roles]]
   name = "sharerr"
   routes = ["GET /v1/publicip/ip", "GET /v1/openvpn/portforwarded", "GET /v1/portforward"]
   auth = "apikey"
   apikey = "<the key>"
   ```

5. Recreate the torrent stack, start this one, then store the credentials in the vault (or through Settings in the web UI on port 8477):

   ```bash
   printf %s "$KEY" | docker exec -i sharerr sharerr vault set gluetun.api_key
   printf %s "$KEY" | docker exec -i sharerr sharerr vault set qbittorrent.api_key
   printf %s "$KEY" | docker exec -i sharerr sharerr vault set sonarr.api_key
   printf %s "$KEY" | docker exec -i sharerr sharerr vault set radarr.api_key
   ```

6. Check credentials, reachability and the path mapping with `docker exec sharerr sharerr doctor`.

Port 8477 serves the web UI as well as the tracker, so forwarding it puts the login page on the internet without TLS. See sharerr's [deploy guide](https://github.com/ivylikethevine/sharerr-rs/blob/main/docker/deploy/README.md#one-port-several-audiences) for a reverse proxy or a tracker-only listener.

## Related Stacks

- **[torrent](../torrent/README.md)** — qBittorrent and the gluetun namespace sharerr joins
- **[servarr](../servarr/README.md)** — Sonarr and Radarr, whose tagged content is shared

## Architecture Compatibility

x64 and arm64 (multi-arch image on ghcr.io).

#### `compose.yaml`

[filename](compose.yaml ':include :type=code')

#### `sharerr.toml.public`

[filename](sharerr.toml.public ':include :type=code')

#### `.env.public`

[filename](.env.public ':include :type=code')
