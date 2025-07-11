# models.py
from extensions import db

class Verification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    document_type = db.Column(db.String(100))
    extracted_text = db.Column(db.Text)
