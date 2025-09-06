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
