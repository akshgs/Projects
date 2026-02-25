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

Problems Faced During Development

Inconsistent Gesture Detection

Finger detection sometimes failed under different lighting conditions.

Rapid hand movement caused unstable landmark tracking.

False Mode Switching

Slight finger bends were misclassified as different gestures.

Lack of palm orientation filtering caused incorrect activation.

Drawing Jitter

Small fluctuations in fingertip position created shaky lines.

No smoothing mechanism was initially implemented.

Performance Constraints

Higher resolution frames reduced FPS.

Real-time processing required optimization.

Limitations

Single-hand tracking only

Fixed brush thickness

No palm direction validation

No drawing save/export functionality

Gesture recognition based only on simple landmark comparison

Sensitive to lighting conditions

How These Limitations Can Be Overcome

Improve Gesture Accuracy

Implement palm orientation detection.

Add angle-based finger validation instead of simple coordinate comparison.

Reduce Drawing Jitter

Apply smoothing techniques (e.g., moving average filter).

Implement Kalman filtering for stable fingertip tracking.

Improve Performance

Resize frames before processing.

Optimize drawing logic and reduce unnecessary calculations.

Enhance Functionality

Add multi-hand support.

Add dynamic brush thickness control.

Implement save/export feature.

Integrate UI-based color palette.

Learning Outcomes

This project strengthens understanding of:

Real-time computer vision pipelines

Landmark-based gesture detection

Bitwise image compositing

Performance optimization in live systems

Designing gesture-driven user interfaces
