#!/usr/bin/env python3
"""
Test Supabase Connection Script
Quick test to verify Supabase database connectivity
"""

import os
import sys
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def test_supabase_connection():
    """Test Supabase database connection"""
    try:
        print("🧪 Testing Supabase Connection")
        print("=" * 40)
        
        # Test 1: Import psycopg2
        print("📦 Testing psycopg2 import...")
        try:
            import psycopg2
            print("✅ psycopg2 imported successfully")
        except ImportError:
            print("❌ psycopg2 not found, installing...")
            import subprocess
            subprocess.check_call([sys.executable, "-m", "pip", "install", "psycopg2-binary"])
            import psycopg2
            print("✅ psycopg2 installed and imported")
        
        # Test 2: DNS Resolution
        print("🌐 Testing DNS resolution...")
        import socket
        try:
            ip = socket.gethostbyname("aws-0-ap-south-1.pooler.supabase.com")
            print(f"✅ DNS resolved: aws-0-ap-south-1.pooler.supabase.com -> {ip}")
        except socket.gaierror as e:
            print(f"❌ DNS resolution failed: {e}")
            return False
        
        # Test 3: Database Connection
        print("🔗 Testing database connection...")
        conn_params = {
            'host': 'aws-0-ap-south-1.pooler.supabase.com',
            'port': 6543,
            'database': 'postgres',
            'user': 'postgres.onscypevhzxnucswtspm',
            'password': 'Arpit1234',
            'connect_timeout': 10,
            'sslmode': 'require'
        }
        
        conn = psycopg2.connect(**conn_params)
        print("✅ Database connection successful")
        
        # Test 4: Query Execution
        print("📊 Testing query execution...")
        cursor = conn.cursor()
        cursor.execute("SELECT version();")
        version = cursor.fetchone()[0]
        print(f"✅ PostgreSQL version: {version[:50]}...")
        
        # Test 5: Check Tables
        print("📋 Checking existing tables...")
        cursor.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public'
            ORDER BY table_name;
        """)
        tables = cursor.fetchall()
        if tables:
            print(f"✅ Found {len(tables)} tables:")
            for table in tables:
                print(f"   - {table[0]}")
        else:
            print("⚠️ No tables found (this is normal for a fresh database)")
        
        # Test 6: Test Insert/Select
        print("🧪 Testing basic operations...")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS test_connection (
                id SERIAL PRIMARY KEY,
                test_message TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        
        cursor.execute("""
            INSERT INTO test_connection (test_message) 
            VALUES ('TasteShift connection test successful!');
        """)
        
        cursor.execute("SELECT test_message, created_at FROM test_connection ORDER BY created_at DESC LIMIT 1;")
        result = cursor.fetchone()
        print(f"✅ Test record: {result[0]} at {result[1]}")
        
        # Cleanup
        cursor.execute("DROP TABLE test_connection;")
        conn.commit()
        
        cursor.close()
        conn.close()
        
        print("\n🎉 All tests passed! Supabase is ready for TasteShift!")
        return True
        
    except Exception as e:
        print(f"\n❌ Connection test failed: {e}")
        print(f"Error type: {type(e).__name__}")
        return False

def test_sqlalchemy_connection():
    """Test SQLAlchemy connection"""
    try:
        print("\n🔧 Testing SQLAlchemy Connection")
        print("=" * 40)
        
        from sqlalchemy import create_engine, text
        
        # Create engine with Supabase URL
        database_url = "postgresql://postgres.onscypevhzxnucswtspm:Arpit1234@aws-0-ap-south-1.pooler.supabase.com:6543/postgres?sslmode=require"
        
        engine = create_engine(
            database_url,
            pool_recycle=300,
            pool_pre_ping=True,
            pool_timeout=30,
            pool_size=5,
            max_overflow=10,
            connect_args={
                "connect_timeout": 10,
                "application_name": "TasteShift_Test",
                "sslmode": "require"
            }
        )
        
        # Test connection
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 'SQLAlchemy connection successful!' as message;"))
            message = result.fetchone()[0]
            print(f"✅ {message}")
        
        print("✅ SQLAlchemy connection test passed!")
        return True
        
    except Exception as e:
        print(f"❌ SQLAlchemy test failed: {e}")
        return False

if __name__ == "__main__":
    print("🚀 TasteShift Supabase Connection Test")
    print("=" * 50)
    
    success = True
    
    # Test direct psycopg2 connection
    if not test_supabase_connection():
        success = False
    
    # Test SQLAlchemy connection
    if not test_sqlalchemy_connection():
        success = False
    
    if success:
        print("\n🎉 All connection tests passed!")
        print("🚀 Ready to start TasteShift with Supabase!")
    else:
        print("\n❌ Some tests failed!")
        print("💡 Try running: pip install -r requirements.txt")
        sys.exit(1)
