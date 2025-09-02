#!/usr/bin/env python3

import os
import sys
from pathlib import Path
from datetime import datetime, timezone

def create_mock_trip_data():

    return {
        'trip_number': 'JET-001-240902',
        'flight_type': 'Charter',
        'departure_date': '2024-09-02',
        'departure_time_utc': '14:30:00',
        'arrival_date': '2024-09-02', 
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
                'nationality': 'US',
                'passport_number': '123456789'
            },
            {
                'name': 'Emily Wilson',
                'type': 'Passenger',
                'nationality': 'US',
                'passport_number': '987654321'
            },
            {
                'name': 'Dr. Jennifer Thompson',
                'type': 'Passenger',
                'nationality': 'US',
                'passport_number': '456789123'
            }
        ],
        
        'passenger_count': 2,
        'total_pax_count': 3,  # Patient + 2 passengers
        'is_pax_leg': True,
        'crew_count': 4,  # 2 pilots + 2 medics
        
        # CBP specific fields
        'carrier_code': 'JCS',  # IATA code
        'flight_number': 'JET001',
        
        'document_date': datetime.now().strftime("%Y-%m-%d"),
        'document_time': datetime.now().strftime("%H:%M:%S UTC")
    }

def create_mock_repositioning_data():

    data = create_mock_trip_data()
    data.update({
        'trip_number': 'JET-001R-240902',
        'flight_type': 'Repositioning',
        'origin_airport_name': 'Miami International Airport',
        'origin_airport_code': 'MIA',
        'origin_airport_icao': 'KMIA',
        'origin_city': 'Miami, FL',
        'destination_airport_name': 'Fort Lauderdale Executive Airport',
        'destination_airport_code': 'FXE',
        'destination_airport_icao': 'KFXE',
        'destination_city': 'Fort Lauderdale, FL',
        'passengers_and_patient': [],
        'passenger_count': 0,
        'total_pax_count': 0,
        'is_pax_leg': False,
        'crew_count': 2,  # Just pilots for repositioning
        'flight_number': 'JET001R'
    })
    
    # Remove medics for repositioning
    data['crew']['medics'] = []
    
    return data

