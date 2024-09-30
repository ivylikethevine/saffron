# Installation of Saffron (+ git, docker, and avahi)

## Easy installation of git & docker

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

### To Update

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

#### `install-saffron.sh`

[filename](install-saffron.sh ':include :type=code')

##### `remove-saffron.sh`
[filename](remove-saffron.sh ':include :type=code')
