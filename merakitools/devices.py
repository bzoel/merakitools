"""
merakitools - devices.py
Billy Zoellers

CLI tools for managing Meraki networks based on Typer
"""
from typing import List, Optional
from time import sleep
import typer
from rich import box
from rich.prompt import Confirm
from rich.table import Table
from merakitools.console import console, status_spinner
from merakitools.dashboardapi import dashboard
from merakitools.meraki_helpers import find_network_by_name, find_org_by_name
from merakitools.formatting_helpers import table_with_columns
from merakitools.types import DeviceModel, DeviceSortOptions

app = typer.Typer()


@app.command()
def list(
    organization_name: str,
    network_name: str,
    type: Optional[DeviceModel] = None,
    sort_by: Optional[DeviceSortOptions] = DeviceSortOptions.model,
    sort_reverse: bool = False,
):
    """
    List Meraki devices
    """
    # Get a list of all devices within the organization/network
    net = find_network_by_name(organization_name, network_name)
    devices = dashboard.networks.getNetworkDevices(net["id"])

    # Filter and sort
    if type:
        devices = [dev for dev in devices if type in dev["model"]]
    devices = sorted(devices, key=lambda k: k[sort_by.value], reverse=sort_reverse)

    # Display a table
    table = table_with_columns(
        ["Serial", "Network", "model", "tags", "Firmware"],
        title=f"Devices in {net['name']}",
        first_column_name="Name",
    )
    for device in devices:
        table.add_row(
            device["name"],
            device["serial"],
            net["name"],
            device["model"],
            ",".join(device["tags"]),
            device["firmware"],
        )
    console.print(table)


@app.command()
def update(
    serial: List[str],
    name: Optional[str] = None,
    address: Optional[str] = None,
    notes: Optional[str] = None,
    add_tag: Optional[List[str]] = None,
    remove_tag: Optional[List[str]] = None,
):
    """
    Update parameters of a Meraki device
    """
    if not serial:
        console.print("You must specify a device using `--serial`")
        raise typer.Abort()

    # Get each specified device
    devices = []
    for sn in serial:
        device = dashboard.devices.getDevice(serial=sn)
        console.print(f"Found device named {device.get('name', sn)} with serial {sn}")
        devices.append(device)

    # Confirm same name assignment to multiple devices
    if name and len(devices) > 1:
        console.print(f"[bold red]You specified a name for {len(devices)} devices")
        confirm = Confirm.ask(
            " Do you want to assign the same name to multiple devices?",
            console=console,
        )
        if not confirm:
            raise typer.Abort()

    for device in devices:
        device_sn = device["serial"]
        device_name = device.get("name", device_sn)
        updated_device = {"serial": device_sn}
        # Set new name
        if name:
            console.print(f" Renamed {device_name} to {name}")
            updated_device["name"] = name
            device_name = name

        # Set new address
        if address:
            console.print(f" Assigned address to {device_name}")
            updated_device["address"] = address
            updated_device["moveMapMarker"] = True

        # Set new notes
        if notes:
            console.print(f" Added notes to {device_name}")
            updated_device["notes"] = notes

        if add_tag or remove_tag:
            updated_device["tags"] = device["tags"]
        # Add tags
        if add_tag:
            for tag in add_tag:
                if tag not in updated_device["tags"]:
                    console.print(f" Added tag {tag} to {device_name}")
                    updated_device["tags"].append(tag)

        # Remove tags
        if remove_tag:
            for tag in remove_tag:
                if tag in updated_device["tags"]:
                    console.print(f" Removed tag {tag} to {device_name}")
                    updated_device["tags"].remove(tag)

        device = dashboard.devices.updateDevice(**updated_device)
        console.print(f"Updated device {device_name}")


