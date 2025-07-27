import os
from app import app

if __name__ == '__main__':
    # Use PORT environment variable for deployment platforms
    port = int(os.environ.get('PORT', 8000))
    debug = os.environ.get('FLASK_ENV') != 'production'
    app.run(host='0.0.0.0', port=port, debug=debug)
