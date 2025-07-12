# EduTrack - Complete Educational Monitoring System

A comprehensive educational monitoring system with real-time engagement tracking, voice-to-video transcript generation, and teacher dashboard management.

[!Watch the Demo Video](output/demo%20video.mp4)

## 🏗️ System Architecture

The EduTrack system consists of three main components:

1. **📊 Classroom Engagement Monitor** (`clr_engage_montr/`) - Real-time face detection and engagement tracking
2. **🎓 Teacher Dashboard** (`teacher-dashboard/`) - Modern web interface for monitoring and analytics
3. **🎙️ Voice-to-Video Transcript** (`voice-to-video-transcript/`) - AI-powered educational video generation

## 🚀 Quick Start Guide

### Prerequisites

- **Python 3.10+** (3.10 recommended for `clr_engage_montr`, 3.13+ compatible for `voice-to-video-transcript`)
- **Node.js 18+** and npm/yarn
- **FFmpeg** (required for audio processing)
- **OpenAI API Key** (for voice-to-video features)

### 📦 Installation Steps

#### 1. Clone the Repository
```bash
git clone https://github.com/your-username/EduTrack.git
cd EduTrack
```

#### 2. Set Up Classroom Engagement Monitor
```bash
cd clr_engage_montr

# Create virtual environment (recommended)
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Start the engagement monitoring service
python -m uvicorn main:app --host 0.0.0.0 --port 8001 --reload
```

**✅ Service will be available at:** `http://localhost:8001`

#### 3. Set Up Teacher Dashboard
```bash
cd ../teacher-dashboard

# Install dependencies
npm install

# Start development server
npm run dev
```

**✅ Dashboard will be available at:** `http://localhost:3000`

#### 4. Set Up Voice-to-Video Transcript System
```bash
cd ../voice-to-video-transcript

# Create virtual environment (if not already created)
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Configure OpenAI API Key
# Create .env file and add:
# OPENAI_API_KEY=your_openai_api_key_here

# Start the voice-to-video service
python -m uvicorn api:app --host 0.0.0.0 --port 8000 --reload
```

**✅ Service will be available at:** `http://localhost:8000`

## 🔧 Detailed Setup Instructions

### System Requirements

#### For Classroom Engagement Monitor
- **Python 3.10** (recommended for optimal compatibility)
- **OpenCV** and **YOLOv8** for face detection
- **DeepSORT** for face tracking
- **FastAPI** for API endpoints

#### For Teacher Dashboard
- **Node.js 18+**
- **Next.js 14+**
- **TypeScript**
- **Tailwind CSS**

#### For Voice-to-Video Transcript
- **Python 3.13+** (compatible with older versions)
- **FFmpeg** (mandatory for audio processing)
- **OpenAI API Key**
- **Manim** (optional, for advanced animations)

### 🐍 Python Environment Setup

#### Option A: Using Virtual Environments (Recommended)
```bash
# For clr_engage_montr (Python 3.10)
cd clr_engage_montr
python3.10 -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt

# For voice-to-video-transcript (Python 3.13+)
cd ../voice-to-video-transcript
python3.13 -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
```

#### Option B: Using Conda
```bash
# For clr_engage_montr
conda create -n edutrack-monitor python=3.10
conda activate edutrack-monitor
pip install -r clr_engage_montr/requirements.txt

# For voice-to-video-transcript
conda create -n edutrack-voice python=3.13
conda activate edutrack-voice
pip install -r voice-to-video-transcript/requirements.txt
```

### 🔑 API Keys and Configuration

