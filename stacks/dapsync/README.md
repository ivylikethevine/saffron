# DAPSync

Syncs curated music (starred, playlists, artists, genres) from Navidrome to a digital audio player's SD card.

<https://hub.docker.com/r/joshuaswilcox/dapsync>

Tracks are downloaded through Navidrome's API, so the stack needs no `/data` mount. Set the Navidrome account in `.env` (see `.env.public`) and mount the SD card on the host at `DAP_MOUNT` (default `/mnt/dap`).

## Related Stacks

- **[navidrome](../navidrome/README.md)** — Music server dapsync pulls from

## Architecture Compatibility

![x64 Version](https://img.shields.io/docker/v/joshuaswilcox/dapsync/latest?arch=amd64&label=x64)

`latest` is published for x64 only.

#### `compose.yaml`

[filename](compose.yaml ':include :type=code')

#### `.env.public`

[filename](.env.public ':include :type=code')
