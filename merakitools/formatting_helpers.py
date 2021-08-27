"""
merakitools - formatting_helpers.py
Billy Zoellers

CLI tools for managing Meraki networks based on Typer
"""
from rich.table import Table

def table_with_columns(columns, title=None, first_column_name=None,):
  """
  Generate a table with specified columns
  """
  table = Table(title=title)
  if first_column_name:
    table.add_column(first_column_name, style="bold blue")
  for col in columns:
    table.add_column(col)

  return table