#!/usr/bin/env python3

import fitz  # PyMuPDF
from pathlib import Path
from datetime import datetime
import os
import sys
import io

# Add backend to path for Django imports
backend_dir = Path(__file__).parent.parent.parent
sys.path.append(str(backend_dir))

class GenDecPDFGenerator:

    def __init__(self):
        self.documents_dir = Path(__file__).parent / "documents"
        
        # PDF form field mapping from our data model to actual PDF fields
        self.field_mapping = {
            # Basic aircraft and flight info
            'owner_operator': 'F[0].P1[0].OwnerorOperator[0]',
            'aircraft_registration': 'F[0].P1[0].MarksofNationality[0]',
            'flight_number': 'F[0].P1[0].flightnumber[0]',
            'date': 'F[0].P1[0].Date[0]',
            'departure_from': 'F[0].P1[0].departurefrom[0]',
            'arrive_at': 'F[0].P1[0].arrivaat[0]',
            
            # Passenger/crew counts by destination (places)
            'place1': 'F[0].P1[0].place1[0]',
            'place2': 'F[0].P1[0].place2[0]',
            'place3': 'F[0].P1[0].place3[0]',
            'place4': 'F[0].P1[0].place4[0]',
            'place5': 'F[0].P1[0].place5[0]',
            'place6': 'F[0].P1[0].place6[0]',
            'place7': 'F[0].P1[0].place7[0]',
            'place8': 'F[0].P1[0].place8[0]',
            
            # Total numbers for each destination
            'total1': 'F[0].P1[0].totalnumber1[0]',
            'total2': 'F[0].P1[0].totalnumber2[0]',
            'total3': 'F[0].P1[0].totalnumber3[0]',
            'total4': 'F[0].P1[0].totalnumber4[0]',
            'total5': 'F[0].P1[0].totalnumber5[0]',
            'total6': 'F[0].P1[0].totalnumber6[0]',
            'total7': 'F[0].P1[0].totalnumber7[0]',
            'total8': 'F[0].P1[0].totalnumber8[0]',
            
            # Passenger movement
            'embarking': 'F[0].P1[0].embarking[0]',
            'through_passengers': 'F[0].P1[0].throughonsameflight[0]',
            'disembarking': 'F[0].P1[0].disembarking[0]',
            'through_passengers2': 'F[0].P1[0].throughonsameflight2[0]',
            
            # Declarations and other info
            'declaration': 'F[0].P1[0].declaration1[0]',
            'other_info': 'F[0].P1[0].other1[0]',
            'details': 'F[0].P1[0].details1[0]',
            
            # Signatures
            'captain_signature': 'F[0].P1[0].sign[0]',
            'agent_signature': 'F[0].P1[0].agentsignature[0]',
            
            # Reference numbers
            'sed_number': 'F[0].P1[0].SED[0]',
            'awb_number': 'F[0].P1[0].AWB[0]'
        }

    def prepare_gendec_data_from_trip_line(self, trip_line):

        # Get related objects
        trip = trip_line.trip
        aircraft = trip.aircraft
        
        # Basic flight information
        data = {
            # Aircraft and operator info
            'owner_operator': getattr(aircraft, 'company', 'Unknown Operator'),
            'aircraft_registration': getattr(aircraft, 'tail_number', 'N-UNKNOWN'),
            
            # Flight details
            'flight_number': getattr(trip, 'flight_number', '') or f"TL{trip_line.id}",
            'date': trip_line.departure_time.strftime('%m/%d/%Y') if trip_line.departure_time else datetime.now().strftime('%m/%d/%Y'),
            'departure_from': f"{trip_line.origin_airport.name} ({trip_line.origin_airport.icao_code})" if trip_line.origin_airport else '',
            'arrive_at': f"{trip_line.destination_airport.name} ({trip_line.destination_airport.icao_code})" if trip_line.destination_airport else '',
            
            # Destination routing (simplified for single destination)
            'place1': f"{trip_line.destination_airport.name} ({trip_line.destination_airport.icao_code})" if trip_line.destination_airport else '',
            'place2': '', 'place3': '', 'place4': '', 'place5': '', 'place6': '', 'place7': '', 'place8': '',
        }
        
        # Calculate passenger counts
        if trip_line.passenger_leg:
            # PAX leg: count passengers + patient
            passengers = list(trip.passengers.all()) if hasattr(trip, 'passengers') else []
            patient = trip.patient if hasattr(trip, 'patient') and trip.patient else None
            
            total_pax = len(passengers) + (1 if patient else 0)
            
            data.update({
                'total1': str(total_pax),
                'embarking': str(total_pax),
                'disembarking': str(total_pax),
                'through_passengers': '0',
                'through_passengers2': '0',
            })
            
            # Generate passenger/patient details
            if patient:
                details = f"Patient: {patient.name}"
                if passengers:
                    passenger_names = [p.name for p in passengers]
                    details += f", Passengers: {', '.join(passenger_names)}"
            elif passengers:
                passenger_names = [p.name for p in passengers]
                details = f"Passengers: {', '.join(passenger_names)}"
            else:
                details = "No passengers"
                
            data['details'] = details
            
        else:
            # Repositioning leg: no passengers
            data.update({
                'total1': '0',
                'embarking': '0', 
                'disembarking': '0',
                'through_passengers': '0',
                'through_passengers2': '0',
                'details': 'Repositioning flight - no passengers'
            })
        
        # Add remaining total fields (empty for single destination)
        for i in range(2, 9):
            data[f'total{i}'] = ''
        
        # Crew information
        primary_pilot = None
        if hasattr(trip, 'crew_members'):
            pilots = [crew for crew in trip.crew_members.all() if 'pilot' in crew.role.lower()]
            if pilots:
                primary_pilot = pilots[0].name
        
        data.update({
            'captain_signature': primary_pilot or 'Aircraft Commander',
            'agent_signature': data['owner_operator'],
            'declaration': 'This flight complies with all applicable US Customs regulations',
            'other_info': 'Medical transport flight' if trip_line.passenger_leg else 'Repositioning flight',
            'awb_number': data['flight_number'],
            'sed_number': ''  # Usually left empty unless specific export requirements
        })
        
        return data

    def fill_gendec_pdf(self, trip_line):

        template_path = self.documents_dir / "GenDec.pdf"
        if not template_path.exists():
            raise FileNotFoundError(f"GenDec.pdf template not found: {template_path}")
        
        # Prepare data from trip line
        data = self.prepare_gendec_data_from_trip_line(trip_line)
        
        # Open PDF and fill form
        doc = fitz.open(template_path)
        
        filled_count = 0
        total_fields = 0
        
        try:
            # Fill form fields
            for page_num in range(doc.page_count):
                page = doc[page_num]
                widgets = list(page.widgets())
                
                for widget in widgets:
                    total_fields += 1
                    field_name = widget.field_name
                    
                    # Find matching data for this field
                    data_key = None
                    for key, pdf_field in self.field_mapping.items():
                        if pdf_field == field_name:
                            data_key = key
                            break
                    
                    if data_key and data_key in data and data[data_key]:
                        widget.field_value = str(data[data_key])
                        widget.update()
                        filled_count += 1
            
            # Save to memory buffer
            pdf_buffer = io.BytesIO()
            doc.save(pdf_buffer)
            pdf_buffer.seek(0)
            
            doc.close()
            
            return {
                'success': True,
                'pdf_data': pdf_buffer.getvalue(),
                'fields_filled': filled_count,
                'total_fields': total_fields,
                'filename': f"GenDec_{trip_line.id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
            }
            
        except Exception as e:
            doc.close()
            raise Exception(f"PDF generation failed: {str(e)}")

    def generate_gendec_pdf_for_trip_line(self, trip_line_id):

        try:
            # Import Django models (only when called)
            os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
            import django
            django.setup()
            
            from api.models import TripLine
            
            trip_line = TripLine.objects.get(id=trip_line_id)
            return self.fill_gendec_pdf(trip_line)
            
        except ImportError as e:
            raise Exception(f"Django models not available: {str(e)}")
        except Exception as e:
            raise Exception(f"Failed to generate GenDec PDF: {str(e)}")

