"""
merakitools - mr.py
Billy Zoellers

CLI tools for managing Meraki networks based on Typer
"""
from meraki.exceptions import APIError
from rich.prompt import Confirm
import typer
from typing import List, Optional

from typer import params
from merakitools.console import console
from merakitools.dashboardapi import dashboard
from merakitools.meraki_helpers import api_req, find_network_by_name, find_org_by_name
from merakitools.formatting_helpers import table_with_columns
from merakitools.types import (
    DeviceModel,
    MRSSIDIPAssignmentMode,
    ProductType,
    MRSSIDAuthMode,
    MRSSIDEncryptionMode,
    MRSSIDWPAEncrytionMode,
)
from rich import inspect
from rich.progress import Progress

app = typer.Typer()


@app.command()
def list_ssid(
    organization_name: str,
    network_name: str,
    include_disabled: bool = typer.Option(False, "--include-disabled"),
    include_psk: bool = False,
):
    """
    List configured SSIDs for a network
    """
    # Get network and confirm it is wireless
    net = find_network_by_name(organization_name, network_name)
    if ProductType.wireless not in net["productTypes"]:
        console.print(f"This network does not contain any MR devices")
        raise typer.Abort()

    # Get list of SSIDs
    ssids = dashboard.wireless.getNetworkWirelessSsids(net["id"])
    if not include_disabled:
        ssids = [ssid for ssid in ssids if ssid["enabled"]]

    # Create table of SSIDs
    table = table_with_columns(
        [
            "Enabled",
            "Authentication",
            "Mode",
            "VLAN Tag",
            "Band",
            "Visible",
            "Availability",
        ],
        title=f"SSIDs for {net['name']}",
        first_column_name="Name",
    )
    for ssid in ssids:
        table.add_row(
            ssid["name"],
            "[green]Enabled" if ssid["enabled"] else "[red]Disabled",
            f"{ssid.get('encryptionMode', 'open')} / {ssid['authMode']}"
            + f" [bold]{ssid.get('psk') if include_psk else ''}",
            ssid["ipAssignmentMode"],
            str(ssid.get("defaultVlanId")) if ssid.get("useVlanTagging") else "none",
            ssid["bandSelection"],
            "[green]Visible" if ssid["visible"] else "[red]Not visible",
            "All APs"
            if ssid["availableOnAllAps"]
            else f"Tags: {', '.join(ssid['availabilityTags'])}",
        )
    console.print(table)


@app.command()
def list_rf(organization_name: str, network_name: str):
    """
    List RF settings for a network
    """
    # Get network and confirm it is wireless
    net = find_network_by_name(organization_name, network_name)
    if ProductType.wireless not in net["productTypes"]:
        console.print(f"This network does not contain any MR devices")
        raise typer.Abort()

    # Maintain a dict of RF profiles
    rf_profiles = {}

    # Get list of all wireless devices
    with console.status("Accessing API..."):
        # Get sorted list of MR devices
        devices = dashboard.networks.getNetworkDevices(net["id"])
        devices = [device for device in devices if DeviceModel.MR in device["model"]]
        devices = sorted(devices, key=lambda k: k["name"], reverse=False)

        # Create a table of MR devices with RF info from API
        table = table_with_columns(
            [
                "RF Profile",
                "2.4Ghz Manual Settings",
                "2.4Ghz Actual",
                "5Ghz Manual Settings",
                "5Ghz Actual",
            ],
            title=f"RF Settings for {net['name']}",
            first_column_name="AP Name",
        )
        for device in devices:
            # Get RF settings and current status
            device_rf = dashboard.wireless.getDeviceWirelessRadioSettings(
                serial=device["serial"]
            )
            device_status = dashboard.wireless.getDeviceWirelessStatus(
                serial=device["serial"]
            )

            # Get RF profile from stored data or API
            rf_profile_id = device_rf.get("rfProfileId")
            if rf_profile_id:
                if rf_profile_id not in rf_profiles:
                    rf_profiles[
                        rf_profile_id
                    ] = dashboard.wireless.getNetworkWirelessRfProfile(
                        net["id"], rf_profile_id
                    )

            # Get first SSID on each band for actual status info
            try:
                twoFour_status = next(
                    bss
                    for bss in device_status["basicServiceSets"]
                    if bss["enabled"]
                    and bss["broadcasting"]
                    and bss["band"] == "2.4 GHz"
                )
            except StopIteration:
                # No 2.4Ghz enabled
                twoFour_status = None
            try:
                five_status = next(
                    bss
                    for bss in device_status["basicServiceSets"]
                    if bss["enabled"] and bss["broadcasting"] and bss["band"] == "5 GHz"
                )
            except StopIteration:
                # No 5Ghz enabled
                five_status = None

            # Readable string for 2.4GHz settings
            twoFourGhzSettings = []
            if device_rf["twoFourGhzSettings"]["channel"]:
                twoFourGhzSettings.append(
                    f"ch {device_rf['twoFourGhzSettings']['channel']}"
                )
            if device_rf["twoFourGhzSettings"]["targetPower"] == -1.0:
                twoFourGhzSettings = ["disabled"]
            elif device_rf["twoFourGhzSettings"]["targetPower"]:
                twoFourGhzSettings.append(
                    f"{device_rf['twoFourGhzSettings']['targetPower']} dBm"
                )

            # Readable string for 5GHz settings
            fiveGhzSettings = []
            if device_rf["fiveGhzSettings"]["channel"]:
                fiveGhzSettings.append(f"ch {device_rf['fiveGhzSettings']['channel']}")
            if device_rf["fiveGhzSettings"]["targetPower"] == -1.0:
                fiveGhzSettings = ["disabled"]
            elif device_rf["fiveGhzSettings"]["targetPower"]:
                fiveGhzSettings.append(
                    f"{device_rf['fiveGhzSettings']['targetPower']} dBm"
                )

            table.add_row(
                device["name"],
                rf_profiles[rf_profile_id]["name"] if rf_profile_id else "None",
                " / ".join(twoFourGhzSettings),
                f"ch {twoFour_status['channel']} / {twoFour_status['power']}"
                if twoFour_status
                else "Not broadcasting",
                " / ".join(fiveGhzSettings),
                f"ch {five_status['channel']} / {five_status['power']}"
                if five_status
                else "Not broadcasting",
            )
    console.print(table)


