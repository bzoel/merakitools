"""
merakitools - ms.py
Billy Zoellers

CLI tools for managing Meraki networks based on Typer
"""
from typing import List, Optional
import time
from meraki.exceptions import APIError
import typer
from rich import inspect
from rich.progress import Progress, track
from merakitools.console import console, status_spinner
from merakitools.dashboardapi import dashboard
from merakitools.meraki_helpers import (
    find_network_by_name,
    find_org_id_by_device_serial,
)
from merakitools.formatting_helpers import table_with_columns
from merakitools.types import (
    DeviceModel,
    MSInterfaceMode,
    TrafficDirection,
    MSSTPGuardType,
)

app = typer.Typer()


@app.command()
def update_switchport(
    serial: str,
    port: Optional[List[int]] = typer.Option(None, min=1, max=52),
    port_range: Optional[str] = None,
    name: Optional[str] = None,
    enabled: Optional[bool] = None,
    poe_enabled: Optional[bool] = None,
    type: Optional[MSInterfaceMode] = None,
    vlan: Optional[int] = typer.Option(None, min=1, max=4094),
    voice_vlan: Optional[int] = typer.Option(None, min=1, max=4094),
    rtsp_enabled: Optional[bool] = None,
    stp_guard: Optional[MSSTPGuardType] = None,
    add_tag: Optional[List[str]] = None,
    remove_tag: Optional[List[str]] = None,
):
    """
    Update switchport(s)
    """
    # Validate device by trying to find OrgID
    org_id = find_org_id_by_device_serial(serial=serial)

    # Create range of ports
    ports = []
    if port_range:
        range_begin, range_end = port_range.split(":")
        ports = list(range(int(range_begin), int(range_end) + 1))

    # Add specified ports to the range
    for port in port:
        if port not in ports:
            ports.append(port)

    if len(ports) < 1:
        console.print("[red]No ports specified.")
        raise typer.Abort()

    # Iterate through each port in the range
    actions = []
    for port in track(ports, description="Processing switchports", console=console):
        try:
            port = dashboard.switch.getDeviceSwitchPort(serial=serial, portId=port)
        except APIError as err:
            console.print(err.message)
            raise typer.Abort()

        # Compile a dict of settings to be updated
        update = {}
        items = {
            "name": name,
            "enabled": enabled,
            "poeEnabled": poe_enabled,
            "type": type.value if type is not None else type,
            "vlan": vlan,
            "voiceVlan": voice_vlan,
            "rtspEnabled": rtsp_enabled,
            "stpGuard": stp_guard.value if stp_guard is not None else stp_guard,
        }
        for key, value in items.items():
            if value is not None:
                if value is not port[key]:
                    update[key] = value

        # Update tags
        if add_tag or remove_tag:
            update["tags"] = port["tags"]
            for tag in add_tag:
                if tag not in update["tags"]:
                    update["tags"].append(tag)
            for tag in remove_tag:
                if tag in update["tags"]:
                    update["tags"].remove(tag)

        # Create an action to be included in action batch
        if update:
            update_action = dashboard.batch.switch.updateDeviceSwitchPort(
                serial=serial, portId=port["portId"], **update
            )
            actions.append(update_action)

    # Use an action batch to execute in one run
    if actions:
        with status_spinner("Waiting for API batch to complete"):
            action_batch = dashboard.organizations.createOrganizationActionBatch(
                organizationId=org_id, actions=actions, confirmed=True
            )
            while True:
                if (
                    action_batch["status"]["completed"]
                    or action_batch["status"]["failed"]
                ):
                    break
                time.sleep(5)
                action_batch = dashboard.organizations.getOrganizationActionBatch(
                    organizationId=org_id, actionBatchId=action_batch["id"]
                )
        if action_batch["status"]["completed"]:
            console.print(f"[green]Updated {len(action_batch['actions'])} switchports")
            raise typer.Exit()
        console.print(f"[red]Failed to update switchports")
    else:
        console.print(f"[red]No changes to apply.")


