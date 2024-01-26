# Saffron

## (S)erver (A)s a (F)ile (F)older (R)unning (O)n (N)etwork
...the second half is a backcronym

### Saffron is a docker compose based implementation of a server deployable via static files.

#### To deploy:

```bash
ssh <hostname>.local
git clone git@github.com:ivylikethevine/saffron.git
cd saffron
cd dockge
docker compose up -d
```

then visit localhost:5001  or \<hostname\>.local:5001 to start and stop individual stacks via the [Dockge](https://github.com/louislam/dockge) interface. Dockge is a WEBUI to manage & control docker containers. As opposed to portainer, the user maintains direct and full control of the compose yaml files.

## v1.00 List of Stacks & Services
- [airsonic-advanced](https://docs.linuxserver.io/images/docker-airsonic-advanced/) - music streaming
- [calibre-web](https://docs.linuxserver.io/images/docker-calibre-web/) - ebook reading
- [crafty](https://docs.craftycontrol.com/pages/getting-started/installation/docker/) - minecraft servers
- [duplicati](https://docs.linuxserver.io/images/docker-duplicati/) - backup to AWS/Backblaze/etc.
- [heimdall](https://docs.linuxserver.io/images/docker-heimdall/) - home page
- [homeassistant](https://www.home-assistant.io/installation/linux#docker-compose) - smart home automation
- [jellyfin](https://docs.linuxserver.io/images/docker-jellyfin/) - media streaming & [jellyseer](https://hub.docker.com/r/fallenbagel/jellyseerr) - media requests
- [netboot](https://docs.linuxserver.io/images/docker-netbootxyz/) - PXE boot system
- [netdata](https://learn.netdata.cloud/docs/installing/docker) - hardware usage/monitoring
- [qbittorrentvpn](https://github.com/MarkusMcNugen/docker-qBittorrentvpn) - torrent client that runs only on VPN connection
- [servarr](https://wiki.servarr.com/docker-guide) - media library system
    * [sonarr](https://docs.linuxserver.io/images/docker-sonarr/) - tv
    * [radarr](https://docs.linuxserver.io/images/docker-radarr/) - movies
    * [lidarr](https://docs.linuxserver.io/images/docker-lidarr/) - music
    * [readarr](https://docs.linuxserver.io/images/docker-readarr/) - ebooks
    * [bazarr](https://docs.linuxserver.io/images/docker-bazarr/) - subtitles for movies/tv
    * [prowlarr](https://docs.linuxserver.io/images/docker-prowlarr/) - search aggregator
    * [flaresolverr](https://github.com/FlareSolverr/FlareSolverr) - search proxy (required for some search engines)
- [speedtest-tracker](https://github.com/alexjustesen/speedtest-tracker) - internet speed monitoring
- [thelounge](https://github.com/thelounge/thelounge-docker) - IRC client
- [watchtower](https://github.com/containrrr/watchtower) - automatically update & restart docker containers

### To-Do:
- Test dockge multiple node system
- Netdata streaming between nodes
- Add traefik autorouting
- Add uptime/monitoring
- Test easy docker install on linux mint

#### Easy docker install

`curl -fsSL https://get.docker.com -o get-docker.sh && sudo sh ./get-docker.sh`

##### Migration Tools

- [composerize](https://github.com/composerize/composerize) - to turn `docker run...` into docker compose yaml
- [decomposerize](https://github.com/composerize/decomposerize) - inverse of above
- [autocompose](https://github.com/Red5d/docker-autocompose) - to turn running containers into docker compose yaml

###### Env Files
This project has two types of .env files:
1. .env - this type is natively loaded by dockge, allowing for WEBUI editing + templating for paths. This is the place that VPN credentials, etc. should be stored since they will not be committed.
2. general.env - this holds basic configurations for each container to work and should be changed with caution. They are not available in the Dockge WEBUI