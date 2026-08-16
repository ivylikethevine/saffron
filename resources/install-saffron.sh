#!/bin/bash
set -euo pipefail

# Color output for better readability
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

error_exit() {
    echo -e "${RED}Error: $1${NC}" >&2
    exit 1
}

success() {
    echo -e "${GREEN}✓ $1${NC}"
}

echo "Starting Saffron Installation"
echo

# Check for required commands
for cmd in docker docker-compose; do
    if ! command -v $cmd &> /dev/null; then
        error_exit "$cmd is not installed. Please install Docker and Docker Compose first."
    fi
done

# Check if running from correct directory
if [ ! -d "stacks" ] || [ ! -f "stacks/common.yaml.public" ]; then
    error_exit "Must run from saffron root directory (/home/$USER/saffron)"
fi

echo "Making /containers directory"
sudo mkdir -p /containers || error_exit "Failed to create /containers"
success "Created /containers directory"

echo "Generating /containers/* directories from saffron/stacks"
ls -d -- /home/$USER/saffron/stacks/* 2>/dev/null | awk -F/ '{print "/containers/" $NF}' | xargs -I {} sudo mkdir -p {} || error_exit "Failed to create container directories"
success "Created container subdirectories"

echo "Changing /containers permissions"
sudo chown -R 1000:1000 /containers || error_exit "Failed to change /containers ownership"
sudo chmod -R 755 /containers || error_exit "Failed to change /containers permissions"
success "Set /containers permissions"

echo
read -p 'Where is the data directory? (ex: /data): ' DATA_DIR

if [ -z "$DATA_DIR" ]; then
    error_exit "Data directory cannot be empty"
fi

echo "Creating DATA_DIR at $DATA_DIR"
sudo mkdir -p "$DATA_DIR" || error_exit "Failed to create $DATA_DIR"
success "Created data directory"

echo "Changing $DATA_DIR permissions"
sudo chown -R 1000:1000 "$DATA_DIR" || error_exit "Failed to change ownership of $DATA_DIR"
sudo chmod -R 755 "$DATA_DIR" || error_exit "Failed to change permissions of $DATA_DIR"
success "Set data directory permissions"

echo
echo "Creating common.yaml from common.yaml.public..."
cd /home/$USER/saffron/stacks
cp common.yaml.public common.yaml || error_exit "Failed to copy common.yaml.public"

# IMPORTANT: Append to the file, not overwrite it
# Find the line with "- /data" and replace with the configured path
sed -i "s|^      - /data:|      - $DATA_DIR:|" common.yaml || error_exit "Failed to update common.yaml with DATA_DIR"
success "Created common.yaml with DATA_DIR=$DATA_DIR"

cd /home/$USER/saffron || error_exit "Failed to cd to saffron directory"

echo
echo "Installation complete! Starting dockge..."
docker compose up -d || error_exit "Failed to start dockge"
success "Dockge started"

echo
echo -e "${YELLOW}Next steps:${NC}"
echo "1. Visit http://$HOSTNAME.local:5001 to access Dockge"
echo "2. Start the desired stacks from the Dockge UI"
echo "3. Configure .env files with your credentials"
echo

# Try to open in browser if possible
if command -v xdg-open &> /dev/null; then
    xdg-open "http://$HOSTNAME.local:5001/" || true
elif command -v open &> /dev/null; then
    open "http://$HOSTNAME.local:5001/" || true
fi
