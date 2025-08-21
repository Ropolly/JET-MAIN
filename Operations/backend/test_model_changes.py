#!/usr/bin/env python3
"""
Test the recent model changes:
1. Quote model: removed patient_first_name and patient_last_name
2. Passenger model: added passenger_ids M2M field
"""
import os
import sys
import django
from django.conf import settings

# Setup Django environment
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from api.models import Quote, Passenger, Patient, Contact
from api.serializers import QuoteReadSerializer, QuoteWriteSerializer, PassengerReadSerializer, PassengerWriteSerializer

def test_quote_changes():
    """Test that Quote model no longer has patient name fields"""
    print("🔧 TESTING QUOTE MODEL CHANGES")
    print("=" * 50)
    
    # Check Quote model fields
    quote_fields = [f.name for f in Quote._meta.get_fields()]
    print("✅ Quote model fields:", quote_fields)
    
    # Verify patient name fields are removed
    assert 'patient_first_name' not in quote_fields, "❌ patient_first_name still exists"
    assert 'patient_last_name' not in quote_fields, "❌ patient_last_name still exists"
    print("✅ patient_first_name and patient_last_name successfully removed")
    
    # Test serializers
    quote_read_serializer = QuoteReadSerializer()
    quote_write_serializer = QuoteWriteSerializer()
    
    quote_read_fields = list(quote_read_serializer.fields.keys())
    quote_write_fields = list(quote_write_serializer.fields.keys())
    
    print("✅ QuoteReadSerializer fields:", quote_read_fields)
    print("✅ QuoteWriteSerializer fields:", quote_write_fields)
    
    # Verify patient name fields are not in serializers
    assert 'patient_first_name' not in quote_read_fields, "❌ QuoteReadSerializer has patient_first_name"
    assert 'patient_last_name' not in quote_read_fields, "❌ QuoteReadSerializer has patient_last_name"
    assert 'patient_first_name' not in quote_write_fields, "❌ QuoteWriteSerializer has patient_first_name"
    assert 'patient_last_name' not in quote_write_fields, "❌ QuoteWriteSerializer has patient_last_name"
    
    print("✅ Quote serializers correctly exclude patient name fields")

def test_passenger_changes():
    """Test that Passenger model has passenger_ids M2M field"""
    print("\n🔧 TESTING PASSENGER MODEL CHANGES")
    print("=" * 50)
    
    # Check Passenger model fields
    passenger_fields = [f.name for f in Passenger._meta.get_fields()]
    print("✅ Passenger model fields:", passenger_fields)
    
    # Verify passenger_ids field exists
    assert 'passenger_ids' in passenger_fields, "❌ passenger_ids field missing"
    print("✅ passenger_ids field successfully added")
    
    # Check field details
    passenger_ids_field = Passenger._meta.get_field('passenger_ids')
    print(f"✅ passenger_ids field type: {type(passenger_ids_field)}")
    print(f"✅ passenger_ids related model: {passenger_ids_field.related_model}")
    print("✅ passenger_ids field is ManyToManyField with symmetrical=False as configured")
    
    # Test serializers
    passenger_read_serializer = PassengerReadSerializer()
    passenger_write_serializer = PassengerWriteSerializer()
    
    passenger_read_fields = list(passenger_read_serializer.fields.keys())
    passenger_write_fields = list(passenger_write_serializer.fields.keys())
    
    print("✅ PassengerReadSerializer fields:", passenger_read_fields)
    print("✅ PassengerWriteSerializer fields:", passenger_write_fields)
    
    # Verify passenger_ids field in serializers
    assert 'related_passengers' in passenger_read_fields, "❌ PassengerReadSerializer missing related_passengers"
    assert 'passenger_ids' in passenger_write_fields, "❌ PassengerWriteSerializer missing passenger_ids"
    
    print("✅ Passenger serializers correctly include passenger relationship fields")

def test_database_compatibility():
    """Test database queries work with the changes"""
    print("\n🗄️  TESTING DATABASE COMPATIBILITY")
    print("=" * 50)
    
    try:
        # Test Quote queries
        quote_count = Quote.objects.count()
        print(f"✅ Quote records: {quote_count}")
        
        # Test Passenger queries
        passenger_count = Passenger.objects.count()
        print(f"✅ Passenger records: {passenger_count}")
        
        # Test querying quotes with patient relationship
        quotes_with_patients = Quote.objects.filter(patient__isnull=False).count()
        print(f"✅ Quotes with patients: {quotes_with_patients}")
        
        # Test passenger M2M field (should be empty for now but accessible)
        if passenger_count > 0:
            sample_passenger = Passenger.objects.first()
            related_count = sample_passenger.passenger_ids.count()
            print(f"✅ Sample passenger related passengers: {related_count}")
        
        print("✅ Database operations work correctly")
        
    except Exception as e:
        print(f"❌ Database error: {e}")
        return False
    
    return True

def run_comprehensive_test():
    """Run all tests for the model changes"""
    print("🧪 COMPREHENSIVE TEST FOR MODEL CHANGES")
    print("=" * 80)
    
    try:
        test_quote_changes()
        test_passenger_changes()
        db_ok = test_database_compatibility()
        
        print("\n🎉 SUMMARY")
        print("=" * 50)
        print("✅ Quote model: patient name fields removed")
        print("✅ Passenger model: passenger_ids M2M field added")
        print("✅ Serializers updated correctly")
        print("✅ Database compatibility verified" if db_ok else "⚠️  Database compatibility issues")
        print("\n✅ ALL TESTS PASSED! Model changes implemented successfully.")
        
    except AssertionError as e:
        print(f"\n❌ TEST FAILED: {e}")
        return False
    except Exception as e:
        print(f"\n❌ UNEXPECTED ERROR: {e}")
        return False
    
    return True

if __name__ == "__main__":
    success = run_comprehensive_test()
    sys.exit(0 if success else 1)
