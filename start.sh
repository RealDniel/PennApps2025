#!/bin/bash

# Food Detection App Startup Script

echo "🍎 Starting Food Detection App..."
echo "=================================="

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8+ first."
    exit 1
fi

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js 18+ first."
    exit 1
fi

# Check if the YOLO model exists
if [ ! -f "yolov8n.pt" ]; then
    echo "❌ YOLO model file (yolov8n.pt) not found in the root directory."
    echo "   Please make sure the model file is present."
    exit 1
fi

echo "✅ Prerequisites check passed!"

# Start backend
echo "🚀 Starting FastAPI backend..."
cd backend

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📥 Installing Python dependencies..."
pip install -r requirements.txt

# Start backend in background
echo "🌐 Starting FastAPI server on http://localhost:8000"
python main.py &
BACKEND_PID=$!

# Go back to root directory
cd ..

# Start frontend
echo "🎨 Starting Next.js frontend..."
cd frontend

# Install dependencies if needed
if [ ! -d "node_modules" ]; then
    echo "📥 Installing Node.js dependencies..."
    npm install
fi

# Start frontend
echo "🌐 Starting Next.js server on http://localhost:3000"
npm run dev &
FRONTEND_PID=$!

# Go back to root directory
cd ..

echo ""
echo "🎉 Food Detection App is starting up!"
echo "=================================="
echo "📱 Frontend: http://localhost:3000"
echo "🔧 Backend API: http://localhost:8000"
echo "📚 API Docs: http://localhost:8000/docs"
echo ""
echo "Press Ctrl+C to stop both servers"

# Function to cleanup on exit
cleanup() {
    echo ""
    echo "🛑 Stopping servers..."
    kill $BACKEND_PID 2>/dev/null
    kill $FRONTEND_PID 2>/dev/null
    echo "✅ Servers stopped successfully!"
    exit 0
}

# Set trap to cleanup on script exit
trap cleanup SIGINT SIGTERM

# Wait for both processes
wait
