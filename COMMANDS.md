# `merakitools`

**Usage**:

```console
$ merakitools [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--install-completion`: Install completion for the current shell.
* `--show-completion`: Show completion for the current shell, to copy it or customize the installation.
* `--help`: Show this message and exit.

**Commands**:

* `devices`: Meraki devices
* `mr`: Meraki MR wireless
* `ms`: Meraki MS switches
* `msp`: Manage multiple networks
* `mx`: Meraki MX appliances
* `networks`: Meraki networks
* `orgs`: Meraki organizations

## `merakitools devices`

Meraki devices

**Usage**:

```console
$ merakitools devices [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--help`: Show this message and exit.

**Commands**:

* `blink-led`: Blink the LEDs of device(s)
* `list`: List Meraki devices
* `ping`: Ping a Meraki device
* `reboot`: Reboot device(s)
* `show-lldp`: Show CDP/LLDP information for Meraki...
* `update`: Update parameters of a Meraki device

### `merakitools devices blink-led`

Blink the LEDs of device(s)

**Usage**:

```console
$ merakitools devices blink-led [OPTIONS]
```

**Options**:

* `--serial TEXT`
* `--duration INTEGER RANGE`: [default: 20]
* `--help`: Show this message and exit.

### `merakitools devices list`

List Meraki devices

**Usage**:

```console
$ merakitools devices list [OPTIONS] ORGANIZATION_NAME NETWORK_NAME
```

**Arguments**:

* `ORGANIZATION_NAME`: [required]
* `NETWORK_NAME`: [required]

**Options**:

* `--type [MX|MR|MS|MV|MT|Z]`
* `--sort-by [name|model]`: [default: model]
* `--sort-reverse / --no-sort-reverse`: [default: False]
* `--help`: Show this message and exit.

### `merakitools devices ping`

Ping a Meraki device

**Usage**:

```console
$ merakitools devices ping [OPTIONS] SERIAL
```

**Arguments**:

* `SERIAL`: [required]

**Options**:

* `--target TEXT`: Specify a target IP or FQDN
* `--count INTEGER RANGE`: Number of pings  [default: 5]
* `--help`: Show this message and exit.

### `merakitools devices reboot`

Reboot device(s)

**Usage**:

```console
$ merakitools devices reboot [OPTIONS]
```

**Options**:

* `--serial TEXT`
* `--help`: Show this message and exit.

### `merakitools devices show-lldp`

Show CDP/LLDP information for Meraki device(s)

**Usage**:

```console
$ merakitools devices show-lldp [OPTIONS]
```

**Options**:

* `--serial TEXT`
* `--organization-name TEXT`
* `--network-name TEXT`
* `--help`: Show this message and exit.

### `merakitools devices update`

Update parameters of a Meraki device

**Usage**:

```console
$ merakitools devices update [OPTIONS] SERIAL...
```

**Arguments**:

* `SERIAL...`: [required]

**Options**:

* `--name TEXT`
* `--address TEXT`
* `--notes TEXT`
* `--add-tag TEXT`
* `--remove-tag TEXT`
* `--help`: Show this message and exit.

## `merakitools mr`

Meraki MR wireless

**Usage**:

```console
$ merakitools mr [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--help`: Show this message and exit.

**Commands**:

* `list-l3-fw`: List layer 3 firewall rules for an SSID
* `list-l7-fw`: List layer 7 firewall rules for an SSID
* `list-mesh`: List mesh status for a network
* `list-rf`: List RF settings for a network
* `list-rf-profiles`: List RF profiles for a network
* `list-ssid`: List configured SSIDs for a network
* `show-ssid`: Show an SSID for a network TODO: formatting
* `update-ssid`: Update an SSID for a network

### `merakitools mr list-l3-fw`

List layer 3 firewall rules for an SSID

**Usage**:

```console
$ merakitools mr list-l3-fw [OPTIONS] ORGANIZATION_NAME NETWORK_NAME SSID_NUMBER
```

**Arguments**:

* `ORGANIZATION_NAME`: [required]
* `NETWORK_NAME`: [required]
* `SSID_NUMBER`: The SSID number  [required]

**Options**:

* `--help`: Show this message and exit.

### `merakitools mr list-l7-fw`

List layer 7 firewall rules for an SSID

**Usage**:

```console
$ merakitools mr list-l7-fw [OPTIONS] ORGANIZATION_NAME NETWORK_NAME SSID_NUMBER
```

**Arguments**:

* `ORGANIZATION_NAME`: [required]
* `NETWORK_NAME`: [required]
* `SSID_NUMBER`: The SSID number  [required]

