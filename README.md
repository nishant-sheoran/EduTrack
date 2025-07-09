# 🎓 EduTrack - Voice to Educational Video Generator

Transform your voice recordings into **3Blue1Brown-style animated educational videos** and **structured PDF transcripts** using AI!

## 🌟 Features

- **🎙️ Voice Transcription**: Uses OpenAI Whisper for accurate speech-to-text conversion
- **🎤 Real-time Recording**: Server-side audio recording with start/stop controls
- **🧠 AI Script Generation**: GPT-4 converts raw transcripts into structured educational content
- **🎬 3Blue1Brown-style Animations**: Beautiful mathematical visualizations using Manim
- **🎵 Natural Narration**: High-quality text-to-speech with gTTS
- **📄 PDF Transcripts**: Clean, formatted PDF documents with LaTeX math support
- **🔄 Complete Pipeline**: Single-click processing from audio to final video + PDF
- **🌐 API Access**: FastAPI implementation for easy integration and automation
- **📱 Session Management**: Track multiple recording sessions and their progress
- **🐍 Python 3.13 Compatible**: Works with both Python 3.10/3.12 and 3.13+

## 🚀 Quick Start

### 1. Installation

```bash
# Clone or download the project
cd EduTrack-voice-features

# Run the setup script for basic setup
python setup.py

# OR use the setup batch file on Windows
setup.bat

# Install required dependencies
pip install -r requirements.txt
```

The setup process will:
- Check your Python version (3.8+ required, including 3.13+)
- Install system dependencies (FFmpeg, etc.)
- Install Python packages
- Create necessary directories
- Set up environment configuration

### 2. Configure API Keys

Edit the `.env` file and add your OpenAI API key:

```bash
OPENAI_API_KEY=your_openai_api_key_here
```

### 3. Run the Application

You have two options to run the application:

#### Option A: Web UI (Streamlit)
```bash
streamlit run app.py
```
This will open the web interface in your browser at `http://localhost:8501`

#### Option B: API Server (FastAPI)
```bash
# Using the batch file (Windows)
start_api_server.bat

# OR manually start the server
uvicorn api:app --reload
```
The API server will be available at `http://localhost:8000`
- API documentation: `http://localhost:8000/docs`
- Test form: Open `test_upload.html` in your browser

## 📋 System Requirements

### Required
- **Python 3.10+** (including Python 3.13+, see Python compatibility note below)
- **OpenAI API Key** (for GPT-4 and Whisper)
- **FFmpeg** (for video/audio processing, MANDATORY for Python 3.13+)

### Python 3.13 Compatibility
- **IMPORTANT**: Python 3.13 removed the `pyaudioop` module that many audio libraries depend on
- This project has been updated to work with Python 3.13+ by using alternative methods
- When running on Python 3.13+:
  - FFmpeg MUST be installed and in your system PATH
  - See `PYTHON_COMPATIBILITY.md` for details and troubleshooting

### Supported Platforms
- ✅ Windows 10/11
- ✅ macOS 10.14+
- ✅ Linux (Ubuntu, Debian, RHEL, CentOS)

### Audio Formats Supported
- WAV, MP3, MP4, M4A, OGG, FLAC, WEBM

## 🎯 How It Works

```
📱 Audio Input → 🎙️ Whisper Transcription → 🧠 GPT-4 Script Generation
                                                        ↓
📄 PDF Generation ← 🎬 Manim Animation ← 🎵 TTS Narration
                           ↓
                    🎥 Final Video
```

### Detailed Pipeline

1. **Audio Transcription**: Upload audio → Whisper converts to text
2. **Script Generation**: GPT-4 structures content into educational format
3. **Content Enhancement**: AI adds visual cues, math expressions, and timing
4. **Narration Creation**: gTTS generates natural-sounding voice
5. **Animation Rendering**: Manim creates 3Blue1Brown-style visuals
6. **Video Composition**: MoviePy merges animation + narration
7. **PDF Generation**: WeasyPrint/ReportLab creates formatted transcript

## 🎨 Example Output

### Input Audio
> "Today I want to explain linear regression. Linear regression is a fundamental concept in machine learning where we try to find the best line that fits through our data points. The equation is y equals mx plus b, where m is the slope and b is the y-intercept..."

### Generated Video Features
- 🎬 Animated coordinate systems and graphs
- 📊 Mathematical equations with LaTeX rendering
- 🎯 Step-by-step visual explanations
- 🎵 Natural narration synchronized with visuals
- 🎨 3Blue1Brown color scheme and styling

### Generated PDF Features
- 📖 Structured sections (Introduction, Concepts, Examples, Summary)
- 🧮 Formatted mathematical expressions
- 📝 Visual cue annotations
- 🏷️ Keywords and metadata
- 📄 Professional formatting

## ⚙️ Configuration Options

### Video Quality Settings
```python
# In .env file
VIDEO_QUALITY=medium_quality  # low_quality, medium_quality, high_quality, production_quality
VIDEO_FPS=30                  # 15, 24, 30, 60
```

