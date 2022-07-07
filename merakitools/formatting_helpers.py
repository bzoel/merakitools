"""
merakitools - formatting_helpers.py
Billy Zoellers

CLI tools for managing Meraki networks based on Typer
"""
import re
from typing import List, Optional
from rich.table import Table, Column
from rich import box

# Mapping of styles to severity - TODO: move to an import
severity_styles = {"critical": "bold red", "warning": "yellow"}


def camel_case_split(input_string) -> str:
    """
    Input: applicationCategory
    Output: Application Category
    """
    return re.sub(r"(\w)([A-Z])", r"\1 \2", input_string).capitalize()


def table_with_columns(
    columns: List, title: Optional[str] = None, first_column_name: Optional[str] = None
) -> Table:
    """
    Generate a table with specified columns
    """
    table = Table(*columns, title=title, expand=False, box=box.ROUNDED)
    if first_column_name:
        first_column = Column(first_column_name, style="bold blue")
        table.columns.insert(0, first_column)

    return table


def table_mx_onetoone_nat(rules: List, title: str = "NAT Entries") -> Table:
    """
    Generate a table to display MX one to one NAT entries
    """
    table = table_with_columns(
        ["External IP", "Internal IP", "Uplink", "Protocol", "Ports", "Allowed IPs"],
        title=title,
        first_column_name="Name",
    )
    for rule in rules:
        table.add_row(
            rule["name"],
            rule["publicIp"],
            rule["lanIp"],
            rule["uplink"],
            "",
            "",
            "",
            style="bold",
        )
        for idx, entry in enumerate(rule["allowedInbound"]):
            is_last_row = idx == len(rule["allowedInbound"]) - 1
            table.add_row(
                "",
                "",
                "",
                "",
                entry["protocol"],
                ",".join(entry["destinationPorts"]),
                ",".join(entry["allowedIps"]),
                end_section=is_last_row,
            )

    return table


def table_network_health(health, title=None, include_network_name=False):
    """
    Create table of network health alerts
    """
    columns = ["Alert", "Category", "Severity", "Details"]
    if include_network_name:
        columns.insert(0, "Network")
        empty_columns = ("", "", "", "")
    else:
        empty_columns = ("", "", "")
    table = table_with_columns(columns, title=title)

    for alert in health:
        row_items = (
            alert["type"],
            alert["category"],
            f"[{severity_styles.get(alert['severity'], '')}]{alert['severity'].capitalize()}",
            "",
        )
        if include_network_name:
            table.add_row(alert["network_name"], *row_items)
        else:
            table.add_row(*row_items)

        # Create additional rows for devices / applications if needed
        for app in alert["scope"]["applications"]:
            table.add_row(*empty_columns, f"-- Application details --")

        for device in alert["scope"]["devices"]:
            detail = f"{device['productType'].capitalize()}: {device['name']}"
            if device.get("lldp"):
                detail += f" Port #{device['lldp']['portId']}"
            table.add_row(*empty_columns, detail)

    return table
