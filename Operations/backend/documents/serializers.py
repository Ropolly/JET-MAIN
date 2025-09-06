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
