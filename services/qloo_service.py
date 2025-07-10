import os
import requests
import logging

QLOO_API_URL = os.environ.get("QLOO_API_URL", "https://hackathon.api.qloo.com")
QLOO_API_KEY = os.environ.get("QLOO_API_KEY", "W-_OejnIgjKjlrZT1exz0fFtkIEf7UtwfwuW33rgedU")

def get_taste_patterns(region, demographic):
    """
    Fetch taste patterns from Qloo API based on region and demographic using search endpoint
    """
    try:
        headers = {
            'X-API-Key': QLOO_API_KEY,
            'Content-Type': 'application/json'
        }
        
        # Search for cultural entities related to the demographic and region
        search_queries = [
            f'{demographic} {region}',
            f'{region} culture',
            f'{demographic} lifestyle'
        ]
        
        taste_data = {
            'music': [],
            'food': [],
            'film': [],
            'fashion': [],
            'books': [],
            'brands': [],
            'search_results': []
        }
        
        # Search for cultural entities related to the demographic and region
        for query in search_queries:
            params = {'query': query}
            
            try:
                response = requests.get(
                    f'{QLOO_API_URL}/search',
                    headers=headers,
                    params=params,
                    timeout=15
                )
                
                if response.status_code == 200:
                    data = response.json()
                    taste_data['search_results'].append({
                        'query': query,
                        'results': data.get('results', [])[:5]
                    })
                    logging.info(f"Successfully fetched search results for: {query}")
                else:
                    logging.error(f"Qloo API search error: {response.status_code} - {response.text}")
            except Exception as e:
                logging.error(f"Error calling Qloo API: {str(e)}")
        
        if taste_data['search_results']:
            logging.info(f"Successfully fetched taste patterns for {demographic} in {region}")
            return taste_data
        else:
            logging.error("Failed to fetch any data from Qloo API")
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
            'X-API-Key': QLOO_API_KEY,
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
