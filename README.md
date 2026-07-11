# AI-Bicep-Curl-Counter

A real-time exercise form tracker and rep counter built with OpenCV and MediaPipe Pose. 
The app uses your webcam to detect body landmarks, calculates joint angles (e.g., elbow 
angle for bicep curls), and automatically counts repetitions based on movement thresholds.

## Features
- Real-time pose detection via webcam
- Joint angle calculation using landmark coordinates
- Automatic rep counting based on angle thresholds
- Visual skeleton overlay with OpenCV

## Tech Stack
- Python
- OpenCV
- MediaPipe (Pose Solutions API)
- NumPy

## Requirements
- Python 3.11 or 3.12 (MediaPipe's legacy Solutions API — `mp.solutions.pose` — 
  does not have pre-built wheels for Python 3.13+)
- mediapipe==0.10.9

## Installation
\```bash
python -m venv venv
venv\Scripts\activate    # Windows
source venv/bin/activate # macOS/Linux

pip install mediapipe==0.10.9 opencv-python numpy
\```

## Usage
\```bash
python main.py
\```
Press `q` to quit the webcam feed.

## How it works
1. OpenCV captures live video from the webcam
2. Each frame is passed to MediaPipe's Pose model, which detects 33 body landmarks
3. Landmark coordinates (shoulder, elbow, wrist) are used to calculate joint angles
4. Angle thresholds determine rep completion (e.g., arm extended → curled → extended)

## Troubleshooting
If you get `NameError: name 'mp_pose' is not defined` or 
`AttributeError: module 'mediapipe' has no attribute 'solutions'`, 
it usually means you're on Python 3.13+, which MediaPipe's legacy 
Solutions API doesn't support. Use Python 3.11 or 3.12 in a virtual 
environment as shown above.
