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
