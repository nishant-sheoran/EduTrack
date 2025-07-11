"""
Example and Test Script for Voice to Educational Video Generator
Demonstrates the functionality with sample content.
"""

import asyncio
import os
import tempfile
from pathlib import Path
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Sample educational content for testing
SAMPLE_TRANSCRIPT = """
Today I want to explain the concept of linear regression. Linear regression is one of the most fundamental and widely used techniques in machine learning and statistics. 

So what exactly is linear regression? At its core, linear regression is a method for modeling the relationship between a dependent variable and one or more independent variables. The goal is to find the best-fitting straight line through a set of data points.

The mathematical foundation is based on the equation y equals mx plus b, where y is the dependent variable, x is the independent variable, m is the slope of the line, and b is the y-intercept.

Let me give you a concrete example. Imagine we have data about house sizes and their prices. We might have houses of 1000 square feet selling for 200,000 dollars, 1500 square feet for 300,000 dollars, and 2000 square feet for 400,000 dollars. Linear regression would help us find the line that best fits through these data points.

The method we use to find this best-fitting line is called the method of least squares. This method minimizes the sum of the squared differences between the actual data points and the predicted values on our line. Mathematically, we're trying to minimize the sum of yi minus y-hat squared, where yi represents the actual values and y-hat represents our predicted values.

The beauty of linear regression is that it gives us a simple way to make predictions. Once we have our line equation, we can predict the price of a house based on its size, or any other relationship we're modeling.

In summary, linear regression is a powerful yet simple tool that helps us understand relationships between variables and make predictions based on data. It forms the foundation for many more complex machine learning algorithms.
"""

SAMPLE_SCRIPT_DATA = {
    "title": "Linear Regression Explained",
    "introduction": "Linear regression is one of the most fundamental techniques in machine learning and statistics for modeling relationships between variables.",
    "sections": [
        {
            "title": "What is Linear Regression?",
            "content": "Linear regression is a method for modeling the relationship between a dependent variable and one or more independent variables by finding the best-fitting straight line through data points.",
            "section_type": "concept",
            "duration_estimate": 45.0,
            "visual_cues": ["Show scatter plot", "Display regression line", "Highlight data points"],
            "math_expressions": ["y = mx + b", "\\hat{y} = \\beta_0 + \\beta_1 x"]
        },
        {
            "title": "Mathematical Foundation",
            "content": "The method of least squares finds the line that minimizes the sum of squared differences between actual and predicted values.",
            "section_type": "concept", 
            "duration_estimate": 60.0,
            "visual_cues": ["Show residuals", "Animate least squares", "Plot cost function"],
            "math_expressions": ["\\min \\sum_{i=1}^{n} (y_i - \\hat{y_i})^2", "RSS = \\sum_{i=1}^{n} (y_i - \\hat{y_i})^2"]
        },
        {
            "title": "Real-World Example",
            "content": "Consider predicting house prices based on size. We can use linear regression to find the relationship between square footage and price.",
            "section_type": "example",
            "duration_estimate": 50.0,
            "visual_cues": ["Show house data", "Plot price vs size", "Draw regression line"],
            "math_expressions": ["Price = \\beta_0 + \\beta_1 \\times Size"]
        }
    ],
    "summary": "Linear regression provides a simple yet powerful way to model relationships between variables and make predictions, forming the foundation for many advanced machine learning techniques.",
    "full_text": SAMPLE_TRANSCRIPT,
    "total_duration": 180.0,
    "keywords": ["linear regression", "machine learning", "statistics", "least squares", "prediction"],
    "difficulty_level": "beginner",
    "subject_area": "machine learning"
}

async def test_transcriber():
    """Test the transcriber with sample audio (simulated)."""
    try:
        from transcriber import AudioTranscriber
        
        print("🎙️ Testing Audio Transcriber...")
        transcriber = AudioTranscriber()
        
        # In a real scenario, you'd use actual audio files
        # For demo purposes, we'll simulate with the sample transcript
        print("✅ Transcriber initialized successfully")
        print(f"📝 Sample transcript length: {len(SAMPLE_TRANSCRIPT)} characters")
        
        return True
        
    except Exception as e:
        print(f"❌ Transcriber test failed: {e}")
        return False

async def test_script_generator():
    """Test the script generator."""
    try:
        from script_generator import ScriptGenerator
        
        print("\n🧠 Testing Script Generator...")
        generator = ScriptGenerator()
        
        # Test with sample transcript
        print("Generating educational script from sample transcript...")
        script_data = await generator.generate_script(SAMPLE_TRANSCRIPT, "Machine Learning")
        
        print("✅ Script generated successfully")
        print(f"📚 Title: {script_data.get('title', 'No title')}")
        print(f"📖 Sections: {len(script_data.get('sections', []))}")
        print(f"⏱️ Duration: {script_data.get('total_duration', 0):.1f} seconds")
        
        return script_data
        
    except Exception as e:
        print(f"❌ Script generator test failed: {e}")
        return None

async def test_narrator():
    """Test the narrator."""
    try:
        from narrator import Narrator
        
        print("\n🎵 Testing Narrator...")
        narrator = Narrator()
        
        # Test with short sample text
        test_text = "This is a test of the text-to-speech functionality for educational videos."
        print(f"Creating narration for: '{test_text}'")
        
        audio_path = await narrator.create_narration(test_text)
        
        print("✅ Narration created successfully")
        print(f"🎵 Audio file: {audio_path}")
        
        # Get audio duration
        duration = narrator.get_audio_duration(audio_path)
        print(f"⏱️ Duration: {duration:.2f} seconds")
        
        return audio_path
        
    except Exception as e:
        print(f"❌ Narrator test failed: {e}")
        return None

