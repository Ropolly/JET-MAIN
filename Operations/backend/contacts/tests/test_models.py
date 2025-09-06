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
