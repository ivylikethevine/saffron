# shellcheck shell=bash
# Shared helpers for the saffron scripts. Source it; don't run it.

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

# The checkout this script lives in, wherever it was cloned.
SAFFRON_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
