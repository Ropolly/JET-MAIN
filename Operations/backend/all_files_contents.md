# Project Structure

The following is the structure of the project:

```
backend/
    debug_pdf_fields.py
    csv processor.py
    debug_itinerary_fields.py
    manage.py
    create_test_data.py
    prompt2.py
transactions/
    admin.py
    urls.py
    views.py
    models.py
    __init__.py
    processor.py
    apps.py
index/
    admin.py
    urls.py
    views.py
    models.py
    __init__.py
    apps.py
    serializers.py
utils/
    __init__.py
    paymentprocess/
        transactionkey.py
    schedulers/
        __init__.py
    webscraping/
        scrapers.py
        __init__.py
    services/
        __init__.py
        docuseal_service.py
    smtp/
        __init__.py
        email.py
api/
    timezone_utils.py
    admin.py
    middleware.py
    urls.py
    views.py
    models.py
    __init__.py
    tests.py
    permissions.py
    utils.py
    signals.py
    apps.py
    serializers.py
    contact_service.py
    external/
        airport.py
        aircraft.py
    tests/
        run_all_tests.py
        __init__.py
        test_patients.py
        test_transactions.py
        base_test.py
        test_documents.py
        test_passengers.py
        test_trips.py
        test_document_generation.py
        test_quotes.py
        test_crew_lines.py
        test_trip_lines.py
        test_userprofile.py
    migrations/
        0016_add_contract_model.py
        0009_fbo_email.py
        0007_contact_date_of_birth_contact_nationality_and_more.py
        0001_initial.py
        __init__.py
        0010_tripevent.py
        0017_add_authorize_net_trans_id_to_transaction.py
        0003_staff_staffrole_staffrolemembership_and_more.py
        0013_comment_and_more.py
        0006_alter_airport_iata_code_alter_airport_icao_code.py
        0002_trip_notes.py
        0004_rename_country_airport_iso_country_and_more.py
        0012_tripline_arrival_fbo_tripline_departure_fbo.py
        0015_document_contact_document_created_by_and_more.py
        0014_quote_payment_status_alter_quote_status.py
        0011_rename_airport_id_tripevent_airport_and_more.py
        0005_airport_airport_type.py
        0008_fbo_phone_fbo_phone_secondary.py
    management/
        __init__.py
        commands/
            seed_fbos.py
            seed_dev.py
            seed_test_data.py
            __init__.py
            check_trip_timezones.py
            setup_test_data.py
            remove_test_data.py
            seed_aircraft_and_staff.py
            seed_staff.py
            import_airports.py
documents/
    PDF/
        dcos/
    agreements/
        PDFS/
    templates/
        docs.py
        nosign_pdf/
        docs/
        docuseal_pdf/
        nosign_out/
backend/
    settings.py
    urls.py
    __init__.py
    asgi.py
    wsgi.py
    documents/
maintenance/
    admin.py
    urls.py
    views.py
    models.py
    __init__.py
    apps.py
    serializers.py
```


# File: debug_pdf_fields.py

```python
#!/usr/bin/env python
"""
Debug script to inspect PDF form fields and test field population.
This will help identify why PDFs are coming out empty.
"""

import os
import sys
from pathlib import Path

# Add the project root to Python path
sys.path.append(str(Path(__file__).parent))

def inspect_pdf_fields(pdf_path):
    """Inspect the form fields in a PDF to see what field names exist."""
    print(f"Inspecting PDF fields in: {pdf_path}")
    
    try:
        from pdfrw import PdfReader
        
        reader = PdfReader(pdf_path)
        print(f"PDF has {len(reader.pages)} pages")
        
        field_names = []
        for page_num, page in enumerate(reader.pages):
            print(f"\nPage {page_num + 1}:")
            if page.Annots:
                print(f"  Found {len(page.Annots)} annotations")
                for i, annotation in enumerate(page.Annots):
                    if annotation.T:  # Field name
                        field_name = annotation.T[1:-1]  # Remove parentheses
                        field_names.append(field_name)
                        print(f"    Field {i+1}: '{field_name}'")
                        
                        # Check if it has a value
                        if hasattr(annotation, 'V') and annotation.V:
                            print(f"      Current value: {annotation.V}")
                        else:
                            print(f"      Current value: (empty)")
            else:
                print("  No annotations found")
        
        return field_names
        
    except Exception as e:
        print(f"pdfrw inspection failed: {e}")
        
        # Try with pypdf
        try:
            from pypdf import PdfReader
            
            reader = PdfReader(pdf_path)
            print(f"PDF has {len(reader.pages)} pages")
            
            field_names = []
            if reader.get_form_text_fields():
                fields = reader.get_form_text_fields()
                print(f"Found {len(fields)} form fields:")
                for field_name, value in fields.items():
                    field_names.append(field_name)
                    print(f"  '{field_name}': '{value}'")
            else:
                print("No form fields found with pypdf")
            
            return field_names
            
        except Exception as e2:
            print(f"pypdf inspection also failed: {e2}")
            return []


def test_field_population():
    """Test populating a PDF with known field names."""
    print("\n" + "="*60)
    print("TESTING FIELD POPULATION")
    print("="*60)
    
    try:
        from documents.templates.docs import populate_pdf_with_fields
        
        # Test with Quote PDF
        template_path = 'documents/templates/nosign_pdf/Quote.pdf'
        output_path = 'documents/templates/nosign_out/debug_quote.pdf'
        
        if not Path(template_path).exists():
            print(f"Template not found: {template_path}")
            return False
        
        # Get actual field names from the PDF
        field_names = inspect_pdf_fields(template_path)
        
        if not field_names:
            print("No fields found - PDF might not have form fields")
            return False
        
        # Create test mapping using actual field names
        test_mapping = {}
        for field_name in field_names[:5]:  # Test first 5 fields
            test_mapping[field_name] = f"TEST_VALUE_{field_name}"
        
        print(f"\nTesting with mapping: {test_mapping}")
        
        # Ensure output directory exists
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        
        # Try to populate
        result = populate_pdf_with_fields(template_path, output_path, test_mapping)
        
        if result:
            print(f"✓ PDF populated successfully: {output_path}")
            
            # Verify the output has the values
            output_fields = inspect_pdf_fields(output_path)
            print(f"\nVerifying output PDF...")
            return True
        else:
            print("✗ PDF population failed")
            return False
            
    except Exception as e:
        print(f"Test failed: {e}")
        return False


def main():
    """Main debug function."""
    print("PDF FIELD DEBUG TOOL")
    print("="*60)
    
    # Check all template PDFs
    templates = [
        'documents/templates/nosign_pdf/Quote.pdf',
        'documents/templates/nosign_pdf/itin.pdf',
        'documents/templates/nosign_pdf/handling_request.pdf'
    ]
    
    for template in templates:
        if Path(template).exists():
            print(f"\n{'='*60}")
            print(f"ANALYZING: {template}")
            print(f"{'='*60}")
            inspect_pdf_fields(template)
        else:
            print(f"\n✗ Template not found: {template}")
    
    # Test field population
    test_field_population()


if __name__ == '__main__':
    main()

```


# File: csv processor.py

```python
import pandas as pd
import re

# Regex pattern to detect phone-like strings
phone_pattern = re.compile(
    r'(\(?\+?\d{1,3}\)?[\s.-]?\d{2,4}[\s.-]?\d{2,4}[\s.-]?\d{2,6})'
)

def extract_numbers(text):
    """Find all phone-like numbers in a text field."""
    if pd.isna(text):
        return []
    return phone_pattern.findall(str(text))

def process_row(row):
    numbers = []

    # Collect numbers from PHONE column
    numbers.extend(extract_numbers(row['PHONE']))

    # Collect numbers from Email column (sometimes contains numbers)
    numbers.extend(extract_numbers(row['Email']))

    # Deduplicate and keep order
    numbers = list(dict.fromkeys(numbers))

    # Assign cleaned numbers back
    row['PHONE'] = numbers[0] if numbers else ''
    row['PHONE2'] = numbers[1] if len(numbers) > 1 else ''

    # If email was a phone number, clear it
    if extract_numbers(row['Email']):
        row['Email'] = ''

    return row

def clean_csv(input_file, output_file):
    df = pd.read_csv(input_file, dtype=str)

    if 'PHONE2' not in df.columns:
        df['PHONE2'] = ''

    df = df.apply(process_row, axis=1)

    df.to_csv(output_file, index=False)
    print(f"Cleaned CSV written to {output_file}")

if __name__ == "__main__":
    clean_csv("FBO.csv", "FBO_clean.csv")

```


# File: debug_itinerary_fields.py

```python
#!/usr/bin/env python
"""
Debug script to find the exact field names for trip_number, trip_date, trip_type, tail_number in itinerary PDF.
"""

import os
import sys
from pathlib import Path

# Add the project root to Python path
sys.path.append(str(Path(__file__).parent))

def find_missing_fields():
    """Find the exact field names for the missing fields in itinerary PDF."""
    print("Searching for trip_number, trip_date, trip_type, tail_number fields in itinerary PDF...")
    
    try:
        from pdfrw import PdfReader
        
        template_path = 'documents/templates/nosign_pdf/itin.pdf'
        reader = PdfReader(template_path)
        
        all_fields = []
        for page_num, page in enumerate(reader.pages):
            print(f"\nPage {page_num + 1}:")
            if page.Annots:
                for i, annotation in enumerate(page.Annots):
                    if annotation.T:  # Field name
                        field_name = annotation.T[1:-1]  # Remove parentheses
                        all_fields.append(field_name)
                        
                        # Look for fields that might be our missing ones
                        field_lower = field_name.lower()
                        if any(keyword in field_lower for keyword in ['trip', 'tail', 'date', 'type', 'number']):
                            print(f"    POTENTIAL MATCH: '{field_name}'")
        
        print(f"\n{'='*60}")
        print("ALL FIELD NAMES IN ITINERARY PDF:")
        print(f"{'='*60}")
        
        for i, field in enumerate(all_fields, 1):
            print(f"{i:3d}. '{field}'")
        
        print(f"\n{'='*60}")
        print("SEARCHING FOR SPECIFIC PATTERNS:")
        print(f"{'='*60}")
        
        # Search for specific patterns
        patterns = {
            'trip_number': ['trip', 'number', 'trip_number', 'tripnumber'],
            'trip_date': ['date', 'trip_date', 'tripdate'],
            'trip_type': ['type', 'trip_type', 'triptype'],
            'tail_number': ['tail', 'tail_number', 'tailnumber', 'aircraft']
        }
        
        for missing_field, search_terms in patterns.items():
            print(f"\nLooking for {missing_field}:")
            matches = []
            for field in all_fields:
                field_lower = field.lower()
                for term in search_terms:
                    if term in field_lower:
                        matches.append(field)
                        break
            
            if matches:
                print(f"  Possible matches: {matches}")
            else:
                print(f"  No matches found")
        
        return all_fields
        
    except Exception as e:
        print(f"Error: {e}")
        return []


def test_field_mapping():
    """Test if our current field mapping includes the basic fields."""
    print(f"\n{'='*60}")
    print("CHECKING CURRENT FIELD MAPPING:")
    print(f"{'='*60}")
    
    try:
        from documents.templates.docs import ItineraryData, populate_itinerary_pdf
        
        # Check what fields we're currently mapping
        template_path = 'documents/templates/nosign_pdf/itin.pdf'
        output_path = 'documents/templates/nosign_out/debug_itinerary_mapping.pdf'
        
        # Create minimal test data
        test_data = ItineraryData(
            trip_number='TEST-TRIP-123',
            tail_number='N123TEST',
            trip_date='2025-01-20',
            trip_type='Medical Test'
        )
        
        # Ensure output directory exists
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        
        # Try to populate
        result = populate_itinerary_pdf(template_path, output_path, test_data)
        
        if result:
            print("✓ PDF generation successful")
            
            # Check what got populated
            from debug_pdf_fields import inspect_pdf_fields
            print("\nChecking populated fields:")
            inspect_pdf_fields(output_path)
        else:
            print("✗ PDF generation failed")
            
    except Exception as e:
        print(f"Error testing field mapping: {e}")


def main():
    """Main debug function."""
    print("DEBUGGING MISSING ITINERARY FIELDS")
    print("=" * 60)
    
    find_missing_fields()
    test_field_mapping()


if __name__ == '__main__':
    main()

```


# File: manage.py

```python
#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()

```


# File: create_test_data.py

```python
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

```


# File: prompt2.py

```python
import os

def save_files_to_md(output_md_file='all_files_contents.md'):
    root_dir = os.path.dirname(os.path.abspath(__file__))  # Root set to the script's location

    def generate_structure():
        structure = []
        for dirpath, dirnames, filenames in os.walk(root_dir):
            # Skip 'venv', '__pycache__', or any hidden directories
            dirnames[:] = [d for d in dirnames if d not in ('venv', '__pycache__') and not d.startswith('.')]
            
            # Build the relative path and indentation for the directory
            rel_dir = os.path.relpath(dirpath, root_dir)
            indent = rel_dir.count(os.sep)
            structure.append('    ' * indent + f'{os.path.basename(dirpath)}/')
            
            for filename in filenames:
                if filename.endswith('.py'):
                    structure.append('    ' * (indent + 1) + filename)
        
        return '\n'.join(structure)

    with open(output_md_file, 'w') as md_file:
        # Write the project structure description at the top
        md_file.write("# Project Structure\n\n")
        md_file.write("The following is the structure of the project:\n\n")
        md_file.write("```\n")
        md_file.write(generate_structure())
        md_file.write("\n```\n")

        # Now iterate through the files to capture code content
        for dirpath, dirnames, filenames in os.walk(root_dir):
            # Skip 'venv', '__pycache__', or any hidden directories
            dirnames[:] = [d for d in dirnames if d not in ('venv', '__pycache__') and not d.startswith('.')]
            
            for filename in filenames:
                if filename.endswith('.py'):
                    file_path = os.path.join(dirpath, filename)
                    relative_path = os.path.relpath(file_path, root_dir)
                    
                    # Add file header with file path
                    md_file.write(f"\n\n# File: {relative_path}\n\n")
                    md_file.write("```python\n")
                    
                    # Write the file's contents
                    with open(file_path, 'r') as f:
                        md_file.write(f.read())
                    
                    md_file.write("\n```\n")

    print(f"All .py files and project structure have been copied to {output_md_file}")

if __name__ == "__main__":
    save_files_to_md()


```


# File: transactions/admin.py

```python
from django.contrib import admin

# Register your models here.
# No models to register for this app as it only handles API endpoints

```


# File: transactions/urls.py

```python
from django.urls import path
from . import views

urlpatterns = [
    path('send/card/', views.send_card_transaction, name='send-card-transaction'),
    path('send/ach/', views.send_ach_transaction, name='send-ach-transaction'),
]

```


# File: transactions/views.py

```python
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .processor import process_card_transaction, process_ach_transaction
from api.models import Transaction, Quote
from api.signals import set_current_user
from api.utils import track_creation, track_modification


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def send_card_transaction(request):
    """
    Process card transaction through Authorize.Net
    """
    # Set current user for modification tracking
    set_current_user(request.user)
    
    transaction_data = request.data
    
    # Call the processing function
    result = process_card_transaction(
        amount=transaction_data.get('amount'),
        card_number=transaction_data.get('cardNumber'),
        expiration_date=transaction_data.get('expirationDate'),
        card_code=transaction_data.get('cardCode'),
        ref_id=transaction_data.get('refId'),
        bill_to=transaction_data.get('billTo'),
        ship_to=transaction_data.get('shipTo'),
        customer_ip=request.META.get('REMOTE_ADDR', '127.0.0.1')
    )
    
    # Check if payment was successful (response code 1)
    transaction_response = result.get('transactionResponse', {})
    messages = transaction_response.get('messages', [])
    message = messages[0] if messages else {}
    
    if message.get('code') == '1':  # Approved
        # Extract transaction details
        trans_id = transaction_response.get('transId', '')
        amount = transaction_data.get('amount', '0')
        customer_email = transaction_data.get('billTo', {}).get('email', '')
        
        # Create transaction record
        transaction = Transaction.objects.create(
            amount=amount,
            payment_method='credit_card',
            payment_status='completed',
            email=customer_email,
            authorize_net_trans_id=trans_id
        )
        
        # Track transaction creation
        track_creation(transaction, request.user)
        
        # Link to quote if quote_id provided
        quote_id = transaction_data.get('quote_id')
        if quote_id:
            try:
                quote = Quote.objects.get(id=quote_id)
                
                # Track the quote modification before changes
                old_payment_status = quote.payment_status
                old_total_paid = quote.get_total_paid()
                
                # Add transaction to quote
                quote.transactions.add(transaction)
                quote.update_payment_status()
                
                # Track the payment received
                track_modification(
                    quote, 
                    'payment_received', 
                    f'${old_total_paid or 0}', 
                    f'${quote.get_total_paid()}',
                    request.user
                )
                
                # Track payment status change if it changed
                if old_payment_status != quote.payment_status:
                    track_modification(
                        quote,
                        'payment_status',
                        old_payment_status,
                        quote.payment_status,
                        request.user
                    )
                
                result['quote_updated'] = True
                result['new_payment_status'] = quote.payment_status
                result['remaining_balance'] = str(quote.get_remaining_balance())
            except Quote.DoesNotExist:
                pass
        
        # Add our custom fields to response
        result['transaction_created'] = True
        result['transaction_id'] = str(transaction.id)
    
    return Response(result, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def send_ach_transaction(request):
    """
    Process ACH transaction through Authorize.Net
    """
    # Set current user for modification tracking
    set_current_user(request.user)
    
    transaction_data = request.data
    
    # Call the processing function
    result = process_ach_transaction(
        amount=transaction_data.get('amount'),
        account_type=transaction_data.get('accountType', 'checking'),
        routing_number=transaction_data.get('routingNumber'),
        account_number=transaction_data.get('accountNumber'),
        name_on_account=transaction_data.get('nameOnAccount'),
        echeck_type=transaction_data.get('echeckType', 'WEB'),
        bank_name=transaction_data.get('bankName', ''),
        ref_id=transaction_data.get('refId'),
        bill_to=transaction_data.get('billTo'),
        ship_to=transaction_data.get('shipTo'),
        customer_ip=request.META.get('REMOTE_ADDR', '127.0.0.1')
    )
    
    # Check if payment was successful (response code 1)
    transaction_response = result.get('transactionResponse', {})
    messages = transaction_response.get('messages', [])
    message = messages[0] if messages else {}
    
    if message.get('code') == '1':  # Approved
        # Extract transaction details
        trans_id = transaction_response.get('transId', '')
        amount = transaction_data.get('amount', '0')
        customer_email = transaction_data.get('billTo', {}).get('email', '')
        
        # Create transaction record
        transaction = Transaction.objects.create(
            amount=amount,
            payment_method='ACH',
            payment_status='completed',
            email=customer_email,
            authorize_net_trans_id=trans_id
        )
        
        # Track transaction creation
        track_creation(transaction, request.user)
        
        # Link to quote if quote_id provided
        quote_id = transaction_data.get('quote_id')
        if quote_id:
            try:
                quote = Quote.objects.get(id=quote_id)
                
                # Track the quote modification before changes
                old_payment_status = quote.payment_status
                old_total_paid = quote.get_total_paid()
                
                # Add transaction to quote
                quote.transactions.add(transaction)
                quote.update_payment_status()
                
                # Track the payment received
                track_modification(
                    quote, 
                    'payment_received', 
                    f'${old_total_paid or 0}', 
                    f'${quote.get_total_paid()}',
                    request.user
                )
                
                # Track payment status change if it changed
                if old_payment_status != quote.payment_status:
                    track_modification(
                        quote,
                        'payment_status',
                        old_payment_status,
                        quote.payment_status,
                        request.user
                    )
                
                result['quote_updated'] = True
                result['new_payment_status'] = quote.payment_status
                result['remaining_balance'] = str(quote.get_remaining_balance())
            except Quote.DoesNotExist:
                pass
        
        # Add our custom fields to response
        result['transaction_created'] = True
        result['transaction_id'] = str(transaction.id)
    
    return Response(result, status=status.HTTP_200_OK)


if __name__ == '__main__':
    """
    Test script for transaction processing functions
    
    To run this test:
    1. Set environment variables:
       export AUTHORIZE_NET_LOGIN_ID="your_login_id"
       export AUTHORIZE_NET_TRANSACTION_KEY="your_transaction_key"
    
    2. Run: python transactions/views.py
    """
    DOT_ENV_PATH = "/home/ropolly/projects/work/JET-MAIN/.env"
    from dotenv import load_dotenv
    load_dotenv()
    
    print("Testing Transaction Processing Functions")
    print("=" * 50)
    
    # Check if environment variables are set
    login_id = os.getenv('AUTHORIZE_NET_LOGIN_ID')
    transaction_key = os.getenv('AUTHORIZE_NET_TRANSACTION_KEY')
    
    if login_id and transaction_key:
        print(f"✓ Environment variables configured:")
        print(f"  AUTHORIZE_NET_LOGIN_ID: {login_id[:4]}***")
        print(f"  AUTHORIZE_NET_TRANSACTION_KEY: {transaction_key[:4]}***")
    else:
        print("⚠ Environment variables not set:")
        print("  Please set AUTHORIZE_NET_LOGIN_ID and AUTHORIZE_NET_TRANSACTION_KEY")
        print("  Skipping actual API tests...")
    
    print("\n" + "=" * 50)
    print("Testing Card Transaction Function")
    print("=" * 50)
    
    # Test card transaction function
    card_result = process_card_transaction(
        amount='10.00',
        card_number='4111111111111111',  # Test card number
        expiration_date='1225',  # MMYY format
        card_code='123',
        ref_id='test_card_001',
        bill_to={
            'firstName': 'John',
            'lastName': 'Doe',
            'address': '123 Test St',
            'city': 'Test City',
            'state': 'CA',
            'zip': '12345',
            'country': 'US'
        },
        customer_ip='127.0.0.1'
    )
    
    print("Card Transaction Result:")
    print(json.dumps(card_result, indent=2))
    
    print("\n" + "=" * 50)
    print("Testing ACH Transaction Function")
    print("=" * 50)
    
    # Test ACH transaction function
    ach_result = process_ach_transaction(
        amount='25.00',
        account_type='checking',
        routing_number='121042882',  # Test routing number
        account_number='123456789',  # Test account number
        name_on_account='John Doe',
        echeck_type='WEB',
        bank_name='Test Bank',
        ref_id='test_ach_001',
        bill_to={
            'firstName': 'John',
            'lastName': 'Doe',
            'address': '123 Test St',
            'city': 'Test City',
            'state': 'CA',
            'zip': '12345',
            'country': 'US'
        },
        customer_ip='127.0.0.1'
    )
    
    print("ACH Transaction Result:")
    print(json.dumps(ach_result, indent=2))
    
    print("\n" + "=" * 50)
    print("Test Summary")
    print("=" * 50)
    print("Functions tested:")
    print("- process_card_transaction()")
    print("- process_ach_transaction()")
    print("\nEndpoints available:")
    print("- POST /transactions/send/card/")
    print("- POST /transactions/send/ach/")
    print("\nNote: Endpoints require JWT authentication")

```


# File: transactions/models.py

```python
from django.db import models

# Create your models here.
# No models needed for this app as it only handles API endpoints for transaction processing

```


# File: transactions/__init__.py

```python

```


# File: transactions/processor.py

```python
import json
import os
import requests
from django.conf import settings


def process_card_transaction(amount, card_number, expiration_date, card_code, ref_id=None, bill_to=None, ship_to=None, customer_ip='127.0.0.1'):
    """
    Process a credit card transaction through Authorize.Net
    
    Args:
        amount (str): Transaction amount
        card_number (str): Credit card number
        expiration_date (str): Card expiration date (MMYY format)
        card_code (str): CVV/CVC code
        ref_id (str, optional): Reference ID for the transaction
        bill_to (dict, optional): Billing address information
        ship_to (dict, optional): Shipping address information
        customer_ip (str, optional): Customer IP address
    
    Returns:
        dict: Response from Authorize.Net with added authorize_net_response_code
    """
    # Get Authorize.Net API credentials from Django settings
    api_login_id = settings.AUTHORIZE_NET_LOGIN_ID
    transaction_key = settings.AUTHORIZE_NET_TRANSACTION_KEY
    
    if not api_login_id or not transaction_key:
        return {
            'error': 'Authorize.Net credentials not configured',
            'details': 'Missing AUTHORIZE_NET_LOGIN_ID or AUTHORIZE_NET_TRANSACTION_KEY environment variables',
            'authorize_net_response_code': 'CONFIG_ERROR'
        }
    
    # Prepare the Authorize.Net API request
    auth_net_data = {
        "createTransactionRequest": {
            "merchantAuthentication": {
                "name": api_login_id,
                "transactionKey": transaction_key
            },
            "refId": ref_id.replace('quote_', '').replace('-', '')[:8].upper() if ref_id and 'quote_' in ref_id else (ref_id[:8] if ref_id else '12345678'),
            "transactionRequest": {
                "transactionType": "authCaptureTransaction",
                "amount": amount,
                "payment": {
                    "creditCard": {
                        "cardNumber": card_number,
                        "expirationDate": expiration_date,
                        "cardCode": card_code
                    }
                },
                "billTo": {k: v for k, v in (bill_to or {}).items() if k in ['firstName', 'lastName', 'company', 'address', 'city', 'state', 'zip', 'country']},
                "shipTo": ship_to or {},
                "customerIP": customer_ip
            }
        }
    }
    
    try:
        # Make request to Authorize.Net API
        # Use sandbox URL for testing, production URL for live transactions
        api_url = "https://apitest.authorize.net/xml/v1/request.api"  # Sandbox
        # api_url = "https://api.authorize.net/xml/v1/request.api"  # Production
        
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        
        response = requests.post(api_url, json=auth_net_data, headers=headers, timeout=30)
        
        # Parse Authorize.Net response - handle UTF-8 BOM
        response_text = response.text
        if response_text.startswith('\ufeff'):
            response_text = response_text[1:]  # Remove BOM
        
        auth_net_response = json.loads(response_text)
        
        # Add Authorize.Net response code to the response
        response_data = auth_net_response
        if 'transactionResponse' in auth_net_response:
            response_data['authorize_net_response_code'] = auth_net_response['transactionResponse'].get('responseCode')
        else:
            response_data['authorize_net_response_code'] = 'ERROR'
        
        return response_data
        
    except requests.exceptions.RequestException as e:
        return {
            'error': 'Failed to communicate with Authorize.Net',
            'details': str(e),
            'authorize_net_response_code': 'NETWORK_ERROR'
        }
    
    except Exception as e:
        return {
            'error': 'Transaction processing failed',
            'details': str(e),
            'authorize_net_response_code': 'PROCESSING_ERROR'
        }


def process_ach_transaction(amount, account_type, routing_number, account_number, name_on_account, 
                           echeck_type='WEB', bank_name='', ref_id=None, bill_to=None, ship_to=None, customer_ip='127.0.0.1'):
    """
    Process an ACH/eCheck transaction through Authorize.Net
    
    Args:
        amount (str): Transaction amount
        account_type (str): 'checking' or 'savings'
        routing_number (str): Bank routing number
        account_number (str): Bank account number
        name_on_account (str): Name on the bank account
        echeck_type (str, optional): Type of eCheck (WEB, PPD, CCD, etc.)
        bank_name (str, optional): Name of the bank
        ref_id (str, optional): Reference ID for the transaction
        bill_to (dict, optional): Billing address information
        ship_to (dict, optional): Shipping address information
        customer_ip (str, optional): Customer IP address
    
    Returns:
        dict: Response from Authorize.Net with added authorize_net_response_code
    """
    # Get Authorize.Net API credentials from Django settings
    api_login_id = settings.AUTHORIZE_NET_LOGIN_ID
    transaction_key = settings.AUTHORIZE_NET_TRANSACTION_KEY
    
    if not api_login_id or not transaction_key:
        return {
            'error': 'Authorize.Net credentials not configured',
            'details': 'Missing AUTHORIZE_NET_LOGIN_ID or AUTHORIZE_NET_TRANSACTION_KEY environment variables',
            'authorize_net_response_code': 'CONFIG_ERROR'
        }
    
    # Prepare the Authorize.Net API request for ACH/eCheck
    auth_net_data = {
        "createTransactionRequest": {
            "merchantAuthentication": {
                "name": api_login_id,
                "transactionKey": transaction_key
            },
            "refId": ref_id.replace('quote_', '').replace('-', '')[:8].upper() if ref_id and 'quote_' in ref_id else (ref_id[:8] if ref_id else '12345678'),
            "transactionRequest": {
                "transactionType": "authCaptureTransaction",
                "amount": amount,
                "payment": {
                    "bankAccount": {
                        "accountType": account_type,
                        "routingNumber": routing_number,
                        "accountNumber": account_number,
                        "nameOnAccount": name_on_account,
                        "echeckType": echeck_type,
                        "bankName": bank_name
                    }
                },
                "billTo": {k: v for k, v in (bill_to or {}).items() if k in ['firstName', 'lastName', 'company', 'address', 'city', 'state', 'zip', 'country']},
                "shipTo": ship_to or {},
                "customerIP": customer_ip
            }
        }
    }
    
    try:
        # Make request to Authorize.Net API
        # Use sandbox URL for testing, production URL for live transactions
        api_url = "https://apitest.authorize.net/xml/v1/request.api"  # Sandbox
        # api_url = "https://api.authorize.net/xml/v1/request.api"  # Production
        
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        
        response = requests.post(api_url, json=auth_net_data, headers=headers, timeout=30)
        
        # Parse Authorize.Net response - handle UTF-8 BOM
        response_text = response.text
        if response_text.startswith('\ufeff'):
            response_text = response_text[1:]  # Remove BOM
        
        auth_net_response = json.loads(response_text)
        
        # Add Authorize.Net response code to the response
        response_data = auth_net_response
        if 'transactionResponse' in auth_net_response:
            response_data['authorize_net_response_code'] = auth_net_response['transactionResponse'].get('responseCode')
        else:
            response_data['authorize_net_response_code'] = 'ERROR'
        
        return response_data
        
    except requests.exceptions.RequestException as e:
        return {
            'error': 'Failed to communicate with Authorize.Net',
            'details': str(e),
            'authorize_net_response_code': 'NETWORK_ERROR'
        }
    
    except Exception as e:
        return {
            'error': 'Transaction processing failed',
            'details': str(e),
            'authorize_net_response_code': 'PROCESSING_ERROR'
        }


if __name__ == '__main__':
    """
    Test script for transaction processing functions
    
    To run this test:
    1. Set environment variables:
       export AUTHORIZE_NET_LOGIN_ID="your_login_id"
       export AUTHORIZE_NET_TRANSACTION_KEY="your_transaction_key"
    
    2. Run: python transactions/processor.py
    """
    # Load environment variables from .env file if available
    try:
        from dotenv import load_dotenv
        load_dotenv("/home/ropolly/projects/work/JET-MAIN/.env")
    except ImportError:
        print("python-dotenv not installed, using system environment variables")
    
    print("Testing Transaction Processing Functions")
    print("=" * 50)
    
    # Check if environment variables are set
    login_id = os.getenv('AUTHORIZE_NET_LOGIN_ID')
    transaction_key = os.getenv('AUTHORIZE_NET_TRANSACTION_KEY')
    
    if login_id and transaction_key:
        print(f"✓ Environment variables configured:")
        print(f"  AUTHORIZE_NET_LOGIN_ID: {login_id[:4]}***")
        print(f"  AUTHORIZE_NET_TRANSACTION_KEY: {transaction_key[:4]}***")
    else:
        print("⚠ Environment variables not set:")
        print("  Please set AUTHORIZE_NET_LOGIN_ID and AUTHORIZE_NET_TRANSACTION_KEY")
        print("  Continuing with test (will show CONFIG_ERROR)...")
    
    print("\n" + "=" * 50)
    print("Testing Card Transaction Function")
    print("=" * 50)
    
    # Test card transaction function
    card_result = process_card_transaction(
        amount='10.00',
        card_number='4111111111111111',  # Test card number
        expiration_date='1225',  # MMYY format
        card_code='123',
        ref_id='test_card_001',
        bill_to={
            'firstName': 'John',
            'lastName': 'Doe',
            'address': '123 Test St',
            'city': 'Test City',
            'state': 'CA',
            'zip': '12345',
            'country': 'US'
        },
        customer_ip='127.0.0.1'
    )
    
    print("Card Transaction Result:")
    print(json.dumps(card_result, indent=2))
    
    print("\n" + "=" * 50)
    print("Testing ACH Transaction Function")
    print("=" * 50)
    
    # Test ACH transaction function
    ach_result = process_ach_transaction(
        amount='25.00',
        account_type='checking',
        routing_number='121042882',  # Test routing number
        account_number='123456789',  # Test account number
        name_on_account='John Doe',
        echeck_type='WEB',
        bank_name='Test Bank',
        ref_id='test_ach_001',
        bill_to={
            'firstName': 'John',
            'lastName': 'Doe',
            'address': '123 Test St',
            'city': 'Test City',
            'state': 'CA',
            'zip': '12345',
            'country': 'US'
        },
        customer_ip='127.0.0.1'
    )
    
    print("ACH Transaction Result:")
    print(json.dumps(ach_result, indent=2))
    
    print("\n" + "=" * 50)
    print("Test Summary")
    print("=" * 50)
    print("Functions tested:")
    print("- process_card_transaction()")
    print("- process_ach_transaction()")
    print("\nTo use in Django:")
    print("from transactions.processor import process_card_transaction, process_ach_transaction")

```


# File: transactions/apps.py

```python
from django.apps import AppConfig


class TransactionsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'transactions'

```


# File: index/admin.py

```python
from django.contrib import admin
from .models import IndexPage

admin.site.register(IndexPage)

```


# File: index/urls.py

```python
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import IndexPageViewSet

router = DefaultRouter()
router.register(r'pages', IndexPageViewSet)

urlpatterns = [
    path('', include(router.urls)),
]

```


# File: index/views.py

```python
from rest_framework import viewsets
from .models import IndexPage
from .serializers import IndexPageSerializer


class IndexPageViewSet(viewsets.ModelViewSet):
    queryset = IndexPage.objects.all()
    serializer_class = IndexPageSerializer
    lookup_field = 'slug'

```


# File: index/models.py

```python
from django.db import models


class IndexPage(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    slug = models.SlugField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title

```


# File: index/__init__.py

```python


```


# File: index/apps.py

```python
from django.apps import AppConfig


class IndexConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'index'

```


# File: index/serializers.py

```python
from rest_framework import serializers
from .models import IndexPage


class IndexPageSerializer(serializers.ModelSerializer):
    class Meta:
        model = IndexPage
        fields = '__all__'

```


# File: utils/__init__.py

```python


```


# File: utils/paymentprocess/transactionkey.py

```python
import requests



```


# File: utils/schedulers/__init__.py

```python


```


# File: utils/webscraping/scrapers.py

```python
import requests
from bs4 import BeautifulSoup
import logging

logger = logging.getLogger(__name__)

class AirportDataScraper:
    """
    Scraper for fetching airport data from public sources
    """
    
    def __init__(self, base_url="https://www.airport-data.com"):
        self.base_url = base_url
        self.session = requests.Session()
        
    def get_airport_info(self, airport_code):
        """
        Fetch information about a specific airport by its IATA code
        """
        try:
            url = f"{self.base_url}/airports/{airport_code}"
            response = self.session.get(url)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Extract airport data (this is a simplified example)
            airport_data = {
                'code': airport_code,
                'name': soup.find('h1').text.strip() if soup.find('h1') else None,
                'location': self._extract_location(soup),
                'elevation': self._extract_elevation(soup),
                'runways': self._extract_runways(soup)
            }
            
            return airport_data
            
        except Exception as e:
            logger.error(f"Error fetching airport data for {airport_code}: {str(e)}")
            return None
    
    def _extract_location(self, soup):
        # Implementation would depend on the actual website structure
        return "Location data extraction placeholder"
    
    def _extract_elevation(self, soup):
        # Implementation would depend on the actual website structure
        return "Elevation data extraction placeholder"
    
    def _extract_runways(self, soup):
        # Implementation would depend on the actual website structure
        return ["Runway data extraction placeholder"]


class WeatherDataScraper:
    """
    Scraper for fetching weather data for flight planning
    """
    
    def __init__(self, base_url="https://aviationweather.gov"):
        self.base_url = base_url
        self.session = requests.Session()
    
    def get_metar(self, airport_code):
        """
        Fetch METAR (Meteorological Aerodrome Report) for a specific airport
        """
        try:
            url = f"{self.base_url}/metar/data?ids={airport_code}&format=raw"
            response = self.session.get(url)
            response.raise_for_status()
            
            # Parse the response to extract METAR data
            return response.text.strip()
            
        except Exception as e:
            logger.error(f"Error fetching METAR for {airport_code}: {str(e)}")
            return None
    
    def get_taf(self, airport_code):
        """
        Fetch TAF (Terminal Aerodrome Forecast) for a specific airport
        """
        try:
            url = f"{self.base_url}/taf/data?ids={airport_code}&format=raw"
            response = self.session.get(url)
            response.raise_for_status()
            
            # Parse the response to extract TAF data
            return response.text.strip()
            
        except Exception as e:
            logger.error(f"Error fetching TAF for {airport_code}: {str(e)}")
            return None

```


# File: utils/webscraping/__init__.py

```python


```


# File: utils/services/__init__.py

```python

```


# File: utils/services/docuseal_service.py

```python
"""
DocuSeal API integration service for managing document signing workflows.
"""
import requests
import logging
from typing import Dict, List, Optional, Any
from django.conf import settings
from django.utils import timezone
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


class DocuSealAPIError(Exception):
    """Custom exception for DocuSeal API errors."""
    pass


class DocuSealService:
    """
    Service class for integrating with DocuSeal API.
    Handles template creation, submission management, and webhook processing.
    """
    
    def __init__(self):
        self.api_key = getattr(settings, 'DOCUSEAL_API_KEY', None)
        self.base_url = getattr(settings, 'DOCUSEAL_BASE_URL', 'https://api.docuseal.com')
        
        if not self.api_key:
            logger.error("DocuSeal API key not configured")
            raise DocuSealAPIError("DocuSeal API key not configured")
    
    def _get_headers(self) -> Dict[str, str]:
        """Get standard headers for DocuSeal API requests."""
        return {
            'X-Auth-Token': self.api_key,
            'Content-Type': 'application/json'
        }
    
    def _make_request(
        self, 
        method: str, 
        endpoint: str, 
        data: Optional[Dict] = None, 
        params: Optional[Dict] = None
    ) -> Dict[str, Any]:
        """
        Make HTTP request to DocuSeal API with error handling.
        
        Args:
            method: HTTP method (GET, POST, PUT, DELETE)
            endpoint: API endpoint path
            data: Request body data
            params: URL query parameters
            
        Returns:
            Dict containing API response data
            
        Raises:
            DocuSealAPIError: If API request fails
        """
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        
        try:
            response = requests.request(
                method=method,
                url=url,
                headers=self._get_headers(),
                json=data,
                params=params,
                timeout=30
            )
            
            # Log the response for debugging
            logger.info(f"DocuSeal API {method} {url} -> {response.status_code}")
            
            if not response.ok:
                error_details = ""
                try:
                    error_data = response.json()
                    error_details = f" - {error_data}"
                except:
                    error_details = f" - {response.text}"
                
                error_msg = f"DocuSeal API request failed: {response.status_code} {response.reason}{error_details}"
                logger.error(error_msg)
                raise DocuSealAPIError(error_msg)
            
            # Handle empty responses
            if response.status_code == 204:
                return {}
            
            return response.json()
            
        except requests.exceptions.RequestException as e:
            error_msg = f"DocuSeal API request failed: {str(e)}"
            logger.error(error_msg)
            raise DocuSealAPIError(error_msg) from e
        except ValueError as e:
            error_msg = f"Failed to parse DocuSeal API response: {str(e)}"
            logger.error(error_msg)
            raise DocuSealAPIError(error_msg) from e
    
    def create_template_from_html(
        self, 
        name: str, 
        html_content: str, 
        fields: List[Dict] = None
    ) -> Dict[str, Any]:
        """
        Create a DocuSeal template from HTML content.
        
        Args:
            name: Template name
            html_content: HTML content for the template
            fields: List of form fields for the template
            
        Returns:
            Dict containing template information including template ID
        """
        data = {
            'name': name,
            'html': html_content
        }
        
        if fields:
            data['fields'] = fields
        
        logger.info(f"Creating DocuSeal template: {name}")
        return self._make_request('POST', '/templates', data=data)
    
    def create_template_from_pdf(
        self, 
        name: str, 
        pdf_content: bytes, 
        filename: str
    ) -> Dict[str, Any]:
        """
        Create a DocuSeal template from PDF content.
        
        Args:
            name: Template name
            pdf_content: PDF file content as bytes
            filename: Original filename
            
        Returns:
            Dict containing template information including template ID
        """
        # For PDF uploads, we need to use multipart/form-data
        files = {
            'file': (filename, pdf_content, 'application/pdf')
        }
        
        form_data = {
            'name': name
        }
        
        url = f"{self.base_url}/templates"
        
        try:
            response = requests.post(
                url=url,
                headers={'X-Auth-Token': self.api_key},
                files=files,
                data=form_data,
                timeout=30
            )
            
            response.raise_for_status()
            logger.info(f"Created DocuSeal template from PDF: {name}")
            return response.json()
            
        except requests.exceptions.RequestException as e:
            error_msg = f"Failed to upload PDF template: {str(e)}"
            logger.error(error_msg)
            raise DocuSealAPIError(error_msg) from e
    
    def create_submission(
        self,
        template_id: str,
        submitters: List[Dict[str, Any]],
        send_email: bool = True,
        completed_redirect_url: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Create a submission (signature request) from a template.
        
        Args:
            template_id: DocuSeal template ID
            submitters: List of submitter information (with fields as dict)
            send_email: Whether to send email notifications
            completed_redirect_url: URL to redirect after completion
            
        Returns:
            Dict containing submission information including submission ID
        """
        # Convert submitters format - DocuSeal expects fields as array of objects
        formatted_submitters = []
        for submitter in submitters:
            formatted_submitter = {
                'name': submitter['name'],
                'email': submitter['email']
            }
            
            # Add role if provided
            if 'role' in submitter:
                formatted_submitter['role'] = submitter['role']
            
            # Convert fields dict to array format expected by DocuSeal
            if 'fields' in submitter and submitter['fields']:
                formatted_submitter['fields'] = [
                    {'name': field_name, 'default_value': field_value}
                    for field_name, field_value in submitter['fields'].items()
                    if field_value  # Only include fields with values
                ]
            else:
                formatted_submitter['fields'] = []
            
            formatted_submitters.append(formatted_submitter)
        
        data = {
            'template_id': int(template_id),
            'submitters': formatted_submitters,
            'send_email': send_email
        }
        
        if completed_redirect_url:
            data['completed_redirect_url'] = completed_redirect_url
        
        logger.info(f"Creating DocuSeal submission for template: {template_id}")
        logger.info(f"Formatted submission data: {data}")
        
        try:
            return self._make_request('POST', '/submissions', data=data)
        except Exception as e:
            logger.error(f"Submission creation failed. Data sent: {data}")
            raise e
    
    def get_submission(self, submission_id: str) -> Dict[str, Any]:
        """
        Get submission details by ID.
        
        Args:
            submission_id: DocuSeal submission ID
            
        Returns:
            Dict containing submission details and status
        """
        logger.info(f"Fetching DocuSeal submission: {submission_id}")
        return self._make_request('GET', f'/submissions/{submission_id}')
    
    def list_submissions(
        self, 
        template_id: Optional[str] = None,
        limit: int = 100,
        after: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        List submissions with optional filtering.
        
        Args:
            template_id: Filter by template ID
            limit: Number of submissions to return
            after: Pagination cursor
            
        Returns:
            Dict containing list of submissions and pagination info
        """
        params = {'limit': limit}
        
        if template_id:
            params['template_id'] = template_id
        if after:
            params['after'] = after
        
        return self._make_request('GET', '/submissions', params=params)
    
    def get_submission_documents(self, submission_id: str) -> bytes:
        """
        Download completed/signed documents for a submission.
        
        Args:
            submission_id: DocuSeal submission ID
            
        Returns:
            PDF document content as bytes
        """
        url = f"{self.base_url}/submissions/{submission_id}/documents"
        
        try:
            response = requests.get(
                url=url,
                headers={'X-Auth-Token': self.api_key},
                timeout=30
            )
            
            response.raise_for_status()
            logger.info(f"Downloaded documents for submission: {submission_id}")
            return response.content
            
        except requests.exceptions.RequestException as e:
            error_msg = f"Failed to download submission documents: {str(e)}"
            logger.error(error_msg)
            raise DocuSealAPIError(error_msg) from e
    
    def archive_submission(self, submission_id: str) -> Dict[str, Any]:
        """
        Archive a submission.
        
        Args:
            submission_id: DocuSeal submission ID
            
        Returns:
            Dict containing archived submission info
        """
        logger.info(f"Archiving DocuSeal submission: {submission_id}")
        return self._make_request('DELETE', f'/submissions/{submission_id}')
    
    def process_webhook_event(self, webhook_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process incoming webhook event from DocuSeal.
        
        Args:
            webhook_data: Webhook payload from DocuSeal
            
        Returns:
            Dict containing processed event information
        """
        event_type = webhook_data.get('event_type')
        submission_data = webhook_data.get('data', {})
        submission_id = submission_data.get('id')
        
        logger.info(f"Processing DocuSeal webhook: {event_type} for submission {submission_id}")
        
        return {
            'event_type': event_type,
            'submission_id': submission_id,
            'submission_data': submission_data,
            'processed_at': timezone.now().isoformat()
        }
    
    def create_contract_fields_mapping(
        self, 
        contract_type: str,
        trip_data: Dict, 
        trip_lines_data: List[Dict] = None,
        contact_data: Dict = None, 
        patient_data: Dict = None,
        passengers_data: List[Dict] = None,
        quote_data: Dict = None
    ) -> Dict[str, Any]:
        """
        Create field mappings for specific contract templates based on contract type.
        
        Args:
            contract_type: Type of contract (consent_transport, payment_agreement, patient_service_agreement)
            trip_data: Trip information dictionary
            trip_lines_data: List of trip line data (can be dicts or objects)
            contact_data: Contact/customer information dictionary  
            patient_data: Patient information dictionary
            passengers_data: List of passenger information
            quote_data: Quote information dictionary
            
        Returns:
            Dict containing field mappings for DocuSeal template
        """
        from datetime import datetime
        
        # Get origin and destination airports from trip lines
        from_airport = ''
        to_airport = ''
        if trip_lines_data and len(trip_lines_data) > 0:
            # Handle both dict and object formats
            first_line = trip_lines_data[0]
            last_line = trip_lines_data[-1]
            
            if hasattr(first_line, 'origin_airport'):
                # Object format
                from_airport = first_line.origin_airport.name if first_line.origin_airport else ''
                to_airport = last_line.destination_airport.name if last_line.destination_airport else ''
            else:
                # Dict format - try different possible field names
                from_airport = first_line.get('origin_airport_name', '') or first_line.get('origin_airport', '')
                to_airport = last_line.get('destination_airport_name', '') or last_line.get('destination_airport', '')
        
        # Calculate price with 2.5% fee if quote data available
        price_with_fee = ''
        if quote_data and quote_data.get('quoted_amount'):
            base_price = float(quote_data.get('quoted_amount', 0))
            price_with_fee = f"${base_price * 1.025:,.2f}"
        
        # Get patient name
        patient_name = ''
        patient_phone = ''
        patient_address = ''
        patient_csz = ''  # City, State, Zip
        if patient_data:
            patient_info = patient_data.get('info', {})
            patient_first = patient_info.get('first_name', '')
            patient_last = patient_info.get('last_name', '')
            patient_name = f"{patient_first} {patient_last}".strip()
            patient_phone = patient_info.get('phone', '')
            patient_address = patient_info.get('address_line1', '')
            
            # Build city, state, zip
            city = patient_info.get('city', '')
            state = patient_info.get('state', '')
            zip_code = patient_info.get('zip', '')
            patient_csz = f"{city}, {state} {zip_code}".strip()
        
        # Get customer name and email
        customer_name = ''
        customer_email = ''
        if contact_data:
            customer_first = contact_data.get('first_name', '')
            customer_last = contact_data.get('last_name', '')
            customer_name = f"{customer_first} {customer_last}".strip()
            if not customer_name and contact_data.get('business_name'):
                customer_name = contact_data.get('business_name', '')
            customer_email = contact_data.get('email', '')
        
        # Get passenger names (first passenger if any)
        passenger_name = 'None'
        if passengers_data and len(passengers_data) > 0:
            passenger_info = passengers_data[0].get('info', {})
            passenger_first = passenger_info.get('first_name', '')
            passenger_last = passenger_info.get('last_name', '')
            passenger_full = f"{passenger_first} {passenger_last}".strip()
            if passenger_full:
                passenger_name = passenger_full
        
        # Get current date components
        now = timezone.now()
        day_number = now.strftime('%d').lstrip('0')  # Remove leading zero
        month_name = now.strftime('%B')  # Full month name like "August"
        
        # Build field mappings based on contract type
        if contract_type == 'consent_transport':
            # Consent for Transport fields
            return {
                'from_airport': from_airport,
                'to_airport': to_airport,
            }
        
        elif contract_type == 'payment_agreement':
            # Air Ambulance Payment Agreement fields
            return {
                'patient_name': patient_name,
                'passenger_name': passenger_name,
                'from_airport': from_airport,
                'to_airport': to_airport,
                'price': price_with_fee,
                'customer_name': customer_name,
                'customer_email': customer_email,
            }
        
        elif contract_type == 'patient_service_agreement':
            # Patient Service Agreement fields
            return {
                'day_number': day_number,
                'month_name': month_name,
                'patient_name': patient_name,
                'patient_phone': patient_phone,
                'patient_address': patient_address,
                'patient_csz': patient_csz,
                'from_airport': from_airport,
                'to_airport': to_airport,
            }
        
        else:
            # Default fields for unknown contract types
            return {
                'from_airport': from_airport,
                'to_airport': to_airport,
                'customer_name': customer_name,
                'customer_email': customer_email,
                'patient_name': patient_name,
            }
```


# File: utils/smtp/__init__.py

```python
from .email import send_email, send_template



__all__ = {
    "send_email",
    "send_template"
}
```


# File: utils/smtp/email.py

```python
from os import getenv
import smtplib
from email.mime.text import MIMEText
from typing import List
from pathlib import Path

EMAIL_TEMPLATE_PATH = Path(__file__).resolve().parent / "email_template.html"


def send_email(subject: str, targets: List[str], body: str, is_html: bool = False):
    msg = MIMEText(body, "html") if is_html else MIMEText(body)
    msg["From"] = getenv("DEFAULT_FROM_EMAIL")
    msg["To"] = ", ".join(targets)
    msg["Subject"] = subject

    server = None
    try:
        host = getenv("EMAIL_HOST")
        port = int(getenv("EMAIL_PORT", "587"))
        user = getenv("EMAIL_HOST_USER")
        password = getenv("EMAIL_HOST_PASSWORD")

        server = smtplib.SMTP(host, port, timeout=20)
        server.ehlo()

        server.starttls()
        server.ehlo()

        server.login(user, password)
        server.sendmail(msg["From"], targets, msg.as_string())
        return True
    except Exception as e:
        print("❌ Email error:", e)
        return False
    finally:
        if server:
            server.quit()


# TODO add support for preview and text below button
def fill_template(text: str, link_address: str, link_label="Click Here!"):
    with open(EMAIL_TEMPLATE_PATH, "r") as file:
        content = file.read()
    html = content.replace("%%%PREVIEW%%%", "").replace("%%%BOTTEXT%%%", "")
    html = (
        html.replace("%%%LINK%%%", link_address)
        .replace("%%%LINKTEXT%%%", link_label)
        .replace("%%%TOPTEXT%%%", text)
    )
    return html


def send_template(subject: str, targets: List[str], title: str, link: str, link_text="Click Here!"):
    body = fill_template(title, link, link_label=link_text)
    return send_email(subject, targets, body, is_html=True)
  


if __name__ == "__main__":
    from dotenv import load_dotenv

    load_dotenv()
    print(
        send_template(
            "Test Email",
            ["myrmelryan@gmail.com","ck@cekitch.com"],
            "click here for fun",
            "http://www.google.com",
        )
    )

```


# File: api/timezone_utils.py

```python
"""
Timezone utilities for handling airport-specific time conversions.

This module provides functions to convert between local airport times and UTC,
properly handling daylight saving time transitions using IANA timezone identifiers.
"""

import pytz
from datetime import datetime, timezone
from typing import Optional, Tuple
from django.utils import timezone as django_timezone


def convert_local_to_utc(local_datetime: datetime, airport_timezone: str) -> datetime:
    """
    Convert a local datetime to UTC using the airport's timezone.
    
    Args:
        local_datetime: Datetime in the airport's local time (naive or aware)
        airport_timezone: IANA timezone identifier (e.g., 'America/New_York')
    
    Returns:
        UTC datetime with timezone info
    
    Raises:
        pytz.exceptions.UnknownTimeZoneError: If timezone is invalid
        pytz.exceptions.AmbiguousTimeError: For ambiguous DST transition times
        pytz.exceptions.NonExistentTimeError: For non-existent DST transition times
    """
    if not airport_timezone:
        raise ValueError("Airport timezone is required")
    
    # Get the timezone object
    tz = pytz.timezone(airport_timezone)
    
    # If datetime already has timezone info, convert directly to UTC
    if local_datetime.tzinfo is not None:
        # If it's already in UTC, return as is
        if local_datetime.tzinfo == pytz.UTC:
            return local_datetime
        # Otherwise, convert to UTC
        return local_datetime.astimezone(pytz.UTC)
    
    # Localize the naive datetime to the airport's timezone
    # This handles DST transitions automatically
    try:
        localized_dt = tz.localize(local_datetime, is_dst=None)
    except pytz.exceptions.AmbiguousTimeError:
        # During "fall back" DST transition, choose the first occurrence (before DST ends)
        localized_dt = tz.localize(local_datetime, is_dst=True)
    except pytz.exceptions.NonExistentTimeError:
        # During "spring forward" DST transition, move to the next valid time
        localized_dt = tz.localize(local_datetime, is_dst=False)
    
    # Convert to UTC
    return localized_dt.astimezone(pytz.UTC)


def convert_utc_to_local(utc_datetime: datetime, airport_timezone: str) -> datetime:
    """
    Convert a UTC datetime to local airport time.
    
    Args:
        utc_datetime: UTC datetime (with or without timezone info)
        airport_timezone: IANA timezone identifier (e.g., 'America/New_York')
    
    Returns:
        Naive datetime in the airport's local time
    
    Raises:
        pytz.exceptions.UnknownTimeZoneError: If timezone is invalid
    """
    if not airport_timezone:
        raise ValueError("Airport timezone is required")
    
    # Ensure UTC datetime is timezone-aware
    if utc_datetime.tzinfo is None:
        utc_datetime = utc_datetime.replace(tzinfo=pytz.UTC)
    elif utc_datetime.tzinfo != pytz.UTC:
        utc_datetime = utc_datetime.astimezone(pytz.UTC)
    
    # Get the timezone object and convert
    tz = pytz.timezone(airport_timezone)
    local_dt = utc_datetime.astimezone(tz)
    
    # Return naive datetime in local time
    return local_dt.replace(tzinfo=None)


def get_timezone_info(airport_timezone: str, dt: Optional[datetime] = None) -> dict:
    """
    Get timezone information for an airport at a specific datetime.
    
    Args:
        airport_timezone: IANA timezone identifier
        dt: Datetime to check (defaults to current time)
    
    Returns:
        Dict with timezone info: {
            'timezone': 'America/New_York',
            'abbreviation': 'EST' or 'EDT',
            'utc_offset': '-05:00',
            'is_dst': True/False,
            'dst_transition_next': datetime or None
        }
    """
    if not airport_timezone:
        raise ValueError("Airport timezone is required")
    
    if dt is None:
        dt = django_timezone.now()
    elif dt.tzinfo is None:
        dt = dt.replace(tzinfo=pytz.UTC)
    
    tz = pytz.timezone(airport_timezone)
    localized_dt = dt.astimezone(tz)
    
    # Get timezone info
    tzinfo = {
        'timezone': airport_timezone,
        'abbreviation': localized_dt.strftime('%Z'),
        'utc_offset': localized_dt.strftime('%z'),
        'is_dst': bool(localized_dt.dst()),
    }
    
    # Find next DST transition (useful for warnings)
    try:
        # Use a safer approach to get DST transitions
        next_transition = None
        
        # Check if timezone has _utc_transition_times and it's iterable
        if hasattr(tz, '_utc_transition_times') and hasattr(tz._utc_transition_times, '__iter__'):
            try:
                # Get transitions for the current year and next year
                current_year = localized_dt.year
                transitions = []
                
                # Safely iterate through transition times
                transition_times = tz._utc_transition_times
                # Handle different pytz versions - some return tuples, some just datetimes
                for transition_item in transition_times:
                    if isinstance(transition_item, tuple) and len(transition_item) >= 3:
                        transition_dt, before_tz, after_tz = transition_item
                    elif hasattr(transition_item, 'year'):  # It's a datetime
                        transition_dt = transition_item
                    else:
                        continue
                        
                    if (hasattr(transition_dt, 'year') and 
                        transition_dt.year in [current_year, current_year + 1] and 
                        transition_dt > dt):
                        transitions.append(transition_dt)
                        
                next_transition = min(transitions) if transitions else None
            except (TypeError, ValueError, AttributeError):
                pass
        
        tzinfo['dst_transition_next'] = next_transition
    except Exception:
        # Fallback - don't include DST transition info if we can't determine it safely
        tzinfo['dst_transition_next'] = None
    
    return tzinfo


def validate_time_consistency(departure_local: datetime, departure_utc: datetime, 
                             departure_timezone: str) -> bool:
    """
    Validate that local and UTC times are consistent for a given timezone.
    
    Args:
        departure_local: Local departure time (naive or aware)
        departure_utc: UTC departure time (with timezone info)
        departure_timezone: IANA timezone identifier
    
    Returns:
        True if times are consistent, False otherwise
    """
    try:
        # Convert local to UTC and compare
        calculated_utc = convert_local_to_utc(departure_local, departure_timezone)
        
        # Ensure both datetimes are timezone-aware for comparison
        if departure_utc.tzinfo is None:
            departure_utc = departure_utc.replace(tzinfo=pytz.UTC)
        elif departure_utc.tzinfo != pytz.UTC:
            departure_utc = departure_utc.astimezone(pytz.UTC)
        
        # Allow for small differences (up to 1 second) due to rounding
        time_diff = abs((calculated_utc - departure_utc).total_seconds())
        return time_diff <= 1.0
        
    except Exception:
        return False


def calculate_flight_duration_with_timezones(
    departure_local: datetime, departure_timezone: str,
    arrival_local: datetime, arrival_timezone: str
) -> Tuple[float, dict]:
    """
    Calculate flight duration accounting for timezone differences.
    
    Args:
        departure_local: Local departure time (naive)
        departure_timezone: Departure airport timezone
        arrival_local: Local arrival time (naive)
        arrival_timezone: Arrival airport timezone
    
    Returns:
        Tuple of (duration_hours, info_dict)
        info_dict contains UTC times and timezone info
    """
    # Convert both times to UTC
    departure_utc = convert_local_to_utc(departure_local, departure_timezone)
    arrival_utc = convert_local_to_utc(arrival_local, arrival_timezone)
    
    # Calculate actual flight duration
    duration_seconds = (arrival_utc - departure_utc).total_seconds()
    duration_hours = duration_seconds / 3600.0
    
    # Prepare info
    info = {
        'departure_utc': departure_utc,
        'arrival_utc': arrival_utc,
        'departure_tz_info': get_timezone_info(departure_timezone, departure_utc),
        'arrival_tz_info': get_timezone_info(arrival_timezone, arrival_utc),
        'duration_seconds': duration_seconds,
        'duration_hours': duration_hours,
        'crosses_date_line': arrival_local.date() != departure_local.date(),
        'timezone_difference_hours': (
            arrival_utc.utcoffset().total_seconds() - departure_utc.utcoffset().total_seconds()
        ) / 3600.0 if arrival_utc.utcoffset() and departure_utc.utcoffset() else 0
    }
    
    return duration_hours, info


def format_time_with_timezone(dt: datetime, timezone_str: str, 
                              include_utc: bool = False) -> str:
    """
    Format a datetime with timezone information for display.
    
    Args:
        dt: Datetime to format (UTC or naive)
        timezone_str: Target timezone for display
        include_utc: Whether to include UTC time in parentheses
    
    Returns:
        Formatted string like "14:30 EST (19:30 UTC)" or "14:30 EST"
    """
    if not timezone_str:
        return dt.strftime('%H:%M')
    
    try:
        if dt.tzinfo is None:
            # Assume it's already in the target timezone
            local_dt = dt
            tz_info = get_timezone_info(timezone_str, 
                                       convert_local_to_utc(dt, timezone_str))
        else:
            # Convert to target timezone
            local_dt = convert_utc_to_local(dt, timezone_str)
            tz_info = get_timezone_info(timezone_str, dt)
        
        formatted = f"{local_dt.strftime('%H:%M')} {tz_info['abbreviation']}"
        
        if include_utc and dt.tzinfo:
            utc_dt = dt.astimezone(pytz.UTC) if dt.tzinfo != pytz.UTC else dt
            formatted += f" ({utc_dt.strftime('%H:%M')} UTC)"
        
        return formatted
        
    except Exception:
        return dt.strftime('%H:%M')


def check_dst_transition_warning(local_dt: datetime, timezone_str: str) -> Optional[dict]:
    """
    Check if a datetime is near a DST transition and return warning info.
    
    Args:
        local_dt: Local datetime to check
        timezone_str: IANA timezone identifier
    
    Returns:
        Dict with warning info or None if no issues
    """
    try:
        tz = pytz.timezone(timezone_str)
        
        # Check if the time is ambiguous (during "fall back")
        try:
            tz.localize(local_dt, is_dst=None)
        except pytz.exceptions.AmbiguousTimeError:
            return {
                'type': 'ambiguous',
                'message': 'This time occurs twice due to daylight saving transition. Using the first occurrence.',
                'suggestion': 'Consider specifying a different time to avoid confusion.'
            }
        except pytz.exceptions.NonExistentTimeError:
            return {
                'type': 'non_existent',
                'message': 'This time does not exist due to daylight saving transition.',
                'suggestion': 'Please choose a time after the DST transition.'
            }
        
        # Check if near a DST transition (within 24 hours)
        tz_info = get_timezone_info(timezone_str, 
                                   convert_local_to_utc(local_dt, timezone_str))
        
        if tz_info.get('dst_transition_next'):
            next_transition = tz_info['dst_transition_next']
            hours_until_transition = (next_transition - convert_local_to_utc(local_dt, timezone_str)).total_seconds() / 3600
            
            if 0 < hours_until_transition <= 24:
                return {
                    'type': 'near_transition',
                    'message': f'DST transition occurs in {hours_until_transition:.1f} hours.',
                    'suggestion': 'Double-check times if this flight crosses the transition.'
                }
        
        return None
        
    except Exception:
        return None
```


# File: api/admin.py

```python
from django.contrib import admin
from .models import (
    Modification, Permission, Role, Department, UserProfile, Contact, 
    FBO, Ground, Airport, Document, Aircraft, Transaction, Agreement,
    Patient, Quote, Passenger, CrewLine, Trip, TripLine
)

# Register models
admin.site.register(Modification)
admin.site.register(Permission)
admin.site.register(Role)
admin.site.register(Department)
admin.site.register(UserProfile)
admin.site.register(Contact)
admin.site.register(FBO)
admin.site.register(Ground)
admin.site.register(Airport)
admin.site.register(Document)
admin.site.register(Aircraft)
admin.site.register(Transaction)
admin.site.register(Agreement)
admin.site.register(Patient)
admin.site.register(Quote)
admin.site.register(Passenger)
admin.site.register(CrewLine)
admin.site.register(Trip)
admin.site.register(TripLine)

```


# File: api/middleware.py

```python
from django.utils.deprecation import MiddlewareMixin
from .signals import set_current_user


class CurrentUserMiddleware(MiddlewareMixin):
    """
    Middleware to set the current user in thread-local storage
    for use in modification tracking
    """
    
    def process_request(self, request):
        """Set the current user at the start of each request"""
        user = getattr(request, 'user', None)
        if user and user.is_authenticated:
            set_current_user(user)
        else:
            set_current_user(None)
        return None
    
    def process_response(self, request, response):
        """Clear the current user after the request is complete"""
        set_current_user(None)
        return response
    
    def process_exception(self, request, exception):
        """Clear the current user if an exception occurs"""
        set_current_user(None)
        return None
```


# File: api/urls.py

```python
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'permissions', views.PermissionViewSet)
router.register(r'roles', views.RoleViewSet)
router.register(r'departments', views.DepartmentViewSet)
router.register(r'users', views.UserProfileViewSet)
router.register(r'contacts', views.ContactViewSet)
router.register(r'fbos', views.FBOViewSet)
router.register(r'grounds', views.GroundViewSet)
router.register(r'airports', views.AirportViewSet)
router.register(r'documents', views.DocumentViewSet)
router.register(r'aircraft', views.AircraftViewSet)
router.register(r'transactions', views.TransactionViewSet)
router.register(r'agreements', views.AgreementViewSet)
router.register(r'patients', views.PatientViewSet)
router.register(r'quotes', views.QuoteViewSet)
router.register(r'passengers', views.PassengerViewSet)
router.register(r'crew-lines', views.CrewLineViewSet)
router.register(r'trips', views.TripViewSet)
router.register(r'trip-lines', views.TripLineViewSet)
router.register(r'modifications', views.ModificationViewSet)
router.register(r"staff", views.StaffViewSet, basename="staff")
router.register(r"staff-roles", views.StaffRoleViewSet, basename="staff-role")
router.register(r"staff-role-memberships", views.StaffRoleMembershipViewSet, basename="staff-role-membership")
router.register(r"trip-events", views.TripEventViewSet, basename="trip-event")
router.register(r'comments', views.CommentViewSet, basename='comment')
router.register(r'contracts', views.ContractViewSet, basename='contract')

urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('airport/fuel-prices/<str:airport_code>/', views.get_fuel_prices, name='fuel-prices'),
    path('dashboard/stats/', views.dashboard_stats, name='dashboard-stats'),
    path('contacts/create-with-related/', views.create_contact_with_related, name='create-contact-with-related'),
    # Timezone utility endpoints
    path('airports/<uuid:airport_id>/timezone-info/', views.get_airport_timezone_info, name='airport-timezone-info'),
    path('timezone/convert/', views.convert_timezone, name='timezone-convert'),
    path('timezone/validate-flight-times/', views.validate_flight_times, name='validate-flight-times'),
    # DocuSeal webhook endpoint
    path('docuseal/webhook/', views.docuseal_webhook, name='docuseal-webhook'),
]

```


# File: api/views.py

```python
from django.shortcuts import render
from rest_framework import viewsets, permissions, status, filters
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from django.db.models import Q
from django.utils import timezone
from django.http import HttpResponse, JsonResponse
import json
from itertools import chain
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from io import BytesIO
import logging
# TripEvent imports moved to consolidated imports section below

from .external.airport import get_airport, parse_fuel_cost

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_fuel_prices(request, airport_code):
    """
    Get fuel prices for a specific airport
    """
    try:
        # Get airport data from FlightAware
        soup = get_airport(airport_code)
        if not soup:
            return JsonResponse({'error': 'Failed to retrieve airport data'}, status=400)
        
        # Parse fuel prices
        fuel_prices = parse_fuel_cost(soup)
        
        return JsonResponse({'fuel_prices': fuel_prices})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

from .models import (
    Modification, Permission, Role, Department, UserProfile, Contact, 
    FBO, Ground, Airport, Document, Aircraft, Transaction, Agreement,
    Patient, Quote, Passenger, CrewLine, Trip, TripLine, Staff, StaffRole, StaffRoleMembership, TripEvent, Comment, Contract
)
from .utils import track_creation, track_deletion
from .contact_service import ContactCreationService, ContactCreationSerializer
from utils.services.docuseal_service import DocuSealService

logger = logging.getLogger(__name__)
from .serializers import (
    ModificationSerializer, PermissionSerializer, RoleSerializer, DepartmentSerializer,
    ContactSerializer, CommentSerializer, FBOSerializer, GroundSerializer, AirportSerializer, AircraftSerializer,
    AgreementSerializer, DocumentSerializer,
    # Standardized CRUD serializers
    UserProfileReadSerializer, UserProfileWriteSerializer,
    PassengerReadSerializer, PassengerWriteSerializer,
    CrewLineReadSerializer, CrewLineWriteSerializer,
    TripLineReadSerializer, TripLineWriteSerializer,
    TripEventReadSerializer, TripEventWriteSerializer,
    TripReadSerializer, TripWriteSerializer,
    QuoteReadSerializer, QuoteWriteSerializer,
    DocumentReadSerializer, DocumentUploadSerializer,
    TransactionPublicReadSerializer, TransactionReadSerializer, TransactionProcessWriteSerializer,
    PatientReadSerializer, PatientWriteSerializer, StaffReadSerializer, StaffWriteSerializer,
    StaffRoleSerializer,
    StaffRoleMembershipReadSerializer, StaffRoleMembershipWriteSerializer,
    ContractReadSerializer, ContractWriteSerializer, ContractCreateFromTripSerializer, 
    ContractDocuSealActionSerializer, DocuSealWebhookSerializer,
)
from .permissions import (
    IsAuthenticatedOrPublicEndpoint, IsTransactionOwner,
    CanReadQuote, CanWriteQuote, CanModifyQuote, CanDeleteQuote,
    CanReadPatient, CanWritePatient, CanModifyPatient, CanDeletePatient,
    CanReadTrip, CanWriteTrip, CanModifyTrip, CanDeleteTrip,
    CanReadPassenger, CanWritePassenger, CanModifyPassenger, CanDeletePassenger,
    CanReadTransaction, CanWriteTransaction, CanModifyTransaction, CanDeleteTransaction,
    CanReadTripLine, CanWriteTripLine, CanModifyTripLine, CanDeleteTripLine
)

# Standard pagination class for all ViewSets
class StandardPagination(PageNumberPagination):
    page_size = 25
    page_size_query_param = 'page_size'
    max_page_size = 100

# Custom pagination for airports (if different settings needed)
class AirportPagination(PageNumberPagination):
    page_size = 25
    page_size_query_param = 'page_size'
    max_page_size = 100

# Base ViewSet with common functionality
class BaseViewSet(viewsets.ModelViewSet):
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = StandardPagination  # Apply pagination to all ViewSets
    
    def perform_create(self, serializer):
        instance = serializer.save(created_by=self.request.user)
        # Track creation
        track_creation(instance, self.request.user)
    
    def perform_update(self, serializer):
        from .signals import set_skip_signal_tracking
        
        # Get the old instance before updating
        if serializer.instance and hasattr(serializer.instance, 'pk'):
            old_instance = serializer.instance.__class__.objects.get(pk=serializer.instance.pk)
            # Exclude system fields that shouldn't be tracked
            excluded_fields = {'id', 'created_on', 'modified_on', 'created_by', 'modified_by'}
            old_fields = {field.name: getattr(old_instance, field.name) 
                         for field in old_instance._meta.fields 
                         if not field.is_relation and field.name not in excluded_fields}
        else:
            old_fields = {}
        
        try:
            # Skip signal tracking during this operation
            set_skip_signal_tracking(True)
            
            # Save the instance
            instance = serializer.save(modified_by=self.request.user)
            
        finally:
            # Re-enable signal tracking
            set_skip_signal_tracking(False)
        
        # Track modifications manually with user
        if old_fields:
            from .utils import track_modification
            # Use same excluded fields for new values
            excluded_fields = {'id', 'created_on', 'modified_on', 'created_by', 'modified_by'}
            new_fields = {field.name: getattr(instance, field.name) 
                         for field in instance._meta.fields 
                         if not field.is_relation and field.name not in excluded_fields}
            
            for field_name, old_value in old_fields.items():
                new_value = new_fields.get(field_name)
                if old_value != new_value:
                    track_modification(instance, field_name, old_value, new_value, self.request.user)
        
    def perform_destroy(self, instance):
        # Track deletion before destroying
        track_deletion(instance, self.request.user)
        instance.delete()

# Permission ViewSet
class PermissionViewSet(BaseViewSet):
    queryset = Permission.objects.all()
    serializer_class = PermissionSerializer
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'created_on']

# Role ViewSet
class RoleViewSet(BaseViewSet):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'created_on']

# Department ViewSet
class DepartmentViewSet(BaseViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'created_on']

# UserProfile ViewSet
class UserProfileViewSet(BaseViewSet):
    queryset = UserProfile.objects.select_related('user').prefetch_related('roles', 'departments')
    search_fields = ['first_name', 'last_name', 'email']
    ordering_fields = ['first_name', 'last_name', 'created_on']
    
    def get_serializer_class(self):
        if self.action in ('list', 'retrieve', 'me'):
            return UserProfileReadSerializer
        return UserProfileWriteSerializer
    
    @action(detail=False, methods=['get'])
    def me(self, request):
        try:
            profile = UserProfile.objects.select_related('user').prefetch_related('roles', 'departments').get(user=request.user)
            serializer = self.get_serializer(profile)
            return Response(serializer.data)
        except UserProfile.DoesNotExist:
            return Response({"detail": "Profile not found"}, status=status.HTTP_404_NOT_FOUND)

# Contact ViewSet
class ContactViewSet(BaseViewSet):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer
    search_fields = ['first_name', 'last_name', 'business_name', 'email']
    ordering_fields = ['first_name', 'last_name', 'business_name', 'created_on']

# FBO ViewSet
class FBOViewSet(BaseViewSet):
    queryset = FBO.objects.all()
    serializer_class = FBOSerializer
    search_fields = ['name', 'city', 'country']
    ordering_fields = ['name', 'created_on']

# Ground ViewSet
class GroundViewSet(BaseViewSet):
    queryset = Ground.objects.all()
    serializer_class = GroundSerializer
    search_fields = ['name', 'city', 'country']
    ordering_fields = ['name', 'created_on']

# Airport ViewSet
class AirportViewSet(BaseViewSet):
    queryset = Airport.objects.all()
    serializer_class = AirportSerializer
    pagination_class = AirportPagination
    search_fields = ['name', 'ident', 'icao_code', 'iata_code', 'municipality', 'iso_country', 'iso_region']
    ordering_fields = ['name', 'ident', 'icao_code', 'iata_code', 'airport_type', 'created_on']
    
    @action(detail=False, methods=['get'])
    def search(self, request):
        query = request.query_params.get('q', '')
        if len(query) < 2:
            return Response({"detail": "Search query too short"}, status=status.HTTP_400_BAD_REQUEST)
            
        airports = Airport.objects.filter(
            Q(name__icontains=query) | 
            Q(ident__icontains=query) |
            Q(icao_code__icontains=query) | 
            Q(iata_code__icontains=query) |
            Q(municipality__icontains=query) |
            Q(iso_country__icontains=query)
        )[:10]
        
        serializer = self.get_serializer(airports, many=True)
        return Response(serializer.data)

# Document ViewSet
class DocumentViewSet(BaseViewSet):
    queryset = Document.objects.all()
    
    def get_serializer_class(self):
        if self.action in ['create', 'update']:
            return DocumentUploadSerializer
        return DocumentReadSerializer
    
    @action(detail=True, methods=['get'])
    def download(self, request, pk=None):
        document = self.get_object()
        response = HttpResponse(document.content, content_type='application/octet-stream')
        response['Content-Disposition'] = f'attachment; filename="{document.filename}"'
        return response

# Aircraft ViewSet
class AircraftViewSet(BaseViewSet):
    queryset = Aircraft.objects.all()
    serializer_class = AircraftSerializer
    search_fields = ['tail_number', 'make', 'model', 'company']
    ordering_fields = ['tail_number', 'make', 'model', 'created_on']

# Transaction ViewSet
class TransactionViewSet(BaseViewSet):
    queryset = Transaction.objects.all()
    search_fields = ['key', 'email', 'payment_status']
    ordering_fields = ['payment_date', 'amount', 'created_on']
    permission_classes = [
        IsAuthenticatedOrPublicEndpoint, 
        IsTransactionOwner,
        CanReadTransaction | CanWriteTransaction | CanModifyTransaction | CanDeleteTransaction
    ]
    public_actions = ['retrieve_by_key']
    
    def get_serializer_class(self):
        # Public read by key uses minimal serializer
        if self.action == 'retrieve_by_key':
            return TransactionPublicReadSerializer
        # Staff read operations use full serializer
        elif self.action in ('list', 'retrieve'):
            return TransactionReadSerializer
        # Process payment uses special write serializer
        elif self.action == 'process_payment':
            return TransactionProcessWriteSerializer
        # Default write operations
        return TransactionProcessWriteSerializer
    
    @action(detail=False, methods=['get'], url_path='pay/(?P<transaction_key>[^/.]+)')
    def retrieve_by_key(self, request, transaction_key=None):
        """
        Public endpoint to retrieve transaction details by key for payment processing.
        """
        try:
            transaction = Transaction.objects.get(key=transaction_key)
            serializer = self.get_serializer(transaction)
            return Response(serializer.data)
        except Transaction.DoesNotExist:
            return Response(
                {"detail": "Transaction not found"}, 
                status=status.HTTP_404_NOT_FOUND
            )
    
    @action(detail=True, methods=['post'])
    def process_payment(self, request, pk=None):
        transaction = self.get_object()
        # Here you would integrate with Authorize.net
        # This is a placeholder for the actual payment processing logic
        transaction.payment_status = "completed"
        transaction.save()
        serializer = self.get_serializer(transaction)
        return Response(serializer.data)

# Agreement ViewSet
class AgreementViewSet(BaseViewSet):
    queryset = Agreement.objects.all()
    serializer_class = AgreementSerializer
    search_fields = ['destination_email', 'status']
    ordering_fields = ['created_on', 'status']
    
    @action(detail=True, methods=['post'])
    def send_for_signature(self, request, pk=None):
        agreement = self.get_object()
        # Here you would integrate with Adobe Sign
        # This is a placeholder for the actual signature request logic
        agreement.status = "pending"
        agreement.save()
        serializer = self.get_serializer(agreement)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def check_signature_status(self, request, pk=None):
        agreement = self.get_object()
        # Here you would check with Adobe Sign API
        # This is a placeholder for the actual status check logic
        serializer = self.get_serializer(agreement)
        return Response(serializer.data)

# Patient ViewSet
class PatientViewSet(BaseViewSet):
    queryset = Patient.objects.select_related('info')
    search_fields = ['info__first_name', 'info__last_name', 'nationality']
    ordering_fields = ['created_on']
    permission_classes = [
        permissions.IsAuthenticated,
        CanReadPatient | CanWritePatient | CanModifyPatient | CanDeletePatient
    ]
    
    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return PatientReadSerializer
        return PatientWriteSerializer
    
    def get_permissions(self):
        """
        Instantiate and return the list of permissions that this view requires.
        """
        if self.action == 'list' or self.action == 'retrieve':
            permission_classes = [permissions.IsAuthenticated, CanReadPatient]
        elif self.action == 'create':
            permission_classes = [permissions.IsAuthenticated, CanWritePatient]
        elif self.action in ['update', 'partial_update']:
            permission_classes = [permissions.IsAuthenticated, CanModifyPatient]
        elif self.action == 'destroy':
            permission_classes = [permissions.IsAuthenticated, CanDeletePatient]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]

# Quote ViewSet
class QuoteViewSet(BaseViewSet):
    queryset = Quote.objects.select_related('contact', 'pickup_airport', 'dropoff_airport', 'patient', 'patient__info').prefetch_related('transactions')
    search_fields = ['contact__first_name', 'contact__last_name', 'patient__info__first_name', 'patient__info__last_name', 'status']
    ordering_fields = ['created_on', 'quoted_amount']
    permission_classes = [
        permissions.IsAuthenticated,
        CanReadQuote | CanWriteQuote | CanModifyQuote | CanDeleteQuote
    ]
    
    def get_queryset(self):
        """
        Filter quotes by status and handle UUID search if provided in query params
        """
        queryset = super().get_queryset()
        
        # Filter by status if provided
        status_filter = self.request.query_params.get('status', None)
        if status_filter:
            queryset = queryset.filter(status=status_filter)
            
        return queryset
    
    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return QuoteReadSerializer
        return QuoteWriteSerializer
    
    def get_permissions(self):
        """
        Instantiate and return the list of permissions that this view requires.
        """
        if self.action == 'list' or self.action == 'retrieve':
            permission_classes = [permissions.IsAuthenticated, CanReadQuote]
        elif self.action == 'create':
            permission_classes = [permissions.IsAuthenticated, CanWriteQuote]
        elif self.action in ['update', 'partial_update']:
            permission_classes = [permissions.IsAuthenticated, CanModifyQuote]
        elif self.action == 'destroy':
            permission_classes = [permissions.IsAuthenticated, CanDeleteQuote]
        elif self.action == 'create_transaction':
            permission_classes = [permissions.IsAuthenticated, CanWriteTransaction]
        elif self.action == 'generate_quote_document':
            permission_classes = [permissions.IsAuthenticated, CanModifyQuote]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]
    
    @action(detail=True, methods=['post'])
    def create_transaction(self, request, pk=None):
        quote = self.get_object()
        amount = request.data.get('amount', quote.quoted_amount)
        email = request.data.get('email', quote.quote_pdf_email)
        
        transaction = Transaction.objects.create(
            created_by=request.user,
            amount=amount,
            payment_method=request.data.get('payment_method', 'credit_card'),
            email=email
        )
        
        quote.transactions.add(transaction)
        
        return Response(TransactionReadSerializer(transaction).data, status=status.HTTP_201_CREATED)
    
    @action(detail=True, methods=['get'])
    def pdf(self, request, pk=None):
        """
        Generate and return a professional quote PDF
        """
        quote = self.get_object()
        
        # Generate PDF
        buffer = BytesIO()
        doc = SimpleDocTemplate(
            buffer, 
            pagesize=letter, 
            rightMargin=50, 
            leftMargin=50, 
            topMargin=50, 
            bottomMargin=50
        )
        
        # Custom styles
        styles = getSampleStyleSheet()
        
        # Company header style
        company_style = ParagraphStyle(
            'CompanyHeader',
            parent=styles['Normal'],
            fontSize=18,
            fontName='Helvetica-Bold',
            textColor=colors.HexColor('#1E40AF'),
            alignment=0,  # Left alignment
            spaceBefore=0,
            spaceAfter=6,
            leading=22
        )
        
        # Company info style
        company_info_style = ParagraphStyle(
            'CompanyInfo',
            parent=styles['Normal'],
            fontSize=9,
            textColor=colors.HexColor('#6B7280'),
            alignment=0,
            spaceBefore=0,
            spaceAfter=0,
            leading=11
        )
        
        # Quote title style
        quote_title_style = ParagraphStyle(
            'QuoteTitle',
            parent=styles['Normal'],
            fontSize=24,
            fontName='Helvetica-Bold',
            textColor=colors.HexColor('#1F2937'),
            alignment=2,  # Right alignment
            spaceBefore=0,
            spaceAfter=6,
            leading=28
        )
        
        # Quote number style
        quote_number_style = ParagraphStyle(
            'QuoteNumber',
            parent=styles['Normal'],
            fontSize=10,
            textColor=colors.HexColor('#6B7280'),
            alignment=2,  # Right alignment
            spaceBefore=0,
            spaceAfter=0,
            leading=12
        )
        
        # Section header style
        section_header_style = ParagraphStyle(
            'SectionHeader',
            parent=styles['Normal'],
            fontSize=11,
            fontName='Helvetica-Bold',
            textColor=colors.HexColor('#1F2937'),
            spaceBefore=25,
            spaceAfter=12,
            leading=13,
            leftIndent=0,
            rightIndent=0
        )
        
        # Build PDF content
        story = []
        
        # Header section with company info and quote title
        header_data = [
            [
                Paragraph("JET ICU MEDICAL TRANSPORT", company_style), 
                Paragraph("QUOTE", quote_title_style)
            ],
            [
                Paragraph("1511 N Westshore Blvd #650<br/>Tampa, FL 33607", company_info_style),
                Paragraph(f"#{quote.id.hex[:8].upper()}", quote_number_style)
            ],
            [
                Paragraph("Phone: (352) 796-2540<br/>Email: info@jeticu.com", company_info_style),
                Paragraph(f"Date: {quote.created_on.strftime('%B %d, %Y') if quote.created_on else 'N/A'}", quote_number_style)
            ]
        ]
        
        header_table = Table(header_data, colWidths=[4.2*inch, 2.3*inch])
        header_table.setStyle(TableStyle([
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('ALIGN', (0, 0), (0, -1), 'LEFT'),
            ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
            ('TOPPADDING', (0, 0), (-1, -1), 4),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
            ('LEFTPADDING', (0, 0), (-1, -1), 0),
            ('RIGHTPADDING', (0, 0), (-1, -1), 0),
        ]))
        
        story.append(header_table)
        story.append(Spacer(1, 25))
        
        # Add customer info style
        customer_info_style = ParagraphStyle(
            'CustomerInfo',
            parent=styles['Normal'],
            fontSize=10,
            leading=14,
            spaceBefore=0,
            spaceAfter=0,
            leftIndent=0,
            rightIndent=0
        )
        
        # Bill To section
        if quote.contact:
            story.append(Paragraph("BILL TO", section_header_style))
            
            # Customer details
            customer_lines = []
            
            # Name and business
            name = f"{quote.contact.first_name} {quote.contact.last_name}"
            if quote.contact.business_name:
                customer_lines.append(quote.contact.business_name)
                customer_lines.append(name)
            else:
                customer_lines.append(name)
            
            # Address
            if quote.contact.address_line1:
                customer_lines.append(quote.contact.address_line1)
            if quote.contact.address_line2:
                customer_lines.append(quote.contact.address_line2)
            if quote.contact.city:
                city_line = quote.contact.city
                if quote.contact.state:
                    city_line += f", {quote.contact.state}"
                if quote.contact.zip:
                    city_line += f" {quote.contact.zip}"
                customer_lines.append(city_line)
            
            # Contact info
            if quote.contact.email:
                customer_lines.append(f"Email: {quote.contact.email}")
            if quote.contact.phone:
                customer_lines.append(f"Phone: {quote.contact.phone}")
            
            story.append(Paragraph("<br/>".join(customer_lines), customer_info_style))
            story.append(Spacer(1, 25))
        
        # Service Details Section
        story.append(Paragraph("SERVICE DETAILS", section_header_style))
        
        # Service table
        service_data = [
            ['Service', 'Details', 'Amount'],
        ]
        
        # Aircraft type description
        aircraft_desc = dict(quote._meta.get_field('aircraft_type').choices).get(quote.aircraft_type, quote.aircraft_type)
        medical_desc = dict(quote._meta.get_field('medical_team').choices).get(quote.medical_team, quote.medical_team)
        
        # Route description
        route = "Medical Air Transport"
        if quote.pickup_airport and quote.dropoff_airport:
            route = f"{quote.pickup_airport.name} → {quote.dropoff_airport.name}"
        
        service_data.append([
            route,
            f"Aircraft: {aircraft_desc}<br/>Medical Team: {medical_desc}<br/>Flight Time: {quote.estimated_flight_time if quote.estimated_flight_time else 'TBD'}",
            f"${quote.quoted_amount:,.2f}"
        ])
        
        # Ground transport if included
        if quote.includes_grounds:
            service_data.append([
                "Ground Transportation",
                "Airport transfers included",
                "Included"
            ])
        
        # Service table with better column distribution
        service_table = Table(service_data, colWidths=[2.2*inch, 2.8*inch, 1.5*inch])
        service_table.setStyle(TableStyle([
            # Header row
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1F2937')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
            ('VALIGN', (0, 0), (-1, 0), 'MIDDLE'),
            
            # Data rows
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 9),
            ('ALIGN', (0, 1), (0, -1), 'LEFT'),      # Service column
            ('ALIGN', (1, 1), (1, -1), 'LEFT'),      # Details column
            ('ALIGN', (2, 1), (2, -1), 'RIGHT'),     # Amount column
            ('VALIGN', (0, 1), (-1, -1), 'TOP'),
            
            # Alternating row colors
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F9FAFB')]),
            
            # Grid
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#E5E7EB')),
            ('LINEBELOW', (0, 0), (-1, 0), 2, colors.HexColor('#1F2937')),
            
            # Padding - increased for better spacing
            ('TOPPADDING', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
            ('LEFTPADDING', (0, 0), (-1, -1), 8),
            ('RIGHTPADDING', (0, 0), (-1, -1), 8),
        ]))
        
        story.append(service_table)
        story.append(Spacer(1, 25))
        
        # Total section
        total_data = [
            ['', 'Subtotal:', f"${quote.quoted_amount:,.2f}"],
            ['', 'Tax:', "$0.00"],
            ['', 'TOTAL:', f"${quote.quoted_amount:,.2f}"]
        ]
        
        total_table = Table(total_data, colWidths=[3.2*inch, 1.6*inch, 1.7*inch])
        total_table.setStyle(TableStyle([
            ('FONTNAME', (1, 0), (-1, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (1, 0), (-1, 1), 10),
            ('FONTSIZE', (1, 2), (-1, 2), 12),  # Total row larger
            ('ALIGN', (1, 0), (-1, -1), 'RIGHT'),
            ('TEXTCOLOR', (1, 2), (-1, 2), colors.HexColor('#1F2937')),
            ('LINEABOVE', (1, 2), (-1, 2), 1.5, colors.HexColor('#1F2937')),
            ('TOPPADDING', (1, 0), (-1, -1), 6),
            ('BOTTOMPADDING', (1, 0), (-1, -1), 6),
            ('LEFTPADDING', (1, 0), (-1, -1), 4),
            ('RIGHTPADDING', (1, 0), (-1, -1), 4),
        ]))
        
        story.append(total_table)
        story.append(Spacer(1, 25))
        
        # Patient Information (if applicable)
        if quote.patient and quote.patient.info:
            story.append(Paragraph("PATIENT INFORMATION", section_header_style))
            
            patient_info_data = [
                ['Patient Name:', f"{quote.patient.info.first_name} {quote.patient.info.last_name}"],
            ]
            
            if quote.patient.info.date_of_birth:
                patient_info_data.append(['Date of Birth:', quote.patient.info.date_of_birth.strftime('%B %d, %Y')])
            
            if quote.patient.info.nationality:
                patient_info_data.append(['Nationality:', quote.patient.info.nationality])
            
            patient_table = Table(patient_info_data, colWidths=[1.8*inch, 4.7*inch])
            patient_table.setStyle(TableStyle([
                ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 9),
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                ('TOPPADDING', (0, 0), (-1, -1), 3),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
                ('LEFTPADDING', (0, 0), (-1, -1), 0),
                ('RIGHTPADDING', (0, 0), (-1, -1), 0),
            ]))
            
            story.append(patient_table)
            story.append(Spacer(1, 25))
        
        # Terms and Conditions
        story.append(Paragraph("TERMS & CONDITIONS", section_header_style))
        
        # Terms style
        terms_style = ParagraphStyle(
            'Terms',
            parent=styles['Normal'],
            fontSize=9,
            leading=12,
            spaceBefore=0,
            spaceAfter=0,
            leftIndent=0,
            rightIndent=0
        )
        
        terms_text = """
        • This quote is valid for 30 days from the date of issue<br/>
        • Payment is due upon acceptance of services<br/>
        • Cancellation policy: 24-hour notice required<br/>
        • Weather and operational delays may affect scheduling<br/>
        • All flights subject to FAA regulations and crew duty time requirements<br/>
        • Medical equipment and staff included as specified
        """
        
        story.append(Paragraph(terms_text, terms_style))
        story.append(Spacer(1, 25))
        
        # Footer
        footer_style = ParagraphStyle(
            'Footer',
            parent=styles['Normal'],
            fontSize=8,
            textColor=colors.HexColor('#6B7280'),
            alignment=1,  # Center
            spaceBefore=0,
            spaceAfter=0,
            leading=10
        )
        
        story.append(Paragraph("Thank you for choosing JET ICU Medical Transport", footer_style))
        story.append(Paragraph("Your trusted partner in medical aviation", footer_style))
        
        # Build PDF
        doc.build(story)
        
        # Return PDF response
        buffer.seek(0)
        response = HttpResponse(buffer, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="quote_{quote.id.hex[:8]}.pdf"'
        return response
    
    @action(detail=True, methods=['post'])
    def generate_quote_document(self, request, pk=None):
        """
        Generate a Quote PDF document using the template and save it to nosign_out directory
        """
        import os
        from datetime import datetime
        from django.conf import settings
        from documents.templates.docs import populate_quote_pdf, QuoteData
        
        quote = self.get_object()
        
        try:
            # Prepare data for the quote document
            quote_data = QuoteData(
                quote_id=str(quote.id.hex[:8].upper()),
                inquiry_date=quote.inquiry_date.strftime('%Y-%m-%d') if quote.inquiry_date else '',
                patient_name=f"{quote.patient.info.first_name} {quote.patient.info.last_name}" if quote.patient and quote.patient.info else '',
                aircraft_type=dict(quote._meta.get_field('aircraft_type').choices).get(quote.aircraft_type, quote.aircraft_type),
                pickup_airport=f"{quote.pickup_airport.name} ({quote.pickup_airport.ident})" if quote.pickup_airport else '',
                dropoff_airport=f"{quote.dropoff_airport.name} ({quote.dropoff_airport.ident})" if quote.dropoff_airport else '',
                trip_date=quote.created_on.strftime('%Y-%m-%d') if quote.created_on else '',
                esitmated_flight_time=str(quote.estimated_flight_time) if quote.estimated_flight_time else '',
                number_of_stops=str(quote.number_of_stops),
                medical_team=dict(quote._meta.get_field('medical_team').choices).get(quote.medical_team, quote.medical_team),
                include_grounds='Yes' if quote.includes_grounds else 'No',
                our_availability='Available',
                amount=f"${quote.quoted_amount:,.2f}",
                notes=quote.notes if hasattr(quote, 'notes') else ''
            )
            
            # Define file paths
            template_path = os.path.join(settings.BASE_DIR, 'documents', 'templates', 'nosign_pdf', 'Quote.pdf')
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            output_filename = f"quote_{quote.id.hex[:8]}_{timestamp}.pdf"
            output_path = os.path.join(settings.BASE_DIR, 'documents', 'templates', 'nosign_out', output_filename)
            
            # Generate the PDF
            success = populate_quote_pdf(template_path, output_path, quote_data)
            
            if success:
                # Create Document record for tracking
                from .models import Document
                document = Document.objects.create(
                    filename=output_filename,
                    file_path=output_path,
                    document_type='quote',
                    created_by=request.user if request.user.is_authenticated else None
                )
                
                # Link document to trip that references this quote
                try:
                    trip = Trip.objects.get(quote_id=quote.id)
                    document.trip = trip
                    document.save()
                except Trip.DoesNotExist:
                    # No trip associated with this quote yet
                    pass
                
                return Response({
                    'success': True,
                    'message': 'Quote document generated successfully',
                    'filename': output_filename,
                    'path': output_path,
                    'document_id': str(document.id)
                }, status=status.HTTP_201_CREATED)
            else:
                return Response({
                    'success': False,
                    'message': 'Failed to generate quote document'
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                
        except Exception as e:
            return Response({
                'success': False,
                'message': f'Error generating quote document: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# Passenger ViewSet
class PassengerViewSet(BaseViewSet):
    queryset = Passenger.objects.select_related('info', 'passport_document')
    search_fields = ['info__first_name', 'info__last_name', 'nationality']
    ordering_fields = ['created_on']
    permission_classes = [
        permissions.IsAuthenticated,
        CanReadPassenger | CanWritePassenger | CanModifyPassenger | CanDeletePassenger
    ]
    
    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return PassengerReadSerializer
        return PassengerWriteSerializer
    
    def get_permissions(self):
        """
        Instantiate and return the list of permissions that this view requires.
        """
        if self.action == 'list' or self.action == 'retrieve':
            permission_classes = [permissions.IsAuthenticated, CanReadPassenger]
        elif self.action == 'create':
            permission_classes = [permissions.IsAuthenticated, CanWritePassenger]
        elif self.action in ['update', 'partial_update']:
            permission_classes = [permissions.IsAuthenticated, CanModifyPassenger]
        elif self.action == 'destroy':
            permission_classes = [permissions.IsAuthenticated, CanDeletePassenger]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]

# CrewLine ViewSet
class CrewLineViewSet(BaseViewSet):
    queryset = CrewLine.objects.select_related('primary_in_command', 'secondary_in_command').prefetch_related('medic_ids')
    ordering_fields = ['created_on']
    
    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return CrewLineReadSerializer
        return CrewLineWriteSerializer

# Trip ViewSet
class TripViewSet(BaseViewSet):
    queryset = Trip.objects.select_related('quote', 'patient', 'patient__info', 'aircraft').prefetch_related('trip_lines', 'passengers__info', 'events__airport', 'events__crew_line')
    search_fields = ['trip_number', 'type', 'patient__info__first_name', 'patient__info__last_name', 'passengers__info__first_name', 'passengers__info__last_name']
    ordering_fields = ['created_on', 'estimated_departure_time']
    permission_classes = [
        permissions.IsAuthenticated,
        CanReadTrip | CanWriteTrip | CanModifyTrip | CanDeleteTrip
    ]
    
    def generate_trip_number(self):
        """
        Generate a unique five-digit auto-incrementing trip number.
        Format: 00001, 00002, etc.
        """
        from django.db.models import Max
        import re
        
        # Get the highest existing trip number
        max_trip = Trip.objects.aggregate(max_num=Max('trip_number'))['max_num']
        
        if not max_trip:
            # First trip
            return '00001'
        
        # Extract numeric value from trip numbers (handle various formats)
        try:
            # Try to extract numeric part from trip number
            match = re.search(r'\d+', max_trip)
            if match:
                max_num = int(match.group())
            else:
                max_num = 0
        except (ValueError, AttributeError):
            # If we can't parse existing numbers, start fresh
            max_num = 0
        
        # Increment and format as 5-digit number
        new_num = max_num + 1
        return str(new_num).zfill(5)
    
    def get_serializer_class(self):
        if self.action in ('list', 'retrieve', 'trip_lines'):
            return TripReadSerializer
        return TripWriteSerializer
    
    def perform_create(self, serializer):
        """
        Override perform_create to automatically generate trip number if not provided.
        """
        # Check if trip_number is provided in the validated data
        if not serializer.validated_data.get('trip_number'):
            # Generate a unique trip number
            trip_number = self.generate_trip_number()
            
            # Ensure uniqueness (in case of race conditions)
            while Trip.objects.filter(trip_number=trip_number).exists():
                # If somehow the number exists, generate the next one
                import re
                match = re.search(r'\d+', trip_number)
                if match:
                    num = int(match.group()) + 1
                    trip_number = str(num).zfill(5)
                else:
                    # Fallback to timestamp if we can't parse
                    import time
                    trip_number = f"T{int(time.time())}"
            
            # Save with the generated trip number
            instance = serializer.save(created_by=self.request.user, trip_number=trip_number)
        else:
            # Trip number was provided, use it
            instance = serializer.save(created_by=self.request.user)
        
        # Track creation
        from .utils import track_creation
        track_creation(instance, self.request.user)
    
    def get_permissions(self):
        """
        Instantiate and return the list of permissions that this view requires.
        """
        if self.action == 'list' or self.action == 'retrieve' or self.action == 'trip_lines':
            permission_classes = [permissions.IsAuthenticated, CanReadTrip]
        elif self.action == 'create':
            permission_classes = [permissions.IsAuthenticated, CanWriteTrip]
        elif self.action in ['update', 'partial_update', 'generate_itineraries', 'generate_handling_requests']:
            permission_classes = [permissions.IsAuthenticated, CanModifyTrip]
        elif self.action == 'destroy':
            permission_classes = [permissions.IsAuthenticated, CanDeleteTrip]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]
    
    @action(detail=True, methods=['post'])
    def generate_itineraries(self, request, pk=None):
        """
        Generate itinerary documents - one per crew line in the trip
        """
        import os
        from datetime import datetime
        from django.conf import settings
        from documents.templates.docs import populate_itinerary_pdf, ItineraryData, CrewInfo, FlightLeg, AirportInfo, TimeInfo
        
        trip = self.get_object()
        generated_files = []
        
        try:
            # Get all crew lines for this trip
            crew_lines = CrewLine.objects.filter(trip_lines__trip=trip).distinct()
            
            if not crew_lines.exists():
                return Response({
                    'success': False,
                    'message': 'No crew lines found for this trip'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            for crew_line in crew_lines:
                # Prepare crew info
                crew_info = CrewInfo(
                    pic=f"{crew_line.primary_in_command.first_name} {crew_line.primary_in_command.last_name}" if crew_line.primary_in_command else '',
                    sic=f"{crew_line.secondary_in_command.first_name} {crew_line.secondary_in_command.last_name}" if crew_line.secondary_in_command else ''
                )
                
                # Add medical crew members
                medics = list(crew_line.medic_ids.all())
                if len(medics) > 0:
                    crew_info.med_1 = f"{medics[0].first_name} {medics[0].last_name}"
                if len(medics) > 1:
                    crew_info.med_2 = f"{medics[1].first_name} {medics[1].last_name}"
                if len(medics) > 2:
                    crew_info.med_4 = f"{medics[2].first_name} {medics[2].last_name}"
                
                # Prepare flight legs
                flight_legs = []
                trip_lines = trip.trip_lines.filter(crew_line=crew_line).order_by('departure_time_utc')
                
                for i, trip_line in enumerate(trip_lines, 1):
                    leg = FlightLeg(
                        leg=str(i),
                        departure_id=trip_line.origin_airport.ident if trip_line.origin_airport else '',
                        edt_utc_local=trip_line.departure_time_local.strftime('%H:%M %Z') if trip_line.departure_time_local else '',
                        arrival_id=trip_line.destination_airport.ident if trip_line.destination_airport else '',
                        flight_time=str(trip_line.flight_time) if trip_line.flight_time else '',
                        eta_utc_local=trip_line.arrival_time_local.strftime('%H:%M %Z') if trip_line.arrival_time_local else '',
                        ground_time=str(trip_line.ground_time) if trip_line.ground_time else '',
                        pax_leg='Yes' if trip_line.passenger_leg else 'No'
                    )
                    flight_legs.append(leg)
                
                # Prepare airport info
                airports = []
                all_airports = set()
                for trip_line in trip_lines:
                    all_airports.add(trip_line.origin_airport)
                    all_airports.add(trip_line.destination_airport)
                
                for airport in all_airports:
                    if airport:
                        airport_info = AirportInfo(
                            icao=airport.icao_code or airport.ident,
                            airport_city_name=airport.name,
                            state_country=f"{airport.iso_region}, {airport.iso_country}",
                            time_zone=getattr(airport, 'timezone', ''),
                            fbo_handler='',  # Will be populated from FBO data if available
                            freq='',
                            phone_fax='',
                            fuel=''
                        )
                        airports.append(airport_info)
                
                # Prepare timing info
                times = TimeInfo(
                    showtime='',
                    origin_edt=trip.estimated_departure_time.strftime('%H:%M %Z') if trip.estimated_departure_time else '',
                    total_flight_time='',
                    total_duty_time='',
                    pre_flight_duty_time=str(trip.pre_flight_duty_time) if trip.pre_flight_duty_time else '',
                    post_flight_duty_time=str(trip.post_flight_duty_time) if trip.post_flight_duty_time else ''
                )
                
                # Prepare passenger list
                passengers = []
                for passenger in trip.passengers.all():
                    if passenger.info:
                        passengers.append(f"{passenger.info.first_name} {passenger.info.last_name}")
                
                # Create itinerary data
                itinerary_data = ItineraryData(
                    trip_number=trip.trip_number or '',
                    tail_number=trip.aircraft.tail_number if trip.aircraft else '',
                    trip_date=trip.trip_lines.first().departure_time_local.strftime('%Y-%m-%d') if trip.trip_lines.exists() and trip.trip_lines.first().departure_time_local else '',
                    trip_type=trip.type.title() if trip.type else 'Charter',
                    patient_name=f"{trip.patient.info.first_name} {trip.patient.info.last_name}" if trip.patient and trip.patient.info else '',
                    bed_at_origin=trip.patient.bed_at_origin if trip.patient else False,
                    bed_at_dest=trip.patient.bed_at_destination if trip.patient else False,
                    special_instructions=trip.patient.special_instructions if trip.patient else trip.notes or '',
                    passengers=passengers,
                    crew=crew_info,
                    flight_legs=flight_legs,
                    airports=airports,
                    times=times
                )
                
                # Define file paths
                template_path = os.path.join(settings.BASE_DIR, 'documents', 'templates', 'nosign_pdf', 'itin.pdf')
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                output_filename = f"itin_{trip.trip_number}_crew_{crew_line.id.hex[:8]}_{timestamp}.pdf"
                output_path = os.path.join(settings.BASE_DIR, 'documents', 'templates', 'nosign_out', output_filename)
                
                # Generate the PDF
                success = populate_itinerary_pdf(template_path, output_path, itinerary_data)
                
                if success:
                    # Create Document record for tracking
                    from .models import Document
                    document = Document.objects.create(
                        filename=output_filename,
                        file_path=output_path,
                        document_type='customer_itinerary',
                        trip=trip,
                        created_by=request.user if request.user.is_authenticated else None
                    )
                    
                    generated_files.append({
                        'crew_line_id': str(crew_line.id),
                        'filename': output_filename,
                        'path': output_path,
                        'document_id': str(document.id)
                    })
                else:
                    return Response({
                        'success': False,
                        'message': f'Failed to generate itinerary for crew line {crew_line.id}'
                    }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
            return Response({
                'success': True,
                'message': f'Generated {len(generated_files)} itinerary documents',
                'files': generated_files
            }, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            return Response({
                'success': False,
                'message': f'Error generating itinerary documents: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    @action(detail=True, methods=['post'])
    def generate_handling_requests(self, request, pk=None):
        """
        Generate handling request documents - one per trip leg with FBO info from arriving airport
        """
        import os
        from datetime import datetime
        from django.conf import settings
        from documents.templates.docs import populate_handling_request_pdf, HandlingRequestData, PassengerInfo
        
        trip = self.get_object()
        generated_files = []
        
        try:
            # Get all trip lines for this trip
            trip_lines = trip.trip_lines.all().order_by('departure_time_utc')
            
            if not trip_lines.exists():
                return Response({
                    'success': False,
                    'message': 'No trip lines found for this trip'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            for trip_line in trip_lines:
                # Prepare aircraft data
                aircraft = trip.aircraft
                handling_data = HandlingRequestData(
                    company='JET Aviation Operations',
                    make=aircraft.make if aircraft else '',
                    model=aircraft.model if aircraft else '',
                    tail_number=aircraft.tail_number if aircraft else '',
                    serial_number=getattr(aircraft, 'serial_number', '') or '',
                    mgtow=str(getattr(aircraft, 'mgtow', '')) or '',
                    mission=trip.type.title() if trip.type else 'Charter',
                    depart_origin=trip_line.departure_time_local.strftime('%H:%M') if trip_line.departure_time_local else '',
                    arrive_dest=trip_line.arrival_time_local.strftime('%H:%M') if trip_line.arrival_time_local else '',
                    depart_dest='',  # For return legs - would need return trip line data
                    arrive_origin=''  # For return legs - would need return trip line data
                )
                
                # Prepare passenger information
                passengers = []
                for passenger in trip.passengers.all():
                    if passenger.info:
                        passenger_info = PassengerInfo(
                            name=f"{passenger.info.first_name} {passenger.info.last_name}",
                            title='',
                            nationality=getattr(passenger.info, 'nationality', '') or '',
                            date_of_birth=passenger.info.date_of_birth.strftime('%Y-%m-%d') if passenger.info.date_of_birth else '',
                            passport_number=getattr(passenger.info, 'passport_number', '') or '',
                            passport_expiration='',  # Would need passport expiration field
                            contact_number=passenger.info.phone or ''
                        )
                        passengers.append(passenger_info)
                
                # Add patient if exists and not already in passengers
                if trip.patient and trip.patient.info:
                    patient_already_added = any(
                        p.name == f"{trip.patient.info.first_name} {trip.patient.info.last_name}" 
                        for p in passengers
                    )
                    if not patient_already_added:
                        patient_info = PassengerInfo(
                            name=f"{trip.patient.info.first_name} {trip.patient.info.last_name}",
                            title='Patient',
                            nationality=getattr(trip.patient, 'nationality', ''),
                            date_of_birth=trip.patient.info.date_of_birth.strftime('%Y-%m-%d') if hasattr(trip.patient.info, 'date_of_birth') and trip.patient.info.date_of_birth else '',
                            passport_number='',
                            passport_expiration='',
                            contact_number=''
                        )
                        passengers.append(patient_info)
                
                handling_data.passengers = passengers
                
                # Define file paths
                template_path = os.path.join(settings.BASE_DIR, 'documents', 'templates', 'nosign_pdf', 'handling_request.pdf')
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                output_filename = f"handling_{trip.trip_number}_leg_{trip_line.id.hex[:8]}_{timestamp}.pdf"
                output_path = os.path.join(settings.BASE_DIR, 'documents', 'templates', 'nosign_out', output_filename)
                
                # Generate the PDF
                success = populate_handling_request_pdf(template_path, output_path, handling_data)
                
                if success:
                    # Create Document record for tracking
                    from .models import Document
                    document = Document.objects.create(
                        filename=output_filename,
                        file_path=output_path,
                        document_type='handling_request',
                        trip=trip,
                        created_by=request.user if request.user.is_authenticated else None
                    )
                    
                    generated_files.append({
                        'trip_line_id': str(trip_line.id),
                        'arrival_airport': trip_line.destination_airport.name if trip_line.destination_airport else '',
                        'arrival_fbo': trip_line.arrival_fbo.name if trip_line.arrival_fbo else 'N/A',
                        'filename': output_filename,
                        'path': output_path,
                        'document_id': str(document.id)
                    })
                else:
                    return Response({
                        'success': False,
                        'message': f'Failed to generate handling request for trip line {trip_line.id}'
                    }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
            return Response({
                'success': True,
                'message': f'Generated {len(generated_files)} handling request documents',
                'files': generated_files
            }, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            return Response({
                'success': False,
                'message': f'Error generating handling request documents: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    @action(detail=True, methods=['get'])
    def trip_lines(self, request, pk=None):
        trip = self.get_object()
        trip_lines = trip.trip_lines.all().order_by('departure_time_utc')
        serializer = TripLineReadSerializer(trip_lines, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def timeline(self, request, pk=None):
        trip = self.get_object()
        legs = TripLineReadSerializer(trip.trip_lines.all(), many=True).data
        for item in legs:
            item["timeline_type"] = "LEG"
            item["sort_at"] = item["departure_time_utc"]

        events = TripEventReadSerializer(trip.events.all(), many=True).data
        for item in events:
            item["timeline_type"] = "EVENT"
            item["sort_at"] = item["start_time_utc"]

        combined = sorted(chain(legs, events), key=lambda x: x["sort_at"] or "")
        return Response(combined)
    
    @action(detail=True, methods=['post'])
    def generate_documents(self, request, pk=None):
        """
        Generate PDF documents for a trip using PDF templates.
        Accepts optional 'document_type' in request body to generate specific document.
        If no document_type provided, generates all applicable documents.
        """
        import os
        from datetime import datetime
        from documents.templates.docs import populate_quote_pdf, QuoteData, populate_itinerary_pdf, ItineraryData, CrewInfo, FlightLeg, AirportInfo, TimeInfo, populate_handling_request_pdf, HandlingRequestData, PassengerInfo
        from .serializers import DocumentSerializer, DocumentCreateSerializer
        
        trip = self.get_object()
        
        # Validate request data
        serializer = DocumentCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        document_type = serializer.validated_data.get('document_type')
        
        try:
            generated_documents = []
            
            # Define base paths
            template_base_path = os.path.join(settings.BASE_DIR, 'documents', 'templates', 'nosign_pdf')
            output_base_path = os.path.join(settings.BASE_DIR, 'documents', 'generated')
            
            # Ensure output directory exists
            os.makedirs(output_base_path, exist_ok=True)
            
            # Available document generators
            document_generators = {
                'gendec': self._generate_gendec_pdf,
                'quote': self._generate_quote_pdf,
                'customer_itinerary': self._generate_itinerary_pdf,
                'internal_itinerary': self._generate_itinerary_pdf,
                'handling_request': self._generate_handling_request_pdf,
            }
            
            if document_type:
                # Generate specific document type
                if document_type in document_generators:
                    doc = document_generators[document_type](trip, template_base_path, output_base_path)
                    if doc:
                        generated_documents.append(doc)
                else:
                    return Response({
                        'error': f'Document type {document_type} not supported'
                    }, status=status.HTTP_400_BAD_REQUEST)
            else:
                # Generate all applicable documents
                for doc_type in ['quote', 'customer_itinerary', 'handling_request']:
                    try:
                        doc = document_generators[doc_type](trip, template_base_path, output_base_path)
                        if doc:
                            generated_documents.append(doc)
                    except Exception as e:
                        print(f"Error generating {doc_type}: {e}")
                        continue
            
            return Response({
                'message': f'{len(generated_documents)} documents generated successfully',
                'documents': DocumentSerializer(generated_documents, many=True).data
            }, status=status.HTTP_201_CREATED)
                
        except Exception as e:
            return Response({
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    @action(detail=True, methods=['get'])
    def documents(self, request, pk=None):
        """
        List all documents associated with a trip.
        """
        from .serializers import DocumentSerializer
        
        trip = self.get_object()
        documents = trip.documents.all().order_by('-created_on')
        serializer = DocumentSerializer(documents, many=True)
        return Response(serializer.data)

# Document ViewSet
class DocumentViewSet(BaseViewSet):
    queryset = Document.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    
    def get_serializer_class(self):
        from .serializers import DocumentSerializer
        return DocumentSerializer
    
    @action(detail=True, methods=['get'])
    def download(self, request, pk=None):
        """
        Download a document file.
        """
        from django.http import FileResponse
        from pathlib import Path
        
        document = self.get_object()
        
        if document.file_path and Path(document.file_path).exists():
            file_path = Path(document.file_path)
            response = FileResponse(
                open(file_path, 'rb'),
                content_type='application/octet-stream'
            )
            response['Content-Disposition'] = f'attachment; filename="{document.filename}"'
            return response
        elif document.content:
            # Fallback to binary content if stored in database
            response = HttpResponse(document.content, content_type='application/octet-stream')
            response['Content-Disposition'] = f'attachment; filename="{document.filename}"'
            return response
        else:
            return Response(
                {'error': 'Document file not found'},
                status=status.HTTP_404_NOT_FOUND
            )

# TripLine ViewSet
class TripLineViewSet(BaseViewSet):
    queryset = TripLine.objects.select_related('trip', 'origin_airport', 'destination_airport', 'crew_line')
    ordering_fields = ['departure_time_utc', 'created_on']
    permission_classes = [
        permissions.IsAuthenticated,
        CanReadTripLine | CanWriteTripLine | CanModifyTripLine | CanDeleteTripLine
    ]
    
    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return TripLineReadSerializer
        return TripLineWriteSerializer
    
    def get_permissions(self):
        """
        Instantiate and return the list of permissions that this view requires.
        """
        if self.action == 'list' or self.action == 'retrieve':
            permission_classes = [permissions.IsAuthenticated, CanReadTripLine]
        elif self.action == 'create':
            permission_classes = [permissions.IsAuthenticated, CanWriteTripLine]
        elif self.action in ['update', 'partial_update']:
            permission_classes = [permissions.IsAuthenticated, CanModifyTripLine]
        elif self.action == 'destroy':
            permission_classes = [permissions.IsAuthenticated, CanDeleteTripLine]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]
    
    def perform_create(self, serializer):
        trip_line = serializer.save(created_by=self.request.user)
        trip = trip_line.trip
        
        # Recalculate times for all trip lines in this trip
        if trip.estimated_departure_time:
            self.recalculate_trip_times(trip)
    
    def perform_update(self, serializer):
        trip_line = serializer.save()
        trip = trip_line.trip
        
        # Recalculate times for all trip lines in this trip
        if trip.estimated_departure_time:
            self.recalculate_trip_times(trip)
    
    def recalculate_trip_times(self, trip):
        # This is a placeholder for the actual time calculation logic
        # In a real implementation, this would update all trip lines based on
        # the trip's estimated departure time and the flight/ground times of each leg
        pass

# Modification ViewSet for tracking changes
class ModificationViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Modification.objects.all()
    serializer_class = ModificationSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['model', 'field']
    ordering_fields = ['time']
    
    @action(detail=False, methods=['get'])
    def for_object(self, request):
        model = request.query_params.get('model')
        object_id = request.query_params.get('object_id')
        
        if not model or not object_id:
            return Response({"detail": "Missing parameters"}, status=status.HTTP_400_BAD_REQUEST)
            
        modifications = Modification.objects.filter(
            model=model,
            object_id=object_id
        ).order_by('-time')
        
        serializer = self.get_serializer(modifications, many=True)
        return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def dashboard_stats(request):
    """
    Get dashboard statistics for JET ICU Operations
    """
    from django.db.models import Count, Sum, Q
    from datetime import datetime, timedelta
    from django.utils import timezone
    
    now = timezone.now()
    thirty_days_ago = now - timedelta(days=30)
    
    # Trip statistics
    total_trips = Trip.objects.count()
    active_trips = Trip.objects.filter(
        Q(estimated_departure_time__gte=now) | 
        Q(estimated_departure_time__isnull=True)
    ).exclude(status='completed').count()
    
    completed_trips_30_days = Trip.objects.filter(
        status='completed',
        created_on__gte=thirty_days_ago
    ).count()
    
    # Quote statistics
    total_quotes = Quote.objects.count()
    pending_quotes = Quote.objects.filter(status='pending').count()
    active_quotes = Quote.objects.filter(status='active').count()
    completed_quotes = Quote.objects.filter(status='completed').count()
    
    # Patient statistics
    total_patients = Patient.objects.count()
    active_patients = Patient.objects.filter(status__in=['confirmed', 'active']).count()
    
    # Aircraft statistics
    total_aircraft = Aircraft.objects.count()
    
    # Financial statistics
    total_revenue = Quote.objects.filter(
        status__in=['completed', 'paid']
    ).aggregate(Sum('quoted_amount'))['quoted_amount__sum'] or 0
    
    pending_revenue = Quote.objects.filter(
        status='active'
    ).aggregate(Sum('quoted_amount'))['quoted_amount__sum'] or 0
    
    # Recent activity
    recent_quotes = Quote.objects.filter(
        created_on__gte=thirty_days_ago
    ).order_by('-created_on')[:5]
    
    recent_trips = Trip.objects.filter(
        created_on__gte=thirty_days_ago
    ).order_by('-created_on')[:5]
    
    # Trip types breakdown
    trip_types = Trip.objects.values('type').annotate(count=Count('type'))
    
    # Status breakdown for quotes
    quote_statuses = Quote.objects.values('status').annotate(count=Count('status'))
    
    return Response({
        'trip_stats': {
            'total': total_trips,
            'active': active_trips,
            'completed_30_days': completed_trips_30_days,
            'types_breakdown': list(trip_types)
        },
        'quote_stats': {
            'total': total_quotes,
            'pending': pending_quotes,
            'active': active_quotes,
            'completed': completed_quotes,
            'statuses_breakdown': list(quote_statuses)
        },
        'patient_stats': {
            'total': total_patients,
            'active': active_patients
        },
        'aircraft_stats': {
            'total': total_aircraft
        },
        'financial_stats': {
            'total_revenue': float(total_revenue),
            'pending_revenue': float(pending_revenue)
        },
        'recent_activity': {
            'quotes': [
                {
                    'id': str(q.id),
                    'amount': float(q.quoted_amount),
                    'status': q.status,
                    'created_on': q.created_on,
                    'patient_name': f"{q.patient.info.first_name or ''} {q.patient.info.last_name or ''}".strip() if q.patient and q.patient.info else 'No patient'
                } for q in recent_quotes
            ],
            'trips': [
                {
                    'id': str(t.id),
                    'trip_number': t.trip_number,
                    'type': t.type,
                    'status': t.status,
                    'created_on': t.created_on,
                    'estimated_departure': t.estimated_departure_time
                } for t in recent_trips
            ]
        }
    })


class StaffViewSet(BaseViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Staff.objects.select_related("contact").all().order_by("-created_on")
    search_fields = ['contact__first_name', 'contact__last_name', 'contact__business_name', 'contact__email']

    def get_serializer_class(self):
        if self.action in ("list", "retrieve"):
            return StaffReadSerializer
        return StaffWriteSerializer


class StaffRoleViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = StaffRole.objects.all().order_by("code")
    serializer_class = StaffRoleSerializer
    
    def perform_create(self, serializer):
        instance = serializer.save(created_by=self.request.user)
        track_creation(instance, self.request.user)
    
    def perform_update(self, serializer):
        instance = serializer.save(modified_by=self.request.user)
        # Updates are automatically tracked by signals
        
    def perform_destroy(self, instance):
        track_deletion(instance, self.request.user)
        instance.delete()


class StaffRoleMembershipViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = StaffRoleMembership.objects.select_related("staff", "role").all().order_by("-created_on")

    def get_queryset(self):
        queryset = super().get_queryset()
        # Filter by staff_id if provided
        staff_id = self.request.query_params.get('staff_id', None)
        if staff_id is not None:
            queryset = queryset.filter(staff_id=staff_id)
        return queryset

    def get_serializer_class(self):
        if self.action in ("list", "retrieve"):
            return StaffRoleMembershipReadSerializer
        return StaffRoleMembershipWriteSerializer
    
    def perform_create(self, serializer):
        instance = serializer.save(created_by=self.request.user)
        track_creation(instance, self.request.user)
    
    def perform_update(self, serializer):
        instance = serializer.save(modified_by=self.request.user)
        # Updates are automatically tracked by signals
        
    def perform_destroy(self, instance):
        track_deletion(instance, self.request.user)
        instance.delete()


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_contact_with_related(request):
    """
    Unified endpoint for creating contacts with related records (Patient, Staff, Passenger, Customer)
    
    POST /api/contacts/create-with-related/
    
    Body:
    {
        "first_name": "John",
        "last_name": "Doe", 
        "email": "john.doe@example.com",
        "phone": "+1234567890",
        "date_of_birth": "1990-01-01",
        "passport_number": "123456789",
        "passport_expiration_date": "2030-01-01",
        "nationality": "US",
        "related_type": "patient",  // "patient", "staff", "passenger", "customer"
        "related_data": {
            "special_instructions": "Requires wheelchair assistance",
            "bed_at_origin": true,
            "status": "confirmed"
        }
    }
    """
    serializer = ContactCreationSerializer(data=request.data, context={'request': request})
    
    if serializer.is_valid():
        try:
            result = serializer.save()
            
            # Return appropriate response based on related type
            contact = result['contact']
            related_instance = result['related_instance']
            related_type = result['related_type']
            
            response_data = {
                'contact': ContactSerializer(contact).data,
                'related_type': related_type,
                'success': True,
                'message': f'{related_type.capitalize()} created successfully'
            }
            
            # Add specific related data
            if related_type == 'patient':
                from .serializers import PatientReadSerializer
                response_data['patient'] = PatientReadSerializer(related_instance).data
            elif related_type == 'staff':
                response_data['staff'] = StaffReadSerializer(related_instance).data
            elif related_type == 'passenger':
                from .serializers import PassengerReadSerializer
                response_data['passenger'] = PassengerReadSerializer(related_instance).data
            elif related_type == 'customer':
                response_data['customer'] = ContactSerializer(related_instance).data
            
            return Response(response_data, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            return Response({
                'error': str(e),
                'success': False
            }, status=status.HTTP_400_BAD_REQUEST)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class TripEventViewSet(BaseViewSet):
    queryset = TripEvent.objects.select_related("trip", "airport", "crew_line")
    ordering_fields = ["start_time_utc", "created_on"]

    def get_serializer_class(self):
        return (TripEventReadSerializer
                if self.action in ("list", "retrieve")
                else TripEventWriteSerializer)


class CommentViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing comments on any model instance.
    Supports filtering by content_type and object_id.
    """
    queryset = Comment.objects.select_related('created_by', 'content_type').order_by('-created_on')
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['text']
    ordering_fields = ['created_on', 'modified_on']
    pagination_class = StandardPagination
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Filter by content_type and object_id if provided
        content_type = self.request.query_params.get('content_type')
        object_id = self.request.query_params.get('object_id')
        
        if content_type:
            # Support both model name and content_type id
            if content_type.isdigit():
                queryset = queryset.filter(content_type_id=content_type)
            else:
                from django.contrib.contenttypes.models import ContentType
                try:
                    ct = ContentType.objects.get(model=content_type.lower())
                    queryset = queryset.filter(content_type=ct)
                except ContentType.DoesNotExist:
                    queryset = queryset.none()
        
        if object_id:
            queryset = queryset.filter(object_id=object_id)
        
        return queryset
    
    def perform_create(self, serializer):
        instance = serializer.save(created_by=self.request.user, modified_by=self.request.user)
        # Track creation
        track_creation(instance, self.request.user)
    
    def perform_update(self, serializer):
        instance = serializer.save(modified_by=self.request.user)
        # Updates are automatically tracked by signals
        
    def perform_destroy(self, instance):
        # Track deletion before destroying
        track_deletion(instance, self.request.user)
        instance.delete()
    
    @action(detail=False, methods=['get'])
    def for_object(self, request):
        """Get all comments for a specific object"""
        model_name = request.query_params.get('model')
        object_id = request.query_params.get('object_id')
        
        if not model_name or not object_id:
            return Response(
                {'error': 'Both model and object_id parameters are required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        from django.contrib.contenttypes.models import ContentType
        try:
            content_type = ContentType.objects.get(model=model_name.lower())
            comments = self.get_queryset().filter(
                content_type=content_type,
                object_id=object_id
            )
            serializer = self.get_serializer(comments, many=True)
            return Response(serializer.data)
        except ContentType.DoesNotExist:
            return Response(
                {'error': f'Model {model_name} not found'},
                status=status.HTTP_404_NOT_FOUND
            )


# Timezone utility API endpoints
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_airport_timezone_info(request, airport_id):
    """
    Get timezone information for a specific airport at a given datetime
    Query params: datetime (ISO format, optional - defaults to current time)
    """
    try:
        from .models import Airport
        from .timezone_utils import get_timezone_info
        from datetime import datetime
        import pytz
        
        airport = Airport.objects.get(id=airport_id)
        
        if not airport.timezone:
            return Response({
                'error': 'Airport does not have timezone information'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Parse datetime from query params or use current time
        dt_param = request.query_params.get('datetime')
        if dt_param:
            try:
                dt = datetime.fromisoformat(dt_param.replace('Z', '+00:00'))
            except ValueError:
                return Response({
                    'error': 'Invalid datetime format. Use ISO format (e.g., 2023-12-25T14:30:00Z)'
                }, status=status.HTTP_400_BAD_REQUEST)
        else:
            from django.utils import timezone as django_timezone
            dt = django_timezone.now()
        
        tz_info = get_timezone_info(airport.timezone, dt)
        tz_info['airport'] = {
            'id': airport.id,
            'name': airport.name,
            'ident': airport.ident,
            'timezone': airport.timezone
        }
        
        return Response(tz_info)
        
    except Airport.DoesNotExist:
        return Response({
            'error': 'Airport not found'
        }, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({
            'error': f'Error getting timezone info: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def validate_flight_times(request):
    """
    Validate timezone consistency between local and UTC times for flight legs
    
    Request body:
    {
        "departure_airport_id": "uuid",
        "departure_local": "2023-12-25T14:30:00",
        "departure_utc": "2023-12-25T19:30:00Z",
        "arrival_airport_id": "uuid", 
        "arrival_local": "2023-12-25T16:30:00",
        "arrival_utc": "2023-12-25T21:30:00Z"
    }
    """
    try:
        from .models import Airport
        from .timezone_utils import validate_time_consistency, check_dst_transition_warning, calculate_flight_duration_with_timezones
        from datetime import datetime
        
        data = request.data
        
        # Parse departure info
        dep_airport_id = data.get('departure_airport_id')
        dep_local_str = data.get('departure_local')
        dep_utc_str = data.get('departure_utc')
        
        # Parse arrival info
        arr_airport_id = data.get('arrival_airport_id')
        arr_local_str = data.get('arrival_local')
        arr_utc_str = data.get('arrival_utc')
        
        if not all([dep_airport_id, dep_local_str, dep_utc_str]):
            return Response({
                'error': 'departure_airport_id, departure_local, and departure_utc are required'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        dep_airport = Airport.objects.get(id=dep_airport_id)
        
        # Parse departure times
        dep_local = datetime.fromisoformat(dep_local_str.replace('Z', '+00:00')).replace(tzinfo=None)
        dep_utc = datetime.fromisoformat(dep_utc_str.replace('Z', '+00:00'))
        
        results = {
            'departure_valid': False,
            'arrival_valid': False,
            'warnings': []
        }
        
        # Validate departure times
        if dep_airport.timezone:
            results['departure_valid'] = validate_time_consistency(dep_local, dep_utc, dep_airport.timezone)
            
            # Check for DST warnings
            dst_warning = check_dst_transition_warning(dep_local, dep_airport.timezone)
            if dst_warning:
                results['warnings'].append(f"Departure: {dst_warning['message']}")
        
        # Validate arrival times if provided
        if arr_airport_id and arr_local_str and arr_utc_str:
            arr_airport = Airport.objects.get(id=arr_airport_id)
            arr_local = datetime.fromisoformat(arr_local_str.replace('Z', '+00:00')).replace(tzinfo=None)
            arr_utc = datetime.fromisoformat(arr_utc_str.replace('Z', '+00:00'))
            
            if arr_airport.timezone:
                results['arrival_valid'] = validate_time_consistency(arr_local, arr_utc, arr_airport.timezone)
                
                # Check for DST warnings
                dst_warning = check_dst_transition_warning(arr_local, arr_airport.timezone)
                if dst_warning:
                    results['warnings'].append(f"Arrival: {dst_warning['message']}")
                
                # Calculate flight duration with timezone info
                duration, info = calculate_flight_duration_with_timezones(
                    dep_local, dep_airport.timezone,
                    arr_local, arr_airport.timezone
                )
                
                results['flight_duration_hours'] = duration
                results['flight_info'] = info
        
        results['overall_valid'] = results['departure_valid'] and (
            results['arrival_valid'] if 'arrival_valid' in results and arr_airport_id else True
        )
        
        return Response(results)
        
    except Airport.DoesNotExist:
        return Response({
            'error': 'Airport not found'
        }, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({
            'error': f'Validation error: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def convert_timezone(request):
    """
    Convert departure time + flight duration to arrival time accounting for timezones
    Used by frontend forms to display correct arrival times
    """
    try:
        departure_date = request.data.get('departure_date')
        departure_time = request.data.get('departure_time')
        flight_time_hours = request.data.get('flight_time_hours')
        origin_timezone = request.data.get('origin_timezone')
        destination_timezone = request.data.get('destination_timezone')
        
        if not all([departure_date, departure_time, flight_time_hours, origin_timezone, destination_timezone]):
            return Response({
                'error': 'Missing required fields: departure_date, departure_time, flight_time_hours, origin_timezone, destination_timezone'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        from .timezone_utils import convert_local_to_utc, convert_utc_to_local
        from datetime import datetime, timedelta
        
        # Create departure datetime
        departure_local = datetime.strptime(f"{departure_date} {departure_time}:00", "%Y-%m-%d %H:%M:%S")
        
        # Convert to UTC using origin timezone
        departure_utc = convert_local_to_utc(departure_local, origin_timezone)
        
        # Add flight time
        arrival_utc = departure_utc + timedelta(hours=float(flight_time_hours))
        
        # Convert to destination local time
        arrival_local = convert_utc_to_local(arrival_utc, destination_timezone)
        
        return Response({
            'arrival_date': arrival_local.date().isoformat(),
            'arrival_time': arrival_local.time().strftime('%H:%M'),
            'departure_utc': departure_utc.isoformat(),
            'arrival_utc': arrival_utc.isoformat(),
            'flight_duration_hours': float(flight_time_hours)
        })
        
    except Exception as e:
        return Response({
            'error': f'Timezone conversion error: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# Contract ViewSet
class ContractViewSet(BaseViewSet):
    queryset = Contract.objects.all()
    search_fields = ['title', 'contract_type', 'signer_email', 'status']
    ordering_fields = ['created_on', 'date_sent', 'date_signed', 'status']
    filterset_fields = ['contract_type', 'status', 'trip']
    
    def get_queryset(self):
        """Override to add custom filtering for trip parameter."""
        queryset = super().get_queryset()
        
        # Handle both DRF Request objects and regular Django requests
        if hasattr(self.request, 'query_params'):
            params = self.request.query_params
        else:
            params = self.request.GET
        
        # Filter by trip if provided
        trip_id = params.get('trip', None)
        if trip_id:
            queryset = queryset.filter(trip_id=trip_id)
            
        # Filter by contract type if provided
        contract_type = params.get('contract_type', None)
        if contract_type:
            queryset = queryset.filter(contract_type=contract_type)
            
        # Filter by status if provided
        status_filter = params.get('status', None)
        if status_filter:
            queryset = queryset.filter(status=status_filter)
            
        return queryset
    
    def get_serializer_class(self):
        """Return appropriate serializer based on action."""
        if self.action in ['list', 'retrieve']:
            return ContractReadSerializer
        elif self.action == 'create_from_trip':
            return ContractCreateFromTripSerializer
        elif self.action in ['send_for_signature', 'docuseal_action']:
            return ContractDocuSealActionSerializer
        return ContractWriteSerializer
    
    @action(detail=False, methods=['post'])
    def create_from_trip(self, request):
        """Create multiple contracts for a trip."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        trip = serializer.validated_data['trip_id']
        contract_types = serializer.validated_data['contract_types']
        send_immediately = serializer.validated_data.get('send_immediately', False)
        custom_signer_email = serializer.validated_data.get('custom_signer_email')
        custom_signer_name = serializer.validated_data.get('custom_signer_name')
        manual_price = serializer.validated_data.get('manual_price')
        manual_price_description = serializer.validated_data.get('manual_price_description')
        
        try:
            # Get customer contact from quote
            customer_contact = None
            if trip.quote and hasattr(trip.quote, 'contact'):
                customer_contact = trip.quote.contact
            
            logger.info(f"Trip {trip.trip_number}: quote={bool(trip.quote)}, customer_contact={bool(customer_contact)}")
            patient = trip.patient
            
            # Determine signer details with fallback logic
            if custom_signer_email:
                signer_email = custom_signer_email
                signer_name = custom_signer_name or ''
            elif customer_contact:
                # Primary: Use quote's customer contact
                signer_email = customer_contact.email
                signer_name = f"{customer_contact.first_name} {customer_contact.last_name}".strip()
            elif patient and patient.info:
                # Fallback: Use patient contact info
                signer_email = patient.info.email
                signer_name = f"{patient.info.first_name} {patient.info.last_name}".strip()
                logger.info(f"Using patient as signer for trip {trip.trip_number}")
            else:
                # Check if payment agreement is requested without pricing info
                if 'payment_agreement' in contract_types and not trip.quote:
                    return Response({
                        'error': 'Payment agreement requires a quote with pricing information, or provide custom_signer_email and manual pricing'
                    }, status=status.HTTP_400_BAD_REQUEST)
                else:
                    return Response({
                        'error': 'No signer information available. Please provide custom_signer_email or ensure trip has a quote with customer contact or patient with contact info.'
                    }, status=status.HTTP_400_BAD_REQUEST)
            
            contracts_created = []
            docuseal_service = DocuSealService()
            
            for contract_type in contract_types:
                # Generate contract title
                contract_type_display = dict(Contract.CONTRACT_TYPES)[contract_type]
                title = f"{contract_type_display} - {trip.trip_number}"
                
                # Create contract
                contract = Contract.objects.create(
                    title=title,
                    contract_type=contract_type,
                    trip=trip,
                    customer_contact=customer_contact,
                    patient=patient,
                    signer_email=signer_email,
                    signer_name=signer_name,
                    created_by=request.user
                )
                
                contracts_created.append(contract)
                
                # If send_immediately is True, attempt to send via DocuSeal
                if send_immediately:
                    try:
                        logger.info(f"Attempting to send contract {contract.id} for signature")
                        result = self._send_contract_for_signature(contract, docuseal_service, manual_price, manual_price_description)
                        logger.info(f"Successfully sent contract {contract.id}: {result}")
                    except Exception as e:
                        logger.error(f"Failed to send contract {contract.id}: {str(e)}", exc_info=True)
                        contract.status = 'failed'
                        contract.notes = f"Failed to send: {str(e)}"
                        contract.save()
            
            # Serialize created contracts
            serializer = ContractReadSerializer(contracts_created, many=True)
            
            return Response({
                'message': f'Created {len(contracts_created)} contracts',
                'contracts': serializer.data
            }, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            logger.error(f"Failed to create contracts: {str(e)}")
            return Response({
                'error': f'Failed to create contracts: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    @action(detail=True, methods=['post'])
    def send_for_signature(self, request, pk=None):
        """Send contract to DocuSeal for signature."""
        contract = self.get_object()
        
        try:
            docuseal_service = DocuSealService()
            result = self._send_contract_for_signature(contract, docuseal_service)
            
            serializer = ContractReadSerializer(contract)
            return Response({
                'message': 'Contract sent for signature',
                'contract': serializer.data,
                'docuseal_response': result
            })
            
        except Exception as e:
            logger.error(f"Failed to send contract for signature: {str(e)}")
            return Response({
                'error': f'Failed to send contract: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    @action(detail=True, methods=['post'])
    def docuseal_action(self, request, pk=None):
        """Perform DocuSeal-specific actions on contract."""
        contract = self.get_object()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        action_type = serializer.validated_data['action']
        custom_message = serializer.validated_data.get('custom_message', '')
        
        try:
            docuseal_service = DocuSealService()
            
            if action_type == 'send_for_signature':
                result = self._send_contract_for_signature(contract, docuseal_service)
                message = 'Contract sent for signature'
                
            elif action_type == 'resend':
                result = self._resend_contract(contract, docuseal_service)
                message = 'Contract resent'
                
            elif action_type == 'cancel':
                result = self._cancel_contract(contract, docuseal_service)
                message = 'Contract cancelled'
                
            elif action_type == 'archive':
                result = self._archive_contract(contract, docuseal_service)
                message = 'Contract archived'
                
            else:
                return Response({
                    'error': f'Unknown action: {action_type}'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            contract_serializer = ContractReadSerializer(contract)
            return Response({
                'message': message,
                'contract': contract_serializer.data,
                'docuseal_response': result
            })
            
        except Exception as e:
            logger.error(f"DocuSeal action failed: {str(e)}")
            return Response({
                'error': f'Action failed: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def _send_contract_for_signature(self, contract, docuseal_service, manual_price=None, manual_price_description=None):
        """Helper method to send contract for signature."""
        from django.conf import settings
        
        # Get template configuration
        template_config = settings.DOCUSEAL_CONTRACT_SETTINGS['templates'].get(contract.contract_type)
        if not template_config:
            raise ValueError(f"No template configuration found for contract type: {contract.contract_type}")
        
        # Use the pre-configured template ID
        template_id = template_config['template_id']
        requires_jet_icu_signature = template_config.get('requires_jet_icu_signature', False)
        
        # Prepare data for field mapping
        trip_data = {
            'trip_number': contract.trip.trip_number,
            'type': contract.trip.type,
            'estimated_departure_time': str(contract.trip.estimated_departure_time) if contract.trip.estimated_departure_time else '',
            'notes': contract.trip.notes or '',
        }
        
        # Get trip lines data - pass as objects for easier access
        trip_lines_data = list(contract.trip.trip_lines.all().order_by('departure_time_utc'))
        
        # Get quote data if available, otherwise use manual pricing
        quote_data = None
        if contract.trip.quote:
            quote_data = {
                'quoted_amount': str(contract.trip.quote.quoted_amount)
            }
        elif manual_price is not None:
            quote_data = {
                'quoted_amount': str(manual_price)
            }
        
        # Get contact data
        contact_data = None
        if contract.customer_contact:
            contact_data = {
                'first_name': contract.customer_contact.first_name or '',
                'last_name': contract.customer_contact.last_name or '',
                'business_name': contract.customer_contact.business_name or '',
                'email': contract.customer_contact.email or '',
                'phone': contract.customer_contact.phone or '',
                'address_line1': contract.customer_contact.address_line1 or '',
                'address_line2': contract.customer_contact.address_line2 or '',
                'city': contract.customer_contact.city or '',
                'state': contract.customer_contact.state or '',
                'zip': contract.customer_contact.zip or '',
                'country': contract.customer_contact.country or '',
            }
        
        # Get patient data
        patient_data = None
        if contract.patient:
            patient_data = {
                'info': {
                    'first_name': contract.patient.info.first_name or '',
                    'last_name': contract.patient.info.last_name or '',
                    'phone': contract.patient.info.phone or '',
                    'address_line1': contract.patient.info.address_line1 or '',
                    'city': contract.patient.info.city or '',
                    'state': contract.patient.info.state or '',
                    'zip': contract.patient.info.zip or '',
                },
                'date_of_birth': str(contract.patient.date_of_birth) if contract.patient.date_of_birth else '',
                'nationality': contract.patient.nationality or '',
                'passport_number': contract.patient.passport_number or '',
                'special_instructions': contract.patient.special_instructions or '',
            }
        
        # Get passengers data
        passengers = contract.trip.passengers.all()
        passengers_data = []
        for passenger in passengers:
            passengers_data.append({
                'info': {
                    'first_name': passenger.info.first_name or '',
                    'last_name': passenger.info.last_name or '',
                }
            })
        
        # Generate field mappings based on contract type
        fields = docuseal_service.create_contract_fields_mapping(
            contract_type=contract.contract_type,
            trip_data=trip_data,
            trip_lines_data=trip_lines_data,
            contact_data=contact_data,
            patient_data=patient_data,
            passengers_data=passengers_data,
            quote_data=quote_data
        )
        
        # Get roles from template configuration
        customer_role = template_config.get('customer_role', 'patient')
        jet_icu_role = template_config.get('jet_icu_role', 'jet_icu')
        
        # Prepare submitters list - assign fields to JET ICU role as requested
        if requires_jet_icu_signature:
            # For contracts requiring JET ICU signature, customer signs but JET ICU gets the field data
            submitters = [
                {
                    'name': contract.signer_name,
                    'email': contract.signer_email,
                    'role': customer_role,
                    'fields': {}  # Customer doesn't fill fields, just signs
                },
                {
                    'name': 'JET ICU Representative', 
                    'email': settings.DOCUSEAL_JET_ICU_SIGNER_EMAIL,
                    'role': jet_icu_role,
                    'fields': fields  # JET ICU gets all the field data
                }
            ]
        else:
            # For single-signature contracts, assign fields to the JET ICU role (First Party)
            submitters = [
                {
                    'name': contract.signer_name,
                    'email': contract.signer_email, 
                    'role': customer_role,
                    'fields': {}  # Customer signs as Second Party with no fields
                },
                {
                    'name': 'JET ICU Representative',
                    'email': settings.DOCUSEAL_JET_ICU_SIGNER_EMAIL,
                    'role': jet_icu_role,
                    'fields': fields  # JET ICU (First Party) gets all the field data
                }
            ]
        
        # Store template ID in contract
        contract.docuseal_template_id = template_id
        
        # Create submission
        submission_result = docuseal_service.create_submission(
            template_id=template_id,
            submitters=submitters,
            send_email=True
        )
        
        # DocuSeal returns an array of submitters, get the submission_id from the first one
        if isinstance(submission_result, list) and len(submission_result) > 0:
            first_submitter = submission_result[0]
            submission_id = first_submitter.get('submission_id')
            
            # Update contract
            contract.docuseal_submission_id = str(submission_id)
            contract.status = 'pending'
            contract.date_sent = timezone.now()
            contract.docuseal_response_data = {
                'submitters': submission_result,
                'submission_id': submission_id
            }
            contract.save()
            
            logger.info(f"Contract {contract.id} updated with submission_id: {submission_id}")
        else:
            logger.error(f"Unexpected DocuSeal response format: {type(submission_result)}")
            raise ValueError("Unexpected DocuSeal response format")
        
        return submission_result
    
    def _generate_contract_summary(self, contract):
        """Generate a summary of contract details for logging/display."""
        from django.conf import settings
        template_config = settings.DOCUSEAL_CONTRACT_SETTINGS['templates'].get(contract.contract_type, {})
        return {
            'contract_id': str(contract.id),
            'contract_type': contract.contract_type,
            'template_id': template_config.get('template_id'),
            'template_name': template_config.get('name'),
            'trip_number': contract.trip.trip_number,
            'signer_email': contract.signer_email,
            'requires_jet_icu_signature': template_config.get('requires_jet_icu_signature', False)
        }
    
    def _resend_contract(self, contract, docuseal_service):
        """Resend existing contract."""
        # Implementation for resending would go here
        contract.date_sent = timezone.now()
        contract.save()
        return {'status': 'resent'}
    
    def _cancel_contract(self, contract, docuseal_service):
        """Cancel contract."""
        contract.status = 'cancelled'
        contract.save()
        return {'status': 'cancelled'}
    
    def _archive_contract(self, contract, docuseal_service):
        """Archive contract."""
        if contract.docuseal_submission_id:
            result = docuseal_service.archive_submission(contract.docuseal_submission_id)
            contract.status = 'cancelled'
            contract.save()
            return result
        return {'status': 'archived'}


# DocuSeal Webhook Handler
@api_view(['POST'])
@permission_classes([])  # Allow unauthenticated access for webhooks
def docuseal_webhook(request):
    """Handle DocuSeal webhook events."""
    try:
        # Validate webhook (in production, you'd verify the signature)
        webhook_data = request.data
        
        # Process webhook
        docuseal_service = DocuSealService()
        processed_event = docuseal_service.process_webhook_event(webhook_data)
        
        submission_id = processed_event.get('submission_id')
        event_type = processed_event.get('event_type')
        
        if submission_id:
            # Find contract by submission ID
            try:
                contract = Contract.objects.get(docuseal_submission_id=submission_id)
                
                # Update contract based on event type
                if event_type == 'form.completed':
                    contract.status = 'signed'
                    contract.date_signed = timezone.now()
                    
                    # Download signed document
                    try:
                        signed_doc_content = docuseal_service.get_submission_documents(submission_id)
                        
                        # Create Document record for signed document
                        signed_document = Document.objects.create(
                            filename=f"{contract.title}_signed.pdf",
                            content=signed_doc_content,
                            document_type='contract',
                            trip=contract.trip,
                            created_by_id=1  # System user
                        )
                        contract.signed_document = signed_document
                        
                    except Exception as e:
                        logger.error(f"Failed to download signed document: {str(e)}")
                
                elif event_type == 'form.viewed':
                    # Contract was viewed but not necessarily completed
                    pass
                    
                elif event_type == 'form.started':
                    # Signing process started
                    pass
                
                # Update response data
                contract.docuseal_response_data.update({
                    'last_webhook_event': processed_event,
                    'last_webhook_time': timezone.now().isoformat()
                })
                contract.save()
                
                logger.info(f"Updated contract {contract.id} from webhook event {event_type}")
                
            except Contract.DoesNotExist:
                logger.warning(f"No contract found for submission ID: {submission_id}")
        
        return Response({'status': 'processed'}, status=status.HTTP_200_OK)
        
    except Exception as e:
        logger.error(f"DocuSeal webhook processing failed: {str(e)}")
        return Response({
            'error': 'Webhook processing failed'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

```


# File: api/models.py

```python
from django.db import models
from django.contrib.auth.models import User
import uuid
from django.utils import timezone
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

# Base model with default fields
class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="%(class)s_created")
    modified_on = models.DateTimeField(auto_now=True)
    modified_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True, related_name="%(class)s_modified"
    )
    status = models.CharField(max_length=50, default="active", db_index=True)
    lock = models.BooleanField(default=False)
    
    class Meta:
        abstract = True

# Modifications model for tracking changes
class Modification(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    model = models.CharField(max_length=100)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.UUIDField()
    model_key = GenericForeignKey('content_type', 'object_id')
    field = models.CharField(max_length=100)
    before = models.TextField(null=True, blank=True)
    after = models.TextField(null=True, blank=True)
    time = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="modifications")
    
    class Meta:
        ordering = ['-time']
        
    def __str__(self):
        return f"{self.model} - {self.field} - {self.time}"

# Permission model
class Permission(BaseModel):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return self.name

# Role model
class Role(BaseModel):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    permissions = models.ManyToManyField(Permission, related_name="roles")
    
    def __str__(self):
        return self.name

# Department model
class Department(BaseModel):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    permission_ids = models.ManyToManyField(Permission, related_name="departments")
    
    def __str__(self):
        return self.name

# Custom User model extending Django's User model
class UserProfile(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    department_ids = models.ManyToManyField(Department, related_name="users")
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    address_line1 = models.CharField(max_length=255, blank=True, null=True)
    address_line2 = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    zip = models.CharField(max_length=20, blank=True, null=True)
    roles = models.ManyToManyField(Role, related_name="users")
    departments = models.ManyToManyField(Department, related_name="department_users")
    flags = models.JSONField(default=list, blank=True)
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"

# Contact model
class Contact(BaseModel):
    first_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    business_name = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    address_line1 = models.CharField(max_length=255, blank=True, null=True)
    address_line2 = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    zip = models.CharField(max_length=20, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    nationality = models.CharField(max_length=100, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    passport_number = models.CharField(max_length=100, blank=True, null=True)
    passport_expiration_date = models.DateField(blank=True, null=True)

    def __str__(self):
        if self.business_name:
            return self.business_name
        return f"{self.first_name} {self.last_name}"
    
    def clean(self):
        if not self.first_name and not self.last_name and not self.business_name:
            raise models.ValidationError("Either first/last name or business name is required")

# FBO (Fixed Base Operator) model
class FBO(BaseModel):
    name = models.CharField(max_length=255)
    address_line1 = models.CharField(max_length=255, blank=True, null=True)
    address_line2 = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    zip = models.CharField(max_length=20, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    contacts = models.ManyToManyField(Contact, related_name="fbos")
    phone = models.CharField(max_length=20, blank=True, null=True)
    phone_secondary = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)

    
    def __str__(self):
        return self.name

# Ground Transportation model
class Ground(BaseModel):
    name = models.CharField(max_length=255)
    address_line1 = models.CharField(max_length=255, blank=True, null=True)
    address_line2 = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    zip = models.CharField(max_length=20, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    contacts = models.ManyToManyField(Contact, related_name="grounds")

    
    def __str__(self):
        return self.name


class AirportType(models.TextChoices):
    LARGE = 'large_airport', 'Large airport'
    MEDIUM = 'medium_airport', 'Medium airport'
    SMALL = 'small_airport', 'Small airport'


# Airport model
class Airport(BaseModel):
    ident = models.CharField(max_length=10, unique=True, db_index=True)
    name = models.CharField(max_length=255)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    elevation = models.IntegerField(blank=True, null=True)
    iso_country = models.CharField(max_length=100)
    iso_region = models.CharField(max_length=100, blank=True, null=True)
    municipality = models.CharField(max_length=100, blank=True, null=True)
    icao_code = models.CharField(max_length=4, unique=True, db_index=True, blank=True, null=True)
    iata_code = models.CharField(max_length=3, db_index=True, blank=True, null=True)
    local_code = models.CharField(max_length=10, blank=True, null=True)
    gps_code = models.CharField(max_length=20, blank=True, null=True)
    airport_type = models.CharField(
        max_length=20,
        choices=AirportType.choices,
        default=AirportType.SMALL,
        db_index=True,
    )
    fbos = models.ManyToManyField(FBO, related_name="airports", blank=True)
    grounds = models.ManyToManyField(Ground, related_name="airports", blank=True)

    timezone = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.name} ({self.icao_code}/{self.iata_code})"

# Document model (for file storage)
class Document(models.Model):
    DOCUMENT_TYPES = [
        ('gendec', 'General Declaration'),
        ('quote', 'Quote Form'),
        ('customer_itinerary', 'Customer Itinerary'),
        ('internal_itinerary', 'Internal Itinerary'),
        ('payment_agreement', 'Payment Agreement'),
        ('consent_transport', 'Consent for Transport'),
        ('psa', 'Patient Service Agreement'),
        ('handling_request', 'Handling Request'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    filename = models.CharField(max_length=255)
    content = models.BinaryField(null=True, blank=True)  # Making it optional since we'll use file_path
    file_path = models.CharField(max_length=500, blank=True, null=True)  # Path to file on filesystem
    document_type = models.CharField(max_length=50, choices=DOCUMENT_TYPES, null=True, blank=True)
    flag = models.IntegerField(default=0)
    created_on = models.DateTimeField(auto_now_add=True)
    
    # Relationships - each document can belong to one of these
    trip = models.ForeignKey('Trip', on_delete=models.CASCADE, related_name='documents', null=True, blank=True)
    contact = models.ForeignKey('Contact', on_delete=models.CASCADE, related_name='documents', null=True, blank=True)
    patient = models.ForeignKey('Patient', on_delete=models.CASCADE, related_name='patient_documents', null=True, blank=True)
    passenger = models.ForeignKey('Passenger', on_delete=models.CASCADE, related_name='passenger_documents', null=True, blank=True)
    created_by = models.ForeignKey('auth.User', on_delete=models.SET_NULL, null=True, blank=True, related_name='created_documents')
    
    def __str__(self):
        doc_type = dict(self.DOCUMENT_TYPES).get(self.document_type, 'Document')
        return f"{doc_type}: {self.filename}"

# Aircraft model
class Aircraft(BaseModel):
    tail_number = models.CharField(max_length=20, unique=True, db_index=True)
    company = models.CharField(max_length=255)
    mgtow = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Maximum Gross Takeoff Weight")
    make = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    serial_number = models.CharField(max_length=100)
    
    def __str__(self):
        return f"{self.tail_number} - {self.make} {self.model}"

# Transaction model
class Transaction(BaseModel):
    key = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, db_index=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=20, choices=[
        ("credit_card", "Credit Card"),
        ("ACH", "ACH Transfer")
    ])
    payment_status = models.CharField(max_length=20, choices=[
        ("created", "Created"),
        ("pending", "Pending"),
        ("completed", "Completed"),
        ("failed", "Failed")
    ], default="created")
    payment_date = models.DateTimeField(default=timezone.now)
    email = models.EmailField()
    authorize_net_trans_id = models.CharField(max_length=50, blank=True, null=True, help_text="Authorize.Net Transaction ID")
    
    def __str__(self):
        return f"Transaction {self.key} - {self.amount} - {self.payment_status}"

# Agreement model
class Agreement(BaseModel):
    destination_email = models.EmailField()
    document_unsigned = models.ForeignKey(Document, on_delete=models.SET_NULL, null=True, blank=True, related_name="unsigned_agreements", db_column="document_unsigned_id")
    document_signed = models.ForeignKey(Document, on_delete=models.SET_NULL, null=True, blank=True, related_name="signed_agreements", db_column="document_signed_id")
    status = models.CharField(max_length=20, choices=[
        ("created", "Created"),
        ("pending", "Pending"),
        ("modified", "Modified"),
        ("signed", "Signed"),
        ("denied", "Denied")
    ], default="created")
    
    def __str__(self):
        return f"Agreement for {self.destination_email} - {self.status}"

# Patient model
class Patient(BaseModel):
    info = models.ForeignKey(Contact, on_delete=models.CASCADE, related_name="patients")
    bed_at_origin = models.BooleanField(default=False)
    bed_at_destination = models.BooleanField(default=False)
    date_of_birth = models.DateField()
    nationality = models.CharField(max_length=100)
    passport_number = models.CharField(max_length=100)
    passport_expiration_date = models.DateField()
    passport_document = models.ForeignKey(Document, on_delete=models.SET_NULL, null=True, blank=True, related_name="passport_patients", db_column="passport_document_id")
    special_instructions = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=[
        ("pending", "Pending"),
        ("confirmed", "Confirmed"),
        ("active", "Active"),
        ("completed", "Completed"),
        ("cancelled", "Cancelled")
    ], default="pending", db_index=True)
    letter_of_medical_necessity = models.ForeignKey(Document, on_delete=models.SET_NULL, null=True, blank=True, related_name="medical_necessity_patients", db_column="letter_of_medical_necessity_id")
    
    def __str__(self):
        return f"Patient: {self.info}"

# Quote model
class Quote(BaseModel):
    quoted_amount = models.DecimalField(max_digits=10, decimal_places=2)
    contact = models.ForeignKey(Contact, on_delete=models.CASCADE, related_name="quotes", db_column="contact_id")
    documents = models.ManyToManyField(Document, related_name="quotes")
    cruise_doctor_first_name = models.CharField(max_length=100, blank=True, null=True)
    cruise_doctor_last_name = models.CharField(max_length=100, blank=True, null=True)
    cruise_line = models.CharField(max_length=100, blank=True, null=True)
    cruise_ship = models.CharField(max_length=100, blank=True, null=True)
    pickup_airport = models.ForeignKey(Airport, on_delete=models.CASCADE, related_name="pickup_quotes", db_column="pickup_airport_id")
    dropoff_airport = models.ForeignKey(Airport, on_delete=models.CASCADE, related_name="dropoff_quotes", db_column="dropoff_airport_id")
    aircraft_type = models.CharField(max_length=20, choices=[
        ("65", "Learjet 65"),
        ("35", "Learjet 35"),
        ("TBD", "To Be Determined")
    ])
    estimated_flight_time = models.DurationField()
    includes_grounds = models.BooleanField(default=False)
    inquiry_date = models.DateTimeField(default=timezone.now)
    medical_team = models.CharField(max_length=20, choices=[
        ("RN/RN", "RN/RN"),
        ("RN/Paramedic", "RN/Paramedic"),
        ("RN/MD", "RN/MD"),
        ("RN/RT", "RN/RT"),
        ("standard", "Standard"),
        ("full", "Full")
    ])

    patient = models.ForeignKey(Patient, on_delete=models.SET_NULL, null=True, blank=True, related_name="quotes", db_column="patient_id")
    status = models.CharField(max_length=20, choices=[
        ("pending", "Pending"),
        ("active", "Active"),
        ("completed", "Completed"),
        ("cancelled", "Cancelled")
    ], default="pending", db_index=True)
    payment_status = models.CharField(max_length=20, choices=[
        ("pending", "Pending"),
        ("partial", "Partial Paid"),
        ("paid", "Paid")
    ], default="pending")
    number_of_stops = models.PositiveIntegerField(default=0)
    quote_pdf = models.ForeignKey(Document, on_delete=models.SET_NULL, null=True, blank=True, related_name="quote_pdfs", db_column="quote_pdf_id")
    quote_pdf_status = models.CharField(max_length=20, choices=[
        ("created", "Created"),
        ("pending", "Pending"),
        ("modified", "Modified"),
        ("accepted", "Accepted"),
        ("denied", "Denied")
    ], default="created")
    quote_pdf_email = models.EmailField()
    payment_agreement = models.ForeignKey(Agreement, on_delete=models.SET_NULL, null=True, blank=True, related_name="payment_quotes", db_column="payment_agreement_id")
    consent_for_transport = models.ForeignKey(Agreement, on_delete=models.SET_NULL, null=True, blank=True, related_name="consent_quotes", db_column="consent_for_transport_id")
    patient_service_agreement = models.ForeignKey(Agreement, on_delete=models.SET_NULL, null=True, blank=True, related_name="service_quotes", db_column="patient_service_agreement_id")
    transactions = models.ManyToManyField(Transaction, related_name="quotes", blank=True)
    
    def get_total_paid(self):
        """Calculate total amount paid from completed transactions."""
        from django.db import models
        return self.transactions.filter(payment_status='completed').aggregate(
            total=models.Sum('amount'))['total'] or 0
    
    def get_remaining_balance(self):
        """Calculate remaining balance after payments."""
        return self.quoted_amount - self.get_total_paid()
    
    def update_payment_status(self):
        """Update payment status based on total payments received."""
        total_paid = self.get_total_paid()
        if total_paid == 0:
            self.payment_status = 'pending'
        elif total_paid >= self.quoted_amount:
            self.payment_status = 'paid'
        else:
            self.payment_status = 'partial'
        self.save()
    
    def __str__(self):
        return f"Quote {self.id} - {self.quoted_amount} - {self.status}"

# Passenger model
class Passenger(BaseModel):
    info = models.ForeignKey(Contact, on_delete=models.CASCADE, related_name="passengers")
    date_of_birth = models.DateField(blank=True, null=True)
    nationality = models.CharField(max_length=100, blank=True, null=True)
    passport_number = models.CharField(max_length=100, blank=True, null=True)
    passport_expiration_date = models.DateField(blank=True, null=True)
    contact_number = models.CharField(max_length=20, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    passport_document = models.ForeignKey(Document, on_delete=models.SET_NULL, null=True, blank=True, related_name="passport_passengers", db_column="passport_document_id")
    passenger_ids = models.ManyToManyField('self', blank=True, symmetrical=False, related_name="related_passengers")
    
    def __str__(self):
        return f"Passenger: {self.info}"

# Crew Line model
class CrewLine(BaseModel):
    primary_in_command = models.ForeignKey(Contact, on_delete=models.CASCADE, related_name="primary_crew_lines", db_column="primary_in_command_id")
    secondary_in_command = models.ForeignKey(Contact, on_delete=models.CASCADE, related_name="secondary_crew_lines", db_column="secondary_in_command_id")
    medic_ids = models.ManyToManyField(Contact, related_name="medic_crew_lines")
    
    def __str__(self):
        return f"Crew: {self.primary_in_command} and {self.secondary_in_command}"

# Trip model
class Trip(BaseModel):
    email_chain = models.JSONField(default=list, blank=True)
    quote = models.ForeignKey(Quote, on_delete=models.CASCADE, related_name="trips", null=True, blank=True, db_column="quote_id")
    type = models.CharField(max_length=20, choices=[
        ("medical", "Medical"),
        ("charter", "Charter"),
        ("part 91", "Part 91"),
        ("other", "Other"),
        ("maintenance", "Maintenance")
    ])
    patient = models.ForeignKey(Patient, on_delete=models.SET_NULL, null=True, blank=True, related_name="trips", db_column="patient_id")
    estimated_departure_time = models.DateTimeField(blank=True, null=True)
    post_flight_duty_time = models.DurationField(blank=True, null=True)
    pre_flight_duty_time = models.DurationField(blank=True, null=True)
    aircraft = models.ForeignKey(Aircraft, on_delete=models.SET_NULL, null=True, blank=True, related_name="trips", db_column="aircraft_id")
    trip_number = models.CharField(max_length=20, unique=True, db_index=True)
    internal_itinerary = models.ForeignKey(Document, on_delete=models.SET_NULL, null=True, blank=True, related_name="internal_itinerary_trips", db_column="internal_itinerary_id")
    customer_itinerary = models.ForeignKey(Document, on_delete=models.SET_NULL, null=True, blank=True, related_name="customer_itinerary_trips", db_column="customer_itinerary_id")
    passengers = models.ManyToManyField(Passenger, related_name="trips", blank=True)
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Trip {self.trip_number} - {self.type}"

# Trip Line model
class TripLine(BaseModel):
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE, related_name="trip_lines", db_column="trip_id")
    origin_airport = models.ForeignKey(Airport, on_delete=models.CASCADE, related_name="origin_trip_lines", db_column="origin_airport_id")
    destination_airport = models.ForeignKey(Airport, on_delete=models.CASCADE, related_name="destination_trip_lines", db_column="destination_airport_id")
    crew_line = models.ForeignKey(CrewLine, on_delete=models.SET_NULL, null=True, blank=True, related_name="trip_lines", db_column="crew_line_id")
    departure_fbo = models.ForeignKey(FBO, on_delete=models.SET_NULL, null=True, blank=True, related_name="departure_trip_lines")
    arrival_fbo = models.ForeignKey(FBO, on_delete=models.SET_NULL, null=True, blank=True, related_name="arrival_trip_lines")
    departure_time_local = models.DateTimeField()
    departure_time_utc = models.DateTimeField()
    arrival_time_local = models.DateTimeField()
    arrival_time_utc = models.DateTimeField()
    distance = models.DecimalField(max_digits=10, decimal_places=2)
    flight_time = models.DurationField()
    ground_time = models.DurationField()
    passenger_leg = models.BooleanField(default=True)
    
    def __str__(self):
        return f"Trip Line: {self.origin_airport} to {self.destination_airport}"
    
    class Meta:
        ordering = ['departure_time_utc']


class Staff(BaseModel):
    contact = models.OneToOneField("api.Contact", on_delete=models.CASCADE, related_name="staff")
    active = models.BooleanField(default=True)
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.contact.first_name} {self.contact.last_name}".strip() or str(self.contact_id)


class StaffRole(BaseModel):
    code = models.CharField(max_length=32, unique=True)   # e.g., 'PIC', 'SIC', 'RN', 'PARAMEDIC'
    name = models.CharField(max_length=64)                # e.g., 'Pilot in Command'

    class Meta:
        indexes = [models.Index(fields=["code"])]

    def __str__(self):
        return self.code


class StaffRoleMembership(BaseModel):
    staff = models.ForeignKey("api.Staff", on_delete=models.CASCADE, related_name="role_memberships")
    role = models.ForeignKey("api.StaffRole", on_delete=models.PROTECT, related_name="memberships")
    start_on = models.DateField(null=True, blank=True)
    end_on = models.DateField(null=True, blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["staff", "role", "start_on", "end_on"],
                name="uniq_staff_role_interval"
            )
        ]


class TripEvent(BaseModel):
    """
    Non-flight timeline items attached to a Trip.
    """
    EVENT_TYPES = [
        ("CREW_CHANGE", "Crew Change"),
        ("OVERNIGHT", "Overnight (New Day)"),
    ]

    trip = models.ForeignKey("api.Trip", on_delete=models.CASCADE, related_name="events")
    airport = models.ForeignKey("api.Airport", on_delete=models.PROTECT, related_name="trip_events")

    event_type = models.CharField(max_length=20, choices=EVENT_TYPES)

    # Start/end timestamps (UTC + local) so you can group by day and show durations
    start_time_local = models.DateTimeField()
    start_time_utc = models.DateTimeField()
    end_time_local = models.DateTimeField(blank=True, null=True)  # required for OVERNIGHT
    end_time_utc = models.DateTimeField(blank=True, null=True)

    # Only used for CREW_CHANGE
    crew_line = models.ForeignKey(
        "api.CrewLine", on_delete=models.SET_NULL, null=True, blank=True, related_name="trip_events"
    )

    notes = models.TextField(blank=True, null=True)

    class Meta:
        indexes = [
            models.Index(fields=["trip", "start_time_utc"]),
            models.Index(fields=["event_type"]),
        ]


class Comment(BaseModel):
    """
    Comments attached to any model instance via a generic foreign key.
    """
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.UUIDField()
    content_object = GenericForeignKey('content_type', 'object_id')

    text = models.TextField()

    class Meta:
        indexes = [
            models.Index(fields=["content_type", "object_id"]),
        ]


class Contract(BaseModel):
    """
    Contract model for managing DocuSeal integration and document signing workflows.
    Extends the existing Agreement functionality with DocuSeal-specific fields.
    """
    CONTRACT_TYPES = [
        ('consent_transport', 'Consent for Transport'),
        ('payment_agreement', 'Air Ambulance Payment Agreement'),
        ('patient_service_agreement', 'Patient Service Agreement'),
    ]
    
    CONTRACT_STATUS = [
        ('draft', 'Draft'),
        ('pending', 'Pending Signature'),
        ('signed', 'Signed'),
        ('completed', 'Completed'),
        ('expired', 'Expired'),
        ('cancelled', 'Cancelled'),
        ('failed', 'Failed'),
    ]
    
    # Basic contract information
    title = models.CharField(max_length=255)
    contract_type = models.CharField(max_length=30, choices=CONTRACT_TYPES)
    status = models.CharField(max_length=20, choices=CONTRACT_STATUS, default='draft')
    
    # Relationships
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE, related_name='contracts')
    customer_contact = models.ForeignKey(Contact, on_delete=models.CASCADE, related_name='customer_contracts', null=True, blank=True)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='patient_contracts', null=True, blank=True)
    
    # DocuSeal integration fields
    docuseal_template_id = models.CharField(max_length=100, blank=True, null=True)
    docuseal_submission_id = models.CharField(max_length=100, blank=True, null=True)
    docuseal_webhook_id = models.CharField(max_length=100, blank=True, null=True)
    
    # Signing details
    signer_email = models.EmailField()
    signer_name = models.CharField(max_length=255, blank=True, null=True)
    date_sent = models.DateTimeField(null=True, blank=True)
    date_signed = models.DateTimeField(null=True, blank=True)
    date_expired = models.DateTimeField(null=True, blank=True)
    
    # Document storage
    unsigned_document = models.ForeignKey(
        Document, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='unsigned_contracts'
    )
    signed_document = models.ForeignKey(
        Document, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='signed_contracts'
    )
    
    # Additional metadata
    notes = models.TextField(blank=True, null=True)
    docuseal_response_data = models.JSONField(default=dict, blank=True)
    
    class Meta:
        indexes = [
            models.Index(fields=['trip', 'contract_type']),
            models.Index(fields=['status']),
            models.Index(fields=['docuseal_submission_id']),
        ]
        
    def __str__(self):
        return f"{self.title} - {self.get_contract_type_display()} ({self.get_status_display()})"
    
    def is_pending_signature(self):
        return self.status == 'pending'
    
    def is_signed(self):
        return self.status in ['signed', 'completed']
```


# File: api/__init__.py

```python

```


# File: api/tests.py

```python
from django.test import TestCase

# Create your tests here.

```


# File: api/permissions.py

```python
from rest_framework import permissions
from django.contrib.auth.models import User
from .models import Permission, Role, UserProfile

class IsAuthenticatedOrPublicEndpoint(permissions.BasePermission):
    """
    Custom permission to allow unauthenticated access to public endpoints.
    """
    
    def has_permission(self, request, view):
        # Allow unauthenticated access to specific actions
        if view.action in getattr(view, 'public_actions', []):
            return True
        
        # Otherwise require authentication
        return request.user and request.user.is_authenticated

class IsTransactionOwner(permissions.BasePermission):
    """
    Custom permission to only allow access to a transaction with the correct key.
    """
    
    def has_permission(self, request, view):
        # Allow access if the transaction key in the URL matches
        transaction_key = request.query_params.get('key')
        if transaction_key and view.action == 'retrieve_by_key':
            return True
        
        # Otherwise require authentication
        return request.user and request.user.is_authenticated

# Model-specific permission classes
class HasModelPermission(permissions.BasePermission):
    """
    Base permission class that checks if a user has the required permission for a model.
    Subclasses should define:
    - model_name: The name of the model (lowercase)
    - required_permission: The required permission type (read, write, modify, delete)
    """
    model_name = None
    required_permission = None
    
    def has_permission(self, request, view):
        # Superusers have all permissions
        if request.user.is_superuser:
            return True
            
        # Check if user has the required permission
        try:
            user_profile = UserProfile.objects.get(user=request.user)
            
            # Check permissions through roles
            for role in user_profile.roles.all():
                permission_name = f"{self.model_name}_{self.required_permission}"
                if role.permissions.filter(name=permission_name).exists():
                    return True
                    
            # Check for any_model permission (global permission)
            for role in user_profile.roles.all():
                permission_name = f"any_{self.required_permission}"
                if role.permissions.filter(name=permission_name).exists():
                    return True
                    
            return False
        except UserProfile.DoesNotExist:
            return False
    
    def has_object_permission(self, request, view, obj):
        # Superusers have all permissions
        if request.user.is_superuser:
            return True
            
        # Check if user has the required permission for any object
        try:
            user_profile = UserProfile.objects.get(user=request.user)
            
            # Check for any object permission
            for role in user_profile.roles.all():
                permission_name = f"{self.model_name}_{self.required_permission}_any"
                if role.permissions.filter(name=permission_name).exists():
                    return True
            
            # Check if user is the creator of the object (own permission)
            if hasattr(obj, 'created_by') and obj.created_by == request.user:
                for role in user_profile.roles.all():
                    permission_name = f"{self.model_name}_{self.required_permission}_own"
                    if role.permissions.filter(name=permission_name).exists():
                        return True
            
            return False
        except UserProfile.DoesNotExist:
            return False

# Quote permissions
class CanReadQuote(HasModelPermission):
    model_name = "quote"
    required_permission = "read"

class CanWriteQuote(HasModelPermission):
    model_name = "quote"
    required_permission = "write"

class CanModifyQuote(HasModelPermission):
    model_name = "quote"
    required_permission = "modify"

class CanDeleteQuote(HasModelPermission):
    model_name = "quote"
    required_permission = "delete"

# Patient permissions
class CanReadPatient(HasModelPermission):
    model_name = "patient"
    required_permission = "read"

class CanWritePatient(HasModelPermission):
    model_name = "patient"
    required_permission = "write"

class CanModifyPatient(HasModelPermission):
    model_name = "patient"
    required_permission = "modify"

class CanDeletePatient(HasModelPermission):
    model_name = "patient"
    required_permission = "delete"

# Trip permissions
class CanReadTrip(HasModelPermission):
    model_name = "trip"
    required_permission = "read"

class CanWriteTrip(HasModelPermission):
    model_name = "trip"
    required_permission = "write"

class CanModifyTrip(HasModelPermission):
    model_name = "trip"
    required_permission = "modify"

class CanDeleteTrip(HasModelPermission):
    model_name = "trip"
    required_permission = "delete"

# Passenger permissions
class CanReadPassenger(HasModelPermission):
    model_name = "passenger"
    required_permission = "read"

class CanWritePassenger(HasModelPermission):
    model_name = "passenger"
    required_permission = "write"

class CanModifyPassenger(HasModelPermission):
    model_name = "passenger"
    required_permission = "modify"

class CanDeletePassenger(HasModelPermission):
    model_name = "passenger"
    required_permission = "delete"

# Transaction permissions
class CanReadTransaction(HasModelPermission):
    model_name = "transaction"
    required_permission = "read"

class CanWriteTransaction(HasModelPermission):
    model_name = "transaction"
    required_permission = "write"

class CanModifyTransaction(HasModelPermission):
    model_name = "transaction"
    required_permission = "modify"

class CanDeleteTransaction(HasModelPermission):
    model_name = "transaction"
    required_permission = "delete"

# TripLine permissions
class CanReadTripLine(HasModelPermission):
    model_name = "tripline"
    required_permission = "read"

class CanWriteTripLine(HasModelPermission):
    model_name = "tripline"
    required_permission = "write"

class CanModifyTripLine(HasModelPermission):
    model_name = "tripline"
    required_permission = "modify"

class CanDeleteTripLine(HasModelPermission):
    model_name = "tripline"
    required_permission = "delete"

```


# File: api/utils.py

```python
from django.contrib.contenttypes.models import ContentType
from .models import Modification
from .signals import get_current_user


def track_modification(instance, field_name, before_value, after_value, user=None):
    """
    Manually track a modification for cases where signals aren't sufficient
    
    Args:
        instance: The model instance that was modified
        field_name: The name of the field that changed
        before_value: The previous value
        after_value: The new value  
        user: The user making the change (optional, will use thread-local if not provided)
    """
    if user is None:
        user = get_current_user()
    
    content_type = ContentType.objects.get_for_model(instance)
    
    Modification.objects.create(
        model=instance.__class__.__name__,
        content_type=content_type,
        object_id=instance.pk,
        field=field_name,
        before=str(before_value) if before_value is not None else None,
        after=str(after_value) if after_value is not None else None,
        user=user
    )


def track_creation(instance, user=None):
    """
    Track the creation of a new model instance
    
    Args:
        instance: The newly created model instance
        user: The user creating the instance (optional, will use thread-local if not provided)
    """
    if user is None:
        user = get_current_user()
    
    content_type = ContentType.objects.get_for_model(instance)
    
    Modification.objects.create(
        model=instance.__class__.__name__,
        content_type=content_type,
        object_id=instance.pk,
        field='__created__',
        before=None,
        after='Instance created',
        user=user
    )


def track_deletion(instance, user=None):
    """
    Track the deletion of a model instance
    
    Args:
        instance: The model instance being deleted
        user: The user deleting the instance (optional, will use thread-local if not provided)
    """
    if user is None:
        user = get_current_user()
    
    content_type = ContentType.objects.get_for_model(instance)
    
    Modification.objects.create(
        model=instance.__class__.__name__,
        content_type=content_type,
        object_id=instance.pk,
        field='__deleted__',
        before='Instance existed',
        after=None,
        user=user
    )
```


# File: api/signals.py

```python
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.apps import apps
from django.contrib.contenttypes.models import ContentType
import json
import threading

from .models import Modification, BaseModel

# Thread-local storage for the current user and tracking state
_local = threading.local()

def set_current_user(user):
    """Set the current user for modification tracking"""
    _local.user = user

def get_current_user():
    """Get the current user from thread-local storage"""
    return getattr(_local, 'user', None)

def set_skip_signal_tracking(skip):
    """Set flag to skip signal-based tracking (for ViewSet operations)"""
    _local.skip_signal_tracking = skip

def get_skip_signal_tracking():
    """Check if signal-based tracking should be skipped"""
    return getattr(_local, 'skip_signal_tracking', False)

def get_model_fields(instance):
    """Get all fields from a model instance, excluding system fields"""
    excluded_fields = {'id', 'created_on', 'modified_on', 'created_by', 'modified_by'}
    return {field.name: getattr(instance, field.name) 
            for field in instance._meta.fields 
            if not field.is_relation and field.name not in excluded_fields}

@receiver(pre_save)
def track_model_changes(sender, instance, **kwargs):
    """Track changes to models that inherit from BaseModel"""
    # Skip if it's not a BaseModel or it's the Modification model itself
    if not isinstance(instance, BaseModel) or sender.__name__ == 'Modification':
        return
    
    # Skip if ViewSet is handling tracking
    if get_skip_signal_tracking():
        return
    
    # Skip if it's a new instance
    if not instance.pk:
        return
    
    try:
        # Get the old instance from the database
        old_instance = sender.objects.get(pk=instance.pk)
        
        # Get the fields for both instances
        old_fields = get_model_fields(old_instance)
        new_fields = get_model_fields(instance)
        
        # Find changed fields
        for field_name, old_value in old_fields.items():
            new_value = new_fields.get(field_name)
            
            # Skip if the field hasn't changed
            if old_value == new_value:
                continue
            
            # Create a modification record
            content_type = ContentType.objects.get_for_model(instance)
            Modification.objects.create(
                model=sender.__name__,
                content_type=content_type,
                object_id=instance.pk,
                field=field_name,
                before=str(old_value) if old_value is not None else None,
                after=str(new_value) if new_value is not None else None,
                user=get_current_user()
            )
    except sender.DoesNotExist:
        # This is a new instance, no need to track changes
        pass
    except Exception as e:
        # Log the error but don't prevent the save
        print(f"Error tracking changes: {e}")

```


# File: api/apps.py

```python
from django.apps import AppConfig


class ApiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'api'
    
    def ready(self):
        import api.signals

```


# File: api/serializers.py

```python
from rest_framework import serializers
from .models import (
    Modification, Permission, Role, Department, UserProfile, Contact, 
    FBO, Ground, Airport, Document, Aircraft, Transaction, Agreement,
    Patient, Quote, Passenger, CrewLine, Trip, TripLine, Staff, StaffRole,
    StaffRoleMembership, TripEvent, Comment, Contract
)
from django.contrib.auth.models import User

# User serializers
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'is_staff']

# Base serializers
class ModificationSerializer(serializers.ModelSerializer):
    user_username = serializers.CharField(source='user.username', read_only=True)
    
    class Meta:
        model = Modification
        fields = ['id', 'model', 'content_type', 'object_id', 'field', 'before', 'after', 'time', 'user', 'user_username']

class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = ['id', 'name', 'description', 'created_on', 'created_by', 'modified_on', 'modified_by']

class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ['id', 'name', 'description', 'permissions', 'created_on', 'created_by', 'status', 'lock']

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ['id', 'name', 'description', 'created_on', 'created_by', 'status', 'lock']

class CommentSerializer(serializers.ModelSerializer):
    created_by_username = serializers.CharField(source='created_by.username', read_only=True)
    created_by_name = serializers.SerializerMethodField(read_only=True)
    content_type_name = serializers.CharField(source='content_type.model', read_only=True)
    
    class Meta:
        model = Comment
        fields = ['id', 'content_type', 'content_type_name', 'object_id', 'text', 
                 'created_on', 'created_by', 'created_by_username', 'created_by_name',
                 'modified_on', 'modified_by', 'status']
    
    def get_created_by_name(self, obj):
        if obj.created_by:
            if hasattr(obj.created_by, 'profile'):
                return f"{obj.created_by.profile.first_name} {obj.created_by.profile.last_name}".strip()
            return obj.created_by.username
        return None

# Contact and location serializers
class ContactSerializer(serializers.ModelSerializer):
    contact_type = serializers.SerializerMethodField()
    
    class Meta:
        model = Contact
        fields = ['id', 'first_name', 'last_name', 'business_name', 'email', 'phone', 
                 'address_line1', 'address_line2', 'city', 'state', 'zip', 'country',
                 'nationality', 'date_of_birth', 'passport_number', 'passport_expiration_date',
                 'contact_type', 'created_on', 'created_by', 'modified_on', 'modified_by']
    
    def get_contact_type(self, obj):
        """
        Determine contact type based on related objects
        """
        # Check if this contact is a patient
        if hasattr(obj, 'patients') and obj.patients.exists():
            return 'Patient'
        
        # Check if this contact is staff
        if hasattr(obj, 'staff'):
            try:
                staff = obj.staff
                # Check staff role memberships to determine if pilot or medic
                role_codes = staff.role_memberships.filter(
                    end_on__isnull=True  # Active memberships only
                ).values_list('role__code', flat=True)
                
                if 'PIC' in role_codes or 'SIC' in role_codes:
                    return 'Staff - Pilot'
                elif 'RN' in role_codes or 'PARAMEDIC' in role_codes:
                    return 'Staff - Medic'
                else:
                    return 'Staff'
            except:
                return 'Staff'
        
        # Check if this contact is a passenger
        if hasattr(obj, 'passengers') and obj.passengers.exists():
            return 'Passenger'
        
        # Check if this contact is a customer (has quotes)
        if hasattr(obj, 'quotes') and obj.quotes.exists():
            return 'Customer'
        
        # Default type
        return 'General'

class FBOSerializer(serializers.ModelSerializer):
    airport_codes = serializers.SerializerMethodField()
    airport_names = serializers.SerializerMethodField()
    contacts = serializers.PrimaryKeyRelatedField(many=True, queryset=Contact.objects.all(), required=False)
    
    class Meta:
        model = FBO
        fields = ['id', 'name', 'address_line1', 'address_line2', 'city', 'state', 'zip', 
                 'country', 'phone', 'phone_secondary', 'email', 'notes', 'contacts',
                 'airport_codes', 'airport_names', 'created_on', 'created_by', 'modified_on', 'modified_by']
    
    def get_airport_codes(self, obj):
        airports = obj.airports.all()
        return [airport.ident for airport in airports] if airports else []
    
    def get_airport_names(self, obj):
        airports = obj.airports.all()
        return [airport.name for airport in airports] if airports else []

class GroundSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ground
        fields = ['id', 'name', 'address_line1', 'address_line2', 'city', 'state', 'zip', 
                 'country', 'notes', 'contacts', 'created_on', 'created_by', 
                 'modified_on', 'modified_by']

# Document Serializers
class DocumentSerializer(serializers.ModelSerializer):
    document_type_display = serializers.CharField(source='get_document_type_display', read_only=True)
    created_by_name = serializers.SerializerMethodField()
    
    class Meta:
        model = Document
        fields = [
            'id', 'filename', 'file_path', 'document_type', 'document_type_display',
            'created_on', 'created_by', 'created_by_name', 'trip', 'contact', 
            'patient', 'passenger'
        ]
        read_only_fields = ['id', 'created_on']
    
    def get_created_by_name(self, obj):
        if obj.created_by:
            return f"{obj.created_by.first_name} {obj.created_by.last_name}".strip() or obj.created_by.username
        return None

class DocumentCreateSerializer(serializers.Serializer):
    """Serializer for document generation request."""
    document_type = serializers.ChoiceField(
        choices=Document.DOCUMENT_TYPES,
        required=False,
        allow_blank=True,
        help_text="Specific document type to generate. If not provided, generates all applicable documents."
    )

class AirportSerializer(serializers.ModelSerializer):
    fbos = FBOSerializer(many=True, read_only=True)
    grounds = GroundSerializer(many=True, read_only=True)
    fbos_count = serializers.SerializerMethodField()
    grounds_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Airport
        fields = ['id', 'ident', 'name', 'latitude', 'longitude', 'elevation', 
                 'iso_country', 'iso_region', 'municipality', 'icao_code', 'iata_code', 
                 'local_code', 'gps_code', 'airport_type', 'timezone', 
                 'fbos', 'grounds', 'fbos_count', 'grounds_count',
                 'created_on', 'created_by', 'modified_on', 'modified_by']
    
    def get_fbos_count(self, obj):
        return obj.fbos.count()
    
    def get_grounds_count(self, obj):
        return obj.grounds.count()

# Aircraft serializer
class AircraftSerializer(serializers.ModelSerializer):
    class Meta:
        model = Aircraft
        fields = ['id', 'tail_number', 'company', 'mgtow', 'make', 'model', 'serial_number', 
                 'created_on', 'created_by', 'modified_on', 'modified_by']

# Document serializer (basic for references)
class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = ['id', 'filename', 'flag', 'created_on']

# Agreement serializer
class AgreementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Agreement
        fields = ['id', 'destination_email', 'document_unsigned', 'document_signed', 
                 'status', 'created_on', 'created_by', 'modified_on', 'modified_by']

# ========== STANDARDIZED CRUD SERIALIZERS ==========

# 1) User Profiles
class UserProfileReadSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    roles = RoleSerializer(many=True, read_only=True)
    departments = DepartmentSerializer(many=True, read_only=True)
    
    class Meta:
        model = UserProfile
        fields = [
            'id', 'user', 'first_name', 'last_name', 'email', 'phone',
            'address_line1', 'address_line2', 'city', 'state', 'country', 'zip',
            'roles', 'departments', 'flags', 'status', 'created_on'
        ]

class UserProfileWriteSerializer(serializers.ModelSerializer):
    user_id = serializers.PrimaryKeyRelatedField(
        source='user', queryset=User.objects.all(), write_only=True
    )
    role_ids = serializers.PrimaryKeyRelatedField(
        source='roles', queryset=Role.objects.all(), many=True, write_only=True
    )
    department_ids = serializers.PrimaryKeyRelatedField(
        source='departments', queryset=Department.objects.all(), many=True, write_only=True
    )
    
    class Meta:
        model = UserProfile
        fields = [
            'user_id', 'first_name', 'last_name', 'email', 'phone',
            'address_line1', 'address_line2', 'city', 'state', 'country', 'zip',
            'role_ids', 'department_ids', 'flags', 'status'
        ]

# 2) Passengers
class PassengerReadSerializer(serializers.ModelSerializer):
    info = ContactSerializer(read_only=True)
    passport_document = DocumentSerializer(read_only=True)
    related_passengers = serializers.SerializerMethodField()
    trips = serializers.SerializerMethodField()
    
    class Meta:
        model = Passenger
        fields = [
            'id', 'info', 'date_of_birth', 'nationality', 'passport_number',
            'passport_expiration_date', 'contact_number', 'notes', 'passport_document',
            'related_passengers', 'trips', 'status', 'created_on'
        ]
    
    def get_related_passengers(self, obj):
        return [{'id': p.id, 'info': ContactSerializer(p.info).data} for p in obj.passenger_ids.all()]
    
    def get_trips(self, obj):
        trips = obj.trips.all()
        return [{'id': trip.id, 'trip_number': trip.trip_number} for trip in trips]

class PassengerWriteSerializer(serializers.ModelSerializer):
    info = serializers.PrimaryKeyRelatedField(
        queryset=Contact.objects.all(), write_only=True
    )
    passport_document = serializers.PrimaryKeyRelatedField(
        queryset=Document.objects.all(), write_only=True, required=False, allow_null=True
    )
    passenger_ids = serializers.PrimaryKeyRelatedField(
        queryset=Passenger.objects.all(), many=True, write_only=True, required=False
    )
    
    class Meta:
        model = Passenger
        fields = [
            'info', 'date_of_birth', 'nationality', 'passport_number',
            'passport_expiration_date', 'contact_number', 'notes', 'passport_document',
            'passenger_ids', 'status'
        ]
    
    def create(self, validated_data):
        # Get contact data for filling deprecated fields
        contact = validated_data['info']
        passenger_ids = validated_data.pop('passenger_ids', [])
        
        # Use contact data as primary source, fallback to provided data
        validated_data['date_of_birth'] = contact.date_of_birth or validated_data.get('date_of_birth')
        validated_data['nationality'] = contact.nationality or validated_data.get('nationality', '')
        validated_data['passport_number'] = contact.passport_number or validated_data.get('passport_number', '')
        validated_data['passport_expiration_date'] = contact.passport_expiration_date or validated_data.get('passport_expiration_date')
        
        passenger = super().create(validated_data)
        
        # Set related passengers if provided
        if passenger_ids:
            passenger.passenger_ids.set(passenger_ids)
        
        return passenger

# 3) Crew Lines
class CrewLineReadSerializer(serializers.ModelSerializer):
    primary_in_command = ContactSerializer(read_only=True)
    secondary_in_command = ContactSerializer(read_only=True)
    medics = ContactSerializer(source='medic_ids', many=True, read_only=True)
    
    class Meta:
        model = CrewLine
        fields = [
            'id', 'primary_in_command', 'secondary_in_command', 'medics',
            'status', 'created_on'
        ]

class CrewLineWriteSerializer(serializers.ModelSerializer):
    primary_in_command = serializers.PrimaryKeyRelatedField(
        queryset=Contact.objects.all(), write_only=True
    )
    secondary_in_command = serializers.PrimaryKeyRelatedField(
        queryset=Contact.objects.all(), write_only=True
    )
    medic_ids = serializers.PrimaryKeyRelatedField(
        queryset=Contact.objects.all(), many=True, write_only=True
    )
    
    class Meta:
        model = CrewLine
        fields = [
            'id', 'primary_in_command', 'secondary_in_command', 'medic_ids', 'status'
        ]

class TripMiniSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trip
        fields = ("id", "trip_number", "type")


class TripLineReadSerializer(serializers.ModelSerializer):
    trip = TripMiniSerializer(read_only=True)
    origin_airport = AirportSerializer(read_only=True)
    destination_airport = AirportSerializer(read_only=True)
    crew_line = CrewLineReadSerializer(read_only=True)
    departure_fbo = FBOSerializer(read_only=True)
    arrival_fbo = FBOSerializer(read_only=True)
    departure_timezone_info = serializers.SerializerMethodField()
    arrival_timezone_info = serializers.SerializerMethodField()
    
    class Meta:
        model = TripLine
        fields = [
            'id', 'trip', 'origin_airport', 'destination_airport', 'crew_line',
            'departure_fbo', 'arrival_fbo', 'departure_time_local', 'departure_time_utc', 
            'arrival_time_local', 'arrival_time_utc', 'distance', 'flight_time', 
            'ground_time', 'passenger_leg', 'status', 'created_on',
            'departure_timezone_info', 'arrival_timezone_info'
        ]
    
    def get_departure_timezone_info(self, obj):
        """Get timezone information for departure airport."""
        print(f"DEBUG: get_departure_timezone_info called for trip line {obj.id}")
        print(f"DEBUG: origin_airport exists: {bool(obj.origin_airport)}")
        if obj.origin_airport:
            print(f"DEBUG: origin_airport timezone: {getattr(obj.origin_airport, 'timezone', 'NO_TIMEZONE_FIELD')}")
        
        if not obj.origin_airport or not obj.origin_airport.timezone:
            print(f"DEBUG: Returning None - no airport or no timezone")
            return None
        
        try:
            from .timezone_utils import get_timezone_info, format_time_with_timezone, convert_utc_to_local
            
            # Use UTC time as source of truth and calculate local time
            if not obj.departure_time_utc:
                print("DEBUG: No departure UTC time available")
                return None
                
            print(f"DEBUG: Converting UTC {obj.departure_time_utc} to {obj.origin_airport.timezone}")
            
            # Convert UTC to proper local time for this airport
            local_time = convert_utc_to_local(obj.departure_time_utc, obj.origin_airport.timezone)
            print(f"DEBUG: Calculated local time: {local_time}")
            
            # Get timezone info for this time
            tz_info = get_timezone_info(obj.origin_airport.timezone, obj.departure_time_utc)
            print(f"DEBUG: Timezone info: {tz_info}")
            
            # Format the calculated local time with timezone info
            formatted_time = format_time_with_timezone(
                local_time, obj.origin_airport.timezone, include_utc=True
            )
            print(f"DEBUG: Formatted time: {formatted_time}")
            tz_info['formatted_time'] = formatted_time
            
            # Also add the calculated local time for reference
            tz_info['calculated_local_time'] = local_time.isoformat()
            
            print(f"DEBUG: Final timezone info: {tz_info}")
            return tz_info
        except Exception as e:
            # Log the error for debugging
            print(f"DEBUG: Exception in get_departure_timezone_info: {str(e)}")
            import traceback
            print(f"DEBUG: Traceback: {traceback.format_exc()}")
            return None
    
    def get_arrival_timezone_info(self, obj):
        """Get timezone information for arrival airport."""
        print(f"DEBUG: get_arrival_timezone_info called for trip line {obj.id}")
        print(f"DEBUG: destination_airport exists: {bool(obj.destination_airport)}")
        if obj.destination_airport:
            print(f"DEBUG: destination_airport timezone: {getattr(obj.destination_airport, 'timezone', 'NO_TIMEZONE_FIELD')}")
        
        if not obj.destination_airport or not obj.destination_airport.timezone:
            print(f"DEBUG: Returning None - no airport or no timezone")
            return None
        
        try:
            from .timezone_utils import get_timezone_info, format_time_with_timezone, convert_utc_to_local
            
            # Use UTC time as source of truth and calculate local time
            if not obj.arrival_time_utc:
                print("DEBUG: No arrival UTC time available")
                return None
                
            print(f"DEBUG: Converting UTC {obj.arrival_time_utc} to {obj.destination_airport.timezone}")
            
            # Convert UTC to proper local time for this airport
            local_time = convert_utc_to_local(obj.arrival_time_utc, obj.destination_airport.timezone)
            print(f"DEBUG: Calculated arrival local time: {local_time}")
            
            # Get timezone info for this time
            tz_info = get_timezone_info(obj.destination_airport.timezone, obj.arrival_time_utc)
            print(f"DEBUG: Arrival timezone info: {tz_info}")
            
            # Format the calculated local time with timezone info
            formatted_time = format_time_with_timezone(
                local_time, obj.destination_airport.timezone, include_utc=True
            )
            print(f"DEBUG: Arrival formatted time: {formatted_time}")
            tz_info['formatted_time'] = formatted_time
            
            # Also add the calculated local time for reference
            tz_info['calculated_local_time'] = local_time.isoformat()
            
            print(f"DEBUG: Final arrival timezone info: {tz_info}")
            return tz_info
        except Exception:
            return None
    
    def get_trip(self, obj):
        # Return minimal trip info to avoid circular references
        return {
            'id': obj.trip.id,
            'trip_number': obj.trip.trip_number,
            'type': obj.trip.type
        }

class TripLineWriteSerializer(serializers.ModelSerializer):
    trip = serializers.PrimaryKeyRelatedField(
        queryset=Trip.objects.all(), write_only=True
    )
    origin_airport = serializers.PrimaryKeyRelatedField(
        queryset=Airport.objects.all(), write_only=True
    )
    destination_airport = serializers.PrimaryKeyRelatedField(
        queryset=Airport.objects.all(), write_only=True
    )
    crew_line = serializers.PrimaryKeyRelatedField(
        queryset=CrewLine.objects.all(), write_only=True, required=False, allow_null=True
    )
    departure_fbo = serializers.PrimaryKeyRelatedField(
        queryset=FBO.objects.all(), write_only=True, required=False, allow_null=True
    )
    arrival_fbo = serializers.PrimaryKeyRelatedField(
        queryset=FBO.objects.all(), write_only=True, required=False, allow_null=True
    )
    
    # Make time fields optional for auto-calculation
    departure_time_utc = serializers.DateTimeField(required=False, allow_null=True)
    arrival_time_local = serializers.DateTimeField(required=False, allow_null=True)
    arrival_time_utc = serializers.DateTimeField(required=False, allow_null=True)
    
    class Meta:
        model = TripLine
        fields = [
            'id', 'trip', 'origin_airport', 'destination_airport', 'crew_line',
            'departure_fbo', 'arrival_fbo', 'departure_time_local', 'departure_time_utc', 
            'arrival_time_local', 'arrival_time_utc', 'distance', 'flight_time', 
            'ground_time', 'passenger_leg', 'status'
        ]
    
    def validate(self, data):
        """
        Validate timezone consistency and auto-calculate missing times.
        """
        from .timezone_utils import (
            convert_local_to_utc, convert_utc_to_local, 
            validate_time_consistency, check_dst_transition_warning
        )
        
        origin_airport = data.get('origin_airport')
        destination_airport = data.get('destination_airport')
        
        # Get timezone info
        origin_timezone = origin_airport.timezone if origin_airport else None
        destination_timezone = destination_airport.timezone if destination_airport else None
        
        departure_local = data.get('departure_time_local')
        departure_utc = data.get('departure_time_utc')
        arrival_local = data.get('arrival_time_local')
        arrival_utc = data.get('arrival_time_utc')
        
        print(f"DEBUG: Received data - departure_local: {departure_local}, departure_utc: {departure_utc}")
        print(f"DEBUG: Received data - arrival_local: {arrival_local}, arrival_utc: {arrival_utc}")
        print(f"DEBUG: Flight time: {data.get('flight_time')}")
        print(f"DEBUG: Origin timezone: {origin_timezone}, Destination timezone: {destination_timezone}")
        
        # Convert timezone-aware datetimes to naive for our timezone functions
        if departure_local and hasattr(departure_local, 'tzinfo') and departure_local.tzinfo:
            departure_local = departure_local.replace(tzinfo=None)
        if arrival_local and hasattr(arrival_local, 'tzinfo') and arrival_local.tzinfo:
            arrival_local = arrival_local.replace(tzinfo=None)
        
        # Validate and auto-calculate departure times
        if departure_local and origin_timezone:
            # Check for DST issues
            dst_warning = check_dst_transition_warning(departure_local, origin_timezone)
            if dst_warning and dst_warning['type'] == 'non_existent':
                raise serializers.ValidationError(
                    f"Departure time issue: {dst_warning['message']} {dst_warning['suggestion']}"
                )
            
            # Auto-calculate UTC from local if missing or inconsistent
            if not departure_utc:
                data['departure_time_utc'] = convert_local_to_utc(departure_local, origin_timezone)
            elif not validate_time_consistency(departure_local, departure_utc, origin_timezone):
                # Local time takes precedence, recalculate UTC
                data['departure_time_utc'] = convert_local_to_utc(departure_local, origin_timezone)
                
        elif departure_utc and origin_timezone:
            # Calculate local from UTC if local is missing
            if not departure_local:
                data['departure_time_local'] = convert_utc_to_local(departure_utc, origin_timezone)
        
        # Validate and auto-calculate arrival times
        if arrival_local and destination_timezone:
            # Check for DST issues
            dst_warning = check_dst_transition_warning(arrival_local, destination_timezone)
            if dst_warning and dst_warning['type'] == 'non_existent':
                raise serializers.ValidationError(
                    f"Arrival time issue: {dst_warning['message']} {dst_warning['suggestion']}"
                )
            
            # Auto-calculate UTC from local if missing or inconsistent
            if not arrival_utc:
                data['arrival_time_utc'] = convert_local_to_utc(arrival_local, destination_timezone)
            elif not validate_time_consistency(arrival_local, arrival_utc, destination_timezone):
                # Local time takes precedence, recalculate UTC
                data['arrival_time_utc'] = convert_local_to_utc(arrival_local, destination_timezone)
                
        elif arrival_utc and destination_timezone:
            # Calculate local from UTC if local is missing
            if not arrival_local:
                data['arrival_time_local'] = convert_utc_to_local(arrival_utc, destination_timezone)
        
        # If arrival times are missing or None but we have departure time and flight time, calculate them PROPERLY
        print(f"DEBUG: Checking if should calculate arrivals - arrival_local: {arrival_local}, arrival_utc: {arrival_utc}")
        if (not arrival_local or arrival_local is None) and (not arrival_utc or arrival_utc is None):
            print("DEBUG: Arrival times are missing, attempting to calculate")
            departure_utc_time = data.get('departure_time_utc') or departure_utc
            flight_time = data.get('flight_time')
            
            print(f"DEBUG: For calculation - departure_utc_time: {departure_utc_time}, flight_time: {flight_time}, destination_timezone: {destination_timezone}")
            if departure_utc_time and flight_time and destination_timezone:
                try:
                    print(f"DEBUG: Calculating arrival from departure UTC: {departure_utc_time}, flight time: {flight_time}")
                    
                    # Parse flight_time - handle both string and timedelta formats
                    if isinstance(flight_time, str):
                        time_parts = flight_time.split(':')
                        flight_hours = int(time_parts[0]) + int(time_parts[1]) / 60.0
                        if len(time_parts) > 2:
                            flight_hours += int(time_parts[2]) / 3600.0
                    elif hasattr(flight_time, 'total_seconds'):  # timedelta object
                        flight_hours = flight_time.total_seconds() / 3600.0
                    else:
                        flight_hours = float(flight_time)
                    
                    print(f"DEBUG: Flight duration in hours: {flight_hours}")
                    
                    from datetime import datetime, timedelta
                    
                    # Ensure departure_utc_time is a datetime object
                    if isinstance(departure_utc_time, str):
                        departure_dt = datetime.fromisoformat(departure_utc_time.replace('Z', '+00:00'))
                        if departure_dt.tzinfo:
                            departure_dt = departure_dt.replace(tzinfo=None)
                    else:
                        departure_dt = departure_utc_time.replace(tzinfo=None) if departure_utc_time.tzinfo else departure_utc_time
                    
                    # Calculate arrival in UTC (proper flight time calculation)
                    arrival_utc_dt = departure_dt + timedelta(hours=flight_hours)
                    print(f"DEBUG: Calculated arrival UTC: {arrival_utc_dt}")
                    
                    # Set the UTC arrival time
                    data['arrival_time_utc'] = arrival_utc_dt
                    
                    # Convert UTC to local time for destination airport
                    arrival_local_dt = convert_utc_to_local(arrival_utc_dt, destination_timezone)
                    data['arrival_time_local'] = arrival_local_dt
                    print(f"DEBUG: Calculated arrival local ({destination_timezone}): {arrival_local_dt}")
                        
                except (ValueError, TypeError) as e:
                    print(f"DEBUG: Error calculating arrival times: {str(e)}")
                    # If calculation fails, let the user provide arrival times manually
                    pass
        
        return data

# 4.5) Trip Events
class TripEventWriteSerializer(serializers.ModelSerializer):
    trip_id = serializers.PrimaryKeyRelatedField(source='trip', queryset=Trip.objects.all())
    airport_id = serializers.PrimaryKeyRelatedField(source='airport', queryset=Airport.objects.all())
    crew_line_id = serializers.PrimaryKeyRelatedField(
        source='crew_line', queryset=CrewLine.objects.all(), required=False, allow_null=True
    )

    class Meta:
        model = TripEvent
        fields = (
            "id",
            "trip_id",
            "airport_id",
            "event_type",
            "start_time_local",
            "start_time_utc",
            "end_time_local",
            "end_time_utc",
            "crew_line_id",
            "notes",
        )

    def validate(self, attrs):
        """Validate trip event data and auto-calculate missing timezone conversions."""
        from .timezone_utils import (
            convert_local_to_utc, convert_utc_to_local, 
            validate_time_consistency, check_dst_transition_warning
        )
        
        ev_type = attrs.get("event_type") or (self.instance and self.instance.event_type)
        if ev_type == "CREW_CHANGE":
            # Check for 'crew_line' in attrs because the field uses source='crew_line'
            if not attrs.get("crew_line") and not (self.instance and self.instance.crew_line):
                raise serializers.ValidationError({"crew_line_id": "Required for CREW_CHANGE"})
            # end_time is not required for crew change; treat as instantaneous or short window

        if ev_type == "OVERNIGHT":
            st = attrs.get("start_time_utc") or (self.instance and self.instance.start_time_utc)
            et = attrs.get("end_time_utc") or (self.instance and self.instance.end_time_utc)
            if not (st and et):
                raise serializers.ValidationError({"end_time_utc": "OVERNIGHT requires start and end times"})
            if et <= st:
                raise serializers.ValidationError({"end_time_utc": "Must be after start_time_utc"})

        # Timezone validation and auto-calculation
        airport = attrs.get("airport") or (self.instance and self.instance.airport)
        if airport and airport.timezone:
            warnings = []
            
            # Handle start time timezone conversion
            start_local = attrs.get("start_time_local")
            start_utc = attrs.get("start_time_utc")
            
            # Convert timezone-aware datetimes to naive for our timezone functions
            if start_local and hasattr(start_local, 'tzinfo') and start_local.tzinfo:
                start_local = start_local.replace(tzinfo=None)
            
            if start_local and start_utc:
                # Both provided - validate consistency
                if not validate_time_consistency(start_local, start_utc, airport.timezone):
                    warnings.append("start_time_local and start_time_utc are inconsistent with airport timezone")
            elif start_local and not start_utc:
                # Auto-calculate UTC from local
                try:
                    attrs['start_time_utc'] = convert_local_to_utc(start_local, airport.timezone)
                    # Check for DST warnings
                    dst_warning = check_dst_transition_warning(start_local, airport.timezone)
                    if dst_warning:
                        warnings.append(f"Start time: {dst_warning['message']}")
                except Exception as e:
                    raise serializers.ValidationError({"start_time_local": f"Invalid time for airport timezone: {str(e)}"})
            elif start_utc and not start_local:
                # Auto-calculate local from UTC
                try:
                    attrs['start_time_local'] = convert_utc_to_local(start_utc, airport.timezone)
                except Exception as e:
                    raise serializers.ValidationError({"start_time_utc": f"Cannot convert to airport timezone: {str(e)}"})

            # Handle end time timezone conversion (for OVERNIGHT events)
            end_local = attrs.get("end_time_local")
            end_utc = attrs.get("end_time_utc")
            
            # Convert timezone-aware datetimes to naive for our timezone functions
            if end_local and hasattr(end_local, 'tzinfo') and end_local.tzinfo:
                end_local = end_local.replace(tzinfo=None)
            
            if end_local and end_utc:
                # Both provided - validate consistency
                if not validate_time_consistency(end_local, end_utc, airport.timezone):
                    warnings.append("end_time_local and end_time_utc are inconsistent with airport timezone")
            elif end_local and not end_utc:
                # Auto-calculate UTC from local
                try:
                    attrs['end_time_utc'] = convert_local_to_utc(end_local, airport.timezone)
                    # Check for DST warnings
                    dst_warning = check_dst_transition_warning(end_local, airport.timezone)
                    if dst_warning:
                        warnings.append(f"End time: {dst_warning['message']}")
                except Exception as e:
                    raise serializers.ValidationError({"end_time_local": f"Invalid time for airport timezone: {str(e)}"})
            elif end_utc and not end_local:
                # Auto-calculate local from UTC
                try:
                    attrs['end_time_local'] = convert_utc_to_local(end_utc, airport.timezone)
                except Exception as e:
                    raise serializers.ValidationError({"end_time_utc": f"Cannot convert to airport timezone: {str(e)}"})

            # Store warnings for potential frontend display
            if warnings:
                if not hasattr(self, '_timezone_warnings'):
                    self._timezone_warnings = []
                self._timezone_warnings.extend(warnings)

        return attrs


class TripEventReadSerializer(serializers.ModelSerializer):
    # Return IDs to match your API style
    trip_id = serializers.PrimaryKeyRelatedField(source='trip', read_only=True)
    airport_id = serializers.PrimaryKeyRelatedField(source='airport', read_only=True)
    crew_line_id = serializers.PrimaryKeyRelatedField(source='crew_line', read_only=True)
    airport_timezone_info = serializers.SerializerMethodField()

    class Meta:
        model = TripEvent
        fields = (
            "id",
            "trip_id",
            "airport_id",
            "event_type",
            "start_time_local",
            "start_time_utc",
            "end_time_local",
            "end_time_utc",
            "crew_line_id",
            "notes",
            "created_on",
            "airport_timezone_info",
        )
    
    def get_airport_timezone_info(self, obj):
        """Get timezone information for the event's airport."""
        if not obj.airport or not obj.airport.timezone:
            return None
        
        try:
            from .timezone_utils import get_timezone_info, format_time_with_timezone
            event_time = obj.start_time_utc or obj.start_time_local
            if not event_time:
                return None
                
            tz_info = get_timezone_info(obj.airport.timezone, event_time)
            
            # Add formatted time displays
            if obj.start_time_local:
                tz_info['start_formatted_time'] = format_time_with_timezone(
                    obj.start_time_local, obj.airport.timezone, include_utc=True
                )
            
            if obj.end_time_local:
                tz_info['end_formatted_time'] = format_time_with_timezone(
                    obj.end_time_local, obj.airport.timezone, include_utc=True
                )
            
            return tz_info
        except Exception:
            return None

# 5) Trips
class TripReadSerializer(serializers.ModelSerializer):
    quote = serializers.SerializerMethodField()
    patient = serializers.SerializerMethodField()
    aircraft = AircraftSerializer(read_only=True)
    trip_lines = TripLineReadSerializer(many=True, read_only=True)
    passengers_data = PassengerReadSerializer(source='passengers', many=True, read_only=True)
    events = TripEventReadSerializer(many=True, read_only=True)
    
    class Meta:
        model = Trip
        fields = [
            'id', 'email_chain', 'quote', 'type', 'patient', 'estimated_departure_time',
            'post_flight_duty_time', 'pre_flight_duty_time', 'aircraft', 'trip_number',
            'trip_lines', 'passengers_data', 'events', 'status', 'created_on'
        ]
    
    def get_quote(self, obj):
        if obj.quote:
            return {
                'id': obj.quote.id,
                'quoted_amount': obj.quote.quoted_amount,
                'status': obj.quote.status
            }
        return None
    
    def get_patient(self, obj):
        if obj.patient:
            return {
                'id': obj.patient.id,
                'status': obj.patient.status,
                'info': ContactSerializer(obj.patient.info).data
            }
        return None

class TripWriteSerializer(serializers.ModelSerializer):
    quote = serializers.PrimaryKeyRelatedField(
        queryset=Quote.objects.all(), write_only=True, required=False, allow_null=True
    )
    patient = serializers.PrimaryKeyRelatedField(
        queryset=Patient.objects.all(), write_only=True, required=False, allow_null=True
    )
    aircraft = serializers.PrimaryKeyRelatedField(
        queryset=Aircraft.objects.all(), write_only=True, required=False, allow_null=True
    )
    passenger_ids = serializers.PrimaryKeyRelatedField(
        source='passengers', queryset=Passenger.objects.all(), many=True, write_only=True, required=False
    )
    # Make trip_number optional - it will be auto-generated if not provided
    trip_number = serializers.CharField(required=False, allow_blank=True)
    
    class Meta:
        model = Trip
        fields = [
            'id', 'email_chain', 'quote', 'type', 'patient', 'estimated_departure_time',
            'post_flight_duty_time', 'pre_flight_duty_time', 'aircraft', 'trip_number',
            'passenger_ids', 'status'
        ]

# 6) Transactions
class TransactionPublicReadSerializer(serializers.ModelSerializer):
    """Minimal safe fields for public access by key"""
    class Meta:
        model = Transaction
        fields = ['id', 'amount', 'status', 'created_on']

class TransactionReadSerializer(serializers.ModelSerializer):
    """Full details for staff access"""
    class Meta:
        model = Transaction
        fields = ['id', 'key', 'amount', 'payment_method', 'payment_status', 'payment_date', 
                 'email', 'authorize_net_trans_id', 'created_on', 'created_by', 'modified_on', 'modified_by']

class TransactionProcessWriteSerializer(serializers.ModelSerializer):
    """For processing payments with gateway inputs"""
    class Meta:
        model = Transaction
        fields = ['amount', 'status', 'payment_method', 'gateway_response']

# 7) Quotes
class QuoteReadSerializer(serializers.ModelSerializer):
    contact = ContactSerializer(read_only=True)
    pickup_airport = AirportSerializer(read_only=True)
    dropoff_airport = AirportSerializer(read_only=True)
    patient = serializers.SerializerMethodField()
    payment_agreement = AgreementSerializer(read_only=True)
    consent_for_transport = AgreementSerializer(read_only=True)
    patient_service_agreement = AgreementSerializer(read_only=True)
    transactions = TransactionReadSerializer(many=True, read_only=True)
    trips = serializers.SerializerMethodField()
    total_paid = serializers.SerializerMethodField()
    remaining_balance = serializers.SerializerMethodField()
    
    class Meta:
        model = Quote
        fields = [
            'id', 'quoted_amount', 'contact', 'pickup_airport', 'dropoff_airport',
            'patient', 'payment_agreement', 'consent_for_transport', 'patient_service_agreement',
            'transactions', 'trips', 'status', 'payment_status', 'quote_pdf_status', 'aircraft_type', 'medical_team',
            'estimated_flight_time', 'includes_grounds', 'number_of_stops',
            'cruise_doctor_first_name', 'cruise_doctor_last_name', 'cruise_line', 'cruise_ship',
            'quote_pdf_email', 'created_on', 'total_paid', 'remaining_balance'
        ]
    
    def get_patient(self, obj):
        if obj.patient:
            patient_data = {
                'id': obj.patient.id,
                'status': obj.patient.status
            }
            # Include patient's contact info (name)
            if obj.patient.info:
                patient_data['info'] = {
                    'id': obj.patient.info.id,
                    'first_name': obj.patient.info.first_name,
                    'last_name': obj.patient.info.last_name,
                    'email': obj.patient.info.email
                }
            return patient_data
        return None
    
    def get_total_paid(self, obj):
        """Get total amount paid from completed transactions."""
        return obj.get_total_paid()
    
    def get_remaining_balance(self, obj):
        """Get remaining balance after payments."""
        return obj.get_remaining_balance()
    
    def get_trips(self, obj):
        # Return minimal trip info to avoid circular references
        return [{
            'id': trip.id,
            'trip_number': trip.trip_number,
            'type': trip.type,
            'status': trip.status
        } for trip in obj.trips.all()]

class QuoteWriteSerializer(serializers.ModelSerializer):
    contact = serializers.PrimaryKeyRelatedField(
        queryset=Contact.objects.all(), write_only=True
    )
    pickup_airport = serializers.PrimaryKeyRelatedField(
        queryset=Airport.objects.all(), write_only=True
    )
    dropoff_airport = serializers.PrimaryKeyRelatedField(
        queryset=Airport.objects.all(), write_only=True
    )
    patient = serializers.PrimaryKeyRelatedField(
        queryset=Patient.objects.all(), write_only=True, required=False, allow_null=True
    )
    payment_agreement = serializers.PrimaryKeyRelatedField(
        queryset=Agreement.objects.all(), write_only=True, required=False, allow_null=True
    )
    consent_for_transport = serializers.PrimaryKeyRelatedField(
        queryset=Agreement.objects.all(), write_only=True, required=False, allow_null=True
    )
    patient_service_agreement = serializers.PrimaryKeyRelatedField(
        queryset=Agreement.objects.all(), write_only=True, required=False, allow_null=True
    )
    transaction_ids = serializers.PrimaryKeyRelatedField(
        source='transactions', queryset=Transaction.objects.all(), many=True, write_only=True, required=False
    )
    
    class Meta:
        model = Quote
        fields = [
            'quoted_amount', 'contact', 'pickup_airport', 'dropoff_airport',
            'patient', 'aircraft_type', 'medical_team', 'estimated_flight_time',
            'number_of_stops', 'includes_grounds', 'cruise_line', 'cruise_ship',
            'cruise_doctor_first_name', 'cruise_doctor_last_name', 'quote_pdf_email',
            'payment_agreement', 'consent_for_transport', 'patient_service_agreement', 
            'transaction_ids', 'status', 'payment_status'
        ]

# 7) Documents
class DocumentReadSerializer(serializers.ModelSerializer):
    content_type = serializers.SerializerMethodField()
    download_url = serializers.SerializerMethodField()
    
    class Meta:
        model = Document
        fields = ['id', 'filename', 'flag', 'content_type', 'download_url', 'created_on']
    
    def get_content_type(self, obj):
        # Return MIME type based on file extension
        import mimetypes
        return mimetypes.guess_type(obj.filename)[0] or 'application/octet-stream'
    
    def get_download_url(self, obj):
        # Return download URL for the document
        request = self.context.get('request')
        if request:
            return request.build_absolute_uri(f'/api/documents/{obj.id}/download/')
        return f'/api/documents/{obj.id}/download/'

class DocumentUploadSerializer(serializers.ModelSerializer):
    content = serializers.FileField(write_only=True)
    
    class Meta:
        model = Document
        fields = ['id', 'filename', 'content', 'flag']

# 8) Patient (updated to follow pattern)
class PatientReadSerializer(serializers.ModelSerializer):
    info = ContactSerializer(read_only=True)
    trips = serializers.SerializerMethodField()
    quotes = serializers.SerializerMethodField()
    
    def get_trips(self, obj):
        trips = obj.trips.all()
        return [{'id': trip.id, 'trip_number': trip.trip_number} for trip in trips]
    
    def get_quotes(self, obj):
        quotes = obj.quotes.all()
        return [{'id': quote.id} for quote in quotes]
    
    class Meta:
        model = Patient
        fields = [
            'id', 
            'info', 
            'date_of_birth', 
            'nationality', 
            'passport_number', 
            'passport_expiration_date', 
            'special_instructions', 
            'status', 
            'bed_at_origin', 
            'bed_at_destination', 
            'created_on',
            'trips',
            'quotes'
        ]

class PatientWriteSerializer(serializers.ModelSerializer):
    info = serializers.PrimaryKeyRelatedField(
        queryset=Contact.objects.all(), write_only=True
    )
    
    class Meta:
        model = Patient
        fields = [
            'info', 
            'date_of_birth', 
            'nationality', 
            'passport_number', 
            'passport_expiration_date', 
            'special_instructions', 
            'status', 
            'bed_at_origin', 
            'bed_at_destination'
        ]
    
    def create(self, validated_data):
        # Get contact data for filling deprecated fields
        contact = validated_data['info']
        
        # Use contact data as primary source, fallback to provided data
        validated_data['date_of_birth'] = contact.date_of_birth or validated_data.get('date_of_birth')
        validated_data['nationality'] = contact.nationality or validated_data.get('nationality', '')
        validated_data['passport_number'] = contact.passport_number or validated_data.get('passport_number', '')
        validated_data['passport_expiration_date'] = contact.passport_expiration_date or validated_data.get('passport_expiration_date')
        
        return super().create(validated_data)


class StaffWriteSerializer(serializers.ModelSerializer):
    # Accept a Contact id on write
    contact_id = serializers.PrimaryKeyRelatedField(
        source="contact", queryset=Contact.objects.all()
    )

    class Meta:
        model = Staff
        fields = ("id", "contact_id", "active", "notes")

    def validate_contact_id(self, contact: Contact):
        # Friendly error if a Staff already exists for the Contact (OneToOne is also enforced by DB)
        if self.instance is None and Staff.objects.filter(contact=contact).exists():
            raise serializers.ValidationError("Staff for this contact already exists.")
        return contact


# --- StaffRole ---

class StaffRoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = StaffRole
        fields = ("id", "code", "name", "created_on")


# --- StaffRoleMembership ---

class StaffRoleMembershipWriteSerializer(serializers.ModelSerializer):
    staff_id = serializers.PrimaryKeyRelatedField(
        source="staff", queryset=Staff.objects.all()
    )
    role_id = serializers.PrimaryKeyRelatedField(
        source="role", queryset=StaffRole.objects.all()
    )

    class Meta:
        model = StaffRoleMembership
        fields = ("id", "staff_id", "role_id", "start_on", "end_on")

    def validate(self, attrs):
        start_on = attrs.get("start_on")
        end_on = attrs.get("end_on")
        if start_on and end_on and end_on < start_on:
            raise serializers.ValidationError({"end_on": "end_on cannot be before start_on"})
        return attrs


class StaffRoleMembershipReadSerializer(serializers.ModelSerializer):
    staff_id = serializers.PrimaryKeyRelatedField(source="staff", read_only=True)
    role_id = serializers.PrimaryKeyRelatedField(source="role", read_only=True)
    role = StaffRoleSerializer(read_only=True)

    class Meta:
        model = StaffRoleMembership
        fields = ("id", "staff_id", "role_id", "role", "start_on", "end_on", "created_on")


class StaffReadSerializer(serializers.ModelSerializer):
    # Return the FK as an id to stay consistent with your API style
    contact_id = serializers.PrimaryKeyRelatedField(source="contact", read_only=True)
    # Include full contact information for display purposes
    contact = ContactSerializer(read_only=True)
    # Include role memberships for display purposes
    role_memberships = StaffRoleMembershipReadSerializer(many=True, read_only=True)

    class Meta:
        model = Staff
        fields = ("id", "contact_id", "contact", "active", "notes", "created_on", "role_memberships")


# Contract Serializers
class ContractReadSerializer(serializers.ModelSerializer):
    """Full contract details for reading."""
    trip_id = serializers.PrimaryKeyRelatedField(source="trip", read_only=True)
    customer_contact_id = serializers.PrimaryKeyRelatedField(source="customer_contact", read_only=True)
    patient_id = serializers.PrimaryKeyRelatedField(source="patient", read_only=True)
    
    # Include related object details for display
    trip = TripReadSerializer(read_only=True)
    customer_contact = ContactSerializer(read_only=True)
    patient = PatientReadSerializer(read_only=True)
    unsigned_document = DocumentReadSerializer(read_only=True)
    signed_document = DocumentReadSerializer(read_only=True)
    
    # Display fields
    contract_type_display = serializers.CharField(source='get_contract_type_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    
    class Meta:
        model = Contract
        fields = [
            'id', 'title', 'contract_type', 'contract_type_display', 'status', 'status_display',
            'trip_id', 'trip', 'customer_contact_id', 'customer_contact', 'patient_id', 'patient',
            'docuseal_template_id', 'docuseal_submission_id', 'docuseal_webhook_id',
            'signer_email', 'signer_name', 'date_sent', 'date_signed', 'date_expired',
            'unsigned_document', 'signed_document', 'notes', 'docuseal_response_data',
            'created_on', 'created_by', 'modified_on', 'modified_by'
        ]


class ContractWriteSerializer(serializers.ModelSerializer):
    """Contract creation and update serializer."""
    trip_id = serializers.PrimaryKeyRelatedField(
        source="trip", 
        queryset=Trip.objects.all()
    )
    customer_contact_id = serializers.PrimaryKeyRelatedField(
        source="customer_contact", 
        queryset=Contact.objects.all(),
        required=False,
        allow_null=True
    )
    patient_id = serializers.PrimaryKeyRelatedField(
        source="patient", 
        queryset=Patient.objects.all(),
        required=False,
        allow_null=True
    )
    
    class Meta:
        model = Contract
        fields = [
            'title', 'contract_type', 'trip_id', 'customer_contact_id', 'patient_id',
            'signer_email', 'signer_name', 'notes'
        ]
    
    def validate(self, data):
        """Validate contract data."""
        # Ensure we have a signer (either customer contact or explicit signer info)
        if not data.get('signer_email') and not data.get('customer_contact'):
            raise serializers.ValidationError(
                "Either signer_email or customer_contact_id is required"
            )
        
        return data


class ContractCreateFromTripSerializer(serializers.Serializer):
    """Serializer for creating multiple contracts from a trip."""
    trip_id = serializers.PrimaryKeyRelatedField(queryset=Trip.objects.all())
    contract_types = serializers.MultipleChoiceField(
        choices=Contract.CONTRACT_TYPES,
        allow_empty=False
    )
    send_immediately = serializers.BooleanField(default=False)
    custom_signer_email = serializers.EmailField(required=False, allow_null=True)
    custom_signer_name = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    # Optional pricing fields for payment agreements without quotes
    manual_price = serializers.DecimalField(max_digits=10, decimal_places=2, required=False, allow_null=True)
    manual_price_description = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    
    def validate(self, data):
        """Validate contract creation data."""
        trip = data['trip_id']
        contract_types = data['contract_types']
        custom_signer_email = data.get('custom_signer_email')
        manual_price = data.get('manual_price')
        
        # Check if we have any way to identify a signer
        has_quote_contact = trip.quote and hasattr(trip.quote, 'contact') and trip.quote.contact
        has_patient_contact = trip.patient and trip.patient.info and trip.patient.info.email
        has_custom_signer = custom_signer_email
        
        if not (has_quote_contact or has_patient_contact or has_custom_signer):
            raise serializers.ValidationError(
                "No signer information available. Trip must have a quote with customer contact, "
                "or patient with contact info, or provide custom_signer_email."
            )
        
        # Special validation for payment agreements
        if 'payment_agreement' in contract_types:
            has_quote_pricing = trip.quote and trip.quote.quoted_amount
            if not has_quote_pricing and not manual_price:
                raise serializers.ValidationError(
                    "Payment agreement requires pricing information. "
                    "Either trip must have a quote with quoted_amount or provide manual_price."
                )
        
        return data


class ContractDocuSealActionSerializer(serializers.Serializer):
    """Serializer for DocuSeal-specific actions."""
    action = serializers.ChoiceField(choices=[
        ('send_for_signature', 'Send for Signature'),
        ('resend', 'Resend'),
        ('cancel', 'Cancel'),
        ('archive', 'Archive')
    ])
    custom_message = serializers.CharField(required=False, allow_blank=True)
    
    
class DocuSealWebhookSerializer(serializers.Serializer):
    """Serializer for processing DocuSeal webhook events."""
    event_type = serializers.CharField()
    data = serializers.DictField()
    timestamp = serializers.DateTimeField(required=False)

```


# File: api/contact_service.py

```python
"""
Unified Contact Creation Service

This service provides a clean, consistent way to create contact records
that can be used for patients, staff, customers, and passengers.
All passport information, birth dates, and contact details are now 
stored on the Contact model.
"""

from django.db import transaction
from django.core.exceptions import ValidationError
from rest_framework import serializers
from .models import Contact, Patient, Staff, Passenger
from typing import Dict, Any, Optional, Tuple
from datetime import date


class ContactCreationService:
    """
    Service class for creating contacts and associated records (Patient, Staff, Passenger, etc.)
    """
    
    @staticmethod
    def create_contact_with_related(
        contact_data: Dict[str, Any],
        related_type: str,
        related_data: Optional[Dict[str, Any]] = None,
        created_by=None
    ) -> Tuple[Contact, Any]:
        """
        Create a contact record along with its related record (Patient, Staff, Passenger, etc.)
        
        Args:
            contact_data: Dictionary containing contact information
            related_type: Type of related record ('patient', 'staff', 'passenger', 'customer')
            related_data: Additional data specific to the related record type
            created_by: User who is creating the record
            
        Returns:
            Tuple of (Contact instance, Related instance)
            
        Raises:
            ValidationError: If data validation fails
        """
        if related_data is None:
            related_data = {}
            
        with transaction.atomic():
            # Validate and create contact
            contact = ContactCreationService._create_contact(contact_data, created_by)
            
            # Create related record
            related_instance = None
            if related_type == 'patient':
                related_instance = ContactCreationService._create_patient(contact, related_data, created_by)
            elif related_type == 'staff':
                related_instance = ContactCreationService._create_staff(contact, related_data, created_by)
            elif related_type == 'passenger':
                related_instance = ContactCreationService._create_passenger(contact, related_data, created_by)
            elif related_type == 'customer':
                # For customers, we just need the contact record
                related_instance = contact
            else:
                raise ValidationError(f"Unknown related type: {related_type}")
                
            return contact, related_instance
    
    @staticmethod
    def _create_contact(contact_data: Dict[str, Any], created_by=None) -> Contact:
        """
        Create and validate a Contact record
        """
        # Validate required fields
        ContactCreationService._validate_contact_data(contact_data)
        
        # Create contact instance
        contact = Contact(
            # Personal Information
            first_name=contact_data.get('first_name', '').strip(),
            last_name=contact_data.get('last_name', '').strip(),
            business_name=contact_data.get('business_name', '').strip(),
            
            # Contact Information
            email=contact_data.get('email', '').strip(),
            phone=contact_data.get('phone', '').strip(),
            
            # Address Information
            address_line1=contact_data.get('address_line1', '').strip(),
            address_line2=contact_data.get('address_line2', '').strip(),
            city=contact_data.get('city', '').strip(),
            state=contact_data.get('state', '').strip(),
            zip=contact_data.get('zip', '').strip(),
            country=contact_data.get('country', '').strip(),
            
            # Personal Details (now on Contact table)
            nationality=contact_data.get('nationality', '').strip(),
            date_of_birth=contact_data.get('date_of_birth'),
            passport_number=contact_data.get('passport_number', '').strip(),
            passport_expiration_date=contact_data.get('passport_expiration_date'),
            
            # Audit fields
            created_by=created_by,
            status=contact_data.get('status', 'active')
        )
        
        # Validate and save
        contact.full_clean()
        contact.save()
        
        return contact
    
    @staticmethod
    def _create_patient(contact: Contact, patient_data: Dict[str, Any], created_by=None) -> Patient:
        """
        Create a Patient record linked to the Contact
        """
        patient = Patient(
            info=contact,
            special_instructions=patient_data.get('special_instructions', '').strip(),
            bed_at_origin=patient_data.get('bed_at_origin', False),
            bed_at_destination=patient_data.get('bed_at_destination', False),
            status=patient_data.get('status', 'pending'),
            created_by=created_by,
            
            # Note: These fields are now deprecated and will be removed in future migration
            # The data should come from contact.date_of_birth, contact.nationality, etc.
            date_of_birth=contact.date_of_birth or date.today(),
            nationality=contact.nationality or 'Unknown',
            passport_number=contact.passport_number or '',
            passport_expiration_date=contact.passport_expiration_date or date.today(),
        )
        
        patient.full_clean()
        patient.save()
        
        return patient
    
    @staticmethod
    def _create_staff(contact: Contact, staff_data: Dict[str, Any], created_by=None) -> Staff:
        """
        Create a Staff record linked to the Contact
        """
        # Check if staff already exists for this contact
        if Staff.objects.filter(contact=contact).exists():
            raise ValidationError("Staff record already exists for this contact")
            
        staff = Staff(
            contact=contact,
            active=staff_data.get('active', True),
            notes=staff_data.get('notes', '').strip(),
            created_by=created_by
        )
        
        staff.full_clean()
        staff.save()
        
        return staff
    
    @staticmethod
    def _create_passenger(contact: Contact, passenger_data: Dict[str, Any], created_by=None) -> Passenger:
        """
        Create a Passenger record linked to the Contact
        """
        passenger = Passenger(
            info=contact,
            contact_number=passenger_data.get('contact_number', '').strip(),
            notes=passenger_data.get('notes', '').strip(),
            status=passenger_data.get('status', 'active'),
            created_by=created_by,
            
            # Note: These fields are now deprecated and will be removed in future migration
            # The data should come from contact.date_of_birth, contact.nationality, etc.
            date_of_birth=contact.date_of_birth,
            nationality=contact.nationality or '',
            passport_number=contact.passport_number or '',
            passport_expiration_date=contact.passport_expiration_date,
        )
        
        passenger.full_clean()
        passenger.save()
        
        return passenger
    
    @staticmethod
    def _validate_contact_data(contact_data: Dict[str, Any]):
        """
        Validate contact data before creation
        """
        # Check that either personal name or business name is provided
        first_name = contact_data.get('first_name', '').strip()
        last_name = contact_data.get('last_name', '').strip()
        business_name = contact_data.get('business_name', '').strip()
        
        if not first_name and not last_name and not business_name:
            raise ValidationError("Either first/last name or business name is required")
        
        # Validate email format if provided
        email = contact_data.get('email', '').strip()
        if email and '@' not in email:
            raise ValidationError("Invalid email format")
        
        # Validate passport expiration is after birth date if both provided
        birth_date = contact_data.get('date_of_birth')
        passport_expiration = contact_data.get('passport_expiration_date')
        
        if birth_date and passport_expiration and passport_expiration <= birth_date:
            raise ValidationError("Passport expiration date must be after date of birth")
    
    @staticmethod
    def update_contact_and_related(
        contact: Contact,
        contact_data: Dict[str, Any],
        related_instance: Any = None,
        related_data: Optional[Dict[str, Any]] = None
    ) -> Tuple[Contact, Any]:
        """
        Update existing contact and related record
        """
        with transaction.atomic():
            # Update contact fields
            for field, value in contact_data.items():
                if hasattr(contact, field):
                    if isinstance(value, str):
                        value = value.strip()
                    setattr(contact, field, value)
            
            contact.full_clean()
            contact.save()
            
            # Update related record if provided
            if related_instance and related_data:
                for field, value in related_data.items():
                    if hasattr(related_instance, field):
                        if isinstance(value, str):
                            value = value.strip()
                        setattr(related_instance, field, value)
                
                related_instance.full_clean()
                related_instance.save()
            
            return contact, related_instance


class ContactCreationSerializer(serializers.Serializer):
    """
    Serializer for unified contact creation requests
    """
    # Contact data
    first_name = serializers.CharField(max_length=100, required=False, allow_blank=True)
    last_name = serializers.CharField(max_length=100, required=False, allow_blank=True)
    business_name = serializers.CharField(max_length=255, required=False, allow_blank=True)
    email = serializers.EmailField(required=False, allow_blank=True)
    phone = serializers.CharField(max_length=20, required=False, allow_blank=True)
    
    # Address fields
    address_line1 = serializers.CharField(max_length=255, required=False, allow_blank=True)
    address_line2 = serializers.CharField(max_length=255, required=False, allow_blank=True)
    city = serializers.CharField(max_length=100, required=False, allow_blank=True)
    state = serializers.CharField(max_length=100, required=False, allow_blank=True)
    zip = serializers.CharField(max_length=20, required=False, allow_blank=True)
    country = serializers.CharField(max_length=100, required=False, allow_blank=True)
    
    # Personal details (now on Contact table)
    nationality = serializers.CharField(max_length=100, required=False, allow_blank=True)
    date_of_birth = serializers.DateField(required=False, allow_null=True)
    passport_number = serializers.CharField(max_length=100, required=False, allow_blank=True)
    passport_expiration_date = serializers.DateField(required=False, allow_null=True)
    
    # Related record type and data
    related_type = serializers.ChoiceField(
        choices=['patient', 'staff', 'passenger', 'customer'],
        required=True
    )
    related_data = serializers.JSONField(required=False, default=dict)
    
    def validate(self, data):
        # Ensure either personal or business name is provided
        first_name = data.get('first_name', '').strip()
        last_name = data.get('last_name', '').strip()
        business_name = data.get('business_name', '').strip()
        
        if not first_name and not last_name and not business_name:
            raise serializers.ValidationError(
                "Either first/last name or business name is required"
            )
        
        return data
    
    def create(self, validated_data):
        # Extract related data
        related_type = validated_data.pop('related_type')
        related_data = validated_data.pop('related_data', {})
        
        # Get user from context
        created_by = self.context.get('request').user if self.context.get('request') else None
        
        # Create contact and related record
        contact, related_instance = ContactCreationService.create_contact_with_related(
            contact_data=validated_data,
            related_type=related_type,
            related_data=related_data,
            created_by=created_by
        )
        
        return {
            'contact': contact,
            'related_instance': related_instance,
            'related_type': related_type
        }
```


# File: api/external/airport.py

```python
import requests
from bs4 import BeautifulSoup

def get_flight_aware(request):
    url = f"https://flightaware.com/{request}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36"
    }

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f"Failed to retrieve data. Status code: {response.status_code}")
        return None

    return BeautifulSoup(response.content, "html.parser")

def get_airport(airport_code):
    url = f"resources/airport/{airport_code}"
    return get_flight_aware(url)


def parse_fuel_cost(soup):
    final = []
    for fbo in soup.find_all('tr', class_='fuel_facility'):
        new = {
            'fbo_name' : fbo.find('a').text.strip(),
            'jet_a_cost': fbo.find_all('td')[6].text.strip(),
        }
        if new['jet_a_cost']:
            final.append(new)

    return final


def get_fbo(airport_code, name):
    url = f"resources/airport/{airport_code}/services/FBO/{name.replace(' ', '%20')}"
    return get_flight_aware(url)

def parse_fbo(soup):
    website = soup.find('div', class_="airportBoardContainer").find('a').text.strip()
    phone = soup.find('div', class_="airportBoardContainer").find_all('td')[3].text.strip().replace('+','').replace('-','')
    return website, phone if phone else None

def parse_timezone(soup):
    timezone = soup.find('table').find_all('td')[2].find('span').text.strip()
    return timezone

if __name__ == "__main__":
    soup = get_airport("KTPA")
    print(parse_fuel_cost(soup))

```


# File: api/external/aircraft.py

```python
from bs4 import BeautifulSoup
from airport import get_flight_aware


def get_current(tailnumber):
    url = f"resources/aircraft/{tailnumber}"
    return get_flight_aware(url)
```


# File: api/tests/run_all_tests.py

```python
#!/usr/bin/env python3
"""
Run all API endpoint tests against a live server.
This script runs all individual test files and provides a summary.
"""
import sys
import os
import subprocess
import time
from datetime import datetime

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from base_test import APITester


def check_server_connectivity():
    """Check if the API server is running and accessible."""
    print("🔍 Checking server connectivity...")
    tester = APITester()
    
    try:
        # Use requests directly to avoid status code checking
        import requests
        response = requests.get(f"{tester.base_url}/api/")
        tester.print_response(response, "Server Connectivity Check")
        
        # Accept 401 as valid since /api/ requires authentication
        status_code = response.status_code
        print(f"DEBUG: Response status code: {status_code}")
        if status_code in [200, 401]:
            print("✅ API server is reachable")
            return True
        else:
            print(f"❌ API server returned error status: {status_code}")
            return False
    except Exception as e:
        print(f"❌ Cannot connect to API server: {e}")
        return False


def run_test_file(test_file):
    """Run a single test file and capture output."""
    print(f"\n{'='*80}")
    print(f"🧪 RUNNING: {test_file}")
    print(f"{'='*80}")
    
    try:
        # Run the test file
        result = subprocess.run(
            [sys.executable, test_file],
            capture_output=True,
            text=True,
            timeout=60  # 60 second timeout per test file
        )
        
        # Print the output
        if result.stdout:
            print(result.stdout)
        
        if result.stderr:
            print("STDERR:")
            print(result.stderr)
        
        return result.returncode == 0
    
    except subprocess.TimeoutExpired:
        print(f"❌ Test {test_file} timed out after 60 seconds")
        return False
    except Exception as e:
        print(f"❌ Error running {test_file}: {e}")
        return False


def main():
    """Run all API tests."""
    print("🚀 JET-MAIN API ENDPOINT TEST SUITE")
    print("=" * 80)
    print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 80)
    
    # Check server connectivity first
    if not check_server_connectivity():
        print("\n❌ Cannot connect to API server. Please ensure the server is running at http://localhost:8000")
        print("Start the server with: python manage.py runserver")
        sys.exit(1)
    
    # Define test files in order
    test_files = [
        "test_userprofile.py",
        "test_passengers.py", 
        "test_crew_lines.py",
        "test_trip_lines.py",
        "test_trips.py",
        "test_quotes.py",
        "test_patients.py",
        "test_documents.py",
        "test_transactions.py"
    ]
    
    # Track results
    results = {}
    start_time = time.time()
    
    # Run each test file
    for test_file in test_files:
        if os.path.exists(test_file):
            success = run_test_file(test_file)
            results[test_file] = success
        else:
            print(f"⚠️  Test file {test_file} not found, skipping...")
            results[test_file] = False
    
    # Print summary
    end_time = time.time()
    duration = end_time - start_time
    
    print(f"\n{'='*80}")
    print("📊 TEST SUMMARY")
    print(f"{'='*80}")
    print(f"Total duration: {duration:.2f} seconds")
    print(f"Completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    passed = 0
    failed = 0
    
    for test_file, success in results.items():
        status = "✅ PASSED" if success else "❌ FAILED"
        print(f"{test_file:<25} {status}")
        if success:
            passed += 1
        else:
            failed += 1
    
    print(f"\n📈 RESULTS: {passed} passed, {failed} failed out of {len(results)} tests")
    
    if failed > 0:
        print("\n⚠️  Some tests failed. Check the output above for details.")
        print("Common issues:")
        print("- Authentication credentials may need adjustment")
        print("- Test data (IDs) may not exist in the database")
        print("- Permissions may not be configured correctly")
        print("- Some endpoints may not be implemented yet")
    else:
        print("\n🎉 All tests completed successfully!")
    
    print(f"\n{'='*80}")
    
    return failed == 0


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

```


# File: api/tests/__init__.py

```python
# Test package for API endpoints

```


# File: api/tests/test_patients.py

```python
#!/usr/bin/env python3
"""
Test Patient endpoints (/api/patients/)
Run this against a live server to test the standardized CRUD endpoints.
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from base_test import APITester


def test_patient_endpoints():
    """Test Patient CRUD endpoints."""
    tester = APITester()
    
    print("🧪 TESTING PATIENT ENDPOINTS")
    print("=" * 80)
    
    # Test authentication
    print("Attempting authentication...")
    if not tester.authenticate("admin", "admin"):
        print("⚠️  Authentication failed, continuing without auth...")
    
    # Test 1: List patients (GET /api/patients/)
    print("\n📋 TEST 1: List Patients")
    response = tester.test_endpoint(
        "/api/patients/",
        method="GET",
        title="List Patients"
    )
    
    # Test 2: Get specific patient (if we have data)
    patient_id = None
    if response and response.status_code == 200:
        try:
            data = response.json()
            results = data.get('results', [])
            if results:
                patient_id = results[0].get('id')
                print(f"\n🔍 TEST 2: Get Specific Patient (ID: {patient_id})")
                tester.test_endpoint(
                    f"/api/patients/{patient_id}/",
                    method="GET",
                    title=f"Get Patient {patient_id}"
                )
        except:
            print("\n⚠️  Could not extract patient ID for detail test")
    
    # Test 3: Create new patient (POST /api/patients/)
    print("\n➕ TEST 3: Create Patient (Write Serializer Test)")
    create_data = {
        "info": 1,  # Expects Contact ID only
        "status": "active",
        "medical_notes": "Test patient creation",
        "emergency_contact": "Emergency Contact Name",
        "emergency_phone": "+1234567890"
    }
    
    tester.test_endpoint(
        "/api/patients/",
        method="POST",
        data=create_data,
        expect_status=201,
        title="Create Patient with ID only"
    )
    
    # Test 4: Try to create with nested objects (should fail)
    print("\n❌ TEST 4: Create Patient with Nested Objects (Should Fail)")
    invalid_data = {
        "info": {  # Should be info_id
            "first_name": "John",
            "last_name": "Patient",
            "email": "patient@example.com"
        },
        "status": "active",
        "medical_notes": "Invalid patient creation"
    }
    
    tester.test_endpoint(
        "/api/patients/",
        method="POST",
        data=invalid_data,
        expect_status=400,
        title="Create Patient with nested objects (should fail)"
    )
    
    # Test 5: Update patient (if we have an ID)
    if patient_id:
        print(f"\n✏️  TEST 5: Update Patient (ID: {patient_id})")
        update_data = {
            "info": 1,
            "status": "inactive",  # Changed status
            "medical_notes": "Updated patient medical notes",
            "emergency_contact": "Updated Emergency Contact",
            "emergency_phone": "+1987654321"
        }
        
        tester.test_endpoint(
            f"/api/patients/{patient_id}/",
            method="PUT",
            data=update_data,
            expect_status=200,
            title=f"Update Patient {patient_id} with ID only"
        )
    
    print("\n✅ Patient endpoint tests completed!")


if __name__ == "__main__":
    test_patient_endpoints()

```


# File: api/tests/test_transactions.py

```python
#!/usr/bin/env python3
"""
Test Transaction endpoints (/api/transactions/)
Run this against a live server to test the standardized CRUD endpoints.
Special focus on public vs staff access patterns.
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from base_test import APITester


def test_transaction_endpoints():
    """Test Transaction CRUD endpoints with special public/staff logic."""
    tester = APITester()
    
    print("🧪 TESTING TRANSACTION ENDPOINTS")
    print("=" * 80)
    
    # Test authentication
    print("Attempting authentication...")
    authenticated = tester.authenticate("admin", "admin")
    if not authenticated:
        print("⚠️  Authentication failed, will test public access...")
    
    # Test 1: List transactions (GET /api/transactions/) - Staff only
    print("\n📋 TEST 1: List Transactions (Staff Access)")
    response = tester.test_endpoint(
        "/api/transactions/",
        method="GET",
        title="List Transactions (Staff)"
    )
    
    # Test 2: Get specific transaction (if we have data)
    transaction_id = None
    transaction_key = None
    if response and response.status_code == 200:
        try:
            data = response.json()
            results = data.get('results', [])
            if results:
                transaction_id = results[0].get('id')
                transaction_key = results[0].get('key')
                
                print(f"\n🔍 TEST 2: Get Specific Transaction (ID: {transaction_id})")
                tester.test_endpoint(
                    f"/api/transactions/{transaction_id}/",
                    method="GET",
                    title=f"Get Transaction {transaction_id} (Staff)"
                )
        except:
            print("\n⚠️  Could not extract transaction data for detail test")
    
    # Test 3: Public read by key (no authentication required)
    if transaction_key:
        print(f"\n🌐 TEST 3: Public Read by Key (Key: {transaction_key})")
        
        # Remove authentication for public test
        public_tester = APITester()  # No auth
        
        public_tester.test_endpoint(
            f"/api/transactions/by-key/{transaction_key}/",
            method="GET",
            title=f"Public Read Transaction by Key {transaction_key}"
        )
        
        # Restore authentication for remaining tests
        if authenticated:
            tester.authenticate("admin", "admin")
    
    # Test 4: Create new transaction (POST /api/transactions/)
    print("\n➕ TEST 4: Create Transaction")
    create_data = {
        "amount": 2500.00,
        "payment_method": "credit_card",
        "email": "customer@example.com",
        "payment_status": "pending",
        "description": "Test transaction creation"
    }
    
    response = tester.test_endpoint(
        "/api/transactions/",
        method="POST",
        data=create_data,
        expect_status=201,
        title="Create Transaction"
    )
    
    # Get the created transaction ID for further tests
    created_transaction_id = None
    if response and response.status_code == 201:
        try:
            created_data = response.json()
            created_transaction_id = created_data.get('id')
        except:
            pass
    
    # Test 5: Process payment (special endpoint)
    if created_transaction_id:
        print(f"\n💳 TEST 5: Process Payment (ID: {created_transaction_id})")
        payment_data = {
            "payment_status": "completed",
            "payment_method": "credit_card",
            "transaction_reference": "ref_12345"
        }
        
        tester.test_endpoint(
            f"/api/transactions/{created_transaction_id}/process_payment/",
            method="POST",
            data=payment_data,
            expect_status=200,
            title=f"Process Payment for Transaction {created_transaction_id}"
        )
    
    # Test 6: Update transaction (if we have an ID)
    if transaction_id:
        print(f"\n✏️  TEST 6: Update Transaction (ID: {transaction_id})")
        update_data = {
            "amount": 3000.00,  # Changed amount
            "payment_method": "bank_transfer",  # Changed method
            "payment_status": "processing",  # Changed status
            "email": "updated@example.com"
        }
        
        tester.test_endpoint(
            f"/api/transactions/{transaction_id}/",
            method="PUT",
            data=update_data,
            expect_status=200,
            title=f"Update Transaction {transaction_id}"
        )
    
    # Test 7: Test access control differences
    print("\n🔒 TEST 7: Access Control Verification")
    
    # Test without authentication
    no_auth_tester = APITester()
    
    print("\n   7a: List transactions without auth (should fail)")
    no_auth_tester.test_endpoint(
        "/api/transactions/",
        method="GET",
        expect_status=401,
        title="List Transactions (No Auth - Should Fail)"
    )
    
    if transaction_id:
        print(f"\n   7b: Get transaction detail without auth (should fail)")
        no_auth_tester.test_endpoint(
            f"/api/transactions/{transaction_id}/",
            method="GET",
            expect_status=401,
            title=f"Get Transaction {transaction_id} (No Auth - Should Fail)"
        )
    
    if transaction_key:
        print(f"\n   7c: Public read by key without auth (should succeed)")
        no_auth_tester.test_endpoint(
            f"/api/transactions/by-key/{transaction_key}/",
            method="GET",
            expect_status=200,
            title=f"Public Read by Key {transaction_key} (No Auth - Should Succeed)"
        )
    
    print("\n✅ Transaction endpoint tests completed!")


if __name__ == "__main__":
    test_transaction_endpoints()

```


# File: api/tests/base_test.py

```python
"""
Base test utilities for API endpoint testing.
Tests are designed to run against a live server.
"""
import json
import requests
import sys
from typing import Dict, Any, Optional


class APITester:
    """Base class for testing API endpoints against a running server."""
    
    def __init__(self, base_url: str = "http://127.0.0.1:8000", auth_token: Optional[str] = None):
        self.base_url = base_url.rstrip('/')
        self.session = requests.Session()
        
        if auth_token:
            self.session.headers.update({
                'Authorization': f'Bearer {auth_token}'
            })
    
    def authenticate(self, username: str, password: str) -> bool:
        """Authenticate with the API and store the token."""
        try:
            response = self.session.post(
                f"{self.base_url}/api/token/",
                json={"username": username, "password": password}
            )
            
            if response.status_code == 200:
                data = response.json()
                token = data.get('access') or data.get('token')
                if token:
                    self.session.headers.update({
                        'Authorization': f'Bearer {token}'
                    })
                    return True
            return False
        except Exception as e:
            print(f"Authentication failed: {e}")
            return False
    
    def print_response(self, response: requests.Response, title: str):
        """Print formatted response details."""
        print(f"\n{'='*60}")
        print(f"TEST: {title}")
        print(f"{'='*60}")
        print(f"URL: {response.request.method} {response.url}")
        print(f"Status Code: {response.status_code}")
        
        if response.request.body:
            print(f"Request Body: {response.request.body}")
        
        try:
            response_data = response.json()
            print(f"Response Body:")
            print(json.dumps(response_data, indent=2))
        except:
            print(f"Response Body (raw): {response.text}")
        
        print(f"{'='*60}\n")
    
    def check_no_id_fields(self, data: Any, path: str = "") -> list:
        """Check for _id fields in response data and return violations."""
        violations = []
        
        if isinstance(data, dict):
            for key, value in data.items():
                current_path = f"{path}.{key}" if path else key
                # Check for _id fields (but allow 'id' itself)
                if key.endswith('_id') and key != 'id':
                    violations.append(f"Found _id field '{key}' at path '{current_path}'")
                violations.extend(self.check_no_id_fields(value, current_path))
        elif isinstance(data, list):
            for i, item in enumerate(data):
                violations.extend(self.check_no_id_fields(item, f"{path}[{i}]"))
        
        return violations
    
    def test_endpoint(self, endpoint: str, method: str = "GET", data: Dict = None, 
                     expect_status: int = 200, title: str = None) -> requests.Response:
        """Test an endpoint and print results."""
        url = f"{self.base_url}{endpoint}"
        title = title or f"{method} {endpoint}"
        
        try:
            if method.upper() == "GET":
                response = self.session.get(url)
            elif method.upper() == "POST":
                response = self.session.post(url, json=data)
            elif method.upper() == "PUT":
                response = self.session.put(url, json=data)
            elif method.upper() == "PATCH":
                response = self.session.patch(url, json=data)
            elif method.upper() == "DELETE":
                response = self.session.delete(url)
            else:
                raise ValueError(f"Unsupported method: {method}")
            
            self.print_response(response, title)
            
            # Check for _id fields in GET responses
            if method.upper() == "GET" and response.status_code == 200:
                try:
                    response_data = response.json()
                    violations = self.check_no_id_fields(response_data)
                    if violations:
                        print("⚠️  _ID FIELD VIOLATIONS FOUND:")
                        for violation in violations:
                            print(f"   - {violation}")
                    else:
                        print("✅ No _id fields found in response")
                except:
                    pass
            
            # Check status code
            if response.status_code == expect_status:
                print(f"✅ Status code matches expected: {expect_status}")
            else:
                print(f"❌ Status code {response.status_code} != expected {expect_status}")
            
            return response
            
        except Exception as e:
            print(f"❌ Request failed: {e}")
            return None


def main():
    """Run basic connectivity test."""
    tester = APITester()
    
    print("Testing API connectivity...")
    response = tester.test_endpoint("/api/", title="API Root Connectivity Test")
    
    if response and response.status_code < 500:
        print("✅ API server is reachable")
    else:
        print("❌ API server is not reachable")
        sys.exit(1)


if __name__ == "__main__":
    main()

```


# File: api/tests/test_documents.py

```python
#!/usr/bin/env python3
"""
Test Document endpoints (/api/documents/)
Run this against a live server to test the standardized CRUD endpoints.
"""
import sys
import os
import base64
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from base_test import APITester


def test_document_endpoints():
    """Test Document CRUD endpoints."""
    tester = APITester()
    
    print("🧪 TESTING DOCUMENT ENDPOINTS")
    print("=" * 80)
    
    # Test authentication
    print("Attempting authentication...")
    if not tester.authenticate("admin", "admin"):
        print("⚠️  Authentication failed, continuing without auth...")
    
    # Test 1: List documents (GET /api/documents/)
    print("\n📋 TEST 1: List Documents")
    response = tester.test_endpoint(
        "/api/documents/",
        method="GET",
        title="List Documents"
    )
    
    # Test 2: Get specific document (if we have data)
    document_id = None
    if response and response.status_code == 200:
        try:
            data = response.json()
            results = data.get('results', [])
            if results:
                document_id = results[0].get('id')
                print(f"\n🔍 TEST 2: Get Specific Document (ID: {document_id})")
                detail_response = tester.test_endpoint(
                    f"/api/documents/{document_id}/",
                    method="GET",
                    title=f"Get Document {document_id}"
                )
                
                # Check for enhanced fields in read serializer
                if detail_response and detail_response.status_code == 200:
                    try:
                        doc_data = detail_response.json()
                        enhanced_fields = ['content_type', 'download_url']
                        found_fields = [field for field in enhanced_fields if field in doc_data]
                        missing_fields = [field for field in enhanced_fields if field not in doc_data]
                        
                        if found_fields:
                            print(f"✅ Enhanced fields found: {found_fields}")
                        if missing_fields:
                            print(f"⚠️  Enhanced fields missing: {missing_fields}")
                    except:
                        pass
                
                # Test download endpoint
                print(f"\n⬇️  TEST 2b: Download Document (ID: {document_id})")
                tester.test_endpoint(
                    f"/api/documents/{document_id}/download/",
                    method="GET",
                    title=f"Download Document {document_id}"
                )
        except:
            print("\n⚠️  Could not extract document ID for detail test")
    
    # Test 3: Upload new document (POST /api/documents/)
    print("\n📤 TEST 3: Upload Document")
    
    # Create sample file content
    sample_content = b"This is a test document content for API testing."
    encoded_content = base64.b64encode(sample_content).decode('utf-8')
    
    upload_data = {
        "filename": "test_upload.txt",
        "flag": "contract",
        "content": encoded_content,  # Base64 encoded content
        "description": "Test document upload via API"
    }
    
    response = tester.test_endpoint(
        "/api/documents/",
        method="POST",
        data=upload_data,
        expect_status=201,
        title="Upload Document"
    )
    
    # Get the uploaded document ID for further tests
    uploaded_document_id = None
    if response and response.status_code == 201:
        try:
            uploaded_data = response.json()
            uploaded_document_id = uploaded_data.get('id')
        except:
            pass
    
    # Test 4: Try alternative upload format
    print("\n📤 TEST 4: Upload Document (Alternative Format)")
    upload_data_alt = {
        "filename": "test_upload_2.pdf",
        "flag": "passport",
        "content": sample_content,  # Raw bytes (may need different handling)
        "description": "Alternative upload test"
    }
    
    tester.test_endpoint(
        "/api/documents/",
        method="POST",
        data=upload_data_alt,
        expect_status=201,
        title="Upload Document (Alternative Format)"
    )
    
    # Test 5: Update document (if we have an ID)
    if uploaded_document_id:
        print(f"\n✏️  TEST 5: Update Document (ID: {uploaded_document_id})")
        update_data = {
            "filename": "updated_test_file.txt",
            "flag": "medical_record",  # Changed flag
            "content": base64.b64encode(b"Updated document content").decode('utf-8'),
            "description": "Updated document description"
        }
        
        tester.test_endpoint(
            f"/api/documents/{uploaded_document_id}/",
            method="PUT",
            data=update_data,
            expect_status=200,
            title=f"Update Document {uploaded_document_id}"
        )
        
        # Test download of updated document
        print(f"\n⬇️  TEST 5b: Download Updated Document")
        tester.test_endpoint(
            f"/api/documents/{uploaded_document_id}/download/",
            method="GET",
            title=f"Download Updated Document {uploaded_document_id}"
        )
    
    # Test 6: Partial update (PATCH)
    if document_id:
        print(f"\n🔧 TEST 6: Partial Update Document (ID: {document_id})")
        patch_data = {
            "description": "Partially updated description",
            "flag": "updated_flag"
        }
        
        tester.test_endpoint(
            f"/api/documents/{document_id}/",
            method="PATCH",
            data=patch_data,
            expect_status=200,
            title=f"Partial Update Document {document_id}"
        )
    
    # Test 7: Test file type validation (if implemented)
    print("\n❌ TEST 7: Invalid File Upload (Testing Validation)")
    invalid_upload = {
        "filename": "",  # Empty filename
        "flag": "invalid_flag",
        "content": "invalid_content_format"
    }
    
    tester.test_endpoint(
        "/api/documents/",
        method="POST",
        data=invalid_upload,
        expect_status=400,
        title="Invalid Document Upload (Should Fail)"
    )
    
    print("\n✅ Document endpoint tests completed!")


if __name__ == "__main__":
    test_document_endpoints()

```


# File: api/tests/test_passengers.py

```python
#!/usr/bin/env python3
"""
Test Passenger endpoints (/api/passengers/)
Run this against a live server to test the standardized CRUD endpoints.
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from base_test import APITester


def test_passenger_endpoints():
    """Test Passenger CRUD endpoints."""
    tester = APITester()
    
    print("🧪 TESTING PASSENGER ENDPOINTS")
    print("=" * 80)
    
    # Test authentication
    print("Attempting authentication...")
    if not tester.authenticate("admin", "admin"):
        print("⚠️  Authentication failed, continuing without auth...")
    
    # Test 1: List passengers (GET /api/passengers/)
    print("\n📋 TEST 1: List Passengers")
    response = tester.test_endpoint(
        "/api/passengers/",
        method="GET",
        title="List Passengers"
    )
    
    # Test 2: Get specific passenger (if we have data)
    passenger_id = None
    if response and response.status_code == 200:
        try:
            data = response.json()
            results = data.get('results', [])
            if results:
                passenger_id = results[0].get('id')
                print(f"\n🔍 TEST 2: Get Specific Passenger (ID: {passenger_id})")
                tester.test_endpoint(
                    f"/api/passengers/{passenger_id}/",
                    method="GET",
                    title=f"Get Passenger {passenger_id}"
                )
        except:
            print("\n⚠️  Could not extract passenger ID for detail test")
    
    # Test 3: Create new passenger (POST /api/passengers/)
    print("\n➕ TEST 3: Create Passenger (Write Serializer Test)")
    create_data = {
        "info": 1,  # Expects Contact ID only
        "date_of_birth": "1990-01-01",
        "nationality": "US",
        "passport_number": "123456789",
        "passport_expiration_date": "2030-01-01",
        "contact_number": "+1234567890",
        "passport_document": 1,  # Expects Document ID only
        "status": "active"
    }
    
    tester.test_endpoint(
        "/api/passengers/",
        method="POST",
        data=create_data,
        expect_status=201,
        title="Create Passenger with IDs only"
    )
    
    # Test 4: Try to create with nested objects (should fail)
    print("\n❌ TEST 4: Create Passenger with Nested Objects (Should Fail)")
    invalid_data = {
        "info": {  # Should be info_id
            "first_name": "John",
            "last_name": "Doe"
        },
        "passport_document": {  # Should be passport_document_id
            "filename": "passport.pdf"
        },
        "date_of_birth": "1990-01-01",
        "nationality": "US"
    }
    
    tester.test_endpoint(
        "/api/passengers/",
        method="POST",
        data=invalid_data,
        expect_status=400,
        title="Create Passenger with nested objects (should fail)"
    )
    
    # Test 5: Update passenger (if we have an ID)
    if passenger_id:
        print(f"\n✏️  TEST 5: Update Passenger (ID: {passenger_id})")
        update_data = {
            "info": 1,
            "date_of_birth": "1990-01-01",
            "nationality": "CA",  # Changed nationality
            "passport_number": "987654321",  # Changed passport
            "passport_expiration_date": "2031-01-01",
            "contact_number": "+1987654321",
            "status": "active"
        }
        
        tester.test_endpoint(
            f"/api/passengers/{passenger_id}/",
            method="PUT",
            data=update_data,
            expect_status=200,
            title=f"Update Passenger {passenger_id} with IDs only"
        )
    
    print("\n✅ Passenger endpoint tests completed!")


if __name__ == "__main__":
    test_passenger_endpoints()

```


# File: api/tests/test_trips.py

```python
#!/usr/bin/env python3
"""
Test Trip endpoints (/api/trips/)
Run this against a live server to test the standardized CRUD endpoints.
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from base_test import APITester


def test_trip_endpoints():
    """Test Trip CRUD endpoints."""
    tester = APITester()
    
    print("🧪 TESTING TRIP ENDPOINTS")
    print("=" * 80)
    
    # Test authentication
    print("Attempting authentication...")
    if not tester.authenticate("admin", "admin"):
        print("⚠️  Authentication failed, continuing without auth...")
    
    # Test 1: List trips (GET /api/trips/)
    print("\n📋 TEST 1: List Trips")
    response = tester.test_endpoint(
        "/api/trips/",
        method="GET",
        title="List Trips"
    )
    
    # Test 2: Get specific trip (if we have data)
    trip_id = None
    if response and response.status_code == 200:
        try:
            data = response.json()
            results = data.get('results', [])
            if results:
                trip_id = results[0].get('id')
                print(f"\n🔍 TEST 2: Get Specific Trip (ID: {trip_id})")
                tester.test_endpoint(
                    f"/api/trips/{trip_id}/",
                    method="GET",
                    title=f"Get Trip {trip_id}"
                )
                
                # Test trip lines for this trip
                print(f"\n🔗 TEST 2b: Get Trip Lines for Trip {trip_id}")
                tester.test_endpoint(
                    f"/api/trips/{trip_id}/trip_lines/",
                    method="GET",
                    title=f"Get Trip Lines for Trip {trip_id}"
                )
                
                # Test generate itineraries
                print(f"\n📅 TEST 2c: Generate Itineraries for Trip {trip_id}")
                tester.test_endpoint(
                    f"/api/trips/{trip_id}/generate_itineraries/",
                    method="POST",
                    title=f"Generate Itineraries for Trip {trip_id}"
                )
        except:
            print("\n⚠️  Could not extract trip ID for detail test")
    
    # Test 3: Create new trip (POST /api/trips/)
    print("\n➕ TEST 3: Create Trip (Write Serializer Test)")
    create_data = {
        "quote": 1,  # Expects Quote ID only
        "patient": 1,  # Expects Patient ID only
        "aircraft": 1,  # Expects Aircraft ID only
        "trip_number": "TR001",
        "type": "medical",
        "status": "scheduled",
        "passenger_ids": [1, 2],  # Expects list of Passenger IDs
        "departure_date": "2024-12-01T10:00:00Z",
        "arrival_date": "2024-12-01T14:00:00Z"
    }
    
    tester.test_endpoint(
        "/api/trips/",
        method="POST",
        data=create_data,
        expect_status=201,
        title="Create Trip with IDs only"
    )
    
    # Test 4: Try to create with nested objects (should fail)
    print("\n❌ TEST 4: Create Trip with Nested Objects (Should Fail)")
    invalid_data = {
        "quote": {  # Should be quote_id
            "quoted_amount": 5000.00
        },
        "patient": {  # Should be patient_id
            "status": "active"
        },
        "aircraft": {  # Should be aircraft_id
            "tail_number": "N123AB"
        },
        "passengers": [  # Should be passenger_ids
            {"info": {"first_name": "John"}}
        ],
        "trip_number": "TR002",
        "type": "charter"
    }
    
    tester.test_endpoint(
        "/api/trips/",
        method="POST",
        data=invalid_data,
        expect_status=400,
        title="Create Trip with nested objects (should fail)"
    )
    
    # Test 5: Update trip (if we have an ID)
    if trip_id:
        print(f"\n✏️  TEST 5: Update Trip (ID: {trip_id})")
        update_data = {
            "quote": 1,
            "patient": 1,
            "aircraft": 1,
            "trip_number": "TR001-UPDATED",
            "type": "charter",  # Changed type
            "status": "in_progress",  # Changed status
            "passenger_ids": [1]
        }
        
        tester.test_endpoint(
            f"/api/trips/{trip_id}/",
            method="PUT",
            data=update_data,
            expect_status=200,
            title=f"Update Trip {trip_id} with IDs only"
        )
    
    print("\n✅ Trip endpoint tests completed!")


if __name__ == "__main__":
    test_trip_endpoints()

```


# File: api/tests/test_document_generation.py

```python
#!/usr/bin/env python3
"""
Test Document Generation endpoints for Quote, Itinerary, and Handling Request PDFs
Run this against a live server to test the new document generation functionality.
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from base_test import APITester


def test_document_generation_endpoints():
    """Test Document Generation endpoints."""
    tester = APITester()
    
    print("🧪 TESTING DOCUMENT GENERATION ENDPOINTS")
    print("=" * 80)
    
    # Test authentication
    print("Attempting authentication...")
    if not tester.authenticate("admin", "admin"):
        print("⚠️  Authentication failed, continuing without auth...")
    
    # Test 1: Get available quotes for testing
    print("\n📋 TEST 1: Get Available Quotes")
    quotes_response = tester.test_endpoint(
        "/api/quotes/",
        method="GET",
        title="List Quotes"
    )
    
    quote_id = None
    if quotes_response and quotes_response.status_code == 200:
        try:
            data = quotes_response.json()
            results = data.get('results', [])
            if results:
                quote_id = results[0].get('id')
                print(f"✅ Found quote ID for testing: {quote_id}")
            else:
                print("⚠️  No quotes found for testing")
        except:
            print("⚠️  Could not parse quotes response")
    
    # Test 2: Generate Quote Document
    if quote_id:
        print(f"\n📄 TEST 2: Generate Quote Document (ID: {quote_id})")
        response = tester.test_endpoint(
            f"/api/quotes/{quote_id}/generate_quote_document/",
            method="POST",
            expect_status=201,
            title="Generate Quote Document"
        )
        
        if response and response.status_code == 201:
            try:
                result = response.json()
                if result.get('success'):
                    print(f"✅ Quote document generated: {result.get('filename')}")
                    print(f"📁 Saved to: {result.get('path')}")
                else:
                    print(f"❌ Quote generation failed: {result.get('message')}")
            except:
                print("⚠️  Could not parse quote generation response")
    
    # Test 3: Get available trips for testing
    print("\n📋 TEST 3: Get Available Trips")
    trips_response = tester.test_endpoint(
        "/api/trips/",
        method="GET",
        title="List Trips"
    )
    
    trip_id = None
    if trips_response and trips_response.status_code == 200:
        try:
            data = trips_response.json()
            results = data.get('results', [])
            if results:
                trip_id = results[0].get('id')
                print(f"✅ Found trip ID for testing: {trip_id}")
            else:
                print("⚠️  No trips found for testing")
        except:
            print("⚠️  Could not parse trips response")
    
    # Test 4: Generate Itinerary Documents
    if trip_id:
        print(f"\n📄 TEST 4: Generate Itinerary Documents (Trip ID: {trip_id})")
        response = tester.test_endpoint(
            f"/api/trips/{trip_id}/generate_itineraries/",
            method="POST",
            expect_status=201,
            title="Generate Itinerary Documents"
        )
        
        if response and response.status_code == 201:
            try:
                result = response.json()
                if result.get('success'):
                    files = result.get('files', [])
                    print(f"✅ Generated {len(files)} itinerary documents")
                    for file_info in files:
                        print(f"  📁 {file_info.get('filename')} (Crew: {file_info.get('crew_line_id')})")
                else:
                    print(f"❌ Itinerary generation failed: {result.get('message')}")
            except:
                print("⚠️  Could not parse itinerary generation response")
    
    # Test 5: Generate Handling Request Documents
    if trip_id:
        print(f"\n📄 TEST 5: Generate Handling Request Documents (Trip ID: {trip_id})")
        response = tester.test_endpoint(
            f"/api/trips/{trip_id}/generate_handling_requests/",
            method="POST",
            expect_status=201,
            title="Generate Handling Request Documents"
        )
        
        if response and response.status_code == 201:
            try:
                result = response.json()
                if result.get('success'):
                    files = result.get('files', [])
                    print(f"✅ Generated {len(files)} handling request documents")
                    for file_info in files:
                        print(f"  📁 {file_info.get('filename')}")
                        print(f"    ✈️  Arrival: {file_info.get('arrival_airport')}")
                        print(f"    🏢 FBO: {file_info.get('arrival_fbo')}")
                else:
                    print(f"❌ Handling request generation failed: {result.get('message')}")
            except:
                print("⚠️  Could not parse handling request generation response")
    
    # Test 6: Test error handling with invalid IDs
    print("\n❌ TEST 6: Test Error Handling")
    
    # Test with invalid quote ID
    invalid_id = "00000000-0000-0000-0000-000000000000"
    tester.test_endpoint(
        f"/api/quotes/{invalid_id}/generate_quote_document/",
        method="POST",
        expect_status=404,
        title="Generate Quote Document (Invalid ID)"
    )
    
    # Test with invalid trip ID
    tester.test_endpoint(
        f"/api/trips/{invalid_id}/generate_itineraries/",
        method="POST",
        expect_status=404,
        title="Generate Itineraries (Invalid ID)"
    )
    
    tester.test_endpoint(
        f"/api/trips/{invalid_id}/generate_handling_requests/",
        method="POST",
        expect_status=404,
        title="Generate Handling Requests (Invalid ID)"
    )
    
    print("\n✅ Document generation endpoint tests completed!")


if __name__ == "__main__":
    test_document_generation_endpoints()

```


# File: api/tests/test_quotes.py

```python
#!/usr/bin/env python3
"""
Test Quote endpoints (/api/quotes/)
Run this against a live server to test the standardized CRUD endpoints.
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from base_test import APITester


def test_quote_endpoints():
    """Test Quote CRUD endpoints."""
    tester = APITester()
    
    print("🧪 TESTING QUOTE ENDPOINTS")
    print("=" * 80)
    
    # Test authentication
    print("Attempting authentication...")
    if not tester.authenticate("admin", "admin"):
        print("⚠️  Authentication failed, continuing without auth...")
    
    # Test 1: List quotes (GET /api/quotes/)
    print("\n📋 TEST 1: List Quotes")
    response = tester.test_endpoint(
        "/api/quotes/",
        method="GET",
        title="List Quotes"
    )
    
    # Test 2: Get specific quote (if we have data)
    quote_id = None
    if response and response.status_code == 200:
        try:
            data = response.json()
            results = data.get('results', [])
            if results:
                quote_id = results[0].get('id')
                print(f"\n🔍 TEST 2: Get Specific Quote (ID: {quote_id})")
                tester.test_endpoint(
                    f"/api/quotes/{quote_id}/",
                    method="GET",
                    title=f"Get Quote {quote_id}"
                )
                
                # Test create transaction for this quote
                print(f"\n💳 TEST 2b: Create Transaction for Quote {quote_id}")
                transaction_data = {
                    "amount": 1000.00,
                    "payment_method": "credit_card",
                    "email": "test@example.com"
                }
                tester.test_endpoint(
                    f"/api/quotes/{quote_id}/create_transaction/",
                    method="POST",
                    data=transaction_data,
                    title=f"Create Transaction for Quote {quote_id}"
                )
        except:
            print("\n⚠️  Could not extract quote ID for detail test")
    
    # Test 3: Create new quote (POST /api/quotes/)
    print("\n➕ TEST 3: Create Quote (Write Serializer Test)")
    create_data = {
        "contact": 1,  # Expects Contact ID only
        "pickup_airport": 1,  # Expects Airport ID only
        "dropoff_airport": 2,  # Expects Airport ID only
        "patient": 1,  # Expects Patient ID only
        "payment_agreement": 1,  # Expects Agreement ID only
        "quoted_amount": 7500.00,
        "status": "pending",
        "departure_date": "2024-12-01T10:00:00Z",
        "arrival_date": "2024-12-01T14:00:00Z",
        "notes": "Test quote creation"
    }
    
    tester.test_endpoint(
        "/api/quotes/",
        method="POST",
        data=create_data,
        expect_status=201,
        title="Create Quote with IDs only"
    )
    
    # Test 4: Try to create with nested objects (should fail)
    print("\n❌ TEST 4: Create Quote with Nested Objects (Should Fail)")
    invalid_data = {
        "contact": {  # Should be contact_id
            "first_name": "John",
            "last_name": "Doe"
        },
        "pickup_airport": {  # Should be pickup_airport_id
            "icao_code": "KORD"
        },
        "dropoff_airport": {  # Should be dropoff_airport_id
            "icao_code": "KLAX"
        },
        "patient": {  # Should be patient_id
            "status": "active"
        },
        "quoted_amount": 8500.00,
        "status": "pending"
    }
    
    tester.test_endpoint(
        "/api/quotes/",
        method="POST",
        data=invalid_data,
        expect_status=400,
        title="Create Quote with nested objects (should fail)"
    )
    
    # Test 5: Update quote (if we have an ID)
    if quote_id:
        print(f"\n✏️  TEST 5: Update Quote (ID: {quote_id})")
        update_data = {
            "contact": 1,
            "pickup_airport": 1,
            "dropoff_airport": 2,
            "patient": 1,
            "payment_agreement": 1,
            "quoted_amount": 8000.00,  # Changed amount
            "status": "accepted",  # Changed status
            "notes": "Updated quote"
        }
        
        tester.test_endpoint(
            f"/api/quotes/{quote_id}/",
            method="PUT",
            data=update_data,
            expect_status=200,
            title=f"Update Quote {quote_id} with IDs only"
        )
    
    print("\n✅ Quote endpoint tests completed!")


if __name__ == "__main__":
    test_quote_endpoints()

```


# File: api/tests/test_crew_lines.py

```python
#!/usr/bin/env python3
"""
Test CrewLine endpoints (/api/crew-lines/)
Run this against a live server to test the standardized CRUD endpoints.
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from base_test import APITester


def test_crew_line_endpoints():
    """Test CrewLine CRUD endpoints."""
    tester = APITester()
    
    print("🧪 TESTING CREW LINE ENDPOINTS")
    print("=" * 80)
    
    # Test authentication
    print("Attempting authentication...")
    if not tester.authenticate("admin", "admin"):
        print("⚠️  Authentication failed, continuing without auth...")
    
    # Test 1: List crew lines (GET /api/crew-lines/)
    print("\n📋 TEST 1: List Crew Lines")
    response = tester.test_endpoint(
        "/api/crew-lines/",
        method="GET",
        title="List Crew Lines"
    )
    
    # Test 2: Get specific crew line (if we have data)
    crew_line_id = None
    if response and response.status_code == 200:
        try:
            data = response.json()
            results = data.get('results', [])
            if results:
                crew_line_id = results[0].get('id')
                print(f"\n🔍 TEST 2: Get Specific Crew Line (ID: {crew_line_id})")
                tester.test_endpoint(
                    f"/api/crew-lines/{crew_line_id}/",
                    method="GET",
                    title=f"Get Crew Line {crew_line_id}"
                )
        except:
            print("\n⚠️  Could not extract crew line ID for detail test")
    
    # Test 3: Create new crew line (POST /api/crew-lines/)
    print("\n➕ TEST 3: Create Crew Line (Write Serializer Test)")
    create_data = {
        "primary_in_command": 1,  # Expects Contact ID only
        "secondary_in_command": 2,  # Expects Contact ID only
        "medic_ids": [3, 4],  # Expects list of Contact IDs
        "status": "active",
        "notes": "Test crew line creation"
    }
    
    tester.test_endpoint(
        "/api/crew-lines/",
        method="POST",
        data=create_data,
        expect_status=201,
        title="Create Crew Line with IDs only"
    )
    
    # Test 4: Try to create with nested objects (should fail)
    print("\n❌ TEST 4: Create Crew Line with Nested Objects (Should Fail)")
    invalid_data = {
        "primary_in_command": {  # Should be primary_in_command_id
            "first_name": "John",
            "last_name": "Pilot"
        },
        "secondary_in_command": {  # Should be secondary_in_command_id
            "first_name": "Jane",
            "last_name": "Copilot"
        },
        "medics": [  # Should be medic_ids
            {"first_name": "Dr. Smith"},
            {"first_name": "Nurse Johnson"}
        ],
        "status": "active"
    }
    
    tester.test_endpoint(
        "/api/crew-lines/",
        method="POST",
        data=invalid_data,
        expect_status=400,
        title="Create Crew Line with nested objects (should fail)"
    )
    
    # Test 5: Update crew line (if we have an ID)
    if crew_line_id:
        print(f"\n✏️  TEST 5: Update Crew Line (ID: {crew_line_id})")
        update_data = {
            "primary_in_command": 2,  # Changed primary
            "secondary_in_command": 3,  # Changed secondary
            "medic_ids": [4],  # Changed medics list
            "status": "standby",  # Changed status
            "notes": "Updated crew line"
        }
        
        tester.test_endpoint(
            f"/api/crew-lines/{crew_line_id}/",
            method="PUT",
            data=update_data,
            expect_status=200,
            title=f"Update Crew Line {crew_line_id} with IDs only"
        )
    
    print("\n✅ Crew Line endpoint tests completed!")


if __name__ == "__main__":
    test_crew_line_endpoints()

```


# File: api/tests/test_trip_lines.py

```python
#!/usr/bin/env python3
"""
Test TripLine endpoints (/api/trip-lines/)
Run this against a live server to test the standardized CRUD endpoints.
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from base_test import APITester


def test_trip_line_endpoints():
    """Test TripLine CRUD endpoints."""
    tester = APITester()
    
    print("🧪 TESTING TRIP LINE ENDPOINTS")
    print("=" * 80)
    
    # Test authentication
    print("Attempting authentication...")
    if not tester.authenticate("admin", "admin"):
        print("⚠️  Authentication failed, continuing without auth...")
    
    # Test 1: List trip lines (GET /api/trip-lines/)
    print("\n📋 TEST 1: List Trip Lines")
    response = tester.test_endpoint(
        "/api/trip-lines/",
        method="GET",
        title="List Trip Lines"
    )
    
    # Test 2: Get specific trip line (if we have data)
    trip_line_id = None
    if response and response.status_code == 200:
        try:
            data = response.json()
            results = data.get('results', [])
            if results:
                trip_line_id = results[0].get('id')
                print(f"\n🔍 TEST 2: Get Specific Trip Line (ID: {trip_line_id})")
                tester.test_endpoint(
                    f"/api/trip-lines/{trip_line_id}/",
                    method="GET",
                    title=f"Get Trip Line {trip_line_id}"
                )
        except:
            print("\n⚠️  Could not extract trip line ID for detail test")
    
    # Test 3: Create new trip line (POST /api/trip-lines/)
    print("\n➕ TEST 3: Create Trip Line (Write Serializer Test)")
    create_data = {
        "trip": 1,  # Expects Trip ID only
        "origin_airport": 1,  # Expects Airport ID only
        "destination_airport": 2,  # Expects Airport ID only
        "crew_line": 1,  # Expects CrewLine ID only
        "departure_date": "2024-12-01T10:00:00Z",
        "arrival_date": "2024-12-01T14:00:00Z",
        "flight_time": "04:00:00",
        "status": "scheduled",
        "notes": "Test trip line creation"
    }
    
    tester.test_endpoint(
        "/api/trip-lines/",
        method="POST",
        data=create_data,
        expect_status=201,
        title="Create Trip Line with IDs only"
    )
    
    # Test 4: Try to create with nested objects (should fail)
    print("\n❌ TEST 4: Create Trip Line with Nested Objects (Should Fail)")
    invalid_data = {
        "trip": {  # Should be trip_id
            "trip_number": "TR001"
        },
        "origin_airport": {  # Should be origin_airport_id
            "icao_code": "KORD"
        },
        "destination_airport": {  # Should be destination_airport_id
            "icao_code": "KLAX"
        },
        "crew_line": {  # Should be crew_line_id
            "status": "active"
        },
        "departure_date": "2024-12-01T10:00:00Z",
        "arrival_date": "2024-12-01T14:00:00Z"
    }
    
    tester.test_endpoint(
        "/api/trip-lines/",
        method="POST",
        data=invalid_data,
        expect_status=400,
        title="Create Trip Line with nested objects (should fail)"
    )
    
    # Test 5: Update trip line (if we have an ID)
    if trip_line_id:
        print(f"\n✏️  TEST 5: Update Trip Line (ID: {trip_line_id})")
        update_data = {
            "trip": 1,
            "origin_airport": 2,  # Changed origin
            "destination_airport": 1,  # Changed destination (reverse)
            "crew_line": 2,  # Changed crew
            "departure_date": "2024-12-02T11:00:00Z",  # Changed time
            "arrival_date": "2024-12-02T15:00:00Z",
            "flight_time": "04:00:00",
            "status": "in_progress",  # Changed status
            "notes": "Updated trip line"
        }
        
        tester.test_endpoint(
            f"/api/trip-lines/{trip_line_id}/",
            method="PUT",
            data=update_data,
            expect_status=200,
            title=f"Update Trip Line {trip_line_id} with IDs only"
        )
    
    print("\n✅ Trip Line endpoint tests completed!")


if __name__ == "__main__":
    test_trip_line_endpoints()

```


# File: api/tests/test_userprofile.py

```python
#!/usr/bin/env python3
"""
Test UserProfile endpoints (/api/users/)
Run this against a live server to test the standardized CRUD endpoints.
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from base_test import APITester


def test_userprofile_endpoints():
    """Test UserProfile CRUD endpoints."""
    tester = APITester()
    
    print("🧪 TESTING USERPROFILE ENDPOINTS")
    print("=" * 80)
    
    # Test authentication first (you may need to adjust credentials)
    print("Attempting authentication...")
    if not tester.authenticate("admin", "admin"):  # Adjust credentials as needed
        print("⚠️  Authentication failed, continuing without auth...")
    
    # Test 1: List users (GET /api/users/)
    print("\n📋 TEST 1: List Users")
    response = tester.test_endpoint(
        "/api/users/",
        method="GET",
        title="List UserProfiles"
    )
    
    # Test 2: Get current user (GET /api/users/me/)
    print("\n👤 TEST 2: Get Current User")
    response = tester.test_endpoint(
        "/api/users/me/",
        method="GET",
        title="Get Current User Profile"
    )
    
    # Test 3: Try to get a specific user (if we have an ID from list)
    if response and response.status_code == 200:
        try:
            user_data = response.json()
            user_id = user_data.get('id')
            if user_id:
                print(f"\n🔍 TEST 3: Get Specific User (ID: {user_id})")
                tester.test_endpoint(
                    f"/api/users/{user_id}/",
                    method="GET",
                    title=f"Get UserProfile {user_id}"
                )
        except:
            print("\n⚠️  Could not extract user ID for detail test")
    
    # Test 4: Create new user (POST /api/users/)
    print("\n➕ TEST 4: Create User (Write Serializer Test)")
    create_data = {
        "user_id": 1,  # This will likely fail, but shows the expected format
        "first_name": "Test",
        "last_name": "User",
        "email": "test@example.com",
        "phone": "+1234567890",
        "role_ids": [1],  # Expects only IDs
        "department_ids": [1],  # Expects only IDs
        "status": "active"
    }
    
    tester.test_endpoint(
        "/api/users/",
        method="POST",
        data=create_data,
        expect_status=201,  # May fail due to constraints, but tests serializer
        title="Create UserProfile with IDs only"
    )
    
    # Test 5: Try to create with nested objects (should fail)
    print("\n❌ TEST 5: Create User with Nested Objects (Should Fail)")
    invalid_data = {
        "user": {"username": "invalid"},  # Should be user_id
        "roles": [{"name": "invalid"}],   # Should be role_ids
        "first_name": "Invalid",
        "last_name": "User"
    }
    
    tester.test_endpoint(
        "/api/users/",
        method="POST",
        data=invalid_data,
        expect_status=400,
        title="Create UserProfile with nested objects (should fail)"
    )
    
    print("\n✅ UserProfile endpoint tests completed!")


if __name__ == "__main__":
    test_userprofile_endpoints()

```


# File: api/migrations/0016_add_contract_model.py

```python
# Generated by Django 5.1.11 on 2025-09-08 20:18

import django.db.models.deletion
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0015_document_contact_document_created_by_and_more"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Contract",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("created_on", models.DateTimeField(auto_now_add=True)),
                ("modified_on", models.DateTimeField(auto_now=True)),
                ("lock", models.BooleanField(default=False)),
                ("title", models.CharField(max_length=255)),
                (
                    "contract_type",
                    models.CharField(
                        choices=[
                            ("payment_agreement", "Payment Agreement"),
                            ("consent_transport", "Consent for Transport"),
                            ("patient_service_agreement", "Patient Service Agreement"),
                            ("medical_necessity", "Medical Necessity Agreement"),
                            ("liability_waiver", "Liability Waiver"),
                            ("hipaa_authorization", "HIPAA Authorization"),
                            ("other", "Other Contract Type"),
                        ],
                        max_length=30,
                    ),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("draft", "Draft"),
                            ("pending", "Pending Signature"),
                            ("signed", "Signed"),
                            ("completed", "Completed"),
                            ("expired", "Expired"),
                            ("cancelled", "Cancelled"),
                            ("failed", "Failed"),
                        ],
                        default="draft",
                        max_length=20,
                    ),
                ),
                (
                    "docuseal_template_id",
                    models.CharField(blank=True, max_length=100, null=True),
                ),
                (
                    "docuseal_submission_id",
                    models.CharField(blank=True, max_length=100, null=True),
                ),
                (
                    "docuseal_webhook_id",
                    models.CharField(blank=True, max_length=100, null=True),
                ),
                ("signer_email", models.EmailField(max_length=254)),
                (
                    "signer_name",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                ("date_sent", models.DateTimeField(blank=True, null=True)),
                ("date_signed", models.DateTimeField(blank=True, null=True)),
                ("date_expired", models.DateTimeField(blank=True, null=True)),
                ("notes", models.TextField(blank=True, null=True)),
                ("docuseal_response_data", models.JSONField(blank=True, default=dict)),
                (
                    "created_by",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="%(class)s_created",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "customer_contact",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="customer_contracts",
                        to="api.contact",
                    ),
                ),
                (
                    "modified_by",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="%(class)s_modified",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "patient",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="patient_contracts",
                        to="api.patient",
                    ),
                ),
                (
                    "signed_document",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="signed_contracts",
                        to="api.document",
                    ),
                ),
                (
                    "trip",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="contracts",
                        to="api.trip",
                    ),
                ),
                (
                    "unsigned_document",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="unsigned_contracts",
                        to="api.document",
                    ),
                ),
            ],
            options={
                "indexes": [
                    models.Index(
                        fields=["trip", "contract_type"],
                        name="api_contrac_trip_id_f14c4b_idx",
                    ),
                    models.Index(
                        fields=["status"], name="api_contrac_status_b0d65d_idx"
                    ),
                    models.Index(
                        fields=["docuseal_submission_id"],
                        name="api_contrac_docusea_d20cde_idx",
                    ),
                ],
            },
        ),
    ]

```


# File: api/migrations/0009_fbo_email.py

```python
# Generated by Django 5.1.11 on 2025-08-26 03:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0008_fbo_phone_fbo_phone_secondary"),
    ]

    operations = [
        migrations.AddField(
            model_name="fbo",
            name="email",
            field=models.EmailField(blank=True, max_length=254, null=True),
        ),
    ]

```


# File: api/migrations/0007_contact_date_of_birth_contact_nationality_and_more.py

```python
# Generated by Django 5.1.11 on 2025-08-24 04:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0006_alter_airport_iata_code_alter_airport_icao_code"),
    ]

    operations = [
        migrations.AddField(
            model_name="contact",
            name="date_of_birth",
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="contact",
            name="nationality",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name="contact",
            name="passport_expiration_date",
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="contact",
            name="passport_number",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]

```


# File: api/migrations/0001_initial.py

```python
# Generated by Django 5.1.11 on 2025-08-22 04:07

import django.db.models.deletion
import django.utils.timezone
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("contenttypes", "0002_remove_content_type_name"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Document",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("filename", models.CharField(max_length=255)),
                ("content", models.BinaryField()),
                ("flag", models.IntegerField(default=0)),
                ("created_on", models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name="Aircraft",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("created_on", models.DateTimeField(auto_now_add=True)),
                ("modified_on", models.DateTimeField(auto_now=True)),
                (
                    "status",
                    models.CharField(db_index=True, default="active", max_length=50),
                ),
                ("lock", models.BooleanField(default=False)),
                (
                    "tail_number",
                    models.CharField(db_index=True, max_length=20, unique=True),
                ),
                ("company", models.CharField(max_length=255)),
                (
                    "mgtow",
                    models.DecimalField(
                        decimal_places=2,
                        max_digits=10,
                        verbose_name="Maximum Gross Takeoff Weight",
                    ),
                ),
                ("make", models.CharField(max_length=100)),
                ("model", models.CharField(max_length=100)),
                ("serial_number", models.CharField(max_length=100)),
                (
                    "created_by",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="%(class)s_created",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "modified_by",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="%(class)s_modified",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="Contact",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("created_on", models.DateTimeField(auto_now_add=True)),
                ("modified_on", models.DateTimeField(auto_now=True)),
                (
                    "status",
                    models.CharField(db_index=True, default="active", max_length=50),
                ),
                ("lock", models.BooleanField(default=False)),
                ("first_name", models.CharField(blank=True, max_length=100, null=True)),
                ("last_name", models.CharField(blank=True, max_length=100, null=True)),
                (
                    "business_name",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                ("email", models.EmailField(blank=True, max_length=254, null=True)),
                ("phone", models.CharField(blank=True, max_length=20, null=True)),
                (
                    "address_line1",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                (
                    "address_line2",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                ("city", models.CharField(blank=True, max_length=100, null=True)),
                ("state", models.CharField(blank=True, max_length=100, null=True)),
                ("zip", models.CharField(blank=True, max_length=20, null=True)),
                ("country", models.CharField(blank=True, max_length=100, null=True)),
                (
                    "created_by",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="%(class)s_created",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "modified_by",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="%(class)s_modified",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="CrewLine",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("created_on", models.DateTimeField(auto_now_add=True)),
                ("modified_on", models.DateTimeField(auto_now=True)),
                (
                    "status",
                    models.CharField(db_index=True, default="active", max_length=50),
                ),
                ("lock", models.BooleanField(default=False)),
                (
                    "created_by",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="%(class)s_created",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "medic_ids",
                    models.ManyToManyField(
                        related_name="medic_crew_lines", to="api.contact"
                    ),
                ),
                (
                    "modified_by",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="%(class)s_modified",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "primary_in_command",
                    models.ForeignKey(
                        db_column="primary_in_command_id",
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="primary_crew_lines",
                        to="api.contact",
                    ),
                ),
                (
                    "secondary_in_command",
                    models.ForeignKey(
                        db_column="secondary_in_command_id",
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="secondary_crew_lines",
                        to="api.contact",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="Agreement",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("created_on", models.DateTimeField(auto_now_add=True)),
                ("modified_on", models.DateTimeField(auto_now=True)),
                ("lock", models.BooleanField(default=False)),
                ("destination_email", models.EmailField(max_length=254)),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("created", "Created"),
                            ("pending", "Pending"),
                            ("modified", "Modified"),
                            ("signed", "Signed"),
                            ("denied", "Denied"),
                        ],
                        default="created",
                        max_length=20,
                    ),
                ),
                (
                    "created_by",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="%(class)s_created",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "modified_by",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="%(class)s_modified",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "document_signed",
                    models.ForeignKey(
                        blank=True,
                        db_column="document_signed_id",
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="signed_agreements",
                        to="api.document",
                    ),
                ),
                (
                    "document_unsigned",
                    models.ForeignKey(
                        blank=True,
                        db_column="document_unsigned_id",
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="unsigned_agreements",
                        to="api.document",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="FBO",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("created_on", models.DateTimeField(auto_now_add=True)),
                ("modified_on", models.DateTimeField(auto_now=True)),
                (
                    "status",
                    models.CharField(db_index=True, default="active", max_length=50),
                ),
                ("lock", models.BooleanField(default=False)),
                ("name", models.CharField(max_length=255)),
                (
                    "address_line1",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                (
                    "address_line2",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                ("city", models.CharField(blank=True, max_length=100, null=True)),
                ("state", models.CharField(blank=True, max_length=100, null=True)),
                ("zip", models.CharField(blank=True, max_length=20, null=True)),
                ("country", models.CharField(blank=True, max_length=100, null=True)),
                ("notes", models.TextField(blank=True, null=True)),
                (
                    "contacts",
                    models.ManyToManyField(related_name="fbos", to="api.contact"),
                ),
                (
                    "created_by",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="%(class)s_created",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "modified_by",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="%(class)s_modified",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="Ground",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("created_on", models.DateTimeField(auto_now_add=True)),
                ("modified_on", models.DateTimeField(auto_now=True)),
                (
                    "status",
                    models.CharField(db_index=True, default="active", max_length=50),
                ),
                ("lock", models.BooleanField(default=False)),
                ("name", models.CharField(max_length=255)),
                (
                    "address_line1",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                (
                    "address_line2",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                ("city", models.CharField(blank=True, max_length=100, null=True)),
                ("state", models.CharField(blank=True, max_length=100, null=True)),
                ("zip", models.CharField(blank=True, max_length=20, null=True)),
                ("country", models.CharField(blank=True, max_length=100, null=True)),
                ("notes", models.TextField(blank=True, null=True)),
                (
                    "contacts",
                    models.ManyToManyField(related_name="grounds", to="api.contact"),
                ),
                (
                    "created_by",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="%(class)s_created",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "modified_by",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="%(class)s_modified",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="Airport",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("created_on", models.DateTimeField(auto_now_add=True)),
                ("modified_on", models.DateTimeField(auto_now=True)),
                (
                    "status",
                    models.CharField(db_index=True, default="active", max_length=50),
                ),
                ("lock", models.BooleanField(default=False)),
                (
                    "icao_code",
                    models.CharField(db_index=True, max_length=4, unique=True),
                ),
                ("iata_code", models.CharField(db_index=True, max_length=3)),
                ("name", models.CharField(max_length=255)),
                ("city", models.CharField(max_length=100)),
                ("state", models.CharField(blank=True, max_length=100, null=True)),
                ("country", models.CharField(max_length=100)),
                ("elevation", models.IntegerField(blank=True, null=True)),
                ("latitude", models.DecimalField(decimal_places=6, max_digits=9)),
                ("longitude", models.DecimalField(decimal_places=6, max_digits=9)),
                ("timezone", models.CharField(max_length=50)),
                (
                    "created_by",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="%(class)s_created",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "modified_by",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="%(class)s_modified",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "fbos",
                    models.ManyToManyField(
                        blank=True, related_name="airports", to="api.fbo"
                    ),
                ),
                (
                    "grounds",
                    models.ManyToManyField(
                        blank=True, related_name="airports", to="api.ground"
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="Modification",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("model", models.CharField(max_length=100)),
                ("object_id", models.UUIDField()),
                ("field", models.CharField(max_length=100)),
                ("before", models.TextField(blank=True, null=True)),
                ("after", models.TextField(blank=True, null=True)),
                ("time", models.DateTimeField(auto_now_add=True)),
                (
                    "content_type",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="contenttypes.contenttype",
                    ),
                ),
            ],
            options={
                "ordering": ["-time"],
            },
        ),
        migrations.CreateModel(
            name="Passenger",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("created_on", models.DateTimeField(auto_now_add=True)),
                ("modified_on", models.DateTimeField(auto_now=True)),
                (
                    "status",
                    models.CharField(db_index=True, default="active", max_length=50),
                ),
                ("lock", models.BooleanField(default=False)),
                ("date_of_birth", models.DateField(blank=True, null=True)),
                (
                    "nationality",
                    models.CharField(blank=True, max_length=100, null=True),
                ),
                (
                    "passport_number",
                    models.CharField(blank=True, max_length=100, null=True),
                ),
                ("passport_expiration_date", models.DateField(blank=True, null=True)),
                (
                    "contact_number",
                    models.CharField(blank=True, max_length=20, null=True),
                ),
                ("notes", models.TextField(blank=True, null=True)),
                (
                    "created_by",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="%(class)s_created",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "info",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="passengers",
                        to="api.contact",
                    ),
                ),
                (
                    "modified_by",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="%(class)s_modified",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "passenger_ids",
                    models.ManyToManyField(
                        blank=True,
                        related_name="related_passengers",
                        to="api.passenger",
                    ),
                ),
                (
                    "passport_document",
                    models.ForeignKey(
                        blank=True,
                        db_column="passport_document_id",
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="passport_passengers",
                        to="api.document",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="Patient",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("created_on", models.DateTimeField(auto_now_add=True)),
                ("modified_on", models.DateTimeField(auto_now=True)),
                ("lock", models.BooleanField(default=False)),
                ("bed_at_origin", models.BooleanField(default=False)),
                ("bed_at_destination", models.BooleanField(default=False)),
                ("date_of_birth", models.DateField()),
                ("nationality", models.CharField(max_length=100)),
                ("passport_number", models.CharField(max_length=100)),
                ("passport_expiration_date", models.DateField()),
                ("special_instructions", models.TextField(blank=True, null=True)),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("pending", "Pending"),
                            ("confirmed", "Confirmed"),
                            ("active", "Active"),
                            ("completed", "Completed"),
                            ("cancelled", "Cancelled"),
                        ],
                        db_index=True,
                        default="pending",
                        max_length=20,
                    ),
                ),
                (
                    "created_by",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="%(class)s_created",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "info",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="patients",
                        to="api.contact",
                    ),
                ),
                (
                    "letter_of_medical_necessity",
                    models.ForeignKey(
                        blank=True,
                        db_column="letter_of_medical_necessity_id",
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="medical_necessity_patients",
                        to="api.document",
                    ),
                ),
                (
                    "modified_by",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="%(class)s_modified",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "passport_document",
                    models.ForeignKey(
                        blank=True,
                        db_column="passport_document_id",
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="passport_patients",
                        to="api.document",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="Permission",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("created_on", models.DateTimeField(auto_now_add=True)),
                ("modified_on", models.DateTimeField(auto_now=True)),
                (
                    "status",
                    models.CharField(db_index=True, default="active", max_length=50),
                ),
                ("lock", models.BooleanField(default=False)),
                ("name", models.CharField(max_length=100, unique=True)),
                ("description", models.TextField(blank=True, null=True)),
                (
                    "created_by",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="%(class)s_created",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "modified_by",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="%(class)s_modified",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="Department",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("created_on", models.DateTimeField(auto_now_add=True)),
                ("modified_on", models.DateTimeField(auto_now=True)),
                (
                    "status",
                    models.CharField(db_index=True, default="active", max_length=50),
                ),
                ("lock", models.BooleanField(default=False)),
                ("name", models.CharField(max_length=100)),
                ("description", models.TextField(blank=True, null=True)),
                (
                    "created_by",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="%(class)s_created",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "modified_by",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="%(class)s_modified",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "permission_ids",
                    models.ManyToManyField(
                        related_name="departments", to="api.permission"
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="Role",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("created_on", models.DateTimeField(auto_now_add=True)),
                ("modified_on", models.DateTimeField(auto_now=True)),
                (
                    "status",
                    models.CharField(db_index=True, default="active", max_length=50),
                ),
                ("lock", models.BooleanField(default=False)),
                ("name", models.CharField(max_length=100, unique=True)),
                ("description", models.TextField(blank=True, null=True)),
                (
                    "created_by",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="%(class)s_created",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "modified_by",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="%(class)s_modified",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "permissions",
                    models.ManyToManyField(related_name="roles", to="api.permission"),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="Transaction",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("created_on", models.DateTimeField(auto_now_add=True)),
                ("modified_on", models.DateTimeField(auto_now=True)),
                (
                    "status",
                    models.CharField(db_index=True, default="active", max_length=50),
                ),
                ("lock", models.BooleanField(default=False)),
                (
                    "key",
                    models.UUIDField(
                        db_index=True, default=uuid.uuid4, editable=False, unique=True
                    ),
                ),
                ("amount", models.DecimalField(decimal_places=2, max_digits=10)),
                (
                    "payment_method",
                    models.CharField(
                        choices=[
                            ("credit_card", "Credit Card"),
                            ("ACH", "ACH Transfer"),
                        ],
                        max_length=20,
                    ),
                ),
                (
                    "payment_status",
                    models.CharField(
                        choices=[
                            ("created", "Created"),
                            ("pending", "Pending"),
                            ("completed", "Completed"),
                            ("failed", "Failed"),
                        ],
                        default="created",
                        max_length=20,
                    ),
                ),
                (
                    "payment_date",
                    models.DateTimeField(default=django.utils.timezone.now),
                ),
                ("email", models.EmailField(max_length=254)),
                (
                    "created_by",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="%(class)s_created",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "modified_by",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="%(class)s_modified",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="Quote",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("created_on", models.DateTimeField(auto_now_add=True)),
                ("modified_on", models.DateTimeField(auto_now=True)),
                ("lock", models.BooleanField(default=False)),
                ("quoted_amount", models.DecimalField(decimal_places=2, max_digits=10)),
                (
                    "cruise_doctor_first_name",
                    models.CharField(blank=True, max_length=100, null=True),
                ),
                (
                    "cruise_doctor_last_name",
                    models.CharField(blank=True, max_length=100, null=True),
                ),
                (
                    "cruise_line",
                    models.CharField(blank=True, max_length=100, null=True),
                ),
                (
                    "cruise_ship",
                    models.CharField(blank=True, max_length=100, null=True),
                ),
                (
                    "aircraft_type",
                    models.CharField(
                        choices=[
                            ("65", "Learjet 65"),
                            ("35", "Learjet 35"),
                            ("TBD", "To Be Determined"),
                        ],
                        max_length=20,
                    ),
                ),
                ("estimated_flight_time", models.DurationField()),
                ("includes_grounds", models.BooleanField(default=False)),
                (
                    "inquiry_date",
                    models.DateTimeField(default=django.utils.timezone.now),
                ),
                (
                    "medical_team",
                    models.CharField(
                        choices=[
                            ("RN/RN", "RN/RN"),
                            ("RN/Paramedic", "RN/Paramedic"),
                            ("RN/MD", "RN/MD"),
                            ("RN/RT", "RN/RT"),
                            ("standard", "Standard"),
                            ("full", "Full"),
                        ],
                        max_length=20,
                    ),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("pending", "Pending"),
                            ("confirmed", "Confirmed"),
                            ("active", "Active"),
                            ("completed", "Completed"),
                            ("cancelled", "Cancelled"),
                            ("paid", "Paid"),
                        ],
                        db_index=True,
                        default="pending",
                        max_length=20,
                    ),
                ),
                ("number_of_stops", models.PositiveIntegerField(default=0)),
                (
                    "quote_pdf_status",
                    models.CharField(
                        choices=[
                            ("created", "Created"),
                            ("pending", "Pending"),
                            ("modified", "Modified"),
                            ("accepted", "Accepted"),
                            ("denied", "Denied"),
                        ],
                        default="created",
                        max_length=20,
                    ),
                ),
                ("quote_pdf_email", models.EmailField(max_length=254)),
                (
                    "consent_for_transport",
                    models.ForeignKey(
                        blank=True,
                        db_column="consent_for_transport_id",
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="consent_quotes",
                        to="api.agreement",
                    ),
                ),
                (
                    "contact",
                    models.ForeignKey(
                        db_column="contact_id",
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="quotes",
                        to="api.contact",
                    ),
                ),
                (
                    "created_by",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="%(class)s_created",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "documents",
                    models.ManyToManyField(related_name="quotes", to="api.document"),
                ),
                (
                    "dropoff_airport",
                    models.ForeignKey(
                        db_column="dropoff_airport_id",
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="dropoff_quotes",
                        to="api.airport",
                    ),
                ),
                (
                    "modified_by",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="%(class)s_modified",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "patient",
                    models.ForeignKey(
                        blank=True,
                        db_column="patient_id",
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="quotes",
                        to="api.patient",
                    ),
                ),
                (
                    "patient_service_agreement",
                    models.ForeignKey(
                        blank=True,
                        db_column="patient_service_agreement_id",
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="service_quotes",
                        to="api.agreement",
                    ),
                ),
                (
                    "payment_agreement",
                    models.ForeignKey(
                        blank=True,
                        db_column="payment_agreement_id",
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="payment_quotes",
                        to="api.agreement",
                    ),
                ),
                (
                    "pickup_airport",
                    models.ForeignKey(
                        db_column="pickup_airport_id",
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="pickup_quotes",
                        to="api.airport",
                    ),
                ),
                (
                    "quote_pdf",
                    models.ForeignKey(
                        blank=True,
                        db_column="quote_pdf_id",
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="quote_pdfs",
                        to="api.document",
                    ),
                ),
                (
                    "transactions",
                    models.ManyToManyField(
                        blank=True, related_name="quotes", to="api.transaction"
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="Trip",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("created_on", models.DateTimeField(auto_now_add=True)),
                ("modified_on", models.DateTimeField(auto_now=True)),
                (
                    "status",
                    models.CharField(db_index=True, default="active", max_length=50),
                ),
                ("lock", models.BooleanField(default=False)),
                ("email_chain", models.JSONField(blank=True, default=list)),
                (
                    "type",
                    models.CharField(
                        choices=[
                            ("medical", "Medical"),
                            ("charter", "Charter"),
                            ("part 91", "Part 91"),
                            ("other", "Other"),
                            ("maintenance", "Maintenance"),
                        ],
                        max_length=20,
                    ),
                ),
                (
                    "estimated_departure_time",
                    models.DateTimeField(blank=True, null=True),
                ),
                ("post_flight_duty_time", models.DurationField(blank=True, null=True)),
                ("pre_flight_duty_time", models.DurationField(blank=True, null=True)),
                (
                    "trip_number",
                    models.CharField(db_index=True, max_length=20, unique=True),
                ),
                (
                    "aircraft",
                    models.ForeignKey(
                        blank=True,
                        db_column="aircraft_id",
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="trips",
                        to="api.aircraft",
                    ),
                ),
                (
                    "created_by",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="%(class)s_created",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "customer_itinerary",
                    models.ForeignKey(
                        blank=True,
                        db_column="customer_itinerary_id",
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="customer_itinerary_trips",
                        to="api.document",
                    ),
                ),
                (
                    "internal_itinerary",
                    models.ForeignKey(
                        blank=True,
                        db_column="internal_itinerary_id",
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="internal_itinerary_trips",
                        to="api.document",
                    ),
                ),
                (
                    "modified_by",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="%(class)s_modified",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "passengers",
                    models.ManyToManyField(
                        blank=True, related_name="trips", to="api.passenger"
                    ),
                ),
                (
                    "patient",
                    models.ForeignKey(
                        blank=True,
                        db_column="patient_id",
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="trips",
                        to="api.patient",
                    ),
                ),
                (
                    "quote",
                    models.ForeignKey(
                        blank=True,
                        db_column="quote_id",
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="trips",
                        to="api.quote",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="TripLine",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("created_on", models.DateTimeField(auto_now_add=True)),
                ("modified_on", models.DateTimeField(auto_now=True)),
                (
                    "status",
                    models.CharField(db_index=True, default="active", max_length=50),
                ),
                ("lock", models.BooleanField(default=False)),
                ("departure_time_local", models.DateTimeField()),
                ("departure_time_utc", models.DateTimeField()),
                ("arrival_time_local", models.DateTimeField()),
                ("arrival_time_utc", models.DateTimeField()),
                ("distance", models.DecimalField(decimal_places=2, max_digits=10)),
                ("flight_time", models.DurationField()),
                ("ground_time", models.DurationField()),
                ("passenger_leg", models.BooleanField(default=True)),
                (
                    "created_by",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="%(class)s_created",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "crew_line",
                    models.ForeignKey(
                        blank=True,
                        db_column="crew_line_id",
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="trip_lines",
                        to="api.crewline",
                    ),
                ),
                (
                    "destination_airport",
                    models.ForeignKey(
                        db_column="destination_airport_id",
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="destination_trip_lines",
                        to="api.airport",
                    ),
                ),
                (
                    "modified_by",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="%(class)s_modified",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "origin_airport",
                    models.ForeignKey(
                        db_column="origin_airport_id",
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="origin_trip_lines",
                        to="api.airport",
                    ),
                ),
                (
                    "trip",
                    models.ForeignKey(
                        db_column="trip_id",
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="trip_lines",
                        to="api.trip",
                    ),
                ),
            ],
            options={
                "ordering": ["departure_time_utc"],
            },
        ),
        migrations.CreateModel(
            name="UserProfile",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("created_on", models.DateTimeField(auto_now_add=True)),
                ("modified_on", models.DateTimeField(auto_now=True)),
                (
                    "status",
                    models.CharField(db_index=True, default="active", max_length=50),
                ),
                ("lock", models.BooleanField(default=False)),
                ("first_name", models.CharField(max_length=100)),
                ("last_name", models.CharField(max_length=100)),
                ("email", models.EmailField(blank=True, max_length=254, null=True)),
                ("phone", models.CharField(blank=True, max_length=20, null=True)),
                (
                    "address_line1",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                (
                    "address_line2",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                ("city", models.CharField(blank=True, max_length=100, null=True)),
                ("state", models.CharField(blank=True, max_length=100, null=True)),
                ("country", models.CharField(blank=True, max_length=100, null=True)),
                ("zip", models.CharField(blank=True, max_length=20, null=True)),
                ("flags", models.JSONField(blank=True, default=list)),
                (
                    "created_by",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="%(class)s_created",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "department_ids",
                    models.ManyToManyField(related_name="users", to="api.department"),
                ),
                (
                    "departments",
                    models.ManyToManyField(
                        related_name="department_users", to="api.department"
                    ),
                ),
                (
                    "modified_by",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="%(class)s_modified",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                ("roles", models.ManyToManyField(related_name="users", to="api.role")),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="profile",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
    ]

```


# File: api/migrations/__init__.py

```python

```


# File: api/migrations/0010_tripevent.py

```python
# Generated by Django 5.1.11 on 2025-08-26 04:02

import django.db.models.deletion
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0009_fbo_email"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="TripEvent",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("created_on", models.DateTimeField(auto_now_add=True)),
                ("modified_on", models.DateTimeField(auto_now=True)),
                (
                    "status",
                    models.CharField(db_index=True, default="active", max_length=50),
                ),
                ("lock", models.BooleanField(default=False)),
                (
                    "event_type",
                    models.CharField(
                        choices=[
                            ("CREW_CHANGE", "Crew Change"),
                            ("OVERNIGHT", "Overnight (New Day)"),
                        ],
                        max_length=20,
                    ),
                ),
                ("start_time_local", models.DateTimeField()),
                ("start_time_utc", models.DateTimeField()),
                ("end_time_local", models.DateTimeField(blank=True, null=True)),
                ("end_time_utc", models.DateTimeField(blank=True, null=True)),
                ("notes", models.TextField(blank=True, null=True)),
                (
                    "airport_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="trip_events",
                        to="api.airport",
                    ),
                ),
                (
                    "created_by",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="%(class)s_created",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "crew_line_id",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="trip_events",
                        to="api.crewline",
                    ),
                ),
                (
                    "modified_by",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="%(class)s_modified",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "trip_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="events",
                        to="api.trip",
                    ),
                ),
            ],
            options={
                "indexes": [
                    models.Index(
                        fields=["trip_id", "start_time_utc"],
                        name="api_tripeve_trip_id_aaf262_idx",
                    ),
                    models.Index(
                        fields=["event_type"], name="api_tripeve_event_t_85f611_idx"
                    ),
                ],
            },
        ),
    ]

```


# File: api/migrations/0017_add_authorize_net_trans_id_to_transaction.py

```python
# Generated by Django 5.1.11 on 2025-09-09 02:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0016_add_contract_model"),
    ]

    operations = [
        migrations.AddField(
            model_name="transaction",
            name="authorize_net_trans_id",
            field=models.CharField(
                blank=True,
                help_text="Authorize.Net Transaction ID",
                max_length=50,
                null=True,
            ),
        ),
        migrations.AlterField(
            model_name="contract",
            name="contract_type",
            field=models.CharField(
                choices=[
                    ("consent_transport", "Consent for Transport"),
                    ("payment_agreement", "Air Ambulance Payment Agreement"),
                    ("patient_service_agreement", "Patient Service Agreement"),
                ],
                max_length=30,
            ),
        ),
    ]

```


# File: api/migrations/0003_staff_staffrole_staffrolemembership_and_more.py

```python
# Generated by Django 5.1.11 on 2025-08-23 05:26

import django.db.models.deletion
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0002_trip_notes"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Staff",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("created_on", models.DateTimeField(auto_now_add=True)),
                ("modified_on", models.DateTimeField(auto_now=True)),
                (
                    "status",
                    models.CharField(db_index=True, default="active", max_length=50),
                ),
                ("lock", models.BooleanField(default=False)),
                ("active", models.BooleanField(default=True)),
                ("notes", models.TextField(blank=True)),
                (
                    "contact",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="staff",
                        to="api.contact",
                    ),
                ),
                (
                    "created_by",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="%(class)s_created",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "modified_by",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="%(class)s_modified",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="StaffRole",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("created_on", models.DateTimeField(auto_now_add=True)),
                ("modified_on", models.DateTimeField(auto_now=True)),
                (
                    "status",
                    models.CharField(db_index=True, default="active", max_length=50),
                ),
                ("lock", models.BooleanField(default=False)),
                ("code", models.CharField(max_length=32, unique=True)),
                ("name", models.CharField(max_length=64)),
                (
                    "created_by",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="%(class)s_created",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "modified_by",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="%(class)s_modified",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="StaffRoleMembership",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("created_on", models.DateTimeField(auto_now_add=True)),
                ("modified_on", models.DateTimeField(auto_now=True)),
                (
                    "status",
                    models.CharField(db_index=True, default="active", max_length=50),
                ),
                ("lock", models.BooleanField(default=False)),
                ("start_on", models.DateField(blank=True, null=True)),
                ("end_on", models.DateField(blank=True, null=True)),
                (
                    "created_by",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="%(class)s_created",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "modified_by",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="%(class)s_modified",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "role",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="memberships",
                        to="api.staffrole",
                    ),
                ),
                (
                    "staff",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="role_memberships",
                        to="api.staff",
                    ),
                ),
            ],
        ),
        migrations.AddIndex(
            model_name="staffrole",
            index=models.Index(fields=["code"], name="api_staffro_code_20dc3e_idx"),
        ),
        migrations.AddConstraint(
            model_name="staffrolemembership",
            constraint=models.UniqueConstraint(
                fields=("staff", "role", "start_on", "end_on"),
                name="uniq_staff_role_interval",
            ),
        ),
    ]

```


# File: api/migrations/0013_comment_and_more.py

```python
# Generated by Django 5.1.11 on 2025-08-28 17:11

import django.db.models.deletion
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0012_tripline_arrival_fbo_tripline_departure_fbo"),
        ("contenttypes", "0002_remove_content_type_name"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Comment",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("created_on", models.DateTimeField(auto_now_add=True)),
                ("modified_on", models.DateTimeField(auto_now=True)),
                (
                    "status",
                    models.CharField(db_index=True, default="active", max_length=50),
                ),
                ("lock", models.BooleanField(default=False)),
                ("object_id", models.UUIDField()),
                ("text", models.TextField()),
            ],
        ),
        migrations.RemoveIndex(
            model_name="tripevent",
            name="api_tripeve_trip_id_708e55_idx",
        ),
        migrations.AddField(
            model_name="modification",
            name="user",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="modifications",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AddIndex(
            model_name="tripevent",
            index=models.Index(
                fields=["trip", "start_time_utc"], name="api_tripeve_trip_id_708e55_idx"
            ),
        ),
        migrations.AddField(
            model_name="comment",
            name="content_type",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="contenttypes.contenttype",
            ),
        ),
        migrations.AddField(
            model_name="comment",
            name="created_by",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="%(class)s_created",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AddField(
            model_name="comment",
            name="modified_by",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="%(class)s_modified",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AddIndex(
            model_name="comment",
            index=models.Index(
                fields=["content_type", "object_id"],
                name="api_comment_content_e00820_idx",
            ),
        ),
    ]

```


# File: api/migrations/0006_alter_airport_iata_code_alter_airport_icao_code.py

```python
# Generated by Django 5.1.11 on 2025-08-24 02:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0005_airport_airport_type"),
    ]

    operations = [
        migrations.AlterField(
            model_name="airport",
            name="iata_code",
            field=models.CharField(blank=True, db_index=True, max_length=3, null=True),
        ),
        migrations.AlterField(
            model_name="airport",
            name="icao_code",
            field=models.CharField(
                blank=True, db_index=True, max_length=4, null=True, unique=True
            ),
        ),
    ]

```


# File: api/migrations/0002_trip_notes.py

```python
# Generated by Django 5.1.11 on 2025-08-22 04:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="trip",
            name="notes",
            field=models.TextField(blank=True, null=True),
        ),
    ]

```


# File: api/migrations/0004_rename_country_airport_iso_country_and_more.py

```python
# Generated by Django 5.1.11 on 2025-08-24 02:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0003_staff_staffrole_staffrolemembership_and_more"),
    ]

    operations = [
        migrations.RenameField(
            model_name="airport",
            old_name="country",
            new_name="iso_country",
        ),
        migrations.RenameField(
            model_name="airport",
            old_name="state",
            new_name="iso_region",
        ),
        migrations.RemoveField(
            model_name="airport",
            name="city",
        ),
        migrations.AddField(
            model_name="airport",
            name="gps_code",
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AddField(
            model_name="airport",
            name="ident",
            field=models.CharField(
                db_index=True, default="UTC", max_length=10, unique=True
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="airport",
            name="local_code",
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AddField(
            model_name="airport",
            name="municipality",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]

```


# File: api/migrations/0012_tripline_arrival_fbo_tripline_departure_fbo.py

```python
# Generated manually

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0011_rename_airport_id_tripevent_airport_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='tripline',
            name='departure_fbo',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='departure_trip_lines', to='api.fbo'),
        ),
        migrations.AddField(
            model_name='tripline',
            name='arrival_fbo',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='arrival_trip_lines', to='api.fbo'),
        ),
    ]
```


# File: api/migrations/0015_document_contact_document_created_by_and_more.py

```python
# Generated by Django 5.1.11 on 2025-08-30 16:02

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0014_quote_payment_status_alter_quote_status"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name="document",
            name="contact",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="documents",
                to="api.contact",
            ),
        ),
        migrations.AddField(
            model_name="document",
            name="created_by",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="created_documents",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AddField(
            model_name="document",
            name="document_type",
            field=models.CharField(
                blank=True,
                choices=[
                    ("gendec", "General Declaration"),
                    ("quote", "Quote Form"),
                    ("customer_itinerary", "Customer Itinerary"),
                    ("internal_itinerary", "Internal Itinerary"),
                    ("payment_agreement", "Payment Agreement"),
                    ("consent_transport", "Consent for Transport"),
                    ("psa", "Patient Service Agreement"),
                    ("handling_request", "Handling Request"),
                ],
                max_length=50,
                null=True,
            ),
        ),
        migrations.AddField(
            model_name="document",
            name="file_path",
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AddField(
            model_name="document",
            name="passenger",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="passenger_documents",
                to="api.passenger",
            ),
        ),
        migrations.AddField(
            model_name="document",
            name="patient",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="patient_documents",
                to="api.patient",
            ),
        ),
        migrations.AddField(
            model_name="document",
            name="trip",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="documents",
                to="api.trip",
            ),
        ),
        migrations.AlterField(
            model_name="document",
            name="content",
            field=models.BinaryField(blank=True, null=True),
        ),
    ]

```


# File: api/migrations/0014_quote_payment_status_alter_quote_status.py

```python
# Generated by Django 5.1.11 on 2025-08-28 18:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0013_comment_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="quote",
            name="payment_status",
            field=models.CharField(
                choices=[
                    ("pending", "Pending"),
                    ("partial", "Partial Paid"),
                    ("paid", "Paid"),
                ],
                default="pending",
                max_length=20,
            ),
        ),
        migrations.AlterField(
            model_name="quote",
            name="status",
            field=models.CharField(
                choices=[
                    ("pending", "Pending"),
                    ("active", "Active"),
                    ("completed", "Completed"),
                    ("cancelled", "Cancelled"),
                ],
                db_index=True,
                default="pending",
                max_length=20,
            ),
        ),
    ]

```


# File: api/migrations/0011_rename_airport_id_tripevent_airport_and_more.py

```python
# Generated by Django 5.1.11 on 2025-08-26 04:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0010_tripevent"),
    ]

    operations = [
        migrations.RenameField(
            model_name="tripevent",
            old_name="airport_id",
            new_name="airport",
        ),
        migrations.RenameField(
            model_name="tripevent",
            old_name="crew_line_id",
            new_name="crew_line",
        ),
        migrations.RenameField(
            model_name="tripevent",
            old_name="trip_id",
            new_name="trip",
        ),
        migrations.RenameIndex(
            model_name="tripevent",
            new_name="api_tripeve_trip_id_708e55_idx",
            old_name="api_tripeve_trip_id_aaf262_idx",
        ),
    ]

```


# File: api/migrations/0005_airport_airport_type.py

```python
# Generated by Django 5.1.11 on 2025-08-24 02:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0004_rename_country_airport_iso_country_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="airport",
            name="airport_type",
            field=models.CharField(
                choices=[
                    ("large_airport", "Large airport"),
                    ("medium_airport", "Medium airport"),
                    ("small_airport", "Small airport"),
                ],
                db_index=True,
                default="small_airport",
                max_length=20,
            ),
        ),
    ]

```


# File: api/migrations/0008_fbo_phone_fbo_phone_secondary.py

```python
# Generated by Django 5.1.11 on 2025-08-26 03:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0007_contact_date_of_birth_contact_nationality_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="fbo",
            name="phone",
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AddField(
            model_name="fbo",
            name="phone_secondary",
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]

```


# File: api/management/__init__.py

```python

```


# File: api/management/commands/seed_fbos.py

```python
import csv
from pathlib import Path

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from api.models import FBO, Airport  # adjust import path if different


HEADERS = {
    "icao": ("ID", "ICAO", "Airport", "Airport ID"),
    "name": ("FBO", "Name"),
    "phone": ("PHONE", "Phone"),
    "phone2": ("PHONE2", "Phone2", "Alt Phone"),
    "email": ("Email", "E-mail"),
    "notes": ("FBO NOTES", "Notes"),
}


def pick(row, keys):
    """Return the first non-empty trimmed value from row for any of the provided keys."""
    for k in keys:
        if k in row and row[k] is not None:
            v = str(row[k]).strip()
            if v != "":
                return v
    return ""


class Command(BaseCommand):
    help = "Seed FBO records from a CSV and link them to Airports by ICAO code."

    def add_arguments(self, parser):
        parser.add_argument("csv_path", type=str, help="Path to the CSV file.")
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Parse and report without writing any changes.",
        )
        parser.add_argument(
            "--update",
            action="store_true",
            help="Update existing FBO phone/email/notes if new data present.",
        )

    @transaction.atomic
    def handle(self, *args, **opts):
        csv_path = Path(opts["csv_path"])
        dry_run = opts["dry_run"]
        do_update = opts["update"]

        if not csv_path.exists():
            raise CommandError(f"CSV not found: {csv_path}")

        created_fbos = 0
        linked_pairs = 0
        updated_fbos = 0
        skipped_rows = 0
        missing_airports = 0

        # Read CSV with BOM tolerance
        with csv_path.open("r", encoding="utf-8-sig", newline="") as f:
            reader = csv.DictReader(f)
            # Normalize header keys once (DictReader preserves original)
            # We'll still use the HEADERS map via pick()

            for i, row in enumerate(reader, start=2):  # start=2 accounts for header row = line 1
                icao = pick(row, HEADERS["icao"]).upper()
                name = pick(row, HEADERS["name"])
                phone = pick(row, HEADERS["phone"])
                phone2 = pick(row, HEADERS["phone2"])
                email = pick(row, HEADERS["email"])
                notes = pick(row, HEADERS["notes"])

                if not icao or not name:
                    skipped_rows += 1
                    self.stdout.write(self.style.WARNING(
                        f"[line {i}] Skipped: missing required ICAO and/or FBO name."
                    ))
                    continue

                airport = Airport.objects.filter(icao_code__iexact=icao).first()
                if not airport:
                    missing_airports += 1
                    self.stdout.write(self.style.WARNING(
                        f"[line {i}] No Airport found for ICAO '{icao}'. Row skipped."
                    ))
                    continue

                # Try to find an existing FBO by name (+email/phone if available) to avoid global name collisions
                fbo_qs = FBO.objects.filter(name__iexact=name)
                if email:
                    fbo_qs = fbo_qs.filter(email__iexact=email) | fbo_qs
                if phone:
                    fbo_qs = fbo_qs.filter(phone__iexact=phone) | fbo_qs

                fbo = fbo_qs.distinct().first()

                if fbo is None:
                    # Create new FBO
                    fbo = FBO(
                        name=name,
                        phone=phone or None,
                        phone_secondary=phone2 or None,
                        email=email or None,
                        notes=notes or None,
                    )
                    if not dry_run:
                        fbo.save()
                    created_fbos += 1
                    self.stdout.write(self.style.SUCCESS(
                        f"[line {i}] Created FBO '{name}'."
                    ))
                else:
                    # Optionally update existing with any new info provided
                    if do_update:
                        changed = False
                        if phone and fbo.phone != phone:
                            fbo.phone = phone
                            changed = True
                        if phone2 and fbo.phone_secondary != phone2:
                            fbo.phone_secondary = phone2
                            changed = True
                        if email and (fbo.email or "").lower() != email.lower():
                            fbo.email = email
                            changed = True
                        if notes and (fbo.notes or "").strip() != notes:
                            fbo.notes = notes
                            changed = True
                        if changed and not dry_run:
                            fbo.save()
                            updated_fbos += 1
                            self.stdout.write(self.style.SUCCESS(
                                f"[line {i}] Updated FBO '{name}'."
                            ))

                # Link to Airport via M2M (Airport ↔ FBO)
                if not dry_run:
                    airport.fbos.add(fbo)
                linked_pairs += 1

        if dry_run:
            self.stdout.write(self.style.WARNING("DRY RUN: no changes were written."))

        self.stdout.write(self.style.SUCCESS(
            f"Done. Created FBOs: {created_fbos}, Updated: {updated_fbos}, "
            f"Linked (Airport↔FBO): {linked_pairs}, Skipped rows: {skipped_rows}, "
            f"Missing airports: {missing_airports}"
        ))

```


# File: api/management/commands/seed_dev.py

```python
# api/management/commands/seed_dev.py
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.db import transaction, connection
from decimal import Decimal
from datetime import timedelta, datetime
from django.utils import timezone
from uuid import UUID

from api.models import (
    Permission, Role, Department, UserProfile, Contact, FBO, Ground, Airport,
    Document, Aircraft, Transaction, Agreement, Patient, Quote, Passenger,
    CrewLine, Trip, TripLine
)

def aware(dt_str: str):
    dt = datetime.fromisoformat(dt_str)
    return timezone.make_aware(dt) if timezone.is_naive(dt) else dt

class Command(BaseCommand):
    help = "Seed development/test data"

    def handle(self, *args, **options):
        with transaction.atomic():
            self.stdout.write(self.style.NOTICE("Seeding data..."))

            # --- Base users for created_by/modified_by ---
            admin_user, _ = User.objects.get_or_create(
                username="admin",
                defaults={"email": "admin@example.com", "is_staff": True, "is_superuser": True}
            )
            if not admin_user.has_usable_password():
                admin_user.set_password("admin123")
                admin_user.save()

            alice_user, _ = User.objects.get_or_create(
                username="alice",
                defaults={"email": "alice@example.com", "is_staff": True}
            )
            if not alice_user.has_usable_password():
                alice_user.set_password("password123")
                alice_user.save()

            bob_user, _ = User.objects.get_or_create(
                username="bob",
                defaults={"email": "bob@example.com"}
            )
            if not bob_user.has_usable_password():
                bob_user.set_password("password123")
                bob_user.save()

            # --- Your explicit auth_user id=7 + exact hash/timestamps ---
            target_user_id = 7
            password_hash = "pbkdf2_sha256$870000$FXqSBkZnJCTre722mo1IwH$feY/56s+7Ry8EnAEmrNRFZdw0q7jZZ6KmjM6jly+R2s="
            last_login_str = "2025-08-16 16:34:56.213251"
            date_joined_str = "2025-08-16 15:54:58.108485"

            u7, created = User.objects.get_or_create(
                id=target_user_id,
                defaults=dict(
                    username="chaimkitchner",
                    email="ck@cekitch.com",
                    is_superuser=True,
                    is_staff=True,
                    is_active=True,
                    password=password_hash,
                    last_login=aware(last_login_str),
                    date_joined=aware(date_joined_str),
                ),
            )
            if not created:
                u7.username = "chaimkitchner"
                u7.email = "ck@cekitch.com"
                u7.is_superuser = True
                u7.is_staff = True
                u7.is_active = True
                u7.password = password_hash
                u7.save(update_fields=["username", "email", "is_superuser", "is_staff", "is_active", "password"])
                User.objects.filter(pk=u7.pk).update(
                    last_login=aware(last_login_str),
                    date_joined=aware(date_joined_str),
                )

            # bump sequence in Postgres so future inserts don't collide with id=7
            if connection.vendor == "postgresql":
                with connection.cursor() as cur:
                    cur.execute(
                        "SELECT setval(pg_get_serial_sequence('auth_user','id'), "
                        "(SELECT GREATEST(COALESCE(MAX(id), 1), 1) FROM auth_user))"
                    )

            # --- Matching api_userprofile record (UUID + timestamps you provided) ---
            profile_id = UUID("26e9897c-9ffe-427d-beaa-e1c6e8978f19")
            created_on_str = "2025-08-16 16:46:57.983721"
            modified_on_str = "2025-08-21 06:52:22.459238"

            up_defaults = dict(
                user=u7,
                first_name="Chaim",
                last_name="Kitchner",
                email="ck@cekitch.com",
                status="active",
                lock=False,
                created_by=u7,
                modified_by=u7,
            )
            up, up_created = UserProfile.objects.get_or_create(id=profile_id, defaults=up_defaults)
            if not up_created:
                up.user = u7
                up.first_name = "Chaim"
                up.last_name = "Kitchner"
                up.email = "ck@cekitch.com"
                up.status = "active"
                up.lock = False
                up.created_by = u7
                up.modified_by = u7
                up.save()
            UserProfile.objects.filter(pk=profile_id).update(
                created_on=aware(created_on_str),
                modified_on=aware(modified_on_str),
            )

            # --- Permissions / Roles / Departments ---
            p_view, _ = Permission.objects.get_or_create(
                name="view_quotes",
                defaults={"description": "Can view quotes", "created_by": admin_user, "modified_by": admin_user},
            )
            p_edit, _ = Permission.objects.get_or_create(
                name="edit_quotes",
                defaults={"description": "Can edit quotes", "created_by": admin_user, "modified_by": admin_user},
            )
            p_trips, _ = Permission.objects.get_or_create(
                name="manage_trips",
                defaults={"description": "Can manage trips", "created_by": admin_user, "modified_by": admin_user},
            )

            role_admin, _ = Role.objects.get_or_create(
                name="Admin",
                defaults={"description": "Admin role", "created_by": admin_user, "modified_by": admin_user},
            )
            role_admin.permissions.set([p_view, p_edit, p_trips])

            role_ops, _ = Role.objects.get_or_create(
                name="Dispatcher",
                defaults={"description": "Operations/Dispatcher", "created_by": admin_user, "modified_by": admin_user},
            )
            role_ops.permissions.set([p_view, p_trips])

            dept_ops, _ = Department.objects.get_or_create(
                name="Operations",
                defaults={"description": "Ops department", "created_by": admin_user, "modified_by": admin_user},
            )
            dept_med, _ = Department.objects.get_or_create(
                name="Medical",
                defaults={"description": "Medical department", "created_by": admin_user, "modified_by": admin_user},
            )
            dept_ops.permission_ids.set([p_view, p_trips, p_edit])
            dept_med.permission_ids.set([p_view])

            # hook M2Ms for user profiles
            up.roles.set([role_admin])
            up.departments.set([dept_ops])
            up.department_ids.set([dept_ops])

            # --- Contacts (pilots/medic/customer) ---
            pilot1, _ = Contact.objects.get_or_create(
                first_name="Pat", last_name="Pilot",
                defaults={"email": "pat.pilot@example.com", "created_by": admin_user, "modified_by": admin_user},
            )
            pilot2, _ = Contact.objects.get_or_create(
                first_name="Sam", last_name="Second",
                defaults={"email": "sam.second@example.com", "created_by": admin_user, "modified_by": admin_user},
            )
            medic1, _ = Contact.objects.get_or_create(
                first_name="Rory", last_name="RN",
                defaults={"email": "rory.rn@example.com", "created_by": admin_user, "modified_by": admin_user},
            )
            customer, _ = Contact.objects.get_or_create(
                business_name="Oceanic Cruises",
                defaults={"email": "ops@oceanic.example.com", "created_by": admin_user, "modified_by": admin_user},
            )

            # --- FBO / Ground / Airports ---
            fbo_jfk, _ = FBO.objects.get_or_create(
                name="Signature JFK",
                defaults={"city": "New York", "state": "NY", "created_by": admin_user, "modified_by": admin_user},
            )
            fbo_jfk.contacts.set([pilot1])

            ground_lax, _ = Ground.objects.get_or_create(
                name="LAX Limo",
                defaults={"city": "Los Angeles", "state": "CA", "created_by": admin_user, "modified_by": admin_user},
            )
            ground_lax.contacts.set([customer])

            jfk, _ = Airport.objects.get_or_create(
                icao_code="KJFK",
                defaults=dict(
                    iata_code="JFK", name="John F. Kennedy International", city="New York",
                    state="NY", country="USA", elevation=13,
                    latitude=Decimal("40.641311"), longitude=Decimal("-73.778139"),
                    timezone="America/New_York", created_by=admin_user, modified_by=admin_user
                ),
            )
            lax, _ = Airport.objects.get_or_create(
                icao_code="KLAX",
                defaults=dict(
                    iata_code="LAX", name="Los Angeles International", city="Los Angeles",
                    state="CA", country="USA", elevation=125,
                    latitude=Decimal("33.941589"), longitude=Decimal("-118.408530"),
                    timezone="America/Los_Angeles", created_by=admin_user, modified_by=admin_user
                ),
            )
            jfk.fbos.add(fbo_jfk)
            lax.grounds.add(ground_lax)

            # --- Aircraft ---
            aircraft, _ = Aircraft.objects.get_or_create(
                tail_number="N123AB",
                defaults=dict(
                    company="Airmed Partners", mgtow=Decimal("21500.00"),
                    make="Learjet", model="35A", serial_number="LJ35-0001",
                    created_by=admin_user, modified_by=admin_user
                ),
            )

            # --- Documents & Agreements ---
            pdf_bytes = b"%PDF-1.4 test\n%%EOF"
            doc_quote, _ = Document.objects.get_or_create(filename="quote.pdf", defaults={"content": pdf_bytes})
            doc_agree, _ = Document.objects.get_or_create(filename="agreement.pdf", defaults={"content": pdf_bytes})
            doc_passport, _ = Document.objects.get_or_create(filename="passport.jpg", defaults={"content": b'\x00\x01TEST'})

            agreement_payment, _ = Agreement.objects.get_or_create(
                destination_email="billing@oceanic.example.com",
                defaults={"document_unsigned": doc_agree, "status": "created",
                          "created_by": admin_user, "modified_by": admin_user},
            )
            agreement_consent, _ = Agreement.objects.get_or_create(
                destination_email="consent@oceanic.example.com",
                defaults={"document_unsigned": doc_agree, "status": "created",
                          "created_by": admin_user, "modified_by": admin_user},
            )

            # --- Patient / Passengers ---
            patient_contact, _ = Contact.objects.get_or_create(
                first_name="Jamie", last_name="Doe",
                defaults={"email": "jamie@example.com", "created_by": admin_user, "modified_by": admin_user},
            )
            patient, _ = Patient.objects.get_or_create(
                info=patient_contact,
                defaults=dict(
                    bed_at_origin=True, bed_at_destination=False,
                    date_of_birth=timezone.now().date().replace(year=1988),
                    nationality="USA", passport_number="X1234567",
                    passport_expiration_date=timezone.now().date().replace(year=2032),
                    passport_document=doc_passport, status="pending",
                    created_by=admin_user, modified_by=admin_user
                ),
            )

            pax_contact1, _ = Contact.objects.get_or_create(
                first_name="Alex", last_name="Doe",
                defaults={"email": "alex@example.com", "created_by": admin_user, "modified_by": admin_user},
            )
            pax1, _ = Passenger.objects.get_or_create(
                info=pax_contact1,
                defaults=dict(
                    nationality="USA", passport_number="PAX001",
                    passport_expiration_date=timezone.now().date().replace(year=2030),
                    contact_number="+1-555-0110", passport_document=doc_passport,
                    created_by=admin_user, modified_by=admin_user
                ),
            )

            pax_contact2, _ = Contact.objects.get_or_create(
                first_name="Taylor", last_name="Smith",
                defaults={"email": "taylor@example.com", "created_by": admin_user, "modified_by": admin_user},
            )
            pax2, _ = Passenger.objects.get_or_create(
                info=pax_contact2,
                defaults=dict(
                    nationality="USA", passport_number="PAX002",
                    passport_expiration_date=timezone.now().date().replace(year=2031),
                    contact_number="+1-555-0111", passport_document=doc_passport,
                    created_by=admin_user, modified_by=admin_user
                ),
            )
            pax1.passenger_ids.add(pax2)

            # --- Crew Line ---
            crew, _ = CrewLine.objects.get_or_create(
                primary_in_command=pilot1,
                secondary_in_command=pilot2,
                defaults={"created_by": admin_user, "modified_by": admin_user},
            )
            crew.medic_ids.set([medic1])

            # --- Quote ---
            quote, _ = Quote.objects.get_or_create(
                contact=customer, pickup_airport=jfk, dropoff_airport=lax,
                defaults=dict(
                    quoted_amount=Decimal("45999.00"),
                    aircraft_type="35",
                    estimated_flight_time=timedelta(hours=5, minutes=30),
                    includes_grounds=True, inquiry_date=timezone.now(),
                    medical_team="RN/Paramedic", patient=patient,
                    status="pending", number_of_stops=1,
                    quote_pdf=doc_quote, quote_pdf_status="created",
                    quote_pdf_email="quotes@airmed.example.com",
                    payment_agreement=agreement_payment,
                    consent_for_transport=agreement_consent,
                    created_by=admin_user, modified_by=admin_user
                ),
            )
            quote.documents.set([doc_quote])

            # --- Transaction ---
            txn, _ = Transaction.objects.get_or_create(
                email="payer@oceanic.example.com",
                amount=Decimal("10000.00"),
                payment_method="credit_card",
                defaults=dict(
                    payment_status="completed",
                    payment_date=timezone.now(),
                    created_by=admin_user, modified_by=admin_user
                ),
            )
            quote.transactions.add(txn)

            # --- Trip + legs ---
            trip, _ = Trip.objects.get_or_create(
                trip_number="TRIP-0001",
                defaults=dict(
                    email_chain=[], quote=quote, type="medical", patient=patient,
                    estimated_departure_time=timezone.now() + timedelta(days=3, hours=2),
                    post_flight_duty_time=timedelta(hours=2),
                    pre_flight_duty_time=timedelta(hours=1),
                    aircraft=aircraft,
                    internal_itinerary=doc_quote,
                    customer_itinerary=doc_quote,
                    created_by=admin_user, modified_by=admin_user
                ),
            )
            trip.passengers.set([pax1, pax2])

            dep_utc = timezone.now() + timedelta(days=3, hours=2)
            arr_utc = dep_utc + timedelta(hours=6)
            TripLine.objects.get_or_create(
                trip=trip, origin_airport=jfk, destination_airport=lax,
                departure_time_local=dep_utc, departure_time_utc=dep_utc,
                arrival_time_local=arr_utc, arrival_time_utc=arr_utc,
                defaults=dict(
                    crew_line=crew, distance=Decimal("2475.50"),
                    flight_time=timedelta(hours=6), ground_time=timedelta(minutes=45),
                    passenger_leg=True, created_by=admin_user, modified_by=admin_user
                ),
            )

            dep2 = arr_utc + timedelta(hours=2)
            arr2 = dep2 + timedelta(hours=5, minutes=45)
            TripLine.objects.get_or_create(
                trip=trip, origin_airport=lax, destination_airport=jfk,
                departure_time_local=dep2, departure_time_utc=dep2,
                arrival_time_local=arr2, arrival_time_utc=arr2,
                defaults=dict(
                    crew_line=crew, distance=Decimal("2475.50"),
                    flight_time=timedelta(hours=5, minutes=45), ground_time=timedelta(minutes=30),
                    passenger_leg=True, created_by=admin_user, modified_by=admin_user
                ),
            )

            self.stdout.write(self.style.SUCCESS("✅ Seed complete."))
            self.stdout.write(self.style.SUCCESS("Users: admin/admin123; alice/bob with password123"))
            self.stdout.write(self.style.SUCCESS("Custom user id=7: chaimkitchner (pre-hashed)"))

```


# File: api/management/commands/seed_test_data.py

```python
from django.core.management.base import BaseCommand
from django.utils import timezone
from decimal import Decimal
import random
from datetime import datetime, timedelta
from api.models import (
    Contact, Patient, Quote, Trip, Passenger, Airport, Aircraft, 
    TripLine, CrewLine, Staff, StaffRole
)

class Command(BaseCommand):
    help = 'Seeds the database with test data: 20 patients, quotes, trips, and passengers'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting to seed test data...'))
        
        # Get some airports and aircraft for relationships
        airports = list(Airport.objects.all()[:10])
        aircraft = list(Aircraft.objects.all()[:5])
        
        if not airports:
            self.stdout.write(self.style.ERROR('No airports found. Please seed airports first.'))
            return
            
        if not aircraft:
            self.stdout.write(self.style.ERROR('No aircraft found. Please seed aircraft first.'))
            return
        
        # Create staff if they don't exist
        self.create_staff_if_needed()
        staff_members = list(Staff.objects.all()[:10])
        
        # Seed patients
        patients = self.seed_patients()
        self.stdout.write(self.style.SUCCESS(f'Created {len(patients)} patients'))
        
        # Seed passengers
        passengers = self.seed_passengers()
        self.stdout.write(self.style.SUCCESS(f'Created {len(passengers)} passengers'))
        
        # Seed quotes
        quotes = self.seed_quotes(patients, airports)
        self.stdout.write(self.style.SUCCESS(f'Created {len(quotes)} quotes'))
        
        # Seed trips
        trips = self.seed_trips(patients, aircraft, airports, staff_members, quotes)
        self.stdout.write(self.style.SUCCESS(f'Created {len(trips)} trips'))
        
        self.stdout.write(self.style.SUCCESS('Successfully seeded all test data!'))

    def create_staff_if_needed(self):
        """Create some basic staff members if they don't exist"""
        if Staff.objects.count() < 5:
            staff_names = [
                ('John', 'Pilot', 'john.pilot@jeticu.com'),
                ('Sarah', 'Copilot', 'sarah.copilot@jeticu.com'),
                ('Mike', 'Nurse', 'mike.nurse@jeticu.com'),
                ('Lisa', 'Paramedic', 'lisa.paramedic@jeticu.com'),
                ('Dave', 'Captain', 'dave.captain@jeticu.com'),
            ]
            
            for first_name, last_name, email in staff_names:
                if not Contact.objects.filter(email=email).exists():
                    contact = Contact.objects.create(
                        first_name=first_name,
                        last_name=last_name,
                        email=email,
                        phone=f'+1-555-{random.randint(100, 999)}-{random.randint(1000, 9999)}'
                    )
                    Staff.objects.create(contact=contact, active=True)

    def seed_patients(self):
        """Create 20 test patients"""
        patients = []
        first_names = ['John', 'Jane', 'Michael', 'Sarah', 'David', 'Lisa', 'Robert', 'Maria', 'James', 'Jennifer',
                      'William', 'Patricia', 'Richard', 'Linda', 'Joseph', 'Barbara', 'Thomas', 'Elizabeth', 'Daniel', 'Susan']
        last_names = ['Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Garcia', 'Miller', 'Davis', 'Rodriguez', 'Martinez',
                     'Hernandez', 'Lopez', 'Gonzalez', 'Wilson', 'Anderson', 'Thomas', 'Taylor', 'Moore', 'Jackson', 'Martin']
        
        for i in range(20):
            # Create contact for patient
            contact = Contact.objects.create(
                first_name=random.choice(first_names),
                last_name=random.choice(last_names),
                email=f'patient{i+1}@example.com',
                phone=f'+1-555-{random.randint(100, 999)}-{random.randint(1000, 9999)}',
                date_of_birth=datetime.now().date() - timedelta(days=random.randint(365*20, 365*80)),
                nationality='United States'
            )
            
            # Create patient
            patient = Patient.objects.create(
                info=contact,
                date_of_birth=contact.date_of_birth,
                nationality=contact.nationality,
                passport_number=f'P{random.randint(100000000, 999999999)}',
                passport_expiration_date=datetime.now().date() + timedelta(days=random.randint(365, 365*5)),
                bed_at_origin=random.choice([True, False]),
                bed_at_destination=random.choice([True, False]),
                special_instructions=f'Special care instructions for patient {i+1}',
                status='active'
            )
            patients.append(patient)
            
        return patients

    def seed_passengers(self):
        """Create 20 test passengers"""
        passengers = []
        first_names = ['Alex', 'Chris', 'Jordan', 'Taylor', 'Morgan', 'Casey', 'Jamie', 'Riley', 'Avery', 'Quinn',
                      'Sage', 'River', 'Phoenix', 'Skyler', 'Cameron', 'Dakota', 'Emery', 'Finley', 'Harper', 'Kendall']
        last_names = ['White', 'Harris', 'Clark', 'Lewis', 'Robinson', 'Walker', 'Perez', 'Hall', 'Young', 'Allen',
                     'Sanchez', 'Wright', 'King', 'Scott', 'Green', 'Baker', 'Adams', 'Nelson', 'Hill', 'Ramirez']
        
        for i in range(20):
            # Create contact for passenger
            contact = Contact.objects.create(
                first_name=random.choice(first_names),
                last_name=random.choice(last_names),
                email=f'passenger{i+1}@example.com',
                phone=f'+1-555-{random.randint(100, 999)}-{random.randint(1000, 9999)}',
                date_of_birth=datetime.now().date() - timedelta(days=random.randint(365*18, 365*70))
            )
            
            # Create passenger
            passenger = Passenger.objects.create(
                info=contact,
                date_of_birth=contact.date_of_birth,
                nationality='United States',
                passport_number=f'P{random.randint(100000000, 999999999)}',
                passport_expiration_date=datetime.now().date() + timedelta(days=random.randint(365, 365*5)),
                contact_number=contact.phone,
                notes=f'Passenger notes for {contact.first_name} {contact.last_name}'
            )
            passengers.append(passenger)
            
        return passengers

    def seed_quotes(self, patients, airports):
        """Create 20 test quotes"""
        quotes = []
        
        for i in range(20):
            # Create contact for customer
            contact = Contact.objects.create(
                first_name=f'Customer{i+1}',
                last_name='Family',
                email=f'customer{i+1}@example.com',
                phone=f'+1-555-{random.randint(100, 999)}-{random.randint(1000, 9999)}'
            )
            
            quote = Quote.objects.create(
                contact=contact,
                patient=random.choice(patients) if random.choice([True, False]) else None,
                pickup_airport=random.choice(airports),
                dropoff_airport=random.choice(airports),
                quoted_amount=Decimal(str(random.randint(5000, 50000))),
                aircraft_type=random.choice(['65', '35', 'TBD']),
                medical_team=random.choice(['RN/RN', 'RN/Paramedic', 'RN/MD', 'standard', 'full']),
                estimated_flight_time=timedelta(hours=random.randint(1, 8)),
                includes_grounds=random.choice([True, False]),
                status=random.choice(['pending', 'active', 'completed', 'cancelled'])
            )
            quotes.append(quote)
            
        return quotes

    def seed_trips(self, patients, aircraft, airports, staff_members, quotes):
        """Create 20 test trips with trip lines"""
        trips = []
        
        for i in range(20):
            # Create trip
            trip = Trip.objects.create(
                trip_number=f'{10000 + i + 1:05d}',
                type=random.choice(['medical', 'charter', 'part 91', 'maintenance']),
                aircraft=random.choice(aircraft) if random.choice([True, False]) else None,
                patient=random.choice(patients) if random.choice([True, False]) else None,
                quote=random.choice(quotes) if random.choice([True, False]) else None,
                status=random.choice(['pending', 'active', 'completed', 'cancelled']),
                notes=f'Trip notes for trip {i+1}',
                estimated_departure_time=timezone.now() + timedelta(days=random.randint(1, 30)),
                pre_flight_duty_time=timedelta(hours=1),
                post_flight_duty_time=timedelta(hours=1)
            )
            
            # Create trip lines for each trip (1-3 legs)
            num_legs = random.randint(1, 3)
            current_time = timezone.now() + timedelta(days=random.randint(1, 30))
            
            for leg in range(num_legs):
                origin = random.choice(airports)
                destination = random.choice([a for a in airports if a != origin])
                
                # Create crew line if we have enough staff
                crew_line = None
                if len(staff_members) >= 2:
                    pic_staff = random.choice(staff_members)
                    sic_staff = random.choice([s for s in staff_members if s != pic_staff])
                    medic_staff = random.sample([s for s in staff_members if s not in [pic_staff, sic_staff]], 
                                              min(2, len(staff_members) - 2))
                    
                    crew_line = CrewLine.objects.create(
                        primary_in_command=pic_staff.contact,
                        secondary_in_command=sic_staff.contact
                    )
                    for medic in medic_staff:
                        crew_line.medic_ids.add(medic.contact)
                
                # Create trip line
                departure_time = current_time + timedelta(hours=random.randint(1, 4))
                flight_duration = timedelta(hours=random.randint(1, 6), minutes=random.randint(0, 59))
                arrival_time = departure_time + flight_duration
                
                TripLine.objects.create(
                    trip=trip,
                    origin_airport=origin,
                    destination_airport=destination,
                    crew_line=crew_line,
                    departure_time_local=departure_time,
                    departure_time_utc=departure_time,
                    arrival_time_local=arrival_time,
                    arrival_time_utc=arrival_time,
                    distance=Decimal(str(random.randint(100, 2000))),
                    flight_time=flight_duration,
                    ground_time=timedelta(hours=1),
                    passenger_leg=True
                )
                
                current_time = arrival_time + timedelta(hours=1)  # 1 hour ground time
            
            trips.append(trip)
            
        return trips
```


# File: api/management/commands/__init__.py

```python

```


# File: api/management/commands/check_trip_timezones.py

```python
from django.core.management.base import BaseCommand
from api.models import Trip, TripLine, Airport


class Command(BaseCommand):
    help = 'Check timezone data for a specific trip'

    def add_arguments(self, parser):
        parser.add_argument('trip_id', type=str, help='Trip ID to check')

    def handle(self, *args, **options):
        trip_id = options['trip_id']
        
        try:
            trip = Trip.objects.get(id=trip_id)
            self.stdout.write(f"Trip: {trip.trip_number}")
            
            trip_lines = trip.trip_lines.all()
            self.stdout.write(f"Found {trip_lines.count()} trip lines")
            
            for i, line in enumerate(trip_lines, 1):
                self.stdout.write(f"\n--- Trip Line {i} ---")
                
                # Check origin airport
                if line.origin_airport:
                    self.stdout.write(f"Origin: {line.origin_airport.name} ({line.origin_airport.ident})")
                    self.stdout.write(f"Origin timezone: {line.origin_airport.timezone or 'NOT SET'}")
                else:
                    self.stdout.write("Origin: NOT SET")
                
                # Check destination airport
                if line.destination_airport:
                    self.stdout.write(f"Destination: {line.destination_airport.name} ({line.destination_airport.ident})")
                    self.stdout.write(f"Destination timezone: {line.destination_airport.timezone or 'NOT SET'}")
                else:
                    self.stdout.write("Destination: NOT SET")
                
                # Check times
                self.stdout.write(f"Departure local: {line.departure_time_local}")
                self.stdout.write(f"Departure UTC: {line.departure_time_utc}")
                self.stdout.write(f"Arrival local: {line.arrival_time_local}")
                self.stdout.write(f"Arrival UTC: {line.arrival_time_utc}")
                
        except Trip.DoesNotExist:
            self.stdout.write(f"Trip {trip_id} not found")
        except Exception as e:
            self.stdout.write(f"Error: {str(e)}")
```


# File: api/management/commands/setup_test_data.py

```python
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.db import transaction
from api.models import (
    Contact, UserProfile, Role, Department, Airport, Aircraft, 
    Passenger, CrewLine, Trip, TripLine, Quote, Patient, Document, Transaction
)
import os


class Command(BaseCommand):
    help = 'Set up test data for API endpoint testing'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Setting up test data...'))
        
        with transaction.atomic():
            # Create admin user
            admin_user, created = User.objects.get_or_create(
                username='admin',
                defaults={
                    'email': 'admin@jetmain.com',
                    'first_name': 'Admin',
                    'last_name': 'User',
                    'is_staff': True,
                    'is_superuser': True
                }
            )
            if created:
                admin_user.set_password('admin')
                admin_user.save()
                self.stdout.write(f'✅ Created admin user: admin/admin')
            else:
                self.stdout.write(f'✅ Admin user already exists')

            # Create test user
            test_user, created = User.objects.get_or_create(
                username='testuser',
                defaults={
                    'email': 'test@jetmain.com',
                    'first_name': 'Test',
                    'last_name': 'User',
                    'is_staff': False,
                    'is_superuser': False
                }
            )
            if created:
                test_user.set_password('testpass')
                test_user.save()
                self.stdout.write(f'✅ Created test user: testuser/testpass')

            # Create roles
            pilot_role, _ = Role.objects.get_or_create(
                name='Pilot',
                defaults={'description': 'Aircraft pilot'}
            )
            medic_role, _ = Role.objects.get_or_create(
                name='Medic',
                defaults={'description': 'Medical personnel'}
            )
            admin_role, _ = Role.objects.get_or_create(
                name='Admin',
                defaults={'description': 'Administrator'}
            )

            # Create departments
            flight_dept, _ = Department.objects.get_or_create(
                name='Flight Operations',
                defaults={'description': 'Flight operations department'}
            )
            medical_dept, _ = Department.objects.get_or_create(
                name='Medical',
                defaults={'description': 'Medical department'}
            )

            # Create contacts
            contacts = []
            for i in range(1, 6):
                contact, _ = Contact.objects.get_or_create(
                    email=f'contact{i}@jetmain.com',
                    defaults={
                        'first_name': f'Contact{i}',
                        'last_name': f'User{i}',
                        'phone': f'+123456789{i}',
                        'address_line1': f'{i}00 Test Street',
                        'city': 'Test City',
                        'state': 'TS',
                        'zip': f'1234{i}',
                        'country': 'USA'
                    }
                )
                contacts.append(contact)

            # Create UserProfiles
            admin_profile, _ = UserProfile.objects.get_or_create(
                user=admin_user,
                defaults={
                    'first_name': 'Admin',
                    'last_name': 'User',
                    'phone': '+1234567890',
                    'address_line1': '123 Admin Street',
                    'city': 'Admin City',
                    'state': 'AC',
                    'zip': '12345',
                    'country': 'USA'
                }
            )
            admin_profile.roles.add(admin_role)
            admin_profile.departments.add(flight_dept)

            test_profile, _ = UserProfile.objects.get_or_create(
                user=test_user,
                defaults={
                    'first_name': 'Test',
                    'last_name': 'User',
                    'phone': '+1234567891',
                    'address_line1': '456 Test Street',
                    'city': 'Test City',
                    'state': 'TC',
                    'zip': '54321',
                    'country': 'USA'
                }
            )
            test_profile.roles.add(pilot_role)
            test_profile.departments.add(flight_dept)

            # Create airports
            airports = []
            airport_data = [
                ('KORD', 'Chicago O\'Hare', 'Chicago', 'IL'),
                ('KLAX', 'Los Angeles International', 'Los Angeles', 'CA'),
                ('KJFK', 'John F Kennedy International', 'New York', 'NY'),
                ('KDEN', 'Denver International', 'Denver', 'CO')
            ]
            
            for icao, name, city, state in airport_data:
                airport, _ = Airport.objects.get_or_create(
                    icao_code=icao,
                    defaults={
                        'name': name,
                        'city': city,
                        'state': state,
                        'country': 'USA',
                        'latitude': 40.0,
                        'longitude': -87.0
                    }
                )
                airports.append(airport)

            # Create aircraft
            aircraft, _ = Aircraft.objects.get_or_create(
                tail_number='N123JM',
                defaults={
                    'company': 'JET-MAIN',
                    'make': 'Cessna',
                    'model': 'Citation X',
                    'serial_number': 'SN123456',
                    'mgtow': 15000.00
                }
            )

            # Create passengers
            passengers = []
            for i, contact in enumerate(contacts[:3]):
                passenger, _ = Passenger.objects.get_or_create(
                    info=contact,
                    defaults={
                        'passport_number': f'P{i+1}234567',
                        'passport_expiration_date': '2030-12-31',
                        'contact_number': f'+198765432{i+1}',
                        'notes': f'No known allergies for passenger {i+1}',
                        'nationality': 'USA'
                    }
                )
                passengers.append(passenger)

            # Create patients
            patients = []
            for i, contact in enumerate(contacts[3:]):
                patient, _ = Patient.objects.get_or_create(
                    info=contact,
                    defaults={
                        'date_of_birth': '1990-01-01',
                        'nationality': 'USA',
                        'passport_number': f'PT{i+1}234567',
                        'passport_expiration_date': '2030-12-31',
                        'status': 'active',
                        'special_instructions': f'Patient {i+1} medical history',
                        'bed_at_origin': False,
                        'bed_at_destination': False
                    }
                )
                patients.append(patient)

            # Create crew lines
            crew_lines = []
            for i in range(2):
                crew_line, _ = CrewLine.objects.get_or_create(
                    primary_in_command_id=contacts[0],
                    secondary_in_command_id=contacts[1]
                )
                crew_line.medic_ids.add(contacts[2])
                crew_lines.append(crew_line)

            # Create quotes
            quotes = []
            for i in range(2):
                quote, _ = Quote.objects.get_or_create(
                    quoted_amount=15000.00,
                    contact_id=contacts[0],
                    pickup_airport_id=airports[0],
                    dropoff_airport_id=airports[1],
                    defaults={
                        'patient_id': patients[0] if patients else None,
                        'aircraft_type': 'TBD',
                        'estimated_fight_time': 4.0,
                        'medical_team': 'standard',
                        'status': 'pending',
                        'quote_pdf_email': f'quote{i+1}@jetmain.com',
                        'includes_grounds': False,
                        'number_of_stops': 0
                    }
                )
                quotes.append(quote)

            # Create trips
            trips = []
            for i, quote in enumerate(quotes):
                trip, _ = Trip.objects.get_or_create(
                    trip_number=f'TR{i+1:04d}',
                    defaults={
                        'quote_id': quote,
                        'patient_id': patients[0] if patients else None,
                        'aircraft_id': aircraft,
                        'type': 'medical',
                        'estimated_departure_time': '2024-12-01T10:00:00Z'
                    }
                )
                trip.passengers.add(passengers[0])
                trips.append(trip)

            # Create trip lines
            for i, trip in enumerate(trips):
                trip_line, _ = TripLine.objects.get_or_create(
                    trip_id=trip,
                    origin_airport_id=airports[i],
                    destination_airport_id=airports[i+1],
                    defaults={
                        'crew_line_id': crew_lines[0],
                        'departure_time_local': '2024-12-01T10:00:00',
                        'departure_time_utc': '2024-12-01T15:00:00Z',
                        'arrival_time_local': '2024-12-01T14:00:00',
                        'arrival_time_utc': '2024-12-01T19:00:00Z',
                        'distance': 1000.00,
                        'flight_time': 4.0,
                        'ground_time': 1.0,
                        'passenger_leg': True
                    }
                )

            # Create documents
            doc, _ = Document.objects.get_or_create(
                filename='test_document.pdf',
                defaults={
                    'content': b'Test document content',
                    'flag': 0
                }
            )

            # Create transactions
            for i, quote in enumerate(quotes):
                transaction_obj, _ = Transaction.objects.get_or_create(
                    amount=quote.quoted_amount,
                    email=f'transaction{i+1}@jetmain.com',
                    defaults={
                        'payment_method': 'credit_card',
                        'payment_status': 'pending'
                    }
                )

        self.stdout.write(self.style.SUCCESS('✅ Test data setup completed!'))
        self.stdout.write(self.style.SUCCESS(''))
        self.stdout.write(self.style.SUCCESS('Test Accounts:'))
        self.stdout.write(self.style.SUCCESS('  Admin: admin/admin'))
        self.stdout.write(self.style.SUCCESS('  User:  testuser/testpass'))
        self.stdout.write(self.style.SUCCESS(''))
        self.stdout.write(self.style.SUCCESS('You can now run the API tests!'))

```


# File: api/management/commands/remove_test_data.py

```python
from django.core.management.base import BaseCommand
from django.db import transaction
from datetime import datetime, timedelta
from api.models import (
    Contact, Patient, Quote, Trip, Passenger, TripLine, CrewLine
)

class Command(BaseCommand):
    help = 'Removes the test data created by seed_test_data command'

    def handle(self, *args, **options):
        self.stdout.write(self.style.WARNING('Starting to remove test data...'))
        
        with transaction.atomic():
            # Remove trips with trip numbers 10001-10020
            trips_deleted = Trip.objects.filter(
                trip_number__in=[f'{10000 + i:05d}' for i in range(1, 21)]
            ).delete()
            self.stdout.write(f'Deleted trips: {trips_deleted[0]} records')
            
            # Remove quotes from test customers
            quotes_deleted = Quote.objects.filter(
                contact__email__startswith='customer'
            ).delete()
            self.stdout.write(f'Deleted quotes: {quotes_deleted[0]} records')
            
            # Remove test contacts (customers)
            customer_contacts_deleted = Contact.objects.filter(
                email__startswith='customer'
            ).delete()
            self.stdout.write(f'Deleted customer contacts: {customer_contacts_deleted[0]} records')
            
            # Remove test patients
            patients_deleted = Patient.objects.filter(
                info__email__startswith='patient'
            ).delete()
            self.stdout.write(f'Deleted patients: {patients_deleted[0]} records')
            
            # Remove test patient contacts
            patient_contacts_deleted = Contact.objects.filter(
                email__startswith='patient'
            ).delete()
            self.stdout.write(f'Deleted patient contacts: {patient_contacts_deleted[0]} records')
            
            # Remove test passengers
            passengers_deleted = Passenger.objects.filter(
                info__email__startswith='passenger'
            ).delete()
            self.stdout.write(f'Deleted passengers: {passengers_deleted[0]} records')
            
            # Remove test passenger contacts
            passenger_contacts_deleted = Contact.objects.filter(
                email__startswith='passenger'
            ).delete()
            self.stdout.write(f'Deleted passenger contacts: {passenger_contacts_deleted[0]} records')
            
            # Clean up orphaned crew lines (crew lines not attached to any trip lines)
            orphaned_crew_lines = CrewLine.objects.filter(trip_lines__isnull=True)
            crew_lines_deleted = orphaned_crew_lines.delete()
            self.stdout.write(f'Deleted orphaned crew lines: {crew_lines_deleted[0]} records')
            
        self.stdout.write(self.style.SUCCESS('Successfully removed test data!'))
```


# File: api/management/commands/seed_aircraft_and_staff.py

```python
from django.core.management.base import BaseCommand
from django.db import transaction, IntegrityError
from django.utils import timezone

from decimal import Decimal
from datetime import datetime
import re

from api.models import (
    Aircraft,
    Contact,
    Staff,
    StaffRole,
    StaffRoleMembership,
)

# -----------------------------
# SOURCE DATA (from your prompt)
# -----------------------------

AIRCRAFT_ROWS = [
    # tail, company, make, model, serial_number, mgtow (lb)
    ("N911KQ", "Secret Squirrel Aerospace LLC", "Kodiak",   "Kodiak 100", "100-0009", "7255"),
    ("N35LJ",  "Worldwide Aircraft Services, Inc.", "Learjet", "35A",       "240",      "18300"),
    ("N36LJ",  "Worldwide Aircraft Services, Inc.", "Learjet", "36A",       "44",       "18300"),
    ("N30LJ",  "Worldwide Aircraft Services, Inc.", "Learjet", "31",        "002",      "18300"),
    ("N60LJ",  "Worldwide Aircraft Services, Inc.", "Learjet", "60",        "52",       "23500"),
    ("N65LJ",  "Worldwide Aircraft Services, Inc.", "Learjet", "60",        "243",      "23500"),
    ("N70LJ",  "Worldwide Aircraft Services, Inc.", "Learjet", "60",        "70",       "23500"),
    ("N80LJ",  "Worldwide Aircraft Services, Inc.", "Learjet", "60",        "305",      "23500"),
    ("N85LJ",  "Worldwide Aircraft Services, Inc.", "Learjet", "60",        "244",      "23500"),
    ("N90LJ",  "Worldwide Aircraft Services, Inc.", "Learjet", "60",        "287",      "23500"),
]

PILOT_ROWS = [
    # Name, Nat., DOB, Passport #, Exp., Contact #, Email
    ("Anthony Guglielmetti","US","11/27/1997","534687611","10/27/2025","813-613-1396","AnthonyGuglielmetti@jeticu.com"),
    ("Christopher McGuire","US","11/26/1985","565155697","02/06/2027","813-468-6889","chris.mcguire@jeticu.com"),
    ("Jason Rowe","US","11/20/1982","583027251","11/08/2027","218-343-2005","jrowe@jeticu.com"),
    ("Kurt Veilleux","US","09/17/1983","A35779864","02/08/2034","813-417-6891","kurt@jeticu.com"),
    ("Michael Honeycutt","US","12/18/1969","A03627887","10/13/2032","727-415-9458","mike@jeticu.com"),
    ("John Cannon II","US","05/06/1998","A61105507","02/24/2035","786-879-9393","john.cannon@jeticu.com"),
    ("Patrick Buttermore","US","12/22/1986","A35779865","02/08/2034","813-951-0961","Patrick.Buttermore@jeticu.com"),
    ("Thomas Lacey","US","08/04/1968","A07991093","12/26/2032","727-510-5189","tom@jeticu.com"),
    ("Steven Peterson","US","04/10/1997","A26963982","07/30/2033","845-520-0244","StevePeterson@jeticu.com"),
    ("Tyler Towle","US","04/28/1997","A36095632","10/20/2034","801-824-2782","TylerTowle@jeticu.com"),
    ("Oleg Baumgart","US","01/12/1981","541154548","12/06/2025","575-571-6363","oleg.baumgart@jeticu.com"),
    ("Gary Kelley","US","09/30/1955","561205578","10/11/2027","727-560-0555","puffin@jeticu.com"),
    ("Jack Al-Hussaini","US","11/06/2002","590363317","12/27/2028","704-818-7600","JackAl-Hussaini@jeticu.com"),
]

MEDIC_ROWS = [
    ("Amy Nicole Nilsen","US","05/31/1993","A35874322","05/21/2034","845-421-0106","AMY.NILSEN31@GMAIL.COM"),
    ("Carlos Smith","US","9/10/1972","645442043","04/15/2029","813-454-7837","emnole1995@gmail.com"),
    ("Christopher Izzi","US","12/31/1990","A06603660","06/13/2032","570-856-2730","deltanu239@gmail.com"),
    ("Jacob Samuel Cruz","US","8/10/1995","559629951","04/03/2027","813-340-9103","jcruzmusic16@icloud.com"),
    ("Devin Mormando","US","9/4/1986","A34987989","12/06/2033","352-573-1380","dmormando@elfr.org"),
    ("Jill Butler","US","5/8/1971","678687790","07/04/2032","813-614-4496","jsbutlerrn@gmail.com"),
    ("Eric Castellucci","US","08/10/1953","512319513","01/25/2024","813-417-3210","trilucci@gmail.com"),
    ("Nicholas Mc Sweeney","US","11/6/1990","542911451","04/03/2026","386-588-4005","nickjb_1106@yahoo.com"),
    ("Gary Hurlbut","US","09/26/1968","A03628812","11/20/2032","727-355-3944","AirHurly@gmail.com"),
    ("Harold John Haverty","US","08/23/1961","583528607","05/19/2028","727-504-0451","havertyjohn@yahoo.com"),
    ("James Byrns","US","07/11/1968","A04083672","10/16/2033","727-518-4441","james.byrns68@gmail.com"),
    ("Jamie Lynn Juliano","US","02/18/1983","554218813","07/19/2026","815-641-4906","jamie.juliano7@gmail.com"),
    ("Jared Wayt","US","02/07/1986","565787394","02/26/2028","813-312-4708","jaredw@jeticu.com"),
    ("Jessica May Mone","US","07/22/1978","598263733","06/12/2029","727-599-5138","mjessy0722@gmail.com"),
    ("John David Mulford","US","08/21/1984","A04704947","02/05/2033","813-833-4663","johnmulford@yahoo.com"),
    ("John P. Opyoke","US","7/30/1969","A20507949","05/30/2033","352-263-6925","trinityurgentcare@yahoo.com"),
    ("Jon Inkrott","US","3/17/1972","599921500","07/17/2029","407-516-5579","jon.inkrott@adventhealth.com"),
    ("Justin Andrews","US","10/24/1984","568082572","10/01/2030","239-233-9799","RFinkle5@me.com"),
    ("Kimberly Recinella","US","4/5/1992","673093739","01/23/2032","513-226-1066","ktrecinella@gmail.com"),
    ("Kristin Howell","US","08/17/1984","587818528","09/17/2028","813-361-3009","kristinvictory@gmail.com"),
    ("Kurt Veilleux","US","09/17/1983","520374483","08/03/2024","813-417-6891","kurt@jeticu.com"),
    ("Mary McCarthy","US","11/06/1955","A03492999","02/15/2032","727-641-0085","mary@jeticu.com"),
    ("Michael Abesada","US","01/07/1979","A23420769","10/25/2033","786-447-7153","abesadam@gmail.com"),
    ("Robert Sullivan","US","12/19/1983","572232934","05/24/2027","352-406-2573","bsullivan403@yahoo.com"),
    ("Anthony Marino","US","03/23/1982","674420053","02/10/2032","772-418-0312","antr0323@gmail.com"),
    ("Jefferson Day","US","09/01/1989","A22153633","06/25/2033","352-585-1068","Jeffy_day@yahoo.com"),
    ("Ronald Figueredo","US","7/31/1976","567221355","06/13/2029","610-952-3430","ronaldfigueredo@gmail.com"),
    ("Ronald Wyant","US","09/28/1963","A04483166","09/27/2033","727-639-5126","swyant1@icloud.com"),
    ("Bruce Loeb Jr.","US","01/27/1971","A10316135","11/06/2032","904-338-6447","bnloeb9@gmail.com"),
    ("Thomas Tropeano","US","2/16/1954","549865068","03/13/2027","352-804-9629","tltropeano@yahoo.com"),
    ("Tiffany Bourne","US","03/15/1973","A04483169","09/27/2033","813-260-0343","bourneid73@gmail.com"),
    ("Carla Lynn Sieber","US","07/27/1991","A49128381","11/13/2034","727-424-6886","carlasieber@msn.com"),
    ("Tyson Elledge","US","08/03/1979","A03502556","03/27/2032","352-442-2819","tysonelledge@aol.com"),
    ("Mario Rocha","US","06/02/1970","641826321","03/10/2029","813-215-3277","mario.r.rocha70@gmail.com"),
    ("Jason A. Berger","US","12/10/1990","643816544","09/16/2029","727-512-2959","jberger9359@gmail.com"),
    ("Courtney Hershey","US","05/12/1979","A15958520","03/04/2033","727-519-4714","hersheycourtney@gmail.com"),
]

# Desired role set per cohort
PILOT_ROLE_CODES = ["PIC", "SIC"]
MEDIC_ROLE_CODES = ["RT", "RN", "PARAMEDIC", "MD"]

# Default human-readable names if roles don't exist
ROLE_NAMES_BY_CODE = {
    "PIC": "Pilot in Command",
    "SIC": "Second in Command",
    "RN": "Registered Nurse",
    "PARAMEDIC": "Paramedic",
    "MD": "Physician",
    "RT": "Respiratory Therapist",
}


# -----------------------------
# HELPERS
# -----------------------------

DATE_PATTERNS = ["%m/%d/%Y", "%m/%d/%y", "%m/%-d/%Y", "%m/%-d/%y"]  # macOS strptime may not support %-d; we'll handle manually.

def parse_date(s):
    if not s:
        return None
    s = s.strip()
    # Normalize single-digit months/days to zero-padded mm/dd/yyyy
    # e.g., 9/4/1986 -> 09/04/1986
    parts = re.split(r"[/-]", s)
    if len(parts) == 3:
        mm, dd, yyyy = parts
        if len(mm) == 1: mm = f"0{mm}"
        if len(dd) == 1: dd = f"0{dd}"
        if len(yyyy) == 2:  # assume 20xx for 2-digit years? safer: 19xx for <=30?
            yyyy = "20" + yyyy if int(yyyy) < 50 else "19" + yyyy
        s = f"{mm}/{dd}/{yyyy}"
    for fmt in ("%m/%d/%Y", "%m/%d/%y"):
        try:
            return datetime.strptime(s, fmt).date()
        except ValueError:
            continue
    return None


def split_name(full_name):
    """
    Split 'First [Middle/Initial/Joint] Last [Suffix]' into first_name, last_name.
    We'll keep everything after the first token as last_name for simplicity,
    but handle common suffixes ("Jr.", "II", "III") gracefully.
    """
    if not full_name:
        return None, None
    parts = full_name.strip().split()
    if len(parts) == 1:
        return parts[0], ""
    # Keep suffix attached to last
    suffixes = {"Jr.", "Jr", "Sr.", "Sr", "II", "III", "IV", "V"}
    first = parts[0]
    last = " ".join(parts[1:])
    # compact "Al-Hussaini" etc. untouched
    # nothing more fancy needed for now
    return first, last


def get_or_create_role(code):
    role = StaffRole.objects.filter(code=code).first()
    if role:
        return role
    # Create with default name if missing
    name = ROLE_NAMES_BY_CODE.get(code, code)
    role = StaffRole.objects.create(code=code, name=name)
    return role


def upsert_contact(name, nationality, dob, passport_no, passport_exp, phone, email):
    first_name, last_name = split_name(name)
    # Try to match by email first; fall back to (name + phone)
    contact = None
    if email:
        contact = Contact.objects.filter(email=email.strip()).first()
    if not contact:
        # Try exact name + phone
        contact = Contact.objects.filter(
            first_name=first_name or "",
            last_name=last_name or "",
            phone=(phone or "").strip() or None,
        ).first()

    dob_dt = parse_date(dob)
    pass_exp_dt = parse_date(passport_exp)

    if contact:
        # Update basics if missing
        dirty = False
        if not contact.first_name and first_name:
            contact.first_name = first_name; dirty = True
        if not contact.last_name and last_name:
            contact.last_name = last_name; dirty = True
        if nationality and (contact.nationality != nationality):
            contact.nationality = nationality; dirty = True
        if email and (contact.email != email):
            contact.email = email; dirty = True
        if phone and (contact.phone != phone):
            contact.phone = phone; dirty = True
        if dob_dt and (contact.date_of_birth != dob_dt):
            contact.date_of_birth = dob_dt; dirty = True
        if passport_no and (contact.passport_number != passport_no):
            contact.passport_number = passport_no; dirty = True
        if pass_exp_dt and (contact.passport_expiration_date != pass_exp_dt):
            contact.passport_expiration_date = pass_exp_dt; dirty = True
        if dirty:
            contact.save()
    else:
        contact = Contact.objects.create(
            first_name=first_name or "",
            last_name=last_name or "",
            nationality=nationality or None,
            date_of_birth=dob_dt,
            passport_number=passport_no or None,
            passport_expiration_date=pass_exp_dt,
            phone=phone or None,
            email=email or None,
        )
    return contact


def ensure_staff_for_contact(contact):
    staff = getattr(contact, "staff", None)
    if staff:
        return staff
    return Staff.objects.create(contact=contact, active=True)


def ensure_memberships(staff, role_codes):
    for code in role_codes:
        role = get_or_create_role(code)
        # Do not create duplicates with same open interval (start_on=None, end_on=None)
        exists = StaffRoleMembership.objects.filter(
            staff=staff, role=role, start_on=None, end_on=None
        ).exists()
        if not exists:
            StaffRoleMembership.objects.create(
                staff=staff, role=role, start_on=None, end_on=None
            )


def d(val):
    """Decimal helper for mgtow."""
    if val is None or str(val).strip() == "":
        return None
    return Decimal(str(val))


# -----------------------------
# COMMAND
# -----------------------------

class Command(BaseCommand):
    help = "Seed Aircraft and Staff (Pilots & Medics) into the database."

    def handle(self, *args, **options):
        created_aircraft = updated_aircraft = 0
        created_contacts = updated_contacts = 0
        created_staff = 0
        created_roles = 0
        created_memberships = 0  # (we won't count precisely per-row here; optional)

        # Ensure baseline roles exist (safe if already present)
        for code in set(PILOT_ROLE_CODES + MEDIC_ROLE_CODES):
            if not StaffRole.objects.filter(code=code).exists():
                StaffRole.objects.create(code=code, name=ROLE_NAMES_BY_CODE.get(code, code))
                created_roles += 1

        # --- Aircraft upsert ---
        for tail, company, make, model, serial, mgtow_lb in AIRCRAFT_ROWS:
            mgtow = d(mgtow_lb)  # store the lb number in Decimal (your field is Decimal)
            obj = Aircraft.objects.filter(tail_number=tail).first()
            if obj:
                dirty = False
                if obj.company != company:
                    obj.company = company; dirty = True
                if obj.make != make:
                    obj.make = make; dirty = True
                if obj.model != model:
                    obj.model = model; dirty = True
                if obj.serial_number != serial:
                    obj.serial_number = serial; dirty = True
                if obj.mgtow != mgtow:
                    obj.mgtow = mgtow; dirty = True
                if dirty:
                    obj.save()
                    updated_aircraft += 1
            else:
                Aircraft.objects.create(
                    tail_number=tail,
                    company=company,
                    make=make,
                    model=model,
                    serial_number=serial,
                    mgtow=mgtow,
                )
                created_aircraft += 1

        # --- Pilots ---
        for (name, nat, dob, passport_no, exp, phone, email) in PILOT_ROWS:
            contact_before = Contact.objects.filter(email=email).first()
            contact = upsert_contact(name, nat, dob, passport_no, exp, phone, email)
            if contact_before is None and contact is not None:
                created_contacts += 1
            elif contact_before is not None:
                # we may have updated fields
                updated_contacts += 0  # keep simple; adjust if you want exact diffs

            staff = ensure_staff_for_contact(contact)
            # Before creating, check how many memberships exist to approximate "created_memberships"
            pre_count = StaffRoleMembership.objects.filter(staff=staff).count()
            ensure_memberships(staff, PILOT_ROLE_CODES)
            post_count = StaffRoleMembership.objects.filter(staff=staff).count()
            created_memberships += max(0, post_count - pre_count)

        # --- Medics ---
        for (name, nat, dob, passport_no, exp, phone, email) in MEDIC_ROWS:
            contact_before = Contact.objects.filter(email=email).first()
            contact = upsert_contact(name, nat, dob, passport_no, exp, phone, email)
            if contact_before is None and contact is not None:
                created_contacts += 1
            else:
                updated_contacts += 0

            staff = ensure_staff_for_contact(contact)
            pre_count = StaffRoleMembership.objects.filter(staff=staff).count()
            ensure_memberships(staff, MEDIC_ROLE_CODES)
            post_count = StaffRoleMembership.objects.filter(staff=staff).count()
            created_memberships += max(0, post_count - pre_count)

        self.stdout.write(self.style.SUCCESS("Seeding complete."))
        self.stdout.write(
            f"Aircraft: created={created_aircraft}, updated={updated_aircraft}\n"
            f"Contacts: created~={created_contacts}\n"
            f"Staff: ensured (created as needed)\n"
            f"Roles: created={created_roles} (only if missing)\n"
            f"Role memberships created~={created_memberships}"
        )

```


# File: api/management/commands/seed_staff.py

```python
# api/management/commands/seed_staff.py
from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone

from api.models import (
    Staff,
    StaffRole,
    StaffRoleMembership,
    Contact,
    CrewLine,
)

ROLE_CODES = [
    ("PIC", "Pilot in Command"),
    ("SIC", "Second in Command"),
    ("RN", "Registered Nurse"),
    ("PARAMEDIC", "Paramedic"),
    ("RT", "Respiratory Therapist"),
    ("MD", "Physician"),
]


class Command(BaseCommand):
    help = (
        "Seeds StaffRole, backfills Staff for Contacts used on CrewLines, "
        "and (optionally) creates basic StaffRoleMemberships for PIC/SIC."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "--with-memberships",
            action="store_true",
            help="Also create StaffRoleMemberships for PIC/SIC based on CrewLine usage.",
        )

    @transaction.atomic
    def handle(self, *args, **opts):
        # Ensure roles exist
        created_roles = 0
        for code, name in ROLE_CODES:
            _, was_created = StaffRole.objects.get_or_create(code=code, defaults={"name": name})
            if was_created:
                created_roles += 1
        self.stdout.write(
            self.style.SUCCESS(
                f"StaffRole ensured (created {created_roles}, total {StaffRole.objects.count()})."
            )
        )

        # Collect all Contact IDs referenced by CrewLine (PIC, SIC, and medics)
        contact_ids = set()

        # PIC / SIC via FK fields (use iterator with chunk_size for memory safety)
        for cl in CrewLine.objects.only(
            "primary_in_command_id", "secondary_in_command_id"
        ).iterator(chunk_size=1000):
            if getattr(cl, "primary_in_command_id_id", None):
                contact_ids.add(cl.primary_in_command_id_id)
            if getattr(cl, "secondary_in_command_id_id", None):
                contact_ids.add(cl.secondary_in_command_id_id)

        # Medics via M2M; when using prefetch_related, don't call iterator() without chunk_size
        for cl in CrewLine.objects.prefetch_related("medic_ids"):
            contact_ids.update(cl.medic_ids.values_list("id", flat=True))

        # Backfill Staff rows for those Contacts
        created_staff = 0
        for cid in contact_ids:
            _, was_created = Staff.objects.get_or_create(contact_id=cid, defaults={"active": True})
            if was_created:
                created_staff += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"Staff ensured for {len(contact_ids)} contact(s) (created {created_staff})."
            )
        )

        # Optionally add PIC/SIC memberships effective today
        if opts.get("with_memberships"):
            today = timezone.now().date()

            roles = {r.code: r for r in StaffRole.objects.filter(code__in=["PIC", "SIC"])}
            pic = roles.get("PIC")
            sic = roles.get("SIC")

            made = 0

            if pic:
                pic_contact_ids = (
                    CrewLine.objects.exclude(primary_in_command_id__isnull=True)
                    .values_list("primary_in_command_id", flat=True)
                    .distinct()
                )
                for cid in pic_contact_ids:
                    staff = Staff.objects.filter(contact_id=cid).first()
                    if staff and not StaffRoleMembership.objects.filter(
                        staff=staff, role=pic, start_on=today, end_on=None
                    ).exists():
                        StaffRoleMembership.objects.create(
                            staff=staff, role=pic, start_on=today, end_on=None
                        )
                        made += 1

            if sic:
                sic_contact_ids = (
                    CrewLine.objects.exclude(secondary_in_command_id__isnull=True)
                    .values_list("secondary_in_command_id", flat=True)
                    .distinct()
                )
                for cid in sic_contact_ids:
                    staff = Staff.objects.filter(contact_id=cid).first()
                    if staff and not StaffRoleMembership.objects.filter(
                        staff=staff, role=sic, start_on=today, end_on=None
                    ).exists():
                        StaffRoleMembership.objects.create(
                            staff=staff, role=sic, start_on=today, end_on=None
                        )
                        made += 1

            self.stdout.write(self.style.SUCCESS(f"PIC/SIC memberships created today: {made}"))
        else:
            self.stdout.write(
                self.style.WARNING("Skipped memberships (run with --with-memberships to add PIC/SIC).")
            )

```


# File: api/management/commands/import_airports.py

```python
import csv
from decimal import Decimal, InvalidOperation
from pathlib import Path

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction, IntegrityError

from api.models import Airport, AirportType  # adjust import path if needed

# Optional timezone lookup
try:
    from timezonefinder import TimezoneFinder
    TF = TimezoneFinder()
except Exception:
    TF = None


def to_decimal(val, places=6):
    if val is None:
        return None
    s = str(val).strip()
    if not s or s.lower() == "null":
        return None
    try:
        d = Decimal(s)
        return d.quantize(Decimal("0." + "0" * places))
    except (InvalidOperation, ValueError):
        return None


def to_int(val):
    if val is None:
        return None
    s = str(val).strip()
    if not s or s.lower() == "null":
        return None
    try:
        return int(Decimal(s))
    except (InvalidOperation, ValueError):
        return None


def norm_str(val):
    if val is None:
        return None
    s = str(val).strip()
    return s or None


TYPE_MAP = {
    "large_airport": getattr(AirportType, "LARGE", "large_airport"),
    "medium_airport": getattr(AirportType, "MEDIUM", "medium_airport"),
    "small_airport": getattr(AirportType, "SMALL", "small_airport"),
    "heliport": getattr(AirportType, "SMALL", "small_airport"),
    "seaplane_base": getattr(AirportType, "SMALL", "small_airport"),
    "closed": getattr(AirportType, "SMALL", "small_airport"),
}


def infer_timezone(lat, lon):
    if lat is None or lon is None:
        return "UTC"
    if TF is None:
        return "UTC"
    try:
        tz = TF.timezone_at(lat=float(lat), lng=float(lon))
        return tz or "UTC"
    except Exception:
        return "UTC"


def flush_buffer(buffer, batch_size):
    """Try bulk_create, then fallback to row-by-row on conflicts."""
    created = 0
    skipped = 0
    if not buffer:
        return 0, 0

    try:
        with transaction.atomic():
            Airport.objects.bulk_create(
                buffer, ignore_conflicts=True, batch_size=batch_size
            )
            created += len(buffer)
        return created, skipped
    except IntegrityError:
        pass  # fallback row by row

    for inst in buffer:
        try:
            with transaction.atomic():
                inst.save()
                created += 1
        except IntegrityError:
            skipped += 1
    return created, skipped


class Command(BaseCommand):
    help = "Import airports from a CSV with columns like OurAirports."

    def add_arguments(self, parser):
        parser.add_argument("csv_path", type=str, help="Path to airports.csv")
        parser.add_argument(
            "--update",
            action="store_true",
            help="Update existing airports matched by ident.",
        )
        parser.add_argument(
            "--batch",
            type=int,
            default=1000,
            help="Bulk create batch size.",
        )

    def handle(self, *args, **opts):
        csv_path = Path(opts["csv_path"])
        if not csv_path.exists():
            raise CommandError(f"CSV not found: {csv_path}")

        update_existing = opts["update"]
        batch_size = opts["batch"]

        created = updated = skipped = 0
        buffer = []

        # preload existing idents for quick lookup
        existing_idents = set(
            Airport.objects.values_list("ident", flat=True)
        )

        with csv_path.open(newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)

            for row in reader:
                ident = norm_str(row.get("ident"))
                if not ident:
                    skipped += 1
                    continue

                name = norm_str(row.get("name")) or ident
                lat = to_decimal(row.get("latitude_deg"))
                lon = to_decimal(row.get("longitude_deg"))
                elevation = to_int(row.get("elevation_ft"))

                iso_country = norm_str(row.get("iso_country")) or "US"
                iso_region = norm_str(row.get("iso_region"))
                municipality = norm_str(row.get("municipality"))

                icao_code = norm_str(row.get("icao_code"))
                iata_code = norm_str(row.get("iata_code"))
                gps_code = norm_str(row.get("gps_code"))
                local_code = norm_str(row.get("local_code"))

                csv_type = (norm_str(row.get("type")) or "").lower()
                airport_type = TYPE_MAP.get(
                    csv_type, getattr(AirportType, "SMALL", "small_airport")
                )

                tz = infer_timezone(lat, lon)

                defaults = dict(
                    name=name,
                    latitude=lat,
                    longitude=lon,
                    elevation=elevation,
                    iso_country=iso_country,
                    iso_region=iso_region,
                    municipality=municipality,
                    icao_code=icao_code,
                    iata_code=iata_code,
                    local_code=local_code,
                    gps_code=gps_code,
                    airport_type=airport_type,
                    timezone=tz,
                )

                if ident in existing_idents:
                    if update_existing:
                        try:
                            Airport.objects.filter(ident=ident).update(**defaults)
                            updated += 1
                        except IntegrityError:
                            skipped += 1
                    continue
                else:
                    buffer.append(Airport(ident=ident, **defaults))
                    if len(buffer) >= batch_size:
                        c, s = flush_buffer(buffer, batch_size)
                        created += c
                        skipped += s
                        buffer = []

        # flush leftover
        if buffer:
            c, s = flush_buffer(buffer, batch_size)
            created += c
            skipped += s

        self.stdout.write(
            self.style.SUCCESS(
                f"Import complete: created={created}, updated={updated}, skipped={skipped}"
            )
        )

```


# File: documents/templates/docs.py

```python
import pypdf
from pypdf import PdfWriter, PdfReader
import PyPDF2
from typing import Dict, Any, Optional, List
from datetime import datetime
from dataclasses import dataclass, field


# Data Classes for PDF Population

@dataclass
class QuoteData:
    """Data class for Quote PDF fields - matches actual PDF field names"""
    quote_id: str = ''
    inquiry_date: str = ''
    patient_name: str = ''
    aircraft_type: str = ''
    pickup_airport: str = ''
    dropoff_airport: str = ''
    trip_date: str = ''
    esitmated_flight_time: str = ''
    number_of_stops: str = ''
    medical_team: str = ''
    include_grounds: str = ''
    our_availability: str = ''
    amount: str = ''
    notes: str = ''


@dataclass
class PassengerInfo:
    """Passenger information for handling requests"""
    name: str = ""
    title: str = ""
    nationality: str = ""
    date_of_birth: str = ""
    passport_number: str = ""
    passport_expiration: str = ""
    contact_number: str = ""


@dataclass
class HandlingRequestData:
    """Data class for Handling Request PDF fields - matches actual PDF field names"""
    company: str = ''
    make: str = ''
    model: str = ''
    tail_number: str = ''
    serial_number: str = ''
    mgtow: str = ''
    mission: str = ''
    depart_origin: str = ''
    arrive_dest: str = ''
    depart_dest: str = ''
    arrive_origin: str = ''
    passengers: List[PassengerInfo] = field(default_factory=list)


@dataclass
class CrewInfo:
    """Crew information for itinerary"""
    pic: str = ""  # Pilot in Command
    sic: str = ""  # Second in Command
    med_1: str = ""  # Medical crew member 1
    med_2: str = ""  # Medical crew member 2
    med_4: str = ""  # Medical crew member 4


@dataclass
class FlightLeg:
    """Flight leg information"""
    leg: str = ""
    departure_id: str = ""
    edt_utc_local: str = ""
    arrival_id: str = ""
    flight_time: str = ""
    eta_utc_local: str = ""
    ground_time: str = ""
    pax_leg: str = ""


@dataclass
class AirportInfo:
    """Airport information"""
    icao: str = ""
    airport_city_name: str = ""
    state_country: str = ""
    time_zone: str = ""
    fbo_handler: str = ""
    freq: str = ""
    phone_fax: str = ""
    fuel: str = ""


@dataclass
class TimeInfo:
    """Time information for itinerary"""
    showtime: str = ""
    origin_edt: str = ""
    total_flight_time: str = ""
    total_duty_time: str = ""
    pre_flight_duty_time: str = ""
    post_flight_duty_time: str = ""


@dataclass
class ItineraryData:
    """Data class for Itinerary PDF fields"""
    trip_number: str = ""
    tail_number: str = ""
    trip_date: str = ""
    trip_type: str = ""
    patient_name: str = ""
    bed_at_origin: bool = False  # Boolean field - will be converted to Yes/No
    bed_at_dest: bool = False    # Boolean field - will be converted to Yes/No
    special_instructions: str = ""
    passengers: List[str] = field(default_factory=list)  # List of passenger names
    crew: CrewInfo = field(default_factory=CrewInfo)
    flight_legs: List[FlightLeg] = field(default_factory=list)
    airports: List[AirportInfo] = field(default_factory=list)
    times: TimeInfo = field(default_factory=TimeInfo)
    apis: str = ""
    apis_2: str = ""
    gen_dec: str = ""
    gen_dec_2: str = ""


def populate_pdf_with_fields(input_pdf_path: str, output_pdf_path: str, field_mapping: Dict[str, str]) -> bool:
    """
    Generic function to populate PDF form fields using pdfrw.
    
    Args:
        input_pdf_path: Path to the input PDF template
        output_pdf_path: Path where the filled PDF will be saved
        field_mapping: Dictionary mapping field names to values
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        from pdfrw import PdfReader, PdfWriter, PdfDict, PdfName
        
        # Read the PDF
        template_pdf = PdfReader(input_pdf_path)
        
        # Clean field mapping - ensure all values are strings
        clean_mapping = {}
        for field_name, value in field_mapping.items():
            if value is not None:
                clean_mapping[field_name] = str(value)
            else:
                clean_mapping[field_name] = ""
        
        # Find and populate form fields
        for page in template_pdf.pages:
            if page.Annots:
                for annotation in page.Annots:
                    if annotation.T:  # Field name
                        field_name = annotation.T[1:-1]  # Remove parentheses
                        if field_name in clean_mapping:
                            # Set the field value
                            annotation.update(PdfDict(V=clean_mapping[field_name]))
                            # Also set appearance value
                            annotation.update(PdfDict(AP=''))
        
        # Write the filled PDF
        PdfWriter(output_pdf_path, trailer=template_pdf).write()
        return True
        
    except Exception as e:
        print(f"pdfrw failed: {e}")
        # Fallback to pypdf
        try:
            from pypdf import PdfReader, PdfWriter
            
            reader = PdfReader(input_pdf_path)
            writer = PdfWriter()
            
            # Copy pages
            for page in reader.pages:
                writer.add_page(page)
            
            # Clean field mapping
            clean_mapping = {}
            for field_name, value in field_mapping.items():
                if value is not None:
                    clean_mapping[field_name] = str(value)
                else:
                    clean_mapping[field_name] = ""
            
            # Update form fields
            writer.update_page_form_field_values(writer.pages[0], clean_mapping)
            
            # Write output
            with open(output_pdf_path, 'wb') as output_file:
                writer.write(output_file)
                
            return True
            
        except Exception as e2:
            print(f"All methods failed: {e2}")
            return False


def populate_quote_pdf(input_pdf_path: str, output_pdf_path: str, data: QuoteData) -> bool:
    """Populate Quote.pdf with data from QuoteData instance"""
    # Map data to actual PDF field names from Quote.pdf
    field_mapping = {
        'quote_id': data.quote_id,
        'inquiry_date': data.inquiry_date,
        'patient_name': data.patient_name,
        'aircraft_type': data.aircraft_type,
        'pickup_airport': data.pickup_airport,
        'dropoff_airport': data.dropoff_airport,
        'trip_date': data.trip_date,
        'esitmated_flight_time': data.esitmated_flight_time,
        'number_of_stops': data.number_of_stops,
        'medical_team': data.medical_team,
        'include_grounds': data.include_grounds,
        'our_availability': data.our_availability,
        'amount': data.amount,
        'notes': data.notes
    }
    
    return populate_pdf_with_fields(input_pdf_path, output_pdf_path, field_mapping)


def populate_handling_request_pdf(input_pdf_path: str, output_pdf_path: str, data: HandlingRequestData) -> bool:
    """Populate handling_request.pdf with data from HandlingRequestData instance"""
    # Map data to actual PDF field names from handling_request.pdf
    # Note: depart/arrive fields should contain TIMES not ICAO codes
    field_mapping = {
        'company': data.company,
        'make': data.make,
        'model': data.model,
        'tail_number': data.tail_number,
        'serial_number': data.serial_number,
        'mgtow': data.mgtow,
        'mission': data.mission,
        'depart_origin': data.depart_origin,  # Should be departure TIME from origin
        'arrive_dest': data.arrive_dest,      # Should be arrival TIME at destination
        'depart_dest': data.depart_dest,      # Should be departure TIME from destination (return leg)
        'arrive_origin': data.arrive_origin   # Should be arrival TIME back at origin (return leg)
    }
    
    # Add passenger information (up to 8 passengers)
    for i in range(1, 9):
        if i <= len(data.passengers):
            passenger = data.passengers[i-1]
            field_mapping.update({
                f'r{i}_name': passenger.name,
                f'r{i}_title': passenger.title,
                f'r{i}_nationality': passenger.nationality,
                f'r{i}_date_of_birth': passenger.date_of_birth,
                f'r{i}_passport_number': passenger.passport_number,
                f'r{i}_passport_expiration': passenger.passport_expiration,
                f'r{i}_contact_number': passenger.contact_number
            })
        else:
            # Fill empty fields for unused passenger slots
            field_mapping.update({
                f'r{i}_name': '',
                f'r{i}_title': '',
                f'r{i}_nationality': '',
                f'r{i}_date_of_birth': '',
                f'r{i}_passport_number': '',
                f'r{i}_passport_expiration': '',
                f'r{i}_contact_number': ''
            })
    
    return populate_pdf_with_fields(input_pdf_path, output_pdf_path, field_mapping)


def populate_itinerary_pdf(input_pdf_path: str, output_pdf_path: str, data: ItineraryData) -> bool:
    """Populate itin.pdf with data from ItineraryData instance"""
    # Map data to actual PDF field names from itin.pdf
    # NOTE: trip_number, tail_number, trip_date, trip_type fields do NOT exist in this PDF template
    field_mapping = {
        'patient_name': data.patient_name,
        'bed_at_origin': 'Yes' if data.bed_at_origin else 'No',
        'bed_at_dest': 'Yes' if data.bed_at_dest else 'No',
        'special_instructions': data.special_instructions,
    }
    
    # Add passenger information (up to 5 passengers)
    for i in range(1, 6):
        if i <= len(data.passengers):
            field_mapping[f'pax_{i}'] = data.passengers[i-1]
        else:
            field_mapping[f'pax_{i}'] = ''
    
    # Add crew information
    field_mapping.update({
        'pic': data.crew.pic,
        'sic': data.crew.sic,
        'med_1': data.crew.med_1,
        'med_2': data.crew.med_2
    })
    
    # Add flight legs (up to 10 legs)
    for i in range(1, 11):
        if i <= len(data.flight_legs):
            leg = data.flight_legs[i-1]
            field_mapping.update({
                f'LegRow{i}': leg.leg,
                f'Departure IDRow{i}': leg.departure_id,
                f'EDT UTCLOCALRow{i}': leg.edt_utc_local,
                f'Arrival IDRow{i}': leg.arrival_id,
                f'Flight TimeRow{i}': leg.flight_time,
                f'ETA UTCLOCALRow{i}': leg.eta_utc_local,
                f'Ground TimeRow{i}': leg.ground_time,
                f'PAX LegRow{i}': leg.pax_leg
            })
        else:
            # Fill empty fields for unused leg slots
            field_mapping.update({
                f'LegRow{i}': '',
                f'Departure IDRow{i}': '',
                f'EDT UTCLOCALRow{i}': '',
                f'Arrival IDRow{i}': '',
                f'Flight TimeRow{i}': '',
                f'ETA UTCLOCALRow{i}': '',
                f'Ground TimeRow{i}': '',
                f'PAX LegRow{i}': ''
            })
    
    # Add airport information (up to 11 airports)
    for i in range(1, 12):
        if i <= len(data.airports):
            airport = data.airports[i-1]
            field_mapping.update({
                f'ICAORow{i}': airport.icao,
                f'Airport City NameRow{i}': airport.airport_city_name,
                f'State CountryRow{i}': airport.state_country,
                f'Time ZoneRow{i}': airport.time_zone,
                f'FBOHandlerRow{i}': airport.fbo_handler,
                f'FreqRow{i}': airport.freq,
                f'Phone FaxRow{i}': airport.phone_fax,
                f'Fuel  Row{i}': airport.fuel  # Note the extra space in "Fuel  Row"
            })
        else:
            # Fill empty fields for unused airport slots
            field_mapping.update({
                f'ICAORow{i}': '',
                f'Airport City NameRow{i}': '',
                f'State CountryRow{i}': '',
                f'Time ZoneRow{i}': '',
                f'FBOHandlerRow{i}': '',
                f'FreqRow{i}': '',
                f'Phone FaxRow{i}': '',
                f'Fuel  Row{i}': ''  # Note the extra space in "Fuel  Row"
            })
    
    # Add timing information
    field_mapping.update({
        'showtime': data.times.showtime,
        'origin_edt': data.times.origin_edt,
        'total_filght_time': data.times.total_flight_time,  # Note: PDF has typo "filght"
        'total_duty_time': data.times.total_duty_time,
        'pre_flight_duty_time': data.times.pre_flight_duty_time,
        'post_flight_duty_time': data.times.post_flight_duty_time
    })
        
    return populate_pdf_with_fields(input_pdf_path, output_pdf_path, field_mapping)


# Example usage functions
def example_populate_quote():
    """Example of how to use the populate_quote_pdf function"""
    sample_data = QuoteData(
        quote_id='Q-2024-001',
        inquiry_date='2024-01-15',
        patient_name='John Smith',
        aircraft_type='Citation CJ3',
        pickup_airport='KJFK',
        dropoff_airport='KLAX',
        trip_date='2024-02-01',
        esitmated_flight_time='5:30',
        number_of_stops='0',
        medical_team='Dr. Johnson, Nurse Williams',
        include_grounds='Yes',
        our_availability='Available',
        amount='$24,255',
        notes='Medical transport with specialized equipment'
    )
    
    return populate_quote_pdf('Quote.pdf', 'Quote_filled.pdf', sample_data)


```


# File: backend/settings.py

```python
"""
Django settings for backend project.

Generated by 'django-admin startproject' using Django 5.2.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.2/ref/settings/
"""

from pathlib import Path
from datetime import timedelta
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-6r7f((os!(^y(1j7tti@m5-fm-rx*rdb5%nxo4wfu1)0&h8@*u'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'corsheaders',
    'api',
    'transactions',
    'rest_framework_simplejwt',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'api.middleware.CurrentUserMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'backend.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'backend.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ.get("POSTGRES_DB", "airmed"),
        "USER": os.environ.get("POSTGRES_USER", "airmed"),
        "PASSWORD": os.environ.get("POSTGRES_PASSWORD", "airmedpass"),
        # If Django is running on your Mac (outside Docker), use localhost:
        "HOST": os.environ.get("POSTGRES_HOST", "127.0.0.1"),
        "PORT": os.environ.get("POSTGRES_PORT", "5432"),
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/

STATIC_URL = 'static/'

# CORS settings
CORS_ALLOW_ALL_ORIGINS = True  # For development only, restrict in production
CORS_ALLOW_CREDENTIALS = True

# CSRF settings
CSRF_TRUSTED_ORIGINS = [
    'http://localhost:5173',
    'http://localhost:5174',
    'http://127.0.0.1:5173',
    'http://127.0.0.1:5174',
    'https://localhost:5173',
    'https://localhost:5174',
    'https://localhost:5175',
    'https://localhost:5176',
    'https://localhost:5177',
    'https://localhost:5178',
    'https://127.0.0.1:5173',
    'https://127.0.0.1:5174',
    'https://127.0.0.1:5175',
    'https://127.0.0.1:5176',
    'https://127.0.0.1:5177',
    'https://127.0.0.1:5178',
]

# REST Framework settings
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10
}

# JWT settings
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(hours=1),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
}

# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# DocuSeal Integration Settings
DOCUSEAL_API_KEY = os.environ.get('DOCUSEAL_API_KEY', 'iMDk8MquWy9jnnMudnde52Efzfe8HKjx9BdCL4BzePT')
DOCUSEAL_BASE_URL = os.environ.get('DOCUSEAL_BASE_URL', 'https://api.docuseal.com')
DOCUSEAL_WEBHOOK_SECRET = os.environ.get('DOCUSEAL_WEBHOOK_SECRET', None)
DOCUSEAL_JET_ICU_SIGNER_EMAIL = os.environ.get('DOCUSEAL_JET_ICU_SIGNER_EMAIL', 'contracts@jeticu.com')

# Authorize.Net Integration Settings
AUTHORIZE_NET_LOGIN_ID = os.environ.get('AUTHORIZE_NET_LOGIN_ID')
AUTHORIZE_NET_TRANSACTION_KEY = os.environ.get('AUTHORIZE_NET_TRANSACTION_KEY')

# DocuSeal Contract Settings
DOCUSEAL_CONTRACT_SETTINGS = {
    'default_expiration_days': 30,
    'send_email_notifications': True,
    'auto_generate_on_trip_creation': True,
    'templates': {
        'consent_transport': {
            'template_id': '1712631',
            'name': 'Consent for Transport',
            'requires_jet_icu_signature': True,  # JET ICU needs to be involved for field data
            'customer_role': 'patient',       # Customer signs as patient
            'jet_icu_role': 'jet_icu',        # JET ICU gets the field data
        },
        'payment_agreement': {
            'template_id': '1712677',
            'name': 'Air Ambulance Payment Agreement',
            'requires_jet_icu_signature': True,
            'customer_role': 'customer',      # Customer signs as customer
            'jet_icu_role': 'jet_icu',        # JET ICU signs as jet_icu (gets the field data)
        },
        'patient_service_agreement': {
            'template_id': '1712724',
            'name': 'Patient Service Agreement',
            'requires_jet_icu_signature': True,
            'customer_role': 'patient',       # Customer signs as patient
            'jet_icu_role': 'jet_icu',        # JET ICU signs as jet_icu (gets the field data)
        }
    }
}

```


# File: backend/urls.py

```python
"""
URL configuration for backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

# Swagger documentation setup
schema_view = get_schema_view(
   openapi.Info(
      title="JET ICU Operations API",
      default_version='v1',
      description="API for JET ICU Operations management system",
      contact=openapi.Contact(email="support@jeticu.com"),
      license=openapi.License(name="Proprietary"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    path('api/transactions/', include('transactions.urls')),
    
    # JWT Authentication
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    
    # API Documentation
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

```


# File: backend/__init__.py

```python

```


# File: backend/asgi.py

```python
"""
ASGI config for backend project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')

application = get_asgi_application()

```


# File: backend/wsgi.py

```python
"""
WSGI config for backend project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')

application = get_wsgi_application()

```


# File: maintenance/admin.py

```python
from django.contrib import admin
from .models import Aircraft, MaintenanceLog

admin.site.register(Aircraft)
admin.site.register(MaintenanceLog)

```


# File: maintenance/urls.py

```python
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AircraftViewSet, MaintenanceLogViewSet

router = DefaultRouter()
router.register(r'aircraft', AircraftViewSet)
router.register(r'logs', MaintenanceLogViewSet)

urlpatterns = [
    path('', include(router.urls)),
]

```


# File: maintenance/views.py

```python
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Aircraft, MaintenanceLog
from .serializers import AircraftSerializer, MaintenanceLogSerializer, AircraftStatusUpdateSerializer


class AircraftViewSet(viewsets.ModelViewSet):
    queryset = Aircraft.objects.all()
    serializer_class = AircraftSerializer
    
    @action(detail=True, methods=['patch'])
    def update_status(self, request, pk=None):
        aircraft = self.get_object()
        serializer = AircraftStatusUpdateSerializer(aircraft, data=request.data, partial=True)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MaintenanceLogViewSet(viewsets.ModelViewSet):
    queryset = MaintenanceLog.objects.all()
    serializer_class = MaintenanceLogSerializer
    
    def get_queryset(self):
        queryset = MaintenanceLog.objects.all()
        aircraft_id = self.request.query_params.get('aircraft_id')
        
        if aircraft_id:
            queryset = queryset.filter(aircraft_id=aircraft_id)
        
        return queryset

```


# File: maintenance/models.py

```python
from django.db import models


class Aircraft(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('maintenance', 'In Maintenance'),
        ('grounded', 'Grounded'),
    ]
    
    registration = models.CharField(max_length=20, unique=True)
    aircraft_type = models.CharField(max_length=100)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    last_maintenance_date = models.DateField(null=True, blank=True)
    next_maintenance_date = models.DateField(null=True, blank=True)
    total_flight_hours = models.FloatField(default=0)
    manufacturing_date = models.DateField(null=True, blank=True)
    capacity = models.IntegerField(default=0)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.registration} - {self.aircraft_type}"


class MaintenanceLog(models.Model):
    aircraft = models.ForeignKey(Aircraft, on_delete=models.CASCADE, related_name='maintenance_logs')
    maintenance_date = models.DateField()
    description = models.TextField()
    performed_by = models.CharField(max_length=100)
    hours_spent = models.FloatField(default=0)
    parts_replaced = models.TextField(blank=True)
    is_scheduled = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.aircraft.registration} - {self.maintenance_date}"

```


# File: maintenance/__init__.py

```python


```


# File: maintenance/apps.py

```python
from django.apps import AppConfig


class MaintenanceConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'maintenance'

```


# File: maintenance/serializers.py

```python
from rest_framework import serializers
from .models import Aircraft, MaintenanceLog


class MaintenanceLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = MaintenanceLog
        fields = '__all__'


class AircraftSerializer(serializers.ModelSerializer):
    maintenance_logs = MaintenanceLogSerializer(many=True, read_only=True)
    
    class Meta:
        model = Aircraft
        fields = '__all__'


class AircraftStatusUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Aircraft
        fields = ['status', 'notes']

```
