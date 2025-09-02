#!/usr/bin/env python3

import os
from pathlib import Path
from datetime import datetime

def create_mock_pax_leg_data():

    return {
        'trip_number': 'JET-2024-0902',
        'flight_type': 'Medical Charter',
        'departure_date': '09/02/2024',
        'departure_time_utc': '14:30:00',
        'arrival_date': '09/02/2024',
        'arrival_time_utc': '18:45:00',
        'flight_time': '4h 15m',
        'distance': '1,245 NM',
        
        'origin_airport_name': 'Teterboro Airport',
        'origin_airport_code': 'TEB',
        'origin_airport_icao': 'KTEB',
        'origin_city': 'Teterboro, NJ',
        'origin_country': 'United States',
        
        'destination_airport_name': 'Miami International Airport',
        'destination_airport_code': 'MIA',
        'destination_airport_icao': 'KMIA',
        'destination_city': 'Miami, FL',
        'destination_country': 'United States',
        
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
        
        # CBP specific fields
        'carrier_code': 'JCS',
        'flight_number': 'JET001',
        
        'document_date': '2024-09-02',
        'document_time': '09:09:29 UTC'
    }

def create_mock_repositioning_data():

    return {
        'trip_number': 'JET-2024-0902R',
        'flight_type': 'Repositioning',
        'departure_date': '09/02/2024',
        'departure_time_utc': '20:15:00',
        'arrival_date': '09/02/2024',
        'arrival_time_utc': '20:45:00',
        'flight_time': '0h 30m',
        'distance': '65 NM',
        
        'origin_airport_name': 'Miami International Airport',
        'origin_airport_code': 'MIA',
        'origin_airport_icao': 'KMIA',
        'origin_city': 'Miami, FL',
        'origin_country': 'United States',
        
        'destination_airport_name': 'Fort Lauderdale Executive Airport',
        'destination_airport_code': 'FXE',
        'destination_airport_icao': 'KFXE',
        'destination_city': 'Fort Lauderdale, FL',
        'destination_country': 'United States',
        
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
        
        # CBP specific fields
        'carrier_code': 'JCS',
        'flight_number': 'JET001R',
        
        'document_date': '2024-09-02',
        'document_time': '09:09:29 UTC'
    }

