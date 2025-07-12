@echo off
echo ========================================
echo    EduTrack - Automated Setup Script
echo    Competition-Ready Installation
echo ========================================
echo.

:: Check if running as administrator
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo [ERROR] Please run as Administrator for complete setup
    echo Right-click and select "Run as Administrator"
    pause
    exit /b 1
)

:: Set colors for better visibility
color 0A

:: Create logs directory
if not exist "logs" mkdir logs
set LOGFILE=logs\setup_%date:~-4,4%%date:~-10,2%%date:~-7,2%_%time:~0,2%%time:~3,2%.log

echo [INFO] Starting EduTrack setup at %date% %time% >> %LOGFILE%
echo [INFO] Log file: %LOGFILE%

:: Check system requirements
echo [STEP 1/7] Checking system requirements...
echo [INFO] Checking system requirements... >> %LOGFILE%

:: Check Python
python --version >nul 2>&1
if %errorLevel% neq 0 (
    echo [ERROR] Python not found! Please install Python 3.10+ from https://python.org
    echo [ERROR] Python not found >> %LOGFILE%
    goto :error_exit
)

:: Check Node.js
node --version >nul 2>&1
if %errorLevel% neq 0 (
    echo [ERROR] Node.js not found! Please install Node.js 18+ from https://nodejs.org
    echo [ERROR] Node.js not found >> %LOGFILE%
    goto :error_exit
)

:: Check FFmpeg
ffmpeg -version >nul 2>&1
if %errorLevel% neq 0 (
    echo [WARNING] FFmpeg not found! Voice-to-Video features may not work
    echo [WARNING] Install FFmpeg from https://ffmpeg.org/download.html
    echo [WARNING] FFmpeg not found >> %LOGFILE%
    set FFMPEG_MISSING=true
) else (
    echo [OK] FFmpeg found
    set FFMPEG_MISSING=false
)

echo [OK] System requirements check complete
echo.

:: Get OpenAI API Key
echo [STEP 2/7] OpenAI API Key Configuration...
echo [INFO] Configuring OpenAI API Key... >> %LOGFILE%

set /p OPENAI_KEY="Enter your OpenAI API Key (press Enter to skip): "
if "%OPENAI_KEY%"=="" (
    echo [WARNING] No OpenAI API Key provided. Voice-to-Video features will be limited.
    echo [WARNING] No OpenAI API Key provided >> %LOGFILE%
) else (
    echo [OK] OpenAI API Key configured
)

echo.

:: Setup Engagement Monitor
echo [STEP 3/7] Setting up Classroom Engagement Monitor...
echo [INFO] Setting up Engagement Monitor... >> %LOGFILE%

cd clr_engage_montr
if %errorLevel% neq 0 (
    echo [ERROR] clr_engage_montr directory not found!
    echo [ERROR] clr_engage_montr directory not found >> %LOGFILE%
    goto :error_exit
)

:: Create virtual environment
echo [INFO] Creating Python virtual environment...
python -m venv venv
if %errorLevel% neq 0 (
    echo [ERROR] Failed to create virtual environment for Engagement Monitor
    echo [ERROR] Failed to create venv for Engagement Monitor >> %LOGFILE%
    goto :error_exit
)

:: Activate virtual environment and install dependencies
echo [INFO] Installing Engagement Monitor dependencies...
call venv\Scripts\activate.bat
pip install --upgrade pip >> %LOGFILE% 2>&1
pip install -r requirements.txt >> %LOGFILE% 2>&1
if %errorLevel% neq 0 (
    echo [ERROR] Failed to install Engagement Monitor dependencies
    echo [ERROR] Failed to install Engagement Monitor dependencies >> %LOGFILE%
    goto :error_exit
)

echo [OK] Engagement Monitor setup complete
cd ..

echo.

:: Setup Teacher Dashboard
echo [STEP 4/7] Setting up Teacher Dashboard...
echo [INFO] Setting up Teacher Dashboard... >> %LOGFILE%

cd teacher-dashboard
if %errorLevel% neq 0 (
    echo [ERROR] teacher-dashboard directory not found!
    echo [ERROR] teacher-dashboard directory not found >> %LOGFILE%
    goto :error_exit
)

