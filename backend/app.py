#!/usr/bin/env python3
"""
Flask Backend for Food Detection App
"""

import cv2
import numpy as np
from ultralytics import YOLO
import time
import os
import base64
from io import BytesIO
from PIL import Image
from flask import Flask, request, jsonify
from flask_cors import CORS
import json
from cerebras.cloud.sdk import Cerebras
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

class FoodDetector:
    food_cache = {}
    last_query_time = 0
    QUERY_INTERVAL = 3  # seconds

    def __init__(self, confidence_threshold=0.5):
        """Initialize the YOLO model for food detection"""
        self.model = YOLO('yolov8n.pt')
        self.confidence_threshold = confidence_threshold

        # COCO class names
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

        # Filter for food-related items
        self.food_items = {
            39: 'bottle', 40: 'wine glass', 41: 'cup', 42: 'fork', 43: 'knife', 44: 'spoon', 45: 'bowl',
            46: 'banana', 47: 'apple', 48: 'sandwich', 49: 'orange', 50: 'broccoli', 51: 'carrot',
            52: 'hot dog', 53: 'pizza', 54: 'donut', 55: 'cake'
        }

    def ask_ai(self, food_name):
        """Query Cerebras about the detected food's carbon footprint"""
        if food_name in FoodDetector.food_cache:
            return FoodDetector.food_cache[food_name]

        now = time.time()
        if now - FoodDetector.last_query_time < FoodDetector.QUERY_INTERVAL:
            return None

        try:
            client = Cerebras(api_key=os.getenv('CEREBRAS_API_KEY'))
            prompt = f"""
            Provide information about the carbon footprint of {food_name}.

            IMPORTANT: Respond ONLY with a valid JSON object. Do not include any text before or after the JSON.

            The JSON object must contain exactly these two fields:
            1. "food_name": The name of the food
            2. "concise_fact": A short, single-line string with the food's approximate carbon footprint (e.g., "0.1kg CO2 per kg")
            3. "detailed_info": A paragraph explaining the carbon footprint in more detail, including factors that affect it and some educational snippets or alternatives

            Example format:
            {{"concise_fact": "Banana: 0.1kg CO2 per kg", "detailed_info": "Bananas have a relatively low carbon footprint compared to other foods..."}}
            """
            chat_completion = client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model="llama-4-scout-17b-16e-instruct",
                max_tokens=600,
                temperature=0.2
            )
            # Parse the JSON response
            response_text = chat_completion.choices[0].message.content
            print(f"AI Response for {food_name}: {response_text[:200]}...")  # Debug log

            try:
                response_json = json.loads(response_text)

                # Cache the parsed JSON object
                FoodDetector.food_cache[food_name] = response_json
                FoodDetector.last_query_time = now

                # Return the structured data
                return response_json
            except json.JSONDecodeError:
                # If JSON parsing fails, return a fallback structure
                fallback_response = {
                    "concise_fact": f"{food_name}: Carbon footprint data unavailable",
                    "detailed_info": f"Carbon footprint information for {food_name} is currently unavailable. This could be due to limited data or processing issues."
                }

                # Cache the fallback response
                FoodDetector.food_cache[food_name] = fallback_response
                FoodDetector.last_query_time = now

                return fallback_response
        except Exception as e:
            print(f"Error querying AI: {e}")
            return None

    def detect_food(self, image_bytes):
        """Detect food items in the image and return results"""
        try:
            # Convert bytes to OpenCV image
            nparr = np.frombuffer(image_bytes, np.uint8)
            frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

            if frame is None:
                raise ValueError("Could not decode image")

            # Run YOLO detection
            results = self.model(frame, verbose=False)

            detections = []
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
                            food_name = self.food_items[class_id].replace('_', ' ').title()

                            # Query AI for carbon footprint info
                            carbon_info = self.ask_ai(food_name)

                            # Create detection result
                            detection = {
                                "food_name": food_name,
                                "confidence": confidence,
                                "bbox": [int(x1), int(y1), int(x2), int(y2)],
                                "carbon_footprint_info": carbon_info
                            }
                            detections.append(detection)

                            # Draw bounding box
                            if confidence > 0.8:
                                color = (0, 255, 0)  # Green
                            elif confidence > 0.6:
                                color = (0, 255, 255)  # Yellow
                            else:
                                color = (0, 165, 255)  # Orange

                            cv2.rectangle(annotated_frame, (x1, y1), (x2, y2), color, 3)

                            # Draw label
                            label = f"{food_name}: {confidence:.1%}"
                            font_scale = 0.7
                            thickness = 2
                            (text_width, text_height), baseline = cv2.getTextSize(
                                label, cv2.FONT_HERSHEY_SIMPLEX, font_scale, thickness
                            )

                            # Draw background rectangle
                            padding = 5
                            cv2.rectangle(annotated_frame,
                                        (x1, y1 - text_height - baseline - padding),
                                        (x1 + text_width + padding, y1),
                                        color, -1)

                            # Draw text
                            cv2.putText(annotated_frame, label,
                                      (x1 + padding//2, y1 - padding//2),
                                      cv2.FONT_HERSHEY_SIMPLEX, font_scale,
                                      (255, 255, 255), thickness)

            # Convert annotated frame to base64
            _, buffer = cv2.imencode('.jpg', annotated_frame)
            annotated_image_b64 = base64.b64encode(buffer).decode('utf-8')

            return {
                "detections": detections,
                "annotated_image": annotated_image_b64,
                "success": True,
                "message": f"Found {len(detections)} food items"
            }

        except Exception as e:
            return {
                "detections": [],
                "annotated_image": "",
                "success": False,
                "message": f"Error processing image: {str(e)}"
            }

# Initialize detector
detector = FoodDetector()

@app.route('/')
def root():
    return jsonify({"message": "Food Detection API is running!"})

@app.route('/health')
def health_check():
    return jsonify({"status": "healthy", "message": "API is running"})

@app.route('/detect', methods=['POST'])
def detect_food_in_image():
    """Detect food items in uploaded image"""
    try:
        if 'file' not in request.files:
            return jsonify({"error": "No file provided"}), 400

        file = request.files['file']
        if file.filename == '':
            return jsonify({"error": "No file selected"}), 400

        # Read image bytes
        image_bytes = file.read()

        # Detect food
        result = detector.detect_food(image_bytes)

        return jsonify(result)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/detect-base64', methods=['POST'])
def detect_food_base64():
    """Detect food items in base64 encoded image"""
    try:
        data = request.get_json()
        if not data or 'image' not in data:
            return jsonify({"error": "No image data provided"}), 400

        image_b64 = data['image']

        # Remove data URL prefix if present
        if image_b64.startswith('data:image'):
            image_b64 = image_b64.split(',')[1]

        # Decode base64
        image_bytes = base64.b64decode(image_b64)

        # Detect food
        result = detector.detect_food(image_bytes)

        return jsonify(result)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    print("🍎 Starting Food Detection Flask Server...")
    print("Backend running on http://localhost:8000")
    app.run(host='0.0.0.0', port=8000, debug=True)
