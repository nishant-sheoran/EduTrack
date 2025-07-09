#!/usr/bin/env python3
"""
FFmpeg Audio Device Test
Quick test to check if FFmpeg can access your microphone.
"""

import subprocess
import os
import sys
import tempfile
from pathlib import Path

def check_ffmpeg_availability():
    """Check if FFmpeg is available and what version"""
    try:
        result = subprocess.run(['ffmpeg', '-version'], 
                              capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            version_line = result.stdout.split('\n')[0]
            print(f"✅ FFmpeg available: {version_line}")
            return True
        else:
            print(f"❌ FFmpeg version check failed: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ FFmpeg not found: {e}")
        return False

def list_audio_devices():
    """List available audio input devices"""
    print("\n🎤 Checking audio input devices...")
    
    if os.name == 'nt':  # Windows
        print("Listing DirectShow audio devices:")
        try:
            result = subprocess.run([
                'ffmpeg', '-list_devices', 'true', '-f', 'dshow', '-i', 'dummy'
            ], capture_output=True, text=True, timeout=10)
            
            # FFmpeg outputs device info to stderr
            output = result.stderr
            if "DirectShow audio devices" in output:
                lines = output.split('\n')
                for line in lines:
                    if '"' in line and 'audio' in line.lower():
                        print(f"  📱 {line.strip()}")
            else:
                print("❌ No DirectShow audio devices found in output")
                print("Full output:", output[:500] + "..." if len(output) > 500 else output)
                
        except Exception as e:
            print(f"❌ Error listing devices: {e}")
    
    elif sys.platform == 'darwin':  # macOS
        print("Listing AVFoundation audio devices:")
        try:
            result = subprocess.run([
                'ffmpeg', '-f', 'avfoundation', '-list_devices', 'true', '-i', ''
            ], capture_output=True, text=True, timeout=10)
            print("Device output:", result.stderr[:1000])
        except Exception as e:
            print(f"❌ Error listing devices: {e}")
    
    else:  # Linux
        print("Listing PulseAudio devices:")
        try:
            result = subprocess.run([
                'ffmpeg', '-f', 'pulse', '-list_devices', 'true', '-i', ''
            ], capture_output=True, text=True, timeout=10)
            print("Device output:", result.stderr[:1000])
        except Exception as e:
            print(f"❌ Error listing devices: {e}")

def test_recording():
    """Test actual recording"""
    print("\n🎙️ Testing 3-second recording...")
    
    # Create temp file
    temp_file = Path(tempfile.gettempdir()) / "ffmpeg_test_recording.wav"
    
    if os.name == 'nt':  # Windows
        # Try different microphone device names
        device_names = [
            'audio=Microphone',
            'audio=Microphone (Realtek Audio)',
            'audio=Microphone Array',
            'audio=Default Audio Device',
            'audio=Stereo Mix'
        ]
        
        for device_name in device_names:
            print(f"\n🔍 Trying device: {device_name}")
            try:
                cmd = [
                    'ffmpeg',
                    '-f', 'dshow',
                    '-i', device_name,
                    '-acodec', 'pcm_s16le',
                    '-ar', '44100',
                    '-ac', '1',
                    '-t', '3',  # Record for 3 seconds
                    '-y',
                    str(temp_file)
                ]
                
                print(f"Command: {' '.join(cmd)}")
                result = subprocess.run(cmd, capture_output=True, text=True, timeout=15)
                
                if result.returncode == 0 and temp_file.exists():
                    file_size = temp_file.stat().st_size
                    print(f"✅ Recording successful! File size: {file_size} bytes")
                    print(f"📁 File saved: {temp_file}")
                    
                    # Clean up
                    temp_file.unlink()
                    return True
                else:
                    print(f"❌ Recording failed with device {device_name}")
                    if result.stderr:
                        print(f"Error: {result.stderr[:300]}")
                    
            except Exception as e:
                print(f"❌ Exception with device {device_name}: {e}")
        
        print("❌ All device names failed")
        return False
    
    else:
        # macOS/Linux
        if sys.platform == 'darwin':
            cmd = ['ffmpeg', '-f', 'avfoundation', '-i', ':0', '-t', '3', '-y', str(temp_file)]
        else:
            cmd = ['ffmpeg', '-f', 'pulse', '-i', 'default', '-t', '3', '-y', str(temp_file)]
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=15)
            
            if result.returncode == 0 and temp_file.exists():
                file_size = temp_file.stat().st_size
                print(f"✅ Recording successful! File size: {file_size} bytes")
                temp_file.unlink()
                return True
            else:
                print(f"❌ Recording failed: {result.stderr}")
                return False
                
        except Exception as e:
            print(f"❌ Recording exception: {e}")
            return False

def main():
    print("🔧 FFmpeg Audio Device Diagnostic Tool")
    print("=" * 50)
    
    # Check FFmpeg
    if not check_ffmpeg_availability():
        print("\n💡 Please install FFmpeg:")
        print("   Windows: Download from https://ffmpeg.org/download.html")
        print("   macOS: brew install ffmpeg")
        print("   Linux: sudo apt install ffmpeg")
        return
    
    # List devices
    list_audio_devices()
    
    # Test recording
    success = test_recording()
    
    print("\n" + "=" * 50)
    print("📊 DIAGNOSTIC SUMMARY")
    print("=" * 50)
    
    if success:
        print("✅ FFmpeg can record audio from your microphone!")
        print("💡 The EduTrack recording should work now.")
    else:
        print("❌ FFmpeg cannot access your microphone.")
        print("💡 Possible solutions:")
        print("   1. Check microphone permissions in Windows Settings")
        print("   2. Try a different microphone device")
        print("   3. Check if other apps can access your microphone")
        print("   4. Restart your computer and try again")

if __name__ == "__main__":
    main()
