# Upgrade & Migration Guide

How to safely upgrade Saffron, migrate to a new host, and keep your data intact.

## Automatic Updates

By default, Saffron automatically updates running containers:

- **pull_policy: always** — Pulls latest image on container start
- **watchtower** — Restarts containers with new images daily

**No action needed!** Updates happen automatically. Check stack logs if you notice behavior changes.

To disable auto-updates, see [Manual Control](#manual-control) below.

---

## Upgrading Saffron Core

### Update the Repository

```bash
cd /home/$USER/saffron
git pull
```

This updates:
- Compose files (new features, security fixes)
- Documentation (README, CLAUDE.md, etc.)
- GitHub Actions workflows
- Install/remove scripts

### Apply Changes to Stacks

Most updates don't require action. However, if a compose file changed:

```bash
# Option 1: Dockge will show a "Redeploy" button
# Click it to apply the new compose.yaml

# Option 2: Manual update
cd stacks/[affected-stack]
docker compose pull
docker compose up -d
```

**Data Safety:** Your config in `/containers/` and `/data/` is never touched by git. Updates only affect the compose files.

---

## Manual Control of Updates

### Disable Auto-Updates

Edit `stacks/[service]/compose.yaml`:

```yaml
services:
  [service]:
    pull_policy: never  # Don't auto-pull images
    # Watchtower won't restart this stack
```

Then restart:
```bash
docker compose -f stacks/[service]/compose.yaml up -d
```

### Disable Watchtower Entirely

```bash
cd stacks/watchtower
docker compose down

# Or remove it from autostart
docker compose -f stacks/watchtower/compose.yaml down -v
```

### Manually Update a Stack

```bash
cd stacks/[service]

# Pull the latest image
docker compose pull

# Restart with the new image
docker compose up -d

# Verify
docker compose logs [service]
```

### Pin to a Specific Image Version

Instead of `latest`, use a specific version:

```yaml
services:
  sonarr:
    image: linuxserver/sonarr:3.0.0  # Instead of :latest
```

Benefits:
- ✓ Predictable behavior
- ✓ Control when upgrades happen
- ✓ Can test before deploying

Drawbacks:
- ✗ Security updates must be applied manually
- ✗ Will eventually become unsupported

---

## Migrating to a New Host

### Step 1: Backup Current System

```bash
# Backup /containers (configs)
tar -czf ~/containers-backup.tar.gz /containers

# Backup /data (media) — optional if very large
tar -czf ~/data-backup.tar.gz $DATA_DIR

# Backup .env files
tar -czf ~/env-backup.tar.gz /home/$USER/saffron/stacks/*/.env

# Store backups somewhere safe (external drive, cloud storage)
```

### Step 2: Clone on New Host

```bash
cd ~
git clone https://github.com/ivylikethevine/saffron.git
cd saffron/resources
./install-saffron.sh  # Creates /containers and common.yaml
```

### Step 3: Restore Configs

```bash
# Stop everything
docker compose down

# Restore /containers
sudo rm -rf /containers
tar -xzf ~/containers-backup.tar.gz -C /

# Fix permissions
sudo chown -R 1000:1000 /containers
sudo chmod -R 755 /containers

# Restore .env files (your secrets)
cd /home/$USER/saffron/stacks
for dir in */; do
  if [ -f ~/env-backup/$dir/.env ]; then
    sudo cp ~/env-backup/$dir/.env $dir/
  fi
done

# Restore /data (media) if migrating storage
# This depends on your setup; may take hours for large media libraries
```

### Step 4: Start Stacks

```bash
# Go to Dockge (http://localhost:5001)
# Start stacks in this order:
# 1. servarr (sonarr, radarr, etc. — set up databases)
# 2. Indexing (prowlarr — needs servarr running)
# 3. Torrent (qbittorrentvpn)
# 4. Media services (plex, navidrome)
# 5. Everything else

# Or manually:
cd stacks/servarr && docker compose up -d
cd stacks/indexing && docker compose up -d
# ... etc
```

### Step 5: Verify

```bash
# Check all containers are running
docker ps | grep -E 'sonarr|plex|qbittorrent'

# Verify data is accessible
# - Plex: Check library counts (should match before)
# - Sonarr: Check episodes are linked
# - qBittorrent: Check torrent list (torrents survive migration!)
```

### Step 6: Update DNS

If running on a different IP:

```bash
# Old host: 192.168.1.10
# New host: 192.168.1.20

# Update router DNS or bookmarks
# Test: ping saffron.local (if using mDNS/avahi)
```

---

## Disk Space Management

As your homelab grows, media and logs consume disk space.

### Monitor Usage

```bash
# See disk usage
df -h /  # Root filesystem
df -h $DATA_DIR  # Media directory

# See what's using space
du -sh /containers/*/
du -sh $DATA_DIR/tv $DATA_DIR/movies
```

### Clean Up Old Data

```bash
# Remove Docker unused data
docker system prune -a

# Remove old logs from containers
docker logs --follow [container] | truncate -s 0 /var/log/docker.log

# Remove old episodes from /data/tv (if desired)
find $DATA_DIR/tv -mtime +365 -exec rm {} \;  # Remove files not accessed in 1 year
```

### Expand Storage

If /data is getting full:

```bash
# Option 1: Add another mount point
sudo mkdir /data2
sudo mount /dev/sdX1 /data2

# Update common.yaml to mount both:
# extends: ../common.yaml
# volumes:
#   - /data:/data:ro
#   - /data2:/data2:ro
# Then configure plex/sonarr/etc to use /data2 for new media

# Option 2: Migrate to external USB/NAS
# This is complex; see documentation for your media server
```

---

## Upgrading Individual Services

### Sonarr, Radarr, Lidarr Updates

These handle database migrations automatically:

```bash
cd stacks/servarr
docker compose pull
docker compose up -d

# Check logs for any errors
docker compose logs sonarr | tail -20
```

**If something breaks:**
```bash
# Rollback to previous version
cd stacks/servarr

# Edit compose.yaml
# image: linuxserver/sonarr:latest  → image: linuxserver/sonarr:4.0.0

# Restart
docker compose up -d
```

### Plex Updates

**Important:** Plex may require licensing/authentication after major version updates.

```bash
cd stacks/plex
docker compose pull
docker compose up -d

# Sign in to Plex settings if prompted
# Check that libraries still work
```

### Servarr Stack Updates (Sonarr/Radarr/Readarr/Bazarr)

Most updates are transparent:

```bash
cd stacks/servarr
docker compose pull
docker compose up -d
```

---

## Downgrading

**Proceed with caution!** Downgrading can cause data corruption.

```bash
# Pin to a previous version
cd stacks/[service]

# Edit compose.yaml
# image: linuxserver/sonarr:latest → image: linuxserver/sonarr:3.0.0

# Restart
docker compose down
docker compose up -d

# Verify database is intact
docker compose logs [service] | grep -i error
```

---

## Backing Up & Restoring

### Automated Backups

Saffron includes **backrest** for automated restic-based backups:

```bash
cd stacks/backrest
docker compose up -d

# Access at http://localhost:9898

# Configure:
# 1. Source: /containers (configs) and $DATA_DIR (media)
# 2. Destination: Local disk, AWS S3, Backblaze B2, etc.
# 3. Schedule: Daily

# Restore:
# Use backrest UI to restore from backup
```

### Manual Backups

```bash
# Backup just configs (fast, ~1GB)
tar -czf saffron-config-$(date +%Y%m%d).tar.gz /containers

# Backup everything (slow, hundreds of GB for media)
tar -czf saffron-full-$(date +%Y%m%d).tar.gz /containers $DATA_DIR

# Store on external drive
cp saffron-config-*.tar.gz /mnt/external-backup/
```

### Restoring from Backups

```bash
# Restore configs
sudo tar -xzf saffron-config-20240816.tar.gz -C /

# Fix permissions
sudo chown -R 1000:1000 /containers

# Restart stacks
docker compose -f stacks/*/compose.yaml up -d
```

---

## Version History

### v1.00 (Current)

- 21 documented stacks
- Auto-updating via pull_policy and watchtower
- Extensive documentation (CLAUDE.md, SECURITY.md, TROUBLESHOOTING.md)
- GitHub Actions validation

### Future Releases

See [ROADMAP.md](ROADMAP.md) for planned improvements and priorities.

---

## Troubleshooting Upgrades

### "Service won't start after update"

```bash
# Check logs
docker logs [container_name]

# Common issues:
# 1. Database schema changed (wait 1-2 minutes for migration)
# 2. New required environment variable
# 3. Port conflict with old container

# Solution: Restart the container
docker compose -f stacks/[service]/compose.yaml restart
```

### "Data corrupted after update"

If you have a backup (you do, right?):

```bash
# Stop the stack
docker compose -f stacks/[service]/compose.yaml down -v

# Restore from backup
tar -xzf backup-file.tar.gz -C /

# Restart
docker compose -f stacks/[service]/compose.yaml up -d
```

---

## Getting Help

- **TROUBLESHOOTING.md** — Common issues
- **CLAUDE.md** — Architecture & design
- Upstream service documentation (links in each stack's README)
- GitHub Issues: <https://github.com/ivylikethevine/saffron/issues>
