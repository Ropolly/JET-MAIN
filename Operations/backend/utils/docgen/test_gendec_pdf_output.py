#!/usr/bin/env python3

import os
import sys
from pathlib import Path
from datetime import datetime

# Add the backend to Python path
sys.path.append(str(Path(__file__).parent.parent.parent))

def create_mock_pax_leg_data():

    return {
        'trip_number': 'JET-2024-0902',
        'departure_date': '09/02/2024',
        'departure_time_utc': '14:30:00',
        'arrival_date': '09/02/2024', 
        'arrival_time_utc': '18:45:00',
        
        'origin_airport_name': 'Teterboro Airport',
        'origin_airport_code': 'TEB',
        'origin_airport_icao': 'KTEB',
        'origin_city': 'Teterboro, NJ',
        
        'destination_airport_name': 'Miami International Airport',
        'destination_airport_code': 'MIA',
        'destination_airport_icao': 'KMIA',
        'destination_city': 'Miami, FL',
        
        'aircraft': {
            'tail_number': 'N525JT',
            'make': 'Cessna',
            'model': 'Citation CJ3+',
            'company': 'JET Charter Services LLC',
            'serial_number': '525C-0924',
            'mgtow': '13,870'
        },
        
        'crew': {
            'primary_pilot': 'Captain John Smith',
            'secondary_pilot': 'First Officer Sarah Johnson',
            'medics': ['Dr. Michael Brown', 'Paramedic Lisa Davis']
        },
        
        'passengers_and_patient': [
            {
                'name': 'Robert Wilson',
                'type': 'Patient',
                'nationality': 'United States',
                'passport_number': 'P123456789',
                'date_of_birth': '1965-03-15'
            },
            {
                'name': 'Emily Wilson', 
                'type': 'Passenger',
                'nationality': 'United States',
                'passport_number': 'P987654321',
                'date_of_birth': '1968-07-22'
            },
            {
                'name': 'Dr. Jennifer Thompson',
                'type': 'Passenger', 
                'nationality': 'United States',
                'passport_number': 'P456789123',
                'date_of_birth': '1972-11-08'
            }
        ],
        
        'passenger_count': 2,
        'total_pax_count': 3,
        'is_pax_leg': True,
        'crew_count': 4,
        'carrier_code': 'JCS',
        'flight_number': 'JET001',
        'pilot_title': 'Aircraft Commander'
    }

def create_mock_repositioning_data():

    return {
        'trip_number': 'JET-2024-0902R',
        'departure_date': '09/02/2024',
        'departure_time_utc': '20:15:00',
        'arrival_date': '09/02/2024',
        'arrival_time_utc': '20:45:00',
        
        'origin_airport_name': 'Miami International Airport',
        'origin_airport_code': 'MIA', 
        'origin_airport_icao': 'KMIA',
        'origin_city': 'Miami, FL',
        
        'destination_airport_name': 'Fort Lauderdale Executive Airport',
        'destination_airport_code': 'FXE',
        'destination_airport_icao': 'KFXE',
        'destination_city': 'Fort Lauderdale, FL',
        
        'aircraft': {
            'tail_number': 'N525JT',
            'make': 'Cessna',
            'model': 'Citation CJ3+',
            'company': 'JET Charter Services LLC',
            'serial_number': '525C-0924',
            'mgtow': '13,870'
        },
        
        'crew': {
            'primary_pilot': 'Captain John Smith',
            'secondary_pilot': 'First Officer Sarah Johnson',
            'medics': []
        },
        
        'passengers_and_patient': [],
        
        'passenger_count': 0,
        'total_pax_count': 0,
        'is_pax_leg': False,
        'crew_count': 2,
        'carrier_code': 'JCS', 
        'flight_number': 'JET001R',
        'pilot_title': 'Aircraft Commander'
    }

