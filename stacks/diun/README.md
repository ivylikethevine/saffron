# Diun

Notifies via gotify when a newer tag of any running container's image is
published. Saffron pins every image tag, so nothing updates itself; diun
tells you when a pin is worth bumping and the change stays in git.

Requires the [gotify](../gotify/README.md) stack and an application token in
`.env` (see `.env.public`). Runs once a day; the first run only records what
is already deployed and sends nothing.

<https://github.com/crazy-max/diun>

<https://crazymax.dev/diun/>

<https://github.com/crazy-max/diun/pkgs/container/diun>

## Related Stacks

- **[gotify](../gotify/README.md)** — Receives the notifications

## Architecture Compatibility

![x64 Version](https://img.shields.io/docker/v/crazymax/diun/latest?arch=amd64&label=x64) ![Arm64 Version](https://img.shields.io/docker/v/crazymax/diun/latest?arch=arm64&label=arm64)

#### `compose.yaml`

[filename](compose.yaml ':include :type=code')
