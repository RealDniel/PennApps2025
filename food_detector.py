#!/usr/bin/env python3
"""
Food Detection App with enhanced visibility for macOS
"""

import cv2
import numpy as np
from ultralytics import YOLO
import time
import os

class FoodDetector:
    def __init__(self, confidence_threshold=0.5):
        """Initialize the YOLO model for food detection"""
        # Load YOLOv8 model (will download automatically on first run)
        self.model = YOLO('yolov8n.pt')  # Using nano version for speed
        self.confidence_threshold = confidence_threshold

        # COCO class names that are food-related
        self.food_classes = {
            0: 'person', 1: 'bicycle', 2: 'car', 3: 'motorcycle', 4: 'airplane', 5: 'bus', 6: 'train', 7: 'truck', 8: 'boat',
            9: 'traffic light', 10: 'fire hydrant', 11: 'stop sign', 12: 'parking meter', 13: 'bench', 14: 'bird', 15: 'cat',
            16: 'dog', 17: 'horse', 18: 'sheep', 19: 'cow', 20: 'elephant', 21: 'bear', 22: 'zebra', 23: 'giraffe', 24: 'backpack',
            25: 'umbrella', 26: 'handbag', 27: 'tie', 28: 'suitcase', 29: 'frisbee', 30: 'skis', 31: 'snowboard', 32: 'sports ball',
            33: 'kite', 34: 'baseball bat', 35: 'baseball glove', 36: 'skateboard', 37: 'surfboard', 38: 'tennis racket',
            39: 'bottle', 40: 'wine glass', 41: 'cup', 42: 'fork', 43: 'knife', 44: 'spoon', 45: 'bowl', 46: 'banana',
            47: 'apple', 48: 'sandwich', 49: 'orange', 50: 'broccoli', 51: 'carrot', 52: 'hot dog', 53: 'pizza',
            54: 'donut', 55: 'cake', 56: 'chair', 57: 'couch', 58: 'potted plant', 59: 'bed', 60: 'dining table',
            61: 'toilet', 62: 'tv', 63: 'laptop', 64: 'mouse', 65: 'remote', 66: 'keyboard', 67: 'cell phone',
            68: 'microwave', 69: 'oven', 70: 'toaster', 71: 'sink', 72: 'refrigerator', 73: 'book', 74: 'clock',
            75: 'vase', 76: 'scissors', 77: 'teddy bear', 78: 'hair drier', 79: 'toothbrush'
        }

        # Filter for food-related items (expanded list)
        self.food_items = {
            39: 'bottle', 40: 'wine glass', 41: 'cup', 42: 'fork', 43: 'knife', 44: 'spoon', 45: 'bowl',
            46: 'banana', 47: 'apple', 48: 'sandwich', 49: 'orange', 50: 'broccoli', 51: 'carrot',
            52: 'hot dog', 53: 'pizza', 54: 'donut', 55: 'cake'
        }

        # Additional food items that might be detected
        self.additional_food_items = {
            68: 'microwave', 69: 'oven', 70: 'toaster', 72: 'refrigerator'
        }

    def detect_food(self, frame):
        """Detect food items in the frame and return annotated frame"""
        # Run YOLO detection
        results = self.model(frame, verbose=False)

        # Process detections
        annotated_frame = frame.copy()

        for result in results:
            boxes = result.boxes
            if boxes is not None:
                for box in boxes:
                    # Get bounding box coordinates
                    x1, y1, x2, y2 = box.xyxy[0].cpu().numpy().astype(int)

                    # Get class ID and confidence
                    class_id = int(box.cls[0].cpu().numpy())
                    confidence = float(box.conf[0].cpu().numpy())

                    # Only process food items with high confidence
                    if class_id in self.food_items and confidence > self.confidence_threshold:
                        # Choose color based on confidence level
                        if confidence > 0.8:
                            color = (0, 255, 0)  # Green for high confidence
                        elif confidence > 0.6:
                            color = (0, 255, 255)  # Yellow for medium confidence
                        else:
                            color = (0, 165, 255)  # Orange for low confidence

                        # Draw bounding box with thicker line
                        cv2.rectangle(annotated_frame, (x1, y1), (x2, y2), color, 3)

                        # Prepare label text with better formatting
                        food_name = self.food_items[class_id].replace('_', ' ').title()
                        label = f"{food_name}: {confidence:.1%}"

                        # Get text size for background rectangle
                        font_scale = 0.7
                        thickness = 2
                        (text_width, text_height), baseline = cv2.getTextSize(
                            label, cv2.FONT_HERSHEY_SIMPLEX, font_scale, thickness
                        )

                        # Draw background rectangle for text with padding
                        padding = 5
                        cv2.rectangle(annotated_frame,
                                    (x1, y1 - text_height - baseline - padding),
                                    (x1 + text_width + padding, y1),
                                    color, -1)

                        # Draw text with better contrast
                        cv2.putText(annotated_frame, label,
                                  (x1 + padding//2, y1 - padding//2),
                                  cv2.FONT_HERSHEY_SIMPLEX, font_scale,
                                  (255, 255, 255), thickness)

        return annotated_frame

def main():
    """Main function to run the food detection app with enhanced visibility"""
    print("🍎 Starting Food Detection App (Enhanced Visibility)")
    print("=" * 50)
    print("📱 Press 'q' to quit the application")
    print("📱 Press 's' to save current frame")
    print("📱 Press 'h' to show/hide help")
    print("📱 Press SPACE to pause/resume")
    print()

    try:
        # Initialize detector
        print("🤖 Loading YOLO model...")
        detector = FoodDetector()
        print("✅ Model loaded successfully!")

        # Initialize camera
        print("📷 Initializing camera...")
        cap = cv2.VideoCapture(0)

        # Test camera immediately
        ret, test_frame = cap.read()
        if not ret:
            print("❌ Error: Camera test failed - cannot read frames")
            cap.release()
            return
        else:
            print(f"✅ Camera test successful! Frame size: {test_frame.shape[1]}x{test_frame.shape[0]}")

        # Set camera properties for better performance
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        cap.set(cv2.CAP_PROP_FPS, 30)

        if not cap.isOpened():
            print("❌ Error: Could not open camera")
            print("💡 Make sure your camera is connected and not being used by another application")
            return

        print("✅ Camera opened successfully!")
        print("🍽️  Point your camera at food items to detect them...")
        print("🎯 Detected food items will be highlighted with colored boxes")
        print("🪟 A window should open showing the camera feed...")
        print()

        frame_count = 0
        show_help = True
        paused = False

        # Create window with specific properties for better visibility
        window_name = 'Food Detection App - Press Q to Quit'
        cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
        cv2.resizeWindow(window_name, 800, 600)

        # Move window to front (macOS specific)
        try:
            os.system('osascript -e "tell application \\"System Events\\" to set frontmost of first process whose unix id is ' + str(os.getpid()) + ' to true"')
        except:
            pass

        print("🔄 Starting main detection loop...")
        print("💡 If you don't see the window, try:")
        print("   - Looking in your dock/taskbar")
        print("   - Pressing Cmd+Tab to cycle through windows")
        print("   - Checking if the window is behind other windows")
        print()

        while True:
            if not paused:
                # Capture frame-by-frame
                ret, frame = cap.read()

                if not ret:
                    print("❌ Error: Could not read frame from camera")
                    break

                # Flip frame horizontally for mirror effect
                frame = cv2.flip(frame, 1)

                # Detect food items
                annotated_frame = detector.detect_food(frame)

                # Add help text overlay
                if show_help:
                    help_text = [
                        "Controls:",
                        "Q - Quit",
                        "S - Save frame",
                        "H - Toggle help",
                        "SPACE - Pause/Resume"
                    ]
                    y_offset = 30
                    for text in help_text:
                        cv2.putText(annotated_frame, text, (10, y_offset),
                                  cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
                        y_offset += 20

                # Add frame counter and status
                status_text = f"Frame: {frame_count} | Status: {'PAUSED' if paused else 'RUNNING'}"
                cv2.putText(annotated_frame, status_text,
                           (10, annotated_frame.shape[0] - 20),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

                # Display the resulting frame
                cv2.imshow(window_name, annotated_frame)
                frame_count += 1

            # Handle key presses
            key = cv2.waitKey(30) & 0xFF  # Increased wait time for better responsiveness
            if key == ord('q'):
                break
            elif key == ord('s'):
                # Save current frame
                if not paused:
                    filename = f"food_detection_{int(time.time())}.jpg"
                    cv2.imwrite(filename, annotated_frame)
                    print(f"📸 Frame saved as {filename}")
            elif key == ord('h'):
                show_help = not show_help
                print(f"ℹ️  Help {'shown' if show_help else 'hidden'}")
            elif key == ord(' '):  # Space bar
                paused = not paused
                print(f"⏸️  {'Paused' if paused else 'Resumed'}")

    except KeyboardInterrupt:
        print("\n⏹️  Application interrupted by user")
    except Exception as e:
        print(f"❌ An error occurred: {str(e)}")
        print("💡 Please check your camera connection and try again")

    finally:
        # Release everything when job is finished
        if 'cap' in locals():
            cap.release()
        cv2.destroyAllWindows()
        print("✅ Application closed successfully")

if __name__ == "__main__":
    main()
