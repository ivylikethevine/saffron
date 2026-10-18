#!/usr/bin/env python3
"""Print a Mermaid diagram of the network topology in stacks/*/compose.yaml.

Services are grouped by the bridge they join, by the gluetun container they
route through (`network_mode: service:<name>`) and by host networking.

Usage:
    python3 resources/generate-topology.py
"""

import sys
from collections import defaultdict
from pathlib import Path

import yaml

# Per-stack bridges named `bridge` are private to their stack; the diagram
# shows what crosses stack boundaries.
PRIVATE_NETWORKS = {"bridge"}


def node(name):
    return name.replace("/", "_").replace("-", "_")


def parse_stacks(stacks_dir="stacks"):
    count = 0
    networks = defaultdict(set)
    vpn_routes = defaultdict(set)
    host_mode = set()
    for path in sorted(Path(stacks_dir).glob("*/compose.yaml")):
        compose = yaml.safe_load(path.read_text()) or {}
        for name, config in compose.get("services", {}).items():
            full = f"{path.parent.name}/{name}"
            count += 1
            for net in config.get("networks") or []:
                if net not in PRIVATE_NETWORKS:
                    networks[net].add(full)
            mode = config.get("network_mode", "")
            if mode.startswith("service:"):
                vpn_routes[mode[len("service:"):]].add(full)
            elif mode == "host":
                host_mode.add(full)
    return count, networks, vpn_routes, host_mode


def subgraph(lines, ident, title, members):
    lines.append(f"    subgraph {ident}[{title}]")
    lines.extend(f'        {node(s)}["{s}"]' for s in sorted(members))
    lines.append("    end")


def main():
    count, networks, vpn_routes, host_mode = parse_stacks()
    if not count:
        sys.exit("No services found in stacks/*/compose.yaml")

    lines = ["graph TB"]
    for net, members in sorted(networks.items()):
        subgraph(lines, node(net), net, members)
    for host, members in sorted(vpn_routes.items()):
        subgraph(lines, f"VPN_{node(host)}", f"VPN: {host}", members)
    if host_mode:
        subgraph(lines, "HostMode", "Host Network Mode", host_mode)
    print("\n".join(lines))

    print(f"\n{count} services; bridges: {', '.join(sorted(networks))}; "
          f"VPN hosts: {', '.join(sorted(vpn_routes))}", file=sys.stderr)


if __name__ == "__main__":
    main()
