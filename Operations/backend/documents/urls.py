from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    DocumentViewSet, AgreementViewSet, DocumentTemplateViewSet,
    GeneratedDocumentViewSet, DocumentAccessViewSet
)

router = DefaultRouter()
router.register(r'documents', DocumentViewSet)
router.register(r'agreements', AgreementViewSet)
router.register(r'templates', DocumentTemplateViewSet)
router.register(r'generated', GeneratedDocumentViewSet)
router.register(r'access-logs', DocumentAccessViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
