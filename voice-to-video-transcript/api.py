from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.responses import JSONResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import os
import tempfile
import asyncio
import sys
from pathlib import Path
from typing import Optional, Dict, Any


# Load environment variables from .env file
try:
    from dotenv import load_dotenv
    load_dotenv()
    print("✅ Environment variables loaded from .env file")
    print(f"🔑 OPENAI_API_KEY loaded: {'Yes' if os.getenv('OPENAI_API_KEY') else 'No'}")
    if os.getenv('OPENAI_API_KEY'):
        print(f"🔑 API Key starts with: {os.getenv('OPENAI_API_KEY')[:10]}...")
    else:
        print("❌ OPENAI_API_KEY not found in environment!")
        print(f"📁 Current working directory: {os.getcwd()}")
        print(f"📄 .env file exists: {os.path.exists('.env')}")
except ImportError:
    print("⚠ python-dotenv not installed. Install with: pip install python-dotenv")
    print("Environment variables will be loaded from system environment.")

# Ensure OpenAI API key is set before proceeding
if not os.getenv('OPENAI_API_KEY'):
    print("🚨 CRITICAL: OPENAI_API_KEY not found!")
    print("Please check your .env file and restart the server.")
else:
    print("✅ OpenAI API key is ready for use")

# Import the new audio recorder
from audio_recorder import AudioRecorder

# Check Python version
PYTHON_VERSION = sys.version_info
IS_PYTHON_313_PLUS = PYTHON_VERSION >= (3, 13)

# Global variables for classes
AudioTranscriber = None
ScriptGenerator = None
Narrator = None
VideoAnimator = None
PDFGenerator = None
VideoMerger = None
FULL_PIPELINE_AVAILABLE = False

# For Python 3.13 compatibility - conditional imports
print(f"🐍 Python version: {PYTHON_VERSION.major}.{PYTHON_VERSION.minor}.{PYTHON_VERSION.micro}")
print(f"🔍 IS_PYTHON_313_PLUS: {IS_PYTHON_313_PLUS}")

# Import modules individually to see which ones fail
modules_imported = 0
total_modules = 6

if not IS_PYTHON_313_PLUS:
    print("📦 Attempting to import Python 3.10/3.12 modules...")
    
    # AudioTranscriber
    try:
        from transcriber import AudioTranscriber
        print("✅ AudioTranscriber imported")
        modules_imported += 1
    except ImportError as e:
        print(f"❌ AudioTranscriber failed: {e}")
        AudioTranscriber = None
    
    # ScriptGenerator
    try:
        from script_generator import ScriptGenerator
        print("✅ ScriptGenerator imported")
        modules_imported += 1
    except ImportError as e:
        print(f"❌ ScriptGenerator failed: {e}")
        ScriptGenerator = None
    
    # Narrator
    try:
        from narrator import Narrator
        print("✅ Narrator imported")
        modules_imported += 1
    except ImportError as e:
        print(f"❌ Narrator failed: {e}")
        Narrator = None
    
    # VideoAnimator
    try:
        from animator import VideoAnimator
        print("✅ VideoAnimator imported")
        modules_imported += 1
    except ImportError as e:
        print(f"❌ VideoAnimator failed: {e}")
        VideoAnimator = None
    
    # PDFGenerator
    try:
        from pdf_generator import PDFGenerator
        print("✅ PDFGenerator imported")
        modules_imported += 1
    except ImportError as e:
        print(f"❌ PDFGenerator failed: {e}")
        PDFGenerator = None
    
    # VideoMerger
    try:
        from video_merger import VideoMerger
        print("✅ VideoMerger imported")
        modules_imported += 1
    except ImportError as e:
        print(f"❌ VideoMerger failed: {e}")
        VideoMerger = None

