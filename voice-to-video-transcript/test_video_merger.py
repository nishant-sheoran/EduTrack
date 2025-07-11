"""
Test video merging functionality.
"""
import asyncio
from video_merger import VideoMerger
from narrator import Narrator

async def test_video_merger():
    """Test video merging with actual files."""
    # Create a sample narration
    narrator = Narrator()
    audio_path = await narrator.create_narration(
        "This is a test narration for video merging functionality."
    )
    
    # Test video merging
    merger = VideoMerger()
    
    # Check if we have the animation file
    video_path = r"output\videos\educational_scene\720p30\EducationalScene.mp4"
    
    try:
        final_video = await merger.merge_audio_video(video_path, audio_path)
        print(f"✅ Final video created: {final_video}")
        return final_video
    except Exception as e:
        print(f"❌ Video merging failed: {e}")
        return None

if __name__ == "__main__":
    asyncio.run(test_video_merger())