:: Install Node.js dependencies
echo [INFO] Installing Dashboard dependencies...
call npm install >> %LOGFILE% 2>&1
if %errorLevel% neq 0 (
    echo [ERROR] Failed to install Dashboard dependencies
    echo [ERROR] Failed to install Dashboard dependencies >> %LOGFILE%
    goto :error_exit
)

:: Build the dashboard
echo [INFO] Building Dashboard...
call npm run build >> %LOGFILE% 2>&1
if %errorLevel% neq 0 (
    echo [WARNING] Dashboard build failed, will use development mode
    echo [WARNING] Dashboard build failed >> %LOGFILE%
)

echo [OK] Teacher Dashboard setup complete
cd ..

echo.

:: Setup Voice-to-Video System
echo [STEP 5/7] Setting up Voice-to-Video System...
echo [INFO] Setting up Voice-to-Video System... >> %LOGFILE%

cd voice-to-video-transcript
if %errorLevel% neq 0 (
    echo [ERROR] voice-to-video-transcript directory not found!
    echo [ERROR] voice-to-video-transcript directory not found >> %LOGFILE%
    goto :error_exit
)

:: Create virtual environment
echo [INFO] Creating Python virtual environment...
python -m venv venv
if %errorLevel% neq 0 (
    echo [ERROR] Failed to create virtual environment for Voice-to-Video
    echo [ERROR] Failed to create venv for Voice-to-Video >> %LOGFILE%
    goto :error_exit
)

:: Activate virtual environment and install dependencies
echo [INFO] Installing Voice-to-Video dependencies...
call venv\Scripts\activate.bat
pip install --upgrade pip >> %LOGFILE% 2>&1
pip install -r requirements.txt >> %LOGFILE% 2>&1
if %errorLevel% neq 0 (
    echo [ERROR] Failed to install Voice-to-Video dependencies
    echo [ERROR] Failed to install Voice-to-Video dependencies >> %LOGFILE%
    goto :error_exit
)

:: Configure OpenAI API Key
if not "%OPENAI_KEY%"=="" (
    echo OPENAI_API_KEY=%OPENAI_KEY% > .env
    echo OPENAI_MODEL=gpt-4 >> .env
    echo WHISPER_MODEL=whisper-1 >> .env
    echo [OK] OpenAI API Key configured for Voice-to-Video
)

echo [OK] Voice-to-Video setup complete
cd ..

echo.

:: Create startup scripts
echo [STEP 6/7] Creating startup scripts...
echo [INFO] Creating startup scripts... >> %LOGFILE%

:: Create start-all.bat
echo @echo off > start-all.bat
echo echo Starting EduTrack Complete System... >> start-all.bat
echo echo. >> start-all.bat
echo echo [1/3] Starting Engagement Monitor on port 8001... >> start-all.bat
echo start "Engagement Monitor" cmd /k "cd clr_engage_montr && venv\Scripts\activate.bat && python -m uvicorn main:app --host 0.0.0.0 --port 8001 --reload" >> start-all.bat
echo timeout /t 5 /nobreak ^> nul >> start-all.bat
echo echo [2/3] Starting Teacher Dashboard on port 3000... >> start-all.bat
echo start "Teacher Dashboard" cmd /k "cd teacher-dashboard && npm run dev" >> start-all.bat
echo timeout /t 5 /nobreak ^> nul >> start-all.bat
echo echo [3/3] Starting Voice-to-Video System on port 8000... >> start-all.bat
echo start "Voice-to-Video" cmd /k "cd voice-to-video-transcript && venv\Scripts\activate.bat && python -m uvicorn api:app --host 0.0.0.0 --port 8000 --reload" >> start-all.bat
echo timeout /t 3 /nobreak ^> nul >> start-all.bat
echo echo. >> start-all.bat
echo echo ========================================== >> start-all.bat
echo echo    EduTrack System Started Successfully! >> start-all.bat
echo echo ========================================== >> start-all.bat
echo echo. >> start-all.bat
echo echo Access the system at: >> start-all.bat
echo echo   Teacher Dashboard: http://localhost:3000 >> start-all.bat
echo echo   Engagement Monitor: http://localhost:8001 >> start-all.bat
echo echo   Voice-to-Video API: http://localhost:8000 >> start-all.bat
echo echo. >> start-all.bat
echo echo Press any key to open the dashboard... >> start-all.bat
echo pause ^> nul >> start-all.bat
echo start http://localhost:3000 >> start-all.bat