**Options**:

* `--help`: Show this message and exit.

### `merakitools mr list-mesh`

List mesh status for a network

**Usage**:

```console
$ merakitools mr list-mesh [OPTIONS] ORGANIZATION_NAME NETWORK_NAME
```

**Arguments**:

* `ORGANIZATION_NAME`: [required]
* `NETWORK_NAME`: [required]

**Options**:

* `--help`: Show this message and exit.

### `merakitools mr list-rf`

List RF settings for a network

**Usage**:

```console
$ merakitools mr list-rf [OPTIONS] ORGANIZATION_NAME NETWORK_NAME
```

**Arguments**:

* `ORGANIZATION_NAME`: [required]
* `NETWORK_NAME`: [required]

**Options**:

* `--help`: Show this message and exit.

### `merakitools mr list-rf-profiles`

List RF profiles for a network

**Usage**:

```console
$ merakitools mr list-rf-profiles [OPTIONS] ORGANIZATION_NAME NETWORK_NAME
```

**Arguments**:

* `ORGANIZATION_NAME`: [required]
* `NETWORK_NAME`: [required]

**Options**:

* `--help`: Show this message and exit.

### `merakitools mr list-ssid`

List configured SSIDs for a network

**Usage**:

```console
$ merakitools mr list-ssid [OPTIONS] ORGANIZATION_NAME NETWORK_NAME
```

**Arguments**:

* `ORGANIZATION_NAME`: [required]
* `NETWORK_NAME`: [required]

**Options**:

* `--include-disabled`: [default: False]
* `--include-psk / --no-include-psk`: [default: False]
* `--help`: Show this message and exit.

### `merakitools mr show-ssid`

Show an SSID for a network

TODO: formatting

**Usage**:

```console
$ merakitools mr show-ssid [OPTIONS] ORGANIZATION_NAME NETWORK_NAME SSID_NUMBER
```

**Arguments**:

* `ORGANIZATION_NAME`: [required]
* `NETWORK_NAME`: [required]
* `SSID_NUMBER`: [required]

**Options**:

* `--help`: Show this message and exit.

### `merakitools mr update-ssid`

Update an SSID for a network

**Usage**:

```console
$ merakitools mr update-ssid [OPTIONS] ORGANIZATION_NAME NETWORK_NAME SSID_NUMBER
```

**Arguments**:

* `ORGANIZATION_NAME`: [required]
* `NETWORK_NAME`: [required]
* `SSID_NUMBER`: The SSID number  [required]

**Options**:

* `--confirm / --no-confirm`: Confirm the current SSID name before applying changes  [default: True]
* `--enabled / --no-enabled`: Whether or not the SSID is enabled
* `--name TEXT`: The name of the SSID
* `--auth-mode [open|psk|open-with-radius|8021x-meraki|8021x-radius|8021x-google|8021x-localradius|ipsk-with-radius|ipsk-without-radius]`: The association control method for the SSID
* `--encryption-mode [wep|wpa]`: The PSK encryption mode for the SSID
* `--wpa-encryption-mode [WPA1 only|WPA1 and WPA2|WPA2 only|WPA3 Transition Mode|WPA3 only]`: The types of WPA encryption
* `--tag-vlan / --no-tag-vlan`: Whether or not traffic shuold be directed to use specific VLANs
* `--default-vlan-id INTEGER RANGE`: The default VLAN ID used for 'all other APs'
* `--pre-shared-key TEXT`: The passkey for the SSID
* `--min-bitrate INTEGER RANGE`: The minimum bitrate in Mbps
* `--ip-assignment-mode [NAT mode|Bridge mode|Layer 3 roaming|Layer 3 roaming with a concentrator|VPN]`: The client IP assignment mode
* `--local-lan-access [allow|deny]`: Policy for wireless clients accessing the Local LAN
* `--help`: Show this message and exit.

## `merakitools ms`

Meraki MS switches

**Usage**:

```console
$ merakitools ms [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--help`: Show this message and exit.

**Commands**:

* `diag-switchport-traffic`: Diagnose all switchports on a network of MS...
* `list-routing-interfaces`: List L3 routed interfaces on an MS switch or...
* `list-stacks`: List switch stacks
* `update-switchport`: Update switchport(s)

### `merakitools ms diag-switchport-traffic`

Diagnose all switchports on a network of MS switches to find
switchports that are top talkers at a given instant

** This command gathers a significant amount of data and may
take some time to complete on larger networks **

**Usage**:

