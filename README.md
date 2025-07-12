# 🎓 EduTrack - Complete Educational Monitoring System

[![Build Status](https://img.shields.io/badge/build-passing-brightgreen)](https://github.com/nishant-sheoran/EduTrack)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Node.js 18+](https://img.shields.io/badge/node.js-18+-green.svg)](https://nodejs.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=flat&logo=fastapi)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-20232A?style=flat&logo=react&logoColor=61DAFB)](https://reactjs.org/)
[![TypeScript](https://img.shields.io/badge/TypeScript-007ACC?style=flat&logo=typescript&logoColor=white)](https://www.typescriptlang.org/)

> **A comprehensive educational monitoring system combining real-time engagement tracking, AI-powered content generation, and modern teacher dashboard analytics.**

## 🏆 **For Competition Judges - Quick Evaluation**

**Want to evaluate EduTrack immediately? We've got you covered!**

### **🚀 One-Click Setup (Recommended)**
1. **Download & Extract** this repository
2. **Windows:** Right-click `setup-edutrack.bat` → "Run as Administrator"  
   **Mac/Linux:** Run `chmod +x setup-edutrack.sh && ./setup-edutrack.sh`
3. **Wait 5-10 minutes** for automatic installation
4. **Launch:** Run `start-all.bat` (Windows) or `./start-all.sh` (Mac/Linux)
5. **Evaluate:** Browser opens automatically at http://localhost:3000

### **📋 Quick Access Points**
- **Teacher Dashboard:** http://localhost:3000 (Main evaluation interface)
- **Engagement Monitor API:** http://localhost:8001/docs (Computer vision demo)
- **Voice-to-Video API:** http://localhost:8000/docs (AI content generation)

### **🆘 If Setup Issues Occur**
- **Run:** `python test-system.py` to validate system health
- **Fallback:** Pre-recorded demo at `report&output/demo video.mp4`
- **Support:** Check [JUDGE_QUICK_START.md](JUDGE_QUICK_START.md) for troubleshooting

---

## 🚀 **What is EduTrack?**

EduTrack is a **next-generation educational technology platform** that transforms traditional classrooms into smart, data-driven learning environments. By combining **computer vision**, **artificial intelligence**, and **modern web technologies**, EduTrack provides educators with unprecedented insights into student engagement while automating educational content creation.

### **🎯 Key Value Propositions**

- **📊 Real-time Engagement Analytics**: Monitor student attention, emotions, and participation live
- **🎬 AI-Powered Content Generation**: Transform voice recordings into 3Blue1Brown-style educational videos
- **📈 Comprehensive Teacher Dashboard**: Beautiful, responsive analytics interface with live KPIs
- **🔄 Seamless Integration**: Three interconnected modules working in harmony
- **⚡ Modern Architecture**: Built with cutting-edge technologies and best practices

---

## 🏗️ **System Architecture**

EduTrack follows a **microservices architecture** with three independent, scalable modules:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                            EduTrack System                                  │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐        │
│  │   📊 Classroom   │    │   🎓 Teacher    │    │  🎙️ Voice-to-   │        │
│  │   Engagement    │    │    Dashboard    │    │  Video System   │        │
│  │    Monitor      │    │                 │    │                 │        │
│  │                 │    │                 │    │                 │        │
│  │  • YOLOv8 Face  │    │  • Next.js UI   │    │  • OpenAI API   │        │
│  │  • OpenVINO ML  │    │  • Live KPIs    │    │  • Manim Animations│      │
│  │  • FastAPI      │    │  • Real-time    │    │  • MoviePy      │        │
│  │                 │    │                 │    │                 │        │
│  │  Port: 8001     │    │  Port: 3000     │    │  Port: 8000     │        │
│  └─────────────────┘    └─────────────────┘    └─────────────────┘        │
│           │                       │                       │                │
│           └───────────────────────┼───────────────────────┘                │
│                                   │                                        │
│                         ┌─────────▼─────────┐                             │
│                         │   Data Flow Hub   │                             │
│                         │                   │                             │
│                         │ • Live Analytics  │                             │
│                         │ • Session Data    │                             │
│                         │ • Content URLs    │                             │
│                         └───────────────────┘                             │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 🎯 **Core Features**

### 1. 📊 **Classroom Engagement Monitor**

**Real-time AI-powered student engagement tracking**

- **🎯 Face Detection**: YOLOv8-powered real-time face detection with ONNX optimization
- **👥 Attendance Tracking**: Automated attendance using DeepSORT multi-object tracking
- **😊 Emotion Recognition**: Intel OpenVINO emotion classification (7 emotions)
- **📐 Head Pose Analysis**: 3D head pose estimation for attention measurement
- **⚡ Live API**: FastAPI endpoints for real-time data streaming

**Technology Stack**: Python, FastAPI, OpenCV, YOLOv8, OpenVINO, DeepSORT

### 2. 🎓 **Teacher Dashboard**

**Modern, responsive web interface for educators**

- **📈 Live KPIs**: Real-time attendance, engagement, and emotion metrics
- **📊 Interactive Charts**: Beautiful visualizations with Recharts
- **🎬 Video Management**: Session recording and playback capabilities
- **📝 Transcript Management**: Automated transcript categorization and download
- **⚙️ Configuration Panel**: Customizable settings and analytics controls
- **🔄 Real-time Updates**: WebSocket integration for live data streaming

**Technology Stack**: Next.js 15, React 19, TypeScript, Tailwind CSS, Recharts

### 3. 🎙️ **Voice-to-Video Transcript System**

**AI-powered educational content generation**

- **🎤 Real-time Recording**: Server-side audio recording with device auto-detection
- **📝 AI Transcription**: OpenAI Whisper for accurate speech-to-text
- **🧠 Script Generation**: GPT-4 powered educational content structuring
- **🎬 3Blue1Brown Animations**: Manim-generated mathematical visualizations
- **🎵 Natural Narration**: High-quality text-to-speech with gTTS
- **📄 PDF Generation**: LaTeX-enabled transcript documents
- **🎥 Video Composition**: MoviePy audio/video merging

**Technology Stack**: Python, FastAPI, OpenAI API, Manim, MoviePy, Streamlit

---

## 🚀 **Quick Start Guide**

### **Prerequisites**

- **Python 3.10+** (3.10 recommended for engagement monitor, 3.13+ compatible for voice system)
- **Node.js 18+** and npm/yarn
- **FFmpeg** (required for audio processing)
- **OpenAI API Key** (for voice-to-video features)

### **⚡ One-Command Setup**

```bash
# Clone the repository
git clone https://github.com/nishant-sheoran/EduTrack.git
cd EduTrack

# Run the automated setup script
# Windows: Right-click "setup-edutrack.bat" → "Run as Administrator"
# Mac/Linux: chmod +x setup-edutrack.sh && ./setup-edutrack.sh

# Wait 5-10 minutes for automatic installation
# Then run: start-all.bat (Windows) or ./start-all.sh (Mac/Linux)
```

### **📦 Manual Installation**

#### **1. Classroom Engagement Monitor**

```bash
cd clr_engage_montr

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Start the engagement monitoring service
python -m uvicorn main:app --host 0.0.0.0 --port 8001 --reload
```

**✅ Service available at**: `http://localhost:8001`

#### **2. Teacher Dashboard**

```bash
cd teacher-dashboard

# Install dependencies
npm install

# Start development server
npm run dev
```

**✅ Dashboard available at**: `http://localhost:3000`

#### **3. Voice-to-Video System**

```bash
cd voice-to-video-transcript

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure OpenAI API Key
echo "OPENAI_API_KEY=your_api_key_here" > .env

# Start the voice-to-video service
python -m uvicorn api:app --host 0.0.0.0 --port 8000 --reload
```

**✅ Service available at**: `http://localhost:8000`

---

## 🔧 **Configuration**

### **Environment Variables**

Create `.env` files in the respective directories:

#### **Voice-to-Video System** (`voice-to-video-transcript/.env`)
```env
OPENAI_API_KEY=sk-your-openai-api-key-here
OPENAI_MODEL=gpt-4
WHISPER_MODEL=whisper-1
```

#### **Teacher Dashboard** (`teacher-dashboard/.env.local`)
```env
NEXT_PUBLIC_ENGAGEMENT_API_URL=http://localhost:8001
NEXT_PUBLIC_VOICE_API_URL=http://localhost:8000
```

### **System Configuration**

#### **Engagement Monitor Settings**
- **Confidence Threshold**: 0.45 (face detection)
- **IoU Threshold**: 0.5 (non-maximum suppression)
- **Frame Processing**: Real-time with intelligent sampling
- **Model Precision**: FP16 for optimal performance

#### **Dashboard Settings**
- **Polling Interval**: 2 seconds for live data
- **Chart Refresh**: Real-time updates
- **Session Management**: Automated session tracking
- **Export Formats**: JSON, CSV, PDF

---

## 🛠️ **Build & Test**

### **Development Mode**

```bash
# Engagement Monitor
cd clr_engage_montr && python -m uvicorn main:app --reload

# Teacher Dashboard  
cd teacher-dashboard && npm run dev

# Voice-to-Video System
cd voice-to-video-transcript && python -m uvicorn api:app --reload
```

### **Production Build**

```bash
# Build Teacher Dashboard for testing
cd teacher-dashboard
npm run build
npm start
```

### **Testing**

```bash
# Run Python tests
cd clr_engage_montr && python -m pytest
cd voice-to-video-transcript && python -m pytest

# Run TypeScript tests
cd teacher-dashboard && npm test

# Integration tests
python test_integration.py
```

### **Linting & Code Quality**

```bash
# Python linting
flake8 . --max-line-length=100
black . --check

# TypeScript linting
cd teacher-dashboard && npm run lint
```

---

## 🐳 **Development Environment**

### **Docker Development**

```bash
# Build Docker images for development
docker-compose build

# Run complete system in development mode
docker-compose up -d
```



---

## 📊 **Usage Examples**

### **API Integration**

#### **Fetch Real-time Engagement Data**
```python
import requests

# Get live classroom metrics
response = requests.get('http://localhost:8001/api/classroom/realtime')
data = response.json()

print(f"Attendance: {data['attendance']['value']}%")
print(f"Engagement: {data['engagement']['value']}%")
print(f"Students Present: {data['students_present']}")
```

#### **Generate Educational Content**
```python
import requests

# Upload audio and generate video
with open('lecture.mp3', 'rb') as f:
    response = requests.post(
        'http://localhost:8000/generate',
        files={'audio': f},
        data={'topic_hint': 'Linear Algebra'}
    )

result = response.json()
print(f"Video URL: {result['video_url']}")
print(f"PDF URL: {result['pdf_url']}")
```

### **Dashboard Integration**

```javascript
// React hook for real-time KPIs
const { kpis, loading, error } = useRealTimeKPIs();

// Display live engagement metrics
<KPIBox
  title="Live Engagement"
  value={kpis.engagement.value}
  delta={kpis.engagement.delta}
  icon={<TrendingUp />}
/>
```


## 🔒 **Security & Privacy**

### **Data Protection**

- **Local Processing**: Face detection runs entirely on local hardware with no facial storage following our privacy first approach.
- **Encrypted Storage**: All recordings and data encrypted at rest
- **API Security**: Rate limiting and authentication for all endpoints
- **Privacy Compliance**: GDPR and COPPA compliant data handling

### **Security Features**

- **Input Validation**: Comprehensive validation for all API inputs
- **CORS Configuration**: Strict cross-origin resource sharing policies
- **Secure Headers**: Security headers implemented for all web endpoints
- **Access Control**: Role-based access control for teacher dashboard

---

## 📚 **Documentation**

### **Complete Documentation**

- **📋 [File Inventory](docs/File_Inventory.md)** - Comprehensive file listing and API documentation
- **🏗️ [Architecture Overview](docs/Architecture.md)** - System design and data flow diagrams
- **🚀 [API Reference](docs/API_Reference.md)** - Complete API documentation
- **🎓 [User Guide](docs/User_Guide.md)** - Step-by-step usage instructions
- **🔧 [Developer Guide](docs/Developer_Guide.md)** - Development setup and contribution guidelines

### **Quick References**

- **Engagement Monitor API**: `http://localhost:8001/docs`
- **Voice-to-Video API**: `http://localhost:8000/docs`
- **Dashboard Components**: Browse `teacher-dashboard/src/components/`

---

## 🎯 **Use Cases**

### **Educational Institutions**

- **K-12 Schools**: Monitor student engagement in traditional classrooms
- **Universities**: Large lecture hall analytics and attendance tracking
- **Online Learning**: Remote education engagement measurement
- **Training Centers**: Corporate and professional training analytics

### **Content Creation**

- **Educational Videos**: Transform lectures into animated content
- **MOOC Platforms**: Automated course content generation
- **Tutoring Services**: Personalized educational material creation
- **Academic Research**: Data-driven educational content analysis

---

## 🛣️ **Roadmap**

### **Phase 1: Core Platform** ✅
- [x] Real-time face detection and tracking
- [x] Emotion recognition with OpenVINO
- [x] Teacher dashboard with live KPIs
- [x] Voice-to-video content generation
- [x] API integration between modules

### **Phase 2: Advanced Features** 🚧
- [ ] Multi-language support (Spanish, French, German)
- [ ] Advanced analytics and reporting
- [ ] Mobile app for teachers
- [ ] Integration with LMS platforms
- [ ] Cloud deployment options

### **Phase 3: AI Enhancement** 📋
- [ ] Personalized learning recommendations
- [ ] Predictive analytics for student performance
- [ ] Advanced natural language processing
- [ ] Automated assessment generation
- [ ] Intelligent content curation

### **Phase 4: Platform Enhancement** 📋
- [ ] Multi-user support
- [ ] Enhanced security features
- [ ] Customizable interface
- [ ] Third-party integrations
- [ ] Advanced analytics dashboard

---

## 🤝 **Contributing**

We welcome contributions from the community! Here's how to get started:

### **Getting Started**

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/amazing-feature`
3. **Make your changes**
4. **Run tests**: `npm test` / `pytest`
5. **Commit your changes**: `git commit -m 'Add amazing feature'`
6. **Push to the branch**: `git push origin feature/amazing-feature`
7. **Open a Pull Request**

### **Development Guidelines**

- **Code Style**: Follow PEP 8 for Python, ESLint for TypeScript
- **Testing**: Write tests for all new features
- **Documentation**: Update documentation for API changes
- **Commits**: Use conventional commit messages

### **Issues and Bugs**

- **Bug Reports**: Use the bug report template
- **Feature Requests**: Use the feature request template
- **Questions**: Use discussions for general questions

---

## 📊 **Project Statistics**

- **📁 Total Files**: 106 source files
- **💾 Total Size**: ~1.2GB (including models and generated content)
- **📝 Lines of Code**: ~8,500 lines (excluding generated/binary files)
- **🔧 Dependencies**: 150+ packages across all modules
- **🎯 Supported Formats**: Audio (MP3, WAV, M4A), Video (MP4), Documents (PDF, MD)

---

---

## 📞 **Support**

### **Getting Help**

- **📋 GitHub Issues**: [Report bugs and request features](https://github.com/nishant-sheoran/EduTrack/issues)
- **📚 Documentation**: Check the docs/ folder for detailed documentation
- **💬 Discussions**: Use GitHub Discussions for questions and community support

### **Community**

- **👥 Contributors**: Welcome new contributors
- **⭐ GitHub Stars**: Star us to support the project
- **🍴 Forks**: Fork and contribute to development
- **💬 Discussions**: Join our community discussions

---

## 📄 **License**

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

```
MIT License

Copyright (c) 2024 EduTrack Contributors

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.
```

---

## 🙏 **Acknowledgments**

### **Technology Partners**

- **Intel**: OpenVINO optimization and Intel DevCloud support
- **OpenAI**: GPT-4 and Whisper API integration
- **3Blue1Brown**: Inspiration for mathematical animations
- **Manim Community**: Animation framework

### **Special Thanks**

- **SRMIST**: Academic support and research environment
- **Open Source Community**: For the amazing tools and libraries
- **Contributors**: All developers who contributed to this project

---

---

<div align="center">

### **Built with ❤️ for educational technology advancement**

**[⭐ Star us on GitHub](https://github.com/nishant-sheoran/EduTrack)** • **[🍴 Fork the Project](https://github.com/nishant-sheoran/EduTrack/fork)** • **[📋 Report Issues](https://github.com/nishant-sheoran/EduTrack/issues)**

---

*Last Updated: July 2025*  
*Version: 1.0.0*

</div>