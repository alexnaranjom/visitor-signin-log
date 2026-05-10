from django.core.management.base import BaseCommand
from visitors.models import Building, Visitor
from django.utils import timezone

class Command(BaseCommand):
    help = 'Seed the database with initial data'

    def handle(self, *args, **kwargs):
        # Clear existing data
        Visitor.objects.all().delete()
        Building.objects.all().delete()

        # Create some buildings
        building_data = [
            {'name': 'Main Office', "building_code": "A-001",'address': '123 Main St', "phone": "4105551000"},
            {'name': 'Warehouse', "building_code": "B-001", 'address': '456 Warehouse Rd', "phone": "4105551001"},   
            {'name': 'Research Lab', "building_code": "C-001", 'address': '789 Research Blvd', "phone": "4105551002"},
            {'name': 'Customer Service', "building_code": "D-001", 'address': '321 Customer St', "phone": "4105551003"},
            {'name': 'IT Department', "building_code": "E-001", 'address': '654 IT Ave', "phone": "4105551004"},
            ]
        
        buildings = []
        for data in building_data:
            building = Building.objects.create(**data)
            buildings.append(building)
            # print(f'Created building: {building.name}')
            self.stdout.write(self.style.SUCCESS(f'Created building: {building.name}'))
        
        # Create some visitors
        visitor_data = [
            {"first_name": "Mario", "last_name": "Bros", "email": "marioBros@example.com", "phone": "2025551001", "building": buildings[0]},
            {"first_name": "Luigi", "last_name": "Bros", "email": "luigiBros@example.com", "phone": "2025551002", "building": buildings[0]},
            {"first_name": "Princess", "last_name": "Peach", "email": "princessPeach@example.com", "phone": "2025551003", "building": buildings[1]},
            {"first_name": "Mathew", "last_name": "Quick", "email": "mathewQuick@example.com", "phone": "2025551004", "building": buildings[2]},
            {"first_name": "David", "last_name": "Johnson", "email": "djohnson@example.com", "phone": "2025551008", "building": buildings[3]},
            {"first_name": "Emily", "last_name": "Anderson", "email": "eanderson@example.com", "phone": "2025551009", "building": buildings[4]},
            {"first_name": "Carlos", "last_name": "Rivera", "email": "crivera@example.com", "phone": "2025551010", "building": buildings[4]},
            {"first_name": "Patricia", "last_name": "Thomas", "email": "pthomas@example.com", "phone": "2025551011", "building": buildings[0]},
            {"first_name": "Daniel", "last_name": "Lee", "email": "dlee@example.com", "phone": "2025551012", "building": buildings[1]},
            {"first_name": "Jessica", "last_name": "Harris", "email": "jharris@example.com", "phone": "2025551013", "building": buildings[2]},
            {"first_name": "Kevin", "last_name": "Clark", "email": "kclark@example.com", "phone": "2025551014", "building": buildings[3]},
            {"first_name": "Amanda", "last_name": "Lewis", "email": "alewis@example.com", "phone": "2025551015", "building": buildings[4]},
        ]

        now = timezone.now()

        for i, data in enumerate(visitor_data):
            visitor = Visitor.objects.create(**data)
            if i % 3 == 0:
                visitor.check_out = now
                visitor.save()
                # print(f'Created visitor: {visitor.first_name} {visitor.last_name}')
                self.stdout.write(self.style.SUCCESS(f'Created visitor: {visitor.first_name} {visitor.last_name} - Check-out: {visitor.check_out}'))
            else:
                # print(f'Created visitor: {visitor.first_name} {visitor.last_name}')
                self.stdout.write(self.style.SUCCESS(f'Created visitor: {visitor.first_name} {visitor.last_name} - Still checked in'))
            
