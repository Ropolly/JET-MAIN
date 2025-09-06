from django.test import TestCase
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import datetime, timedelta, date
from decimal import Decimal
from unittest.mock import patch, Mock

from operations.models import Quote, Patient, Passenger, CrewLine, Trip, TripLine, TripEvent
from operations.services.trip_service import TripService, CrewService
from operations.services.quote_service import QuoteService, PatientService
from contacts.models import Contact
from airports.models import Airport
from aircraft.models import Aircraft


class TripServiceTest(TestCase):
    """Test cases for TripService business logic."""
    
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
        
        # Create test aircraft
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
        
        # Create test trip
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
        
        self.trip_service = TripService()
    
    def test_create_trip(self):
        """Test trip creation through service."""
        trip_data = {
            'trip_number': 'TRIP-002',
            'customer': self.contact,
            'aircraft': self.aircraft,
            'pickup_airport': self.pickup_airport,
            'dropoff_airport': self.dropoff_airport,
            'pickup_date': timezone.now().date() + timedelta(days=10),
            'pickup_time': timezone.now().time(),
            'status': 'PENDING'
        }
        
        trip = self.trip_service.create_trip(trip_data)
        
        self.assertIsNotNone(trip)
        self.assertEqual(trip.trip_number, 'TRIP-002')
        self.assertEqual(trip.customer, self.contact)
        self.assertEqual(trip.status, 'PENDING')
    
    def test_update_trip_status(self):
        """Test trip status update."""
        updated_trip = self.trip_service.update_trip_status(self.trip.id, 'CONFIRMED')
        
        self.assertEqual(updated_trip.status, 'CONFIRMED')
        
        # Refresh from database
        self.trip.refresh_from_db()
        self.assertEqual(self.trip.status, 'CONFIRMED')
    
    def test_calculate_trip_duration(self):
        """Test trip duration calculation."""
        # Set dropoff time
        self.trip.dropoff_date = self.trip.pickup_date
        self.trip.dropoff_time = (datetime.combine(date.today(), self.trip.pickup_time) + timedelta(hours=5)).time()
        self.trip.save()
        
        duration = self.trip_service.calculate_trip_duration(self.trip.id)
        
        self.assertIsNotNone(duration)
        self.assertEqual(duration.total_seconds(), 5 * 3600)  # 5 hours
    
    def test_get_trips_by_date_range(self):
        """Test retrieving trips by date range."""
        start_date = timezone.now().date()
        end_date = start_date + timedelta(days=30)
        
        trips = self.trip_service.get_trips_by_date_range(start_date, end_date)
        
        self.assertIn(self.trip, trips)
    
    def test_get_trips_by_aircraft(self):
        """Test retrieving trips by aircraft."""
        trips = self.trip_service.get_trips_by_aircraft(self.aircraft.id)
        
        self.assertIn(self.trip, trips)
    
    def test_add_passenger_to_trip(self):
        """Test adding passenger to trip."""
        passenger_data = {
            'first_name': 'Jane',
            'last_name': 'Smith',
            'email': 'jane.smith@example.com',
            'phone': '555-5678'
        }
        
        passenger = self.trip_service.add_passenger_to_trip(self.trip.id, passenger_data)
        
        self.assertIsNotNone(passenger)
        self.assertEqual(passenger.first_name, 'Jane')
        self.assertEqual(passenger.trip, self.trip)
    
    def test_cancel_trip(self):
        """Test trip cancellation."""
        cancelled_trip = self.trip_service.cancel_trip(self.trip.id, 'Customer request')
        
        self.assertEqual(cancelled_trip.status, 'CANCELLED')
        self.assertIsNotNone(cancelled_trip.cancellation_reason)


