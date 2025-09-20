@echo off
REM Food Detection App Startup Script for Windows

echo 🍎 Starting Food Detection App...
echo ==================================

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed. Please install Python 3.8+ first.
    echo Download from: https://www.python.org/downloads/
    pause
    exit /b 1
)

REM Check if Node.js is installed
node --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Node.js is not installed. Please install Node.js 18+ first.
    echo Download from: https://nodejs.org/
    pause
    exit /b 1
)

REM Check if the YOLO model exists
if not exist "yolov8n.pt" (
    echo ❌ YOLO model file (yolov8n.pt) not found in the root directory.
    echo Please make sure the model file is present.
    pause
    exit /b 1
)

echo ✅ Prerequisites check passed!

REM Start backend
echo 🚀 Starting FastAPI backend...
cd backend

REM Check if virtual environment exists
if not exist "venv" (
    echo 📦 Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
echo 🔧 Activating virtual environment...
call venv\Scripts\activate.bat

REM Install dependencies
echo 📥 Installing Python dependencies...
pip install -r requirements.txt

REM Start backend in background
echo 🌐 Starting FastAPI server on http://localhost:8000
start /B python main.py

REM Go back to root directory
cd ..

REM Start frontend
echo 🎨 Starting Next.js frontend...
cd frontend

REM Install dependencies if needed
if not exist "node_modules" (
    echo 📥 Installing Node.js dependencies...
    npm install
)

REM Start frontend
echo 🌐 Starting Next.js server on http://localhost:3000
start /B npm run dev

REM Go back to root directory
cd ..

echo.
echo 🎉 Food Detection App is starting up!
echo ==================================
echo 📱 Frontend: http://localhost:3000
echo 🔧 Backend API: http://localhost:8000
echo 📚 API Docs: http://localhost:8000/docs
echo.
echo Press any key to stop both servers...

pause >nul

echo.
echo 🛑 Stopping servers...
taskkill /F /IM python.exe >nul 2>&1
taskkill /F /IM node.exe >nul 2>&1
echo ✅ Servers stopped successfully!
pause
