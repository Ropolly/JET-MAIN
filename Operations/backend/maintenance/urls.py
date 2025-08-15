from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AircraftViewSet, MaintenanceLogViewSet

router = DefaultRouter()
router.register(r'aircraft', AircraftViewSet)
router.register(r'logs', MaintenanceLogViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