@app.command()
def show_lldp(
    serial: Optional[List[str]] = None,
    organization_name: Optional[str] = None,
    network_name: Optional[str] = None,
):
    """
    Show CDP/LLDP information for Meraki device(s)
    """
    # Create a list of devices from the specified serial(s)
    devices = []
    for ser in serial:
        device = dashboard.devices.getDevice(serial=ser)
        devices.append(device)

    # If organization name and/or network name are specified, add devices from that scope
    if organization_name:
        if network_name:
            net = find_network_by_name(organization_name, network_name)
            add_devices = dashboard.networks.getNetworkDevices(net["id"])
        else:
            org = find_org_by_name(organization_name)
            add_devices = dashboard.organizations.getOrganizationDevices(org["id"])

        devices += add_devices

    elif network_name:
        console.print("You cannot specify a network name without an organization name.")
        raise typer.Abort()

    if not devices:
        console.print("No devices found.")
        raise typer.Abort()

    console.print(f"Getting CDP/LLDP data for {len(devices)} devices")
    for dev in devices:
        device_lldp = dashboard.devices.getDeviceLldpCdp(dev["serial"])
        if not device_lldp:
            console.print(
                f"No CDP/LLDP data found for {dev.get('name', dev['serial'])}"
            )
            continue

        table = table_with_columns(
            ["Type", "System Name", "Remote Port", "Mgmt Address"],
            title=f"{dev['name']} ({dev['serial']})",
            first_column_name="Port",
        )

        for port, data in device_lldp["ports"].items():
            if port:
                table.add_row(port)
            if "cdp" in data.keys():
                table.add_row(
                    "",
                    "CDP",
                    data["cdp"].get("deviceId"),
                    data["cdp"].get("portId"),
                    data["cdp"].get("address"),
                )
            if "lldp" in data.keys():
                table.add_row(
                    "",
                    "LLDP",
                    data["lldp"].get("systemName"),
                    data["lldp"].get("portId"),
                    data["lldp"].get("managementAddress"),
                )
        console.print(table)


@app.command()
def reboot(serial: List[str] = None):
    """
    Reboot device(s)
    """
    if not serial:
        console.print("No serial numbers entered.")
        raise typer.Abort()

    for sn in serial:
        reboot = dashboard.devices.rebootDevice(serial=sn)
        if reboot["success"]:
            console.print(f"Rebooted device with SN [bold]{sn}")
        else:
            console.print(f"Unabe to reboot device with SN [bold]{sn}")


@app.command()
def blink_led(
    serial: List[str] = None, duration: int = typer.Option(20, min=5, max=120)
):
    """
    Blink the LEDs of device(s)
    """
    if not serial:
        console.print("No serial numbers entered.")
        raise typer.Abort()

    for sn in serial:
        blink = dashboard.devices.blinkDeviceLeds(serial=sn, duration=duration)
        console.print(
            f"Blinking [bold]{sn}[/bold] LEDs for {blink['duration']} seconds"
        )


@app.command()
def ping(
    serial: str,
    target: str = typer.Option(None, help="Specify a target IP or FQDN"),
    count: int = typer.Option(5, min=1, max=5, help="Number of pings"),
):
    """
    Ping a Meraki device
    """
    with status_spinner("Pinging device"):
        # Create a new ping task
        params = {
            "serial": serial,
            "count": count,
        }
        if target is None:
            ping = dashboard.devices.createDeviceLiveToolsPingDevice(**params)
        else:
            params["target"] = target
            ping = dashboard.devices.createDeviceLiveToolsPing(**params)

        # Poll for an update on the ping ttask
        while ping["status"] in ["new", "running"]:
            params = {
                "serial": serial,
                "id": ping["pingId"],
            }
            if target is None:
                ping = dashboard.devices.getDeviceLiveToolsPingDevice(**params)
            else:
                ping = dashboard.devices.getDeviceLiveToolsPing(**params)
            sleep(1)

    # Use 'Meraki cloud' if no target is specified
    if target is None:
        target = "Meraki cloud"

    # Emulate UNIX ping display with statistics
    table = Table(
        show_header=False,
        box=box.HEAVY_EDGE,
        title=f"Ping from Meraki device [bold]{serial}",
    )
    if "replies" in ping["results"].keys():
        for reply in ping["results"]["replies"]:
            table.add_row(
                f"{reply['size']} bytes from {target}:"
                f" icmp_seq={reply['sequenceId']} time={reply['latency']}"
            )
    table.add_row(f"\n--- {target} ping statistics ---")
    table.add_row(
        f"{ping['results']['sent']} packets transmitted,"
        f" {ping['results']['received']} packets received,"
        f" {ping['results']['loss']['percentage']}% packet loss"
    )
    if "latencies" in ping["results"].keys():
        table.add_row(
            "round-trip min/avg/max ="
            f" {ping['results']['latencies']['minimum']}/{ping['results']['latencies']['average']}/{ping['results']['latencies']['maximum']}"
        )
    console.print(table)
