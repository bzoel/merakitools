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
  """"
  STP Guard modues on an MS switch
  """
  disabled = "disabled"
  root = "root guard"
  bpdu = "bpdu guard"
  loop = "loop guard"
