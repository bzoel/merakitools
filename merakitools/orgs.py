"""
merakitools - orgs.py
Billy Zoellers

CLI tools for managing Meraki networks based on Typer
"""
from typing import List, Optional
import typer
from merakitools.console import console, status_spinner
from merakitools.dashboardapi import dashboard, APIError
from merakitools.meraki_helpers import (
    find_network_by_name,
    find_org_by_name,
    find_orgs_by_name,
    api_req,
)
from merakitools.formatting_helpers import table_with_columns, table_network_health

app = typer.Typer()


@app.command()
def list(name: Optional[str] = None, include_counts: bool = False):
    """
    List Meraki organizations
    """
    orgs = find_orgs_by_name(name)
    console.print(f"Found [bold]{len(orgs)} organizations")

    if not orgs:
        raise typer.Abort()

    # Create a table of organizations
    columns = ["Name", "ID", "API"]
    if include_counts:
        columns.extend(["Networks", "Devices"])
    table = table_with_columns(columns, title="Organizations")

    with status_spinner("Gathering network and device counts"):
        for org in orgs:
            networks = devices = None
            if include_counts and org["api"]["enabled"]:
                try:
                    networks = dashboard.organizations.getOrganizationNetworks(
                        org["id"]
                    )
                    devices = dashboard.organizations.getOrganizationDevices(org["id"])
                except APIError:
                    console.print(f"Unable to access {org['name']}")

            row = [
                org["name"],
                org["id"],
                "[green]Enabled" if org["api"]["enabled"] else "[red]Disabled",
            ]
            if include_counts:
                row.extend(
                    [
                        str(len(networks)) if networks else "",
                        str(len(devices)) if devices else "",
                    ]
                )
            table.add_row(*row)

    console.print(table)


@app.command()
def network_health(organization_name: str):
    """
    Meraki network health (global alerts) for all network
    """
    org = find_org_by_name(organization_name)

    orgwide_health = []
    with status_spinner("Gathering health information"):
        networks = dashboard.organizations.getOrganizationNetworks(org["id"])
        for net in networks:
            health = dashboard.networks.getNetworkHealthAlerts(net["id"])
            for alert in health:
                alert["network_name"] = net["name"]
                orgwide_health.append(alert)

    console.print(
        table_network_health(
            health=orgwide_health,
            title=f"Health for {org['name']}",
            include_network_name=True,
        )
    )


@app.command()
def mx_uplinks(
    organization_name: str,
):
    """
    Return the uplink loss and latency for every MX in the organization
    """
    org = find_org_by_name(organization_name)
    with status_spinner("Gathering data"):
        networks = dashboard.organizations.getOrganizationNetworks(org["id"])
        devices = dashboard.organizations.getOrganizationDevices(org["id"])
        uplinks = dashboard.organizations.getOrganizationDevicesUplinksLossAndLatency(
            org["id"]
        )

    # Create network ID to name mapping
    network_map = {}
    for network in networks:
        network_map[network["id"]] = network["name"]

    # Create serial to device mapping
    device_map = {}
    for device in devices:
        device_map[device["serial"]] = device["name"]

    table = table_with_columns(
        ["Uplink", "IP", "Loss", "Latency", "Time"], first_column_name="Device"
    )

    for uplink in uplinks:
        table.add_row(
            f"{network_map[uplink['networkId']]} / {device_map[uplink['serial']]}",
            uplink["uplink"],
            uplink["ip"],
            f"{uplink['timeSeries'][-1]['lossPercent']}%"
            if uplink["timeSeries"][-1]["lossPercent"] is not None
            else "",
            f"{uplink['timeSeries'][-1]['latencyMs']}ms"
            if uplink["timeSeries"][-1]["latencyMs"] is not None
            else "",
            f"{uplink['timeSeries'][-1]['ts']}",
        )

    console.print(table)


