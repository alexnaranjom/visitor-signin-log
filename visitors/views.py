from rest_framework import viewsets
from .models import Visitor, Building
from .serializers import VisitorSerializer, BuildingSerializer

class VisitorViewSet(viewsets.ModelViewSet):
    queryset = Visitor.objects.all()
    serializer_class = VisitorSerializer

class BuildingViewSet(viewsets.ModelViewSet):
    queryset = Building.objects.all()
    serializer_class = BuildingSerializer

# Create your views here.
