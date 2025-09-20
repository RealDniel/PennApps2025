// Configuration
const API_BASE_URL = "http://localhost:8000";

// DOM elements
const uploadArea = document.getElementById("uploadArea");
const fileInput = document.getElementById("fileInput");
const loading = document.getElementById("loading");
const results = document.getElementById("results");
const error = document.getElementById("error");
const resultImage = document.getElementById("resultImage");
const detections = document.getElementById("detections");
const errorMessage = document.getElementById("errorMessage");

// Camera elements
const video = document.getElementById("video");
const canvas = document.getElementById("canvas");
const uploadSection = document.getElementById("uploadSection");
const cameraSection = document.getElementById("cameraSection");
const startCameraBtn = document.getElementById("startCameraBtn");
const stopCameraBtn = document.getElementById("stopCameraBtn");
const captureBtn = document.getElementById("captureBtn");
const toggleDetectionBtn = document.getElementById("toggleDetectionBtn");
const cameraStatus = document.getElementById("cameraStatus");
const detectionInfo = document.getElementById("detectionInfo");
const detectionList = document.getElementById("detectionList");

// Camera state
let stream = null;
let isDetectionEnabled = false;
let detectionInterval = null;

// Initialize event listeners
document.addEventListener("DOMContentLoaded", function () {
  setupEventListeners();
});

function setupEventListeners() {
  // File input change
  fileInput.addEventListener("change", handleFileSelect);

  // Drag and drop events
  uploadArea.addEventListener("dragover", handleDragOver);
  uploadArea.addEventListener("dragleave", handleDragLeave);
  uploadArea.addEventListener("drop", handleDrop);

  // Click to upload
  uploadArea.addEventListener("click", () => fileInput.click());
}

function handleDragOver(e) {
  e.preventDefault();
  uploadArea.classList.add("dragover");
}

function handleDragLeave(e) {
  e.preventDefault();
  uploadArea.classList.remove("dragover");
}

function handleDrop(e) {
  e.preventDefault();
  uploadArea.classList.remove("dragover");

  const files = e.dataTransfer.files;
  if (files.length > 0) {
    handleFile(files[0]);
  }
}

function handleFileSelect(e) {
  const file = e.target.files[0];
  if (file) {
    handleFile(file);
  }
}

function handleFile(file) {
  // Validate file type
  if (!file.type.startsWith("image/")) {
    showError("Please select a valid image file.");
    return;
  }

  // Validate file size (max 10MB)
  if (file.size > 10 * 1024 * 1024) {
    showError("File size too large. Please select an image smaller than 10MB.");
    return;
  }

  // Hide previous results and errors
  hideAllSections();

  // Show loading
  showLoading();

  // Process the image
  processImage(file);
}

async function processImage(file) {
  try {
    // Convert file to base64
    const base64 = await fileToBase64(file);

    // Send to backend
    const response = await fetch(`${API_BASE_URL}/detect-base64`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        image: base64
      })
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const data = await response.json();

    if (data.success) {
      displayResults(data);
    } else {
      showError(data.message || "Failed to process image");
    }
  } catch (err) {
    console.error("Error processing image:", err);
    showError(
      "Failed to connect to the server. Make sure the backend is running on port 8000."
    );
  }
}

function fileToBase64(file) {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.onload = () => resolve(reader.result);
    reader.onerror = (error) => reject(error);
    reader.readAsDataURL(file);
  });
}

function displayResults(data) {
  hideAllSections();

  // Display annotated image
  if (data.annotated_image) {
    resultImage.src = `data:image/jpeg;base64,${data.annotated_image}`;
  }

  // Display detections
  if (data.detections && data.detections.length > 0) {
    detections.innerHTML = "";

    data.detections.forEach((detection, index) => {
      const detectionElement = createDetectionElement(detection, index);
      detections.appendChild(detectionElement);
    });
  } else {
    detections.innerHTML =
      '<p style="text-align: center; color: #666; font-style: italic;">No food items detected in this image.</p>';
  }

  // Show results
  results.style.display = "block";
}