@app.command()
def list_rf_profiles(organization_name: str, network_name: str):
    """
    List RF profiles for a network
    """
    # Get network and confirm it is wireless
    net = find_network_by_name(organization_name, network_name)
    if ProductType.wireless not in net["productTypes"]:
        console.print(f"This network does not contain any MR devices")
        raise typer.Abort()

    # Get RF profiles
    with console.status("Accessing API..."):
        rf_profiles = dashboard.wireless.getNetworkWirelessRfProfiles(
            net["id"], includeTemplateProfiles=True
        )
        if not rf_profiles:
            console.print("No RF Profiles found")
            raise typer.Abort()

        table = table_with_columns(
            [
                "Client Balancing",
                "Band Settings",
                "2.4GHz Power",
                "2.4GHz Min. Bitrate",
                "2.4GHz AutoChannel",
                "5GHz Power",
                "5GHz Min. Bitrate",
                "5GHz AutoChannel",
                "5GHz Width",
            ],
            title=f"RF Profiles for {net['name']}",
            first_column_name="Name",
        )

        for profile in rf_profiles:
            twoFourGhzChannels = [
                str(int) for int in profile["twoFourGhzSettings"]["validAutoChannels"]
            ]
            fiveGhzChannels = [
                str(int) for int in profile["fiveGhzSettings"]["validAutoChannels"]
            ]

            table.add_row(
                profile["name"],
                "[green]Enabled"
                if profile["clientBalancingEnabled"]
                else "[red]Disabled",
                f"{profile['apBandSettings']['bandOperationMode']} / {'[green]Band Steering Enabled' if profile['apBandSettings']['bandSteeringEnabled'] else '[red]Band Steering Disabled'}"
                if profile["bandSelectionType"] == "ap"
                else "per SSID",
                f"{profile['twoFourGhzSettings']['minPower']}-{profile['twoFourGhzSettings']['maxPower']}dBm",
                f"{profile['twoFourGhzSettings']['minBitrate']}Mbps"
                if profile["minBitrateType"] == "band"
                else "per SSID",
                ", ".join(twoFourGhzChannels),
                f"{profile['fiveGhzSettings']['minPower']}-{profile['fiveGhzSettings']['maxPower']}dBm",
                f"{profile['fiveGhzSettings']['minBitrate']}Mbps"
                if profile["minBitrateType"] == "band"
                else "per SSID",
                ", ".join(fiveGhzChannels),
                profile["fiveGhzSettings"]["channelWidth"]
                if profile["fiveGhzSettings"]["channelWidth"] == "auto"
                else f"{profile['fiveGhzSettings']['channelWidth']}MHz",
                end_section=True,
            )
        console.print(table)


