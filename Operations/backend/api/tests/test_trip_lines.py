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
