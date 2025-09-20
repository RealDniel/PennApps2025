# Food Detection & Carbon Footprint App

A modern web application that uses computer vision to detect food items in images and provides information about their carbon footprint using AI.

## Features

- 🍎 Real-time food detection using YOLOv8
- 📷 Camera capture and image upload
- 🌱 AI-powered carbon footprint analysis
- 🎨 Modern, responsive UI built with Next.js
- ⚡ Simple Flask backend

## Tech Stack

### Frontend

- Next.js 15 with TypeScript
- Tailwind CSS for styling
- Lucide React for icons
- Camera API for image capture

### Backend

- Flask (Python)
- YOLOv8 for object detection
- Cerebras AI for carbon footprint analysis
- OpenCV for image processing

## Setup Instructions

### Prerequisites

- Python 3.8+
- Node.js 18+
- Camera access (for live detection)

### Backend Setup

1. Navigate to the backend directory:

```bash
cd backend
```

2. Create a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Set up environment variables:
   Create a `.env` file in the backend directory:

```
CEREBRAS_API_KEY=your_cerebras_api_key_here
```

5. Download the YOLO model (this will happen automatically on first run):
   The model file `yolov8n.pt` should be in the project root.

6. Start the Flask server:

```bash
python app.py
```

The API will be available at `http://localhost:8000`

### Frontend Setup

1. Navigate to the frontend directory:

```bash
cd frontend
```

2. Install dependencies:

```bash
npm install
```

3. Start the development server:

```bash
npm run dev
```

The app will be available at `http://localhost:3000`

## Usage

1. Open your browser and go to `http://localhost:3000`
2. Click "Start Camera" to use your device's camera
3. Point the camera at food items
4. Click "Capture" to take a photo
5. View the detection results and carbon footprint information
6. Or upload an image file instead of using the camera

## API Endpoints

- `GET /` - Health check
- `GET /health` - API status
- `POST /detect` - Upload image file for detection
- `POST /detect-base64` - Send base64 encoded image for detection

## Project Structure

```
PennApps2025/
├── backend/
│   ├── app.py              # Flask application
│   ├── requirements.txt     # Python dependencies
│   └── venv/               # Virtual environment
├── frontend/
│   ├── src/
│   │   ├── app/
│   │   │   └── page.tsx    # Main page component
│   │   └── components/
│   │       ├── CameraCapture.tsx
│   │       ├── DetectionResults.tsx
│   │       └── LoadingSpinner.tsx
│   ├── package.json
│   └── ...
├── food_detector.py        # Original standalone script
├── yolov8n.pt             # YOLO model file
└── README.md
```

## Environment Variables

Create a `.env` file in the backend directory with:

```
CEREBRAS_API_KEY=your_cerebras_api_key_here
```

## Troubleshooting

### Camera Issues

- Make sure to allow camera permissions in your browser
- Try refreshing the page if camera doesn't start
- Use the "Upload Image" option as an alternative

### API Connection Issues

- Ensure the backend is running on port 8000
- Check that CORS is properly configured
- Verify the Cerebras API key is set correctly

### Model Loading Issues

- The YOLO model will download automatically on first run
- Ensure you have a stable internet connection
- Check that the model file `yolov8n.pt` is in the project root

## Development

To run both frontend and backend in development mode:

1. Terminal 1 (Backend):

```bash
cd backend
source venv/bin/activate
python app.py
```

2. Terminal 2 (Frontend):

```bash
cd frontend
npm run dev
```

## License

This project is part of PennApps 2025.
