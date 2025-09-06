"""
Django test cases for document generation functionality.

Converted from custom test scripts to proper Django TestCase.
"""

from django.test import TestCase
from django.utils import timezone
from datetime import datetime, timedelta
from operations.models import Trip, TripLine, CrewLine, Passenger, Patient, Quote
from contacts.models import Contact
from aircraft.models import Aircraft
from airports.models import Airport
from documents.services.document_generation_service import DocumentGenerationService, generate_general_declaration


class DocumentGenerationTestCase(TestCase):
    """Test case for document generation functionality."""
    
    def setUp(self):
        """Set up test data for document generation tests."""
        # Create airports
        self.origin_airport = Airport.objects.create(
            name="Los Angeles International Airport",
            iata_code="LAX",
            icao_code="KLAX",
            city="Los Angeles",
            state="CA",
            country="USA",
            latitude=33.942536,
            longitude=-118.408074,
            timezone="America/Los_Angeles"
        )
        
        self.destination_airport = Airport.objects.create(
            name="John F. Kennedy International Airport", 
            iata_code="JFK",
            icao_code="KJFK",
            city="New York",
            state="NY", 
            country="USA",
            latitude=40.639751,
            longitude=-73.778925,
            timezone="America/New_York"
        )
        
        # Create aircraft
        self.aircraft = Aircraft.objects.create(
            tail_number="N123AB",
            company="Test Aviation Company",
            make="Cessna",
            model="Citation X",
            mgtow=16300.00,
            serial_number="560-5001"
        )
        
        # Create contacts for crew
        self.pilot1_contact = Contact.objects.create(
            first_name="John",
            last_name="Smith",
            email="pilot1@test.com"
        )
        
        self.pilot2_contact = Contact.objects.create(
            first_name="Jane", 
            last_name="Doe",
            email="pilot2@test.com"
        )
        
        self.medic_contact = Contact.objects.create(
            first_name="Dr. Sarah",
            last_name="Johnson",
            email="medic@test.com"
        )
        
        # Create crew line
        self.crew_line = CrewLine.objects.create(
            primary_in_command=self.pilot1_contact,
            secondary_in_command=self.pilot2_contact
        )
        self.crew_line.medic_ids.add(self.medic_contact)
        
        # Create passenger contacts and passengers
        self.passenger1_contact = Contact.objects.create(
            first_name="Michael",
            last_name="Brown",
            email="passenger1@test.com"
        )
        
        self.passenger2_contact = Contact.objects.create(
            first_name="Lisa",
            last_name="Williams", 
            email="passenger2@test.com"
        )
        
        self.passenger1 = Passenger.objects.create(
            info=self.passenger1_contact,
            nationality="USA",
            passport_number="123456789",
            date_of_birth=datetime(1980, 5, 15).date()
        )
        
        self.passenger2 = Passenger.objects.create(
            info=self.passenger2_contact,
            nationality="USA", 
            passport_number="987654321",
            date_of_birth=datetime(1975, 8, 22).date()
        )
        
        # Create patient for medical trip
        self.patient_contact = Contact.objects.create(
            first_name="Patient",
            last_name="Smith",
            email="patient@test.com"
        )
        
        self.patient = Patient.objects.create(
            info=self.patient_contact,
            date_of_birth=datetime(1960, 3, 10).date()
        )
        
        # Initialize document generation service
        self.generator = DocumentGenerationService()
    
    def test_passenger_trip_gendec_generation(self):
        """Test GenDec generation for a passenger-carrying trip."""
        # Create medical trip with passengers
        trip = Trip.objects.create(
            trip_number="TEST001",
            type="medical",
            aircraft=self.aircraft,
            patient=self.patient,
            estimated_departure_time=timezone.now() + timedelta(hours=2)
        )
        trip.passengers.add(self.passenger1, self.passenger2)
        
        # Create passenger leg
        trip_line = TripLine.objects.create(
            trip=trip,
            origin_airport=self.origin_airport,
            destination_airport=self.destination_airport,
            crew_line=self.crew_line,
            departure_time_local=timezone.now() + timedelta(hours=2),
            departure_time_utc=timezone.now() + timedelta(hours=10),
            arrival_time_local=timezone.now() + timedelta(hours=7),
            arrival_time_utc=timezone.now() + timedelta(hours=12),
            distance=2475.00,
            flight_time=timedelta(hours=5),
            ground_time=timedelta(hours=1),
            passenger_leg=True
        )
        
        # Generate GenDec
        document = self.generator.generate_general_declaration(str(trip.id))
        
        # Assertions
        self.assertIsNotNone(document, "Document should be generated")
        self.assertIsNotNone(document.content, "Document should have content")
        self.assertGreater(document.file_size, 1000, "Document should have reasonable size")
        self.assertEqual(document.document_category, 'itinerary')
        self.assertIn('GenDec', document.filename)
    
    def test_repositioning_trip_gendec_generation(self):
        """Test GenDec generation for a repositioning (no passenger) trip.""" 
        # Create repositioning trip (no passengers)
        trip = Trip.objects.create(
            trip_number="REPO001",
            type="maintenance", 
            aircraft=self.aircraft,
            estimated_departure_time=timezone.now() + timedelta(hours=1)
        )
        
        # Create repositioning leg
        trip_line = TripLine.objects.create(
            trip=trip,
            origin_airport=self.destination_airport,
            destination_airport=self.origin_airport,
            crew_line=self.crew_line,
            departure_time_local=timezone.now() + timedelta(hours=1),
            departure_time_utc=timezone.now() + timedelta(hours=6),
            arrival_time_local=timezone.now() + timedelta(hours=6),
            arrival_time_utc=timezone.now() + timedelta(hours=14),
            distance=2475.00,
            flight_time=timedelta(hours=5),
            ground_time=timedelta(hours=1),
            passenger_leg=False
        )
        
        # Generate GenDec
        document = self.generator.generate_general_declaration(str(trip.id))
        
        # Assertions
        self.assertIsNotNone(document, "Repositioning document should be generated")
        self.assertIsNotNone(document.content, "Document should have content")
        self.assertGreater(document.file_size, 1000, "Document should have reasonable size")
    
    def test_convenience_function(self):
        """Test the convenience function for generating GenDec."""
        # Create a simple trip for testing
        trip = Trip.objects.create(
            trip_number="CONV001",
            type="charter",
            aircraft=self.aircraft
        )
        
        trip_line = TripLine.objects.create(
            trip=trip,
            origin_airport=self.origin_airport,
            destination_airport=self.destination_airport,
            crew_line=self.crew_line,
            departure_time_local=timezone.now() + timedelta(hours=3),
            departure_time_utc=timezone.now() + timedelta(hours=11),
            arrival_time_local=timezone.now() + timedelta(hours=8),
            arrival_time_utc=timezone.now() + timedelta(hours=13),
            distance=2475.00,
            flight_time=timedelta(hours=5),
            ground_time=timedelta(hours=1),
            passenger_leg=False
        )
        
        # Test convenience function
        document = generate_general_declaration(str(trip.id))
        
        # Assertions
        self.assertIsNotNone(document, "Convenience function should work")
        self.assertIsNotNone(document.content, "Document should have content")
    
    def test_quote_document_generation(self):
        """Test quote document generation."""
        # Create a quote
        quote = Quote.objects.create(
            contact=self.passenger1_contact,
            pickup_airport=self.origin_airport,
            dropoff_airport=self.destination_airport,
            aircraft_type="light_jet",
            medical_team="basic",
            quoted_amount=15000.00,
            estimated_flight_time=timedelta(hours=5),
            number_of_stops=0,
            includes_grounds=True,
            patient=self.patient
        )
        
        # Generate quote document
        document = self.generator.generate_quote_document(str(quote.id))
        
        # Assertions
        self.assertIsNotNone(document, "Quote document should be generated")
        self.assertIsNotNone(document.content, "Document should have content")
        self.assertEqual(document.document_category, 'quote')
        self.assertIn('Quote', document.filename)
    
    def test_customer_itinerary_generation(self):
        """Test customer-facing itinerary generation."""
        # Create trip with multiple legs
        trip = Trip.objects.create(
            trip_number="ITIN001",
            type="charter",
            aircraft=self.aircraft,
            estimated_departure_time=timezone.now() + timedelta(hours=2)
        )
        trip.passengers.add(self.passenger1)
        
        # Create multiple trip lines
        TripLine.objects.create(
            trip=trip,
            origin_airport=self.origin_airport,
            destination_airport=self.destination_airport,
            crew_line=self.crew_line,
            departure_time_local=timezone.now() + timedelta(hours=2),
            departure_time_utc=timezone.now() + timedelta(hours=10),
            arrival_time_local=timezone.now() + timedelta(hours=7),
            arrival_time_utc=timezone.now() + timedelta(hours=12),
            distance=2475.00,
            flight_time=timedelta(hours=5),
            passenger_leg=True
        )
        
        # Generate customer itinerary
        document = self.generator.generate_itinerary(str(trip.id), customer_facing=True)
        
        # Assertions
        self.assertIsNotNone(document, "Customer itinerary should be generated")
        self.assertIsNotNone(document.content, "Document should have content")
        self.assertEqual(document.document_category, 'itinerary')
        self.assertIn('Customer_Itinerary', document.filename)
    
    def test_internal_itinerary_generation(self):
        """Test internal itinerary generation."""
        # Create trip
        trip = Trip.objects.create(
            trip_number="ITIN002",
            type="medical",
            aircraft=self.aircraft,
            patient=self.patient,
            estimated_departure_time=timezone.now() + timedelta(hours=1)
        )
        
        # Create trip line
        TripLine.objects.create(
            trip=trip,
            origin_airport=self.origin_airport,
            destination_airport=self.destination_airport,
            crew_line=self.crew_line,
            departure_time_local=timezone.now() + timedelta(hours=1),
            departure_time_utc=timezone.now() + timedelta(hours=9),
            arrival_time_local=timezone.now() + timedelta(hours=6),
            arrival_time_utc=timezone.now() + timedelta(hours=11),
            distance=2475.00,
            flight_time=timedelta(hours=5),
            passenger_leg=True
        )
        
        # Generate internal itinerary
        document = self.generator.generate_itinerary(str(trip.id), customer_facing=False)
        
        # Assertions
        self.assertIsNotNone(document, "Internal itinerary should be generated")
        self.assertIsNotNone(document.content, "Document should have content")
        self.assertEqual(document.document_category, 'itinerary')
        self.assertIn('Internal_Itinerary', document.filename)
    
    def test_document_generation_error_handling(self):
        """Test error handling in document generation."""
        # Test with non-existent trip ID
        document = self.generator.generate_general_declaration("non-existent-id")
        self.assertIsNone(document, "Should return None for non-existent trip")
        
        # Test with invalid quote ID
        document = self.generator.generate_quote_document("invalid-quote-id")
        self.assertIsNone(document, "Should return None for invalid quote")
    
    def test_template_management(self):
        """Test template management functionality."""
        # Test listing available templates
        templates = self.generator.list_available_templates()
        self.assertIsInstance(templates, list, "Should return a list of templates")
        
        # Test cleanup functionality (should not raise errors)
        try:
            deleted_count = self.generator.cleanup_old_documents(days_old=365)
            self.assertIsInstance(deleted_count, int, "Should return count of deleted files")
        except Exception as e:
            self.fail(f"Cleanup should not raise exceptions: {e}")
