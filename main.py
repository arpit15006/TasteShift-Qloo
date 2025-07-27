import os
import logging

# Configure logging for Railway
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

logger.info("🚀 Starting TasteShift main.py")

try:
    from app import app
    logger.info("✅ App imported successfully")
except Exception as e:
    logger.error(f"❌ Failed to import app: {str(e)}")
    raise

if __name__ == '__main__':
    # Use PORT environment variable for deployment platforms
    try:
        port_env = os.environ.get('PORT', '8000')
        # Handle case where PORT might be a string like '$PORT'
        if port_env.startswith('$'):
            port = 8000
            logger.warning(f"⚠️ Invalid PORT environment variable: {port_env}, using default: {port}")
        else:
            port = int(port_env)
    except (ValueError, TypeError):
        port = 8000
        logger.warning(f"⚠️ Could not parse PORT, using default: {port}")

    debug = os.environ.get('FLASK_ENV') != 'production'

    logger.info(f"🌐 Starting server on port {port}")
    logger.info(f"🔧 Debug mode: {debug}")

    app.run(host='0.0.0.0', port=port, debug=debug)
else:
    logger.info("📦 App module loaded for WSGI server")
