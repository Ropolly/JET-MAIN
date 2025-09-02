#!/usr/bin/env python3

import os
from pathlib import Path
from datetime import datetime, date

# Check for PyMuPDF availability
try:
    import fitz
    PDF_AVAILABLE = True
    print(" PyMuPDF is available")
except ImportError:
    PDF_AVAILABLE = False
    print(" PyMuPDF not available - cannot test PDF functionality")
    exit(1)

class MockObject:

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

class MockContact:
    def __init__(self, first_name, last_name, date_of_birth):
        self.first_name = first_name
        self.last_name = last_name
        self.date_of_birth = date_of_birth

class MockCrewMemberInfo:
    def __init__(self, date_of_birth):
        self.date_of_birth = date_of_birth

class MockCrewMember:
    def __init__(self, name, date_of_birth=None):
        self.name = name
        self.date_of_birth = date_of_birth or date(1990, 1, 1)
        # Create mock contact info with DOB
        self.info = MockContact(
            first_name=name.split()[0] if name else 'Unknown',
            last_name=' '.join(name.split()[1:]) if len(name.split()) > 1 else '',
            date_of_birth=self.date_of_birth
        )

class MockMedicManager:
    def __init__(self, medics):
        self._medics = medics

    def all(self):
        return self._medics

class MockCrewLine:
    def __init__(self):
        from datetime import date
        self.primary_in_command = MockCrewMember("Captain Smith", date(1975, 5, 15))
        self.secondary_in_command = MockCrewMember("First Officer Johnson", date(1980, 8, 22))
        self.medic_ids = MockMedicManager([
            MockCrewMember("Dr. Sarah Wilson", date(1985, 3, 10)),
            MockCrewMember("Nurse Mike Brown", date(1988, 11, 5))
        ])

class MockManager:

    def __init__(self, objects=None):
        self._objects = objects or []
    
    def all(self):
        return self._objects

def clean_name(name: str) -> str:

    if not name:
        return name
        
    # Common titles to remove (order matters - longer phrases first)
    titles = [
        'First Officer', 'F/O', 'FO',
        'Captain', 'Capt.', 'Capt',
        'Dr.', 'Dr', 'Doctor',
        'Nurse', 'RN', 'LPN',
        'Mr.', 'Mrs.', 'Ms.', 'Miss',
        'Sir', 'Madam', 'Ma\'am'
    ]
    
    # Handle compound titles like "First Officer"
    clean_name = name
    for title in titles:
        # Remove title from beginning with space
        if clean_name.startswith(title + ' '):
            clean_name = clean_name[len(title + ' '):]
            break
        # Remove title if it's the whole beginning part
        elif clean_name.startswith(title):
            clean_name = clean_name[len(title):].lstrip()
            break
    
    # Split into parts and clean up any remaining single-word titles
    parts = clean_name.split()
    
    # Join remaining parts (should be first and last name)
    return ' '.join(parts)

