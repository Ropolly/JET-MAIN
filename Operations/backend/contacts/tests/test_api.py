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
