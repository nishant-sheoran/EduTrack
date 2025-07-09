"""
End-to-End Pipeline Test
Tests the full workflow: transcript -> script -> animation + narration -> final video
"""
import asyncio
from script_generator import ScriptGenerator
from narrator import Narrator
from animator import VideoAnimator
from video_merger import VideoMerger
import os

async def test_full_pipeline():
    """Test the complete pipeline from script to final video."""
    sample_transcript = """
    Linear regression is one of the fundamental concepts in machine learning and statistics. 
    It helps us understand the relationship between variables and make predictions. 
    The basic idea is to find the best line that fits through a set of data points.
    """
    
    print("🎬 Starting End-to-End Pipeline Test")
    print("=" * 50)
    
    try:
        # Step 1: Generate educational script
        print("📝 Step 1: Generating educational script...")
        script_generator = ScriptGenerator()
        script = await script_generator.generate_script(sample_transcript)
        print(f"✅ Script generated: {script['title']}")
        
        # Step 2: Create narration
        print("🎵 Step 2: Creating narration...")
        narrator = Narrator()
        narration_text = script['sections'][0]['content'][:100] + "..."  # First 100 chars
        narration_path = await narrator.create_narration(narration_text)
        print(f"✅ Narration created: {narration_path}")
        
        # Step 3: Create animation
        print("🎬 Step 3: Creating animation...")
        animator = VideoAnimator()
        animation_path = await animator.create_animation(script)
        print(f"✅ Animation created: {animation_path}")
        
        # Step 4: Merge video and audio
        print("🎞️ Step 4: Merging video and audio...")
        video_merger = VideoMerger()
        final_video = await video_merger.merge_audio_video(
            animation_path, 
            narration_path,
            sync_method="cut"
        )
        print(f"✅ Final video created: {final_video}")
        
        # Check if final video exists
        if os.path.exists(final_video):
            file_size = os.path.getsize(final_video) / (1024*1024)  # MB
            print(f"📊 Final video file size: {file_size:.2f} MB")
            print("🎉 End-to-End Pipeline Test SUCCESSFUL!")
            return final_video
        else:
            print("❌ Final video file not found!")
            return None
            
    except Exception as e:
        print(f"❌ Pipeline test failed: {e}")
        return None

if __name__ == "__main__":
    result = asyncio.run(test_full_pipeline())
    if result:
        print(f"\n🎯 SUCCESS: Complete video created at: {result}")
    else:
        print("\n💥 FAILED: Pipeline test unsuccessful")