### Voice Settings
```python
DEFAULT_LANGUAGE=en           # en, es, fr, de, it, pt, etc.
DEFAULT_SPEECH_SPEED=1.0      # 0.5 to 2.0
```

### Animation Style
```python
ANIMATION_STYLE=3blue1brown   # 3blue1brown, minimal, academic, colorful
```

## 🛠️ Advanced Usage

### Command Line Interface

```bash
# Generate video from audio file
python cli.py process audio_file.wav --topic "Linear Algebra" --output my_video.mp4

# Batch processing
python cli.py batch audio1.wav audio2.wav audio3.wav --format both

# Custom quality settings
python cli.py process audio.wav --video-quality high --audio-quality high
```

### API Usage

#### Python Module Usage
```python
from transcriber import AudioTranscriber
from script_generator import ScriptGenerator
from animator import VideoAnimator

# Initialize components
transcriber = AudioTranscriber()
script_gen = ScriptGenerator()
animator = VideoAnimator()

# Process audio
transcript = await transcriber.transcribe("audio.wav")
script = await script_gen.generate_script(transcript, "Mathematics")
video_path = await animator.create_animation(script)
```

#### FastAPI REST Endpoints

**File Upload Endpoints:**
```
# Upload an audio file
POST /upload-audio
- Form data: audio (file)

# Generate educational content from audio
POST /generate
- Form data: audio (file), topic_hint (string, optional)
```

**Real-time Recording Endpoints:**
```
# Start server-side recording
POST /recording/start
- Body: {"session_id": "optional"}

# Stop recording and process
POST /recording/stop  
- Body: {"process_immediately": true, "topic_hint": "optional"}

# Check recording status
GET /recording/status

# Get session information
GET /session/{session_id}
GET /sessions

# Download results
GET /download/video/{filename}
GET /download/pdf/{filename}
```

Example usage with curl:
```bash
# Upload audio file (traditional method)
curl -X POST -F "audio=@my_recording.mp3" http://localhost:8000/upload-audio

# Generate educational content with topic hint (traditional method)
curl -X POST -F "audio=@my_recording.mp3" -F "topic_hint=Linear Algebra" http://localhost:8000/generate

# Real-time recording (new method)
# Start recording
curl -X POST -H "Content-Type: application/json" -d '{}' http://localhost:8000/recording/start

# Stop recording and process immediately  
curl -X POST -H "Content-Type: application/json" -d '{"process_immediately": true, "topic_hint": "Mathematics"}' http://localhost:8000/recording/stop

# Check session status
curl http://localhost:8000/sessions
```

For real-time recording, use the included test interface: open `test_recording.html` in your browser.

## 📚 Project Structure

```
EduTrack-voice-features/
├── app.py                     # Streamlit web interface
├── api.py                     # FastAPI implementation with real-time recording
├── audio_recorder.py          # Real-time audio recording module
├── transcriber.py             # Whisper transcription (Python ≤3.12)
├── transcriber_py313.py       # Python 3.13+ compatible transcriber
├── script_generator.py        # GPT-4 script creation
├── narrator.py                # Text-to-speech generation
├── animator.py                # Manim animation creation
├── pdf_generator.py           # PDF document generation
├── video_merger.py            # Video/audio combination
├── setup.py                   # Installation script
├── setup.bat                  # Windows setup script
├── start_api_server.bat       # API server starter script
├── requirements.txt           # Python dependencies
├── PYTHON_COMPATIBILITY.md    # Python 3.13+ compatibility info
├── RECORDING_INTEGRATION_GUIDE.md  # Real-time recording integration guide
├── test_upload.html           # HTML test form for file upload API
├── test_recording.html        # HTML test form for real-time recording API
├── output/                    # Generated videos and PDFs
└── README.md                  # This file
```

## 🔧 Troubleshooting

### Common Issues

**1. "No module named 'pyaudioop'" or "ModuleNotFoundError: No module named 'pyaudioop'"**
- This occurs on Python 3.13+ where the pyaudioop module has been removed
- Solution 1: Use Python 3.10 or 3.12 instead of 3.13+
- Solution 2: Ensure FFmpeg is installed and in your PATH
- See `PYTHON_COMPATIBILITY.md` for detailed guidance

**2. "Import manim could not be resolved"**
```bash
# Install Manim manually
pip install manim
# Or with conda
conda install -c conda-forge manim
```

**3. "FFmpeg not found"**
- **Windows**: Download from https://ffmpeg.org/ and add to PATH
- **macOS**: `brew install ffmpeg`
- **Linux**: `sudo apt-get install ffmpeg`

**4. "Form data requires 'python-multipart' to be installed"**
```bash
pip install python-multipart
```

**5. "OpenAI API error"**
- Check your API key in `.env` file
- Ensure you have sufficient API credits
- Verify internet connection

