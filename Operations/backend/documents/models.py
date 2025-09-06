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
