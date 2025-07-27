#!/usr/bin/env python3
"""
Railway Startup Script for TasteShift
Ensures proper initialization before starting the server
"""

import os
import sys
import logging
import time

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def check_environment():
    """Check if environment is properly configured"""
    logging.info("🔍 Checking environment configuration...")
    
    # Check Python version
    python_version = sys.version_info
    logging.info(f"🐍 Python version: {python_version.major}.{python_version.minor}.{python_version.micro}")
    
    # Check PORT environment variable
    port = os.environ.get('PORT', '8000')
    logging.info(f"🌐 Server will run on port: {port}")
    
    # Check if we're in production
    flask_env = os.environ.get('FLASK_ENV', 'development')
    logging.info(f"🏭 Environment: {flask_env}")
    
    return True

def initialize_database():
    """Initialize database with error handling"""
    logging.info("🗄️ Initializing database...")
    try:
        from app import init_database
        success = init_database()
        if success:
            logging.info("✅ Database initialized successfully")
        else:
            logging.warning("⚠️ Database initialization failed, continuing anyway")
        return True
    except Exception as e:
        logging.error(f"❌ Database initialization error: {str(e)}")
        logging.info("🚀 Continuing without database (demo mode)")
        return True

def start_application():
    """Start the Flask application"""
    logging.info("🚀 Starting TasteShift application...")
    
    # Import the app
    from app import app
    
    # Get configuration
    port = int(os.environ.get('PORT', 8000))
    debug = os.environ.get('FLASK_ENV') != 'production'
    
    logging.info(f"🌟 TasteShift starting on port {port}")
    logging.info(f"🔧 Debug mode: {debug}")
    
    # Start the application
    app.run(host='0.0.0.0', port=port, debug=debug)

def main():
    """Main startup function"""
    logging.info("🎯 TasteShift Railway Startup")
    logging.info("=" * 50)
    
    try:
        # Step 1: Check environment
        if not check_environment():
            logging.error("❌ Environment check failed")
            sys.exit(1)
        
        # Step 2: Initialize database
        if not initialize_database():
            logging.error("❌ Database initialization failed")
            # Don't exit, continue without database
        
        # Step 3: Start application
        start_application()
        
    except KeyboardInterrupt:
        logging.info("🛑 Application stopped by user")
    except Exception as e:
        logging.error(f"💥 Startup failed: {str(e)}")
        sys.exit(1)

if __name__ == '__main__':
    main()
