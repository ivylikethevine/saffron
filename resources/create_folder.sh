#!/bin/bash
DATA_DIR=$1

read -p "Are you sure you want to create the /containers folders?" -n 1 -r
echo # (optional) move to a new line
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    [[ "$0" = "$BASH_SOURCE" ]] && exit 1 || return 1 # handle exits from shell or function but don't exit interactive shell
fi

echo "Making /containers directory"
sudo mkdir /containers
cd /containers

echo "Generating /containers/* directories from saffron/stacks"
ls -d -- /home/$USER/saffron/stacks/* | awk -F/ '{print "/containers/" $NF}' | xargs -I {} mkdir {}

echo "Changing /containers permissions"
sudo chown -R 1000:1000 /containers
sudo chmod -R 755 /containers

if [ -z "$DATA_DIR" ]; then
    echo "No DATA_DIR supplied, exiting"
else
    read -p "Are you sure you want to create the /$DATA_DIR folder?" -n 1 -r
    echo # (optional) move to a new line
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        [[ "$0" = "$BASH_SOURCE" ]] && exit 1 || return 1 # handle exits from shell or function but don't exit interactive shell
    fi

    echo "Creating DATA_DIR at $DATA_DIR"
    sudo mkdir $DATA_DIR

    echo "Changing $DATA_DIR permissions"
    sudo chown -R 1000:1000 $DATA_DIR
    sudo chmod -R 755 $DATA_DIR
fi
