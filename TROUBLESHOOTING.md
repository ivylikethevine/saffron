# Troubleshooting Guide

Common issues and solutions for Saffron deployments.

## Installation & Setup

### "Command not found: docker-compose"

**Problem:** Docker is installed but docker-compose isn't available.

**Solution:**
```bash
# Check if docker-compose-v2 is installed
docker compose version  # v2 syntax (newer)

# If using v1 (older), install v2:
sudo apt install docker-compose-v2
```

**Why:** Docker now includes compose as `docker compose` (v2). The standalone `docker-compose` (v1) is deprecated but still works.

---

### "Permission denied while trying to connect to Docker daemon"

**Problem:** User can't access docker without sudo.

**Solution:**
```bash
# Add current user to docker group
sudo usermod -aG docker $USER
newgrp docker

# Verify
docker ps
```

**Why:** Docker daemon requires special permissions. The docker group grants access without sudo.

---

### "Failed to start dockge" during install

**Problem:** `docker compose up -d` fails immediately after install script.

**Solution:**
```bash
# Check the error
docker compose logs dockge

# Common cause: port already in use
sudo lsof -i :5001  # See what's using port 5001

# If something else is using it, change the port in compose.yaml
```

**Why:** Port 5001 might already be in use by another service.

---

### "Cannot connect to /var/run/docker.sock: Permission denied"

**Problem:** Even after adding to docker group, still get permission errors.

**Solution:**
```bash
# Log out and back in to apply new group membership
exit  # Close terminal
# Open a new terminal and try again

# OR, reset the docker socket
sudo systemctl restart docker
```

**Why:** Group changes require a new login session to take effect.

---

## Compose File Issues

### "Compose file invalid" in Dockge UI

**Problem:** Stack shows error, won't deploy.

**Solution:**
```bash
# Validate the compose file
cd stacks/[stackname]
docker compose config

# If error, check for:
# - YAML syntax (indentation, colons, quotes)
# - Missing image: line
# - Undefined environment variables

# Test with a simpler compose file
docker compose -f stacks/gotify/compose.yaml config  # This one should work
```

**Why:** Docker compose is strict about YAML syntax and image definitions.

---

### "service not defined in common.yaml"

**Problem:** Stack fails with "service 'base-settings' not found".

**Solution:**
```bash
# Verify common.yaml exists
ls -la stacks/common.yaml

# If missing, regenerate it
cd stacks
cp common.yaml.public common.yaml
sed -i 's|^      - /data:|      - /path/to/data:|' common.yaml

# Test the stack
docker compose -f servarr/compose.yaml config
```

**Why:** The install script creates common.yaml. If it doesn't exist, stacks fail.

---

## Runtime Issues

### "Can't connect to Docker daemon" when starting stacks

**Problem:** Dockge shows "Connection error" when trying to deploy.

**Solution:**
```bash
# Check if docker daemon is running
sudo systemctl status docker

# If not running, start it
sudo systemctl start docker

# If it won't start, check logs
sudo journalctl -u docker -n 50
```

**Why:** Docker daemon may have crashed or stopped.

---

### "port is already allocated"

**Problem:** Stack fails to start: "port 8080:8080 is already allocated".

**Solution:**
```bash
# Find what's using the port
sudo lsof -i :8080

# Option 1: Stop the conflicting container
docker stop [container_name]

# Option 2: Change the port in compose.yaml (left side of mapping)
# ports:
#   - "8081:8080"  # Changed from 8080:8080
```

**Why:** Another container or service is already listening on that port.

---

### "Cannot connect to [service_name]:8989"

**Problem:** One stack can't reach another (e.g., torrent can't reach servarr).

**Solution:**
```bash
# Check if both containers are running
docker ps | grep sonarr
docker ps | grep qbittorrent

# Check if they're on the same network
docker network inspect servarr_bridge

# If the network doesn't exist, create it
docker network create servarr_bridge

# Restart both stacks
cd stacks/servarr && docker compose up -d
cd stacks/torrent && docker compose up -d
```

**Why:** Containers can only communicate if they're on the same docker network.

