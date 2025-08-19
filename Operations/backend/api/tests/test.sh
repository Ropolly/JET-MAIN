#!/bin/bash

# JET-MAIN API Test Runner
# This script runs all API endpoint tests against a live server

echo "🚀 JET-MAIN API Test Suite"
echo "============================"

# Check if server is running
echo "🔍 Checking if Django server is running..."
if ! curl -s http://127.0.0.1:8000 > /dev/null 2>&1; then
    echo "❌ Server is not running at http://127.0.0.1:8000"
    echo "Please start the server with: python manage.py runserver"
    exit 1
fi
echo "✅ Server is running"
echo "🧪 Running API endpoint tests..."
echo ""

# Run the Python test runner
python3 run_all_tests.py

# Capture exit code
EXIT_CODE=$?

echo ""
if [ $EXIT_CODE -eq 0 ]; then
    echo "🎉 All tests completed successfully!"
else
    echo "⚠️  Some tests failed. Check output above for details."
fi

exit $EXIT_CODE