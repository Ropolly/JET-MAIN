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
