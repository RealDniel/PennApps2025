@echo off
REM Food Detection App Startup Script for Windows

echo 🍎 Starting Food Detection App...
echo ================================

REM Check if virtual environment exists
if not exist "backend\venv" (
    echo 📦 Creating Python virtual environment...
    cd backend
    python -m venv venv
    call venv\Scripts\activate.bat
    echo 📥 Installing Python dependencies...
    pip install -r requirements.txt
    cd ..
)

REM Check for .env file
if not exist "backend\.env" (
    echo ⚠️  Warning: No .env file found in backend directory
    echo Please create backend\.env with your CEREBRAS_API_KEY
    echo Example:
    echo CEREBRAS_API_KEY=your_api_key_here
    echo.
)

echo 🚀 Starting backend server...
cd backend
call venv\Scripts\activate.bat
start /B python app.py

echo 🚀 Starting frontend server...
cd ..\frontend
start /B python -m http.server 3000

echo.
echo ✅ Both servers are starting up!
echo Backend: http://localhost:8000
echo Frontend: http://localhost:3000
echo.
echo Press any key to stop both servers...

pause > nul

REM Kill the background processes
taskkill /F /IM python.exe 2>nul

echo ✅ Servers stopped
pause
