#!/bin/bash

echo "Starting Saffron Installation"

echo "Making /containers directory"
sudo mkdir /containers
cd /containers

echo "Generating /containers/* directories from saffron/stacks"
ls -d -- /home/$USER/saffron/stacks/* | awk -F/ '{print "/containers/" $NF}' | xargs -I {} sudo mkdir {}

echo "Changing /containers permissions"
sudo chown -R 1000:1000 /containers
sudo chmod -R 755 /containers

read -p 'Where is the data directory? (ex: /data): ' DATA_DIR

echo "Creating DATA_DIR at $DATA_DIR"
sudo mkdir $DATA_DIR

echo "Changing $DATA_DIR permissions"
sudo chown -R 1000:1000 $DATA_DIR
sudo chmod -R 755 $DATA_DIR

cd /home/$USER/saffron/
echo "Installation complete, starting dockge..."
docker compose up -d

echo "Creating common.yaml from common.yaml.public..."
cd /home/$USER/saffron/stacks
cp common.yaml.public common.yaml
sed -i -e "s/host_data_dir/$DATA_DIR/g" common.yaml
cd /home/$USER/saffron

echo "Opening dockge in web browser"
xdg-open http://$HOSTNAME.local:5001/