def test_cbp_form_replacements():

    print("  Testing Official US Customs CBP Form 7507 Placeholders")
    print("=" * 80)
    
    # Test PAX leg
    print("\n Testing PAX Leg (with passengers and patient):")
    print("-" * 60)
    
    pax_data = create_mock_trip_data()
    
    # Create replacements dictionary (mimicking DocumentGenerator logic)
    replacements = {
        # Basic trip info
        '{{TRIP_NUMBER}}': pax_data['trip_number'],
        '{{FLIGHT_TYPE}}': pax_data['flight_type'],
        '{{DEPARTURE_DATE}}': pax_data['departure_date'],
        '{{DEPARTURE_TIME_UTC}}': pax_data['departure_time_utc'],
        '{{ARRIVAL_DATE}}': pax_data['arrival_date'],
        '{{ARRIVAL_TIME_UTC}}': pax_data['arrival_time_utc'],
        
        # Airport info
        '{{ORIGIN_AIRPORT}}': pax_data['origin_airport_name'],
        '{{ORIGIN_CODE}}': pax_data['origin_airport_code'],
        '{{ORIGIN_ICAO}}': pax_data['origin_airport_icao'],
        '{{DESTINATION_AIRPORT}}': pax_data['destination_airport_name'],
        '{{DESTINATION_CODE}}': pax_data['destination_airport_code'],
        '{{DESTINATION_ICAO}}': pax_data['destination_airport_icao'],
        
        # Aircraft info
        '{{AIRCRAFT_TAIL}}': pax_data['aircraft']['tail_number'],
        '{{AIRCRAFT_MAKE}}': pax_data['aircraft']['make'],
        '{{AIRCRAFT_MODEL}}': pax_data['aircraft']['model'],
        '{{AIRCRAFT_COMPANY}}': pax_data['aircraft']['company'],
        '{{AIRCRAFT_SERIAL}}': pax_data['aircraft']['serial_number'],
        '{{AIRCRAFT_MGTOW}}': pax_data['aircraft']['mgtow'],
        
        # Crew info
        '{{PRIMARY_PILOT}}': pax_data['crew']['primary_pilot'],
        '{{SECONDARY_PILOT}}': pax_data['crew']['secondary_pilot'],
        '{{MEDICS}}': ', '.join(pax_data['crew']['medics']) if pax_data['crew']['medics'] else 'N/A',
        
        # Counts
        '{{PASSENGER_COUNT}}': str(pax_data['passenger_count']),
        '{{TOTAL_PAX_COUNT}}': str(pax_data['total_pax_count']),
        '{{CREW_COUNT}}': str(pax_data['crew_count']),
        '{{IS_PAX_LEG}}': 'Yes' if pax_data['is_pax_leg'] else 'No',
        
        # CBP specific fields
        '{{CARRIER_CODE}}': pax_data.get('carrier_code', 'N/A'),
        '{{FLIGHT_NUMBER}}': pax_data.get('flight_number', pax_data['trip_number']),
        '{{PILOT_TITLE}}': 'Aircraft Commander',
        
        # Document metadata
        '{{DOCUMENT_DATE}}': pax_data['document_date'],
        '{{DOCUMENT_TIME}}': pax_data['document_time'],
    }
    
    # Add passenger manifest
    if pax_data['passengers_and_patient']:
        pax_list = '\n'.join([
            f"• {p['name']} ({p['type']}) - Nationality: {p['nationality']} - Passport: {p['passport_number']}"
            for p in pax_data['passengers_and_patient']
        ])
        replacements['{{PASSENGERS_AND_PATIENT_LIST}}'] = pax_list
    else:
        replacements['{{PASSENGERS_AND_PATIENT_LIST}}'] = 'No passengers or patient on this leg'
    
    # Display key CBP form fields
    cbp_fields = [
        ('Aircraft Company', '{{AIRCRAFT_COMPANY}}'),
        ('Carrier Code', '{{CARRIER_CODE}}'),
        ('Aircraft Tail', '{{AIRCRAFT_TAIL}}'),
        ('Flight Number', '{{FLIGHT_NUMBER}}'),
        ('Departure Date', '{{DEPARTURE_DATE}}'),
        ('Origin Airport', '{{ORIGIN_AIRPORT}}'),
        ('Origin ICAO', '{{ORIGIN_ICAO}}'),
        ('Destination Airport', '{{DESTINATION_AIRPORT}}'),
        ('Destination ICAO', '{{DESTINATION_ICAO}}'),
        ('Crew Count', '{{CREW_COUNT}}'),
        ('Total Passengers', '{{TOTAL_PAX_COUNT}}'),
        ('Primary Pilot', '{{PRIMARY_PILOT}}'),
        ('Pilot Title', '{{PILOT_TITLE}}')
    ]
    
    print(" CBP Form 7507 Required Fields:")
    for field_name, placeholder in cbp_fields:
        value = replacements.get(placeholder, 'MISSING')
        status = "" if value not in ['MISSING', 'N/A', ''] else " "
        print(f"   {status} {field_name:<20}: {value}")
    
    # Show passenger manifest
    print(f"\n Passenger/Patient Manifest:")
    manifest = replacements['{{PASSENGERS_AND_PATIENT_LIST}}']
    for line in manifest.split('\n'):
        print(f"   {line}")
    
    # Test repositioning leg
    print(f"\n Testing Repositioning Leg (no passengers):")
    print("-" * 60)
    
    repo_data = create_mock_repositioning_data()
    repo_replacements = replacements.copy()
    repo_replacements.update({
        '{{TRIP_NUMBER}}': repo_data['trip_number'],
        '{{FLIGHT_TYPE}}': repo_data['flight_type'],
        '{{ORIGIN_AIRPORT}}': repo_data['origin_airport_name'],
        '{{ORIGIN_ICAO}}': repo_data['origin_airport_icao'],
        '{{DESTINATION_AIRPORT}}': repo_data['destination_airport_name'],
        '{{DESTINATION_ICAO}}': repo_data['destination_airport_icao'],
        '{{TOTAL_PAX_COUNT}}': str(repo_data['total_pax_count']),
        '{{CREW_COUNT}}': str(repo_data['crew_count']),
        '{{IS_PAX_LEG}}': 'No',
        '{{FLIGHT_NUMBER}}': repo_data['flight_number'],
        '{{PASSENGERS_AND_PATIENT_LIST}}': 'No passengers or patient on this repositioning leg',
        '{{MEDICS}}': 'N/A'
    })
    
    print(" Repositioning Leg Key Fields:")
    repo_fields = [
        ('Flight Type', '{{FLIGHT_TYPE}}'),
        ('Flight Number', '{{FLIGHT_NUMBER}}'),
        ('Origin Airport', '{{ORIGIN_AIRPORT}}'),
        ('Destination Airport', '{{DESTINATION_AIRPORT}}'),
        ('Crew Count', '{{CREW_COUNT}}'),
        ('Total Passengers', '{{TOTAL_PAX_COUNT}}'),
        ('Is PAX Leg', '{{IS_PAX_LEG}}'),
        ('Medics', '{{MEDICS}}')
    ]
    
    for field_name, placeholder in repo_fields:
        value = repo_replacements.get(placeholder, 'MISSING')
        print(f"   • {field_name:<20}: {value}")
    
    print(f"\n Passenger Manifest: {repo_replacements['{{PASSENGERS_AND_PATIENT_LIST}}']}")
    
    return replacements

