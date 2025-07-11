from app import db
from datetime import datetime

class Verification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(100))
    document_type = db.Column(db.String(20))
    extracted_text = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
