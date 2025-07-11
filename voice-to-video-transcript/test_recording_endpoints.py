#!/usr/bin/env python3
"""
Recording Test Script
Quick test to check if start/stop recording endpoints are working.
"""

import requests
import time
import json
import sys

API_BASE = "http://localhost:8000"

def test_server_connection():
    """Test if the API server is responding"""
    print("🔌 Testing server connection...")
    try:
        response = requests.get(f"{API_BASE}/recording/status", timeout=5)
        if response.status_code == 200:
            print("✅ Server is responding")
            return True
        else:
            print(f"❌ Server responded with status {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Cannot connect to server: {e}")
        print("💡 Make sure to start the server with: uvicorn api:app --reload")
        return False

def check_recording_status():
    """Check current recording status"""
    try:
        response = requests.get(f"{API_BASE}/recording/status")
        data = response.json()
        print(f"📊 Recording Status:")
        print(f"   Is Recording: {data.get('is_recording', 'Unknown')}")
        print(f"   Session ID: {data.get('session_id', 'None')}")
        print(f"   Recording Method: {data.get('recording_method', 'Unknown')}")
        print(f"   PyAudio Available: {data.get('pyaudio_available', 'Unknown')}")
        return data
    except Exception as e:
        print(f"❌ Error checking status: {e}")
        return None

def start_recording():
    """Start a recording session"""
    print("\n🎙️ Starting recording...")
    try:
        response = requests.post(
            f"{API_BASE}/recording/start",
            headers={"Content-Type": "application/json"},
            json={}
        )
        
        if response.status_code == 200:
            data = response.json()
            if data.get("status") == "success":
                print(f"✅ Recording started successfully!")
                print(f"   Session ID: {data.get('session_id')}")
                return data.get('session_id')
            else:
                print(f"❌ Failed to start recording: {data.get('message')}")
                return None
        else:
            print(f"❌ Server error: {response.status_code} - {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ Error starting recording: {e}")
        return None

def stop_recording():
    """Stop the recording session"""
    print("\n⏹️ Stopping recording...")
    try:
        response = requests.post(
            f"{API_BASE}/recording/stop",
            headers={"Content-Type": "application/json"},
            json={
                "process_immediately": True,
                "topic_hint": "Test recording"
            }
        )
        
        if response.status_code == 200:
            data = response.json()
            if data.get("status") == "success":
                print(f"✅ Recording stopped successfully!")
                print(f"   Message: {data.get('message')}")
                print(f"   File path: {data.get('file_path', 'Not provided')}")
                return data
            else:
                print(f"❌ Failed to stop recording: {data.get('message')}")
                return None
        else:
            print(f"❌ Server error: {response.status_code} - {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ Error stopping recording: {e}")
        return None

def check_sessions():
    """Check all sessions"""
    print("\n📋 Checking sessions...")
    try:
        response = requests.get(f"{API_BASE}/sessions")
        if response.status_code == 200:
            data = response.json()
            sessions = data.get('sessions', [])
            print(f"   Total sessions: {data.get('total_count', 0)}")
            
            if sessions:
                for i, session in enumerate(sessions[-3:], 1):  # Show last 3 sessions
                    print(f"   {i}. ID: {session.get('session_id', 'Unknown')[:8]}...")
                    print(f"      Status: {session.get('status', 'Unknown')}")
                    print(f"      Title: {session.get('title', 'N/A')}")
            else:
                print("   No sessions found")
            return sessions
        else:
            print(f"❌ Error: {response.status_code}")
            return []
    except Exception as e:
        print(f"❌ Error checking sessions: {e}")
        return []

def main():
    print("🎙️ EduTrack Recording Test Script")
    print("=" * 50)
    
    # Test server connection
    if not test_server_connection():
        sys.exit(1)
    
    # Check initial status
    print("\n📊 Initial Status Check:")
    initial_status = check_recording_status()
    if not initial_status:
        sys.exit(1)
    
    # Check if already recording
    if initial_status.get('is_recording', False):
        print("\n⚠️ Already recording! Stopping first...")
        stop_recording()
        time.sleep(1)
    
    print("\n" + "="*50)
    print("🧪 TESTING START/STOP RECORDING")
    print("="*50)
    
    # Test 1: Start recording
    session_id = start_recording()
    if not session_id:
        print("\n❌ Cannot proceed - recording start failed")
        sys.exit(1)
    
    # Verify recording is active
    time.sleep(1)
    print("\n📊 Verifying recording is active...")
    status = check_recording_status()
    if status and status.get('is_recording'):
        print("✅ Confirmed: Recording is active")
    else:
        print("⚠️ Warning: Recording may not be active")
    
    # Wait for user input
    print("\n🎤 Recording is now active!")
    print("💬 Speak into your microphone...")
    
    try:
        input("Press ENTER when you're done speaking (or wait 10 seconds)...")
    except KeyboardInterrupt:
        print("\nTest interrupted by user")
    
    # Test 2: Stop recording
    result = stop_recording()
    if not result:
        print("\n❌ Recording stop failed")
        sys.exit(1)
    
    # Verify recording stopped
    time.sleep(1)
    print("\n📊 Verifying recording stopped...")
    status = check_recording_status()
    if status and not status.get('is_recording'):
        print("✅ Confirmed: Recording stopped")
    else:
        print("⚠️ Warning: Recording may still be active")
    
    # Check sessions
    sessions = check_sessions()
    
    print("\n" + "="*50)
    print("🎯 TEST RESULTS SUMMARY")
    print("="*50)
    
    if session_id and result:
        print("✅ START/STOP RECORDING: WORKING")
        print(f"✅ Session created: {session_id[:8]}...")
        print(f"✅ File generated: {result.get('file_path', 'Unknown')}")
        
        if sessions:
            latest_session = sessions[-1]
            status = latest_session.get('status', 'unknown')
            print(f"📋 Latest session status: {status}")
            
            if status == "processing":
                print("🔄 Tip: Check sessions again in a few minutes to see completed results")
                print("   Use: curl http://localhost:8000/sessions")
            elif status == "completed":
                print("🎉 Processing completed! Check the output directory.")
    else:
        print("❌ START/STOP RECORDING: FAILED")
        print("💡 Check the server logs for error details")
    
    print(f"\n💡 Next steps:")
    print(f"   - Open test_recording.html for a web interface")
    print(f"   - Check output/ directory for generated files")
    print(f"   - Monitor sessions: curl {API_BASE}/sessions")

if __name__ == "__main__":
    main()