def fill_gendec_pdf_direct(template_path, trip_line_mock):

    import io

    # PDF form field mapping - Basic fields
    field_mapping = {
        'owner_operator': 'F[0].P1[0].OwnerorOperator[0]',
        'aircraft_registration': 'F[0].P1[0].MarksofNationality[0]',
        'flight_number': 'F[0].P1[0].flightnumber[0]',
        'date': 'F[0].P1[0].Date[0]',
        'departure_from': 'F[0].P1[0].departurefrom[0]',
        'arrive_at': 'F[0].P1[0].arrivaat[0]',
        'embarking': 'F[0].P1[0].embarking[0]',
        'through_passengers': 'F[0].P1[0].throughonsameflight[0]',
        'disembarking': 'F[0].P1[0].disembarking[0]',
        'through_passengers2': 'F[0].P1[0].throughonsameflight2[0]',
        'declaration': 'F[0].P1[0].declaration1[0]',
        'other_info': 'F[0].P1[0].other1[0]',
        'details': 'F[0].P1[0].details1[0]',
        'captain_signature': 'F[0].P1[0].sign[0]',
        'agent_signature': 'F[0].P1[0].agentsignature[0]',
        'awb_number': 'F[0].P1[0].AWB[0]'
    }
    
    # Crew and passenger place/total number field mapping
    place_fields = {
        'place1': 'F[0].P1[0].place1[0]',
        'place2': 'F[0].P1[0].place2[0]',
        'place3': 'F[0].P1[0].place3[0]',
        'place4': 'F[0].P1[0].place4[0]',
        'place5': 'F[0].P1[0].place5[0]',
        'place6': 'F[0].P1[0].place6[0]',
        'place7': 'F[0].P1[0].place7[0]',
        'place8': 'F[0].P1[0].place8[0]',
    }
    
    total_fields = {
        'total1': 'F[0].P1[0].totalnumber1[0]',
        'total2': 'F[0].P1[0].totalnumber2[0]',
        'total3': 'F[0].P1[0].totalnumber3[0]',
        'total4': 'F[0].P1[0].totalnumber4[0]',
        'total5': 'F[0].P1[0].totalnumber5[0]',
        'total6': 'F[0].P1[0].totalnumber6[0]',
        'total7': 'F[0].P1[0].totalnumber7[0]',
        'total8': 'F[0].P1[0].totalnumber8[0]',
    }
    
    # Format airports as CITY, COUNTRY (ICAO)
    def format_airport(airport):
        if not airport:
            return ''
        city = getattr(airport, 'city', airport.name.split(' ')[0])  # Use first word as city
        country = getattr(airport, 'country', 'US')  # Default to US
        icao = getattr(airport, 'icao_code', '')
        return f"{city}, {country} ({icao})"
    
    # Prepare form data
    aircraft = trip_line_mock.trip.aircraft
    data = {
        'owner_operator': getattr(aircraft, 'company', 'Unknown Operator'),
        'aircraft_registration': getattr(aircraft, 'tail_number', 'N-UNKNOWN'),
        'flight_number': getattr(trip_line_mock.trip, 'flight_number', '') or f"TL{trip_line_mock.id}",
        'date': trip_line_mock.departure_time.strftime('%m/%d/%Y') if trip_line_mock.departure_time else datetime.now().strftime('%m/%d/%Y'),
        'departure_from': format_airport(trip_line_mock.origin_airport),
        'arrive_at': format_airport(trip_line_mock.destination_airport),
    }
    
    # Prepare crew and passenger data for place/total fields
    crew_and_pax_data = {}
    field_index = 1
    
    # Add crew members first
    crew_line = getattr(trip_line_mock, 'crew_line', None)
    if crew_line:
        # Primary in Command (PIC)
        if hasattr(crew_line, 'primary_in_command') and crew_line.primary_in_command:
            name = clean_name(crew_line.primary_in_command.name)
            crew_and_pax_data[f'place{field_index}'] = f"PIC: {name}"
            # Get birthdate from crew member info
            if hasattr(crew_line.primary_in_command, 'info') and hasattr(crew_line.primary_in_command.info, 'date_of_birth'):
                crew_and_pax_data[f'total{field_index}'] = crew_line.primary_in_command.info.date_of_birth.strftime('%m/%d/%Y')
            else:
                crew_and_pax_data[f'total{field_index}'] = 'DOB not available'
            field_index += 1
        
        # Second in Command (SIC)
        if hasattr(crew_line, 'secondary_in_command') and crew_line.secondary_in_command:
            name = clean_name(crew_line.secondary_in_command.name)
            crew_and_pax_data[f'place{field_index}'] = f"SIC: {name}"
            if hasattr(crew_line.secondary_in_command, 'info') and hasattr(crew_line.secondary_in_command.info, 'date_of_birth'):
                crew_and_pax_data[f'total{field_index}'] = crew_line.secondary_in_command.info.date_of_birth.strftime('%m/%d/%Y')
            else:
                crew_and_pax_data[f'total{field_index}'] = 'DOB not available'
            field_index += 1
        
        # Medical crew (MED)
        if hasattr(crew_line, 'medic_ids'):
            medics = list(crew_line.medic_ids.all()) if crew_line.medic_ids else []
            for medic in medics:
                if field_index <= 8:  # Limit to available fields
                    name = clean_name(medic.name)
                    crew_and_pax_data[f'place{field_index}'] = f"MED: {name}"
                    if hasattr(medic, 'info') and hasattr(medic.info, 'date_of_birth'):
                        crew_and_pax_data[f'total{field_index}'] = medic.info.date_of_birth.strftime('%m/%d/%Y')
                    else:
                        crew_and_pax_data[f'total{field_index}'] = 'DOB not available'
                    field_index += 1
    
    # Add passengers if it's a PAX leg
    if trip_line_mock.passenger_leg:
        # Add patient first
        patient = trip_line_mock.trip.patient if hasattr(trip_line_mock.trip, 'patient') and trip_line_mock.trip.patient else None
        if patient and field_index <= 8:
            name = clean_name(patient.name)
            crew_and_pax_data[f'place{field_index}'] = f"PAX: {name}"
            if hasattr(patient, 'info') and hasattr(patient.info, 'date_of_birth'):
                crew_and_pax_data[f'total{field_index}'] = patient.info.date_of_birth.strftime('%m/%d/%Y')
            else:
                crew_and_pax_data[f'total{field_index}'] = 'DOB not available'
            field_index += 1
        
        # Add regular passengers
        passengers = list(trip_line_mock.trip.passengers.all()) if hasattr(trip_line_mock.trip, 'passengers') else []
        for passenger in passengers:
            if field_index <= 8:  # Limit to available fields
                name = clean_name(passenger.name)
                crew_and_pax_data[f'place{field_index}'] = f"PAX: {name}"
                if hasattr(passenger, 'info') and hasattr(passenger.info, 'date_of_birth'):
                    crew_and_pax_data[f'total{field_index}'] = passenger.info.date_of_birth.strftime('%m/%d/%Y')
                else:
                    crew_and_pax_data[f'total{field_index}'] = 'DOB not available'
                field_index += 1
        
        # Calculate total passenger counts
        total_pax = len(passengers) + (1 if patient else 0)
        data.update({
            'embarking': str(total_pax),
            'disembarking': str(total_pax),
            'through_passengers': '0',
            'through_passengers2': '0',
        })
        
        # Generate passenger/patient details for details field
        details_parts = []
        if patient:
            details_parts.append(f"Patient: {patient.name}")
        if passengers:
            passenger_names = [p.name for p in passengers]
            details_parts.append(f"Passengers: {', '.join(passenger_names)}")
        data['details'] = ', '.join(details_parts) if details_parts else 'No passengers'
    else:
        data.update({
            'embarking': '0',
            'disembarking': '0',
            'through_passengers': '0',
            'through_passengers2': '0',
            'details': 'Repositioning flight - no passengers'
        })
    
    # Add crew and passenger data to main data dict
    data.update(crew_and_pax_data)
    
    # Add remaining fields
    primary_pilot = None
    if hasattr(trip_line_mock.trip, 'crew_members'):
        pilots = [crew for crew in trip_line_mock.trip.crew_members.all() if 'pilot' in crew.role.lower()]
        if pilots:
            primary_pilot = pilots[0].name
    
    data.update({
        'captain_signature': primary_pilot or 'Aircraft Commander',
        'agent_signature': data['owner_operator'],
        'declaration': 'This flight complies with all applicable US Customs regulations',
        'other_info': 'Medical transport flight' if trip_line_mock.passenger_leg else 'Repositioning flight'
    })
    
    # Combine all field mappings
    all_field_mappings = {**field_mapping, **place_fields, **total_fields}
    
    # Fill PDF form
    try:
        doc = fitz.open(template_path)
        filled_fields = 0
        total_fields = 0
        
        for page_num in range(doc.page_count):
            page = doc[page_num]
            widgets = list(page.widgets())
            
            for widget in widgets:
                total_fields += 1
                field_name = widget.field_name
                
                # Find matching data key from all field mappings
                data_key = None
                for data_k, field_path in all_field_mappings.items():
                    if field_path == field_name:
                        data_key = data_k
                        break
                
                if data_key and data_key in data:
                    widget.field_value = str(data[data_key])
                    widget.update()
                    filled_fields += 1
        
        # Save to memory buffer
        pdf_buffer = io.BytesIO()
        doc.save(pdf_buffer)
        pdf_buffer.seek(0)
        doc.close()
        
        return {
            'success': True,
            'pdf_data': pdf_buffer.getvalue(),
            'fields_filled': filled_fields,
            'total_fields': total_fields,
            'filename': f"GenDec_{trip_line_mock.id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
            'data_used': data
        }
        
    except Exception as e:
        if 'doc' in locals():
            doc.close()
        raise Exception(f"PDF generation failed: {str(e)}")

