import os
import logging
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

# Supabase configuration
SUPABASE_URL = os.environ.get("SUPABASE_URL", "https://soxuvylsurltctqhendh.supabase.co")
SUPABASE_ANON_KEY = os.environ.get("SUPABASE_ANON_KEY", "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InNveHV2eWxzdXJsdGN0cWhlbmRoIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTIxMjg0MDksImV4cCI6MjA2NzcwNDQwOX0.p5jVtshmHS_TIKSQvb5I2drtcaU0MMkpLQZXYlEa0ro")

class SupabaseService:
    def __init__(self):
        # Note: DATABASE_URL should be set in environment with the full PostgreSQL connection string
        self.database_url = os.environ.get("DATABASE_URL")
        if self.database_url:
            self.engine = create_engine(self.database_url)
            Session = sessionmaker(bind=self.engine)
            self.session = Session()
        else:
            logging.warning("DATABASE_URL not set, Supabase service unavailable")
            self.engine = None
            self.session = None

    def test_connection(self):
        """Test the database connection"""
        if not self.session:
            return False
        
        try:
            result = self.session.execute(text("SELECT 1"))
            return result.fetchone() is not None
        except Exception as e:
            logging.error(f"Database connection test failed: {str(e)}")
            return False

    def execute_query(self, query, params=None):
        """Execute a custom SQL query"""
        if not self.session:
            return None
        
        try:
            if params:
                result = self.session.execute(text(query), params)
            else:
                result = self.session.execute(text(query))
            self.session.commit()
            return result
        except Exception as e:
            logging.error(f"Query execution failed: {str(e)}")
            self.session.rollback()
            return None

    def get_analytics_data(self):
        """Get analytics data about personas and campaigns"""
        if not self.session:
            return {}
        
        try:
            # Get total personas
            personas_result = self.session.execute(text("SELECT COUNT(*) FROM persona"))
            total_personas = personas_result.fetchone()[0]
            
            # Get total analyses
            analyses_result = self.session.execute(text("SELECT COUNT(*) FROM campaign_analysis"))
            total_analyses = analyses_result.fetchone()[0]
            
            # Get average shock score
            avg_score_result = self.session.execute(text("SELECT AVG(taste_shock_score) FROM campaign_analysis WHERE taste_shock_score IS NOT NULL"))
            avg_shock_score = avg_score_result.fetchone()[0] or 0
            
            return {
                'total_personas': total_personas,
                'total_analyses': total_analyses,
                'avg_shock_score': round(float(avg_shock_score), 2)
            }
        except Exception as e:
            logging.error(f"Error fetching analytics: {str(e)}")
            return {}

    def close(self):
        """Close the database session"""
        if self.session:
            self.session.close()

# Global instance
supabase_service = SupabaseService()
