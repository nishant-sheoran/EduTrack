# Python Compatibility Guide

## Python Version Support

This application has been updated to work with both Python 3.10/3.12 and Python 3.13+.

### Python 3.13+ Compatibility

Python 3.13 removed the internal `audioop`/`pyaudioop` module that many audio processing libraries depend on, including `pydub`. To address this, we've implemented the following solutions:

1. **Conditional Imports**: The application detects your Python version and uses appropriate modules.
2. **Python 3.13+ Compatible Transcriber**: A special version of the `AudioTranscriber` class that uses `ffmpeg` directly instead of `pydub`.

### Requirements

- For Python 3.13+:
  - `ffmpeg` must be installed and available in your system PATH
  - All other dependencies in `requirements.txt`
  
- For Python 3.10/3.12:
  - All dependencies in `requirements.txt`

## Running the API Server

Run the FastAPI server using uvicorn:

```bash
uvicorn api:app --reload
```

The server will be available at http://localhost:8000

## API Endpoints

- **POST /upload-audio**: Simple endpoint to test audio file uploads
- **POST /generate**: Process audio through the full pipeline (transcription, script, narration, animation, video, PDF)
- **GET /download/video/{filename}**: Download generated video files
- **GET /download/pdf/{filename}**: Download generated PDF files

## Full Pipeline Support

The application will automatically detect your Python version and use the appropriate implementation:

- **Python 3.10/3.12**: Uses the standard pipeline with full functionality
- **Python 3.13+**: Uses ffmpeg-based audio processing instead of pydub to avoid dependency on the removed pyaudioop module

## Troubleshooting

If you encounter issues on Python 3.13+:

1. Ensure `ffmpeg` is installed and in your system PATH
2. Check that all required packages are installed: `pip install -r requirements.txt`
3. For audio processing issues, you may need to downgrade to Python 3.12 until all dependencies are updated

For more information on the Python 3.13 changes that affected audio processing libraries, see [PEP 594](https://peps.python.org/pep-0594/) which deprecated and later removed several standard library modules.
