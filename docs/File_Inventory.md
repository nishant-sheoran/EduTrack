# 📋 EduTrack - Complete File Inventory

## Overview
This document provides a comprehensive inventory of all files in the EduTrack project, organized by module and function. Each entry includes file path, size, language/format, role, and key interfaces.

---

## 🏗️ Project Structure Summary

The EduTrack system consists of three main modules:

1. **📊 Classroom Engagement Monitor** (`clr_engage_montr/`) - Real-time face detection and engagement tracking
2. **🎓 Teacher Dashboard** (`teacher-dashboard/`) - Modern web interface for monitoring and analytics  
3. **🎙️ Voice-to-Video Transcript** (`voice-to-video-transcript/`) - AI-powered educational video generation

---

## 📁 Module 1: Classroom Engagement Monitor (`clr_engage_montr/`)

### Core Application Files

| File | Size | Language | Role | Key APIs/Classes |
|------|------|----------|------|------------------|
| `main.py` | ~3.2KB | Python | **FastAPI Server & Video Processing Pipeline** | `FastAPI app`, `run_video_analysis()`, `/api/classroom/realtime` endpoint |
| `requirements.txt` | ~2.8KB | Text | **Dependencies Specification** | 107 packages including FastAPI, OpenCV, YOLOv8, TensorFlow |

### AI Models (`models/`)

| File | Size | Language | Role | Key APIs/Classes |
|------|------|----------|------|------------------|
| `face_detection.py` | ~3.1KB | Python | **YOLOv8 Face Detection** | `YoloV8FaceDetector`, `detect()`, `_format_image()`, `_process_output()` |
| `face_tracking.py` | ~1.8KB | Python | **DeepSORT Face Tracking** | `DeepSortFaceTracker`, `update_tracks()`, `get_track_id()` |
| `face_expression.py` | ~2.4KB | Python | **Emotion Recognition** | `EmotionRecognizer`, `recognize_emotion()`, Intel OpenVINO integration |
| `face_direction.py` | ~1.9KB | Python | **Head Pose Estimation** | `HeadPoseEstimator`, `estimate_pose()`, 3D angle calculation |

### Pre-trained Weights (`models/weights/`)

| Directory | Size | Format | Role | Models |
|-----------|------|--------|------|--------|
| `intel/emotions-recognition-retail-0003/` | ~12MB | OpenVINO | **Emotion Detection Models** | FP16, FP16-INT8, FP32 variants |
| `intel/head-pose-estimation-adas-0001/` | ~8MB | OpenVINO | **Head Pose Models** | FP16, FP16-INT8, FP32 variants |
| `yolov8n-face.onnx` | ~6MB | ONNX | **Face Detection Model** | YOLOv8 nano face detection |

---

## 📁 Module 2: Teacher Dashboard (`teacher-dashboard/`)

### Configuration Files

| File | Size | Language | Role | Key Configuration |
|------|------|----------|------|------------------|
| `package.json` | ~1.2KB | JSON | **Node.js Dependencies** | Next.js 15, React 19, TypeScript 5, Tailwind CSS |
| `tailwind.config.ts` | ~2.5KB | TypeScript | **Styling Configuration** | Custom animations, colors, border utilities |
| `next.config.ts` | ~0.3KB | TypeScript | **Next.js Configuration** | Build and runtime settings |
| `tsconfig.json` | ~0.8KB | JSON | **TypeScript Configuration** | Strict mode, path aliases, React JSX |

### Core Application (`src/app/`)

| File | Size | Language | Role | Key Components/APIs |
|------|------|----------|------|------------------|
| `layout.tsx` | ~1.4KB | TypeScript/React | **Root Layout & Providers** | `RootLayout`, Context providers, metadata |
| `page.tsx` | ~0.8KB | TypeScript/React | **Home Page** | Landing page component |
| `globals.css` | ~1.2KB | CSS | **Global Styles** | Tailwind base, CSS variables |
| `dashboard/page.tsx` | ~14.5KB | TypeScript/React | **Main Dashboard** | Live KPIs, real-time updates, analytics control |

### Dashboard Pages (`src/app/`)

| File | Size | Language | Role | Key Features |
|------|------|----------|------|--------------|
| `emotion-distribution/page.tsx` | ~2.1KB | TypeScript/React | **Emotion Analytics** | Emotion distribution charts, donut charts |
| `engagement-timeline/page.tsx` | ~3.2KB | TypeScript/React | **Engagement Timeline** | Time-series engagement data |
| `session-videos/page.tsx` | ~3.8KB | TypeScript/React | **Video Session Management** | Video playback, session data |
| `transcripts/page.tsx` | ~2.5KB | TypeScript/React | **Transcript Management** | Transcript viewing, subject categorization |

### React Components (`src/components/`)

