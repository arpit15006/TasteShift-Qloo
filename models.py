from datetime import datetime
import json
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app import db, Base

class Persona(Base):
    __tablename__ = 'persona'

    id = Column(Integer, primary_key=True)
    region = Column(String(100), nullable=False)
    demographic = Column(String(100), nullable=False)
    taste_data = Column(Text)  # JSON string of Qloo taste patterns
    persona_description = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'region': self.region,
            'demographic': self.demographic,
            'taste_data': json.loads(self.taste_data) if self.taste_data else {},
            'persona_description': self.persona_description,
            'created_at': self.created_at.isoformat()
        }

class CampaignAnalysis(Base):
    __tablename__ = 'campaign_analysis'

    id = Column(Integer, primary_key=True)
    persona_id = Column(Integer, ForeignKey('persona.id'), nullable=False)
    campaign_brief = Column(Text, nullable=False)
    taste_shock_score = Column(Integer)
    creative_suggestions = Column(Text)  # JSON string
    created_at = Column(DateTime, default=datetime.utcnow)

    persona = relationship('Persona', backref='analyses')

    def to_dict(self):
        return {
            'id': self.id,
            'persona_id': self.persona_id,
            'campaign_brief': self.campaign_brief,
            'taste_shock_score': self.taste_shock_score,
            'creative_suggestions': json.loads(self.creative_suggestions) if self.creative_suggestions else [],
            'created_at': self.created_at.isoformat()
        }
