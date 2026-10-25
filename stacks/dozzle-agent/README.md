# Dozzle Agent

Serves this host's container logs on port 7007 to a
[dozzle](../dozzle/README.md) running on another host. On that host, set
`DOZZLE_REMOTE_AGENT=media.local:7007` in `stacks/dozzle/.env`; this host's
containers then appear beside the local ones.

<https://dozzle.dev/guide/agent>

<https://github.com/amir20/dozzle>

## Related Stacks

- **[dozzle](../dozzle/README.md)** — The UI that reads the agent

## Architecture Compatibility

![x64](https://img.shields.io/docker/v/amir20/dozzle/latest?arch=amd64&label=x64) ![arm64](https://img.shields.io/docker/v/amir20/dozzle/latest?arch=arm64&label=arm64)

#### `compose.yaml`

[filename](compose.yaml ':include :type=code')
