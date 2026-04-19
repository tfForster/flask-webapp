from app import db
from datetime import datetime


class CurrentStatus(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    description = db.Column(db.String(255))
    tech_stack = db.Column(db.String(200))        # kommasepariert wie bei Project
    is_active = db.Column(db.Boolean, default=True)  # nur einer sollte True sein
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<CurrentStatus {self.title}>'