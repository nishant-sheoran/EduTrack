#!/usr/bin/env python3
"""
Session Inspector Tool
Use this to check and debug session state in the EduTrack system.
"""

import requests
import json
import os
import sys
from pathlib import Path
import argparse

API_BASE = "http://localhost:8000"

def check_api_server():
    """Check if the API server is running"""
    try:
        response = requests.get(f"{API_BASE}/recording/status", timeout=5)
        return response.status_code == 200
    except requests.exceptions.RequestException:
        return False

def get_all_sessions():
    """Get all active sessions"""
    try:
        response = requests.get(f"{API_BASE}/sessions")
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error: {response.status_code} - {response.text}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Connection error: {e}")
        return None

def get_session_details(session_id):
    """Get details for a specific session"""
    try:
        response = requests.get(f"{API_BASE}/session/{session_id}")
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error: {response.status_code} - {response.text}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Connection error: {e}")
        return None

def check_output_files():
    """Check what files exist in the output directory"""
    output_dir = Path("output")
    if not output_dir.exists():
        return []
    
    files = []
    for file_path in output_dir.iterdir():
        if file_path.is_file():
            stat = file_path.stat()
            files.append({
                "name": file_path.name,
                "size_mb": stat.st_size / (1024 * 1024),
                "modified": stat.st_mtime
            })
    
    return sorted(files, key=lambda x: x["modified"], reverse=True)

def check_recording_status():
    """Check current recording status"""
    try:
        response = requests.get(f"{API_BASE}/recording/status")
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error: {response.status_code} - {response.text}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Connection error: {e}")
        return None

def main():
    parser = argparse.ArgumentParser(description="EduTrack Session Inspector")
    parser.add_argument("--session-id", "-s", help="Check specific session ID")
    parser.add_argument("--files-only", "-f", action="store_true", help="Only check output files")
    parser.add_argument("--watch", "-w", action="store_true", help="Watch sessions continuously")
    
    args = parser.parse_args()
    
    print("🔍 EduTrack Session Inspector")
    print("=" * 50)
    
    if args.files_only:
        print("\n📁 Output Files:")
        files = check_output_files()
        if files:
            for file_info in files[:10]:  # Show last 10 files
                print(f"  📄 {file_info['name']} ({file_info['size_mb']:.2f} MB)")
        else:
            print("  No files found in output directory")
        return
    
    # Check if API server is running
    if not check_api_server():
        print("❌ API server is not running!")
        print("💡 Start it with: uvicorn api:app --reload")
        return
    
    print("✅ API server is running")
    
    # Check recording status
    recording_status = check_recording_status()
    if recording_status:
        print(f"\n🎙️ Recording Status:")
        print(f"  Is Recording: {recording_status.get('is_recording', 'Unknown')}")
        print(f"  Session ID: {recording_status.get('session_id', 'None')}")
        print(f"  Method: {recording_status.get('recording_method', 'Unknown')}")
        print(f"  PyAudio Available: {recording_status.get('pyaudio_available', 'Unknown')}")
    
    if args.session_id:
        # Check specific session
        print(f"\n📋 Session Details: {args.session_id}")
        session = get_session_details(args.session_id)
        if session:
            print(json.dumps(session, indent=2))
        else:
            print("❌ Session not found or error occurred")
    else:
        # Check all sessions
        print(f"\n📊 All Sessions:")
        sessions_data = get_all_sessions()
        if sessions_data:
            sessions = sessions_data.get('sessions', [])
            total_count = sessions_data.get('total_count', 0)
            
            print(f"  Total Sessions: {total_count}")
            
            if sessions:
                for i, session in enumerate(sessions, 1):
                    print(f"\n  {i}. Session ID: {session.get('session_id', 'Unknown')}")
                    print(f"     Status: {session.get('status', 'Unknown')}")
                    print(f"     Title: {session.get('title', 'N/A')}")
                    print(f"     Created: {session.get('created_at', 'Unknown')}")
                    print(f"     Video: {'✅' if session.get('video_path') else '❌'}")
                    print(f"     PDF: {'✅' if session.get('pdf_path') else '❌'}")
            else:
                print("  No active sessions found")
                print("  💡 This is expected if:")
                print("     - No recordings have been made")
                print("     - Server was recently restarted (sessions are in-memory)")
        else:
            print("❌ Could not retrieve sessions")
    
    # Check output files
    print(f"\n📁 Recent Output Files:")
    files = check_output_files()
    if files:
        for file_info in files[:5]:  # Show last 5 files
            print(f"  📄 {file_info['name']} ({file_info['size_mb']:.2f} MB)")
        if len(files) > 5:
            print(f"  ... and {len(files) - 5} more files")
    else:
        print("  No files found in output directory")
    
    print(f"\n💡 Tips:")
    print(f"  - Use --session-id <ID> to check a specific session")
    print(f"  - Use --files-only to only see output files") 
    print(f"  - Sessions are stored in memory and reset on server restart")
    print(f"  - Check test_recording.html for a web interface")

if __name__ == "__main__":
    main()
