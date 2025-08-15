from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import IndexPageViewSet

router = DefaultRouter()
router.register(r'pages', IndexPageViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
