#!/bin/bash
set -euo pipefail
# shellcheck source=lib.sh
source "$(dirname "$0")/lib.sh"

echo "Starting Saffron Installation"
echo

command -v docker >/dev/null || error_exit "docker is not installed. Please install Docker first."
docker compose version >/dev/null 2>&1 || error_exit "docker compose (v2) is not installed."

echo "Making /containers directories"
sudo mkdir -p /containers || error_exit "Failed to create /containers"
for dir in "$SAFFRON_DIR"/stacks/*/; do
    sudo mkdir -p "/containers/$(basename "$dir")" || error_exit "Failed to create /containers/$(basename "$dir")"
done
sudo chown -R 1000:1000 /containers || error_exit "Failed to change /containers ownership"
sudo chmod -R 755 /containers || error_exit "Failed to change /containers permissions"
success "Created /containers"

echo
read -rp 'Where is the data directory? (ex: /data): ' DATA_DIR
[ -n "$DATA_DIR" ] || error_exit "Data directory cannot be empty"
sudo mkdir -p "$DATA_DIR" || error_exit "Failed to create $DATA_DIR"
sudo chown -R 1000:1000 "$DATA_DIR" || error_exit "Failed to change ownership of $DATA_DIR"
sudo chmod -R 755 "$DATA_DIR" || error_exit "Failed to change permissions of $DATA_DIR"
success "Created $DATA_DIR"

echo
# media-access mounts DATA_DIR at /data in every container that extends it
sed "s|^      - /data:|      - $DATA_DIR:|" "$SAFFRON_DIR/stacks/common.yaml.public" > "$SAFFRON_DIR/stacks/common.yaml" \
    || error_exit "Failed to create stacks/common.yaml"
success "Created stacks/common.yaml with DATA_DIR=$DATA_DIR"

if [ -d "$SAFFRON_DIR/.git" ]; then
    ln -sf ../../resources/pre-commit "$SAFFRON_DIR/.git/hooks/pre-commit"
    success "Installed the webp pre-commit hook"
fi

echo
echo "Starting dockge..."
(cd "$SAFFRON_DIR" && docker compose up -d) || error_exit "Failed to start dockge"
success "Dockge started"

echo
echo -e "${YELLOW}Next steps:${NC}"
echo "1. Visit http://$HOSTNAME.local:5001 to access Dockge"
echo "2. Start the desired stacks from the Dockge UI"
echo "3. Configure .env files with your credentials"
echo

if command -v xdg-open >/dev/null; then
    xdg-open "http://$HOSTNAME.local:5001/" || true
elif command -v open >/dev/null; then
    open "http://$HOSTNAME.local:5001/" || true
fi
