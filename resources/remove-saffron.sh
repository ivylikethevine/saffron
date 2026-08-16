#!/bin/bash
set -euo pipefail

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo "Starting Saffron Removal"
echo
echo -e "${RED}WARNING: This will permanently delete:${NC}"
echo "  - /containers directory (all container data)"
echo "  - /home/$USER/saffron directory (all configuration)"
echo "  - All running Saffron containers"
echo
echo "This action CANNOT be undone."
echo

read -p "Are you absolutely sure? Type 'yes' to proceed: " response

if [ "$response" != "yes" ]; then
    echo "Operation canceled."
    exit 0
fi

echo
echo "Stopping all Docker containers..."
if containers=$(docker ps -aq); then
    if [ -n "$containers" ]; then
        docker stop $containers || true
        echo -e "${GREEN}✓ Stopped containers${NC}"
    fi
fi

echo "Removing /containers directory..."
if [ -d "/containers" ]; then
    sudo rm -rf /containers || exit 1
    echo -e "${GREEN}✓ Removed /containers${NC}"
fi

echo "Removing /home/$USER/saffron directory..."
if [ -d "/home/$USER/saffron" ]; then
    sudo rm -rf /home/$USER/saffron || exit 1
    echo -e "${GREEN}✓ Removed saffron${NC}"
fi

echo
echo -e "${GREEN}Removal complete!${NC}"
echo "Leftover Docker resources can be cleaned with:"
echo "  docker system prune -a"
echo