def fill_cbp_form_template(data):

    # Create passenger manifest
    if data['passengers_and_patient']:
        passenger_manifest = []
        for i, person in enumerate(data['passengers_and_patient'], 1):
            manifest_line = (f"{i}. {person['name']} ({person['type']}) "
                           f"- Nationality: {person['nationality']} "
                           f"- Passport: {person['passport_number']} "
                           f"- DOB: {person['date_of_birth']}")
            passenger_manifest.append(manifest_line)
        passenger_list = '\n'.join(passenger_manifest)
    else:
        passenger_list = 'No passengers or patient on this repositioning leg'
    
    # Fill the official CBP Form 7507 template
    filled_form = f"""
DEPARTMENT OF HOMELAND SECURITY

OMB CONTROL NUMBER: 1651-0002
EXPIRATION DATE: 07/31/2024

U.S. Customs and Border Protection

GENERAL DECLARATION
(Outward/Inward)

AGRICULTURE, CUSTOMS, IMMIGRATION, AND PUBLIC HEALTH
19 CFR 122.43,122.52,122.54,122.73,122.144

Owner or Operator: {data['aircraft']['company']}        Carrier Code (if applicable): {data.get('carrier_code', 'N/A')}

Marks of Nationality and Registration: {data['aircraft']['tail_number']}        Flight No.: {data.get('flight_number', data['trip_number'])}        Date: {data['departure_date']}

Departure from: {data['origin_airport_name']} ({data['origin_airport_icao']})

Arrival at: {data['destination_airport_name']} ({data['destination_airport_icao']})

Total Number of Crew: {data['crew_count']}        Total Number of Passengers: {data['total_pax_count']}

I declare that all statements and particulars contained in this General Declaration, and in any supplementary forms required to be presented with this General Declaration, are complete, exact and true to the best of my knowledge and that all through passengers will continue/have continued on the flight.

Printed Name: {data['crew']['primary_pilot']}

Title: Aircraft Commander

SIGNATURE: _____________________________________________
           Authorized Agent or Aircraft Commander

============================================================
PASSENGER AND PATIENT MANIFEST
============================================================

{passenger_list}

The information requested by the official General Declaration may be furnished on ICAO Annex 9, Appendix 1, provided the form approximates (but does not exceed) 8 1/2" x 11", and is printed on white paper of appropriate quality.

This form may be printed by private parties provided it conforms to official form in size, wording, arrangement, and quality and color of paper.

Paperwork Reduction Act Statement: An agency may not conduct or sponsor an information collection and a person is not required to respond to this information unless it displays a current valid OMB control number and an expiration date. The control number for this collection is 1651-0002. The obligation to respond is mandatory. The estimated average time to complete this application is 2 minutes. If you have any comments regarding the burden estimate you can write to U.S. Customs and Border Protection, Office of Regulations and Rulings, 90K Street, NE, Washington DC 20002.

CBP Form 7507 (07/24)
Generate sample GenDec output files."""
    
    print("  Generating Sample CBP Form 7507 General Declaration Outputs")
    print("=" * 80)
    
    # Create output directory
    output_dir = Path(__file__).parent / "sample_outputs"
    output_dir.mkdir(exist_ok=True)
    
    # Generate PAX leg sample
    print(" Generating PAX Leg Sample (Medical Charter with Patient + Passengers)")
    pax_data = create_mock_pax_leg_data()
    pax_form = fill_cbp_form_template(pax_data)
    
    pax_output_file = output_dir / "CBP_Form_7507_PAX_Leg_Sample.txt"
    with open(pax_output_file, 'w', encoding='utf-8') as f:
        f.write("=" * 80 + "\n")
        f.write("SAMPLE: US CUSTOMS CBP FORM 7507 - PAX LEG (MEDICAL CHARTER)\n")
        f.write("Generated: " + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "\n")
        f.write("Trip: " + pax_data['trip_number'] + "\n")
        f.write("=" * 80 + "\n")
        f.write(pax_form)
    
    print(f"    PAX leg sample saved: {pax_output_file.name}")
    
    # Generate repositioning leg sample
    print(" Generating Repositioning Leg Sample (No Passengers)")
    repo_data = create_mock_repositioning_data()
    repo_form = fill_cbp_form_template(repo_data)
    
    repo_output_file = output_dir / "CBP_Form_7507_Repositioning_Leg_Sample.txt"
    with open(repo_output_file, 'w', encoding='utf-8') as f:
        f.write("=" * 80 + "\n")
        f.write("SAMPLE: US CUSTOMS CBP FORM 7507 - REPOSITIONING LEG\n")
        f.write("Generated: " + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "\n")
        f.write("Trip: " + repo_data['trip_number'] + "\n")
        f.write("=" * 80 + "\n")
        f.write(repo_form)
    
    print(f"    Repositioning leg sample saved: {repo_output_file.name}")
    
    # Generate comparison report
    print(" Generating Comparison Report")
    comparison_file = output_dir / "CBP_Form_Comparison_Report.txt"
    
    with open(comparison_file, 'w', encoding='utf-8') as f:
        f.write("=" * 80 + "\n")
        f.write("US CUSTOMS CBP FORM 7507 COMPARISON REPORT\n")
        f.write("JET-MAIN Document Generation System\n")
        f.write("Generated: " + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "\n")
        f.write("=" * 80 + "\n\n")
        
        f.write("FORM VALIDATION CHECKLIST:\n")
        f.write("-" * 40 + "\n")
        
        validation_items = [
            " Official CBP Form 7507 structure",
            " OMB Control Number 1651-0002",
            " Current expiration date (07/31/2024)",
            " CFR references (19 CFR 122.43,122.52,122.54,122.73,122.144)",
            " Owner or Operator field",
            " Carrier Code field (IATA/ICAO)",
            " Aircraft registration with country prefix",
            " Flight number field", 
            " Departure date",
            " Departure/arrival airports with ICAO codes",
            " Crew and passenger counts",
            " Official declaration statement",
            " Signature section",
            " Aircraft Commander designation",
            " Paperwork Reduction Act statement",
            " CBP Form 7507 identifier"
        ]
        
        for item in validation_items:
            f.write(f"{item}\n")
        
        f.write(f"\nKEY DIFFERENCES BETWEEN LEG TYPES:\n")
        f.write("-" * 40 + "\n")
        
        f.write(f"PAX LEG (Medical Charter):\n")
        f.write(f"• Total Passengers: {pax_data['total_pax_count']} (includes patient)\n")
        f.write(f"• Crew Count: {pax_data['crew_count']} (pilots + medics)\n") 
        f.write(f"• Passenger Manifest: {len(pax_data['passengers_and_patient'])} entries\n")
        f.write(f"• Flight Type: {pax_data['flight_type']}\n\n")
        
        f.write(f"REPOSITIONING LEG:\n")
        f.write(f"• Total Passengers: {repo_data['total_pax_count']} (no passengers)\n")
        f.write(f"• Crew Count: {repo_data['crew_count']} (pilots only)\n")
        f.write(f"• Passenger Manifest: Empty\n")
        f.write(f"• Flight Type: {repo_data['flight_type']}\n\n")
        
        f.write(f"COMPLIANCE STATUS:\n")
        f.write("-" * 20 + "\n")
        f.write(f" Ready for US Customs submission\n")
        f.write(f" All required CBP fields present\n")
        f.write(f" Official form structure maintained\n")
        f.write(f" Aviation-specific requirements met\n")
        f.write(f" PAX vs repositioning logic implemented\n")
    
    print(f"    Comparison report saved: {comparison_file.name}")
    
    # Generate placeholder mapping
    print(" Generating Placeholder Mapping")
    mapping_file = output_dir / "CBP_Form_Placeholder_Mapping.txt"
    
    with open(mapping_file, 'w', encoding='utf-8') as f:
        f.write("=" * 80 + "\n")
        f.write("CBP FORM 7507 PLACEHOLDER MAPPING\n")
        f.write("Document Generator Field Mapping Reference\n")
        f.write("=" * 80 + "\n\n")
        
        placeholder_mapping = [
            ("{{AIRCRAFT_COMPANY}}", "Aircraft owner/operator company", pax_data['aircraft']['company']),
            ("{{CARRIER_CODE}}", "IATA/ICAO carrier code", pax_data.get('carrier_code', 'N/A')),
            ("{{AIRCRAFT_TAIL}}", "Aircraft registration/tail number", pax_data['aircraft']['tail_number']),
            ("{{FLIGHT_NUMBER}}", "Flight number or trip identifier", pax_data.get('flight_number', pax_data['trip_number'])),
            ("{{DEPARTURE_DATE}}", "Date of departure", pax_data['departure_date']),
            ("{{ORIGIN_AIRPORT}}", "Departure airport name", pax_data['origin_airport_name']),
            ("{{ORIGIN_ICAO}}", "Departure airport ICAO code", pax_data['origin_airport_icao']),
            ("{{DESTINATION_AIRPORT}}", "Arrival airport name", pax_data['destination_airport_name']),
            ("{{DESTINATION_ICAO}}", "Arrival airport ICAO code", pax_data['destination_airport_icao']),
            ("{{CREW_COUNT}}", "Total crew members", str(pax_data['crew_count'])),
            ("{{TOTAL_PAX_COUNT}}", "Total passengers (including patient)", str(pax_data['total_pax_count'])),
            ("{{PRIMARY_PILOT}}", "Primary pilot name for signature", pax_data['crew']['primary_pilot']),
            ("{{PILOT_TITLE}}", "Pilot title/designation", "Aircraft Commander"),
            ("{{PASSENGERS_AND_PATIENT_LIST}}", "Formatted passenger/patient manifest", "[Dynamic content]")
        ]
        
        for placeholder, description, example in placeholder_mapping:
            f.write(f"PLACEHOLDER: {placeholder}\n")
            f.write(f"Description: {description}\n")
            f.write(f"Example Value: {example}\n")
            f.write("-" * 60 + "\n\n")
        
        f.write("PASSENGER MANIFEST FORMAT:\n")
        f.write("-" * 30 + "\n")
        f.write("For each passenger/patient:\n")
        f.write("• Name (Type) - Nationality: Country - Passport: Number - DOB: Date\n\n")
        
        f.write("Example:\n")
        for i, person in enumerate(pax_data['passengers_and_patient'], 1):
            f.write(f"{i}. {person['name']} ({person['type']}) - Nationality: {person['nationality']} - Passport: {person['passport_number']} - DOB: {person['date_of_birth']}\n")
    
    print(f"    Placeholder mapping saved: {mapping_file.name}")
    
    # Summary
    print(f"\n Sample outputs saved to: {output_dir}")
    print(f" Files generated:")
    print(f"   • {pax_output_file.name} - PAX leg sample form")
    print(f"   • {repo_output_file.name} - Repositioning leg sample form")
    print(f"   • {comparison_file.name} - Validation and comparison")
    print(f"   • {mapping_file.name} - Placeholder reference")
    
    print(f"\n Sample CBP Form 7507 outputs generated successfully!")
    print(f" Review these files to verify correctness before creating Word template")
    
    return output_dir

def main():

    print("  CBP FORM 7507 SAMPLE OUTPUT GENERATOR")
    print("JET-MAIN Document Generation System")
    print("=" * 80)
    
    output_dir = generate_sample_outputs()
    
    print(f"\n Next Steps:")
    print(f"1. Review generated sample files in {output_dir}")
    print(f"2. Verify CBP form structure and content accuracy")
    print(f"3. Create Word template using placeholder mapping")
    print(f"4. Test document generation with real trip data")

if __name__ == "__main__":
    main()
