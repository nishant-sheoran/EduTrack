"""
Check MoviePy structure and available modules.
"""
import moviepy
print(f"MoviePy version: {moviepy.__version__}")
print(f"MoviePy location: {moviepy.__file__}")

# Check what's available in moviepy
print("\nAvailable in moviepy:")
for attr in dir(moviepy):
    if not attr.startswith('_'):
        print(f"  - {attr}")

# Try different import patterns
print("\n=== Testing import patterns ===")

try:
    from moviepy.video.io.VideoFileClip import VideoFileClip
    print("✅ VideoFileClip from moviepy.video.io.VideoFileClip")
    
    # Test instance creation
    print("Testing VideoFileClip methods:")
    methods = [m for m in dir(VideoFileClip) if not m.startswith('_')]
    for method in methods[:10]:  # Show first 10 methods
        print(f"  - {method}")
    
except ImportError as e:
    print(f"❌ VideoFileClip from moviepy.video.io.VideoFileClip: {e}")

try:
    from moviepy.audio.io.AudioFileClip import AudioFileClip
    print("✅ AudioFileClip from moviepy.audio.io.AudioFileClip")
except ImportError as e:
    print(f"❌ AudioFileClip from moviepy.audio.io.AudioFileClip: {e}")

try:
    from moviepy.video.compositing.CompositeVideoClip import CompositeVideoClip
    print("✅ CompositeVideoClip from moviepy.video.compositing.CompositeVideoClip")
except ImportError as e:
    print(f"❌ CompositeVideoClip from moviepy.video.compositing.CompositeVideoClip: {e}")
