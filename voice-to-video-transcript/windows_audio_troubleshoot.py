#!/usr/bin/env python3
"""
Windows Audio Troubleshooting Script for EduTrack
This script helps diagnose and fix microphone access issues on Windows.
"""

import subprocess
import sys
import json
import platform
import logging
from pathlib import Path

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def check_system_info():
    """Check basic system information"""
    print("\n" + "="*60)
    print("SYSTEM INFORMATION")
    print("="*60)
    print(f"Platform: {platform.platform()}")
    print(f"Python Version: {sys.version}")
    print(f"Architecture: {platform.architecture()}")
    
def check_ffmpeg_installation():
    """Check if FFmpeg is properly installed"""
    print("\n" + "="*60)
    print("FFMPEG INSTALLATION CHECK")
    print("="*60)
    
    try:
        result = subprocess.run(['ffmpeg', '-version'], 
                              capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            lines = result.stdout.split('\n')
            print(f"✓ FFmpeg is installed: {lines[0] if lines else 'Unknown version'}")
            return True
        else:
            print("✗ FFmpeg is installed but returned error")
            print(f"Error: {result.stderr}")
            return False
    except subprocess.TimeoutExpired:
        print("✗ FFmpeg command timed out")
        return False
    except FileNotFoundError:
        print("✗ FFmpeg is not installed or not in PATH")
        return False
    except Exception as e:
        print(f"✗ Error checking FFmpeg: {e}")
        return False

def list_directshow_devices():
    """List all DirectShow audio devices"""
    print("\n" + "="*60)
    print("DIRECTSHOW AUDIO DEVICES")
    print("="*60)
    
    try:
        # List audio input devices
        cmd = ['ffmpeg', '-f', 'dshow', '-list_devices', 'true', '-i', 'dummy']
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=15)
        
        output = result.stderr  # FFmpeg outputs device list to stderr
        print("Raw FFmpeg Output:")
        print("-" * 40)
        print(output)
        print("-" * 40)
        
        # Parse audio input devices
        audio_devices = []
        lines = output.split('\n')
        in_audio_section = False
        
        for line in lines:
            if 'DirectShow audio devices' in line:
                in_audio_section = True
                continue
            elif 'DirectShow video devices' in line:
                in_audio_section = False
                continue
            elif in_audio_section and '"' in line:
                # Extract device name between quotes
                start = line.find('"') + 1
                end = line.rfind('"')
                if start < end:
                    device_name = line[start:end]
                    audio_devices.append(device_name)
        
        print(f"\nFound {len(audio_devices)} audio input devices:")
        for i, device in enumerate(audio_devices, 1):
            print(f"  {i}. {device}")
        
        return audio_devices
        
    except subprocess.TimeoutExpired:
        print("✗ Device listing command timed out")
        return []
    except Exception as e:
        print(f"✗ Error listing devices: {e}")
        return []

def test_device_access(device_name):
    """Test if we can access a specific audio device"""
    print(f"\n{'='*60}")
    print(f"TESTING DEVICE: {device_name}")
    print("="*60)
    
    try:
        # Try to record 2 seconds from the device
        cmd = [
            'ffmpeg', '-f', 'dshow', 
            '-i', f'audio={device_name}',
            '-t', '2',  # Record for 2 seconds
            '-y',  # Overwrite output file
            'test_recording.wav'
        ]
        
        print(f"Command: {' '.join(cmd)}")
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=15)
        
        if result.returncode == 0:
            print("✓ Successfully recorded from device!")
            # Check if file was created
            if Path('test_recording.wav').exists():
                size = Path('test_recording.wav').stat().st_size
                print(f"✓ Output file created: test_recording.wav ({size} bytes)")
                return True
            else:
                print("✗ No output file created")
                return False
        else:
            print("✗ Failed to record from device")
            print(f"Error output: {result.stderr}")
            return False
            
    except subprocess.TimeoutExpired:
        print("✗ Recording test timed out")
        return False
    except Exception as e:
        print(f"✗ Error testing device: {e}")
        return False

def check_windows_permissions():
    """Check Windows microphone permissions"""
    print("\n" + "="*60)
    print("WINDOWS MICROPHONE PERMISSIONS")
    print("="*60)
    
    print("To check Windows microphone permissions:")
    print("1. Open Windows Settings (Win + I)")
    print("2. Go to Privacy & Security > Microphone")
    print("3. Ensure 'Microphone access' is turned ON")
    print("4. Ensure 'Let apps access your microphone' is turned ON")
    print("5. Check if Python/Command Prompt has microphone access")
    print("\nAlternatively, you can:")
    print("- Right-click the speaker icon in system tray")
    print("- Select 'Open Sound settings'")
    print("- Go to 'Sound Control Panel' > Recording tab")
    print("- Check if your microphone is listed and enabled")

