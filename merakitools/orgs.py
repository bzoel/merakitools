"""
merakitools - orgs.py
Billy Zoellers

CLI tools for managing Meraki networks based on Typer
"""
from typing import List, Optional
import typer
import meraki
from meraki.exceptions import APIError
from rich.console import Console
from rich.table import Table
from rich import inspect
from merakitools.meraki_helpers import find_orgs_by_name

app = typer.Typer()
console = Console()

# Create a Meraki dashboard connection
try:
  dashboard = meraki.DashboardAPI(
    output_log=False, print_console=False, suppress_logging=True
  )
except APIError:
  console.print("[bold red]Unable to connect to the Meraki Dashboard.")
  console.print_exception()

@app.command()
def list(name: Optional[str] = None):
  """
  List Meraki organizations
  """
  orgs = find_orgs_by_name(dashboard, name)
  console.print(f"[bold]Found {len(orgs)} organizations")

  if not orgs:
    raise typer.Abort()

  table = Table(title="Organizations")
  columns = ['Name', 'ID', 'API', 'Networks', 'Devices']
  for c in columns:
    table.add_column(c)

  with console.status("Accessing API..."):
    for org in orgs:
      if org['api']['enabled']:
        try:
          networks = dashboard.organizations.getOrganizationNetworks(org['id'])
          devices = dashboard.organizations.getOrganizationDevices(org['id'])
        except APIError:
          console.print(f"Unable to access {org['name']}")
      table.add_row(
        org['name'],
        org['id'],
        "[green]Enabled" if org['api']['enabled'] else "[red]Disabled",
        str(len(networks)) if networks else "n/a",
        str(len(devices)) if devices else "n/a"
      )

  console.print(table)