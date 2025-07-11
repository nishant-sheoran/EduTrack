"""
Video and Audio Merger Module
Combines Manim animations with narration audio to create final educational videos.
"""

import os
import asyncio
import subprocess
from pathlib import Path
from typing import Optional, List, Tuple
import logging
import tempfile
import json

# Try to import MoviePy, use fallback if not available
try:
    # Use the working import method as provided by user
    from moviepy import VideoFileClip, AudioFileClip, CompositeVideoClip, TextClip
    MOVIEPY_AVAILABLE = True
except ImportError:
    try:
        # Fallback to editor import
        from moviepy.editor import VideoFileClip, AudioFileClip, CompositeVideoClip, TextClip
        MOVIEPY_AVAILABLE = True
    except ImportError:
        MOVIEPY_AVAILABLE = False
        VideoFileClip = None
        AudioFileClip = None
        CompositeVideoClip = None
        TextClip = None

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class VideoMerger:
    """Handles merging of video animations with audio narration."""
    
    def __init__(self, output_dir: str = "output"):
        """
        Initialize the video merger.
        
        Args:
            output_dir: Directory to save merged videos
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        
        # Check for required dependencies
        self.ffmpeg_available = self._check_ffmpeg()
        self.moviepy_available = MOVIEPY_AVAILABLE
        
        if not MOVIEPY_AVAILABLE:
            logger.warning("MoviePy not available. Video merging functionality will be limited.")
            logger.info("To enable full video merging, install: pip install moviepy")
        
        if not (self.ffmpeg_available or self.moviepy_available):
            logger.warning("Neither ffmpeg nor MoviePy is properly configured")
    
    def _check_ffmpeg(self) -> bool:
        """Check if ffmpeg is available."""
        try:
            result = subprocess.run(['ffmpeg', '-version'], 
                                  capture_output=True, text=True, timeout=10)
            return result.returncode == 0
        except (subprocess.TimeoutExpired, FileNotFoundError, subprocess.SubprocessError):
            return False
    
    async def merge_audio_video(self, video_path: str, audio_path: str, 
                               output_path: Optional[str] = None,
                               sync_method: str = "stretch") -> str:
        """
        Merge video animation with audio narration.
        
        Args:
            video_path: Path to the video file (animation)
            audio_path: Path to the audio file (narration)
            output_path: Custom output path (generates if None)
            sync_method: Method to sync audio/video ("stretch", "cut", "loop")
            
        Returns:
            Path to the merged video file
        """
        try:
            logger.info(f"Merging video {video_path} with audio {audio_path}")
            
            # Validate input files
            if not os.path.exists(video_path):
                raise FileNotFoundError(f"Video file not found: {video_path}")
            if not os.path.exists(audio_path):
                raise FileNotFoundError(f"Audio file not found: {audio_path}")
            
            # Generate output path if not provided
            if not output_path:
                timestamp = int(asyncio.get_event_loop().time())
                output_path = self.output_dir / f"educational_video_{timestamp}.mp4"
            
            # Try MoviePy first, then fall back to ffmpeg
            if self.moviepy_available:
                merged_path = await self._merge_with_moviepy(
                    video_path, audio_path, str(output_path), sync_method
                )
            elif self.ffmpeg_available:
                merged_path = await self._merge_with_ffmpeg(
                    video_path, audio_path, str(output_path), sync_method
                )
            else:
                # Create a simple fallback - just copy the video file
                logger.warning("No video merging tools available. Creating placeholder output.")
                import shutil
                shutil.copy2(video_path, str(output_path))
                merged_path = str(output_path)
            
            logger.info(f"Video merged successfully: {merged_path}")
            return merged_path
            
        except Exception as e:
            logger.error(f"Error merging video and audio: {e}")
            raise
    
    async def _merge_with_moviepy(self, video_path: str, audio_path: str, 
                                 output_path: str, sync_method: str) -> str:
        """Merge using MoviePy."""
        if not MOVIEPY_AVAILABLE:
            raise RuntimeError("MoviePy is not available. Please install with: pip install moviepy")
        
        try:
            # Load video and audio
            video_clip = VideoFileClip(video_path)
            audio_clip = AudioFileClip(audio_path)
            
            video_duration = video_clip.duration
            audio_duration = audio_clip.duration
            
            logger.info(f"Video duration: {video_duration:.2f}s, Audio duration: {audio_duration:.2f}s")
            
            # Sync video and audio based on method
            if sync_method == "stretch":
                # Stretch video to match audio duration
                # NOTE: Speed adjustment is not available in this MoviePy version
                # Falling back to cut method
                logger.info("Speed adjustment not supported, using cut method instead")
                sync_method = "cut"
            
            if sync_method == "cut":
                # Cut longer one to match shorter one
                min_duration = min(video_duration, audio_duration)
                video_clip = video_clip.subclipped(0, min_duration)
                audio_clip = audio_clip.subclipped(0, min_duration)
                logger.info(f"Both video and audio cut to {min_duration:.2f}s")
                
            elif sync_method == "loop":
                # Loop shorter one to match longer one
                max_duration = max(video_duration, audio_duration)
                if video_duration < max_duration:
                    loops_needed = int(max_duration / video_duration) + 1
                    video_clip = video_clip.looped(loops_needed).subclipped(0, max_duration)
                if audio_duration < max_duration:
                    loops_needed = int(max_duration / audio_duration) + 1
                    audio_clip = audio_clip.looped(loops_needed).subclipped(0, max_duration)
                logger.info(f"Video/audio looped to {max_duration:.2f}s")
            
            # Set audio to video
            final_video = video_clip.with_audio(audio_clip)
            
            # Write final video
            logger.info("Writing final video file...")
            final_video.write_videofile(
                output_path,
                codec='libx264',
                audio_codec='aac',
                temp_audiofile='temp-audio.m4a',
                remove_temp=True
            )
            
            # Close clips to free memory
            video_clip.close()
            audio_clip.close()
            final_video.close()
            
            return output_path
            
        except Exception as e:
            logger.error(f"Error with MoviePy merging: {e}")
            raise
    
    async def _merge_with_ffmpeg(self, video_path: str, audio_path: str, 
                                output_path: str, sync_method: str) -> str:
        """Merge using ffmpeg (alternative method)."""
        try:
            # Get video and audio info
            video_info = await self._get_media_info(video_path)
            audio_info = await self._get_media_info(audio_path)
            
            video_duration = float(video_info.get('duration', 0))
            audio_duration = float(audio_info.get('duration', 0))
            
            # Build ffmpeg command based on sync method
            cmd = ['ffmpeg', '-i', video_path, '-i', audio_path]
            
            if sync_method == "stretch":
                # Stretch video to match audio
                if abs(video_duration - audio_duration) > 1.0:
                    filter_v = f"setpts={video_duration/audio_duration}*PTS"
                    cmd.extend(['-filter:v', filter_v])
            
            elif sync_method == "cut":
                # Cut to shortest duration
                min_duration = min(video_duration, audio_duration)
                cmd.extend(['-t', str(min_duration)])
            
            elif sync_method == "loop":
                # This is more complex in ffmpeg, using simple approach
                max_duration = max(video_duration, audio_duration)
                cmd.extend(['-t', str(max_duration)])
            
            # Output settings
            cmd.extend([
                '-c:v', 'libx264',
                '-c:a', 'aac',
                '-preset', 'medium',
                '-crf', '23',
                '-y',  # Overwrite output file
                output_path
            ])
            
            logger.info(f"Running ffmpeg command: {' '.join(cmd)}")
            
            # Run ffmpeg
            process = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            
            stdout, stderr = await process.communicate()
            
            if process.returncode != 0:
                error_msg = stderr.decode() if stderr else "Unknown error"
                raise RuntimeError(f"ffmpeg failed: {error_msg}")
            
            return output_path
            
        except Exception as e:
            logger.error(f"Error with ffmpeg merging: {e}")
            raise
    
    async def _get_media_info(self, file_path: str) -> dict:
        """Get media file information using ffprobe."""
        try:
            cmd = [
                'ffprobe', '-v', 'quiet', '-print_format', 'json',
                '-show_format', '-show_streams', file_path
            ]
            
            process = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            
            stdout, stderr = await process.communicate()
            
            if process.returncode != 0:
                raise RuntimeError(f"ffprobe failed: {stderr.decode()}")
            
            info = json.loads(stdout.decode())
            return info.get('format', {})
            
        except Exception as e:
            logger.error(f"Error getting media info: {e}")
            return {}
    
    def merge_multiple_segments(self, video_segments: List[str], 
                               audio_segments: List[str], 
                               output_path: str) -> str:
        """
        Merge multiple video segments with corresponding audio segments.
        
        Args:
            video_segments: List of video file paths
            audio_segments: List of audio file paths
            output_path: Output file path
            
        Returns:
            Path to the merged video
        """
        try:
            if len(video_segments) != len(audio_segments):
                raise ValueError("Number of video and audio segments must match")
            
            logger.info(f"Merging {len(video_segments)} segments")
            
            # Create clips for each segment
            final_clips = []
            
            for i, (video_path, audio_path) in enumerate(zip(video_segments, audio_segments)):
                if not os.path.exists(video_path):
                    logger.warning(f"Video segment {i} not found: {video_path}")
                    continue
                if not os.path.exists(audio_path):
                    logger.warning(f"Audio segment {i} not found: {audio_path}")
                    continue
                
                # Load and combine video and audio
                video_clip = VideoFileClip(video_path)
                audio_clip = AudioFileClip(audio_path)
                
                # Sync duration (use audio duration)
                video_clip = video_clip.set_duration(audio_clip.duration)
                combined_clip = video_clip.set_audio(audio_clip)
                
                final_clips.append(combined_clip)
            
            if not final_clips:
                raise ValueError("No valid segments to merge")
            
            # Concatenate all clips
            final_video = CompositeVideoClip(final_clips).concatenate_videoclips()
            
            # Write final video
            final_video.write_videofile(
                output_path,
                codec='libx264',
                audio_codec='aac',
                verbose=False,
                logger=None
            )
            
            # Close all clips
            for clip in final_clips:
                clip.close()
            final_video.close()
            
            logger.info(f"Multiple segments merged successfully: {output_path}")
            return output_path
            
        except Exception as e:
            logger.error(f"Error merging multiple segments: {e}")
            raise
    
    def add_intro_outro(self, video_path: str, intro_path: Optional[str] = None,
                       outro_path: Optional[str] = None, output_path: Optional[str] = None) -> str:
        """
        Add intro and/or outro to a video.
        
        Args:
            video_path: Main video file path
            intro_path: Intro video file path (optional)
            outro_path: Outro video file path (optional)
            output_path: Output file path
            
        Returns:
            Path to the video with intro/outro
        """
        try:
            clips = []
            
            # Add intro if provided
            if intro_path and os.path.exists(intro_path):
                intro_clip = VideoFileClip(intro_path)
                clips.append(intro_clip)
                logger.info("Intro added")
            
            # Add main video
            main_clip = VideoFileClip(video_path)
            clips.append(main_clip)
            
            # Add outro if provided
            if outro_path and os.path.exists(outro_path):
                outro_clip = VideoFileClip(outro_path)
                clips.append(outro_clip)
                logger.info("Outro added")
            
            if len(clips) == 1:
                logger.info("No intro/outro to add")
                return video_path
            
            # Generate output path if not provided
            if not output_path:
                video_file = Path(video_path)
                output_path = str(video_file.parent / f"{video_file.stem}_with_intro_outro{video_file.suffix}")
            
            # Concatenate clips
            final_video = CompositeVideoClip(clips).concatenate_videoclips()
            
            # Write final video
            final_video.write_videofile(
                output_path,
                codec='libx264',
                audio_codec='aac',
                verbose=False,
                logger=None
            )
            
            # Close clips
            for clip in clips:
                clip.close()
            final_video.close()
            
            logger.info(f"Intro/outro added successfully: {output_path}")
            return output_path
            
        except Exception as e:
            logger.error(f"Error adding intro/outro: {e}")
            raise
    
    def adjust_video_quality(self, video_path: str, quality: str = "medium",
                           output_path: Optional[str] = None) -> str:
        """
        Adjust video quality and compression.
        
        Args:
            video_path: Input video file path
            quality: Quality setting ("low", "medium", "high", "max")
            output_path: Output file path
            
        Returns:
            Path to the quality-adjusted video
        """
        try:
            quality_settings = {
                "low": {"crf": 28, "preset": "fast"},
                "medium": {"crf": 23, "preset": "medium"},
                "high": {"crf": 18, "preset": "slow"},
                "max": {"crf": 15, "preset": "veryslow"}
            }
            
            settings = quality_settings.get(quality, quality_settings["medium"])
            
            if not output_path:
                video_file = Path(video_path)
                output_path = str(video_file.parent / f"{video_file.stem}_{quality}{video_file.suffix}")
            
            # Load video
            video_clip = VideoFileClip(video_path)
            
            # Write with quality settings
            video_clip.write_videofile(
                output_path,
                codec='libx264',
                preset=settings["preset"],
                ffmpeg_params=['-crf', str(settings["crf"])],
                verbose=False,
                logger=None
            )
            
            video_clip.close()
            
            logger.info(f"Video quality adjusted to {quality}: {output_path}")
            return output_path
            
        except Exception as e:
            logger.error(f"Error adjusting video quality: {e}")
            raise
    
    def get_video_info(self, video_path: str) -> dict:
        """
        Get basic information about a video file.
        
        Args:
            video_path: Path to video file
            
        Returns:
            Dictionary with video information
        """
        try:
            clip = VideoFileClip(video_path)
            info = {
                "duration": clip.duration,
                "fps": clip.fps,
                "size": clip.size,
                "has_audio": clip.audio is not None
            }
            clip.close()
            return info
        except Exception as e:
            logger.error(f"Error getting video info: {e}")
            return {}

# Example usage
if __name__ == "__main__":
    async def test_video_merger():
        """Test the video merger functionality."""
        try:
            merger = VideoMerger()
            
            # Note: These would be actual file paths in real usage
            test_video = "test_animation.mp4"
            test_audio = "test_narration.mp3"
            
            if os.path.exists(test_video) and os.path.exists(test_audio):
                print("Testing video/audio merge...")
                
                # Test basic merge
                merged_video = await merger.merge_audio_video(
                    test_video, test_audio, "test_merged.mp4"
                )
                print(f"Merged video created: {merged_video}")
                
                # Test video info
                info = merger.get_video_info(merged_video)
                print(f"Video info: {info}")
                
            else:
                print("Test files not found. Creating sample test...")
                print("Video merger module created successfully.")
                print("To test, provide actual video and audio files.")
            
        except Exception as e:
            print(f"Test failed: {e}")
    
    # Run test
    asyncio.run(test_video_merger())
