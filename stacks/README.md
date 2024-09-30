# Saffron Stacks & Services

## v1.00 List of Stacks & Services

[Stacks](stacks/README.md) rely on a customized [common.yaml.public] for correct permissions, time zones, and data directory mounts.

\*\* Names are lowercased per dockge stack naming requirements

- &#x2705; [docsify](stacks/docsify/README.md) - Web UI to view this repo's `README.md`'s as a wiki reflecting local edits. See the [public](https://ivylikethevine.github.io/saffron) instance or visit <http://hostname.local:5001> (if the container is running).

- &#x2705; [dockge](dockge.md) - Web UI to manage docker compose files (integral to `saffron`).

- &#x2705; [dozzle](stacks/dozzle/README.md) - Web UI to live docker container logs.

- &#x2705; [duplicati](stacks/duplicati/README.md) - Automated backup to AWS/Backblaze/etc.

- &#x2705; [esphome](stacks/esphome/README.md) - Easily create & mange esp32-based IoT devices, such as temp. sensors.

- &#x2705; [heimdall](stacks/heimdall/README.md) - Easy to use home page.

- &#x2705; [homeassistant](stacks/homeassistant/README.md) - Smart home automation.

- &#x2705; [it-tools](stacks/it-tools/README.md) - Helpful tool for various tasks (generating UUIDs, hashes, etc.).

- &#x2705; [jellyfin](stacks/jellyfin/README.md) - TV/movie streaming.

  - &#x2705; jellyseerr - TV/movie requests.

- &#128994; [media-clients](stacks/media-clients/README.md) - Various media streaming services.

  - &#x2705; kavita - Ebook reader.

  - &#x2705; navidrome - Music streaming service.

  - &#x2705; audiobookshelf - Audiobook streaming.

- &#x2705; [metube](stacks/metube/README.md) - Hardware usage/monitoring (incl. containers).

- &#x2705; [netdata](stacks/netdata/README.md) - Hardware usage/monitoring (incl. containers).

- &#x2705; [octoprint](stacks/octoprint/README.md) - 3D printer automation/monitoring

- &#x2705; [plex](stacks/plex/README.md) - Fully featured media player/environment with many smart tv integrations.

  - &#x2705; overseerrr - TV/movie requests.

- &#128994; [servarr](stacks/servarr/README.md) - Media library systems.

  - &#x2705; sonarr - TV library manager.

  - &#x2705; radarr - Movie library manager.

  - &#x2705; lidarr - Music library manager.

  - &#x2705; readarr - Ebook library manager.

  - &#x2705; bazarr - Subtitle management/requests for sonarr/radarr.

- &#x2705; [speedtest-tracker](stacks/speedtest-tracker/README.md) - Internet speed monitoring.

- &#128994; [torrent](stacks/torrent/README.md) - Full torrenting suite with a preconfigured <a href="https://github.com/ivylikethevine/saffron/blob/main/stacks/torrent/.env.public"><code>.env.public</code></a>.

  - &#x2705; qbittorrentvpn - Torrent client that runs only on VPN connection.

  - &#x2705; prowlarr - Search aggregator.

  - &#x2705; flaresolverr - Search proxy (required for some search engines & reduces error rates in general).

- &#x2705; [uptime-kuma](stacks/uptime-kuma/README.md) - Nice health checking tool with simple UI (same dev as Dockge!).

- &#x2705; [ustreamer](stacks/ustreamer/README.md) - Easily deployable IP camera.

- &#x2705; [vscode-server](stacks/vscode-server/README.md) - VSCode running with a Web UI (for editing saffron config files, etc.).

- &#x2705; [watchtower](stacks/watchtower/README.md) - Automatically update & restart docker containers.

- &#x2705; [windows](stacks/windows/README.md) - Automatic install/configuration with web VNC & native RDP for Windows XP -> Windows 11

- For other projects that use a docker compose file from locally build Dockerfiles, clone the repo into `/home/$USER/saffron/stacks`, then add `stacks/repoName/` to the `.gitignore` file. An alternative is to use either the `p-` or `dev-` prefix in the stack name to be ignored by git. See [editing .gitignore](https://git-scm.com/book/en/v2/Git-Basics-Recording-Changes-to-the-Repository#_ignoring) for more information.

### `common.yaml`

[Live view of local common.yaml](common.yaml ':include :type=yaml')

#### `common.yaml.public`

[Default saffron common.yaml.public](common.yaml.public ':include :type=yaml yaml')

