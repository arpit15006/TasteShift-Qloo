# 🗄️ TasteShift Supabase Setup Guide

This guide will help you connect TasteShift to your Supabase PostgreSQL database.

## 📋 Prerequisites

- Python 3.8+
- Internet connection
- Your Supabase credentials (already configured)

## 🚀 Quick Setup

### 1. Test Supabase Connection

First, test if your Supabase database is accessible:

```bash
python test_supabase.py
```

This will:
- ✅ Test DNS resolution
- ✅ Test database connectivity
- ✅ Verify PostgreSQL version
- ✅ Test basic operations
- ✅ Test SQLAlchemy integration

### 2. Initialize Database

Run the database initialization script:

```bash
python init_database.py
```

This will:
- 📋 Create required tables (personas, campaign_analyses, roi_calculations, case_studies)
- 🔍 Add database indexes for performance
- 🌱 Insert sample data if tables are empty

### 3. Start the Application

```bash
./start_server.sh
```

This will:
- 📦 Install required packages
- 🗄️ Initialize database
- 🚀 Start TasteShift on http://localhost:8000

## 🔧 Configuration Details

### Database Connection

Your Supabase configuration:
- **Host**: `aws-0-ap-south-1.pooler.supabase.com`
- **Port**: `6543`
- **Database**: `postgres`
- **User**: `postgres.onscypevhzxnucswtspm`
- **SSL**: Required

### Environment Variables

The following environment variables are set in `start_server.sh`:

```bash
export GEMINI_API_KEY="AIzaSyCJmaRDeEs4SQOYLkpQv_JVVoC_-mXe1N8"
export USE_LOCAL_DB="false"  # Use Supabase
export SUPABASE_URL="https://onscypevhzxnucswtspm.supabase.co"
export SUPABASE_ANON_KEY="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

## 📊 Database Schema

### Tables Created

1. **personas**
   - `id` (Primary Key)
   - `region` (VARCHAR)
   - `demographic` (VARCHAR)
   - `taste_data` (JSONB)
   - `persona_description` (TEXT)
   - `created_at`, `updated_at` (TIMESTAMP)

2. **campaign_analyses**
   - `id` (Primary Key)
   - `persona_id` (Foreign Key)
   - `campaign_brief` (TEXT)
   - `taste_shock_score` (INTEGER)
   - `creative_suggestions` (JSONB)
   - `analysis_result` (JSONB)
   - `created_at`, `updated_at` (TIMESTAMP)

3. **roi_calculations**
   - `id` (Primary Key)
   - `business_idea` (TEXT)
   - `industry` (VARCHAR)
   - `budget` (DECIMAL)
   - `markets` (INTEGER)
   - `company_size` (VARCHAR)
   - `risk_level` (VARCHAR)
   - `roi_percentage` (DECIMAL)
   - `total_roi` (DECIMAL)
   - `calculation_data` (JSONB)
   - `created_at` (TIMESTAMP)

4. **case_studies**
   - `id` (Primary Key)
   - `company` (VARCHAR)
   - `industry` (VARCHAR)
   - `region` (VARCHAR)
   - `challenge` (TEXT)
   - `approach` (TEXT)
   - `results` (JSONB)
   - `roi_improvement` (VARCHAR)
   - `market_penetration` (VARCHAR)
   - `timeline` (VARCHAR)
   - `confidence_score` (INTEGER)
   - `data_sources` (JSONB)
   - `created_at` (TIMESTAMP)

## 🔍 Troubleshooting

### Connection Issues

If you see DNS resolution errors:
```
❌ DNS resolution failed for Supabase
```

**Solutions**:
1. Check your internet connection
2. Try using a different DNS server (8.8.8.8)
3. Temporarily use local database: `export USE_LOCAL_DB="true"`

### SSL Certificate Issues

If you see SSL errors:
```
❌ SSL connection failed
```

**Solutions**:
1. Ensure `sslmode=require` is in connection string
2. Update certificates: `pip install --upgrade certifi`

### Package Installation Issues

If psycopg2 installation fails:
```bash
# On macOS
brew install postgresql

# On Ubuntu/Debian
sudo apt-get install libpq-dev

# Then reinstall
pip install psycopg2-binary
```

## 🎯 Features Enabled with Supabase

✅ **Real Data Persistence**
- Personas saved to database
- Campaign analyses stored
- ROI calculations tracked
- Case studies managed

✅ **Performance Optimizations**
- Connection pooling
- Database indexes
- Query optimization

✅ **Scalability**
- PostgreSQL performance
- Concurrent user support
- Data integrity

## 🚀 Ready for Hackathon!

Once setup is complete, you'll have:
- 🗄️ Supabase PostgreSQL database connected
- 📊 Real data persistence
- 🔧 Case studies using real API data
- 🌍 Market Expansion Opportunities functional
- 💰 ROI Calculator with database storage

Your TasteShift application is now ready for the Qloo Taste AI Hackathon with full database functionality!
