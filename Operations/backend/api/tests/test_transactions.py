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
