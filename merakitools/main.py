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

import merakitools.orgs as orgs

app = typer.Typer()
app.add_typer(orgs.app, name="orgs", help="Meraki organizations")