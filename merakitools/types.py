"""
merakitools - networks.py
Billy Zoellers

CLI tools for managing Meraki networks based on Typer
"""
from enum import Enum


class ProductType(str, Enum):
    """
    Types of Meraki products
    """

    appliance = "appliance"
    switch = "switch"
    wireless = "wireless"
    camera = "camera"
    systemsManager = "systemsManager"
    enviornmental = "enviornmental"
    sensor = "sensor"
    cellularGateway = "cellularGateway"


class DeviceModel(str, Enum):
    """
    Models of Meraki devices
    """

    MX = "MX"
    MR = "MR"
    MS = "MS"
    MV = "MV"
    MT = "MT"
    Z = "Z"


class DeviceSortOptions(str, Enum):
    """
    Options to sort a list of devices
    """

    name = "name"
    model = "model"


class FirewallPolicyOption(str, Enum):
    """
    Firewall policy options
    """

    allow = "allow"
    deny = "deny"


class MXInternetUplinks(str, Enum):
    """
    Uplink types on an MX device
    """

    one = "internet1"
    two = "internet2"


class TrafficDirection(str, Enum):
    """
    Directions traffic can flow from an interface
    """

    total = "total"
    recv = "recv"
    sent = "sent"


class MSInterfaceMode(str, Enum):
    """
    Interface modes on an MS switch
    """

    access = "access"
    trunk = "trunk"


class MSSTPGuardType(str, Enum):
    """ "
    STP Guard modues on an MS switch
    """

    disabled = "disabled"
    root = "root guard"
    bpdu = "bpdu guard"
    loop = "loop guard"


class MRSSIDAuthMode(str, Enum):
    """
    Authentication modes on an MR SSID
    """

    open = "open"
    psk = "psk"
    open_with_radius = "open-with-radius"
    dot1x_meraki = "8021x-meraki"
    dot1x_radius = "8021x-radius"
    dot1x_google = "8021x-google"
    dot1x_localradius = "8021x-localradius"
    ipsk_with_radius = "ipsk-with-radius"
    ipsk_without_radius = "ipsk-without-radius"


class MRSSIDEncryptionMode(str, Enum):
    """
    Encryption modes on an MR SSID
    """

    wep = "wep"
    wpa = "wpa"


class MRSSIDWPAEncrytionMode(str, Enum):
    """
    WPA Encryption modes on an MR SSID
    """

    wpa1_only = "WPA1 only"
    wpa12 = "WPA1 and WPA2"
    wpa2_only = "WPA2 only"
    wpa3_transition = "WPA3 Transition Mode"
    wpa3_only = "WPA3 only"


class MRSSIDIPAssignmentMode(str, Enum):
    """
    IP assignment mode on an MR SSID
    """

    nat_mode = "NAT mode"
    bridge_mode = "Bridge mode"
    l3_roaming = "Layer 3 roaming"
    l3_roaming_concentrator = "Layer 3 roaming with a concentrator"
    vpn = "VPN"


class NetworkTrafficAnalysisMode(str, Enum):
    """
    Traffic Analysis mode for a network
    """

    disabled = "disabled"
    basic = "basic"
    detailed = "detailed"


class MTMetricType(str, Enum):
    """
    Meraki MT metric types
    """

    battery = "battery"
    temperature = "temperature"
    humidity = "humidity"
    water = "water"
    door = "door"
    noise = "noise"
    co2 = "co2"
    tvoc = "tvoc"
    indoorAirQuality = "indoorAirQuality"
    pm25 = "pm25"
    button = "button"
