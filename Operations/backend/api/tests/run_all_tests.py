#!/usr/bin/env python3
"""
Run all API endpoint tests against a live server.
This script runs all individual test files and provides a summary.
"""
import sys
import os
import subprocess
import time
from datetime import datetime

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from base_test import APITester


def check_server_connectivity():
    """Check if the API server is running and accessible."""
    print("🔍 Checking server connectivity...")
    tester = APITester()
    
    try:
        # Use requests directly to avoid status code checking
        import requests
        response = requests.get(f"{tester.base_url}/api/")
        tester.print_response(response, "Server Connectivity Check")
        
        # Accept 401 as valid since /api/ requires authentication
        status_code = response.status_code
        print(f"DEBUG: Response status code: {status_code}")
        if status_code in [200, 401]:
            print("✅ API server is reachable")
            return True
        else:
            print(f"❌ API server returned error status: {status_code}")
            return False
    except Exception as e:
        print(f"❌ Cannot connect to API server: {e}")
        return False


def run_test_file(test_file):
    """Run a single test file and capture output."""
    print(f"\n{'='*80}")
    print(f"🧪 RUNNING: {test_file}")
    print(f"{'='*80}")
    
    try:
        # Run the test file
        result = subprocess.run(
            [sys.executable, test_file],
            capture_output=True,
            text=True,
            timeout=60  # 60 second timeout per test file
        )
        
        # Print the output
        if result.stdout:
            print(result.stdout)
        
        if result.stderr:
            print("STDERR:")
            print(result.stderr)
        
        return result.returncode == 0
    
    except subprocess.TimeoutExpired:
        print(f"❌ Test {test_file} timed out after 60 seconds")
        return False
    except Exception as e:
        print(f"❌ Error running {test_file}: {e}")
        return False


def main():
    """Run all API tests."""
    print("🚀 JET-MAIN API ENDPOINT TEST SUITE")
    print("=" * 80)
    print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 80)
    
    # Check server connectivity first
    if not check_server_connectivity():
        print("\n❌ Cannot connect to API server. Please ensure the server is running at http://localhost:8000")
        print("Start the server with: python manage.py runserver")
        sys.exit(1)
    
    # Define test files in order
    test_files = [
        "test_userprofile.py",
        "test_passengers.py", 
        "test_crew_lines.py",
        "test_trip_lines.py",
        "test_trips.py",
        "test_quotes.py",
        "test_patients.py",
        "test_documents.py",
        "test_transactions.py"
    ]
    
    # Track results
    results = {}
    start_time = time.time()
    
    # Run each test file
    for test_file in test_files:
        if os.path.exists(test_file):
            success = run_test_file(test_file)
            results[test_file] = success
        else:
            print(f"⚠️  Test file {test_file} not found, skipping...")
            results[test_file] = False
    
    # Print summary
    end_time = time.time()
    duration = end_time - start_time
    
    print(f"\n{'='*80}")
    print("📊 TEST SUMMARY")
    print(f"{'='*80}")
    print(f"Total duration: {duration:.2f} seconds")
    print(f"Completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    passed = 0
    failed = 0
    
    for test_file, success in results.items():
        status = "✅ PASSED" if success else "❌ FAILED"
        print(f"{test_file:<25} {status}")
        if success:
            passed += 1
        else:
            failed += 1
    
    print(f"\n📈 RESULTS: {passed} passed, {failed} failed out of {len(results)} tests")
    
    if failed > 0:
        print("\n⚠️  Some tests failed. Check the output above for details.")
        print("Common issues:")
        print("- Authentication credentials may need adjustment")
        print("- Test data (IDs) may not exist in the database")
        print("- Permissions may not be configured correctly")
        print("- Some endpoints may not be implemented yet")
    else:
        print("\n🎉 All tests completed successfully!")
    
    print(f"\n{'='*80}")
    
    return failed == 0


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
