# merakitools
[![published](https://static.production.devnetcloud.com/codeexchange/assets/images/devnet-published.svg)](https://developer.cisco.com/codeexchange/github/repo/billyzoellers/merakitools)
[![CI](https://github.com/billyzoellers/merakitools/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/billyzoellers/merakitools/actions/workflows/ci.yml)
[![linting: pylint](https://img.shields.io/badge/linting-pylint-yellowgreen)](https://github.com/PyCQA/pylint)
[![security: bandit](https://img.shields.io/badge/security-bandit-yellow.svg)](https://github.com/PyCQA/bandit)

CLI tools for managing Meraki networks based on [Typer](https://typer.tiangolo.com/).

merakitools provides CLI based to monitoring and configuration tools available through the Meraki
Dashboard API. It was designed to help with bulk configuration creation and migrations to the Meraki platform.

## Installation
Install with `pip` or your favorite PyPi package mananger.
```
pip install merakitools
```

Set enviornment variable `MERAKI_DASHBOARD_API_KEY` to your Meraki API key

Then try a command.
```
merakitools orgs list
```

## Example Commands
List Meraki Networks in an organization
```
merakitools networks list <YourOrgName>
```

List Meraki MR devices in a network
```
merakitools devices list <YourOrgName> <YourNetworkName> --type MR\
```

Create a static NAT entry on a Meraki MX security appliance
```
merakitools mx create-staticnat <YourOrgName> <YourNetworkName> --nat <name>!<publicIP>!<privateIP> --port tcp!636!192.0.2.1/32 --port tcp!8080!any
```

***For more commands check out the [command documentation](COMMANDS.md).***

## Testing
For a free and easy to use testing enviornment, use the Cisco DevNet Sandbox [Meraki](https://developer.cisco.com/docs/sandbox/#!networking/meraki).
*Note: The sandbox is read-only, so you will not be able to test commands that write data to the Dashboard*

## License
Copyright (C) 2021  Billy Zoellers

This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
You should have received a copy of the GNU General Public License along with this program. If not, see <http://www.gnu.org/licenses/>.
