#!/bin/bash

echo "Starting Saffron Removal"

echo "This script will delete all empty files in /containers, /home/$USER/saffron, and DATA_DIR. Are you sure you want to proceed? (y/n)"

while true; do
    read -s -n 1 key

    case $key in
    y | Y)
        echo "Stopping all containers"
        docker stop $(docker ps -a -q)

        echo "Deleting /containers directory"
        sudo rm -rf /containers

        read -p 'Where is the data directory? (ex: /data): ' $DATA_DIR

        echo "Deleting DATA_DIR at $DATA_DIR"
        sudo rm -rf $DATA_DIR

        cd /home/$USER/saffron/
        echo "Removal complete."
        exit 0
        ;;

    n | N)
        echo "You pressed $key. Operation canceled."
        exit 0
        ;;
    *)
        echo "Invalid input. Please press 'y' or 'n'."
        ;;
    esac

done
