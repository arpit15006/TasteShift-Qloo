from app import db
from datetime import datetime
import json

class Persona(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    region = db.Column(db.String(100), nullable=False)
    demographic = db.Column(db.String(100), nullable=False)
    taste_data = db.Column(db.Text)  # JSON string of Qloo taste patterns
    persona_description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'region': self.region,
            'demographic': self.demographic,
            'taste_data': json.loads(self.taste_data) if self.taste_data else {},
            'persona_description': self.persona_description,
            'created_at': self.created_at.isoformat()
        }

class CampaignAnalysis(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    persona_id = db.Column(db.Integer, db.ForeignKey('persona.id'), nullable=False)
    campaign_brief = db.Column(db.Text, nullable=False)
    taste_shock_score = db.Column(db.Integer)
    creative_suggestions = db.Column(db.Text)  # JSON string
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    persona = db.relationship('Persona', backref=db.backref('analyses', lazy=True))
    
    def to_dict(self):
        return {
            'id': self.id,
            'persona_id': self.persona_id,
            'campaign_brief': self.campaign_brief,
            'taste_shock_score': self.taste_shock_score,
            'creative_suggestions': json.loads(self.creative_suggestions) if self.creative_suggestions else [],
            'created_at': self.created_at.isoformat()
        }
