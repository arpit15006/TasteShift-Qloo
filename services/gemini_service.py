import os
import json
import logging
from google import genai
from google.genai import types

# Initialize Gemini client
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    logging.error("GEMINI_API_KEY not found in environment variables")
    GEMINI_API_KEY = "AIzaSyBbYvRipCZLg2qn2ySFkiKnRjXcp164vG0"
client = genai.Client(api_key=GEMINI_API_KEY)

def generate_persona(taste_data, region, demographic):
    """
    Generate a detailed persona based on Qloo taste data
    """
    try:
        prompt = f"""
        Based on the following cultural taste data for {demographic} in {region}, create a detailed "Future Persona" profile.

        Taste Data: {json.dumps(taste_data, indent=2)}

        Create a comprehensive persona that includes:
        1. Demographics and psychographics
        2. Cultural preferences and behaviors
        3. Media consumption habits
        4. Shopping and lifestyle patterns
        5. Values and motivations
        6. Communication style preferences
        7. Emerging trends they're likely to adopt

        Write this as a detailed, engaging profile that a marketing team could use to understand this audience segment.
        """

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        if response.text:
            logging.info(f"Successfully generated persona for {demographic} in {region}")
            return response.text
        else:
            logging.error("Empty response from Gemini when generating persona")
            return None

    except Exception as e:
        logging.error(f"Error generating persona with Gemini: {str(e)}")
        return None

def analyze_campaign(persona_description, taste_data, campaign_brief):
    """
    Analyze campaign alignment with persona and generate creative suggestions
    """
    try:
        system_prompt = """
        You are a cultural intelligence expert analyzing marketing campaigns. Based on the persona and taste data provided, 
        analyze the campaign brief and provide:
        1. A Taste Shock Score (0-100) where:
           - 0-30: Highly aligned with cultural preferences
           - 31-60: Moderately aligned, some cultural disruption
           - 61-100: Highly disruptive, challenges cultural norms
        2. Three creative suggestions that would better align with this audience

        Respond in JSON format with this structure:
        {
            "taste_shock_score": number,
            "creative_suggestions": [
                {"type": "tagline", "suggestion": "text"},
                {"type": "concept", "suggestion": "text"},
                {"type": "visual", "suggestion": "text"}
            ],
            "reasoning": "explanation of the score and suggestions"
        }
        """

        prompt = f"""
        Persona: {persona_description}
        
        Taste Data: {json.dumps(taste_data, indent=2)}
        
        Campaign Brief: {campaign_brief}
        
        Analyze this campaign against the persona and provide the requested analysis.
        """

        response = client.models.generate_content(
            model="gemini-2.5-pro",
            contents=[
                types.Content(role="user", parts=[types.Part(text=prompt)])
            ],
            config=types.GenerateContentConfig(
                system_instruction=system_prompt,
                response_mime_type="application/json"
            )
        )

        if response.text:
            try:
                result = json.loads(response.text)
                logging.info(f"Successfully analyzed campaign with shock score: {result.get('taste_shock_score')}")
                return result
            except json.JSONDecodeError:
                logging.error("Invalid JSON response from Gemini")
                return None
        else:
            logging.error("Empty response from Gemini when analyzing campaign")
            return None

    except Exception as e:
        logging.error(f"Error analyzing campaign with Gemini: {str(e)}")
        return None

def generate_creative_content(persona_description, campaign_type, brand_context=""):
    """
    Generate creative content suggestions for a specific campaign type
    """
    try:
        prompt = f"""
        Based on this persona: {persona_description}
        
        Generate creative content for a {campaign_type} campaign.
        Brand context: {brand_context}
        
        Provide:
        1. Three compelling taglines
        2. Three social media post concepts
        3. Three visual direction suggestions
        4. Key messaging pillars
        
        Format as JSON with clear categories.
        """

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        if response.text:
            return response.text
        else:
            return None

    except Exception as e:
        logging.error(f"Error generating creative content: {str(e)}")
        return None
