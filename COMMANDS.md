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

* `list-mesh`: List mesh status for a network
* `list-rf`: List RF settings for a network
* `list-rf-profiles`: List RF profiles for a network
* `list-ssid`: List configured SSIDs for a network
* `show-ssid`: Show an SSID for a network TODO: formatting
* `update-ssid`: Update an SSID for a network

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
* `SSID_NUMBER`: [required]

**Options**:

* `--confirm / --no-confirm`: [default: True]
* `--enabled / --no-enabled`
* `--name TEXT`
* `--auth-mode [open|psk|open-with-radius|8021x-meraki|8021x-radius|8021x-google|8021x-localradius|ipsk-with-radius|ipsk-without-radius]`
* `--tag-vlan / --no-tag-vlan`
* `--default-vlan-id INTEGER RANGE`
* `--pre-shared-key TEXT`
* `--min-bitrate INTEGER`
* `--ip-assignment-mode [NAT mode|Bridge mode|Layer 3 roaming|Layer 3 roaming with a concentrator|VPN]`
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

## `merakitools networks`

Meraki networks

**Usage**:

```console
$ merakitools networks [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--help`: Show this message and exit.

**Commands**:

* `list`: List Meraki networks in an organization

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

## `merakitools orgs`

Meraki organizations

**Usage**:

```console
$ merakitools orgs [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--help`: Show this message and exit.

**Commands**:

* `api`: Enable or disable Meraki API
* `create-ip-objects`: Create new IP objects within organization,...
* `list`: List Meraki organizations
* `list-api-requests`: List API requests for organization

### `merakitools orgs api`

Enable or disable Meraki API

**Usage**:

```console
$ merakitools orgs api [OPTIONS] ORGANIZATION_NAME
```

**Arguments**:

* `ORGANIZATION_NAME`: [required]

**Options**:

* `--enable / --disable`
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
