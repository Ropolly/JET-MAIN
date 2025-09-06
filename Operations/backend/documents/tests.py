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
