# LAN Orangutan

Lightweight network scanner with persistent device labels, on port 291.

<https://github.com/291-Group/LAN-Orangutan>

<https://github.com/291-Group/LAN-Orangutan/pkgs/container/lan-orangutan>

Runs in host network mode with `NET_RAW`/`NET_ADMIN`, so it scans the real LAN; Linux hosts only. The first visit asks for a dashboard password; to reset it, delete `/containers/lan-orangutan/auth` and restart.

## Related Stacks

- **[watchyourlan](../watchyourlan/README.md)** — LAN device monitor (overlapping purpose)

## Architecture Compatibility

![x64 Version](https://img.shields.io/docker/v/291group/lan-orangutan/latest?arch=amd64&label=x64) ![arm64 Version](https://img.shields.io/docker/v/291group/lan-orangutan/latest?arch=arm64&label=arm64)

#### `compose.yaml`

[filename](compose.yaml ':include :type=code')
