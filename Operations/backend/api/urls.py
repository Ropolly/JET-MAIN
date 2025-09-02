from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from . import document_views

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
router.register(r"staff", views.StaffViewSet, basename="staff")
router.register(r"staff-roles", views.StaffRoleViewSet, basename="staff-role")
router.register(r"staff-role-memberships", views.StaffRoleMembershipViewSet, basename="staff-role-membership")
router.register(r"trip-events", views.TripEventViewSet, basename="trip-event")
router.register(r'comments', views.CommentViewSet, basename='comment')

urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('airport/fuel-prices/<str:airport_code>/', views.get_fuel_prices, name='fuel-prices'),
    path('dashboard/stats/', views.dashboard_stats, name='dashboard-stats'),
    path('contacts/create-with-related/', views.create_contact_with_related, name='create-contact-with-related'),
    # Timezone utility endpoints
    path('airports/<uuid:airport_id>/timezone-info/', views.get_airport_timezone_info, name='airport-timezone-info'),
    path('timezone/convert/', views.convert_timezone, name='timezone-convert'),
    path('timezone/validate-flight-times/', views.validate_flight_times, name='validate-flight-times'),
    
    # Document generation endpoints
    path('documents/gendec/<uuid:trip_line_id>/', document_views.generate_gendec, name='generate-gendec'),
    path('documents/handling-request/<uuid:trip_line_id>/', document_views.generate_handling_request, name='generate-handling-request'),
    path('documents/trip/<uuid:trip_id>/', document_views.generate_trip_documents, name='generate-trip-documents'),
    path('documents/info/', document_views.document_info, name='document-info'),
]
