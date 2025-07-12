"""
Setup Script for Voice to Educational Video Generator
Helps users install dependencies and configure the environment.
"""

import os
import sys
import subprocess
import platform
from pathlib import Path

def print_header():
    """Print setup header."""
    print("=" * 60)
    print("🎓 Voice to Educational Video Generator - Setup")
    print("=" * 60)
    print()

def check_python_version():
    """Check if Python version is compatible."""
    print("🐍 Checking Python version...")
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python 3.8 or higher is required!")
        print(f"   Current version: {version.major}.{version.minor}.{version.micro}")
        return False
    else:
        print(f"✅ Python {version.major}.{version.minor}.{version.micro} - OK")
        return True

def install_system_dependencies():
    """Install system-level dependencies."""
    print("\n🔧 Checking system dependencies...")
    
    system = platform.system().lower()
    
    if system == "windows":
        print("📝 Windows detected. Please ensure you have:")
        print("   1. Microsoft Visual C++ Build Tools")
        print("   2. FFmpeg (download from https://ffmpeg.org/)")
        print("   3. Add FFmpeg to your PATH")
        
    elif system == "darwin":  # macOS
        print("🍎 macOS detected. Installing dependencies...")
        try:
            # Check if Homebrew is installed
            subprocess.run(["brew", "--version"], check=True, capture_output=True)
            print("   Installing FFmpeg via Homebrew...")
            subprocess.run(["brew", "install", "ffmpeg"], check=True)
            print("✅ FFmpeg installed")
        except (subprocess.CalledProcessError, FileNotFoundError):
            print("❌ Homebrew not found. Please install:")
            print("   1. Homebrew: /bin/bash -c \"$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)\"")
            print("   2. Then run: brew install ffmpeg")
    
    elif system == "linux":
        print("🐧 Linux detected. Installing dependencies...")
        try:
            # Try apt-get (Ubuntu/Debian)
            subprocess.run(["sudo", "apt-get", "update"], check=True)
            subprocess.run(["sudo", "apt-get", "install", "-y", "ffmpeg", "build-essential"], check=True)
            print("✅ Dependencies installed via apt-get")
        except subprocess.CalledProcessError:
            try:
                # Try yum (RHEL/CentOS)
                subprocess.run(["sudo", "yum", "install", "-y", "ffmpeg", "gcc", "gcc-c++"], check=True)
                print("✅ Dependencies installed via yum")
            except subprocess.CalledProcessError:
                print("❌ Could not install dependencies automatically.")
                print("   Please install FFmpeg and build tools manually.")

def install_python_dependencies():
    """Install Python dependencies."""
    print("\n📦 Installing Python dependencies...")
    
    try:
        # Upgrade pip first
        subprocess.run([sys.executable, "-m", "pip", "install", "--upgrade", "pip"], check=True)
        
        # Install requirements
        requirements_file = Path("requirements.txt")
        if requirements_file.exists():
            print("   Installing from requirements.txt...")
            subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], check=True)
            print("✅ Python dependencies installed")
        else:
            print("❌ requirements.txt not found!")
            return False
            
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install Python dependencies: {e}")
        return False
    
    return True

def setup_environment():
    """Set up environment configuration."""
    print("\n⚙️ Setting up environment...")
    
    env_file = Path(".env")
    env_example = Path(".env.example")
    
    if not env_file.exists() and env_example.exists():
        # Copy example to .env
        env_file.write_text(env_example.read_text())
        print("✅ Created .env file from example")
    
    # Check if OpenAI API key is set
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("⚠️  OpenAI API key not found!")
        print("   Please edit .env file and add your OpenAI API key:")
        print("   OPENAI_API_KEY=your_api_key_here")
        
        # Try to get API key from user
        user_key = input("\n🔑 Enter your OpenAI API key (or press Enter to skip): ").strip()
        if user_key:
            # Update .env file
            env_content = env_file.read_text() if env_file.exists() else ""
            if "OPENAI_API_KEY=" in env_content:
                env_content = env_content.replace("OPENAI_API_KEY=your_openai_api_key_here", f"OPENAI_API_KEY={user_key}")
            else:
                env_content += f"\nOPENAI_API_KEY={user_key}\n"
            env_file.write_text(env_content)
            print("✅ API key saved to .env file")
    else:
        print("✅ OpenAI API key found")

def create_directories():
    """Create necessary directories."""
    print("\n📁 Creating directories...")
    
    directories = ["output", "temp"]
    for dir_name in directories:
        dir_path = Path(dir_name)
        dir_path.mkdir(exist_ok=True)
        print(f"✅ Created {dir_name}/ directory")

def test_installation():
    """Test if installation is working."""
    print("\n🧪 Testing installation...")
    
    try:
        # Test imports
        print("   Testing imports...")
        
        # Core imports
        import openai
        print("   ✅ OpenAI")
        
        import streamlit
        print("   ✅ Streamlit")
        
        # Try manim import
        try:
            import manim
            print("   ✅ Manim")
        except ImportError:
            print("   ⚠️  Manim import failed - may need manual installation")
        
        # Try moviepy import
        try:
            import moviepy
            print("   ✅ MoviePy")
        except ImportError:
            print("   ⚠️  MoviePy import failed")
        
        # Try pydub import
        try:
            import pydub
            print("   ✅ Pydub")
        except ImportError:
            print("   ⚠️  Pydub import failed")
        
        print("✅ Basic imports successful")
        
    except ImportError as e:
        print(f"❌ Import test failed: {e}")
        return False
    
    return True

def print_next_steps():
    """Print next steps for the user."""
    print("\n🚀 Setup Complete! Next Steps:")
    print("-" * 40)
    print("1. Make sure your OpenAI API key is set in .env file")
    print("2. Test the installation:")
    print("   python -c \"import openai, streamlit; print('✅ Ready to go!')\"")
    print("3. Run the application:")
    print("   streamlit run app.py")
    print("4. Upload an audio file and generate your first educational video!")
    print()
    print("📚 Documentation and examples:")
    print("   - Check the README.md file for detailed usage instructions")
    print("   - Sample audio files can be found in the examples/ folder")
    print()
    print("❓ Need help?")
    print("   - Check the troubleshooting section in README.md") 
    print("   - Make sure FFmpeg is installed and in your PATH")
    print("   - Ensure you have a valid OpenAI API key")

def main():
    """Main setup function."""
    print_header()
    
    # Check Python version
    if not check_python_version():
        print("\n❌ Setup failed: Incompatible Python version")
        sys.exit(1)
    
    # Install system dependencies
    install_system_dependencies()
    
    # Install Python dependencies
    if not install_python_dependencies():
        print("\n❌ Setup failed: Could not install Python dependencies")
        sys.exit(1)
    
    # Setup environment
    setup_environment()
    
    # Create directories
    create_directories()
    
    # Test installation
    if test_installation():
        print("\n✅ Installation test passed!")
    else:
        print("\n⚠️  Installation test had some issues, but you can still try running the app")
    
    # Print next steps
    print_next_steps()

if __name__ == "__main__":
    main()