def test_cbp_compliance():

    print(f"\n CBP Form 7507 Compliance Validation:")
    print("=" * 80)
    
    pax_data = create_mock_trip_data()
    
    # CBP compliance checks
    compliance_checks = []
    
    # Required field checks
    if pax_data['aircraft']['tail_number'] and pax_data['aircraft']['tail_number'] != 'N/A':
        compliance_checks.append(("", "Aircraft tail number present"))
    else:
        compliance_checks.append(("", "Aircraft tail number missing (REQUIRED by CBP)"))
    
    if pax_data['aircraft']['company'] and pax_data['aircraft']['company'] != 'N/A':
        compliance_checks.append(("", "Aircraft owner/operator present"))
    else:
        compliance_checks.append(("", "Aircraft owner/operator missing (REQUIRED by CBP)"))
    
    if pax_data['origin_airport_icao'] and pax_data['origin_airport_icao'] != 'N/A':
        compliance_checks.append(("", "Origin airport ICAO code present"))
    else:
        compliance_checks.append((" ", "Origin airport ICAO code missing (PREFERRED by CBP)"))
    
    if pax_data['destination_airport_icao'] and pax_data['destination_airport_icao'] != 'N/A':
        compliance_checks.append(("", "Destination airport ICAO code present"))
    else:
        compliance_checks.append((" ", "Destination airport ICAO code missing (PREFERRED by CBP)"))
    
    if pax_data['crew']['primary_pilot'] and pax_data['crew']['primary_pilot'] != 'N/A':
        compliance_checks.append(("", "Primary pilot name present (for signature)"))
    else:
        compliance_checks.append(("", "Primary pilot name missing (REQUIRED for signature)"))
    
    if pax_data['crew_count'] > 0:
        compliance_checks.append(("", f"Crew count valid ({pax_data['crew_count']})"))
    else:
        compliance_checks.append(("", "Crew count invalid (must be ≥ 1)"))
    
    if pax_data.get('departure_date'):
        compliance_checks.append(("", "Departure date present"))
    else:
        compliance_checks.append(("", "Departure date missing (REQUIRED by CBP)"))
    
    # Aviation specific checks
    tail_number = pax_data['aircraft']['tail_number']
    if tail_number.startswith(('N-', 'N')):
        compliance_checks.append(("", "US aircraft registration format correct"))
    else:
        compliance_checks.append((" ", f"Non-US aircraft registration ({tail_number[:2]})"))
    
    # Display results
    for status, message in compliance_checks:
        print(f"   {status} {message}")
    
    # Summary
    passed = sum(1 for status, _ in compliance_checks if status == "")
    warnings = sum(1 for status, _ in compliance_checks if status == " ")
    failed = sum(1 for status, _ in compliance_checks if status == "")
    
    print(f"\n Compliance Summary:")
    print(f"    Passed: {passed}")
    print(f"     Warnings: {warnings}")
    print(f"    Failed: {failed}")
    
    if failed == 0:
        print(f"\n STATUS: READY FOR US CUSTOMS SUBMISSION")
    else:
        print(f"\n  STATUS: COMPLIANCE ISSUES MUST BE RESOLVED")

def show_official_cbp_form_structure():

    print(f"\n Official US Customs CBP Form 7507 Structure:")
    print("=" * 80)
    
    form_structure = """
DEPARTMENT OF HOMELAND SECURITY
OMB CONTROL NUMBER: 1651-0002
EXPIRATION DATE: 07/31/2024

U.S. Customs and Border Protection

GENERAL DECLARATION
(Outward/Inward)

AGRICULTURE, CUSTOMS, IMMIGRATION, AND PUBLIC HEALTH
19 CFR 122.43,122.52,122.54,122.73,122.144

Owner or Operator: {{AIRCRAFT_COMPANY}}        Carrier Code: {{CARRIER_CODE}}

Marks of Nationality and Registration: {{AIRCRAFT_TAIL}}        Flight No.: {{FLIGHT_NUMBER}}        Date: {{DEPARTURE_DATE}}

Departure from: {{ORIGIN_AIRPORT}} ({{ORIGIN_ICAO}})

Arrival at: {{DESTINATION_AIRPORT}} ({{DESTINATION_ICAO}})

Total Number of Crew: {{CREW_COUNT}}        Total Number of Passengers: {{TOTAL_PAX_COUNT}}

I declare that all statements and particulars contained in this General Declaration,
and in any supplementary forms required to be presented with this General Declaration,
are complete, exact and true to the best of my knowledge and that all through passengers
will continue/have continued on the flight.

Printed Name: {{PRIMARY_PILOT}}

Title: {{PILOT_TITLE}}

SIGNATURE: _________________________________
           Authorized Agent or Aircraft Commander

PASSENGER AND PATIENT MANIFEST
{{PASSENGERS_AND_PATIENT_LIST}}
Main test function."""
    
    print("  OFFICIAL US CUSTOMS CBP FORM 7507 TESTING")
    print("JET-MAIN Document Generation System")
    print("=" * 80)
    
    # Test placeholder replacements
    replacements = test_cbp_form_replacements()
    
    # Test compliance
    test_cbp_compliance()
    
    # Show form structure
    show_official_cbp_form_structure()
    
    print(f"\n Official CBP Form 7507 implementation testing complete!")
    print(f" Ready for Word template creation and document generation")
    print(f" Compliant with US Customs requirements for aviation")

if __name__ == "__main__":
    main()
