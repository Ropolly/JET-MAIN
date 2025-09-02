#!/usr/bin/env python
"""
Test script for document generation API endpoints.

This script tests the new API endpoints that generate GenDec and Handling Request
documents directly without storing them.
"""

import os
import sys
import django
from pathlib import Path

# Setup Django environment
sys.path.append(str(Path(__file__).parent))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from django.test import Client
from django.contrib.auth.models import User
from django.utils import timezone
from api.models import *
from utils.docgen.docgen import DocumentGenerator
import json

def setup_test_data():
    """Set up test data for document generation."""
    print("Setting up test data...")
    
    # Create user and authenticate
    user, created = User.objects.get_or_create(
        username='testuser',
        defaults={'email': 'test@example.com'}
    )
    if created:
        user.set_password('testpass123')
        user.save()
    
    # Get or create user profile
    user_profile, created = UserProfile.objects.get_or_create(
        user=user,
        defaults={'first_name': 'Test', 'last_name': 'User'}
    )
    
    # Create airports
    origin_airport, _ = Airport.objects.get_or_create(
        iata_code='LAX',
        defaults={
            'icao_code': 'KLAX',
            'name': 'Los Angeles International Airport',
            'city': 'Los Angeles',
            'country': 'USA',
            'timezone': 'America/Los_Angeles'
        }
    )
    
    destination_airport, _ = Airport.objects.get_or_create(
        iata_code='JFK',
        defaults={
            'icao_code': 'KJFK',
            'name': 'John F. Kennedy International Airport',
            'city': 'New York',
            'country': 'USA',
            'timezone': 'America/New_York'
        }
    )
    
    # Create aircraft
    aircraft, _ = Aircraft.objects.get_or_create(
        tail_number='N123JT',
        defaults={
            'company': 'JET Aviation',
            'make': 'Gulfstream',
            'model': 'G650',
            'serial_number': 'SN12345',
            'mgtow': 45000.00
        }
    )
    
    # Create contacts
    pilot_contact, _ = Contact.objects.get_or_create(
        email='pilot@example.com',
        defaults={
            'first_name': 'John',
            'last_name': 'Pilot',
            'phone': '+1234567890'
        }
    )
    
    patient_contact, _ = Contact.objects.get_or_create(
        email='patient@example.com',
        defaults={
            'first_name': 'Jane',
            'last_name': 'Patient',
            'phone': '+0987654321'
        }
    )
    
    # Create patient
    patient, _ = Patient.objects.get_or_create(
        info=patient_contact,
        defaults={
            'date_of_birth': timezone.now().date() - timezone.timedelta(days=365*45),
            'nationality': 'USA',
            'passport_number': 'P12345678'
        }
    )
    
    # Create crew line
    crew_line, _ = CrewLine.objects.get_or_create(
        primary_in_command=pilot_contact,
        defaults={'secondary_in_command': None}
    )
    
    # Create trip
    trip, _ = Trip.objects.get_or_create(
        trip_number='JT001',
        defaults={
            'aircraft': aircraft,
            'patient': patient,
            'departure_time': timezone.now() + timezone.timedelta(days=1),
            'arrival_time': timezone.now() + timezone.timedelta(days=1, hours=5)
        }
    )
    
    # Create trip line
    trip_line, _ = TripLine.objects.get_or_create(
        trip=trip,
        origin_airport=origin_airport,
        destination_airport=destination_airport,
        defaults={
            'crew_line': crew_line,
            'passenger_leg': True,
            'departure_time': timezone.now() + timezone.timedelta(days=1),
            'arrival_time': timezone.now() + timezone.timedelta(days=1, hours=5),
            'flight_time': timezone.timedelta(hours=5),
            'distance': 2500
        }
    )
    
    print(f"Test data setup complete:")
    print(f"- Trip: {trip.trip_number} ({trip.id})")
    print(f"- Trip Line: {origin_airport.iata_code} -> {destination_airport.iata_code} ({trip_line.id})")
    print(f"- User: {user.username}")
    
    return {
        'trip_line_id': str(trip_line.id),
        'trip_id': str(trip.id),
        'user': user
    }

