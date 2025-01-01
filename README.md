# People Counter - Deep Remaster AI

The definitive version of the People Counter project, transformed into a professional-grade analytics tool using state-of-the-art AI.

## Deep Remaster Features
- **Full Person Detection**: Upgraded from simple face detection to **MediaPipe Object Detection**. This reliably detects the entire human figure from any angle, even if the face is hidden.
- **Persistent Analytics**: Automatically logs every session to `logs/traffic.csv` with precise timestamps, tracking session totals, current occupancy, and peak traffic counts.
- **advanced Statistics**: Real-time tracking of:
    - **Current Count**: Number of people in the frame right now.
    - **Peak Count**: The highest number of people detected since the session started.
    - **Session Total**: Cumulative number of unique people detected during the session.
- **Stylized HUD**: A high-contrast Heads-Up Display for clear data visualization.
- **Modular Architecture**: Clean, thread-safe Python package structure.

## Project Structure
```text
people-counter-remastered/
├── src/
│   ├── core/           # AI Detection (Multi-person support)
│   ├── audio/          # Threaded Voice Engine
│   ├── utils/          # UI Helpers & Persistent Logger
│   └── app.py          # Main AI Control Center
├── logs/               # Persistent data logs (CSV)
├── requirements.txt    # Project dependencies
└── README.md           # Documentation
```

## Installation
1. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage
Launch the AI Control Center:
```bash
python src/app.py
```
- **Option 1**: Deep analysis of a static image.
- **Option 2**: Real-time live analytics via webcam.
- **Press 'q'**: Exit gracefully and save the session log.

## Technologies
- **Python 3**
- **MediaPipe** (High-fidelity Person Detection)
- **OpenCV** (Real-time Vision)
- **gTTS & Pygame** (Asynchronous Audio)
- **CSV Data Persistence**
