"""
Server-side Audio Recorder Module
Handles real-time audio recording controlled by start/stop signals from frontend.
"""

import os
import asyncio
import tempfile
import threading
import time
import signal
import sys
import subprocess
from pathlib import Path
from typing import Optional, Dict, Any
import logging
import json
import uuid
import sys

# Try different audio recording libraries based on Python version
PYTHON_VERSION = sys.version_info
IS_PYTHON_313_PLUS = PYTHON_VERSION >= (3, 13)

if not IS_PYTHON_313_PLUS:
    # For Python 3.10/3.12, try pyaudio first
    try:
        import pyaudio
        import wave
        PYAUDIO_AVAILABLE = True
        RECORDING_METHOD = "pyaudio"
    except ImportError:
        PYAUDIO_AVAILABLE = False
        RECORDING_METHOD = "subprocess"
else:
    # For Python 3.13+, use subprocess with ffmpeg
    PYAUDIO_AVAILABLE = False
    RECORDING_METHOD = "subprocess"

import subprocess

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AudioRecorder:
    """Handles server-side real-time audio recording."""
    
    def __init__(self, output_dir: str = "output"):
        """
        Initialize the audio recorder.
        
        Args:
            output_dir: Directory to save recorded audio files
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        
        # Recording state
        self.is_recording = False
        self.recording_thread = None
        self.current_session_id = None
        self.current_file_path = None
        
        # Audio settings
        self.sample_rate = 44100
        self.channels = 1
        self.chunk_size = 1024
        self.audio_format = pyaudio.paInt16 if PYAUDIO_AVAILABLE else None
        
        # Auto-detect best audio device
        self.device_name = self._detect_audio_device()
        
        # PyAudio instance
        self.audio = None
        self.stream = None
        
        # Subprocess recording
        self.ffmpeg_process = None
        
        logger.info(f"AudioRecorder initialized with method: {RECORDING_METHOD}")
        logger.info(f"Using audio device: {self.device_name}")
    
    async def start_recording(self, session_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Start audio recording.
        
        Args:
            session_id: Optional session identifier
            
        Returns:
            Dict with session_id and status
        """
        if self.is_recording:
            return {
                "status": "error",
                "message": "Recording already in progress",
                "session_id": self.current_session_id
            }
        
        # Generate session ID if not provided
        if not session_id:
            session_id = str(uuid.uuid4())
        
        self.current_session_id = session_id
        timestamp = int(time.time())
        filename = f"recording_{session_id}_{timestamp}.wav"
        self.current_file_path = self.output_dir / filename
        
        try:
            if RECORDING_METHOD == "pyaudio":
                success = await self._start_pyaudio_recording()
            else:
                success = await self._start_subprocess_recording()
            
            if success:
                self.is_recording = True
                logger.info(f"Started recording: {self.current_file_path}")
                return {
                    "status": "success",
                    "message": "Recording started",
                    "session_id": session_id,
                    "file_path": str(self.current_file_path)
                }
            else:
                return {
                    "status": "error",
                    "message": "Failed to start recording",
                    "session_id": session_id
                }
                
        except Exception as e:
            logger.error(f"Error starting recording: {e}")
            return {
                "status": "error",
                "message": f"Recording error: {str(e)}",
                "session_id": session_id
            }
    
    async def stop_recording(self) -> Dict[str, Any]:
        """
        Stop audio recording.
        
        Returns:
            Dict with file path and status
        """
        if not self.is_recording:
            return {
                "status": "error",
                "message": "No recording in progress"
            }
        
        try:
            if RECORDING_METHOD == "pyaudio":
                success = await self._stop_pyaudio_recording()
            else:
                success = await self._stop_subprocess_recording()
            
            self.is_recording = False
            
            if success and self.current_file_path and self.current_file_path.exists():
                file_size = self.current_file_path.stat().st_size
                logger.info(f"Recording stopped: {self.current_file_path} ({file_size} bytes)")
                
                result = {
                    "status": "success",
                    "message": "Recording stopped",
                    "session_id": self.current_session_id,
                    "file_path": str(self.current_file_path),
                    "file_size": file_size
                }
                
                # Reset state
                self.current_session_id = None
                current_path = self.current_file_path
                self.current_file_path = None
                
                # Return the path for further processing
                result["file_path"] = str(current_path)
                return result
            else:
                return {
                    "status": "error",
                    "message": "Failed to stop recording or file not found"
                }
                
        except Exception as e:
            logger.error(f"Error stopping recording: {e}")
            self.is_recording = False
            return {
                "status": "error",
                "message": f"Stop recording error: {str(e)}"
            }
    
    async def get_recording_status(self) -> Dict[str, Any]:
        """
        Get current recording status.
        
        Returns:
            Dict with recording status and session info
        """
        return {
            "is_recording": self.is_recording,
            "session_id": self.current_session_id,
            "file_path": str(self.current_file_path) if self.current_file_path else None,
            "recording_method": RECORDING_METHOD,
            "pyaudio_available": PYAUDIO_AVAILABLE
        }
    
    async def _start_pyaudio_recording(self) -> bool:
        """Start recording using PyAudio."""
        try:
            self.audio = pyaudio.PyAudio()
            
            self.stream = self.audio.open(
                format=self.audio_format,
                channels=self.channels,
                rate=self.sample_rate,
                input=True,
                frames_per_buffer=self.chunk_size
            )
            
            # Start recording thread
            self.recording_thread = threading.Thread(target=self._pyaudio_recording_thread)
            self.recording_thread.daemon = True
            self.recording_thread.start()
            
            return True
            
        except Exception as e:
            logger.error(f"PyAudio recording start error: {e}")
            return False
    
    async def _stop_pyaudio_recording(self) -> bool:
        """Stop PyAudio recording."""
        try:
            if self.stream:
                self.stream.stop_stream()
                self.stream.close()
                self.stream = None
            
            if self.audio:
                self.audio.terminate()
                self.audio = None
            
            # Wait for recording thread to finish
            if self.recording_thread and self.recording_thread.is_alive():
                self.recording_thread.join(timeout=5.0)
            
            return True
            
        except Exception as e:
            logger.error(f"PyAudio recording stop error: {e}")
            return False
    
    def _pyaudio_recording_thread(self):
        """PyAudio recording thread function."""
        frames = []
        
        try:
            while self.is_recording and self.stream:
                try:
                    data = self.stream.read(self.chunk_size, exception_on_overflow=False)
                    frames.append(data)
                except Exception as e:
                    logger.error(f"Recording thread error: {e}")
                    break
            
            # Save the recorded audio
            if frames and self.current_file_path:
                with wave.open(str(self.current_file_path), 'wb') as wf:
                    wf.setnchannels(self.channels)
                    wf.setsampwidth(self.audio.get_sample_size(self.audio_format))
                    wf.setframerate(self.sample_rate)
                    wf.writeframes(b''.join(frames))
                
                logger.info(f"Audio saved to: {self.current_file_path}")
            
        except Exception as e:
            logger.error(f"Recording thread error: {e}")
    
    async def _start_subprocess_recording(self) -> bool:
        """Start recording using ffmpeg subprocess."""
        try:
            # FFmpeg command for recording from default microphone
            if os.name == 'nt':  # Windows
                cmd = [
                    'ffmpeg',
                    '-f', 'dshow',
                    '-i', f'audio={self.device_name}',  # Use detected device name
                    '-acodec', 'pcm_s16le',
                    '-ar', str(self.sample_rate),
                    '-ac', str(self.channels),
                    '-y',  # Overwrite output file
                    str(self.current_file_path)
                ]
            elif sys.platform == 'darwin':  # macOS
                cmd = [
                    'ffmpeg',
                    '-f', 'avfoundation',
                    '-i', ':0',  # Default audio input
                    '-acodec', 'pcm_s16le',
                    '-ar', str(self.sample_rate),
                    '-ac', str(self.channels),
                    '-y',
                    str(self.current_file_path)
                ]
            else:  # Linux
                cmd = [
                    'ffmpeg',
                    '-f', 'pulse',
                    '-i', 'default',  # Default audio input
                    '-acodec', 'pcm_s16le',
                    '-ar', str(self.sample_rate),
                    '-ac', str(self.channels),
                    '-y',
                    str(self.current_file_path)
                ]
            
            logger.info(f"Starting FFmpeg with command: {' '.join(cmd)}")
            
            # Start ffmpeg process
            self.ffmpeg_process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                stdin=subprocess.PIPE,
                creationflags=subprocess.CREATE_NEW_PROCESS_GROUP if os.name == 'nt' else 0
            )
            
            # Give FFmpeg a moment to start
            await asyncio.sleep(1)
            
            # Check if process is still running (if it failed, it would exit immediately)
            if self.ffmpeg_process.poll() is None:
                logger.info("FFmpeg recording process started successfully")
                return True
            else:
                # Process ended, check error
                stdout, stderr = self.ffmpeg_process.communicate()
                logger.error(f"FFmpeg failed to start: {stderr.decode() if stderr else 'Unknown error'}")
                return False
            
        except Exception as e:
            logger.error(f"FFmpeg recording start error: {e}")
            return False
    
    async def _stop_subprocess_recording(self) -> bool:
        """Stop ffmpeg recording."""
        try:
            if self.ffmpeg_process:
                logger.info("Stopping FFmpeg recording process...")
                
                if os.name == 'nt':  # Windows
                    # On Windows, terminate directly (CTRL_C_EVENT is unreliable)
                    try:
                        self.ffmpeg_process.terminate()
                        logger.info("Terminated FFmpeg process")
                    except:
                        self.ffmpeg_process.kill()
                        logger.info("Killed FFmpeg process")
                else:
                    # On Unix systems, send 'q' to stdin
                    try:
                        self.ffmpeg_process.stdin.write(b'q\n')
                        self.ffmpeg_process.stdin.flush()
                        logger.info("Sent 'q' command to FFmpeg")
                    except:
                        self.ffmpeg_process.terminate()
                        logger.info("Terminated FFmpeg process")
                
                # Wait for process to finish
                try:
                    stdout, stderr = self.ffmpeg_process.communicate(timeout=5)
                    logger.info("FFmpeg process ended gracefully")
                except subprocess.TimeoutExpired:
                    # Force terminate if it doesn't stop gracefully
                    self.ffmpeg_process.kill()
                    stdout, stderr = self.ffmpeg_process.communicate()
                    logger.warning("FFmpeg process killed forcefully")
                
                # Log any errors for debugging
                if stderr:
                    logger.info(f"FFmpeg stderr: {stderr.decode()[:200]}...")
                
                self.ffmpeg_process = None
                
                # Wait a moment for file to be written
                await asyncio.sleep(1)
            
            return True
            
        except Exception as e:
            logger.error(f"FFmpeg recording stop error: {e}")
            return False
    
    def _detect_audio_device(self) -> str:
        """
        Detect the best available audio input device.
        
        Returns:
            str: Name of the audio device to use
        """
        logger.info("Auto-detecting audio input device...")
        
        if RECORDING_METHOD == "pyaudio" and PYAUDIO_AVAILABLE:
            return self._detect_pyaudio_device()
        else:
            return self._detect_ffmpeg_device()
    
    def _detect_pyaudio_device(self) -> str:
        """Detect audio device using PyAudio."""
        try:
            import pyaudio
            p = pyaudio.PyAudio()
            
            # Get default input device
            default_device = p.get_default_input_device_info()
            device_name = default_device['name']
            
            logger.info(f"PyAudio default device: {device_name}")
            p.terminate()
            return device_name
            
        except Exception as e:
            logger.warning(f"PyAudio device detection failed: {e}")
            return "default"
    
    def _detect_ffmpeg_device(self) -> str:
        """Detect audio device using FFmpeg DirectShow."""
        # Known working devices from detection
        working_devices = [
            "Microphone Array (Realtek(R) Audio)",
            "Headset (Airdopes Primo)"
        ]
        
        # Common Windows microphone device names to try as fallback
        common_devices = [
            "Microphone",
            "Microphone (Realtek High Definition Audio)", 
            "Microphone Array",
            "Built-in Microphone",
            "Internal Microphone",
            "Stereo Mix",
            "Line In"
        ]
        
        # First, try known working devices
        for device in working_devices:
            if self._test_ffmpeg_device(device):
                logger.info(f"Selected working device: {device}")
                return device
        
        # Then try to list all DirectShow devices
        try:
            cmd = ['ffmpeg', '-f', 'dshow', '-list_devices', 'true', '-i', 'dummy']
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
            
            # Parse device list from stderr
            output = result.stderr
            audio_devices = []
            lines = output.split('\n')
            in_audio_section = False
            
            for line in lines:
                if 'DirectShow audio devices' in line:
                    in_audio_section = True
                    continue
                elif 'DirectShow video devices' in line:
                    in_audio_section = False
                    continue
                elif in_audio_section and '"' in line:
                    # Extract device name between quotes
                    start = line.find('"') + 1
                    end = line.rfind('"')
                    if start < end:
                        device_name = line[start:end]
                        if "(audio)" in line:  # Only audio devices
                            audio_devices.append(device_name)
            
            if audio_devices:
                logger.info(f"Found DirectShow devices: {audio_devices}")
                # Test each device to find working one
                for device in audio_devices:
                    if self._test_ffmpeg_device(device):
                        logger.info(f"Selected discovered device: {device}")
                        return device
                        
        except Exception as e:
            logger.warning(f"DirectShow device listing failed: {e}")
        
        # Fallback: test common device names
        logger.info("Testing common device names...")
        for device in common_devices:
            if self._test_ffmpeg_device(device):
                logger.info(f"Selected fallback device: {device}")
                return device
        
        # Final fallback - use the first known working device
        logger.warning("No working audio device found via testing, using known working device")
        return "Microphone Array (Realtek(R) Audio)"
    
    def _test_ffmpeg_device(self, device_name: str) -> bool:
        """Test if an FFmpeg device is accessible."""
        try:
            cmd = [
                'ffmpeg', '-f', 'dshow', 
                '-i', f'audio={device_name}',
                '-t', '1',  # 1 second test
                '-f', 'null', '-'  # Don't create output file
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=5)
            return result.returncode == 0
            
        except Exception:
            return False
    
    def cleanup(self):
        """Clean up resources."""
        if self.is_recording:
            asyncio.create_task(self.stop_recording())
        
        if self.ffmpeg_process:
            try:
                self.ffmpeg_process.terminate()
                self.ffmpeg_process = None
            except:
                pass
