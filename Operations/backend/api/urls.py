from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'permissions', views.PermissionViewSet)
router.register(r'roles', views.RoleViewSet)
router.register(r'departments', views.DepartmentViewSet)
router.register(r'users', views.UserProfileViewSet)
router.register(r'contacts', views.ContactViewSet)
router.register(r'fbos', views.FBOViewSet)
router.register(r'grounds', views.GroundViewSet)
router.register(r'airports', views.AirportViewSet)
router.register(r'documents', views.DocumentViewSet)
router.register(r'aircraft', views.AircraftViewSet)
router.register(r'transactions', views.TransactionViewSet)
router.register(r'agreements', views.AgreementViewSet)
router.register(r'patients', views.PatientViewSet)
router.register(r'quotes', views.QuoteViewSet)
router.register(r'passengers', views.PassengerViewSet)
router.register(r'crew-lines', views.CrewLineViewSet)
router.register(r'trips', views.TripViewSet)
router.register(r'trip-lines', views.TripLineViewSet)
router.register(r'modifications', views.ModificationViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('airport/fuel-prices/<str:airport_code>/', views.get_fuel_prices, name='fuel-prices'),
]
