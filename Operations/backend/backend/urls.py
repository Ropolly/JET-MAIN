"""
URL configuration for backend project - Modular Architecture
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

# Swagger documentation setup
schema_view = get_schema_view(
   openapi.Info(
      title="JET ICU Operations API",
      default_version='v1',
      description="API for JET ICU Operations management system",
      contact=openapi.Contact(email="support@jeticu.com"),
      license=openapi.License(name="Proprietary"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Modular API routes organized by domain
    path('api/users/', include('users.urls')),
    path('api/contacts/', include('contacts.urls')),
    path('api/airports/', include('airports.urls')),
    path('api/aircraft/', include('aircraft.urls')),
    path('api/operations/', include('operations.urls')),
    path('api/documents/', include('documents.urls')),
    path('api/finance/', include('finance.urls')),
    
    # JWT Authentication
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    
    # API Documentation
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
