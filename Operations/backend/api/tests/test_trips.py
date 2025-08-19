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
        "quote_id": 1,  # Expects Quote ID only
        "patient_id": 1,  # Expects Patient ID only
        "aircraft_id": 1,  # Expects Aircraft ID only
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
            "quote_id": 1,
            "patient_id": 1,
            "aircraft_id": 1,
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
