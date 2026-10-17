# instadroid

Turns an Instagram following feed into RSS by scrolling the app on an Android container.

<https://github.com/ivylikethevine/instadroid>

<https://github.com/ivylikethevine/instadroid/pkgs/container/instadroid>

- **redroid** — the Android device (privileged); ADB on `127.0.0.1:5555`
- **instadroid** — the scraper and the feed server, on host networking

Both use `restart: "no"`, so start the stack from dockge when wanted. Copy `.env.public` to `.env` and set the Instagram account. The app runs as uid 1000, so create its data directories first:

```bash
mkdir -p /containers/instadroid/{android,db,media,debug,apk}
chown 1000:1000 /containers/instadroid/{db,media,debug,apk}
```

The feed server defaults to `127.0.0.1:8000`, which the torrent stack's gluetun control server also publishes; set `FEED_PORT` in `.env` when both run on one host.

## Related Stacks

- **[freshrss](../freshrss/README.md)** — Feed reader for the generated feeds

## Architecture Compatibility

x64 only (the redroid image and the bundled `apkeep` are x64 builds).

#### `compose.yaml`

[filename](compose.yaml ':include :type=code')

#### `.env.public`

[filename](.env.public ':include :type=code')
