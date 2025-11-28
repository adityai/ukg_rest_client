#!/bin/bash

# UKG Mock Server Test Runner
# Starts the mock server, loads sample data, and runs tests

echo "🚀 Starting UKG Mock Server Test Suite"
echo "======================================"

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not installed"
    exit 1
fi

# Install dependencies if needed
echo "📦 Installing dependencies..."
pip install -r requirements.txt > /dev/null 2>&1

# Start the mock server in background
echo "🌐 Starting mock server on http://localhost:8080..."
python3 mock_server.py &
SERVER_PID=$!

# Wait for server to start
echo "⏳ Waiting for server to start..."
sleep 3

# Check if server is running
if ! curl -s http://localhost:8080/api/v2/client/health > /dev/null 2>&1; then
    echo "❌ Failed to start mock server"
    kill $SERVER_PID 2>/dev/null
    exit 1
fi

echo "✅ Mock server is running (PID: $SERVER_PID)"

# Load sample data
echo "📊 Loading sample data..."
python3 sample_data.py

if [ $? -eq 0 ]; then
    echo "✅ Sample data loaded successfully"
else
    echo "⚠️  Sample data loading failed, continuing with tests..."
fi

# Run the test suite
echo "🧪 Running test suite..."
python3 test_client.py

TEST_RESULT=$?

# Cleanup: Stop the server
echo "🧹 Cleaning up..."
kill $SERVER_PID 2>/dev/null
wait $SERVER_PID 2>/dev/null

if [ $TEST_RESULT -eq 0 ]; then
    echo ""
    echo "🎉 All tests passed!"
    echo "✅ Mock UKG REST API is ready for use"
    echo ""
    echo "To use the mock server:"
    echo "1. Start server: python3 mock_server.py"
    echo "2. Load data: python3 sample_data.py"
    echo "3. Point your client to: http://localhost:8080"
else
    echo ""
    echo "❌ Some tests failed"
    echo "Check the output above for details"
fi

exit $TEST_RESULT