# degoog

Self-hosted search engine and results aggregator with an extension system.

<https://github.com/degoog-org/degoog>

<https://github.com/degoog-org/degoog/pkgs/container/degoog>

Set `DEGOOG_SETTINGS_PASSWORDS` in `.env` before exposing it: an unlocked instance lets anyone install extensions, which run code on the server.

## Architecture Compatibility

x64 and arm64 (multi-arch image on ghcr.io).

#### `compose.yaml`

[filename](compose.yaml ':include :type=code')

#### `.env.public`

[filename](.env.public ':include :type=code')
