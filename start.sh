#!/bin/bash

# Food Detection App Startup Script

echo "🍎 Starting Food Detection App..."
echo "================================"

# Check if virtual environment exists
if [ ! -d "backend/venv" ]; then
    echo "📦 Creating Python virtual environment..."
    cd backend
    python3 -m venv venv
    source venv/bin/activate
    echo "📥 Installing Python dependencies..."
    pip install -r requirements.txt
    cd ..
fi

# Check if frontend dependencies are installed
if [ ! -d "frontend/node_modules" ]; then
    echo "📦 Installing frontend dependencies..."
    cd frontend
    npm install
    cd ..
fi

# Check for .env file
if [ ! -f "backend/.env" ]; then
    echo "⚠️  Warning: No .env file found in backend directory"
    echo "Please create backend/.env with your CEREBRAS_API_KEY"
    echo "Example:"
    echo "CEREBRAS_API_KEY=your_api_key_here"
    echo ""
fi

echo "🚀 Starting backend server..."
cd backend
source venv/bin/activate
python app.py &
BACKEND_PID=$!

echo "🚀 Starting frontend server..."
cd ../frontend
npm run dev &
FRONTEND_PID=$!

echo ""
echo "✅ Both servers are starting up!"
echo "Backend: http://localhost:8000"
echo "Frontend: http://localhost:3000"
echo ""
echo "Press Ctrl+C to stop both servers"

# Function to cleanup on exit
cleanup() {
    echo ""
    echo "🛑 Stopping servers..."
    kill $BACKEND_PID 2>/dev/null
    kill $FRONTEND_PID 2>/dev/null
    echo "✅ Servers stopped"
    exit 0
}

# Set trap to cleanup on script exit
trap cleanup SIGINT SIGTERM

# Wait for both processes
wait