else:
    print("📦 Attempting to import Python 3.13+ compatible modules...")
    
    # AudioTranscriber
    try:
        from transcriber_py313 import AudioTranscriberPy313 as AudioTranscriber
        print("✅ AudioTranscriberPy313 imported")
        modules_imported += 1
    except ImportError as e:
        print(f"❌ AudioTranscriberPy313 failed: {e}")
        AudioTranscriber = None
    
    # ScriptGenerator
    try:
        from script_generator import ScriptGenerator
        print("✅ ScriptGenerator imported")
        modules_imported += 1
    except ImportError as e:
        print(f"❌ ScriptGenerator failed: {e}")
        ScriptGenerator = None
    
    # Narrator
    try:
        from narrator import Narrator
        print("✅ Narrator imported")
        modules_imported += 1
    except ImportError as e:
        print(f"❌ Narrator failed: {e}")
        Narrator = None
    
    # VideoAnimator
    try:
        from animator import VideoAnimator
        print("✅ VideoAnimator imported")
        modules_imported += 1
    except ImportError as e:
        print(f"❌ VideoAnimator failed: {e}")
        VideoAnimator = None
    
    # PDFGenerator
    try:
        from pdf_generator import PDFGenerator
        print("✅ PDFGenerator imported")
        modules_imported += 1
    except ImportError as e:
        print(f"❌ PDFGenerator failed: {e}")
        PDFGenerator = None
    
    # VideoMerger
    try:
        from video_merger import VideoMerger
        print("✅ VideoMerger imported")
        modules_imported += 1
    except ImportError as e:
        print(f"❌ VideoMerger failed: {e}")
        VideoMerger = None

# Set pipeline availability - require at least AudioTranscriber and ScriptGenerator for basic functionality
FULL_PIPELINE_AVAILABLE = modules_imported >= 2 and AudioTranscriber is not None and ScriptGenerator is not None

print(f"📊 Module import summary: {modules_imported}/{total_modules} modules imported successfully")
print(f"🚀 FULL_PIPELINE_AVAILABLE: {FULL_PIPELINE_AVAILABLE}")
print(f"🔧 Classes available: AudioTranscriber={AudioTranscriber is not None}, ScriptGenerator={ScriptGenerator is not None}, Narrator={Narrator is not None}")
print(f"🔧 More classes: VideoAnimator={VideoAnimator is not None}, PDFGenerator={PDFGenerator is not None}, VideoMerger={VideoMerger is not None}")

# Pydantic models for request/response
class RecordingStartRequest(BaseModel):
    session_id: Optional[str] = None

class RecordingStopRequest(BaseModel):
    process_immediately: bool = True
    topic_hint: Optional[str] = None

class SessionInfo(BaseModel):
    session_id: str
    video_path: Optional[str] = None
    pdf_path: Optional[str] = None
    transcript: Optional[str] = None
    title: Optional[str] = None
    status: str  # "recording", "processing", "completed", "error"
    created_at: str

app = FastAPI(title="Voice to Educational Video API with Real-time Recording")
app.mount("/static", StaticFiles(directory="output"), name="static")


# Add CORS middleware to allow browser requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Create output directory if it doesn't exist
os.makedirs("output", exist_ok=True)

# Global audio recorder instance
audio_recorder = AudioRecorder()

# Session storage for tracking processing status
active_sessions: Dict[str, SessionInfo] = {}

# === HEALTH CHECK ENDPOINTS ===

@app.get("/")
async def health_check():
    """Simple health check endpoint"""
    return {"status": "healthy", "message": "EduTrack Recording API is running"}

@app.get("/health")
async def health_check_detailed():
    """Detailed health check"""
    return {
        "status": "healthy",
        "api_version": "1.0",
        "recording_available": True,
        "active_sessions": len(active_sessions),
        "full_pipeline_available": FULL_PIPELINE_AVAILABLE
    }

# === REAL-TIME RECORDING ENDPOINTS ===

@app.post("/recording/start")
async def start_recording(request: RecordingStartRequest):
    """Start real-time audio recording"""
    try:
        print(f"📡 Received start recording request: {request}")
        result = await audio_recorder.start_recording(request.session_id)
        print(f"🎙 Recording start result: {result}")
        
        if result["status"] == "success":
            # Create session info
            from datetime import datetime
            session_info = SessionInfo(
                session_id=result["session_id"],
                status="recording",
                created_at=datetime.now().isoformat()
            )
            active_sessions[result["session_id"]] = session_info
            print(f"📋 Session created: {result['session_id']}")
            
        return JSONResponse(result)
        
    except Exception as e:
        print(f"❌ Error in start_recording: {e}")
        import traceback
        traceback.print_exc()
        return JSONResponse({"status": "error", "message": str(e)}, status_code=500)

