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
        status = "checked out" if visitor["check_out"] else "active"
        print(f"  [{visitor['id']}] {visitor['first_name']} {visitor['last_name']} -> Building {visitor['building']} ({status})")
    
    return visitors

def create_visitor(first_name, last_name, email, phone, building_id):
    """POST /api/visitors/ -- like gr.insert() in ServiceNow"""
    payload = {
        "first_name": first_name,
        "last_name": last_name,
        "email": email,
        "phone": phone,
        "building": building_id
    }
    response = requests.post(f"{BASE_URL}/visitors/", json=payload)
    response.raise_for_status()  # Raise an error for bad responses
    visitor = response.json()
    print(f"\n--- Created Visitor ---")
    print(f"  ID: {visitor['id']}")
    print(f"  Name: {visitor['first_name']} {visitor['last_name']}")
    print(f"  Check-in: {visitor['check_in']}")
    print(f"  Check-out: {visitor['check_out']}")
    return visitor

def checkout_visitor(visitor_id):
    """
    PATCH /api/visitors/:id/ -- like gr.update() in ServiceNow.
    Sets check_out to current time.
    Uses PATCH (partial update) instead of PUT (full replace).
    """
    from datetime import datetime, timezone

    payload = {"check_out": datetime.now(timezone.utc).isoformat()}  # Set check_out
    response = requests.patch(f"{BASE_URL}/visitors/{visitor_id}/", json=payload)
    response.raise_for_status()  # Raise an error for bad responses
    visitor = response.json()
    print(f"\n--- Checked Out Visitor ---")
    print(f"  {visitor['first_name']} {visitor['last_name']}")
    print(f"  Check-out: {visitor['check_out']}")
    return visitor

def delete_visitor(visitor_id):
    """DELETE /api/visitors/:id/ -- like gr.delete() in ServiceNow"""
    response = requests.delete(f"{BASE_URL}/visitors/{visitor_id}/")
    if response.status_code == 204:
        print(f"\n--- Deleted Visitor ID {visitor_id} ---")
        return True
    response.rause_for_status()  # Raise an error for bad responses

def create_building(name, building_code, address, phone):
    """POST /api/buildings/ -- like gr.insert() in ServiceNow"""
    payload = {
        "name": name,
        "building_code": building_code,
        "address": address,
        "phone": phone
    }
    response = requests.post(f"{BASE_URL}/buildings/", json=payload)
    response.raise_for_status()  # Raise an error for bad responses
    building = response.json()
    print(f"\n--- Created Building ---")
    print(f"  ID: {building['id']}")
    print(f"  Name: {building['name']} ({building['building_code']})")
    return building

def delete_building(building_id):
    """DELETE /api/buildings/:id/ -- like gr.delete() in ServiceNow"""
    response = requests.delete(f"{BASE_URL}/buildings/{building_id}/")
    if response.status_code == 204:
        print(f"\n--- Deleted Building ID {building_id} (Cascade: visitors deleted too)---")
        return True
    response.raise_for_status()  # Raise an error for bad responses

if __name__ == "__main__":
    print("=" * 60)
    print("Visitor Sign-In Log -- REST Client Demo")
    print("=" * 60)
    print("Make sure Django server is running with: python manage.py runserver")
    print("="*60)

    # 1. Read exiting data
    buildings = get_all_buildings()
    visitors = get_all_visitors()

    # 2. Create a test building
    test_building = create_building(
        name="Test Building",
        building_code="TEST",
        address="123 Test St, Test City, TS 12345",
        phone="555-0000"
    )

    # 3. Create a test visitor
    test_visitor = create_visitor(
        first_name="Test",
        last_name="User",
        email="test.user@example.com",
        phone="555-1111",
        building_id=test_building['id']
    )

    # 4. Check out the test visitor
    checked_out_visitor = checkout_visitor(test_visitor['id'])

    # 5. Delete the test visitor
    delete_visitor(test_visitor['id'])

    # 6. Delete the test building (shows cascade would work if visitors existed)
    delete_building(test_building['id'])

    # 7. Confimr original data is unchanged
    print("\n--- Final Data Check ---")
    final_buildings = get_all_buildings()
    final_visitors = get_all_visitors()
    print(f"\nBuildings: {len(final_buildings)}") 
    print(f"Visitors: {len(final_visitors)}")

    print("\n" + "="*60)
    print("Done! All CRUD operations completed successfully.")
    print("="*60)
