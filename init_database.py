#!/usr/bin/env python3
"""
TasteShift Database Initialization Script
Initializes Supabase PostgreSQL database with required tables
"""

import os
import sys
import logging
from datetime import datetime

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def init_supabase_database():
    """Initialize Supabase database with required tables"""
    try:
        # Import required modules
        import psycopg2
        from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
        
        # Connection parameters
        conn_params = {
            'host': 'aws-0-ap-south-1.pooler.supabase.com',
            'port': 6543,
            'database': 'postgres',
            'user': 'postgres.onscypevhzxnucswtspm',
            'password': 'Arpit1234',
            'sslmode': 'require'
        }
        
        logging.info("🔗 Connecting to Supabase PostgreSQL...")
        conn = psycopg2.connect(**conn_params)
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = conn.cursor()
        
        # Create personas table
        logging.info("📋 Creating personas table...")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS personas (
                id SERIAL PRIMARY KEY,
                region VARCHAR(100) NOT NULL,
                demographic VARCHAR(100) NOT NULL,
                taste_data JSONB,
                persona_description TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        
        # Create campaign_analyses table
        logging.info("📊 Creating campaign_analyses table...")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS campaign_analyses (
                id SERIAL PRIMARY KEY,
                persona_id INTEGER REFERENCES personas(id) ON DELETE CASCADE,
                campaign_brief TEXT NOT NULL,
                taste_shock_score INTEGER,
                creative_suggestions JSONB,
                analysis_result JSONB,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        
        # Create roi_calculations table
        logging.info("💰 Creating roi_calculations table...")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS roi_calculations (
                id SERIAL PRIMARY KEY,
                business_idea TEXT,
                industry VARCHAR(100),
                budget DECIMAL(15,2),
                markets INTEGER,
                company_size VARCHAR(50),
                risk_level VARCHAR(50),
                roi_percentage DECIMAL(8,2),
                total_roi DECIMAL(15,2),
                calculation_data JSONB,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        
        # Create case_studies table
        logging.info("📚 Creating case_studies table...")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS case_studies (
                id SERIAL PRIMARY KEY,
                company VARCHAR(200) NOT NULL,
                industry VARCHAR(100) NOT NULL,
                region VARCHAR(100),
                challenge TEXT,
                approach TEXT,
                results JSONB,
                roi_improvement VARCHAR(50),
                market_penetration VARCHAR(50),
                timeline VARCHAR(50),
                confidence_score INTEGER,
                data_sources JSONB,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        
        # Create indexes for better performance
        logging.info("🔍 Creating database indexes...")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_personas_region ON personas(region);")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_personas_demographic ON personas(demographic);")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_campaign_analyses_persona_id ON campaign_analyses(persona_id);")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_roi_calculations_industry ON roi_calculations(industry);")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_case_studies_company ON case_studies(company);")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_case_studies_industry ON case_studies(industry);")
        
        # Insert sample data if tables are empty
        logging.info("📝 Checking for sample data...")
        cursor.execute("SELECT COUNT(*) FROM personas;")
        persona_count = cursor.fetchone()[0]
        
        if persona_count == 0:
            logging.info("🌱 Inserting sample persona data...")
            cursor.execute("""
                INSERT INTO personas (region, demographic, taste_data, persona_description) VALUES
                ('United States', 'Gen Z', '{"music": ["pop", "hip-hop"], "fashion": ["streetwear", "sustainable"]}', 'Tech-savvy Gen Z consumer focused on sustainability and social impact'),
                ('Japan', 'Millennials', '{"music": ["j-pop", "electronic"], "fashion": ["minimalist", "tech-wear"]}', 'Japanese millennial with appreciation for minimalist design and technology integration'),
                ('Germany', 'Gen X', '{"music": ["rock", "classical"], "fashion": ["premium", "traditional"]}', 'German Gen X consumer valuing quality, tradition, and premium experiences');
            """)
        
        cursor.execute("SELECT COUNT(*) FROM case_studies;")
        case_study_count = cursor.fetchone()[0]
        
        if case_study_count == 0:
            logging.info("📊 Inserting sample case study data...")
            cursor.execute("""
                INSERT INTO case_studies (company, industry, region, challenge, approach, results, roi_improvement, market_penetration, timeline, confidence_score, data_sources) VALUES
                ('Spotify', 'Music Streaming', 'Global', 'Expand into Middle Eastern markets with cultural sensitivity', 'Used Qloo cross-domain cultural intelligence', '["43% increase in user acquisition", "68% higher retention rate"]', '412%', '85%', '8 months', 94, '["Qloo API", "Gemini AI"]'),
                ('Nike', 'Sportswear', 'Southeast Asia', 'Launch athletic wear line across diverse cultural contexts', 'Cultural intelligence analysis across 7 countries', '["28% higher engagement", "Zero cultural incidents"]', '215%', '72%', '6 months', 91, '["Qloo API", "Gemini AI"]');
            """)
        
        cursor.close()
        conn.close()
        
        logging.info("✅ Supabase database initialization completed successfully!")
        return True
        
    except Exception as e:
        logging.error(f"❌ Database initialization failed: {e}")
        return False

def test_database_connection():
    """Test the database connection"""
    try:
        import psycopg2
        
        conn_params = {
            'host': 'aws-0-ap-south-1.pooler.supabase.com',
            'port': 6543,
            'database': 'postgres',
            'user': 'postgres.onscypevhzxnucswtspm',
            'password': 'Arpit1234',
            'sslmode': 'require'
        }
        
        logging.info("🧪 Testing database connection...")
        conn = psycopg2.connect(**conn_params)
        cursor = conn.cursor()
        cursor.execute("SELECT version();")
        version = cursor.fetchone()[0]
        logging.info(f"✅ Connected to: {version}")
        
        cursor.close()
        conn.close()
        return True
        
    except Exception as e:
        logging.error(f"❌ Connection test failed: {e}")
        return False

if __name__ == "__main__":
    print("🚀 TasteShift Database Initialization")
    print("=" * 50)
    
    # Test connection first
    if test_database_connection():
        # Initialize database
        if init_supabase_database():
            print("🎉 Database setup completed successfully!")
            print("🌟 Ready to run TasteShift application!")
        else:
            print("❌ Database initialization failed!")
            sys.exit(1)
    else:
        print("❌ Cannot connect to database!")
        sys.exit(1)