@app.post("/recording/stop")
async def stop_recording(request: RecordingStopRequest):
    """Stop audio recording and optionally process immediately"""
    try:
        result = await audio_recorder.stop_recording()

        print("result cool!")
        print(request)
        
        if result["status"] == "success":
            print("Status Success!!!!!!!")
            session_id = result["session_id"]
            
            # Update session status - FIX: Remove await and fix assignment
            if session_id in active_sessions:
                active_sessions[session_id].status = "processing" if request.process_immediately else "recorded"
            
            # Process Audio - FIX: Now it's async, so we need await
            print("processing audio now")
            processing_result: dict = await process_recorded_audio(
                result["file_path"], 
                session_id, 
                request.topic_hint
            )
            print("processing audio done")

            print(processing_result.get('status'))
            
            # If processing was successful, update the result with the processing output
            if processing_result.get("status") == "success":
                print("Processing was successful!")
                result.update({
                    "videoUrl": processing_result["videoUrl"],
                    "transcriptUrl": processing_result["transcriptUrl"],
                    "transcript": processing_result.get("transcript", ""),
                    "title": processing_result.get("title", "Educational Video")
                })
                print(f"Final result: {result}")
            else:
                # If processing failed, include the error
                result.update({
                    "processing_error": processing_result.get("error", "Unknown processing error")
                })
        
        return JSONResponse(result)
        
    except Exception as e:
        print(f"❌ Error in stop_recording: {e}")
        import traceback
        traceback.print_exc()
        return JSONResponse({"error": str(e)}, status_code=500)

@app.get("/recording/status")
async def get_recording_status():
    """Get current recording status"""
    try:
        status = await audio_recorder.get_recording_status()
        return JSONResponse(status)
        
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)

@app.get("/session/{session_id}")
async def get_session_info(session_id: str):
    """Get information about a specific session"""
    if session_id not in active_sessions:
        return JSONResponse({"error": "Session not found"}, status_code=404)
    
    session_info = active_sessions[session_id]
    return JSONResponse(session_info.dict())

@app.get("/sessions")
async def get_all_sessions():
    """Get all active sessions"""
    return JSONResponse({
        "sessions": [session.dict() for session in active_sessions.values()],
        "total_count": len(active_sessions)
    })

@app.delete("/session/{session_id}")
async def delete_session(session_id: str):
    """Delete a session and its associated files"""
    if session_id not in active_sessions:
        return JSONResponse({"error": "Session not found"}, status_code=404)
    
    session_info = active_sessions[session_id]
    
    # Clean up files
    files_deleted = []
    if session_info.video_path and os.path.exists(session_info.video_path):
        os.unlink(session_info.video_path)
        files_deleted.append(session_info.video_path)
    
    if session_info.pdf_path and os.path.exists(session_info.pdf_path):
        os.unlink(session_info.pdf_path)
        files_deleted.append(session_info.pdf_path)
    
    # Remove from active sessions
    del active_sessions[session_id]
    
    return JSONResponse({
        "message": "Session deleted",
        "files_deleted": files_deleted
    })

