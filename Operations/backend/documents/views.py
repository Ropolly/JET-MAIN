from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from common.permissions import IsOwnerOrReadOnly, HasRolePermission
from .models import Document, Agreement, DocumentTemplate, GeneratedDocument, DocumentAccess
from .serializers import (
    DocumentSerializer, DocumentUploadSerializer, AgreementSerializer,
    AgreementSignatureSerializer, DocumentTemplateSerializer,
    GenerateDocumentSerializer, GeneratedDocumentSerializer, DocumentAccessSerializer
)
from .services.document_service import DocumentService, AgreementService, DocumentTemplateService
import logging

logger = logging.getLogger(__name__)


class DocumentViewSet(viewsets.ModelViewSet):
    """ViewSet for Document operations."""
    queryset = Document.objects.filter(flag=0)  # Exclude deleted documents
    serializer_class = DocumentSerializer
    permission_classes = [permissions.IsAuthenticated, HasRolePermission]
    
    def get_queryset(self):
        """Filter documents based on user permissions."""
        queryset = super().get_queryset()
        
        # Filter by category if specified
        category = self.request.query_params.get('category')
        if category:
            queryset = queryset.filter(document_category=category)
        
        # Filter by uploaded user if specified
        uploaded_by = self.request.query_params.get('uploaded_by')
        if uploaded_by:
            queryset = queryset.filter(uploaded_by_id=uploaded_by)
        
        return queryset.order_by('-created_on')
    
    @action(detail=False, methods=['post'])
    def upload(self, request):
        """Upload a new document."""
        serializer = DocumentUploadSerializer(data=request.data)
        if serializer.is_valid():
            try:
                uploaded_file = serializer.validated_data['file']
                category = serializer.validated_data['document_category']
                
                # Create document using service
                document = DocumentService.create_document(
                    filename=uploaded_file.name,
                    content=uploaded_file.read(),
                    content_type=uploaded_file.content_type,
                    uploaded_by=request.user,
                    document_category=category
                )
                
                # Return serialized document
                doc_serializer = DocumentSerializer(document)
                return Response(doc_serializer.data, status=status.HTTP_201_CREATED)
                
            except Exception as e:
                logger.error(f"Document upload failed: {str(e)}")
                return Response(
                    {'error': 'Document upload failed'},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['get'])
    def download(self, request, pk=None):
        """Download document content."""
        document = get_object_or_404(Document, pk=pk, flag=0)
        
        # Log document access
        DocumentService.log_document_access(
            document=document,
            user=request.user,
            access_type='download',
            ip_address=request.META.get('REMOTE_ADDR'),
            user_agent=request.META.get('HTTP_USER_AGENT')
        )
        
        # Return file content
        response = HttpResponse(
            document.content,
            content_type=document.content_type or 'application/octet-stream'
        )
        response['Content-Disposition'] = f'attachment; filename="{document.filename}"'
        return response
    
    @action(detail=True, methods=['get'])
    def view(self, request, pk=None):
        """View document content inline."""
        document = get_object_or_404(Document, pk=pk, flag=0)
        
        # Log document access
        DocumentService.log_document_access(
            document=document,
            user=request.user,
            access_type='view',
            ip_address=request.META.get('REMOTE_ADDR'),
            user_agent=request.META.get('HTTP_USER_AGENT')
        )
        
        # Return file content for inline viewing
        response = HttpResponse(
            document.content,
            content_type=document.content_type or 'application/octet-stream'
        )
        response['Content-Disposition'] = f'inline; filename="{document.filename}"'
        return response
    
    def destroy(self, request, *args, **kwargs):
        """Soft delete document."""
        document = self.get_object()
        success = DocumentService.delete_document(document.id, request.user)
        
        if success:
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(
                {'error': 'Document deletion failed'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class AgreementViewSet(viewsets.ModelViewSet):
    """ViewSet for Agreement operations."""
    queryset = Agreement.objects.all()
    serializer_class = AgreementSerializer
    permission_classes = [permissions.IsAuthenticated, HasRolePermission]
    
    def get_queryset(self):
        """Filter agreements based on query parameters."""
        queryset = super().get_queryset()
        
        # Filter by status
        status_filter = self.request.query_params.get('status')
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        
        # Filter by agreement type
        agreement_type = self.request.query_params.get('type')
        if agreement_type:
            queryset = queryset.filter(agreement_type=agreement_type)
        
        # Filter by destination email
        email = self.request.query_params.get('email')
        if email:
            queryset = queryset.filter(destination_email__icontains=email)
        
        return queryset.order_by('-created_on')
    
    @action(detail=True, methods=['post'])
    def send(self, request, pk=None):
        """Send agreement to recipient."""
        agreement = self.get_object()
        
        if agreement.status != 'created':
            return Response(
                {'error': 'Agreement can only be sent from created status'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        updated_agreement = AgreementService.send_agreement(agreement.id, request.user)
        if updated_agreement:
            serializer = self.get_serializer(updated_agreement)
            return Response(serializer.data)
        
        return Response(
            {'error': 'Failed to send agreement'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    
    @action(detail=True, methods=['post'])
    def sign(self, request, pk=None):
        """Sign an agreement."""
        agreement = self.get_object()
        serializer = AgreementSignatureSerializer(data=request.data)
        
        if serializer.is_valid():
            signed_agreement = AgreementService.sign_agreement(
                agreement_id=agreement.id,
                signature_ip=request.META.get('REMOTE_ADDR'),
                signature_user_agent=request.META.get('HTTP_USER_AGENT'),
                terms_accepted=serializer.validated_data['terms_accepted'],
                terms_version=serializer.validated_data.get('terms_version')
            )
            
            if signed_agreement:
                response_serializer = self.get_serializer(signed_agreement)
                return Response(response_serializer.data)
            else:
                return Response(
                    {'error': 'Agreement cannot be signed'},
                    status=status.HTTP_400_BAD_REQUEST
                )
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['get'])
    def expiring(self, request):
        """Get agreements expiring soon."""
        days_ahead = int(request.query_params.get('days', 7))
        expiring_agreements = AgreementService.get_expiring_agreements(days_ahead)
        
        serializer = self.get_serializer(expiring_agreements, many=True)
        return Response(serializer.data)


class DocumentTemplateViewSet(viewsets.ModelViewSet):
    """ViewSet for DocumentTemplate operations."""
    queryset = DocumentTemplate.objects.filter(is_active=True)
    serializer_class = DocumentTemplateSerializer
    permission_classes = [permissions.IsAuthenticated, HasRolePermission]
    
    def get_queryset(self):
        """Filter templates based on query parameters."""
        queryset = super().get_queryset()
        
        # Filter by template type
        template_type = self.request.query_params.get('type')
        if template_type:
            queryset = queryset.filter(template_type=template_type)
        
        return queryset.order_by('name')
    
    @action(detail=True, methods=['post'])
    def generate(self, request, pk=None):
        """Generate document from template."""
        template = self.get_object()
        serializer = GenerateDocumentSerializer(data=request.data)
        
        if serializer.is_valid():
            try:
                document, generated_doc = DocumentTemplateService.generate_document_from_template(
                    template_id=template.id,
                    variables=serializer.validated_data['variables'],
                    filename=serializer.validated_data.get('filename'),
                    related_quote_id=serializer.validated_data.get('related_quote_id'),
                    related_trip_id=serializer.validated_data.get('related_trip_id'),
                    related_agreement_id=serializer.validated_data.get('related_agreement_id')
                )
                
                if document and generated_doc:
                    doc_serializer = DocumentSerializer(document)
                    return Response(doc_serializer.data, status=status.HTTP_201_CREATED)
                else:
                    return Response(
                        {'error': 'Document generation failed'},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR
                    )
                    
            except ValueError as e:
                return Response(
                    {'error': str(e)},
                    status=status.HTTP_400_BAD_REQUEST
                )
            except Exception as e:
                logger.error(f"Document generation failed: {str(e)}")
                return Response(
                    {'error': 'Document generation failed'},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['get'])
    def by_type(self, request):
        """Get templates by type."""
        template_type = request.query_params.get('type')
        if not template_type:
            return Response(
                {'error': 'Template type parameter is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        templates = DocumentTemplateService.get_active_templates(template_type)
        serializer = self.get_serializer(templates, many=True)
        return Response(serializer.data)


class GeneratedDocumentViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for GeneratedDocument operations (read-only)."""
    queryset = GeneratedDocument.objects.all()
    serializer_class = GeneratedDocumentSerializer
    permission_classes = [permissions.IsAuthenticated, HasRolePermission]
    
    def get_queryset(self):
        """Filter generated documents based on query parameters."""
        queryset = super().get_queryset()
        
        # Filter by template
        template_id = self.request.query_params.get('template')
        if template_id:
            queryset = queryset.filter(template_id=template_id)
        
        # Filter by related entities
        quote_id = self.request.query_params.get('quote_id')
        if quote_id:
            queryset = queryset.filter(related_quote_id=quote_id)
        
        trip_id = self.request.query_params.get('trip_id')
        if trip_id:
            queryset = queryset.filter(related_trip_id=trip_id)
        
        return queryset.order_by('-generation_date')


class DocumentAccessViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for DocumentAccess operations (read-only)."""
    queryset = DocumentAccess.objects.all()
    serializer_class = DocumentAccessSerializer
    permission_classes = [permissions.IsAuthenticated, HasRolePermission]
    
    def get_queryset(self):
        """Filter document access logs based on query parameters."""
        queryset = super().get_queryset()
        
        # Filter by document
        document_id = self.request.query_params.get('document')
        if document_id:
            queryset = queryset.filter(document_id=document_id)
        
        # Filter by user
        user_id = self.request.query_params.get('user')
        if user_id:
            queryset = queryset.filter(accessed_by_id=user_id)
        
        # Filter by access type
        access_type = self.request.query_params.get('access_type')
        if access_type:
            queryset = queryset.filter(access_type=access_type)
        
        return queryset.order_by('-access_date')
