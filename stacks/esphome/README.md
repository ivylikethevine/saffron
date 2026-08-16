# ESPHome

Easily create and manage ESP32-based IoT devices (temperature sensors, smart switches, etc.).

<https://esphome.io/>

<https://github.com/esphome/esphome>

<https://hub.docker.com/r/esphome/esphome>

## Architecture Compatibility

x64 and ARM64 supported

## Related Stacks

- **[homeassistant](../homeassistant/README.md)** — Integrates with Home Assistant for automation
- **[watchtower](../watchtower/README.md)** — Keeps ESPHome container updated

## Highlights

- **Web-based editor** for device configuration (no need to learn C++)
- **Over-the-air (OTA) updates** for deployed devices
- **First-class Home Assistant integration** for automations
- **Supports hundreds of components** (sensors, switches, lights, etc.)

### Setup

1. Access the web UI at `http://localhost:6052`
2. Create a new device configuration (YAML-based)
3. Flash to an ESP32/ESP8266 via USB
4. Device will connect to WiFi and receive OTA updates

### Common Use Cases

- Temperature and humidity sensors (DHT22, BME280)
- Motion sensors (PIR)
- Smart switches (relay control)
- Presence detection (WiFi)
- Custom environmental monitoring

#### `compose.yaml`

[filename](compose.yaml ':include :type=code')