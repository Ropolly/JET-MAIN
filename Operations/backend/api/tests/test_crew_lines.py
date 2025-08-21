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
