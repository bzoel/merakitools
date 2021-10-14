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
from merakitools.types import ProductType, NetworkTrafficAnalysisMode
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
    Update network settings
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


@app.command()
def traffic_analysis(
    organization_name: str,
    network_name: str,
    confirm: bool = typer.Option(
        True, help="Confirm the network name before applying changes"
    ),
    set_mode: NetworkTrafficAnalysisMode = typer.Option(
        None, help="Traffic analysis mode for network"
    ),
):
    """
    Get or update the traffic analysis mode for a network
    """
    net = find_network_by_name(organization_name, network_name)
    with console.status("Getting current settings..", spinner="material"):
        traffic_analysis = dashboard.networks.getNetworkTrafficAnalysis(
            networkId=net["id"]
        )

    # Print current mode
    console.print(f"Current Traffic analysis mode: [bold]{traffic_analysis['mode']}")

    # Update mode if requested
    if set_mode is not None:
        # Confirm network name with user before continuing
        if confirm:
            confirmed = Confirm.ask("Do you want to continue?", console=console)
            if not confirmed:
                raise typer.Abort()

        # Make change only if required
        if set_mode.lower() == traffic_analysis["mode"].lower():
            console.print(f"[bold green]No settings changed.")
            raise typer.Abort()

        # Update settings
        with console.status("Updating settings..", spinner="material"):
            settings = dashboard.networks.updateNetworkTrafficAnalysis(
                networkId=net["id"],
                mode=set_mode,
            )
        console.print(
            f"[bold green]Traffic analysis mode for '{net['name']}' changed to {set_mode}"
        )


@app.command()
def list_webhook_servers(
    organization_name: str,
    network_name: str,
):
    """
    List webhook servers for a network
    """
    # Get a list of the current webhook servers
    net = find_network_by_name(organization_name, network_name)
    with console.status("Getting current settings..", spinner="material"):
        http_servers = dashboard.networks.getNetworkWebhooksHttpServers(
            networkId=net["id"]
        )

    # Output to table
    table = table_with_columns(
        ["URL"], first_column_name="Name", title=f"Webhook Servers for {net['name']}"
    )
    for server in http_servers:
        table.add_row(server["name"], server["url"])
    console.print(table)


@app.command()
def new_webhook_server(
    organization_name: str,
    network_name: str,
    name: str = typer.Option(..., help="A name for easy reference"),
    shared_secret: str = typer.Option(
        None, help="A shared secret included in POSTs send to the HTTP server"
    ),
    url: str = typer.Option(
        ..., help="The URL of the HTTP server. Cannot be updated later."
    ),
):
    """
    Create a new webhook server for a network
    """
    # Get a list of the current webhook servers
    net = find_network_by_name(organization_name, network_name)
    with console.status("Getting current webhook servers..", spinner="material"):
        http_servers = dashboard.networks.getNetworkWebhooksHttpServers(
            networkId=net["id"]
        )

    # Validate inputs
    duplicate_name = duplicate_url = None
    for server in http_servers:
        if server["name"] == name:
            duplicate_name = server
            break
        if server["url"] == url:
            duplicate_url = server
    if duplicate_name:
        console.print(f"[red]A webhook server named {name} already exists!")
        raise typer.Abort()
    if duplicate_url:
        console.print(
            f"[red]A webhook server named {duplicate_url['name']} already exists with this URL!"
        )
        raise typer.Abort()

    # Create new webhook server
    new_server = dashboard.networks.createNetworkWebhooksHttpServer(
        networkId=net["id"],
        name=name,
        url=url,
        sharedSecret=shared_secret if shared_secret else "",
    )
    console.print(
        f"[bold green]New webhook server named '{new_server['name']}' created."
    )
