from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    QuoteViewSet, PatientViewSet, PassengerViewSet,
    CrewLineViewSet, TripViewSet, TripLineViewSet, TripEventViewSet
)

# Create router and register viewsets
router = DefaultRouter()
router.register(r'quotes', QuoteViewSet)
router.register(r'patients', PatientViewSet)
router.register(r'passengers', PassengerViewSet)
router.register(r'crew-lines', CrewLineViewSet)
router.register(r'trips', TripViewSet)
router.register(r'trip-lines', TripLineViewSet)
router.register(r'trip-events', TripEventViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
