from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import cv2
import numpy as np
from ultralytics import YOLO
import io
from PIL import Image
import base64
import uvicorn
from typing import List, Dict, Any
import os

app = FastAPI(title="Food Detection API", version="1.0.0")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Next.js default port
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class FoodDetector:
    def __init__(self, confidence_threshold=0.5):
        """Initialize the YOLO model for food detection"""
        # Load YOLOv8 model
        model_path = os.path.join("..", "yolov8n.pt")  # Go up one directory to find the model
        self.model = YOLO(model_path)
        self.confidence_threshold = confidence_threshold

        # Food-related items from COCO dataset
        self.food_items = {
            39: 'bottle', 40: 'wine glass', 41: 'cup', 42: 'fork', 43: 'knife', 44: 'spoon', 45: 'bowl',
            46: 'banana', 47: 'apple', 48: 'sandwich', 49: 'orange', 50: 'broccoli', 51: 'carrot',
            52: 'hot dog', 53: 'pizza', 54: 'donut', 55: 'cake'
        }

    def detect_food(self, image: np.ndarray) -> Dict[str, Any]:
        """Detect food items in the image and return results"""
        # Run YOLO detection
        results = self.model(image, verbose=False)
        
        detections = []
        annotated_image = image.copy()

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
                        
                        # Draw bounding box
                        cv2.rectangle(annotated_image, (x1, y1), (x2, y2), color, 3)
                        
                        # Prepare label text
                        food_name = self.food_items[class_id].replace('_', ' ').title()
                        label = f"{food_name}: {confidence:.1%}"
                        
                        # Get text size for background rectangle
                        font_scale = 0.7
                        thickness = 2
                        (text_width, text_height), baseline = cv2.getTextSize(
                            label, cv2.FONT_HERSHEY_SIMPLEX, font_scale, thickness
                        )
                        
                        # Draw background rectangle for text
                        padding = 5
                        cv2.rectangle(annotated_image,
                                    (x1, y1 - text_height - baseline - padding),
                                    (x1 + text_width + padding, y1),
                                    color, -1)
                        
                        # Draw text
                        cv2.putText(annotated_image, label,
                                  (x1 + padding//2, y1 - padding//2),
                                  cv2.FONT_HERSHEY_SIMPLEX, font_scale,
                                  (255, 255, 255), thickness)
                        
                        # Add detection to results
                        detections.append({
                            "class_id": class_id,
                            "class_name": self.food_items[class_id],
                            "confidence": confidence,
                            "bbox": {
                                "x1": int(x1),
                                "y1": int(y1),
                                "x2": int(x2),
                                "y2": int(y2)
                            }
                        })
        
        return {
            "detections": detections,
            "annotated_image": annotated_image,
            "total_detections": len(detections)
        }

# Initialize the detector
detector = FoodDetector()

@app.get("/")
async def root():
    return {"message": "Food Detection API is running!"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "model_loaded": True}

@app.post("/detect")
async def detect_food_in_image(file: UploadFile = File(...)):
    """Detect food items in uploaded image"""
    try:
        # Validate file type
        if not file.content_type.startswith("image/"):
            raise HTTPException(status_code=400, detail="File must be an image")
        
        # Read image data
        image_data = await file.read()
        
        # Convert to OpenCV format
        image = Image.open(io.BytesIO(image_data))
        image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
        
        # Detect food items
        results = detector.detect_food(image)
        
        # Convert annotated image back to base64 for response
        _, buffer = cv2.imencode('.jpg', results["annotated_image"])
        annotated_image_b64 = base64.b64encode(buffer).decode('utf-8')
        
        return JSONResponse(content={
            "success": True,
            "detections": results["detections"],
            "total_detections": results["total_detections"],
            "annotated_image": f"data:image/jpeg;base64,{annotated_image_b64}"
        })
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing image: {str(e)}")

@app.post("/detect-base64")
async def detect_food_base64(data: dict):
    """Detect food items in base64 encoded image"""
    try:
        # Extract base64 data
        if "image" not in data:
            raise HTTPException(status_code=400, detail="No image data provided")
        
        # Remove data URL prefix if present
        image_data = data["image"]
        if image_data.startswith("data:image"):
            image_data = image_data.split(",")[1]
        
        # Decode base64 image
        image_bytes = base64.b64decode(image_data)
        image = Image.open(io.BytesIO(image_bytes))
        image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
        
        # Detect food items
        results = detector.detect_food(image)
        
        # Convert annotated image back to base64
        _, buffer = cv2.imencode('.jpg', results["annotated_image"])
        annotated_image_b64 = base64.b64encode(buffer).decode('utf-8')
        
        return JSONResponse(content={
            "success": True,
            "detections": results["detections"],
            "total_detections": results["total_detections"],
            "annotated_image": f"data:image/jpeg;base64,{annotated_image_b64}"
        })
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing image: {str(e)}")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