#### OpenAI API Setup
1. Get your API key from [OpenAI Platform](https://platform.openai.com/)
2. Create `.env` file in `voice-to-video-transcript/`:
```env
OPENAI_API_KEY=sk-your-actual-api-key-here
OPENAI_MODEL=gpt-3.5-turbo
```

#### FFmpeg Installation
```bash
# Windows (using Chocolatey)
choco install ffmpeg

# macOS (using Homebrew)
brew install ffmpeg

# Ubuntu/Debian
sudo apt update
sudo apt install ffmpeg

# Verify installation
ffmpeg -version
```

## 🚀 Running the Complete System

### Step 1: Start All Services

#### Terminal 1 - Classroom Monitor
```bash
cd clr_engage_montr
source venv/bin/activate  # Windows: venv\Scripts\activate
python -m uvicorn main:app --host 0.0.0.0 --port 8001 --reload
```

#### Terminal 2 - Teacher Dashboard
```bash
cd teacher-dashboard
npm run dev
```

#### Terminal 3 - Voice-to-Video Service
```bash
cd voice-to-video-transcript
source venv/bin/activate  # Windows: venv\Scripts\activate
python -m uvicorn api:app --host 0.0.0.0 --port 8000 --reload
```

### Step 2: Access the System

1. **Teacher Dashboard**: [http://localhost:3000](http://localhost:3000)
2. **Engagement Monitor API**: [http://localhost:8001](http://localhost:8001)
3. **Voice-to-Video API**: [http://localhost:8000](http://localhost:8000)
4. **API Documentation**: 
   - Engagement: [http://localhost:8001/docs](http://localhost:8001/docs)
   - Voice-to-Video: [http://localhost:8000/docs](http://localhost:8000/docs)

## 📊 System Features

### Classroom Engagement Monitor
- **Real-time face detection** using YOLOv8
- **Engagement scoring** based on facial expressions
- **Attendance tracking** with face recognition
- **REST API** for data access

### Teacher Dashboard
- **Live KPI monitoring** (attendance, engagement)
- **Interactive charts** and visualizations
- **Session management** and video playback
- **Transcript management** with subject categorization
- **System health monitoring**

### Voice-to-Video Transcript
- **Real-time audio recording** with browser integration
- **AI-powered transcription** using OpenAI Whisper
- **Educational script generation** with GPT-4
- **3Blue1Brown-style animations** using Manim
- **PDF transcript generation**

## 🧪 Testing the System

### 1. Test Engagement Monitor
```bash
curl http://localhost:8001/api/classroom/realtime
```

### 2. Test Voice Recording
- Open [http://localhost:8000](http://localhost:8000)
- Navigate to the recording interface
- Test start/stop recording functionality

### 3. Test Dashboard Integration
- Open [http://localhost:3000](http://localhost:3000)
- Check live KPI updates
- Verify chart data integration

## 🔧 Troubleshooting

### Common Issues

#### Python Version Compatibility
```bash
# Check Python version
python --version

# For clr_engage_montr - use Python 3.10
python3.10 -m venv venv

# For voice-to-video-transcript - Python 3.13+ compatible
python3.13 -m venv venv
```

#### FFmpeg Issues
```bash
# Test FFmpeg installation
ffmpeg -version

# If not found, install based on your OS (see installation section above)
```

#### Port Conflicts
```bash
# Check if ports are in use
netstat -an | grep :8000
netstat -an | grep :8001
netstat -an | grep :3000

# Kill processes if needed
# Windows: taskkill /F /PID <PID>
# macOS/Linux: kill -9 <PID>
```

#### Module Import Errors
```bash
# Make sure virtual environment is activated
source venv/bin/activate  # or venv\Scripts\activate

# Reinstall requirements
pip install -r requirements.txt
```

### Service-Specific Issues

#### Engagement Monitor
- **Camera access**: Ensure camera permissions are granted
- **Model loading**: YOLOv8 models will download on first run
- **Performance**: Adjust `test_video3.mp4` path in `main.py` for testing

#### Voice-to-Video Service
- **Audio recording**: Check microphone permissions
- **API quotas**: Monitor OpenAI API usage
- **Python 3.13+**: Ensure FFmpeg is in system PATH

## 📁 Project Structure

```
EduTrack/
├── clr_engage_montr/           # Engagement monitoring service
│   ├── main.py                 # FastAPI server
│   ├── models/                 # AI models (face detection, tracking, etc.)
│   ├── requirements.txt        # Python dependencies
│   └── test_images/           # Test video files
├── teacher-dashboard/          # Next.js web interface
│   ├── src/                   # Source code
│   ├── package.json           # Node.js dependencies
│   └── tailwind.config.ts     # Styling configuration
├── voice-to-video-transcript/  # Voice processing service
│   ├── api.py                 # FastAPI server
│   ├── audio_recorder.py      # Real-time recording
│   ├── requirements.txt       # Python dependencies
│   └── .env                   # Environment variables
└── README.md                  # This file
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Commit your changes (`git commit -m 'Add amazing feature'`)
5. Push to the branch (`git push origin feature/amazing-feature`)
6. Open a Pull Request

## 📞 Support

For issues and questions:
- Check the troubleshooting section above
- Review individual component documentation
- Open an issue on GitHub

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

**Built with ❤️ for educational technology advancement**