---

### "Out of memory" or "Killed"

**Problem:** Container crashes with no error, or system becomes unresponsive.

**Solution:**
```bash
# Check memory usage
free -h
docker stats

# Find memory hogs
docker stats --no-stream | sort -k4 -h

# If a stack is using too much, adjust it
# Example: Plex using 8GB (add memory limit to compose.yaml):
# deploy:
#   resources:
#     limits:
#       memory: 2G

# Restart containers
docker compose -f stacks/plex/compose.yaml restart
```

**Why:** Some services (Plex, elastic search) can use excessive memory if not limited.

---

## Network Issues

### "Can't access stack from another computer"

**Problem:** Service works on `localhost:8080` but not from `192.168.1.x:8080`.

**Solution:**
```bash
# Check if port is bound to localhost only
sudo netstat -tlnp | grep 8080

# If it shows 127.0.0.1:8080, it's localhost-only

# To expose to LAN, change ports in compose.yaml:
# Before:  - "8080:8080"
# After:   - "0.0.0.0:8080:8080"

# Or better yet, use a reverse proxy (traefik, nginx)
```

**Why:** By default, docker binds ports to 127.0.0.1 for security.

---

### "VPN container won't start" (torrent, bitmagnet)

**Problem:** Service using gluetun fails with "Cannot configure VPN".

**Solution:**
```bash
# Check VPN configuration in .env
cd stacks/torrent
cat .env  # Verify PROVIDER, PRIVATE_KEY, etc. are set

# Test VPN connection
docker logs qbittorrentvpn  # Check for errors

# Common issues:
# - Invalid wireguard credentials
# - VPN provider website changed format
# - Port forwarding misconfigured

# Verify credentials format
echo "PRIVATE_KEY value should start with: [Interface]..."
```

**Why:** VPN configuration is complex; small typos break the connection.

---

### "DNS not resolving inside containers"

**Problem:** Container can't reach `example.com`, DNS queries fail.

**Solution:**
```bash
# Check docker DNS configuration
cat /etc/docker/daemon.json

# Add custom DNS if needed
sudo cat > /etc/docker/daemon.json << 'EOF'
{
  "dns": ["8.8.8.8", "8.8.4.4"]
}
EOF
sudo systemctl restart docker

# Restart containers
docker compose -f stacks/torrent/compose.yaml restart
```

**Why:** Docker uses host's DNS by default; some networks block or misconfigure it.

---

## Data & Persistence

### "Data disappeared after restart"

**Problem:** All container data is gone after `docker-compose down`.

**Solution:**
```bash
# Check volume configuration
docker volume ls

# Verify /containers directory exists
ls -la /containers/

# Check file permissions
ls -la /containers/gotify/

# Restore from backup if available
# (backrest should have backups)
```

**Why:** If volumes aren't properly mounted, data is lost when containers stop.

---

### "Permission denied: /containers/[service]"

**Problem:** Container can't write to `/containers/service` directory.

**Solution:**
```bash
# Check permissions
ls -la /containers/gotify/

# Fix ownership (should be 1000:1000)
sudo chown -R 1000:1000 /containers/gotify

# Fix permissions
sudo chmod -R 755 /containers/gotify

# Restart the stack
docker compose -f stacks/gotify/compose.yaml restart
```

**Why:** Containers run as PUID/PGID 1000:1000 (user). If directory is owned by root, they can't write.

---

### "Disk full" error

**Problem:** Container crashes, "no space left on device".

**Solution:**
```bash
# Find what's using disk space
du -sh /containers/*
du -sh $DATA_DIR  # Media directory

# Clean up old logs/data
docker system prune -a

# Remove unused images
docker image prune -a

# If media dir is full, add more storage or delete old files
df -h  # See disk usage
```

**Why:** Docker logs, images, and media files accumulate over time.

---

## Performance Issues

### "High CPU usage" or "slow response times"

**Problem:** Service is slow or CPU-bound.

