# Project Structure

The following is the structure of the project:

```
backend/
    prompt2.py
    manage.py
documents/
    models.py
    serializers.py
    views.py
    apps.py
    __init__.py
    tests.py
    urls.py
    admin.py
    services/
        __init__.py
        document_generation_service.py
        document_service.py
    tests/
        test_document_generation.py
        __init__.py
    migrations/
    templates/
        docuseal_pdf/
        docuseal_html/
        docs/
operations/
    models.py
    serializers.py
    pricing.py
    views.py
    apps.py
    __init__.py
    urls.py
    admin.py
    services/
        quote_service.py
        trip_service.py
        __init__.py
    tests/
        test_models.py
        test_api.py
        __init__.py
        test_services.py
    migrations/
index/
    models.py
    serializers.py
    views.py
    apps.py
    __init__.py
    urls.py
    admin.py
aircraft/
    models.py
    apps.py
    __init__.py
    admin.py
    services/
        aircraft_service.py
    tests/
        test_models.py
        test_api.py
        __init__.py
        test_services.py
    migrations/
airports/
    models.py
    apps.py
    __init__.py
    admin.py
    services/
        __init__.py
        weather_scraper.py
        airport_service.py
    tests/
        test_weather_scraper.py
        __init__.py
    migrations/
maintenance/
    models.py
    serializers.py
    views.py
    apps.py
    __init__.py
    urls.py
    admin.py
users/
    models.py
    apps.py
    __init__.py
    admin.py
    services/
        user_service.py
    tests/
        test_models.py
        __init__.py
    migrations/
common/
    middleware.py
    models.py
    permissions.py
    __init__.py
    utils.py
    timezone_utils.py
    services/
        scheduler_service.py
    tests/
        __init__.py
        test_scheduler_service.py
backend/
    asgi.py
    __init__.py
    urls.py
    wsgi.py
    settings.py
    documents/
finance/
    models.py
    serializers.py
    views.py
    apps.py
    __init__.py
    tests.py
    urls.py
    admin.py
    services/
        finance_service.py
        payment_processor.py
        __init__.py
    tests/
        test_payment_processor.py
    migrations/
contacts/
    models.py
    apps.py
    __init__.py
    admin.py
    services/
        contact_service.py
    tests/
        test_models.py
        test_api.py
        __init__.py
        test_services.py
    migrations/
```


# File: prompt2.py

```python
import os

def save_files_to_md(output_md_file='all_files_contents.md'):
    root_dir = os.path.dirname(os.path.abspath(__file__))  # Root set to the script's location

    def generate_structure():
        structure = []
        for dirpath, dirnames, filenames in os.walk(root_dir):
            # Skip 'venv', '__pycache__', or any hidden directories
            dirnames[:] = [d for d in dirnames if d not in ('venv', '__pycache__') and not d.startswith('.')]
            
            # Build the relative path and indentation for the directory
            rel_dir = os.path.relpath(dirpath, root_dir)
            indent = rel_dir.count(os.sep)
            structure.append('    ' * indent + f'{os.path.basename(dirpath)}/')
            
            for filename in filenames:
                if filename.endswith('.py'):
                    structure.append('    ' * (indent + 1) + filename)
        
        return '\n'.join(structure)

    with open(output_md_file, 'w') as md_file:
        # Write the project structure description at the top
        md_file.write("# Project Structure\n\n")
        md_file.write("The following is the structure of the project:\n\n")
        md_file.write("```\n")
        md_file.write(generate_structure())
        md_file.write("\n```\n")

        # Now iterate through the files to capture code content
        for dirpath, dirnames, filenames in os.walk(root_dir):
            # Skip 'venv', '__pycache__', or any hidden directories
            dirnames[:] = [d for d in dirnames if d not in ('venv', '__pycache__') and not d.startswith('.')]
            
            for filename in filenames:
                if filename.endswith('.py'):
                    file_path = os.path.join(dirpath, filename)
                    relative_path = os.path.relpath(file_path, root_dir)
                    
                    # Add file header with file path
                    md_file.write(f"\n\n# File: {relative_path}\n\n")
                    md_file.write("```python\n")
                    
                    # Write the file's contents
                    with open(file_path, 'r') as f:
                        md_file.write(f.read())
                    
                    md_file.write("\n```\n")

    print(f"All .py files and project structure have been copied to {output_md_file}")

if __name__ == "__main__":
    save_files_to_md()
```


# File: manage.py

```python
#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()

```


# File: documents/models.py

```python
from django.db import models
from common.models import BaseModel
import uuid


class Document(models.Model):
    """Document model for file storage and management."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    filename = models.CharField(max_length=255)
    content = models.BinaryField()
    content_type = models.CharField(max_length=100, blank=True, null=True)
    file_size = models.PositiveIntegerField(default=0)
    
    # Document metadata
    flag = models.IntegerField(default=0)
    created_on = models.DateTimeField(auto_now_add=True)
    uploaded_by = models.ForeignKey(
        'auth.User', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name="uploaded_documents"
    )
    
    # Document categorization
    document_category = models.CharField(max_length=50, choices=[
        ('quote', 'Quote Document'),
        ('agreement', 'Agreement'),
        ('passport', 'Passport'),
        ('medical', 'Medical Document'),
        ('itinerary', 'Itinerary'),
        ('certificate', 'Certificate'),
        ('other', 'Other')
    ], default='other')
    
    class Meta:
        indexes = [
            models.Index(fields=['filename']),
            models.Index(fields=['document_category']),
            models.Index(fields=['created_on']),
        ]
    
    def __str__(self):
        return self.filename
    
    @property
    def file_size_mb(self):
        """Return file size in megabytes."""
        return self.file_size / (1024 * 1024) if self.file_size else 0


class Agreement(BaseModel):
    """Agreement model for contracts and legal documents."""
    
    AGREEMENT_STATUS = [
        ('created', 'Created'),
        ('sent', 'Sent'),
        ('pending', 'Pending Signature'),
        ('modified', 'Modified'),
        ('signed', 'Signed'),
        ('denied', 'Denied'),
        ('expired', 'Expired'),
    ]
    
    AGREEMENT_TYPES = [
        ('payment', 'Payment Agreement'),
        ('consent', 'Consent for Transport'),
        ('service', 'Patient Service Agreement'),
        ('charter', 'Charter Agreement'),
        ('nda', 'Non-Disclosure Agreement'),
        ('other', 'Other Agreement'),
    ]
    
    # Agreement identification
    agreement_type = models.CharField(max_length=20, choices=AGREEMENT_TYPES)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    
    # Parties involved
    destination_email = models.EmailField()
    signatory_name = models.CharField(max_length=255, blank=True, null=True)
    signatory_title = models.CharField(max_length=100, blank=True, null=True)
    
    # Document references
    document_unsigned = models.ForeignKey(
        Document, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name="unsigned_agreements"
    )
    document_signed = models.ForeignKey(
        Document, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name="signed_agreements"
    )
    
    # Status and timing
    status = models.CharField(max_length=20, choices=AGREEMENT_STATUS, default='created')
    sent_date = models.DateTimeField(null=True, blank=True)
    signed_date = models.DateTimeField(null=True, blank=True)
    expiration_date = models.DateTimeField(null=True, blank=True)
    
    # Digital signature information
    signature_ip_address = models.GenericIPAddressField(null=True, blank=True)
    signature_user_agent = models.TextField(blank=True, null=True)
    
    # Terms and conditions
    terms_accepted = models.BooleanField(default=False)
    terms_version = models.CharField(max_length=20, blank=True, null=True)
    
    class Meta:
        indexes = [
            models.Index(fields=['status', 'created_on']),
            models.Index(fields=['agreement_type']),
            models.Index(fields=['destination_email']),
            models.Index(fields=['expiration_date']),
        ]
    
    def __str__(self):
        return f"{self.get_agreement_type_display()} for {self.destination_email} - {self.status}"
    
    @property
    def is_expired(self):
        """Check if agreement has expired."""
        if not self.expiration_date:
            return False
        
        from django.utils import timezone
        return timezone.now() > self.expiration_date
    
    @property
    def is_signed(self):
        """Check if agreement is signed."""
        return self.status == 'signed'
    
    @property
    def days_until_expiration(self):
        """Calculate days until expiration."""
        if not self.expiration_date:
            return None
        
        from django.utils import timezone
        delta = self.expiration_date - timezone.now()
        return delta.days


class DocumentTemplate(BaseModel):
    """Template model for generating standardized documents."""
    
    TEMPLATE_TYPES = [
        ('quote', 'Quote Template'),
        ('agreement', 'Agreement Template'),
        ('itinerary', 'Itinerary Template'),
        ('invoice', 'Invoice Template'),
        ('report', 'Report Template'),
    ]
    
    name = models.CharField(max_length=255)
    template_type = models.CharField(max_length=20, choices=TEMPLATE_TYPES)
    description = models.TextField(blank=True, null=True)
    
    # Template content
    template_content = models.TextField()  # HTML or other markup
    css_styles = models.TextField(blank=True, null=True)
    
    # Template variables and configuration
    required_variables = models.JSONField(default=list, blank=True)
    optional_variables = models.JSONField(default=list, blank=True)
    
    # Version control
    version = models.CharField(max_length=20, default='1.0')
    is_active = models.BooleanField(default=True)
    
    class Meta:
        indexes = [
            models.Index(fields=['template_type', 'is_active']),
            models.Index(fields=['name']),
        ]
    
    def __str__(self):
        return f"{self.name} (v{self.version})"


class GeneratedDocument(BaseModel):
    """Track documents generated from templates."""
    
    template = models.ForeignKey(
        DocumentTemplate, 
        on_delete=models.CASCADE, 
        related_name="generated_documents"
    )
    document = models.OneToOneField(
        Document, 
        on_delete=models.CASCADE, 
        related_name="generation_info"
    )
    
    # Generation context
    variables_used = models.JSONField(default=dict, blank=True)
    generation_date = models.DateTimeField(auto_now_add=True)
    
    # Related entities (generic foreign keys could be used here)
    related_quote_id = models.UUIDField(null=True, blank=True)
    related_trip_id = models.UUIDField(null=True, blank=True)
    related_agreement_id = models.UUIDField(null=True, blank=True)
    
    class Meta:
        indexes = [
            models.Index(fields=['template', 'generation_date']),
            models.Index(fields=['related_quote_id']),
            models.Index(fields=['related_trip_id']),
        ]
    
    def __str__(self):
        return f"Generated {self.template.name} - {self.generation_date.date()}"


class DocumentAccess(BaseModel):
    """Track document access and downloads."""
    
    document = models.ForeignKey(Document, on_delete=models.CASCADE, related_name="access_logs")
    accessed_by = models.ForeignKey(
        'auth.User', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name="document_accesses"
    )
    
    # Access details
    access_date = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True, null=True)
    
    # Access type
    access_type = models.CharField(max_length=20, choices=[
        ('view', 'View'),
        ('download', 'Download'),
        ('print', 'Print'),
        ('share', 'Share'),
    ], default='view')
    
    class Meta:
        indexes = [
            models.Index(fields=['document', 'access_date']),
            models.Index(fields=['accessed_by', 'access_date']),
        ]
    
    def __str__(self):
        return f"{self.document.filename} accessed by {self.accessed_by} on {self.access_date}"

```


# File: documents/serializers.py

```python
from rest_framework import serializers
from .models import Document, Agreement, DocumentTemplate, GeneratedDocument, DocumentAccess


class DocumentSerializer(serializers.ModelSerializer):
    """Serializer for Document model."""
    file_size_mb = serializers.ReadOnlyField()
    uploaded_by_name = serializers.CharField(source='uploaded_by.get_full_name', read_only=True)
    
    class Meta:
        model = Document
        fields = [
            'id', 'filename', 'content_type', 'file_size', 'file_size_mb',
            'flag', 'created_on', 'uploaded_by', 'uploaded_by_name',
            'document_category'
        ]
        read_only_fields = ['id', 'created_on', 'file_size', 'file_size_mb']
    
    def validate_filename(self, value):
        """Validate filename format."""
        if not value or len(value.strip()) == 0:
            raise serializers.ValidationError("Filename cannot be empty.")
        
        # Check for invalid characters
        invalid_chars = ['<', '>', ':', '"', '|', '?', '*']
        if any(char in value for char in invalid_chars):
            raise serializers.ValidationError("Filename contains invalid characters.")
        
        return value.strip()


class DocumentUploadSerializer(serializers.Serializer):
    """Serializer for document upload operations."""
    file = serializers.FileField()
    document_category = serializers.ChoiceField(
        choices=Document._meta.get_field('document_category').choices,
        default='other'
    )
    
    def validate_file(self, value):
        """Validate uploaded file."""
        # Check file size (50MB limit)
        max_size = 50 * 1024 * 1024  # 50MB
        if value.size > max_size:
            raise serializers.ValidationError("File size cannot exceed 50MB.")
        
        return value


class AgreementSerializer(serializers.ModelSerializer):
    """Serializer for Agreement model."""
    is_expired = serializers.ReadOnlyField()
    is_signed = serializers.ReadOnlyField()
    days_until_expiration = serializers.ReadOnlyField()
    agreement_type_display = serializers.CharField(source='get_agreement_type_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    
    class Meta:
        model = Agreement
        fields = [
            'id', 'agreement_type', 'agreement_type_display', 'title', 'description',
            'destination_email', 'signatory_name', 'signatory_title',
            'document_unsigned', 'document_signed', 'status', 'status_display',
            'sent_date', 'signed_date', 'expiration_date', 'signature_ip_address',
            'terms_accepted', 'terms_version', 'is_expired', 'is_signed',
            'days_until_expiration', 'created_on', 'updated_on'
        ]
        read_only_fields = [
            'id', 'sent_date', 'signed_date', 'signature_ip_address',
            'created_on', 'updated_on'
        ]
    
    def validate_destination_email(self, value):
        """Validate destination email format."""
        if not value:
            raise serializers.ValidationError("Destination email is required.")
        return value.lower().strip()
    
    def validate_expiration_date(self, value):
        """Validate expiration date is in the future."""
        if value:
            from django.utils import timezone
            if value <= timezone.now():
                raise serializers.ValidationError("Expiration date must be in the future.")
        return value


class AgreementSignatureSerializer(serializers.Serializer):
    """Serializer for agreement signature operations."""
    terms_accepted = serializers.BooleanField(default=True)
    terms_version = serializers.CharField(max_length=20, required=False)
    
    def validate_terms_accepted(self, value):
        """Ensure terms are accepted."""
        if not value:
            raise serializers.ValidationError("Terms must be accepted to sign the agreement.")
        return value


class DocumentTemplateSerializer(serializers.ModelSerializer):
    """Serializer for DocumentTemplate model."""
    template_type_display = serializers.CharField(source='get_template_type_display', read_only=True)
    
    class Meta:
        model = DocumentTemplate
        fields = [
            'id', 'name', 'template_type', 'template_type_display', 'description',
            'template_content', 'css_styles', 'required_variables', 'optional_variables',
            'version', 'is_active', 'created_on', 'updated_on'
        ]
        read_only_fields = ['id', 'created_on', 'updated_on']
    
    def validate_name(self, value):
        """Validate template name."""
        if not value or len(value.strip()) == 0:
            raise serializers.ValidationError("Template name cannot be empty.")
        return value.strip()
    
    def validate_template_content(self, value):
        """Validate template content."""
        if not value or len(value.strip()) == 0:
            raise serializers.ValidationError("Template content cannot be empty.")
        return value
    
    def validate_required_variables(self, value):
        """Validate required variables format."""
        if not isinstance(value, list):
            raise serializers.ValidationError("Required variables must be a list.")
        return value
    
    def validate_optional_variables(self, value):
        """Validate optional variables format."""
        if not isinstance(value, list):
            raise serializers.ValidationError("Optional variables must be a list.")
        return value


class GenerateDocumentSerializer(serializers.Serializer):
    """Serializer for document generation from templates."""
    template_id = serializers.UUIDField()
    variables = serializers.JSONField()
    filename = serializers.CharField(max_length=255, required=False)
    related_quote_id = serializers.UUIDField(required=False)
    related_trip_id = serializers.UUIDField(required=False)
    related_agreement_id = serializers.UUIDField(required=False)
    
    def validate_variables(self, value):
        """Validate variables format."""
        if not isinstance(value, dict):
            raise serializers.ValidationError("Variables must be a dictionary.")
        return value


class GeneratedDocumentSerializer(serializers.ModelSerializer):
    """Serializer for GeneratedDocument model."""
    template_name = serializers.CharField(source='template.name', read_only=True)
    document_filename = serializers.CharField(source='document.filename', read_only=True)
    
    class Meta:
        model = GeneratedDocument
        fields = [
            'id', 'template', 'template_name', 'document', 'document_filename',
            'variables_used', 'generation_date', 'related_quote_id',
            'related_trip_id', 'related_agreement_id', 'created_on'
        ]
        read_only_fields = ['id', 'generation_date', 'created_on']


class DocumentAccessSerializer(serializers.ModelSerializer):
    """Serializer for DocumentAccess model."""
    document_filename = serializers.CharField(source='document.filename', read_only=True)
    accessed_by_name = serializers.CharField(source='accessed_by.get_full_name', read_only=True)
    access_type_display = serializers.CharField(source='get_access_type_display', read_only=True)
    
    class Meta:
        model = DocumentAccess
        fields = [
            'id', 'document', 'document_filename', 'accessed_by', 'accessed_by_name',
            'access_date', 'ip_address', 'access_type', 'access_type_display'
        ]
        read_only_fields = ['id', 'access_date']

```


# File: documents/views.py

```python
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

```


# File: documents/apps.py

```python
from django.apps import AppConfig


class DocumentsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'documents'
    verbose_name = 'Document Management'

```


# File: documents/__init__.py

```python

```


# File: documents/tests.py

```python
from django.test import TestCase
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.files.base import ContentFile
from .models import Document, Agreement, DocumentTemplate, GeneratedDocument, DocumentAccess
from .services.document_service import DocumentService, AgreementService, DocumentTemplateService
import uuid


class DocumentModelTest(TestCase):
    """Test cases for Document model."""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
    
    def test_document_creation(self):
        """Test document creation with basic fields."""
        document = Document.objects.create(
            filename='test.pdf',
            content=b'test content',
            content_type='application/pdf',
            file_size=1024,
            uploaded_by=self.user,
            document_category='quote'
        )
        
        self.assertEqual(document.filename, 'test.pdf')
        self.assertEqual(document.content_type, 'application/pdf')
        self.assertEqual(document.file_size, 1024)
        self.assertEqual(document.uploaded_by, self.user)
        self.assertEqual(document.document_category, 'quote')
        self.assertIsNotNone(document.id)
        self.assertIsNotNone(document.created_on)
    
    def test_file_size_mb_property(self):
        """Test file size in MB calculation."""
        document = Document.objects.create(
            filename='large.pdf',
            content=b'x' * (2 * 1024 * 1024),  # 2MB
            file_size=2 * 1024 * 1024,
            uploaded_by=self.user
        )
        
        self.assertEqual(document.file_size_mb, 2.0)


class AgreementModelTest(TestCase):
    """Test cases for Agreement model."""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
    
    def test_agreement_creation(self):
        """Test agreement creation with required fields."""
        future_date = timezone.now() + timezone.timedelta(days=30)
        
        agreement = Agreement.objects.create(
            agreement_type='payment',
            title='Payment Agreement',
            destination_email='client@example.com',
            signatory_name='John Doe',
            expiration_date=future_date
        )
        
        self.assertEqual(agreement.agreement_type, 'payment')
        self.assertEqual(agreement.title, 'Payment Agreement')
        self.assertEqual(agreement.destination_email, 'client@example.com')
        self.assertEqual(agreement.status, 'created')
        self.assertFalse(agreement.is_expired)
        self.assertFalse(agreement.is_signed)
    
    def test_agreement_expiration(self):
        """Test agreement expiration logic."""
        past_date = timezone.now() - timezone.timedelta(days=1)
        
        agreement = Agreement.objects.create(
            agreement_type='consent',
            title='Expired Agreement',
            destination_email='client@example.com',
            expiration_date=past_date
        )
        
        self.assertTrue(agreement.is_expired)
        self.assertLess(agreement.days_until_expiration, 0)
    
    def test_agreement_signing(self):
        """Test agreement signing process."""
        agreement = Agreement.objects.create(
            agreement_type='service',
            title='Service Agreement',
            destination_email='client@example.com',
            status='sent'
        )
        
        # Sign the agreement
        agreement.status = 'signed'
        agreement.signed_date = timezone.now()
        agreement.terms_accepted = True
        agreement.save()
        
        self.assertTrue(agreement.is_signed)
        self.assertIsNotNone(agreement.signed_date)
        self.assertTrue(agreement.terms_accepted)


class DocumentServiceTest(TestCase):
    """Test cases for DocumentService."""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
    
    def test_create_document(self):
        """Test document creation via service."""
        content = b'Test document content'
        
        document = DocumentService.create_document(
            filename='service_test.txt',
            content=content,
            content_type='text/plain',
            uploaded_by=self.user,
            document_category='other'
        )
        
        self.assertIsNotNone(document)
        self.assertEqual(document.filename, 'service_test.txt')
        self.assertEqual(document.content, content)
        self.assertEqual(document.uploaded_by, self.user)
        self.assertEqual(document.file_size, len(content))
    
    def test_get_document_content(self):
        """Test document content retrieval."""
        content = b'Retrievable content'
        document = DocumentService.create_document(
            filename='retrieve_test.txt',
            content=content,
            uploaded_by=self.user
        )
        
        retrieved_content = DocumentService.get_document_content(document.id)
        self.assertEqual(retrieved_content, content)
    
    def test_delete_document(self):
        """Test document soft deletion."""
        document = DocumentService.create_document(
            filename='delete_test.txt',
            content=b'To be deleted',
            uploaded_by=self.user
        )
        
        success = DocumentService.delete_document(document.id, self.user)
        self.assertTrue(success)
        
        # Refresh from database
        document.refresh_from_db()
        self.assertEqual(document.flag, 1)  # Marked as deleted


class AgreementServiceTest(TestCase):
    """Test cases for AgreementService."""
    
    def test_create_agreement(self):
        """Test agreement creation via service."""
        agreement = AgreementService.create_agreement(
            agreement_type='payment',
            title='Service Test Agreement',
            destination_email='service@example.com',
            description='Test agreement created via service',
            expiration_days=30
        )
        
        self.assertIsNotNone(agreement)
        self.assertEqual(agreement.agreement_type, 'payment')
        self.assertEqual(agreement.title, 'Service Test Agreement')
        self.assertEqual(agreement.destination_email, 'service@example.com')
        self.assertEqual(agreement.status, 'created')
        self.assertIsNotNone(agreement.expiration_date)
    
    def test_send_agreement(self):
        """Test agreement sending via service."""
        agreement = AgreementService.create_agreement(
            agreement_type='consent',
            title='Send Test Agreement',
            destination_email='send@example.com'
        )
        
        sent_agreement = AgreementService.send_agreement(agreement.id)
        
        self.assertIsNotNone(sent_agreement)
        self.assertEqual(sent_agreement.status, 'sent')
        self.assertIsNotNone(sent_agreement.sent_date)
    
    def test_sign_agreement(self):
        """Test agreement signing via service."""
        agreement = AgreementService.create_agreement(
            agreement_type='service',
            title='Sign Test Agreement',
            destination_email='sign@example.com'
        )
        
        # Send first
        AgreementService.send_agreement(agreement.id)
        
        # Then sign
        signed_agreement = AgreementService.sign_agreement(
            agreement_id=agreement.id,
            signature_ip='192.168.1.1',
            signature_user_agent='Test Browser',
            terms_accepted=True,
            terms_version='1.0'
        )
        
        self.assertIsNotNone(signed_agreement)
        self.assertEqual(signed_agreement.status, 'signed')
        self.assertIsNotNone(signed_agreement.signed_date)
        self.assertEqual(signed_agreement.signature_ip_address, '192.168.1.1')
        self.assertTrue(signed_agreement.terms_accepted)


class DocumentTemplateTest(TestCase):
    """Test cases for DocumentTemplate model and service."""
    
    def test_template_creation(self):
        """Test document template creation."""
        template = DocumentTemplate.objects.create(
            name='Test Template',
            template_type='quote',
            description='A test template',
            template_content='<h1>{{title}}</h1><p>{{content}}</p>',
            required_variables=['title', 'content'],
            optional_variables=['footer']
        )
        
        self.assertEqual(template.name, 'Test Template')
        self.assertEqual(template.template_type, 'quote')
        self.assertTrue(template.is_active)
        self.assertEqual(template.version, '1.0')
    
    def test_document_generation_from_template(self):
        """Test document generation from template."""
        template = DocumentTemplateService.create_template(
            name='Generation Test Template',
            template_type='quote',
            template_content='<h1>{{title}}</h1><p>Amount: ${{amount}}</p>',
            required_variables=['title', 'amount']
        )
        
        variables = {
            'title': 'Test Quote',
            'amount': '1000.00'
        }
        
        document, generated_doc = DocumentTemplateService.generate_document_from_template(
            template_id=template.id,
            variables=variables,
            filename='generated_quote.html'
        )
        
        self.assertIsNotNone(document)
        self.assertIsNotNone(generated_doc)
        self.assertEqual(document.filename, 'generated_quote.html')
        self.assertEqual(generated_doc.template, template)
        self.assertEqual(generated_doc.variables_used, variables)
    
    def test_missing_required_variables(self):
        """Test error handling for missing required variables."""
        template = DocumentTemplateService.create_template(
            name='Required Vars Template',
            template_type='agreement',
            template_content='<h1>{{title}}</h1><p>{{required_field}}</p>',
            required_variables=['title', 'required_field']
        )
        
        variables = {'title': 'Test'}  # Missing required_field
        
        with self.assertRaises(ValueError):
            DocumentTemplateService.generate_document_from_template(
                template_id=template.id,
                variables=variables
            )


class DocumentAccessTest(TestCase):
    """Test cases for DocumentAccess model."""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
        self.document = Document.objects.create(
            filename='access_test.pdf',
            content=b'test content',
            uploaded_by=self.user
        )
    
    def test_document_access_logging(self):
        """Test document access logging."""
        DocumentService.log_document_access(
            document=self.document,
            user=self.user,
            access_type='view',
            ip_address='192.168.1.1',
            user_agent='Test Browser'
        )
        
        access_log = DocumentAccess.objects.filter(document=self.document).first()
        
        self.assertIsNotNone(access_log)
        self.assertEqual(access_log.document, self.document)
        self.assertEqual(access_log.accessed_by, self.user)
        self.assertEqual(access_log.access_type, 'view')
        self.assertEqual(access_log.ip_address, '192.168.1.1')
        self.assertIsNotNone(access_log.access_date)

```


# File: documents/urls.py

```python
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

```


# File: documents/admin.py

```python
from django.contrib import admin
from .models import Document, Agreement, DocumentTemplate, GeneratedDocument, DocumentAccess


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    """Admin configuration for Document model."""
    list_display = ['filename', 'document_category', 'file_size_mb', 'uploaded_by', 'created_on', 'flag']
    list_filter = ['document_category', 'created_on', 'flag', 'uploaded_by']
    search_fields = ['filename', 'uploaded_by__username', 'uploaded_by__email']
    readonly_fields = ['id', 'file_size', 'created_on']
    
    fieldsets = (
        ('Document Information', {
            'fields': ('filename', 'document_category', 'content_type', 'file_size')
        }),
        ('Upload Information', {
            'fields': ('uploaded_by', 'created_on', 'flag')
        }),
        ('Content', {
            'fields': ('content',),
            'classes': ('collapse',)
        }),
    )
    
    def file_size_mb(self, obj):
        """Display file size in MB."""
        return f"{obj.file_size_mb:.2f} MB" if obj.file_size else "0 MB"
    file_size_mb.short_description = 'File Size'
    
    def get_queryset(self, request):
        """Include deleted documents for admin."""
        return Document.objects.all()


@admin.register(Agreement)
class AgreementAdmin(admin.ModelAdmin):
    """Admin configuration for Agreement model."""
    list_display = [
        'title', 'agreement_type', 'destination_email', 'status', 
        'sent_date', 'signed_date', 'is_expired', 'created_on'
    ]
    list_filter = [
        'agreement_type', 'status', 'created_on', 'sent_date', 
        'signed_date', 'terms_accepted'
    ]
    search_fields = [
        'title', 'destination_email', 'signatory_name', 'description'
    ]
    readonly_fields = [
        'id', 'sent_date', 'signed_date', 'signature_ip_address', 
        'created_on', 'updated_on', 'is_expired', 'days_until_expiration'
    ]
    
    fieldsets = (
        ('Agreement Details', {
            'fields': (
                'agreement_type', 'title', 'description', 'status'
            )
        }),
        ('Parties', {
            'fields': (
                'destination_email', 'signatory_name', 'signatory_title'
            )
        }),
        ('Documents', {
            'fields': ('document_unsigned', 'document_signed')
        }),
        ('Dates and Expiration', {
            'fields': (
                'sent_date', 'signed_date', 'expiration_date', 
                'is_expired', 'days_until_expiration'
            )
        }),
        ('Signature Information', {
            'fields': (
                'signature_ip_address', 'signature_user_agent', 
                'terms_accepted', 'terms_version'
            ),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_on', 'updated_on'),
            'classes': ('collapse',)
        }),
    )
    
    def is_expired(self, obj):
        """Display expiration status."""
        return obj.is_expired
    is_expired.boolean = True
    is_expired.short_description = 'Expired'


@admin.register(DocumentTemplate)
class DocumentTemplateAdmin(admin.ModelAdmin):
    """Admin configuration for DocumentTemplate model."""
    list_display = ['name', 'template_type', 'version', 'is_active', 'created_on']
    list_filter = ['template_type', 'is_active', 'created_on']
    search_fields = ['name', 'description']
    readonly_fields = ['id', 'created_on', 'updated_on']
    
    fieldsets = (
        ('Template Information', {
            'fields': ('name', 'template_type', 'description', 'version', 'is_active')
        }),
        ('Template Content', {
            'fields': ('template_content', 'css_styles')
        }),
        ('Variables', {
            'fields': ('required_variables', 'optional_variables'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_on', 'updated_on'),
            'classes': ('collapse',)
        }),
    )


@admin.register(GeneratedDocument)
class GeneratedDocumentAdmin(admin.ModelAdmin):
    """Admin configuration for GeneratedDocument model."""
    list_display = [
        'document', 'template', 'generation_date', 
        'related_quote_id', 'related_trip_id', 'related_agreement_id'
    ]
    list_filter = ['template', 'generation_date']
    search_fields = ['document__filename', 'template__name']
    readonly_fields = [
        'id', 'generation_date', 'created_on', 'updated_on'
    ]
    
    fieldsets = (
        ('Generation Information', {
            'fields': ('template', 'document', 'generation_date')
        }),
        ('Related Entities', {
            'fields': (
                'related_quote_id', 'related_trip_id', 'related_agreement_id'
            )
        }),
        ('Variables Used', {
            'fields': ('variables_used',),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_on', 'updated_on'),
            'classes': ('collapse',)
        }),
    )


@admin.register(DocumentAccess)
class DocumentAccessAdmin(admin.ModelAdmin):
    """Admin configuration for DocumentAccess model."""
    list_display = [
        'document', 'accessed_by', 'access_type', 'access_date', 'ip_address'
    ]
    list_filter = ['access_type', 'access_date', 'accessed_by']
    search_fields = [
        'document__filename', 'accessed_by__username', 
        'accessed_by__email', 'ip_address'
    ]
    readonly_fields = [
        'id', 'access_date', 'created_on', 'updated_on'
    ]
    
    fieldsets = (
        ('Access Information', {
            'fields': ('document', 'accessed_by', 'access_type', 'access_date')
        }),
        ('Technical Details', {
            'fields': ('ip_address', 'user_agent'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_on', 'updated_on'),
            'classes': ('collapse',)
        }),
    )
    
    def has_add_permission(self, request):
        """Disable manual creation of access logs."""
        return False
    
    def has_change_permission(self, request, obj=None):
        """Make access logs read-only."""
        return False

```


# File: documents/services/__init__.py

```python

```


# File: documents/services/document_generation_service.py

```python
#!/usr/bin/env python
"""
Document Generation Service for JET Aviation Operations

Moved from utils/docgen/docgen.py to documents/services/document_generation_service.py
This service handles the generation of aviation-related documents including:
- General Declaration (GenDec)
- Handling Requests
- Customer Itineraries
- Internal Itineraries
- Quote Forms
"""

import os
from pathlib import Path
from datetime import datetime, timedelta
from typing import Optional, Dict, Any, List
from django.utils import timezone
from django.conf import settings
from operations.models import TripLine, Trip
from aircraft.models import Aircraft
from contacts.models import Contact
from operations.models import Passenger, Patient
from ..models import Document, DocumentTemplate
import logging

logger = logging.getLogger(__name__)

try:
    from docx import Document as DocxDocument
    from docx.shared import Inches
    DOCX_AVAILABLE = True
except ImportError:
    logger.warning("python-docx not installed. Install with: pip install python-docx")
    DocxDocument = None
    DOCX_AVAILABLE = False


class DocumentGenerationService:
    """Main document generation service for aviation documents."""
    
    def __init__(self):
        """Initialize the document generator with template and output paths."""
        self.base_dir = Path(__file__).parent.parent
        self.templates_dir = self.base_dir / "templates"
        self.outputs_dir = settings.MEDIA_ROOT / "generated_documents"
        
        # Ensure outputs directory exists
        self.outputs_dir.mkdir(parents=True, exist_ok=True)
        
        # Check if templates directory exists
        if not self.templates_dir.exists():
            self.templates_dir.mkdir(parents=True, exist_ok=True)
            logger.warning(f"Created templates directory: {self.templates_dir}")
    
    def generate_general_declaration(self, trip_id: str, output_filename: Optional[str] = None) -> Optional[Document]:
        """
        Generate a General Declaration (GenDec) document for a trip.
        
        Args:
            trip_id: UUID of the trip
            output_filename: Optional custom filename
            
        Returns:
            Document instance if successful, None otherwise
        """
        try:
            trip = Trip.objects.get(id=trip_id)
            
            if not DOCX_AVAILABLE:
                logger.error("python-docx not available for document generation")
                return None
            
            # Create new document
            doc = DocxDocument()
            
            # Add title
            title = doc.add_heading('GENERAL DECLARATION', 0)
            title.alignment = 1  # Center alignment
            
            # Add trip information
            doc.add_heading('Flight Information', level=1)
            
            # Basic trip details
            trip_table = doc.add_table(rows=0, cols=2)
            trip_table.style = 'Table Grid'
            
            self._add_table_row(trip_table, 'Trip Number:', trip.trip_number)
            self._add_table_row(trip_table, 'Trip Type:', trip.get_type_display())
            self._add_table_row(trip_table, 'Aircraft:', str(trip.aircraft) if trip.aircraft else 'TBD')
            
            if trip.estimated_departure_time:
                self._add_table_row(trip_table, 'Departure Time:', 
                                  trip.estimated_departure_time.strftime('%Y-%m-%d %H:%M UTC'))
            
            # Add trip lines (flight legs)
            if trip.trip_lines.exists():
                doc.add_heading('Flight Legs', level=1)
                
                legs_table = doc.add_table(rows=1, cols=5)
                legs_table.style = 'Table Grid'
                
                # Header row
                header_cells = legs_table.rows[0].cells
                header_cells[0].text = 'Origin'
                header_cells[1].text = 'Destination'
                header_cells[2].text = 'Departure'
                header_cells[3].text = 'Arrival'
                header_cells[4].text = 'Distance'
                
                for trip_line in trip.trip_lines.all():
                    row_cells = legs_table.add_row().cells
                    row_cells[0].text = str(trip_line.origin_airport)
                    row_cells[1].text = str(trip_line.destination_airport)
                    row_cells[2].text = trip_line.departure_time_local.strftime('%Y-%m-%d %H:%M')
                    row_cells[3].text = trip_line.arrival_time_local.strftime('%Y-%m-%d %H:%M')
                    row_cells[4].text = f"{trip_line.distance} nm"
            
            # Add passengers if any
            if trip.passengers.exists():
                doc.add_heading('Passengers', level=1)
                
                pax_table = doc.add_table(rows=1, cols=4)
                pax_table.style = 'Table Grid'
                
                # Header row
                header_cells = pax_table.rows[0].cells
                header_cells[0].text = 'Name'
                header_cells[1].text = 'Nationality'
                header_cells[2].text = 'Passport'
                header_cells[3].text = 'Date of Birth'
                
                for passenger in trip.passengers.all():
                    row_cells = pax_table.add_row().cells
                    row_cells[0].text = str(passenger.info)
                    row_cells[1].text = passenger.nationality or 'N/A'
                    row_cells[2].text = passenger.passport_number or 'N/A'
                    row_cells[3].text = passenger.date_of_birth.strftime('%Y-%m-%d') if passenger.date_of_birth else 'N/A'
            
            # Add patient information if medical trip
            if trip.patient:
                doc.add_heading('Patient Information', level=1)
                
                patient_table = doc.add_table(rows=0, cols=2)
                patient_table.style = 'Table Grid'
                
                self._add_table_row(patient_table, 'Patient Name:', str(trip.patient.info))
                self._add_table_row(patient_table, 'Date of Birth:', 
                                  trip.patient.date_of_birth.strftime('%Y-%m-%d'))
                self._add_table_row(patient_table, 'Nationality:', trip.patient.nationality)
                self._add_table_row(patient_table, 'Passport:', trip.patient.passport_number)
                
                if trip.patient.special_instructions:
                    doc.add_heading('Special Instructions', level=2)
                    doc.add_paragraph(trip.patient.special_instructions)
            
            # Save document
            if not output_filename:
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                output_filename = f"GenDec_{trip.trip_number}_{timestamp}.docx"
            
            output_path = self.outputs_dir / output_filename
            doc.save(str(output_path))
            
            # Create Document record
            with open(output_path, 'rb') as f:
                content = f.read()
            
            document = Document.objects.create(
                filename=output_filename,
                content=content,
                content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document',
                file_size=len(content),
                document_category='itinerary'
            )
            
            logger.info(f"Generated General Declaration: {output_filename}")
            return document
            
        except Trip.DoesNotExist:
            logger.error(f"Trip not found: {trip_id}")
            return None
        except Exception as e:
            logger.error(f"Error generating General Declaration: {str(e)}")
            return None
    
    def generate_quote_document(self, quote_id: str, output_filename: Optional[str] = None) -> Optional[Document]:
        """
        Generate a quote document.
        
        Args:
            quote_id: UUID of the quote
            output_filename: Optional custom filename
            
        Returns:
            Document instance if successful, None otherwise
        """
        try:
            from operations.models import Quote
            quote = Quote.objects.get(id=quote_id)
            
            if not DOCX_AVAILABLE:
                logger.error("python-docx not available for document generation")
                return None
            
            # Create new document
            doc = DocxDocument()
            
            # Add title
            title = doc.add_heading('FLIGHT QUOTE', 0)
            title.alignment = 1  # Center alignment
            
            # Add quote information
            doc.add_heading('Quote Details', level=1)
            
            quote_table = doc.add_table(rows=0, cols=2)
            quote_table.style = 'Table Grid'
            
            self._add_table_row(quote_table, 'Quote Amount:', f"${quote.quoted_amount:,.2f}")
            self._add_table_row(quote_table, 'Contact:', str(quote.contact))
            self._add_table_row(quote_table, 'Aircraft Type:', quote.get_aircraft_type_display())
            self._add_table_row(quote_table, 'Medical Team:', quote.get_medical_team_display())
            self._add_table_row(quote_table, 'Pickup Airport:', str(quote.pickup_airport))
            self._add_table_row(quote_table, 'Dropoff Airport:', str(quote.dropoff_airport))
            self._add_table_row(quote_table, 'Estimated Flight Time:', str(quote.estimated_flight_time))
            self._add_table_row(quote_table, 'Number of Stops:', str(quote.number_of_stops))
            self._add_table_row(quote_table, 'Includes Ground Transport:', 'Yes' if quote.includes_grounds else 'No')
            self._add_table_row(quote_table, 'Status:', quote.get_status_display())
            self._add_table_row(quote_table, 'Payment Status:', quote.get_payment_status_display())
            
            # Add cruise information if available
            if quote.cruise_line:
                doc.add_heading('Cruise Information', level=1)
                
                cruise_table = doc.add_table(rows=0, cols=2)
                cruise_table.style = 'Table Grid'
                
                self._add_table_row(cruise_table, 'Cruise Line:', quote.cruise_line)
                self._add_table_row(cruise_table, 'Ship:', quote.cruise_ship or 'N/A')
                if quote.cruise_doctor_first_name and quote.cruise_doctor_last_name:
                    doctor_name = f"{quote.cruise_doctor_first_name} {quote.cruise_doctor_last_name}"
                    self._add_table_row(cruise_table, 'Ship Doctor:', doctor_name)
            
            # Add patient information if available
            if quote.patient:
                doc.add_heading('Patient Information', level=1)
                
                patient_table = doc.add_table(rows=0, cols=2)
                patient_table.style = 'Table Grid'
                
                self._add_table_row(patient_table, 'Patient:', str(quote.patient.info))
                self._add_table_row(patient_table, 'Bed at Origin:', 'Yes' if quote.patient.bed_at_origin else 'No')
                self._add_table_row(patient_table, 'Bed at Destination:', 'Yes' if quote.patient.bed_at_destination else 'No')
                
                if quote.patient.special_instructions:
                    doc.add_heading('Special Instructions', level=2)
                    doc.add_paragraph(quote.patient.special_instructions)
            
            # Add footer with generation date
            doc.add_paragraph()
            footer = doc.add_paragraph(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            footer.alignment = 1  # Center alignment
            
            # Save document
            if not output_filename:
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                output_filename = f"Quote_{quote.id}_{timestamp}.docx"
            
            output_path = self.outputs_dir / output_filename
            doc.save(str(output_path))
            
            # Create Document record
            with open(output_path, 'rb') as f:
                content = f.read()
            
            document = Document.objects.create(
                filename=output_filename,
                content=content,
                content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document',
                file_size=len(content),
                document_category='quote'
            )
            
            logger.info(f"Generated quote document: {output_filename}")
            return document
            
        except Exception as e:
            logger.error(f"Error generating quote document: {str(e)}")
            return None
    
    def generate_itinerary(self, trip_id: str, customer_facing: bool = True, 
                          output_filename: Optional[str] = None) -> Optional[Document]:
        """
        Generate an itinerary document for a trip.
        
        Args:
            trip_id: UUID of the trip
            customer_facing: Whether this is for customer or internal use
            output_filename: Optional custom filename
            
        Returns:
            Document instance if successful, None otherwise
        """
        try:
            trip = Trip.objects.get(id=trip_id)
            
            if not DOCX_AVAILABLE:
                logger.error("python-docx not available for document generation")
                return None
            
            # Create new document
            doc = DocxDocument()
            
            # Add title
            title_text = 'FLIGHT ITINERARY' if customer_facing else 'INTERNAL FLIGHT ITINERARY'
            title = doc.add_heading(title_text, 0)
            title.alignment = 1  # Center alignment
            
            # Add trip information
            doc.add_heading('Trip Information', level=1)
            
            trip_table = doc.add_table(rows=0, cols=2)
            trip_table.style = 'Table Grid'
            
            self._add_table_row(trip_table, 'Trip Number:', trip.trip_number)
            self._add_table_row(trip_table, 'Trip Type:', trip.get_type_display())
            
            if not customer_facing or trip.aircraft:
                self._add_table_row(trip_table, 'Aircraft:', str(trip.aircraft) if trip.aircraft else 'TBD')
            
            if trip.estimated_departure_time:
                self._add_table_row(trip_table, 'Departure Time:', 
                                  trip.estimated_departure_time.strftime('%Y-%m-%d %H:%M UTC'))
            
            # Add detailed flight schedule
            if trip.trip_lines.exists():
                doc.add_heading('Flight Schedule', level=1)
                
                for i, trip_line in enumerate(trip.trip_lines.all(), 1):
                    doc.add_heading(f'Leg {i}: {trip_line.origin_airport} → {trip_line.destination_airport}', level=2)
                    
                    leg_table = doc.add_table(rows=0, cols=2)
                    leg_table.style = 'Table Grid'
                    
                    self._add_table_row(leg_table, 'Origin:', f"{trip_line.origin_airport} ({trip_line.origin_airport.city})")
                    self._add_table_row(leg_table, 'Destination:', f"{trip_line.destination_airport} ({trip_line.destination_airport.city})")
                    self._add_table_row(leg_table, 'Departure (Local):', trip_line.departure_time_local.strftime('%Y-%m-%d %H:%M'))
                    self._add_table_row(leg_table, 'Arrival (Local):', trip_line.arrival_time_local.strftime('%Y-%m-%d %H:%M'))
                    self._add_table_row(leg_table, 'Flight Time:', str(trip_line.flight_time))
                    self._add_table_row(leg_table, 'Distance:', f"{trip_line.distance} nm")
                    
                    if not customer_facing:
                        self._add_table_row(leg_table, 'Departure (UTC):', trip_line.departure_time_utc.strftime('%Y-%m-%d %H:%M'))
                        self._add_table_row(leg_table, 'Arrival (UTC):', trip_line.arrival_time_utc.strftime('%Y-%m-%d %H:%M'))
                        
                        if trip_line.departure_fbo:
                            self._add_table_row(leg_table, 'Departure FBO:', str(trip_line.departure_fbo))
                        if trip_line.arrival_fbo:
                            self._add_table_row(leg_table, 'Arrival FBO:', str(trip_line.arrival_fbo))
                        
                        if trip_line.crew_line:
                            self._add_table_row(leg_table, 'Crew:', str(trip_line.crew_line))
            
            # Add notes if any
            if trip.notes:
                doc.add_heading('Notes', level=1)
                doc.add_paragraph(trip.notes)
            
            # Add footer
            doc.add_paragraph()
            footer = doc.add_paragraph(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            footer.alignment = 1  # Center alignment
            
            # Save document
            if not output_filename:
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                doc_type = 'Customer' if customer_facing else 'Internal'
                output_filename = f"{doc_type}_Itinerary_{trip.trip_number}_{timestamp}.docx"
            
            output_path = self.outputs_dir / output_filename
            doc.save(str(output_path))
            
            # Create Document record
            with open(output_path, 'rb') as f:
                content = f.read()
            
            document = Document.objects.create(
                filename=output_filename,
                content=content,
                content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document',
                file_size=len(content),
                document_category='itinerary'
            )
            
            logger.info(f"Generated itinerary: {output_filename}")
            return document
            
        except Trip.DoesNotExist:
            logger.error(f"Trip not found: {trip_id}")
            return None
        except Exception as e:
            logger.error(f"Error generating itinerary: {str(e)}")
            return None
    
    def _add_table_row(self, table, label: str, value: str):
        """Helper method to add a row to a table."""
        row_cells = table.add_row().cells
        row_cells[0].text = label
        row_cells[1].text = value
    
    def list_available_templates(self) -> List[str]:
        """List all available document templates."""
        if not self.templates_dir.exists():
            return []
        
        templates = []
        for file_path in self.templates_dir.glob('*.docx'):
            templates.append(file_path.name)
        
        return templates
    
    def cleanup_old_documents(self, days_old: int = 30):
        """Clean up old generated documents."""
        cutoff_date = datetime.now() - timedelta(days=days_old)
        
        deleted_count = 0
        for file_path in self.outputs_dir.glob('*.docx'):
            if file_path.stat().st_mtime < cutoff_date.timestamp():
                try:
                    file_path.unlink()
                    deleted_count += 1
                except OSError as e:
                    logger.error(f"Error deleting old document {file_path}: {e}")
        
        logger.info(f"Cleaned up {deleted_count} old documents")
        return deleted_count


# Convenience functions for backward compatibility
def generate_general_declaration(trip_id: str, output_filename: Optional[str] = None) -> Optional[Document]:
    """Generate a General Declaration document."""
    service = DocumentGenerationService()
    return service.generate_general_declaration(trip_id, output_filename)


def generate_quote_document(quote_id: str, output_filename: Optional[str] = None) -> Optional[Document]:
    """Generate a quote document."""
    service = DocumentGenerationService()
    return service.generate_quote_document(quote_id, output_filename)


def generate_itinerary(trip_id: str, customer_facing: bool = True, 
                      output_filename: Optional[str] = None) -> Optional[Document]:
    """Generate an itinerary document."""
    service = DocumentGenerationService()
    return service.generate_itinerary(trip_id, customer_facing, output_filename)

```


# File: documents/services/document_service.py

```python
from django.core.files.base import ContentFile
from django.utils import timezone
from django.template.loader import render_to_string
from django.conf import settings
from ..models import Document, Agreement, DocumentTemplate, GeneratedDocument, DocumentAccess
import uuid
import mimetypes
from io import BytesIO
import logging

logger = logging.getLogger(__name__)


class DocumentService:
    """Service for document management operations."""
    
    @staticmethod
    def create_document(filename, content, content_type=None, uploaded_by=None, document_category='other'):
        """Create a new document with file content."""
        try:
            # Determine content type if not provided
            if not content_type:
                content_type, _ = mimetypes.guess_type(filename)
                if not content_type:
                    content_type = 'application/octet-stream'
            
            # Calculate file size
            if isinstance(content, bytes):
                file_size = len(content)
            elif hasattr(content, 'size'):
                file_size = content.size
            else:
                file_size = 0
            
            document = Document.objects.create(
                filename=filename,
                content=content,
                content_type=content_type,
                file_size=file_size,
                uploaded_by=uploaded_by,
                document_category=document_category
            )
            
            logger.info(f"Document created: {document.filename} ({document.id})")
            return document
            
        except Exception as e:
            logger.error(f"Error creating document: {str(e)}")
            raise
    
    @staticmethod
    def get_document_content(document_id):
        """Retrieve document content by ID."""
        try:
            document = Document.objects.get(id=document_id)
            return document.content
        except Document.DoesNotExist:
            logger.error(f"Document not found: {document_id}")
            return None
    
    @staticmethod
    def log_document_access(document, user, access_type='view', ip_address=None, user_agent=None):
        """Log document access for audit purposes."""
        try:
            DocumentAccess.objects.create(
                document=document,
                accessed_by=user,
                access_type=access_type,
                ip_address=ip_address,
                user_agent=user_agent
            )
            logger.info(f"Document access logged: {document.filename} by {user}")
        except Exception as e:
            logger.error(f"Error logging document access: {str(e)}")
    
    @staticmethod
    def delete_document(document_id, user=None):
        """Soft delete a document by setting flag."""
        try:
            document = Document.objects.get(id=document_id)
            document.flag = 1  # Mark as deleted
            document.save()
            
            if user:
                DocumentService.log_document_access(document, user, 'delete')
            
            logger.info(f"Document deleted: {document.filename}")
            return True
        except Document.DoesNotExist:
            logger.error(f"Document not found for deletion: {document_id}")
            return False


class AgreementService:
    """Service for agreement management operations."""
    
    @staticmethod
    def create_agreement(agreement_type, title, destination_email, description=None, 
                        signatory_name=None, signatory_title=None, expiration_days=30):
        """Create a new agreement."""
        try:
            # Calculate expiration date
            expiration_date = None
            if expiration_days:
                expiration_date = timezone.now() + timezone.timedelta(days=expiration_days)
            
            agreement = Agreement.objects.create(
                agreement_type=agreement_type,
                title=title,
                description=description,
                destination_email=destination_email,
                signatory_name=signatory_name,
                signatory_title=signatory_title,
                expiration_date=expiration_date,
                status='created'
            )
            
            logger.info(f"Agreement created: {agreement.title} for {destination_email}")
            return agreement
            
        except Exception as e:
            logger.error(f"Error creating agreement: {str(e)}")
            raise
    
    @staticmethod
    def send_agreement(agreement_id, user=None):
        """Mark agreement as sent and update sent date."""
        try:
            agreement = Agreement.objects.get(id=agreement_id)
            agreement.status = 'sent'
            agreement.sent_date = timezone.now()
            agreement.save()
            
            logger.info(f"Agreement sent: {agreement.title}")
            return agreement
            
        except Agreement.DoesNotExist:
            logger.error(f"Agreement not found: {agreement_id}")
            return None
    
    @staticmethod
    def sign_agreement(agreement_id, signature_ip=None, signature_user_agent=None, 
                      terms_accepted=True, terms_version=None):
        """Process agreement signature."""
        try:
            agreement = Agreement.objects.get(id=agreement_id)
            
            # Check if agreement is still valid
            if agreement.is_expired:
                logger.error(f"Cannot sign expired agreement: {agreement_id}")
                return None
            
            if agreement.status not in ['sent', 'pending']:
                logger.error(f"Agreement not in signable state: {agreement.status}")
                return None
            
            # Update agreement with signature information
            agreement.status = 'signed'
            agreement.signed_date = timezone.now()
            agreement.signature_ip_address = signature_ip
            agreement.signature_user_agent = signature_user_agent
            agreement.terms_accepted = terms_accepted
            agreement.terms_version = terms_version
            agreement.save()
            
            logger.info(f"Agreement signed: {agreement.title}")
            return agreement
            
        except Agreement.DoesNotExist:
            logger.error(f"Agreement not found: {agreement_id}")
            return None
    
    @staticmethod
    def get_expiring_agreements(days_ahead=7):
        """Get agreements expiring within specified days."""
        try:
            cutoff_date = timezone.now() + timezone.timedelta(days=days_ahead)
            return Agreement.objects.filter(
                expiration_date__lte=cutoff_date,
                status__in=['sent', 'pending']
            ).order_by('expiration_date')
        except Exception as e:
            logger.error(f"Error getting expiring agreements: {str(e)}")
            return Agreement.objects.none()


class DocumentTemplateService:
    """Service for document template operations."""
    
    @staticmethod
    def create_template(name, template_type, template_content, description=None,
                       css_styles=None, required_variables=None, optional_variables=None):
        """Create a new document template."""
        try:
            template = DocumentTemplate.objects.create(
                name=name,
                template_type=template_type,
                description=description,
                template_content=template_content,
                css_styles=css_styles or '',
                required_variables=required_variables or [],
                optional_variables=optional_variables or [],
                is_active=True
            )
            
            logger.info(f"Document template created: {template.name}")
            return template
            
        except Exception as e:
            logger.error(f"Error creating document template: {str(e)}")
            raise
    
    @staticmethod
    def generate_document_from_template(template_id, variables, filename=None, 
                                      related_quote_id=None, related_trip_id=None, 
                                      related_agreement_id=None):
        """Generate a document from a template with provided variables."""
        try:
            template = DocumentTemplate.objects.get(id=template_id, is_active=True)
            
            # Validate required variables
            missing_vars = []
            for var in template.required_variables:
                if var not in variables:
                    missing_vars.append(var)
            
            if missing_vars:
                raise ValueError(f"Missing required variables: {', '.join(missing_vars)}")
            
            # Render template content
            from django.template import Context, Template
            django_template = Template(template.template_content)
            context = Context(variables)
            rendered_content = django_template.render(context)
            
            # Generate filename if not provided
            if not filename:
                timestamp = timezone.now().strftime('%Y%m%d_%H%M%S')
                filename = f"{template.name}_{timestamp}.html"
            
            # Create document
            document = DocumentService.create_document(
                filename=filename,
                content=rendered_content.encode('utf-8'),
                content_type='text/html',
                document_category=template.template_type
            )
            
            # Create generation record
            generated_doc = GeneratedDocument.objects.create(
                template=template,
                document=document,
                variables_used=variables,
                related_quote_id=related_quote_id,
                related_trip_id=related_trip_id,
                related_agreement_id=related_agreement_id
            )
            
            logger.info(f"Document generated from template: {template.name}")
            return document, generated_doc
            
        except DocumentTemplate.DoesNotExist:
            logger.error(f"Template not found or inactive: {template_id}")
            return None, None
        except Exception as e:
            logger.error(f"Error generating document from template: {str(e)}")
            raise
    
    @staticmethod
    def get_active_templates(template_type=None):
        """Get all active templates, optionally filtered by type."""
        try:
            queryset = DocumentTemplate.objects.filter(is_active=True)
            if template_type:
                queryset = queryset.filter(template_type=template_type)
            return queryset.order_by('name')
        except Exception as e:
            logger.error(f"Error getting active templates: {str(e)}")
            return DocumentTemplate.objects.none()

```


# File: documents/tests/test_document_generation.py

```python
"""
Django test cases for document generation functionality.

Converted from custom test scripts to proper Django TestCase.
"""

from django.test import TestCase
from django.utils import timezone
from datetime import datetime, timedelta
from operations.models import Trip, TripLine, CrewLine, Passenger, Patient, Quote
from contacts.models import Contact
from aircraft.models import Aircraft
from airports.models import Airport
from documents.services.document_generation_service import DocumentGenerationService, generate_general_declaration


class DocumentGenerationTestCase(TestCase):
    """Test case for document generation functionality."""
    
    def setUp(self):
        """Set up test data for document generation tests."""
        # Create airports
        self.origin_airport = Airport.objects.create(
            name="Los Angeles International Airport",
            iata_code="LAX",
            icao_code="KLAX",
            city="Los Angeles",
            state="CA",
            country="USA",
            latitude=33.942536,
            longitude=-118.408074,
            timezone="America/Los_Angeles"
        )
        
        self.destination_airport = Airport.objects.create(
            name="John F. Kennedy International Airport", 
            iata_code="JFK",
            icao_code="KJFK",
            city="New York",
            state="NY", 
            country="USA",
            latitude=40.639751,
            longitude=-73.778925,
            timezone="America/New_York"
        )
        
        # Create aircraft
        self.aircraft = Aircraft.objects.create(
            tail_number="N123AB",
            company="Test Aviation Company",
            make="Cessna",
            model="Citation X",
            mgtow=16300.00,
            serial_number="560-5001"
        )
        
        # Create contacts for crew
        self.pilot1_contact = Contact.objects.create(
            first_name="John",
            last_name="Smith",
            email="pilot1@test.com"
        )
        
        self.pilot2_contact = Contact.objects.create(
            first_name="Jane", 
            last_name="Doe",
            email="pilot2@test.com"
        )
        
        self.medic_contact = Contact.objects.create(
            first_name="Dr. Sarah",
            last_name="Johnson",
            email="medic@test.com"
        )
        
        # Create crew line
        self.crew_line = CrewLine.objects.create(
            primary_in_command=self.pilot1_contact,
            secondary_in_command=self.pilot2_contact
        )
        self.crew_line.medic_ids.add(self.medic_contact)
        
        # Create passenger contacts and passengers
        self.passenger1_contact = Contact.objects.create(
            first_name="Michael",
            last_name="Brown",
            email="passenger1@test.com"
        )
        
        self.passenger2_contact = Contact.objects.create(
            first_name="Lisa",
            last_name="Williams", 
            email="passenger2@test.com"
        )
        
        self.passenger1 = Passenger.objects.create(
            info=self.passenger1_contact,
            nationality="USA",
            passport_number="123456789",
            date_of_birth=datetime(1980, 5, 15).date()
        )
        
        self.passenger2 = Passenger.objects.create(
            info=self.passenger2_contact,
            nationality="USA", 
            passport_number="987654321",
            date_of_birth=datetime(1975, 8, 22).date()
        )
        
        # Create patient for medical trip
        self.patient_contact = Contact.objects.create(
            first_name="Patient",
            last_name="Smith",
            email="patient@test.com"
        )
        
        self.patient = Patient.objects.create(
            info=self.patient_contact,
            date_of_birth=datetime(1960, 3, 10).date()
        )
        
        # Initialize document generation service
        self.generator = DocumentGenerationService()
    
    def test_passenger_trip_gendec_generation(self):
        """Test GenDec generation for a passenger-carrying trip."""
        # Create medical trip with passengers
        trip = Trip.objects.create(
            trip_number="TEST001",
            type="medical",
            aircraft=self.aircraft,
            patient=self.patient,
            estimated_departure_time=timezone.now() + timedelta(hours=2)
        )
        trip.passengers.add(self.passenger1, self.passenger2)
        
        # Create passenger leg
        trip_line = TripLine.objects.create(
            trip=trip,
            origin_airport=self.origin_airport,
            destination_airport=self.destination_airport,
            crew_line=self.crew_line,
            departure_time_local=timezone.now() + timedelta(hours=2),
            departure_time_utc=timezone.now() + timedelta(hours=10),
            arrival_time_local=timezone.now() + timedelta(hours=7),
            arrival_time_utc=timezone.now() + timedelta(hours=12),
            distance=2475.00,
            flight_time=timedelta(hours=5),
            ground_time=timedelta(hours=1),
            passenger_leg=True
        )
        
        # Generate GenDec
        document = self.generator.generate_general_declaration(str(trip.id))
        
        # Assertions
        self.assertIsNotNone(document, "Document should be generated")
        self.assertIsNotNone(document.content, "Document should have content")
        self.assertGreater(document.file_size, 1000, "Document should have reasonable size")
        self.assertEqual(document.document_category, 'itinerary')
        self.assertIn('GenDec', document.filename)
    
    def test_repositioning_trip_gendec_generation(self):
        """Test GenDec generation for a repositioning (no passenger) trip.""" 
        # Create repositioning trip (no passengers)
        trip = Trip.objects.create(
            trip_number="REPO001",
            type="maintenance", 
            aircraft=self.aircraft,
            estimated_departure_time=timezone.now() + timedelta(hours=1)
        )
        
        # Create repositioning leg
        trip_line = TripLine.objects.create(
            trip=trip,
            origin_airport=self.destination_airport,
            destination_airport=self.origin_airport,
            crew_line=self.crew_line,
            departure_time_local=timezone.now() + timedelta(hours=1),
            departure_time_utc=timezone.now() + timedelta(hours=6),
            arrival_time_local=timezone.now() + timedelta(hours=6),
            arrival_time_utc=timezone.now() + timedelta(hours=14),
            distance=2475.00,
            flight_time=timedelta(hours=5),
            ground_time=timedelta(hours=1),
            passenger_leg=False
        )
        
        # Generate GenDec
        document = self.generator.generate_general_declaration(str(trip.id))
        
        # Assertions
        self.assertIsNotNone(document, "Repositioning document should be generated")
        self.assertIsNotNone(document.content, "Document should have content")
        self.assertGreater(document.file_size, 1000, "Document should have reasonable size")
    
    def test_convenience_function(self):
        """Test the convenience function for generating GenDec."""
        # Create a simple trip for testing
        trip = Trip.objects.create(
            trip_number="CONV001",
            type="charter",
            aircraft=self.aircraft
        )
        
        trip_line = TripLine.objects.create(
            trip=trip,
            origin_airport=self.origin_airport,
            destination_airport=self.destination_airport,
            crew_line=self.crew_line,
            departure_time_local=timezone.now() + timedelta(hours=3),
            departure_time_utc=timezone.now() + timedelta(hours=11),
            arrival_time_local=timezone.now() + timedelta(hours=8),
            arrival_time_utc=timezone.now() + timedelta(hours=13),
            distance=2475.00,
            flight_time=timedelta(hours=5),
            ground_time=timedelta(hours=1),
            passenger_leg=False
        )
        
        # Test convenience function
        document = generate_general_declaration(str(trip.id))
        
        # Assertions
        self.assertIsNotNone(document, "Convenience function should work")
        self.assertIsNotNone(document.content, "Document should have content")
    
    def test_quote_document_generation(self):
        """Test quote document generation."""
        # Create a quote
        quote = Quote.objects.create(
            contact=self.passenger1_contact,
            pickup_airport=self.origin_airport,
            dropoff_airport=self.destination_airport,
            aircraft_type="light_jet",
            medical_team="basic",
            quoted_amount=15000.00,
            estimated_flight_time=timedelta(hours=5),
            number_of_stops=0,
            includes_grounds=True,
            patient=self.patient
        )
        
        # Generate quote document
        document = self.generator.generate_quote_document(str(quote.id))
        
        # Assertions
        self.assertIsNotNone(document, "Quote document should be generated")
        self.assertIsNotNone(document.content, "Document should have content")
        self.assertEqual(document.document_category, 'quote')
        self.assertIn('Quote', document.filename)
    
    def test_customer_itinerary_generation(self):
        """Test customer-facing itinerary generation."""
        # Create trip with multiple legs
        trip = Trip.objects.create(
            trip_number="ITIN001",
            type="charter",
            aircraft=self.aircraft,
            estimated_departure_time=timezone.now() + timedelta(hours=2)
        )
        trip.passengers.add(self.passenger1)
        
        # Create multiple trip lines
        TripLine.objects.create(
            trip=trip,
            origin_airport=self.origin_airport,
            destination_airport=self.destination_airport,
            crew_line=self.crew_line,
            departure_time_local=timezone.now() + timedelta(hours=2),
            departure_time_utc=timezone.now() + timedelta(hours=10),
            arrival_time_local=timezone.now() + timedelta(hours=7),
            arrival_time_utc=timezone.now() + timedelta(hours=12),
            distance=2475.00,
            flight_time=timedelta(hours=5),
            passenger_leg=True
        )
        
        # Generate customer itinerary
        document = self.generator.generate_itinerary(str(trip.id), customer_facing=True)
        
        # Assertions
        self.assertIsNotNone(document, "Customer itinerary should be generated")
        self.assertIsNotNone(document.content, "Document should have content")
        self.assertEqual(document.document_category, 'itinerary')
        self.assertIn('Customer_Itinerary', document.filename)
    
    def test_internal_itinerary_generation(self):
        """Test internal itinerary generation."""
        # Create trip
        trip = Trip.objects.create(
            trip_number="ITIN002",
            type="medical",
            aircraft=self.aircraft,
            patient=self.patient,
            estimated_departure_time=timezone.now() + timedelta(hours=1)
        )
        
        # Create trip line
        TripLine.objects.create(
            trip=trip,
            origin_airport=self.origin_airport,
            destination_airport=self.destination_airport,
            crew_line=self.crew_line,
            departure_time_local=timezone.now() + timedelta(hours=1),
            departure_time_utc=timezone.now() + timedelta(hours=9),
            arrival_time_local=timezone.now() + timedelta(hours=6),
            arrival_time_utc=timezone.now() + timedelta(hours=11),
            distance=2475.00,
            flight_time=timedelta(hours=5),
            passenger_leg=True
        )
        
        # Generate internal itinerary
        document = self.generator.generate_itinerary(str(trip.id), customer_facing=False)
        
        # Assertions
        self.assertIsNotNone(document, "Internal itinerary should be generated")
        self.assertIsNotNone(document.content, "Document should have content")
        self.assertEqual(document.document_category, 'itinerary')
        self.assertIn('Internal_Itinerary', document.filename)
    
    def test_document_generation_error_handling(self):
        """Test error handling in document generation."""
        # Test with non-existent trip ID
        document = self.generator.generate_general_declaration("non-existent-id")
        self.assertIsNone(document, "Should return None for non-existent trip")
        
        # Test with invalid quote ID
        document = self.generator.generate_quote_document("invalid-quote-id")
        self.assertIsNone(document, "Should return None for invalid quote")
    
    def test_template_management(self):
        """Test template management functionality."""
        # Test listing available templates
        templates = self.generator.list_available_templates()
        self.assertIsInstance(templates, list, "Should return a list of templates")
        
        # Test cleanup functionality (should not raise errors)
        try:
            deleted_count = self.generator.cleanup_old_documents(days_old=365)
            self.assertIsInstance(deleted_count, int, "Should return count of deleted files")
        except Exception as e:
            self.fail(f"Cleanup should not raise exceptions: {e}")

```


# File: documents/tests/__init__.py

```python

```


# File: operations/models.py

```python
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from common.models import BaseModel


class Quote(BaseModel):
    """Quote model for flight operations pricing."""
    quoted_amount = models.DecimalField(max_digits=10, decimal_places=2)
    contact = models.ForeignKey('contacts.Contact', on_delete=models.CASCADE, related_name="quotes")
    documents = models.ManyToManyField('documents.Document', related_name="quotes")
    
    # Cruise information
    cruise_doctor_first_name = models.CharField(max_length=100, blank=True, null=True)
    cruise_doctor_last_name = models.CharField(max_length=100, blank=True, null=True)
    cruise_line = models.CharField(max_length=100, blank=True, null=True)
    cruise_ship = models.CharField(max_length=100, blank=True, null=True)
    
    # Flight details
    pickup_airport = models.ForeignKey('airports.Airport', on_delete=models.CASCADE, related_name="pickup_quotes")
    dropoff_airport = models.ForeignKey('airports.Airport', on_delete=models.CASCADE, related_name="dropoff_quotes")
    aircraft_type = models.CharField(max_length=20, choices=[
        ("65", "Learjet 65"),
        ("35", "Learjet 35"),
        ("TBD", "To Be Determined")
    ])
    estimated_flight_time = models.DurationField()
    includes_grounds = models.BooleanField(default=False)
    number_of_stops = models.PositiveIntegerField(default=0)
    
    # Medical team configuration
    medical_team = models.CharField(max_length=20, choices=[
        ("RN/RN", "RN/RN"),
        ("RN/Paramedic", "RN/Paramedic"),
        ("RN/MD", "RN/MD"),
        ("RN/RT", "RN/RT"),
        ("standard", "Standard"),
        ("full", "Full")
    ])
    
    # Status and dates
    inquiry_date = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=20, choices=[
        ("pending", "Pending"),
        ("active", "Active"),
        ("completed", "Completed"),
        ("cancelled", "Cancelled")
    ], default="pending", db_index=True)
    
    # Payment information
    payment_status = models.CharField(max_length=20, choices=[
        ("pending", "Pending"),
        ("partial", "Partial Paid"),
        ("paid", "Paid")
    ], default="pending")
    
    # Related entities
    patient = models.ForeignKey('Patient', on_delete=models.SET_NULL, null=True, blank=True, related_name="quotes")
    transactions = models.ManyToManyField('finance.Transaction', related_name="quotes", blank=True)
    
    # Documents
    quote_pdf = models.ForeignKey('documents.Document', on_delete=models.SET_NULL, null=True, blank=True, related_name="quote_pdfs")
    quote_pdf_status = models.CharField(max_length=20, choices=[
        ("created", "Created"),
        ("pending", "Pending"),
        ("modified", "Modified"),
        ("accepted", "Accepted"),
        ("denied", "Denied")
    ], default="created")
    quote_pdf_email = models.EmailField()
    
    # Agreements
    payment_agreement = models.ForeignKey('documents.Agreement', on_delete=models.SET_NULL, null=True, blank=True, related_name="payment_quotes")
    consent_for_transport = models.ForeignKey('documents.Agreement', on_delete=models.SET_NULL, null=True, blank=True, related_name="consent_quotes")
    patient_service_agreement = models.ForeignKey('documents.Agreement', on_delete=models.SET_NULL, null=True, blank=True, related_name="service_quotes")
    
    class Meta:
        indexes = [
            models.Index(fields=['status', 'created_on']),
            models.Index(fields=['payment_status']),
        ]
    
    def __str__(self):
        return f"Quote {self.id} - ${self.quoted_amount} - {self.status}"


class Patient(BaseModel):
    """Patient model for medical transport operations."""
    info = models.ForeignKey('contacts.Contact', on_delete=models.CASCADE, related_name="patients")
    
    # Medical requirements
    bed_at_origin = models.BooleanField(default=False)
    bed_at_destination = models.BooleanField(default=False)
    special_instructions = models.TextField(blank=True, null=True)
    
    # Personal information
    date_of_birth = models.DateField()
    nationality = models.CharField(max_length=100)
    
    # Travel documents
    passport_number = models.CharField(max_length=100)
    passport_expiration_date = models.DateField()
    passport_document = models.ForeignKey('documents.Document', on_delete=models.SET_NULL, null=True, blank=True, related_name="passport_patients")
    letter_of_medical_necessity = models.ForeignKey('documents.Document', on_delete=models.SET_NULL, null=True, blank=True, related_name="medical_necessity_patients")
    
    # Status
    status = models.CharField(max_length=20, choices=[
        ("pending", "Pending"),
        ("confirmed", "Confirmed"),
        ("active", "Active"),
        ("completed", "Completed"),
        ("cancelled", "Cancelled")
    ], default="pending", db_index=True)
    
    class Meta:
        indexes = [
            models.Index(fields=['status', 'created_on']),
        ]
    
    def __str__(self):
        return f"Patient: {self.info}"


class Passenger(BaseModel):
    """Passenger model for charter operations."""
    info = models.ForeignKey('contacts.Contact', on_delete=models.CASCADE, related_name="passengers")
    
    # Personal information
    date_of_birth = models.DateField(blank=True, null=True)
    nationality = models.CharField(max_length=100, blank=True, null=True)
    contact_number = models.CharField(max_length=20, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    
    # Travel documents
    passport_number = models.CharField(max_length=100, blank=True, null=True)
    passport_expiration_date = models.DateField(blank=True, null=True)
    passport_document = models.ForeignKey('documents.Document', on_delete=models.SET_NULL, null=True, blank=True, related_name="passport_passengers")
    
    # Relationships
    passenger_ids = models.ManyToManyField('self', blank=True, symmetrical=False, related_name="related_passengers")
    
    def __str__(self):
        return f"Passenger: {self.info}"


class CrewLine(BaseModel):
    """Crew assignment for flight operations."""
    primary_in_command = models.ForeignKey('contacts.Contact', on_delete=models.CASCADE, related_name="primary_crew_lines")
    secondary_in_command = models.ForeignKey('contacts.Contact', on_delete=models.CASCADE, related_name="secondary_crew_lines")
    medic_ids = models.ManyToManyField('contacts.Contact', related_name="medic_crew_lines")
    
    class Meta:
        indexes = [
            models.Index(fields=['primary_in_command', 'secondary_in_command']),
        ]
    
    def __str__(self):
        return f"Crew: {self.primary_in_command} and {self.secondary_in_command}"


class TripStatus(models.TextChoices):
    """Trip lifecycle status choices."""
    REQUESTED = 'REQUESTED', 'Requested'
    QUOTED = 'QUOTED', 'Quoted'
    CONFIRMED = 'CONFIRMED', 'Confirmed'
    IN_PROGRESS = 'IN_PROGRESS', 'In Progress'
    COMPLETED = 'COMPLETED', 'Completed'
    BILLED = 'BILLED', 'Billed'
    CANCELLED = 'CANCELLED', 'Cancelled'


class Trip(BaseModel):
    """Main trip model representing a complete flight operation."""
    
    TRIP_TYPES = [
        ("medical", "Medical"),
        ("charter", "Charter"),
        ("part_91", "Part 91"),
        ("other", "Other"),
        ("maintenance", "Maintenance")
    ]
    
    # Basic information
    trip_number = models.CharField(max_length=50, unique=True)
    type = models.CharField(max_length=50, choices=TRIP_TYPES, default='CHARTER')
    status = models.CharField(max_length=50, choices=TripStatus.choices, default=TripStatus.REQUESTED)
    notes = models.TextField(blank=True, null=True)
    
    # Status tracking
    status_history = models.JSONField(default=list, blank=True)
    last_status_change = models.DateTimeField(auto_now=True)
    
    # Pricing information
    quoted_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    final_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    pricing_breakdown = models.JSONField(default=dict, blank=True)
    
    # Related entities
    quote = models.ForeignKey(Quote, on_delete=models.CASCADE, related_name="trips", null=True, blank=True)
    patient = models.ForeignKey(Patient, on_delete=models.SET_NULL, null=True, blank=True, related_name="trips")
    aircraft = models.ForeignKey('aircraft.Aircraft', on_delete=models.SET_NULL, null=True, blank=True, related_name="trips")
    passengers = models.ManyToManyField(Passenger, related_name="trips", blank=True)
    
    # Timing
    estimated_departure_time = models.DateTimeField(blank=True, null=True)
    pre_flight_duty_time = models.DurationField(blank=True, null=True)
    post_flight_duty_time = models.DurationField(blank=True, null=True)
    
    # Documents
    internal_itinerary = models.ForeignKey('documents.Document', on_delete=models.SET_NULL, null=True, blank=True, related_name="internal_itinerary_trips")
    customer_itinerary = models.ForeignKey('documents.Document', on_delete=models.SET_NULL, null=True, blank=True, related_name="customer_itinerary_trips")
    
    # Communication
    email_chain = models.JSONField(default=list, blank=True)
    
    class Meta:
        indexes = [
            models.Index(fields=['trip_number']),
            models.Index(fields=['type', 'status']),
            models.Index(fields=['estimated_departure_time']),
        ]
    
    def update_status(self, new_status: str, user=None, notes: str = ""):
        """Update trip status with history tracking."""
        if new_status not in [choice[0] for choice in TripStatus.choices]:
            raise ValueError(f"Invalid status: {new_status}")
        
        # Add to status history
        status_entry = {
            'from_status': self.status,
            'to_status': new_status,
            'timestamp': timezone.now().isoformat(),
            'user': str(user) if user else None,
            'notes': notes
        }
        
        if not self.status_history:
            self.status_history = []
        
        self.status_history.append(status_entry)
        self.status = new_status
        self.last_status_change = timezone.now()
        self.save()
    
    def can_transition_to(self, new_status: str) -> bool:
        """Check if status transition is valid."""
        valid_transitions = {
            TripStatus.REQUESTED: [TripStatus.QUOTED, TripStatus.CANCELLED],
            TripStatus.QUOTED: [TripStatus.CONFIRMED, TripStatus.CANCELLED],
            TripStatus.CONFIRMED: [TripStatus.IN_PROGRESS, TripStatus.CANCELLED],
            TripStatus.IN_PROGRESS: [TripStatus.COMPLETED, TripStatus.CANCELLED],
            TripStatus.COMPLETED: [TripStatus.BILLED],
            TripStatus.BILLED: [],  # Final state
            TripStatus.CANCELLED: []  # Final state
        }
        
        return new_status in valid_transitions.get(self.status, [])
    
    def get_status_display_with_time(self):
        """Get status with last change time."""
        return f"{self.get_status_display()} (since {self.last_status_change.strftime('%m/%d/%Y %H:%M')})"

    def __str__(self):
        return f"Trip {self.trip_number} - {self.type} ({self.get_status_display()})"


class TripLine(BaseModel):
    """Individual flight leg within a trip."""
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE, related_name="trip_lines")
    
    # Airports and FBOs
    origin_airport = models.ForeignKey('airports.Airport', on_delete=models.CASCADE, related_name="origin_trip_lines")
    destination_airport = models.ForeignKey('airports.Airport', on_delete=models.CASCADE, related_name="destination_trip_lines")
    departure_fbo = models.ForeignKey('contacts.FBO', on_delete=models.SET_NULL, null=True, blank=True, related_name="departure_trip_lines")
    arrival_fbo = models.ForeignKey('contacts.FBO', on_delete=models.SET_NULL, null=True, blank=True, related_name="arrival_trip_lines")
    
    # Crew
    crew_line = models.ForeignKey(CrewLine, on_delete=models.SET_NULL, null=True, blank=True, related_name="trip_lines")
    
    # Timing (both local and UTC for proper timezone handling)
    departure_time_local = models.DateTimeField()
    departure_time_utc = models.DateTimeField()
    arrival_time_local = models.DateTimeField()
    arrival_time_utc = models.DateTimeField()
    
    # Flight details
    distance = models.DecimalField(max_digits=10, decimal_places=2)
    flight_time = models.DurationField()
    ground_time = models.DurationField()
    passenger_leg = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['departure_time_utc']
        indexes = [
            models.Index(fields=['trip', 'departure_time_utc']),
            models.Index(fields=['origin_airport', 'destination_airport']),
        ]
    
    def __str__(self):
        return f"Trip Line: {self.origin_airport} to {self.destination_airport}"


class TripEvent(BaseModel):
    """Non-flight timeline items attached to a Trip."""
    
    EVENT_TYPES = [
        ("CREW_CHANGE", "Crew Change"),
        ("OVERNIGHT", "Overnight (New Day)"),
    ]
    
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE, related_name="events")
    airport = models.ForeignKey('airports.Airport', on_delete=models.PROTECT, related_name="trip_events")
    event_type = models.CharField(max_length=20, choices=EVENT_TYPES)
    
    # Start/end timestamps (UTC + local) for proper timezone handling
    start_time_local = models.DateTimeField()
    start_time_utc = models.DateTimeField()
    end_time_local = models.DateTimeField(blank=True, null=True)  # required for OVERNIGHT
    end_time_utc = models.DateTimeField(blank=True, null=True)
    
    # Only used for CREW_CHANGE
    crew_line = models.ForeignKey(CrewLine, on_delete=models.SET_NULL, null=True, blank=True, related_name="trip_events")
    notes = models.TextField(blank=True, null=True)
    
    class Meta:
        indexes = [
            models.Index(fields=["trip", "start_time_utc"]),
            models.Index(fields=["event_type"]),
        ]
    
    def __str__(self):
        return f"{self.event_type} at {self.airport} - {self.start_time_local}"

```


# File: operations/serializers.py

```python
from rest_framework import serializers
from .models import Quote, Patient, Passenger, CrewLine, Trip, TripLine, TripEvent


class QuoteSerializer(serializers.ModelSerializer):
    """Serializer for Quote model with nested relationships."""
    
    contact_name = serializers.CharField(source='contact.business_name', read_only=True)
    pickup_airport_name = serializers.CharField(source='pickup_airport.name', read_only=True)
    dropoff_airport_name = serializers.CharField(source='dropoff_airport.name', read_only=True)
    patient_name = serializers.CharField(source='patient.info.first_name', read_only=True)
    
    class Meta:
        model = Quote
        fields = [
            'id', 'quoted_amount', 'contact', 'contact_name',
            'pickup_airport', 'pickup_airport_name',
            'dropoff_airport', 'dropoff_airport_name',
            'aircraft_type', 'estimated_flight_time', 'medical_team',
            'status', 'payment_status', 'inquiry_date',
            'patient', 'patient_name', 'includes_grounds',
            'number_of_stops', 'quote_pdf_status', 'quote_pdf_email',
            'cruise_doctor_first_name', 'cruise_doctor_last_name',
            'cruise_line', 'cruise_ship', 'created_on', 'modified_on'
        ]
        read_only_fields = ['id', 'created_on', 'modified_on']
    
    def validate_aircraft_type(self, value):
        """Validate aircraft type selection."""
        valid_types = ['65', '35', 'TBD']
        if value not in valid_types:
            raise serializers.ValidationError(f"Aircraft type must be one of: {valid_types}")
        return value
    
    def validate_medical_team(self, value):
        """Validate medical team configuration."""
        valid_teams = ['RN/RN', 'RN/Paramedic', 'RN/MD', 'RN/RT', 'standard', 'full']
        if value not in valid_teams:
            raise serializers.ValidationError(f"Medical team must be one of: {valid_teams}")
        return value


class PatientSerializer(serializers.ModelSerializer):
    """Serializer for Patient model with contact information."""
    
    contact_name = serializers.CharField(source='info.first_name', read_only=True)
    contact_email = serializers.EmailField(source='info.email', read_only=True)
    
    class Meta:
        model = Patient
        fields = [
            'id', 'info', 'contact_name', 'contact_email',
            'bed_at_origin', 'bed_at_destination', 'date_of_birth',
            'nationality', 'passport_number', 'passport_expiration_date',
            'special_instructions', 'status', 'passport_document',
            'letter_of_medical_necessity', 'created_on', 'modified_on'
        ]
        read_only_fields = ['id', 'created_on', 'modified_on']
    
    def validate_passport_expiration_date(self, value):
        """Validate passport is not expired."""
        from django.utils import timezone
        if value <= timezone.now().date():
            raise serializers.ValidationError("Passport expiration date must be in the future")
        return value


class PassengerSerializer(serializers.ModelSerializer):
    """Serializer for Passenger model."""
    
    contact_name = serializers.CharField(source='info.first_name', read_only=True)
    contact_email = serializers.EmailField(source='info.email', read_only=True)
    
    class Meta:
        model = Passenger
        fields = [
            'id', 'info', 'contact_name', 'contact_email',
            'date_of_birth', 'nationality', 'passport_number',
            'passport_expiration_date', 'contact_number', 'notes',
            'passport_document', 'created_on', 'modified_on'
        ]
        read_only_fields = ['id', 'created_on', 'modified_on']


class CrewLineSerializer(serializers.ModelSerializer):
    """Serializer for CrewLine model with crew member details."""
    
    primary_name = serializers.CharField(source='primary_in_command.first_name', read_only=True)
    secondary_name = serializers.CharField(source='secondary_in_command.first_name', read_only=True)
    medic_names = serializers.SerializerMethodField()
    
    class Meta:
        model = CrewLine
        fields = [
            'id', 'primary_in_command', 'primary_name',
            'secondary_in_command', 'secondary_name',
            'medic_ids', 'medic_names', 'created_on', 'modified_on'
        ]
        read_only_fields = ['id', 'created_on', 'modified_on']
    
    def get_medic_names(self, obj):
        """Get names of all medics assigned to this crew line."""
        return [f"{medic.first_name} {medic.last_name}" for medic in obj.medic_ids.all()]
    
    def validate(self, data):
        """Validate crew line data."""
        if data.get('primary_in_command') == data.get('secondary_in_command'):
            raise serializers.ValidationError(
                "Primary and secondary pilots must be different people"
            )
        return data


class TripLineSerializer(serializers.ModelSerializer):
    """Serializer for TripLine model with airport and crew details."""
    
    origin_airport_name = serializers.CharField(source='origin_airport.name', read_only=True)
    destination_airport_name = serializers.CharField(source='destination_airport.name', read_only=True)
    departure_fbo_name = serializers.CharField(source='departure_fbo.name', read_only=True)
    arrival_fbo_name = serializers.CharField(source='arrival_fbo.name', read_only=True)
    
    class Meta:
        model = TripLine
        fields = [
            'id', 'trip', 'origin_airport', 'origin_airport_name',
            'destination_airport', 'destination_airport_name',
            'departure_fbo', 'departure_fbo_name',
            'arrival_fbo', 'arrival_fbo_name',
            'crew_line', 'departure_time_local', 'departure_time_utc',
            'arrival_time_local', 'arrival_time_utc',
            'distance', 'flight_time', 'ground_time', 'passenger_leg',
            'created_on', 'modified_on'
        ]
        read_only_fields = ['id', 'created_on', 'modified_on']
    
    def validate(self, data):
        """Validate trip line timing."""
        departure_utc = data.get('departure_time_utc')
        arrival_utc = data.get('arrival_time_utc')
        
        if departure_utc and arrival_utc and departure_utc >= arrival_utc:
            raise serializers.ValidationError(
                "Departure time must be before arrival time"
            )
        
        return data


class TripEventSerializer(serializers.ModelSerializer):
    """Serializer for TripEvent model."""
    
    airport_name = serializers.CharField(source='airport.name', read_only=True)
    
    class Meta:
        model = TripEvent
        fields = [
            'id', 'trip', 'airport', 'airport_name', 'event_type',
            'start_time_local', 'start_time_utc',
            'end_time_local', 'end_time_utc',
            'crew_line', 'notes', 'created_on', 'modified_on'
        ]
        read_only_fields = ['id', 'created_on', 'modified_on']
    
    def validate(self, data):
        """Validate trip event data."""
        event_type = data.get('event_type')
        end_time_utc = data.get('end_time_utc')
        
        # OVERNIGHT events must have end time
        if event_type == 'OVERNIGHT' and not end_time_utc:
            raise serializers.ValidationError(
                "Overnight events must have an end time"
            )
        
        # CREW_CHANGE events must have crew_line
        if event_type == 'CREW_CHANGE' and not data.get('crew_line'):
            raise serializers.ValidationError(
                "Crew change events must specify the new crew line"
            )
        
        return data


class TripSerializer(serializers.ModelSerializer):
    """Serializer for Trip model with nested relationships."""
    
    trip_lines = TripLineSerializer(many=True, read_only=True)
    events = TripEventSerializer(many=True, read_only=True)
    aircraft_tail_number = serializers.CharField(source='aircraft.tail_number', read_only=True)
    quote_amount = serializers.DecimalField(source='quote.quoted_amount', max_digits=10, decimal_places=2, read_only=True)
    patient_name = serializers.CharField(source='patient.info.first_name', read_only=True)
    
    class Meta:
        model = Trip
        fields = [
            'id', 'trip_number', 'type', 'quote', 'quote_amount',
            'patient', 'patient_name', 'aircraft', 'aircraft_tail_number',
            'estimated_departure_time', 'pre_flight_duty_time',
            'post_flight_duty_time', 'internal_itinerary',
            'customer_itinerary', 'passengers', 'notes',
            'email_chain', 'status', 'trip_lines', 'events',
            'created_on', 'modified_on'
        ]
        read_only_fields = ['id', 'created_on', 'modified_on']
    
    def validate_trip_number(self, value):
        """Validate trip number uniqueness."""
        if self.instance and self.instance.trip_number == value:
            return value  # No change, skip validation
        
        if Trip.objects.filter(trip_number=value).exists():
            raise serializers.ValidationError("Trip number must be unique")
        
        return value
    
    def validate(self, data):
        """Validate trip data based on type."""
        trip_type = data.get('type')
        patient = data.get('patient')
        
        # Medical trips must have a patient
        if trip_type == 'medical' and not patient:
            raise serializers.ValidationError(
                "Medical trips must have an associated patient"
            )
        
        return data


class TripTimelineSerializer(serializers.Serializer):
    """Serializer for trip timeline view."""
    
    type = serializers.CharField()
    time_utc = serializers.DateTimeField()
    time_local = serializers.DateTimeField()
    event = serializers.CharField()
    location = serializers.CharField()
    details = serializers.JSONField()

```


# File: operations/pricing.py

```python
from decimal import Decimal
from datetime import datetime, time
from enum import Enum
from typing import Dict, Any, Optional
from dataclasses import dataclass


class PricingTier(Enum):
    """Pricing tiers for different service levels."""
    STANDARD = "standard"
    URGENT = "urgent"
    MEDICAL_COMPLEX = "medical_complex"
    VIP = "vip"


class TimeOfDay(Enum):
    """Time of day categories for pricing."""
    DAY = "day"  # 6 AM - 6 PM
    NIGHT = "night"  # 6 PM - 6 AM
    WEEKEND = "weekend"


@dataclass
class PricingFactors:
    """Factors that influence pricing calculations."""
    base_rate_per_mile: Decimal
    urgency_multiplier: Decimal = Decimal('1.0')
    time_multiplier: Decimal = Decimal('1.0')
    medical_complexity_multiplier: Decimal = Decimal('1.0')
    aircraft_type_multiplier: Decimal = Decimal('1.0')
    passenger_count_multiplier: Decimal = Decimal('1.0')
    fuel_surcharge: Decimal = Decimal('0.0')
    landing_fees: Decimal = Decimal('0.0')
    crew_overtime: Decimal = Decimal('0.0')
    minimum_charge: Decimal = Decimal('5000.0')


class PricingEngine:
    """Advanced pricing engine with tiered pricing logic."""
    
    # Base rates per mile by aircraft type
    BASE_RATES = {
        'Citation CJ3': Decimal('8.50'),
        'King Air 350': Decimal('6.75'),
        'Gulfstream G650': Decimal('15.00'),
        'Learjet 75': Decimal('7.25'),
        'Challenger 350': Decimal('9.50'),
    }
    
    # Pricing multipliers
    URGENCY_MULTIPLIERS = {
        PricingTier.STANDARD: Decimal('1.0'),
        PricingTier.URGENT: Decimal('1.5'),
        PricingTier.MEDICAL_COMPLEX: Decimal('1.8'),
        PricingTier.VIP: Decimal('2.0'),
    }
    
    TIME_MULTIPLIERS = {
        TimeOfDay.DAY: Decimal('1.0'),
        TimeOfDay.NIGHT: Decimal('1.25'),
        TimeOfDay.WEEKEND: Decimal('1.15'),
    }
    
    # Medical complexity factors
    MEDICAL_MULTIPLIERS = {
        'standard': Decimal('1.0'),
        'oxygen_required': Decimal('1.2'),
        'stretcher_required': Decimal('1.4'),
        'icu_transport': Decimal('1.8'),
        'organ_transport': Decimal('2.2'),
    }
    
    def __init__(self):
        self.fuel_price_per_gallon = Decimal('5.50')  # Current fuel price
    
    def calculate_quote_price(self, 
                            distance_miles: float,
                            aircraft_type: str,
                            departure_time: datetime,
                            passenger_count: int = 1,
                            pricing_tier: PricingTier = PricingTier.STANDARD,
                            medical_requirements: Optional[Dict[str, Any]] = None,
                            additional_services: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Calculate comprehensive quote pricing with all factors.
        
        Returns detailed pricing breakdown.
        """
        
        # Get base rate
        base_rate = self.BASE_RATES.get(aircraft_type, Decimal('10.00'))
        
        # Initialize pricing factors
        factors = PricingFactors(
            base_rate_per_mile=base_rate,
            urgency_multiplier=self.URGENCY_MULTIPLIERS.get(pricing_tier, Decimal('1.0')),
            time_multiplier=self._get_time_multiplier(departure_time),
            medical_complexity_multiplier=self._get_medical_multiplier(medical_requirements),
            aircraft_type_multiplier=Decimal('1.0'),  # Already in base rate
            passenger_count_multiplier=self._get_passenger_multiplier(passenger_count)
        )
        
        # Calculate base flight cost
        base_flight_cost = Decimal(str(distance_miles)) * factors.base_rate_per_mile
        
        # Apply multipliers
        adjusted_cost = base_flight_cost
        adjusted_cost *= factors.urgency_multiplier
        adjusted_cost *= factors.time_multiplier
        adjusted_cost *= factors.medical_complexity_multiplier
        adjusted_cost *= factors.passenger_count_multiplier
        
        # Calculate additional costs
        fuel_surcharge = self._calculate_fuel_surcharge(distance_miles, aircraft_type)
        landing_fees = self._calculate_landing_fees(additional_services)
        crew_costs = self._calculate_crew_costs(departure_time, pricing_tier)
        
        # Total before minimum
        subtotal = adjusted_cost + fuel_surcharge + landing_fees + crew_costs
        
        # Apply minimum charge
        final_total = max(subtotal, factors.minimum_charge)
        
        return {
            'base_flight_cost': base_flight_cost,
            'distance_miles': Decimal(str(distance_miles)),
            'base_rate_per_mile': factors.base_rate_per_mile,
            'multipliers': {
                'urgency': factors.urgency_multiplier,
                'time_of_day': factors.time_multiplier,
                'medical_complexity': factors.medical_complexity_multiplier,
                'passenger_count': factors.passenger_count_multiplier,
            },
            'additional_costs': {
                'fuel_surcharge': fuel_surcharge,
                'landing_fees': landing_fees,
                'crew_costs': crew_costs,
            },
            'subtotal': subtotal,
            'minimum_charge': factors.minimum_charge,
            'final_total': final_total,
            'pricing_tier': pricing_tier.value,
            'breakdown_notes': self._generate_pricing_notes(factors, pricing_tier)
        }
    
    def _get_time_multiplier(self, departure_time: datetime) -> Decimal:
        """Calculate time-based pricing multiplier."""
        hour = departure_time.hour
        weekday = departure_time.weekday()
        
        # Weekend pricing (Saturday = 5, Sunday = 6)
        if weekday >= 5:
            return self.TIME_MULTIPLIERS[TimeOfDay.WEEKEND]
        
        # Night pricing (6 PM to 6 AM)
        if hour >= 18 or hour < 6:
            return self.TIME_MULTIPLIERS[TimeOfDay.NIGHT]
        
        # Day pricing
        return self.TIME_MULTIPLIERS[TimeOfDay.DAY]
    
    def _get_medical_multiplier(self, medical_requirements: Optional[Dict[str, Any]]) -> Decimal:
        """Calculate medical complexity multiplier."""
        if not medical_requirements:
            return Decimal('1.0')
        
        multiplier = Decimal('1.0')
        
        if medical_requirements.get('oxygen_required'):
            multiplier *= self.MEDICAL_MULTIPLIERS['oxygen_required']
        
        if medical_requirements.get('stretcher_required'):
            multiplier *= self.MEDICAL_MULTIPLIERS['stretcher_required']
        
        if medical_requirements.get('icu_level_care'):
            multiplier *= self.MEDICAL_MULTIPLIERS['icu_transport']
        
        if medical_requirements.get('organ_transport'):
            multiplier *= self.MEDICAL_MULTIPLIERS['organ_transport']
        
        return multiplier
    
    def _get_passenger_multiplier(self, passenger_count: int) -> Decimal:
        """Calculate passenger count multiplier."""
        if passenger_count <= 4:
            return Decimal('1.0')
        elif passenger_count <= 8:
            return Decimal('1.1')
        else:
            return Decimal('1.2')
    
    def _calculate_fuel_surcharge(self, distance_miles: float, aircraft_type: str) -> Decimal:
        """Calculate fuel surcharge based on distance and aircraft type."""
        # Estimated fuel consumption per mile by aircraft type
        fuel_consumption_rates = {
            'Citation CJ3': 0.8,  # gallons per mile
            'King Air 350': 0.6,
            'Gulfstream G650': 1.2,
            'Learjet 75': 0.7,
            'Challenger 350': 0.9,
        }
        
        consumption_rate = fuel_consumption_rates.get(aircraft_type, 0.8)
        fuel_needed = Decimal(str(distance_miles * consumption_rate))
        
        return fuel_needed * self.fuel_price_per_gallon
    
    def _calculate_landing_fees(self, additional_services: Optional[Dict[str, Any]]) -> Decimal:
        """Calculate landing and service fees."""
        if not additional_services:
            return Decimal('500.0')  # Standard landing fees
        
        fees = Decimal('500.0')
        
        if additional_services.get('ground_transportation'):
            fees += Decimal('300.0')
        
        if additional_services.get('catering'):
            fees += Decimal('200.0')
        
        if additional_services.get('customs_handling'):
            fees += Decimal('400.0')
        
        return fees
    
    def _calculate_crew_costs(self, departure_time: datetime, pricing_tier: PricingTier) -> Decimal:
        """Calculate crew-related costs."""
        base_crew_cost = Decimal('800.0')
        
        # Night and weekend crew premiums
        hour = departure_time.hour
        weekday = departure_time.weekday()
        
        if weekday >= 5:  # Weekend
            base_crew_cost *= Decimal('1.2')
        elif hour >= 18 or hour < 6:  # Night
            base_crew_cost *= Decimal('1.15')
        
        # Urgent flights may require overtime
        if pricing_tier in [PricingTier.URGENT, PricingTier.MEDICAL_COMPLEX]:
            base_crew_cost *= Decimal('1.3')
        
        return base_crew_cost
    
    def _generate_pricing_notes(self, factors: PricingFactors, pricing_tier: PricingTier) -> list:
        """Generate human-readable pricing breakdown notes."""
        notes = []
        
        if factors.urgency_multiplier > Decimal('1.0'):
            notes.append(f"Urgency surcharge: {(factors.urgency_multiplier - 1) * 100:.0f}%")
        
        if factors.time_multiplier > Decimal('1.0'):
            notes.append(f"Time premium: {(factors.time_multiplier - 1) * 100:.0f}%")
        
        if factors.medical_complexity_multiplier > Decimal('1.0'):
            notes.append(f"Medical complexity: {(factors.medical_complexity_multiplier - 1) * 100:.0f}%")
        
        if factors.passenger_count_multiplier > Decimal('1.0'):
            notes.append(f"Passenger surcharge: {(factors.passenger_count_multiplier - 1) * 100:.0f}%")
        
        return notes
    
    def get_pricing_estimate_ranges(self, distance_miles: float, aircraft_type: str) -> Dict[str, Decimal]:
        """Get pricing ranges for different tiers."""
        base_time = datetime.now().replace(hour=12)  # Noon for standard pricing
        
        estimates = {}
        for tier in PricingTier:
            pricing = self.calculate_quote_price(
                distance_miles=distance_miles,
                aircraft_type=aircraft_type,
                departure_time=base_time,
                pricing_tier=tier
            )
            estimates[tier.value] = pricing['final_total']
        
        return estimates

```


# File: operations/views.py

```python
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db import transaction
from django.utils import timezone

from .models import Quote, Patient, Passenger, CrewLine, Trip, TripLine, TripEvent
from .serializers import (
    QuoteSerializer, PatientSerializer, PassengerSerializer,
    CrewLineSerializer, TripSerializer, TripLineSerializer,
    TripEventSerializer, TripTimelineSerializer
)
from .services.trip_service import TripService, CrewService
from .services.quote_service import QuoteService, PatientService


class QuoteViewSet(viewsets.ModelViewSet):
    """ViewSet for Quote operations."""
    
    queryset = Quote.objects.all()
    serializer_class = QuoteSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """Filter quotes based on user permissions and query parameters."""
        queryset = super().get_queryset()
        
        # Filter by status
        status_filter = self.request.query_params.get('status')
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        
        # Filter by payment status
        payment_status = self.request.query_params.get('payment_status')
        if payment_status:
            queryset = queryset.filter(payment_status=payment_status)
        
        # Filter by date range
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')
        if start_date:
            queryset = queryset.filter(inquiry_date__gte=start_date)
        if end_date:
            queryset = queryset.filter(inquiry_date__lte=end_date)
        
        return queryset.select_related('contact', 'pickup_airport', 'dropoff_airport', 'patient')
    
    def perform_create(self, serializer):
        """Create quote using service layer."""
        quote_data = serializer.validated_data
        
        # Use service to create quote with business logic
        quote = QuoteService.create_quote(
            contact_id=quote_data['contact'].id,
            pickup_airport_id=quote_data['pickup_airport'].id,
            dropoff_airport_id=quote_data['dropoff_airport'].id,
            aircraft_type=quote_data['aircraft_type'],
            medical_team=quote_data['medical_team'],
            estimated_flight_time=quote_data['estimated_flight_time'],
            **{k: v for k, v in quote_data.items() if k not in [
                'contact', 'pickup_airport', 'dropoff_airport'
            ]}
        )
        
        serializer.instance = quote
    
    @action(detail=True, methods=['post'])
    def update_status(self, request, pk=None):
        """Update quote status with validation."""
        quote = self.get_object()
        new_status = request.data.get('status')
        
        if not new_status:
            return Response(
                {'error': 'Status is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            updated_quote = QuoteService.update_quote_status(
                quote, new_status, request.user
            )
            serializer = self.get_serializer(updated_quote)
            return Response(serializer.data)
        except ValueError as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
    
    @action(detail=True, methods=['post'])
    def generate_pdf(self, request, pk=None):
        """Generate PDF document for quote."""
        quote = self.get_object()
        
        try:
            document_id = QuoteService.generate_quote_pdf(quote)
            return Response({
                'document_id': document_id,
                'message': 'PDF generated successfully'
            })
        except Exception as e:
            return Response(
                {'error': f'Failed to generate PDF: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @action(detail=True, methods=['get'])
    def payment_schedule(self, request, pk=None):
        """Get payment schedule for quote."""
        quote = self.get_object()
        schedule = QuoteService.calculate_payment_schedule(quote)
        return Response(schedule)


class PatientViewSet(viewsets.ModelViewSet):
    """ViewSet for Patient operations."""
    
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """Filter patients based on query parameters."""
        queryset = super().get_queryset()
        
        # Filter by status
        status_filter = self.request.query_params.get('status')
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        
        return queryset.select_related('info')
    
    @action(detail=True, methods=['post'])
    def update_status(self, request, pk=None):
        """Update patient status with validation."""
        patient = self.get_object()
        new_status = request.data.get('status')
        
        if not new_status:
            return Response(
                {'error': 'Status is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            updated_patient = PatientService.update_patient_status(
                patient, new_status, request.user
            )
            serializer = self.get_serializer(updated_patient)
            return Response(serializer.data)
        except ValueError as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
    
    @action(detail=True, methods=['get'])
    def validate_documents(self, request, pk=None):
        """Validate patient medical documents."""
        patient = self.get_object()
        validation_results = PatientService.validate_medical_documents(patient)
        return Response(validation_results)


class PassengerViewSet(viewsets.ModelViewSet):
    """ViewSet for Passenger operations."""
    
    queryset = Passenger.objects.all()
    serializer_class = PassengerSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """Get passengers with related contact information."""
        return super().get_queryset().select_related('info')


class CrewLineViewSet(viewsets.ModelViewSet):
    """ViewSet for CrewLine operations."""
    
    queryset = CrewLine.objects.all()
    serializer_class = CrewLineSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """Get crew lines with related contact information."""
        return super().get_queryset().select_related(
            'primary_in_command', 'secondary_in_command'
        ).prefetch_related('medic_ids')
    
    def perform_create(self, serializer):
        """Create crew line using service layer."""
        crew_data = serializer.validated_data
        
        try:
            crew_line = CrewService.create_crew_line(
                primary_pic_id=crew_data['primary_in_command'].id,
                secondary_sic_id=crew_data['secondary_in_command'].id,
                medic_ids=[medic.id for medic in crew_data.get('medic_ids', [])]
            )
            serializer.instance = crew_line
        except ValueError as e:
            raise serializers.ValidationError(str(e))
    
    @action(detail=True, methods=['post'])
    def check_availability(self, request, pk=None):
        """Check crew availability for given time period."""
        crew_line = self.get_object()
        start_time = request.data.get('start_time')
        end_time = request.data.get('end_time')
        
        if not start_time or not end_time:
            return Response(
                {'error': 'start_time and end_time are required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            start_datetime = timezone.datetime.fromisoformat(start_time.replace('Z', '+00:00'))
            end_datetime = timezone.datetime.fromisoformat(end_time.replace('Z', '+00:00'))
            
            availability = CrewService.validate_crew_availability(
                crew_line, start_datetime, end_datetime
            )
            return Response(availability)
        except ValueError as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )


class TripViewSet(viewsets.ModelViewSet):
    """ViewSet for Trip operations."""
    
    queryset = Trip.objects.all()
    serializer_class = TripSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """Get trips with related information."""
        queryset = super().get_queryset()
        
        # Filter by type
        trip_type = self.request.query_params.get('type')
        if trip_type:
            queryset = queryset.filter(type=trip_type)
        
        # Filter by status
        status_filter = self.request.query_params.get('status')
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        
        # Filter by date range
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')
        if start_date:
            queryset = queryset.filter(estimated_departure_time__gte=start_date)
        if end_date:
            queryset = queryset.filter(estimated_departure_time__lte=end_date)
        
        return queryset.select_related(
            'quote', 'patient', 'aircraft'
        ).prefetch_related('trip_lines', 'events', 'passengers')
    
    def perform_create(self, serializer):
        """Create trip using service layer."""
        trip_data = serializer.validated_data
        
        try:
            trip = TripService.create_trip(
                trip_number=trip_data.get('trip_number', ''),
                trip_type=trip_data['type'],
                aircraft_id=trip_data.get('aircraft').id if trip_data.get('aircraft') else None,
                quote_id=trip_data.get('quote').id if trip_data.get('quote') else None,
                patient_id=trip_data.get('patient').id if trip_data.get('patient') else None,
                **{k: v for k, v in trip_data.items() if k not in [
                    'type', 'aircraft', 'quote', 'patient'
                ]}
            )
            serializer.instance = trip
        except ValueError as e:
            raise serializers.ValidationError(str(e))
    
    @action(detail=True, methods=['post'])
    def add_trip_line(self, request, pk=None):
        """Add a flight leg to the trip."""
        trip = self.get_object()
        
        required_fields = [
            'origin_airport_id', 'destination_airport_id',
            'departure_time_local', 'arrival_time_local'
        ]
        
        for field in required_fields:
            if field not in request.data:
                return Response(
                    {'error': f'{field} is required'},
                    status=status.HTTP_400_BAD_REQUEST
                )
        
        try:
            trip_line = TripService.add_trip_line(
                trip=trip,
                origin_airport_id=request.data['origin_airport_id'],
                destination_airport_id=request.data['destination_airport_id'],
                departure_time_local=timezone.datetime.fromisoformat(
                    request.data['departure_time_local'].replace('Z', '+00:00')
                ),
                arrival_time_local=timezone.datetime.fromisoformat(
                    request.data['arrival_time_local'].replace('Z', '+00:00')
                ),
                crew_line_id=request.data.get('crew_line_id'),
                **{k: v for k, v in request.data.items() if k not in required_fields + ['crew_line_id']}
            )
            
            serializer = TripLineSerializer(trip_line)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
    
    @action(detail=True, methods=['post'])
    def add_crew_change(self, request, pk=None):
        """Add a crew change event to the trip."""
        trip = self.get_object()
        
        required_fields = ['airport_id', 'new_crew_line_id', 'event_time_local']
        
        for field in required_fields:
            if field not in request.data:
                return Response(
                    {'error': f'{field} is required'},
                    status=status.HTTP_400_BAD_REQUEST
                )
        
        try:
            event = TripService.add_crew_change_event(
                trip=trip,
                airport_id=request.data['airport_id'],
                new_crew_line_id=request.data['new_crew_line_id'],
                event_time_local=timezone.datetime.fromisoformat(
                    request.data['event_time_local'].replace('Z', '+00:00')
                ),
                notes=request.data.get('notes')
            )
            
            serializer = TripEventSerializer(event)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
    
    @action(detail=True, methods=['get'])
    def timeline(self, request, pk=None):
        """Get chronological timeline of trip events."""
        trip = self.get_object()
        timeline = TripService.get_trip_timeline(trip)
        serializer = TripTimelineSerializer(timeline, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def duration(self, request, pk=None):
        """Get total trip duration."""
        trip = self.get_object()
        duration = TripService.calculate_trip_duration(trip)
        
        if duration:
            return Response({
                'total_duration_seconds': duration.total_seconds(),
                'total_duration_hours': duration.total_seconds() / 3600
            })
        else:
            return Response({
                'total_duration_seconds': None,
                'total_duration_hours': None,
                'message': 'No trip lines found'
            })


class TripLineViewSet(viewsets.ModelViewSet):
    """ViewSet for TripLine operations."""
    
    queryset = TripLine.objects.all()
    serializer_class = TripLineSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """Get trip lines with related information."""
        queryset = super().get_queryset()
        
        # Filter by trip
        trip_id = self.request.query_params.get('trip_id')
        if trip_id:
            queryset = queryset.filter(trip_id=trip_id)
        
        return queryset.select_related(
            'trip', 'origin_airport', 'destination_airport',
            'departure_fbo', 'arrival_fbo', 'crew_line'
        )


class TripEventViewSet(viewsets.ModelViewSet):
    """ViewSet for TripEvent operations."""
    
    queryset = TripEvent.objects.all()
    serializer_class = TripEventSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """Get trip events with related information."""
        queryset = super().get_queryset()
        
        # Filter by trip
        trip_id = self.request.query_params.get('trip_id')
        if trip_id:
            queryset = queryset.filter(trip_id=trip_id)
        
        # Filter by event type
        event_type = self.request.query_params.get('event_type')
        if event_type:
            queryset = queryset.filter(event_type=event_type)
        
        return queryset.select_related('trip', 'airport', 'crew_line')

```


# File: operations/apps.py

```python
from django.apps import AppConfig


class OperationsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'operations'
    verbose_name = 'Flight Operations'

```


# File: operations/__init__.py

```python

```


# File: operations/urls.py

```python
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

```


# File: operations/admin.py

```python
from django.contrib import admin
from .models import Quote, Patient, Passenger, CrewLine, Trip, TripLine, TripEvent


@admin.register(Quote)
class QuoteAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'quoted_amount', 'contact', 'pickup_airport', 
        'dropoff_airport', 'status', 'payment_status', 'inquiry_date'
    ]
    list_filter = ['status', 'payment_status', 'aircraft_type', 'medical_team']
    search_fields = ['contact__business_name', 'contact__first_name', 'contact__last_name']
    readonly_fields = ['id', 'created_on', 'modified_on']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('contact', 'quoted_amount', 'status', 'payment_status')
        }),
        ('Flight Details', {
            'fields': (
                'pickup_airport', 'dropoff_airport', 'aircraft_type',
                'estimated_flight_time', 'medical_team', 'includes_grounds',
                'number_of_stops'
            )
        }),
        ('Cruise Information', {
            'fields': (
                'cruise_doctor_first_name', 'cruise_doctor_last_name',
                'cruise_line', 'cruise_ship'
            ),
            'classes': ('collapse',)
        }),
        ('Documents & Agreements', {
            'fields': (
                'quote_pdf', 'quote_pdf_status', 'quote_pdf_email',
                'payment_agreement', 'consent_for_transport',
                'patient_service_agreement'
            ),
            'classes': ('collapse',)
        }),
        ('Metadata', {
            'fields': ('id', 'created_on', 'modified_on'),
            'classes': ('collapse',)
        })
    )


@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'info', 'date_of_birth', 'nationality', 
        'passport_number', 'status'
    ]
    list_filter = ['status', 'nationality', 'bed_at_origin', 'bed_at_destination']
    search_fields = ['info__first_name', 'info__last_name', 'passport_number']
    readonly_fields = ['id', 'created_on', 'modified_on']
    
    fieldsets = (
        ('Patient Information', {
            'fields': ('info', 'date_of_birth', 'nationality', 'status')
        }),
        ('Medical Requirements', {
            'fields': ('bed_at_origin', 'bed_at_destination', 'special_instructions')
        }),
        ('Travel Documents', {
            'fields': (
                'passport_number', 'passport_expiration_date',
                'passport_document', 'letter_of_medical_necessity'
            )
        }),
        ('Metadata', {
            'fields': ('id', 'created_on', 'modified_on'),
            'classes': ('collapse',)
        })
    )


@admin.register(Passenger)
class PassengerAdmin(admin.ModelAdmin):
    list_display = ['id', 'info', 'date_of_birth', 'nationality', 'contact_number']
    search_fields = ['info__first_name', 'info__last_name', 'passport_number']
    readonly_fields = ['id', 'created_on', 'modified_on']


@admin.register(CrewLine)
class CrewLineAdmin(admin.ModelAdmin):
    list_display = ['id', 'primary_in_command', 'secondary_in_command']
    search_fields = [
        'primary_in_command__first_name', 'primary_in_command__last_name',
        'secondary_in_command__first_name', 'secondary_in_command__last_name'
    ]
    readonly_fields = ['id', 'created_on', 'modified_on']
    
    fieldsets = (
        ('Crew Assignment', {
            'fields': ('primary_in_command', 'secondary_in_command', 'medic_ids')
        }),
        ('Metadata', {
            'fields': ('id', 'created_on', 'modified_on'),
            'classes': ('collapse',)
        })
    )


@admin.register(Trip)
class TripAdmin(admin.ModelAdmin):
    list_display = [
        'trip_number', 'type', 'status', 'aircraft', 
        'estimated_departure_time', 'created_on'
    ]
    list_filter = ['type', 'status']
    search_fields = ['trip_number', 'notes']
    readonly_fields = ['id', 'created_on', 'modified_on']
    
    fieldsets = (
        ('Trip Information', {
            'fields': ('trip_number', 'type', 'status', 'notes')
        }),
        ('Related Entities', {
            'fields': ('quote', 'patient', 'aircraft', 'passengers')
        }),
        ('Timing', {
            'fields': (
                'estimated_departure_time', 'pre_flight_duty_time',
                'post_flight_duty_time'
            )
        }),
        ('Documents', {
            'fields': ('internal_itinerary', 'customer_itinerary'),
            'classes': ('collapse',)
        }),
        ('Communication', {
            'fields': ('email_chain',),
            'classes': ('collapse',)
        }),
        ('Metadata', {
            'fields': ('id', 'created_on', 'modified_on'),
            'classes': ('collapse',)
        })
    )


@admin.register(TripLine)
class TripLineAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'trip', 'origin_airport', 'destination_airport',
        'departure_time_local', 'arrival_time_local', 'passenger_leg'
    ]
    list_filter = ['passenger_leg', 'origin_airport', 'destination_airport']
    search_fields = ['trip__trip_number']
    readonly_fields = ['id', 'created_on', 'modified_on']
    
    fieldsets = (
        ('Flight Information', {
            'fields': (
                'trip', 'origin_airport', 'destination_airport',
                'departure_fbo', 'arrival_fbo', 'crew_line'
            )
        }),
        ('Timing', {
            'fields': (
                'departure_time_local', 'departure_time_utc',
                'arrival_time_local', 'arrival_time_utc'
            )
        }),
        ('Flight Details', {
            'fields': ('distance', 'flight_time', 'ground_time', 'passenger_leg')
        }),
        ('Metadata', {
            'fields': ('id', 'created_on', 'modified_on'),
            'classes': ('collapse',)
        })
    )


@admin.register(TripEvent)
class TripEventAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'trip', 'event_type', 'airport',
        'start_time_local', 'end_time_local'
    ]
    list_filter = ['event_type', 'airport']
    search_fields = ['trip__trip_number', 'notes']
    readonly_fields = ['id', 'created_on', 'modified_on']
    
    fieldsets = (
        ('Event Information', {
            'fields': ('trip', 'event_type', 'airport', 'crew_line')
        }),
        ('Timing', {
            'fields': (
                'start_time_local', 'start_time_utc',
                'end_time_local', 'end_time_utc'
            )
        }),
        ('Notes', {
            'fields': ('notes',)
        }),
        ('Metadata', {
            'fields': ('id', 'created_on', 'modified_on'),
            'classes': ('collapse',)
        })
    )

```


# File: operations/services/quote_service.py

```python
"""
Quote service module containing business logic for quote operations.
Extracted from models and views to follow clean architecture principles.
"""
from django.db import transaction
from django.core.exceptions import ValidationError
from django.utils import timezone
from decimal import Decimal
from typing import Dict, List, Optional, Any
from ..models import Quote, Trip, Patient, Passenger, TripStatus
from ..pricing import PricingEngine, PricingTier

from contacts.models import Contact
from airports.models import Airport


class QuoteService:
    """Service class for quote-related business logic."""
    
    def __init__(self):
        self.pricing_engine = PricingEngine()
    
    def create_quote(
        self,
        contact_id: str,
        origin_airport_id: str,
        destination_airport_id: str,
        departure_time: timezone.datetime,
        passenger_count: int = 1,
        aircraft_type: str = None,
        trip_type: str = 'charter',
        medical_requirements: Dict[str, Any] = None,
        pricing_tier: str = 'standard',
        additional_services: Dict[str, Any] = None,
        **kwargs
    ) -> Quote:
        """
        Create a new quote with automatic pricing calculation.
        
        Args:
            contact_id: Customer contact ID
            origin_airport_id: Origin airport ID
            destination_airport_id: Destination airport ID
            departure_time: Departure time
            passenger_count: Number of passengers
            aircraft_type: Type of aircraft requested
            trip_type: Type of trip (charter or medical)
            medical_requirements: Medical requirements for the trip
            pricing_tier: Pricing tier (standard, urgent, medical_complex, vip)
            additional_services: Additional services required
            **kwargs: Additional quote fields
            
        Returns:
            Created Quote instance
        """
        # Calculate distance using airports
        from airports.services.airport_service import AirportService
        airport_service = AirportService()
        distance_miles = airport_service.calculate_distance(
            origin_airport_id, destination_airport_id
        )
        
        # Determine pricing tier
        tier_mapping = {
            'standard': PricingTier.STANDARD,
            'urgent': PricingTier.URGENT,
            'medical_complex': PricingTier.MEDICAL_COMPLEX,
            'vip': PricingTier.VIP
        }
        pricing_tier_enum = tier_mapping.get(pricing_tier, PricingTier.STANDARD)
        
        # Use advanced pricing engine
        pricing_result = self.pricing_engine.calculate_quote_price(
            distance_miles=distance_miles,
            aircraft_type=aircraft_type or 'Citation CJ3',
            departure_time=departure_time,
            passenger_count=passenger_count,
            pricing_tier=pricing_tier_enum,
            medical_requirements=medical_requirements,
            additional_services=additional_services
        )
        
        quoted_amount = pricing_result['final_total']
        
        with transaction.atomic():
            quote = Quote.objects.create(
                contact_id=contact_id,
                origin_airport_id=origin_airport_id,
                destination_airport_id=destination_airport_id,
                departure_time=departure_time,
                passenger_count=passenger_count,
                aircraft_type=aircraft_type,
                trip_type=trip_type,
                medical_requirements=medical_requirements,
                pricing_tier=pricing_tier,
                additional_services=additional_services,
                quoted_amount=quoted_amount,
                pricing_breakdown=pricing_result,
                inquiry_date=timezone.now(),
                **kwargs
            )
            
            return quote
    
    def update_quote_status(self, quote: Quote, new_status: str, user=None) -> Quote:
        """
        Update quote status with proper validation and logging.
        
        Args:
            quote: Quote instance
            new_status: New status value
            user: User making the change
            
        Returns:
            Updated Quote instance
            
        Raises:
            ValueError: If status transition is invalid
        """
        valid_transitions = {
            'pending': ['active', 'cancelled'],
            'active': ['completed', 'cancelled'],
            'completed': [],  # Terminal state
            'cancelled': []   # Terminal state
        }
        
        if new_status not in valid_transitions.get(quote.status, []):
            raise ValueError(
                f"Invalid status transition from {quote.status} to {new_status}"
            )
        
        quote.status = new_status
        if user:
            quote.modified_by = user
        quote.save()
        
        return quote
    
    def update_quote_pricing(self, quote_id: str, **pricing_params) -> Quote:
        """
        Update quote pricing with new parameters.
        
        Args:
            quote_id: Quote ID
            **pricing_params: New pricing parameters
            
        Returns:
            Updated Quote instance
        """
        quote = Quote.objects.get(id=quote_id)
        
        # Recalculate pricing with updated parameters
        if any(param in pricing_params for param in ['departure_time', 'passenger_count', 'aircraft_type', 'pricing_tier']):
            # Get current quote data
            distance_miles = pricing_params.get('distance_miles', 500)  # Would get from airports
            aircraft_type = pricing_params.get('aircraft_type', quote.aircraft_type or 'Citation CJ3')
            departure_time = pricing_params.get('departure_time', quote.departure_time)
            passenger_count = pricing_params.get('passenger_count', quote.passenger_count)
            pricing_tier = pricing_params.get('pricing_tier', getattr(quote, 'pricing_tier', 'standard'))
            
            # Determine pricing tier
            tier_mapping = {
                'standard': PricingTier.STANDARD,
                'urgent': PricingTier.URGENT,
                'medical_complex': PricingTier.MEDICAL_COMPLEX,
                'vip': PricingTier.VIP
            }
            pricing_tier_enum = tier_mapping.get(pricing_tier, PricingTier.STANDARD)
            
            # Recalculate pricing
            pricing_result = self.pricing_engine.calculate_quote_price(
                distance_miles=distance_miles,
                aircraft_type=aircraft_type,
                departure_time=departure_time,
                passenger_count=passenger_count,
                pricing_tier=pricing_tier_enum,
                medical_requirements=pricing_params.get('medical_requirements', {}),
                additional_services=pricing_params.get('additional_services', {})
            )
            
            quote.quoted_amount = pricing_result['final_total']
            quote.pricing_breakdown = pricing_result
        elif 'quoted_amount' in pricing_params:
            quote.quoted_amount = Decimal(str(pricing_params['quoted_amount']))
        
        quote.save()
        
        return quote
    
    def get_pricing_estimates(self, origin_airport_id: str, destination_airport_id: str, aircraft_type: str = None) -> Dict[str, Decimal]:
        """
        Get pricing estimates for a trip.
        
        Args:
            origin_airport_id: Origin airport ID
            destination_airport_id: Destination airport ID
            aircraft_type: Type of aircraft
            
        Returns:
            Dictionary with pricing estimates
        """
        # Calculate distance using airports
        from airports.services.airport_service import AirportService
        airport_service = AirportService()
        distance_miles = airport_service.calculate_distance(
            origin_airport_id, destination_airport_id
        )
        
        # Get pricing estimates for all tiers
        estimates = self.pricing_engine.get_pricing_estimate_ranges(
            distance_miles=distance_miles,
            aircraft_type=aircraft_type or 'Citation CJ3'
        )
        
        return estimates
    
    def calculate_payment_schedule(self, quote: Quote) -> Dict[str, Decimal]:
        """
        Calculate payment schedule based on quote amount and type.
        
        Args:
            quote: Quote instance
            
        Returns:
            Dictionary with payment schedule
        """
        total_amount = quote.quoted_amount
        
        # Medical flights typically require 50% deposit
        if hasattr(quote, 'patient') and quote.patient:
            deposit_percentage = Decimal('0.50')
        else:
            # Charter flights require 25% deposit
            deposit_percentage = Decimal('0.25')
        
        deposit_amount = total_amount * deposit_percentage
        balance_amount = total_amount - deposit_amount
        
        return {
            'total_amount': total_amount,
            'deposit_amount': deposit_amount,
            'balance_amount': balance_amount,
            'deposit_percentage': deposit_percentage
        }
    
    def generate_quote_pdf(self, quote: Quote) -> str:
        """
        Generate PDF document for the quote.
        
        Args:
            quote: Quote instance
            
        Returns:
            Document ID of generated PDF
        """
        from documents.services.generation_service import DocumentGenerationService
        
        # Prepare quote data for PDF generation
        quote_data = {
            'quote_id': str(quote.id),
            'contact': quote.contact,
            'pickup_airport': quote.pickup_airport,
            'dropoff_airport': quote.dropoff_airport,
            'aircraft_type': quote.aircraft_type,
            'medical_team': quote.medical_team,
            'quoted_amount': quote.quoted_amount,
            'estimated_flight_time': quote.estimated_flight_time,
            'inquiry_date': quote.inquiry_date,
            'payment_schedule': QuoteService.calculate_payment_schedule(quote)
        }
        
        # Generate PDF using document service
        document_id = DocumentGenerationService.generate_quote_pdf(quote_data)
        
        # Update quote with generated PDF
        quote.quote_pdf_id = document_id
        quote.quote_pdf_status = 'created'
        quote.save()
        
        return document_id
    
    @staticmethod
    def _calculate_base_price(
        aircraft_type: str,
        flight_time: timedelta,
        medical_team: str
    ) -> Decimal:
        """
        Calculate base price based on aircraft and medical team.
        
        Args:
            aircraft_type: Type of aircraft
            flight_time: Flight duration
            medical_team: Medical team configuration
            
        Returns:
            Base price amount
        """
        # Base hourly rates by aircraft type
        aircraft_rates = {
            '65': Decimal('4500.00'),  # Learjet 65
            '35': Decimal('3500.00'),  # Learjet 35
            'TBD': Decimal('4000.00')  # Default rate
        }
        
        # Medical team surcharges
        medical_surcharges = {
            'RN/RN': Decimal('2000.00'),
            'RN/Paramedic': Decimal('2500.00'),
            'RN/MD': Decimal('5000.00'),
            'RN/RT': Decimal('3000.00'),
            'standard': Decimal('1000.00'),
            'full': Decimal('6000.00')
        }
        
        base_rate = aircraft_rates.get(aircraft_type, aircraft_rates['TBD'])
        medical_surcharge = medical_surcharges.get(medical_team, Decimal('0.00'))
        
        # Calculate flight hours (minimum 2 hours)
        flight_hours = max(flight_time.total_seconds() / 3600, 2)
        
        return (base_rate * Decimal(str(flight_hours))) + medical_surcharge
    
    @staticmethod
    def _calculate_distance_adjustment(
        pickup_airport_id: str,
        dropoff_airport_id: str
    ) -> Decimal:
        """
        Calculate price adjustment based on distance.
        
        Args:
            pickup_airport_id: Origin airport ID
            dropoff_airport_id: Destination airport ID
            
        Returns:
            Distance-based price adjustment
        """
        from airports.services.airport_service import AirportService
        
        pickup_airport = Airport.objects.get(id=pickup_airport_id)
        dropoff_airport = Airport.objects.get(id=dropoff_airport_id)
        
        distance = AirportService.calculate_distance(pickup_airport, dropoff_airport)
        
        # Long distance surcharge (over 1000 nautical miles)
        if distance > 1000:
            return Decimal('1000.00')
        
        # Short distance minimum charge (under 200 nautical miles)
        if distance < 200:
            return Decimal('500.00')
        
        return Decimal('0.00')


class PatientService:
    """Service class for patient-related business logic."""
    
    @staticmethod
    def create_patient_from_contact(
        contact_id: str,
        date_of_birth: datetime.date,
        nationality: str,
        passport_number: str,
        passport_expiration_date: datetime.date,
        **kwargs
    ) -> Patient:
        """
        Create a patient record from an existing contact.
        
        Args:
            contact_id: Contact ID
            date_of_birth: Patient's date of birth
            nationality: Patient's nationality
            passport_number: Passport number
            passport_expiration_date: Passport expiration date
            **kwargs: Additional patient fields
            
        Returns:
            Created Patient instance
            
        Raises:
            ValueError: If validation fails
        """
        # Validate contact exists
        contact = Contact.objects.get(id=contact_id)
        
        # Validate passport not expired
        if passport_expiration_date <= timezone.now().date():
            raise ValueError("Passport is expired")
        
        # Validate age (must be reasonable for medical transport)
        age = (timezone.now().date() - date_of_birth).days / 365.25
        if age < 0 or age > 120:
            raise ValueError("Invalid date of birth")
        
        return Patient.objects.create(
            info_id=contact_id,
            date_of_birth=date_of_birth,
            nationality=nationality,
            passport_number=passport_number,
            passport_expiration_date=passport_expiration_date,
            **kwargs
        )
    
    @staticmethod
    def validate_medical_documents(patient: Patient) -> Dict[str, bool]:
        """
        Validate that all required medical documents are present.
        
        Args:
            patient: Patient instance
            
        Returns:
            Dictionary with validation results
        """
        validation_results = {
            'passport_document': bool(patient.passport_document),
            'medical_necessity': bool(patient.letter_of_medical_necessity),
            'passport_valid': (
                patient.passport_expiration_date > timezone.now().date()
                if patient.passport_expiration_date else False
            )
        }
        
        validation_results['all_valid'] = all(validation_results.values())
        
        return validation_results
    
    @staticmethod
    def update_patient_status(patient: Patient, new_status: str, user=None) -> Patient:
        """
        Update patient status with proper validation.
        
        Args:
            patient: Patient instance
            new_status: New status value
            user: User making the change
            
        Returns:
            Updated Patient instance
            
        Raises:
            ValueError: If status transition is invalid
        """
        valid_transitions = {
            'pending': ['confirmed', 'cancelled'],
            'confirmed': ['active', 'cancelled'],
            'active': ['completed', 'cancelled'],
            'completed': [],  # Terminal state
            'cancelled': []   # Terminal state
        }
        
        if new_status not in valid_transitions.get(patient.status, []):
            raise ValueError(
                f"Invalid status transition from {patient.status} to {new_status}"
            )
        
        patient.status = new_status
        if user:
            patient.modified_by = user
        patient.save()
        
        return patient

```


# File: operations/services/trip_service.py

```python
"""
Trip service module containing business logic for trip operations.
Extracted from models and views to follow clean architecture principles.
"""
from django.db import transaction
from django.core.exceptions import ValidationError
from django.utils import timezone
from decimal import Decimal
from typing import Dict, List, Optional, Any
from ..models import Trip, Quote, Patient, Passenger, CrewLine, TripLine, TripEvent, TripStatus
from contacts.models import Contact
from airports.models import Airport
from aircraft.models import Aircraft


class TripService:
    """Service class for trip-related business logic."""
    
    @staticmethod
    def create_trip(
        trip_number: str,
        trip_type: str,
        quote_id: str = None,
        aircraft_id: str = None,
        initial_status: str = TripStatus.REQUESTED,
        **kwargs
    ) -> Trip:
        """
        Create a new trip with proper validation and business rules.
        
        Args:
            trip_number: Unique trip identifier
            trip_type: Type of trip (medical, charter, etc.)
            quote_id: Optional related quote
            aircraft_id: Optional aircraft assignment
            initial_status: Initial status of the trip
            **kwargs: Additional trip fields
            
        Returns:
            Created Trip instance
            
        Raises:
            ValueError: If business rules are violated
        """
        # Validate trip number uniqueness
        if Trip.objects.filter(trip_number=trip_number).exists():
            raise ValueError(f"Trip number {trip_number} already exists")
        
        # Validate medical trips have patients
        if trip_type == 'medical' and not kwargs.get('patient_id'):
            raise ValueError("Medical trips must have an associated patient")
        
        with transaction.atomic():
            trip = Trip.objects.create(
                trip_number=trip_number,
                type=trip_type,
                status=initial_status,
                quote_id=quote_id,
                aircraft_id=aircraft_id,
                **kwargs
            )
            
            # Initialize status history
            trip.update_status(initial_status, notes="Trip created")
            
            # Auto-generate trip number if not provided
            if not trip_number:
                trip.trip_number = TripService._generate_trip_number(trip.type)
                trip.save()
            
            return trip
    
    @staticmethod
    def add_trip_line(
        trip: Trip,
        origin_airport_id: str,
        destination_airport_id: str,
        departure_time_local: datetime,
        arrival_time_local: datetime,
        crew_line_id: Optional[str] = None,
        **kwargs
    ) -> TripLine:
        """
        Add a flight leg to a trip with proper timezone handling.
        
        Args:
            trip: Trip instance
            origin_airport_id: Origin airport ID
            destination_airport_id: Destination airport ID
            departure_time_local: Local departure time
            arrival_time_local: Local arrival time
            crew_line_id: Optional crew assignment
            **kwargs: Additional trip line fields
            
        Returns:
            Created TripLine instance
        """
        from airports.services.airport_service import AirportService
        
        # Get airports for timezone conversion
        origin_airport = Airport.objects.get(id=origin_airport_id)
        destination_airport = Airport.objects.get(id=destination_airport_id)
        
        # Convert local times to UTC
        departure_time_utc = AirportService.convert_to_utc(
            departure_time_local, origin_airport.timezone
        )
        arrival_time_utc = AirportService.convert_to_utc(
            arrival_time_local, destination_airport.timezone
        )
        
        # Calculate flight time and distance
        flight_time = arrival_time_utc - departure_time_utc
        distance = AirportService.calculate_distance(origin_airport, destination_airport)
        
        return TripLine.objects.create(
            trip=trip,
            origin_airport_id=origin_airport_id,
            destination_airport_id=destination_airport_id,
            departure_time_local=departure_time_local,
            departure_time_utc=departure_time_utc,
            arrival_time_local=arrival_time_local,
            arrival_time_utc=arrival_time_utc,
            flight_time=flight_time,
            distance=distance,
            crew_line_id=crew_line_id,
            **kwargs
        )
    
    @staticmethod
    def add_crew_change_event(
        trip: Trip,
        airport_id: str,
        new_crew_line_id: str,
        event_time_local: datetime,
        notes: Optional[str] = None
    ) -> TripEvent:
        """
        Add a crew change event to a trip.
        
        Args:
            trip: Trip instance
            airport_id: Airport where crew change occurs
            new_crew_line_id: New crew assignment
            event_time_local: Local time of crew change
            notes: Optional notes about the crew change
            
        Returns:
            Created TripEvent instance
        """
        from airports.services.airport_service import AirportService
        
        airport = Airport.objects.get(id=airport_id)
        event_time_utc = AirportService.convert_to_utc(
            event_time_local, airport.timezone
        )
        
        return TripEvent.objects.create(
            trip=trip,
            airport_id=airport_id,
            event_type='CREW_CHANGE',
            start_time_local=event_time_local,
            start_time_utc=event_time_utc,
            crew_line_id=new_crew_line_id,
            notes=notes
        )
    
    @staticmethod
    def calculate_trip_duration(trip: Trip) -> Optional[timedelta]:
        """
        Calculate total trip duration from first departure to last arrival.
        
        Args:
            trip: Trip instance
            
        Returns:
            Total trip duration or None if no trip lines
        """
        trip_lines = trip.trip_lines.order_by('departure_time_utc')
        
        if not trip_lines.exists():
            return None
        
        first_departure = trip_lines.first().departure_time_utc
        last_arrival = trip_lines.last().arrival_time_utc
        
        return last_arrival - first_departure
    
    @staticmethod
    def get_trip_timeline(trip: Trip) -> List[Dict[str, Any]]:
        """
        Get chronological timeline of all trip events and flight legs.
        
        Args:
            trip: Trip instance
            
        Returns:
            List of timeline events sorted by time
        """
        timeline = []
        
        # Add trip lines
        for trip_line in trip.trip_lines.all():
            timeline.append({
                'type': 'flight',
                'time_utc': trip_line.departure_time_utc,
                'time_local': trip_line.departure_time_local,
                'event': 'departure',
                'location': trip_line.origin_airport,
                'details': trip_line
            })
            timeline.append({
                'type': 'flight',
                'time_utc': trip_line.arrival_time_utc,
                'time_local': trip_line.arrival_time_local,
                'event': 'arrival',
                'location': trip_line.destination_airport,
                'details': trip_line
            })
        
        # Add trip events
        for event in trip.events.all():
            timeline.append({
                'type': 'event',
                'time_utc': event.start_time_utc,
                'time_local': event.start_time_local,
                'event': event.event_type.lower(),
                'location': event.airport,
                'details': event
            })
        
        # Sort by UTC time
        timeline.sort(key=lambda x: x['time_utc'])
        
        return timeline
    
    @staticmethod
    def get_trips_by_status(status: str) -> List[Trip]:
        """
        Get all trips with the given status.
        
        Args:
            status: Status to filter by
            
        Returns:
            List of Trip instances
        """
        # Validate status
        if status not in [choice[0] for choice in TripStatus.choices]:
            raise ValidationError(f"Invalid status: {status}")
        
        return Trip.objects.filter(status=status).order_by('-created_at')
    
    @staticmethod
    def update_trip_status(trip_id: str, new_status: str, user=None, notes: str = "") -> Trip:
        """
        Update the status of a trip.
        
        Args:
            trip_id: ID of the trip to update
            new_status: New status to set
            user: Optional user making the update
            notes: Optional notes about the status update
            
        Returns:
            Updated Trip instance
        """
        trip = Trip.objects.get(id=trip_id)
        trip.update_status(new_status, user=user, notes=notes)
        return trip
    
    @staticmethod
    def get_trip_status_summary() -> Dict[str, int]:
        """
        Get a summary of trip counts by status.
        
        Returns:
            Dictionary with status as key and count as value
        """
        # Get counts for all possible statuses
        status_counts = Trip.objects.values('status').annotate(
            count=Count('id')
        ).order_by('status')
        
        # Initialize with all possible statuses
        summary = {status[0]: 0 for status in TripStatus.choices}
        
        # Update with actual counts
        for item in status_counts:
            summary[item['status']] = item['count']
        
        return summary
    
    @staticmethod
    def _generate_trip_number(trip_type: str) -> str:
        """
        Generate a unique trip number based on type and date.
        
        Args:
            trip_type: Type of trip
            
        Returns:
            Generated trip number
        """
        today = timezone.now().date()
        prefix_map = {
            'medical': 'MED',
            'charter': 'CHR',
            'part_91': 'P91',
            'maintenance': 'MNT',
            'other': 'OTH'
        }
        
        prefix = prefix_map.get(trip_type, 'TRP')
        date_str = today.strftime('%Y%m%d')
        
        # Find next available number for today
        existing_count = Trip.objects.filter(
            trip_number__startswith=f"{prefix}{date_str}",
            created_on__date=today
        ).count()
        
        return f"{prefix}{date_str}{existing_count + 1:03d}"


class CrewService:
    """Service class for crew-related business logic."""
    
    @staticmethod
    def create_crew_line(
        primary_pic_id: str,
        secondary_sic_id: str,
        medic_ids: Optional[List[str]] = None
    ) -> CrewLine:
        """
        Create a crew line with validation.
        
        Args:
            primary_pic_id: Primary pilot in command contact ID
            secondary_sic_id: Secondary pilot in command contact ID
            medic_ids: Optional list of medic contact IDs
            
        Returns:
            Created CrewLine instance
            
        Raises:
            ValueError: If crew validation fails
        """
        # Validate pilots are different
        if primary_pic_id == secondary_sic_id:
            raise ValueError("Primary and secondary pilots must be different")
        
        # Validate contacts exist and are staff
        primary_contact = Contact.objects.get(id=primary_pic_id)
        secondary_contact = Contact.objects.get(id=secondary_sic_id)
        
        if not hasattr(primary_contact, 'staff') or not primary_contact.staff.active:
            raise ValueError("Primary pilot must be active staff")
        
        if not hasattr(secondary_contact, 'staff') or not secondary_contact.staff.active:
            raise ValueError("Secondary pilot must be active staff")
        
        crew_line = CrewLine.objects.create(
            primary_in_command_id=primary_pic_id,
            secondary_in_command_id=secondary_sic_id
        )
        
        if medic_ids:
            crew_line.medic_ids.set(medic_ids)
        
        return crew_line
    
    @staticmethod
    def validate_crew_availability(
        crew_line: CrewLine,
        start_time: datetime,
        end_time: datetime
    ) -> Dict[str, bool]:
        """
        Check if crew members are available for the given time period.
        
        Args:
            crew_line: CrewLine instance
            start_time: Start of duty period
            end_time: End of duty period
            
        Returns:
            Dictionary with availability status for each crew member
        """
        availability = {}
        
        # Check primary pilot
        primary_conflicts = TripLine.objects.filter(
            crew_line__primary_in_command=crew_line.primary_in_command,
            departure_time_utc__lt=end_time,
            arrival_time_utc__gt=start_time
        ).exists()
        availability['primary_available'] = not primary_conflicts
        
        # Check secondary pilot
        secondary_conflicts = TripLine.objects.filter(
            crew_line__secondary_in_command=crew_line.secondary_in_command,
            departure_time_utc__lt=end_time,
            arrival_time_utc__gt=start_time
        ).exists()
        availability['secondary_available'] = not secondary_conflicts
        
        # Check medics
        for medic in crew_line.medic_ids.all():
            medic_conflicts = TripLine.objects.filter(
                crew_line__medic_ids=medic,
                departure_time_utc__lt=end_time,
                arrival_time_utc__gt=start_time
            ).exists()
            availability[f'medic_{medic.id}_available'] = not medic_conflicts
        
        return availability

```


# File: operations/services/__init__.py

```python

```


# File: operations/tests/test_models.py

```python
from django.test import TestCase
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import datetime, timedelta, date
from decimal import Decimal

from .models import Quote, Patient, Passenger, CrewLine, Trip, TripLine, TripEvent
from .services.trip_service import TripService, CrewService
from .services.quote_service import QuoteService, PatientService
from contacts.models import Contact
from airports.models import Airport
from aircraft.models import Aircraft


class QuoteServiceTest(TestCase):
    """Test cases for QuoteService business logic."""
    
    def setUp(self):
        """Set up test data."""
        self.user = User.objects.create_user(username='testuser', password='testpass')
        
        # Create test contact
        self.contact = Contact.objects.create(
            first_name='John',
            last_name='Doe',
            email='john.doe@example.com',
            phone='555-1234'
        )
        
        # Create test airports
        self.pickup_airport = Airport.objects.create(
            ident='KJFK',
            name='John F. Kennedy International Airport',
            latitude=40.6413,
            longitude=-73.7781,
            iso_country='US',
            icao_code='KJFK',
            iata_code='JFK',
            timezone='America/New_York'
        )
        
        self.dropoff_airport = Airport.objects.create(
            ident='KLAX',
            name='Los Angeles International Airport',
            latitude=33.9425,
            longitude=-118.4081,
            iso_country='US',
            icao_code='KLAX',
            iata_code='LAX',
            timezone='America/Los_Angeles'
        )
    
    def test_create_quote_with_valid_data(self):
        """Test creating a quote with valid data."""
        quote = QuoteService.create_quote(
            contact_id=str(self.contact.id),
            pickup_airport_id=str(self.pickup_airport.id),
            dropoff_airport_id=str(self.dropoff_airport.id),
            aircraft_type='65',
            medical_team='RN/RN',
            estimated_flight_time=timedelta(hours=5)
        )
        
        self.assertIsInstance(quote, Quote)
        self.assertEqual(quote.contact, self.contact)
        self.assertEqual(quote.pickup_airport, self.pickup_airport)
        self.assertEqual(quote.dropoff_airport, self.dropoff_airport)
        self.assertGreater(quote.quoted_amount, 0)
    
    def test_quote_status_transitions(self):
        """Test valid and invalid quote status transitions."""
        quote = Quote.objects.create(
            contact=self.contact,
            pickup_airport=self.pickup_airport,
            dropoff_airport=self.dropoff_airport,
            aircraft_type='65',
            medical_team='RN/RN',
            estimated_flight_time=timedelta(hours=5),
            quoted_amount=Decimal('25000.00'),
            status='pending'
        )
        
        # Valid transition: pending -> active
        updated_quote = QuoteService.update_quote_status(quote, 'active', self.user)
        self.assertEqual(updated_quote.status, 'active')
        
        # Invalid transition: active -> pending
        with self.assertRaises(ValueError):
            QuoteService.update_quote_status(quote, 'pending', self.user)
    
    def test_payment_schedule_calculation(self):
        """Test payment schedule calculation for different quote types."""
        quote = Quote.objects.create(
            contact=self.contact,
            pickup_airport=self.pickup_airport,
            dropoff_airport=self.dropoff_airport,
            aircraft_type='65',
            medical_team='RN/RN',
            estimated_flight_time=timedelta(hours=5),
            quoted_amount=Decimal('20000.00')
        )
        
        schedule = QuoteService.calculate_payment_schedule(quote)
        
        self.assertEqual(schedule['total_amount'], Decimal('20000.00'))
        self.assertIn('deposit_amount', schedule)
        self.assertIn('balance_amount', schedule)
        self.assertEqual(
            schedule['deposit_amount'] + schedule['balance_amount'],
            schedule['total_amount']
        )


class PatientServiceTest(TestCase):
    """Test cases for PatientService business logic."""
    
    def setUp(self):
        """Set up test data."""
        self.contact = Contact.objects.create(
            first_name='Jane',
            last_name='Patient',
            email='jane.patient@example.com',
            date_of_birth=date(1980, 1, 1)
        )
    
    def test_create_patient_with_valid_data(self):
        """Test creating a patient with valid data."""
        future_date = timezone.now().date() + timedelta(days=365)
        
        patient = PatientService.create_patient_from_contact(
            contact_id=str(self.contact.id),
            date_of_birth=date(1980, 1, 1),
            nationality='US',
            passport_number='123456789',
            passport_expiration_date=future_date
        )
        
        self.assertIsInstance(patient, Patient)
        self.assertEqual(patient.info, self.contact)
        self.assertEqual(patient.nationality, 'US')
    
    def test_create_patient_with_expired_passport(self):
        """Test creating a patient with expired passport fails."""
        past_date = timezone.now().date() - timedelta(days=30)
        
        with self.assertRaises(ValueError):
            PatientService.create_patient_from_contact(
                contact_id=str(self.contact.id),
                date_of_birth=date(1980, 1, 1),
                nationality='US',
                passport_number='123456789',
                passport_expiration_date=past_date
            )
    
    def test_validate_medical_documents(self):
        """Test medical document validation."""
        future_date = timezone.now().date() + timedelta(days=365)
        
        patient = Patient.objects.create(
            info=self.contact,
            date_of_birth=date(1980, 1, 1),
            nationality='US',
            passport_number='123456789',
            passport_expiration_date=future_date
        )
        
        validation = PatientService.validate_medical_documents(patient)
        
        self.assertIn('passport_document', validation)
        self.assertIn('medical_necessity', validation)
        self.assertIn('passport_valid', validation)
        self.assertIn('all_valid', validation)


class TripServiceTest(TestCase):
    """Test cases for TripService business logic."""
    
    def setUp(self):
        """Set up test data."""
        self.user = User.objects.create_user(username='testuser', password='testpass')
        
        # Create test aircraft
        self.aircraft = Aircraft.objects.create(
            tail_number='N123AB',
            company='Test Aviation',
            mgtow=Decimal('65000.00'),
            make='Learjet',
            model='65',
            serial_number='65-123'
        )
        
        # Create test airports
        self.origin_airport = Airport.objects.create(
            ident='KJFK',
            name='John F. Kennedy International Airport',
            latitude=40.6413,
            longitude=-73.7781,
            iso_country='US',
            icao_code='KJFK',
            iata_code='JFK',
            timezone='America/New_York'
        )
        
        self.destination_airport = Airport.objects.create(
            ident='KLAX',
            name='Los Angeles International Airport',
            latitude=33.9425,
            longitude=-118.4081,
            iso_country='US',
            icao_code='KLAX',
            iata_code='LAX',
            timezone='America/Los_Angeles'
        )
    
    def test_create_trip_with_valid_data(self):
        """Test creating a trip with valid data."""
        trip = TripService.create_trip(
            trip_number='TEST001',
            trip_type='charter',
            aircraft_id=str(self.aircraft.id)
        )
        
        self.assertIsInstance(trip, Trip)
        self.assertEqual(trip.trip_number, 'TEST001')
        self.assertEqual(trip.type, 'charter')
        self.assertEqual(trip.aircraft, self.aircraft)
    
    def test_create_medical_trip_without_patient_fails(self):
        """Test that medical trips require a patient."""
        with self.assertRaises(ValueError):
            TripService.create_trip(
                trip_number='MED001',
                trip_type='medical'
            )
    
    def test_trip_number_generation(self):
        """Test automatic trip number generation."""
        trip = TripService.create_trip(
            trip_number='',  # Empty trip number should trigger auto-generation
            trip_type='charter'
        )
        
        self.assertTrue(trip.trip_number.startswith('CHR'))
        self.assertGreater(len(trip.trip_number), 3)
    
    def test_calculate_trip_duration(self):
        """Test trip duration calculation."""
        trip = Trip.objects.create(
            trip_number='TEST001',
            type='charter',
            aircraft=self.aircraft
        )
        
        # Add trip lines
        departure_time = timezone.now()
        arrival_time = departure_time + timedelta(hours=5)
        
        TripLine.objects.create(
            trip=trip,
            origin_airport=self.origin_airport,
            destination_airport=self.destination_airport,
            departure_time_local=departure_time,
            departure_time_utc=departure_time,
            arrival_time_local=arrival_time,
            arrival_time_utc=arrival_time,
            distance=Decimal('2500.00'),
            flight_time=timedelta(hours=5),
            ground_time=timedelta(hours=1)
        )
        
        duration = TripService.calculate_trip_duration(trip)
        self.assertEqual(duration, timedelta(hours=5))


class CrewServiceTest(TestCase):
    """Test cases for CrewService business logic."""
    
    def setUp(self):
        """Set up test data."""
        # Create test contacts for crew members
        self.pilot1 = Contact.objects.create(
            first_name='John',
            last_name='Pilot',
            email='john.pilot@example.com'
        )
        
        self.pilot2 = Contact.objects.create(
            first_name='Jane',
            last_name='Copilot',
            email='jane.copilot@example.com'
        )
        
        self.medic = Contact.objects.create(
            first_name='Bob',
            last_name='Medic',
            email='bob.medic@example.com'
        )
    
    def test_create_crew_line_with_valid_data(self):
        """Test creating a crew line with valid data."""
        crew_line = CrewService.create_crew_line(
            primary_pic_id=str(self.pilot1.id),
            secondary_sic_id=str(self.pilot2.id),
            medic_ids=[str(self.medic.id)]
        )
        
        self.assertIsInstance(crew_line, CrewLine)
        self.assertEqual(crew_line.primary_in_command, self.pilot1)
        self.assertEqual(crew_line.secondary_in_command, self.pilot2)
        self.assertIn(self.medic, crew_line.medic_ids.all())
    
    def test_create_crew_line_with_same_pilots_fails(self):
        """Test that crew line creation fails with same pilot for both positions."""
        with self.assertRaises(ValueError):
            CrewService.create_crew_line(
                primary_pic_id=str(self.pilot1.id),
                secondary_sic_id=str(self.pilot1.id)  # Same pilot
            )


class TripModelTest(TestCase):
    """Test cases for Trip model functionality."""
    
    def setUp(self):
        """Set up test data."""
        self.aircraft = Aircraft.objects.create(
            tail_number='N123AB',
            company='Test Aviation',
            mgtow=Decimal('65000.00'),
            make='Learjet',
            model='65',
            serial_number='65-123'
        )
    
    def test_trip_string_representation(self):
        """Test trip string representation."""
        trip = Trip.objects.create(
            trip_number='TEST001',
            type='charter',
            aircraft=self.aircraft
        )
        
        expected_str = 'Trip TEST001 - charter'
        self.assertEqual(str(trip), expected_str)
    
    def test_trip_number_uniqueness(self):
        """Test that trip numbers must be unique."""
        Trip.objects.create(
            trip_number='TEST001',
            type='charter',
            aircraft=self.aircraft
        )
        
        # Creating another trip with the same number should fail
        with self.assertRaises(Exception):
            Trip.objects.create(
                trip_number='TEST001',
                type='medical',
                aircraft=self.aircraft
            )


class QuoteModelTest(TestCase):
    """Test cases for Quote model functionality."""
    
    def setUp(self):
        """Set up test data."""
        self.contact = Contact.objects.create(
            first_name='John',
            last_name='Customer',
            email='john.customer@example.com'
        )
        
        self.pickup_airport = Airport.objects.create(
            ident='KJFK',
            name='John F. Kennedy International Airport',
            latitude=40.6413,
            longitude=-73.7781,
            iso_country='US',
            icao_code='KJFK',
            iata_code='JFK',
            timezone='America/New_York'
        )
        
        self.dropoff_airport = Airport.objects.create(
            ident='KLAX',
            name='Los Angeles International Airport',
            latitude=33.9425,
            longitude=-118.4081,
            iso_country='US',
            icao_code='KLAX',
            iata_code='LAX',
            timezone='America/Los_Angeles'
        )
    
    def test_quote_string_representation(self):
        """Test quote string representation."""
        quote = Quote.objects.create(
            contact=self.contact,
            pickup_airport=self.pickup_airport,
            dropoff_airport=self.dropoff_airport,
            aircraft_type='65',
            medical_team='RN/RN',
            estimated_flight_time=timedelta(hours=5),
            quoted_amount=Decimal('25000.00')
        )
        
        expected_str = f'Quote {quote.id} - $25000.00 - pending'
        self.assertEqual(str(quote), expected_str)

```


# File: operations/tests/test_api.py

```python
from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from django.utils import timezone
from datetime import timedelta
from decimal import Decimal

from operations.models import Trip, Quote, Patient, Passenger, CrewLine
from contacts.models import Contact
from airports.models import Airport
from aircraft.models import Aircraft


class TripAPITest(TestCase):
    """Test cases for Trip API endpoints."""
    
    def setUp(self):
        """Set up test data."""
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.force_authenticate(user=self.user)
        
        # Create test data
        self.contact = Contact.objects.create(
            first_name='John',
            last_name='Doe',
            email='john.doe@example.com',
            phone='555-1234'
        )
        
        self.pickup_airport = Airport.objects.create(
            ident='KJFK',
            name='John F. Kennedy International Airport',
            latitude=40.6413,
            longitude=-73.7781,
            iso_country='US',
            icao_code='KJFK',
            iata_code='JFK',
            timezone='America/New_York'
        )
        
        self.dropoff_airport = Airport.objects.create(
            ident='KLAX',
            name='Los Angeles International Airport',
            latitude=33.9425,
            longitude=-118.4081,
            iso_country='US',
            icao_code='KLAX',
            iata_code='LAX',
            timezone='America/Los_Angeles'
        )
        
        self.aircraft = Aircraft.objects.create(
            tail_number='N123AB',
            aircraft_type='Citation CJ3',
            manufacturer='Cessna',
            model='Citation CJ3',
            year=2020,
            max_passengers=8,
            range_nm=2040,
            cruise_speed=417
        )
        
        self.trip = Trip.objects.create(
            trip_number='TRIP-001',
            customer=self.contact,
            aircraft=self.aircraft,
            pickup_airport=self.pickup_airport,
            dropoff_airport=self.dropoff_airport,
            pickup_date=timezone.now().date() + timedelta(days=7),
            pickup_time=timezone.now().time(),
            status='PENDING'
        )
    
    def test_list_trips(self):
        """Test listing trips."""
        url = reverse('trip-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['trip_number'], 'TRIP-001')
    
    def test_create_trip(self):
        """Test creating a trip."""
        url = reverse('trip-list')
        data = {
            'trip_number': 'TRIP-002',
            'customer': self.contact.id,
            'aircraft': self.aircraft.id,
            'pickup_airport': self.pickup_airport.id,
            'dropoff_airport': self.dropoff_airport.id,
            'pickup_date': (timezone.now().date() + timedelta(days=10)).isoformat(),
            'pickup_time': timezone.now().time().isoformat(),
            'status': 'PENDING'
        }
        
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['trip_number'], 'TRIP-002')
    
    def test_update_trip(self):
        """Test updating a trip."""
        url = reverse('trip-detail', kwargs={'pk': self.trip.pk})
        data = {
            'status': 'CONFIRMED'
        }
        
        response = self.client.patch(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], 'CONFIRMED')
    
    def test_delete_trip(self):
        """Test deleting a trip."""
        url = reverse('trip-detail', kwargs={'pk': self.trip.pk})
        response = self.client.delete(url)
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Trip.objects.filter(pk=self.trip.pk).exists())


class QuoteAPITest(TestCase):
    """Test cases for Quote API endpoints."""
    
    def setUp(self):
        """Set up test data."""
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.force_authenticate(user=self.user)
        
        # Create test data
        self.contact = Contact.objects.create(
            first_name='John',
            last_name='Doe',
            email='john.doe@example.com',
            phone='555-1234'
        )
        
        self.pickup_airport = Airport.objects.create(
            ident='KJFK',
            name='John F. Kennedy International Airport',
            latitude=40.6413,
            longitude=-73.7781,
            iso_country='US',
            icao_code='KJFK',
            iata_code='JFK',
            timezone='America/New_York'
        )
        
        self.dropoff_airport = Airport.objects.create(
            ident='KLAX',
            name='Los Angeles International Airport',
            latitude=33.9425,
            longitude=-118.4081,
            iso_country='US',
            icao_code='KLAX',
            iata_code='LAX',
            timezone='America/Los_Angeles'
        )
        
        self.aircraft = Aircraft.objects.create(
            tail_number='N123AB',
            aircraft_type='Citation CJ3',
            manufacturer='Cessna',
            model='Citation CJ3',
            year=2020,
            max_passengers=8,
            range_nm=2040,
            cruise_speed=417
        )
        
        self.quote = Quote.objects.create(
            quote_number='QUOTE-001',
            customer=self.contact,
            aircraft=self.aircraft,
            pickup_airport=self.pickup_airport,
            dropoff_airport=self.dropoff_airport,
            pickup_date=timezone.now().date() + timedelta(days=7),
            pickup_time=timezone.now().time(),
            passenger_count=4,
            total_cost=Decimal('15000.00'),
            status='PENDING'
        )
    
    def test_list_quotes(self):
        """Test listing quotes."""
        url = reverse('quote-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['quote_number'], 'QUOTE-001')
    
    def test_create_quote(self):
        """Test creating a quote."""
        url = reverse('quote-list')
        data = {
            'quote_number': 'QUOTE-002',
            'customer': self.contact.id,
            'aircraft': self.aircraft.id,
            'pickup_airport': self.pickup_airport.id,
            'dropoff_airport': self.dropoff_airport.id,
            'pickup_date': (timezone.now().date() + timedelta(days=10)).isoformat(),
            'pickup_time': timezone.now().time().isoformat(),
            'passenger_count': 6,
            'total_cost': '18000.00',
            'status': 'PENDING'
        }
        
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['quote_number'], 'QUOTE-002')
    
    def test_convert_quote_to_trip(self):
        """Test converting quote to trip."""
        url = reverse('quote-convert-to-trip', kwargs={'pk': self.quote.pk})
        response = self.client.post(url)
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Trip.objects.filter(customer=self.quote.customer).exists())


class PatientAPITest(TestCase):
    """Test cases for Patient API endpoints."""
    
    def setUp(self):
        """Set up test data."""
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.force_authenticate(user=self.user)
        
        # Create test data
        self.contact = Contact.objects.create(
            first_name='John',
            last_name='Doe',
            email='john.doe@example.com',
            phone='555-1234'
        )
        
        self.pickup_airport = Airport.objects.create(
            ident='KJFK',
            name='John F. Kennedy International Airport',
            latitude=40.6413,
            longitude=-73.7781,
            iso_country='US',
            icao_code='KJFK',
            iata_code='JFK',
            timezone='America/New_York'
        )
        
        self.dropoff_airport = Airport.objects.create(
            ident='KLAX',
            name='Los Angeles International Airport',
            latitude=33.9425,
            longitude=-118.4081,
            iso_country='US',
            icao_code='KLAX',
            iata_code='LAX',
            timezone='America/Los_Angeles'
        )
        
        self.aircraft = Aircraft.objects.create(
            tail_number='N123AB',
            aircraft_type='Citation CJ3',
            manufacturer='Cessna',
            model='Citation CJ3',
            year=2020,
            max_passengers=8,
            range_nm=2040,
            cruise_speed=417
        )
        
        self.trip = Trip.objects.create(
            trip_number='TRIP-001',
            customer=self.contact,
            aircraft=self.aircraft,
            pickup_airport=self.pickup_airport,
            dropoff_airport=self.dropoff_airport,
            pickup_date=timezone.now().date() + timedelta(days=7),
            pickup_time=timezone.now().time(),
            status='PENDING'
        )
        
        self.patient = Patient.objects.create(
            trip=self.trip,
            first_name='Jane',
            last_name='Patient',
            date_of_birth='1980-01-01',
            medical_condition='Post-surgery recovery',
            mobility_assistance=True,
            oxygen_required=False,
            stretcher_required=False
        )
    
    def test_list_patients(self):
        """Test listing patients."""
        url = reverse('patient-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['first_name'], 'Jane')
    
    def test_create_patient(self):
        """Test creating a patient."""
        url = reverse('patient-list')
        data = {
            'trip': self.trip.id,
            'first_name': 'John',
            'last_name': 'Patient2',
            'date_of_birth': '1975-05-15',
            'medical_condition': 'Recovery',
            'mobility_assistance': False,
            'oxygen_required': True,
            'stretcher_required': False
        }
        
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['first_name'], 'John')
        self.assertTrue(response.data['oxygen_required'])

```


# File: operations/tests/__init__.py

```python

```


# File: operations/tests/test_services.py

```python
from django.test import TestCase
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import datetime, timedelta, date
from decimal import Decimal
from unittest.mock import patch, Mock

from operations.models import Quote, Patient, Passenger, CrewLine, Trip, TripLine, TripEvent
from operations.services.trip_service import TripService, CrewService
from operations.services.quote_service import QuoteService, PatientService
from contacts.models import Contact
from airports.models import Airport
from aircraft.models import Aircraft


class TripServiceTest(TestCase):
    """Test cases for TripService business logic."""
    
    def setUp(self):
        """Set up test data."""
        self.user = User.objects.create_user(username='testuser', password='testpass')
        
        # Create test contact
        self.contact = Contact.objects.create(
            first_name='John',
            last_name='Doe',
            email='john.doe@example.com',
            phone='555-1234'
        )
        
        # Create test airports
        self.pickup_airport = Airport.objects.create(
            ident='KJFK',
            name='John F. Kennedy International Airport',
            latitude=40.6413,
            longitude=-73.7781,
            iso_country='US',
            icao_code='KJFK',
            iata_code='JFK',
            timezone='America/New_York'
        )
        
        self.dropoff_airport = Airport.objects.create(
            ident='KLAX',
            name='Los Angeles International Airport',
            latitude=33.9425,
            longitude=-118.4081,
            iso_country='US',
            icao_code='KLAX',
            iata_code='LAX',
            timezone='America/Los_Angeles'
        )
        
        # Create test aircraft
        self.aircraft = Aircraft.objects.create(
            tail_number='N123AB',
            aircraft_type='Citation CJ3',
            manufacturer='Cessna',
            model='Citation CJ3',
            year=2020,
            max_passengers=8,
            range_nm=2040,
            cruise_speed=417
        )
        
        # Create test trip
        self.trip = Trip.objects.create(
            trip_number='TRIP-001',
            customer=self.contact,
            aircraft=self.aircraft,
            pickup_airport=self.pickup_airport,
            dropoff_airport=self.dropoff_airport,
            pickup_date=timezone.now().date() + timedelta(days=7),
            pickup_time=timezone.now().time(),
            status='PENDING'
        )
        
        self.trip_service = TripService()
    
    def test_create_trip(self):
        """Test trip creation through service."""
        trip_data = {
            'trip_number': 'TRIP-002',
            'customer': self.contact,
            'aircraft': self.aircraft,
            'pickup_airport': self.pickup_airport,
            'dropoff_airport': self.dropoff_airport,
            'pickup_date': timezone.now().date() + timedelta(days=10),
            'pickup_time': timezone.now().time(),
            'status': 'PENDING'
        }
        
        trip = self.trip_service.create_trip(trip_data)
        
        self.assertIsNotNone(trip)
        self.assertEqual(trip.trip_number, 'TRIP-002')
        self.assertEqual(trip.customer, self.contact)
        self.assertEqual(trip.status, 'PENDING')
    
    def test_update_trip_status(self):
        """Test trip status update."""
        updated_trip = self.trip_service.update_trip_status(self.trip.id, 'CONFIRMED')
        
        self.assertEqual(updated_trip.status, 'CONFIRMED')
        
        # Refresh from database
        self.trip.refresh_from_db()
        self.assertEqual(self.trip.status, 'CONFIRMED')
    
    def test_calculate_trip_duration(self):
        """Test trip duration calculation."""
        # Set dropoff time
        self.trip.dropoff_date = self.trip.pickup_date
        self.trip.dropoff_time = (datetime.combine(date.today(), self.trip.pickup_time) + timedelta(hours=5)).time()
        self.trip.save()
        
        duration = self.trip_service.calculate_trip_duration(self.trip.id)
        
        self.assertIsNotNone(duration)
        self.assertEqual(duration.total_seconds(), 5 * 3600)  # 5 hours
    
    def test_get_trips_by_date_range(self):
        """Test retrieving trips by date range."""
        start_date = timezone.now().date()
        end_date = start_date + timedelta(days=30)
        
        trips = self.trip_service.get_trips_by_date_range(start_date, end_date)
        
        self.assertIn(self.trip, trips)
    
    def test_get_trips_by_aircraft(self):
        """Test retrieving trips by aircraft."""
        trips = self.trip_service.get_trips_by_aircraft(self.aircraft.id)
        
        self.assertIn(self.trip, trips)
    
    def test_add_passenger_to_trip(self):
        """Test adding passenger to trip."""
        passenger_data = {
            'first_name': 'Jane',
            'last_name': 'Smith',
            'email': 'jane.smith@example.com',
            'phone': '555-5678'
        }
        
        passenger = self.trip_service.add_passenger_to_trip(self.trip.id, passenger_data)
        
        self.assertIsNotNone(passenger)
        self.assertEqual(passenger.first_name, 'Jane')
        self.assertEqual(passenger.trip, self.trip)
    
    def test_cancel_trip(self):
        """Test trip cancellation."""
        cancelled_trip = self.trip_service.cancel_trip(self.trip.id, 'Customer request')
        
        self.assertEqual(cancelled_trip.status, 'CANCELLED')
        self.assertIsNotNone(cancelled_trip.cancellation_reason)


class CrewServiceTest(TestCase):
    """Test cases for CrewService business logic."""
    
    def setUp(self):
        """Set up test data."""
        self.user = User.objects.create_user(username='testuser', password='testpass')
        
        # Create test contact for customer
        self.contact = Contact.objects.create(
            first_name='John',
            last_name='Doe',
            email='john.doe@example.com',
            phone='555-1234'
        )
        
        # Create test contact for crew member
        self.crew_member = Contact.objects.create(
            first_name='Captain',
            last_name='Smith',
            email='captain.smith@example.com',
            phone='555-9999'
        )
        
        # Create test airports
        self.pickup_airport = Airport.objects.create(
            ident='KJFK',
            name='John F. Kennedy International Airport',
            latitude=40.6413,
            longitude=-73.7781,
            iso_country='US',
            icao_code='KJFK',
            iata_code='JFK',
            timezone='America/New_York'
        )
        
        self.dropoff_airport = Airport.objects.create(
            ident='KLAX',
            name='Los Angeles International Airport',
            latitude=33.9425,
            longitude=-118.4081,
            iso_country='US',
            icao_code='KLAX',
            iata_code='LAX',
            timezone='America/Los_Angeles'
        )
        
        # Create test aircraft
        self.aircraft = Aircraft.objects.create(
            tail_number='N123AB',
            aircraft_type='Citation CJ3',
            manufacturer='Cessna',
            model='Citation CJ3',
            year=2020,
            max_passengers=8,
            range_nm=2040,
            cruise_speed=417
        )
        
        # Create test trip
        self.trip = Trip.objects.create(
            trip_number='TRIP-001',
            customer=self.contact,
            aircraft=self.aircraft,
            pickup_airport=self.pickup_airport,
            dropoff_airport=self.dropoff_airport,
            pickup_date=timezone.now().date() + timedelta(days=7),
            pickup_time=timezone.now().time(),
            status='PENDING'
        )
        
        self.crew_service = CrewService()
    
    def test_assign_crew_to_trip(self):
        """Test crew assignment to trip."""
        crew_line = self.crew_service.assign_crew_to_trip(
            trip_id=self.trip.id,
            crew_member=self.crew_member,
            role='CAPTAIN',
            duty_start=timezone.now(),
            duty_end=timezone.now() + timedelta(hours=8)
        )
        
        self.assertIsNotNone(crew_line)
        self.assertEqual(crew_line.trip, self.trip)
        self.assertEqual(crew_line.crew_member, self.crew_member)
        self.assertEqual(crew_line.role, 'CAPTAIN')
    
    def test_get_crew_for_trip(self):
        """Test retrieving crew for a trip."""
        # Create crew line
        CrewLine.objects.create(
            trip=self.trip,
            crew_member=self.crew_member,
            role='CAPTAIN',
            duty_start=timezone.now(),
            duty_end=timezone.now() + timedelta(hours=8)
        )
        
        crew_lines = self.crew_service.get_crew_for_trip(self.trip.id)
        
        self.assertEqual(len(crew_lines), 1)
        self.assertEqual(crew_lines[0].crew_member, self.crew_member)
    
    def test_calculate_crew_duty_time(self):
        """Test crew duty time calculation."""
        duty_start = timezone.now()
        duty_end = duty_start + timedelta(hours=10)
        
        crew_line = CrewLine.objects.create(
            trip=self.trip,
            crew_member=self.crew_member,
            role='CAPTAIN',
            duty_start=duty_start,
            duty_end=duty_end
        )
        
        duty_time = self.crew_service.calculate_crew_duty_time(crew_line.id)
        
        self.assertEqual(duty_time.total_seconds(), 10 * 3600)  # 10 hours
    
    def test_check_crew_availability(self):
        """Test crew availability checking."""
        # Create existing crew assignment
        existing_start = timezone.now() + timedelta(days=1)
        existing_end = existing_start + timedelta(hours=8)
        
        CrewLine.objects.create(
            trip=self.trip,
            crew_member=self.crew_member,
            role='CAPTAIN',
            duty_start=existing_start,
            duty_end=existing_end
        )
        
        # Check availability for overlapping time
        overlap_start = existing_start + timedelta(hours=4)
        overlap_end = overlap_start + timedelta(hours=8)
        
        is_available = self.crew_service.check_crew_availability(
            self.crew_member.id,
            overlap_start,
            overlap_end
        )
        
        self.assertFalse(is_available)
        
        # Check availability for non-overlapping time
        non_overlap_start = existing_end + timedelta(hours=1)
        non_overlap_end = non_overlap_start + timedelta(hours=8)
        
        is_available = self.crew_service.check_crew_availability(
            self.crew_member.id,
            non_overlap_start,
            non_overlap_end
        )
        
        self.assertTrue(is_available)


class QuoteServiceTest(TestCase):
    """Test cases for QuoteService business logic."""
    
    def setUp(self):
        """Set up test data."""
        self.user = User.objects.create_user(username='testuser', password='testpass')
        
        # Create test contact
        self.contact = Contact.objects.create(
            first_name='John',
            last_name='Doe',
            email='john.doe@example.com',
            phone='555-1234'
        )
        
        # Create test airports
        self.pickup_airport = Airport.objects.create(
            ident='KJFK',
            name='John F. Kennedy International Airport',
            latitude=40.6413,
            longitude=-73.7781,
            iso_country='US',
            icao_code='KJFK',
            iata_code='JFK',
            timezone='America/New_York'
        )
        
        self.dropoff_airport = Airport.objects.create(
            ident='KLAX',
            name='Los Angeles International Airport',
            latitude=33.9425,
            longitude=-118.4081,
            iso_country='US',
            icao_code='KLAX',
            iata_code='LAX',
            timezone='America/Los_Angeles'
        )
        
        # Create test aircraft
        self.aircraft = Aircraft.objects.create(
            tail_number='N123AB',
            aircraft_type='Citation CJ3',
            manufacturer='Cessna',
            model='Citation CJ3',
            year=2020,
            max_passengers=8,
            range_nm=2040,
            cruise_speed=417
        )
        
        self.quote_service = QuoteService()
    
    def test_create_quote(self):
        """Test quote creation through service."""
        quote_data = {
            'quote_number': 'QUOTE-001',
            'customer': self.contact,
            'aircraft': self.aircraft,
            'pickup_airport': self.pickup_airport,
            'dropoff_airport': self.dropoff_airport,
            'pickup_date': timezone.now().date() + timedelta(days=7),
            'pickup_time': timezone.now().time(),
            'passenger_count': 4,
            'total_cost': Decimal('15000.00')
        }
        
        quote = self.quote_service.create_quote(quote_data)
        
        self.assertIsNotNone(quote)
        self.assertEqual(quote.quote_number, 'QUOTE-001')
        self.assertEqual(quote.customer, self.contact)
        self.assertEqual(quote.total_cost, Decimal('15000.00'))
    
    @patch('operations.services.quote_service.QuoteService.calculate_distance')
    def test_calculate_quote_cost(self, mock_calculate_distance):
        """Test quote cost calculation."""
        mock_calculate_distance.return_value = 2500  # miles
        
        cost = self.quote_service.calculate_quote_cost(
            pickup_airport=self.pickup_airport,
            dropoff_airport=self.dropoff_airport,
            aircraft=self.aircraft,
            passenger_count=4
        )
        
        self.assertIsInstance(cost, Decimal)
        self.assertGreater(cost, Decimal('0'))
    
    def test_update_quote_status(self):
        """Test quote status update."""
        quote = Quote.objects.create(
            quote_number='QUOTE-002',
            customer=self.contact,
            aircraft=self.aircraft,
            pickup_airport=self.pickup_airport,
            dropoff_airport=self.dropoff_airport,
            pickup_date=timezone.now().date() + timedelta(days=7),
            pickup_time=timezone.now().time(),
            passenger_count=4,
            total_cost=Decimal('15000.00'),
            status='PENDING'
        )
        
        updated_quote = self.quote_service.update_quote_status(quote.id, 'ACCEPTED')
        
        self.assertEqual(updated_quote.status, 'ACCEPTED')
    
    def test_convert_quote_to_trip(self):
        """Test converting quote to trip."""
        quote = Quote.objects.create(
            quote_number='QUOTE-003',
            customer=self.contact,
            aircraft=self.aircraft,
            pickup_airport=self.pickup_airport,
            dropoff_airport=self.dropoff_airport,
            pickup_date=timezone.now().date() + timedelta(days=7),
            pickup_time=timezone.now().time(),
            passenger_count=4,
            total_cost=Decimal('15000.00'),
            status='ACCEPTED'
        )
        
        trip = self.quote_service.convert_quote_to_trip(quote.id)
        
        self.assertIsNotNone(trip)
        self.assertEqual(trip.customer, quote.customer)
        self.assertEqual(trip.aircraft, quote.aircraft)
        self.assertEqual(trip.pickup_airport, quote.pickup_airport)
        self.assertEqual(trip.dropoff_airport, quote.dropoff_airport)


class PatientServiceTest(TestCase):
    """Test cases for PatientService business logic."""
    
    def setUp(self):
        """Set up test data."""
        self.user = User.objects.create_user(username='testuser', password='testpass')
        
        # Create test contact
        self.contact = Contact.objects.create(
            first_name='John',
            last_name='Doe',
            email='john.doe@example.com',
            phone='555-1234'
        )
        
        # Create test airports
        self.pickup_airport = Airport.objects.create(
            ident='KJFK',
            name='John F. Kennedy International Airport',
            latitude=40.6413,
            longitude=-73.7781,
            iso_country='US',
            icao_code='KJFK',
            iata_code='JFK',
            timezone='America/New_York'
        )
        
        self.dropoff_airport = Airport.objects.create(
            ident='KLAX',
            name='Los Angeles International Airport',
            latitude=33.9425,
            longitude=-118.4081,
            iso_country='US',
            icao_code='KLAX',
            iata_code='LAX',
            timezone='America/Los_Angeles'
        )
        
        # Create test aircraft
        self.aircraft = Aircraft.objects.create(
            tail_number='N123AB',
            aircraft_type='Citation CJ3',
            manufacturer='Cessna',
            model='Citation CJ3',
            year=2020,
            max_passengers=8,
            range_nm=2040,
            cruise_speed=417
        )
        
        # Create test trip
        self.trip = Trip.objects.create(
            trip_number='TRIP-001',
            customer=self.contact,
            aircraft=self.aircraft,
            pickup_airport=self.pickup_airport,
            dropoff_airport=self.dropoff_airport,
            pickup_date=timezone.now().date() + timedelta(days=7),
            pickup_time=timezone.now().time(),
            status='PENDING'
        )
        
        self.patient_service = PatientService()
    
    def test_create_patient_record(self):
        """Test patient record creation."""
        patient_data = {
            'trip': self.trip,
            'first_name': 'Jane',
            'last_name': 'Patient',
            'date_of_birth': date(1980, 1, 1),
            'medical_condition': 'Post-surgery recovery',
            'mobility_assistance': True,
            'oxygen_required': False,
            'stretcher_required': False
        }
        
        patient = self.patient_service.create_patient_record(patient_data)
        
        self.assertIsNotNone(patient)
        self.assertEqual(patient.first_name, 'Jane')
        self.assertEqual(patient.trip, self.trip)
        self.assertTrue(patient.mobility_assistance)
    
    def test_update_medical_requirements(self):
        """Test updating patient medical requirements."""
        patient = Patient.objects.create(
            trip=self.trip,
            first_name='Jane',
            last_name='Patient',
            date_of_birth=date(1980, 1, 1),
            medical_condition='Post-surgery recovery',
            mobility_assistance=False,
            oxygen_required=False,
            stretcher_required=False
        )
        
        updated_patient = self.patient_service.update_medical_requirements(
            patient.id,
            {
                'oxygen_required': True,
                'stretcher_required': True,
                'medical_notes': 'Requires continuous oxygen monitoring'
            }
        )
        
        self.assertTrue(updated_patient.oxygen_required)
        self.assertTrue(updated_patient.stretcher_required)
        self.assertIn('oxygen monitoring', updated_patient.medical_notes)
    
    def test_validate_aircraft_medical_capability(self):
        """Test aircraft medical capability validation."""
        patient = Patient.objects.create(
            trip=self.trip,
            first_name='Jane',
            last_name='Patient',
            date_of_birth=date(1980, 1, 1),
            medical_condition='Post-surgery recovery',
            mobility_assistance=False,
            oxygen_required=True,
            stretcher_required=True
        )
        
        # Mock aircraft capabilities check
        with patch.object(self.patient_service, 'check_aircraft_medical_equipment') as mock_check:
            mock_check.return_value = True
            
            is_capable = self.patient_service.validate_aircraft_medical_capability(
                patient.id,
                self.aircraft.id
            )
            
            self.assertTrue(is_capable)
            mock_check.assert_called_once()
    
    def test_get_patients_for_trip(self):
        """Test retrieving patients for a trip."""
        # Create multiple patients
        Patient.objects.create(
            trip=self.trip,
            first_name='Jane',
            last_name='Patient1',
            date_of_birth=date(1980, 1, 1),
            medical_condition='Condition 1'
        )
        
        Patient.objects.create(
            trip=self.trip,
            first_name='John',
            last_name='Patient2',
            date_of_birth=date(1975, 5, 15),
            medical_condition='Condition 2'
        )
        
        patients = self.patient_service.get_patients_for_trip(self.trip.id)
        
        self.assertEqual(len(patients), 2)
        self.assertEqual(patients[0].trip, self.trip)
        self.assertEqual(patients[1].trip, self.trip)

```


# File: index/models.py

```python
from django.db import models


class IndexPage(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    slug = models.SlugField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title

```


# File: index/serializers.py

```python
from rest_framework import serializers
from .models import IndexPage


class IndexPageSerializer(serializers.ModelSerializer):
    class Meta:
        model = IndexPage
        fields = '__all__'

```


# File: index/views.py

```python
from rest_framework import viewsets
from .models import IndexPage
from .serializers import IndexPageSerializer


class IndexPageViewSet(viewsets.ModelViewSet):
    queryset = IndexPage.objects.all()
    serializer_class = IndexPageSerializer
    lookup_field = 'slug'

```


# File: index/apps.py

```python
from django.apps import AppConfig


class IndexConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'index'

```


# File: index/__init__.py

```python


```


# File: index/urls.py

```python
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import IndexPageViewSet

router = DefaultRouter()
router.register(r'pages', IndexPageViewSet)

urlpatterns = [
    path('', include(router.urls)),
]

```


# File: index/admin.py

```python
from django.contrib import admin
from .models import IndexPage

admin.site.register(IndexPage)

```


# File: aircraft/models.py

```python
from django.db import models
from common.models import BaseModel
from decimal import Decimal


class Aircraft(BaseModel):
    """Aircraft model for fleet management."""
    tail_number = models.CharField(max_length=20, unique=True, db_index=True)
    company = models.CharField(max_length=255)
    
    # Aircraft specifications
    mgtow = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        verbose_name="Maximum Gross Takeoff Weight"
    )
    make = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    serial_number = models.CharField(max_length=100)
    
    # Registration and certification
    registration_country = models.CharField(max_length=3, default='US')
    year_manufactured = models.IntegerField(null=True, blank=True)
    
    # Operational specifications
    max_passengers = models.IntegerField(null=True, blank=True)
    max_range_nm = models.IntegerField(null=True, blank=True, verbose_name="Maximum Range (NM)")
    cruise_speed_knots = models.IntegerField(null=True, blank=True)
    service_ceiling_feet = models.IntegerField(null=True, blank=True)
    
    # Status and availability
    operational_status = models.CharField(max_length=20, choices=[
        ('active', 'Active'),
        ('maintenance', 'In Maintenance'),
        ('inactive', 'Inactive'),
        ('retired', 'Retired')
    ], default='active')
    
    # Medical equipment configuration
    medical_equipped = models.BooleanField(default=False)
    stretcher_capacity = models.IntegerField(default=0)
    
    # Notes and additional information
    notes = models.TextField(blank=True, null=True)

    class Meta:
        indexes = [
            models.Index(fields=['tail_number']),
            models.Index(fields=['make', 'model']),
            models.Index(fields=['operational_status']),
        ]

    def __str__(self):
        return f"{self.tail_number} - {self.make} {self.model}"
    
    @property
    def is_available(self):
        """Check if aircraft is available for operations."""
        return self.operational_status == 'active'
    
    @property
    def full_designation(self):
        """Return full aircraft designation."""
        return f"{self.make} {self.model} ({self.tail_number})"


class MaintenanceLog(BaseModel):
    """Maintenance log entries for aircraft."""
    
    MAINTENANCE_TYPES = [
        ('inspection', 'Inspection'),
        ('repair', 'Repair'),
        ('modification', 'Modification'),
        ('overhaul', 'Overhaul'),
        ('ad_compliance', 'AD Compliance'),
        ('sb_compliance', 'SB Compliance'),
    ]
    
    MAINTENANCE_STATUS = [
        ('scheduled', 'Scheduled'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('deferred', 'Deferred'),
        ('cancelled', 'Cancelled'),
    ]
    
    aircraft = models.ForeignKey(Aircraft, on_delete=models.CASCADE, related_name="maintenance_logs")
    
    # Maintenance details
    maintenance_type = models.CharField(max_length=20, choices=MAINTENANCE_TYPES)
    description = models.TextField()
    work_order_number = models.CharField(max_length=50, blank=True, null=True)
    
    # Scheduling
    scheduled_date = models.DateTimeField()
    started_date = models.DateTimeField(null=True, blank=True)
    completed_date = models.DateTimeField(null=True, blank=True)
    
    # Status and tracking
    status = models.CharField(max_length=20, choices=MAINTENANCE_STATUS, default='scheduled')
    priority = models.CharField(max_length=10, choices=[
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('critical', 'Critical')
    ], default='medium')
    
    # Personnel and costs
    technician = models.ForeignKey(
        'contacts.Contact', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name="maintenance_work"
    )
    estimated_hours = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    actual_hours = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    estimated_cost = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    actual_cost = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    
    # Compliance and documentation
    regulatory_reference = models.CharField(max_length=100, blank=True, null=True)
    compliance_due_date = models.DateField(null=True, blank=True)
    next_due_date = models.DateField(null=True, blank=True)
    
    # Parts and materials
    parts_used = models.JSONField(default=list, blank=True)
    
    # Documentation
    work_performed = models.TextField(blank=True, null=True)
    discrepancies_found = models.TextField(blank=True, null=True)
    corrective_action = models.TextField(blank=True, null=True)
    
    class Meta:
        indexes = [
            models.Index(fields=['aircraft', 'scheduled_date']),
            models.Index(fields=['status', 'priority']),
            models.Index(fields=['maintenance_type']),
            models.Index(fields=['compliance_due_date']),
        ]
        ordering = ['-scheduled_date']
    
    def __str__(self):
        return f"{self.aircraft.tail_number} - {self.get_maintenance_type_display()} - {self.scheduled_date.date()}"
    
    @property
    def is_overdue(self):
        """Check if maintenance is overdue."""
        if self.status in ['completed', 'cancelled']:
            return False
        
        from django.utils import timezone
        return self.scheduled_date < timezone.now()
    
    @property
    def duration_hours(self):
        """Calculate actual duration of maintenance work."""
        if self.started_date and self.completed_date:
            duration = self.completed_date - self.started_date
            return duration.total_seconds() / 3600
        return None


class AircraftDocument(BaseModel):
    """Documents associated with aircraft (certificates, manuals, etc.)."""
    
    DOCUMENT_TYPES = [
        ('certificate', 'Certificate'),
        ('manual', 'Manual'),
        ('logbook', 'Logbook'),
        ('inspection', 'Inspection Report'),
        ('insurance', 'Insurance'),
        ('registration', 'Registration'),
        ('other', 'Other'),
    ]
    
    aircraft = models.ForeignKey(Aircraft, on_delete=models.CASCADE, related_name="documents")
    document_type = models.CharField(max_length=20, choices=DOCUMENT_TYPES)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    
    # Document file reference
    document_file = models.ForeignKey(
        'documents.Document', 
        on_delete=models.CASCADE, 
        related_name="aircraft_documents"
    )
    
    # Validity and expiration
    issue_date = models.DateField(null=True, blank=True)
    expiration_date = models.DateField(null=True, blank=True)
    
    # Regulatory information
    issuing_authority = models.CharField(max_length=100, blank=True, null=True)
    document_number = models.CharField(max_length=100, blank=True, null=True)
    
    class Meta:
        indexes = [
            models.Index(fields=['aircraft', 'document_type']),
            models.Index(fields=['expiration_date']),
        ]
    
    def __str__(self):
        return f"{self.aircraft.tail_number} - {self.title}"
    
    @property
    def is_expired(self):
        """Check if document is expired."""
        if not self.expiration_date:
            return False
        
        from django.utils import timezone
        return self.expiration_date < timezone.now().date()
    
    @property
    def days_until_expiration(self):
        """Calculate days until document expires."""
        if not self.expiration_date:
            return None
        
        from django.utils import timezone
        delta = self.expiration_date - timezone.now().date()
        return delta.days

```


# File: aircraft/apps.py

```python
from django.apps import AppConfig


class AircraftConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'aircraft'
    verbose_name = 'Aircraft Management'

```


# File: aircraft/__init__.py

```python

```


# File: aircraft/admin.py

```python
"""
Admin configuration for aircraft app.
"""
from django.contrib import admin
from .models import Aircraft, MaintenanceLog


@admin.register(Aircraft)
class AircraftAdmin(admin.ModelAdmin):
    """Admin configuration for Aircraft model."""
    list_display = ('tail_number', 'aircraft_type', 'manufacturer', 'model', 'year_manufactured', 'is_active')
    list_filter = ('manufacturer', 'is_active', 'year_manufactured', 'created_at')
    search_fields = ('tail_number', 'aircraft_type', 'manufacturer', 'model', 'serial_number')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('tail_number', 'aircraft_type', 'manufacturer', 'model', 'serial_number', 'year_manufactured')
        }),
        ('Specifications', {
            'fields': ('max_passengers', 'max_range_nm', 'cruise_speed_kts', 'fuel_capacity_gallons')
        }),
        ('Weight & Balance', {
            'fields': ('empty_weight_lbs', 'max_takeoff_weight_lbs', 'max_landing_weight_lbs')
        }),
        ('Operational Details', {
            'fields': ('home_base', 'insurance_policy', 'registration_expiry', 'annual_inspection_due')
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )


@admin.register(MaintenanceLog)
class MaintenanceLogAdmin(admin.ModelAdmin):
    """Admin configuration for MaintenanceLog model."""
    list_display = ('aircraft', 'maintenance_type', 'date_performed', 'performed_by', 'cost', 'is_completed')
    list_filter = ('maintenance_type', 'is_completed', 'date_performed', 'created_at')
    search_fields = ('aircraft__tail_number', 'description', 'performed_by', 'part_numbers')
    readonly_fields = ('created_at', 'updated_at')
    date_hierarchy = 'date_performed'
    
    fieldsets = (
        ('Maintenance Information', {
            'fields': ('aircraft', 'maintenance_type', 'date_performed', 'performed_by')
        }),
        ('Details', {
            'fields': ('description', 'part_numbers', 'hours_at_maintenance', 'next_due_hours')
        }),
        ('Cost & Completion', {
            'fields': ('cost', 'is_completed', 'completion_notes')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )

```


# File: aircraft/services/aircraft_service.py

```python
from django.db.models import Q
from typing import List, Dict, Any, Optional
from decimal import Decimal
from datetime import datetime, timedelta

from aircraft.models import Aircraft, MaintenanceLog


class AircraftService:
    """Service class for Aircraft business logic."""
    
    def create_aircraft(self, aircraft_data: Dict[str, Any]) -> Aircraft:
        """Create a new aircraft with validation."""
        aircraft = Aircraft.objects.create(**aircraft_data)
        return aircraft
    
    def update_aircraft_status(self, aircraft_id: int, status: str) -> Aircraft:
        """Update aircraft status."""
        aircraft = Aircraft.objects.get(id=aircraft_id)
        aircraft.status = status
        aircraft.save()
        return aircraft
    
    def get_available_aircraft(self) -> List[Aircraft]:
        """Get all available aircraft."""
        return Aircraft.objects.filter(status='AVAILABLE')
    
    def search_aircraft_by_criteria(self, **criteria) -> List[Aircraft]:
        """Search aircraft by various criteria."""
        queryset = Aircraft.objects.all()
        
        if 'manufacturer' in criteria:
            queryset = queryset.filter(manufacturer=criteria['manufacturer'])
        
        if 'min_passengers' in criteria:
            queryset = queryset.filter(max_passengers__gte=criteria['min_passengers'])
        
        if 'min_range' in criteria:
            queryset = queryset.filter(range_nm__gte=criteria['min_range'])
        
        if 'aircraft_type' in criteria:
            queryset = queryset.filter(aircraft_type=criteria['aircraft_type'])
        
        return list(queryset)
    
    def check_range_capability(self, aircraft_id: int, distance_nm: float) -> bool:
        """Check if aircraft can fly the required distance."""
        aircraft = Aircraft.objects.get(id=aircraft_id)
        return aircraft.range_nm >= distance_nm
    
    def calculate_flight_time(self, aircraft_id: int, distance_nm: float) -> float:
        """Calculate flight time for given distance."""
        aircraft = Aircraft.objects.get(id=aircraft_id)
        return distance_nm / aircraft.cruise_speed
    
    def calculate_fuel_consumption(self, aircraft_id: int, distance_nm: float) -> float:
        """Calculate fuel consumption for given distance."""
        aircraft = Aircraft.objects.get(id=aircraft_id)
        # Simplified calculation - typically would use more complex formulas
        fuel_burn_rate = 200  # gallons per hour (example)
        flight_time = self.calculate_flight_time(aircraft_id, distance_nm)
        return fuel_burn_rate * flight_time
    
    def calculate_operating_cost(self, aircraft_id: int, flight_hours: float) -> Decimal:
        """Calculate operating cost for given flight hours."""
        aircraft = Aircraft.objects.get(id=aircraft_id)
        # Simplified cost calculation based on aircraft type
        cost_per_hour_map = {
            'Citation CJ3': Decimal('2500.00'),
            'King Air 350': Decimal('1800.00'),
            'Gulfstream G650': Decimal('6500.00'),
        }
        
        cost_per_hour = cost_per_hour_map.get(aircraft.aircraft_type, Decimal('3000.00'))
        return cost_per_hour * Decimal(str(flight_hours))
    
    def get_aircraft_specifications(self, aircraft_id: int) -> Dict[str, Any]:
        """Get detailed aircraft specifications."""
        aircraft = Aircraft.objects.get(id=aircraft_id)
        
        return {
            'performance': {
                'cruise_speed': aircraft.cruise_speed,
                'range_nm': aircraft.range_nm,
                'max_passengers': aircraft.max_passengers,
                'fuel_capacity': aircraft.fuel_capacity,
            },
            'dimensions': {
                'length': getattr(aircraft, 'length', None),
                'wingspan': getattr(aircraft, 'wingspan', None),
                'height': getattr(aircraft, 'height', None),
            },
            'weights': {
                'empty_weight': aircraft.empty_weight,
                'max_takeoff_weight': aircraft.max_takeoff_weight,
                'useful_load': aircraft.max_takeoff_weight - aircraft.empty_weight if aircraft.max_takeoff_weight and aircraft.empty_weight else None,
            }
        }


class MaintenanceService:
    """Service class for Aircraft Maintenance business logic."""
    
    def create_maintenance_log(self, maintenance_data: Dict[str, Any]) -> MaintenanceLog:
        """Create a new maintenance log."""
        maintenance_log = MaintenanceLog.objects.create(**maintenance_data)
        return maintenance_log
    
    def schedule_maintenance(self, aircraft_id: int, maintenance_type: str, 
                           description: str, scheduled_date: datetime, 
                           estimated_cost: Decimal = None) -> MaintenanceLog:
        """Schedule future maintenance."""
        aircraft = Aircraft.objects.get(id=aircraft_id)
        
        maintenance_log = MaintenanceLog.objects.create(
            aircraft=aircraft,
            maintenance_type=maintenance_type,
            description=description,
            maintenance_date=scheduled_date,
            cost=estimated_cost or Decimal('0.00'),
            status='SCHEDULED'
        )
        
        return maintenance_log
    
    def get_maintenance_history(self, aircraft_id: int) -> List[MaintenanceLog]:
        """Get maintenance history for an aircraft."""
        return MaintenanceLog.objects.filter(
            aircraft_id=aircraft_id
        ).order_by('-maintenance_date')
    
    def get_upcoming_maintenance(self, aircraft_id: int) -> List[MaintenanceLog]:
        """Get upcoming scheduled maintenance."""
        return MaintenanceLog.objects.filter(
            aircraft_id=aircraft_id,
            status='SCHEDULED',
            maintenance_date__gte=datetime.now().date()
        ).order_by('maintenance_date')
    
    def calculate_maintenance_costs(self, aircraft_id: int, start_date: datetime, 
                                  end_date: datetime) -> Decimal:
        """Calculate total maintenance costs for a period."""
        logs = MaintenanceLog.objects.filter(
            aircraft_id=aircraft_id,
            maintenance_date__range=[start_date, end_date],
            cost__isnull=False
        )
        
        total_cost = sum(log.cost for log in logs if log.cost)
        return Decimal(str(total_cost))
    
    def check_maintenance_due(self, aircraft_id: int, days_ahead: int = 30) -> bool:
        """Check if maintenance is due within specified days."""
        cutoff_date = datetime.now().date() + timedelta(days=days_ahead)
        
        return MaintenanceLog.objects.filter(
            aircraft_id=aircraft_id,
            next_due_date__lte=cutoff_date,
            status__in=['SCHEDULED', 'PENDING']
        ).exists()
    
    def update_maintenance_status(self, maintenance_log_id: int, status: str) -> MaintenanceLog:
        """Update maintenance status."""
        maintenance_log = MaintenanceLog.objects.get(id=maintenance_log_id)
        maintenance_log.status = status
        maintenance_log.save()
        return maintenance_log
    
    def complete_maintenance(self, maintenance_log_id: int, 
                           completion_data: Dict[str, Any]) -> MaintenanceLog:
        """Complete maintenance and update details."""
        maintenance_log = MaintenanceLog.objects.get(id=maintenance_log_id)
        
        maintenance_log.status = 'COMPLETED'
        maintenance_log.maintenance_date = datetime.now().date()
        
        for field, value in completion_data.items():
            setattr(maintenance_log, field, value)
        
        maintenance_log.save()
        return maintenance_log
    
    def generate_maintenance_report(self, aircraft_id: int, start_date: datetime, 
                                  end_date: datetime) -> Dict[str, Any]:
        """Generate maintenance report for a period."""
        logs = MaintenanceLog.objects.filter(
            aircraft_id=aircraft_id,
            maintenance_date__range=[start_date, end_date]
        ).order_by('-maintenance_date')
        
        total_cost = self.calculate_maintenance_costs(aircraft_id, start_date, end_date)
        
        return {
            'aircraft_id': aircraft_id,
            'period': {
                'start_date': start_date,
                'end_date': end_date
            },
            'maintenance_count': logs.count(),
            'total_cost': total_cost,
            'maintenance_logs': list(logs),
            'scheduled_count': logs.filter(maintenance_type='SCHEDULED').count(),
            'unscheduled_count': logs.filter(maintenance_type='UNSCHEDULED').count(),
        }

```


# File: aircraft/tests/test_models.py

```python
"""
Tests for aircraft app models.
"""
from django.test import TestCase
from django.core.exceptions import ValidationError
from decimal import Decimal
from aircraft.models import Aircraft, MaintenanceLog


class AircraftModelTest(TestCase):
    """Test cases for Aircraft model."""
    
    def test_aircraft_creation(self):
        """Test Aircraft creation with valid data."""
        aircraft = Aircraft.objects.create(
            tail_number='N123AB',
            aircraft_type='Citation CJ3',
            manufacturer='Cessna',
            model='Citation CJ3',
            year_manufactured=2020,
            max_passengers=8,
            max_range_nm=2040,
            cruise_speed_kts=417,
            fuel_capacity_gallons=Decimal('1560.00'),
            empty_weight_lbs=Decimal('10500.00'),
            max_takeoff_weight_lbs=Decimal('17110.00')
        )
        
        self.assertEqual(aircraft.tail_number, 'N123AB')
        self.assertEqual(aircraft.aircraft_type, 'Citation CJ3')
        self.assertEqual(aircraft.manufacturer, 'Cessna')
        self.assertEqual(aircraft.max_passengers, 8)
        self.assertTrue(aircraft.is_active)
        self.assertEqual(str(aircraft), 'N123AB - Citation CJ3')
        
    def test_aircraft_tail_number_validation(self):
        """Test Aircraft tail number validation."""
        aircraft = Aircraft(
            tail_number='',  # Empty tail number
            aircraft_type='Test Type',
            manufacturer='Test Mfg'
        )
        
        with self.assertRaises(ValidationError):
            aircraft.full_clean()
            
    def test_aircraft_unique_tail_number(self):
        """Test that tail numbers must be unique."""
        Aircraft.objects.create(
            tail_number='N123AB',
            aircraft_type='Type 1',
            manufacturer='Mfg 1'
        )
        
        with self.assertRaises(Exception):
            Aircraft.objects.create(
                tail_number='N123AB',
                aircraft_type='Type 2',
                manufacturer='Mfg 2'
            )


class MaintenanceLogModelTest(TestCase):
    """Test cases for MaintenanceLog model."""
    
    def setUp(self):
        """Set up test data."""
        self.aircraft = Aircraft.objects.create(
            tail_number='N456CD',
            aircraft_type='King Air 350',
            manufacturer='Beechcraft',
            model='King Air 350'
        )
        
    def test_maintenance_log_creation(self):
        """Test MaintenanceLog creation with valid data."""
        log = MaintenanceLog.objects.create(
            aircraft=self.aircraft,
            maintenance_type='inspection',
            description='100-hour inspection completed',
            performed_by='John Smith, A&P',
            cost=Decimal('2500.00'),
            hours_at_maintenance=Decimal('1250.5')
        )
        
        self.assertEqual(log.aircraft, self.aircraft)
        self.assertEqual(log.maintenance_type, 'inspection')
        self.assertEqual(log.description, '100-hour inspection completed')
        self.assertEqual(log.cost, Decimal('2500.00'))
        self.assertIsNotNone(log.date_performed)
        self.assertEqual(str(log), f'N456CD - inspection on {log.date_performed.strftime("%Y-%m-%d")}')
        
    def test_maintenance_log_aircraft_relationship(self):
        """Test MaintenanceLog aircraft relationship."""
        log1 = MaintenanceLog.objects.create(
            aircraft=self.aircraft,
            maintenance_type='repair',
            description='Engine repair'
        )
        
        log2 = MaintenanceLog.objects.create(
            aircraft=self.aircraft,
            maintenance_type='inspection',
            description='Annual inspection'
        )
        
        # Test reverse relationship
        logs = self.aircraft.maintenance_logs.all()
        self.assertEqual(logs.count(), 2)
        self.assertIn(log1, logs)
        self.assertIn(log2, logs)

```


# File: aircraft/tests/test_api.py

```python
from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from django.utils import timezone
from datetime import timedelta
from decimal import Decimal

from aircraft.models import Aircraft, MaintenanceLog


class AircraftAPITest(TestCase):
    """Test cases for Aircraft API endpoints."""
    
    def setUp(self):
        """Set up test data."""
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.force_authenticate(user=self.user)
        
        self.aircraft = Aircraft.objects.create(
            tail_number='N123AB',
            aircraft_type='Citation CJ3',
            manufacturer='Cessna',
            model='Citation CJ3',
            year=2020,
            max_passengers=8,
            range_nm=2040,
            cruise_speed=417,
            fuel_capacity=5562,
            empty_weight=11200,
            max_takeoff_weight=17110
        )
    
    def test_list_aircraft(self):
        """Test listing aircraft."""
        url = reverse('aircraft-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['tail_number'], 'N123AB')
    
    def test_create_aircraft(self):
        """Test creating an aircraft."""
        url = reverse('aircraft-list')
        data = {
            'tail_number': 'N456CD',
            'aircraft_type': 'King Air 350',
            'manufacturer': 'Beechcraft',
            'model': 'King Air 350',
            'year': 2019,
            'max_passengers': 11,
            'range_nm': 1806,
            'cruise_speed': 359,
            'fuel_capacity': 3621,
            'empty_weight': 9421,
            'max_takeoff_weight': 15000
        }
        
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['tail_number'], 'N456CD')
        self.assertEqual(response.data['manufacturer'], 'Beechcraft')
    
    def test_update_aircraft(self):
        """Test updating an aircraft."""
        url = reverse('aircraft-detail', kwargs={'pk': self.aircraft.pk})
        data = {
            'status': 'MAINTENANCE'
        }
        
        response = self.client.patch(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], 'MAINTENANCE')
    
    def test_delete_aircraft(self):
        """Test deleting an aircraft."""
        url = reverse('aircraft-detail', kwargs={'pk': self.aircraft.pk})
        response = self.client.delete(url)
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Aircraft.objects.filter(pk=self.aircraft.pk).exists())
    
    def test_filter_aircraft_by_status(self):
        """Test filtering aircraft by status."""
        # Create aircraft with different status
        Aircraft.objects.create(
            tail_number='N789EF',
            aircraft_type='Gulfstream G650',
            manufacturer='Gulfstream',
            model='G650',
            year=2021,
            max_passengers=14,
            range_nm=7000,
            cruise_speed=516,
            status='MAINTENANCE'
        )
        
        url = reverse('aircraft-list')
        response = self.client.get(url, {'status': 'AVAILABLE'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['status'], 'AVAILABLE')
    
    def test_search_aircraft_by_manufacturer(self):
        """Test searching aircraft by manufacturer."""
        # Create aircraft from different manufacturer
        Aircraft.objects.create(
            tail_number='N999XY',
            aircraft_type='King Air 350',
            manufacturer='Beechcraft',
            model='King Air 350',
            year=2018,
            max_passengers=11,
            range_nm=1806,
            cruise_speed=359
        )
        
        url = reverse('aircraft-list')
        response = self.client.get(url, {'manufacturer': 'Cessna'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['manufacturer'], 'Cessna')


class MaintenanceLogAPITest(TestCase):
    """Test cases for MaintenanceLog API endpoints."""
    
    def setUp(self):
        """Set up test data."""
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.force_authenticate(user=self.user)
        
        self.aircraft = Aircraft.objects.create(
            tail_number='N123AB',
            aircraft_type='Citation CJ3',
            manufacturer='Cessna',
            model='Citation CJ3',
            year=2020,
            max_passengers=8,
            range_nm=2040,
            cruise_speed=417
        )
        
        self.maintenance_log = MaintenanceLog.objects.create(
            aircraft=self.aircraft,
            maintenance_type='SCHEDULED',
            description='100-hour inspection',
            performed_by='Certified Mechanic',
            maintenance_date=timezone.now().date(),
            next_due_date=timezone.now().date() + timedelta(days=90),
            cost=Decimal('2500.00'),
            flight_hours_at_maintenance=100.5
        )
    
    def test_list_maintenance_logs(self):
        """Test listing maintenance logs."""
        url = reverse('maintenancelog-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['description'], '100-hour inspection')
    
    def test_create_maintenance_log(self):
        """Test creating a maintenance log."""
        url = reverse('maintenancelog-list')
        data = {
            'aircraft': self.aircraft.id,
            'maintenance_type': 'UNSCHEDULED',
            'description': 'Engine repair',
            'performed_by': 'Engine Specialist',
            'maintenance_date': timezone.now().date().isoformat(),
            'cost': '5000.00',
            'flight_hours_at_maintenance': 150.0
        }
        
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['description'], 'Engine repair')
        self.assertEqual(response.data['maintenance_type'], 'UNSCHEDULED')
    
    def test_update_maintenance_log(self):
        """Test updating a maintenance log."""
        url = reverse('maintenancelog-detail', kwargs={'pk': self.maintenance_log.pk})
        data = {
            'status': 'COMPLETED',
            'notes': 'Inspection completed successfully'
        }
        
        response = self.client.patch(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], 'COMPLETED')
        self.assertEqual(response.data['notes'], 'Inspection completed successfully')
    
    def test_filter_maintenance_logs_by_aircraft(self):
        """Test filtering maintenance logs by aircraft."""
        # Create another aircraft and maintenance log
        other_aircraft = Aircraft.objects.create(
            tail_number='N456CD',
            aircraft_type='King Air 350',
            manufacturer='Beechcraft',
            model='King Air 350',
            year=2019,
            max_passengers=11,
            range_nm=1806,
            cruise_speed=359
        )
        
        MaintenanceLog.objects.create(
            aircraft=other_aircraft,
            maintenance_type='SCHEDULED',
            description='Annual inspection',
            performed_by='Inspector',
            maintenance_date=timezone.now().date(),
            cost=Decimal('3000.00'),
            flight_hours_at_maintenance=200.0
        )
        
        url = reverse('maintenancelog-list')
        response = self.client.get(url, {'aircraft': self.aircraft.id})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['aircraft'], self.aircraft.id)
    
    def test_filter_maintenance_logs_by_type(self):
        """Test filtering maintenance logs by type."""
        # Create unscheduled maintenance log
        MaintenanceLog.objects.create(
            aircraft=self.aircraft,
            maintenance_type='UNSCHEDULED',
            description='Emergency repair',
            performed_by='Emergency Crew',
            maintenance_date=timezone.now().date(),
            cost=Decimal('1500.00'),
            flight_hours_at_maintenance=105.0
        )
        
        url = reverse('maintenancelog-list')
        response = self.client.get(url, {'maintenance_type': 'SCHEDULED'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['maintenance_type'], 'SCHEDULED')

```


# File: aircraft/tests/__init__.py

```python

```


# File: aircraft/tests/test_services.py

```python
from django.test import TestCase
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import datetime, timedelta, date
from decimal import Decimal
from unittest.mock import patch, Mock

from aircraft.models import Aircraft, MaintenanceLog
from aircraft.services.aircraft_service import AircraftService, MaintenanceService


class AircraftServiceTest(TestCase):
    """Test cases for AircraftService business logic."""
    
    def setUp(self):
        """Set up test data."""
        self.user = User.objects.create_user(username='testuser', password='testpass')
        
        self.aircraft = Aircraft.objects.create(
            tail_number='N123AB',
            aircraft_type='Citation CJ3',
            manufacturer='Cessna',
            model='Citation CJ3',
            year=2020,
            max_passengers=8,
            range_nm=2040,
            cruise_speed=417,
            fuel_capacity=5562,
            empty_weight=11200,
            max_takeoff_weight=17110
        )
        
        self.aircraft_service = AircraftService()
    
    def test_create_aircraft(self):
        """Test aircraft creation through service."""
        aircraft_data = {
            'tail_number': 'N456CD',
            'aircraft_type': 'King Air 350',
            'manufacturer': 'Beechcraft',
            'model': 'King Air 350',
            'year': 2019,
            'max_passengers': 11,
            'range_nm': 1806,
            'cruise_speed': 359,
            'fuel_capacity': 3621,
            'empty_weight': 9421,
            'max_takeoff_weight': 15000
        }
        
        aircraft = self.aircraft_service.create_aircraft(aircraft_data)
        
        self.assertIsNotNone(aircraft)
        self.assertEqual(aircraft.tail_number, 'N456CD')
        self.assertEqual(aircraft.manufacturer, 'Beechcraft')
        self.assertEqual(aircraft.max_passengers, 11)
    
    def test_update_aircraft_status(self):
        """Test aircraft status update."""
        updated_aircraft = self.aircraft_service.update_aircraft_status(
            self.aircraft.id, 
            'MAINTENANCE'
        )
        
        self.assertEqual(updated_aircraft.status, 'MAINTENANCE')
        
        # Refresh from database
        self.aircraft.refresh_from_db()
        self.assertEqual(self.aircraft.status, 'MAINTENANCE')
    
    def test_calculate_fuel_consumption(self):
        """Test fuel consumption calculation."""
        distance_nm = 1000
        fuel_consumption = self.aircraft_service.calculate_fuel_consumption(
            self.aircraft.id,
            distance_nm
        )
        
        self.assertIsInstance(fuel_consumption, float)
        self.assertGreater(fuel_consumption, 0)
    
    def test_check_range_capability(self):
        """Test aircraft range capability check."""
        # Test within range
        can_fly_1500 = self.aircraft_service.check_range_capability(
            self.aircraft.id,
            1500
        )
        self.assertTrue(can_fly_1500)
        
        # Test beyond range
        can_fly_3000 = self.aircraft_service.check_range_capability(
            self.aircraft.id,
            3000
        )
        self.assertFalse(can_fly_3000)
    
    def test_calculate_flight_time(self):
        """Test flight time calculation."""
        distance_nm = 1200
        flight_time = self.aircraft_service.calculate_flight_time(
            self.aircraft.id,
            distance_nm
        )
        
        expected_time = distance_nm / self.aircraft.cruise_speed
        self.assertAlmostEqual(flight_time, expected_time, places=2)
    
    def test_get_available_aircraft(self):
        """Test retrieving available aircraft."""
        # Create another aircraft
        Aircraft.objects.create(
            tail_number='N789EF',
            aircraft_type='Gulfstream G650',
            manufacturer='Gulfstream',
            model='G650',
            year=2021,
            max_passengers=14,
            range_nm=7000,
            cruise_speed=516,
            status='MAINTENANCE'
        )
        
        available_aircraft = self.aircraft_service.get_available_aircraft()
        
        # Only the first aircraft should be available (default status is AVAILABLE)
        self.assertEqual(len(available_aircraft), 1)
        self.assertEqual(available_aircraft[0].tail_number, 'N123AB')
    
    def test_search_aircraft_by_criteria(self):
        """Test aircraft search by various criteria."""
        # Create additional aircraft
        Aircraft.objects.create(
            tail_number='N999XY',
            aircraft_type='King Air 350',
            manufacturer='Beechcraft',
            model='King Air 350',
            year=2018,
            max_passengers=11,
            range_nm=1806,
            cruise_speed=359
        )
        
        # Search by manufacturer
        cessna_aircraft = self.aircraft_service.search_aircraft_by_criteria(
            manufacturer='Cessna'
        )
        self.assertEqual(len(cessna_aircraft), 1)
        self.assertEqual(cessna_aircraft[0].manufacturer, 'Cessna')
        
        # Search by minimum passenger capacity
        large_aircraft = self.aircraft_service.search_aircraft_by_criteria(
            min_passengers=10
        )
        self.assertEqual(len(large_aircraft), 1)
        self.assertEqual(large_aircraft[0].tail_number, 'N999XY')
        
        # Search by minimum range
        long_range_aircraft = self.aircraft_service.search_aircraft_by_criteria(
            min_range=2000
        )
        self.assertEqual(len(long_range_aircraft), 1)
        self.assertEqual(long_range_aircraft[0].tail_number, 'N123AB')
    
    def test_calculate_operating_cost(self):
        """Test operating cost calculation."""
        flight_hours = 2.5
        operating_cost = self.aircraft_service.calculate_operating_cost(
            self.aircraft.id,
            flight_hours
        )
        
        self.assertIsInstance(operating_cost, Decimal)
        self.assertGreater(operating_cost, Decimal('0'))
    
    def test_get_aircraft_specifications(self):
        """Test retrieving aircraft specifications."""
        specs = self.aircraft_service.get_aircraft_specifications(self.aircraft.id)
        
        self.assertIn('performance', specs)
        self.assertIn('dimensions', specs)
        self.assertIn('weights', specs)
        self.assertEqual(specs['performance']['cruise_speed'], 417)
        self.assertEqual(specs['performance']['range_nm'], 2040)


class MaintenanceServiceTest(TestCase):
    """Test cases for MaintenanceService business logic."""
    
    def setUp(self):
        """Set up test data."""
        self.user = User.objects.create_user(username='testuser', password='testpass')
        
        self.aircraft = Aircraft.objects.create(
            tail_number='N123AB',
            aircraft_type='Citation CJ3',
            manufacturer='Cessna',
            model='Citation CJ3',
            year=2020,
            max_passengers=8,
            range_nm=2040,
            cruise_speed=417
        )
        
        self.maintenance_log = MaintenanceLog.objects.create(
            aircraft=self.aircraft,
            maintenance_type='SCHEDULED',
            description='100-hour inspection',
            performed_by='Certified Mechanic',
            maintenance_date=timezone.now().date(),
            next_due_date=timezone.now().date() + timedelta(days=90),
            cost=Decimal('2500.00'),
            flight_hours_at_maintenance=100.5
        )
        
        self.maintenance_service = MaintenanceService()
    
    def test_create_maintenance_log(self):
        """Test maintenance log creation."""
        maintenance_data = {
            'aircraft': self.aircraft,
            'maintenance_type': 'UNSCHEDULED',
            'description': 'Engine repair',
            'performed_by': 'Engine Specialist',
            'maintenance_date': timezone.now().date(),
            'cost': Decimal('5000.00'),
            'flight_hours_at_maintenance': 150.0
        }
        
        log = self.maintenance_service.create_maintenance_log(maintenance_data)
        
        self.assertIsNotNone(log)
        self.assertEqual(log.maintenance_type, 'UNSCHEDULED')
        self.assertEqual(log.description, 'Engine repair')
        self.assertEqual(log.cost, Decimal('5000.00'))
    
    def test_schedule_maintenance(self):
        """Test maintenance scheduling."""
        scheduled_maintenance = self.maintenance_service.schedule_maintenance(
            aircraft_id=self.aircraft.id,
            maintenance_type='ANNUAL',
            description='Annual inspection',
            scheduled_date=timezone.now().date() + timedelta(days=30),
            estimated_cost=Decimal('3000.00')
        )
        
        self.assertIsNotNone(scheduled_maintenance)
        self.assertEqual(scheduled_maintenance.maintenance_type, 'ANNUAL')
        self.assertEqual(scheduled_maintenance.status, 'SCHEDULED')
    
    def test_get_maintenance_history(self):
        """Test retrieving maintenance history."""
        # Create additional maintenance log
        MaintenanceLog.objects.create(
            aircraft=self.aircraft,
            maintenance_type='UNSCHEDULED',
            description='Tire replacement',
            performed_by='Ground Crew',
            maintenance_date=timezone.now().date() - timedelta(days=30),
            cost=Decimal('800.00'),
            flight_hours_at_maintenance=85.0
        )
        
        history = self.maintenance_service.get_maintenance_history(self.aircraft.id)
        
        self.assertEqual(len(history), 2)
        # Should be ordered by maintenance_date descending
        self.assertEqual(history[0].description, '100-hour inspection')
        self.assertEqual(history[1].description, 'Tire replacement')
    
    def test_get_upcoming_maintenance(self):
        """Test retrieving upcoming maintenance."""
        # Create future maintenance
        MaintenanceLog.objects.create(
            aircraft=self.aircraft,
            maintenance_type='SCHEDULED',
            description='200-hour inspection',
            maintenance_date=timezone.now().date() + timedelta(days=60),
            next_due_date=timezone.now().date() + timedelta(days=150),
            status='SCHEDULED'
        )
        
        upcoming = self.maintenance_service.get_upcoming_maintenance(self.aircraft.id)
        
        self.assertEqual(len(upcoming), 1)
        self.assertEqual(upcoming[0].description, '200-hour inspection')
    
    def test_calculate_maintenance_costs(self):
        """Test maintenance cost calculation."""
        # Create additional maintenance logs
        MaintenanceLog.objects.create(
            aircraft=self.aircraft,
            maintenance_type='UNSCHEDULED',
            description='Repair work',
            performed_by='Mechanic',
            maintenance_date=timezone.now().date() - timedelta(days=30),
            cost=Decimal('1500.00'),
            flight_hours_at_maintenance=90.0
        )
        
        # Calculate costs for last 90 days
        start_date = timezone.now().date() - timedelta(days=90)
        end_date = timezone.now().date()
        
        total_cost = self.maintenance_service.calculate_maintenance_costs(
            self.aircraft.id,
            start_date,
            end_date
        )
        
        expected_cost = Decimal('2500.00') + Decimal('1500.00')  # Both logs within range
        self.assertEqual(total_cost, expected_cost)
    
    def test_check_maintenance_due(self):
        """Test checking if maintenance is due."""
        # Test with maintenance due soon
        self.maintenance_log.next_due_date = timezone.now().date() + timedelta(days=5)
        self.maintenance_log.save()
        
        is_due = self.maintenance_service.check_maintenance_due(
            self.aircraft.id,
            days_ahead=7
        )
        
        self.assertTrue(is_due)
        
        # Test with maintenance not due
        self.maintenance_log.next_due_date = timezone.now().date() + timedelta(days=30)
        self.maintenance_log.save()
        
        is_due = self.maintenance_service.check_maintenance_due(
            self.aircraft.id,
            days_ahead=7
        )
        
        self.assertFalse(is_due)
    
    def test_update_maintenance_status(self):
        """Test updating maintenance status."""
        # Create scheduled maintenance
        scheduled_maintenance = MaintenanceLog.objects.create(
            aircraft=self.aircraft,
            maintenance_type='SCHEDULED',
            description='Scheduled inspection',
            maintenance_date=timezone.now().date() + timedelta(days=7),
            status='SCHEDULED'
        )
        
        updated_maintenance = self.maintenance_service.update_maintenance_status(
            scheduled_maintenance.id,
            'IN_PROGRESS'
        )
        
        self.assertEqual(updated_maintenance.status, 'IN_PROGRESS')
    
    def test_complete_maintenance(self):
        """Test completing maintenance."""
        # Create in-progress maintenance
        in_progress_maintenance = MaintenanceLog.objects.create(
            aircraft=self.aircraft,
            maintenance_type='SCHEDULED',
            description='In progress inspection',
            maintenance_date=timezone.now().date(),
            status='IN_PROGRESS'
        )
        
        completion_data = {
            'performed_by': 'Senior Mechanic',
            'cost': Decimal('2000.00'),
            'flight_hours_at_maintenance': 120.0,
            'notes': 'Completed successfully'
        }
        
        completed_maintenance = self.maintenance_service.complete_maintenance(
            in_progress_maintenance.id,
            completion_data
        )
        
        self.assertEqual(completed_maintenance.status, 'COMPLETED')
        self.assertEqual(completed_maintenance.performed_by, 'Senior Mechanic')
        self.assertEqual(completed_maintenance.cost, Decimal('2000.00'))
    
    def test_generate_maintenance_report(self):
        """Test generating maintenance report."""
        # Create additional maintenance logs
        MaintenanceLog.objects.create(
            aircraft=self.aircraft,
            maintenance_type='UNSCHEDULED',
            description='Emergency repair',
            performed_by='Emergency Crew',
            maintenance_date=timezone.now().date() - timedelta(days=15),
            cost=Decimal('3000.00'),
            flight_hours_at_maintenance=95.0
        )
        
        start_date = timezone.now().date() - timedelta(days=30)
        end_date = timezone.now().date()
        
        report = self.maintenance_service.generate_maintenance_report(
            self.aircraft.id,
            start_date,
            end_date
        )
        
        self.assertIn('total_cost', report)
        self.assertIn('maintenance_count', report)
        self.assertIn('maintenance_logs', report)
        self.assertEqual(report['maintenance_count'], 2)
        self.assertEqual(report['total_cost'], Decimal('5500.00'))

```


# File: airports/models.py

```python
from django.db import models
from common.models import BaseModel
import math


class AirportType(models.TextChoices):
    """Airport type choices."""
    LARGE = 'large_airport', 'Large airport'
    MEDIUM = 'medium_airport', 'Medium airport'
    SMALL = 'small_airport', 'Small airport'


class Airport(BaseModel):
    """Airport model with location and operational data."""
    ident = models.CharField(max_length=10, unique=True, db_index=True)
    name = models.CharField(max_length=255)
    
    # Geographic coordinates
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    elevation = models.IntegerField(blank=True, null=True)
    
    # Location information
    iso_country = models.CharField(max_length=100)
    iso_region = models.CharField(max_length=100, blank=True, null=True)
    municipality = models.CharField(max_length=100, blank=True, null=True)
    
    # Airport codes
    icao_code = models.CharField(max_length=4, unique=True, db_index=True, blank=True, null=True)
    iata_code = models.CharField(max_length=3, db_index=True, blank=True, null=True)
    local_code = models.CharField(max_length=10, blank=True, null=True)
    gps_code = models.CharField(max_length=20, blank=True, null=True)
    
    # Airport classification
    airport_type = models.CharField(
        max_length=20,
        choices=AirportType.choices,
        default=AirportType.SMALL,
        db_index=True,
    )
    
    # Timezone for proper time calculations
    timezone = models.CharField(max_length=50)
    
    # Related services
    fbos = models.ManyToManyField('contacts.FBO', related_name="airports", blank=True)
    grounds = models.ManyToManyField('contacts.Ground', related_name="airports", blank=True)

    class Meta:
        indexes = [
            models.Index(fields=['ident']),
            models.Index(fields=['icao_code']),
            models.Index(fields=['iata_code']),
            models.Index(fields=['airport_type']),
            models.Index(fields=['iso_country']),
        ]

    def __str__(self):
        codes = []
        if self.icao_code:
            codes.append(self.icao_code)
        if self.iata_code:
            codes.append(self.iata_code)
        code_str = "/".join(codes) if codes else self.ident
        return f"{self.name} ({code_str})"
    
    @property
    def primary_code(self):
        """Return the primary airport code (ICAO preferred, then IATA, then ident)."""
        return self.icao_code or self.iata_code or self.ident
    
    def calculate_distance_to(self, other_airport):
        """
        Calculate great circle distance to another airport in nautical miles.
        
        Args:
            other_airport: Another Airport instance
            
        Returns:
            Distance in nautical miles
        """
        if not isinstance(other_airport, Airport):
            raise ValueError("other_airport must be an Airport instance")
        
        # Convert to radians
        lat1 = math.radians(float(self.latitude))
        lon1 = math.radians(float(self.longitude))
        lat2 = math.radians(float(other_airport.latitude))
        lon2 = math.radians(float(other_airport.longitude))
        
        # Haversine formula
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
        c = 2 * math.asin(math.sqrt(a))
        
        # Earth's radius in nautical miles
        earth_radius_nm = 3440.065
        
        return c * earth_radius_nm
    
    def get_nearby_airports(self, radius_nm=50):
        """
        Get airports within a specified radius.
        
        Args:
            radius_nm: Radius in nautical miles
            
        Returns:
            QuerySet of nearby airports
        """
        # This is a simplified implementation
        # In production, you'd use PostGIS or similar for efficient spatial queries
        nearby_airports = []
        
        for airport in Airport.objects.exclude(id=self.id):
            distance = self.calculate_distance_to(airport)
            if distance <= radius_nm:
                nearby_airports.append(airport.id)
        
        return Airport.objects.filter(id__in=nearby_airports)


class WeatherData(BaseModel):
    """Weather data for airports (from scraping services)."""
    airport = models.ForeignKey(Airport, on_delete=models.CASCADE, related_name="weather_data")
    
    # Weather conditions
    temperature_celsius = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    wind_speed_knots = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    wind_direction_degrees = models.IntegerField(null=True, blank=True)
    visibility_miles = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    
    # Pressure and humidity
    barometric_pressure_inhg = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    humidity_percent = models.IntegerField(null=True, blank=True)
    
    # Conditions
    conditions = models.CharField(max_length=100, blank=True, null=True)  # Clear, Cloudy, Rain, etc.
    ceiling_feet = models.IntegerField(null=True, blank=True)
    
    # Metadata
    observation_time = models.DateTimeField()
    source = models.CharField(max_length=50, default='METAR')  # METAR, TAF, etc.
    raw_data = models.TextField(blank=True, null=True)  # Original weather report
    
    class Meta:
        indexes = [
            models.Index(fields=['airport', 'observation_time']),
            models.Index(fields=['source']),
        ]
        ordering = ['-observation_time']
    
    def __str__(self):
        return f"Weather for {self.airport.primary_code} at {self.observation_time}"

```


# File: airports/apps.py

```python
from django.apps import AppConfig


class AirportsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'airports'
    verbose_name = 'Airport Management'

```


# File: airports/__init__.py

```python

```


# File: airports/admin.py

```python
"""
Admin configuration for airports app.
"""
from django.contrib import admin
from .models import Airport, WeatherData


@admin.register(Airport)
class AirportAdmin(admin.ModelAdmin):
    """Admin configuration for Airport model."""
    list_display = ('icao_code', 'iata_code', 'name', 'city', 'state', 'country', 'is_active')
    list_filter = ('country', 'state', 'is_active', 'created_at')
    search_fields = ('icao_code', 'iata_code', 'name', 'city', 'state', 'country')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Identification', {
            'fields': ('icao_code', 'iata_code', 'ident', 'name')
        }),
        ('Location', {
            'fields': ('city', 'state', 'country', 'latitude', 'longitude', 'elevation')
        }),
        ('Operational Details', {
            'fields': ('timezone', 'type', 'municipality', 'scheduled_service')
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )


@admin.register(WeatherData)
class WeatherDataAdmin(admin.ModelAdmin):
    """Admin configuration for WeatherData model."""
    list_display = ('airport', 'observation_time', 'temperature_c', 'wind_speed_kts', 'visibility_sm')
    list_filter = ('observation_time', 'created_at')
    search_fields = ('airport__icao_code', 'airport__name', 'metar_raw', 'taf_raw')
    readonly_fields = ('created_at', 'updated_at')
    date_hierarchy = 'observation_time'
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('airport', 'observation_time', 'data_source')
        }),
        ('Weather Conditions', {
            'fields': ('temperature_c', 'dewpoint_c', 'wind_direction_deg', 'wind_speed_kts', 'wind_gust_kts')
        }),
        ('Visibility & Pressure', {
            'fields': ('visibility_sm', 'altimeter_in_hg', 'conditions')
        }),
        ('Raw Data', {
            'fields': ('metar_raw', 'taf_raw'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )

```


# File: airports/services/__init__.py

```python

```


# File: airports/services/weather_scraper.py

```python
"""
Weather Data Scraper Service for Airport Operations

Moved from utils/webscraping/scrapers.py to airports/services/weather_scraper.py
This service handles fetching weather data for flight planning.
"""

import requests
from bs4 import BeautifulSoup
import logging
from django.utils import timezone
from ..models import Airport, WeatherData

logger = logging.getLogger(__name__)


class WeatherScrapingService:
    """
    Service for fetching weather data for flight planning
    """
    
    def __init__(self, base_url="https://aviationweather.gov"):
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'JET-ICU-Operations/1.0 (Weather Data Service)'
        })
    
    def get_metar(self, airport_code):
        """
        Fetch METAR (Meteorological Aerodrome Report) for a specific airport
        
        Args:
            airport_code: ICAO or IATA airport code
            
        Returns:
            str: METAR data or None if error
        """
        try:
            url = f"{self.base_url}/metar/data?ids={airport_code}&format=raw"
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            
            # Parse the response to extract METAR data
            metar_data = response.text.strip()
            
            if metar_data and not metar_data.startswith('No METAR'):
                logger.info(f"Successfully fetched METAR for {airport_code}")
                return metar_data
            else:
                logger.warning(f"No METAR data available for {airport_code}")
                return None
            
        except requests.RequestException as e:
            logger.error(f"Network error fetching METAR for {airport_code}: {str(e)}")
            return None
        except Exception as e:
            logger.error(f"Error fetching METAR for {airport_code}: {str(e)}")
            return None
    
    def get_taf(self, airport_code):
        """
        Fetch TAF (Terminal Aerodrome Forecast) for a specific airport
        
        Args:
            airport_code: ICAO or IATA airport code
            
        Returns:
            str: TAF data or None if error
        """
        try:
            url = f"{self.base_url}/taf/data?ids={airport_code}&format=raw"
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            
            # Parse the response to extract TAF data
            taf_data = response.text.strip()
            
            if taf_data and not taf_data.startswith('No TAF'):
                logger.info(f"Successfully fetched TAF for {airport_code}")
                return taf_data
            else:
                logger.warning(f"No TAF data available for {airport_code}")
                return None
            
        except requests.RequestException as e:
            logger.error(f"Network error fetching TAF for {airport_code}: {str(e)}")
            return None
        except Exception as e:
            logger.error(f"Error fetching TAF for {airport_code}: {str(e)}")
            return None
    
    def update_airport_weather(self, airport_code):
        """
        Update weather data for a specific airport and store in database
        
        Args:
            airport_code: ICAO or IATA airport code
            
        Returns:
            WeatherData instance or None if error
        """
        try:
            # Try to find airport by ICAO code first, then IATA
            airport = None
            try:
                airport = Airport.objects.get(icao_code=airport_code.upper())
            except Airport.DoesNotExist:
                try:
                    airport = Airport.objects.get(iata_code=airport_code.upper())
                except Airport.DoesNotExist:
                    logger.error(f"Airport not found: {airport_code}")
                    return None
            
            # Fetch weather data
            metar = self.get_metar(airport_code)
            taf = self.get_taf(airport_code)
            
            if not metar and not taf:
                logger.warning(f"No weather data available for {airport_code}")
                return None
            
            # Create or update weather data record
            weather_data, created = WeatherData.objects.update_or_create(
                airport=airport,
                defaults={
                    'metar': metar,
                    'taf': taf,
                    'last_updated': timezone.now(),
                    'data_source': 'aviationweather.gov'
                }
            )
            
            action = "Created" if created else "Updated"
            logger.info(f"{action} weather data for {airport.icao_code}")
            
            return weather_data
            
        except Exception as e:
            logger.error(f"Error updating weather data for {airport_code}: {str(e)}")
            return None
    
    def bulk_update_weather(self, airport_codes):
        """
        Update weather data for multiple airports
        
        Args:
            airport_codes: List of ICAO or IATA airport codes
            
        Returns:
            dict: Results summary with success/failure counts
        """
        results = {
            'success': 0,
            'failed': 0,
            'errors': []
        }
        
        for airport_code in airport_codes:
            try:
                weather_data = self.update_airport_weather(airport_code)
                if weather_data:
                    results['success'] += 1
                else:
                    results['failed'] += 1
                    results['errors'].append(f"Failed to update {airport_code}")
            except Exception as e:
                results['failed'] += 1
                results['errors'].append(f"Error updating {airport_code}: {str(e)}")
        
        logger.info(f"Bulk weather update completed: {results['success']} success, {results['failed']} failed")
        return results
    
    def get_weather_conditions(self, metar_string):
        """
        Parse METAR string to extract basic weather conditions
        
        Args:
            metar_string: Raw METAR string
            
        Returns:
            dict: Parsed weather conditions
        """
        if not metar_string:
            return {}
        
        conditions = {
            'visibility': None,
            'wind_speed': None,
            'wind_direction': None,
            'temperature': None,
            'conditions': []
        }
        
        try:
            parts = metar_string.split()
            
            for part in parts:
                # Wind information (e.g., 27008KT)
                if 'KT' in part and len(part) >= 5:
                    try:
                        wind_dir = part[:3]
                        wind_speed = part[3:5]
                        if wind_dir.isdigit():
                            conditions['wind_direction'] = int(wind_dir)
                        if wind_speed.isdigit():
                            conditions['wind_speed'] = int(wind_speed)
                    except (ValueError, IndexError):
                        pass
                
                # Temperature/Dewpoint (e.g., M02/M08)
                if '/' in part and len(part) <= 7:
                    try:
                        temp_part = part.split('/')[0]
                        if temp_part.startswith('M'):
                            temp = -int(temp_part[1:])
                        else:
                            temp = int(temp_part)
                        conditions['temperature'] = temp
                    except (ValueError, IndexError):
                        pass
                
                # Visibility (e.g., 10SM)
                if 'SM' in part:
                    try:
                        vis = part.replace('SM', '')
                        conditions['visibility'] = float(vis)
                    except ValueError:
                        pass
                
                # Weather conditions
                weather_codes = ['RA', 'SN', 'FG', 'BR', 'OVC', 'BKN', 'SCT', 'FEW', 'CLR']
                for code in weather_codes:
                    if code in part:
                        conditions['conditions'].append(code)
            
        except Exception as e:
            logger.error(f"Error parsing METAR: {str(e)}")
        
        return conditions


class AirportDataScrapingService:
    """
    Service for fetching airport data from public sources
    """
    
    def __init__(self, base_url="https://www.airport-data.com"):
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'JET-ICU-Operations/1.0 (Airport Data Service)'
        })
        
    def get_airport_info(self, airport_code):
        """
        Fetch information about a specific airport by its IATA/ICAO code
        
        Args:
            airport_code: IATA or ICAO airport code
            
        Returns:
            dict: Airport information or None if error
        """
        try:
            url = f"{self.base_url}/airports/{airport_code}"
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Extract airport data (this is a simplified example)
            airport_data = {
                'code': airport_code.upper(),
                'name': self._extract_name(soup),
                'location': self._extract_location(soup),
                'elevation': self._extract_elevation(soup),
                'coordinates': self._extract_coordinates(soup),
                'runways': self._extract_runways(soup)
            }
            
            logger.info(f"Successfully scraped airport data for {airport_code}")
            return airport_data
            
        except requests.RequestException as e:
            logger.error(f"Network error fetching airport data for {airport_code}: {str(e)}")
            return None
        except Exception as e:
            logger.error(f"Error fetching airport data for {airport_code}: {str(e)}")
            return None
    
    def _extract_name(self, soup):
        """Extract airport name from soup"""
        try:
            h1_tag = soup.find('h1')
            if h1_tag:
                return h1_tag.text.strip()
        except Exception:
            pass
        return None
    
    def _extract_location(self, soup):
        """Extract airport location from soup"""
        try:
            # Look for location information in various possible elements
            location_selectors = [
                '.airport-location',
                '.location',
                'td:contains("Location")',
                'th:contains("Location")'
            ]
            
            for selector in location_selectors:
                element = soup.select_one(selector)
                if element:
                    return element.text.strip()
        except Exception:
            pass
        return "Location data not available"
    
    def _extract_elevation(self, soup):
        """Extract airport elevation from soup"""
        try:
            # Look for elevation information
            elevation_selectors = [
                '.elevation',
                'td:contains("Elevation")',
                'th:contains("Elevation")'
            ]
            
            for selector in elevation_selectors:
                element = soup.select_one(selector)
                if element:
                    text = element.text.strip()
                    # Extract numeric elevation
                    import re
                    match = re.search(r'(\d+)', text)
                    if match:
                        return int(match.group(1))
        except Exception:
            pass
        return None
    
    def _extract_coordinates(self, soup):
        """Extract airport coordinates from soup"""
        try:
            # Look for coordinate information
            coord_selectors = [
                '.coordinates',
                'td:contains("Coordinates")',
                'th:contains("Coordinates")'
            ]
            
            for selector in coord_selectors:
                element = soup.select_one(selector)
                if element:
                    text = element.text.strip()
                    # Parse coordinates (simplified)
                    import re
                    lat_match = re.search(r'(\d+\.?\d*)[°\s]*N', text)
                    lon_match = re.search(r'(\d+\.?\d*)[°\s]*W', text)
                    
                    if lat_match and lon_match:
                        return {
                            'latitude': float(lat_match.group(1)),
                            'longitude': -float(lon_match.group(1))  # West is negative
                        }
        except Exception:
            pass
        return None
    
    def _extract_runways(self, soup):
        """Extract runway information from soup"""
        try:
            # Look for runway information
            runway_selectors = [
                '.runways',
                'td:contains("Runway")',
                'th:contains("Runway")'
            ]
            
            runways = []
            for selector in runway_selectors:
                elements = soup.select(selector)
                for element in elements:
                    text = element.text.strip()
                    if text and 'runway' in text.lower():
                        runways.append(text)
            
            return runways if runways else ["Runway data not available"]
        except Exception:
            pass
        return ["Runway data not available"]


# Convenience functions for backward compatibility
def get_metar(airport_code):
    """Get METAR data for an airport"""
    service = WeatherScrapingService()
    return service.get_metar(airport_code)


def get_taf(airport_code):
    """Get TAF data for an airport"""
    service = WeatherScrapingService()
    return service.get_taf(airport_code)


def update_airport_weather(airport_code):
    """Update weather data for an airport"""
    service = WeatherScrapingService()
    return service.update_airport_weather(airport_code)

```


# File: airports/services/airport_service.py

```python
"""
Airport service module containing business logic for airport operations.
"""
from django.db import transaction
from django.utils import timezone
from typing import List, Optional, Dict, Any
from datetime import datetime
import math

from ..models import Airport, WeatherData
from common.timezone_utils import convert_local_to_utc, convert_utc_to_local


class AirportService:
    """Service class for airport-related business logic."""
    
    @staticmethod
    def calculate_distance(airport1: Airport, airport2: Airport) -> float:
        """
        Calculate great circle distance between two airports in nautical miles.
        
        Args:
            airport1: First Airport instance
            airport2: Second Airport instance
            
        Returns:
            Distance in nautical miles
        """
        return airport1.calculate_distance_to(airport2)
    
    @staticmethod
    def convert_to_utc(local_datetime: datetime, airport_timezone: str) -> datetime:
        """
        Convert local airport time to UTC.
        
        Args:
            local_datetime: Local datetime
            airport_timezone: Airport timezone string
            
        Returns:
            UTC datetime
        """
        return convert_local_to_utc(local_datetime, airport_timezone)
    
    @staticmethod
    def convert_from_utc(utc_datetime: datetime, airport_timezone: str) -> datetime:
        """
        Convert UTC time to local airport time.
        
        Args:
            utc_datetime: UTC datetime
            airport_timezone: Airport timezone string
            
        Returns:
            Local datetime
        """
        return convert_utc_to_local(utc_datetime, airport_timezone)
    
    @staticmethod
    def find_airports_by_code(code: str) -> List[Airport]:
        """
        Find airports by ICAO, IATA, or identifier code.
        
        Args:
            code: Airport code to search for
            
        Returns:
            List of matching airports
        """
        code_upper = code.upper()
        
        airports = Airport.objects.filter(
            models.Q(icao_code__iexact=code_upper) |
            models.Q(iata_code__iexact=code_upper) |
            models.Q(ident__iexact=code_upper)
        ).distinct()
        
        return list(airports)
    
    @staticmethod
    def search_airports(query: str, limit: int = 20) -> List[Airport]:
        """
        Search airports by name, code, or location.
        
        Args:
            query: Search query
            limit: Maximum number of results
            
        Returns:
            List of matching airports
        """
        from django.db import models
        
        query_upper = query.upper()
        
        airports = Airport.objects.filter(
            models.Q(name__icontains=query) |
            models.Q(municipality__icontains=query) |
            models.Q(icao_code__icontains=query_upper) |
            models.Q(iata_code__icontains=query_upper) |
            models.Q(ident__icontains=query_upper)
        ).distinct()[:limit]
        
        return list(airports)
    
    @staticmethod
    def get_airports_in_region(country: str, region: Optional[str] = None) -> List[Airport]:
        """
        Get airports in a specific country or region.
        
        Args:
            country: ISO country code
            region: Optional ISO region code
            
        Returns:
            List of airports in the region
        """
        queryset = Airport.objects.filter(iso_country=country)
        
        if region:
            queryset = queryset.filter(iso_region=region)
        
        return list(queryset.order_by('name'))
    
    @staticmethod
    def calculate_flight_path(
        origin: Airport,
        destination: Airport,
        waypoints: Optional[List[Airport]] = None
    ) -> Dict[str, Any]:
        """
        Calculate flight path information between airports.
        
        Args:
            origin: Origin airport
            destination: Destination airport
            waypoints: Optional list of waypoint airports
            
        Returns:
            Dictionary with flight path information
        """
        total_distance = 0
        legs = []
        
        if waypoints:
            # Calculate distance through waypoints
            current_airport = origin
            
            for waypoint in waypoints:
                leg_distance = AirportService.calculate_distance(current_airport, waypoint)
                legs.append({
                    'from': current_airport,
                    'to': waypoint,
                    'distance_nm': leg_distance
                })
                total_distance += leg_distance
                current_airport = waypoint
            
            # Final leg to destination
            final_leg_distance = AirportService.calculate_distance(current_airport, destination)
            legs.append({
                'from': current_airport,
                'to': destination,
                'distance_nm': final_leg_distance
            })
            total_distance += final_leg_distance
        else:
            # Direct flight
            total_distance = AirportService.calculate_distance(origin, destination)
            legs.append({
                'from': origin,
                'to': destination,
                'distance_nm': total_distance
            })
        
        return {
            'origin': origin,
            'destination': destination,
            'waypoints': waypoints or [],
            'legs': legs,
            'total_distance_nm': total_distance,
            'estimated_flight_time_hours': AirportService._estimate_flight_time(total_distance)
        }
    
    @staticmethod
    def _estimate_flight_time(distance_nm: float, aircraft_speed_knots: float = 400) -> float:
        """
        Estimate flight time based on distance and average speed.
        
        Args:
            distance_nm: Distance in nautical miles
            aircraft_speed_knots: Average aircraft speed in knots
            
        Returns:
            Estimated flight time in hours
        """
        return distance_nm / aircraft_speed_knots


class WeatherService:
    """Service class for weather-related operations."""
    
    @staticmethod
    def get_current_weather(airport: Airport) -> Optional[WeatherData]:
        """
        Get the most recent weather data for an airport.
        
        Args:
            airport: Airport instance
            
        Returns:
            Most recent WeatherData or None
        """
        return airport.weather_data.first()  # Already ordered by -observation_time
    
    @staticmethod
    def get_weather_history(
        airport: Airport,
        hours_back: int = 24
    ) -> List[WeatherData]:
        """
        Get weather history for an airport.
        
        Args:
            airport: Airport instance
            hours_back: Number of hours to look back
            
        Returns:
            List of WeatherData instances
        """
        cutoff_time = timezone.now() - timezone.timedelta(hours=hours_back)
        
        return list(airport.weather_data.filter(
            observation_time__gte=cutoff_time
        ))
    
    @staticmethod
    def store_weather_data(
        airport: Airport,
        weather_info: Dict[str, Any],
        source: str = 'METAR'
    ) -> WeatherData:
        """
        Store weather data for an airport.
        
        Args:
            airport: Airport instance
            weather_info: Dictionary with weather information
            source: Weather data source
            
        Returns:
            Created WeatherData instance
        """
        return WeatherData.objects.create(
            airport=airport,
            temperature_celsius=weather_info.get('temperature_celsius'),
            wind_speed_knots=weather_info.get('wind_speed_knots'),
            wind_direction_degrees=weather_info.get('wind_direction_degrees'),
            visibility_miles=weather_info.get('visibility_miles'),
            barometric_pressure_inhg=weather_info.get('barometric_pressure_inhg'),
            humidity_percent=weather_info.get('humidity_percent'),
            conditions=weather_info.get('conditions'),
            ceiling_feet=weather_info.get('ceiling_feet'),
            observation_time=weather_info.get('observation_time', timezone.now()),
            source=source,
            raw_data=weather_info.get('raw_data')
        )
    
    @staticmethod
    def analyze_weather_conditions(weather_data: WeatherData) -> Dict[str, Any]:
        """
        Analyze weather conditions for flight operations.
        
        Args:
            weather_data: WeatherData instance
            
        Returns:
            Dictionary with weather analysis
        """
        analysis = {
            'suitable_for_flight': True,
            'warnings': [],
            'conditions_summary': weather_data.conditions or 'Unknown'
        }
        
        # Check visibility
        if weather_data.visibility_miles and weather_data.visibility_miles < 3:
            analysis['suitable_for_flight'] = False
            analysis['warnings'].append('Low visibility')
        
        # Check wind conditions
        if weather_data.wind_speed_knots and weather_data.wind_speed_knots > 35:
            analysis['suitable_for_flight'] = False
            analysis['warnings'].append('High winds')
        
        # Check ceiling
        if weather_data.ceiling_feet and weather_data.ceiling_feet < 1000:
            analysis['warnings'].append('Low ceiling')
        
        # Check for severe weather conditions
        severe_conditions = ['thunderstorm', 'tornado', 'hail', 'freezing']
        if weather_data.conditions:
            for condition in severe_conditions:
                if condition.lower() in weather_data.conditions.lower():
                    analysis['suitable_for_flight'] = False
                    analysis['warnings'].append(f'Severe weather: {condition}')
        
        return analysis

```


# File: airports/tests/test_weather_scraper.py

```python
"""
Django test cases for weather scraping functionality.

Converted from custom test scripts to proper Django TestCase.
"""

from django.test import TestCase
from unittest.mock import patch, Mock
from airports.models import Airport, WeatherData
from airports.services.weather_scraper import WeatherScrapingService, AirportDataScrapingService


class WeatherScrapingTestCase(TestCase):
    """Test case for weather scraping functionality."""
    
    def setUp(self):
        """Set up test data for weather scraping tests."""
        self.airport = Airport.objects.create(
            name="Los Angeles International Airport",
            iata_code="LAX",
            icao_code="KLAX",
            city="Los Angeles",
            state="CA",
            country="USA",
            latitude=33.942536,
            longitude=-118.408074,
            timezone="America/Los_Angeles"
        )
        
        self.weather_service = WeatherScrapingService()
        self.airport_service = AirportDataScrapingService()
    
    @patch('airports.services.weather_scraper.requests.Session.get')
    def test_metar_fetching_success(self, mock_get):
        """Test successful METAR data fetching."""
        # Mock successful response
        mock_response = Mock()
        mock_response.text = "KLAX 121953Z 25008KT 10SM FEW015 SCT250 22/18 A2995 RMK AO2 SLP141 T02220183"
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        
        # Test METAR fetching
        metar = self.weather_service.get_metar("KLAX")
        
        # Assertions
        self.assertIsNotNone(metar)
        self.assertIn("KLAX", metar)
        self.assertIn("25008KT", metar)
        mock_get.assert_called_once()
    
    @patch('airports.services.weather_scraper.requests.Session.get')
    def test_metar_fetching_no_data(self, mock_get):
        """Test METAR fetching when no data is available."""
        # Mock no data response
        mock_response = Mock()
        mock_response.text = "No METAR available"
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        
        # Test METAR fetching
        metar = self.weather_service.get_metar("INVALID")
        
        # Assertions
        self.assertIsNone(metar)
    
    @patch('airports.services.weather_scraper.requests.Session.get')
    def test_taf_fetching_success(self, mock_get):
        """Test successful TAF data fetching."""
        # Mock successful response
        mock_response = Mock()
        mock_response.text = "KLAX 121720Z 1218/1324 25008KT P6SM FEW015 SCT250"
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        
        # Test TAF fetching
        taf = self.weather_service.get_taf("KLAX")
        
        # Assertions
        self.assertIsNotNone(taf)
        self.assertIn("KLAX", taf)
        self.assertIn("25008KT", taf)
    
    @patch('airports.services.weather_scraper.requests.Session.get')
    def test_weather_update_success(self, mock_get):
        """Test successful weather data update for airport."""
        # Mock successful responses for both METAR and TAF
        mock_response = Mock()
        mock_response.text = "KLAX 121953Z 25008KT 10SM FEW015 SCT250 22/18 A2995"
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        
        # Test weather update
        weather_data = self.weather_service.update_airport_weather("KLAX")
        
        # Assertions
        self.assertIsNotNone(weather_data)
        self.assertEqual(weather_data.airport, self.airport)
        self.assertIsNotNone(weather_data.metar)
        self.assertEqual(weather_data.data_source, 'aviationweather.gov')
        
        # Verify database record was created
        self.assertTrue(WeatherData.objects.filter(airport=self.airport).exists())
    
    def test_weather_update_nonexistent_airport(self):
        """Test weather update for non-existent airport."""
        weather_data = self.weather_service.update_airport_weather("INVALID")
        self.assertIsNone(weather_data)
    
    @patch('airports.services.weather_scraper.WeatherScrapingService.update_airport_weather')
    def test_bulk_weather_update(self, mock_update):
        """Test bulk weather update functionality."""
        # Mock successful updates
        mock_update.side_effect = [Mock(), None, Mock()]  # 2 success, 1 failure
        
        # Test bulk update
        results = self.weather_service.bulk_update_weather(["KLAX", "INVALID", "KJFK"])
        
        # Assertions
        self.assertEqual(results['success'], 2)
        self.assertEqual(results['failed'], 1)
        self.assertEqual(len(results['errors']), 1)
        self.assertEqual(mock_update.call_count, 3)
    
    def test_metar_parsing(self):
        """Test METAR string parsing functionality."""
        metar_string = "KLAX 121953Z 25008KT 10SM FEW015 SCT250 22/18 A2995"
        
        conditions = self.weather_service.get_weather_conditions(metar_string)
        
        # Assertions
        self.assertEqual(conditions['wind_direction'], 250)
        self.assertEqual(conditions['wind_speed'], 8)
        self.assertEqual(conditions['temperature'], 22)
        self.assertEqual(conditions['visibility'], 10.0)
        self.assertIn('FEW', conditions['conditions'])
        self.assertIn('SCT', conditions['conditions'])
    
    def test_metar_parsing_negative_temperature(self):
        """Test METAR parsing with negative temperature."""
        metar_string = "KLAX 121953Z 25008KT 10SM CLR M05/M10 A2995"
        
        conditions = self.weather_service.get_weather_conditions(metar_string)
        
        # Assertions
        self.assertEqual(conditions['temperature'], -5)
        self.assertIn('CLR', conditions['conditions'])
    
    def test_metar_parsing_empty_string(self):
        """Test METAR parsing with empty string."""
        conditions = self.weather_service.get_weather_conditions("")
        
        # Should return empty dict
        self.assertEqual(conditions, {})
    
    @patch('airports.services.weather_scraper.requests.Session.get')
    def test_network_error_handling(self, mock_get):
        """Test network error handling."""
        # Mock network error
        mock_get.side_effect = Exception("Network error")
        
        # Test METAR fetching with error
        metar = self.weather_service.get_metar("KLAX")
        self.assertIsNone(metar)
        
        # Test TAF fetching with error
        taf = self.weather_service.get_taf("KLAX")
        self.assertIsNone(taf)


class AirportDataScrapingTestCase(TestCase):
    """Test case for airport data scraping functionality."""
    
    def setUp(self):
        """Set up test data for airport data scraping tests."""
        self.airport_service = AirportDataScrapingService()
    
    @patch('airports.services.weather_scraper.requests.Session.get')
    def test_airport_info_scraping_success(self, mock_get):
        """Test successful airport information scraping."""
        # Mock HTML response
        mock_response = Mock()
        mock_response.text = """
        <html>
            <h1>Los Angeles International Airport</h1>
            <div class="location">Los Angeles, CA, USA</div>
            <div class="elevation">125 ft</div>
        </html>
        """
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        
        # Test airport info scraping
        airport_data = self.airport_service.get_airport_info("LAX")
        
        # Assertions
        self.assertIsNotNone(airport_data)
        self.assertEqual(airport_data['code'], 'LAX')
        self.assertEqual(airport_data['name'], 'Los Angeles International Airport')
        mock_get.assert_called_once()
    
    @patch('airports.services.weather_scraper.requests.Session.get')
    def test_airport_info_scraping_error(self, mock_get):
        """Test airport information scraping with network error."""
        # Mock network error
        mock_get.side_effect = Exception("Network error")
        
        # Test airport info scraping
        airport_data = self.airport_service.get_airport_info("LAX")
        
        # Assertions
        self.assertIsNone(airport_data)
    
    def test_coordinate_extraction(self):
        """Test coordinate extraction from HTML."""
        from bs4 import BeautifulSoup
        
        html = """
        <div class="coordinates">33.942536°N 118.408074°W</div>
        """
        soup = BeautifulSoup(html, 'html.parser')
        
        coordinates = self.airport_service._extract_coordinates(soup)
        
        # Note: This is a simplified test - actual implementation may vary
        # based on the website structure
        if coordinates:
            self.assertIsInstance(coordinates, dict)
            self.assertIn('latitude', coordinates)
            self.assertIn('longitude', coordinates)
    
    def test_elevation_extraction(self):
        """Test elevation extraction from HTML."""
        from bs4 import BeautifulSoup
        
        html = """
        <div class="elevation">125 ft MSL</div>
        """
        soup = BeautifulSoup(html, 'html.parser')
        
        elevation = self.airport_service._extract_elevation(soup)
        
        # Should extract numeric elevation
        if elevation:
            self.assertEqual(elevation, 125)

```


# File: airports/tests/__init__.py

```python

```


# File: maintenance/models.py

```python
from django.db import models


class Aircraft(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('maintenance', 'In Maintenance'),
        ('grounded', 'Grounded'),
    ]
    
    registration = models.CharField(max_length=20, unique=True)
    aircraft_type = models.CharField(max_length=100)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    last_maintenance_date = models.DateField(null=True, blank=True)
    next_maintenance_date = models.DateField(null=True, blank=True)
    total_flight_hours = models.FloatField(default=0)
    manufacturing_date = models.DateField(null=True, blank=True)
    capacity = models.IntegerField(default=0)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.registration} - {self.aircraft_type}"


class MaintenanceLog(models.Model):
    aircraft = models.ForeignKey(Aircraft, on_delete=models.CASCADE, related_name='maintenance_logs')
    maintenance_date = models.DateField()
    description = models.TextField()
    performed_by = models.CharField(max_length=100)
    hours_spent = models.FloatField(default=0)
    parts_replaced = models.TextField(blank=True)
    is_scheduled = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.aircraft.registration} - {self.maintenance_date}"

```


# File: maintenance/serializers.py

```python
from rest_framework import serializers
from .models import Aircraft, MaintenanceLog


class MaintenanceLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = MaintenanceLog
        fields = '__all__'


class AircraftSerializer(serializers.ModelSerializer):
    maintenance_logs = MaintenanceLogSerializer(many=True, read_only=True)
    
    class Meta:
        model = Aircraft
        fields = '__all__'


class AircraftStatusUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Aircraft
        fields = ['status', 'notes']

```


# File: maintenance/views.py

```python
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Aircraft, MaintenanceLog
from .serializers import AircraftSerializer, MaintenanceLogSerializer, AircraftStatusUpdateSerializer


class AircraftViewSet(viewsets.ModelViewSet):
    queryset = Aircraft.objects.all()
    serializer_class = AircraftSerializer
    
    @action(detail=True, methods=['patch'])
    def update_status(self, request, pk=None):
        aircraft = self.get_object()
        serializer = AircraftStatusUpdateSerializer(aircraft, data=request.data, partial=True)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MaintenanceLogViewSet(viewsets.ModelViewSet):
    queryset = MaintenanceLog.objects.all()
    serializer_class = MaintenanceLogSerializer
    
    def get_queryset(self):
        queryset = MaintenanceLog.objects.all()
        aircraft_id = self.request.query_params.get('aircraft_id')
        
        if aircraft_id:
            queryset = queryset.filter(aircraft_id=aircraft_id)
        
        return queryset

```


# File: maintenance/apps.py

```python
from django.apps import AppConfig


class MaintenanceConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'maintenance'

```


# File: maintenance/__init__.py

```python


```


# File: maintenance/urls.py

```python
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AircraftViewSet, MaintenanceLogViewSet

router = DefaultRouter()
router.register(r'aircraft', AircraftViewSet)
router.register(r'logs', MaintenanceLogViewSet)

urlpatterns = [
    path('', include(router.urls)),
]

```


# File: maintenance/admin.py

```python
from django.contrib import admin
from .models import Aircraft, MaintenanceLog

admin.site.register(Aircraft)
admin.site.register(MaintenanceLog)

```


# File: users/models.py

```python
from django.db import models
from django.contrib.auth.models import User
from common.models import BaseModel


class Permission(BaseModel):
    """Permission model for fine-grained access control."""
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    
    class Meta:
        indexes = [
            models.Index(fields=['name']),
        ]
    
    def __str__(self):
        return self.name


class Role(BaseModel):
    """Role model for grouping permissions."""
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    permissions = models.ManyToManyField(Permission, related_name="roles")
    
    class Meta:
        indexes = [
            models.Index(fields=['name']),
        ]
    
    def __str__(self):
        return self.name


class Department(BaseModel):
    """Department model for organizational structure."""
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    permission_ids = models.ManyToManyField(Permission, related_name="departments")
    
    class Meta:
        indexes = [
            models.Index(fields=['name']),
        ]
    
    def __str__(self):
        return self.name


class UserProfile(BaseModel):
    """Extended user profile with additional fields and relationships."""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    department_ids = models.ManyToManyField(Department, related_name="users")
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    
    # Address information
    address_line1 = models.CharField(max_length=255, blank=True, null=True)
    address_line2 = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    zip = models.CharField(max_length=20, blank=True, null=True)
    
    # Role and department relationships
    roles = models.ManyToManyField(Role, related_name="users")
    departments = models.ManyToManyField(Department, related_name="department_users")
    
    # Additional metadata
    flags = models.JSONField(default=list, blank=True)
    
    class Meta:
        indexes = [
            models.Index(fields=['user']),
            models.Index(fields=['email']),
        ]
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
    @property
    def full_name(self):
        """Return full name of the user."""
        return f"{self.first_name} {self.last_name}".strip()
    
    def has_permission(self, permission_name):
        """Check if user has a specific permission through roles."""
        return self.roles.filter(permissions__name=permission_name).exists()
    
    def get_all_permissions(self):
        """Get all permissions for this user through roles."""
        return Permission.objects.filter(roles__users=self).distinct()


class Staff(BaseModel):
    """Staff model for operational crew members."""
    contact = models.OneToOneField("contacts.Contact", on_delete=models.CASCADE, related_name="staff")
    active = models.BooleanField(default=True)
    notes = models.TextField(blank=True)
    
    class Meta:
        indexes = [
            models.Index(fields=['active']),
        ]
    
    def __str__(self):
        return f"{self.contact.first_name} {self.contact.last_name}".strip() or str(self.contact_id)


class StaffRole(BaseModel):
    """Staff role model for operational positions."""
    code = models.CharField(max_length=32, unique=True)   # e.g., 'PIC', 'SIC', 'RN', 'PARAMEDIC'
    name = models.CharField(max_length=64)                # e.g., 'Pilot in Command'
    
    class Meta:
        indexes = [
            models.Index(fields=["code"]),
        ]
    
    def __str__(self):
        return self.code


class StaffRoleMembership(BaseModel):
    """Staff role membership with time periods."""
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE, related_name="role_memberships")
    role = models.ForeignKey(StaffRole, on_delete=models.PROTECT, related_name="memberships")
    start_on = models.DateField(null=True, blank=True)
    end_on = models.DateField(null=True, blank=True)
    
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["staff", "role", "start_on", "end_on"],
                name="uniq_staff_role_interval"
            )
        ]
        indexes = [
            models.Index(fields=['staff', 'role']),
            models.Index(fields=['start_on', 'end_on']),
        ]
    
    def __str__(self):
        return f"{self.staff} - {self.role}"

```


# File: users/apps.py

```python
from django.apps import AppConfig


class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'
    verbose_name = 'User Management'

```


# File: users/__init__.py

```python

```


# File: users/admin.py

```python
"""
Admin configuration for users app.
"""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import UserProfile, Role, Permission, Department


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    """Admin configuration for UserProfile model."""
    list_display = ('user', 'department', 'phone_number', 'hire_date', 'is_active')
    list_filter = ('department', 'is_active', 'hire_date')
    search_fields = ('user__username', 'user__first_name', 'user__last_name', 'phone_number')
    filter_horizontal = ('roles', 'permissions')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('User Information', {
            'fields': ('user', 'department', 'phone_number', 'address')
        }),
        ('Employment', {
            'fields': ('hire_date', 'emergency_contact', 'is_active')
        }),
        ('Permissions', {
            'fields': ('roles', 'permissions')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    """Admin configuration for Role model."""
    list_display = ('name', 'description', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('name', 'description')
    readonly_fields = ('created_at', 'updated_at')


@admin.register(Permission)
class PermissionAdmin(admin.ModelAdmin):
    """Admin configuration for Permission model."""
    list_display = ('name', 'resource', 'action', 'description')
    list_filter = ('resource', 'action')
    search_fields = ('name', 'resource', 'action', 'description')
    readonly_fields = ('created_at', 'updated_at')


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    """Admin configuration for Department model."""
    list_display = ('name', 'manager_email', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('name', 'description', 'manager_email')
    readonly_fields = ('created_at', 'updated_at')


# Extend the default User admin to show related profile info
class UserProfileInline(admin.StackedInline):
    """Inline admin for UserProfile."""
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Profile'
    filter_horizontal = ('roles', 'permissions')


class UserAdmin(BaseUserAdmin):
    """Extended User admin with profile inline."""
    inlines = (UserProfileInline,)
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'get_department')
    
    def get_department(self, obj):
        """Get user's department from profile."""
        try:
            return obj.userprofile.department.name if obj.userprofile.department else 'No Department'
        except UserProfile.DoesNotExist:
            return 'No Profile'
    get_department.short_description = 'Department'


# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)

```


# File: users/services/user_service.py

```python
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db.models import Q
from typing import List, Dict, Any, Optional

from users.models import UserProfile, Role, Permission, Department


class UserService:
    """Service class for User management business logic."""
    
    def create_user_with_profile(self, user_data: Dict[str, Any], 
                                profile_data: Dict[str, Any]) -> User:
        """Create a new user with associated profile."""
        # Create user
        user = User.objects.create_user(
            username=user_data['username'],
            email=user_data['email'],
            password=user_data['password'],
            first_name=user_data.get('first_name', ''),
            last_name=user_data.get('last_name', '')
        )
        
        # Create profile
        profile_data['user'] = user
        UserProfile.objects.create(**profile_data)
        
        return user
    
    def update_user_profile(self, user_id: int, profile_data: Dict[str, Any]) -> UserProfile:
        """Update user profile information."""
        profile = UserProfile.objects.get(user_id=user_id)
        
        for field, value in profile_data.items():
            if field != 'user':  # Don't allow changing user reference
                setattr(profile, field, value)
        
        profile.full_clean()
        profile.save()
        return profile
    
    def assign_role_to_user(self, user_id: int, role_id: int) -> UserProfile:
        """Assign a role to a user."""
        profile = UserProfile.objects.get(user_id=user_id)
        role = Role.objects.get(id=role_id)
        
        profile.roles.add(role)
        return profile
    
    def remove_role_from_user(self, user_id: int, role_id: int) -> UserProfile:
        """Remove a role from a user."""
        profile = UserProfile.objects.get(user_id=user_id)
        role = Role.objects.get(id=role_id)
        
        profile.roles.remove(role)
        return profile
    
    def get_user_permissions(self, user_id: int) -> List[Permission]:
        """Get all permissions for a user through their roles."""
        profile = UserProfile.objects.get(user_id=user_id)
        permissions = []
        
        for role in profile.roles.all():
            permissions.extend(role.permissions.all())
        
        # Remove duplicates
        return list(set(permissions))
    
    def check_user_permission(self, user_id: int, permission_name: str) -> bool:
        """Check if user has a specific permission."""
        permissions = self.get_user_permissions(user_id)
        return any(perm.name == permission_name for perm in permissions)
    
    def search_users(self, query: str) -> List[User]:
        """Search users by username, email, or name."""
        return User.objects.filter(
            Q(username__icontains=query) |
            Q(email__icontains=query) |
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query)
        ).distinct()
    
    def get_users_by_department(self, department_id: int) -> List[UserProfile]:
        """Get all users in a specific department."""
        return UserProfile.objects.filter(department_id=department_id)
    
    def get_users_by_role(self, role_id: int) -> List[UserProfile]:
        """Get all users with a specific role."""
        return UserProfile.objects.filter(roles__id=role_id)
    
    def activate_user(self, user_id: int) -> User:
        """Activate a user account."""
        user = User.objects.get(id=user_id)
        user.is_active = True
        user.save()
        return user
    
    def deactivate_user(self, user_id: int) -> User:
        """Deactivate a user account."""
        user = User.objects.get(id=user_id)
        user.is_active = False
        user.save()
        return user


class RoleService:
    """Service class for Role management business logic."""
    
    def create_role(self, role_data: Dict[str, Any]) -> Role:
        """Create a new role."""
        role = Role.objects.create(**role_data)
        return role
    
    def assign_permission_to_role(self, role_id: int, permission_id: int) -> Role:
        """Assign a permission to a role."""
        role = Role.objects.get(id=role_id)
        permission = Permission.objects.get(id=permission_id)
        
        role.permissions.add(permission)
        return role
    
    def remove_permission_from_role(self, role_id: int, permission_id: int) -> Role:
        """Remove a permission from a role."""
        role = Role.objects.get(id=role_id)
        permission = Permission.objects.get(id=permission_id)
        
        role.permissions.remove(permission)
        return role
    
    def get_role_permissions(self, role_id: int) -> List[Permission]:
        """Get all permissions for a role."""
        role = Role.objects.get(id=role_id)
        return list(role.permissions.all())
    
    def clone_role(self, source_role_id: int, new_role_name: str, 
                   new_role_description: str = '') -> Role:
        """Clone an existing role with its permissions."""
        source_role = Role.objects.get(id=source_role_id)
        
        new_role = Role.objects.create(
            name=new_role_name,
            description=new_role_description
        )
        
        # Copy permissions
        for permission in source_role.permissions.all():
            new_role.permissions.add(permission)
        
        return new_role


class PermissionService:
    """Service class for Permission management business logic."""
    
    def create_permission(self, permission_data: Dict[str, Any]) -> Permission:
        """Create a new permission."""
        permission = Permission.objects.create(**permission_data)
        return permission
    
    def get_permissions_by_category(self, category: str) -> List[Permission]:
        """Get permissions by category."""
        return Permission.objects.filter(category=category)
    
    def search_permissions(self, query: str) -> List[Permission]:
        """Search permissions by name or description."""
        return Permission.objects.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query)
        )


class DepartmentService:
    """Service class for Department management business logic."""
    
    def create_department(self, department_data: Dict[str, Any]) -> Department:
        """Create a new department."""
        department = Department.objects.create(**department_data)
        return department
    
    def update_department(self, department_id: int, update_data: Dict[str, Any]) -> Department:
        """Update department information."""
        department = Department.objects.get(id=department_id)
        
        for field, value in update_data.items():
            setattr(department, field, value)
        
        department.full_clean()
        department.save()
        return department
    
    def get_department_hierarchy(self, department_id: int) -> Dict[str, Any]:
        """Get department hierarchy including parent and children."""
        department = Department.objects.get(id=department_id)
        
        return {
            'department': department,
            'parent': department.parent,
            'children': list(Department.objects.filter(parent=department)),
            'all_descendants': self._get_all_descendants(department)
        }
    
    def _get_all_descendants(self, department: Department) -> List[Department]:
        """Recursively get all descendant departments."""
        descendants = []
        children = Department.objects.filter(parent=department)
        
        for child in children:
            descendants.append(child)
            descendants.extend(self._get_all_descendants(child))
        
        return descendants
    
    def move_department(self, department_id: int, new_parent_id: Optional[int]) -> Department:
        """Move department to a new parent."""
        department = Department.objects.get(id=department_id)
        
        if new_parent_id:
            new_parent = Department.objects.get(id=new_parent_id)
            # Prevent circular references
            if department in self._get_all_descendants(new_parent):
                raise ValidationError("Cannot move department to its own descendant")
            department.parent = new_parent
        else:
            department.parent = None
        
        department.save()
        return department
    
    def get_department_users_count(self, department_id: int) -> int:
        """Get count of users in a department."""
        return UserProfile.objects.filter(department_id=department_id).count()

```


# File: users/tests/test_models.py

```python
"""
Tests for users app models.
"""
from django.test import TestCase
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from users.models import UserProfile, Role, Permission, Department


class UserProfileModelTest(TestCase):
    """Test cases for UserProfile model."""
    
    def setUp(self):
        """Set up test data."""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.department = Department.objects.create(
            name='Operations',
            description='Flight operations department'
        )
        
    def test_user_profile_creation(self):
        """Test UserProfile creation with valid data."""
        profile = UserProfile.objects.create(
            user=self.user,
            phone_number='+1234567890',
            address='123 Test St, Test City, TC 12345',
            emergency_contact='Jane Doe - +0987654321',
            department=self.department
        )
        
        self.assertEqual(profile.user, self.user)
        self.assertEqual(profile.phone_number, '+1234567890')
        self.assertTrue(profile.is_active)
        self.assertEqual(str(profile), f"{self.user.get_full_name() or self.user.username} Profile")
        
    def test_user_profile_str_method(self):
        """Test UserProfile string representation."""
        self.user.first_name = 'John'
        self.user.last_name = 'Doe'
        self.user.save()
        
        profile = UserProfile.objects.create(
            user=self.user,
            department=self.department
        )
        
        self.assertEqual(str(profile), "John Doe Profile")


class RoleModelTest(TestCase):
    """Test cases for Role model."""
    
    def test_role_creation(self):
        """Test Role creation with valid data."""
        role = Role.objects.create(
            name='Pilot',
            description='Aircraft pilot role'
        )
        
        self.assertEqual(role.name, 'Pilot')
        self.assertEqual(role.description, 'Aircraft pilot role')
        self.assertTrue(role.is_active)
        self.assertEqual(str(role), 'Pilot')
        
    def test_role_unique_name(self):
        """Test that role names must be unique."""
        Role.objects.create(name='Pilot', description='First pilot role')
        
        with self.assertRaises(Exception):
            Role.objects.create(name='Pilot', description='Second pilot role')


class PermissionModelTest(TestCase):
    """Test cases for Permission model."""
    
    def test_permission_creation(self):
        """Test Permission creation with valid data."""
        permission = Permission.objects.create(
            name='view_trips',
            description='Can view trip information',
            resource='trips',
            action='view'
        )
        
        self.assertEqual(permission.name, 'view_trips')
        self.assertEqual(permission.resource, 'trips')
        self.assertEqual(permission.action, 'view')
        self.assertEqual(str(permission), 'view_trips')


class DepartmentModelTest(TestCase):
    """Test cases for Department model."""
    
    def test_department_creation(self):
        """Test Department creation with valid data."""
        department = Department.objects.create(
            name='Medical',
            description='Medical staff department',
            manager_email='manager@medical.com'
        )
        
        self.assertEqual(department.name, 'Medical')
        self.assertEqual(department.description, 'Medical staff department')
        self.assertEqual(department.manager_email, 'manager@medical.com')
        self.assertTrue(department.is_active)
        self.assertEqual(str(department), 'Medical')
        
    def test_department_unique_name(self):
        """Test that department names must be unique."""
        Department.objects.create(name='Operations', description='First ops dept')
        
        with self.assertRaises(Exception):
            Department.objects.create(name='Operations', description='Second ops dept')

```


# File: users/tests/__init__.py

```python

```


# File: common/middleware.py

```python
from django.utils.deprecation import MiddlewareMixin
import threading

# Thread-local storage for current user
_thread_locals = threading.local()


def get_current_user():
    """Get the current user from thread-local storage."""
    return getattr(_thread_locals, 'user', None)


def set_current_user(user):
    """Set the current user in thread-local storage."""
    _thread_locals.user = user


class CurrentUserMiddleware(MiddlewareMixin):
    """
    Middleware to set the current user in thread-local storage
    for use in modification tracking and audit trails.
    """
    
    def process_request(self, request):
        """Set the current user at the start of each request."""
        user = getattr(request, 'user', None)
        if user and user.is_authenticated:
            set_current_user(user)
        else:
            set_current_user(None)
        return None
    
    def process_response(self, request, response):
        """Clear the current user after the request is complete."""
        set_current_user(None)
        return response
    
    def process_exception(self, request, exception):
        """Clear the current user if an exception occurs."""
        set_current_user(None)
        return None

```


# File: common/models.py

```python
from django.db import models
from django.contrib.auth.models import User
import uuid
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType


class BaseModel(models.Model):
    """Base model with common fields for all entities."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="%(class)s_created")
    modified_on = models.DateTimeField(auto_now=True)
    modified_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True, related_name="%(class)s_modified"
    )
    status = models.CharField(max_length=50, default="active", db_index=True)
    lock = models.BooleanField(default=False)
    
    class Meta:
        abstract = True


class Modification(models.Model):
    """Model for tracking changes to other models."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    model = models.CharField(max_length=100)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.UUIDField()
    model_key = GenericForeignKey('content_type', 'object_id')
    field = models.CharField(max_length=100)
    before = models.TextField(null=True, blank=True)
    after = models.TextField(null=True, blank=True)
    time = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="modifications")
    
    class Meta:
        ordering = ['-time']
        
    def __str__(self):
        return f"{self.model} - {self.field} - {self.time}"


class Comment(models.Model):
    """Comments attached to any model instance via a generic foreign key."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.UUIDField()
    content_object = GenericForeignKey('content_type', 'object_id')
    
    text = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="comments_created")
    
    class Meta:
        indexes = [
            models.Index(fields=["content_type", "object_id"]),
        ]
        ordering = ['-created_on']
    
    def __str__(self):
        return f"Comment on {self.content_object} by {self.created_by}"

```


# File: common/permissions.py

```python
from rest_framework import permissions
from django.contrib.auth.models import User


class IsAuthenticatedOrPublicEndpoint(permissions.BasePermission):
    """
    Custom permission to allow unauthenticated access to public endpoints.
    """
    
    def has_permission(self, request, view):
        # Allow unauthenticated access to specific actions
        if view.action in getattr(view, 'public_actions', []):
            return True
        
        # Otherwise require authentication
        return request.user and request.user.is_authenticated


class IsTransactionOwner(permissions.BasePermission):
    """
    Custom permission to only allow access to a transaction with the correct key.
    """
    
    def has_permission(self, request, view):
        # Allow access if the transaction key in the URL matches
        transaction_key = request.query_params.get('key')
        if transaction_key and view.action == 'retrieve_by_key':
            return True
        
        # Otherwise require authentication
        return request.user and request.user.is_authenticated


class HasModelPermission(permissions.BasePermission):
    """
    Base permission class that checks if a user has the required permission for a model.
    Subclasses should define:
    - model_name: The name of the model (lowercase)
    - required_permission: The required permission type (read, write, modify, delete)
    """
    model_name = None
    required_permission = None
    
    def has_permission(self, request, view):
        # Superusers have all permissions
        if request.user.is_superuser:
            return True
            
        # Check if user has the required permission
        try:
            from users.models import UserProfile
            user_profile = UserProfile.objects.get(user=request.user)
            
            # Check permissions through roles
            for role in user_profile.roles.all():
                permission_name = f"{self.model_name}_{self.required_permission}"
                if role.permissions.filter(name=permission_name).exists():
                    return True
                    
            # Check for any_model permission (global permission)
            for role in user_profile.roles.all():
                permission_name = f"any_{self.required_permission}"
                if role.permissions.filter(name=permission_name).exists():
                    return True
                    
            return False
        except:
            return False
    
    def has_object_permission(self, request, view, obj):
        # Superusers have all permissions
        if request.user.is_superuser:
            return True
            
        # Check if user has the required permission for any object
        try:
            from users.models import UserProfile
            user_profile = UserProfile.objects.get(user=request.user)
            
            # Check for any object permission
            for role in user_profile.roles.all():
                permission_name = f"{self.model_name}_{self.required_permission}_any"
                if role.permissions.filter(name=permission_name).exists():
                    return True
            
            # Check if user is the creator of the object (own permission)
            if hasattr(obj, 'created_by') and obj.created_by == request.user:
                for role in user_profile.roles.all():
                    permission_name = f"{self.model_name}_{self.required_permission}_own"
                    if role.permissions.filter(name=permission_name).exists():
                        return True
            
            return False
        except:
            return False


# Operations permissions
class CanReadQuote(HasModelPermission):
    model_name = "quote"
    required_permission = "read"

class CanWriteQuote(HasModelPermission):
    model_name = "quote"
    required_permission = "write"

class CanModifyQuote(HasModelPermission):
    model_name = "quote"
    required_permission = "modify"

class CanDeleteQuote(HasModelPermission):
    model_name = "quote"
    required_permission = "delete"

class CanReadPatient(HasModelPermission):
    model_name = "patient"
    required_permission = "read"

class CanWritePatient(HasModelPermission):
    model_name = "patient"
    required_permission = "write"

class CanModifyPatient(HasModelPermission):
    model_name = "patient"
    required_permission = "modify"

class CanDeletePatient(HasModelPermission):
    model_name = "patient"
    required_permission = "delete"

class CanReadTrip(HasModelPermission):
    model_name = "trip"
    required_permission = "read"

class CanWriteTrip(HasModelPermission):
    model_name = "trip"
    required_permission = "write"

class CanModifyTrip(HasModelPermission):
    model_name = "trip"
    required_permission = "modify"

class CanDeleteTrip(HasModelPermission):
    model_name = "trip"
    required_permission = "delete"

class CanReadPassenger(HasModelPermission):
    model_name = "passenger"
    required_permission = "read"

class CanWritePassenger(HasModelPermission):
    model_name = "passenger"
    required_permission = "write"

class CanModifyPassenger(HasModelPermission):
    model_name = "passenger"
    required_permission = "modify"

class CanDeletePassenger(HasModelPermission):
    model_name = "passenger"
    required_permission = "delete"

```


# File: common/__init__.py

```python

```


# File: common/utils.py

```python
from django.contrib.contenttypes.models import ContentType
from .models import Modification
from .middleware import get_current_user


def track_modification(instance, field_name, before_value, after_value, user=None):
    """
    Manually track a modification for cases where signals aren't sufficient
    
    Args:
        instance: The model instance that was modified
        field_name: The name of the field that changed
        before_value: The previous value
        after_value: The new value  
        user: The user making the change (optional, will use thread-local if not provided)
    """
    if user is None:
        user = get_current_user()
    
    content_type = ContentType.objects.get_for_model(instance)
    
    Modification.objects.create(
        model=instance.__class__.__name__,
        content_type=content_type,
        object_id=instance.pk,
        field=field_name,
        before=str(before_value) if before_value is not None else None,
        after=str(after_value) if after_value is not None else None,
        user=user
    )


def track_creation(instance, user=None):
    """
    Track the creation of a new model instance
    
    Args:
        instance: The newly created model instance
        user: The user creating the instance (optional, will use thread-local if not provided)
    """
    if user is None:
        user = get_current_user()
    
    content_type = ContentType.objects.get_for_model(instance)
    
    Modification.objects.create(
        model=instance.__class__.__name__,
        content_type=content_type,
        object_id=instance.pk,
        field='__created__',
        before=None,
        after='Instance created',
        user=user
    )


def track_deletion(instance, user=None):
    """
    Track the deletion of a model instance
    
    Args:
        instance: The model instance being deleted
        user: The user deleting the instance (optional, will use thread-local if not provided)
    """
    if user is None:
        user = get_current_user()
    
    content_type = ContentType.objects.get_for_model(instance)
    
    Modification.objects.create(
        model=instance.__class__.__name__,
        content_type=content_type,
        object_id=instance.pk,
        field='__deleted__',
        before='Instance existed',
        after=None,
        user=user
    )

```


# File: common/timezone_utils.py

```python
"""
Timezone utilities for handling airport-specific time conversions.

This module provides functions to convert between local airport times and UTC,
properly handling daylight saving time transitions using IANA timezone identifiers.
"""

import pytz
from datetime import datetime, timezone
from typing import Optional, Tuple
from django.utils import timezone as django_timezone


def convert_local_to_utc(local_datetime: datetime, airport_timezone: str) -> datetime:
    """
    Convert a local datetime to UTC using the airport's timezone.
    
    Args:
        local_datetime: Datetime in the airport's local time (naive or aware)
        airport_timezone: IANA timezone identifier (e.g., 'America/New_York')
    
    Returns:
        UTC datetime with timezone info
    
    Raises:
        pytz.exceptions.UnknownTimeZoneError: If timezone is invalid
        pytz.exceptions.AmbiguousTimeError: For ambiguous DST transition times
        pytz.exceptions.NonExistentTimeError: For non-existent DST transition times
    """
    if not airport_timezone:
        raise ValueError("Airport timezone is required")
    
    # Get the timezone object
    tz = pytz.timezone(airport_timezone)
    
    # If datetime already has timezone info, convert directly to UTC
    if local_datetime.tzinfo is not None:
        # If it's already in UTC, return as is
        if local_datetime.tzinfo == pytz.UTC:
            return local_datetime
        # Otherwise, convert to UTC
        return local_datetime.astimezone(pytz.UTC)
    
    # Localize the naive datetime to the airport's timezone
    # This handles DST transitions automatically
    try:
        localized_dt = tz.localize(local_datetime, is_dst=None)
    except pytz.exceptions.AmbiguousTimeError:
        # During "fall back" DST transition, choose the first occurrence (before DST ends)
        localized_dt = tz.localize(local_datetime, is_dst=True)
    except pytz.exceptions.NonExistentTimeError:
        # During "spring forward" DST transition, move to the next valid time
        localized_dt = tz.localize(local_datetime, is_dst=False)
    
    # Convert to UTC
    return localized_dt.astimezone(pytz.UTC)


def convert_utc_to_local(utc_datetime: datetime, airport_timezone: str) -> datetime:
    """
    Convert a UTC datetime to local airport time.
    
    Args:
        utc_datetime: UTC datetime (with or without timezone info)
        airport_timezone: IANA timezone identifier (e.g., 'America/New_York')
    
    Returns:
        Naive datetime in the airport's local time
    
    Raises:
        pytz.exceptions.UnknownTimeZoneError: If timezone is invalid
    """
    if not airport_timezone:
        raise ValueError("Airport timezone is required")
    
    # Ensure UTC datetime is timezone-aware
    if utc_datetime.tzinfo is None:
        utc_datetime = utc_datetime.replace(tzinfo=pytz.UTC)
    elif utc_datetime.tzinfo != pytz.UTC:
        utc_datetime = utc_datetime.astimezone(pytz.UTC)
    
    # Get the timezone object and convert
    tz = pytz.timezone(airport_timezone)
    local_dt = utc_datetime.astimezone(tz)
    
    # Return naive datetime in local time
    return local_dt.replace(tzinfo=None)


def get_timezone_info(airport_timezone: str, dt: Optional[datetime] = None) -> dict:
    """
    Get timezone information for an airport at a specific datetime.
    
    Args:
        airport_timezone: IANA timezone identifier
        dt: Datetime to check (defaults to current time)
    
    Returns:
        Dict with timezone info: {
            'timezone': 'America/New_York',
            'abbreviation': 'EST' or 'EDT',
            'utc_offset': '-05:00',
            'is_dst': True/False,
            'dst_transition_next': datetime or None
        }
    """
    if not airport_timezone:
        raise ValueError("Airport timezone is required")
    
    if dt is None:
        dt = django_timezone.now()
    elif dt.tzinfo is None:
        dt = dt.replace(tzinfo=pytz.UTC)
    
    tz = pytz.timezone(airport_timezone)
    localized_dt = dt.astimezone(tz)
    
    # Get timezone info
    tzinfo = {
        'timezone': airport_timezone,
        'abbreviation': localized_dt.strftime('%Z'),
        'utc_offset': localized_dt.strftime('%z'),
        'is_dst': bool(localized_dt.dst()),
    }
    
    # Find next DST transition (useful for warnings)
    try:
        # Get transitions for the current year and next year
        current_year = localized_dt.year
        transitions = []
        for year in [current_year, current_year + 1]:
            for transition_dt, before_tz, after_tz in tz._utc_transition_times:
                if transition_dt.year == year and transition_dt > dt:
                    transitions.append(transition_dt)
                    break
        
        tzinfo['dst_transition_next'] = min(transitions) if transitions else None
    except (AttributeError, IndexError):
        tzinfo['dst_transition_next'] = None
    
    return tzinfo


def validate_time_consistency(departure_local: datetime, departure_utc: datetime, 
                             departure_timezone: str) -> bool:
    """
    Validate that local and UTC times are consistent for a given timezone.
    
    Args:
        departure_local: Local departure time (naive or aware)
        departure_utc: UTC departure time (with timezone info)
        departure_timezone: IANA timezone identifier
    
    Returns:
        True if times are consistent, False otherwise
    """
    try:
        # Convert local to UTC and compare
        calculated_utc = convert_local_to_utc(departure_local, departure_timezone)
        
        # Ensure both datetimes are timezone-aware for comparison
        if departure_utc.tzinfo is None:
            departure_utc = departure_utc.replace(tzinfo=pytz.UTC)
        elif departure_utc.tzinfo != pytz.UTC:
            departure_utc = departure_utc.astimezone(pytz.UTC)
        
        # Allow for small differences (up to 1 second) due to rounding
        time_diff = abs((calculated_utc - departure_utc).total_seconds())
        return time_diff <= 1.0
        
    except Exception:
        return False


def calculate_flight_duration_with_timezones(
    departure_local: datetime, departure_timezone: str,
    arrival_local: datetime, arrival_timezone: str
) -> Tuple[float, dict]:
    """
    Calculate flight duration accounting for timezone differences.
    
    Args:
        departure_local: Local departure time (naive)
        departure_timezone: Departure airport timezone
        arrival_local: Local arrival time (naive)
        arrival_timezone: Arrival airport timezone
    
    Returns:
        Tuple of (duration_hours, info_dict)
        info_dict contains UTC times and timezone info
    """
    # Convert both times to UTC
    departure_utc = convert_local_to_utc(departure_local, departure_timezone)
    arrival_utc = convert_local_to_utc(arrival_local, arrival_timezone)
    
    # Calculate actual flight duration
    duration_seconds = (arrival_utc - departure_utc).total_seconds()
    duration_hours = duration_seconds / 3600.0
    
    # Prepare info
    info = {
        'departure_utc': departure_utc,
        'arrival_utc': arrival_utc,
        'departure_tz_info': get_timezone_info(departure_timezone, departure_utc),
        'arrival_tz_info': get_timezone_info(arrival_timezone, arrival_utc),
        'duration_seconds': duration_seconds,
        'duration_hours': duration_hours,
        'crosses_date_line': arrival_local.date() != departure_local.date(),
        'timezone_difference_hours': (
            arrival_utc.utcoffset().total_seconds() - departure_utc.utcoffset().total_seconds()
        ) / 3600.0 if arrival_utc.utcoffset() and departure_utc.utcoffset() else 0
    }
    
    return duration_hours, info


def format_time_with_timezone(dt: datetime, timezone_str: str, 
                              include_utc: bool = False) -> str:
    """
    Format a datetime with timezone information for display.
    
    Args:
        dt: Datetime to format (UTC or naive)
        timezone_str: Target timezone for display
        include_utc: Whether to include UTC time in parentheses
    
    Returns:
        Formatted string like "14:30 EST (19:30 UTC)" or "14:30 EST"
    """
    if not timezone_str:
        return dt.strftime('%H:%M')
    
    try:
        if dt.tzinfo is None:
            # Assume it's already in the target timezone
            local_dt = dt
            tz_info = get_timezone_info(timezone_str, 
                                       convert_local_to_utc(dt, timezone_str))
        else:
            # Convert to target timezone
            local_dt = convert_utc_to_local(dt, timezone_str)
            tz_info = get_timezone_info(timezone_str, dt)
        
        formatted = f"{local_dt.strftime('%H:%M')} {tz_info['abbreviation']}"
        
        if include_utc and dt.tzinfo:
            utc_dt = dt.astimezone(pytz.UTC) if dt.tzinfo != pytz.UTC else dt
            formatted += f" ({utc_dt.strftime('%H:%M')} UTC)"
        
        return formatted
        
    except Exception:
        return dt.strftime('%H:%M')


def check_dst_transition_warning(local_dt: datetime, timezone_str: str) -> Optional[dict]:
    """
    Check if a datetime is near a DST transition and return warning info.
    
    Args:
        local_dt: Local datetime to check
        timezone_str: IANA timezone identifier
    
    Returns:
        Dict with warning info or None if no issues
    """
    try:
        tz = pytz.timezone(timezone_str)
        
        # Check if the time is ambiguous (during "fall back")
        try:
            tz.localize(local_dt, is_dst=None)
        except pytz.exceptions.AmbiguousTimeError:
            return {
                'type': 'ambiguous',
                'message': 'This time occurs twice due to daylight saving transition. Using the first occurrence.',
                'suggestion': 'Consider specifying a different time to avoid confusion.'
            }
        except pytz.exceptions.NonExistentTimeError:
            return {
                'type': 'non_existent',
                'message': 'This time does not exist due to daylight saving transition.',
                'suggestion': 'Please choose a time after the DST transition.'
            }
        
        # Check if near a DST transition (within 24 hours)
        tz_info = get_timezone_info(timezone_str, 
                                   convert_local_to_utc(local_dt, timezone_str))
        
        if tz_info.get('dst_transition_next'):
            next_transition = tz_info['dst_transition_next']
            hours_until_transition = (next_transition - convert_local_to_utc(local_dt, timezone_str)).total_seconds() / 3600
            
            if 0 < hours_until_transition <= 24:
                return {
                    'type': 'near_transition',
                    'message': f'DST transition occurs in {hours_until_transition:.1f} hours.',
                    'suggestion': 'Double-check times if this flight crosses the transition.'
                }
        
        return None
        
    except Exception:
        return None

```


# File: common/services/scheduler_service.py

```python
"""
Scheduler Service for Common Operations

Moved from utils/schedulers/ to common/services/scheduler_service.py
This service handles scheduled tasks and background job management.
"""

import logging
from datetime import datetime, timedelta
from django.utils import timezone
from django.conf import settings
from typing import Optional, Dict, Any, List, Callable
import threading
import time

logger = logging.getLogger(__name__)

try:
    from celery import Celery
    from celery.schedules import crontab
    CELERY_AVAILABLE = True
except ImportError:
    logger.warning("Celery not installed. Install with: pip install celery")
    Celery = None
    crontab = None
    CELERY_AVAILABLE = False


class SchedulerService:
    """
    Service for managing scheduled tasks and background jobs
    """
    
    def __init__(self):
        self.scheduled_tasks = {}
        self.running_tasks = {}
        self._stop_event = threading.Event()
        
    def schedule_task(self, task_name: str, func: Callable, interval_seconds: int, 
                     *args, **kwargs) -> bool:
        """
        Schedule a recurring task
        
        Args:
            task_name: Unique name for the task
            func: Function to execute
            interval_seconds: Interval between executions in seconds
            *args: Arguments to pass to the function
            **kwargs: Keyword arguments to pass to the function
            
        Returns:
            bool: True if scheduled successfully
        """
        try:
            if task_name in self.scheduled_tasks:
                logger.warning(f"Task {task_name} already scheduled, updating...")
                self.unschedule_task(task_name)
            
            task_info = {
                'func': func,
                'interval': interval_seconds,
                'args': args,
                'kwargs': kwargs,
                'next_run': timezone.now() + timedelta(seconds=interval_seconds),
                'last_run': None,
                'run_count': 0,
                'active': True
            }
            
            self.scheduled_tasks[task_name] = task_info
            logger.info(f"Scheduled task '{task_name}' to run every {interval_seconds} seconds")
            
            return True
            
        except Exception as e:
            logger.error(f"Error scheduling task {task_name}: {str(e)}")
            return False
    
    def schedule_daily_task(self, task_name: str, func: Callable, hour: int = 0, 
                           minute: int = 0, *args, **kwargs) -> bool:
        """
        Schedule a daily recurring task
        
        Args:
            task_name: Unique name for the task
            func: Function to execute
            hour: Hour to run (0-23)
            minute: Minute to run (0-59)
            *args: Arguments to pass to the function
            **kwargs: Keyword arguments to pass to the function
            
        Returns:
            bool: True if scheduled successfully
        """
        try:
            # Calculate next run time
            now = timezone.now()
            next_run = now.replace(hour=hour, minute=minute, second=0, microsecond=0)
            
            # If the time has already passed today, schedule for tomorrow
            if next_run <= now:
                next_run += timedelta(days=1)
            
            task_info = {
                'func': func,
                'interval': 86400,  # 24 hours in seconds
                'args': args,
                'kwargs': kwargs,
                'next_run': next_run,
                'last_run': None,
                'run_count': 0,
                'active': True,
                'daily': True,
                'hour': hour,
                'minute': minute
            }
            
            self.scheduled_tasks[task_name] = task_info
            logger.info(f"Scheduled daily task '{task_name}' to run at {hour:02d}:{minute:02d}")
            
            return True
            
        except Exception as e:
            logger.error(f"Error scheduling daily task {task_name}: {str(e)}")
            return False
    
    def unschedule_task(self, task_name: str) -> bool:
        """
        Remove a scheduled task
        
        Args:
            task_name: Name of the task to remove
            
        Returns:
            bool: True if removed successfully
        """
        try:
            if task_name in self.scheduled_tasks:
                del self.scheduled_tasks[task_name]
                logger.info(f"Unscheduled task '{task_name}'")
                return True
            else:
                logger.warning(f"Task '{task_name}' not found in scheduled tasks")
                return False
                
        except Exception as e:
            logger.error(f"Error unscheduling task {task_name}: {str(e)}")
            return False
    
    def run_task_now(self, task_name: str) -> bool:
        """
        Execute a scheduled task immediately
        
        Args:
            task_name: Name of the task to run
            
        Returns:
            bool: True if executed successfully
        """
        try:
            if task_name not in self.scheduled_tasks:
                logger.error(f"Task '{task_name}' not found")
                return False
            
            task_info = self.scheduled_tasks[task_name]
            
            if task_name in self.running_tasks:
                logger.warning(f"Task '{task_name}' is already running")
                return False
            
            # Execute the task in a separate thread
            thread = threading.Thread(
                target=self._execute_task,
                args=(task_name, task_info),
                daemon=True
            )
            thread.start()
            
            return True
            
        except Exception as e:
            logger.error(f"Error running task {task_name}: {str(e)}")
            return False
    
    def _execute_task(self, task_name: str, task_info: Dict[str, Any]):
        """Execute a task and handle errors"""
        try:
            self.running_tasks[task_name] = {
                'start_time': timezone.now(),
                'thread': threading.current_thread()
            }
            
            logger.info(f"Executing task '{task_name}'")
            
            # Call the task function
            result = task_info['func'](*task_info['args'], **task_info['kwargs'])
            
            # Update task info
            task_info['last_run'] = timezone.now()
            task_info['run_count'] += 1
            
            # Calculate next run time
            if task_info.get('daily', False):
                # For daily tasks, schedule for next day at same time
                next_run = task_info['last_run'].replace(
                    hour=task_info['hour'],
                    minute=task_info['minute'],
                    second=0,
                    microsecond=0
                ) + timedelta(days=1)
            else:
                # For interval tasks, add interval to last run
                next_run = task_info['last_run'] + timedelta(seconds=task_info['interval'])
            
            task_info['next_run'] = next_run
            
            logger.info(f"Task '{task_name}' completed successfully. Next run: {next_run}")
            
        except Exception as e:
            logger.error(f"Error executing task '{task_name}': {str(e)}")
            
        finally:
            # Remove from running tasks
            if task_name in self.running_tasks:
                del self.running_tasks[task_name]
    
    def start_scheduler(self):
        """Start the task scheduler in a background thread"""
        if hasattr(self, '_scheduler_thread') and self._scheduler_thread.is_alive():
            logger.warning("Scheduler is already running")
            return
        
        self._stop_event.clear()
        self._scheduler_thread = threading.Thread(target=self._scheduler_loop, daemon=True)
        self._scheduler_thread.start()
        logger.info("Task scheduler started")
    
    def stop_scheduler(self):
        """Stop the task scheduler"""
        self._stop_event.set()
        if hasattr(self, '_scheduler_thread'):
            self._scheduler_thread.join(timeout=5)
        logger.info("Task scheduler stopped")
    
    def _scheduler_loop(self):
        """Main scheduler loop"""
        while not self._stop_event.is_set():
            try:
                now = timezone.now()
                
                # Check each scheduled task
                for task_name, task_info in list(self.scheduled_tasks.items()):
                    if not task_info.get('active', True):
                        continue
                    
                    if task_name in self.running_tasks:
                        continue  # Task is already running
                    
                    if now >= task_info['next_run']:
                        # Time to run this task
                        thread = threading.Thread(
                            target=self._execute_task,
                            args=(task_name, task_info),
                            daemon=True
                        )
                        thread.start()
                
                # Sleep for a short interval before checking again
                time.sleep(10)  # Check every 10 seconds
                
            except Exception as e:
                logger.error(f"Error in scheduler loop: {str(e)}")
                time.sleep(30)  # Wait longer on error
    
    def get_task_status(self, task_name: str) -> Optional[Dict[str, Any]]:
        """
        Get status information for a scheduled task
        
        Args:
            task_name: Name of the task
            
        Returns:
            dict: Task status information or None if not found
        """
        if task_name not in self.scheduled_tasks:
            return None
        
        task_info = self.scheduled_tasks[task_name]
        is_running = task_name in self.running_tasks
        
        status = {
            'name': task_name,
            'active': task_info.get('active', True),
            'interval': task_info['interval'],
            'next_run': task_info['next_run'],
            'last_run': task_info['last_run'],
            'run_count': task_info['run_count'],
            'is_running': is_running
        }
        
        if is_running:
            running_info = self.running_tasks[task_name]
            status['running_since'] = running_info['start_time']
            status['running_duration'] = timezone.now() - running_info['start_time']
        
        return status
    
    def list_scheduled_tasks(self) -> List[Dict[str, Any]]:
        """
        List all scheduled tasks with their status
        
        Returns:
            list: List of task status dictionaries
        """
        tasks = []
        for task_name in self.scheduled_tasks:
            status = self.get_task_status(task_name)
            if status:
                tasks.append(status)
        
        return tasks
    
    def pause_task(self, task_name: str) -> bool:
        """
        Pause a scheduled task (it won't run until resumed)
        
        Args:
            task_name: Name of the task to pause
            
        Returns:
            bool: True if paused successfully
        """
        if task_name not in self.scheduled_tasks:
            logger.error(f"Task '{task_name}' not found")
            return False
        
        self.scheduled_tasks[task_name]['active'] = False
        logger.info(f"Paused task '{task_name}'")
        return True
    
    def resume_task(self, task_name: str) -> bool:
        """
        Resume a paused task
        
        Args:
            task_name: Name of the task to resume
            
        Returns:
            bool: True if resumed successfully
        """
        if task_name not in self.scheduled_tasks:
            logger.error(f"Task '{task_name}' not found")
            return False
        
        self.scheduled_tasks[task_name]['active'] = True
        logger.info(f"Resumed task '{task_name}'")
        return True


class CelerySchedulerService:
    """
    Celery-based scheduler service for production environments
    """
    
    def __init__(self):
        if not CELERY_AVAILABLE:
            raise ImportError("Celery is required for CelerySchedulerService")
        
        self.app = Celery('jet_operations')
        self.app.config_from_object('django.conf:settings', namespace='CELERY')
        self.app.autodiscover_tasks()
    
    def schedule_periodic_task(self, task_name: str, task_path: str, 
                              schedule_type: str = 'interval', **schedule_kwargs):
        """
        Schedule a periodic task using Celery Beat
        
        Args:
            task_name: Unique name for the task
            task_path: Python path to the task function
            schedule_type: 'interval', 'crontab', or 'solar'
            **schedule_kwargs: Schedule parameters
        """
        try:
            if schedule_type == 'interval':
                from celery.schedules import schedule
                schedule_obj = schedule(seconds=schedule_kwargs.get('seconds', 60))
            elif schedule_type == 'crontab':
                schedule_obj = crontab(
                    minute=schedule_kwargs.get('minute', '*'),
                    hour=schedule_kwargs.get('hour', '*'),
                    day_of_week=schedule_kwargs.get('day_of_week', '*'),
                    day_of_month=schedule_kwargs.get('day_of_month', '*'),
                    month_of_year=schedule_kwargs.get('month_of_year', '*')
                )
            else:
                raise ValueError(f"Unsupported schedule type: {schedule_type}")
            
            # Add to Celery beat schedule
            self.app.conf.beat_schedule[task_name] = {
                'task': task_path,
                'schedule': schedule_obj,
                'args': schedule_kwargs.get('args', ()),
                'kwargs': schedule_kwargs.get('kwargs', {})
            }
            
            logger.info(f"Scheduled Celery task '{task_name}' with {schedule_type} schedule")
            return True
            
        except Exception as e:
            logger.error(f"Error scheduling Celery task {task_name}: {str(e)}")
            return False


# Global scheduler instance
_scheduler_instance = None


def get_scheduler() -> SchedulerService:
    """Get the global scheduler instance"""
    global _scheduler_instance
    if _scheduler_instance is None:
        _scheduler_instance = SchedulerService()
    return _scheduler_instance


# Convenience functions
def schedule_task(task_name: str, func: Callable, interval_seconds: int, *args, **kwargs) -> bool:
    """Schedule a recurring task"""
    scheduler = get_scheduler()
    return scheduler.schedule_task(task_name, func, interval_seconds, *args, **kwargs)


def schedule_daily_task(task_name: str, func: Callable, hour: int = 0, minute: int = 0, 
                       *args, **kwargs) -> bool:
    """Schedule a daily recurring task"""
    scheduler = get_scheduler()
    return scheduler.schedule_daily_task(task_name, func, hour, minute, *args, **kwargs)


def start_scheduler():
    """Start the global scheduler"""
    scheduler = get_scheduler()
    scheduler.start_scheduler()


def stop_scheduler():
    """Stop the global scheduler"""
    scheduler = get_scheduler()
    scheduler.stop_scheduler()

```


# File: common/tests/__init__.py

```python

```


# File: common/tests/test_scheduler_service.py

```python
"""
Django test cases for scheduler service functionality.

Converted from custom test scripts to proper Django TestCase.
"""

from django.test import TestCase
from unittest.mock import patch, Mock
import threading
import time
from datetime import datetime, timedelta
from django.utils import timezone
from common.services.scheduler_service import SchedulerService, get_scheduler, schedule_task, schedule_daily_task


class SchedulerServiceTestCase(TestCase):
    """Test case for scheduler service functionality."""
    
    def setUp(self):
        """Set up test data for scheduler service tests."""
        self.scheduler = SchedulerService()
        self.test_results = []
    
    def test_task_function(self, message="test"):
        """Simple test function for scheduler testing."""
        self.test_results.append(f"Task executed: {message}")
        return f"Task completed: {message}"
    
    def test_schedule_task_success(self):
        """Test successful task scheduling."""
        result = self.scheduler.schedule_task(
            "test_task",
            self.test_task_function,
            60,
            "test_message"
        )
        
        # Assertions
        self.assertTrue(result)
        self.assertIn("test_task", self.scheduler.scheduled_tasks)
        
        task_info = self.scheduler.scheduled_tasks["test_task"]
        self.assertEqual(task_info['func'], self.test_task_function)
        self.assertEqual(task_info['interval'], 60)
        self.assertEqual(task_info['args'], ("test_message",))
        self.assertTrue(task_info['active'])
    
    def test_schedule_daily_task_success(self):
        """Test successful daily task scheduling."""
        result = self.scheduler.schedule_daily_task(
            "daily_test",
            self.test_task_function,
            9,
            30,
            "daily_message"
        )
        
        # Assertions
        self.assertTrue(result)
        self.assertIn("daily_test", self.scheduler.scheduled_tasks)
        
        task_info = self.scheduler.scheduled_tasks["daily_test"]
        self.assertEqual(task_info['interval'], 86400)  # 24 hours
        self.assertTrue(task_info.get('daily', False))
        self.assertEqual(task_info['hour'], 9)
        self.assertEqual(task_info['minute'], 30)
    
    def test_unschedule_task_success(self):
        """Test successful task unscheduling."""
        # First schedule a task
        self.scheduler.schedule_task("temp_task", self.test_task_function, 60)
        self.assertIn("temp_task", self.scheduler.scheduled_tasks)
        
        # Then unschedule it
        result = self.scheduler.unschedule_task("temp_task")
        
        # Assertions
        self.assertTrue(result)
        self.assertNotIn("temp_task", self.scheduler.scheduled_tasks)
    
    def test_unschedule_nonexistent_task(self):
        """Test unscheduling a non-existent task."""
        result = self.scheduler.unschedule_task("nonexistent_task")
        self.assertFalse(result)
    
    def test_run_task_now_success(self):
        """Test running a scheduled task immediately."""
        # Schedule a task
        self.scheduler.schedule_task("immediate_task", self.test_task_function, 3600, "immediate")
        
        # Run it immediately
        result = self.scheduler.run_task_now("immediate_task")
        
        # Assertions
        self.assertTrue(result)
        
        # Wait a moment for the task to complete
        time.sleep(0.1)
        
        # Check if task was executed
        self.assertIn("Task executed: immediate", self.test_results)
    
    def test_run_nonexistent_task(self):
        """Test running a non-existent task."""
        result = self.scheduler.run_task_now("nonexistent_task")
        self.assertFalse(result)
    
    def test_get_task_status_success(self):
        """Test getting task status for existing task."""
        # Schedule a task
        self.scheduler.schedule_task("status_task", self.test_task_function, 120)
        
        # Get status
        status = self.scheduler.get_task_status("status_task")
        
        # Assertions
        self.assertIsNotNone(status)
        self.assertEqual(status['name'], "status_task")
        self.assertEqual(status['interval'], 120)
        self.assertTrue(status['active'])
        self.assertEqual(status['run_count'], 0)
        self.assertFalse(status['is_running'])
        self.assertIsNone(status['last_run'])
    
    def test_get_task_status_nonexistent(self):
        """Test getting status for non-existent task."""
        status = self.scheduler.get_task_status("nonexistent_task")
        self.assertIsNone(status)
    
    def test_list_scheduled_tasks(self):
        """Test listing all scheduled tasks."""
        # Schedule multiple tasks
        self.scheduler.schedule_task("task1", self.test_task_function, 60)
        self.scheduler.schedule_task("task2", self.test_task_function, 120)
        self.scheduler.schedule_daily_task("daily_task", self.test_task_function, 10, 0)
        
        # List tasks
        tasks = self.scheduler.list_scheduled_tasks()
        
        # Assertions
        self.assertEqual(len(tasks), 3)
        task_names = [task['name'] for task in tasks]
        self.assertIn("task1", task_names)
        self.assertIn("task2", task_names)
        self.assertIn("daily_task", task_names)
    
    def test_pause_and_resume_task(self):
        """Test pausing and resuming a task."""
        # Schedule a task
        self.scheduler.schedule_task("pause_test", self.test_task_function, 60)
        
        # Pause the task
        result = self.scheduler.pause_task("pause_test")
        self.assertTrue(result)
        
        # Check if task is paused
        status = self.scheduler.get_task_status("pause_test")
        self.assertFalse(status['active'])
        
        # Resume the task
        result = self.scheduler.resume_task("pause_test")
        self.assertTrue(result)
        
        # Check if task is active again
        status = self.scheduler.get_task_status("pause_test")
        self.assertTrue(status['active'])
    
    def test_pause_nonexistent_task(self):
        """Test pausing a non-existent task."""
        result = self.scheduler.pause_task("nonexistent_task")
        self.assertFalse(result)
    
    def test_resume_nonexistent_task(self):
        """Test resuming a non-existent task."""
        result = self.scheduler.resume_task("nonexistent_task")
        self.assertFalse(result)
    
    def test_scheduler_start_stop(self):
        """Test starting and stopping the scheduler."""
        # Start scheduler
        self.scheduler.start_scheduler()
        
        # Check if scheduler thread is running
        self.assertTrue(hasattr(self.scheduler, '_scheduler_thread'))
        self.assertTrue(self.scheduler._scheduler_thread.is_alive())
        
        # Stop scheduler
        self.scheduler.stop_scheduler()
        
        # Wait for thread to stop
        time.sleep(0.1)
        
        # Check if stop event is set
        self.assertTrue(self.scheduler._stop_event.is_set())
    
    def test_task_execution_with_error(self):
        """Test task execution when task function raises an error."""
        def error_task():
            raise Exception("Test error")
        
        # Schedule error task
        self.scheduler.schedule_task("error_task", error_task, 60)
        
        # Run task (should not crash scheduler)
        result = self.scheduler.run_task_now("error_task")
        self.assertTrue(result)
        
        # Wait for task to complete
        time.sleep(0.1)
        
        # Task should still be in scheduled tasks
        self.assertIn("error_task", self.scheduler.scheduled_tasks)
    
    def test_task_update_existing(self):
        """Test updating an existing scheduled task."""
        # Schedule initial task
        self.scheduler.schedule_task("update_task", self.test_task_function, 60, "original")
        original_next_run = self.scheduler.scheduled_tasks["update_task"]['next_run']
        
        # Update the task
        self.scheduler.schedule_task("update_task", self.test_task_function, 120, "updated")
        
        # Assertions
        task_info = self.scheduler.scheduled_tasks["update_task"]
        self.assertEqual(task_info['interval'], 120)
        self.assertEqual(task_info['args'], ("updated",))
        # Next run time should be updated
        self.assertNotEqual(task_info['next_run'], original_next_run)
    
    def test_global_scheduler_instance(self):
        """Test global scheduler instance functionality."""
        scheduler1 = get_scheduler()
        scheduler2 = get_scheduler()
        
        # Should return the same instance
        self.assertIs(scheduler1, scheduler2)
    
    def test_convenience_functions(self):
        """Test convenience functions."""
        # Test schedule_task convenience function
        result = schedule_task("conv_task", self.test_task_function, 60, "convenience")
        self.assertTrue(result)
        
        # Test schedule_daily_task convenience function
        result = schedule_daily_task("conv_daily", self.test_task_function, 12, 0, "daily_convenience")
        self.assertTrue(result)
        
        # Verify tasks were scheduled in global scheduler
        global_scheduler = get_scheduler()
        self.assertIn("conv_task", global_scheduler.scheduled_tasks)
        self.assertIn("conv_daily", global_scheduler.scheduled_tasks)
    
    def test_daily_task_next_run_calculation(self):
        """Test next run calculation for daily tasks."""
        now = timezone.now()
        current_hour = now.hour
        
        # Schedule daily task for an hour that has already passed today
        past_hour = (current_hour - 1) % 24
        self.scheduler.schedule_daily_task("past_daily", self.test_task_function, past_hour, 0)
        
        task_info = self.scheduler.scheduled_tasks["past_daily"]
        next_run = task_info['next_run']
        
        # Next run should be tomorrow
        self.assertGreater(next_run, now)
        self.assertEqual(next_run.hour, past_hour)
        
        # Schedule daily task for a future hour today
        future_hour = (current_hour + 1) % 24
        self.scheduler.schedule_daily_task("future_daily", self.test_task_function, future_hour, 0)
        
        task_info = self.scheduler.scheduled_tasks["future_daily"]
        next_run = task_info['next_run']
        
        # Next run should be today (if future hour is later today) or tomorrow
        self.assertGreater(next_run, now)
        self.assertEqual(next_run.hour, future_hour)
    
    def tearDown(self):
        """Clean up after tests."""
        # Stop scheduler if running
        if hasattr(self.scheduler, '_scheduler_thread') and self.scheduler._scheduler_thread.is_alive():
            self.scheduler.stop_scheduler()
        
        # Clear test results
        self.test_results.clear()


class CelerySchedulerServiceTestCase(TestCase):
    """Test case for Celery scheduler service functionality."""
    
    def setUp(self):
        """Set up test data for Celery scheduler tests."""
        # Skip if Celery is not available
        try:
            from common.services.scheduler_service import CelerySchedulerService
            self.celery_service = CelerySchedulerService()
        except ImportError:
            self.skipTest("Celery not available")
    
    def test_celery_service_initialization(self):
        """Test Celery scheduler service initialization."""
        from common.services.scheduler_service import CelerySchedulerService
        
        service = CelerySchedulerService()
        self.assertIsNotNone(service.app)
        self.assertEqual(service.app.main, 'jet_operations')
    
    def test_schedule_interval_task(self):
        """Test scheduling an interval-based task with Celery."""
        from common.services.scheduler_service import CelerySchedulerService
        
        service = CelerySchedulerService()
        
        result = service.schedule_periodic_task(
            task_name="test_interval",
            task_path="myapp.tasks.test_task",
            schedule_type="interval",
            seconds=300
        )
        
        self.assertTrue(result)
        self.assertIn("test_interval", service.app.conf.beat_schedule)
    
    def test_schedule_crontab_task(self):
        """Test scheduling a crontab-based task with Celery."""
        from common.services.scheduler_service import CelerySchedulerService
        
        service = CelerySchedulerService()
        
        result = service.schedule_periodic_task(
            task_name="test_crontab",
            task_path="myapp.tasks.daily_task",
            schedule_type="crontab",
            hour=9,
            minute=30
        )
        
        self.assertTrue(result)
        self.assertIn("test_crontab", service.app.conf.beat_schedule)
    
    def test_unsupported_schedule_type(self):
        """Test scheduling with unsupported schedule type."""
        from common.services.scheduler_service import CelerySchedulerService
        
        service = CelerySchedulerService()
        
        result = service.schedule_periodic_task(
            task_name="test_unsupported",
            task_path="myapp.tasks.test_task",
            schedule_type="unsupported"
        )
        
        self.assertFalse(result)

```


# File: backend/asgi.py

```python
"""
ASGI config for backend project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')

application = get_asgi_application()

```


# File: backend/__init__.py

```python

```


# File: backend/urls.py

```python
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

```


# File: backend/wsgi.py

```python
"""
WSGI config for backend project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')

application = get_wsgi_application()

```


# File: backend/settings.py

```python
"""
Django settings for backend project - Modular Architecture

Generated by 'django-admin startproject' using Django 5.2.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.2/ref/settings/
"""

from pathlib import Path
from datetime import timedelta
import os
import environ

# Initialize environment variables
env = environ.Env(
    # Set casting and default values
    DEBUG=(bool, True),
    SECRET_KEY=(str, 'django-insecure-6r7f((os!(^y(1j7tti@m5-fm-rx*rdb5%nxo4wfu1)0&h8@*u'),
    ALLOWED_HOSTS=(list, []),
)

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Take environment variables from .env file if it exists
env_file = BASE_DIR / '.env'
if env_file.exists():
    environ.Env.read_env(env_file)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env('DEBUG')

ALLOWED_HOSTS = env('ALLOWED_HOSTS') if env('ALLOWED_HOSTS') else []

# Application definition - Modular app structure
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Third-party apps
    'rest_framework',
    'corsheaders',
    'rest_framework_simplejwt',
    
    # Common utilities
    'common',
    
    # Domain-specific apps
    'users',
    'contacts',
    'airports',
    'aircraft',
    'operations',
    'documents',
    'finance',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'common.middleware.CurrentUserMiddleware',  # Updated path
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'backend.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'backend.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": env("POSTGRES_DB", default="airmed"),
        "USER": env("POSTGRES_USER", default="airmed"),
        "PASSWORD": env("POSTGRES_PASSWORD", default="airmedpass"),
        "HOST": env("POSTGRES_HOST", default="127.0.0.1"),
        "PORT": env("POSTGRES_PORT", default="5432"),
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/

STATIC_URL = 'static/'

# CORS settings
CORS_ALLOW_ALL_ORIGINS = True  # For development only, restrict in production
CORS_ALLOW_CREDENTIALS = True

# CSRF settings
CSRF_TRUSTED_ORIGINS = [
    'http://localhost:5173',
    'http://localhost:5174',
    'http://127.0.0.1:5173',
    'http://127.0.0.1:5174',
]

# REST Framework settings
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10
}

# JWT settings
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(hours=1),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
}

# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

```


# File: finance/models.py

```python
from django.db import models
from common.models import BaseModel
from django.utils import timezone
import uuid
from decimal import Decimal


class Transaction(BaseModel):
    """Transaction model for financial operations."""
    
    PAYMENT_METHODS = [
        ('credit_card', 'Credit Card'),
        ('debit_card', 'Debit Card'),
        ('ach', 'ACH Transfer'),
        ('wire', 'Wire Transfer'),
        ('check', 'Check'),
        ('cash', 'Cash'),
        ('other', 'Other'),
    ]
    
    PAYMENT_STATUS = [
        ('created', 'Created'),
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('cancelled', 'Cancelled'),
        ('refunded', 'Refunded'),
    ]
    
    TRANSACTION_TYPES = [
        ('payment', 'Payment'),
        ('refund', 'Refund'),
        ('fee', 'Fee'),
        ('adjustment', 'Adjustment'),
    ]
    
    # Transaction identification
    key = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, db_index=True)
    transaction_type = models.CharField(max_length=20, choices=TRANSACTION_TYPES, default='payment')
    
    # Financial details
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, default='USD')
    
    # Payment information
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHODS)
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS, default='created')
    payment_date = models.DateTimeField(default=timezone.now)
    
    # Customer information
    email = models.EmailField()
    customer_name = models.CharField(max_length=255, blank=True, null=True)
    billing_address = models.JSONField(default=dict, blank=True)
    
    # Payment processor details
    processor_transaction_id = models.CharField(max_length=255, blank=True, null=True)
    processor_name = models.CharField(max_length=50, blank=True, null=True)  # Stripe, PayPal, etc.
    processor_fee = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    
    # Related entities
    related_quote_id = models.UUIDField(null=True, blank=True)
    related_trip_id = models.UUIDField(null=True, blank=True)
    
    # Additional metadata
    description = models.TextField(blank=True, null=True)
    reference_number = models.CharField(max_length=100, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    
    class Meta:
        indexes = [
            models.Index(fields=['key']),
            models.Index(fields=['payment_status', 'payment_date']),
            models.Index(fields=['email']),
            models.Index(fields=['related_quote_id']),
            models.Index(fields=['processor_transaction_id']),
        ]
        ordering = ['-payment_date']
    
    def __str__(self):
        return f"Transaction {self.key} - ${self.amount} - {self.payment_status}"
    
    @property
    def net_amount(self):
        """Calculate net amount after processor fees."""
        if self.processor_fee:
            return self.amount - self.processor_fee
        return self.amount
    
    @property
    def is_successful(self):
        """Check if transaction was successful."""
        return self.payment_status == 'completed'
    
    @property
    def can_be_refunded(self):
        """Check if transaction can be refunded."""
        return self.payment_status == 'completed' and self.transaction_type == 'payment'


class Invoice(BaseModel):
    """Invoice model for billing operations."""
    
    INVOICE_STATUS = [
        ('draft', 'Draft'),
        ('sent', 'Sent'),
        ('viewed', 'Viewed'),
        ('paid', 'Paid'),
        ('overdue', 'Overdue'),
        ('cancelled', 'Cancelled'),
    ]
    
    # Invoice identification
    invoice_number = models.CharField(max_length=50, unique=True, db_index=True)
    
    # Customer information
    customer_email = models.EmailField()
    customer_name = models.CharField(max_length=255)
    billing_address = models.JSONField(default=dict, blank=True)
    
    # Financial details
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    tax_amount = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, default='USD')
    
    # Dates
    issue_date = models.DateField(default=timezone.now)
    due_date = models.DateField()
    paid_date = models.DateField(null=True, blank=True)
    
    # Status and tracking
    status = models.CharField(max_length=20, choices=INVOICE_STATUS, default='draft')
    sent_date = models.DateTimeField(null=True, blank=True)
    
    # Related entities
    related_quote_id = models.UUIDField(null=True, blank=True)
    related_trip_id = models.UUIDField(null=True, blank=True)
    
    # Payment tracking
    transactions = models.ManyToManyField(Transaction, related_name="invoices", blank=True)
    
    # Additional information
    description = models.TextField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    
    class Meta:
        indexes = [
            models.Index(fields=['invoice_number']),
            models.Index(fields=['status', 'due_date']),
            models.Index(fields=['customer_email']),
            models.Index(fields=['related_quote_id']),
        ]
        ordering = ['-issue_date']
    
    def __str__(self):
        return f"Invoice {self.invoice_number} - ${self.total_amount} - {self.status}"
    
    @property
    def is_overdue(self):
        """Check if invoice is overdue."""
        if self.status == 'paid':
            return False
        return timezone.now().date() > self.due_date
    
    @property
    def days_overdue(self):
        """Calculate days overdue."""
        if not self.is_overdue:
            return 0
        return (timezone.now().date() - self.due_date).days
    
    @property
    def amount_paid(self):
        """Calculate total amount paid through transactions."""
        return sum(
            t.amount for t in self.transactions.filter(
                payment_status='completed',
                transaction_type='payment'
            )
        )
    
    @property
    def amount_remaining(self):
        """Calculate remaining amount to be paid."""
        return self.total_amount - self.amount_paid


class InvoiceLineItem(BaseModel):
    """Line items for invoices."""
    
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name="line_items")
    
    # Item details
    description = models.CharField(max_length=255)
    quantity = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('1.00'))
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    
    # Tax information
    taxable = models.BooleanField(default=True)
    tax_rate = models.DecimalField(max_digits=5, decimal_places=4, default=Decimal('0.0000'))
    
    class Meta:
        indexes = [
            models.Index(fields=['invoice']),
        ]
    
    def __str__(self):
        return f"{self.description} - ${self.total_price}"
    
    def save(self, *args, **kwargs):
        """Calculate total price on save."""
        self.total_price = self.quantity * self.unit_price
        super().save(*args, **kwargs)


class PaymentMethod(BaseModel):
    """Stored payment methods for customers."""
    
    PAYMENT_TYPES = [
        ('credit_card', 'Credit Card'),
        ('bank_account', 'Bank Account'),
    ]
    
    # Customer information
    customer_email = models.EmailField()
    customer_name = models.CharField(max_length=255, blank=True, null=True)
    
    # Payment method details
    payment_type = models.CharField(max_length=20, choices=PAYMENT_TYPES)
    is_default = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    
    # Masked details for display
    last_four_digits = models.CharField(max_length=4, blank=True, null=True)
    brand = models.CharField(max_length=50, blank=True, null=True)  # Visa, MasterCard, etc.
    expiry_month = models.IntegerField(null=True, blank=True)
    expiry_year = models.IntegerField(null=True, blank=True)
    
    # Processor information
    processor_payment_method_id = models.CharField(max_length=255, blank=True, null=True)
    processor_name = models.CharField(max_length=50, blank=True, null=True)
    
    class Meta:
        indexes = [
            models.Index(fields=['customer_email', 'is_active']),
            models.Index(fields=['processor_payment_method_id']),
        ]
    
    def __str__(self):
        if self.last_four_digits:
            return f"{self.brand} ending in {self.last_four_digits}"
        return f"{self.get_payment_type_display()} for {self.customer_email}"
    
    @property
    def is_expired(self):
        """Check if payment method is expired (for cards)."""
        if self.payment_type != 'credit_card' or not self.expiry_month or not self.expiry_year:
            return False
        
        from datetime import date
        today = date.today()
        return (self.expiry_year < today.year or 
                (self.expiry_year == today.year and self.expiry_month < today.month))

```


# File: finance/serializers.py

```python
from rest_framework import serializers
from decimal import Decimal
from .models import Transaction, Invoice, InvoiceLineItem, PaymentMethod


class TransactionSerializer(serializers.ModelSerializer):
    """Serializer for Transaction model."""
    net_amount = serializers.ReadOnlyField()
    is_successful = serializers.ReadOnlyField()
    can_be_refunded = serializers.ReadOnlyField()
    payment_method_display = serializers.CharField(source='get_payment_method_display', read_only=True)
    payment_status_display = serializers.CharField(source='get_payment_status_display', read_only=True)
    transaction_type_display = serializers.CharField(source='get_transaction_type_display', read_only=True)
    
    class Meta:
        model = Transaction
        fields = [
            'id', 'key', 'transaction_type', 'transaction_type_display',
            'amount', 'currency', 'net_amount', 'payment_method', 'payment_method_display',
            'payment_status', 'payment_status_display', 'payment_date',
            'email', 'customer_name', 'billing_address',
            'processor_transaction_id', 'processor_name', 'processor_fee',
            'related_quote_id', 'related_trip_id', 'description', 'reference_number',
            'notes', 'is_successful', 'can_be_refunded', 'created_on', 'updated_on'
        ]
        read_only_fields = [
            'id', 'key', 'payment_date', 'processor_transaction_id', 
            'processor_name', 'processor_fee', 'created_on', 'updated_on'
        ]
    
    def validate_amount(self, value):
        """Validate transaction amount."""
        if value <= 0:
            raise serializers.ValidationError("Amount must be greater than zero.")
        if value > Decimal('999999.99'):
            raise serializers.ValidationError("Amount cannot exceed $999,999.99.")
        return value
    
    def validate_email(self, value):
        """Validate customer email."""
        if not value:
            raise serializers.ValidationError("Customer email is required.")
        return value.lower().strip()


class CreateTransactionSerializer(serializers.Serializer):
    """Serializer for creating new transactions."""
    amount = serializers.DecimalField(max_digits=10, decimal_places=2)
    currency = serializers.CharField(max_length=3, default='USD')
    payment_method = serializers.ChoiceField(choices=Transaction.PAYMENT_METHODS)
    email = serializers.EmailField()
    customer_name = serializers.CharField(max_length=255, required=False)
    transaction_type = serializers.ChoiceField(choices=Transaction.TRANSACTION_TYPES, default='payment')
    description = serializers.CharField(required=False)
    related_quote_id = serializers.UUIDField(required=False)
    related_trip_id = serializers.UUIDField(required=False)
    billing_address = serializers.JSONField(required=False)
    
    def validate_amount(self, value):
        """Validate transaction amount."""
        if value <= 0:
            raise serializers.ValidationError("Amount must be greater than zero.")
        return value


class ProcessPaymentSerializer(serializers.Serializer):
    """Serializer for processing payments."""
    processor_transaction_id = serializers.CharField(max_length=255)
    processor_name = serializers.CharField(max_length=50)
    processor_fee = serializers.DecimalField(max_digits=10, decimal_places=2, required=False)


class RefundSerializer(serializers.Serializer):
    """Serializer for creating refunds."""
    refund_amount = serializers.DecimalField(max_digits=10, decimal_places=2, required=False)
    reason = serializers.CharField(required=False)
    
    def validate_refund_amount(self, value):
        """Validate refund amount."""
        if value and value <= 0:
            raise serializers.ValidationError("Refund amount must be greater than zero.")
        return value


class InvoiceLineItemSerializer(serializers.ModelSerializer):
    """Serializer for InvoiceLineItem model."""
    
    class Meta:
        model = InvoiceLineItem
        fields = [
            'id', 'description', 'quantity', 'unit_price', 'total_price',
            'taxable', 'tax_rate'
        ]
        read_only_fields = ['id', 'total_price']
    
    def validate_quantity(self, value):
        """Validate quantity."""
        if value <= 0:
            raise serializers.ValidationError("Quantity must be greater than zero.")
        return value
    
    def validate_unit_price(self, value):
        """Validate unit price."""
        if value < 0:
            raise serializers.ValidationError("Unit price cannot be negative.")
        return value


class InvoiceSerializer(serializers.ModelSerializer):
    """Serializer for Invoice model."""
    line_items = InvoiceLineItemSerializer(many=True, read_only=True)
    is_overdue = serializers.ReadOnlyField()
    days_overdue = serializers.ReadOnlyField()
    amount_paid = serializers.ReadOnlyField()
    amount_remaining = serializers.ReadOnlyField()
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    
    class Meta:
        model = Invoice
        fields = [
            'id', 'invoice_number', 'customer_email', 'customer_name',
            'billing_address', 'subtotal', 'tax_amount', 'total_amount',
            'currency', 'issue_date', 'due_date', 'paid_date',
            'status', 'status_display', 'sent_date', 'related_quote_id',
            'related_trip_id', 'description', 'notes', 'line_items',
            'is_overdue', 'days_overdue', 'amount_paid', 'amount_remaining',
            'created_on', 'updated_on'
        ]
        read_only_fields = [
            'id', 'invoice_number', 'sent_date', 'paid_date',
            'created_on', 'updated_on'
        ]
    
    def validate_customer_email(self, value):
        """Validate customer email."""
        if not value:
            raise serializers.ValidationError("Customer email is required.")
        return value.lower().strip()
    
    def validate_due_date(self, value):
        """Validate due date."""
        from django.utils import timezone
        if value < timezone.now().date():
            raise serializers.ValidationError("Due date cannot be in the past.")
        return value


class CreateInvoiceSerializer(serializers.Serializer):
    """Serializer for creating new invoices."""
    customer_email = serializers.EmailField()
    customer_name = serializers.CharField(max_length=255)
    billing_address = serializers.JSONField(required=False)
    due_days = serializers.IntegerField(default=30, min_value=1)
    related_quote_id = serializers.UUIDField(required=False)
    related_trip_id = serializers.UUIDField(required=False)
    description = serializers.CharField(required=False)
    tax_rate = serializers.DecimalField(max_digits=5, decimal_places=4, default=Decimal('0.00'))
    line_items = serializers.ListField(
        child=serializers.DictField(),
        min_length=1
    )
    
    def validate_line_items(self, value):
        """Validate line items format."""
        required_fields = ['description', 'unit_price', 'total_price']
        
        for item in value:
            for field in required_fields:
                if field not in item:
                    raise serializers.ValidationError(f"Line item missing required field: {field}")
            
            # Validate numeric fields
            try:
                unit_price = Decimal(str(item['unit_price']))
                total_price = Decimal(str(item['total_price']))
                quantity = Decimal(str(item.get('quantity', '1.00')))
                
                if unit_price < 0:
                    raise serializers.ValidationError("Unit price cannot be negative.")
                if total_price < 0:
                    raise serializers.ValidationError("Total price cannot be negative.")
                if quantity <= 0:
                    raise serializers.ValidationError("Quantity must be greater than zero.")
                    
            except (ValueError, TypeError):
                raise serializers.ValidationError("Invalid numeric values in line items.")
        
        return value


class PaymentMethodSerializer(serializers.ModelSerializer):
    """Serializer for PaymentMethod model."""
    is_expired = serializers.ReadOnlyField()
    payment_type_display = serializers.CharField(source='get_payment_type_display', read_only=True)
    
    class Meta:
        model = PaymentMethod
        fields = [
            'id', 'customer_email', 'customer_name', 'payment_type',
            'payment_type_display', 'is_default', 'is_active',
            'last_four_digits', 'brand', 'expiry_month', 'expiry_year',
            'is_expired', 'created_on', 'updated_on'
        ]
        read_only_fields = [
            'id', 'processor_payment_method_id', 'processor_name',
            'created_on', 'updated_on'
        ]
    
    def validate_customer_email(self, value):
        """Validate customer email."""
        if not value:
            raise serializers.ValidationError("Customer email is required.")
        return value.lower().strip()
    
    def validate_expiry_month(self, value):
        """Validate expiry month."""
        if value and (value < 1 or value > 12):
            raise serializers.ValidationError("Expiry month must be between 1 and 12.")
        return value
    
    def validate_expiry_year(self, value):
        """Validate expiry year."""
        if value:
            from datetime import date
            current_year = date.today().year
            if value < current_year or value > current_year + 20:
                raise serializers.ValidationError("Invalid expiry year.")
        return value


class CreatePaymentMethodSerializer(serializers.Serializer):
    """Serializer for creating payment methods."""
    customer_email = serializers.EmailField()
    customer_name = serializers.CharField(max_length=255, required=False)
    payment_type = serializers.ChoiceField(choices=PaymentMethod.PAYMENT_TYPES)
    processor_payment_method_id = serializers.CharField(max_length=255)
    processor_name = serializers.CharField(max_length=50)
    last_four_digits = serializers.CharField(max_length=4, required=False)
    brand = serializers.CharField(max_length=50, required=False)
    expiry_month = serializers.IntegerField(min_value=1, max_value=12, required=False)
    expiry_year = serializers.IntegerField(required=False)
    is_default = serializers.BooleanField(default=False)
    
    def validate_customer_email(self, value):
        """Validate customer email."""
        return value.lower().strip()

```


# File: finance/views.py

```python
from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from common.permissions import IsOwnerOrReadOnly, HasRolePermission
from .models import Transaction, Invoice, InvoiceLineItem, PaymentMethod
from .serializers import (
    TransactionSerializer, CreateTransactionSerializer, ProcessPaymentSerializer,
    RefundSerializer, InvoiceSerializer, CreateInvoiceSerializer,
    PaymentMethodSerializer, CreatePaymentMethodSerializer
)
from .services.finance_service import TransactionService, InvoiceService, PaymentMethodService
import logging

logger = logging.getLogger(__name__)


class TransactionViewSet(viewsets.ModelViewSet):
    """ViewSet for Transaction operations."""
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    permission_classes = [permissions.IsAuthenticated, HasRolePermission]
    
    def get_queryset(self):
        """Filter transactions based on query parameters."""
        queryset = super().get_queryset()
        
        # Filter by payment status
        status_filter = self.request.query_params.get('status')
        if status_filter:
            queryset = queryset.filter(payment_status=status_filter)
        
        # Filter by transaction type
        transaction_type = self.request.query_params.get('type')
        if transaction_type:
            queryset = queryset.filter(transaction_type=transaction_type)
        
        # Filter by customer email
        email = self.request.query_params.get('email')
        if email:
            queryset = queryset.filter(email__icontains=email)
        
        # Filter by related entities
        quote_id = self.request.query_params.get('quote_id')
        if quote_id:
            queryset = queryset.filter(related_quote_id=quote_id)
        
        trip_id = self.request.query_params.get('trip_id')
        if trip_id:
            queryset = queryset.filter(related_trip_id=trip_id)
        
        return queryset.order_by('-payment_date')
    
    def create(self, request, *args, **kwargs):
        """Create a new transaction."""
        serializer = CreateTransactionSerializer(data=request.data)
        if serializer.is_valid():
            try:
                transaction = TransactionService.create_transaction(
                    amount=serializer.validated_data['amount'],
                    currency=serializer.validated_data.get('currency', 'USD'),
                    payment_method=serializer.validated_data['payment_method'],
                    email=serializer.validated_data['email'],
                    customer_name=serializer.validated_data.get('customer_name'),
                    transaction_type=serializer.validated_data.get('transaction_type', 'payment'),
                    description=serializer.validated_data.get('description'),
                    related_quote_id=serializer.validated_data.get('related_quote_id'),
                    related_trip_id=serializer.validated_data.get('related_trip_id'),
                    billing_address=serializer.validated_data.get('billing_address')
                )
                
                response_serializer = TransactionSerializer(transaction)
                return Response(response_serializer.data, status=status.HTTP_201_CREATED)
                
            except Exception as e:
                logger.error(f"Transaction creation failed: {str(e)}")
                return Response(
                    {'error': 'Transaction creation failed'},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['post'])
    def process(self, request, pk=None):
        """Process a payment transaction."""
        transaction = self.get_object()
        serializer = ProcessPaymentSerializer(data=request.data)
        
        if serializer.is_valid():
            try:
                updated_transaction = TransactionService.process_payment(
                    transaction_id=transaction.id,
                    processor_transaction_id=serializer.validated_data['processor_transaction_id'],
                    processor_name=serializer.validated_data['processor_name'],
                    processor_fee=serializer.validated_data.get('processor_fee')
                )
                
                if updated_transaction:
                    response_serializer = TransactionSerializer(updated_transaction)
                    return Response(response_serializer.data)
                else:
                    return Response(
                        {'error': 'Transaction cannot be processed'},
                        status=status.HTTP_400_BAD_REQUEST
                    )
                    
            except Exception as e:
                logger.error(f"Payment processing failed: {str(e)}")
                return Response(
                    {'error': 'Payment processing failed'},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['post'])
    def complete(self, request, pk=None):
        """Mark payment as completed."""
        transaction = self.get_object()
        
        try:
            updated_transaction = TransactionService.complete_payment(transaction.id)
            if updated_transaction:
                response_serializer = TransactionSerializer(updated_transaction)
                return Response(response_serializer.data)
            else:
                return Response(
                    {'error': 'Transaction not found'},
                    status=status.HTTP_404_NOT_FOUND
                )
                
        except Exception as e:
            logger.error(f"Payment completion failed: {str(e)}")
            return Response(
                {'error': 'Payment completion failed'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @action(detail=True, methods=['post'])
    def fail(self, request, pk=None):
        """Mark payment as failed."""
        transaction = self.get_object()
        reason = request.data.get('reason')
        
        try:
            updated_transaction = TransactionService.fail_payment(transaction.id, reason)
            if updated_transaction:
                response_serializer = TransactionSerializer(updated_transaction)
                return Response(response_serializer.data)
            else:
                return Response(
                    {'error': 'Transaction not found'},
                    status=status.HTTP_404_NOT_FOUND
                )
                
        except Exception as e:
            logger.error(f"Payment failure update failed: {str(e)}")
            return Response(
                {'error': 'Payment failure update failed'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @action(detail=True, methods=['post'])
    def refund(self, request, pk=None):
        """Create a refund for this transaction."""
        transaction = self.get_object()
        serializer = RefundSerializer(data=request.data)
        
        if serializer.is_valid():
            try:
                refund_transaction = TransactionService.create_refund(
                    original_transaction_id=transaction.id,
                    refund_amount=serializer.validated_data.get('refund_amount'),
                    reason=serializer.validated_data.get('reason')
                )
                
                if refund_transaction:
                    response_serializer = TransactionSerializer(refund_transaction)
                    return Response(response_serializer.data, status=status.HTTP_201_CREATED)
                else:
                    return Response(
                        {'error': 'Transaction cannot be refunded'},
                        status=status.HTTP_400_BAD_REQUEST
                    )
                    
            except Exception as e:
                logger.error(f"Refund creation failed: {str(e)}")
                return Response(
                    {'error': 'Refund creation failed'},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class InvoiceViewSet(viewsets.ModelViewSet):
    """ViewSet for Invoice operations."""
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer
    permission_classes = [permissions.IsAuthenticated, HasRolePermission]
    
    def get_queryset(self):
        """Filter invoices based on query parameters."""
        queryset = super().get_queryset()
        
        # Filter by status
        status_filter = self.request.query_params.get('status')
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        
        # Filter by customer email
        email = self.request.query_params.get('email')
        if email:
            queryset = queryset.filter(customer_email__icontains=email)
        
        # Filter by related entities
        quote_id = self.request.query_params.get('quote_id')
        if quote_id:
            queryset = queryset.filter(related_quote_id=quote_id)
        
        trip_id = self.request.query_params.get('trip_id')
        if trip_id:
            queryset = queryset.filter(related_trip_id=trip_id)
        
        # Filter overdue invoices
        overdue = self.request.query_params.get('overdue')
        if overdue and overdue.lower() == 'true':
            from django.utils import timezone
            queryset = queryset.filter(
                due_date__lt=timezone.now().date(),
                status__in=['sent', 'viewed']
            )
        
        return queryset.order_by('-issue_date')
    
    def create(self, request, *args, **kwargs):
        """Create a new invoice."""
        serializer = CreateInvoiceSerializer(data=request.data)
        if serializer.is_valid():
            try:
                invoice = InvoiceService.create_invoice(
                    customer_email=serializer.validated_data['customer_email'],
                    customer_name=serializer.validated_data['customer_name'],
                    line_items=serializer.validated_data['line_items'],
                    due_days=serializer.validated_data.get('due_days', 30),
                    related_quote_id=serializer.validated_data.get('related_quote_id'),
                    related_trip_id=serializer.validated_data.get('related_trip_id'),
                    billing_address=serializer.validated_data.get('billing_address'),
                    description=serializer.validated_data.get('description'),
                    tax_rate=serializer.validated_data.get('tax_rate')
                )
                
                response_serializer = InvoiceSerializer(invoice)
                return Response(response_serializer.data, status=status.HTTP_201_CREATED)
                
            except Exception as e:
                logger.error(f"Invoice creation failed: {str(e)}")
                return Response(
                    {'error': 'Invoice creation failed'},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['post'])
    def send(self, request, pk=None):
        """Send invoice to customer."""
        invoice = self.get_object()
        
        try:
            updated_invoice = InvoiceService.send_invoice(invoice.id)
            if updated_invoice:
                response_serializer = InvoiceSerializer(updated_invoice)
                return Response(response_serializer.data)
            else:
                return Response(
                    {'error': 'Invoice not found'},
                    status=status.HTTP_404_NOT_FOUND
                )
                
        except Exception as e:
            logger.error(f"Invoice sending failed: {str(e)}")
            return Response(
                {'error': 'Invoice sending failed'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @action(detail=True, methods=['post'])
    def record_payment(self, request, pk=None):
        """Record a payment against this invoice."""
        invoice = self.get_object()
        transaction_id = request.data.get('transaction_id')
        
        if not transaction_id:
            return Response(
                {'error': 'Transaction ID is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            updated_invoice = InvoiceService.record_payment(invoice.id, transaction_id)
            if updated_invoice:
                response_serializer = InvoiceSerializer(updated_invoice)
                return Response(response_serializer.data)
            else:
                return Response(
                    {'error': 'Payment recording failed'},
                    status=status.HTTP_400_BAD_REQUEST
                )
                
        except Exception as e:
            logger.error(f"Payment recording failed: {str(e)}")
            return Response(
                {'error': 'Payment recording failed'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        """Cancel an invoice."""
        invoice = self.get_object()
        reason = request.data.get('reason')
        
        try:
            updated_invoice = InvoiceService.cancel_invoice(invoice.id, reason)
            if updated_invoice:
                response_serializer = InvoiceSerializer(updated_invoice)
                return Response(response_serializer.data)
            else:
                return Response(
                    {'error': 'Invoice cannot be cancelled'},
                    status=status.HTTP_400_BAD_REQUEST
                )
                
        except Exception as e:
            logger.error(f"Invoice cancellation failed: {str(e)}")
            return Response(
                {'error': 'Invoice cancellation failed'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @action(detail=False, methods=['get'])
    def overdue(self, request):
        """Get all overdue invoices."""
        try:
            overdue_invoices = InvoiceService.get_overdue_invoices()
            serializer = InvoiceSerializer(overdue_invoices, many=True)
            return Response(serializer.data)
        except Exception as e:
            logger.error(f"Getting overdue invoices failed: {str(e)}")
            return Response(
                {'error': 'Failed to retrieve overdue invoices'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class PaymentMethodViewSet(viewsets.ModelViewSet):
    """ViewSet for PaymentMethod operations."""
    queryset = PaymentMethod.objects.filter(is_active=True)
    serializer_class = PaymentMethodSerializer
    permission_classes = [permissions.IsAuthenticated, HasRolePermission]
    
    def get_queryset(self):
        """Filter payment methods based on query parameters."""
        queryset = super().get_queryset()
        
        # Filter by customer email
        email = self.request.query_params.get('email')
        if email:
            queryset = queryset.filter(customer_email__icontains=email)
        
        # Filter by payment type
        payment_type = self.request.query_params.get('type')
        if payment_type:
            queryset = queryset.filter(payment_type=payment_type)
        
        # Show only active payment methods by default
        include_inactive = self.request.query_params.get('include_inactive')
        if not include_inactive or include_inactive.lower() != 'true':
            queryset = queryset.filter(is_active=True)
        
        return queryset.order_by('-is_default', '-created_on')
    
    def create(self, request, *args, **kwargs):
        """Create a new payment method."""
        serializer = CreatePaymentMethodSerializer(data=request.data)
        if serializer.is_valid():
            try:
                payment_method = PaymentMethodService.create_payment_method(
                    customer_email=serializer.validated_data['customer_email'],
                    payment_type=serializer.validated_data['payment_type'],
                    processor_payment_method_id=serializer.validated_data['processor_payment_method_id'],
                    processor_name=serializer.validated_data['processor_name'],
                    customer_name=serializer.validated_data.get('customer_name'),
                    last_four_digits=serializer.validated_data.get('last_four_digits'),
                    brand=serializer.validated_data.get('brand'),
                    expiry_month=serializer.validated_data.get('expiry_month'),
                    expiry_year=serializer.validated_data.get('expiry_year'),
                    is_default=serializer.validated_data.get('is_default', False)
                )
                
                response_serializer = PaymentMethodSerializer(payment_method)
                return Response(response_serializer.data, status=status.HTTP_201_CREATED)
                
            except Exception as e:
                logger.error(f"Payment method creation failed: {str(e)}")
                return Response(
                    {'error': 'Payment method creation failed'},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['post'])
    def set_default(self, request, pk=None):
        """Set this payment method as default."""
        payment_method = self.get_object()
        
        try:
            updated_payment_method = PaymentMethodService.set_default_payment_method(payment_method.id)
            if updated_payment_method:
                response_serializer = PaymentMethodSerializer(updated_payment_method)
                return Response(response_serializer.data)
            else:
                return Response(
                    {'error': 'Payment method not found'},
                    status=status.HTTP_404_NOT_FOUND
                )
                
        except Exception as e:
            logger.error(f"Setting default payment method failed: {str(e)}")
            return Response(
                {'error': 'Setting default payment method failed'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @action(detail=True, methods=['post'])
    def deactivate(self, request, pk=None):
        """Deactivate this payment method."""
        payment_method = self.get_object()
        
        try:
            updated_payment_method = PaymentMethodService.deactivate_payment_method(payment_method.id)
            if updated_payment_method:
                response_serializer = PaymentMethodSerializer(updated_payment_method)
                return Response(response_serializer.data)
            else:
                return Response(
                    {'error': 'Payment method not found'},
                    status=status.HTTP_404_NOT_FOUND
                )
                
        except Exception as e:
            logger.error(f"Payment method deactivation failed: {str(e)}")
            return Response(
                {'error': 'Payment method deactivation failed'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @action(detail=False, methods=['get'])
    def by_customer(self, request):
        """Get payment methods for a specific customer."""
        customer_email = request.query_params.get('email')
        if not customer_email:
            return Response(
                {'error': 'Customer email parameter is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            payment_methods = PaymentMethodService.get_customer_payment_methods(customer_email)
            serializer = PaymentMethodSerializer(payment_methods, many=True)
            return Response(serializer.data)
        except Exception as e:
            logger.error(f"Getting customer payment methods failed: {str(e)}")
            return Response(
                {'error': 'Failed to retrieve payment methods'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

```


# File: finance/apps.py

```python
from django.apps import AppConfig


class FinanceConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'finance'
    verbose_name = 'Financial Management'

```


# File: finance/__init__.py

```python

```


# File: finance/tests.py

```python
from django.test import TestCase
from django.contrib.auth.models import User
from django.utils import timezone
from decimal import Decimal
from .models import Transaction, Invoice, InvoiceLineItem, PaymentMethod
from .services.finance_service import TransactionService, InvoiceService, PaymentMethodService
import uuid


class TransactionModelTest(TestCase):
    """Test cases for Transaction model."""
    
    def test_transaction_creation(self):
        """Test transaction creation with required fields."""
        transaction = Transaction.objects.create(
            amount=Decimal('100.00'),
            currency='USD',
            payment_method='credit_card',
            email='customer@example.com',
            customer_name='John Doe'
        )
        
        self.assertEqual(transaction.amount, Decimal('100.00'))
        self.assertEqual(transaction.currency, 'USD')
        self.assertEqual(transaction.payment_method, 'credit_card')
        self.assertEqual(transaction.email, 'customer@example.com')
        self.assertEqual(transaction.payment_status, 'created')
        self.assertIsNotNone(transaction.key)
    
    def test_net_amount_calculation(self):
        """Test net amount calculation with processor fee."""
        transaction = Transaction.objects.create(
            amount=Decimal('100.00'),
            currency='USD',
            payment_method='credit_card',
            email='test@example.com',
            processor_fee=Decimal('3.50')
        )
        
        self.assertEqual(transaction.net_amount, Decimal('96.50'))
    
    def test_transaction_status_properties(self):
        """Test transaction status properties."""
        transaction = Transaction.objects.create(
            amount=Decimal('100.00'),
            currency='USD',
            payment_method='credit_card',
            email='test@example.com',
            payment_status='completed',
            transaction_type='payment'
        )
        
        self.assertTrue(transaction.is_successful)
        self.assertTrue(transaction.can_be_refunded)
        
        # Test refund transaction
        refund = Transaction.objects.create(
            amount=Decimal('50.00'),
            currency='USD',
            payment_method='credit_card',
            email='test@example.com',
            payment_status='completed',
            transaction_type='refund'
        )
        
        self.assertTrue(refund.is_successful)
        self.assertFalse(refund.can_be_refunded)  # Refunds can't be refunded


class InvoiceModelTest(TestCase):
    """Test cases for Invoice model."""
    
    def test_invoice_creation(self):
        """Test invoice creation with required fields."""
        due_date = timezone.now().date() + timezone.timedelta(days=30)
        
        invoice = Invoice.objects.create(
            invoice_number='INV-20240101-0001',
            customer_email='customer@example.com',
            customer_name='John Doe',
            subtotal=Decimal('100.00'),
            tax_amount=Decimal('8.00'),
            total_amount=Decimal('108.00'),
            due_date=due_date
        )
        
        self.assertEqual(invoice.invoice_number, 'INV-20240101-0001')
        self.assertEqual(invoice.customer_email, 'customer@example.com')
        self.assertEqual(invoice.total_amount, Decimal('108.00'))
        self.assertEqual(invoice.status, 'draft')
        self.assertFalse(invoice.is_overdue)
    
    def test_invoice_overdue_logic(self):
        """Test invoice overdue calculation."""
        past_due_date = timezone.now().date() - timezone.timedelta(days=5)
        
        invoice = Invoice.objects.create(
            invoice_number='INV-OVERDUE-001',
            customer_email='overdue@example.com',
            customer_name='Overdue Customer',
            subtotal=Decimal('200.00'),
            total_amount=Decimal('200.00'),
            due_date=past_due_date,
            status='sent'
        )
        
        self.assertTrue(invoice.is_overdue)
        self.assertEqual(invoice.days_overdue, 5)
    
    def test_invoice_payment_tracking(self):
        """Test invoice payment amount tracking."""
        invoice = Invoice.objects.create(
            invoice_number='INV-PAYMENT-001',
            customer_email='payment@example.com',
            customer_name='Payment Customer',
            subtotal=Decimal('500.00'),
            total_amount=Decimal('500.00'),
            due_date=timezone.now().date() + timezone.timedelta(days=30)
        )
        
        # Create completed transaction
        transaction = Transaction.objects.create(
            amount=Decimal('300.00'),
            currency='USD',
            payment_method='credit_card',
            email='payment@example.com',
            payment_status='completed',
            transaction_type='payment'
        )
        
        # Add transaction to invoice
        invoice.transactions.add(transaction)
        
        self.assertEqual(invoice.amount_paid, Decimal('300.00'))
        self.assertEqual(invoice.amount_remaining, Decimal('200.00'))


class InvoiceLineItemTest(TestCase):
    """Test cases for InvoiceLineItem model."""
    
    def setUp(self):
        self.invoice = Invoice.objects.create(
            invoice_number='INV-LINE-001',
            customer_email='line@example.com',
            customer_name='Line Customer',
            subtotal=Decimal('100.00'),
            total_amount=Decimal('100.00'),
            due_date=timezone.now().date() + timezone.timedelta(days=30)
        )
    
    def test_line_item_creation(self):
        """Test line item creation and total calculation."""
        line_item = InvoiceLineItem.objects.create(
            invoice=self.invoice,
            description='Test Service',
            quantity=Decimal('2.00'),
            unit_price=Decimal('50.00'),
            taxable=True,
            tax_rate=Decimal('0.08')
        )
        
        self.assertEqual(line_item.description, 'Test Service')
        self.assertEqual(line_item.quantity, Decimal('2.00'))
        self.assertEqual(line_item.unit_price, Decimal('50.00'))
        self.assertEqual(line_item.total_price, Decimal('100.00'))
        self.assertTrue(line_item.taxable)


class PaymentMethodModelTest(TestCase):
    """Test cases for PaymentMethod model."""
    
    def test_payment_method_creation(self):
        """Test payment method creation."""
        payment_method = PaymentMethod.objects.create(
            customer_email='payment@example.com',
            customer_name='Payment Customer',
            payment_type='credit_card',
            processor_payment_method_id='pm_test123',
            processor_name='stripe',
            last_four_digits='4242',
            brand='Visa',
            expiry_month=12,
            expiry_year=2025,
            is_default=True
        )
        
        self.assertEqual(payment_method.customer_email, 'payment@example.com')
        self.assertEqual(payment_method.payment_type, 'credit_card')
        self.assertEqual(payment_method.brand, 'Visa')
        self.assertTrue(payment_method.is_default)
        self.assertTrue(payment_method.is_active)
        self.assertFalse(payment_method.is_expired)
    
    def test_payment_method_expiration(self):
        """Test payment method expiration logic."""
        from datetime import date
        current_year = date.today().year
        
        expired_method = PaymentMethod.objects.create(
            customer_email='expired@example.com',
            payment_type='credit_card',
            processor_payment_method_id='pm_expired',
            processor_name='stripe',
            expiry_month=1,
            expiry_year=current_year - 1  # Last year
        )
        
        self.assertTrue(expired_method.is_expired)


class TransactionServiceTest(TestCase):
    """Test cases for TransactionService."""
    
    def test_create_transaction(self):
        """Test transaction creation via service."""
        transaction = TransactionService.create_transaction(
            amount=Decimal('150.00'),
            currency='USD',
            payment_method='credit_card',
            email='service@example.com',
            customer_name='Service Customer',
            description='Service test transaction'
        )
        
        self.assertIsNotNone(transaction)
        self.assertEqual(transaction.amount, Decimal('150.00'))
        self.assertEqual(transaction.email, 'service@example.com')
        self.assertEqual(transaction.payment_status, 'created')
    
    def test_process_payment(self):
        """Test payment processing via service."""
        transaction = TransactionService.create_transaction(
            amount=Decimal('100.00'),
            currency='USD',
            payment_method='credit_card',
            email='process@example.com'
        )
        
        processed = TransactionService.process_payment(
            transaction_id=transaction.id,
            processor_transaction_id='txn_test123',
            processor_name='stripe',
            processor_fee=Decimal('3.20')
        )
        
        self.assertIsNotNone(processed)
        self.assertEqual(processed.payment_status, 'processing')
        self.assertEqual(processed.processor_transaction_id, 'txn_test123')
        self.assertEqual(processed.processor_fee, Decimal('3.20'))
    
    def test_complete_payment(self):
        """Test payment completion via service."""
        transaction = TransactionService.create_transaction(
            amount=Decimal('75.00'),
            currency='USD',
            payment_method='ach',
            email='complete@example.com'
        )
        
        completed = TransactionService.complete_payment(transaction.id)
        
        self.assertIsNotNone(completed)
        self.assertEqual(completed.payment_status, 'completed')
        self.assertIsNotNone(completed.payment_date)
    
    def test_create_refund(self):
        """Test refund creation via service."""
        # Create original transaction
        original = TransactionService.create_transaction(
            amount=Decimal('200.00'),
            currency='USD',
            payment_method='credit_card',
            email='refund@example.com'
        )
        
        # Complete it first
        TransactionService.complete_payment(original.id)
        
        # Create refund
        refund = TransactionService.create_refund(
            original_transaction_id=original.id,
            refund_amount=Decimal('100.00'),
            reason='Customer request'
        )
        
        self.assertIsNotNone(refund)
        self.assertEqual(refund.transaction_type, 'refund')
        self.assertEqual(refund.amount, Decimal('100.00'))
        self.assertEqual(refund.payment_status, 'completed')
        self.assertEqual(refund.notes, 'Customer request')


class InvoiceServiceTest(TestCase):
    """Test cases for InvoiceService."""
    
    def test_create_invoice(self):
        """Test invoice creation via service."""
        line_items = [
            {
                'description': 'Flight Service',
                'quantity': Decimal('1.00'),
                'unit_price': Decimal('1000.00'),
                'total_price': Decimal('1000.00'),
                'taxable': True
            },
            {
                'description': 'Ground Transport',
                'quantity': Decimal('2.00'),
                'unit_price': Decimal('50.00'),
                'total_price': Decimal('100.00'),
                'taxable': False
            }
        ]
        
        invoice = InvoiceService.create_invoice(
            customer_email='invoice@example.com',
            customer_name='Invoice Customer',
            line_items=line_items,
            due_days=30,
            tax_rate=Decimal('0.08')
        )
        
        self.assertIsNotNone(invoice)
        self.assertEqual(invoice.customer_email, 'invoice@example.com')
        self.assertEqual(invoice.subtotal, Decimal('1100.00'))
        self.assertEqual(invoice.tax_amount, Decimal('80.00'))  # Only taxable items
        self.assertEqual(invoice.total_amount, Decimal('1180.00'))
        self.assertEqual(invoice.line_items.count(), 2)
    
    def test_send_invoice(self):
        """Test invoice sending via service."""
        line_items = [{'description': 'Test', 'unit_price': Decimal('100.00'), 'total_price': Decimal('100.00')}]
        
        invoice = InvoiceService.create_invoice(
            customer_email='send@example.com',
            customer_name='Send Customer',
            line_items=line_items
        )
        
        sent_invoice = InvoiceService.send_invoice(invoice.id)
        
        self.assertIsNotNone(sent_invoice)
        self.assertEqual(sent_invoice.status, 'sent')
        self.assertIsNotNone(sent_invoice.sent_date)
    
    def test_record_payment(self):
        """Test payment recording via service."""
        line_items = [{'description': 'Test', 'unit_price': Decimal('500.00'), 'total_price': Decimal('500.00')}]
        
        invoice = InvoiceService.create_invoice(
            customer_email='payment@example.com',
            customer_name='Payment Customer',
            line_items=line_items
        )
        
        # Create completed transaction
        transaction = TransactionService.create_transaction(
            amount=Decimal('500.00'),
            currency='USD',
            payment_method='credit_card',
            email='payment@example.com'
        )
        TransactionService.complete_payment(transaction.id)
        
        # Record payment
        updated_invoice = InvoiceService.record_payment(invoice.id, transaction.id)
        
        self.assertIsNotNone(updated_invoice)
        self.assertEqual(updated_invoice.status, 'paid')
        self.assertIsNotNone(updated_invoice.paid_date)
        self.assertTrue(updated_invoice.transactions.filter(id=transaction.id).exists())


class PaymentMethodServiceTest(TestCase):
    """Test cases for PaymentMethodService."""
    
    def test_create_payment_method(self):
        """Test payment method creation via service."""
        payment_method = PaymentMethodService.create_payment_method(
            customer_email='method@example.com',
            customer_name='Method Customer',
            payment_type='credit_card',
            processor_payment_method_id='pm_service123',
            processor_name='stripe',
            last_four_digits='1234',
            brand='MasterCard',
            expiry_month=6,
            expiry_year=2026,
            is_default=True
        )
        
        self.assertIsNotNone(payment_method)
        self.assertEqual(payment_method.customer_email, 'method@example.com')
        self.assertEqual(payment_method.brand, 'MasterCard')
        self.assertTrue(payment_method.is_default)
        self.assertTrue(payment_method.is_active)
    
    def test_set_default_payment_method(self):
        """Test setting default payment method via service."""
        # Create first payment method as default
        method1 = PaymentMethodService.create_payment_method(
            customer_email='default@example.com',
            payment_type='credit_card',
            processor_payment_method_id='pm_first',
            processor_name='stripe',
            is_default=True
        )
        
        # Create second payment method
        method2 = PaymentMethodService.create_payment_method(
            customer_email='default@example.com',
            payment_type='credit_card',
            processor_payment_method_id='pm_second',
            processor_name='stripe',
            is_default=False
        )
        
        # Set second as default
        updated_method = PaymentMethodService.set_default_payment_method(method2.id)
        
        self.assertIsNotNone(updated_method)
        self.assertTrue(updated_method.is_default)
        
        # Check first method is no longer default
        method1.refresh_from_db()
        self.assertFalse(method1.is_default)
    
    def test_get_customer_payment_methods(self):
        """Test retrieving customer payment methods."""
        customer_email = 'multi@example.com'
        
        # Create multiple payment methods
        PaymentMethodService.create_payment_method(
            customer_email=customer_email,
            payment_type='credit_card',
            processor_payment_method_id='pm_1',
            processor_name='stripe',
            is_default=True
        )
        
        PaymentMethodService.create_payment_method(
            customer_email=customer_email,
            payment_type='bank_account',
            processor_payment_method_id='pm_2',
            processor_name='stripe'
        )
        
        methods = PaymentMethodService.get_customer_payment_methods(customer_email)
        
        self.assertEqual(methods.count(), 2)
        # Default should be first
        self.assertTrue(methods.first().is_default)
    
    def test_deactivate_payment_method(self):
        """Test payment method deactivation via service."""
        payment_method = PaymentMethodService.create_payment_method(
            customer_email='deactivate@example.com',
            payment_type='credit_card',
            processor_payment_method_id='pm_deactivate',
            processor_name='stripe',
            is_default=True
        )
        
        deactivated = PaymentMethodService.deactivate_payment_method(payment_method.id)
        
        self.assertIsNotNone(deactivated)
        self.assertFalse(deactivated.is_active)
        self.assertFalse(deactivated.is_default)

```


# File: finance/urls.py

```python
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TransactionViewSet, InvoiceViewSet, PaymentMethodViewSet

router = DefaultRouter()
router.register(r'transactions', TransactionViewSet)
router.register(r'invoices', InvoiceViewSet)
router.register(r'payment-methods', PaymentMethodViewSet)

urlpatterns = [
    path('', include(router.urls)),
]

```


# File: finance/admin.py

```python
from django.contrib import admin
from .models import Transaction, Invoice, InvoiceLineItem, PaymentMethod


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    """Admin configuration for Transaction model."""
    list_display = [
        'key', 'transaction_type', 'amount', 'currency', 'payment_status',
        'payment_method', 'email', 'payment_date'
    ]
    list_filter = [
        'transaction_type', 'payment_status', 'payment_method', 
        'currency', 'payment_date', 'processor_name'
    ]
    search_fields = [
        'key', 'email', 'customer_name', 'processor_transaction_id',
        'reference_number', 'description'
    ]
    readonly_fields = [
        'id', 'key', 'net_amount', 'is_successful', 'can_be_refunded',
        'created_on', 'updated_on'
    ]
    
    fieldsets = (
        ('Transaction Details', {
            'fields': (
                'key', 'transaction_type', 'amount', 'currency', 'net_amount'
            )
        }),
        ('Payment Information', {
            'fields': (
                'payment_method', 'payment_status', 'payment_date'
            )
        }),
        ('Customer Information', {
            'fields': (
                'email', 'customer_name', 'billing_address'
            )
        }),
        ('Processor Details', {
            'fields': (
                'processor_transaction_id', 'processor_name', 'processor_fee'
            ),
            'classes': ('collapse',)
        }),
        ('Related Entities', {
            'fields': (
                'related_quote_id', 'related_trip_id'
            )
        }),
        ('Additional Information', {
            'fields': (
                'description', 'reference_number', 'notes'
            ),
            'classes': ('collapse',)
        }),
        ('Status Flags', {
            'fields': (
                'is_successful', 'can_be_refunded'
            ),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_on', 'updated_on'),
            'classes': ('collapse',)
        }),
    )
    
    def net_amount(self, obj):
        """Display net amount after fees."""
        return f"${obj.net_amount:.2f}"
    net_amount.short_description = 'Net Amount'


class InvoiceLineItemInline(admin.TabularInline):
    """Inline admin for invoice line items."""
    model = InvoiceLineItem
    extra = 1
    readonly_fields = ['total_price']


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    """Admin configuration for Invoice model."""
    list_display = [
        'invoice_number', 'customer_email', 'total_amount', 'status',
        'issue_date', 'due_date', 'is_overdue', 'amount_paid'
    ]
    list_filter = [
        'status', 'currency', 'issue_date', 'due_date', 'paid_date'
    ]
    search_fields = [
        'invoice_number', 'customer_email', 'customer_name', 'description'
    ]
    readonly_fields = [
        'id', 'invoice_number', 'is_overdue', 'days_overdue',
        'amount_paid', 'amount_remaining', 'created_on', 'updated_on'
    ]
    inlines = [InvoiceLineItemInline]
    
    fieldsets = (
        ('Invoice Information', {
            'fields': (
                'invoice_number', 'status', 'issue_date', 'due_date', 'paid_date'
            )
        }),
        ('Customer Information', {
            'fields': (
                'customer_email', 'customer_name', 'billing_address'
            )
        }),
        ('Financial Details', {
            'fields': (
                'subtotal', 'tax_amount', 'total_amount', 'currency',
                'amount_paid', 'amount_remaining'
            )
        }),
        ('Status Information', {
            'fields': (
                'sent_date', 'is_overdue', 'days_overdue'
            ),
            'classes': ('collapse',)
        }),
        ('Related Entities', {
            'fields': (
                'related_quote_id', 'related_trip_id'
            )
        }),
        ('Additional Information', {
            'fields': (
                'description', 'notes'
            ),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_on', 'updated_on'),
            'classes': ('collapse',)
        }),
    )
    
    def is_overdue(self, obj):
        """Display overdue status."""
        return obj.is_overdue
    is_overdue.boolean = True
    is_overdue.short_description = 'Overdue'
    
    def amount_paid(self, obj):
        """Display amount paid."""
        return f"${obj.amount_paid:.2f}"
    amount_paid.short_description = 'Amount Paid'


@admin.register(InvoiceLineItem)
class InvoiceLineItemAdmin(admin.ModelAdmin):
    """Admin configuration for InvoiceLineItem model."""
    list_display = [
        'invoice', 'description', 'quantity', 'unit_price', 
        'total_price', 'taxable'
    ]
    list_filter = ['taxable', 'tax_rate']
    search_fields = ['description', 'invoice__invoice_number']
    readonly_fields = ['id', 'total_price', 'created_on', 'updated_on']
    
    fieldsets = (
        ('Line Item Details', {
            'fields': (
                'invoice', 'description', 'quantity', 'unit_price', 'total_price'
            )
        }),
        ('Tax Information', {
            'fields': ('taxable', 'tax_rate')
        }),
        ('Timestamps', {
            'fields': ('created_on', 'updated_on'),
            'classes': ('collapse',)
        }),
    )


@admin.register(PaymentMethod)
class PaymentMethodAdmin(admin.ModelAdmin):
    """Admin configuration for PaymentMethod model."""
    list_display = [
        'customer_email', 'payment_type', 'brand', 'last_four_digits',
        'is_default', 'is_active', 'is_expired'
    ]
    list_filter = [
        'payment_type', 'is_default', 'is_active', 'brand',
        'processor_name', 'expiry_year'
    ]
    search_fields = [
        'customer_email', 'customer_name', 'brand', 'last_four_digits',
        'processor_payment_method_id'
    ]
    readonly_fields = [
        'id', 'is_expired', 'created_on', 'updated_on'
    ]
    
    fieldsets = (
        ('Customer Information', {
            'fields': ('customer_email', 'customer_name')
        }),
        ('Payment Method Details', {
            'fields': (
                'payment_type', 'is_default', 'is_active'
            )
        }),
        ('Card Information', {
            'fields': (
                'last_four_digits', 'brand', 'expiry_month', 
                'expiry_year', 'is_expired'
            )
        }),
        ('Processor Information', {
            'fields': (
                'processor_payment_method_id', 'processor_name'
            ),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_on', 'updated_on'),
            'classes': ('collapse',)
        }),
    )
    
    def is_expired(self, obj):
        """Display expiration status."""
        return obj.is_expired
    is_expired.boolean = True
    is_expired.short_description = 'Expired'

```


# File: finance/services/finance_service.py

```python
from django.utils import timezone
from django.db import transaction
from decimal import Decimal
from ..models import Transaction, Invoice, InvoiceLineItem, PaymentMethod
import uuid
import logging

logger = logging.getLogger(__name__)


class TransactionService:
    """Service for transaction management operations."""
    
    @staticmethod
    def create_transaction(amount, currency, payment_method, email, customer_name=None,
                          transaction_type='payment', description=None, related_quote_id=None,
                          related_trip_id=None, billing_address=None):
        """Create a new transaction."""
        try:
            transaction_obj = Transaction.objects.create(
                amount=amount,
                currency=currency,
                payment_method=payment_method,
                email=email,
                customer_name=customer_name,
                transaction_type=transaction_type,
                description=description,
                related_quote_id=related_quote_id,
                related_trip_id=related_trip_id,
                billing_address=billing_address or {},
                payment_status='created'
            )
            
            logger.info(f"Transaction created: {transaction_obj.key} - ${amount}")
            return transaction_obj
            
        except Exception as e:
            logger.error(f"Error creating transaction: {str(e)}")
            raise
    
    @staticmethod
    def process_payment(transaction_id, processor_transaction_id, processor_name, 
                       processor_fee=None):
        """Process a payment transaction."""
        try:
            with transaction.atomic():
                trans = Transaction.objects.select_for_update().get(id=transaction_id)
                
                if trans.payment_status != 'created':
                    logger.error(f"Transaction not in processable state: {trans.payment_status}")
                    return None
                
                trans.payment_status = 'processing'
                trans.processor_transaction_id = processor_transaction_id
                trans.processor_name = processor_name
                trans.processor_fee = processor_fee
                trans.save()
                
                logger.info(f"Transaction processing: {trans.key}")
                return trans
                
        except Transaction.DoesNotExist:
            logger.error(f"Transaction not found: {transaction_id}")
            return None
        except Exception as e:
            logger.error(f"Error processing payment: {str(e)}")
            raise
    
    @staticmethod
    def complete_payment(transaction_id):
        """Mark a payment as completed."""
        try:
            trans = Transaction.objects.get(id=transaction_id)
            trans.payment_status = 'completed'
            trans.payment_date = timezone.now()
            trans.save()
            
            logger.info(f"Transaction completed: {trans.key}")
            return trans
            
        except Transaction.DoesNotExist:
            logger.error(f"Transaction not found: {transaction_id}")
            return None
    
    @staticmethod
    def fail_payment(transaction_id, reason=None):
        """Mark a payment as failed."""
        try:
            trans = Transaction.objects.get(id=transaction_id)
            trans.payment_status = 'failed'
            if reason:
                trans.notes = reason
            trans.save()
            
            logger.info(f"Transaction failed: {trans.key}")
            return trans
            
        except Transaction.DoesNotExist:
            logger.error(f"Transaction not found: {transaction_id}")
            return None
    
    @staticmethod
    def create_refund(original_transaction_id, refund_amount=None, reason=None):
        """Create a refund transaction."""
        try:
            original = Transaction.objects.get(id=original_transaction_id)
            
            if not original.can_be_refunded:
                logger.error(f"Transaction cannot be refunded: {original.key}")
                return None
            
            refund_amount = refund_amount or original.amount
            
            refund = Transaction.objects.create(
                amount=refund_amount,
                currency=original.currency,
                payment_method=original.payment_method,
                email=original.email,
                customer_name=original.customer_name,
                transaction_type='refund',
                description=f"Refund for transaction {original.key}",
                related_quote_id=original.related_quote_id,
                related_trip_id=original.related_trip_id,
                billing_address=original.billing_address,
                payment_status='completed',
                notes=reason
            )
            
            logger.info(f"Refund created: {refund.key} for ${refund_amount}")
            return refund
            
        except Transaction.DoesNotExist:
            logger.error(f"Original transaction not found: {original_transaction_id}")
            return None
        except Exception as e:
            logger.error(f"Error creating refund: {str(e)}")
            raise


class InvoiceService:
    """Service for invoice management operations."""
    
    @staticmethod
    def create_invoice(customer_email, customer_name, line_items, due_days=30,
                      related_quote_id=None, related_trip_id=None, billing_address=None,
                      description=None, tax_rate=Decimal('0.00')):
        """Create a new invoice with line items."""
        try:
            with transaction.atomic():
                # Generate invoice number
                invoice_number = InvoiceService._generate_invoice_number()
                
                # Calculate totals
                subtotal = sum(item['total_price'] for item in line_items)
                tax_amount = subtotal * tax_rate
                total_amount = subtotal + tax_amount
                
                # Calculate due date
                due_date = timezone.now().date() + timezone.timedelta(days=due_days)
                
                # Create invoice
                invoice = Invoice.objects.create(
                    invoice_number=invoice_number,
                    customer_email=customer_email,
                    customer_name=customer_name,
                    billing_address=billing_address or {},
                    subtotal=subtotal,
                    tax_amount=tax_amount,
                    total_amount=total_amount,
                    due_date=due_date,
                    related_quote_id=related_quote_id,
                    related_trip_id=related_trip_id,
                    description=description,
                    status='draft'
                )
                
                # Create line items
                for item_data in line_items:
                    InvoiceLineItem.objects.create(
                        invoice=invoice,
                        description=item_data['description'],
                        quantity=item_data.get('quantity', Decimal('1.00')),
                        unit_price=item_data['unit_price'],
                        total_price=item_data['total_price'],
                        taxable=item_data.get('taxable', True),
                        tax_rate=tax_rate if item_data.get('taxable', True) else Decimal('0.00')
                    )
                
                logger.info(f"Invoice created: {invoice.invoice_number} - ${total_amount}")
                return invoice
                
        except Exception as e:
            logger.error(f"Error creating invoice: {str(e)}")
            raise
    
    @staticmethod
    def _generate_invoice_number():
        """Generate a unique invoice number."""
        timestamp = timezone.now().strftime('%Y%m%d')
        count = Invoice.objects.filter(
            invoice_number__startswith=f"INV-{timestamp}"
        ).count() + 1
        return f"INV-{timestamp}-{count:04d}"
    
    @staticmethod
    def send_invoice(invoice_id):
        """Mark invoice as sent."""
        try:
            invoice = Invoice.objects.get(id=invoice_id)
            invoice.status = 'sent'
            invoice.sent_date = timezone.now()
            invoice.save()
            
            logger.info(f"Invoice sent: {invoice.invoice_number}")
            return invoice
            
        except Invoice.DoesNotExist:
            logger.error(f"Invoice not found: {invoice_id}")
            return None
    
    @staticmethod
    def record_payment(invoice_id, transaction_id):
        """Record a payment against an invoice."""
        try:
            with transaction.atomic():
                invoice = Invoice.objects.get(id=invoice_id)
                trans = Transaction.objects.get(id=transaction_id)
                
                if trans.payment_status != 'completed':
                    logger.error(f"Cannot record incomplete payment: {trans.key}")
                    return None
                
                # Add transaction to invoice
                invoice.transactions.add(trans)
                
                # Update invoice status based on payment
                if invoice.amount_paid >= invoice.total_amount:
                    invoice.status = 'paid'
                    invoice.paid_date = timezone.now().date()
                
                invoice.save()
                
                logger.info(f"Payment recorded for invoice: {invoice.invoice_number}")
                return invoice
                
        except (Invoice.DoesNotExist, Transaction.DoesNotExist) as e:
            logger.error(f"Invoice or transaction not found: {str(e)}")
            return None
        except Exception as e:
            logger.error(f"Error recording payment: {str(e)}")
            raise
    
    @staticmethod
    def get_overdue_invoices():
        """Get all overdue invoices."""
        try:
            today = timezone.now().date()
            return Invoice.objects.filter(
                due_date__lt=today,
                status__in=['sent', 'viewed']
            ).order_by('due_date')
        except Exception as e:
            logger.error(f"Error getting overdue invoices: {str(e)}")
            return Invoice.objects.none()
    
    @staticmethod
    def cancel_invoice(invoice_id, reason=None):
        """Cancel an invoice."""
        try:
            invoice = Invoice.objects.get(id=invoice_id)
            
            if invoice.status == 'paid':
                logger.error(f"Cannot cancel paid invoice: {invoice.invoice_number}")
                return None
            
            invoice.status = 'cancelled'
            if reason:
                invoice.notes = reason
            invoice.save()
            
            logger.info(f"Invoice cancelled: {invoice.invoice_number}")
            return invoice
            
        except Invoice.DoesNotExist:
            logger.error(f"Invoice not found: {invoice_id}")
            return None


class PaymentMethodService:
    """Service for payment method management."""
    
    @staticmethod
    def create_payment_method(customer_email, payment_type, processor_payment_method_id,
                             processor_name, customer_name=None, last_four_digits=None,
                             brand=None, expiry_month=None, expiry_year=None, is_default=False):
        """Create a new payment method."""
        try:
            with transaction.atomic():
                # If this is set as default, unset other defaults for this customer
                if is_default:
                    PaymentMethod.objects.filter(
                        customer_email=customer_email,
                        is_default=True
                    ).update(is_default=False)
                
                payment_method = PaymentMethod.objects.create(
                    customer_email=customer_email,
                    customer_name=customer_name,
                    payment_type=payment_type,
                    processor_payment_method_id=processor_payment_method_id,
                    processor_name=processor_name,
                    last_four_digits=last_four_digits,
                    brand=brand,
                    expiry_month=expiry_month,
                    expiry_year=expiry_year,
                    is_default=is_default,
                    is_active=True
                )
                
                logger.info(f"Payment method created for {customer_email}")
                return payment_method
                
        except Exception as e:
            logger.error(f"Error creating payment method: {str(e)}")
            raise
    
    @staticmethod
    def get_customer_payment_methods(customer_email, active_only=True):
        """Get payment methods for a customer."""
        try:
            queryset = PaymentMethod.objects.filter(customer_email=customer_email)
            if active_only:
                queryset = queryset.filter(is_active=True)
            return queryset.order_by('-is_default', '-created_on')
        except Exception as e:
            logger.error(f"Error getting payment methods: {str(e)}")
            return PaymentMethod.objects.none()
    
    @staticmethod
    def set_default_payment_method(payment_method_id):
        """Set a payment method as default for the customer."""
        try:
            with transaction.atomic():
                payment_method = PaymentMethod.objects.get(id=payment_method_id)
                
                # Unset other defaults for this customer
                PaymentMethod.objects.filter(
                    customer_email=payment_method.customer_email,
                    is_default=True
                ).update(is_default=False)
                
                # Set this one as default
                payment_method.is_default = True
                payment_method.save()
                
                logger.info(f"Default payment method set for {payment_method.customer_email}")
                return payment_method
                
        except PaymentMethod.DoesNotExist:
            logger.error(f"Payment method not found: {payment_method_id}")
            return None
        except Exception as e:
            logger.error(f"Error setting default payment method: {str(e)}")
            raise
    
    @staticmethod
    def deactivate_payment_method(payment_method_id):
        """Deactivate a payment method."""
        try:
            payment_method = PaymentMethod.objects.get(id=payment_method_id)
            payment_method.is_active = False
            payment_method.is_default = False
            payment_method.save()
            
            logger.info(f"Payment method deactivated: {payment_method_id}")
            return payment_method
            
        except PaymentMethod.DoesNotExist:
            logger.error(f"Payment method not found: {payment_method_id}")
            return None

```


# File: finance/services/payment_processor.py

```python
"""
Payment Processing Service for Finance Operations

Moved from utils/paymentprocess/ to finance/services/payment_processor.py
This service handles payment processing integration with external providers.
"""

import requests
import logging
from decimal import Decimal
from django.conf import settings
from django.utils import timezone
from ..models import Transaction, PaymentMethod
from .finance_service import TransactionService

logger = logging.getLogger(__name__)


class PaymentProcessorService:
    """
    Service for handling payment processing with external providers
    """
    
    def __init__(self, provider='stripe'):
        self.provider = provider
        self.api_key = self._get_api_key()
        self.base_url = self._get_base_url()
        
    def _get_api_key(self):
        """Get API key for the payment provider"""
        if self.provider == 'stripe':
            return getattr(settings, 'STRIPE_SECRET_KEY', None)
        elif self.provider == 'square':
            return getattr(settings, 'SQUARE_ACCESS_TOKEN', None)
        elif self.provider == 'paypal':
            return getattr(settings, 'PAYPAL_CLIENT_SECRET', None)
        return None
    
    def _get_base_url(self):
        """Get base URL for the payment provider API"""
        if self.provider == 'stripe':
            return 'https://api.stripe.com/v1'
        elif self.provider == 'square':
            sandbox = getattr(settings, 'SQUARE_SANDBOX', True)
            return 'https://connect.squareupsandbox.com/v2' if sandbox else 'https://connect.squareup.com/v2'
        elif self.provider == 'paypal':
            sandbox = getattr(settings, 'PAYPAL_SANDBOX', True)
            return 'https://api.sandbox.paypal.com' if sandbox else 'https://api.paypal.com'
        return None
    
    def create_payment_intent(self, amount, currency='USD', customer_email=None, 
                            description=None, metadata=None):
        """
        Create a payment intent with the payment provider
        
        Args:
            amount: Payment amount in cents/smallest currency unit
            currency: Currency code (default: USD)
            customer_email: Customer email address
            description: Payment description
            metadata: Additional metadata
            
        Returns:
            dict: Payment intent data or None if error
        """
        try:
            if self.provider == 'stripe':
                return self._create_stripe_payment_intent(
                    amount, currency, customer_email, description, metadata
                )
            elif self.provider == 'square':
                return self._create_square_payment(
                    amount, currency, customer_email, description, metadata
                )
            else:
                logger.error(f"Unsupported payment provider: {self.provider}")
                return None
                
        except Exception as e:
            logger.error(f"Error creating payment intent: {str(e)}")
            return None
    
    def _create_stripe_payment_intent(self, amount, currency, customer_email, description, metadata):
        """Create Stripe payment intent"""
        if not self.api_key:
            logger.error("Stripe API key not configured")
            return None
        
        headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        
        data = {
            'amount': int(amount * 100),  # Convert to cents
            'currency': currency.lower(),
            'automatic_payment_methods[enabled]': 'true'
        }
        
        if customer_email:
            data['receipt_email'] = customer_email
        
        if description:
            data['description'] = description
        
        if metadata:
            for key, value in metadata.items():
                data[f'metadata[{key}]'] = str(value)
        
        try:
            response = requests.post(
                f'{self.base_url}/payment_intents',
                headers=headers,
                data=data,
                timeout=30
            )
            response.raise_for_status()
            
            result = response.json()
            logger.info(f"Created Stripe payment intent: {result['id']}")
            
            return {
                'id': result['id'],
                'client_secret': result['client_secret'],
                'amount': result['amount'] / 100,  # Convert back to dollars
                'currency': result['currency'].upper(),
                'status': result['status'],
                'provider': 'stripe'
            }
            
        except requests.RequestException as e:
            logger.error(f"Stripe API error: {str(e)}")
            return None
    
    def _create_square_payment(self, amount, currency, customer_email, description, metadata):
        """Create Square payment"""
        if not self.api_key:
            logger.error("Square access token not configured")
            return None
        
        headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json',
            'Square-Version': '2023-10-18'
        }
        
        # Square uses cents for USD
        amount_money = {
            'amount': int(amount * 100),
            'currency': currency.upper()
        }
        
        data = {
            'source_id': 'EXTERNAL',  # This would be replaced with actual payment source
            'amount_money': amount_money,
            'idempotency_key': f"payment_{timezone.now().timestamp()}"
        }
        
        if description:
            data['note'] = description
        
        try:
            response = requests.post(
                f'{self.base_url}/payments',
                headers=headers,
                json=data,
                timeout=30
            )
            response.raise_for_status()
            
            result = response.json()
            payment = result.get('payment', {})
            
            logger.info(f"Created Square payment: {payment.get('id')}")
            
            return {
                'id': payment.get('id'),
                'amount': payment.get('amount_money', {}).get('amount', 0) / 100,
                'currency': payment.get('amount_money', {}).get('currency', currency),
                'status': payment.get('status', 'unknown'),
                'provider': 'square'
            }
            
        except requests.RequestException as e:
            logger.error(f"Square API error: {str(e)}")
            return None
    
    def confirm_payment(self, payment_intent_id, payment_method_id=None):
        """
        Confirm a payment intent
        
        Args:
            payment_intent_id: Payment intent ID from provider
            payment_method_id: Payment method ID (if required)
            
        Returns:
            dict: Payment confirmation data or None if error
        """
        try:
            if self.provider == 'stripe':
                return self._confirm_stripe_payment(payment_intent_id, payment_method_id)
            elif self.provider == 'square':
                return self._get_square_payment_status(payment_intent_id)
            else:
                logger.error(f"Unsupported payment provider: {self.provider}")
                return None
                
        except Exception as e:
            logger.error(f"Error confirming payment: {str(e)}")
            return None
    
    def _confirm_stripe_payment(self, payment_intent_id, payment_method_id):
        """Confirm Stripe payment intent"""
        if not self.api_key:
            logger.error("Stripe API key not configured")
            return None
        
        headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        
        data = {}
        if payment_method_id:
            data['payment_method'] = payment_method_id
        
        try:
            response = requests.post(
                f'{self.base_url}/payment_intents/{payment_intent_id}/confirm',
                headers=headers,
                data=data,
                timeout=30
            )
            response.raise_for_status()
            
            result = response.json()
            logger.info(f"Confirmed Stripe payment: {payment_intent_id}")
            
            return {
                'id': result['id'],
                'status': result['status'],
                'amount': result['amount'] / 100,
                'currency': result['currency'].upper(),
                'provider': 'stripe'
            }
            
        except requests.RequestException as e:
            logger.error(f"Stripe confirmation error: {str(e)}")
            return None
    
    def _get_square_payment_status(self, payment_id):
        """Get Square payment status"""
        if not self.api_key:
            logger.error("Square access token not configured")
            return None
        
        headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Square-Version': '2023-10-18'
        }
        
        try:
            response = requests.get(
                f'{self.base_url}/payments/{payment_id}',
                headers=headers,
                timeout=30
            )
            response.raise_for_status()
            
            result = response.json()
            payment = result.get('payment', {})
            
            return {
                'id': payment.get('id'),
                'status': payment.get('status', 'unknown'),
                'amount': payment.get('amount_money', {}).get('amount', 0) / 100,
                'currency': payment.get('amount_money', {}).get('currency', 'USD'),
                'provider': 'square'
            }
            
        except requests.RequestException as e:
            logger.error(f"Square status check error: {str(e)}")
            return None
    
    def create_refund(self, payment_id, amount=None, reason=None):
        """
        Create a refund for a payment
        
        Args:
            payment_id: Original payment ID
            amount: Refund amount (None for full refund)
            reason: Refund reason
            
        Returns:
            dict: Refund data or None if error
        """
        try:
            if self.provider == 'stripe':
                return self._create_stripe_refund(payment_id, amount, reason)
            elif self.provider == 'square':
                return self._create_square_refund(payment_id, amount, reason)
            else:
                logger.error(f"Unsupported payment provider: {self.provider}")
                return None
                
        except Exception as e:
            logger.error(f"Error creating refund: {str(e)}")
            return None
    
    def _create_stripe_refund(self, payment_intent_id, amount, reason):
        """Create Stripe refund"""
        if not self.api_key:
            logger.error("Stripe API key not configured")
            return None
        
        headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        
        data = {
            'payment_intent': payment_intent_id
        }
        
        if amount:
            data['amount'] = int(amount * 100)  # Convert to cents
        
        if reason:
            data['reason'] = reason
        
        try:
            response = requests.post(
                f'{self.base_url}/refunds',
                headers=headers,
                data=data,
                timeout=30
            )
            response.raise_for_status()
            
            result = response.json()
            logger.info(f"Created Stripe refund: {result['id']}")
            
            return {
                'id': result['id'],
                'amount': result['amount'] / 100,
                'currency': result['currency'].upper(),
                'status': result['status'],
                'provider': 'stripe'
            }
            
        except requests.RequestException as e:
            logger.error(f"Stripe refund error: {str(e)}")
            return None
    
    def _create_square_refund(self, payment_id, amount, reason):
        """Create Square refund"""
        if not self.api_key:
            logger.error("Square access token not configured")
            return None
        
        headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json',
            'Square-Version': '2023-10-18'
        }
        
        data = {
            'payment_id': payment_id,
            'idempotency_key': f"refund_{timezone.now().timestamp()}"
        }
        
        if amount:
            data['amount_money'] = {
                'amount': int(amount * 100),
                'currency': 'USD'
            }
        
        if reason:
            data['reason'] = reason
        
        try:
            response = requests.post(
                f'{self.base_url}/refunds',
                headers=headers,
                json=data,
                timeout=30
            )
            response.raise_for_status()
            
            result = response.json()
            refund = result.get('refund', {})
            
            logger.info(f"Created Square refund: {refund.get('id')}")
            
            return {
                'id': refund.get('id'),
                'amount': refund.get('amount_money', {}).get('amount', 0) / 100,
                'currency': refund.get('amount_money', {}).get('currency', 'USD'),
                'status': refund.get('status', 'unknown'),
                'provider': 'square'
            }
            
        except requests.RequestException as e:
            logger.error(f"Square refund error: {str(e)}")
            return None
    
    def process_transaction(self, transaction_id, payment_method_data=None):
        """
        Process a transaction through the payment provider
        
        Args:
            transaction_id: Internal transaction ID
            payment_method_data: Payment method information
            
        Returns:
            Transaction instance or None if error
        """
        try:
            transaction = Transaction.objects.get(id=transaction_id)
            
            if transaction.payment_status != 'created':
                logger.error(f"Transaction {transaction_id} not in processable state")
                return None
            
            # Create payment intent
            payment_intent = self.create_payment_intent(
                amount=transaction.amount,
                currency=transaction.currency,
                customer_email=transaction.email,
                description=transaction.description,
                metadata={
                    'transaction_id': str(transaction.id),
                    'customer_name': transaction.customer_name or ''
                }
            )
            
            if not payment_intent:
                logger.error(f"Failed to create payment intent for transaction {transaction_id}")
                return None
            
            # Update transaction with payment provider details
            updated_transaction = TransactionService.process_payment(
                transaction_id=transaction.id,
                processor_transaction_id=payment_intent['id'],
                processor_name=self.provider
            )
            
            return updated_transaction
            
        except Transaction.DoesNotExist:
            logger.error(f"Transaction not found: {transaction_id}")
            return None
        except Exception as e:
            logger.error(f"Error processing transaction {transaction_id}: {str(e)}")
            return None


# Convenience functions for backward compatibility
def create_payment_intent(amount, currency='USD', customer_email=None, description=None):
    """Create a payment intent"""
    service = PaymentProcessorService()
    return service.create_payment_intent(amount, currency, customer_email, description)


def process_transaction(transaction_id, payment_method_data=None):
    """Process a transaction"""
    service = PaymentProcessorService()
    return service.process_transaction(transaction_id, payment_method_data)

```


# File: finance/services/__init__.py

```python

```


# File: finance/tests/test_payment_processor.py

```python
"""
Django test cases for payment processing functionality.

Converted from custom test scripts to proper Django TestCase.
"""

from django.test import TestCase
from django.contrib.auth.models import User
from unittest.mock import Mock, patch, MagicMock
from decimal import Decimal
from datetime import date, timedelta
from finance.services.payment_processor import PaymentProcessorService
from finance.services.finance_service import FinanceService, InvoiceService
from finance.models import Transaction, PaymentMethod, Invoice, LineItem
from contacts.models import Contact


class PaymentProcessorServiceTest(TestCase):
    """Test cases for PaymentProcessorService."""
    
    def setUp(self):
        """Set up test data."""
        self.service = PaymentProcessorService()
        
    @patch('stripe.PaymentIntent.create')
    def test_stripe_payment_intent_creation(self, mock_stripe_create):
        """Test Stripe payment intent creation."""
        # Mock Stripe response
        mock_intent = Mock()
        mock_intent.id = 'pi_test123'
        mock_intent.client_secret = 'pi_test123_secret'
        mock_intent.status = 'requires_payment_method'
        mock_stripe_create.return_value = mock_intent
        
        result = self.service.create_payment_intent(
            amount=Decimal('100.00'),
            currency='usd',
            provider='stripe'
        )
        
        self.assertEqual(result['payment_intent_id'], 'pi_test123')
        self.assertEqual(result['client_secret'], 'pi_test123_secret')
        self.assertEqual(result['status'], 'requires_payment_method')
        
    @patch('squareup.payments_api.PaymentsApi.create_payment')
    def test_square_payment_creation(self, mock_square_create):
        """Test Square payment creation."""
        # Mock Square response
        mock_response = Mock()
        mock_payment = Mock()
        mock_payment.id = 'sq_test123'
        mock_payment.status = 'COMPLETED'
        mock_response.body = {'payment': mock_payment}
        mock_square_create.return_value = mock_response
        
        result = self.service.process_payment(
            amount=Decimal('50.00'),
            payment_method_token='cnon:test-token',
            provider='square'
        )
        
        self.assertEqual(result['transaction_id'], 'sq_test123')
        self.assertEqual(result['status'], 'COMPLETED')
        
    def test_unsupported_provider_error(self):
        """Test error handling for unsupported payment provider."""
        with self.assertRaises(ValueError):
            self.service.create_payment_intent(
                amount=Decimal('100.00'),
                provider='unsupported_provider'
            )
            
    @patch('stripe.Refund.create')
    def test_stripe_refund_processing(self, mock_stripe_refund):
        """Test Stripe refund processing."""
        # Mock Stripe refund response
        mock_refund = Mock()
        mock_refund.id = 're_test123'
        mock_refund.status = 'succeeded'
        mock_refund.amount = 5000  # $50.00 in cents
        mock_stripe_refund.return_value = mock_refund
        
        result = self.service.process_refund(
            transaction_id='pi_original123',
            amount=Decimal('50.00'),
            provider='stripe'
        )
        
        self.assertEqual(result['refund_id'], 're_test123')
        self.assertEqual(result['status'], 'succeeded')
        self.assertEqual(result['amount'], Decimal('50.00'))
        
    def test_payment_validation(self):
        """Test payment amount and currency validation."""
        with self.assertRaises(ValueError):
            self.service.create_payment_intent(
                amount=Decimal('0.00'),  # Zero amount
                provider='stripe'
            )
            
        with self.assertRaises(ValueError):
            self.service.create_payment_intent(
                amount=Decimal('-10.00'),  # Negative amount
                provider='stripe'
            )


class FinanceServiceTest(TestCase):
    """Test cases for FinanceService business logic."""
    
    def setUp(self):
        """Set up test data."""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
        self.contact = Contact.objects.create(
            first_name='John',
            last_name='Customer',
            email='john@example.com',
            phone='+1234567890'
        )
        
    def test_create_transaction_record(self):
        """Test transaction record creation."""
        transaction = FinanceService.create_transaction(
            transaction_id='txn_test123',
            amount=Decimal('250.00'),
            currency='USD',
            payment_provider='stripe',
            customer_email='john@example.com',
            description='Test flight payment'
        )
        
        self.assertEqual(transaction.transaction_id, 'txn_test123')
        self.assertEqual(transaction.amount, Decimal('250.00'))
        self.assertEqual(transaction.currency, 'USD')
        self.assertEqual(transaction.status, 'pending')
        
    def test_calculate_payment_fees(self):
        """Test payment fee calculations."""
        # Stripe fees: 2.9% + $0.30
        stripe_fee = FinanceService.calculate_payment_fees(
            amount=Decimal('100.00'),
            provider='stripe'
        )
        expected_stripe = Decimal('100.00') * Decimal('0.029') + Decimal('0.30')
        self.assertEqual(stripe_fee, expected_stripe)
        
        # Square fees: 2.6% + $0.10
        square_fee = FinanceService.calculate_payment_fees(
            amount=Decimal('100.00'),
            provider='square'
        )
        expected_square = Decimal('100.00') * Decimal('0.026') + Decimal('0.10')
        self.assertEqual(square_fee, expected_square)
        
    def test_transaction_status_updates(self):
        """Test transaction status transitions."""
        transaction = Transaction.objects.create(
            transaction_id='status_test',
            amount=Decimal('100.00'),
            currency='USD',
            status='pending'
        )
        
        # Valid transition: pending -> completed
        updated = FinanceService.update_transaction_status(
            transaction.id, 'completed'
        )
        self.assertEqual(updated.status, 'completed')
        
        # Invalid transition: completed -> pending
        with self.assertRaises(ValueError):
            FinanceService.update_transaction_status(
                transaction.id, 'pending'
            )


class InvoiceServiceTest(TestCase):
    """Test cases for InvoiceService."""
    
    def setUp(self):
        """Set up test data."""
        self.contact = Contact.objects.create(
            first_name='Jane',
            last_name='Client',
            email='jane@example.com',
            company='Test Aviation'
        )
        
    def test_create_invoice_with_line_items(self):
        """Test invoice creation with line items."""
        invoice = InvoiceService.create_invoice(
            customer=self.contact,
            invoice_number='INV-2024-001',
            due_date=date.today() + timedelta(days=30),
            line_items=[
                {
                    'description': 'Flight JFK-LAX',
                    'quantity': 1,
                    'unit_price': Decimal('15000.00')
                },
                {
                    'description': 'Ground handling',
                    'quantity': 2,
                    'unit_price': Decimal('500.00')
                }
            ]
        )
        
        self.assertEqual(invoice.customer, self.contact)
        self.assertEqual(invoice.invoice_number, 'INV-2024-001')
        self.assertEqual(invoice.status, 'draft')
        
        # Check line items
        line_items = invoice.line_items.all()
        self.assertEqual(line_items.count(), 2)
        
        # Check total calculation
        expected_total = Decimal('15000.00') + (Decimal('500.00') * 2)
        self.assertEqual(invoice.total_amount, expected_total)
        
    def test_invoice_payment_tracking(self):
        """Test invoice payment tracking."""
        invoice = Invoice.objects.create(
            customer=self.contact,
            invoice_number='PAY-TEST-001',
            total_amount=Decimal('1000.00'),
            status='sent'
        )
        
        # Record partial payment
        InvoiceService.record_payment(
            invoice_id=invoice.id,
            amount=Decimal('600.00'),
            payment_method='credit_card',
            transaction_id='txn_partial'
        )
        
        invoice.refresh_from_db()
        self.assertEqual(invoice.paid_amount, Decimal('600.00'))
        self.assertEqual(invoice.balance_due, Decimal('400.00'))
        self.assertEqual(invoice.status, 'partially_paid')
        
        # Record remaining payment
        InvoiceService.record_payment(
            invoice_id=invoice.id,
            amount=Decimal('400.00'),
            payment_method='credit_card',
            transaction_id='txn_final'
        )
        
        invoice.refresh_from_db()
        self.assertEqual(invoice.paid_amount, Decimal('1000.00'))
        self.assertEqual(invoice.balance_due, Decimal('0.00'))
        self.assertEqual(invoice.status, 'paid')
        
    def test_overdue_invoice_detection(self):
        """Test overdue invoice detection."""
        past_due_date = date.today() - timedelta(days=5)
        
        overdue_invoice = Invoice.objects.create(
            customer=self.contact,
            invoice_number='OVERDUE-001',
            total_amount=Decimal('500.00'),
            due_date=past_due_date,
            status='sent'
        )
        
        overdue_invoices = InvoiceService.get_overdue_invoices()
        self.assertIn(overdue_invoice, overdue_invoices)
        
        # Check days overdue calculation
        days_overdue = InvoiceService.calculate_days_overdue(overdue_invoice)
        self.assertEqual(days_overdue, 5)


class TransactionModelTest(TestCase):
    """Test cases for Transaction model."""
    
    def test_transaction_creation(self):
        """Test Transaction model creation."""
        transaction = Transaction.objects.create(
            transaction_id='test_txn_123',
            amount=Decimal('150.00'),
            currency='USD',
            status='completed',
            payment_provider='stripe',
            description='Test payment'
        )
        
        self.assertEqual(transaction.transaction_id, 'test_txn_123')
        self.assertEqual(transaction.amount, Decimal('150.00'))
        self.assertEqual(transaction.currency, 'USD')
        self.assertEqual(transaction.status, 'completed')
        self.assertEqual(str(transaction), 'test_txn_123 - $150.00')
        
    def test_transaction_amount_validation(self):
        """Test transaction amount validation."""
        with self.assertRaises(Exception):
            Transaction.objects.create(
                transaction_id='invalid_txn',
                amount=Decimal('-50.00'),  # Negative amount should fail
                currency='USD',
                status='pending'
            )


class PaymentMethodModelTest(TestCase):
    """Test cases for PaymentMethod model."""
    
    def test_payment_method_creation(self):
        """Test PaymentMethod model creation."""
        payment_method = PaymentMethod.objects.create(
            customer_email='test@example.com',
            provider='stripe',
            provider_payment_method_id='pm_test123',
            payment_type='card',
            last_four_digits='4242',
            expiry_month=12,
            expiry_year=2025
        )
        
        self.assertEqual(payment_method.customer_email, 'test@example.com')
        self.assertEqual(payment_method.provider, 'stripe')
        self.assertEqual(payment_method.last_four_digits, '4242')
        self.assertTrue(payment_method.is_active)
        
    def test_payment_method_masking(self):
        """Test payment method number masking."""
        payment_method = PaymentMethod.objects.create(
            customer_email='mask@example.com',
            provider='square',
            payment_type='card',
            last_four_digits='1234'
        )
        
        masked = payment_method.get_masked_number()
        self.assertEqual(masked, '****-****-****-1234')
        
    def test_expired_payment_method_detection(self):
        """Test detection of expired payment methods."""
        # Create expired payment method
        expired_method = PaymentMethod.objects.create(
            customer_email='expired@example.com',
            provider='stripe',
            payment_type='card',
            last_four_digits='9999',
            expiry_month=1,
            expiry_year=2020  # Expired
        )
        
        self.assertTrue(expired_method.is_expired())
        
        # Create valid payment method
        valid_method = PaymentMethod.objects.create(
            customer_email='valid@example.com',
            provider='stripe',
            payment_type='card',
            last_four_digits='1111',
            expiry_month=12,
            expiry_year=2030  # Future
        )
        
        self.assertFalse(valid_method.is_expired())


class LineItemModelTest(TestCase):
    """Test cases for LineItem model."""
    
    def setUp(self):
        """Set up test data."""
        self.contact = Contact.objects.create(
            first_name='Test',
            last_name='Customer',
            email='customer@example.com'
        )
        
        self.invoice = Invoice.objects.create(
            customer=self.contact,
            invoice_number='LINE-TEST-001',
            total_amount=Decimal('0.00')
        )
        
    def test_line_item_total_calculation(self):
        """Test line item total calculation."""
        line_item = LineItem.objects.create(
            invoice=self.invoice,
            description='Test service',
            quantity=3,
            unit_price=Decimal('100.00'),
            tax_rate=Decimal('0.08')  # 8% tax
        )
        
        expected_subtotal = Decimal('300.00')  # 3 * 100
        expected_tax = expected_subtotal * Decimal('0.08')  # 24.00
        expected_total = expected_subtotal + expected_tax  # 324.00
        
        self.assertEqual(line_item.subtotal, expected_subtotal)
        self.assertEqual(line_item.tax_amount, expected_tax)
        self.assertEqual(line_item.total, expected_total)

```


# File: contacts/models.py

```python
from django.db import models
from common.models import BaseModel


class Contact(BaseModel):
    """Contact model for customers, crew, and other personnel."""
    first_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    business_name = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    
    # Address information
    address_line1 = models.CharField(max_length=255, blank=True, null=True)
    address_line2 = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    zip = models.CharField(max_length=20, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    
    # Travel document information
    nationality = models.CharField(max_length=100, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    passport_number = models.CharField(max_length=100, blank=True, null=True)
    passport_expiration_date = models.DateField(blank=True, null=True)

    class Meta:
        indexes = [
            models.Index(fields=['first_name', 'last_name']),
            models.Index(fields=['business_name']),
            models.Index(fields=['email']),
        ]

    def __str__(self):
        if self.business_name:
            return self.business_name
        return f"{self.first_name} {self.last_name}".strip() or "Unnamed Contact"
    
    def clean(self):
        """Validate that either name or business name is provided."""
        if not self.first_name and not self.last_name and not self.business_name:
            raise models.ValidationError("Either first/last name or business name is required")
    
    @property
    def full_name(self):
        """Return full name or business name."""
        if self.business_name:
            return self.business_name
        return f"{self.first_name} {self.last_name}".strip()


class FBO(BaseModel):
    """Fixed Base Operator model for airport services."""
    name = models.CharField(max_length=255)
    
    # Address information
    address_line1 = models.CharField(max_length=255, blank=True, null=True)
    address_line2 = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    zip = models.CharField(max_length=20, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    
    # Contact information
    contacts = models.ManyToManyField(Contact, related_name="fbos")
    phone = models.CharField(max_length=20, blank=True, null=True)
    phone_secondary = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)

    class Meta:
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['city', 'state']),
        ]
        verbose_name = "FBO"
        verbose_name_plural = "FBOs"
    
    def __str__(self):
        return self.name


class Ground(BaseModel):
    """Ground Transportation model for airport ground services."""
    name = models.CharField(max_length=255)
    
    # Address information
    address_line1 = models.CharField(max_length=255, blank=True, null=True)
    address_line2 = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    zip = models.CharField(max_length=20, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    
    # Contact information and notes
    notes = models.TextField(blank=True, null=True)
    contacts = models.ManyToManyField(Contact, related_name="grounds")

    class Meta:
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['city', 'state']),
        ]
        verbose_name = "Ground Transportation"
        verbose_name_plural = "Ground Transportation"
    
    def __str__(self):
        return self.name

```


# File: contacts/apps.py

```python
from django.apps import AppConfig


class ContactsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'contacts'
    verbose_name = 'Contact Management'

```


# File: contacts/__init__.py

```python

```


# File: contacts/admin.py

```python
"""
Admin configuration for contacts app.
"""
from django.contrib import admin
from .models import Contact, FBO, Ground


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    """Admin configuration for Contact model."""
    list_display = ('full_name', 'email', 'phone', 'company', 'contact_type', 'is_active')
    list_filter = ('contact_type', 'is_active', 'created_at')
    search_fields = ('first_name', 'last_name', 'email', 'phone', 'company')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Personal Information', {
            'fields': ('first_name', 'last_name', 'email', 'phone', 'date_of_birth')
        }),
        ('Professional Information', {
            'fields': ('company', 'title', 'contact_type')
        }),
        ('Address & Notes', {
            'fields': ('address', 'notes')
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )


@admin.register(FBO)
class FBOAdmin(admin.ModelAdmin):
    """Admin configuration for FBO model."""
    list_display = ('name', 'airport_code', 'phone', 'email', 'is_active')
    list_filter = ('is_active', 'created_at')
    search_fields = ('name', 'airport_code', 'phone', 'email', 'services_offered')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'airport_code', 'phone', 'email')
        }),
        ('Services & Details', {
            'fields': ('services_offered', 'operating_hours', 'notes')
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )


@admin.register(Ground)
class GroundAdmin(admin.ModelAdmin):
    """Admin configuration for Ground model."""
    list_display = ('company_name', 'airport_code', 'contact_person', 'phone', 'is_active')
    list_filter = ('is_active', 'created_at')
    search_fields = ('company_name', 'airport_code', 'contact_person', 'phone', 'services')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Company Information', {
            'fields': ('company_name', 'airport_code', 'contact_person', 'phone', 'email')
        }),
        ('Services & Details', {
            'fields': ('services', 'equipment', 'notes')
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )

```


# File: contacts/services/contact_service.py

```python
from django.core.exceptions import ValidationError
from django.db.models import Q
from typing import List, Dict, Any, Optional

from contacts.models import Contact, FBO, Ground


class ContactService:
    """Service class for Contact business logic."""
    
    def create_contact(self, contact_data: Dict[str, Any]) -> Contact:
        """Create a new contact with validation."""
        # Check for duplicate email
        if Contact.objects.filter(email=contact_data.get('email')).exists():
            raise ValidationError(f"Contact with email {contact_data.get('email')} already exists")
        
        contact = Contact.objects.create(**contact_data)
        return contact
    
    def update_contact(self, contact_id: int, update_data: Dict[str, Any]) -> Contact:
        """Update an existing contact."""
        contact = Contact.objects.get(id=contact_id)
        
        for field, value in update_data.items():
            setattr(contact, field, value)
        
        contact.full_clean()
        contact.save()
        return contact
    
    def search_contacts(self, query: str) -> List[Contact]:
        """Search contacts by name, email, or company."""
        return Contact.objects.filter(
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query) |
            Q(email__icontains=query) |
            Q(company__icontains=query)
        ).distinct()
    
    def get_contacts_by_company(self, company_name: str) -> List[Contact]:
        """Get all contacts for a specific company."""
        return Contact.objects.filter(company=company_name)
    
    def format_contact_name(self, contact_id: int, include_title: bool = False) -> str:
        """Format contact name for display."""
        contact = Contact.objects.get(id=contact_id)
        name = f"{contact.first_name} {contact.last_name}"
        
        if include_title and contact.title:
            name += f", {contact.title}"
        
        return name
    
    def get_contact_history(self, contact_id: int) -> Dict[str, Any]:
        """Get interaction history for a contact."""
        trips = self.get_trip_history(contact_id)
        quotes = self.get_quote_history(contact_id)
        
        return {
            'trips': trips,
            'quotes': quotes,
            'total_interactions': len(trips) + len(quotes)
        }
    
    def get_trip_history(self, contact_id: int) -> List:
        """Get trip history for a contact."""
        # This would typically query the Trip model
        # Placeholder implementation
        return []
    
    def get_quote_history(self, contact_id: int) -> List:
        """Get quote history for a contact."""
        # This would typically query the Quote model
        # Placeholder implementation
        return []
    
    def merge_contacts(self, primary_contact_id: int, duplicate_contact_id: int, 
                      merge_data: Dict[str, Any]) -> Contact:
        """Merge duplicate contacts."""
        primary_contact = Contact.objects.get(id=primary_contact_id)
        duplicate_contact = Contact.objects.get(id=duplicate_contact_id)
        
        # Update primary contact with merged data
        for field, value in merge_data.items():
            setattr(primary_contact, field, value)
        
        primary_contact.save()
        
        # TODO: Transfer related records (trips, quotes, etc.) to primary contact
        
        # Delete duplicate contact
        duplicate_contact.delete()
        
        return primary_contact
    
    def create_fbo(self, fbo_data: Dict[str, Any]) -> FBO:
        """Create a new FBO."""
        fbo = FBO.objects.create(**fbo_data)
        return fbo
    
    def search_fbos_by_airport(self, airport_code: str) -> List[FBO]:
        """Search FBOs by airport code."""
        return FBO.objects.filter(airport_code=airport_code)
    
    def get_fbo_services(self, fbo_id: int) -> List[str]:
        """Get services offered by an FBO."""
        fbo = FBO.objects.get(id=fbo_id)
        if fbo.services_offered:
            return [service.strip() for service in fbo.services_offered.split(',')]
        return []
    
    def check_fbo_fuel_availability(self, fbo_id: int, fuel_type: str) -> bool:
        """Check if FBO has specific fuel type available."""
        fbo = FBO.objects.get(id=fbo_id)
        if fbo.fuel_types:
            available_fuels = [fuel.strip() for fuel in fbo.fuel_types.split(',')]
            return fuel_type in available_fuels
        return False
    
    def create_ground_service(self, ground_data: Dict[str, Any]) -> Ground:
        """Create a new ground service."""
        ground = Ground.objects.create(**ground_data)
        return ground
    
    def search_ground_services_by_airport(self, airport_code: str) -> List[Ground]:
        """Search ground services by airport code."""
        return Ground.objects.filter(airport_code=airport_code)
    
    def check_vehicle_availability(self, ground_service_id: int, vehicle_type: str) -> bool:
        """Check if ground service has specific vehicle type available."""
        ground_service = Ground.objects.get(id=ground_service_id)
        if ground_service.vehicle_types:
            available_vehicles = [vehicle.strip() for vehicle in ground_service.vehicle_types.split(',')]
            return vehicle_type in available_vehicles
        return False
    
    def get_ground_service_coverage(self, ground_service_id: int) -> str:
        """Get coverage area for ground service."""
        ground_service = Ground.objects.get(id=ground_service_id)
        return ground_service.coverage_area or ""

```


# File: contacts/tests/test_models.py

```python
"""
Tests for contacts app models.
"""
from django.test import TestCase
from django.core.exceptions import ValidationError
from contacts.models import Contact, FBO, Ground


class ContactModelTest(TestCase):
    """Test cases for Contact model."""
    
    def test_contact_creation(self):
        """Test Contact creation with valid data."""
        contact = Contact.objects.create(
            first_name='John',
            last_name='Doe',
            email='john.doe@example.com',
            phone='+1234567890',
            company='Test Aviation',
            title='Operations Manager',
            contact_type='customer'
        )
        
        self.assertEqual(contact.first_name, 'John')
        self.assertEqual(contact.last_name, 'Doe')
        self.assertEqual(contact.email, 'john.doe@example.com')
        self.assertEqual(contact.contact_type, 'customer')
        self.assertTrue(contact.is_active)
        self.assertEqual(str(contact), 'John Doe')
        
    def test_contact_full_name_property(self):
        """Test Contact full_name property."""
        contact = Contact.objects.create(
            first_name='Jane',
            last_name='Smith',
            email='jane@example.com'
        )
        
        self.assertEqual(contact.full_name, 'Jane Smith')
        
    def test_contact_email_validation(self):
        """Test Contact email validation."""
        contact = Contact(
            first_name='Test',
            last_name='User',
            email='invalid-email'
        )
        
        with self.assertRaises(ValidationError):
            contact.full_clean()


class FBOModelTest(TestCase):
    """Test cases for FBO model."""
    
    def test_fbo_creation(self):
        """Test FBO creation with valid data."""
        fbo = FBO.objects.create(
            name='Test FBO Services',
            airport_code='KORD',
            phone='+1234567890',
            email='services@testfbo.com',
            services_offered='Fuel, Hangar, Catering'
        )
        
        self.assertEqual(fbo.name, 'Test FBO Services')
        self.assertEqual(fbo.airport_code, 'KORD')
        self.assertEqual(fbo.services_offered, 'Fuel, Hangar, Catering')
        self.assertTrue(fbo.is_active)
        self.assertEqual(str(fbo), 'Test FBO Services (KORD)')
        
    def test_fbo_airport_code_format(self):
        """Test FBO airport code format validation."""
        fbo = FBO.objects.create(
            name='Test FBO',
            airport_code='kord',  # lowercase
            phone='+1234567890'
        )
        
        # Should be converted to uppercase
        self.assertEqual(fbo.airport_code, 'KORD')


class GroundModelTest(TestCase):
    """Test cases for Ground model."""
    
    def test_ground_creation(self):
        """Test Ground creation with valid data."""
        ground = Ground.objects.create(
            company_name='Elite Ground Services',
            airport_code='KJFK',
            contact_person='Mike Johnson',
            phone='+1987654321',
            services='Ground handling, Baggage, Catering'
        )
        
        self.assertEqual(ground.company_name, 'Elite Ground Services')
        self.assertEqual(ground.airport_code, 'KJFK')
        self.assertEqual(ground.contact_person, 'Mike Johnson')
        self.assertEqual(ground.services, 'Ground handling, Baggage, Catering')
        self.assertTrue(ground.is_active)
        self.assertEqual(str(ground), 'Elite Ground Services (KJFK)')
        
    def test_ground_airport_code_validation(self):
        """Test Ground airport code validation."""
        ground = Ground.objects.create(
            company_name='Test Ground',
            airport_code='jfk',  # lowercase
            contact_person='Test Person'
        )
        
        # Should be converted to uppercase
        self.assertEqual(ground.airport_code, 'JFK')

```


# File: contacts/tests/test_api.py

```python
from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status

from contacts.models import Contact, FBO, Ground


class ContactAPITest(TestCase):
    """Test cases for Contact API endpoints."""
    
    def setUp(self):
        """Set up test data."""
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.force_authenticate(user=self.user)
        
        self.contact = Contact.objects.create(
            first_name='John',
            last_name='Doe',
            email='john.doe@example.com',
            phone='555-1234',
            company='Test Company',
            title='Manager'
        )
    
    def test_list_contacts(self):
        """Test listing contacts."""
        url = reverse('contact-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['first_name'], 'John')
    
    def test_create_contact(self):
        """Test creating a contact."""
        url = reverse('contact-list')
        data = {
            'first_name': 'Jane',
            'last_name': 'Smith',
            'email': 'jane.smith@example.com',
            'phone': '555-5678',
            'company': 'New Company',
            'title': 'Director'
        }
        
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['first_name'], 'Jane')
        self.assertEqual(response.data['email'], 'jane.smith@example.com')
    
    def test_update_contact(self):
        """Test updating a contact."""
        url = reverse('contact-detail', kwargs={'pk': self.contact.pk})
        data = {
            'phone': '555-9999',
            'title': 'Senior Manager'
        }
        
        response = self.client.patch(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['phone'], '555-9999')
        self.assertEqual(response.data['title'], 'Senior Manager')
    
    def test_delete_contact(self):
        """Test deleting a contact."""
        url = reverse('contact-detail', kwargs={'pk': self.contact.pk})
        response = self.client.delete(url)
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Contact.objects.filter(pk=self.contact.pk).exists())
    
    def test_search_contacts(self):
        """Test contact search functionality."""
        # Create additional contacts
        Contact.objects.create(
            first_name='Alice',
            last_name='Johnson',
            email='alice.johnson@example.com',
            phone='555-1111',
            company='ABC Corp'
        )
        
        url = reverse('contact-list')
        response = self.client.get(url, {'search': 'Alice'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['first_name'], 'Alice')


class FBOAPITest(TestCase):
    """Test cases for FBO API endpoints."""
    
    def setUp(self):
        """Set up test data."""
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.force_authenticate(user=self.user)
        
        self.fbo = FBO.objects.create(
            name='Test FBO',
            airport_code='KJFK',
            phone='555-FBO1',
            email='info@testfbo.com',
            services_offered='Fuel, Hangar, Catering',
            fuel_types='Jet A, Avgas',
            operating_hours='24/7'
        )
    
    def test_list_fbos(self):
        """Test listing FBOs."""
        url = reverse('fbo-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], 'Test FBO')
    
    def test_create_fbo(self):
        """Test creating an FBO."""
        url = reverse('fbo-list')
        data = {
            'name': 'New FBO',
            'airport_code': 'KLAX',
            'phone': '555-FBO2',
            'email': 'info@newfbo.com',
            'services_offered': 'Fuel, Maintenance',
            'fuel_types': 'Jet A',
            'operating_hours': '6AM-10PM'
        }
        
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], 'New FBO')
        self.assertEqual(response.data['airport_code'], 'KLAX')
    
    def test_filter_fbos_by_airport(self):
        """Test filtering FBOs by airport code."""
        # Create FBO at different airport
        FBO.objects.create(
            name='LAX FBO',
            airport_code='KLAX',
            phone='555-FBO3',
            email='info@laxfbo.com'
        )
        
        url = reverse('fbo-list')
        response = self.client.get(url, {'airport_code': 'KJFK'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['airport_code'], 'KJFK')


class GroundAPITest(TestCase):
    """Test cases for Ground service API endpoints."""
    
    def setUp(self):
        """Set up test data."""
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.force_authenticate(user=self.user)
        
        self.ground_service = Ground.objects.create(
            name='Test Ground Services',
            airport_code='KJFK',
            phone='555-GRND',
            email='info@testground.com',
            services_offered='Transportation, Catering, Customs',
            vehicle_types='Sedan, SUV, Van',
            coverage_area='NYC Metro Area'
        )
    
    def test_list_ground_services(self):
        """Test listing ground services."""
        url = reverse('ground-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], 'Test Ground Services')
    
    def test_create_ground_service(self):
        """Test creating a ground service."""
        url = reverse('ground-list')
        data = {
            'name': 'New Ground Services',
            'airport_code': 'KLAX',
            'phone': '555-GRND2',
            'email': 'info@newground.com',
            'services_offered': 'Transportation, Concierge',
            'vehicle_types': 'Luxury Sedan, Limousine',
            'coverage_area': 'LA Metro Area'
        }
        
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], 'New Ground Services')
        self.assertEqual(response.data['airport_code'], 'KLAX')
    
    def test_filter_ground_services_by_airport(self):
        """Test filtering ground services by airport code."""
        # Create ground service at different airport
        Ground.objects.create(
            name='LAX Ground',
            airport_code='KLAX',
            phone='555-GRND3',
            email='info@laxground.com'
        )
        
        url = reverse('ground-list')
        response = self.client.get(url, {'airport_code': 'KJFK'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['airport_code'], 'KJFK')

```


# File: contacts/tests/__init__.py

```python

```


# File: contacts/tests/test_services.py

```python
from django.test import TestCase
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from unittest.mock import patch, Mock

from contacts.models import Contact, FBO, Ground
from contacts.services.contact_service import ContactService


class ContactServiceTest(TestCase):
    """Test cases for ContactService business logic."""
    
    def setUp(self):
        """Set up test data."""
        self.user = User.objects.create_user(username='testuser', password='testpass')
        
        self.contact = Contact.objects.create(
            first_name='John',
            last_name='Doe',
            email='john.doe@example.com',
            phone='555-1234',
            company='Test Company',
            title='Manager'
        )
        
        self.contact_service = ContactService()
    
    def test_create_contact(self):
        """Test contact creation through service."""
        contact_data = {
            'first_name': 'Jane',
            'last_name': 'Smith',
            'email': 'jane.smith@example.com',
            'phone': '555-5678',
            'company': 'New Company',
            'title': 'Director'
        }
        
        contact = self.contact_service.create_contact(contact_data)
        
        self.assertIsNotNone(contact)
        self.assertEqual(contact.first_name, 'Jane')
        self.assertEqual(contact.email, 'jane.smith@example.com')
        self.assertEqual(contact.company, 'New Company')
    
    def test_update_contact(self):
        """Test contact update."""
        update_data = {
            'phone': '555-9999',
            'title': 'Senior Manager'
        }
        
        updated_contact = self.contact_service.update_contact(self.contact.id, update_data)
        
        self.assertEqual(updated_contact.phone, '555-9999')
        self.assertEqual(updated_contact.title, 'Senior Manager')
        self.assertEqual(updated_contact.first_name, 'John')  # Unchanged
    
    def test_search_contacts(self):
        """Test contact search functionality."""
        # Create additional contacts
        Contact.objects.create(
            first_name='Alice',
            last_name='Johnson',
            email='alice.johnson@example.com',
            phone='555-1111',
            company='ABC Corp'
        )
        
        Contact.objects.create(
            first_name='Bob',
            last_name='Wilson',
            email='bob.wilson@testcompany.com',
            phone='555-2222',
            company='Test Company'
        )
        
        # Search by name
        results = self.contact_service.search_contacts('Alice')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].first_name, 'Alice')
        
        # Search by company
        results = self.contact_service.search_contacts('Test Company')
        self.assertEqual(len(results), 2)  # John and Bob
        
        # Search by email
        results = self.contact_service.search_contacts('alice.johnson')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].email, 'alice.johnson@example.com')
    
    def test_get_contacts_by_company(self):
        """Test retrieving contacts by company."""
        # Create additional contact with same company
        Contact.objects.create(
            first_name='Jane',
            last_name='Doe',
            email='jane.doe@example.com',
            phone='555-5555',
            company='Test Company'
        )
        
        contacts = self.contact_service.get_contacts_by_company('Test Company')
        
        self.assertEqual(len(contacts), 2)
        for contact in contacts:
            self.assertEqual(contact.company, 'Test Company')
    
    def test_validate_email_uniqueness(self):
        """Test email uniqueness validation."""
        duplicate_data = {
            'first_name': 'Duplicate',
            'last_name': 'User',
            'email': 'john.doe@example.com',  # Same as existing contact
            'phone': '555-0000'
        }
        
        with self.assertRaises(ValidationError):
            self.contact_service.create_contact(duplicate_data)
    
    def test_format_contact_name(self):
        """Test contact name formatting."""
        formatted_name = self.contact_service.format_contact_name(self.contact.id)
        
        self.assertEqual(formatted_name, 'John Doe')
        
        # Test with title
        formatted_name_with_title = self.contact_service.format_contact_name(
            self.contact.id, 
            include_title=True
        )
        
        self.assertEqual(formatted_name_with_title, 'John Doe, Manager')
    
    def test_get_contact_history(self):
        """Test retrieving contact interaction history."""
        # Mock history retrieval
        with patch.object(self.contact_service, 'get_trip_history') as mock_trips, \
             patch.object(self.contact_service, 'get_quote_history') as mock_quotes:
            
            mock_trips.return_value = []
            mock_quotes.return_value = []
            
            history = self.contact_service.get_contact_history(self.contact.id)
            
            self.assertIn('trips', history)
            self.assertIn('quotes', history)
            mock_trips.assert_called_once_with(self.contact.id)
            mock_quotes.assert_called_once_with(self.contact.id)
    
    def test_merge_contacts(self):
        """Test contact merging functionality."""
        # Create duplicate contact
        duplicate_contact = Contact.objects.create(
            first_name='John',
            last_name='Doe',
            email='john.doe.alt@example.com',
            phone='555-9876',
            company='Test Company Alt'
        )
        
        merged_contact = self.contact_service.merge_contacts(
            primary_contact_id=self.contact.id,
            duplicate_contact_id=duplicate_contact.id,
            merge_data={
                'phone': duplicate_contact.phone,  # Keep duplicate's phone
                'company': self.contact.company    # Keep primary's company
            }
        )
        
        self.assertEqual(merged_contact.phone, '555-9876')
        self.assertEqual(merged_contact.company, 'Test Company')
        self.assertFalse(Contact.objects.filter(id=duplicate_contact.id).exists())


class FBOServiceTest(TestCase):
    """Test cases for FBO service functionality."""
    
    def setUp(self):
        """Set up test data."""
        self.user = User.objects.create_user(username='testuser', password='testpass')
        
        self.fbo = FBO.objects.create(
            name='Test FBO',
            airport_code='KJFK',
            phone='555-FBO1',
            email='info@testfbo.com',
            services_offered='Fuel, Hangar, Catering',
            fuel_types='Jet A, Avgas',
            operating_hours='24/7'
        )
        
        self.contact_service = ContactService()
    
    def test_create_fbo(self):
        """Test FBO creation."""
        fbo_data = {
            'name': 'New FBO',
            'airport_code': 'KLAX',
            'phone': '555-FBO2',
            'email': 'info@newfbo.com',
            'services_offered': 'Fuel, Maintenance',
            'fuel_types': 'Jet A',
            'operating_hours': '6AM-10PM'
        }
        
        fbo = self.contact_service.create_fbo(fbo_data)
        
        self.assertIsNotNone(fbo)
        self.assertEqual(fbo.name, 'New FBO')
        self.assertEqual(fbo.airport_code, 'KLAX')
    
    def test_search_fbos_by_airport(self):
        """Test searching FBOs by airport code."""
        # Create additional FBO
        FBO.objects.create(
            name='Another FBO',
            airport_code='KJFK',
            phone='555-FBO3',
            email='info@anotherfbo.com'
        )
        
        fbos = self.contact_service.search_fbos_by_airport('KJFK')
        
        self.assertEqual(len(fbos), 2)
        for fbo in fbos:
            self.assertEqual(fbo.airport_code, 'KJFK')
    
    def test_get_fbo_services(self):
        """Test retrieving FBO services."""
        services = self.contact_service.get_fbo_services(self.fbo.id)
        
        self.assertIn('Fuel', services)
        self.assertIn('Hangar', services)
        self.assertIn('Catering', services)
    
    def test_check_fbo_fuel_availability(self):
        """Test checking FBO fuel availability."""
        has_jet_a = self.contact_service.check_fbo_fuel_availability(self.fbo.id, 'Jet A')
        has_diesel = self.contact_service.check_fbo_fuel_availability(self.fbo.id, 'Diesel')
        
        self.assertTrue(has_jet_a)
        self.assertFalse(has_diesel)


class GroundServiceTest(TestCase):
    """Test cases for Ground service functionality."""
    
    def setUp(self):
        """Set up test data."""
        self.user = User.objects.create_user(username='testuser', password='testpass')
        
        self.ground_service = Ground.objects.create(
            name='Test Ground Services',
            airport_code='KJFK',
            phone='555-GRND',
            email='info@testground.com',
            services_offered='Transportation, Catering, Customs',
            vehicle_types='Sedan, SUV, Van',
            coverage_area='NYC Metro Area'
        )
        
        self.contact_service = ContactService()
    
    def test_create_ground_service(self):
        """Test ground service creation."""
        ground_data = {
            'name': 'New Ground Services',
            'airport_code': 'KLAX',
            'phone': '555-GRND2',
            'email': 'info@newground.com',
            'services_offered': 'Transportation, Concierge',
            'vehicle_types': 'Luxury Sedan, Limousine',
            'coverage_area': 'LA Metro Area'
        }
        
        ground = self.contact_service.create_ground_service(ground_data)
        
        self.assertIsNotNone(ground)
        self.assertEqual(ground.name, 'New Ground Services')
        self.assertEqual(ground.airport_code, 'KLAX')
    
    def test_search_ground_services_by_airport(self):
        """Test searching ground services by airport."""
        # Create additional ground service
        Ground.objects.create(
            name='Another Ground Service',
            airport_code='KJFK',
            phone='555-GRND3',
            email='info@anotherground.com'
        )
        
        services = self.contact_service.search_ground_services_by_airport('KJFK')
        
        self.assertEqual(len(services), 2)
        for service in services:
            self.assertEqual(service.airport_code, 'KJFK')
    
    def test_check_vehicle_availability(self):
        """Test checking vehicle type availability."""
        has_sedan = self.contact_service.check_vehicle_availability(
            self.ground_service.id, 
            'Sedan'
        )
        has_helicopter = self.contact_service.check_vehicle_availability(
            self.ground_service.id, 
            'Helicopter'
        )
        
        self.assertTrue(has_sedan)
        self.assertFalse(has_helicopter)
    
    def test_get_coverage_area(self):
        """Test retrieving ground service coverage area."""
        coverage = self.contact_service.get_ground_service_coverage(self.ground_service.id)
        
        self.assertEqual(coverage, 'NYC Metro Area')

```
