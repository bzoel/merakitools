"""
merakitools - mx.py
Billy Zoellers

CLI tools for managing Meraki networks based on Typer
"""
from typing import List, Optional
import typer
from merakitools.console import console
from merakitools.dashboardapi import dashboard, APIError
from merakitools.meraki_helpers import find_network_by_name, find_orgs_by_name, find_org_by_name
from merakitools.formatting_helpers import table_with_columns
from merakitools.types import ProductType
from rich import inspect
import ipaddress

app = typer.Typer()

@app.command()
def add_staticroute(
  organization_name: str,
  network_name: str,
  route: Optional[List[str]] = None,
  default_next_hop: Optional[str] = None
):
  """
  Add one or more static routes to an MX device
  """
  if not route:
    console.print(f"No routes provided.")
    raise typer.Abort()

  # Find the network
  net = find_network_by_name(organization_name, network_name)

  # Iterate through each provided route
  for route in route:
    args = len(route.split("!"))
    # Each route item should be formatted as 'routeCIDR' OR 'routeName!routeCIDR' or 'routeName!routeCIDR!routeNextHop'
    if 0 > args > 4:
      console.print("Incorect --route formatting")
      raise typer.Abort()
    
    if args == 3:
      # 'routeName!routeCIDR!routeNextHop' format
      route_name, route_subnet, route_nexthop = route.split("!")
    elif default_next_hop:
      route_nexthop = default_next_hop
      if args == 1:
        # 'routeCIDR' format
        route_name = route.replace(".","-").replace("/","-")
        route_subnet = route
      elif args == 2:
        # 'routeName!routeCIDR' format
        route_name, route_subnet = route.split("!")
    else:
      console.print("A next hop must be provided for each route, or --default-next-hop specified")
      raise typer.Abort

    # Check route_subnet and route_nexthop validity
    try:
      route_subnet = ipaddress.ip_network(route_subnet)
    except ValueError as err:
      console.print(f"Invalid next hop IP {route_subnet}. {err}")
      raise typer.Abort()

    try:
      route_nexthop = ipaddress.ip_address(route_nexthop)
    except ValueError as err:
      console.print(f"Invalid next hop IP {route_nexthop}. {err}")
      raise typer.Abort()

    # Add route via API
    with console.status("Accessing API..."):
      try:
        dashboard.appliance.createNetworkApplianceStaticRoute(
          networkId=net["id"],
          name=route_name,
          subnet=format(route_subnet),
          gatewayIp=format(route_nexthop)
        )
      except APIError as err:
        console.print(f"Failed to create route [bold]{route_name}[/bold]:")
        for e in err.message["errors"]:
          console.print(f" - {e}")
    