#!/bin/bash

echo "Starting Saffron Removal"

echo "This script will delete all files in /containers and /home/$USER/saffron. Are you sure you want to proceed? (y/n)"

while true; do
    read -s -n 1 key

    case $key in
    y | Y)
        echo "Stopping all containers"
        docker stop $(docker ps -a -q)

        echo "Deleting /containers directory"
        cd /
        sudo rm -rf containers

        echo "Deleting /home/$USER/saffron"
        cd /home/$USER/
        sudo rm -rf saffron
        echo "Removal complete. If you want to remove leftover docker images, use docker [container|image|system|network|etc] prune"
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
