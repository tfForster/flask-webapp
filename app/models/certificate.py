from app import db
from datetime import datetime


class Certificate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    issuer = db.Column(db.String(120))
    date = db.Column(db.Date)
    file = db.Column(db.String(200), nullable=False)      # Dateiname der PDF
    type = db.Column(db.String(50), default="Zertifikat") # "Ausbildung", "Kurs", "Zertifikat"
    is_public = db.Column(db.Boolean, default=True)
    order = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Certificate {self.title}>'