:: Create quick-demo.bat
echo @echo off > quick-demo.bat
echo echo ========================================== >> quick-demo.bat
echo echo    EduTrack - Quick Demo Access >> quick-demo.bat
echo echo ========================================== >> quick-demo.bat
echo echo. >> quick-demo.bat
echo echo Opening all EduTrack interfaces... >> quick-demo.bat
echo start http://localhost:3000 >> quick-demo.bat
echo timeout /t 2 /nobreak ^> nul >> quick-demo.bat
echo start http://localhost:8001/docs >> quick-demo.bat
echo timeout /t 2 /nobreak ^> nul >> quick-demo.bat
echo start http://localhost:8000/docs >> quick-demo.bat
echo echo. >> quick-demo.bat
echo echo All interfaces opened in your browser! >> quick-demo.bat
echo pause >> quick-demo.bat

echo [OK] Startup scripts created
echo.

:: System validation
echo [STEP 7/7] System validation...
echo [INFO] Performing system validation... >> %LOGFILE%

:: Check Python packages
echo [INFO] Validating Python packages...
cd clr_engage_montr
call venv\Scripts\activate.bat
python -c "import cv2, fastapi, numpy; print('Engagement Monitor packages OK')" >> %LOGFILE% 2>&1
if %errorLevel% neq 0 (
    echo [WARNING] Some Engagement Monitor packages may have issues
    echo [WARNING] Engagement Monitor package validation failed >> %LOGFILE%
)
cd ..

cd voice-to-video-transcript
call venv\Scripts\activate.bat
python -c "import openai, fastapi, streamlit; print('Voice-to-Video packages OK')" >> %LOGFILE% 2>&1
if %errorLevel% neq 0 (
    echo [WARNING] Some Voice-to-Video packages may have issues
    echo [WARNING] Voice-to-Video package validation failed >> %LOGFILE%
)
cd ..

echo [OK] System validation complete
echo.

:: Success message
echo ==========================================
echo    EduTrack Setup Complete! 
echo ==========================================
echo.
echo [SUCCESS] All components installed successfully!
echo.
echo Next steps:
echo 1. Run "start-all.bat" to start all services
echo 2. Run "quick-demo.bat" to open all interfaces
echo 3. Access Teacher Dashboard at: http://localhost:3000
echo.
echo Troubleshooting:
echo - Check logs in: %LOGFILE%
echo - View README.md for detailed instructions
echo - Check individual component documentation
echo.
if "%FFMPEG_MISSING%"=="true" (
    echo [NOTE] FFmpeg is missing - Voice-to-Video features limited
    echo Install from: https://ffmpeg.org/download.html
    echo.
)
if "%OPENAI_KEY%"=="" (
    echo [NOTE] OpenAI API Key not configured - Voice-to-Video limited
    echo Configure in: voice-to-video-transcript\.env
    echo.
)
echo [INFO] Setup completed successfully at %date% %time% >> %LOGFILE%
echo Press any key to exit...
pause >nul
exit /b 0

:error_exit
echo.
echo ==========================================
echo    Setup Failed! 
echo ==========================================
echo.
echo [ERROR] EduTrack setup encountered errors.
echo.
echo Troubleshooting:
echo 1. Check the log file: %LOGFILE%
echo 2. Ensure you have administrator privileges
echo 3. Verify Python 3.10+ and Node.js 18+ are installed
echo 4. Check internet connection for downloads
echo 5. Refer to README.md for manual setup
echo.
echo [ERROR] Setup failed at %date% %time% >> %LOGFILE%
echo Press any key to exit...
pause >nul
exit /b 1 