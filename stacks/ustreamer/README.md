# Ustreamer

Lightweight, high-performance IP camera streaming server for USB cameras and video devices.

<https://github.com/pikvm/ustreamer>

<https://pikvm.org/> (part of PiKVM project)

## Architecture Compatibility

x64 and ARM64 supported (optimized for Raspberry Pi)

## Related Stacks

- **[homeassistant](../homeassistant/README.md)** — Integrates with Home Assistant for monitoring
- **[watchtower](../watchtower/README.md)** — Keeps ustreamer updated

## Features

- **Ultra-low latency** video streaming (~0.1 seconds)
- **Minimal CPU/memory usage** (ideal for embedded systems)
- **MJPEG and H.264 support**
- **Web-based viewing** (no plugins required)
- **Resolution/framerate/quality tuning** via environment variables

## Setup

1. Connect USB camera to host system
2. Identify device: `ls -la /dev/video*`
3. Update compose.yaml device mapping (currently `/dev/video0`)
4. Access at `http://localhost:8083`

### Configuration

The compose file includes tuning options:
- Resolution: `1280x720` (adjust in command)
- Framerate: `1` fps (adjust in command)
- Quality: `60` (0-100, higher = better quality)
- Bitrate: `32` (for JPEG compression)

### Common Devices

- USB webcams (most common)
- Raspberry Pi Camera (with libcamera on RPi)
- Security cameras (RTSP via IP-to-USB converters)

#### `compose.yaml`

[filename](compose.yaml ':include :type=code')