**Solution:**
```bash
# Identify the culprit
docker stats --no-stream | sort -k3 -h

# Check container logs for errors
docker logs [container_name]

# Common causes:
# 1. Indexing/scanning (sonarr, radarr do this on start)
# 2. Backup running (backrest)
# 3. Transcoding (plex)
# 4. Search indexing (prowlarr)

# These are normal; they'll complete eventually
```

**Why:** Some operations are intentionally resource-intensive; they run in the background.

---

### "Slow stack startup"

**Problem:** Stack takes 5+ minutes to start.

**Solution:**
```bash
# Check for initialization tasks
docker compose -f stacks/[name]/compose.yaml logs

# Look for:
# - "Creating database..." (normal, first run)
# - "Building search index..." (expected for indexing services)
# - "Waiting for service to be healthy..." (depends_on health checks)

# If taking too long, check:
docker ps  # See if all containers actually started

# Increase startup timeout in docker daemon
# /etc/docker/daemon.json:
# "default-ulimits": {"nofile": {"Name": "nofile", "Soft": 65536, "Hard": 65536}}
```

**Why:** First startup includes database initialization and service health checks.

---

## Logging & Debugging

### "I need to see what's happening inside a container"

**Problem:** Need to debug a failing service.

**Solution:**
```bash
# View logs in real-time
docker logs -f [container_name]

# View only recent logs
docker logs --tail 50 [container_name]

# Get timestamps
docker logs --timestamps [container_name]

# View logs from Dockge UI:
# 1. Click on the stack name
# 2. Click "View Logs" tab
```

**Why:** Container logs show initialization messages, errors, and runtime events.

---

### "How do I get a shell inside a container?"

**Problem:** Need to run commands or investigate filesystem.

**Solution:**
```bash
# Get a bash shell
docker exec -it [container_name] bash

# Get a sh shell (if bash isn't available)
docker exec -it [container_name] sh

# Run a single command
docker exec [container_name] ls -la /config

# Run as root
docker exec -u 0 [container_name] apt update  # (for Debian-based images)
```

**Why:** Interactive debugging sometimes requires direct shell access.

---

## Updates & Maintenance

### "How do I update a service?"

**Problem:** Want to get the latest version of a service.

**Solution:**
```bash
# Option 1: Watchtower does this automatically (once daily)

# Option 2: Manual update
cd stacks/[service]
docker compose pull  # Download latest image
docker compose up -d  # Apply the update

# Verify update worked
docker image inspect [image_name] | grep -A 2 '"Created"'
```

**Why:** `pull_policy: always` ensures latest image on start; watchtower automates this.

---

## When All Else Fails

### "Stack is completely broken, I want to reset it"

**Problem:** Can't recover from a configuration mistake.

**Solution:**
```bash
# BACKUP FIRST if the stack has data you care about
docker compose -f stacks/[service]/compose.yaml down -v  # -v removes volumes!

# Reset compose file to original
cd stacks/[service]
git checkout compose.yaml

# Reset .env to template
rm .env
cp .env.public .env
# Edit .env with correct values

# Start fresh
docker compose up -d
```

**Warning:** The `-v` flag deletes all data. Backup first!

---

### "Docker is completely broken, I need to reinstall"

**Problem:** Docker daemon won't start or is corrupted.

**Solution:**
```bash
# BACKUP all data in /containers/ and $DATA_DIR first!

# Stop all containers
docker compose -f stacks/*/compose.yaml down

# Uninstall docker
sudo apt remove docker-ce docker-ce-cli containerd.io

# Reinstall
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Verify
docker --version
docker run hello-world
```

**Why:** Full reinstall clears any corrupted state.

---

## Getting Help

If you can't find the answer here:

1. **Check CLAUDE.md** — Architecture and design decisions
2. **Check SECURITY.md** — Security-related issues
3. **Upstream docs:**
   - [Docker Compose](https://docs.docker.com/compose/)
   - [Dockge](https://github.com/louislam/dockge)
   - Individual service docs (each stack's README has links)
4. **GitHub Issues:** <https://github.com/ivylikethevine/saffron/issues>

---

## Contributing Solutions

Found a solution to a problem not listed here? Please open an issue or PR on GitHub!