@app.command()
def list_mesh(organization_name: str, network_name: str):
    """
    List mesh status for a network
    """
    # Get network and confirm it is wireless
    net = find_network_by_name(organization_name, network_name)
    if ProductType.wireless not in net["productTypes"]:
        console.print(f"This network does not contain any MR devices")
        raise typer.Abort()

    # Get network mesh status
    with console.status("Accessing API..."):
        try:
            mesh = dashboard.wireless.getNetworkWirelessMeshStatuses(net["id"])
        except APIError as err:
            console.print(f"[bold]{err.message['errors'][0]}")
            raise typer.Abort()

    # Maintain a dict of mesh device info
    devices = {}

    # Create a table of mesh devices and routes
    table = table_with_columns(
        ["Mesh Route", "Mbps", "Metric", "Usage"],
        title=f"Mesh Status for {net['name']}",
        first_column_name="AP Name",
    )
    for ap in mesh:
        mesh_route = ""
        # Iterate through each item in the mesh route
        for idx, serial in enumerate(ap["meshRoute"]):
            # Get device data for new serials
            if serial not in devices:
                devices[serial] = dashboard.devices.getDevice(serial)

            # Add mesh name to mesh route
            last_item = idx == len(ap["meshRoute"]) - 1
            mesh_route += f"[bold]{devices[serial]['name']}[/bold]"
            if not last_item:
                mesh_route += " -> "

        table.add_row(
            devices[ap["serial"]]["name"],
            mesh_route,
            f"{ap['latestMeshPerformance']['mbps']}Mbps",
            str(ap["latestMeshPerformance"]["metric"]),
            ap["latestMeshPerformance"]["usagePercentage"],
        )
    console.print(table)


@app.command()
def show_ssid(
    organization_name: str,
    network_name: str,
    ssid_number: int = typer.Argument(..., min=0, max=15),
):
    """
    Show an SSID for a network

    TODO: formatting
    """
    net = find_network_by_name(organization_name, network_name)
    with console.status("Accessing API..."):
        ssid = dashboard.wireless.getNetworkWirelessSsid(
            networkId=net["id"], number=ssid_number
        )

    console.print(ssid)


@app.command()
def update_ssid(
    organization_name: str,
    network_name: str,
    ssid_number: int = typer.Argument(..., help="The SSID number", min=0, max=15),
    confirm: bool = typer.Option(
        True, help="Confirm the current SSID name before applying changes"
    ),
    enabled: Optional[bool] = typer.Option(
        None, help="Whether or not the SSID is enabled"
    ),
    name: Optional[str] = typer.Option(None, help="The name of the SSID"),
    auth_mode: Optional[MRSSIDAuthMode] = typer.Option(
        None, help="The association control method for the SSID"
    ),
    encryption_mode: Optional[MRSSIDEncryptionMode] = typer.Option(
        None, help="The PSK encryption mode for the SSID"
    ),
    wpa_encryption_mode: Optional[MRSSIDWPAEncrytionMode] = typer.Option(
        None, help="The types of WPA encryption"
    ),
    tag_vlan: Optional[bool] = typer.Option(
        None, help="Whether or not traffic shuold be directed to use specific VLANs"
    ),
    default_vlan_id: Optional[int] = typer.Option(
        None, help="The default VLAN ID used for 'all other APs'", min=1, max=4094
    ),
    pre_shared_key: Optional[str] = typer.Option(None, help="The passkey for the SSID"),
    min_bitrate: Optional[int] = typer.Option(
        None, help="The minimum bitrate in Mbps", min=1, max=54
    ),
    ip_assignment_mode: Optional[MRSSIDIPAssignmentMode] = typer.Option(
        None, help="The client IP assignment mode"
    ),
):
    """
    Update an SSID for a network
    """
    net = find_network_by_name(organization_name, network_name)
    with console.status("Accessing API..."):
        ssid = dashboard.wireless.getNetworkWirelessSsid(
            networkId=net["id"], number=ssid_number
        )

    # Confirm SSID name with user before continuing
    if confirm:
        console.print(
            f"SSID number [bold]{ssid_number}[/bold] is named [bold]{ssid['name']}[/bold]"
        )
        confirmed = Confirm.ask("Do you want to continue?", console=console)
        if not confirmed:
            raise typer.Abort()

    update = {}
    items = {
        "name": name,
        "enabled": enabled,
        "useVlanTagging": tag_vlan,
        "defaultVlanId": default_vlan_id,
        "authMode": auth_mode.value if auth_mode is not None else None,
        "encryptionMode": encryption_mode.value
        if encryption_mode is not None
        else None,
        "wpaEncryptionMode": wpa_encryption_mode.value
        if wpa_encryption_mode is not None
        else None,
        "minBitrate": min_bitrate,
        "psk": pre_shared_key,
        "ipAssignmentMode": ip_assignment_mode.value
        if ip_assignment_mode is not None
        else None,
    }
    for k, v in items.items():
        if v is not None:
            if v is not ssid.get(k, None):
                update[k] = v

    # Do not call API if no changes were made
    if not update:
        console.print(f"[bold green]No settings changed.")
        raise typer.Exit()

    # Update SSID
    ssid = dashboard.wireless.updateNetworkWirelessSsid(
        networkId=net["id"], number=ssid_number, **update
    )
    console.print(f"[bold green]SSID '{ssid['name']}' has been updated.")
    console.print(f" The following parameters were updated: {', '.join(update)}")
