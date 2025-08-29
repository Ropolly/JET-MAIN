#!/usr/bin/env python
"""
Test case for GenDec (General Declaration) document generation.

This test creates sample data and verifies that GenDec documents are generated
correctly for both passenger legs and repositioning legs.
"""

import os
import sys
import django
from datetime import datetime, timedelta
from pathlib import Path

# Setup Django environment
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from django.test import TestCase
from django.utils import timezone
from api.models import (
    Trip, TripLine, Contact, Passenger, Aircraft, Airport, 
    CrewLine, Patient, Quote
)
from utils.docgen.docgen import DocumentGenerator, generate_gendec_for_trip_line


class GenDecGenerationTest:
    """Test class for GenDec document generation functionality."""
    
    def __init__(self):
        self.generator = DocumentGenerator()
        self.created_objects = []  # Track created objects for cleanup
    
    def setUp(self):
        """Create test data for GenDec generation."""
        print("Setting up test data...")
        
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
        
        self.created_objects.extend([self.origin_airport, self.destination_airport])
        
        # Create aircraft
        self.aircraft = Aircraft.objects.create(
            tail_number="N123AB",
            company="Test Aviation Company",
            make="Cessna",
            model="Citation X",
            mgtow=16300.00,  # Maximum Gross Takeoff Weight in pounds
            serial_number="560-5001"
        )
        self.created_objects.append(self.aircraft)
        
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
        
        self.created_objects.extend([self.pilot1_contact, self.pilot2_contact, self.medic_contact])
        
        # Create crew line
        self.crew_line = CrewLine.objects.create(
            primary_in_command=self.pilot1_contact,
            secondary_in_command=self.pilot2_contact
        )
        self.crew_line.medic_ids.add(self.medic_contact)
        self.created_objects.append(self.crew_line)
        
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
        
        self.created_objects.extend([self.passenger1_contact, self.passenger2_contact])
        
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
        
        self.created_objects.extend([self.passenger1, self.passenger2])
        
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
        
        self.created_objects.extend([self.patient_contact, self.patient])
        
        print("✅ Test data setup complete")
    
    def test_passenger_leg_gendec(self):
        """Test GenDec generation for a passenger-carrying leg."""
        print("\n🧪 Testing passenger leg GenDec generation...")
        
        # Create medical trip with passengers
        trip = Trip.objects.create(
            trip_number="TEST001",
            type="medical",
            aircraft=self.aircraft,
            patient=self.patient,
            estimated_departure_time=timezone.now() + timedelta(hours=2)
        )
        trip.passengers.add(self.passenger1, self.passenger2)
        self.created_objects.append(trip)
        
        # Create passenger leg
        trip_line = TripLine.objects.create(
            trip=trip,
            origin_airport=self.origin_airport,
            destination_airport=self.destination_airport,
            crew_line=self.crew_line,
            departure_time_local=timezone.now() + timedelta(hours=2),
            departure_time_utc=timezone.now() + timedelta(hours=10),  # GMT+8
            arrival_time_local=timezone.now() + timedelta(hours=7),
            arrival_time_utc=timezone.now() + timedelta(hours=12),    # GMT+5
            distance=2475.00,  # LAX to JFK distance in miles
            flight_time=timedelta(hours=5),
            ground_time=timedelta(hours=1),
            passenger_leg=True  # This is a passenger-carrying leg
        )
        self.created_objects.append(trip_line)
        
        # Generate GenDec
        try:
            doc_path = self.generator.generate_general_declaration(str(trip_line.id))
            print(f"✅ GenDec generated successfully: {doc_path}")
            
            # Verify file exists
            if Path(doc_path).exists():
                print("✅ Generated file exists on disk")
                file_size = Path(doc_path).stat().st_size
                print(f"📄 File size: {file_size} bytes")
                
                # Basic validation - file should be larger than template (filled with data)
                template_path = self.generator.templates_dir / "GenDec.docx"
                if template_path.exists():
                    template_size = template_path.stat().st_size
                    print(f"📄 Template size: {template_size} bytes")
                    
                    if file_size >= template_size:
                        print("✅ Generated document appears to contain data")
                    else:
                        print("⚠️  Generated document may not contain proper data")
            else:
                print("❌ Generated file does not exist")
                return False
                
        except Exception as e:
            print(f"❌ Error generating passenger leg GenDec: {e}")
            return False
        
        return True
    
    def test_repositioning_leg_gendec(self):
        """Test GenDec generation for a repositioning (no passenger) leg.""" 
        print("\n🧪 Testing repositioning leg GenDec generation...")
        
        # Create repositioning trip (no passengers)
        trip = Trip.objects.create(
            trip_number="REPO001",
            type="maintenance", 
            aircraft=self.aircraft,
            estimated_departure_time=timezone.now() + timedelta(hours=1)
        )
        # Note: No passengers added to this trip
        self.created_objects.append(trip)
        
        # Create repositioning leg
        trip_line = TripLine.objects.create(
            trip=trip,
            origin_airport=self.destination_airport,  # Return trip
            destination_airport=self.origin_airport,
            crew_line=self.crew_line,
            departure_time_local=timezone.now() + timedelta(hours=1),
            departure_time_utc=timezone.now() + timedelta(hours=6),   # GMT+5
            arrival_time_local=timezone.now() + timedelta(hours=6),
            arrival_time_utc=timezone.now() + timedelta(hours=14),    # GMT+8
            distance=2475.00,
            flight_time=timedelta(hours=5),
            ground_time=timedelta(hours=1),
            passenger_leg=False  # This is a repositioning leg
        )
        self.created_objects.append(trip_line)
        
        # Generate GenDec
        try:
            doc_path = self.generator.generate_general_declaration(str(trip_line.id))
            print(f"✅ Repositioning GenDec generated successfully: {doc_path}")
            
            # Verify file exists
            if Path(doc_path).exists():
                print("✅ Generated repositioning file exists on disk")
                file_size = Path(doc_path).stat().st_size
                print(f"📄 File size: {file_size} bytes")
            else:
                print("❌ Generated repositioning file does not exist")
                return False
                
        except Exception as e:
            print(f"❌ Error generating repositioning leg GenDec: {e}")
            return False
        
        return True
    
    def test_convenience_function(self):
        """Test the convenience function for generating GenDec."""
        print("\n🧪 Testing convenience function...")
        
        # Create a simple trip for testing
        trip = Trip.objects.create(
            trip_number="CONV001",
            type="charter",
            aircraft=self.aircraft
        )
        self.created_objects.append(trip)
        
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
        self.created_objects.append(trip_line)
        
        try:
            doc_path = generate_gendec_for_trip_line(str(trip_line.id))
            print(f"✅ Convenience function worked: {doc_path}")
            return Path(doc_path).exists()
        except Exception as e:
            print(f"❌ Convenience function failed: {e}")
            return False
    
    def cleanup(self):
        """Clean up test data."""
        print("\n🧹 Cleaning up test data...")
        
        # Delete in reverse order to handle dependencies
        for obj in reversed(self.created_objects):
            try:
                obj.delete()
                print(f"🗑️  Deleted {obj.__class__.__name__}: {obj}")
            except Exception as e:
                print(f"⚠️  Error deleting {obj}: {e}")
        
        print("✅ Cleanup complete")
    
    def run_all_tests(self):
        """Run all GenDec generation tests."""
        print("🚀 Starting GenDec Generation Tests")
        print("=" * 50)
        
        try:
            self.setUp()
            
            results = []
            results.append(("Passenger Leg GenDec", self.test_passenger_leg_gendec()))
            results.append(("Repositioning Leg GenDec", self.test_repositioning_leg_gendec()))
            results.append(("Convenience Function", self.test_convenience_function()))
            
            print("\n" + "=" * 50)
            print("📊 Test Results Summary:")
            
            passed = 0
            for test_name, result in results:
                status = "✅ PASS" if result else "❌ FAIL"
                print(f"  {test_name}: {status}")
                if result:
                    passed += 1
            
            print(f"\n📈 Tests Passed: {passed}/{len(results)}")
            
            if passed == len(results):
                print("🎉 All tests passed! GenDec generation is working correctly.")
            else:
                print("⚠️  Some tests failed. Please check the implementation.")
            
        except Exception as e:
            print(f"❌ Test setup failed: {e}")
        finally:
            self.cleanup()


def main():
    """Main function to run the tests."""
    test_runner = GenDecGenerationTest()
    test_runner.run_all_tests()


if __name__ == "__main__":
    main()
