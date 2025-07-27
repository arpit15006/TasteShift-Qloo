#!/bin/bash

# TasteShift Server Startup Script
# This script sets up the environment and starts the TasteShift server

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_header() {
    echo -e "${PURPLE}$1${NC}"
}

# Header
clear
echo -e "${CYAN}"
echo "╔══════════════════════════════════════════════════════════════╗"
echo "║                    🚀 TasteShift Server                      ║"
echo "║              AI-Powered Cultural Intelligence                ║"
echo "║                  Qloo Taste AI Hackathon                    ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo -e "${NC}"

print_header "🔧 Starting TasteShift Server Setup..."

# Check if we're in the right directory
if [ ! -f "main.py" ] || [ ! -f "app.py" ]; then
    print_error "TasteShift files not found in current directory!"
    print_status "Please navigate to the TasteShift project directory first."
    exit 1
fi

print_success "Found TasteShift project files"

# Step 1: Activate virtual environment if it exists
if [ -d ".venv" ]; then
    print_status "Activating virtual environment (.venv)..."
    source .venv/bin/activate
    print_success "Virtual environment activated"
    PYTHON_CMD="python"  # Use venv python
elif [ -d "venv" ]; then
    print_status "Activating virtual environment (venv)..."
    source venv/bin/activate
    print_success "Virtual environment activated"
    PYTHON_CMD="python"  # Use venv python
else
    print_warning "No virtual environment found. Creating one..."
    if command -v python3 >/dev/null 2>&1; then
        python3 -m venv .venv
        source .venv/bin/activate
        print_success "Virtual environment created and activated"
        PYTHON_CMD="python"
    else
        print_warning "python3 not found. Using system Python."
        PYTHON_CMD="python"
    fi
fi

# Step 2: Set environment variables
print_status "Setting up environment variables..."

# Set the Gemini API Key
export GEMINI_API_KEY="AIzaSyCJmaRDeEs4SQOYLkpQv_JVVoC_-mXe1N8"

# Connect to Supabase PostgreSQL database
export USE_LOCAL_DB="false"

# Supabase configuration
export SUPABASE_URL="https://onscypevhzxnucswtspm.supabase.co"
export SUPABASE_ANON_KEY="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im9uc2N5cGV2aHp4bnVjc3d0c3BtIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTIyMjk1NDEsImV4cCI6MjA2NzgwNTU0MX0.44Ykn5tfwFi0JhAmFqJSBSVE4dh2gt6j3RIADCZoSm0"

# Optional: Set Qloo API key if available
# export QLOO_API_KEY="your_qloo_key_here"

print_success "Environment variables configured"

# Step 3: Check Python version
print_status "Checking Python version..."
# If PYTHON_CMD wasn't set in venv activation, detect it
if [ -z "$PYTHON_CMD" ]; then
    if command -v python3 >/dev/null 2>&1; then
        PYTHON_CMD="python3"
    elif command -v python >/dev/null 2>&1; then
        PYTHON_CMD="python"
    else
        print_error "Python not found! Please install Python 3.8 or higher."
        exit 1
    fi
fi

python_version=$($PYTHON_CMD --version 2>&1)
if [ -n "$VIRTUAL_ENV" ]; then
    print_success "Using: $python_version with command: $PYTHON_CMD (Virtual Environment: $VIRTUAL_ENV)"
else
    print_success "Using: $python_version with command: $PYTHON_CMD (System Python)"
fi

# Step 4: Upgrade pip
print_status "Upgrading pip..."
$PYTHON_CMD -m pip install --upgrade pip --quiet

# Step 5: Install/upgrade critical dependencies
print_status "Installing critical dependencies..."

# Install SQLAlchemy first (compatible version for Python 3.13)
$PYTHON_CMD -m pip install --upgrade "SQLAlchemy>=2.0.41" --quiet

