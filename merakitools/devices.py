"""
merakitools - devices.py
Billy Zoellers

CLI tools for managing Meraki networks based on Typer
"""
from typing import List, Optional
import typer
from merakitools.console import console
from merakitools.dashboardapi import dashboard
from merakitools.meraki_helpers import api_req, find_network_by_name, find_org_by_name
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

@app.command()
def show_lldp(
  serial: Optional[List[str]] = None,
  organization_name: Optional[str] = None,
  network_name: Optional[str] = None
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
      console.print(f"No CDP/LLDP data found for {dev.get('name', dev['serial'])}")
      continue

    table = table_with_columns(
      ["Type", "System Name", "Remote Port", "Mgmt Address"],
      title=f"{dev['name']} ({dev['serial']})",
      first_column_name="Port"
    )

    for port, data in device_lldp["ports"].items():
      if port:
        table.add_row(port)
      if 'cdp' in data.keys():
        table.add_row(
          '', 'CDP',
          data['cdp'].get('deviceId'),
          data['cdp'].get('portId'),
          data['cdp'].get('address')
        )
      if 'lldp' in data.keys():
        table.add_row(
          '', 'LLDP',
          data['lldp'].get('systemName'),
          data['lldp'].get('portId'),
          data['lldp'].get('managementAddress')
        )
    console.print(table)

@app.command()
def reboot(
  serial: List[str] = None
):
  """
  Reboot device(s)
  """
  for sn in serial:
    reboot = dashboard.devices.rebootDevice(serial=sn)
    if reboot["success"]:
      console.print(f"Rebooted device with SN [bold]{sn}")
    else:
      console.print(f"Unabe to reboot device with SN [bold]{sn}")

@app.command()
def blink_led(
  serial: List[str] = None,
  duration: int = typer.Option(20, min=5, max=120)
):
  """
  Blink the LEDs of device(s)
  """
  for sn in serial:
    blink = dashboard.devices.blinkDeviceLeds(serial=sn, duration=duration)
    console.print(f"Blinking [bold]{sn}[/bold] LEDs for {blink['duration']} seconds")