async def process_recorded_audio(audio_file_path: str, session_id: str, topic_hint: Optional[str] = None):
    """Background task to process recorded audio through the full pipeline"""
    try:
        if session_id in active_sessions:
            active_sessions[session_id].status = "processing"
        
        print(f"🎵 Starting audio processing for session: {session_id}")
        print(f"📁 Input audio file: {os.path.abspath(audio_file_path)}")
        
        # Check if pipeline is available
        if not FULL_PIPELINE_AVAILABLE:
            raise ValueError("Full pipeline not available - missing required modules")
        
        # Check if essential classes are imported (AudioTranscriber and ScriptGenerator are required)
        if not AudioTranscriber or not ScriptGenerator:
            raise ValueError("Essential classes (AudioTranscriber, ScriptGenerator) not imported properly")
        
        # Check which optional modules are available
        has_narrator = Narrator is not None
        has_video_animator = VideoAnimator is not None
        has_pdf_generator = PDFGenerator is not None
        has_video_merger = VideoMerger is not None
        
        print(f"🔧 Available modules: Narrator={has_narrator}, VideoAnimator={has_video_animator}, PDFGenerator={has_pdf_generator}, VideoMerger={has_video_merger}")
        
        # Step 1: Transcribe audio
        transcriber = AudioTranscriber()
        transcript = await transcriber.transcribe(audio_file_path)
        print(f"📝 Transcription completed: {len(transcript)} characters")
        
        # Step 2: Generate educational script
        script_gen = ScriptGenerator()
        script_data = await script_gen.generate_script(transcript, topic_hint)
        print(f"📚 Script generated with title: {script_data.get('title', 'No title')}")
        
        # Initialize paths
        narration_path = None
        animation_path = None
        final_video_path = None
        pdf_path = None
        
        # Step 3: Create narration (if available)
        if has_narrator:
            try:
                narrator = Narrator()
                narration_path = await narrator.create_narration(script_data['full_text'])
                print(f"🎙 Narration created: {os.path.abspath(narration_path)}")
            except Exception as e:
                print(f"⚠ Narration failed: {e}")
                narration_path = None
        else:
            print("⚠ Narrator not available - skipping narration step")
        
        # Step 4: Create animations (if available)
        if has_video_animator:
            try:
                animator = VideoAnimator()
                animation_path = await animator.create_animation(script_data)
                print(f"🎬 Animation created: {os.path.abspath(animation_path)}")
            except Exception as e:
                print(f"⚠ Animation failed: {e}")
                animation_path = None
        else:
            print("⚠ VideoAnimator not available - skipping animation step")
        
        # Step 5: Merge video and audio (if both are available)
        if has_video_merger and animation_path and narration_path:
            try:
                merger = VideoMerger()
                final_video_path = await merger.merge_audio_video(animation_path, narration_path)
                print(f"🎥 Final video created: {os.path.abspath(final_video_path)}")
            except Exception as e:
                print(f"⚠ Video merging failed: {e}")
                final_video_path = None
        else:
            print("⚠ Video merging not available - missing components")
        
        # Step 6: Generate PDF (if available)
        if has_pdf_generator:
            try:
                pdf_gen = PDFGenerator()
                pdf_path = await pdf_gen.create_pdf(script_data)
                print(f"📄 PDF transcript created: {os.path.abspath(pdf_path)}")
            except Exception as e:
                print(f"⚠ PDF generation failed: {e}")
                pdf_path = None
        else:
            print("⚠ PDFGenerator not available - skipping PDF step")
        
        # Get absolute paths for return
        video_full_path = os.path.basename(final_video_path) if final_video_path else None
        transcript_full_path = os.path.basename(pdf_path) if pdf_path else None
        
        # PRINT THE EXACT PATHS ON YOUR PC
        print(f"\n🎯 FILES SAVED TO YOUR PC:")
        if video_full_path:
            print(f"📹 Video File: {video_full_path}")
        if transcript_full_path:
            print(f"📄 Transcript PDF: {transcript_full_path}")
        print(f"📁 Working Directory: {os.getcwd()}")
        
        # Update session with results
        if session_id in active_sessions:
            session = active_sessions[session_id]
            session.status = "completed"
            session.video_path = video_full_path
            session.pdf_path = transcript_full_path
            session.transcript = transcript
            session.title = script_data.get('title', 'Educational Video')
        
        # Create result dictionary with FIXED URLs
        result = {
            "status": "success",
            "videoUrl": f"http://127.0.0.1:8000/static/{video_full_path}" if video_full_path else None,
            "transcriptUrl": f"http://127.0.0.1:8000/static/{transcript_full_path}" if transcript_full_path else None,
            "transcript": transcript,
            "title": script_data.get('title', 'Educational Video'),
            "session_id": session_id
        }
        
        print(f"✅ Processing completed for session {session_id}")
        print(f"📊 Result: {result}")
        
        return result
        
    except Exception as e:
        print(f"❌ Error processing session {session_id}: {e}")
        import traceback
        traceback.print_exc()
        
        if session_id in active_sessions:
            active_sessions[session_id].status = "error"
        
        # Return error result
        return {
            "status": "error",
            "error": str(e),
            "session_id": session_id
        }
    
    finally:
        # Clean up the original recorded audio file
        if os.path.exists(audio_file_path):
            os.unlink(audio_file_path)
            print(f"🗑 Cleaned up temporary audio file: {audio_file_path}")

# === ORIGINAL ENDPOINTS (for file upload) ===

@app.post("/upload-audio")
async def upload_audio(audio: UploadFile = File(...)):
    """Simple endpoint to test audio file upload"""
    contents = await audio.read()
    with open(f"received_{audio.filename}", "wb") as f:
        f.write(contents)
    return JSONResponse({
        "filename": audio.filename, 
        "size": len(contents), 
        "message": "Audio received successfully!"
    })

