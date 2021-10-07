"""
merakitools - orgs.py
Billy Zoellers

CLI tools for managing Meraki networks based on Typer
"""
from typing import List, Optional
import typer
from merakitools.console import console
from merakitools.dashboardapi import dashboard, APIError
from merakitools.meraki_helpers import find_org_by_name, find_orgs_by_name, api_req
from merakitools.formatting_helpers import table_with_columns
from rich import inspect

app = typer.Typer()


@app.command()
def list(name: Optional[str] = None, include_counts: bool = False):
    """
    List Meraki organizations
    """
    orgs = find_orgs_by_name(name)
    console.print(f"[bold]Found {len(orgs)} organizations")

    if not orgs:
        raise typer.Abort()

    table = table_with_columns(
        ["Name", "ID", "API", "Networks", "Devices"], title="Organizations"
    )

    with console.status("Accessing API..."):
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
            table.add_row(
                org["name"],
                org["id"],
                "[green]Enabled" if org["api"]["enabled"] else "[red]Disabled",
                str(len(networks)) if networks else "",
                str(len(devices)) if devices else "",
            )

    console.print(table)


@app.command()
def api(
    organization_name: str, enable: bool = typer.Option(None, "--enable/--disable")
):
    """
    Enable or disable Meraki API
    """
    # Get organization and print current API status
    org = find_org_by_name(organization_name)
    api_status = org["api"]["enabled"]
    console.print(
        f"API for [bold]{org['name']}[/bold] is currently [bold]{'enabled' if api_status else 'disabled'}."
    )

    # No change requested
    if enable is None:
        return api_status

    # No change required
    if api_status == enable:
        console.print(
            f" No change. API is already [bold]{'enabled' if api_status else 'disabled'}."
        )
        return api_status

    # Change API status
    with console.status("Accessing API..."):
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
            "organizations/{org['id']}/policyObjects",
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
        new_group = api_req(
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
    with console.status("Accessing API..."):
        api_requests = dashboard.organizations.getOrganizationApiRequests(
            org["id"], total_pages="all", perPage=250
        )
    table = table_with_columns(
        ["Method", "Path", "Response Code", "Source IP", "Time"],
        title=f"API Requests for {org['name']}",
    )
    for req in api_requests:
        table.add_row(
            req["method"],
            f"{req['path']}{req['queryString']}",
            str(req["responseCode"]),
            req["sourceIp"],
            req["ts"],
        )

    console.print(table)
