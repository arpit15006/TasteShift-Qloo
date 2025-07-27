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
    port = 8000  # Default port

    # Try to get PORT from environment
    port_env = os.environ.get('PORT')
    if port_env:
        try:
            # Only try to convert if it's not a variable reference
            if not port_env.startswith('$') and port_env.isdigit():
                port = int(port_env)
                logger.info(f"✅ Using PORT from environment: {port}")
            else:
                logger.warning(f"⚠️ Invalid PORT environment variable: {port_env}, using default: {port}")
        except (ValueError, TypeError) as e:
            logger.warning(f"⚠️ Could not parse PORT '{port_env}': {e}, using default: {port}")
    else:
        logger.info(f"ℹ️ No PORT environment variable set, using default: {port}")

    debug = os.environ.get('FLASK_ENV') != 'production'

    logger.info(f"🌐 Starting server on port {port}")
    logger.info(f"🔧 Debug mode: {debug}")

    app.run(host='0.0.0.0', port=port, debug=debug)
else:
    logger.info("📦 App module loaded for WSGI server")
