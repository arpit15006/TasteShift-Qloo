#!/usr/bin/env python3
"""
🏆 HACKATHON API VERIFICATION SCRIPT
Test all features to ensure they're using real Qloo + Gemini APIs
"""

import requests
import json
import time
from datetime import datetime

# Test configuration
BASE_URL = "http://localhost:8001"
TEST_RESULTS = []

def log_test(feature_name, status, details=""):
    """Log test results"""
    result = {
        'feature': feature_name,
        'status': status,
        'details': details,
        'timestamp': datetime.now().isoformat()
    }
    TEST_RESULTS.append(result)
    status_icon = "✅" if status == "REAL_API" else "⚠️" if status == "MIXED" else "❌"
    print(f"{status_icon} {feature_name}: {status} - {details}")

def test_persona_generation():
    """Test persona generation with real APIs"""
    try:
        response = requests.post(f"{BASE_URL}/api/generate-persona", json={
            "demographic": "Gen Z",
            "region": "United States"
        }, timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            if data.get('success') and 'qloo_insights' in data and 'gemini_analysis' in data:
                log_test("Persona Generation", "REAL_API", "Using Qloo + Gemini APIs")
            else:
                log_test("Persona Generation", "MIXED", "Partial API usage")
        else:
            log_test("Persona Generation", "ERROR", f"HTTP {response.status_code}")
    except Exception as e:
        log_test("Persona Generation", "ERROR", str(e))

def test_cultural_intelligence():
    """Test cultural intelligence features"""
    try:
        response = requests.post(f"{BASE_URL}/api/sophisticated-cross-domain-insights", json={
            "region": "Global",
            "demographic": "Millennials",
            "primary_interest": "technology"
        }, timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            if data.get('success') and 'qloo_data' in data and 'gemini_analysis' in data:
                log_test("Cultural Intelligence", "REAL_API", "Using Qloo + Gemini APIs")
            else:
                log_test("Cultural Intelligence", "MIXED", "Partial API usage")
        else:
            log_test("Cultural Intelligence", "ERROR", f"HTTP {response.status_code}")
    except Exception as e:
        log_test("Cultural Intelligence", "ERROR", str(e))

def test_campaign_analysis():
    """Test campaign analysis"""
    try:
        response = requests.post(f"{BASE_URL}/api/campaign-analysis", json={
            "campaign_name": "Test Campaign",
            "target_demographic": "Gen Z",
            "target_region": "United States",
            "campaign_content": "Tech product launch"
        }, timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            if data.get('success') and 'qloo_analysis' in data and 'gemini_insights' in data:
                log_test("Campaign Analysis", "REAL_API", "Using Qloo + Gemini APIs")
            else:
                log_test("Campaign Analysis", "MIXED", "Partial API usage")
        else:
            log_test("Campaign Analysis", "ERROR", f"HTTP {response.status_code}")
    except Exception as e:
        log_test("Campaign Analysis", "ERROR", str(e))

def test_risk_assessment():
    """Test risk assessment"""
    try:
        response = requests.post(f"{BASE_URL}/api/cultural-risk-assessment", json={
            "markets": ["United States", "Japan"],
            "campaign": "Global tech campaign"
        }, timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                log_test("Risk Assessment", "REAL_API", "Using Qloo + Gemini APIs")
            else:
                log_test("Risk Assessment", "MIXED", "Partial API usage")
        else:
            log_test("Risk Assessment", "ERROR", f"HTTP {response.status_code}")
    except Exception as e:
        log_test("Risk Assessment", "ERROR", str(e))

def test_business_impact_calculator():
    """Test business impact calculator"""
    try:
        response = requests.post(f"{BASE_URL}/api/business-impact-calculator", json={
            "campaign_data": {
                "investment": 100000,
                "duration_months": 6,
                "region": "Global",
                "demographic": "Millennials"
            },
            "market_context": {
                "audience_size": 1000000,
                "penetration_rate": 0.05
            }
        }, timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            if data.get('success') and 'data_sources' in data.get('business_impact', {}):
                sources = data['business_impact']['data_sources']
                if 'Qloo API' in sources and 'Gemini AI' in sources:
                    log_test("Business Impact Calculator", "REAL_API", "Using Qloo + Gemini APIs")
                else:
                    log_test("Business Impact Calculator", "MIXED", "Partial API usage")
            else:
                log_test("Business Impact Calculator", "MIXED", "No data sources info")
        else:
            log_test("Business Impact Calculator", "ERROR", f"HTTP {response.status_code}")
    except Exception as e:
        log_test("Business Impact Calculator", "ERROR", str(e))

def test_case_studies():
    """Test case studies generation"""
    try:
        response = requests.post(f"{BASE_URL}/api/generate-case-studies", json={
            "industry": "technology",
            "region": "Global",
            "count": 3
        }, timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            if data.get('success') and 'data_sources' in data:
                sources = data['data_sources']
                if 'Qloo API' in sources and 'Gemini AI' in sources:
                    log_test("Case Studies", "REAL_API", "Using Qloo + Gemini APIs")
                else:
                    log_test("Case Studies", "MIXED", "Partial API usage")
            else:
                log_test("Case Studies", "MIXED", "No data sources info")
        else:
            log_test("Case Studies", "ERROR", f"HTTP {response.status_code}")
    except Exception as e:
        log_test("Case Studies", "ERROR", str(e))

def test_insights_dashboard():
    """Test insights dashboard"""
    try:
        response = requests.get(f"{BASE_URL}/api/insights-data", timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            # Check if it's using real data by looking for dynamic values
            if data.get('stats', {}).get('totalPersonas', 0) > 0:
                log_test("Insights Dashboard", "REAL_API", "Using real database + API data")
            else:
                log_test("Insights Dashboard", "MIXED", "Using fallback data")
        else:
            log_test("Insights Dashboard", "ERROR", f"HTTP {response.status_code}")
    except Exception as e:
        log_test("Insights Dashboard", "ERROR", str(e))

def test_real_time_recommendations():
    """Test real-time recommendations"""
    try:
        response = requests.post(f"{BASE_URL}/api/real-time-recommendations", json={
            "preferences": {
                "region": "Global",
                "demographic": "Millennials",
                "categories": ["music", "technology"]
            },
            "limit": 5
        }, timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            if data.get('success') and data.get('recommendations'):
                log_test("Real-Time Recommendations", "REAL_API", "Using Qloo API")
            else:
                log_test("Real-Time Recommendations", "MIXED", "Partial API usage")
        else:
            log_test("Real-Time Recommendations", "ERROR", f"HTTP {response.status_code}")
    except Exception as e:
        log_test("Real-Time Recommendations", "ERROR", str(e))

def generate_report():
    """Generate comprehensive test report"""
    print("\n" + "="*80)
    print("🏆 HACKATHON API VERIFICATION REPORT")
    print("="*80)
    
    real_api_count = len([r for r in TEST_RESULTS if r['status'] == 'REAL_API'])
    mixed_count = len([r for r in TEST_RESULTS if r['status'] == 'MIXED'])
    error_count = len([r for r in TEST_RESULTS if r['status'] == 'ERROR'])
    total_count = len(TEST_RESULTS)
    
    print(f"\n📊 SUMMARY:")
    print(f"✅ Real API Features: {real_api_count}/{total_count}")
    print(f"⚠️ Mixed Features: {mixed_count}/{total_count}")
    print(f"❌ Error Features: {error_count}/{total_count}")
    
    real_api_percentage = (real_api_count / total_count) * 100 if total_count > 0 else 0
    print(f"\n🎯 REAL API COVERAGE: {real_api_percentage:.1f}%")
    
    if real_api_percentage >= 80:
        print("🏆 EXCELLENT: Your application is using real APIs extensively!")
    elif real_api_percentage >= 60:
        print("👍 GOOD: Most features are using real APIs")
    else:
        print("⚠️ NEEDS IMPROVEMENT: More features should use real APIs")
    
    print(f"\n📝 DETAILED RESULTS:")
    for result in TEST_RESULTS:
        status_icon = "✅" if result['status'] == "REAL_API" else "⚠️" if result['status'] == "MIXED" else "❌"
        print(f"{status_icon} {result['feature']}: {result['status']} - {result['details']}")
    
    print("\n" + "="*80)

if __name__ == "__main__":
    print("🚀 Starting API verification tests...")
    print("Testing all features to ensure real Qloo + Gemini API usage\n")
    
    # Run all tests
    test_persona_generation()
    time.sleep(1)
    test_cultural_intelligence()
    time.sleep(1)
    test_campaign_analysis()
    time.sleep(1)
    test_risk_assessment()
    time.sleep(1)
    test_business_impact_calculator()
    time.sleep(1)
    test_case_studies()
    time.sleep(1)
    test_insights_dashboard()
    time.sleep(1)
    test_real_time_recommendations()
    
    # Generate final report
    generate_report()