@app.post("/generate")
async def generate_educational_video(
    audio: UploadFile = File(...),
    topic_hint: str = Form(""),
):
    """
    Process audio through the full pipeline:
    1. Transcribe audio to text
    2. Generate educational script
    3. Create narration audio
    4. Generate animations
    5. Merge audio & video
    6. Create PDF transcript
    
    Returns paths to the video, PDF, and the transcript.
    """
    # Save uploaded audio to temp file
    with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(audio.filename)[1]) as tmp_audio:
        tmp_audio.write(await audio.read())
        audio_path = tmp_audio.name
    
    try:
        # Check if full pipeline is available based on Python version
        if not FULL_PIPELINE_AVAILABLE:
            # Python 3.13+ path - just save the file and return placeholder
            save_path = os.path.join("output", f"received_{audio.filename}")
            with open(save_path, "wb") as f:
                with open(audio_path, "rb") as src_file:
                    f.write(src_file.read())
            
            return JSONResponse({
                "status": "success",
                "message": f"Audio received. Full pipeline not available on Python {PYTHON_VERSION.major}.{PYTHON_VERSION.minor}.",
                "note": "For full processing, run this API on Python 3.10 or 3.12 where pyaudioop is available",
                "audio_file": save_path,
                "topic_hint": topic_hint
            })
        
        # Full pipeline is available (Python 3.10/3.12)
        # Step 1: Transcribe audio
        transcriber = AudioTranscriber()
        transcript = await transcriber.transcribe(audio_path)
        
        # Step 2: Generate educational script
        script_gen = ScriptGenerator()
        script_data = await script_gen.generate_script(transcript, topic_hint)
        
        # Step 3: Create narration
        narrator = Narrator()
        narration_path = await narrator.create_narration(script_data['full_text'])
        
        # Step 4: Create animations
        animator = VideoAnimator()
        animation_path = await animator.create_animation(script_data)
        
        # Step 5: Merge video and audio
        merger = VideoMerger()
        final_video_path = await merger.merge_audio_video(animation_path, narration_path)
        
        # Step 6: Generate PDF
        pdf_gen = PDFGenerator()
        pdf_path = await pdf_gen.create_pdf(script_data)
        
        return JSONResponse({
            "video_path": os.path.abspath(final_video_path),
            "pdf_path": os.path.abspath(pdf_path),
            "transcript": transcript,
            "title": script_data.get('title', 'Educational Video')
        })
        
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)
    finally:
        # Clean up temp audio file
        if os.path.exists(audio_path):
            os.unlink(audio_path)

@app.get("/download/video/{filename}")
async def download_video(filename: str):
    """Download a generated video file"""
    video_path = os.path.join("output", filename)
    if not os.path.exists(video_path):
        return JSONResponse({"error": "Video not found"}, status_code=404)
    return FileResponse(video_path, media_type="video/mp4", filename=filename)

@app.get("/download/pdf/{filename}")
async def download_pdf(filename: str):
    """Download a generated PDF file"""
    pdf_path = os.path.join("output", filename)
    if not os.path.exists(pdf_path):
        return JSONResponse({"error": "PDF not found"}, status_code=404)
    return FileResponse(pdf_path, media_type="application/pdf", filename=filename)

@app.get("/test/manim")
async def test_manim():
    """Test Manim installation and basic functionality"""
    try:
        if not VideoAnimator:
            return {"error": "VideoAnimator not available"}
        
        # Test Manim installation
        animator = VideoAnimator()
        manim_test = animator.test_manim_installation()
        
        # Try to create a simple test animation
        test_script = {
            'title': 'Test Animation',
            'sections': [
                {
                    'type': 'introduction',
                    'content': 'This is a test animation to verify Manim is working properly.'
                }
            ],
            'full_text': 'This is a test animation to verify Manim is working properly.'
        }
        
        # Generate scene file only (don't render)
        scene_file_path = animator._generate_scene_file(test_script)
        
        return {
            "manim_test": manim_test,
            "scene_file_generated": os.path.exists(scene_file_path),
            "scene_file_path": scene_file_path
        }
        
    except Exception as e:
        return {"error": str(e)}