| File | Size | Language | Role | Key Props/APIs |
|------|------|----------|------|----------------|
| `KPIBox.tsx` | ~1.8KB | TypeScript/React | **KPI Display Component** | `KPIBoxProps`, live metrics display |
| `ChartBox.tsx` | ~2.4KB | TypeScript/React | **Chart Visualization** | Recharts integration, responsive charts |
| `VideoBox.tsx` | ~3.1KB | TypeScript/React | **Video Player Component** | Video playback, controls, metadata |
| `TranscriptList.tsx` | ~4.2KB | TypeScript/React | **Transcript List Display** | Filtering, categorization, download |
| `ConfigPanel.tsx` | ~2.8KB | TypeScript/React | **Configuration Panel** | Settings management, real-time updates |
| `SystemHealthMarquee.tsx` | ~1.9KB | TypeScript/React | **System Health Display** | Animated status indicators |

### Magic UI Components (`src/components/magicui/`)

| File | Size | Language | Role | Key Features |
|------|------|----------|------|--------------|
| `bento-grid.tsx` | ~4.1KB | TypeScript/React | **Bento Grid Layout** | `BentoGrid`, `BentoCard`, responsive grid |
| `animated-circular-progress-bar.tsx` | ~2.3KB | TypeScript/React | **Animated Progress** | Circular progress with animations |
| `marquee.tsx` | ~3.2KB | TypeScript/React | **Scrolling Marquee** | Horizontal/vertical scrolling text |
| `border-beam.tsx` | ~2.8KB | TypeScript/React | **Animated Border Effect** | CSS animations, gradient borders |
| `pulsating-button.tsx` | ~1.4KB | TypeScript/React | **Pulsating Button** | Animated button with pulse effect |
| `ripple-button.tsx` | ~2.1KB | TypeScript/React | **Ripple Effect Button** | Click ripple animations |
| `scratch-to-reveal.tsx` | ~1.6KB | TypeScript/React | **Scratch Reveal Effect** | Interactive scratch-to-reveal |

### Context & Hooks (`src/contexts/`, `src/hooks/`)

| File | Size | Language | Role | Key APIs |
|------|------|----------|------|----------|
| `ConfigContext.tsx` | ~3.8KB | TypeScript/React | **Configuration State** | `TeacherConfig`, `useConfig()`, analytics state |
| `ToastContext.tsx` | ~2.1KB | TypeScript/React | **Toast Notifications** | `useToast()`, notification management |
| `useDashboardData.ts` | ~1.9KB | TypeScript | **Dashboard Data Hook** | Data fetching, loading states |
| `useRealTimeKPIs.ts` | ~2.4KB | TypeScript | **Real-time KPI Hook** | Live metrics, WebSocket integration |
| `useAnalyticsRecording.ts` | ~2.8KB | TypeScript | **Analytics Recording** | Session recording, API integration |
| `useSystemHealth.ts` | ~1.6KB | TypeScript | **System Health Hook** | Health monitoring, status checks |

### Utilities (`src/lib/`)

| File | Size | Language | Role | Key Functions |
|------|------|----------|------|---------------|
| `mockData.ts` | ~4.2KB | TypeScript | **Mock Data Generator** | Sample data for development/testing |
| `utils.ts` | ~0.9KB | TypeScript | **Utility Functions** | Class name utilities, common helpers |

---

## 📁 Module 3: Voice-to-Video Transcript (`voice-to-video-transcript/`)

### Core Application Files

| File | Size | Language | Role | Key APIs/Classes |
|------|------|----------|------|------------------|
| `api.py` | ~25.1KB | Python | **FastAPI Server with Real-time Recording** | Recording endpoints, session management, full pipeline |
| `app.py` | ~12.4KB | Python | **Streamlit Web Interface** | `VoiceToEducationalApp`, UI components |
| `main.py` | ~3.8KB | Python | **Command Line Interface** | CLI argument parsing, batch processing |
| `requirements.txt` | ~1.2KB | Text | **Dependencies** | OpenAI, FastAPI, Streamlit, audio processing |

### Core Processing Pipeline

| File | Size | Language | Role | Key APIs/Classes |
|------|------|----------|------|------------------|
| `transcriber.py` | ~9.1KB | Python | **OpenAI Whisper Transcription** | `AudioTranscriber`, `transcribe()`, format conversion |
| `transcriber_py313.py` | ~6.8KB | Python | **Python 3.13+ Compatible Transcriber** | `AudioTranscriberPy313`, FFmpeg integration |
| `script_generator.py` | ~8.4KB | Python | **GPT-4 Script Generation** | `ScriptGenerator`, educational content creation |
| `narrator.py` | ~5.2KB | Python | **Text-to-Speech Narration** | `Narrator`, gTTS integration, voice synthesis |
| `animator.py` | ~11.7KB | Python | **3Blue1Brown-style Animation** | `VideoAnimator`, Manim integration |
| `pdf_generator.py` | ~6.9KB | Python | **PDF Transcript Generation** | `PDFGenerator`, LaTeX math support |
| `video_merger.py` | ~18.3KB | Python | **Video/Audio Composition** | `VideoMerger`, MoviePy integration |

### Real-time Recording System

