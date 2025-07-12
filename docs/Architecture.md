# 🏗️ EduTrack - System Architecture Overview

## 🎯 Executive Summary

EduTrack is a comprehensive educational monitoring and content generation system built with a **microservices architecture**. The system consists of three loosely-coupled modules that work together to provide real-time classroom analytics, teacher dashboards, and AI-powered educational content generation.

**Key Design Principles:**
- **Microservices Architecture**: Independent, scalable services
- **Real-time Processing**: Live data streaming and updates
- **AI-First Design**: Machine learning at the core of each module
- **Modern Web Technologies**: React, TypeScript, FastAPI
- **API-Driven Integration**: RESTful APIs with WebSocket support

---

## 🔧 High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                            EduTrack System Architecture                      │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐        │
│  │   Classroom     │    │     Teacher     │    │  Voice-to-Video │        │
│  │   Engagement    │    │    Dashboard    │    │   Transcript    │        │
│  │    Monitor      │    │                 │    │    System       │        │
│  │                 │    │                 │    │                 │        │
│  │  ┌───────────┐  │    │  ┌───────────┐  │    │  ┌───────────┐  │        │
│  │  │  YOLOv8   │  │    │  │ Next.js   │  │    │  │  OpenAI   │  │        │
│  │  │Face Detect│  │    │  │   React   │  │    │  │  Whisper  │  │        │
│  │  └───────────┘  │    │  └───────────┘  │    │  └───────────┘  │        │
│  │  ┌───────────┐  │    │  ┌───────────┐  │    │  ┌───────────┐  │        │
│  │  │ OpenVINO  │  │    │  │ TypeScript│  │    │  │   Manim   │  │        │
│  │  │ Emotions  │  │    │  │   Hooks   │  │    │  │  3Blue1B  │  │        │
│  │  └───────────┘  │    │  └───────────┘  │    │  └───────────┘  │        │
│  │  ┌───────────┐  │    │  ┌───────────┐  │    │  ┌───────────┐  │        │
│  │  │  FastAPI  │  │    │  │ TailwindCSS│    │  │ MoviePy   │  │        │
│  │  │  Server   │  │    │  │   UI      │  │    │  │  FFmpeg   │  │        │
│  │  └───────────┘  │    │  └───────────┘  │    │  └───────────┘  │        │
│  │                 │    │                 │    │                 │        │
│  │  Port: 8001     │    │  Port: 3000     │    │  Port: 8000     │        │
│  └─────────────────┘    └─────────────────┘    └─────────────────┘        │
│           │                       │                       │                │
│           │                       │                       │                │
│           └───────────────────────┼───────────────────────┘                │
│                                   │                                        │
│                         ┌─────────▼─────────┐                             │
│                         │   Data Flow Hub   │                             │
│                         │                   │                             │
│                         │ • Real-time KPIs  │                             │
│                         │ • Session Data    │                             │
│                         │ • Analytics      │                             │
│                         │ • Video URLs     │                             │
│                         │ • Transcripts    │                             │
│                         └───────────────────┘                             │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 📋 Module-by-Module Architecture

### 1. 📊 Classroom Engagement Monitor (`clr_engage_montr/`)

**Architecture Pattern**: **Pipeline + API Gateway**

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    Classroom Engagement Monitor                             │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  Video Input → Face Detection → Face Tracking → Emotion Analysis → KPIs     │
│                                                                             │
│  ┌─────────────┐   ┌─────────────┐   ┌─────────────┐   ┌─────────────┐     │
│  │   Camera    │   │   YOLOv8    │   │  DeepSORT   │   │  OpenVINO   │     │
│  │    Feed     │──▶│Face Detector│──▶│  Tracker    │──▶│  Emotions   │     │
│  └─────────────┘   └─────────────┘   └─────────────┘   └─────────────┘     │
│                                                                   │         │
│  ┌─────────────┐   ┌─────────────┐   ┌─────────────┐   ┌─────────▼─────┐   │
│  │   FastAPI   │   │   Shared    │   │  Head Pose  │   │  Engagement   │   │
│  │  Endpoint   │◀──│   State     │◀──│  Estimator  │◀──│    Scorer     │   │
│  └─────────────┘   └─────────────┘   └─────────────┘   └───────────────┘   │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