@app.command()
def create(
    name: str,
    org_admin: Optional[List[str]] = typer.Option(
        None, help="Org admins in Name!Email format"
    ),
    claim_order: Optional[List[str]] = typer.Option(None),
):
    """
    Create a new Meraki organization
    """
    # Create organization
    try:
        org = dashboard.organizations.createOrganization(name=name)
        console.print(
            f"Created new organization [bold]{org['name']}[/bold]. ID: {org['id']}"
        )
    except APIError as err:
        console.print(f"Unable to create organization. {err.message}")
        raise typer.Abort()

    # Create org_admins if specified
    if org_admin:
        for admin in org_admin:
            name, email = admin.split("!")
            try:
                admin = dashboard.organizations.createOrganizationAdmin(
                    organizationId=org["id"], name=name, email=email, orgAccess="full"
                )
                console.print(f"Created new admin {email}.")
            except APIError as err:
                console.print(f"Unable to create admin {email}. {err.message}")
                raise typer.Abort()

    # Claim orders if specified
    if claim_order:
        try:
            dashboard.organizations.claimIntoOrganization(
                organizationId=org["id"], orders=claim_order
            )
            console.print(f"Claimed orders: {', '.join(claim_order)}")
        except APIError as err:
            console.print(f"Unable to claim order(s). {err.message}")


@app.command()
def saml(
    organization_name: str, enable: bool = typer.Option(None, "--enable/--disable")
):
    """
    Organization SAML status
    """
    # Get organization and print current status
    org = find_org_by_name(organization_name)
    saml_status = dashboard.organizations.getOrganizationSaml(organizationId=org["id"])[
        "enabled"
    ]
    console.print(
        f"SAML for [bold]{org['name']}[/bold] is currently"
        f" [bold]{'enabled' if saml_status else 'disabled'}."
    )

    if enable is not None:
        if saml_status == enable:
            # No change is requried
            console.print(
                " No change. SAML is already"
                f" [bold]{'enabled' if saml_status else 'disabled'}."
            )
        else:
            # Change API status
            with status_spinner("Updating organization"):
                saml_status = dashboard.organizations.updateOrganizationSaml(
                    organizationId=org["id"], enabled=enable
                )["enabled"]
            console.print(
                f" API is now [bold]{'enabled' if saml_status else 'disabled'}"
            )

    return saml_status


@app.command()
def create_saml_idp(organization_name: str, saml_x509_cert: str, saml_slo_logout: str):
    """
    Create a SAML IDP
    """
    # Find organization
    org = find_org_by_name(organization_name)

    # Create SAML IDP
    saml_idp = dashboard.organizations.createOrganizationSamlIdp(
        organizationId=org["id"],
        x509certSha1Fingerprint=saml_x509_cert,
        sloLogoutUrl=saml_slo_logout,
    )
    console.print(
        f"Created SAML IDP. Consumer URL is [bold]{saml_idp['consumerUrl']}[/bold]"
    )
    return saml_idp


@app.command()
def create_saml_role(
    organization_name: str,
    role: str,
    access: str = "full",
):
    """
    Create a SAML role
    """
    org = find_org_by_name(organization_name)
    new_role = dashboard.organizations.createOrganizationSamlRole(
        organizationId=org["id"], role=role, orgAccess=access
    )
    console.print(f"Created SAML role {new_role['role']}")


