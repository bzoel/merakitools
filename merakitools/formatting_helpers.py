"""
merakitools - formatting_helpers.py
Billy Zoellers

CLI tools for managing Meraki networks based on Typer
"""
from typing import List, Optional
from rich.table import Table, Column
from rich import box
import re


def camel_case_split(str) -> str:
    """
    Input: applicationCategory
    Output: Application Category
    """
    return re.sub(r"(\w)([A-Z])", r"\1 \2", str).capitalize()


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
