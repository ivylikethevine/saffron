#!/bin/bash

echo "Starting install of Saffron"
echo "Installing prerequisites"

sudo apt install -y git avahi-daemon

echo "Installing docker via get-docker.sh"
curl -fsSL https://get.docker.com -o get-docker.sh && sudo sh ./get-docker.sh
echo "Docker installation complete"

echo "Making docker not require root"
sudo groupadd docker
sudo usermod -aG docker $USER
newgrp docker

echo "Making /containers directory"
sudo mkdir /containers
cd /containers

echo "Generating /containers/* directories from saffron/stacks"
ls -d -- /home/$USER/saffron/stacks/* | awk -F/ '{print "/containers/" $NF}' | xargs -I {} mkdir {}

echo "Changing /containers permissions"
sudo chown -R 1000:1000 /containers
sudo chmod -R 755 /containers

# Ask the user for login details
read -p 'Where is the data directory? (ex: /data, /media/harddrive, etc.): ' $DATA_DIR

echo "Creating DATA_DIR at $DATA_DIR"
sudo mkdir $DATA_DIR

echo "Changing $DATA_DIR permissions"
sudo chown -R 1000:1000 $DATA_DIR
sudo chmod -R 755 $DATA_DIR

echo "Installation complete, starting dockge..."
docker compose up -d
xdg-open http://$HOSTNAME.local:5001/