@app.command()
def list_stacks(organization_name: str, network_name: str):
    """
    List switch stacks
    """
    # Get a list of switch stacks for specified network
    net = find_network_by_name(organization_name, network_name)
    with status_spinner("Getting switch stacks"):
        stacks = dashboard.switch.getNetworkSwitchStacks(networkId=net["id"])

    # Exit if no stacks are found
    if len(stacks) == 0:
        console.print("No switch stacks found.")
        raise typer.Exit()

    # Create a table of stacks
    table = table_with_columns(
        ["Serials"],
        title=f"Switch stacks in {net['name']}",
        first_column_name="Name",
    )
    for stack in stacks:
        table.add_row(stack["name"], f"{', '.join(stack['serials'])}")
    console.print(table)


@app.command()
def list_routing_interfaces(
    organization_name: str, network_name: str, serial: str, include_dhcp: bool = False
):
    """
    List L3 routed interfaces on an MS switch or stack
    """
    net = find_network_by_name(organization_name, network_name)
    with status_spinner("Getting routing interfaces"):
        try:
            routing_interfaces = dashboard.switch.getDeviceSwitchRoutingInterfaces(
                serial=serial
            )
            stack = False
        except APIError as err:
            if "switches in switch stack" in err.message["errors"][0].lower():
                console.print(f"This switch is a member of a stack.")
                stacks = dashboard.switch.getNetworkSwitchStacks(networkId=net["id"])
                stack = next(stack for stack in stacks if serial in stack["serials"])
                routing_interfaces = (
                    dashboard.switch.getNetworkSwitchStackRoutingInterfaces(
                        networkId=net["id"], switchStackId=stack["id"]
                    )
                )
            else:
                console.print(err.message)
                raise typer.Abort()

    if not routing_interfaces:
        console.print("No routing interfaces found.")
        raise typer.Exit()

    # Create and print a table
    cols = ["Subnet", "Interface IP", "VLAN ID"]
    if include_dhcp:
        cols.append("DHCP")
    table = table_with_columns(
        cols, title="Routing interfaces", first_column_name="Name"
    )
    for intf in routing_interfaces:
        rows = [intf["name"], intf["subnet"], intf["interfaceIp"], str(intf["vlanId"])]

        if include_dhcp:
            # Get DHCP info
            with status_spinner("Getting DHCP settings"):
                if stack:
                    dhcp = dashboard.switch.getNetworkSwitchStackRoutingInterfaceDhcp(
                        networkId=net["id"],
                        switchStackId=stack["id"],
                        interfaceId=intf["interfaceId"],
                    )
                else:
                    dhcp = dashboard.switch.getDeviceSwitchRoutingInterfaceDhcp(
                        serial=serial, interfaceId=intf["interfaceId"]
                    )

            # Format DHCP cell, and add to table rows
            if dhcp["dhcpMode"] == "dhcpDisabled":
                dhcp_formatted = "Disabled"
            elif dhcp["dhcpMode"] == "dhcpServer":
                if dhcp["dnsNameserversOption"] == "custom":
                    dhcp_formatted = (
                        "[bold]Server[/bold] DNS:"
                        f" {', '.join(dhcp['dnsCustomNameservers'])}"
                    )
                else:
                    dhcp_formatted = (
                        "[bold]Server[/bold]"
                        f" {dhcp['dnsNameserversOption'].capitalize()}"
                    )
            elif dhcp["dhcpMode"] == "dhcpRelay":
                dhcp_formatted = (
                    "[bold]Relay[/bold] Servers:"
                    f" {', '.join(dhcp['dhcpRelayServerIps'])}"
                )
            else:
                dhcp_formatted = dhcp["dhcpMode"].capitalize()
                inspect(dhcp)
            rows.append(dhcp_formatted)

        table.add_row(*rows)

    console.print(table)


