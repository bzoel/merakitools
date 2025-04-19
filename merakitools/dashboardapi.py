"""
merakitools - dashboard.py
Billy Zoellers

CLI tools for managing Meraki networks based on Typer
"""
import meraki
from meraki.exceptions import APIError, APIKeyError
from merakitools.__init__ import __version__
from merakitools.console import console
import sys

try:
    dashboard = meraki.DashboardAPI(
        output_log=False,
        print_console=False,
        suppress_logging=True,
        caller=f"merakitools/{__version__}",
    )
except APIKeyError:
    console.print("[bold][red]No Meraki Dashboard API Key.[/bold]\n\tTry [i]export MERAKI_DASHBOARD_API_KEY=YOUR_KEY_HERE[/i][/red]")
    sys.exit(1)
except APIError:
    console.print("[bold red]Unable to connect to the Meraki Dashboard.")
    console.print_exception()