**6. "Video rendering failed"**
- Check available disk space
- Ensure write permissions in output directory
- Try lower quality settings

**7. "Audio processing error"**
- Check audio file format (should be supported format)
- Ensure file isn't corrupted
- Try converting to WAV format first

**8. "uvicorn command not found" or similar**
```bash
pip install uvicorn[standard]
```

### Performance Tips

- **For faster processing**: Use `VIDEO_QUALITY=low_quality` for testing
- **For better quality**: Use `VIDEO_QUALITY=production_quality` for final videos
- **Large files**: Audio files >25MB will be automatically compressed
- **Memory usage**: Close other applications for large video rendering

## 🤝 Contributing

We welcome contributions! Here's how you can help:

1. **Bug Reports**: Open an issue with detailed reproduction steps
2. **Feature Requests**: Suggest new features or improvements  
3. **Code Contributions**: Submit pull requests with new features or fixes
4. **Documentation**: Help improve documentation and examples

### Development Setup

```bash
# Clone the repository
git clone <repository-url>
cd voice-to-educational-video

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install development dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt  # If available

# Run tests
python -m pytest tests/
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **3Blue1Brown** for inspiration and the amazing Manim library
- **OpenAI** for Whisper and GPT-4 APIs
- **Manim Community** for the excellent animation framework
- **Contributors** who help improve this project

## 🔗 Links

- **Manim Documentation**: https://docs.manim.community/
- **OpenAI API**: https://platform.openai.com/docs
- **Streamlit Documentation**: https://docs.streamlit.io/
- **3Blue1Brown Channel**: https://www.youtube.com/c/3blue1brown

## 📞 Support

- **Documentation**: Check this README, PYTHON_COMPATIBILITY.md, and inline code comments
- **Issues**: Open a GitHub issue for bugs or feature requests
- **Discussions**: Use GitHub Discussions for general questions

## 📝 Quick Reference

| Feature | Command/URL |
|---------|-------------|
| Start API Server | `uvicorn api:app --reload` |
| API Documentation | http://localhost:8000/docs |
| Test Upload Form | Open `test_upload.html` |
| Web UI | `streamlit run app.py` |
| Web UI URL | http://localhost:8501 |
| Output Directory | `./output/` |

## 📅 Last Updated

July 3, 2025 - Added Python 3.13+ compatibility and FastAPI integration

---

**Built with ❤️ using Python, FastAPI, OpenAI, Manim, and other amazing open-source tools.**

## 🐍 Python 3.13+ Compatibility Guide

Starting with Python 3.13, the `audioop`/`pyaudioop` module was removed from the standard library. This affects many audio processing libraries including `pydub`, which is used in this project.

### How We've Solved This

1. **Version Detection**: The code automatically detects your Python version
2. **Alternative Implementation**: For Python 3.13+, we use a special transcriber that relies on `ffmpeg` directly instead of `pydub`
3. **Conditional Imports**: The right modules are imported based on your Python version
4. **Graceful Fallback**: If running on Python 3.13+ without `ffmpeg`, a helpful error message is displayed

### Setting Up for Python 3.13+

1. **Install FFmpeg** (MANDATORY):
   - **Windows**: Download from https://ffmpeg.org/download.html and add to PATH
   - **macOS**: `brew install ffmpeg`
   - **Linux**: `sudo apt install ffmpeg`

2. **Verify FFmpeg Installation**:
   ```bash
   ffmpeg -version
   ```
   You should see version information, not "command not found"

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Start the API Server**:
   ```bash
   uvicorn api:app --reload
   ```

### Detailed Information

For more details, please read the `PYTHON_COMPATIBILITY.md` file.

## 🚀 Step-by-Step API Usage Guide

### 1. Start the API Server

**Option 1: Using the batch file (Windows)**
```bash
start_api_server.bat
```

**Option 2: Manual start**
```bash
cd EduTrack-voice-features
uvicorn api:app --reload --host 0.0.0.0 --port 8000
```

### 2. Test the API

**Option 1: Using the HTML Form**
1. Open `test_upload.html` in your browser
2. Select an audio file and click "Upload Audio" to test basic upload
3. Select an audio file, add an optional topic hint, and click "Generate Educational Content" for full processing

**Option 2: Using Swagger UI**
1. Open your browser to http://localhost:8000/docs
2. Test the endpoints using the interactive documentation

**Option 3: Using curl**
```bash
# Test audio upload
curl -X POST -F "audio=@your_audio_file.mp3" http://localhost:8000/upload-audio

# Generate educational content
curl -X POST -F "audio=@your_audio_file.mp3" -F "topic_hint=Your Topic" http://localhost:8000/generate
```

### 3. Retrieve Generated Content

After successful processing, you'll receive URLs to download the video and PDF:

- Video: `http://localhost:8000/download/video/{filename}`
- PDF: `http://localhost:8000/download/pdf/{filename}`

All generated files are also saved in the `output/` directory.
