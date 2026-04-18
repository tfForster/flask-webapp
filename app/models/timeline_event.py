from app import db
from datetime import datetime


class TimelineEvent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    year = db.Column(db.String(20), nullable=False)       # z.B. "2025 – heute" oder "Sommer 2025"
    title = db.Column(db.String(120), nullable=False)
    subtitle = db.Column(db.String(255))
    is_current = db.Column(db.Boolean, default=False)     # grüner Punkt wenn True
    order = db.Column(db.Integer, default=0)              # Reihenfolge (niedrig = oben)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<TimelineEvent {self.title}>'