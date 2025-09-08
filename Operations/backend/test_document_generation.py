#!/usr/bin/env python
"""
Test script for document generation system
"""

import os
import sys
import django
from pathlib import Path

# Setup Django environment
sys.path.append(str(Path(__file__).parent))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from api.models import Trip
from utils.docgen.trip_document_generator import TripDocumentGenerator

def test_document_generation():
    """Test document generation for a trip"""
    # Get first available trip
    trip = Trip.objects.first()
    if not trip:
        print("No trips available for testing")
        return
    
    print(f"Testing document generation for Trip {trip.trip_number} (ID: {trip.id})")
    print(f"Trip type: {trip.type}")
    print(f"Has aircraft: {trip.aircraft is not None}")
    print(f"Has patient: {trip.patient is not None}")
    print(f"Has quote: {trip.quote is not None}")
    print(f"Trip lines count: {trip.trip_lines.count()}")
    print()
    
    # Create document generator
    generator = TripDocumentGenerator(str(trip.id))
    
    # Test data preparation methods
    print("=== Testing Data Preparation ===")
    try:
        trip_data = generator._prepare_trip_data()
        print(f"Trip data keys: {list(trip_data.keys())}")
        print(f"Trip number: {trip_data.get('trip_number')}")
        print(f"Aircraft tail: {trip_data['aircraft']['tail_number']}")
        print(f"Primary pilot: {trip_data['crew']['primary_pilot']}")
        print()
    except Exception as e:
        print(f"Error in trip data preparation: {e}")
        return
    
    # Test quote data if available
    quote_data = None
    if trip.quote:
        try:
            quote_data = generator._prepare_quote_data()
            print(f"Quote data keys: {list(quote_data.keys())}")
            print(f"Quoted amount: {quote_data.get('quoted_amount')}")
            print()
        except Exception as e:
            print(f"Error in quote data preparation: {e}")
    
    # Test patient data if available
    patient_data = None
    if trip.patient:
        try:
            patient_data = generator._prepare_patient_data()
            print(f"Patient data keys: {list(patient_data.keys())}")
            print(f"Patient name: {patient_data.get('patient_name')}")
            print()
        except Exception as e:
            print(f"Error in patient data preparation: {e}")
    
    # Test placeholder mappings
    print("=== Testing Placeholder Mappings ===")
    try:
        placeholders = generator._create_placeholder_mappings(
            trip_data, 
            quote_data if trip.quote else None, 
            patient_data
        )
        print(f"Total placeholders: {len(placeholders)}")
        
        # Show key placeholders
        key_placeholders = ['{{TRIP_NUMBER}}', '{{AIRCRAFT_TAIL}}', '{{PRIMARY_PILOT}}', '{{DEPARTURE_DATE}}']
        for placeholder in key_placeholders:
            print(f"{placeholder}: {placeholders.get(placeholder, 'NOT FOUND')}")
        print()
    except Exception as e:
        print(f"Error creating placeholder mappings: {e}")
        return
    
    # Test document generation
    print("=== Testing Document Generation ===")
    
    # Test GenDec (this should already work)
    if trip.trip_lines.exists():
        try:
            print("Generating GenDec document...")
            gendec_doc = generator._generate_gendec()
            if gendec_doc:
                print(f"✓ GenDec generated: {gendec_doc.filename}")
            else:
                print("✗ GenDec generation failed")
        except Exception as e:
            print(f"✗ GenDec generation error: {e}")
    
    # Test Customer Itinerary (newly implemented)
    try:
        print("Generating Customer Itinerary...")
        itinerary_doc = generator._generate_customer_itinerary()
        if itinerary_doc:
            print(f"✓ Customer Itinerary generated: {itinerary_doc.filename}")
        else:
            print("✗ Customer Itinerary generation failed")
    except Exception as e:
        print(f"✗ Customer Itinerary generation error: {e}")
    
    # Test Quote Form (if applicable)
    if trip.quote:
        try:
            print("Generating Quote Form...")
            quote_doc = generator._generate_quote_form()
            if quote_doc:
                print(f"✓ Quote Form generated: {quote_doc.filename}")
            else:
                print("✗ Quote Form generation failed")
        except Exception as e:
            print(f"✗ Quote Form generation error: {e}")
    
    # Test Handling Request
    try:
        print("Generating Handling Request...")
        handling_doc = generator._generate_handling_request()
        if handling_doc:
            print(f"✓ Handling Request generated: {handling_doc.filename}")
        else:
            print("✗ Handling Request generation failed")
    except Exception as e:
        print(f"✗ Handling Request generation error: {e}")
    
    print("\n=== Test Complete ===")

if __name__ == "__main__":
    test_document_generation()