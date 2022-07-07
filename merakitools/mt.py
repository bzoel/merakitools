"""
merakitools - mt.py
Billy Zoellers

CLI tools for managing Meraki networks based on Typer
"""

from typing import List, Optional
import typer
from merakitools.meraki_helpers import find_org_by_name
from merakitools.types import MTMetricType
from merakitools.console import console
from merakitools.dashboardapi import dashboard
from merakitools.formatting_helpers import table_with_columns

app = typer.Typer()


@app.command()
def latest_readings(
    organization_name: str,
    serial: Optional[List[str]] = None,
):
    """
    Show the latest reading for each metric from each sensor
    """
    org = find_org_by_name(organization_name)
    readings = dashboard.sensor.getOrganizationSensorReadingsLatest(org["id"])

    for device in readings:
        if serial and device["serial"] not in serial:
            continue

        table = table_with_columns(
            ["Data", "Time"],
            title=f"{device['network']['name']}: {device['serial']}",
            first_column_name="Metric",
        )
        for reading in device["readings"]:
            table.add_row(
                reading["metric"].capitalize(),
                str(reading[reading["metric"]]),
                reading["ts"],
            )

        console.print(table)


@app.command()
def history(
    organization_name: str,
    serial: Optional[List[str]] = None,
    metric_type: Optional[List[MTMetricType]] = None,
):
    """
    Show the historical sensor readings for an organization
    """
    org = find_org_by_name(organization_name)
    readings = dashboard.sensor.getOrganizationSensorReadingsHistory(org["id"])

    table = table_with_columns(
        ["Data", "Time", "Network / Serial"], "History", first_column_name="Metric"
    )
    for reading in readings:
        if metric_type and reading["metric"] not in metric_type:
            continue

        if serial and reading["serial"] not in serial:
            continue

        table.add_row(
            reading["metric"],
            str(reading[reading["metric"]]),
            reading["ts"],
            f"{reading['network']['name']} / {reading['serial']}",
        )
    console.print(table)
