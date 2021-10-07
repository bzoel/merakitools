"""
merakitools - networks.py
Billy Zoellers

CLI tools for managing Meraki networks based on Typer
"""
from typing import List, Optional
import typer
from merakitools.console import console
from merakitools.dashboardapi import dashboard
from merakitools.meraki_helpers import find_orgs_by_name, find_org_by_name
from merakitools.formatting_helpers import table_with_columns
from merakitools.types import ProductType
from rich import inspect

app = typer.Typer()


@app.command()
def list(organization_name: str, product_type: Optional[ProductType] = None):
    """
    List Meraki networks in an organization
    """
    # Find an organization and get associated networks
    org = find_org_by_name(organization_name)
    with console.status("Accessing API..."):
        networks = dashboard.organizations.getOrganizationNetworks(org["id"])

    # Filter based on input and sort alphabetically
    if product_type:
        networks = [
            net for net in networks if product_type.value in net["productTypes"]
        ]
    networks = sorted(networks, key=lambda i: i["name"])

    # Display a table
    table = table_with_columns(["Name", "Type", "ID", "Time Zone"])
    for net in networks:
        table.add_row(
            net["name"], ", ".join(net["productTypes"]), net["id"], net["timeZone"]
        )
    console.print(table)
