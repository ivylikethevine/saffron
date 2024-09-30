# Saffron

[![GitHub repo size](https://img.shields.io/github/repo-size/ivylikethevine/saffron) ![GitHub last commit](https://img.shields.io/github/last-commit/ivylikethevine/saffron) ![GitHub Repo stars](https://img.shields.io/github/stars/ivylikethevine/saffron) ![GitHub License](https://img.shields.io/github/license/ivylikethevine/saffron)](https://github.com/ivylikethevine/saffron)

## (S)erver (A)s a (F)ile (F)older (R)unning (O)n (N)etwork

...the second half is a backcronym

### What is Saffron?

Saffron is a(n)
1. open sourced
2. homelab deployment
3. annotated notebook
4. self documenting wiki
5. docker compose system

**Saffron is GPL-3.0 open sourced [on github](https://github.com/ivylikethevine/saffron)**

### Saffron is a docker compose deployment of a homelab via (almost entirely) static files

[Why Saffron?](https://ivylikethevine.com/projects/saffron)

I built saffron because I wanted a way to utilize docker compose on a homelab server with easy SVM, configurability, and simple setup.

Read this project's README's as a wiki [here](https://ivylikethevine.github.io/saffron), served via [docsify](https://ivylikethevine.github.io/saffron).

### What does Saffron replace?

- Media libraries for TV, movies, music, ebooks, & audiobooks. (+ subtitles!)
  - Radarr/Sonarr + Plex/Jellyfin
  - Lidarr + Navidrome
  - Readarr + Kavita & Audiobookshelf
  - Bazarr
  - Overseerr/Jellyseer
- Self contained and reactive wiki
  - docsify
  - vscode-server
- Comprehensive monitoring/administration suite
  - dockage
  - uptime kuma
  - dozzle
  - netdata
  - speedtest-tracker
- Full torrenting suite with VPN integration.
  - qbittorrentvpn
  - prowlarr
  - flaresolvarr
- Automated backup to cloud storage.
  - duplicati
- Smart home automation & integration.
  - homeassistant
  - ustreamer
  - octoprint
  - esphome

AND MORE

All while being:

- Zero DNS or networking configuration outside of docker.
- Easily configurable volume mounting via [common.yaml](#common-yaml) and [docker extends](https://docs.docker.com/compose/multiple-compose-files/extends/)
- Easy migration from any existing docker or docker compose deployment.

<!-- [filename](.gitignore ':include :type=code') -->

### Configuration

#### `common.yaml` <a id="common-yaml"></a>

By using a set of base "services"\*\* inside of `saffron/stacks/common.yaml`, we can limit the length of each docker compose file & allow for easy re-use of shared docker configurations, mainly:

1. Consistent PUID/PGID & UMASK - all extended services have shared environment variables.
2. Consistent mount locations (such as media libraries) - library locations only have to be defined once.
3. Consistent localtime - not very important, but nice to have.

On install, saffron copies it's local `stacks/common.yaml.public` file to `stacks/compose.yaml`, setting `/data` in all extended containers to the value of `$DATA_DIR` used during setup. This can be changed by using vscode-server and editing files in the saffron directory. `common.yaml` is set to be ignored by git to prevent committing personal directory paths.

\*\* : These aren't full services since they have no images defined. As such, they can't run alone.

[filename](stacks/common.yaml.public ":include :type=code")

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
version: "3.8"
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

#### To Install \* Deploy

In depth instructions, including prerequisites [here](resources/README.md).

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

Then visit `http://localhost:5001` or `http://<hostname>.local:5001` to start and stop individual stacks via the [Dockge](https://github.com/louislam/dockge) interface. Dockge is a Web UI to manage & control docker containers. As opposed to portainer, the user maintains direct and full control of the [compose](https://docs.docker.com/compose/) [yaml](https://learnxinyminutes.com/docs/yaml/) files.

If a service isn't on here yet, feel free to add it! Most of these are very simple applications of the excellent [linuxserver docker images](https://docs.linuxserver.io/images/). See creating a [saffron-styled compose](#saffron-example) for more detail on the format of `compose.yaml`. There are also the [official docker hub images](https://hub.docker.com/u/library).

I've also made stacks using Lissy93's well maintained [portainer template repo](https://github.com/Lissy93/portainer-templates), although this is slightly different than working from raw compose files.

### Important Paths

1. `/containers/` - stores individual generated configs, db files, etc.
   - This is not a perfect separation, since some containers will use config for "data" (such as torrent clients using it as a default download location)
2. `/home/$USER/saffron/stacks` - all stacks & services' compose files
3. `$DATA_DIR` - where bulk files are stored (configured during setup) See [common.yaml](#common-yaml) for more infromation.
