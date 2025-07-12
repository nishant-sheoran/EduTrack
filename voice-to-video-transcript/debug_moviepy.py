"""
Debug MoviePy import to see what's available.
"""
try:
    from moviepy import VideoFileClip, AudioFileClip
    print("✅ MoviePy import successful")
    
    # Check what methods are available
    video_clip = VideoFileClip.__dict__
    print("\nVideoFileClip methods:")
    for method in sorted(video_clip.keys()):
        if not method.startswith('_'):
            print(f"  - {method}")
            
except ImportError as e:
    print(f"❌ MoviePy import failed: {e}")
    
try:
    from moviepy.editor import VideoFileClip, AudioFileClip
    print("✅ MoviePy.editor import successful")
    
    # Check what methods are available
    video_clip = VideoFileClip.__dict__
    print("\nVideoFileClip methods:")
    for method in sorted(video_clip.keys()):
        if not method.startswith('_'):
            print(f"  - {method}")
            
except ImportError as e:
    print(f"❌ MoviePy.editor import failed: {e}")
