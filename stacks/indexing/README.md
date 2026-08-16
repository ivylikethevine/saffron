# Indexing

Search aggregation services for the *arr stack.

## Related Stacks

- **[servarr](../servarr/README.md)** — Sonarr, Radarr, Readarr, Bazarr (uses prowlarr for searches)
- **[torrent](../torrent/README.md)** — qBittorrent client for automated downloads
- **[profilarr](../profilarr/README.md)** — Quality profile management for the *arr apps

# Prowlarr

Search aggregator.

<https://wiki.servarr.com/en/prowlarr>

<https://github.com/Prowlarr/Prowlarr>

<https://github.com/linuxserver/docker-prowlarr>

<https://docs.linuxserver.io/images/docker-prowlarr/>

<https://hub.docker.com/r/linuxserver/prowlarr>

## Architecture Compatibility

![x64 Version](https://img.shields.io/docker/v/linuxserver/prowlarr/latest?arch=amd64&label=x64) ![arm64 Version](https://img.shields.io/docker/v/linuxserver/prowlarr/latest?arch=arm64&label=arm64)

# Flaresolverr

Search proxy (required for some search engines & reduces error rates in general).

<https://github.com/flaresolverr/flaresolverr>

<https://hub.docker.com/r/flaresolverr/flaresolverr/>

## Architecture Compatibility

![x64 Version](https://img.shields.io/docker/v/flaresolverr/flaresolverr/latest?arch=amd64&label=x64) ![arm64 Version](https://img.shields.io/docker/v/flaresolverr/flaresolverr/latest?arch=arm64&label=arm64)

# Byparr

Indexer proxy for the *arr apps.

<https://github.com/thephaseless/byparr>

<https://hub.docker.com/r/ghcr.io/thephaseless/byparr>

## Architecture Compatibility

x64 only (GHCR-hosted image)

#### `compose.yaml`

[filename](compose.yaml ':include :type=code')
