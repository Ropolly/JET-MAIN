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
