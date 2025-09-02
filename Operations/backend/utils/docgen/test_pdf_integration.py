#!/usr/bin/env python3

import os
import sys
from pathlib import Path
from datetime import datetime, timedelta

# Setup Django environment
sys.path.append(str(Path(__file__).parent.parent.parent))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')

import django
django.setup()

from django.utils import timezone
from docgen import DocumentGenerator

class MockObject:

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

class MockManager:

    def __init__(self, objects=None):
        self._objects = objects or []
    
    def all(self):
        return self._objects

def create_mock_trip_line():

    # Mock aircraft
    aircraft = MockObject(
        tail_number="N123JT",
        make="Cessna",
        model="Citation X",
        company="JetMedical Transport",
        serial_number="560-1234",
        mgtow="36100"
    )
    
    # Mock airports
    origin_airport = MockObject(
        name="Los Angeles International Airport",
        iata_code="LAX",
        icao_code="KLAX",
        city="Los Angeles",
        country="United States"
    )
    
    destination_airport = MockObject(
        name="John F. Kennedy International Airport",
        iata_code="JFK",
        icao_code="KJFK",
        city="New York",
        country="United States"
    )
    
    # Mock patient
    patient_info = MockObject(
        name="John Patient",
        date_of_birth=datetime(1970, 5, 15).date()
    )
    
    patient = MockObject(
        name="John Patient",
        info=patient_info
    )
    
    # Mock passengers
    passenger1_info = MockObject(
        name="Jane Companion",
        date_of_birth=datetime(1975, 8, 22).date(),
        nationality="US",
        passport_number="123456789"
    )
    
    passenger1 = MockObject(
        name="Jane Companion",
        info=passenger1_info
    )
    
    passenger2_info = MockObject(
        name="Bob Guardian",
        date_of_birth=datetime(1968, 3, 10).date(),
        nationality="US",
        passport_number="987654321"
    )
    
    passenger2 = MockObject(
        name="Bob Guardian",
        info=passenger2_info
    )
    
    # Mock crew
    primary_pilot = MockObject(name="Captain John Smith")
    secondary_pilot = MockObject(name="First Officer Jane Doe")
    medic = MockObject(name="Dr. Emergency Response")
    
    crew_line = MockObject(
        primary_in_command=primary_pilot,
        secondary_in_command=secondary_pilot,
        medic_ids=MockManager([medic])
    )
    
    # Mock trip
    trip = MockObject(
        trip_number="JT001",
        flight_number="JT001",
        aircraft=aircraft,
        patient=patient,
        passengers=MockManager([passenger1, passenger2]),
        crew_members=MockManager([
            MockObject(name="Captain John Smith", role="captain"),
            MockObject(name="First Officer Jane Doe", role="first_officer"),
            MockObject(name="Dr. Emergency Response", role="medic")
        ])
    )
    
    # Mock trip line (PAX leg)
    pax_trip_line = MockObject(
        id="test-pax-123",
        passenger_leg=True,
        departure_time=timezone.now(),
        origin_airport=origin_airport,
        destination_airport=destination_airport,
        trip=trip,
        crew_line=crew_line
    )
    
    return pax_trip_line

def create_mock_repositioning_trip_line():

    # Use same aircraft and airports as PAX leg
    pax_trip_line = create_mock_trip_line()
    
    # Create repositioning leg (swap airports)
    repo_trip_line = MockObject(
        id="test-repo-456",
        passenger_leg=False,
        departure_time=timezone.now() + timedelta(hours=2),
        origin_airport=pax_trip_line.destination_airport,  # JFK
        destination_airport=MockObject(
            name="Miami International Airport",
            iata_code="MIA",
            icao_code="KMIA",
            city="Miami",
            country="United States"
        ),
        trip=pax_trip_line.trip,
        crew_line=pax_trip_line.crew_line
    )
    
    return repo_trip_line

