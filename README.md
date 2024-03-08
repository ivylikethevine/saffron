# Saffron

![GitHub repo size](https://img.shields.io/github/repo-size/ivylikethevine/saffron) ![GitHub last commit](https://img.shields.io/github/last-commit/ivylikethevine/saffron) ![GitHub Repo stars](https://img.shields.io/github/stars/ivylikethevine/saffron) ![GitHub forks](https://img.shields.io/github/forks/ivylikethevine/saffron) ![GitHub License](https://img.shields.io/github/license/ivylikethevine/saffron)

## (S)erver (A)s a (F)ile (F)older (R)unning (O)n (N)etwork

...the second half is a backcronym

### Saffron is a docker compose deployment of a homelab via (almost entirely) static files

[Why Saffron?](https://ivylikethevine.com/projects/saffron)

I built saffron because I wanted a way to utilize docker compose on a homelab server with easy SVM, configurability, and simple setup.

#### Features

- Media libraries for TV, movies, music, ebooks, & audiobooks. (+ subtitles!)
- Easy migration from any existing docker or docker compose deployment.
- Full torrenting suite with VPN integration.
- Automated backup to cloud storage.
- Smart home automation & integration.
- Network speedtests + hardware monitoring.
- Minecraft server hosting.
- PXE environment for OS booting on other nodes.
- Zero DNS or networking configuration outside of docker.
- Easily configurable volume mounting via [common.yaml](#common-yaml) and [docker extends](https://docs.docker.com/compose/multiple-compose-files/extends/)

##### Features (Under Development)

1. Automatic traefik routing of containers using docker integration.
1. Avahi mdns/nss-mdns discovery.
1. Git submodules/subtrees for additional services.
1. SSL certs

#### To deploy

Requires: git, docker, docker compose

Tested on: Linux Mint, Ubuntu, and Debian

```bash
# Grab saffron (either http or ssh)
git clone https://github.com/ivylikethevine/saffron.git # http, works with no SSH key
git clone git@github.com:ivylikethevine/saffron.git # ssh
cd saffron/resources

# Make directories with correct permssions, create common.yaml, & start dockge
./install-saffron.sh
```

##### Easy installation of git & docker

```bash
sudo apt install -y git # required to install saffron
sudo apt install -y curl # required to install docker via script
sudo apt install -y avahi-daemon # optional, but highly recommended for easy configuration

# Install docker from the easy install script
curl -fsSL https://get.docker.com -o get-docker.sh && sudo sh ./get-docker.sh

# Allow docker to run without sudo
sudo usermod -aG docker $USER && newgrp docker
# And verify
docker run hello-world
```

Then visit `http://localhost:5001` or `http://<hostname>.local:5001` to start and stop individual stacks via the [Dockge](https://github.com/louislam/dockge) interface. Dockge is a Web UI to manage & control docker containers. As opposed to portainer, the user maintains direct and full control of the compose yaml files.

##### To Update

```bash
docker stop $(docker ps -a -q) # Important to stop before updates! (remove the $ if using fish shell)
cd /home/$USER/saffron
git pull
docker compose up -d dockge # Then visit dockge to start/stop containers
```

#### To Remove

```bash
cd /home/$USER/saffron/resources
./remove-saffron.sh
```

### Important Paths

1. `/containers/` - stores individual generated configs, db files, etc.
   - This is not a perfect separation, since some containers will use config for "data" (such as torrent clients using it as a default download location)
2. `/home/$USER/saffron/stacks` - all stacks & services' compose files
3. `$DATA_DIR` - where bulk files are stored (configured during setup) See [common.yaml](#common-yaml) for more infromation.

## v0.30 List of Stacks & Services (30+ Containers)

\*\* Names are lowercased per dockge stack naming requirements

- &#128679; [avahi](stacks/avahi/README.md) - Allows docker containers to access mdns on LAN.

- &#x2705; [crafty](stacks/crafty/README.md) - Easily deploy/manage minecraft servers.

- &#x2705; [dokemon](stacks/dokemon/README.md) - Web UI to manage docker containers/view logs/etc.

- &#x2705; [dockge](https://github.com/louislam/dockge) - Web UI to manage docker compose files (integral to `saffron`).

  - <details>
      <h3>WebUI Dashboard</h3>
      <img src="resources/screenshots/dockge.webp" alt="dockge ui screenshot"/>

      <img alt="x64 Version" src="https://img.shields.io/docker/v/louislam/dockge/latest?arch=amd64&label=x64">
      <img alt="Arm64 Version" src="https://img.shields.io/docker/v/louislam/dockge/latest?arch=arm64&label=arm64">
    </details>

- &#x2705; [dozzle](stacks/dozzle/README.md) - Web UI to live docker container logs.

- &#x2705; [duplicati](stacks/duplicati/README.md) - Automated backup to AWS/Backblaze/etc.

- &#x2705; [handbrake](stacks/handbrake/README.md) - Web UI for transcoding video/audio files.

- &#x2705; [heimdall](stacks/heimdall/README.md) - Easy to use home page.

- &#x2705; [homeassistant](stacks/homeassistant/README.md) - Smart home automation.

- &#x2705; [it-tools](stacks/it-tools/README.md) - Helpful tool for various tasks (generating UUIDs, hashes, etc.).

- &#x2705; [mariadb](stacks/mariadb/README.md) - Basic database (mostly used as template for adding to services that require a DB).

- &#128994; [media-clients](stacks/media-clients/README.md) - Various media streaming services.

  - &#x2705; jellyfin - TV/movie streaming.

  - &#x2705; jellyseerr - TV/movie requests.

  - &#x2705; kavita - Ebook reader.

  - &#x2705; navidrome - Music streaming service.

  - &#x2705; audiobookshelf - Audiobook streaming.

- &#x2705; [netboot](stacks/netboot/README.md) - PXE boot system.

- &#x2705; [netdata](stacks/netdata/README.md) - Hardware usage/monitoring (incl. containers).

- &#128679; [octoprint](stacks/octoprint/README.md) - 3D printer automation/monitoring

- &#x2705; [plex](stacks/plex/README.md) - Fully featured media player/environment with many smart tv integrations.

- &#128994; [servarr](stacks/servarr/README.md) - Media library systems.

  - &#x2705; sonarr - TV library manager.

  - &#x2705; radarr - Movie library manager.

  - &#x2705; lidarr - Music library manager.

  - &#x2705; readarr - Ebook library manager.

  - &#x2705; bazarr - Subtitle management/requests for sonarr/radarr.

- &#x2705; [speedtest-tracker](stacks/speedtest-tracker/README.md) - Internet speed monitoring.

- &#128679; [tdarr](stacks/tdarr/README.md) - Additional Web UI for transcoding video/audio files, with ability to use distributed compute nodes.

- &#x2705; [thelounge](stacks/thelounge/README.md) - IRC client.

- &#128994; [torrent](stacks/torrent/README.md) - Full torrenting suite with a preconfigured <a href="https://github.com/ivylikethevine/saffron/blob/main/stacks/torrent/.env.public"><code>.env.public</code></a>.

  - &#x2705; qbittorrentvpn - Torrent client that runs only on VPN connection.

  - &#x2705; prowlarr - Search aggregator.

  - &#x2705; flaresolverr - Search proxy (required for some search engines & reduces error rates in general).

- &#128679; [traefik](stacks/traefik/README.md) - Reverse proxy with easy docker integration.

- &#x2705; [uptime-kuma](stacks/uptime-kuma/README.md) - Nice health checking tool with simple UI (same dev as Dockge!).

- &#x2705; [utils](stacks/utils/README.md) - Simple dockerfile-based compose with basic utils for debugging.

- &#x2705; [vscode-server](stacks/vscode-server/README.md) - VSCode running with a Web UI (for editing saffron config files, etc.).

- &#x2705; [watchtower](stacks/watchtower/README.md) - Automatically update & restart docker containers.

- &#x2705; [windows](stacks/windows/README.md) - Automatic install/configuration with web VNC & native RDP for Windows XP -> Windows 11

### Services under consideration

- [Adguard](https://adguard.com/en/welcome.html) - for whole home ad blocking.
- [Ansible Semaphore](https://www.semui.co/) - for easier host updating/management.
- Mail Server - for notifications.
- [Cloudflare](https://developers.cloudflare.com/cloudflare-one/) - for access outside of home network.
- [Nextcloud](https://nextcloud.com/) - for general homelab "cloud".

If a service isn't on here yet, feel free to add it! Most of these are very simple applications of the excellent [linuxserver docker images](https://docs.linuxserver.io/images/). See creating a [saffron-styled compose](#saffron-example) for more detail on the format of `compose.yaml`. There are also the [official docker hub images](https://hub.docker.com/u/library).

I've also made stacks using Lissy93's well maintained [portainer template repo](https://github.com/Lissy93/portainer-templates), although this is slightly different than working from raw compose files.

#### Compatible with

- [obico](https://www.obico.io/docs/server-guides/install/) - 3D print failure detection notification/stopping

  - To install:
    `cd /home/$USER/saffron/stacks && git clone -b release https://github.com/TheSpaghettiDetective/obico-server.git && cd obico-server && docker compose up -d`

- For other projects that use a docker compose file from locally build Dockerfiles, clone the repo into `/home/$USER/saffron/stacks`, then add `stacks/repoName/` to the `.gitignore` file. An alternative is to use either the `p-` or `dev-` prefix in the stack name to be ignored by git. See [editing .gitignore](https://git-scm.com/book/en/v2/Git-Basics-Recording-Changes-to-the-Repository#_ignoring) for more information.

### Configuration

#### `common.yaml` (new in v0.25) <a id="common-yaml"></a>

By using a set of base "services"\*\* inside of `saffron/stacks/common.yaml`, we can limit the length of each docker compose file & allow for easy re-use of shared docker configurations, mainly:

1. Consistent PUID/PGID & UMASK - all extended services have shared environment variables.
2. Consistent mount locations (such as media libraries) - library locations only have to be defined once.
3. Consistent localtime - not very important, but nice to have.

On install, saffron copies it's local `stacks/common.yaml.public` file to `stacks/compose.yaml`, setting `/data` in all extended containers to the value of `$DATA_DIR` used during setup. This can be changed by using vscode-server and editing files in the saffron directory. `common.yaml` is set to be ignored by git to prevent committing personal directory paths.

\*\* : These aren't full services since they have no images defined. As such, they can't run alone.

#### Env Files

This project has 2 types of `.env` files:

1. `.env` - this type is natively loaded by dockge, allowing for Web UI editing + templating for paths. This is the place that VPN credentials, etc. should be stored since they will not be committed.
   - if stacks throw errors about undefined variables, make sure to define those variables in the `.env` for that stack.
   - these files are ignored by git, so they can locally hold some credentials (such as VPN logins) + personal folder routing
2. `.env.public` - this holds basic preconfigurations for each container to work and should be changed with caution. They are not available in the Dockge Web UI.

#### Docker Volumes

When editing the DATA_DIR(s), it is often best to have the last part of the host volume match the container volume, such as:

- `/data/television/:/local/library/television` -> Intuitive
- `/data/TV/:/local/library/television` -> Often confusing (at least for me!)

#### Migration Tools

- [composerize](https://github.com/composerize/composerize) - to turn `docker run...` into docker compose yaml (though dockge does have an implementation of this in the UI)
- [decomposerize](https://github.com/composerize/decomposerize) - inverse of above
- [autocompose](https://github.com/Red5d/docker-autocompose) - to turn running containers into docker compose yaml

##### Internal Routing

For configuring docker containers that talk to each other, you can replace `localhost` with the `container_name` of the service to network, as long as both are inside of the same `compose.yaml`. For example, connecting prowlarr & sonarr, you can use `prowlarr:9696` and `sonarr:8989`. If the containers are not in the same stack, this will require a bridge connection. An example of a bridge is included in `servarr` and `torrent`. To connect to `servarr` from `torrent`, `qbittorrentvpn` must use the `servarr_bridge` network.

### Creating a Saffron-Styled compose from Scratch <a id="saffron-example"></a>

Saffron is designed to be extensible. It is more an amalgamation of my experience than a specific software suite. As such, here is a compilation of my advice when creating new docker compose files for use with saffron or similar deployments.

1. Only edit in one mode at a time - Implemented in this repository is a vscode server, which allows for editing of files that dockge does not display in the UI (such as `.env.public`, `.gitignore`, and the dockge `compose.yaml`). Using dockge to edit some files & vscode to edit others can often result in mismatches and confusion. For any operation, pick one tool and use that until you can fully transition to the other tool.
2. Keep secrets in `.env` and double check your commits! An alternative option is [docker secrets](https://docs.docker.com/compose/use-secrets/), but same rules apply. Make sure your commits never contain private keys, etc.
3. Consistent naming - In the homelab space, some of the more advanced features of docker are not as useful and often lead to confusion. Here is an example format for a compose file, with explanations. Also, [here is the compose documentation](https://docs.docker.com/compose/compose-file/05-services/).

- It is often easiest to name the stack after the main service in the compose file.
  ![image](resources/screenshots/dockge-stack-naming.webp)

#### stacks/vscode-server/compose.yaml

```yaml
version: '3.8'
services:
  vscode-server:
    # "vscode-server" is the name of our service.
    image: linuxserver/code-server
    # Typically, the service name would be derived from the image name (the part after the "/"). Here, it is different to be easier for human readability since "code-server" is quite vague.
    container_name: vscode-server
    # Usually easiest to keep as exact duplicate of service name.
    restart: on-failure
    # Always remember to define a restart policy.
    ports:
      - 8445:8443
      # The port assignments in saffron are designed to avoid conflicts. host:container is the format, and it is easiest to change host mapping by itself, and not to mess with default port mappings. Some containers require environment variables to change the internal port, so its best to avoid.
    extends:
      file: ../common.yaml
      service: base-settings
      # base-settings: PUID, PGID, UMASK & localtime
      # media-access: base-settings + volume mounting $DATA_DIR(s)
    volumes:
      - /containers/vscode-server/config:/config
      # Again, usually easiest to follow /containers/container_name/folder:/folder for consistency & clarity.
networks: {}
```