def test_document_generation():

    print(" TESTING GENDEC PDF GENERATION")
    print("=" * 60)
    
    try:
        # Import the document generator
        from utils.docgen.docgen import DocumentGenerator
        
        # Initialize generator
        generator = DocumentGenerator()
        
        # Create output directory for PDFs
        output_dir = Path(__file__).parent / "pdf_outputs"
        output_dir.mkdir(exist_ok=True)
        
        print(f" PDF outputs will be saved to: {output_dir}")
        
        # Test PAX leg
        print("\n Testing PAX Leg GenDec (Medical Charter)")
        print("-" * 40)
        
        pax_data = create_mock_pax_leg_data()
        
        try:
            # Generate GenDec document for PAX leg
            pdf_content = generator.generate_gendec_pdf(pax_data)
            
            # Save PDF file
            pax_filename = f"GenDec_PAX_Leg_{pax_data['flight_number']}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
            pax_filepath = output_dir / pax_filename
            
            with open(pax_filepath, 'wb') as f:
                f.write(pdf_content)
            
            print(f"    PAX leg PDF generated: {pax_filename}")
            print(f"    File size: {len(pdf_content):,} bytes")
            print(f"    Flight: {pax_data['origin_airport_icao']} → {pax_data['destination_airport_icao']}")
            print(f"    Passengers: {pax_data['total_pax_count']} (including patient)")
            print(f"    Crew: {pax_data['crew_count']}")
            
        except Exception as e:
            print(f"    PAX leg generation failed: {str(e)}")
        
        # Test repositioning leg
        print("\n Testing Repositioning Leg GenDec")
        print("-" * 40)
        
        repo_data = create_mock_repositioning_data()
        
        try:
            # Generate GenDec document for repositioning leg
            pdf_content = generator.generate_gendec_pdf(repo_data)
            
            # Save PDF file
            repo_filename = f"GenDec_Repositioning_{repo_data['flight_number']}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
            repo_filepath = output_dir / repo_filename
            
            with open(repo_filepath, 'wb') as f:
                f.write(pdf_content)
            
            print(f"    Repositioning PDF generated: {repo_filename}")
            print(f"    File size: {len(pdf_content):,} bytes")
            print(f"    Flight: {repo_data['origin_airport_icao']} → {repo_data['destination_airport_icao']}")
            print(f"    Passengers: {repo_data['total_pax_count']}")
            print(f"    Crew: {repo_data['crew_count']}")
            
        except Exception as e:
            print(f"    Repositioning generation failed: {str(e)}")
        
        print(f"\n Generated files location: {output_dir}")
        print(" GenDec PDF testing complete!")
        
    except ImportError as e:
        print(f" Import error: {str(e)}")
        print(" Using mock generation instead...")
        test_mock_generation()
    except Exception as e:
        print(f" Error: {str(e)}")
        print(" Using mock generation instead...")
        test_mock_generation()

