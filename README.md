# Hand Gesture Recognition using MediaPipe and OpenCV

## Description
This project is a real-time hand gesture recognition system using a webcam. It leverages MediaPipe for hand tracking, OpenCV for video processing, and Tkinter for the graphical user interface. The application can recognize several hand gestures and display the results in a user-friendly GUI. One version (`main.py`) also provides text-to-speech feedback for recognized gestures.

## Features
- Real-time hand gesture recognition via webcam
- User-friendly GUI with login screen (default: admin/1234)
- Text-to-speech feedback (in `main.py`)
- Multiple gesture detection (e.g., Peace, I, Fist, I Love You, Okay, Call, Stop, Help, Super)
- Visual feedback for left/right/both hands

## Requirements
- Python 3.11
- Webcam

### Python Packages
- opencv-python
- mediapipe
- protobuf
- pyttsx3 (for TTS, used in `main.py`)
- ttkbootstrap
- Pillow
- google.protobuf

## Installation
1. Install Python 3.11 and add it to your PATH.
2. Install dependencies:
   ```
   pip install opencv-python mediapipe protobuf pyttsx3 ttkbootstrap Pillow
   ```

## Usage
1. Run the application:
   ```
   python main.py
   ```
   or
   ```
   python final.py
   ```
2. Login with:
   - Username: `admin`
   - Password: `1234`
3. Allow webcam access and perform hand gestures in front of the camera.

## Files
- `main.py`: Main application with TTS feedback.
- `final.py`: Alternative version with additional gestures.
- `model.h5`: (If used) Pre-trained model file.
- `Req_sign.txt`: List of required packages.

## Notes
- Ensure your webcam is connected and accessible.
- The login credentials are hardcoded for demonstration purposes.
- For any issues, check that all dependencies are installed and you are using Python 3.11.
