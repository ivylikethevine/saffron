# Jellyfin

TV/movie streaming.

<https://github.com/jellyfin/jellyfin>

<https://docs.linuxserver.io/images/docker-jellyfin/>

## Architecture Compatibility

![x64 Version](https://img.shields.io/docker/v/linuxserver/jellyfin/latest?arch=amd64&label=x64) ![Arm64 Version](https://img.shields.io/docker/v/linuxserver/jellyfin/latest?arch=arm64&label=arm64)

### WebUI Dashboard

![Jellyfin UI](../../resources/screenshots/jellyfin.webp)

#### This container implements the Intel Quicksync hardware encoding, but others are configurable as per [jellyfin acceleration](https://docs.linuxserver.io/images/docker-jellyfin/#hardware-acceleration-enhancements) and [linuxserver's docker mods](https://mods.linuxserver.io/?mod=jellyfin).

# Jellyseerr

TV/movie requests.

<https://github.com/Fallenbagel/jellyseerr>

<https://hub.docker.com/r/fallenbagel/jellyseerr>

## Architecture Compatibility

![x64 Version](https://img.shields.io/docker/v/fallenbagel/jellyseerr/latest?arch=amd64&label=x64) ![Arm64 Version](https://img.shields.io/docker/v/fallenbagel/jellyseerr/latest?arch=arm64&label=arm64)

### WebUI Dashboard

![Jellyseerr UI](../../resources/screenshots/jellyseerr.webp)

#### Login Issues

##### If you can't login to jellyseer, make sure that your containers have a bridge network between them, and that your jellyfin password is long enough.

#### `compose.yaml`

[filename](compose.yaml ':include :type=code')