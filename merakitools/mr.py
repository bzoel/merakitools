"""
merakitools - mr.py
Billy Zoellers

CLI tools for managing Meraki networks based on Typer
"""
from meraki.exceptions import APIError
import typer
from typing import List

from typer import params
from merakitools.console import console
from merakitools.dashboardapi import dashboard
from merakitools.meraki_helpers import api_req, find_network_by_name, find_org_by_name
from merakitools.formatting_helpers import table_with_columns
from merakitools.types import DeviceModel, ProductType
from rich import inspect
from rich.progress import Progress

app = typer.Typer()

@app.command()
def list_ssid(
  organization_name: str,
  network_name: str,
  include_disabled: bool = typer.Option(False, "--include-disabled"),
  include_psk: bool = False
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
    ["Enabled", "Authentication", "Mode", "VLAN Tag", "Band", "Visible", "Availability"],
    title=f"SSIDs for {net['name']}",
    first_column_name="Name"
  )
  for ssid in ssids:
    table.add_row(
      ssid["name"],
      "[green]Enabled" if ssid["enabled"] else "[red]Disabled",
      f"{ssid.get('encryptionMode', 'open')} / {ssid['authMode']}" + f" [bold]{ssid.get('psk') if include_psk else ''}",
      ssid["ipAssignmentMode"],
      str(ssid.get("defaultVlanId")) if ssid.get("useVlanTagging") else "none",
      ssid["bandSelection"],
      "[green]Visible" if ssid["visible"] else "[red]Not visible",
      "All APs" if ssid["availableOnAllAps"] else f"Tags: {', '.join(ssid['availabilityTags'])}"
    )
  console.print(table)

@app.command()
def list_mesh(
  organization_name: str,
  network_name: str
):
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
      mesh = dashboard.wireless.getNetworkWirelessMeshStatuses(net['id'])
    except APIError as err:
      console.print(f"[bold]{err.message['errors'][0]}")
      raise typer.Abort()
  
  # Maintain a dict of mesh device info
  devices = {}

  # Create a table of mesh devices and routes
  table = table_with_columns(
    ["Mesh Route", "Mbps", "Metric", "Usage"],
    title=f"Mesh Status for {net['name']}",
    first_column_name="AP Name"
  )
  for ap in mesh:
    mesh_route = ""
    # Iterate through each item in the mesh route
    for idx, serial in enumerate(ap['meshRoute']):
      # Get device data for new serials
      if serial not in devices:
        devices[serial] = dashboard.devices.getDevice(serial)

      # Add mesh name to mesh route  
      last_item = idx == len(ap['meshRoute'])-1
      mesh_route += f"[bold]{devices[serial]['name']}[/bold]"
      if not last_item:
        mesh_route += " -> "

    table.add_row(
      devices[ap['serial']]['name'],
      mesh_route,
      f"{ap['latestMeshPerformance']['mbps']}Mbps",
      str(ap["latestMeshPerformance"]["metric"]),
      ap["latestMeshPerformance"]["usagePercentage"]
    )
  console.print(table)