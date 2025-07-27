#!/bin/bash

# TasteShift Local Deployment Script
# This script sets up and runs TasteShift in production mode locally

set -e  # Exit on any error

echo "🚀 TasteShift Local Deployment"
echo "=============================="

# Check if we're in the right directory
if [ ! -f "main.py" ] || [ ! -f "app.py" ]; then
    echo "❌ Error: TasteShift files not found in current directory!"
    echo "Please navigate to the TasteShift project directory first."
    exit 1
fi

# Create virtual environment if it doesn't exist
if [ ! -d ".venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv .venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source .venv/bin/activate

# Install/upgrade pip
echo "⬆️ Upgrading pip..."
pip install --upgrade pip

# Install requirements
echo "📚 Installing requirements..."
pip install -r requirements.txt

# Set production environment
export FLASK_ENV=production
export PORT=5000

# Load environment variables if .env exists
if [ -f ".env" ]; then
    echo "🔑 Loading environment variables from .env..."
    export $(cat .env | grep -v '^#' | xargs)
else
    echo "⚠️ Warning: .env file not found. Using default environment variables."
    echo "💡 Copy .env.example to .env and configure your API keys for full functionality."
fi

# Initialize database
echo "🗄️ Initializing database..."
python init_database.py || echo "⚠️ Database initialization completed with warnings"

# Start the application with Gunicorn
echo "🌟 Starting TasteShift in production mode..."
echo "📍 Application will be available at: http://localhost:5000"
echo "🛑 Press Ctrl+C to stop the server"
echo ""

gunicorn main:app --bind 0.0.0.0:5000 --workers 1 --timeout 120 --reload
