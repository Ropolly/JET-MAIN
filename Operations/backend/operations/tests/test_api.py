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
