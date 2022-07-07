"""
merakitools - meraki_helpers.py
Billy Zoellers

CLI tools for managing Meraki networks based on Typer
"""
import os
from typing import Optional, List
from meraki.exceptions import APIError
import requests
import typer
from merakitools.console import console
from merakitools.dashboardapi import dashboard


def find_orgs_by_name(org_name: Optional[str]) -> List:
    """
    Given a name, find any matching organizations
    """
    with console.status("Finding Organizations..", spinner="material"):
        orgs = dashboard.organizations.getOrganizations()
    if org_name:
        orgs = [org for org in orgs if org_name in org["name"]]
    return orgs


def find_org_by_name(org_name: str):
    """
    Accepts an organization name or ID, and return the Meraki organization
    """
    with console.status("Finding organization..", spinner="material"):
        # Use numeric values as Org IDs
        if org_name.isnumeric():
            try:
                # Get org by ID
                org = dashboard.organizations.getOrganization(organizationId=org_name)
            except APIError as exc:
                console.print(
                    f"Organization ID [bold]{org_name}[/bold] not accessible."
                )
                raise typer.Abort() from exc
        else:
            try:
                # Get list of accessible orgs and search by name
                orgs = dashboard.organizations.getOrganizations()
                org = next(org for org in orgs if org["name"] == org_name)
            except APIError as err:
                console.print(f"{err.message}")
                raise typer.Abort()
            except StopIteration as exc:
                console.print(f"Organization named [bold]{org_name}[/bold] not found.")
                raise typer.Abort() from exc

    console.print(f"Organization: [bold]{org['name']}")
    return org


def find_org_id_by_device_serial(serial: str):
    """
    Given a serial, find the organization it belongs to
    """
    try:
        device = dashboard.devices.getDevice(serial=serial)
    except APIError as exc:
        console.print(f"[red]Unable to find device with serial '{serial}'")
        raise typer.Abort() from exc

    network = dashboard.networks.getNetwork(networkId=device["networkId"])

    return network["organizationId"]


def find_network_by_name(org_name: str, net_name: str):
    """
    Find a network given an orgaization name and network name
    """
    org = find_org_by_name(org_name)
    with console.status("Finding network..", spinner="material"):
        nets = dashboard.organizations.getOrganizationNetworks(org["id"])

    try:
        net = next(net for net in nets if net["name"] == net_name)
    except StopIteration as exc:
        print("Network not found.")
        raise typer.Abort() from exc

    console.print(f"Network: [bold]{net['name']}")
    return net


def api_req(resource: str, method: str = "GET", **kwargs):
    """
    API request outside of the Meraki Python SDK
    """
    base_url = "https://api.meraki.com/api/v1"
    headers = {
        "Accept": "application/json",
        "X-Cisco-Meraki-API-Key": os.getenv("MERAKI_DASHBOARD_API_KEY"),
    }

    resp = requests.request(
        url=f"{base_url}/{resource}", method=method, headers=headers, **kwargs
    )

    resp.raise_for_status()
    if resp.text:
        return resp.json()

    return {}
