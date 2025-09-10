#!/usr/bin/env python3
"""
Create test data for document generation testing
"""
import os
import sys
import django
from datetime import datetime, timedelta
from decimal import Decimal

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from api.models import Contact, Airport, Aircraft, Quote, Patient, Trip, TripLine, CrewLine, Passenger
from django.contrib.auth.models import User

def create_test_data():
    print("Creating test data for document generation...")
    
    # Get or create admin user
    admin_user = User.objects.get(username='admin')
    
    # Create test airports
    jfk, _ = Airport.objects.get_or_create(
        ident='KJFK',
        defaults={
            'name': 'John F Kennedy International Airport',
            'icao_code': 'KJFK',
            'iata_code': 'JFK',
            'municipality': 'New York',
            'iso_country': 'US',
            'iso_region': 'US-NY',
            'latitude': 40.6413,
            'longitude': -73.7781,
            'elevation': 13,
            'created_by': admin_user
        }
    )
    
    lax, _ = Airport.objects.get_or_create(
        ident='KLAX',
        defaults={
            'name': 'Los Angeles International Airport',
            'icao_code': 'KLAX',
            'iata_code': 'LAX',
            'municipality': 'Los Angeles',
            'iso_country': 'US',
            'iso_region': 'US-CA',
            'latitude': 33.9425,
            'longitude': -118.4081,
            'elevation': 125,
            'created_by': admin_user
        }
    )
    
    # Create test contact
    contact, _ = Contact.objects.get_or_create(
        email='test@example.com',
        defaults={
            'first_name': 'John',
            'last_name': 'Smith',
            'business_name': 'Test Medical Center',
            'phone': '555-123-4567',
            'address_line1': '123 Main St',
            'city': 'New York',
            'state': 'NY',
            'zip': '10001',
            'created_by': admin_user
        }
    )
    
    # Create patient contact
    patient_contact, _ = Contact.objects.get_or_create(
        email='patient@example.com',
        defaults={
            'first_name': 'Jane',
            'last_name': 'Doe',
            'phone': '555-987-6543',
            'date_of_birth': datetime(1980, 5, 15).date(),
            'created_by': admin_user
        }
    )
    
    # Create patient
    patient, _ = Patient.objects.get_or_create(
        info=patient_contact,
        defaults={
            'nationality': 'US',
            'date_of_birth': datetime(1980, 5, 15).date(),
            'passport_expiration_date': datetime(2030, 5, 15).date(),
            'created_by': admin_user
        }
    )
    
    # Create aircraft
    aircraft, _ = Aircraft.objects.get_or_create(
        tail_number='N123JM',
        defaults={
            'make': 'Learjet',
            'model': '65',
            'company': 'JET ICU MEDICAL TRANSPORT',
            'mgtow': 23500,
            'created_by': admin_user
        }
    )
    
    # Create quote
    quote, _ = Quote.objects.get_or_create(
        contact=contact,
        defaults={
            'quoted_amount': Decimal('25000.00'),
            'pickup_airport': jfk,
            'dropoff_airport': lax,
            'aircraft_type': '65',
            'estimated_flight_time': timedelta(hours=5, minutes=30),
            'includes_grounds': True,
            'medical_team': 'RN/MD',
            'patient': patient,
            'quote_pdf_email': 'test@example.com',
            'number_of_stops': 0,
            'created_by': admin_user
        }
    )
    
    # Create crew contacts
    pic_contact, _ = Contact.objects.get_or_create(
        email='pilot1@jeticu.com',
        defaults={
            'first_name': 'Captain',
            'last_name': 'Johnson',
            'created_by': admin_user
        }
    )
    
    sic_contact, _ = Contact.objects.get_or_create(
        email='pilot2@jeticu.com',
        defaults={
            'first_name': 'First Officer',
            'last_name': 'Williams',
            'created_by': admin_user
        }
    )
    
    medic1_contact, _ = Contact.objects.get_or_create(
        email='medic1@jeticu.com',
        defaults={
            'first_name': 'Dr. Sarah',
            'last_name': 'Davis',
            'created_by': admin_user
        }
    )
    
    medic2_contact, _ = Contact.objects.get_or_create(
        email='medic2@jeticu.com',
        defaults={
            'first_name': 'Nurse',
            'last_name': 'Brown',
            'created_by': admin_user
        }
    )
    
    # Create crew line
    crew_line, _ = CrewLine.objects.get_or_create(
        primary_in_command=pic_contact,
        secondary_in_command=sic_contact,
        defaults={
            'created_by': admin_user
        }
    )
    crew_line.medic_ids.add(medic1_contact, medic2_contact)
    
    # Create passenger
    passenger, _ = Passenger.objects.get_or_create(
        info=contact,
        defaults={
            'nationality': 'US',
            'passport_number': 'A12345678',
            'contact_number': '555-123-4567',
            'created_by': admin_user
        }
    )
    
    # Create trip
    trip, _ = Trip.objects.get_or_create(
        trip_number='00001',
        defaults={
            'quote': quote,
            'type': 'medical',
            'patient': patient,
            'aircraft': aircraft,
            'estimated_departure_time': datetime.now() + timedelta(days=1),
            'pre_flight_duty_time': timedelta(hours=1),
            'post_flight_duty_time': timedelta(minutes=30),
            'notes': 'Medical transport with specialized equipment required',
            'created_by': admin_user
        }
    )
    trip.passengers.add(passenger)
    
    # Create trip line
    trip_line, _ = TripLine.objects.get_or_create(
        trip=trip,
        origin_airport=jfk,
        destination_airport=lax,
        defaults={
            'crew_line': crew_line,
            'departure_time_local': datetime.now() + timedelta(days=1, hours=8),
            'departure_time_utc': datetime.now() + timedelta(days=1, hours=13),
            'arrival_time_local': datetime.now() + timedelta(days=1, hours=11),
            'arrival_time_utc': datetime.now() + timedelta(days=1, hours=16),
            'distance': Decimal('2475.00'),
            'flight_time': timedelta(hours=5, minutes=30),
            'ground_time': timedelta(hours=1),
            'passenger_leg': True,
            'created_by': admin_user
        }
    )
    
    print(f"✅ Created test data:")
    print(f"   Quote ID: {quote.id}")
    print(f"   Trip ID: {trip.id}")
    print(f"   Trip Number: {trip.trip_number}")
    
    return quote.id, trip.id

if __name__ == "__main__":
    quote_id, trip_id = create_test_data()
    print(f"\nTest data created successfully!")
    print(f"Quote ID: {quote_id}")
    print(f"Trip ID: {trip_id}")
