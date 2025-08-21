#!/usr/bin/env python3
"""
Test Document endpoints (/api/documents/)
Run this against a live server to test the standardized CRUD endpoints.
"""
import sys
import os
import base64
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from base_test import APITester


def test_document_endpoints():
    """Test Document CRUD endpoints."""
    tester = APITester()
    
    print("🧪 TESTING DOCUMENT ENDPOINTS")
    print("=" * 80)
    
    # Test authentication
    print("Attempting authentication...")
    if not tester.authenticate("admin", "admin"):
        print("⚠️  Authentication failed, continuing without auth...")
    
    # Test 1: List documents (GET /api/documents/)
    print("\n📋 TEST 1: List Documents")
    response = tester.test_endpoint(
        "/api/documents/",
        method="GET",
        title="List Documents"
    )
    
    # Test 2: Get specific document (if we have data)
    document_id = None
    if response and response.status_code == 200:
        try:
            data = response.json()
            results = data.get('results', [])
            if results:
                document_id = results[0].get('id')
                print(f"\n🔍 TEST 2: Get Specific Document (ID: {document_id})")
                detail_response = tester.test_endpoint(
                    f"/api/documents/{document_id}/",
                    method="GET",
                    title=f"Get Document {document_id}"
                )
                
                # Check for enhanced fields in read serializer
                if detail_response and detail_response.status_code == 200:
                    try:
                        doc_data = detail_response.json()
                        enhanced_fields = ['content_type', 'download_url']
                        found_fields = [field for field in enhanced_fields if field in doc_data]
                        missing_fields = [field for field in enhanced_fields if field not in doc_data]
                        
                        if found_fields:
                            print(f"✅ Enhanced fields found: {found_fields}")
                        if missing_fields:
                            print(f"⚠️  Enhanced fields missing: {missing_fields}")
                    except:
                        pass
                
                # Test download endpoint
                print(f"\n⬇️  TEST 2b: Download Document (ID: {document_id})")
                tester.test_endpoint(
                    f"/api/documents/{document_id}/download/",
                    method="GET",
                    title=f"Download Document {document_id}"
                )
        except:
            print("\n⚠️  Could not extract document ID for detail test")
    
    # Test 3: Upload new document (POST /api/documents/)
    print("\n📤 TEST 3: Upload Document")
    
    # Create sample file content
    sample_content = b"This is a test document content for API testing."
    encoded_content = base64.b64encode(sample_content).decode('utf-8')
    
    upload_data = {
        "filename": "test_upload.txt",
        "flag": "contract",
        "content": encoded_content,  # Base64 encoded content
        "description": "Test document upload via API"
    }
    
    response = tester.test_endpoint(
        "/api/documents/",
        method="POST",
        data=upload_data,
        expect_status=201,
        title="Upload Document"
    )
    
    # Get the uploaded document ID for further tests
    uploaded_document_id = None
    if response and response.status_code == 201:
        try:
            uploaded_data = response.json()
            uploaded_document_id = uploaded_data.get('id')
        except:
            pass
    
    # Test 4: Try alternative upload format
    print("\n📤 TEST 4: Upload Document (Alternative Format)")
    upload_data_alt = {
        "filename": "test_upload_2.pdf",
        "flag": "passport",
        "content": sample_content,  # Raw bytes (may need different handling)
        "description": "Alternative upload test"
    }
    
    tester.test_endpoint(
        "/api/documents/",
        method="POST",
        data=upload_data_alt,
        expect_status=201,
        title="Upload Document (Alternative Format)"
    )
    
    # Test 5: Update document (if we have an ID)
    if uploaded_document_id:
        print(f"\n✏️  TEST 5: Update Document (ID: {uploaded_document_id})")
        update_data = {
            "filename": "updated_test_file.txt",
            "flag": "medical_record",  # Changed flag
            "content": base64.b64encode(b"Updated document content").decode('utf-8'),
            "description": "Updated document description"
        }
        
        tester.test_endpoint(
            f"/api/documents/{uploaded_document_id}/",
            method="PUT",
            data=update_data,
            expect_status=200,
            title=f"Update Document {uploaded_document_id}"
        )
        
        # Test download of updated document
        print(f"\n⬇️  TEST 5b: Download Updated Document")
        tester.test_endpoint(
            f"/api/documents/{uploaded_document_id}/download/",
            method="GET",
            title=f"Download Updated Document {uploaded_document_id}"
        )
    
    # Test 6: Partial update (PATCH)
    if document_id:
        print(f"\n🔧 TEST 6: Partial Update Document (ID: {document_id})")
        patch_data = {
            "description": "Partially updated description",
            "flag": "updated_flag"
        }
        
        tester.test_endpoint(
            f"/api/documents/{document_id}/",
            method="PATCH",
            data=patch_data,
            expect_status=200,
            title=f"Partial Update Document {document_id}"
        )
    
    # Test 7: Test file type validation (if implemented)
    print("\n❌ TEST 7: Invalid File Upload (Testing Validation)")
    invalid_upload = {
        "filename": "",  # Empty filename
        "flag": "invalid_flag",
        "content": "invalid_content_format"
    }
    
    tester.test_endpoint(
        "/api/documents/",
        method="POST",
        data=invalid_upload,
        expect_status=400,
        title="Invalid Document Upload (Should Fail)"
    )
    
    print("\n✅ Document endpoint tests completed!")


if __name__ == "__main__":
    test_document_endpoints()