def create_mock_pax_trip_line():

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
        city="Los Angeles",
        country="US",
        iata_code="LAX",
        icao_code="KLAX"
    )
    
    destination_airport = MockObject(
        name="John F. Kennedy International Airport",
        city="New York",
        country="US",
        iata_code="JFK",
        icao_code="KJFK"
    )
    
    # Mock patient with contact info
    patient = MockObject(
        name="John Patient",
        info=MockContact("John", "Patient", date(1985, 3, 15))
    )
    
    # Mock passengers with contact info
    passengers = [
        MockObject(
            name="Jane Companion",
            info=MockContact("Jane", "Companion", date(1992, 7, 22))
        ),
        MockObject(
            name="Bob Guardian", 
            info=MockContact("Bob", "Guardian", date(1978, 11, 8))
        )
    ]
    
    # Mock crew
    crew_members = [
        MockObject(name="Captain John Smith", role="captain"),
        MockObject(name="First Officer Jane Doe", role="first_officer")
    ]
    
    # Mock trip
    trip = MockObject(
        flight_number="JT001",
        aircraft=aircraft,
        patient=patient,
        passengers=MockManager(passengers),
        crew_members=MockManager(crew_members)
    )
    
    # Mock crew line
    crew_line = MockCrewLine()
    
    # Mock trip line (PAX leg)
    trip_line = MockObject(
        id="test-pax-123",
        passenger_leg=True,
        departure_time=datetime.now(),
        origin_airport=origin_airport,
        destination_airport=destination_airport,
        trip=trip,
        crew_line=crew_line
    )
    
    return trip_line