**Key Components:**
- **YoloV8FaceDetector**: Real-time face detection with ONNX optimization
- **DeepSortFaceTracker**: Multi-object tracking for attendance
- **EmotionRecognizer**: Intel OpenVINO emotion classification
- **HeadPoseEstimator**: 3D head pose analysis for engagement
- **FastAPI Server**: RESTful API with CORS support

**Data Flow:**
1. **Video Input** → Camera/file stream
2. **Face Detection** → Bounding boxes + confidence scores
3. **Face Tracking** → Unique ID assignment + movement tracking
4. **Emotion Analysis** → 7-class emotion classification
5. **Engagement Scoring** → Composite engagement metrics
6. **API Response** → JSON KPIs for dashboard consumption

### 2. 🎓 Teacher Dashboard (`teacher-dashboard/`)

**Architecture Pattern**: **Component-Based SPA + Real-time State Management**

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         Teacher Dashboard                                   │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌─────────────┐   ┌─────────────┐   ┌─────────────┐   ┌─────────────┐     │
│  │   Pages     │   │ Components  │   │   Hooks     │   │  Contexts   │     │
│  │             │   │             │   │             │   │             │     │
│  │ • Dashboard │   │ • KPIBox    │   │ • useDash   │   │ • Config    │     │
│  │ • Emotions  │   │ • ChartBox  │   │ • useKPIs   │   │ • Toast     │     │
│  │ • Timeline  │   │ • VideoBox  │   │ • useHealth │   │ • Analytics │     │
│  │ • Videos    │   │ • Transcript│   │ • useRecord │   │             │     │
│  │ • Transcripts│   │ • MagicUI   │   │             │   │             │     │
│  └─────────────┘   └─────────────┘   └─────────────┘   └─────────────┘     │
│         │                  │                  │                  │         │
│         └──────────────────┼──────────────────┼──────────────────┘         │
│                            │                  │                            │
│                    ┌───────▼──────────────────▼───────┐                    │
│                    │     Next.js App Router           │                    │
│                    │                                  │                    │
│                    │ • Server Components             │                    │
│                    │ • Client Components             │                    │
│                    │ • API Routes                    │                    │
│                    │ • Static Generation             │                    │
│                    └──────────────────────────────────┘                    │
│                                     │                                      │
│                    ┌────────────────▼────────────────┐                     │
│                    │        External APIs            │                     │
│                    │                                 │                     │
│                    │ • Engagement Monitor :8001     │                     │
│                    │ • Voice-to-Video :8000         │                     │
│                    │ • WebSocket Connections        │                     │
│                    └─────────────────────────────────┘                     │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

**Key Components:**
- **Pages**: Route-based page components with dynamic imports
- **Components**: Reusable UI components with TypeScript props
- **Hooks**: Custom React hooks for data fetching + state management
- **Contexts**: Global state management (config, analytics, toast)
- **MagicUI**: Advanced UI components with animations

**State Management Flow:**
1. **Context Providers** → Global state initialization
2. **Custom Hooks** → API calls + real-time updates
3. **Component Props** → Type-safe data flow
4. **Event Handlers** → User interactions + analytics triggers
5. **Real-time Updates** → WebSocket/SSE for live data

### 3. 🎙️ Voice-to-Video Transcript (`voice-to-video-transcript/`)

