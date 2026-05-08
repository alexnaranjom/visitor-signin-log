from django.db import models

# Create your models here.
class Building(models.Model):
    """Represents the building a visitor can go to"""
    name = models.CharField(max_length=200)
    address = models.CharField(max_length=300, blank=True, default='')
    building_code = models.CharField(max_length=20, unique=True)
    phone = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.name} ({self.building_code})"

class Visitor(models.Model):
    """Represents a visitor to the building"""
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=10)
    # Cascade delete visitors if the building is deletedx   
    building = models.ForeignKey(Building, on_delete=models.CASCADE)
    visit_date = models.DateTimeField(auto_now_add=True)
    check_in = models.DateTimeField(auto_now_add=True)
    check_out = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} visiting {self.building.name}"