class CrewServiceTest(TestCase):
    """Test cases for CrewService business logic."""
    
    def setUp(self):
        """Set up test data."""
        self.user = User.objects.create_user(username='testuser', password='testpass')
        
        # Create test contact for customer
        self.contact = Contact.objects.create(
            first_name='John',
            last_name='Doe',
            email='john.doe@example.com',
            phone='555-1234'
        )
        
        # Create test contact for crew member
        self.crew_member = Contact.objects.create(
            first_name='Captain',
            last_name='Smith',
            email='captain.smith@example.com',
            phone='555-9999'
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
        
        # Create test aircraft
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
        
        # Create test trip
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
        
        self.crew_service = CrewService()
    
    def test_assign_crew_to_trip(self):
        """Test crew assignment to trip."""
        crew_line = self.crew_service.assign_crew_to_trip(
            trip_id=self.trip.id,
            crew_member=self.crew_member,
            role='CAPTAIN',
            duty_start=timezone.now(),
            duty_end=timezone.now() + timedelta(hours=8)
        )
        
        self.assertIsNotNone(crew_line)
        self.assertEqual(crew_line.trip, self.trip)
        self.assertEqual(crew_line.crew_member, self.crew_member)
        self.assertEqual(crew_line.role, 'CAPTAIN')
    
    def test_get_crew_for_trip(self):
        """Test retrieving crew for a trip."""
        # Create crew line
        CrewLine.objects.create(
            trip=self.trip,
            crew_member=self.crew_member,
            role='CAPTAIN',
            duty_start=timezone.now(),
            duty_end=timezone.now() + timedelta(hours=8)
        )
        
        crew_lines = self.crew_service.get_crew_for_trip(self.trip.id)
        
        self.assertEqual(len(crew_lines), 1)
        self.assertEqual(crew_lines[0].crew_member, self.crew_member)
    
    def test_calculate_crew_duty_time(self):
        """Test crew duty time calculation."""
        duty_start = timezone.now()
        duty_end = duty_start + timedelta(hours=10)
        
        crew_line = CrewLine.objects.create(
            trip=self.trip,
            crew_member=self.crew_member,
            role='CAPTAIN',
            duty_start=duty_start,
            duty_end=duty_end
        )
        
        duty_time = self.crew_service.calculate_crew_duty_time(crew_line.id)
        
        self.assertEqual(duty_time.total_seconds(), 10 * 3600)  # 10 hours
    
    def test_check_crew_availability(self):
        """Test crew availability checking."""
        # Create existing crew assignment
        existing_start = timezone.now() + timedelta(days=1)
        existing_end = existing_start + timedelta(hours=8)
        
        CrewLine.objects.create(
            trip=self.trip,
            crew_member=self.crew_member,
            role='CAPTAIN',
            duty_start=existing_start,
            duty_end=existing_end
        )
        
        # Check availability for overlapping time
        overlap_start = existing_start + timedelta(hours=4)
        overlap_end = overlap_start + timedelta(hours=8)
        
        is_available = self.crew_service.check_crew_availability(
            self.crew_member.id,
            overlap_start,
            overlap_end
        )
        
        self.assertFalse(is_available)
        
        # Check availability for non-overlapping time
        non_overlap_start = existing_end + timedelta(hours=1)
        non_overlap_end = non_overlap_start + timedelta(hours=8)
        
        is_available = self.crew_service.check_crew_availability(
            self.crew_member.id,
            non_overlap_start,
            non_overlap_end
        )
        
        self.assertTrue(is_available)


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
        
        # Create test aircraft
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
        
        self.quote_service = QuoteService()
    
    def test_create_quote(self):
        """Test quote creation through service."""
        quote_data = {
            'quote_number': 'QUOTE-001',
            'customer': self.contact,
            'aircraft': self.aircraft,
            'pickup_airport': self.pickup_airport,
            'dropoff_airport': self.dropoff_airport,
            'pickup_date': timezone.now().date() + timedelta(days=7),
            'pickup_time': timezone.now().time(),
            'passenger_count': 4,
            'total_cost': Decimal('15000.00')
        }
        
        quote = self.quote_service.create_quote(quote_data)
        
        self.assertIsNotNone(quote)
        self.assertEqual(quote.quote_number, 'QUOTE-001')
        self.assertEqual(quote.customer, self.contact)
        self.assertEqual(quote.total_cost, Decimal('15000.00'))
    
    @patch('operations.services.quote_service.QuoteService.calculate_distance')
    def test_calculate_quote_cost(self, mock_calculate_distance):
        """Test quote cost calculation."""
        mock_calculate_distance.return_value = 2500  # miles
        
        cost = self.quote_service.calculate_quote_cost(
            pickup_airport=self.pickup_airport,
            dropoff_airport=self.dropoff_airport,
            aircraft=self.aircraft,
            passenger_count=4
        )
        
        self.assertIsInstance(cost, Decimal)
        self.assertGreater(cost, Decimal('0'))
    
    def test_update_quote_status(self):
        """Test quote status update."""
        quote = Quote.objects.create(
            quote_number='QUOTE-002',
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
        
        updated_quote = self.quote_service.update_quote_status(quote.id, 'ACCEPTED')
        
        self.assertEqual(updated_quote.status, 'ACCEPTED')
    
    def test_convert_quote_to_trip(self):
        """Test converting quote to trip."""
        quote = Quote.objects.create(
            quote_number='QUOTE-003',
            customer=self.contact,
            aircraft=self.aircraft,
            pickup_airport=self.pickup_airport,
            dropoff_airport=self.dropoff_airport,
            pickup_date=timezone.now().date() + timedelta(days=7),
            pickup_time=timezone.now().time(),
            passenger_count=4,
            total_cost=Decimal('15000.00'),
            status='ACCEPTED'
        )
        
        trip = self.quote_service.convert_quote_to_trip(quote.id)
        
        self.assertIsNotNone(trip)
        self.assertEqual(trip.customer, quote.customer)
        self.assertEqual(trip.aircraft, quote.aircraft)
        self.assertEqual(trip.pickup_airport, quote.pickup_airport)
        self.assertEqual(trip.dropoff_airport, quote.dropoff_airport)


class PatientServiceTest(TestCase):
    """Test cases for PatientService business logic."""
    
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
        
        # Create test aircraft
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
        
        # Create test trip
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
        
        self.patient_service = PatientService()
    
    def test_create_patient_record(self):
        """Test patient record creation."""
        patient_data = {
            'trip': self.trip,
            'first_name': 'Jane',
            'last_name': 'Patient',
            'date_of_birth': date(1980, 1, 1),
            'medical_condition': 'Post-surgery recovery',
            'mobility_assistance': True,
            'oxygen_required': False,
            'stretcher_required': False
        }
        
        patient = self.patient_service.create_patient_record(patient_data)
        
        self.assertIsNotNone(patient)
        self.assertEqual(patient.first_name, 'Jane')
        self.assertEqual(patient.trip, self.trip)
        self.assertTrue(patient.mobility_assistance)
    
    def test_update_medical_requirements(self):
        """Test updating patient medical requirements."""
        patient = Patient.objects.create(
            trip=self.trip,
            first_name='Jane',
            last_name='Patient',
            date_of_birth=date(1980, 1, 1),
            medical_condition='Post-surgery recovery',
            mobility_assistance=False,
            oxygen_required=False,
            stretcher_required=False
        )
        
        updated_patient = self.patient_service.update_medical_requirements(
            patient.id,
            {
                'oxygen_required': True,
                'stretcher_required': True,
                'medical_notes': 'Requires continuous oxygen monitoring'
            }
        )
        
        self.assertTrue(updated_patient.oxygen_required)
        self.assertTrue(updated_patient.stretcher_required)
        self.assertIn('oxygen monitoring', updated_patient.medical_notes)
    
    def test_validate_aircraft_medical_capability(self):
        """Test aircraft medical capability validation."""
        patient = Patient.objects.create(
            trip=self.trip,
            first_name='Jane',
            last_name='Patient',
            date_of_birth=date(1980, 1, 1),
            medical_condition='Post-surgery recovery',
            mobility_assistance=False,
            oxygen_required=True,
            stretcher_required=True
        )
        
        # Mock aircraft capabilities check
        with patch.object(self.patient_service, 'check_aircraft_medical_equipment') as mock_check:
            mock_check.return_value = True
            
            is_capable = self.patient_service.validate_aircraft_medical_capability(
                patient.id,
                self.aircraft.id
            )
            
            self.assertTrue(is_capable)
            mock_check.assert_called_once()
    
    def test_get_patients_for_trip(self):
        """Test retrieving patients for a trip."""
        # Create multiple patients
        Patient.objects.create(
            trip=self.trip,
            first_name='Jane',
            last_name='Patient1',
            date_of_birth=date(1980, 1, 1),
            medical_condition='Condition 1'
        )
        
        Patient.objects.create(
            trip=self.trip,
            first_name='John',
            last_name='Patient2',
            date_of_birth=date(1975, 5, 15),
            medical_condition='Condition 2'
        )
        
        patients = self.patient_service.get_patients_for_trip(self.trip.id)
        
        self.assertEqual(len(patients), 2)
        self.assertEqual(patients[0].trip, self.trip)
        self.assertEqual(patients[1].trip, self.trip)
