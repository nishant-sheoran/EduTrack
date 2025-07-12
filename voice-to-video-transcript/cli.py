"""
Command Line Interface for Voice to Educational Video Generator
Provides command-line access to the video generation pipeline.
"""

import argparse
import asyncio
import os
import sys
from pathlib import Path
from typing import List, Optional
import logging

# Add current directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from transcriber import AudioTranscriber
from script_generator import ScriptGenerator
from narrator import Narrator
from animator import VideoAnimator
from pdf_generator import PDFGenerator
from video_merger import VideoMerger

# Load environment variables
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    print("Note: python-dotenv not installed. Using system environment variables.")

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class VoiceToVideoProcessor:
    """Main processor class for CLI operations."""
    
    def __init__(self):
        """Initialize all components."""
        self.transcriber = AudioTranscriber()
        self.script_generator = ScriptGenerator()
        self.narrator = Narrator()
        self.animator = VideoAnimator()
        self.pdf_generator = PDFGenerator()
        self.video_merger = VideoMerger()
    
    async def process_audio_file(self, audio_path: str, topic_hint: str = "",
                               output_path: Optional[str] = None,
                               generate_pdf: bool = True,
                               video_quality: str = "medium") -> tuple:
        """
        Process a single audio file through the complete pipeline.
        
        Args:
            audio_path: Path to audio file
            topic_hint: Optional topic hint
            output_path: Optional custom output path
            generate_pdf: Whether to generate PDF transcript
            video_quality: Video quality setting
            
        Returns:
            Tuple of (video_path, pdf_path)
        """
        try:
            logger.info(f"Processing audio file: {audio_path}")
            
            # Step 1: Transcribe audio
            logger.info("Step 1/6: Transcribing audio...")
            transcript = await self.transcriber.transcribe(audio_path)
            logger.info(f"Transcription complete ({len(transcript)} characters)")
            
            # Step 2: Generate educational script
            logger.info("Step 2/6: Generating educational script...")
            script_data = await self.script_generator.generate_script(transcript, topic_hint)
            logger.info("Educational script generated")
            
            # Step 3: Create narration
            logger.info("Step 3/6: Creating narration audio...")
            narration_path = await self.narrator.create_narration(script_data['full_text'])
            logger.info("Narration audio created")
            
            # Step 4: Create animation
            logger.info("Step 4/6: Generating animations...")
            self.animator.quality = f"{video_quality}_quality"
            animation_path = await self.animator.create_animation(script_data)
            logger.info("Animations rendered")
            
            # Step 5: Merge video and audio
            logger.info("Step 5/6: Combining audio and visuals...")
            final_video_path = await self.video_merger.merge_audio_video(
                animation_path, narration_path, output_path
            )
            logger.info("Final video created")
            
            # Step 6: Generate PDF (optional)
            pdf_path = None
            if generate_pdf:
                logger.info("Step 6/6: Creating PDF transcript...")
                pdf_path = await self.pdf_generator.create_pdf(script_data)
                logger.info("PDF transcript generated")
            
            logger.info("✅ Processing complete!")
            return final_video_path, pdf_path
            
        except Exception as e:
            logger.error(f"Error processing audio file: {e}")
            raise
    
    async def batch_process(self, audio_files: List[str], topic_hints: List[str] = None,
                          output_format: str = "both") -> List[tuple]:
        """
        Process multiple audio files in batch.
        
        Args:
            audio_files: List of audio file paths
            topic_hints: Optional list of topic hints (same length as audio_files)
            output_format: "video", "pdf", or "both"
            
        Returns:
            List of (video_path, pdf_path) tuples
        """
        results = []
        topic_hints = topic_hints or [""] * len(audio_files)
        
        for i, (audio_file, topic_hint) in enumerate(zip(audio_files, topic_hints)):
            try:
                logger.info(f"Processing file {i+1}/{len(audio_files)}: {audio_file}")
                
                generate_pdf = output_format in ["pdf", "both"]
                video_path, pdf_path = await self.process_audio_file(
                    audio_file, topic_hint, generate_pdf=generate_pdf
                )
                
                results.append((video_path, pdf_path))
                logger.info(f"✅ File {i+1} complete: {video_path}")
                
            except Exception as e:
                logger.error(f"❌ Failed to process {audio_file}: {e}")
                results.append((None, None))
        
        return results

