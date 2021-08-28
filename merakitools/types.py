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
  one = "internet1"
  two = "internet2"