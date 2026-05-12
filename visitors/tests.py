from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import response, status
from visitors.models import Building, Visitor

class BuildingAPITests(TestCase):
    """Tests for the Building API endpoints"""
    def setUp(self):
        self.client = APIClient()
        self.building = Building.objects.create(
            name="Main Office",
            address="123 Main St",
            building_code="MOFF",
            phone="5551234567"
        )
    
    def test_list_buildings(self):
        """GET /api/buildings/ returns all buildings"""
        response = self.client.get('/api/buildings/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], "Main Office")
    
    def test_create_building(self):
        """POST /api/buildings/ creates a new building"""
        data = {
            "name": "Annex",
            "address": "456 Side St",
            "building_code": "ANEX",
            "phone": "5559876543"
        }
        response = self.client.post('/api/buildings/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Building.objects.count(), 2)
        self.assertEqual(Building.objects.get(id=response.data['id']).name, "Annex")

    def test_create_building_duplicate_code(self): 
        """POST /api/buildings/ with duplicate building_code should fail"""
        data = {
            "name": "Duplicate Code Building",
            "address": "789 Another St",
            "building_code": "MOFF",  # Same code as existing building
            "phone": "5551112222"
        }
        response = self.client.post('/api/buildings/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_building(self):
        """DELETE /api/buildings/:id/ removes the building"""
        response = self.client.delete(f"/api/buildings/{self.building.id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Building.objects.count(), 0)
    
class VisitorAPITests(TestCase):
    """Tests for the Visitor API endpoints"""
    def setUp(self):
        self.client = APIClient()
        self.building = Building.objects.create(
            name="Main Office",
            address="123 Main St",
            building_code="MOFF",
            phone="5551234567"
        )
        self.visitor = Visitor.objects.create(
            first_name="John",
            last_name="Doe",
            email="test@email.com",
            phone="5550001111",
            building=self.building
        )

    def test_list_visitors(self):
        """GET /api/visitors/ returns all visitors"""
        response = self.client.get('/api/visitors/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['first_name'], "John")
        
    def test_create_visitor(self):
        """POST /api/visitors/ creates a visitor with auto check_in"""
        data = {
            "first_name": "Jane",
            "last_name": "Smith",
            "email": "jane@email.com",
            "phone": "5552223333",
            "building": self.building.id
        }
        response = self.client.post('/api/visitors/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Visitor.objects.count(), 2)
        self.assertEqual(Visitor.objects.get(id=response.data['id']).first_name, "Jane")

    def test_create_visitor_invalid_building_fails(self):
        """POST with non-existent building ID should fail"""
        data = {
            "first_name": "Bad",
            "last_name": "Visitor",
            "email": "bad@example.com",
            "phone": "5555550003",
            "building": 9999,
        }
        response = self.client.post("/api/visitors/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)       

    def test_checkout_visitor(self):
        """PATCH /api/visitors/:id/ adds check_out timestamp"""
        data = {"check_out": "2026-05-11T17:00:00Z"}
        response = self.client.patch(f"/api/visitors/{self.visitor.id}/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(response.data["check_out"])
    
    def test_cascade_delete(self):
        """Deleting a building should cascade-delete its visitors"""
        self.building.delete()
        self.assertEqual(Visitor.objects.count(), 0)