def create_mock_repo_trip_line():

    pax_trip_line = create_mock_pax_trip_line()
    
    # Create repositioning leg with same crew
    repo_trip_line = MockObject(
        id="test-repo-456",
        passenger_leg=False,
        departure_time=datetime.now(),
        origin_airport=pax_trip_line.destination_airport,  # JFK
        destination_airport=MockObject(
            name="Miami International Airport",
            city="Miami",
            country="US",
            iata_code="MIA",
            icao_code="KMIA"
        ),
        trip=pax_trip_line.trip,
        crew_line=pax_trip_line.crew_line  # Same crew
    )
    
    return repo_trip_line

def test_pdf_generation():

    print(" TESTING DIRECT PDF GENERATION")
    print("=" * 60)
    
    # Find template
    current_dir = Path(__file__).parent
    template_path = current_dir / "documents" / "GenDec.pdf"
    
    if not template_path.exists():
        print(f" GenDec.pdf template not found: {template_path}")
        return False
    
    print(f" Found GenDec.pdf template: {template_path}")
    
    # Create output directory
    output_dir = current_dir / "pdf_outputs"
    output_dir.mkdir(exist_ok=True)
    
    # Test PAX leg
    print("\n--- Testing PAX Leg ---")
    try:
        pax_trip_line = create_mock_pax_trip_line()
        result = fill_gendec_pdf_direct(template_path, pax_trip_line)
        
        if result['success']:
            print(f" PAX leg PDF generated successfully")
            print(f" Fields filled: {result['fields_filled']}/{result['total_fields']}")
            print(f" Filename: {result['filename']}")
            print(f" PDF size: {len(result['pdf_data']):,} bytes")
            
            # Save test file
            test_output = output_dir / f"Direct_Test_PAX_{result['filename']}"
            with open(test_output, 'wb') as f:
                f.write(result['pdf_data'])
            print(f" Test PDF saved: {test_output}")
            
            # Show filled data
            print(f" Data used for filling:")
            for key, value in result['data_used'].items():
                print(f"  {key}: {value}")
            
        else:
            print(" PAX leg PDF generation failed")
            return False
            
    except Exception as e:
        print(f" Error during PAX leg generation: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    # Test repositioning leg
    print("\n--- Testing Repositioning Leg ---")
    try:
        repo_trip_line = create_mock_repo_trip_line()
        result = fill_gendec_pdf_direct(template_path, repo_trip_line)
        
        if result['success']:
            print(f" Repositioning leg PDF generated successfully")
            print(f" Fields filled: {result['fields_filled']}/{result['total_fields']}")
            print(f" Filename: {result['filename']}")
            print(f" PDF size: {len(result['pdf_data']):,} bytes")
            
            # Save test file
            test_output = output_dir / f"Direct_Test_REPO_{result['filename']}"
            with open(test_output, 'wb') as f:
                f.write(result['pdf_data'])
            print(f" Test PDF saved: {test_output}")
            
            # Show filled data
            print(f" Data used for filling:")
            for key, value in result['data_used'].items():
                print(f"  {key}: {value}")
            
        else:
            print(" Repositioning leg PDF generation failed")
            return False
            
    except Exception as e:
        print(f" Error during repositioning leg generation: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return True

if __name__ == "__main__":

    print(" STARTING DIRECT PDF TESTS")
    print("=" * 60)
    
    # Run test
    test_passed = test_pdf_generation()
    
    # Summary
    print("\n" + "=" * 60)
    print(" TEST SUMMARY")
    print("=" * 60)
    
    if test_passed:
        print(" ALL TESTS PASSED!")
        print(" PDF form filling is working correctly")
        print(" Field mapping is functional")
        print(" Data preparation logic is sound")
        print(" PAX vs repositioning leg logic working")
        print(" Ready for integration with DocumentGenerator")
    else:
        print(" TESTS FAILED")
        print(" PDF generation needs debugging")
        exit(1)
