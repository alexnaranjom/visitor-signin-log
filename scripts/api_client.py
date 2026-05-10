"""
REST client that talks to the Visitor Sign-In Log API.
Mirrors how ServiceNow REST Messages work:
  - Define endpoint URL
  - Set HTTP method (GET, POST, PUT, DELETE)
  - Send payload as JSON
  - Parse the JSON response
"""

import requests

BASE_URL = "http://127.0.0.1:8000/api"

def get_all_buildings():
    """Fetches all buildings from the API
    GET /api/buildings/ -- like GlideRecord query on a ServiceNow table"""
    response = requests.get(f"{BASE_URL}/buildings/")
    response.raise_for_status()  # Raise an error for bad responses
    buildings = response.json()
    print(f"\n---- All Buildings ---- ({len(buildings)}) ----")
    for building in buildings:
        print(f" [{building['id']}] {building['name']} {building['building_code']}) ")
    
    return buildings

def get_all_visitors():
    """Fetches all visitors from the API
    GET /api/visitors/ -- like GlideRecord query on a ServiceNow table"""
    response = requests.get(f"{BASE_URL}/visitors/")
    response.raise_for_status()  # Raise an error for bad responses
    visitors = response.json()
    print(f"\n---- All Visitors ---- ({len(visitors)}) ----")
    for visitor in visitors:
        print(f" [{visitor['id']}] {visitor['first_name']} {visitor['last_name']} visiting {visitor['building']['name']} (Checked in: {visitor['check_in']}, Checked out: {visitor['check_out']})")
    
    return visitors



              
  
