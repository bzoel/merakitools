"""
merakitools - formatting_helpers.py
Billy Zoellers

CLI tools for managing Meraki networks based on Typer
"""
from rich.table import Table

def table_with_columns(columns, title=None, first_column_name=None,style=None):
  """
  Generate a table with specified columns
  """
  table = Table(title=title, style=style)
  if first_column_name:
    table.add_column(first_column_name, style="bold blue")
  for col in columns:
    table.add_column(col)

  return table

def table_mx_onetoone_nat(rules, title="NAT Entries", style=None):
  """
  Generate a table to display MX one to one NAT entries
  """
  table = table_with_columns(
    ['External IP', 'Internal IP', 'Uplink', 'Protocol', 'Ports', 'Allowed IPs'],
    title=title,
    first_column_name="Name",
    style=style
  )
  for rule in rules:
    table.add_row(
      rule['name'], rule['publicIp'], rule['lanIp'], rule['uplink'], '', '', '',
      style='bold'
      )
    for idx, entry in enumerate(rule["allowedInbound"]):
      is_last_row = (idx == len(rule["allowedInbound"])-1)
      table.add_row('','','','',entry['protocol'], ','.join(entry['destinationPorts']), ','.join(entry['allowedIps']), end_section=is_last_row)

  return table