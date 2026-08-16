#!/usr/bin/env python3
"""
Generate network topology diagram from Saffron compose files.

Parses stacks/*/compose.yaml to identify:
- Services using external networks (servarr_bridge, etc.)
- VPN-routed services (network_mode: service:gluetun)
- Direct host-mode services
- Service dependencies

Outputs a Mermaid diagram to stdout that can be embedded in CLAUDE.md.
"""

import yaml
from pathlib import Path
from collections import defaultdict
import sys


def parse_stacks(stacks_dir="stacks"):
    """Parse all compose.yaml files and extract topology info."""
    services = {}
    networks = defaultdict(set)
    vpn_routes = defaultdict(list)
    host_mode = []
    dependencies = defaultdict(set)

    for stack_path in sorted(Path(stacks_dir).glob("*/compose.yaml")):
        stack_name = stack_path.parent.name
        with open(stack_path) as f:
            try:
                compose = yaml.safe_load(f)
            except yaml.YAMLError as e:
                print(f"Warning: Failed to parse {stack_path}: {e}", file=sys.stderr)
                continue

        if not compose or "services" not in compose:
            continue

        stack_services = compose.get("services", {})

        for service_name, service_config in stack_services.items():
            full_name = f"{stack_name}/{service_name}"
            services[full_name] = service_config

            # Track external networks
            if "networks" in service_config:
                svc_networks = service_config["networks"]
                if isinstance(svc_networks, list):
                    for net in svc_networks:
                        networks[net].add(full_name)
                elif isinstance(svc_networks, dict):
                    for net in svc_networks.keys():
                        networks[net].add(full_name)

            # Track VPN routing
            if "network_mode" in service_config:
                mode = service_config["network_mode"]
                if mode.startswith("service:"):
                    vpn_host = mode.replace("service:", "")
                    vpn_routes[vpn_host].append(full_name)

            # Track host mode
            if service_config.get("network_mode") == "host":
                host_mode.append(full_name)

            # Track dependencies
            if "depends_on" in service_config:
                deps = service_config["depends_on"]
                if isinstance(deps, list):
                    for dep in deps:
                        dependencies[full_name].add(dep)
                elif isinstance(deps, dict):
                    for dep in deps.keys():
                        dependencies[full_name].add(dep)

    return services, networks, vpn_routes, host_mode, dependencies


def generate_mermaid_diagram(services, networks, vpn_routes, host_mode, dependencies):
    """Generate Mermaid diagram of the network topology."""
    lines = [
        "graph TB",
        "    subgraph Bridge[Default Bridge]",
        "        direction TB",
    ]

    # Collect services per bridge
    bridge_services = defaultdict(list)
    for net, svcs in networks.items():
        for svc in svcs:
            bridge_services[net].append(svc)

    # Add servarr_bridge services
    if "servarr_bridge" in networks:
        lines.append("    end")
        lines.append("    subgraph Servarr[servarr_bridge]")
        for svc in sorted(networks["servarr_bridge"]):
            safe_name = svc.replace("/", "_").replace("-", "_")
            lines.append(f"        {safe_name}[\"{svc}\"]")

    # Add VPN-routed services
    for vpn_host, routed_svcs in sorted(vpn_routes.items()):
        if routed_svcs:
            safe_host = vpn_host.replace("/", "_").replace("-", "_")
            lines.append("    end")
            lines.append(f"    subgraph VPN{safe_host.replace('_', '')}[VPN: {vpn_host}]")
            for svc in sorted(routed_svcs):
                safe_name = svc.replace("/", "_").replace("-", "_")
                lines.append(f"        {safe_name}[\"{svc}\"]")

    # Add host-mode services
    if host_mode:
        lines.append("    end")
        lines.append("    subgraph HostMode[Host Network Mode]")
        for svc in sorted(host_mode):
            safe_name = svc.replace("/", "_").replace("-", "_")
            lines.append(f"        {safe_name}[\"{svc}\"]")

    lines.append("    end")

    # Add edges for dependencies within stacks
    for svc, deps in sorted(dependencies.items()):
        safe_svc = svc.replace("/", "_").replace("-", "_")
        for dep in sorted(deps):
            # Only draw intra-stack deps (same stack name before /)
            svc_stack = svc.split("/")[0]
            dep_stack = dep.split("/")[0] if "/" in dep else svc_stack
            if svc_stack == dep_stack and "/" in dep:
                safe_dep = dep.replace("/", "_").replace("-", "_")
                lines.append(f"    {safe_svc} -->|depends_on| {safe_dep}")

    return "\n".join(lines)


def main():
    """Parse stacks and generate topology diagram."""
    services, networks, vpn_routes, host_mode, dependencies = parse_stacks()

    if not services:
        print("No services found in stacks/*/compose.yaml", file=sys.stderr)
        sys.exit(1)

    diagram = generate_mermaid_diagram(services, networks, vpn_routes, host_mode, dependencies)
    print(diagram)

    # Also print summary to stderr
    print(f"\nSummary:", file=sys.stderr)
    print(f"  Total services: {len(services)}", file=sys.stderr)
    print(f"  External networks: {', '.join(sorted(networks.keys()))}", file=sys.stderr)
    print(f"  VPN-routed hosts: {', '.join(sorted(vpn_routes.keys()))}", file=sys.stderr)
    print(f"  Host-mode services: {', '.join(sorted(host_mode))}", file=sys.stderr)


if __name__ == "__main__":
    main()