# Install psycopg2-binary for PostgreSQL
if ! $PYTHON_CMD -m pip show psycopg2-binary > /dev/null 2>&1; then
    print_status "Installing PostgreSQL adapter..."
    $PYTHON_CMD -m pip install psycopg2-binary --quiet
    if [ $? -eq 0 ]; then
        print_success "PostgreSQL adapter installed"
    else
        print_warning "PostgreSQL adapter installation failed. Trying alternative..."
        $PYTHON_CMD -m pip install psycopg2 --quiet
    fi
else
    print_success "PostgreSQL adapter already installed"
fi

# Step 6: Install remaining requirements
print_status "Installing remaining requirements..."
if [ -f "requirements_minimal.txt" ]; then
    $PYTHON_CMD -m pip install -r requirements_minimal.txt --quiet
elif [ -f "requirements.txt" ]; then
    $PYTHON_CMD -m pip install -r requirements.txt --quiet
else
    print_warning "No requirements file found. Installing core dependencies..."
    $PYTHON_CMD -m pip install Flask Flask-SQLAlchemy Flask-CORS google-generativeai requests python-dotenv aiohttp matplotlib seaborn plotly --quiet
fi

print_success "Dependencies installed"

# Step 7: Test critical imports
print_status "Testing critical imports..."
$PYTHON_CMD -c "import flask; print('✅ Flask:', flask.__version__)" 2>/dev/null
$PYTHON_CMD -c "import psycopg2; print('✅ PostgreSQL adapter: OK')" 2>/dev/null
$PYTHON_CMD -c "import google.generativeai; print('✅ Gemini AI: OK')" 2>/dev/null
$PYTHON_CMD -c "import aiohttp; print('✅ aiohttp: OK')" 2>/dev/null || print_warning "aiohttp not available"
$PYTHON_CMD -c "import matplotlib; print('✅ matplotlib: OK')" 2>/dev/null || print_warning "matplotlib not available"
$PYTHON_CMD -c "import seaborn; print('✅ seaborn: OK')" 2>/dev/null || print_warning "seaborn not available"
$PYTHON_CMD -c "import plotly; print('✅ plotly: OK')" 2>/dev/null || print_warning "plotly not available"

# Step 8: Check and free port 8000
print_status "Checking port 8000..."
if command -v lsof >/dev/null 2>&1; then
    if lsof -Pi :8000 -sTCP:LISTEN -t >/dev/null; then
        print_warning "Port 8000 is in use. Freeing it..."
        lsof -ti:8000 | xargs kill -9 2>/dev/null || true
        sleep 2
        print_success "Port 8000 freed"
    else
        print_success "Port 8000 is available"
    fi
else
    print_warning "lsof not available, skipping port check"
fi

# Step 9: Initialize database
print_status "Initializing database..."
if [ -f "init_database.py" ]; then
    $PYTHON_CMD init_database.py
    if [ $? -eq 0 ]; then
        print_success "Database initialized"
    else
        print_warning "Database initialization had issues (may be normal)"
    fi
else
    print_warning "Database initialization script not found"
fi

# Step 10: Display startup information
echo ""
print_header "🌟 TasteShift Server Ready!"
echo ""
print_success "✅ Environment: Configured"
if [ -n "$VIRTUAL_ENV" ]; then
    print_success "✅ Virtual Environment: Active (.venv)"
else
    print_success "✅ Python: System Python"
fi
print_success "✅ Database: Supabase PostgreSQL"
print_success "✅ AI Integration: Gemini API"
print_success "✅ Dependencies: Installed"
echo ""
print_status "🌐 Server will be available at:"
print_status "   • Local: http://127.0.0.1:8000"
print_status "   • Network: http://localhost:8000"
echo ""
print_status "🎯 Features enabled:"
print_status "   • AI-powered persona generation"
print_status "   • Campaign analysis with Qloo + Gemini"
print_status "   • Interactive data visualizations"
print_status "   • Cross-cultural intelligence tools"
print_status "   • Real-time Supabase database"
echo ""
print_header "🚀 Starting Flask application..."
echo ""

# Step 11: Start the Flask application
$PYTHON_CMD main.py
