"""
Start the API server without auto-reload to prevent Manim interruption
"""
import uvicorn
import os
import sys

# Ensure we're in the right directory
os.chdir(os.path.dirname(os.path.abspath(__file__)))

if __name__ == "__main__":
    print("🚀 Starting Voice to Educational Video API...")
    print(f"📁 Working directory: {os.getcwd()}")
    print("🔧 Auto-reload DISABLED to prevent Manim interruption")
    
    # Start the server WITHOUT reload
    uvicorn.run(
        "api:app",
        host="0.0.0.0",
        port=8000,
        reload=False,  # DISABLED to prevent KeyboardInterrupt during Manim rendering
        access_log=True,
        log_level="info"
    )