**Architecture Pattern**: **Pipeline Processing + Event-Driven Architecture**

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    Voice-to-Video Transcript System                         │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  Audio Input → Transcription → Script Generation → Content Creation         │
│                                                                             │
│  ┌─────────────┐   ┌─────────────┐   ┌─────────────┐   ┌─────────────┐     │
│  │   Audio     │   │   OpenAI    │   │    GPT-4    │   │   Content   │     │
│  │  Recorder   │──▶│   Whisper   │──▶│   Script    │──▶│  Generator  │     │
│  │             │   │             │   │  Generator  │   │             │     │
│  └─────────────┘   └─────────────┘   └─────────────┘   └─────────────┘     │
│                                                                   │         │
│  ┌─────────────┐   ┌─────────────┐   ┌─────────────┐   ┌─────────▼─────┐   │
│  │   FastAPI   │   │   Session   │   │    File     │   │  Narration  │   │
│  │  Endpoints  │◀──│  Manager    │◀──│   Storage   │◀──│    (gTTS)   │   │
│  └─────────────┘   └─────────────┘   └─────────────┘   └───────────────┘   │
│                                                                   │         │
│  ┌─────────────┐   ┌─────────────┐   ┌─────────────┐   ┌─────────▼─────┐   │
│  │  Streamlit  │   │   Video     │   │    Manim    │   │  Animation  │   │
│  │     UI      │   │   Merger    │◀──│  Animator   │◀──│   Engine    │   │
│  └─────────────┘   └─────────────┘   └─────────────┘   └───────────────┘   │
│                                                                   │         │
│                    ┌─────────────┐   ┌─────────────┐   ┌─────────▼─────┐   │
│                    │     PDF     │   │  MoviePy    │   │ Final Video │   │
│                    │  Generator  │   │  Composer   │   │    Output   │   │
│                    └─────────────┘   └─────────────┘   └───────────────┘   │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

**Key Components:**
- **AudioRecorder**: Real-time recording with device auto-detection
- **AudioTranscriber**: OpenAI Whisper API integration
- **ScriptGenerator**: GPT-4 educational content creation
- **VideoAnimator**: Manim 3Blue1Brown-style animations
- **VideoMerger**: MoviePy audio/video composition
- **PDFGenerator**: LaTeX-enabled transcript generation

**Processing Pipeline:**
1. **Audio Capture** → Real-time recording or file upload
2. **Transcription** → OpenAI Whisper speech-to-text
3. **Script Generation** → GPT-4 educational content structuring
4. **Content Creation** → Parallel processing:
   - **Narration**: gTTS text-to-speech
   - **Animation**: Manim visual generation
   - **PDF**: LaTeX document creation
5. **Video Composition** → MoviePy audio/video merging
6. **Output Delivery** → File storage + API response

---

## 🔄 Data Flow & Integration Patterns

### Inter-Module Communication

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           Data Flow Diagram                                 │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌─────────────────┐                                                        │
│  │   Classroom     │                                                        │
│  │   Engagement    │                                                        │
│  │    Monitor      │                                                        │
│  │                 │                                                        │
│  │  Live Analytics │────┐                                                   │
│  │  • Attendance   │    │                                                   │
│  │  • Engagement   │    │                                                   │
│  │  • Emotions     │    │                                                   │
│  │  • Head Pose    │    │                                                   │
│  │                 │    │                                                   │
│  │  Port: 8001     │    │                                                   │
│  └─────────────────┘    │                                                   │
│                         │                                                   │
│                         │  HTTP/REST API                                    │
│                         │  JSON Payload                                     │
│                         │                                                   │
│                         ▼                                                   │
│  ┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐               │
│  │     Teacher     │ │  Data Polling   │ │  State Updates  │               │
│  │    Dashboard    │ │                 │ │                 │               │
│  │                 │ │ • useRealTime   │ │ • Config Context│               │
│  │  Visualization  │ │ • useDashboard  │ │ • Analytics     │               │
│  │  • KPI Cards    │ │ • useHealth     │ │ • Toast Events  │               │
│  │  • Charts       │ │                 │ │                 │               │
│  │  • TimeSeries   │ │ Interval: 2s    │ │ Real-time: Yes  │               │
│  │  • Health       │ │                 │ │                 │               │
│  │                 │ └─────────────────┘ └─────────────────┘               │
│  │  Port: 3000     │                                                        │
│  └─────────────────┘                                                        │
│           │                                                                 │
│           │                                                                 │
│           │  Session Analytics                                              │
│           │  HTTP POST                                                      │
│           │                                                                 │
│           ▼                                                                 │
│  ┌─────────────────┐                                                        │
│  │  Voice-to-Video │                                                        │
│  │   Transcript    │                                                        │
│  │                 │                                                        │
│  │  Recording API  │                                                        │
│  │  • Start/Stop   │                                                        │
│  │  • Sessions     │                                                        │
│  │  • Processing   │                                                        │
│  │  • Downloads    │                                                        │
│  │                 │                                                        │
│  │  Generated      │                                                        │
│  │  Content URLs   │────┐                                                   │
│  │                 │    │                                                   │
│  │  Port: 8000     │    │                                                   │
│  └─────────────────┘    │                                                   │
│                         │                                                   │
│                         │  Video/PDF URLs                                   │
│                         │  HTTP Response                                    │
│                         │                                                   │
│                         ▼                                                   │
│  ┌─────────────────┐ ┌─────────────────┐                                   │
│  │  Dashboard      │ │  File Storage   │                                   │
│  │  Integration    │ │                 │                                   │
│  │                 │ │ • Video Files   │                                   │
│  │ • VideoBox      │ │ • PDF Files     │                                   │
│  │ • Transcripts   │ │ • Audio Files   │                                   │
│  │ • Downloads     │ │ • Session Data  │                                   │
│  │                 │ │                 │                                   │
│  └─────────────────┘ └─────────────────┘                                   │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### API Integration Points

