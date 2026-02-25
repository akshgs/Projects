# Air Drawing – Real-Time Hand Gesture Based Virtual Canvas

## Overview

Air Drawing is a real-time computer vision application that enables users to draw, change colors, and erase on a virtual canvas using hand gestures captured through a webcam.

The system leverages MediaPipe for accurate hand landmark detection and OpenCV for real-time frame processing and canvas rendering. Gesture-based interaction is implemented by analyzing the spatial relationships between finger landmarks to switch dynamically between operational modes.

This project demonstrates practical implementation of gesture-driven Human-Computer Interaction (HCI) using computer vision.

---

## Features

- Real-time hand tracking using 21 landmark points
- Draw on screen using index finger gesture
- Change drawing color using two-finger gesture
- Erase drawings using multi-finger gesture
- Smooth canvas rendering using layered frame merging
- Bitwise masking for efficient overlay processing
- Keyboard controls for clearing canvas and exiting application

---

## Technology Stack

- Python 3.x
- OpenCV
- MediaPipe
- NumPy

---

## System Workflow

1. Capture live video stream from webcam
2. Flip frame horizontally for mirror interaction
3. Detect hand landmarks using MediaPipe
4. Extract fingertip and joint coordinates
5. Determine active fingers via landmark comparison
6. Switch operational mode based on gesture
7. Render drawing or erasing on a separate NumPy canvas
8. Merge canvas with live frame using bitwise operations
9. Display final output in real time

---

## Gesture Mapping

| Gesture Configuration | Mode |
|-----------------------|------|
| Index Finger Up | Draw Mode |
| Index + Middle Finger Up | Color Selection Mode |
| Index + Middle + Ring + Pinky Up | Erase Mode |

---

## Installation

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/air-drawing.git
cd air-drawing
```
