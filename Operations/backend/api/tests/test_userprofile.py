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
