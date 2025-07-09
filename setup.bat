@echo off
echo ====================================================
echo Voice to Educational Video Generator - Windows Setup
echo ====================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://python.org
    pause
    exit /b 1
)

echo Python found:
python --version

REM Check if pip is available
pip --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: pip is not available
    echo Please ensure pip is installed with Python
    pause
    exit /b 1
)

echo.
echo Installing Python dependencies...
echo ================================

REM Upgrade pip first
python -m pip install --upgrade pip

REM Install requirements
if exist requirements.txt (
    echo Installing from requirements.txt...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo WARNING: Some packages may have failed to install
        echo This is normal - the app will use fallback options
    )
) else (
    echo requirements.txt not found, installing core packages...
    pip install streamlit openai gTTS pydub moviepy python-dotenv requests numpy matplotlib
)

echo.
echo Setting up directories...
echo ========================
if not exist "output" mkdir output
if not exist "temp" mkdir temp
echo Directories created.

echo.
echo Setting up environment...
echo ========================
if not exist ".env" (
    if exist ".env.example" (
        copy ".env.example" ".env"
        echo Created .env file from example
    ) else (
        echo OPENAI_API_KEY=your_openai_api_key_here > .env
        echo Created basic .env file
    )
    echo.
    echo IMPORTANT: Please edit .env file and add your OpenAI API key!
) else (
    echo .env file already exists
)

echo.
echo Checking FFmpeg...
echo =================
ffmpeg -version >nul 2>&1
if errorlevel 1 (
    echo WARNING: FFmpeg not found in PATH
    echo Please download FFmpeg from https://ffmpeg.org/download.html
    echo and add it to your system PATH for full functionality
) else (
    echo FFmpeg found - OK
)

echo.
echo Testing installation...
echo ======================
python -c "import streamlit, openai; print('Core modules OK')" 2>nul
if errorlevel 1 (
    echo WARNING: Some core modules failed to import
    echo You may need to install additional dependencies
) else (
    echo Core modules imported successfully
)

echo.
echo ====================================================
echo Setup Complete!
echo ====================================================
echo.
echo Next steps:
echo 1. Edit .env file and add your OpenAI API key
echo 2. Run: streamlit run app.py
echo 3. Upload an audio file and generate your first video!
echo.
echo For command line usage:
echo   python cli.py process audio_file.wav --topic "Your Topic"
echo.
echo For testing:
echo   python example_test.py
echo.
pause
