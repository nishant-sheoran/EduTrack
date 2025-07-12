"""
Test script to verify Manim is working properly
"""
import subprocess
import sys
import os

def test_manim_basic():
    """Test basic Manim functionality"""
    print("Testing Manim installation...")
    
    # Test 1: Check if manim command exists
    try:
        result = subprocess.run(
            ['manim', '--version'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=10
        )
        print(f"✅ Manim version: {result.stdout.strip()}")
    except Exception as e:
        print(f"❌ Manim command failed: {e}")
        return False
    
    # Test 2: Create a simple scene
    simple_scene = '''
from manim import *

class SimpleTest(Scene):
    def construct(self):
        self.camera.background_color = "#0e1116"
        
        # Simple text
        text = Text("Hello Manim!", font_size=48, color=BLUE)
        self.play(Write(text))
        self.wait(2)
        self.play(FadeOut(text))
'''
    
    # Write test scene
    with open('test_scene.py', 'w') as f:
        f.write(simple_scene)
    
    print("Testing simple scene rendering...")
    
    # Test 3: Render the simple scene
    try:
        cmd = [
            'manim',
            '-ql',  # Low quality for fast testing
            '--media_dir', 'test_output',
            'test_scene.py',
            'SimpleTest'
        ]
        
        print(f"Running: {' '.join(cmd)}")
        
        result = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=30
        )
        
        print(f"Return code: {result.returncode}")
        print(f"Stdout: {result.stdout}")
        print(f"Stderr: {result.stderr}")
        
        if result.returncode == 0:
            print("✅ Simple scene rendered successfully!")
            return True
        else:
            print(f"❌ Simple scene failed with code {result.returncode}")
            return False
            
    except subprocess.TimeoutExpired:
        print("❌ Manim rendering timed out")
        return False
    except Exception as e:
        print(f"❌ Error running Manim: {e}")
        return False
    
    finally:
        # Cleanup
        if os.path.exists('test_scene.py'):
            os.unlink('test_scene.py')

if __name__ == "__main__":
    success = test_manim_basic()
    if success:
        print("\n🎉 Manim is working correctly!")
    else:
        print("\n💥 Manim has issues that need to be fixed")
    
    sys.exit(0 if success else 1)
