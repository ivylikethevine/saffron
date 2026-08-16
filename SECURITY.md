# Saffron Security Model

## Overview

Saffron is designed for **trusted homelab environments** where:
- Network is private (not exposed to public internet by default)
- Users are trusted (no untrusted users on the system)
- Goal is convenience and functionality over defense-in-depth

This document outlines security considerations, trade-offs, and recommendations.

## Security Architecture

### Threat Model

**In Scope:**
- Prevent accidental misconfiguration that exposes services
- Document intentional privilege elevation (and why)
- Best practices for credential management

**Out of Scope:**
- Defense against compromised host OS
- Container escape attacks
- Supply chain attacks (malicious base images)

### Network Boundaries

```
┌─────────────────────┐
│   Saffron Host      │
│  ┌───────────────┐  │
│  │  Docker      │  │  ← Trusted: private LAN only
│  │  Containers  │  │     (unless explicitly port-forwarded)
│  └───────────────┘  │
└─────────────────────┘
         ↓
   Private LAN (trusted)
```

**Assumptions:**
- Host is on trusted LAN (no untrusted users)
- Docker daemon is only accessible to trusted users (docker group)
- Port mappings default to `localhost` (no external binding)

## Privilege Analysis

### Services Requiring Elevated Privileges

#### esphome (privileged: true)
- **Why:** Needs direct hardware access to serial ports for ESP32 flashing
- **Risk:** Can escape container isolation
- **Mitigation:** Only needed during device flashing, could be split into separate container
- **Recommendation:** Keep as-is for homelab

#### homeassistant (privileged: true)
- **Why:** Needs access to `/run/dbus` for system integration (bluetooth, other devices)
- **Risk:** Can escape container isolation
- **Mitigation:** dbus access is read-only where possible
- **Recommendation:** Consider splitting dbus access into separate privileged container if concerned

#### octoprint (privileged: true)
- **Why:** Needs access to USB serial port for 3D printer communication
- **Risk:** Can escape container isolation
- **Mitigation:** USB device could be mounted more precisely (instead of full privileged)
- **Recommendation:** Could be improved by mounting `/dev/ttyUSB*` instead of `privileged: true`

#### torrent (cap_add: NET_ADMIN)
- **Why:** gluetun VPN container needs network admin to set up wireguard interface
- **Risk:** Allows network manipulation but contained to VPN container
- **Mitigation:** Only the VPN container has this cap, not the torrent client
- **Recommendation:** This is the minimal capability needed for VPN routing

#### bitmagnet (cap_add: NET_ADMIN)
- **Why:** gluetun VPN container (same as torrent)
- **Risk:** Contained to VPN container
- **Mitigation:** Same as torrent
- **Recommendation:** Acceptable trade-off

### Services NOT Requiring Privileges (Good!)
- linuxserver.io images (sonarr, radarr, prowlarr, lidarr, bazarr): Run as PUID:PGID (typically 1000:1000)
- Most other services: Unprivileged with PUID/PGID via `common.yaml`

## Secrets Management

### Current Approach
1. **Environment variables in compose files:** ✗ Never secret data
2. **`.env` files:** ✓ User-created, gitignored, holds actual secrets
3. **`.env.public` templates:** ✓ Documented in git, shows what's needed

### Recommended Practices

#### For Single User
```bash
# Create .env from .env.public template
cd stacks/torrent
cp .env.public .env
# Edit .env with actual VPN credentials (never commit this)
```

#### For Team/Multi-User
Consider using git-crypt or bitwarden-cli:

```bash
# Option 1: git-crypt (encrypt specific files in git)
git-crypt init
echo ".env filter=git-crypt diff=git-crypt" >> .gitattributes
git add .gitattributes

# Now commit .env files encrypted
git add stacks/*/.env
git commit -m "Add encrypted env files"
```

#### Secrets to Watch
- **VPN credentials** (torrent, bitmagnet): Private keys should never be committed
- **API keys** (speedtest-tracker, navidrome): Can be rotated if leaked
- **Passwords** (database, apps): Should be strong and unique
- **Tokens** (github, etc.): Should be revoked if leaked

**Never commit:**
- `.env` files with real credentials
- Private keys
- API tokens
- Database passwords

## Volume Security

### Sensitive Volume Mounts

| Stack | Mount | Risk | Mitigation |
|-------|-------|------|-----------|
| homeassistant | `/run/dbus:ro` | dbus access | Read-only; only needed for device integration |
| bitmagnet | `/root/.config` | Home directory config | Intentional; app needs this location |
| docsify | `/home/$USER/saffron:ro` | Source code access | Read-only; only for serving docs |
| octoprint | `/dev/ttyUSB*` (via privileged) | Serial port | Necessary for printer control |

