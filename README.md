# Food Detection App

A modern web application that uses AI-powered computer vision to detect food items in real-time. Built with Next.js frontend and FastAPI backend.

## Features

- 🎥 **Real-time camera detection** - Detect food items using your webcam
- 📁 **Image upload** - Upload images to detect food items
- 🤖 **AI-powered** - Uses YOLOv8 for accurate food detection
- 🎨 **Modern UI** - Beautiful, responsive interface built with Tailwind CSS
- ⚡ **Fast API** - FastAPI backend for high-performance image processing

## Architecture

- **Frontend**: Next.js 14 with TypeScript and Tailwind CSS
- **Backend**: FastAPI with Python
- **AI Model**: YOLOv8 (nano version for speed)
- **Computer Vision**: OpenCV for image processing

## 🚀 Quick Start (For Your Friends)

### Prerequisites
- **Python 3.8+** ([Download here](https://www.python.org/downloads/))
- **Node.js 18+** ([Download here](https://nodejs.org/))
- **Git** ([Download here](https://git-scm.com/downloads))

### Step 1: Clone the Repository
```bash
git clone <your-github-repo-url>
cd <your-repo-name>
```

### Step 2: Easy Setup (Recommended)

**For macOS/Linux:**
```bash
./start.sh
```

**For Windows:**
```cmd
start.bat
```

These scripts will automatically:
- Set up Python virtual environment
- Install all dependencies
- Start both backend and frontend servers

### Step 3: Access the Application
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs

---

## 🔧 Manual Setup (Alternative)

If the startup script doesn't work, follow these manual steps:

### Backend Setup

1. **Navigate to backend directory:**
   ```bash
   cd backend
   ```

2. **Create Python virtual environment:**
   ```bash
   # On macOS/Linux:
   python3 -m venv venv
   source venv/bin/activate
   
   # On Windows:
   python -m venv venv
   venv\Scripts\activate
   ```

3. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Start the FastAPI server:**
   ```bash
   python main.py
   ```
   The backend will be available at `http://localhost:8000`

### Frontend Setup (New Terminal)

1. **Navigate to frontend directory:**
   ```bash
   cd frontend
   ```

2. **Install Node.js dependencies:**
   ```bash
   npm install
   ```

3. **Start the development server:**
   ```bash
   npm run dev
   ```
   The frontend will be available at `http://localhost:3000`

---

## 🎯 What Your Friends Will See

1. **Beautiful web interface** with camera detection and file upload
2. **Real-time food detection** - just point camera at food items
3. **Live overlay** showing detected food names and confidence scores
4. **Image upload** functionality for static images
5. **Responsive design** that works on desktop and mobile

## 🎮 How to Use

### Real-time Camera Detection (Recommended)
1. **Start Camera** → Click to activate your webcam
2. **Start Real-time Detection** → Click to begin continuous detection
3. **Point camera at food** → Detection results appear automatically in the overlay
4. **Move around** → Results update every second as you point at different items
5. **Stop Real-time Detection** → Click to pause continuous detection

### Single Detection Mode
1. **Start Camera** → Click to activate your webcam
2. **Single Detection** → Click to analyze the current frame once
3. **View results** → See detection results in the results section below

### Image Upload
1. **Choose File** → Select an image from your computer
2. **Automatic processing** → The image will be analyzed automatically
3. **View results** → See detection results with annotated image

## 🛠️ Troubleshooting

### Common Issues

**1. Camera not working:**
- Make sure to allow camera permissions in your browser
- Try refreshing the page and allowing permissions again
- Check if another application is using your camera

**2. Backend connection error:**
- Ensure the FastAPI server is running on port 8000
- Check if port 8000 is available (not used by another application)
- Try restarting the backend server

**3. Model loading error:**
- The YOLO model (`yolov8n.pt`) should be in the root directory
- If missing, the model will download automatically on first run
- Make sure you have internet connection for the first run

**4. CORS errors:**
- Backend CORS is configured for `localhost:3000`
- Make sure frontend is running on port 3000
- Don't access frontend via IP address, use `localhost:3000`

**5. Startup script not working:**
- Make sure the script is executable: `chmod +x start.sh`
- On Windows, use Git Bash or WSL to run the script
- Follow the manual setup steps if the script fails

### Getting Help

If you encounter issues:
1. Check the terminal/console for error messages
2. Make sure all prerequisites are installed
3. Try the manual setup steps
4. Check if ports 3000 and 8000 are available

## API Endpoints

- `GET /` - Health check
- `GET /health` - API status
- `POST /detect` - Upload image file for detection
- `POST /detect-base64` - Send base64 encoded image for detection

## Detected Food Items

The app can detect the following food-related items:
- Fruits: apple, banana, orange
- Vegetables: broccoli, carrot
- Prepared foods: pizza, sandwich, hot dog, donut, cake
- Utensils: fork, knife, spoon, bowl, cup, bottle, wine glass

## Development

### Backend Development
- The main API logic is in `backend/main.py`
- Food detection logic is in the `FoodDetector` class
- CORS is configured to allow requests from `localhost:3000`

### Frontend Development
- Main page component is in `frontend/src/app/page.tsx`
- Uses React hooks for state management
- Camera access uses the MediaDevices API
- Image processing uses HTML5 Canvas

## Troubleshooting

1. **Camera not working**: Make sure to allow camera permissions in your browser
2. **Backend connection error**: Ensure the FastAPI server is running on port 8000
3. **Model loading error**: Make sure `yolov8n.pt` is in the correct location
4. **CORS errors**: Check that the backend CORS settings allow your frontend URL

## Future Enhancements

- [ ] Real-time video streaming detection
- [ ] Food nutrition information
- [ ] Calorie counting
- [ ] Multiple model support
- [ ] User authentication
- [ ] Detection history
- [ ] Mobile app version