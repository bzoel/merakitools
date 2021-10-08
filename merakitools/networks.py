"""
merakitools - networks.py
Billy Zoellers

CLI tools for managing Meraki networks based on Typer
"""
from typing import List, Optional
from rich.prompt import Confirm
import typer
from merakitools.console import console
from merakitools.dashboardapi import dashboard
from merakitools.meraki_helpers import (
    find_orgs_by_name,
    find_org_by_name,
    find_network_by_name,
)
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


@app.command()
def update_settings(
    organization_name: str,
    network_name: str,
    confirm: bool = typer.Option(
        True, help="Confirm the network name before applying changes"
    ),
    local_status: bool = typer.Option(
        None,
        "--enable-local-status/--disable-local-status",
        help="Local device status pages",
    ),
    remote_status: bool = typer.Option(
        None,
        "--enable-remote-status/--disable-remote-status",
        help="Remote device status pages",
    ),
):
    """
    Update a network
    """
    net = find_network_by_name(organization_name, network_name)
    with console.status("Getting current settings..", spinner="material"):
        settings = dashboard.networks.getNetworkSettings(networkId=net["id"])

    # Confirm SSID name with user before continuing
    if confirm:
        console.print(f"Network is named [bold]{net['name']}[/bold]")
        confirmed = Confirm.ask("Do you want to continue?", console=console)
        if not confirmed:
            raise typer.Abort()

    update = {}
    items = {
        "localStatusPageEnabled": local_status,
        "remoteStatusPageEnabled": remote_status,
    }
    for k, v in items.items():
        if v is not None:
            if v is not settings.get(k, None):
                update[k] = v

    # Do not call API if no changes were made
    if not update:
        console.print(f"[bold green]No settings changed.")
        raise typer.Exit()

    # Update settings
    with console.status("Updating settings..", spinner="material"):
        settings = dashboard.networks.updateNetworkSettings(
            networkId=net["id"], **update
        )
    console.print(f"[bold green]Settings for'{net['name']}' have been updated.")
    console.print(f" The following parameters were updated: {', '.join(update)}")
