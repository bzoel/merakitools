"""
merakitools - ms.py
Billy Zoellers

CLI tools for managing Meraki networks based on Typer
"""
import typer
from typing import List
from merakitools.console import console
from merakitools.dashboardapi import dashboard
from merakitools.meraki_helpers import find_network_by_name
from merakitools.formatting_helpers import table_with_columns
from merakitools.types import DeviceModel, MSInterfaceMode, TrafficDirection
from rich import inspect
from rich.progress import Progress

app = typer.Typer()

@app.command()
def diag_switchport_traffic(
  organization_name: str,
  network_name: str,
  top: int = 100,
  sort_by: TrafficDirection = TrafficDirection.total,
  interface_mode: MSInterfaceMode = None,
  ignore_device_tag: List[str] = None,
  ignore_switchport_tag: List[str] = None
):
  """
  Diagnose all switchports on a network of MS switches to find
  switchports that are top talkers at a given instant

  ** This command gathers a significant amount of data and may
  take some time to complete on larger networks **
  """
  net = find_network_by_name(organization_name, network_name)
  with console.status("Accessing API..."):
    devices = dashboard.networks.getNetworkDevices(net["id"])

  console.print("Analyzing each switchport on the network, this may take a few minutes")
  switchports = []
  with Progress(console=console) as progress:
    task_devices = progress.add_task(f"[blue]Processing {len(devices)} devices..", total=len(devices))
    # Iterate through each switchport and add to the master switchport list
    for dev in devices:
      progress.update(task_devices, advance=1, description=f"[blue] Processing device \'{dev['name']}\'")

      # Ignore non-MS devices
      if DeviceModel.MS not in dev["model"]:
        continue

      # Ignore devices with specific tags
      if ignore_device_tag and any(tag in dev["tags"] for tag in ignore_device_tag):
        continue

      # Get switchport configuration and status
      switchport_configs = dashboard.switch.getDeviceSwitchPorts(serial=dev["serial"])
      switchport_statuses = dashboard.switch.getDeviceSwitchPortsStatuses(serial=dev["serial"])

      # Iterate through each switchport
      for swp_stat in switchport_statuses:
        # Ignore non-connected switchports
        if not swp_stat["status"] == "Connected":
          continue

        # Create a combined switchport record (status+config)
        swp_cfg = next(swp_cfg for swp_cfg in switchport_configs if swp_cfg["portId"] == swp_stat["portId"])
        swp = swp_stat|swp_cfg
        swp["switch_name"] = dev["name"]

        # Ignore switchports with specific tags
        if ignore_switchport_tag and any(tag in swp["tags"] for tag in ignore_switchport_tag):
          continue

        # Add combined switchport record to list of switchports
        switchports.append(swp)

    progress.update(task_devices, description=f"[green]Processed {len(devices)} devices.")

    # Sort all switchports based on the specified sort_by value (highest to lowest)
    switchports = sorted(switchports, key=lambda k: k['trafficInKbps'][sort_by.value], reverse=True)
    table = table_with_columns(
      ["Port", "Status", "Traffic (Total)", "Traffic (Sent)", "Traffic (Received)", "# of Clients", "CDP/LLDP", "Errors/Warnings"],
      title=f"Top {top} switchports",
      first_column_name="Device"
    )

    for swp in switchports[:top]:
      # get Mbps values for traffic
      mb_size = 1024
      rounding_precision = 2
      total_mbps = round(swp['trafficInKbps']['total']/mb_size, rounding_precision)
      recv_mbps = round(swp['trafficInKbps']['recv']/mb_size, rounding_precision)
      sent_mbps = round(swp['trafficInKbps']['sent']/mb_size, rounding_precision)

      # get discovery data if available
      if 'cdp' in swp.keys():
        discovery = swp['cdp'].get('systemName', None)
      elif 'lldp' in swp.keys():
        discovery = swp['lldp'].get('systemName', None)
      else:
        discovery = None

      # collate error/warning data
      errorwarn = swp['errors'] + swp['warnings']

      table.add_row(
          f"{swp['switch_name']}",
          f"{swp['portId']} ({swp['name']})",
          f"{swp['status']} ({swp['speed']})",
          f"{str(total_mbps)} Mbps",
          f"{str(sent_mbps)} Mbps",
          f"{str(recv_mbps)} Mbps",
          str(swp['clientCount']),
          discovery,
          (', ').join(errorwarn)
        )

    console.print(table)