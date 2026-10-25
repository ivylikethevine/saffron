# Docker Socket Proxy

Read-only Docker API on port 2375, so a [homepage](../homepage/README.md) on
another host can discover this host's containers by their `homepage.*`
labels. Only container listing is allowed; `POST` and every other endpoint
are refused. Anyone on the LAN can still list containers and their labels, so
run it only on a trusted network.

On the host running homepage, add this host to
`/containers/homepage/docker.yaml`:

```yaml
saffron:
  socket: /var/run/docker.sock
media:
  host: media.local
  port: 2375
```

<https://github.com/linuxserver/docker-socket-proxy>

<https://docs.linuxserver.io/images/docker-socket-proxy/>

## Related Stacks

- **[homepage](../homepage/README.md)** — Reads the proxy

## Architecture Compatibility

![x64 Version](https://img.shields.io/docker/v/linuxserver/socket-proxy/latest?arch=amd64&label=x64) ![Arm64 Version](https://img.shields.io/docker/v/linuxserver/socket-proxy/latest?arch=arm64&label=arm64)

#### `compose.yaml`

[filename](compose.yaml ':include :type=code')
