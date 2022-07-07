"""
merakitools - msp.py
Billy Zoellers

CLI tools for managing Meraki networks based on Typer
"""

from typing import List, Optional
from datetime import datetime, timedelta
import typer
from rich.progress import track
from merakitools.console import console, status_spinner
from merakitools.dashboardapi import dashboard, APIError


app = typer.Typer()


@app.command()
def enable_api_all():
    """
    Enable the Meraki API for all accessible organizations
    """
    with status_spinner("Finding organizations"):
        orgs = dashboard.organizations.getOrganizations()
        orgs = [org for org in orgs if not org["api"]["enabled"]]
    console.print(f"Found {len(orgs)} organizations with API disabled.")

    for org in track(orgs, console=console):
        try:
            org = dashboard.organizations.updateOrganization(
                organizationId=org["id"], name=org["name"], api={"enabled": True}
            )
        except APIError:
            console.print(f"[red]Error enabling API for {org['name']}")
            continue
        console.print(f"[green]API enabled for {org['name']}")


@app.command()
def list_security_events(
    days_ago: int = typer.Option(3, help="How many days to look back for events"),
    organization_name: Optional[List[str]] = typer.Option(
        None, help="Specify organization"
    ),
    filter_event_name: Optional[str] = typer.Option(
        None, help="Filter by event message"
    ),
):
    """
    List security events for organization(s), filtering by organization or event name
    """
    # Get all accessible organizations, filtering by name if specified
    with status_spinner("Finding organizations"):
        orgs = dashboard.organizations.getOrganizations()
        if organization_name:
            orgs = [org for org in orgs if org["name"] in organization_name]
    console.print(f"[bold]Found {len(orgs)} organizations.")

    # Calculate number of days to look back
    end_time = datetime.now()
    start_time = end_time - timedelta(days=days_ago)
    start_time = datetime.combine(start_time, start_time.min.time())
    dtformat = "%Y-%m-%d %H:%M:%S"
    console.print(
        f" [italic]Displaying events from {start_time.strftime(dtformat)} to"
        f" {end_time.strftime(dtformat)}."
    )

    # Iterate through each org to gather security events
    for org in track(orgs, console=console):
        try:
            events = dashboard.appliance.getOrganizationApplianceSecurityEvents(
                organizationId=org["id"],
                total_pages="all",
                perPage=1000,
                t0=start_time,
                t1=end_time,
            )
        except APIError:
            continue

        # Iterate through each event
        event_hosts = []
        filtered_events = []
        for event in events:
            # Drop events that do not match the filter
            if filter_event_name is not None:
                if not filter_event_name in event["message"]:
                    continue
            filtered_events.append(event)

            # Maintain a list of associated hosts
            if not event["destIp"] in event_hosts:
                event_hosts.append(event["destIp"])

        if len(filtered_events) > 0:
            console.print(
                f"[bold]{org['name']}[/bold] matched {len(filtered_events)} events."
            )
            for host in event_hosts:
                console.print(f" {host}")
