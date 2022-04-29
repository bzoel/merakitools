"""
merakitools - main.py
Billy Zoellers

CLI tools for managing Meraki networks based on Typer
"""

# Python 3.9+ is required
import sys

MIN_PYTHON = (3, 9)
if sys.version_info < MIN_PYTHON:
    sys.exit("Python %s.%s or later is required.\n" % MIN_PYTHON)

import typer

from merakitools import orgs, networks, devices, mx, ms, mr, mt, msp

app = typer.Typer()
app.add_typer(orgs.app, name="orgs", help="Meraki organizations")
app.add_typer(networks.app, name="networks", help="Meraki networks")
app.add_typer(devices.app, name="devices", help="Meraki devices")
app.add_typer(mx.app, name="mx", help="Meraki MX appliances")
app.add_typer(ms.app, name="ms", help="Meraki MS switches")
app.add_typer(mr.app, name="mr", help="Meraki MR wireless")
app.add_typer(mt.app, name="mt", help="Meraki MT sensors")
app.add_typer(msp.app, name="msp", help="Manage multiple networks")
