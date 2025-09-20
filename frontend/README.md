# Food Detection Frontend

A simple, modern web interface for the Food Detection & Carbon Footprint Analyzer.

## Features

- 🖼️ **Image Upload**: Drag & drop or click to upload images
- 📷 **Live Camera**: Real-time camera feed with instant food detection
- 🔍 **Real-time Detection**: Uses YOLO to detect food items in images
- 🌱 **Carbon Footprint**: Shows environmental impact information using Cerebras AI
- 📱 **Responsive Design**: Works on desktop and mobile devices
- ✨ **Modern UI**: Clean, intuitive interface with smooth animations
- 🎥 **Camera Controls**: Start/stop camera, capture images, toggle real-time detection

## How to Use

1. **Start the Backend** (in a separate terminal):

   ```bash
   cd backend
   python app.py
   ```

2. **Start the Frontend**:

   ```bash
   # From the project root
   ./start_frontend.sh

   # Or manually
   cd frontend
   python3 -m http.server 3000
   ```

3. **Open in Browser**:
   - Go to `http://localhost:3000`
   - Choose between **Upload Image** or **Live Camera** mode
   - **Upload Mode**: Drag & drop or click to upload images
   - **Camera Mode**:
     - Click "Start Camera" to begin live feed
     - Use "Capture & Analyze" for one-time detection
     - Toggle "Real-time Detection" for continuous monitoring
   - View detection results and carbon footprint information

## File Structure

```
frontend/
├── index.html      # Main HTML structure
├── style.css       # Modern CSS styling
├── script.js       # JavaScript functionality
└── README.md       # This file
```

## API Integration

The frontend communicates with the backend API at `http://localhost:8000`:

- `POST /detect-base64` - Upload base64 encoded image for detection
- `GET /health` - Check if backend is running

## Browser Compatibility

- Chrome (recommended)
- Firefox
- Safari
- Edge

## Troubleshooting

- **"Failed to connect to server"**: Make sure the backend is running on port 8000
- **Images not uploading**: Check file size (max 10MB) and format (JPG, PNG, etc.)
- **No detections**: Try images with clear, well-lit food items
- **Camera not working**:
  - Allow camera access when prompted
  - Make sure you're using HTTPS (required for camera access on most browsers)
  - Try refreshing the page and allowing camera access again
- **Real-time detection slow**: Detection runs every 2 seconds to avoid overwhelming the server