function createDetectionElement(detection, index) {
  const div = document.createElement("div");
  div.className = "detection-item";

  const confidencePercentage = Math.round(detection.confidence * 100);

  div.innerHTML = `
        <div class="detection-header">
            <span class="food-name">${detection.food_name}</span>
            <span class="confidence">${confidencePercentage}% confidence</span>
        </div>
        ${
          detection.carbon_footprint_info
            ? `
            <div class="carbon-info">
                <h4>🌱 Carbon Footprint Information</h4>
                <p>${detection.carbon_footprint_info}</p>
            </div>
        `
            : `
            <div class="carbon-info">
                <h4>🌱 Carbon Footprint Information</h4>
                <p>Carbon footprint information is being processed. Please wait a moment and try again.</p>
            </div>
        `
        }
    `;

  return div;
}

function showLoading() {
  loading.style.display = "block";
}

function showError(message) {
  hideAllSections();
  errorMessage.textContent = message;
  error.style.display = "block";
}

function hideAllSections() {
  loading.style.display = "none";
  results.style.display = "none";
  error.style.display = "none";
}

// Utility function to check if backend is running
async function checkBackendHealth() {
  try {
    const response = await fetch(`${API_BASE_URL}/health`);
    return response.ok;
  } catch (error) {
    return false;
  }
}

// Check backend health on page load
document.addEventListener("DOMContentLoaded", async function () {
  const isHealthy = await checkBackendHealth();
  if (!isHealthy) {
    console.warn(
      "Backend server is not responding. Make sure it's running on port 8000."
    );
  }
});

// Mode switching
function switchMode(mode) {
  const uploadModeBtn = document.getElementById("uploadModeBtn");
  const cameraModeBtn = document.getElementById("cameraModeBtn");

  if (mode === "upload") {
    uploadModeBtn.classList.add("active");
    cameraModeBtn.classList.remove("active");
    uploadSection.style.display = "block";
    cameraSection.style.display = "none";
    stopCamera(); // Stop camera if running
  } else if (mode === "camera") {
    uploadModeBtn.classList.remove("active");
    cameraModeBtn.classList.add("active");
    uploadSection.style.display = "none";
    cameraSection.style.display = "block";
  }
}

// Camera functions
async function startCamera() {
  try {
    updateCameraStatus("Starting camera...", "loading");

    const constraints = {
      video: {
        width: { ideal: 640 },
        height: { ideal: 480 },
        facingMode: "environment" // Use back camera on mobile
      }
    };

    stream = await navigator.mediaDevices.getUserMedia(constraints);
    video.srcObject = stream;

    video.onloadedmetadata = () => {
      updateCameraStatus("Camera ready", "active");
      startCameraBtn.style.display = "none";
      stopCameraBtn.style.display = "inline-block";
      captureBtn.style.display = "inline-block";
      toggleDetectionBtn.style.display = "inline-block";
    };
  } catch (err) {
    console.error("Error accessing camera:", err);
    updateCameraStatus("Camera access denied or not available", "error");

    if (err.name === "NotAllowedError") {
      alert("Camera access denied. Please allow camera access and try again.");
    } else if (err.name === "NotFoundError") {
      alert("No camera found. Please connect a camera and try again.");
    } else {
      alert("Error accessing camera: " + err.message);
    }
  }
}

function stopCamera() {
  if (stream) {
    stream.getTracks().forEach((track) => track.stop());
    stream = null;
  }

  video.srcObject = null;
  updateCameraStatus("Camera stopped", "");

  startCameraBtn.style.display = "inline-block";
  stopCameraBtn.style.display = "none";
  captureBtn.style.display = "none";
  toggleDetectionBtn.style.display = "none";

  // Stop detection if running
  if (detectionInterval) {
    clearInterval(detectionInterval);
    detectionInterval = null;
    isDetectionEnabled = false;
  }

  // Clear detection info
  clearDetectionInfo();
}

function captureImage() {
  if (!stream) {
    alert("Please start the camera first");
    return;
  }

  // Hide previous results
  hideAllSections();
  showLoading();

  // Capture current frame
  const context = canvas.getContext("2d");
  canvas.width = video.videoWidth;
  canvas.height = video.videoHeight;
  context.drawImage(video, 0, 0);

  // Convert to blob and process
  canvas.toBlob(
    async (blob) => {
      try {
        const base64 = await blobToBase64(blob);
        await processImageFromBase64(base64);
      } catch (err) {
        console.error("Error processing captured image:", err);
        showError("Failed to process captured image");
      }
    },
    "image/jpeg",
    0.8
  );
}