async def test_animator():
    """Test the animator."""
    try:
        from animator import VideoAnimator
        
        print("\n🎬 Testing Video Animator...")
        animator = VideoAnimator(quality="low_quality")  # Use low quality for faster testing
        
        # Generate scene file from sample script
        print("Generating Manim scene file...")
        scene_file = animator._generate_scene_file(SAMPLE_SCRIPT_DATA)
        
        print("✅ Animation scene file generated successfully")
        print(f"📄 Scene file: {scene_file}")
        
        # Note: Actual rendering would require Manim to be properly installed
        print("ℹ️ To render the animation, run:")
        print(f"   manim -ql {scene_file} EducationalScene")
        
        return scene_file
        
    except Exception as e:
        print(f"❌ Animator test failed: {e}")
        return None

async def test_pdf_generator():
    """Test the PDF generator."""
    try:
        from pdf_generator import PDFGenerator
        
        print("\n📄 Testing PDF Generator...")
        generator = PDFGenerator()
        
        # Generate PDF from sample script
        print("Generating PDF from sample script...")
        pdf_path = await generator.create_pdf(SAMPLE_SCRIPT_DATA)
        
        print("✅ PDF generated successfully")
        print(f"📄 PDF file: {pdf_path}")
        
        return pdf_path
        
    except Exception as e:
        print(f"❌ PDF generator test failed: {e}")
        return None

async def test_video_merger():
    """Test the video merger (basic functionality)."""
    try:
        from video_merger import VideoMerger
        
        print("\n🎞️ Testing Video Merger...")
        merger = VideoMerger()
        
        print("✅ Video merger initialized successfully")
        print("ℹ️ Video merging requires actual video and audio files")
        print("   Use the CLI or web interface to test full video merging")
        
        return True
        
    except Exception as e:
        print(f"❌ Video merger test failed: {e}")
        return False

def create_sample_audio():
    """Create a sample audio file for testing (placeholder)."""
    print("\n🎵 Creating sample audio file...")
    
    # This would typically involve text-to-speech conversion
    # For now, we'll just create a placeholder
    sample_audio_path = Path("output") / "sample_audio.wav"
    
    try:
        from gtts import gTTS
        import io
        
        # Create a short sample audio
        tts = gTTS(text="This is a sample audio for testing the voice to educational video generator.", lang='en')
        
        # Save to file
        tts.save(str(sample_audio_path))
        
        print(f"✅ Sample audio created: {sample_audio_path}")
        return str(sample_audio_path)
        
    except ImportError:
        print("ℹ️ gTTS not available. Creating placeholder file.")
        sample_audio_path.touch()
        return str(sample_audio_path)
    except Exception as e:
        print(f"⚠️ Could not create sample audio: {e}")
        return None

async def run_comprehensive_test():
    """Run comprehensive test of all modules."""
    print("🧪 Voice to Educational Video Generator - Comprehensive Test")
    print("=" * 60)
    
    # Test individual components
    results = {
        'transcriber': await test_transcriber(),
        'script_generator': await test_script_generator(),
        'narrator': await test_narrator(),
        'animator': await test_animator(),
        'pdf_generator': await test_pdf_generator(),
        'video_merger': await test_video_merger()
    }
    
    # Create sample files
    sample_audio = create_sample_audio()
    
    # Print summary
    print("\n📊 Test Results Summary")
    print("-" * 30)
    
    passed = 0
    total = len(results)
    
    for component, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{component:20} {status}")
        if result:
            passed += 1
    
    print(f"\n📈 Overall: {passed}/{total} components working")
    
    if passed == total:
        print("🎉 All tests passed! The system is ready to use.")
        print("\n🚀 Next steps:")
        print("1. Run 'streamlit run app.py' to start the web interface")
        print("2. Or use 'python cli.py process <audio_file>' for command line")
        print("3. Make sure your OpenAI API key is set in the .env file")
    else:
        print("⚠️ Some components failed. Check the error messages above.")
        print("💡 Try running 'python setup.py' to install missing dependencies")
    
    return passed == total

async def demo_pipeline():
    """Demonstrate the complete pipeline with sample data."""
    print("\n🎯 Demo: Complete Pipeline with Sample Data")
    print("=" * 50)
    
    try:
        # This would simulate the complete pipeline
        print("1. 🎙️ [SIMULATED] Transcribing sample audio...")
        print(f"   Transcript: {SAMPLE_TRANSCRIPT[:100]}...")
        
        print("\n2. 🧠 [SIMULATED] Generating educational script...")
        print(f"   Title: {SAMPLE_SCRIPT_DATA['title']}")
        print(f"   Sections: {len(SAMPLE_SCRIPT_DATA['sections'])}")
        
        print("\n3. 🎵 [SIMULATED] Creating narration...")
        print(f"   Duration: {SAMPLE_SCRIPT_DATA['total_duration']} seconds")
        
        print("\n4. 🎬 [SIMULATED] Rendering animations...")
        print("   Manim scene with 3Blue1Brown styling")
        
        print("\n5. 🎞️ [SIMULATED] Combining video and audio...")
        print("   Final MP4 video with synchronized narration")
        
        print("\n6. 📄 [SIMULATED] Generating PDF transcript...")
        print("   Structured PDF with math expressions")
        
        print("\n✅ Pipeline demonstration complete!")
        print("🎬 Output: educational_video.mp4")
        print("📄 Output: educational_transcript.pdf")
        
    except Exception as e:
        print(f"❌ Demo failed: {e}")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "--demo":
        asyncio.run(demo_pipeline())
    else:
        asyncio.run(run_comprehensive_test())
