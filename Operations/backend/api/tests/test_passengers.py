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
