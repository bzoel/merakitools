"""
merakitools - dashboard.py
Billy Zoellers

CLI tools for managing Meraki networks based on Typer
"""
import meraki
from meraki.exceptions import APIError
from merakitools.__init__ import __version__
from merakitools.console import console

try:
    dashboard = meraki.DashboardAPI(
        output_log=False,
        print_console=False,
        suppress_logging=True,
        caller=f"merakitools/{__version__}",
    )
except APIError:
    console.print("[bold red]Unable to connect to the Meraki Dashboard.")
    console.print_exception()
