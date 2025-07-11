"""
Python 3.13 Compatible Audio Transcription Module using OpenAI Whisper
This version avoids using pydub which depends on the removed pyaudioop module.
"""

import os
import tempfile
import asyncio
import shutil
import subprocess
from typing import Optional
from pathlib import Path
import logging
import openai

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AudioTranscriberPy313:
    """Handles audio transcription using OpenAI Whisper API without pydub."""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the transcriber.
        
        Args:
            api_key: OpenAI API key (will use environment variable if not provided)
        """
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OpenAI API key is required. Set OPENAI_API_KEY environment variable or pass it directly.")
        
        # Initialize OpenAI client
        openai.api_key = self.api_key
        self.client = openai.OpenAI(api_key=self.api_key)
        
        # Supported audio formats
        self.supported_formats = {'.mp3', '.mp4', '.wav', '.m4a', '.ogg', '.flac', '.webm'}
        
        # Check if ffmpeg is available
        try:
            subprocess.run(['ffmpeg', '-version'], capture_output=True, check=True)
            self.ffmpeg_available = True
        except (subprocess.SubprocessError, FileNotFoundError):
            self.ffmpeg_available = False
            logger.warning("ffmpeg not found. Some audio processing features may be limited.")
    
    def _prepare_audio(self, audio_path: str) -> str:
        """
        Prepare audio file for transcription by converting format if needed.
        Uses ffmpeg directly instead of pydub.
        
        Args:
            audio_path: Path to the input audio file
            
        Returns:
            Path to the prepared audio file
        """
        audio_path = Path(audio_path)
        
        # Check if file exists
        if not audio_path.exists():
            raise FileNotFoundError(f"Audio file not found: {audio_path}")
        
        # Check file size (Whisper API has a 25MB limit)
        file_size_mb = audio_path.stat().st_size / (1024 * 1024)
        logger.info(f"Audio file size: {file_size_mb:.2f} MB")
        
        if file_size_mb > 25:
            logger.warning("File size exceeds 25MB limit. Compressing audio...")
            return self._compress_audio(str(audio_path))
        
        # Check if format is supported
        if audio_path.suffix.lower() not in self.supported_formats:
            logger.info(f"Converting unsupported format {audio_path.suffix} to WAV")
            return self._convert_to_wav(str(audio_path))
        
        return str(audio_path)
    
    def _compress_audio(self, audio_path: str) -> str:
        """
        Compress audio file using ffmpeg directly instead of pydub.
        
        Args:
            audio_path: Path to the input audio file
            
        Returns:
            Path to the compressed audio file
        """
        if not self.ffmpeg_available:
            logger.warning("Cannot compress audio: ffmpeg not available. Using original file.")
            return audio_path
        
        try:
            # Create temporary file for compressed audio
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp:
                compressed_path = tmp.name
            
            # Use ffmpeg to compress
            subprocess.run([
                'ffmpeg', 
                '-i', audio_path,
                '-ar', '16000',  # Sample rate 16kHz
                '-ac', '1',      # Mono channel
                '-b:a', '64k',   # Bitrate 64k
                compressed_path
            ], check=True, capture_output=True)
            
            logger.info(f"Audio compressed from {Path(audio_path).stat().st_size / (1024*1024):.2f}MB to {Path(compressed_path).stat().st_size / (1024*1024):.2f}MB")
            
            return compressed_path
            
        except Exception as e:
            logger.error(f"Error compressing audio: {e}")
            return audio_path
    
    def _convert_to_wav(self, audio_path: str) -> str:
        """
        Convert audio to WAV format using ffmpeg directly.
        
        Args:
            audio_path: Path to the input audio file
            
        Returns:
            Path to the WAV file
        """
        if not self.ffmpeg_available:
            logger.warning("Cannot convert audio: ffmpeg not available. Using original file.")
            return audio_path
            
        try:
            # Create temporary file for WAV
            with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
                wav_path = tmp.name
                
            # Use ffmpeg to convert
            subprocess.run([
                'ffmpeg', 
                '-i', audio_path,
                wav_path
            ], check=True, capture_output=True)
            
            logger.info(f"Audio converted to WAV format: {wav_path}")
            return wav_path
            
        except Exception as e:
            logger.error(f"Error converting audio to WAV: {e}")
            return audio_path
    
    async def transcribe(self, audio_path: str) -> str:
        """
        Transcribe audio file to text.
        
        Args:
            audio_path: Path to the audio file
            
        Returns:
            Transcription text
        """
        try:
            # Prepare audio for transcription
            prepared_audio = self._prepare_audio(audio_path)
            logger.info(f"Transcribing audio file: {prepared_audio}")
            
            # Open and transcribe using OpenAI API
            with open(prepared_audio, "rb") as audio_file:
                transcription = await asyncio.to_thread(
                    self.client.audio.transcriptions.create,
                    file=audio_file,
                    model="whisper-1"
                )
            
            # Clean up temporary file if created
            if prepared_audio != audio_path and os.path.exists(prepared_audio):
                os.unlink(prepared_audio)
            
            return transcription.text
            
        except Exception as e:
            logger.error(f"Error in transcription: {e}")
            raise
