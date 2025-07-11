"""
Video Combiner Module

This module handles combining audio and video files using MoviePy.
It synchronizes narration audio with corresponding Manim animations
to create the final educational video.
"""

import os
import tempfile
from typing import List, Optional
from moviepy.editor import VideoFileClip, AudioFileClip, CompositeVideoClip, concatenate_videoclips
import moviepy.config as mp_config


class VideoCombiner:
    """Handles combining audio and video files using MoviePy."""
    
    def __init__(self, temp_dir: str = None, output_dir: str = None):
        """
        Initialize the VideoCombiner.
        
        Args:
            temp_dir (str): Directory for temporary files
            output_dir (str): Directory for output videos
        """
        self.temp_dir = temp_dir or os.path.join(tempfile.gettempdir(), 'video_combiner')
        self.output_dir = output_dir or os.path.join(tempfile.gettempdir(), 'combined_videos')
        os.makedirs(self.temp_dir, exist_ok=True)
        os.makedirs(self.output_dir, exist_ok=True)
    
    def combine_audio_and_video(self, audio_files: List[str], video_files: List[str], 
                               output_file: str) -> str:
        """
        Combine audio and video files into a single video with precise synchronization.
        
        Args:
            audio_files (List[str]): List of audio file paths
            video_files (List[str]): List of video file paths
            output_file (str): Output video file name
            
        Returns:
            str: Path to combined video file
        """
        if len(audio_files) != len(video_files):
            print(f"Warning: Audio files ({len(audio_files)}) and video files ({len(video_files)}) count mismatch")
            # Pad the shorter list
            max_len = max(len(audio_files), len(video_files))
            audio_files = audio_files + [None] * (max_len - len(audio_files))
            video_files = video_files + [None] * (max_len - len(video_files))
        
        output_path = os.path.join(self.output_dir, output_file)
        
        try:
            # Process each audio-video pair with precise timing
            combined_clips = []
            
            for i, (audio_path, video_path) in enumerate(zip(audio_files, video_files)):
                print(f"Processing scene {i+1}/{len(audio_files)}")
                
                # Load and validate audio first (audio is the timing reference)
                if audio_path and os.path.exists(audio_path):
                    audio_clip = AudioFileClip(audio_path)
                    target_duration = audio_clip.duration
                    print(f"  Audio duration: {target_duration:.2f}s")
                else:
                    print(f"  Warning: Audio file missing: {audio_path}")
                    target_duration = 5.0  # Default duration
                    audio_clip = None
                
                # Load video and adjust to match audio timing
                if video_path and os.path.exists(video_path):
                    # Check if it's a text file (fallback) and create a simple video
                    if video_path.endswith('.txt'):
                        video_clip = self._create_black_video(duration=target_duration)
                    else:
                        video_clip = VideoFileClip(video_path)
                        print(f"  Video duration: {video_clip.duration:.2f}s")
                        
                        # Precise duration matching
                        duration_diff = abs(video_clip.duration - target_duration)
                        if duration_diff > 0.1:  # More than 100ms difference
                            print(f"  Adjusting video timing (diff: {duration_diff:.2f}s)")
                            
                            if video_clip.duration > target_duration:
                                # Trim video to match audio
                                video_clip = video_clip.subclip(0, target_duration)
                            else:
                                # Extend video by looping or slowing down
                                if target_duration / video_clip.duration < 1.5:
                                    # Slow down video slightly (up to 1.5x slower)
                                    speed_factor = video_clip.duration / target_duration
                                    video_clip = video_clip.speedx(speed_factor)
                                else:
                                    # Loop video to reach target duration
                                    loops_needed = int(target_duration / video_clip.duration) + 1
                                    looped_clips = [video_clip] * loops_needed
                                    extended_video = concatenate_videoclips(looped_clips)
                                    video_clip = extended_video.subclip(0, target_duration)
                else:
                    # Create a black video clip if video is missing
                    print(f"  Warning: Video file missing: {video_path}")
                    video_clip = self._create_black_video(duration=target_duration)
                
                # Combine audio and video with precise timing
                if audio_clip:
                    # Ensure exact duration match
                    if abs(video_clip.duration - audio_clip.duration) > 0.05:  # 50ms tolerance
                        video_clip = video_clip.subclip(0, audio_clip.duration)
                    
                    final_clip = video_clip.set_audio(audio_clip)
                    print(f"  Final clip duration: {final_clip.duration:.2f}s")
                else:
                    # Use video without audio if audio is missing
                    final_clip = video_clip
                
                combined_clips.append(final_clip)
            
            # Concatenate all clips with precise timing
            if combined_clips:
                print("\nCombining all scenes...")
                final_video = concatenate_videoclips(combined_clips, method="compose")
                
                total_duration = sum(clip.duration for clip in combined_clips)
                print(f"Total video duration: {total_duration:.2f}s")
                
                # Write final video with high quality settings
                final_video.write_videofile(
                    output_path,
                    fps=30,
                    codec='libx264',
                    audio_codec='aac',
                    bitrate='2000k',  # Higher bitrate for better quality
                    temp_audiofile=os.path.join(self.output_dir, 'temp_audio.m4a'),
                    remove_temp=True,
                    logger=None
                )
                
                # Clean up clips
                for clip in combined_clips:
                    clip.close()
                final_video.close()
                
                print(f"Successfully created combined video: {output_path}")
                return output_path
            else:
                print("No valid clips to combine")
                return None
                
        except Exception as e:
            print(f"Error combining audio and video: {e}")
            import traceback
            traceback.print_exc()
            return self._create_fallback_video(output_path, audio_files)
    
    def sync_audio_to_video(self, audio_path: str, video_path: str, 
                           output_path: str = None) -> str:
        """
        Synchronize a single audio file with a video file.
        
        Args:
            audio_path (str): Path to audio file
            video_path (str): Path to video file
            output_path (str): Output file path (optional)
            
        Returns:
            str: Path to synchronized video file
        """
        if output_path is None:
            base_name = os.path.splitext(os.path.basename(video_path))[0]
            output_path = os.path.join(self.output_dir, f"{base_name}_synced.mp4")
        
        try:
            if not os.path.exists(video_path):
                print(f"Video file not found: {video_path}")
                return None
            
            if not os.path.exists(audio_path):
                print(f"Audio file not found: {audio_path}")
                return video_path  # Return original video
            
            video_clip = VideoFileClip(video_path)
            audio_clip = AudioFileClip(audio_path)
            
            # Adjust video duration to match audio
            if abs(video_clip.duration - audio_clip.duration) > 0.5:
                if video_clip.duration > audio_clip.duration:
                    video_clip = video_clip.subclip(0, audio_clip.duration)
                else:
                    # Speed up or slow down video to match audio
                    speed_factor = video_clip.duration / audio_clip.duration
                    video_clip = video_clip.speedx(speed_factor)
            
            # Combine audio and video
            final_clip = video_clip.set_audio(audio_clip)
            
            # Write output with explicit FPS
            final_clip.write_videofile(
                output_path,
                fps=30,
                codec='libx264',
                audio_codec='aac',
                logger=None
            )
            
            # Clean up
            video_clip.close()
            audio_clip.close()
            final_clip.close()
            
            print(f"Synchronized video created: {output_path}")
            return output_path
            
        except Exception as e:
            print(f"Error synchronizing audio and video: {e}")
            return video_path
    
    def adjust_video_timing(self, video_clips: List[VideoFileClip], 
                           target_durations: List[float]) -> List[VideoFileClip]:
        """
        Adjust video clip timings to match target durations.
        
        Args:
            video_clips (List[VideoFileClip]): List of video clips
            target_durations (List[float]): Target durations in seconds
            
        Returns:
            List[VideoFileClip]: List of adjusted video clips
        """
        adjusted_clips = []
        
        for clip, target_duration in zip(video_clips, target_durations):
            try:
                if abs(clip.duration - target_duration) <= 0.5:
                    # Duration is close enough, no adjustment needed
                    adjusted_clips.append(clip)
                elif clip.duration > target_duration:
                    # Trim clip to target duration
                    adjusted_clip = clip.subclip(0, target_duration)
                    adjusted_clips.append(adjusted_clip)
                else:
                    # Extend clip by looping or slowing down
                    if target_duration / clip.duration <= 2.0:
                        # Loop the clip
                        loops_needed = int(target_duration / clip.duration) + 1
                        adjusted_clip = clip.loop(n=loops_needed).subclip(0, target_duration)
                    else:
                        # Slow down the clip
                        speed_factor = clip.duration / target_duration
                        adjusted_clip = clip.speedx(1/speed_factor)
                    
                    adjusted_clips.append(adjusted_clip)
                    
            except Exception as e:
                print(f"Error adjusting clip timing: {e}")
                adjusted_clips.append(clip)  # Use original clip
        
        return adjusted_clips
    
    def add_transitions(self, video_clips: List[VideoFileClip], 
                       transition_duration: float = 0.5) -> List[VideoFileClip]:
        """
        Add fade transitions between video clips.
        
        Args:
            video_clips (List[VideoFileClip]): List of video clips
            transition_duration (float): Duration of transitions in seconds
            
        Returns:
            List[VideoFileClip]: List of clips with transitions
        """
        if len(video_clips) <= 1:
            return video_clips
        
        try:
            transitioned_clips = []
            
            for i, clip in enumerate(video_clips):
                if i == 0:
                    # First clip: fade in
                    clip_with_transition = clip.fadein(transition_duration)
                elif i == len(video_clips) - 1:
                    # Last clip: fade out
                    clip_with_transition = clip.fadeout(transition_duration)
                else:
                    # Middle clips: no transitions (handled by concatenation)
                    clip_with_transition = clip
                
                transitioned_clips.append(clip_with_transition)
            
            return transitioned_clips
            
        except Exception as e:
            print(f"Error adding transitions: {e}")
            return video_clips
    
    def _create_black_video(self, duration: float = 5.0, resolution: tuple = (1920, 1080)) -> VideoFileClip:
        """Create a black video clip for fallback."""
        try:
            from moviepy.editor import ColorClip
            black_clip = ColorClip(size=resolution, color=(0, 0, 0), duration=duration)
            return black_clip
        except Exception as e:
            print(f"Error creating black video: {e}")
            # Create a minimal video using numpy if available
            try:
                import numpy as np
                from moviepy.editor import ImageClip
                
                # Create a black image
                black_image = np.zeros((resolution[1], resolution[0], 3), dtype=np.uint8)
                image_clip = ImageClip(black_image, duration=duration)
                return image_clip
            except Exception as e2:
                print(f"Error creating image clip: {e2}")
                return None
    
    def _create_fallback_video(self, output_path: str, audio_files: List[str]) -> str:
        """Create a fallback video when normal processing fails."""
        try:
            # Calculate total duration from audio files
            total_duration = 0
            valid_audio_files = [f for f in audio_files if f and os.path.exists(f)]
            
            if valid_audio_files:
                for audio_file in valid_audio_files:
                    try:
                        audio_clip = AudioFileClip(audio_file)
                        total_duration += audio_clip.duration
                        audio_clip.close()
                    except:
                        total_duration += 5.0  # Default duration
            else:
                total_duration = 10.0  # Default total duration
            
            # Create a simple black video with text
            black_video = self._create_black_video(duration=total_duration)
            
            if black_video:
                black_video.write_videofile(
                    output_path,
                    fps=30,
                    codec='libx264',
                    logger=None
                )
                black_video.close()
                
                print(f"Created fallback video: {output_path}")
                return output_path
            
        except Exception as e:
            print(f"Error creating fallback video: {e}")
        
        return None
    
    def get_video_info(self, video_path: str) -> dict:
        """Get information about a video file."""
        try:
            if not os.path.exists(video_path):
                return {"error": "File not found"}
            
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
            return {"error": str(e)}
    
    def cleanup_temp_files(self):
        """Clean up temporary video files."""
        try:
            import shutil
            temp_files = [f for f in os.listdir(self.output_dir) 
                         if f.startswith('temp_') or f.endswith('.tmp')]
            
            for temp_file in temp_files:
                temp_path = os.path.join(self.output_dir, temp_file)
                try:
                    os.remove(temp_path)
                except:
                    pass
                    
            print("Cleaned up temporary video files")
            
        except Exception as e:
            print(f"Error cleaning up temp files: {e}")


def main():
    """Test the video combiner."""
    combiner = VideoCombiner()
    
    # Test with dummy files (would need actual files for real testing)
    print("VideoCombiner module loaded successfully")
    print(f"Output directory: {combiner.output_dir}")
    
    # Test video info (with a non-existent file for demonstration)
    info = combiner.get_video_info("nonexistent.mp4")
    print(f"Video info test: {info}")


if __name__ == "__main__":
    main()