def check_alternative_devices():
    """Suggest alternative device names to try"""
    print("\n" + "="*60)
    print("ALTERNATIVE DEVICE NAMES TO TRY")
    print("="*60)
    
    common_device_names = [
        "Microphone",
        "Microphone (Realtek High Definition Audio)",
        "Microphone Array",
        "Built-in Microphone", 
        "Internal Microphone",
        "Default",
        "Stereo Mix",
        "Line In"
    ]
    
    print("Common Windows microphone device names:")
    for i, name in enumerate(common_device_names, 1):
        print(f"  {i}. {name}")
    
    return common_device_names

def test_pyaudio_fallback():
    """Test if PyAudio can access audio devices as a fallback"""
    print("\n" + "="*60)
    print("PYAUDIO FALLBACK TEST")
    print("="*60)
    
    try:
        import pyaudio
        
        p = pyaudio.PyAudio()
        device_count = p.get_device_count()
        print(f"PyAudio found {device_count} audio devices:")
        
        input_devices = []
        for i in range(device_count):
            info = p.get_device_info_by_index(i)
            if info['maxInputChannels'] > 0:
                input_devices.append((i, info['name']))
                print(f"  {i}: {info['name']} (inputs: {info['maxInputChannels']})")
        
        p.terminate()
        
        if input_devices:
            print(f"\n✓ PyAudio found {len(input_devices)} input devices")
            print("Consider using PyAudio as fallback for Python < 3.13")
            return True
        else:
            print("\n✗ No input devices found by PyAudio")
            return False
            
    except ImportError:
        print("PyAudio not installed. To install: pip install pyaudio")
        return False
    except Exception as e:
        print(f"Error testing PyAudio: {e}")
        return False

def create_test_recording_script():
    """Create a simple test script for manual testing"""
    script_content = '''#!/usr/bin/env python3
"""
Simple test script to manually test different microphone device names
"""
import subprocess
import sys

def test_recording(device_name, duration=3):
    """Test recording from a specific device"""
    print(f"Testing device: {device_name}")
    
    cmd = [
        'ffmpeg', '-f', 'dshow', 
        '-i', f'audio={device_name}',
        '-t', str(duration),
        '-y', 'manual_test.wav'
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=duration + 5)
        if result.returncode == 0:
            print(f"✓ SUCCESS: Recorded {duration} seconds to manual_test.wav")
            return True
        else:
            print(f"✗ FAILED: {result.stderr[:200]}...")
            return False
    except Exception as e:
        print(f"✗ ERROR: {e}")
        return False

if __name__ == "__main__":
    if len(sys.argv) > 1:
        device_name = sys.argv[1]
        test_recording(device_name)
    else:
        print("Usage: python manual_test_recording.py 'Device Name'")
        print("Example: python manual_test_recording.py 'Microphone'")
'''
    
    with open('manual_test_recording.py', 'w') as f:
        f.write(script_content)
    
    print("\n" + "="*60)
    print("MANUAL TEST SCRIPT CREATED")
    print("="*60)
    print("Created 'manual_test_recording.py' for manual device testing")
    print("Usage: python manual_test_recording.py 'Device Name'")

def main():
    """Main troubleshooting function"""
    print("EduTrack Windows Audio Troubleshooting")
    print("This script will help diagnose microphone access issues on Windows")
    
    # Basic system check
    check_system_info()
    
    # Check FFmpeg
    if not check_ffmpeg_installation():
        print("\n❌ FFmpeg is not properly installed. Please install FFmpeg first.")
        return
    
    # List devices
    devices = list_directshow_devices()
    
    # Test device access if devices found
    working_devices = []
    if devices:
        print(f"\nTesting access to {len(devices)} found devices...")
        for device in devices:
            if test_device_access(device):
                working_devices.append(device)
    
    # Check alternative device names if no devices found or none working
    if not devices or not working_devices:
        alternative_devices = check_alternative_devices()
        print(f"\nTesting alternative device names...")
        for device in alternative_devices:
            if test_device_access(device):
                working_devices.append(device)
    
    # Check PyAudio as fallback
    test_pyaudio_fallback()
    
    # Check Windows permissions
    check_windows_permissions()
    
    # Create manual test script
    create_test_recording_script()
    
    # Summary
    print("\n" + "="*60)
    print("TROUBLESHOOTING SUMMARY")
    print("="*60)
    
    if working_devices:
        print(f"✓ Found {len(working_devices)} working audio devices:")
        for device in working_devices:
            print(f"  - {device}")
        print(f"\nYou can use any of these device names in your audio_recorder.py")
    else:
        print("❌ No working audio devices found")
        print("\nNext steps:")
        print("1. Check Windows microphone permissions (see instructions above)")
        print("2. Test with Windows Voice Recorder app")
        print("3. Update audio drivers")
        print("4. Try running as Administrator")
        print("5. Use the manual test script: python manual_test_recording.py 'Device Name'")
    
    # Cleanup test files
    try:
        Path('test_recording.wav').unlink(missing_ok=True)
        Path('manual_test.wav').unlink(missing_ok=True)
    except:
        pass

if __name__ == "__main__":
    main()
