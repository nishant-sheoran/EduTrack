"""
Test what methods are actually available in VideoFileClip instance.
"""
from moviepy.video.io.VideoFileClip import VideoFileClip
import os

# Use the animation file we know exists
video_path = r"output\videos\educational_scene\720p30\EducationalScene.mp4"

if os.path.exists(video_path):
    try:
        video_clip = VideoFileClip(video_path)
        print("✅ VideoFileClip loaded successfully")
        print(f"Duration: {video_clip.duration}")
        
        print("\nAvailable methods:")
        methods = [m for m in dir(video_clip) if not m.startswith('_')]
        for method in sorted(methods):
            print(f"  - {method}")
            
        video_clip.close()
        
    except Exception as e:
        print(f"❌ Error loading video: {e}")
else:
    print(f"❌ Video file not found: {video_path}")