@app.command()
def diag_switchport_traffic(
    organization_name: str,
    network_name: str,
    top: int = 100,
    sort_by: TrafficDirection = TrafficDirection.total,
    interface_mode: MSInterfaceMode = None,
    ignore_device_tag: List[str] = None,
    ignore_switchport_tag: List[str] = None,
):
    """
    Diagnose all switchports on a network of MS switches to find
    switchports that are top talkers at a given instant

    ** This command gathers a significant amount of data and may
    take some time to complete on larger networks **
    """
    net = find_network_by_name(organization_name, network_name)
    with status_spinner("Getting network devices"):
        devices = dashboard.networks.getNetworkDevices(net["id"])

    console.print(
        "Analyzing each switchport on the network, this may take a few minutes"
    )
    switchports = []
    with Progress(console=console) as progress:
        task_devices = progress.add_task(
            f"[blue]Processing {len(devices)} devices..", total=len(devices)
        )
        # Iterate through each switchport and add to the master switchport list
        for dev in devices:
            progress.update(
                task_devices,
                advance=1,
                description=f"[blue] Processing device '{dev['name']}'",
            )

            # Ignore non-MS devices
            if DeviceModel.MS not in dev["model"]:
                continue

            # Ignore devices with specific tags
            if ignore_device_tag and any(
                tag in dev["tags"] for tag in ignore_device_tag
            ):
                continue

            # Get switchport configuration and status
            switchport_configs = dashboard.switch.getDeviceSwitchPorts(
                serial=dev["serial"]
            )
            switchport_statuses = dashboard.switch.getDeviceSwitchPortsStatuses(
                serial=dev["serial"]
            )

            # Iterate through each switchport
            for swp_stat in switchport_statuses:
                # Ignore non-connected switchports
                if not swp_stat["status"] == "Connected":
                    continue

                # Create a combined switchport record (status+config)
                swp_cfg = next(
                    swp_cfg
                    for swp_cfg in switchport_configs
                    if swp_cfg["portId"] == swp_stat["portId"]
                )
                swp = swp_stat | swp_cfg
                swp["switch_name"] = dev["name"]

                # Ignore switchports with specific tags
                if ignore_switchport_tag and any(
                    tag in swp["tags"] for tag in ignore_switchport_tag
                ):
                    continue

                # Add combined switchport record to list of switchports
                switchports.append(swp)

        progress.update(
            task_devices, description=f"[green]Processed {len(devices)} devices."
        )

        # Sort all switchports based on the specified sort_by value (highest to lowest)
        switchports = sorted(
            switchports, key=lambda k: k["trafficInKbps"][sort_by.value], reverse=True
        )
        table = table_with_columns(
            [
                "Port",
                "Status",
                "Traffic (Total)",
                "Traffic (Sent)",
                "Traffic (Received)",
                "# of Clients",
                "CDP/LLDP",
                "Errors/Warnings",
            ],
            title=f"Top {top} switchports",
            first_column_name="Device",
        )

        for swp in switchports[:top]:
            # get Mbps values for traffic
            mb_size = 1024
            rounding_precision = 2
            total_mbps = round(
                swp["trafficInKbps"]["total"] / mb_size, rounding_precision
            )
            recv_mbps = round(
                swp["trafficInKbps"]["recv"] / mb_size, rounding_precision
            )
            sent_mbps = round(
                swp["trafficInKbps"]["sent"] / mb_size, rounding_precision
            )

            # get discovery data if available
            if "cdp" in swp.keys():
                discovery = swp["cdp"].get("systemName", None)
            elif "lldp" in swp.keys():
                discovery = swp["lldp"].get("systemName", None)
            else:
                discovery = None

            # collate error/warning data
            errorwarn = swp["errors"] + swp["warnings"]

            table.add_row(
                f"{swp['switch_name']}",
                f"{swp['portId']} ({swp['name']})",
                f"{swp['status']} ({swp['speed']})",
                f"{str(total_mbps)} Mbps",
                f"{str(sent_mbps)} Mbps",
                f"{str(recv_mbps)} Mbps",
                str(swp["clientCount"]),
                discovery,
                (", ").join(errorwarn),
            )

        console.print(table)
