"""
Direct test of the animator with simple data
"""
import asyncio
from animator import VideoAnimator

async def test_simple_animator():
    """Test the animator with hardcoded data."""
    try:
        print("Testing updated animator...")
        
        # Create animator
        animator = VideoAnimator()
        
        # Simple test data
        test_script = {
            "title": "Simple Test Video",
            "sections": []
        }
        
        print("Creating animation...")
        video_path = await animator.create_animation(test_script)
        print(f"✅ Animation created: {video_path}")
        
        return True
        
    except Exception as e:
        print(f"❌ Animation failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = asyncio.run(test_simple_animator())
    if success:
        print("🎉 Simple animator test passed!")
    else:
        print("💥 Simple animator test failed!")