| File | Size | Language | Role | Key APIs/Classes |
|------|------|----------|------|------------------|
| `audio_recorder.py` | ~9.6KB | Python | **Real-time Audio Recording** | `AudioRecorder`, device detection, session management |
| `test_recording.html` | ~4.8KB | HTML/JavaScript | **Browser Recording Interface** | Web-based testing, API integration |
| `test_recording_endpoints.py` | ~7.1KB | Python | **CLI Recording Tests** | Endpoint testing, automation |

### Testing & Diagnostics

| File | Size | Language | Role | Key Functions |
|------|------|----------|------|---------------|
| `test_full_pipeline.py` | ~3.2KB | Python | **Full Pipeline Testing** | End-to-end testing, integration validation |
| `test_manim.py` | ~2.1KB | Python | **Manim Animation Testing** | Animation rendering tests |
| `test_ffmpeg_audio.py` | ~2.8KB | Python | **FFmpeg Audio Testing** | Audio processing validation |
| `windows_audio_troubleshoot.py` | ~12.4KB | Python | **Audio Diagnostics** | Device detection, troubleshooting |

### Documentation & Guides

| File | Size | Language | Role | Content |
|------|------|----------|------|---------|
| `RECORDING_INTEGRATION_GUIDE.md` | ~6.8KB | Markdown | **Integration Guide** | Real-time recording setup, API usage |
| `RECORDING_SUCCESS_SUMMARY.md` | ~5.1KB | Markdown | **Implementation Summary** | Technical achievements, configuration |
| `PYTHON_COMPATIBILITY.md` | ~3.4KB | Markdown | **Python 3.13+ Compatibility** | Version compatibility, troubleshooting |
| `GETTING_STARTED.md` | ~2.9KB | Markdown | **Quick Start Guide** | Installation, basic usage |

### Output & Generated Content (`output/`)

| Directory | Size | Type | Role | Contents |
|-----------|------|------|------|----------|
| `videos/` | ~450MB | Video | **Generated Educational Videos** | MP4 files, animation scenes |
| `texts/` | ~2.1MB | SVG/Images | **Generated Visual Elements** | Mathematical expressions, diagrams |
| `*.pdf` | ~15MB | PDF | **Generated Transcripts** | Educational transcripts, formatted documents |
| `*.mp3` | ~28MB | Audio | **Generated Narrations** | TTS audio files, voice synthesis |
| `*.mp4` | ~380MB | Video | **Final Educational Videos** | Complete video products |

---

## 📄 Project Root Files

| File | Size | Language | Role | Content |
|------|------|----------|------|---------|
| `README.md` | ~12.1KB | Markdown | **Project Documentation** | Setup instructions, architecture overview |
| `report&output/` | ~85MB | Mixed | **Project Deliverables** | Demo videos, reports, outputs |

---

## 🔧 File Type Distribution

### By Language/Format
- **Python**: 45 files (~180KB source code)
- **TypeScript/React**: 38 files (~120KB source code)
- **Markdown**: 12 files (~45KB documentation)
- **JSON/Config**: 8 files (~15KB configuration)
- **HTML/CSS**: 6 files (~12KB web assets)
- **Binary/Models**: 15 files (~850MB models & weights)

### By Role Category
- **Core Logic**: 28 files (API servers, processing pipelines)
- **UI Components**: 25 files (React components, pages)
- **Configuration**: 12 files (package.json, config files)
- **Testing**: 15 files (test scripts, validation)
- **Documentation**: 8 files (guides, README)
- **Assets/Models**: 18 files (pre-trained models, generated content)

### By Module
- **Classroom Monitor**: 8 files + 850MB models
- **Teacher Dashboard**: 42 files + dependencies
- **Voice-to-Video**: 35 files + generated content

---

## 🚀 Key Integration Points

### API Endpoints
- **Engagement Monitor**: `localhost:8001/api/classroom/realtime`
- **Voice-to-Video**: `localhost:8000/recording/*`, `localhost:8000/generate`  
- **Teacher Dashboard**: `localhost:3000` (frontend)

### Data Flow
1. **Engagement Monitor** → Real-time face detection → KPI data
2. **Teacher Dashboard** → Consumes KPI data → Visualizations
3. **Voice-to-Video** → Audio processing → Educational content

### Technology Stack
- **Backend**: FastAPI, OpenCV, YOLOv8, OpenAI API
- **Frontend**: Next.js, React, TypeScript, Tailwind CSS
- **AI/ML**: OpenVINO, Manim, MoviePy, Whisper
- **Real-time**: WebSocket, Server-Sent Events, PyAudio

---

## 📊 Statistics

- **Total Files**: 106 source files
- **Total Size**: ~1.2GB (including models and generated content)
- **Lines of Code**: ~8,500 lines (excluding generated/binary files)
- **Dependencies**: 150+ packages across all modules
- **Supported Formats**: Audio (MP3, WAV, M4A), Video (MP4), Images (SVG, PNG), Documents (PDF, MD)

---

*Last Updated: January 2025*
*Generated as part of EduTrack documentation initiative* 