```console
$ merakitools ms diag-switchport-traffic [OPTIONS] ORGANIZATION_NAME NETWORK_NAME
```

**Arguments**:

* `ORGANIZATION_NAME`: [required]
* `NETWORK_NAME`: [required]

**Options**:

* `--top INTEGER`: [default: 100]
* `--sort-by [total|recv|sent]`: [default: total]
* `--interface-mode [access|trunk]`
* `--ignore-device-tag TEXT`
* `--ignore-switchport-tag TEXT`
* `--help`: Show this message and exit.

### `merakitools ms list-routing-interfaces`

List L3 routed interfaces on an MS switch or stack

**Usage**:

```console
$ merakitools ms list-routing-interfaces [OPTIONS] ORGANIZATION_NAME NETWORK_NAME SERIAL
```

**Arguments**:

* `ORGANIZATION_NAME`: [required]
* `NETWORK_NAME`: [required]
* `SERIAL`: [required]

**Options**:

* `--include-dhcp / --no-include-dhcp`: [default: False]
* `--help`: Show this message and exit.

### `merakitools ms list-stacks`

List switch stacks

**Usage**:

```console
$ merakitools ms list-stacks [OPTIONS] ORGANIZATION_NAME NETWORK_NAME
```

**Arguments**:

* `ORGANIZATION_NAME`: [required]
* `NETWORK_NAME`: [required]

**Options**:

* `--help`: Show this message and exit.

### `merakitools ms update-switchport`

Update switchport(s)

**Usage**:

```console
$ merakitools ms update-switchport [OPTIONS] SERIAL
```

**Arguments**:

* `SERIAL`: [required]

**Options**:

* `--port INTEGER RANGE`
* `--port-range TEXT`
* `--name TEXT`
* `--enabled / --no-enabled`
* `--poe-enabled / --no-poe-enabled`
* `--type [access|trunk]`
* `--vlan INTEGER RANGE`
* `--voice-vlan INTEGER RANGE`
* `--rtsp-enabled / --no-rtsp-enabled`
* `--stp-guard [disabled|root guard|bpdu guard|loop guard]`
* `--add-tag TEXT`
* `--remove-tag TEXT`
* `--help`: Show this message and exit.

## `merakitools msp`

Manage multiple networks

**Usage**:

```console
$ merakitools msp [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--help`: Show this message and exit.

**Commands**:

* `enable-api-all`: Enable the Meraki API for all accessible...
* `list-security-events`: List security events for organization(s),...

### `merakitools msp enable-api-all`

Enable the Meraki API for all accessible organizations

**Usage**:

```console
$ merakitools msp enable-api-all [OPTIONS]
```

**Options**:

* `--help`: Show this message and exit.

### `merakitools msp list-security-events`

List security events for organization(s), filtering by organization or event name

**Usage**:

```console
$ merakitools msp list-security-events [OPTIONS]
```

**Options**:

* `--days-ago INTEGER`: How many days to look back for events  [default: 3]
* `--organization-name TEXT`: Specify organization
* `--filter-event-name TEXT`: Filter by event message
* `--help`: Show this message and exit.

## `merakitools mx`

Meraki MX appliances

**Usage**:

```console
$ merakitools mx [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--help`: Show this message and exit.

**Commands**:

* `add-staticroute`: Add one or more static routes to an MX device
* `create-staticnat`: Add a 1:1 NAT entry to an MX device
* `list-routes`: List MX device routes
* `list-vlans`

### `merakitools mx add-staticroute`

Add one or more static routes to an MX device

**Usage**:

```console
$ merakitools mx add-staticroute [OPTIONS] ORGANIZATION_NAME NETWORK_NAME
```

**Arguments**:

* `ORGANIZATION_NAME`: [required]
* `NETWORK_NAME`: [required]

**Options**:

* `--route TEXT`
* `--default-next-hop TEXT`
* `--help`: Show this message and exit.

### `merakitools mx create-staticnat`

Add a 1:1 NAT entry to an MX device

**Usage**:

```console
$ merakitools mx create-staticnat [OPTIONS] ORGANIZATION_NAME NETWORK_NAME
```

**Arguments**:

* `ORGANIZATION_NAME`: [required]
* `NETWORK_NAME`: [required]

**Options**:

* `--nat TEXT`
* `--port TEXT`
* `--uplink [internet1|internet2]`: [default: internet1]
* `--confirm / --no-confirm`: [default: True]
* `--help`: Show this message and exit.

### `merakitools mx list-routes`

List MX device routes

**Usage**:

```console
$ merakitools mx list-routes [OPTIONS] ORGANIZATION_NAME NETWORK_NAME
```

