---
avahi
---

# Avahi

- <details>
      <h3>WebUI Dashboard</h3>
      <img src="resources/screenshots/netdata.webp" alt="netdata ui screenshot"/>
      <h4>Configure Streaming between Nodes</h4>
      <h5>Initial Setup, per <a href="https://learn.netdata.cloud/docs/streaming/streaming-configuration-reference">netdata docs</a></h5>
      <ul>To get the <code>API_KEY</code> run <code>docker container exec netdata cat /var/lib/netdata/registry/netdata.public.unique.id</code></ul>
      <ul>Then, replace <code>API_KEY</code> in <code>parent/stream.conf</code> and <code>child/stream.conf</code> with the value from above, as well as updating the <code>PARENT_IP_ADDRESS</code> in <code>child/stream.conf</code></ul>

      <h5>For the parent node, mount:</h5>
      <ul><code>/home/$USER/saffron/stacks/netdata/parent/stream.conf</code></ul>
      <ul><code>/home/$USER/saffron/stacks/netdata/parent/netdata.conf</code></ul>

      <h5> For child nodes, mount:</h5>
      <ul><code>/home/$USER/saffron/stacks/netdata/child/stream.conf</code></ul>
      <ul><code>/home/$USER/saffron/stacks/netdata/child/netdata.conf</code></ul>

      <p>Note: changes to the <code>stream.conf</code> files will not be committed, but the files remain in the repo unchanged per <code>git update-index --assume-unchanged [<file> ...]</code> <a href="https://stackoverflow.com/questions/3319479/can-i-git-commit-a-file-and-ignore-its-content-changes">See Reference</a></p><p>To continue tracking: <code>git update-index --no-assume-unchanged [<file> ...]</code></p>
      <img alt="x64 Version" src="https://img.shields.io/docker/v/netdata/netdata/stable?arch=amd64&label=x64">
      <img alt="Arm64 Version" src="https://img.shields.io/docker/v/netdata/netdata/stable?arch=arm64&label=arm64">

    </details>
  (https://learn.netdata.cloud/docs/installing/docker)
