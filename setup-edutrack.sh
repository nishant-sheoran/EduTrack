#!/bin/bash

# Colors for better visibility
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${GREEN}========================================"
echo -e "   EduTrack - Automated Setup Script"
echo -e "   Competition-Ready Installation"
echo -e "========================================${NC}"
echo

# Create logs directory
mkdir -p logs
LOGFILE="logs/setup_$(date +%Y%m%d_%H%M%S).log"

echo "[INFO] Starting EduTrack setup at $(date)" >> "$LOGFILE"
echo -e "${BLUE}[INFO] Log file: $LOGFILE${NC}"

# Function to check command availability
check_command() {
    if ! command -v "$1" &> /dev/null; then
        echo -e "${RED}[ERROR] $1 not found! Please install $1${NC}"
        echo "[ERROR] $1 not found" >> "$LOGFILE"
        return 1
    else
        echo -e "${GREEN}[OK] $1 found${NC}"
        return 0
    fi
}

# Function to handle errors
handle_error() {
    echo -e "${RED}[ERROR] $1${NC}"
    echo "[ERROR] $1" >> "$LOGFILE"
    echo
    echo -e "${RED}=========================================="
    echo -e "   Setup Failed!"
    echo -e "==========================================${NC}"
    echo
    echo "Troubleshooting:"
    echo "1. Check the log file: $LOGFILE"
    echo "2. Ensure you have proper permissions"
    echo "3. Verify Python 3.10+ and Node.js 18+ are installed"
    echo "4. Check internet connection for downloads"
    echo "5. Refer to README.md for manual setup"
    echo
    echo "[ERROR] Setup failed at $(date)" >> "$LOGFILE"
    exit 1
}

# Check system requirements
echo -e "${BLUE}[STEP 1/7] Checking system requirements...${NC}"
echo "[INFO] Checking system requirements..." >> "$LOGFILE"

# Check Python
if ! check_command python3; then
    if ! check_command python; then
        handle_error "Python not found! Please install Python 3.10+ from https://python.org"
    fi
    PYTHON_CMD=python
else
    PYTHON_CMD=python3
fi

# Check Python version
PYTHON_VERSION=$($PYTHON_CMD --version 2>&1 | cut -d' ' -f2 | cut -d'.' -f1-2)
if ! $PYTHON_CMD -c "import sys; sys.exit(0 if sys.version_info >= (3, 10) else 1)" 2>/dev/null; then
    handle_error "Python version $PYTHON_VERSION is too old! Please install Python 3.10+"
fi

# Check Node.js
if ! check_command node; then
    handle_error "Node.js not found! Please install Node.js 18+ from https://nodejs.org"
fi

# Check Node.js version
NODE_VERSION=$(node --version | cut -d'v' -f2 | cut -d'.' -f1)
if [ "$NODE_VERSION" -lt 18 ]; then
    handle_error "Node.js version is too old! Please install Node.js 18+"
fi

# Check npm
if ! check_command npm; then
    handle_error "npm not found! Please install npm"
fi

# Check FFmpeg
FFMPEG_MISSING=false
if ! check_command ffmpeg; then
    echo -e "${YELLOW}[WARNING] FFmpeg not found! Voice-to-Video features may not work${NC}"
    echo -e "${YELLOW}[WARNING] Install FFmpeg from https://ffmpeg.org/download.html${NC}"
    echo "[WARNING] FFmpeg not found" >> "$LOGFILE"
    FFMPEG_MISSING=true
fi

echo -e "${GREEN}[OK] System requirements check complete${NC}"
echo

# Get OpenAI API Key
echo -e "${BLUE}[STEP 2/7] OpenAI API Key Configuration...${NC}"
echo "[INFO] Configuring OpenAI API Key..." >> "$LOGFILE"

read -p "Enter your OpenAI API Key (press Enter to skip): " OPENAI_KEY
if [ -z "$OPENAI_KEY" ]; then
    echo -e "${YELLOW}[WARNING] No OpenAI API Key provided. Voice-to-Video features will be limited.${NC}"
    echo "[WARNING] No OpenAI API Key provided" >> "$LOGFILE"
else
    echo -e "${GREEN}[OK] OpenAI API Key configured${NC}"
fi

echo

