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
