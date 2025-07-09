from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.responses import JSONResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
import tempfile
import asyncio
import sys
from pathlib import Path
from typing import Optional, Dict, Any

# Import the new audio recorder
from audio_recorder import AudioRecorder

# Check Python version
PYTHON_VERSION = sys.version_info
IS_PYTHON_313_PLUS = PYTHON_VERSION >= (3, 13)

# For Python 3.13 compatibility - conditional imports
if not IS_PYTHON_313_PLUS:
    # These imports will work on Python 3.10 or 3.12
    try:
        from transcriber import AudioTranscriber
        from script_generator import ScriptGenerator
        from narrator import Narrator
        from animator import VideoAnimator
        from pdf_generator import PDFGenerator
        from video_merger import VideoMerger
        FULL_PIPELINE_AVAILABLE = True
    except ImportError as e:
        print(f"WARNING: Could not import pipeline modules: {e}")
        FULL_PIPELINE_AVAILABLE = False
else:
    # On Python 3.13+, try to use the compatible transcriber
    try:
        from transcriber_py313 import AudioTranscriberPy313 as AudioTranscriber
        from script_generator import ScriptGenerator
        from narrator import Narrator
        from animator import VideoAnimator
        from pdf_generator import PDFGenerator
        from video_merger import VideoMerger
        FULL_PIPELINE_AVAILABLE = True
        print("Using Python 3.13+ compatible modules")
    except ImportError as e:
        print(f"WARNING: Could not import Python 3.13+ compatible modules: {e}")
        FULL_PIPELINE_AVAILABLE = False

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
        print(f"🎙️ Recording start result: {result}")
        
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
        
        if result["status"] == "success":
            session_id = result["session_id"]
            
            # Update session status
            if session_id in active_sessions:
                active_sessions[session_id].status = "processing" if request.process_immediately else "recorded"
            
            # If process_immediately is True, start the pipeline
            if request.process_immediately and FULL_PIPELINE_AVAILABLE:
                # Start background processing
                asyncio.create_task(process_recorded_audio(
                    result["file_path"], 
                    session_id, 
                    request.topic_hint
                ))
                
                result["message"] = "Recording stopped, processing started"
            else:
                result["message"] = "Recording stopped, ready for manual processing"
        
        return JSONResponse(result)
        
    except Exception as e:
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
        
        # Step 1: Transcribe audio
        transcriber = AudioTranscriber()
        transcript = await transcriber.transcribe(audio_file_path)
        
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
        
        # Update session with results
        if session_id in active_sessions:
            session = active_sessions[session_id]
            session.status = "completed"
            session.video_path = final_video_path
            session.pdf_path = pdf_path
            session.transcript = transcript
            session.title = script_data.get('title', 'Educational Video')
        
        print(f"Processing completed for session {session_id}")
        
    except Exception as e:
        print(f"Error processing session {session_id}: {e}")
        if session_id in active_sessions:
            active_sessions[session_id].status = "error"
    
    finally:
        # Clean up the original recorded audio file
        if os.path.exists(audio_file_path):
            os.unlink(audio_file_path)

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