def test_pdf_generation():

    print(" TESTING PDF-BASED GENDEC GENERATION")
    print("=" * 60)
    
    try:
        # Initialize DocumentGenerator
        generator = DocumentGenerator()
        
        # Check if PDF template exists
        pdf_template = generator.templates_dir / "GenDec.pdf"
        if not pdf_template.exists():
            print(f" GenDec.pdf template not found: {pdf_template}")
            return False
        
        print(f" Found GenDec.pdf template: {pdf_template}")
        
        # Test PAX leg generation
        print("\n--- Testing PAX Leg ---")
        pax_trip_line = create_mock_trip_line()
        
        try:
            result = generator.generate_gendec_pdf(pax_trip_line.id)
            
            if result['success']:
                print(f" PAX leg PDF generated successfully")
                print(f" Fields filled: {result['fields_filled']}/{result['total_fields']}")
                print(f" Filename: {result['filename']}")
                print(f" PDF size: {len(result['pdf_data']):,} bytes")
                
                # Save test file
                test_output = generator.outputs_dir / f"Test_{result['filename']}"
                with open(test_output, 'wb') as f:
                    f.write(result['pdf_data'])
                print(f" Test PDF saved: {test_output}")
                
            else:
                print(" PAX leg PDF generation failed")
                return False
                
        except Exception as e:
            print(f" Error during PAX leg generation: {e}")
            return False
        
        # Test repositioning leg generation
        print("\n--- Testing Repositioning Leg ---")
        repo_trip_line = create_mock_repositioning_trip_line()
        
        try:
            result = generator.generate_gendec_pdf(repo_trip_line.id)
            
            if result['success']:
                print(f" Repositioning leg PDF generated successfully")
                print(f" Fields filled: {result['fields_filled']}/{result['total_fields']}")
                print(f" Filename: {result['filename']}")
                print(f" PDF size: {len(result['pdf_data']):,} bytes")
                
                # Save test file
                test_output = generator.outputs_dir / f"Test_{result['filename']}"
                with open(test_output, 'wb') as f:
                    f.write(result['pdf_data'])
                print(f" Test PDF saved: {test_output}")
                
            else:
                print(" Repositioning leg PDF generation failed")
                return False
                
        except Exception as e:
            print(f" Error during repositioning leg generation: {e}")
            return False
        
        return True
        
    except Exception as e:
        print(f" Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_fallback_to_docx():

    print("\n TESTING DOCX FALLBACK")
    print("=" * 60)
    
    try:
        # Initialize DocumentGenerator
        generator = DocumentGenerator()
        
        # Test PAX leg generation with DOCX
        print("--- Testing DOCX GenDec Generation ---")
        pax_trip_line = create_mock_trip_line()
        
        try:
            docx_path = generator.generate_gendec(pax_trip_line.id)
            print(f" DOCX GenDec generated: {docx_path}")
            
            # Check file exists and has reasonable size
            if Path(docx_path).exists():
                size = Path(docx_path).stat().st_size
                print(f" DOCX file size: {size:,} bytes")
                return True
            else:
                print(" DOCX file was not created")
                return False
                
        except Exception as e:
            print(f" Error during DOCX generation: {e}")
            return False
            
    except Exception as e:
        print(f" DOCX fallback test failed: {e}")
        return False

if __name__ == "__main__":

    print(" STARTING PDF INTEGRATION TESTS")
    print("=" * 60)
    
    # Run tests
    pdf_test_passed = test_pdf_generation()
    docx_test_passed = test_fallback_to_docx()
    
    # Summary
    print("\n" + "=" * 60)
    print(" TEST SUMMARY")
    print("=" * 60)
    print(f"PDF Generation Test: {' PASSED' if pdf_test_passed else ' FAILED'}")
    print(f"DOCX Fallback Test: {' PASSED' if docx_test_passed else ' FAILED'}")
    
    if pdf_test_passed and docx_test_passed:
        print("\n ALL TESTS PASSED!")
        print(" PDF-based GenDec generation is working correctly")
        print(" DOCX fallback is functional")
        print(" Integration with DocumentGenerator successful")
    else:
        print("\n SOME TESTS FAILED")
        if not pdf_test_passed:
            print(" PDF generation needs attention")
        if not docx_test_passed:
            print(" DOCX fallback needs attention")
        
        sys.exit(1)
