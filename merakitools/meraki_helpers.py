"""
merakitools - meraki_helpers.py
Billy Zoellers

CLI tools for managing Meraki networks based on Typer
"""

def find_orgs_by_name(dashboard, org_name):
  """
  Given a name, find any matching organizations
  """
  orgs = dashboard.organizations.getOrganizations()
  if org_name:
    orgs = [org for org in orgs if org_name in org['name']]
  return orgs