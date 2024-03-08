# Netdata

<https://learn.netdata.cloud/docs/installing/docker>

## Architecture Compatibility

![x64 Version](https://img.shields.io/docker/v/netdata/netdata/stable?arch=amd64&label=x64) ![Arm64 Version](https://img.shields.io/docker/v/netdata/netdata/stable?arch=arm64&label=arm64)

### WebUI Dashboard

![Netdata UI](../../resources/screenshots/netdata.webp)

#### Configure Streaming between Nodes

##### Initial Setup, per [netdata docs](https://learn.netdata.cloud/docs/streaming/streaming-configuration-reference)

To get the `API_KEY` run `docker container exec netdata cat /var/lib/netdata/registry/netdata.public.unique.id`

Then, replace `API_KEY` in `parent/stream.conf` and `child/stream.conf` with the value from above, as well as updating the `PARENT_IP_ADDRESS` in `child/stream.conf`

##### For the parent node, mount:

`/home/$USER/saffron/stacks/netdata/parent/stream.conf`

`/home/$USER/saffron/stacks/netdata/parent/netdata.conf`

##### For child nodes, mount:

`/home/$USER/saffron/stacks/netdata/child/stream.conf`

`/home/$USER/saffron/stacks/netdata/child/netdata.conf`

Note: changes to the `stream.conf` files will not be committed, but the files remain in the repo unchanged per `git update-index --assume-unchanged [ ...]` [See Reference](https://stackoverflow.com/questions/3319479/can-i-git-commit-a-file-and-ignore-its-content-changes)

To continue tracking: `git update-index --no-assume-unchanged [ ...]`