**1. Engagement Monitor → Teacher Dashboard**
```javascript
// Real-time KPI fetching
const response = await fetch('http://localhost:8001/api/classroom/realtime');
const kpis = await response.json();

// Data Structure:
{
  "attendance": {"value": 85, "delta": 5},
  "engagement": {"value": 92, "delta": -2},
  "emotions": {"happy": 60, "focused": 30, "confused": 10},
  "students_present": 25,
  "timestamp": "2025-01-12T10:30:00Z"
}
```

**2. Teacher Dashboard → Voice-to-Video System**
```javascript
// Session recording integration
const startRecording = async (sessionId) => {
  const response = await fetch('http://localhost:8000/recording/start', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({session_id: sessionId})
  });
  return response.json();
};

// Generated content URLs
{
  "video_url": "http://localhost:8000/download/video/session_123.mp4",
  "pdf_url": "http://localhost:8000/download/pdf/transcript_123.pdf"
}
```

---

## 🎯 Design Patterns & Best Practices

### 1. **Microservices Architecture**
- **Independence**: Each module can be developed, deployed, and scaled separately
- **Technology Diversity**: Python (AI/ML), TypeScript (Frontend), specialized tools
- **Fault Isolation**: Failure in one module doesn't affect others
- **API Contracts**: Well-defined REST APIs for integration

### 2. **Event-Driven Architecture**
- **Real-time Updates**: WebSocket/SSE for live data streaming
- **Asynchronous Processing**: Non-blocking operations for better UX
- **Session Management**: Event-based recording and processing
- **State Synchronization**: Consistent state across modules

### 3. **Component-Based Design**
- **React Components**: Reusable UI components with TypeScript
- **Custom Hooks**: Encapsulated logic for data fetching and state
- **Context API**: Global state management without prop drilling
- **Atomic Design**: Hierarchical component structure

### 4. **Pipeline Architecture**
- **Video Processing**: Multi-stage face detection → tracking → analysis
- **Audio Processing**: Recording → transcription → generation → composition
- **Error Handling**: Graceful degradation and retry mechanisms
- **Caching**: Intelligent caching for performance optimization

### 5. **API Gateway Pattern**
- **Single Entry Point**: Centralized API access per module
- **CORS Configuration**: Cross-origin resource sharing for web integration
- **Rate Limiting**: Protection against abuse and overload
- **Documentation**: OpenAPI/Swagger for API documentation

---

## 🚀 Performance & Scalability