def create_parser():
    """Create argument parser for CLI."""
    parser = argparse.ArgumentParser(
        description="Voice to Educational Video Generator - CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python cli.py process audio.wav --topic "Linear Algebra"
  python cli.py process audio.wav --output my_video.mp4 --quality high
  python cli.py batch audio1.wav audio2.wav --format both
  python cli.py batch *.wav --topics "Math" "Physics" "Chemistry"
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Commands')
    
    # Process single file
    process_parser = subparsers.add_parser('process', help='Process a single audio file')
    process_parser.add_argument('audio_file', help='Path to audio file')
    process_parser.add_argument('--topic', '-t', default='', help='Topic hint for better processing')
    process_parser.add_argument('--output', '-o', help='Output video file path')
    process_parser.add_argument('--quality', '-q', choices=['low', 'medium', 'high', 'production'],
                              default='medium', help='Video quality setting')
    process_parser.add_argument('--no-pdf', action='store_true', help='Skip PDF generation')
    process_parser.add_argument('--language', '-l', default='en', help='Audio language code')
    
    # Batch processing
    batch_parser = subparsers.add_parser('batch', help='Process multiple audio files')
    batch_parser.add_argument('audio_files', nargs='+', help='Paths to audio files')
    batch_parser.add_argument('--topics', nargs='+', help='Topic hints (one per audio file)')
    batch_parser.add_argument('--format', choices=['video', 'pdf', 'both'], default='both',
                            help='Output format')
    batch_parser.add_argument('--quality', '-q', choices=['low', 'medium', 'high', 'production'],
                            default='medium', help='Video quality setting')
    batch_parser.add_argument('--language', '-l', default='en', help='Audio language code')
    
    # Configuration
    config_parser = subparsers.add_parser('config', help='Show configuration information')
    config_parser.add_argument('--check', action='store_true', help='Check system dependencies')
    
    return parser

async def process_command(args):
    """Handle the process command."""
    processor = VoiceToVideoProcessor()
    
    try:
        # Check if audio file exists
        if not os.path.exists(args.audio_file):
            print(f"❌ Audio file not found: {args.audio_file}")
            return 1
        
        # Process the file
        video_path, pdf_path = await processor.process_audio_file(
            audio_path=args.audio_file,
            topic_hint=args.topic,
            output_path=args.output,
            generate_pdf=not args.no_pdf,
            video_quality=args.quality
        )
        
        print(f"✅ Processing complete!")
        print(f"📹 Video: {video_path}")
        if pdf_path:
            print(f"📄 PDF: {pdf_path}")
        
        return 0
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return 1

async def batch_command(args):
    """Handle the batch command."""
    processor = VoiceToVideoProcessor()
    
    try:
        # Validate audio files
        audio_files = []
        for file_path in args.audio_files:
            if os.path.exists(file_path):
                audio_files.append(file_path)
            else:
                print(f"⚠️ Skipping missing file: {file_path}")
        
        if not audio_files:
            print("❌ No valid audio files found")
            return 1
        
        # Process files
        results = await processor.batch_process(
            audio_files=audio_files,
            topic_hints=args.topics,
            output_format=args.format
        )
        
        # Print results
        print(f"\n✅ Batch processing complete!")
        print(f"📊 Processed {len(audio_files)} files:")
        
        for i, (video_path, pdf_path) in enumerate(results):
            print(f"  {i+1}. {audio_files[i]}")
            if video_path:
                print(f"     📹 Video: {video_path}")
            if pdf_path:
                print(f"     📄 PDF: {pdf_path}")
            if not video_path and not pdf_path:
                print(f"     ❌ Failed to process")
        
        return 0
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return 1

def config_command(args):
    """Handle the config command."""
    print("🔧 Voice to Educational Video Generator - Configuration")
    print("=" * 50)
    
    # Check API key
    api_key = os.getenv("OPENAI_API_KEY")
    if api_key:
        print(f"✅ OpenAI API Key: {'*' * (len(api_key) - 8) + api_key[-8:]}")
    else:
        print("❌ OpenAI API Key: Not set")
    
    # Check system dependencies
    if args.check:
        print("\n🔍 Checking system dependencies...")
        
        # Check Python packages
        packages = [
            "openai", "streamlit", "manim", "moviepy", "pydub", 
            "gtts", "weasyprint", "reportlab"
        ]
        
        for package in packages:
            try:
                __import__(package)
                print(f"   ✅ {package}")
            except ImportError:
                print(f"   ❌ {package}")
        
        # Check FFmpeg
        try:
            import subprocess
            subprocess.run(['ffmpeg', '-version'], capture_output=True, check=True)
            print("   ✅ ffmpeg")
        except (subprocess.CalledProcessError, FileNotFoundError):
            print("   ❌ ffmpeg")
    
    # Show current settings
    print(f"\n⚙️ Current Settings:")
    print(f"   Output Directory: {os.path.abspath('output')}")
    print(f"   Default Language: {os.getenv('DEFAULT_LANGUAGE', 'en')}")
    print(f"   Default Quality: {os.getenv('VIDEO_QUALITY', 'medium_quality')}")
    
    return 0

async def main():
    """Main CLI function."""
    parser = create_parser()
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return 1
    
    # Handle different commands
    if args.command == 'process':
        return await process_command(args)
    elif args.command == 'batch':
        return await batch_command(args)
    elif args.command == 'config':
        return config_command(args)
    else:
        print(f"❌ Unknown command: {args.command}")
        return 1

if __name__ == "__main__":
    try:
        exit_code = asyncio.run(main())
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\n⚠️ Operation cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        sys.exit(1)
