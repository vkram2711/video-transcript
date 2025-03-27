# Video Transcription with Whisper & WebSockets

This project allows you to extract transcripts from video files using OpenAI's Whisper model running **locally**. The app provides **real-time transcription updates** via WebSockets and includes both a frontend and a backend component.

---

## Features

- Transcribes videos using OpenAI's Whisper model (runs locally)
- Real-time transcription progress updates via WebSockets
- Frontend UI to upload and view transcription in real-time
- Backend handles video processing, Whisper integration, and WebSocket communication

---

## Tech Stack

### Backend
- Python
- Flask
- WebSockets
- OpenAI Whisper (local model)

### Frontend
- React (or specify your framework)
- WebSocket client
- File upload interface and live transcription display

---

## Getting Started

### 1. Clone the Repository
```bash
git clone https://github.com/vkram2711/video-transcript.git
cd video-transcript
```

### 2. Backend Setup

#### Install dependencies
```bash
cd videoTranscribeServer
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
```

#### Run the server
```bash
python main.py
```

Make sure you have `ffmpeg` installed and available in your system path.

### 3. Frontend Setup
```bash
cd ../video-transcript-front
npm install
npm start
```

---

## How It Works
1. Upload a video file via the frontend.
2. The backend receives the file, processes it chunk-by-chunk.
3. As transcription progresses, it emits updates via WebSockets.
4. The frontend receives partial transcriptions and displays them live.


## Requirements
- Python 3.8+
- Node.js + npm
- ffmpeg installed

---

## Future Improvements
- Multi-language support
- Authentication & upload history
- More robust error handling and logging

