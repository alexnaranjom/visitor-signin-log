from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import VisitorViewSet, BuildingViewSet

router = DefaultRouter()
router.register(r'visitors', VisitorViewSet)
router.register(r'buildings', BuildingViewSet)

urlpatterns = [
    path('', include(router.urls)),
]