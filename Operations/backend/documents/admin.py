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
