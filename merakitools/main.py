"""
merakitools - main.py
Billy Zoellers

CLI tools for managing Meraki networks based on Typer
"""

import sys
import typer
from merakitools import orgs, networks, devices, mx, ms, mr, mt, msp

# Python 3.9+ is required
MIN_PYTHON = (3, 9)
if sys.version_info < MIN_PYTHON:
    sys.exit(f"Python {MIN_PYTHON[0]}.{MIN_PYTHON[1]} or later is required")

typer_params = {
    "no_args_is_help": True,
}

app = typer.Typer(**typer_params, rich_markup_mode="rich")
app.add_typer(orgs.app, name="orgs", help="Meraki organizations", **typer_params)
app.add_typer(networks.app, name="networks", help="Meraki networks", **typer_params)
app.add_typer(devices.app, name="devices", help="Meraki devices", **typer_params)
app.add_typer(mx.app, name="mx", help="Meraki MX appliances", **typer_params)
app.add_typer(ms.app, name="ms", help="Meraki MS switches", **typer_params)
app.add_typer(mr.app, name="mr", help="Meraki MR wireless", **typer_params)
app.add_typer(mt.app, name="mt", help="Meraki MT sensors", **typer_params)
app.add_typer(msp.app, name="msp", help="Manage multiple networks", **typer_params)
