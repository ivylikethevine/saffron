# Homepage

Dashboard that discovers services from Docker labels, so a stack adds itself
by carrying `homepage.*` labels instead of being entered by hand. Runs on
port 82 beside [heimdall](../heimdall/README.md) on port 80.

Enable discovery once by adding the socket to `/containers/homepage/docker.yaml`:

```yaml
saffron:
  socket: /var/run/docker.sock
```

Every service carries `homepage.*` labels. Their links use `HOMEPAGE_HOST`,
which dockge passes down from the root `compose.yaml` (default `localhost`);
set it to the name you browse from, e.g. `HOMEPAGE_HOST=hostname.local`, in
the shell that starts dockge.

<https://github.com/gethomepage/homepage>

<https://gethomepage.dev/>

<https://github.com/gethomepage/homepage/pkgs/container/homepage>

## Related Stacks

- **[heimdall](../heimdall/README.md)** — Hand-curated dashboard on port 80

## Architecture Compatibility

![x64 Version](https://img.shields.io/docker/v/gethomepage/homepage/latest?arch=amd64&label=x64) ![Arm64 Version](https://img.shields.io/docker/v/gethomepage/homepage/latest?arch=arm64&label=arm64)

#### `compose.yaml`

[filename](compose.yaml ':include :type=code')
