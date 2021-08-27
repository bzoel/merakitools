"""
merakitools - devices.py
Billy Zoellers

CLI tools for managing Meraki networks based on Typer
"""
from typing import List, Optional
import typer
from merakitools.console import console
from merakitools.dashboardapi import dashboard
from merakitools.meraki_helpers import find_network_by_name, find_org_by_name
from merakitools.formatting_helpers import table_with_columns
from merakitools.types import DeviceModel, DeviceSortOptions
from rich import inspect

app = typer.Typer()

@app.command()
def list(
  organization_name: str,
  network_name: str,
  type: Optional[DeviceModel] = None,
  sort_by: Optional[DeviceSortOptions] = DeviceSortOptions.model,
  sort_reverse: bool = False
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
    first_column_name="Name"
  )
  for device in devices:
    table.add_row(
      device["name"],
      device["serial"],
      net["name"],
      device["model"],
      ",".join(device["tags"]),
      device["firmware"]
    )
  console.print(table)