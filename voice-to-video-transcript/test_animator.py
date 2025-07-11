"""
Quick test for the animator module with corrected indentation.
"""
import asyncio
from script_generator import ScriptGenerator
from animator import VideoAnimator

async def test_animator():
    """Test the animator with proper async handling."""
    # Generate a script
    script_generator = ScriptGenerator()
    script = await script_generator.generate_script(
        "This is a sample audio transcript about linear algebra and matrix operations."
    )
    
    # Create animation
    animator = VideoAnimator()
    scene_file = await animator.create_animation(script)
    
    print(f"✅ Animation scene file created: {scene_file}")
    return scene_file

if __name__ == "__main__":
    asyncio.run(test_animator())