def test_document_endpoints():
    """Test the document generation endpoints."""
    print("\n" + "="*50)
    print("TESTING DOCUMENT GENERATION ENDPOINTS")
    print("="*50)
    
    # Setup test data  
    test_data = setup_test_data()
    
    # Create test client
    client = Client()
    
    # Login user
    login_success = client.login(username='testuser', password='testpass123')
    if not login_success:
        print("❌ Failed to login user")
        return
    print("✅ User logged in successfully")
    
    # Test document info endpoint
    print("\n--- Testing Document Info Endpoint ---")
    response = client.get('/api/documents/info/')
    print(f"Status Code: {response.status_code}")
    if response.status_code == 200:
        info = response.json()
        print("✅ Document info retrieved successfully")
        print(f"Available document types: {list(info['document_types'].keys())}")
        print(f"Python-docx available: {info['python_docx_available']}")
    else:
        print(f"❌ Document info endpoint failed: {response.content}")
    
    # Test GenDec generation
    print("\n--- Testing GenDec Generation ---")
    response = client.get(f'/api/documents/gendec/{test_data["trip_line_id"]}/')
    print(f"Status Code: {response.status_code}")
    if response.status_code == 200:
        print("✅ GenDec generated successfully")
        print(f"Content-Type: {response.get('Content-Type')}")
        print(f"Content-Disposition: {response.get('Content-Disposition')}")
        print(f"Response size: {len(response.content)} bytes")
    else:
        print(f"❌ GenDec generation failed: {response.content}")
    
    # Test Handling Request generation
    print("\n--- Testing Handling Request Generation ---")
    response = client.get(f'/api/documents/handling-request/{test_data["trip_line_id"]}/')
    print(f"Status Code: {response.status_code}")
    if response.status_code == 200:
        print("✅ Handling Request generated successfully")
        print(f"Content-Type: {response.get('Content-Type')}")
        print(f"Content-Disposition: {response.get('Content-Disposition')}")
        print(f"Response size: {len(response.content)} bytes")
    else:
        print(f"❌ Handling Request generation failed: {response.content}")
    
    # Test trip documents generation (ZIP)
    print("\n--- Testing Trip Documents Generation (ZIP) ---")
    response = client.get(f'/api/documents/trip/{test_data["trip_id"]}/')
    print(f"Status Code: {response.status_code}")
    if response.status_code == 200:
        print("✅ Trip documents ZIP generated successfully")
        print(f"Content-Type: {response.get('Content-Type')}")
        print(f"Content-Disposition: {response.get('Content-Disposition')}")
        print(f"ZIP file size: {len(response.content)} bytes")
    else:
        print(f"❌ Trip documents generation failed: {response.content}")
    
    print("\n" + "="*50)
    print("TESTING COMPLETE!")
    print("="*50)

def test_pax_leg_logic():
    """Test the PAX leg logic in document data preparation."""
    print("\n--- Testing PAX Leg Logic ---")
    
    # Get the test trip line
    try:
        trip_line = TripLine.objects.filter(passenger_leg=True).first()
        if not trip_line:
            print("❌ No PAX leg trip line found")
            return
        
        generator = DocumentGenerator()
        data = generator._prepare_gendec_data(trip_line)
        
        print(f"✅ Data prepared for trip line: {trip_line.origin_airport.iata_code} -> {trip_line.destination_airport.iata_code}")
        print(f"Is PAX leg: {data['is_pax_leg']}")
        print(f"Total PAX count: {data['total_pax_count']}")
        print(f"Combined passengers and patient: {len(data['passengers_and_patient'])}")
        
        # Verify PAX leg logic
        if data['is_pax_leg'] and data['passengers_and_patient']:
            print("✅ PAX leg logic working correctly")
            for i, pax in enumerate(data['passengers_and_patient']):
                print(f"  {i+1}. {pax['name']} ({pax['type']}) - {pax['nationality']}")
        else:
            print("ℹ️ No passengers/patient in this leg")
        
    except Exception as e:
        print(f"❌ Error testing PAX leg logic: {e}")

if __name__ == "__main__":
    try:
        test_document_endpoints()
        test_pax_leg_logic()
    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
