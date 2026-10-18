# RSSHub

Generates RSS feeds for sites that don't publish one, on port 1200.

<https://docs.rsshub.app/>

<https://github.com/DIYgod/RSSHub>

<https://hub.docker.com/r/diygod/rsshub>

- **rsshub** — the feed server
- **rsshub-browserless** — headless Chrome for routes that need JavaScript rendering; optional
- **rsshub-redis** — response cache

## Related Stacks

- **[freshrss](../freshrss/README.md)** — Feed reader to subscribe to the generated feeds

## Architecture Compatibility

![x64 Version](https://img.shields.io/docker/v/diygod/rsshub/latest?arch=amd64&label=x64) ![arm64 Version](https://img.shields.io/docker/v/diygod/rsshub/latest?arch=arm64&label=arm64)

#### `compose.yaml`

[filename](compose.yaml ':include :type=code')
