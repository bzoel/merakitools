"""
merakitools - orgs.py
Billy Zoellers

CLI tools for managing Meraki networks based on Typer
"""
from typing import List, Optional
import typer
from merakitools.console import console
from merakitools.dashboardapi import dashboard, APIError
from merakitools.meraki_helpers import find_orgs_by_name
from merakitools.formatting_helpers import table_with_columns
from rich import inspect

app = typer.Typer()

@app.command()
def list(name: Optional[str] = None, include_counts: bool = False):
  """
  List Meraki organizations
  """
  with console.status("Accessing API..."):
    orgs = find_orgs_by_name(name)
  console.print(f"[bold]Found {len(orgs)} organizations")

  if not orgs:
    raise typer.Abort()

  table = table_with_columns(
    ['Name', 'ID', 'API', 'Networks', 'Devices'],
    title="Organizations"
  )

  with console.status("Accessing API..."):
    for org in orgs:
      networks = devices = None
      if include_counts and org['api']['enabled']:
        try:
          networks = dashboard.organizations.getOrganizationNetworks(org['id'])
          devices = dashboard.organizations.getOrganizationDevices(org['id'])
        except APIError:
          console.print(f"Unable to access {org['name']}")
      table.add_row(
        org['name'],
        org['id'],
        "[green]Enabled" if org['api']['enabled'] else "[red]Disabled",
        str(len(networks)) if networks else "",
        str(len(devices)) if devices else ""
      )

  console.print(table)