import os
import logging
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from sqlalchemy.orm import DeclarativeBase
from werkzeug.middleware.proxy_fix import ProxyFix

# Configure logging
logging.basicConfig(level=logging.DEBUG)

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)

# Create the app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "dev-secret-key")
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

# Enable CORS for frontend-backend communication
CORS(app, origins=['*'])

# Configure the database with better connection handling
def configure_database():
    database_url = os.environ.get("DATABASE_URL")
    use_local_db = os.environ.get("USE_LOCAL_DB", "false").lower() == "true"

    # Check if user wants to force local database
    if use_local_db:
        logging.info("🏠 Using local SQLite database (forced by USE_LOCAL_DB)")
        return "sqlite:///tasteshift_demo.db"

    # Try Supabase first, fallback to SQLite for demo
    if not database_url:
        try:
            # Use your Supabase PostgreSQL database
            supabase_url = "postgresql://postgres.onscypevhzxnucswtspm:Arpit1234@aws-0-ap-south-1.pooler.supabase.com:6543/postgres"
            logging.info("🔗 Connecting to Supabase PostgreSQL database...")

            # Install required packages if not available
            try:
                import psycopg2
            except ImportError:
                logging.info("📦 Installing psycopg2-binary for PostgreSQL support...")
                import subprocess
                import sys
                subprocess.check_call([sys.executable, "-m", "pip", "install", "psycopg2-binary"])
                import psycopg2

            # Test database connection with proper timeout and SSL settings
            import psycopg2
            from psycopg2 import OperationalError

            # Connection parameters for Supabase
            conn_params = {
                'host': 'aws-0-ap-south-1.pooler.supabase.com',
                'port': 6543,
                'database': 'postgres',
                'user': 'postgres.onscypevhzxnucswtspm',
                'password': 'Arpit1234',
                'connect_timeout': 10,
                'sslmode': 'require'  # Supabase requires SSL
            }

            logging.info("🔐 Testing Supabase connection with SSL...")
            test_conn = psycopg2.connect(**conn_params)
            test_conn.close()
            logging.info("✅ Supabase database connection successful!")

            # Use the connection string format that works with SQLAlchemy
            database_url = f"postgresql://postgres.onscypevhzxnucswtspm:Arpit1234@aws-0-ap-south-1.pooler.supabase.com:6543/postgres?sslmode=require"

        except Exception as e:
            logging.warning(f"⚠️ Supabase connection failed: {e}")
            logging.info("🔄 Falling back to SQLite for demo purposes")
            database_url = "sqlite:///tasteshift_demo.db"

    elif database_url and '#' in database_url:
        # Fix URL encoding for special characters in password
        database_url = database_url.replace('#', '%23')
        logging.info("Fixed URL encoding for database password")

    logging.info(f"📊 Using database: {'PostgreSQL (Supabase)' if 'postgresql' in database_url else 'SQLite (Local)'}")
    return database_url

database_url = configure_database()
app.config["SQLALCHEMY_DATABASE_URI"] = database_url

# Configure SQLAlchemy engine options based on database type
if database_url.startswith('postgresql'):
    # Supabase PostgreSQL configuration
    app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
        "pool_recycle": 300,
        "pool_pre_ping": True,
        "pool_timeout": 30,
        "pool_size": 10,
        "max_overflow": 20,
        "connect_args": {
            "connect_timeout": 10,
            "application_name": "TasteShift_Hackathon",
            "sslmode": "require",
            "options": "-c timezone=utc"
        }
    }
else:
    # SQLite configuration
    app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
        "pool_recycle": 300,
        "pool_pre_ping": True,
        "connect_args": {
            "check_same_thread": False,
            "timeout": 20
        }
    }
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Initialize the app with the extension
db.init_app(app)

with app.app_context():
    try:
        # Import models to ensure tables are created
        # Use a more specific import to avoid circular import issues
        from models import Base
        db.create_all()
        logging.info("Database tables created successfully")
    except ImportError as e:
        logging.error(f"Models import failed: {str(e)}")
        logging.info("Attempting alternative import approach...")
        try:
            # Try direct table creation without importing models
            # This is a fallback for demo purposes
            from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
            from sqlalchemy.orm import relationship
            from datetime import datetime

            # Define models directly if import fails
            class Persona(Base):
                __tablename__ = 'persona'
                id = Column(Integer, primary_key=True)
                region = Column(String(100), nullable=False)
                demographic = Column(String(100), nullable=False)
                taste_data = Column(Text)
                persona_description = Column(Text)
                created_at = Column(DateTime, default=datetime.utcnow)

            class CampaignAnalysis(Base):
                __tablename__ = 'campaign_analysis'
                id = Column(Integer, primary_key=True)
                persona_id = Column(Integer, ForeignKey('persona.id'), nullable=False)
                campaign_brief = Column(Text, nullable=False)
                taste_shock_score = Column(Integer)
                creative_suggestions = Column(Text)
                created_at = Column(DateTime, default=datetime.utcnow)

                persona = relationship('Persona', backref='analyses')

            db.create_all()
            logging.info("Database tables created with fallback approach")
        except Exception as inner_e:
            logging.error(f"Fallback table creation failed: {str(inner_e)}")
    except Exception as e:
        logging.error(f"Database initialization failed: {str(e)}")
        # Continue with app startup even if database fails
        pass

# Import routes
from routes import *

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8001, debug=True)
