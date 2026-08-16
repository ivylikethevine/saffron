# Saffron Stacks & Services

## List of Stacks & Services

[Stacks](stacks/README.md) rely on a customized [common.yaml.public](common.yaml.public) for correct permissions, time zones, and data directory mounts.

\*\* Names are lowercased per dockge stack naming requirements

- &#x2705; [backrest](stacks/backrest/README.md) - Web UI for restic backups.

- &#x2705; [bitmagnet](stacks/bitmagnet/README.md) - Self-hosted DHT crawler and torrent indexer, VPN-routed via gluetun.

- &#x2705; [docsify](stacks/docsify/README.md) - Web UI to view this repo's `README.md`'s as a wiki reflecting local edits. See the [public](https://ivylikethevine.github.io/saffron) instance or visit <http://hostname.local:5001> (if the container is running).

- &#x2705; [dockge](dockge.md) - Web UI to manage docker compose files (integral to `saffron`).

- &#x2705; [dozzle](stacks/dozzle/README.md) - Web UI to live docker container logs.

- &#x2705; [esphome](stacks/esphome/README.md) - Easily create & manage esp32-based IoT devices, such as temp. sensors.

- &#x2705; [gotify](stacks/gotify/README.md) - Simple self-hosted push notification server.

- &#x2705; [heimdall](stacks/heimdall/README.md) - Easy to use home page.

- &#x2705; [homeassistant](stacks/homeassistant/README.md) - Smart home automation.

- &#128994; [indexing](stacks/indexing/README.md) - Search aggregation services.

  - &#x2705; prowlarr - Search aggregator.

  - &#x2705; flaresolverr - Search proxy (required for some search engines & reduces error rates in general).

  - &#x2705; byparr - Indexer proxy.

- &#x2705; [lidarr](stacks/lidarr/README.md) - Music library manager.

- &#x2705; [navidrome](stacks/navidrome/README.md) - Music streaming service.

- &#x2705; [octoprint](stacks/octoprint/README.md) - 3D printer automation and monitoring.

- &#x2705; [plex](stacks/plex/README.md) - Fully featured media player/environment with many smart TV integrations.

  - &#x2705; overseerr - TV/movie requests.

- &#x2705; [profilarr](stacks/profilarr/README.md) - Quality profile and custom format sync for the *arr apps.

- &#128994; [servarr](stacks/servarr/README.md) - Media library systems.

  - &#x2705; sonarr - TV library manager.

  - &#x2705; radarr - Movie library manager.

  - &#x2705; readarr - Ebook library manager.

  - &#x2705; bazarr - Subtitle management/requests for sonarr/radarr.

- &#x2705; [slskd](stacks/slskd/README.md) - Soulseek client, VPN-routed via bitmagnet's gluetun.

- &#x2705; [speedtest-tracker](stacks/speedtest-tracker/README.md) - Internet speed monitoring.

- &#128994; [torrent](stacks/torrent/README.md) - Full torrenting suite with a preconfigured <a href="https://github.com/ivylikethevine/saffron/blob/main/stacks/torrent/.env.public"><code>.env.public</code></a>.

  - &#x2705; qbittorrentvpn - Torrent client that runs only on VPN connection.

- &#x2705; [ustreamer](stacks/ustreamer/README.md) - Easily deployable IP camera.

- &#x2705; [watchtower](stacks/watchtower/README.md) - Automatically update and restart docker containers.

- &#x2705; [watchyourlan](stacks/watchyourlan/README.md) - Lightweight LAN device and network monitor.

- For other projects that use a docker compose file from locally built Dockerfiles, clone the repo into `/home/$USER/saffron/stacks`, then add `stacks/repoName/` to the `.gitignore` file. An alternative is to use either the `p-` or `dev-` prefix in the stack name to be ignored by git. See [editing .gitignore](https://git-scm.com/book/en/v2/Git-Basics-Recording-Changes-to-the-Repository#_ignoring) for more information.

### `common.yaml`

[Live view of local common.yaml](common.yaml ':include :type=yaml')

#### `common.yaml.public`

[Default saffron common.yaml.public](common.yaml.public ':include :type=yaml yaml')

