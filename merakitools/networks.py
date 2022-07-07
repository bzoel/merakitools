"""
merakitools - networks.py
Billy Zoellers

CLI tools for managing Meraki networks based on Typer
"""
from typing import Optional
from rich.prompt import Confirm
import typer
from merakitools.console import console, status_spinner
from merakitools.dashboardapi import dashboard
from merakitools.meraki_helpers import (
    find_org_by_name,
    find_network_by_name,
    api_req,
)
from merakitools.formatting_helpers import table_with_columns, table_network_health
from merakitools.types import ProductType, NetworkTrafficAnalysisMode

app = typer.Typer()


@app.command()
def list(organization_name: str, product_type: Optional[ProductType] = None):
    """
    List Meraki networks in an organization
    """
    # Find an organization and get associated networks
    org = find_org_by_name(organization_name)
    with status_spinner("Getting networks"):
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
    with status_spinner("Getting current settings"):
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
    for key, value in items.items():
        if value is not None:
            if value is not settings.get(key, None):
                update[key] = value

    # Do not call API if no changes were made
    if not update:
        console.print("[bold green]No settings changed.")
        raise typer.Exit()

    # Update settings
    with status_spinner("Updating settings"):
        settings = dashboard.networks.updateNetworkSettings(
            networkId=net["id"], **update
        )
    console.print(f"[bold green]Settings for'{net['name']}' have been updated.")
    console.print(f" The following parameters were updated: {', '.join(update)}")


@app.command()
def health(organization_name: str, network_name: str):
    """
    Get Meraki network health (global alerts) for a network
    """
    # Find a network and get network health alerts
    net = find_network_by_name(organization_name, network_name)
    with status_spinner("Gathering health information"):
        health = dashboard.networks.getNetworkHealthAlerts(net["id"])

    # Print number of alerts found, exist it no alerts
    if not health:
        console.print(f"[green]No health alerts found for {net['name']}!")
        raise typer.Exit()
    console.print(f"Found {len(health)} alerts for {net['name']}")

    console.print(
        table_network_health(health, title=f"Network health for {net['name']}")
    )


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
    with status_spinner("Getting current settings"):
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
            console.print("[bold green]No settings changed.")
            raise typer.Abort()

        # Update settings
        with status_spinner("Updating settings"):
            dashboard.networks.updateNetworkTrafficAnalysis(
                networkId=net["id"],
                mode=set_mode,
            )
        console.print(
            f"[bold green]Traffic analysis mode for '{net['name']}' changed to"
            f" {set_mode}"
        )


@app.command()
def list_firmware_upgrades(
    organization_name: str,
    network_name: str,
):
    """
    List firmware upgrades for a network
    """
    net = find_network_by_name(organization_name, network_name)
    with status_spinner("Getting firmware information"):
        firmware_upgrades = dashboard.networks.getNetworkFirmwareUpgrades(
            networkId=net["id"]
        )

    table = table_with_columns(
        [
            "Current Version",
            "Last Upgrade",
            "Last Upgrade Time",
            "Available Versions",
            "Upgrade Scheduled",
            "Upgrade Time",
        ],
        first_column_name="Product",
    )
    for product, fw_info in firmware_upgrades["products"].items():
        available_versions = [
            av["shortName"]
            for av in fw_info["availableVersions"]
            if av["id"] != fw_info["currentVersion"]["id"]
        ]

        table.add_row(
            product.capitalize(),
            f"[bold]{fw_info['currentVersion']['shortName']}[/bold]"
            f" ({fw_info['currentVersion']['releaseType']})",
            f"[bold]{fw_info['lastUpgrade']['fromVersion'].get('shortName', None)}[/bold]"
            f" -> [bold]{fw_info['lastUpgrade']['toVersion'].get('shortName', None)}[/bold]",
            fw_info["lastUpgrade"]["time"],
            ", ".join(available_versions),
            f"{fw_info['nextUpgrade']['toVersion']['shortName']} ({fw_info['nextUpgrade']['toVersion']['releaseType']})"
            if fw_info["nextUpgrade"]["time"]
            else "",
            fw_info["nextUpgrade"]["time"] if fw_info["nextUpgrade"]["time"] else "",
        )

    console.print(table)


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
    with status_spinner("Getting current settings"):
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
    with status_spinner("Getting current webhook servers"):
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
            f"[red]A webhook server named {duplicate_url['name']} already exists with"
            " this URL!"
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


@app.command()
def list_payload_templates(
    organization_name: str,
    network_name: str,
):
    """
    List webhook payload templates for a network
    """
    net = find_network_by_name(organization_name, network_name)
    with status_spinner("Getting templates"):
        templates = api_req(f"networks/{net['id']}/webhooks/payloadTemplates")

    # Output to table
    table = table_with_columns(
        ["Type", "ID"],
        first_column_name="Name",
        title=f"Payload templates for {net['name']}",
    )
    for template in templates:
        table.add_row(
            template["name"],
            template["type"],
            template["payloadTemplateId"],
        )
    console.print(table)


@app.command()
def new_payload_template(
    organization_name: str,
    network_name: str,
    name: str = typer.Option(..., help="A name for the payload template"),
    headers: typer.FileBinaryRead = typer.Option(
        ..., help="A file with the headers template"
    ),
    body: typer.FileBinaryRead = typer.Option(
        ..., help="A file with the body template"
    ),
):
    """
    Create a webhook payload template
    """
    net = find_network_by_name(organization_name, network_name)

    with status_spinner(f"Creating template [bold]{name}"):
        data = {"name": name}
        files = {
            "headersFile": headers,
            "bodyFile": body,
        }

        template = api_req(
            f"networks/{net['id']}/webhooks/payloadTemplates",
            method="POST",
            data=data,
            files=files,
        )

    console.print(
        f"[green]Created new template named [bold]{template['name']}[/bold] with ID"
        f" {template['payloadTemplateId']}."
    )


@app.command()
def delete_payload_template(
    organization_name: str,
    network_name: str,
    name: str = typer.Option(..., help="Name of the payload template"),
    confirm: bool = typer.Option(True, help="Confirm before deleting"),
):
    """
    Delete a webhook payload template
    """
    # Get a list of payload templates for the network
    net = find_network_by_name(organization_name, network_name)
    with status_spinner("Getting templates"):
        templates = api_req(f"networks/{net['id']}/webhooks/payloadTemplates")

    # Search by name
    try:
        found = next(t for t in templates if t["name"] == name)
    except StopIteration as exc:
        console.print(f"[red]Payload template named [bold]{name}[/bold] not found.")
        raise typer.Abort() from exc
    console.print(f"Found template named [bold]{found['name']}")

    # Confirm with user
    if confirm:
        confirmed = Confirm.ask("Do you want to delete?", console=console)
        if not confirmed:
            raise typer.Abort()

    api_req(
        f"networks/{net['id']}/webhooks/payloadTemplates/{found['payloadTemplateId']}",
        method="DELETE",
    )
    console.print(f"[green]Deleted payload template [bold]{name}")
