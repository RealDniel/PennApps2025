# 🍎 Food Detection App

A real-time food detection application using YOLOv8 and OpenCV that identifies various food items through your camera with food names displayed on bounding boxes.

## ✨ Features

- **Real-time Detection**: Live camera feed with instant food recognition
- **Food Name Labels**: Food names displayed prominently on top of detection boxes
- **Visual Feedback**: Color-coded bounding boxes based on confidence levels
- **16+ Food Categories**: Fruits, vegetables, meals, and kitchen items
- **Interactive Controls**: Save frames, pause/resume, toggle help
- **High Performance**: Optimized for smooth real-time processing

## 🚀 Quick Start

1. **Clone and Setup**:

   ```bash
   git clone <your-repo-url>
   cd pennapps
   pip install -r requirements.txt
   ```

2. **Run the App**:

   ```bash
   python3 food_detector.py
   ```

3. **Use the App**:
   - Point your camera at food items
   - Watch as detected foods are highlighted with colored boxes
   - Food names appear clearly above each detection box

## 🎮 Controls

- **Q**: Quit the application
- **S**: Save current frame as image
- **H**: Toggle help overlay on/off
- **SPACE**: Pause/Resume (enhanced version only)

## 🍽️ Supported Food Items

The app detects 16+ food categories:

- **Fruits**: Apple, Banana, Orange
- **Vegetables**: Broccoli, Carrot
- **Meals**: Pizza, Hot Dog, Sandwich, Cake, Donut
- **Kitchen Items**: Bottle, Wine Glass, Cup, Fork, Knife, Spoon, Bowl
- **Appliances**: Microwave, Oven, Toaster, Refrigerator

## 🎨 Visual Indicators

- **🟢 Green Box**: High confidence (>80%)
- **🟡 Yellow Box**: Medium confidence (60-80%)
- **🟠 Orange Box**: Lower confidence (50-60%)

## 📁 Project Structure

```
pennapps/
├── food_detector.py          # Main food detection app
├── requirements.txt          # Python dependencies
├── .gitignore               # Git ignore rules
└── README.md                # This file
```

## 📋 Requirements

- Python 3.7+
- Webcam or camera device
- OpenCV, Ultralytics YOLO, NumPy, Pillow

## 🔧 Technical Details

- **Model**: YOLOv8 nano for fast inference
- **Performance**: Real-time processing at 30 FPS
- **Resolution**: 640x480 (optimized for performance)
- **Confidence**: 50% threshold (adjustable)
- **Platform**: Cross-platform (tested on macOS)

## 🐛 Troubleshooting

- **Camera not working**: Ensure no other apps are using the camera
- **Window not visible**: Check your dock/taskbar or press Cmd+Tab to cycle through windows
- **Poor detection**: Improve lighting or adjust confidence threshold
- **Performance issues**: Close other applications to free up resources

## 🎯 Key Features

The app successfully demonstrates:

- Real-time object detection using YOLO
- Food name labeling on bounding boxes
- Color-coded confidence indicators
- Interactive camera controls
- Cross-platform compatibility

Perfect for food recognition, kitchen inventory, or educational purposes! 🍕🥗🍎