**Arguments**:

* `ORGANIZATION_NAME`: [required]
* `NETWORK_NAME`: [required]

**Options**:

* `--name TEXT`: Only show routes with a specific name
* `--subnet TEXT`: Only show routes with a specific subnet
* `--gateway TEXT`: Only show routes with a specific gateway
* `--help`: Show this message and exit.

### `merakitools mx list-vlans`

**Usage**:

```console
$ merakitools mx list-vlans [OPTIONS] ORGANIZATION_NAME NETWORK_NAME
```

**Arguments**:

* `ORGANIZATION_NAME`: [required]
* `NETWORK_NAME`: [required]

**Options**:

* `--include-dhcp / --no-include-dhcp`: Include DHCP information for each subnet  [default: False]
* `--help`: Show this message and exit.

## `merakitools networks`

Meraki networks

**Usage**:

```console
$ merakitools networks [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--help`: Show this message and exit.

**Commands**:

* `delete-payload-template`: Delete a webhook payload template
* `list`: List Meraki networks in an organization
* `list-payload-templates`: List webhook payload templates for a network
* `list-webhook-servers`: List webhook servers for a network
* `new-payload-template`: Create a webhook payload template
* `new-webhook-server`: Create a new webhook server for a network
* `traffic-analysis`: Get or update the traffic analysis mode for a...
* `update-settings`: Update network settings

### `merakitools networks delete-payload-template`

Delete a webhook payload template

**Usage**:

```console
$ merakitools networks delete-payload-template [OPTIONS] ORGANIZATION_NAME NETWORK_NAME
```

**Arguments**:

* `ORGANIZATION_NAME`: [required]
* `NETWORK_NAME`: [required]

**Options**:

* `--name TEXT`: Name of the payload template  [required]
* `--confirm / --no-confirm`: Confirm before deleting  [default: True]
* `--help`: Show this message and exit.

### `merakitools networks list`

List Meraki networks in an organization

**Usage**:

```console
$ merakitools networks list [OPTIONS] ORGANIZATION_NAME
```

**Arguments**:

* `ORGANIZATION_NAME`: [required]

**Options**:

* `--product-type [appliance|switch|wireless|camera|systemsManager|enviornmental|sensor|cellularGateway]`
* `--help`: Show this message and exit.

### `merakitools networks list-payload-templates`

List webhook payload templates for a network

**Usage**:

```console
$ merakitools networks list-payload-templates [OPTIONS] ORGANIZATION_NAME NETWORK_NAME
```

**Arguments**:

* `ORGANIZATION_NAME`: [required]
* `NETWORK_NAME`: [required]

**Options**:

* `--help`: Show this message and exit.

### `merakitools networks list-webhook-servers`

List webhook servers for a network

**Usage**:

```console
$ merakitools networks list-webhook-servers [OPTIONS] ORGANIZATION_NAME NETWORK_NAME
```

**Arguments**:

* `ORGANIZATION_NAME`: [required]
* `NETWORK_NAME`: [required]

**Options**:

* `--help`: Show this message and exit.

### `merakitools networks new-payload-template`

Create a webhook payload template

**Usage**:

```console
$ merakitools networks new-payload-template [OPTIONS] ORGANIZATION_NAME NETWORK_NAME
```

**Arguments**:

* `ORGANIZATION_NAME`: [required]
* `NETWORK_NAME`: [required]

**Options**:

* `--name TEXT`: A name for the payload template  [required]
* `--headers FILENAME`: A file with the headers template  [required]
* `--body FILENAME`: A file with the body template  [required]
* `--help`: Show this message and exit.

### `merakitools networks new-webhook-server`

Create a new webhook server for a network

**Usage**:

```console
$ merakitools networks new-webhook-server [OPTIONS] ORGANIZATION_NAME NETWORK_NAME
```

**Arguments**:

* `ORGANIZATION_NAME`: [required]
* `NETWORK_NAME`: [required]

**Options**:

* `--name TEXT`: A name for easy reference  [required]
* `--shared-secret TEXT`: A shared secret included in POSTs send to the HTTP server
* `--url TEXT`: The URL of the HTTP server. Cannot be updated later.  [required]
* `--help`: Show this message and exit.

### `merakitools networks traffic-analysis`

Get or update the traffic analysis mode for a network

**Usage**:

```console
$ merakitools networks traffic-analysis [OPTIONS] ORGANIZATION_NAME NETWORK_NAME
```

**Arguments**:

* `ORGANIZATION_NAME`: [required]
* `NETWORK_NAME`: [required]

