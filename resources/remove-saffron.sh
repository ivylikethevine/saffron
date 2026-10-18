#!/bin/bash
set -euo pipefail
# shellcheck source=lib.sh
source "$(dirname "$0")/lib.sh"

echo "Starting Saffron Removal"
echo
echo -e "${RED}WARNING: This will permanently delete:${NC}"
echo "  - every saffron container and network"
echo "  - /containers (all container data)"
echo "  - $SAFFRON_DIR (this checkout)"
echo
echo "This action CANNOT be undone."
echo

read -rp "Are you absolutely sure? Type 'yes' to proceed: " response
if [ "$response" != "yes" ]; then
    echo "Operation canceled."
    exit 0
fi

echo
echo "Removing saffron stacks..."
for file in "$SAFFRON_DIR"/stacks/*/compose.yaml "$SAFFRON_DIR"/compose.yaml; do
    docker compose -f "$file" down --remove-orphans || true
done
success "Removed containers and networks"

sudo rm -rf /containers
success "Removed /containers"

sudo rm -rf "$SAFFRON_DIR"
success "Removed $SAFFRON_DIR"

echo
echo "Leftover images can be cleaned with: docker image prune -a"
