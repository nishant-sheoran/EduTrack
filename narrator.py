"""
Text-to-Speech Narrator Module
Converts educational scripts into natural-sounding narration audio.
"""

import os
import asyncio
import tempfile
from pathlib import Path
from typing import Optional, List, Union
import logging
from gtts import gTTS
from pydub import AudioSegment
from pydub.silence import split_on_silence
import re

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Narrator:
    """Handles text-to-speech conversion for educational content."""
    
    def __init__(self, default_language: str = "en", default_speed: float = 1.0):
        """
        Initialize the narrator.
        
        Args:
            default_language: Default language code (e.g., 'en', 'es', 'fr')
            default_speed: Default speech speed multiplier
        """
        self.default_language = default_language
        self.default_speed = default_speed
        self.output_dir = Path("output")
        self.output_dir.mkdir(exist_ok=True)
        
        # Supported languages
        self.supported_languages = {
            'en': 'English',
            'es': 'Spanish', 
            'fr': 'French',
            'de': 'German',
            'it': 'Italian',
            'pt': 'Portuguese',
            'ru': 'Russian',
            'ja': 'Japanese',
            'ko': 'Korean',
            'zh': 'Chinese'
        }
    
    async def create_narration(self, text: str, language: Optional[str] = None, 
                             speed: Optional[float] = None, 
                             output_path: Optional[str] = None) -> str:
        """
        Create narration audio from text.
        
        Args:
            text: Text to convert to speech
            language: Language code (uses default if None)
            speed: Speech speed multiplier (uses default if None)
            output_path: Custom output path (generates if None)
            
        Returns:
            Path to the generated audio file
        """
        try:
            language = language or self.default_language
            speed = speed or self.default_speed
            
            logger.info(f"Creating narration for {len(text)} characters in {language}")
            
            # Clean and prepare text
            cleaned_text = self._clean_text(text)
            
            # Generate output path if not provided
            if not output_path:
                output_path = self.output_dir / f"narration_{hash(text) % 100000}.mp3"
            
            # Create narration using gTTS
            narration_path = await self._create_gtts_narration(
                cleaned_text, language, str(output_path)
            )
            
            # Adjust speed if needed
            if speed != 1.0:
                narration_path = self._adjust_speed(narration_path, speed)
            
            logger.info(f"Narration created successfully: {narration_path}")
            return narration_path
            
        except Exception as e:
            logger.error(f"Error creating narration: {e}")
            raise
    
    def _clean_text(self, text: str) -> str:
        """
        Clean text for better text-to-speech conversion.
        
        Args:
            text: Raw text
            
        Returns:
            Cleaned text
        """
        # Remove excessive whitespace
        text = re.sub(r'\s+', ' ', text)
        
        # Handle mathematical expressions
        # Convert common mathematical symbols to words
        math_replacements = {
            '∫': ' integral of ',
            '∑': ' sum of ',
            '∏': ' product of ',
            '∞': ' infinity ',
            '≈': ' approximately equals ',
            '≠': ' not equals ',
            '≤': ' less than or equal to ',
            '≥': ' greater than or equal to ',
            '→': ' approaches ',
            '∈': ' belongs to ',
            '∀': ' for all ',
            '∃': ' there exists ',
            'α': ' alpha ',
            'β': ' beta ',
            'γ': ' gamma ',
            'δ': ' delta ',
            'ε': ' epsilon ',
            'θ': ' theta ',
            'λ': ' lambda ',
            'μ': ' mu ',
            'π': ' pi ',
            'σ': ' sigma ',
            'φ': ' phi ',
            'ψ': ' psi ',
            'ω': ' omega '
        }
        
        for symbol, replacement in math_replacements.items():
            text = text.replace(symbol, replacement)
        
        # Handle LaTeX expressions (remove LaTeX commands)
        text = re.sub(r'\\[a-zA-Z]+\{([^}]*)\}', r'\1', text)
        text = re.sub(r'\$+([^$]+)\$+', r'\1', text)
        
        # Handle fractions
        text = re.sub(r'(\d+)/(\d+)', r'\1 over \2', text)
        
        # Handle exponents
        text = re.sub(r'\^(\d+)', r' to the power of \1', text)
        text = re.sub(r'\^2', r' squared', text)
        text = re.sub(r'\^3', r' cubed', text)
        
        # Add pauses for better pacing
        text = re.sub(r'\.', '. ', text)  # Pause after periods
        text = re.sub(r'\?', '? ', text)  # Pause after questions
        text = re.sub(r'!', '! ', text)   # Pause after exclamations
        text = re.sub(r';', '; ', text)   # Pause after semicolons
        text = re.sub(r':', ': ', text)   # Pause after colons
        
        # Clean up extra spaces
        text = re.sub(r'\s+', ' ', text).strip()
        
        return text
    
    async def _create_gtts_narration(self, text: str, language: str, output_path: str) -> str:
        """
        Create narration using Google Text-to-Speech.
        
        Args:
            text: Text to convert
            language: Language code
            output_path: Output file path
            
        Returns:
            Path to the generated audio file
        """
        try:
            # Create gTTS object
            tts = gTTS(text=text, lang=language, slow=False)
            
            # Save to temporary file first
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp_file:
                temp_path = tmp_file.name
            
            # Generate audio
            tts.save(temp_path)
            
            # Move to final location
            os.rename(temp_path, output_path)
            
            return output_path
            
        except Exception as e:
            logger.error(f"Error with gTTS: {e}")
            raise
    
    def _adjust_speed(self, audio_path: str, speed: float) -> str:
        """
        Adjust the speed of audio without changing pitch.
        
        Args:
            audio_path: Path to input audio file
            speed: Speed multiplier (1.0 = normal, >1.0 = faster, <1.0 = slower)
            
        Returns:
            Path to speed-adjusted audio file
        """
        try:
            # Load audio
            audio = AudioSegment.from_file(audio_path)
            
            # Adjust speed by changing frame rate
            # This method changes both speed and pitch
            new_sample_rate = int(audio.frame_rate * speed)
            speed_adjusted = audio._spawn(audio.raw_data, overrides={"frame_rate": new_sample_rate})
            
            # Normalize back to original sample rate to maintain pitch
            speed_adjusted = speed_adjusted.set_frame_rate(audio.frame_rate)
            
            # Create new output path
            path = Path(audio_path)
            speed_adjusted_path = path.parent / f"{path.stem}_speed_{speed}{path.suffix}"
            
            # Export adjusted audio
            speed_adjusted.export(str(speed_adjusted_path), format="mp3")
            
            # Replace original file
            os.replace(str(speed_adjusted_path), audio_path)
            
            logger.info(f"Audio speed adjusted to {speed}x")
            return audio_path
            
        except Exception as e:
            logger.error(f"Error adjusting audio speed: {e}")
            return audio_path  # Return original if adjustment fails
    
    def create_section_narrations(self, script_data: dict, language: Optional[str] = None) -> List[str]:
        """
        Create separate narration files for each script section.
        
        Args:
            script_data: Educational script data
            language: Language code
            
        Returns:
            List of paths to narration files
        """
        narration_paths = []
        
        try:
            # Create narration for introduction
            if script_data.get('introduction'):
                intro_path = asyncio.run(self.create_narration(
                    script_data['introduction'], 
                    language,
                    output_path=str(self.output_dir / "intro_narration.mp3")
                ))
                narration_paths.append(intro_path)
            
            # Create narrations for each section
            for i, section in enumerate(script_data.get('sections', [])):
                if section.get('content'):
                    section_path = asyncio.run(self.create_narration(
                        section['content'],
                        language,
                        output_path=str(self.output_dir / f"section_{i}_narration.mp3")
                    ))
                    narration_paths.append(section_path)
            
            # Create narration for summary
            if script_data.get('summary'):
                summary_path = asyncio.run(self.create_narration(
                    script_data['summary'],
                    language,
                    output_path=str(self.output_dir / "summary_narration.mp3")
                ))
                narration_paths.append(summary_path)
            
            return narration_paths
            
        except Exception as e:
            logger.error(f"Error creating section narrations: {e}")
            raise
    
    def combine_narrations(self, narration_paths: List[str], output_path: str, 
                          pause_duration: float = 1.0) -> str:
        """
        Combine multiple narration files into a single file.
        
        Args:
            narration_paths: List of paths to narration files
            output_path: Path for combined output
            pause_duration: Duration of pause between sections (seconds)
            
        Returns:
            Path to combined narration file
        """
        try:
            combined_audio = AudioSegment.empty()
            pause = AudioSegment.silent(duration=int(pause_duration * 1000))
            
            for path in narration_paths:
                if os.path.exists(path):
                    audio = AudioSegment.from_file(path)
                    combined_audio += audio + pause
                else:
                    logger.warning(f"Narration file not found: {path}")
            
            # Remove final pause
            if len(combined_audio) > pause_duration * 1000:
                combined_audio = combined_audio[:-int(pause_duration * 1000)]
            
            # Export combined audio
            combined_audio.export(output_path, format="mp3")
            
            logger.info(f"Combined narration saved to: {output_path}")
            return output_path
            
        except Exception as e:
            logger.error(f"Error combining narrations: {e}")
            raise
    
    def get_audio_duration(self, audio_path: str) -> float:
        """
        Get the duration of an audio file in seconds.
        
        Args:
            audio_path: Path to audio file
            
        Returns:
            Duration in seconds
        """
        try:
            audio = AudioSegment.from_file(audio_path)
            return len(audio) / 1000.0  # Convert milliseconds to seconds
        except Exception as e:
            logger.error(f"Error getting audio duration: {e}")
            return 0.0
    
    def normalize_audio(self, audio_path: str) -> str:
        """
        Normalize audio volume levels.
        
        Args:
            audio_path: Path to audio file
            
        Returns:
            Path to normalized audio file
        """
        try:
            audio = AudioSegment.from_file(audio_path)
            
            # Normalize to -20 dBFS
            normalized_audio = audio.normalize().apply_gain(-20 - audio.dBFS)
            
            # Export normalized audio
            normalized_audio.export(audio_path, format="mp3")
            
            logger.info("Audio normalized successfully")
            return audio_path
            
        except Exception as e:
            logger.error(f"Error normalizing audio: {e}")
            return audio_path
    
    def add_background_music(self, narration_path: str, music_path: str, 
                           music_volume: float = 0.1) -> str:
        """
        Add background music to narration.
        
        Args:
            narration_path: Path to narration audio
            music_path: Path to background music
            music_volume: Volume level for background music (0.0 to 1.0)
            
        Returns:
            Path to audio with background music
        """
        try:
            if not os.path.exists(music_path):
                logger.warning(f"Background music file not found: {music_path}")
                return narration_path
            
            # Load audio files
            narration = AudioSegment.from_file(narration_path)
            music = AudioSegment.from_file(music_path)
            
            # Adjust music volume
            music = music + (20 * music_volume - 20)  # Convert to dB
            
            # Loop music to match narration length if needed
            if len(music) < len(narration):
                loops_needed = len(narration) // len(music) + 1
                music = music * loops_needed
            
            # Trim music to narration length
            music = music[:len(narration)]
            
            # Mix narration and music
            mixed_audio = narration.overlay(music)
            
            # Export mixed audio
            mixed_path = narration_path.replace('.mp3', '_with_music.mp3')
            mixed_audio.export(mixed_path, format="mp3")
            
            logger.info(f"Background music added: {mixed_path}")
            return mixed_path
            
        except Exception as e:
            logger.error(f"Error adding background music: {e}")
            return narration_path

# Example usage
if __name__ == "__main__":
    async def test_narrator():
        """Test the narrator functionality."""
        try:
            narrator = Narrator()
            
            # Test text
            test_text = """
            Welcome to this educational video about linear regression. 
            Linear regression is a fundamental concept in machine learning and statistics. 
            The equation y = mx + b represents a line where m is the slope and b is the y-intercept.
            We'll explore how to find the best fitting line through data points.
            """
            
            print("Testing narration creation...")
            audio_path = await narrator.create_narration(test_text)
            print(f"Narration created: {audio_path}")
            
            # Test duration
            duration = narrator.get_audio_duration(audio_path)
            print(f"Audio duration: {duration:.2f} seconds")
            
            # Test normalization
            normalized_path = narrator.normalize_audio(audio_path)
            print(f"Audio normalized: {normalized_path}")
            
        except Exception as e:
            print(f"Test failed: {e}")
    
    # Run test
    asyncio.run(test_narrator())