**Best practice:** Use read-only (`:ro`) mounts where possible.

## Network Port Exposure

### Default Behavior
- All ports are bound to `127.0.0.1` (localhost only) ✓
- Accessible only from the host machine
- Not exposed to LAN by default

### If Exposing to LAN
```yaml
# NOT recommended, but if needed:
ports:
  - "0.0.0.0:8080:8080"  # Accessible from anywhere on LAN
```

**Better approach:** Use a reverse proxy (traefik, nginx) with:
- Authentication (OAuth, basic auth)
- TLS/HTTPS
- Rate limiting

### If Exposing to Internet
**High risk!** Requires:
1. VPN or SSH tunnel (recommended)
2. OR reverse proxy with strong auth + TLS
3. OR cloudflare tunneling
4. Consider limiting which services are exposed (heimdall, docsify only?)

## Image Security

### Current Approach
- `pull_policy: always`: Forces re-pull on every start
- Watchtower: Updates running containers daily
- **No image signing/verification**

### Recommended Improvements
1. **Scan images for vulnerabilities:**
   ```bash
   docker run --rm -v /var/run/docker.sock:/var/run/docker.sock \
     aquasec/trivy image linuxserver/sonarr:latest
   ```

2. **Pin to specific versions instead of `latest`:**
   ```yaml
   image: linuxserver/sonarr:3.0.0  # Instead of :latest
   ```

3. **Use trusted image sources:**
   - linuxserver.io: Widely used, regularly updated ✓
   - Official Docker Library: Well-maintained ✓
   - GHCR (GitHub): Depends on source project
   - Avoid: Random Docker Hub images from unknown sources

4. **Image signature verification (future):**
   ```bash
   # Docker Content Trust (beta)
   export DOCKER_CONTENT_TRUST=1
   docker pull linuxserver/sonarr  # Fails if image not signed
   ```

## Database Security

### Databases in Saffron

| Service | Database | Default | Risk |
|---------|----------|---------|------|
| bitmagnet | PostgreSQL | Password in `.env.public` | Should be changed at first run |
| most *arr apps | SQLite | File in `/containers/` | No authentication; relies on container isolation |

### Recommendations
- Bitmagnet: Use strong password in `.env` (generated passphrase recommended)
- SQLite stacks: Accept that database is accessed only from container
- No direct database access from host (by design)

## Firewall Recommendations

For production homelab:

```bash
# Assume host is behind NAT router
# Set docker iptables rules to restrict port access:

# Option 1: UFW (Uncomplicated Firewall)
sudo ufw default deny incoming
sudo ufw allow from 192.168.1.0/24 to any port 5001  # dockge from LAN
sudo ufw allow from 192.168.1.100 to any port 8080   # qbittorrent from one machine

# Option 2: Configure each service to bind to specific IP
# (modify compose files to bind to 192.168.1.x instead of 127.0.0.1)
```

## Compliance & Legal

- **GDPR:** Saffron stores media files; ensure they're properly licensed
- **DMCA:** Circumventing DRM (e.g., streaming services) may violate local laws
- **Copyright:** Use subscriptions (spotify, netflix) where available

## Incident Response

### If a Container is Compromised

1. **Stop the container:**
   ```bash
   docker-compose -f stacks/[service]/compose.yaml down
   ```

2. **Review logs:**
   ```bash
   docker logs [container_name] > /tmp/logs.txt
   ```

3. **Delete the image and re-pull:**
   ```bash
   docker rmi [image_name]
   docker-compose -f stacks/[service]/compose.yaml up -d
   ```

4. **Check if other containers were affected** (same network)

### If the Host is Compromised

Saffron cannot protect against host compromise. Standard remediation:
- Isolate host from network
- Backup important data
- Reinstall OS
- Restore from backup

## Security Checklist

Before going to production:

- [ ] Change default passwords in `.env` files
- [ ] Use strong passwords (consider password manager)
- [ ] Review exposed ports; disable unnecessary ones
- [ ] Enable firewall (ufw or router ACLs)
- [ ] Review volume mounts; ensure no unintended access
- [ ] Don't commit `.env` files to git
- [ ] Consider git-crypt for team deployments
- [ ] Regularly update images (watchtower does this)
- [ ] Backup config and media regularly (backrest)
- [ ] Monitor logs for errors (dozzle)

## Future Improvements

- [ ] Add AppArmor profiles for privileged containers
- [ ] Document reverse proxy setup (traefik)
- [ ] Add network policies (isolate untrusted containers)
- [ ] Support for image signing/verification
- [ ] Secrets rotation automation
- [ ] Automated backup encryption
