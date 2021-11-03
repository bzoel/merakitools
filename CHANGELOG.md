# merakitools - CHANGELOG
### v0.1.7
 - [new] Update network traffic analysis settings
 - [new] List and create network webhook servers
 - [new] List, create, delete network webhook payload templates
 - [new] Claim an order and add devices to network
 - [new] List MR L3/L7 firewall rules
 - [new] Ping device or IP/FQDN using device livetools

 - [update] *mr update-ssid* command now includes *local LAN firewall*

### v0.1.6
 - [new] Update network settings
 - [new] Create organization, claim orders, and add admins
 - [new] Enable SAML and update SAML parameters
 - [new] Accept organization name *or* ID
 - [new] New spinner and table format

 - [update] *mr update-ssid* command now includes *encryption mode*, *WPA encryption mode*

 - [fix] *orgs api* command can list, enable, or disable and is now idempotent
 - [fix] Python Black library for better formatting
 - [fix] Find single organization without y/n questions
 - [fix] various refactoring

### v0.1.5
 - Added multiple commands to **ms** and **mr** modules

### v0.1.4
 - Added **ms** and **mr** modules
 - Added commands for **mr** for RF profiles, RF settings, SSIDs, and mesh performance
 - Added commands for **ms** for switchport utilization diagnostics
 - Added *reboot* and *blink-led* commands for **devices**
 - Added *api* and *list-api-requests* commands for **orgs**

 *Various bugfixes*