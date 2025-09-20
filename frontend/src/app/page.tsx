'use client';

import { useState, useRef, useCallback, useEffect } from 'react';
import Image from 'next/image';

interface Detection {
  class_id: number;
  class_name: string;
  confidence: number;
  bbox: {
    x1: number;
    y1: number;
    x2: number;
    y2: number;
  };
}

interface DetectionResult {
  success: boolean;
  detections: Detection[];
  total_detections: number;
  annotated_image: string;
}

export default function Home() {
  const [isDetecting, setIsDetecting] = useState(false);
  const [result, setResult] = useState<DetectionResult | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [isCameraActive, setIsCameraActive] = useState(false);
  const [isRealTimeMode, setIsRealTimeMode] = useState(false);
  const [currentDetections, setCurrentDetections] = useState<Detection[]>([]);
  const videoRef = useRef<HTMLVideoElement>(null);
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const streamRef = useRef<MediaStream | null>(null);
  const detectionIntervalRef = useRef<NodeJS.Timeout | null>(null);

  const startCamera = useCallback(async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ 
        video: { 
          width: { ideal: 640 },
          height: { ideal: 480 }
        } 
      });
      
      if (videoRef.current) {
        videoRef.current.srcObject = stream;
        streamRef.current = stream;
        setIsCameraActive(true);
        setError(null);
      }
    } catch (err) {
      setError('Failed to access camera. Please check permissions.');
      console.error('Camera error:', err);
    }
  }, []);

  const stopCamera = useCallback(() => {
    if (streamRef.current) {
      streamRef.current.getTracks().forEach(track => track.stop());
      streamRef.current = null;
    }
    setIsCameraActive(false);
    setIsRealTimeMode(false);
    setCurrentDetections([]);
    
    // Clear any running detection interval
    if (detectionIntervalRef.current) {
      clearInterval(detectionIntervalRef.current);
      detectionIntervalRef.current = null;
    }
  }, []);

  const performDetection = useCallback(async (updateCurrentDetections = false) => {
    if (!videoRef.current || !canvasRef.current) return;

    const video = videoRef.current;
    const canvas = canvasRef.current;
    const ctx = canvas.getContext('2d');

    if (!ctx) return;

    // Set canvas size to match video
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;

    // Draw current video frame to canvas
    ctx.drawImage(video, 0, 0, canvas.width, canvas.height);

    // Convert canvas to base64
    const imageData = canvas.toDataURL('image/jpeg', 0.6); // Lower quality for faster processing

    if (!updateCurrentDetections) {
      setIsDetecting(true);
    }
    setError(null);

    try {
      const response = await fetch('http://localhost:8000/detect-base64', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ image: imageData }),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data: DetectionResult = await response.json();
      
      if (updateCurrentDetections) {
        setCurrentDetections(data.detections);
      } else {
        setResult(data);
      }
    } catch (err) {
      if (!updateCurrentDetections) {
        setError('Failed to detect food items. Please try again.');
      }
      console.error('Detection error:', err);
    } finally {
      if (!updateCurrentDetections) {
        setIsDetecting(false);
      }
    }
  }, []);

  const captureAndDetect = useCallback(async () => {
    await performDetection(false);
  }, [performDetection]);

  const startRealTimeDetection = useCallback(() => {
    if (detectionIntervalRef.current) return; // Already running
    
    setIsRealTimeMode(true);
    setCurrentDetections([]);
    
    // Perform detection every 1 second for real-time feel
    detectionIntervalRef.current = setInterval(() => {
      performDetection(true);
    }, 1000);
  }, [performDetection]);

  const stopRealTimeDetection = useCallback(() => {
    if (detectionIntervalRef.current) {
      clearInterval(detectionIntervalRef.current);
      detectionIntervalRef.current = null;
    }
    setIsRealTimeMode(false);
    setCurrentDetections([]);
  }, []);

  const handleFileUpload = useCallback(async (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (!file) return;

    setIsDetecting(true);
    setError(null);

    try {
      const formData = new FormData();
      formData.append('file', file);

      const response = await fetch('http://localhost:8000/detect', {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data: DetectionResult = await response.json();
      setResult(data);
    } catch (err) {
      setError('Failed to detect food items. Please try again.');
      console.error('Detection error:', err);
    } finally {
      setIsDetecting(false);
    }
  }, []);

  // Cleanup effect
  useEffect(() => {
    return () => {
      if (detectionIntervalRef.current) {
        clearInterval(detectionIntervalRef.current);
      }
      if (streamRef.current) {
        streamRef.current.getTracks().forEach(track => track.stop());
      }
    };
  }, []);

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      <div className="container mx-auto px-4 py-8">
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold text-gray-800 mb-4">
            🍎 Food Detection App
          </h1>
          <p className="text-lg text-gray-600">
            Detect food items in real-time using AI-powered computer vision
          </p>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Camera Section */}
          <div className="bg-white rounded-lg shadow-lg p-6">
            <h2 className="text-2xl font-semibold mb-4 text-gray-800">
              📷 Live Camera Detection
            </h2>
            
            <div className="space-y-4">
              <div className="relative bg-gray-100 rounded-lg overflow-hidden">
                <video
                  ref={videoRef}
                  autoPlay
                  playsInline
                  muted
                  className="w-full h-64 object-cover"
                  style={{ display: isCameraActive ? 'block' : 'none' }}
                />
                {!isCameraActive && (
                  <div className="w-full h-64 flex items-center justify-center text-gray-500">
                    <div className="text-center">
                      <div className="text-4xl mb-2">📹</div>
                      <p>Camera not active</p>
                    </div>
                  </div>
                )}
                
                {/* Real-time detection overlay */}
                {isRealTimeMode && isCameraActive && (
                  <div className="absolute top-2 left-2 right-2">
                    <div className="bg-black bg-opacity-70 text-white p-2 rounded-lg">
                      <div className="flex items-center justify-between mb-1">
                        <span className="text-sm font-semibold">🎥 Real-time Detection</span>
                        <span className="text-xs text-green-400">● LIVE</span>
                      </div>
                      {currentDetections.length > 0 ? (
                        <div className="space-y-1">
                          {currentDetections.map((detection, index) => (
                            <div key={index} className="text-xs flex justify-between">
                              <span className="font-medium">
                                {detection.class_name.replace('_', ' ').toUpperCase()}
                              </span>
                              <span className="text-green-400">
                                {(detection.confidence * 100).toFixed(0)}%
                              </span>
                            </div>
                          ))}
                        </div>
                      ) : (
                        <div className="text-xs text-gray-300">
                          Point camera at food items...
                        </div>
                      )}
                    </div>
                  </div>
                )}
              </div>

              <canvas ref={canvasRef} className="hidden" />

              <div className="space-y-2">
                {!isCameraActive ? (
                  <button
                    onClick={startCamera}
                    className="w-full bg-green-500 hover:bg-green-600 text-white font-semibold py-2 px-4 rounded-lg transition-colors"
                  >
                    Start Camera
                  </button>
                ) : (
                  <div className="space-y-2">
                    <div className="flex gap-2">
                      {!isRealTimeMode ? (
                        <button
                          onClick={startRealTimeDetection}
                          className="flex-1 bg-purple-500 hover:bg-purple-600 text-white font-semibold py-2 px-4 rounded-lg transition-colors"
                        >
                          🎥 Start Real-time Detection
                        </button>
                      ) : (
                        <button
                          onClick={stopRealTimeDetection}
                          className="flex-1 bg-orange-500 hover:bg-orange-600 text-white font-semibold py-2 px-4 rounded-lg transition-colors"
                        >
                          ⏸️ Stop Real-time Detection
                        </button>
                      )}
                      <button
                        onClick={captureAndDetect}
                        disabled={isDetecting || isRealTimeMode}
                        className="flex-1 bg-blue-500 hover:bg-blue-600 disabled:bg-gray-400 text-white font-semibold py-2 px-4 rounded-lg transition-colors"
                      >
                        {isDetecting ? 'Detecting...' : '📸 Single Detection'}
                      </button>
                    </div>
                    <button
                      onClick={stopCamera}
                      className="w-full bg-red-500 hover:bg-red-600 text-white font-semibold py-2 px-4 rounded-lg transition-colors"
                    >
                      Stop Camera
                    </button>
                  </div>
                )}
              </div>
            </div>
          </div>

          {/* File Upload Section */}
          <div className="bg-white rounded-lg shadow-lg p-6">
            <h2 className="text-2xl font-semibold mb-4 text-gray-800">
              📁 Upload Image
            </h2>
            
            <div className="space-y-4">
              <div className="border-2 border-dashed border-gray-300 rounded-lg p-8 text-center">
                <div className="text-4xl mb-4">📸</div>
                <p className="text-gray-600 mb-4">
                  Upload an image to detect food items
                </p>
                <input
                  type="file"
                  accept="image/*"
                  onChange={handleFileUpload}
                  disabled={isDetecting}
                  className="block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-lg file:border-0 file:text-sm file:font-semibold file:bg-blue-50 file:text-blue-700 hover:file:bg-blue-100"
                />
              </div>
            </div>
          </div>
        </div>

        {/* Results Section */}
        {(result || error) && (
          <div className="mt-8 bg-white rounded-lg shadow-lg p-6">
            <h2 className="text-2xl font-semibold mb-4 text-gray-800">
              🔍 Detection Results
            </h2>
            
            {error && (
              <div className="bg-red-50 border border-red-200 rounded-lg p-4 mb-4">
                <p className="text-red-800">{error}</p>
              </div>
            )}

            {result && (
              <div className="space-y-4">
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div>
                    <h3 className="text-lg font-semibold mb-2">Detected Items</h3>
                    <div className="space-y-2">
                      {result.detections.length > 0 ? (
                        result.detections.map((detection, index) => (
                          <div key={index} className="bg-green-50 border border-green-200 rounded-lg p-3">
                            <div className="flex justify-between items-center">
                              <span className="font-medium text-green-800">
                                {detection.class_name.replace('_', ' ').toUpperCase()}
                              </span>
                              <span className="text-sm text-green-600">
                                {(detection.confidence * 100).toFixed(1)}%
                              </span>
                            </div>
                          </div>
                        ))
                      ) : (
                        <p className="text-gray-500">No food items detected</p>
                      )}
                    </div>
                  </div>
                  
                  <div>
                    <h3 className="text-lg font-semibold mb-2">Annotated Image</h3>
                    {result.annotated_image && (
                      <div className="relative">
                        <Image
                          src={result.annotated_image}
                          alt="Detection result"
                          width={400}
                          height={300}
                          className="rounded-lg border border-gray-200"
                        />
                      </div>
                    )}
                  </div>
                </div>
                
                <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
                  <p className="text-blue-800">
                    <strong>Total detections:</strong> {result.total_detections}
                  </p>
                </div>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
}