function toggleDetection() {
  if (!stream) {
    alert("Please start the camera first");
    return;
  }

  isDetectionEnabled = !isDetectionEnabled;

  if (isDetectionEnabled) {
    updateCameraStatus("Real-time detection enabled", "active");
    toggleDetectionBtn.textContent = "🔍 Stop Detection";

    // Start detection every 2 seconds
    detectionInterval = setInterval(async () => {
      if (isDetectionEnabled && stream) {
        try {
          await performRealTimeDetection();
        } catch (err) {
          console.error("Detection error:", err);
        }
      }
    }, 2000);
  } else {
    updateCameraStatus("Real-time detection disabled", "");
    toggleDetectionBtn.textContent = "🔍 Toggle Detection";

    if (detectionInterval) {
      clearInterval(detectionInterval);
      detectionInterval = null;
    }
  }
}

async function performRealTimeDetection() {
  if (!stream) return;

  // Capture current frame
  const context = canvas.getContext("2d");
  canvas.width = video.videoWidth;
  canvas.height = video.videoHeight;
  context.drawImage(video, 0, 0);

  // Convert to base64
  const base64 = await new Promise((resolve) => {
    canvas.toBlob(
      (blob) => {
        const reader = new FileReader();
        reader.onload = () => resolve(reader.result);
        reader.readAsDataURL(blob);
      },
      "image/jpeg",
      0.7
    );
  });

  try {
    const response = await fetch(`${API_BASE_URL}/detect-base64`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        image: base64
      })
    });

    if (response.ok) {
      const data = await response.json();
      if (data.success && data.detections && data.detections.length > 0) {
        // Show brief notification of detections
        updateCameraStatus(
          `Detected ${data.detections.length} food item(s)`,
          "active"
        );

        // Update detection info panel
        updateDetectionInfo(data.detections);

        // Show results after a short delay
        setTimeout(() => {
          displayResults(data);
        }, 1000);
      } else {
        // Clear detection info if no detections
        clearDetectionInfo();
      }
    }
  } catch (err) {
    console.error("Real-time detection error:", err);
  }
}

function updateCameraStatus(message, type = "") {
  cameraStatus.textContent = message;
  cameraStatus.className = `camera-status ${type}`;
}

function updateDetectionInfo(detections) {
  if (!detections || detections.length === 0) {
    clearDetectionInfo();
    return;
  }

  detectionList.innerHTML = "";

  detections.forEach((detection, index) => {
    const confidence = detection.confidence;
    const foodName = detection.food_name;
    const confidencePercentage = Math.round(confidence * 100);

    // Determine confidence class
    let confidenceClass = "low-confidence";
    if (confidence > 0.8) {
      confidenceClass = "high-confidence";
    } else if (confidence > 0.6) {
      confidenceClass = "medium-confidence";
    }

    const detectionItem = document.createElement("div");
    detectionItem.className = `detection-item-mini ${confidenceClass}`;
    detectionItem.innerHTML = `
      <span class="detection-name">${index + 1}. ${foodName}</span>
      <span class="detection-confidence">${confidencePercentage}%</span>
    `;

    detectionList.appendChild(detectionItem);
  });

  detectionInfo.style.display = "block";
}

function clearDetectionInfo() {
  detectionList.innerHTML = "";
  detectionInfo.style.display = "none";
}

function blobToBase64(blob) {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.onload = () => resolve(reader.result);
    reader.onerror = (error) => reject(error);
    reader.readAsDataURL(blob);
  });
}

async function processImageFromBase64(base64) {
  try {
    const response = await fetch(`${API_BASE_URL}/detect-base64`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        image: base64
      })
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const data = await response.json();

    if (data.success) {
      displayResults(data);
    } else {
      showError(data.message || "Failed to process image");
    }
  } catch (err) {
    console.error("Error processing image:", err);
    showError(
      "Failed to connect to the server. Make sure the backend is running on port 8000."
    );
  }
}