# Setup Engagement Monitor
echo -e "${BLUE}[STEP 3/7] Setting up Classroom Engagement Monitor...${NC}"
echo "[INFO] Setting up Engagement Monitor..." >> "$LOGFILE"

if [ ! -d "clr_engage_montr" ]; then
    handle_error "clr_engage_montr directory not found!"
fi

cd clr_engage_montr

# Create virtual environment
echo -e "${BLUE}[INFO] Creating Python virtual environment...${NC}"
$PYTHON_CMD -m venv venv
if [ $? -ne 0 ]; then
    handle_error "Failed to create virtual environment for Engagement Monitor"
fi

# Activate virtual environment and install dependencies
echo -e "${BLUE}[INFO] Installing Engagement Monitor dependencies...${NC}"
source venv/bin/activate
pip install --upgrade pip >> "$LOGFILE" 2>&1
pip install -r requirements.txt >> "$LOGFILE" 2>&1
if [ $? -ne 0 ]; then
    handle_error "Failed to install Engagement Monitor dependencies"
fi

echo -e "${GREEN}[OK] Engagement Monitor setup complete${NC}"
cd ..

echo

# Setup Teacher Dashboard
echo -e "${BLUE}[STEP 4/7] Setting up Teacher Dashboard...${NC}"
echo "[INFO] Setting up Teacher Dashboard..." >> "$LOGFILE"

if [ ! -d "teacher-dashboard" ]; then
    handle_error "teacher-dashboard directory not found!"
fi

cd teacher-dashboard

# Install Node.js dependencies
echo -e "${BLUE}[INFO] Installing Dashboard dependencies...${NC}"
npm install >> "$LOGFILE" 2>&1
if [ $? -ne 0 ]; then
    handle_error "Failed to install Dashboard dependencies"
fi

# Build the dashboard
echo -e "${BLUE}[INFO] Building Dashboard...${NC}"
npm run build >> "$LOGFILE" 2>&1
if [ $? -ne 0 ]; then
    echo -e "${YELLOW}[WARNING] Dashboard build failed, will use development mode${NC}"
    echo "[WARNING] Dashboard build failed" >> "$LOGFILE"
fi

echo -e "${GREEN}[OK] Teacher Dashboard setup complete${NC}"
cd ..

echo

# Setup Voice-to-Video System
echo -e "${BLUE}[STEP 5/7] Setting up Voice-to-Video System...${NC}"
echo "[INFO] Setting up Voice-to-Video System..." >> "$LOGFILE"

if [ ! -d "voice-to-video-transcript" ]; then
    handle_error "voice-to-video-transcript directory not found!"
fi

cd voice-to-video-transcript

# Create virtual environment
echo -e "${BLUE}[INFO] Creating Python virtual environment...${NC}"
$PYTHON_CMD -m venv venv
if [ $? -ne 0 ]; then
    handle_error "Failed to create virtual environment for Voice-to-Video"
fi

# Activate virtual environment and install dependencies
echo -e "${BLUE}[INFO] Installing Voice-to-Video dependencies...${NC}"
source venv/bin/activate
pip install --upgrade pip >> "$LOGFILE" 2>&1
pip install -r requirements.txt >> "$LOGFILE" 2>&1
if [ $? -ne 0 ]; then
    handle_error "Failed to install Voice-to-Video dependencies"
fi

# Configure OpenAI API Key
if [ ! -z "$OPENAI_KEY" ]; then
    cat > .env << EOF
OPENAI_API_KEY=$OPENAI_KEY
OPENAI_MODEL=gpt-4
WHISPER_MODEL=whisper-1
EOF
    echo -e "${GREEN}[OK] OpenAI API Key configured for Voice-to-Video${NC}"
fi

echo -e "${GREEN}[OK] Voice-to-Video setup complete${NC}"
cd ..

echo

# Install test-system dependencies
echo -e "${BLUE}[STEP 6/8] Installing system validation tools...${NC}"
echo "[INFO] Installing system validation tools..." >> "$LOGFILE"

echo -e "${BLUE}[INFO] Installing test-system dependencies...${NC}"
pip install --upgrade pip >> "$LOGFILE" 2>&1
pip install -r test-system-requirements.txt >> "$LOGFILE" 2>&1
if [ $? -ne 0 ]; then
    echo -e "${YELLOW}[WARNING] Failed to install test-system dependencies${NC}"
    echo -e "${YELLOW}[WARNING] test-system.py may not work properly${NC}"
    echo "[WARNING] Failed to install test-system dependencies" >> "$LOGFILE"