@app.command()
def claim_order(
    organization_name: str,
    order_number: Optional[List[str]] = typer.Option(...),
    claim_to_network_name: Optional[str] = typer.Option(None),
):
    """
    Claim an order into an organization
    """
    # Find organization or network
    if claim_to_network_name is None:
        org = find_org_by_name(org_name=organization_name)
        org_id = org["id"]
    else:
        net = find_network_by_name(
            org_name=organization_name, net_name=claim_to_network_name
        )
        org_id = net["organizationId"]

    # Attempt to claim order
    try:
        claim = dashboard.organizations.claimIntoOrganization(
            organizationId=org["id"], orders=order_number
        )
    except APIError as err:
        console.print(f"Unable to claim order(s). {err.message}")
        raise typer.Abort()

    console.print(f"Claimed orders: {', '.join(claim['orders'])}")

    # Find serials contained in this order number
    inventory = dashboard.organizations.getOrganizationInventoryDevices(
        organizationId=org_id
    )
    serials = []
    for device in inventory:
        if device["orderNumber"] in order_number:
            console.print(f" {device['model']} {device['serial']}")

            # Create a list of serials
            if claim_to_network_name is not None:
                if device["networkId"] is None:
                    serials.append(device["serial"])

    # Claim devices into networks if requested
    if claim_to_network_name is not None:
        dashboard.networks.claimNetworkDevices(networkId=net["id"], serials=serials)
        console.print(
            f"[green]{len(serials)} devices were added to [bold]{net['name']}"
        )


@app.command()
def api(
    organization_name: str, enable: bool = typer.Option(None, "--enable/--disable")
):
    """
    Organization API status
    """
    # Get organization and print current API status
    org = find_org_by_name(organization_name)
    api_status = org["api"]["enabled"]
    console.print(
        f"API for [bold]{org['name']}[/bold] is currently"
        f" [bold]{'enabled' if api_status else 'disabled'}."
    )

    # No change requested
    if enable is None:
        return api_status

    # No change required
    if api_status == enable:
        console.print(
            " No change. API is already"
            f" [bold]{'enabled' if api_status else 'disabled'}."
        )
        return api_status

    # Change API status
    with status_spinner("Updating organization"):
        org = dashboard.organizations.updateOrganization(
            organizationId=org["id"], name=org["name"], api={"enabled": enable}
        )
    console.print(f" API is now [bold]{'enabled' if enable else 'disabled'}")
    return enable


@app.command()
def create_ip_objects(
    organization_name: str, group_name: str = None, object: Optional[List[str]] = None
):
    """
    Create new IP objects within organization, optionally adding to specified group
    """
    if not object:
        console.print("No objects provided")
        raise typer.Abort()

    org = find_org_by_name(organization_name)

    # Iterate through each new object
    new_objects = []
    for obj in object:
        args = len(obj.split("!"))
        # Each port item should  be formatted as 'objectIP' or 'objectName!objectIP'
        if not 0 < args < 3:
            console.print("Incorect --object formatting")
            raise typer.Abort()

        if args == 2:
            # 'objectName!objectIP' format
            obj_name, obj_cidr = obj.split("!")
        elif args == 1:
            # 'objectIP' format
            obj_cidr = obj
            obj_name = obj.replace(".", "-")

        new_obj = api_req(
            f"organizations/{org['id']}/policyObjects",
            method="POST",
            json={
                "name": obj_name,
                "category": "network",
                "type": "cidr",
                "cidr": obj_cidr,
            },
        )
        new_objects.append(new_obj["id"])
        console.print(f"Created object named {obj_name} with IP {obj_cidr}")

    # Create a group with the new objects included
    if group_name:
        api_req(
            f"organizations/{org['id']}/policyObjects/groups",
            method="POST",
            json={
                "name": group_name,
                "category": "NetworkObjectGroup",
                "objectIds": new_objects,
            },
        )
        console.print(f"Created group named {group_name}")


@app.command()
def list_api_requests(organization_name: str):
    """
    List API requests for organization
    """
    org = find_org_by_name(organization_name)
    with status_spinner("Gathering API requests"):
        api_requests = dashboard.organizations.getOrganizationApiRequests(
            org["id"], total_pages="all", perPage=250
        )
    table = table_with_columns(
        ["Endpoint", "Response Code", "Source IP", "User Agent", "Time"],
        title=f"API Requests for {org['name']}",
    )
    for req in api_requests:
        table.add_row(
            f"{req['method']} {req['path']}{req['queryString']}",
            str(req["responseCode"]),
            req["sourceIp"],
            req["userAgent"][0:20],
            req["ts"],
        )

    console.print(table)