### Performance Optimizations

**1. Classroom Engagement Monitor**
- **Model Optimization**: ONNX format for fast inference
- **Frame Sampling**: Intelligent frame selection for processing
- **Memory Management**: Efficient buffer management for video streams
- **Batch Processing**: Vectorized operations for multiple faces

**2. Teacher Dashboard**
- **React Optimization**: Memoization, lazy loading, code splitting
- **Data Polling**: Intelligent polling intervals (2s for live data)
- **Caching Strategy**: Browser caching + service worker potential
- **Bundle Optimization**: Tree shaking, minification, compression

**3. Voice-to-Video System**
- **Async Processing**: Non-blocking audio/video processing
- **Parallel Execution**: Concurrent narration and animation generation
- **File Management**: Efficient temporary file handling
- **Memory Optimization**: Streaming processing for large files

### Scalability Considerations

**Horizontal Scaling:**
- **Load Balancing**: Multiple instances behind load balancer
- **Database Scaling**: Distributed storage for session data
- **CDN Integration**: Static asset delivery optimization
- **Container Orchestration**: Docker + Kubernetes deployment

**Vertical Scaling:**
- **GPU Acceleration**: CUDA/OpenCL for ML model inference
- **Multi-threading**: Parallel processing for video analysis
- **Memory Scaling**: Increased RAM for large video processing
- **SSD Storage**: Fast storage for model weights and generated content

---

## 🔒 Security & Privacy

### Data Protection
- **Local Processing**: Face detection runs locally, no cloud transmission
- **API Security**: Authentication and authorization for API access
- **Data Encryption**: Encrypted storage for sensitive recordings
- **Privacy Compliance**: GDPR/COPPA compliance for educational data

### Security Measures
- **Input Validation**: Comprehensive validation for all API inputs
- **Rate Limiting**: Protection against DoS attacks
- **CORS Configuration**: Strict origin policies
- **Secure Headers**: Security headers for web applications

---

## 📊 Technology Stack Summary

### Backend Technologies
- **Python 3.10-3.13**: Core programming language
- **FastAPI**: Modern, fast web framework
- **OpenCV**: Computer vision library
- **YOLOv8**: Object detection model
- **OpenVINO**: Intel's AI inference toolkit
- **OpenAI API**: GPT-4 and Whisper integration
- **Manim**: Mathematical animation engine
- **MoviePy**: Video processing library

### Frontend Technologies
- **Next.js 15**: React framework with SSR/SSG
- **React 19**: User interface library
- **TypeScript 5**: Type-safe JavaScript
- **Tailwind CSS**: Utility-first CSS framework
- **Recharts**: React charting library
- **Framer Motion**: Animation library

### Infrastructure & Tools
- **FFmpeg**: Audio/video processing
- **PyAudio**: Real-time audio recording
- **Streamlit**: Rapid prototyping framework
- **Docker**: Containerization (potential)
- **WebSockets**: Real-time communication
- **CORS**: Cross-origin resource sharing

---

## 🎓 Educational Technology Integration

### Classroom Integration
- **Real-time Monitoring**: Live engagement tracking during lessons
- **Automated Attendance**: Face recognition-based attendance
- **Emotion Analytics**: Student sentiment analysis
- **Performance Metrics**: Teacher effectiveness indicators

### Content Creation
- **Voice-to-Video**: Transform lectures into animated content
- **Educational Animations**: 3Blue1Brown-style mathematics
- **Transcript Generation**: Automated lesson transcription
- **Multi-format Output**: Video, PDF, audio formats

### Teacher Tools
- **Dashboard Analytics**: Comprehensive teaching insights
- **Session Management**: Recording and playback capabilities
- **Progress Tracking**: Student engagement over time
- **Export Capabilities**: Data export for reporting

---

*This architecture document provides a comprehensive overview of the EduTrack system design. For implementation details, refer to the individual module documentation and source code.*

*Last Updated: January 2025*
*Generated as part of EduTrack documentation initiative* 