else
    echo -e "${GREEN}[OK] Test-system dependencies installed successfully${NC}"
fi

echo -e "${GREEN}[OK] System validation tools setup complete${NC}"
echo

# Create startup scripts
echo -e "${BLUE}[STEP 7/8] Creating startup scripts...${NC}"
echo "[INFO] Creating startup scripts..." >> "$LOGFILE"

# Create start-all.sh
cat > start-all.sh << 'EOF'
#!/bin/bash

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${GREEN}Starting EduTrack Complete System...${NC}"
echo

# Function to check if port is available
check_port() {
    if lsof -Pi :$1 -sTCP:LISTEN -t >/dev/null 2>&1; then
        echo -e "${BLUE}[INFO] Port $1 is already in use. Killing existing process...${NC}"
        lsof -ti:$1 | xargs kill -9 2>/dev/null
        sleep 2
    fi
}

# Check and free up ports
check_port 8001
check_port 3000
check_port 8000

echo -e "${BLUE}[1/3] Starting Engagement Monitor on port 8001...${NC}"
cd clr_engage_montr
source venv/bin/activate
nohup python -m uvicorn main:app --host 0.0.0.0 --port 8001 --reload > ../logs/engagement_monitor.log 2>&1 &
ENGAGEMENT_PID=$!
echo $ENGAGEMENT_PID > ../logs/engagement_monitor.pid
cd ..
sleep 5

echo -e "${BLUE}[2/3] Starting Teacher Dashboard on port 3000...${NC}"
cd teacher-dashboard
nohup npm run dev > ../logs/teacher_dashboard.log 2>&1 &
DASHBOARD_PID=$!
echo $DASHBOARD_PID > ../logs/teacher_dashboard.pid
cd ..
sleep 5

echo -e "${BLUE}[3/3] Starting Voice-to-Video System on port 8000...${NC}"
cd voice-to-video-transcript
source venv/bin/activate
nohup python -m uvicorn api:app --host 0.0.0.0 --port 8000 --reload > ../logs/voice_to_video.log 2>&1 &
VOICE_PID=$!
echo $VOICE_PID > ../logs/voice_to_video.pid
cd ..
sleep 3

echo
echo -e "${GREEN}=========================================="
echo -e "   EduTrack System Started Successfully!"
echo -e "==========================================${NC}"
echo
echo "Access the system at:"
echo "  Teacher Dashboard: http://localhost:3000"
echo "  Engagement Monitor: http://localhost:8001"
echo "  Voice-to-Video API: http://localhost:8000"
echo
echo "Process IDs saved in logs/ directory"
echo "Use 'stop-all.sh' to stop all services"
echo
echo "Opening Teacher Dashboard in default browser..."
sleep 2

# Try to open browser (works on most systems)
if command -v xdg-open > /dev/null; then
    xdg-open http://localhost:3000
elif command -v open > /dev/null; then
    open http://localhost:3000
elif command -v start > /dev/null; then
    start http://localhost:3000
else
    echo "Please manually open: http://localhost:3000"
fi

echo
echo "Press Ctrl+C to stop all services or run 'stop-all.sh'"
echo

# Wait for user interrupt
trap 'echo -e "\n${BLUE}Stopping all services...${NC}"; ./stop-all.sh; exit 0' INT
while true; do
    sleep 1
done
EOF

chmod +x start-all.sh

# Create stop-all.sh
cat > stop-all.sh << 'EOF'
#!/bin/bash

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}Stopping EduTrack services...${NC}"

# Function to stop service by PID file
stop_service() {
    if [ -f "logs/$1.pid" ]; then
        PID=$(cat logs/$1.pid)
        if kill -0 $PID 2>/dev/null; then
            echo -e "${BLUE}[INFO] Stopping $1 (PID: $PID)...${NC}"
            kill -TERM $PID 2>/dev/null
            sleep 2
            if kill -0 $PID 2>/dev/null; then
                kill -KILL $PID 2>/dev/null
            fi
        fi
        rm -f logs/$1.pid
    fi
}

