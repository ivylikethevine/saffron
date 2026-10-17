# FreshRSS

Self-hosted RSS and Atom feed aggregator, on port 8084.

<https://freshrss.org/>

<https://github.com/FreshRSS/FreshRSS>

<https://hub.docker.com/r/freshrss/freshrss>

Feeds refresh at minutes 3 and 33 of each hour (`CRON_MIN`). FreshRSS 1.30+ refuses to fetch feeds on internal hosts; to subscribe to one (an [rsshub](../rsshub/README.md) or [instadroid](../instadroid/README.md) feed on this LAN), add `INTERNAL_HOST_ALLOWLIST` with that `host:port` to the environment.

## Related Stacks

- **[rsshub](../rsshub/README.md)** — Generates feeds for sites that have none
- **[instadroid](../instadroid/README.md)** — Instagram to RSS

## Architecture Compatibility

![x64 Version](https://img.shields.io/docker/v/freshrss/freshrss/latest?arch=amd64&label=x64) ![arm64 Version](https://img.shields.io/docker/v/freshrss/freshrss/latest?arch=arm64&label=arm64)

#### `compose.yaml`

[filename](compose.yaml ':include :type=code')
