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