def test_mock_generation():

    print("\n MOCK GENDEC PDF GENERATION TEST")
    print("=" * 60)
    
    # Create output directory
    output_dir = Path(__file__).parent / "pdf_outputs"
    output_dir.mkdir(exist_ok=True)
    
    # Create mock PDF content info files
    pax_data = create_mock_pax_leg_data()
    repo_data = create_mock_repositioning_data()
    
    # Mock PAX leg PDF info
    pax_info_file = output_dir / f"GenDec_PAX_Info_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    with open(pax_info_file, 'w') as f:
        f.write("MOCK GENDEC PDF - PAX LEG (MEDICAL CHARTER)\n")
        f.write("=" * 50 + "\n\n")
        f.write(f"Trip Number: {pax_data['trip_number']}\n")
        f.write(f"Flight Number: {pax_data['flight_number']}\n")
        f.write(f"Aircraft: {pax_data['aircraft']['tail_number']} ({pax_data['aircraft']['make']} {pax_data['aircraft']['model']})\n")
        f.write(f"Route: {pax_data['origin_airport_icao']} → {pax_data['destination_airport_icao']}\n") 
        f.write(f"Date: {pax_data['departure_date']}\n")
        f.write(f"Crew Count: {pax_data['crew_count']}\n")
        f.write(f"Passenger Count: {pax_data['total_pax_count']} (including patient)\n\n")
        
        f.write("PASSENGERS AND PATIENT:\n")
        for i, person in enumerate(pax_data['passengers_and_patient'], 1):
            f.write(f"{i}. {person['name']} ({person['type']})\n")
        
        f.write(f"\nThis would be generated as a PDF from GenDec.docx template\n")
        f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    print(f" PAX leg mock info: {pax_info_file.name}")
    
    # Mock repositioning leg PDF info  
    repo_info_file = output_dir / f"GenDec_Repositioning_Info_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    with open(repo_info_file, 'w') as f:
        f.write("MOCK GENDEC PDF - REPOSITIONING LEG\n")
        f.write("=" * 50 + "\n\n")
        f.write(f"Trip Number: {repo_data['trip_number']}\n")
        f.write(f"Flight Number: {repo_data['flight_number']}\n")
        f.write(f"Aircraft: {repo_data['aircraft']['tail_number']} ({repo_data['aircraft']['make']} {repo_data['aircraft']['model']})\n")
        f.write(f"Route: {repo_data['origin_airport_icao']} → {repo_data['destination_airport_icao']}\n")
        f.write(f"Date: {repo_data['departure_date']}\n")
        f.write(f"Crew Count: {repo_data['crew_count']}\n") 
        f.write(f"Passenger Count: {repo_data['total_pax_count']}\n\n")
        f.write(f"No passengers on repositioning leg\n\n")
        f.write(f"This would be generated as a PDF from GenDec.docx template\n")
        f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    print(f" Repositioning mock info: {repo_info_file.name}")
    
    # Template info
    template_info_file = output_dir / "GenDec_Template_Info.txt"
    with open(template_info_file, 'w') as f:
        f.write("GENDEC TEMPLATE INFORMATION\n")
        f.write("=" * 50 + "\n\n")
        f.write("Template File: GenDec.docx\n")
        f.write("Location: utils/docgen/documents/GenDec.docx\n")
        f.write("Output Format: PDF\n\n")
        
        f.write("KEY PLACEHOLDERS:\n")
        placeholders = [
            "{{AIRCRAFT_COMPANY}} - Aircraft owner/operator",
            "{{CARRIER_CODE}} - IATA/ICAO carrier code", 
            "{{AIRCRAFT_TAIL}} - Aircraft registration",
            "{{FLIGHT_NUMBER}} - Flight number",
            "{{DEPARTURE_DATE}} - Date of departure",
            "{{ORIGIN_AIRPORT}} - Departure airport",
            "{{ORIGIN_ICAO}} - Departure ICAO code", 
            "{{DESTINATION_AIRPORT}} - Arrival airport",
            "{{DESTINATION_ICAO}} - Arrival ICAO code",
            "{{CREW_COUNT}} - Total crew members",
            "{{TOTAL_PAX_COUNT}} - Total passengers",
            "{{PRIMARY_PILOT}} - Primary pilot name",
            "{{PILOT_TITLE}} - Pilot designation",
            "{{PASSENGERS_AND_PATIENT_LIST}} - Passenger manifest"
        ]
        
        for placeholder in placeholders:
            f.write(f"• {placeholder}\n")
        
        f.write(f"\nGenerated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    print(f" Template info: {template_info_file.name}")
    print(f"\n Mock files saved to: {output_dir}")
    print(" Mock GenDec PDF generation complete!")

def main():

    print(" GENDEC PDF OUTPUT GENERATOR")
    print("JET-MAIN Document Generation System")
    print("=" * 60)
    
    test_document_generation()
    
    print(f"\n Next Steps:")
    print("1. Review generated PDF files")
    print("2. Verify GenDec template content and formatting")
    print("3. Test with real trip data from database")
    print("4. Validate PDF output meets requirements")

if __name__ == "__main__":
    main()
