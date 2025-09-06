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