def test_pdf_generator():

    print(" TESTING PDF GENERATOR")
    print("=" * 50)
    
    generator = GenDecPDFGenerator()
    
    # Test with mock trip line data
    class MockAircraft:
        company = "JET Charter Services LLC"
        tail_number = "N123JT"
    
    class MockAirport:
        name = "Los Angeles International Airport"
        icao_code = "KLAX"
    
    class MockDestAirport:
        name = "John F. Kennedy International Airport" 
        icao_code = "KJFK"
    
    class MockPatient:
        name = "John Doe"
    
    class MockPassenger:
        name = "Jane Smith"
    
    class MockPassengerManager:
        def all(self):
            return [MockPassenger()]
    
    class MockTrip:
        flight_number = "JET001"
        aircraft = MockAircraft()
        patient = MockPatient()
        passengers = MockPassengerManager()
    
    class MockTripLine:
        id = "test-123"
        passenger_leg = True
        departure_time = datetime.now()
        origin_airport = MockAirport()
        destination_airport = MockDestAirport()
        trip = MockTrip()
    
    try:
        result = generator.fill_gendec_pdf(MockTripLine())
        
        if result['success']:
            print(" PDF generation successful!")
            print(f" Fields filled: {result['fields_filled']}/{result['total_fields']}")
            print(f" Filename: {result['filename']}")
            print(f" PDF size: {len(result['pdf_data']):,} bytes")
            
            # Save test output
            output_dir = Path(__file__).parent / "pdf_outputs"
            output_dir.mkdir(exist_ok=True)
            
            test_path = output_dir / "GenDec_Generator_Test.pdf"
            with open(test_path, 'wb') as f:
                f.write(result['pdf_data'])
            
            print(f" Test PDF saved: {test_path}")
            return True
        else:
            print(" PDF generation failed")
            return False
            
    except Exception as e:
        print(f" Test failed: {str(e)}")
        return False

if __name__ == "__main__":
    success = test_pdf_generator()
    print(f"\n{' TEST PASSED' if success else ' TEST FAILED'}")
    sys.exit(0 if success else 1)
