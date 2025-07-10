from flask import render_template, request, jsonify
from app import app, db
from models import Persona, CampaignAnalysis
from services.qloo_service import get_taste_patterns
from services.gemini_service import generate_persona, analyze_campaign
import json
import logging

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/onboarding')
def onboarding():
    return render_template('onboarding.html')

@app.route('/api/generate-persona', methods=['POST'])
def generate_persona_route():
    try:
        data = request.get_json()
        region = data.get('region')
        demographic = data.get('demographic')
        
        if not region or not demographic:
            return jsonify({'error': 'Region and demographic are required'}), 400
        
        # Get taste patterns from Qloo API
        taste_data = get_taste_patterns(region, demographic)
        
        if not taste_data:
            return jsonify({'error': 'Failed to fetch taste patterns'}), 500
        
        # Generate persona using Gemini
        persona_description = generate_persona(taste_data, region, demographic)
        
        if not persona_description:
            return jsonify({'error': 'Failed to generate persona'}), 500
        
        # Save to database
        try:
            persona = Persona(
                region=region,
                demographic=demographic,
                taste_data=json.dumps(taste_data),
                persona_description=persona_description
            )
            db.session.add(persona)
            db.session.commit()
        except Exception as db_error:
            logging.error(f"Database error when saving persona: {str(db_error)}")
            # Return success even if database save fails
            persona = {
                'id': None,
                'region': region,
                'demographic': demographic,
                'taste_data': taste_data,
                'persona_description': persona_description,
                'created_at': None
            }
        
        return jsonify({
            'success': True,
            'persona': persona.to_dict() if hasattr(persona, 'to_dict') else persona
        })
        
    except Exception as e:
        logging.error(f"Error generating persona: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/api/analyze-campaign', methods=['POST'])
def analyze_campaign_route():
    try:
        data = request.get_json()
        persona_id = data.get('persona_id')
        campaign_brief = data.get('campaign_brief')
        
        if not persona_id or not campaign_brief:
            return jsonify({'error': 'Persona ID and campaign brief are required'}), 400
        
        # Get persona from database
        persona = Persona.query.get(persona_id)
        if not persona:
            return jsonify({'error': 'Persona not found'}), 404
        
        # Analyze campaign with Gemini
        analysis_result = analyze_campaign(
            persona.persona_description,
            json.loads(persona.taste_data),
            campaign_brief
        )
        
        if not analysis_result:
            return jsonify({'error': 'Failed to analyze campaign'}), 500
        
        # Save analysis to database
        try:
            campaign_analysis = CampaignAnalysis(
                persona_id=persona_id,
                campaign_brief=campaign_brief,
                taste_shock_score=analysis_result.get('taste_shock_score'),
                creative_suggestions=json.dumps(analysis_result.get('creative_suggestions', []))
            )
            db.session.add(campaign_analysis)
            db.session.commit()
        except Exception as db_error:
            logging.error(f"Database error when saving analysis: {str(db_error)}")
            # Return success even if database save fails
            campaign_analysis = {
                'id': None,
                'persona_id': persona_id,
                'campaign_brief': campaign_brief,
                'taste_shock_score': analysis_result.get('taste_shock_score'),
                'creative_suggestions': analysis_result.get('creative_suggestions', []),
                'created_at': None
            }
        
        return jsonify({
            'success': True,
            'analysis': campaign_analysis.to_dict() if hasattr(campaign_analysis, 'to_dict') else campaign_analysis
        })
        
    except Exception as e:
        logging.error(f"Error analyzing campaign: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/api/personas', methods=['GET'])
def get_personas():
    try:
        personas = Persona.query.order_by(Persona.created_at.desc()).limit(10).all()
        return jsonify({
            'personas': [persona.to_dict() for persona in personas]
        })
    except Exception as e:
        logging.error(f"Error fetching personas: {str(e)}")
        # Return empty list if database is not available
        return jsonify({'personas': []})

@app.route('/api/persona/<int:persona_id>/analyses', methods=['GET'])
def get_persona_analyses(persona_id):
    try:
        analyses = CampaignAnalysis.query.filter_by(persona_id=persona_id).order_by(CampaignAnalysis.created_at.desc()).all()
        return jsonify({
            'analyses': [analysis.to_dict() for analysis in analyses]
        })
    except Exception as e:
        logging.error(f"Error fetching analyses: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500
