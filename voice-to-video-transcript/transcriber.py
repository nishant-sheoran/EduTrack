"""
Audio Transcription Module using OpenAI Whisper
Handles voice-to-text conversion with high accuracy.
"""

import os
import tempfile
import asyncio
from typing import Optional
from pathlib import Path
import aiofiles
import openai
from pydub import AudioSegment
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AudioTranscriber:
    """Handles audio transcription using OpenAI Whisper API."""
    
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
    
    def _prepare_audio(self, audio_path: str) -> str:
        """
        Prepare audio file for transcription by converting format if needed.
        
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
        Compress audio file to reduce size while maintaining quality.
        
        Args:
            audio_path: Path to the input audio file
            
        Returns:
            Path to the compressed audio file
        """
        try:
            # Load audio
            audio = AudioSegment.from_file(audio_path)
            
            # Reduce quality settings
            compressed_audio = audio.set_frame_rate(16000).set_channels(1)
            
            # Create temporary file for compressed audio
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp:
                compressed_path = tmp.name
            
            # Export compressed audio
            compressed_audio.export(compressed_path, format="mp3", bitrate="64k")
            
            logger.info(f"Audio compressed from {Path(audio_path).stat().st_size / (1024*1024):.2f}MB to {Path(compressed_path).stat().st_size / (1024*1024):.2f}MB")
            
            return compressed_path
            
        except Exception as e:
            logger.error(f"Error compressing audio: {e}")
            raise
    
    def _convert_to_wav(self, audio_path: str) -> str:
        """
        Convert audio file to WAV format.
        
        Args:
            audio_path: Path to the input audio file
            
        Returns:
            Path to the converted WAV file
        """
        try:
            # Load audio
            audio = AudioSegment.from_file(audio_path)
            
            # Create temporary WAV file
            with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
                wav_path = tmp.name
            
            # Export as WAV
            audio.export(wav_path, format="wav")
            
            logger.info(f"Audio converted to WAV: {wav_path}")
            return wav_path
            
        except Exception as e:
            logger.error(f"Error converting audio to WAV: {e}")
            raise
    
    async def transcribe(self, audio_path: str, language: Optional[str] = None, prompt: Optional[str] = None) -> str:
        """
        Transcribe audio file to text using OpenAI Whisper.
        
        Args:
            audio_path: Path to the audio file
            language: Language code (e.g., 'en', 'es', 'fr') - auto-detected if None
            prompt: Optional prompt to guide transcription
            
        Returns:
            Transcribed text
        """
        try:
            # Prepare audio file
            prepared_audio_path = self._prepare_audio(audio_path)
            
            logger.info(f"Starting transcription of: {prepared_audio_path}")
            
            # Prepare transcription parameters
            transcription_params = {
                "model": "whisper-1",
                "response_format": "text",
                "temperature": 0.0  # Lower temperature for more consistent output
            }
            
            # Add optional parameters
            if language:
                transcription_params["language"] = language
            if prompt:
                transcription_params["prompt"] = prompt
            
            # Read audio file
            with open(prepared_audio_path, "rb") as audio_file:
                # Make API call
                response = self.client.audio.transcriptions.create(
                    file=audio_file,
                    **transcription_params
                )
            
            # Extract transcribed text
            if isinstance(response, str):
                transcript = response
            else:
                transcript = response.text if hasattr(response, 'text') else str(response)
            
            logger.info(f"Transcription completed. Length: {len(transcript)} characters")
            
            # Clean up temporary files if they were created
            if prepared_audio_path != audio_path and os.path.exists(prepared_audio_path):
                os.unlink(prepared_audio_path)
            
            return transcript.strip()
            
        except Exception as e:
            logger.error(f"Error during transcription: {e}")
            raise
    
    def transcribe_with_timestamps(self, audio_path: str, language: Optional[str] = None) -> dict:
        """
        Transcribe audio with word-level timestamps.
        
        Args:
            audio_path: Path to the audio file
            language: Language code (optional)
            
        Returns:
            Dict containing transcript with timestamps
        """
        try:
            prepared_audio_path = self._prepare_audio(audio_path)
            
            logger.info(f"Starting transcription with timestamps: {prepared_audio_path}")
            
            # Prepare parameters for detailed response
            transcription_params = {
                "model": "whisper-1",
                "response_format": "verbose_json",
                "temperature": 0.0,
                "timestamp_granularities": ["word"]
            }
            
            if language:
                transcription_params["language"] = language
            
            # Read audio file and transcribe
            with open(prepared_audio_path, "rb") as audio_file:
                response = self.client.audio.transcriptions.create(
                    file=audio_file,
                    **transcription_params
                )
            
            # Clean up temporary files
            if prepared_audio_path != audio_path and os.path.exists(prepared_audio_path):
                os.unlink(prepared_audio_path)
            
            return response
            
        except Exception as e:
            logger.error(f"Error during timestamped transcription: {e}")
            raise
    
    def batch_transcribe(self, audio_files: list[str], language: Optional[str] = None) -> list[str]:
        """
        Transcribe multiple audio files.
        
        Args:
            audio_files: List of paths to audio files
            language: Language code (optional)
            
        Returns:
            List of transcribed texts
        """
        transcripts = []
        
        for audio_file in audio_files:
            try:
                transcript = asyncio.run(self.transcribe(audio_file, language))
                transcripts.append(transcript)
                logger.info(f"Successfully transcribed: {audio_file}")
            except Exception as e:
                logger.error(f"Failed to transcribe {audio_file}: {e}")
                transcripts.append("")  # Add empty string for failed transcriptions
        
        return transcripts

# Example usage and testing
if __name__ == "__main__":
    async def test_transcriber():
        """Test the transcriber with a sample audio file."""
        try:
            # Initialize transcriber
            transcriber = AudioTranscriber()
            
            # Test with a sample audio file (you would need to provide this)
            test_audio = "test_audio.wav"  # Replace with actual test file
            
            if os.path.exists(test_audio):
                print("Testing transcription...")
                transcript = await transcriber.transcribe(test_audio)
                print(f"Transcript: {transcript}")
                
                print("\nTesting transcription with timestamps...")
                detailed_result = transcriber.transcribe_with_timestamps(test_audio)
                print(f"Detailed result keys: {detailed_result.keys() if isinstance(detailed_result, dict) else 'Not a dict'}")
            else:
                print(f"Test audio file {test_audio} not found. Skipping test.")
                
        except Exception as e:
            print(f"Test failed: {e}")
    
    # Run test
    asyncio.run(test_transcriber())