**Options**:

* `--confirm / --no-confirm`: Confirm the network name before applying changes  [default: True]
* `--set-mode [disabled|basic|detailed]`: Traffic analysis mode for network
* `--help`: Show this message and exit.

### `merakitools networks update-settings`

Update network settings

**Usage**:

```console
$ merakitools networks update-settings [OPTIONS] ORGANIZATION_NAME NETWORK_NAME
```

**Arguments**:

* `ORGANIZATION_NAME`: [required]
* `NETWORK_NAME`: [required]

**Options**:

* `--confirm / --no-confirm`: Confirm the network name before applying changes  [default: True]
* `--enable-local-status / --disable-local-status`: Local device status pages
* `--enable-remote-status / --disable-remote-status`: Remote device status pages
* `--help`: Show this message and exit.

## `merakitools orgs`

Meraki organizations

**Usage**:

```console
$ merakitools orgs [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--help`: Show this message and exit.

**Commands**:

* `api`: Organization API status
* `claim-order`: Claim an order into an organization
* `create`: Create a new Meraki organization
* `create-ip-objects`: Create new IP objects within organization,...
* `create-saml-idp`: Create a SAML IDP
* `create-saml-role`: Create a SAML role
* `list`: List Meraki organizations
* `list-api-requests`: List API requests for organization
* `saml`: Organization SAML status

### `merakitools orgs api`

Organization API status

**Usage**:

```console
$ merakitools orgs api [OPTIONS] ORGANIZATION_NAME
```

**Arguments**:

* `ORGANIZATION_NAME`: [required]

**Options**:

* `--enable / --disable`
* `--help`: Show this message and exit.

### `merakitools orgs claim-order`

Claim an order into an organization

**Usage**:

```console
$ merakitools orgs claim-order [OPTIONS] ORGANIZATION_NAME
```

**Arguments**:

* `ORGANIZATION_NAME`: [required]

**Options**:

* `--order-number TEXT`: [required]
* `--claim-to-network-name TEXT`
* `--help`: Show this message and exit.

### `merakitools orgs create`

Create a new Meraki organization

**Usage**:

```console
$ merakitools orgs create [OPTIONS] NAME
```

**Arguments**:

* `NAME`: [required]

**Options**:

* `--org-admin TEXT`: Org admins in Name!Email format
* `--claim-order TEXT`
* `--help`: Show this message and exit.

### `merakitools orgs create-ip-objects`

Create new IP objects within organization, optionally adding to specified group

**Usage**:

```console
$ merakitools orgs create-ip-objects [OPTIONS] ORGANIZATION_NAME
```

**Arguments**:

* `ORGANIZATION_NAME`: [required]

**Options**:

* `--group-name TEXT`
* `--object TEXT`
* `--help`: Show this message and exit.

### `merakitools orgs create-saml-idp`

Create a SAML IDP

**Usage**:

```console
$ merakitools orgs create-saml-idp [OPTIONS] ORGANIZATION_NAME SAML_X509_CERT SAML_SLO_LOGOUT
```

**Arguments**:

* `ORGANIZATION_NAME`: [required]
* `SAML_X509_CERT`: [required]
* `SAML_SLO_LOGOUT`: [required]

**Options**:

* `--help`: Show this message and exit.

### `merakitools orgs create-saml-role`

Create a SAML role

**Usage**:

```console
$ merakitools orgs create-saml-role [OPTIONS] ORGANIZATION_NAME ROLE
```

**Arguments**:

* `ORGANIZATION_NAME`: [required]
* `ROLE`: [required]

**Options**:

* `--access TEXT`: [default: full]
* `--help`: Show this message and exit.

### `merakitools orgs list`

List Meraki organizations

**Usage**:

```console
$ merakitools orgs list [OPTIONS]
```

**Options**:

* `--name TEXT`
* `--include-counts / --no-include-counts`: [default: False]
* `--help`: Show this message and exit.

### `merakitools orgs list-api-requests`

List API requests for organization

**Usage**:

```console
$ merakitools orgs list-api-requests [OPTIONS] ORGANIZATION_NAME
```

**Arguments**:

* `ORGANIZATION_NAME`: [required]

**Options**:

* `--help`: Show this message and exit.

### `merakitools orgs saml`

Organization SAML status

**Usage**:

```console
$ merakitools orgs saml [OPTIONS] ORGANIZATION_NAME
```

**Arguments**:

* `ORGANIZATION_NAME`: [required]

**Options**:

* `--enable / --disable`
* `--help`: Show this message and exit.
