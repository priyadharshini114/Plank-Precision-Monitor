# Plank-Precision-Monitor

**Plank Precision Monitor** is a real-time application designed to evaluate and enhance plank exercises using pose estimation technology. It provides detailed feedback on body alignment and tracks the duration of the plank position.

## Description

This project uses MediaPipe to analyze plank exercises from video input. It calculates body angles to ensure proper form, tracks the duration of the plank position, and provides real-time feedback on posture accuracy.

## Features

- Real-time pose estimation
- Accurate angle calculation for body alignment
- Plank duration tracking with start and end times
- Summary of total plank time at the end of the video

## Requirements

Install the required packages using:
```bash
pip install -r requirements.txt
```

**requirements.txt:**
- `opencv-python`
- `mediapipe`
- `numpy`

## Key Components

- **Pose Estimation**: Uses MediaPipe for body landmark detection.
- **Angle Calculation**: Determines angles between shoulder, hip, and ankle for posture assessment.
- **Real-time Feedback**: Displays current plank position and elapsed time.
- **Final Summary**: Shows total plank duration after video playback.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for enhancements or bug fixes.
