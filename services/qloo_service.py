import os
import requests
import logging

QLOO_API_URL = os.environ.get("QLOO_API_URL", "https://hackathon.api.qloo.com")
QLOO_API_KEY = os.environ.get("QLOO_API_KEY", "W-_OejnIgjKjlrZT1exz0fFtkIEf7UtwfwuW33rgedU")

def get_taste_patterns(region, demographic):
    """
    Fetch taste patterns from Qloo API based on region and demographic
    """
    try:
        headers = {
            'Authorization': f'Bearer {QLOO_API_KEY}',
            'Content-Type': 'application/json'
        }
        
        # Construct the API request based on region and demographic
        payload = {
            'query': f'{demographic} in {region}',
            'domains': ['music', 'food', 'film', 'fashion', 'books', 'brands'],
            'limit': 20
        }
        
        response = requests.post(
            f'{QLOO_API_URL}/taste',
            headers=headers,
            json=payload,
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            logging.info(f"Successfully fetched taste patterns for {demographic} in {region}")
            return data
        else:
            logging.error(f"Qloo API error: {response.status_code} - {response.text}")
            return None
            
    except requests.exceptions.RequestException as e:
        logging.error(f"Request error when calling Qloo API: {str(e)}")
        return None
    except Exception as e:
        logging.error(f"Unexpected error in get_taste_patterns: {str(e)}")
        return None

def get_cultural_insights(region, demographic):
    """
    Get cultural insights and trends for a specific demographic
    """
    try:
        headers = {
            'Authorization': f'Bearer {QLOO_API_KEY}',
            'Content-Type': 'application/json'
        }
        
        payload = {
            'query': f'cultural trends {demographic} {region}',
            'domains': ['culture', 'lifestyle', 'entertainment'],
            'limit': 10
        }
        
        response = requests.post(
            f'{QLOO_API_URL}/insights',
            headers=headers,
            json=payload,
            timeout=30
        )
        
        if response.status_code == 200:
            return response.json()
        else:
            logging.error(f"Qloo insights API error: {response.status_code}")
            return None
            
    except Exception as e:
        logging.error(f"Error fetching cultural insights: {str(e)}")
        return None
