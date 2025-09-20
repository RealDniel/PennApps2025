#!/bin/bash

echo "🍎 Starting Food Detection App with Frontend"
echo "============================================="

# Check if backend is running
if ! curl -s http://localhost:8000/health > /dev/null; then
    echo "❌ Backend is not running. Please start the backend first:"
    echo "   cd backend && python app.py"
    echo ""
    echo "Starting frontend server anyway..."
fi

# Start a simple HTTP server for the frontend
echo "🌐 Starting frontend server on http://localhost:3000"
echo "📱 Open your browser and go to: http://localhost:3000"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

cd frontend
python3 -m http.server 3000