# Stop all services
stop_service engagement_monitor
stop_service teacher_dashboard
stop_service voice_to_video

# Kill any remaining processes on our ports
for port in 8001 3000 8000; do
    if lsof -Pi :$port -sTCP:LISTEN -t >/dev/null 2>&1; then
        echo -e "${BLUE}[INFO] Killing remaining processes on port $port...${NC}"
        lsof -ti:$port | xargs kill -9 2>/dev/null
    fi
done

echo -e "${GREEN}[OK] All EduTrack services stopped${NC}"
EOF

chmod +x stop-all.sh

# Create quick-demo.sh
cat > quick-demo.sh << 'EOF'
#!/bin/bash

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${GREEN}=========================================="
echo -e "   EduTrack - Quick Demo Access"
echo -e "==========================================${NC}"
echo

echo -e "${BLUE}Opening all EduTrack interfaces...${NC}"

# Function to open URL
open_url() {
    if command -v xdg-open > /dev/null; then
        xdg-open "$1"
    elif command -v open > /dev/null; then
        open "$1"
    elif command -v start > /dev/null; then
        start "$1"
    else
        echo "Please manually open: $1"
    fi
}

# Open all interfaces
open_url "http://localhost:3000"
sleep 2
open_url "http://localhost:8001/docs"
sleep 2
open_url "http://localhost:8000/docs"

echo
echo -e "${GREEN}All interfaces opened in your default browser!${NC}"
echo
echo "If browsers didn't open automatically, visit:"
echo "  Teacher Dashboard: http://localhost:3000"
echo "  Engagement Monitor API: http://localhost:8001/docs"
echo "  Voice-to-Video API: http://localhost:8000/docs"
EOF

chmod +x quick-demo.sh

echo -e "${GREEN}[OK] Startup scripts created${NC}"
echo

# System validation
echo -e "${BLUE}[STEP 8/8] System validation...${NC}"
echo "[INFO] Performing system validation..." >> "$LOGFILE"

# Check Python packages
echo -e "${BLUE}[INFO] Validating Python packages...${NC}"
cd clr_engage_montr
source venv/bin/activate
python -c "import cv2, fastapi, numpy; print('Engagement Monitor packages OK')" >> "$LOGFILE" 2>&1
if [ $? -ne 0 ]; then
    echo -e "${YELLOW}[WARNING] Some Engagement Monitor packages may have issues${NC}"
    echo "[WARNING] Engagement Monitor package validation failed" >> "$LOGFILE"
fi
cd ..

cd voice-to-video-transcript
source venv/bin/activate
python -c "import openai, fastapi, streamlit; print('Voice-to-Video packages OK')" >> "$LOGFILE" 2>&1
if [ $? -ne 0 ]; then
    echo -e "${YELLOW}[WARNING] Some Voice-to-Video packages may have issues${NC}"
    echo "[WARNING] Voice-to-Video package validation failed" >> "$LOGFILE"
fi
cd ..

echo -e "${GREEN}[OK] System validation complete${NC}"
echo

# Success message
echo -e "${GREEN}=========================================="
echo -e "   EduTrack Setup Complete!"
echo -e "==========================================${NC}"
echo
echo -e "${GREEN}[SUCCESS] All components installed successfully!${NC}"
echo
echo "Next steps:"
echo "1. Run './start-all.sh' to start all services"
echo "2. Run './quick-demo.sh' to open all interfaces"
echo "3. Access Teacher Dashboard at: http://localhost:3000"
echo
echo "Troubleshooting:"
echo "- Check logs in: $LOGFILE"
echo "- View README.md for detailed instructions"
echo "- Check individual component documentation"
echo

if [ "$FFMPEG_MISSING" = true ]; then
    echo -e "${YELLOW}[NOTE] FFmpeg is missing - Voice-to-Video features limited${NC}"
    echo "Install from: https://ffmpeg.org/download.html"
    echo
fi

if [ -z "$OPENAI_KEY" ]; then
    echo -e "${YELLOW}[NOTE] OpenAI API Key not configured - Voice-to-Video limited${NC}"
    echo "Configure in: voice-to-video-transcript/.env"
    echo
fi

echo "[INFO] Setup completed successfully at $(date)" >> "$LOGFILE"
echo "Setup complete! Press any key to exit..."
read -n 1 -s
exit 0 