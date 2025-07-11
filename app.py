from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
import pytesseract
from PIL import Image, UnidentifiedImageError
from pdf2image import convert_from_path
import os
import re
from datetime import datetime

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///verifications.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Model Import
from models import Verification

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

# Validator function
def identify_document(text):
    if re.search(r"\d{4}\s\d{4}\s\d{4}", text):
        return "Aadhaar"
    elif re.search(r"[A-Z]{5}\d{4}[A-Z]", text):
        return "PAN"
    elif re.search(r"[A-Z]{1}-?\d{7}", text):
        return "Passport"
    return "Invalid Document"

@app.route('/')
def index():
    records = Verification.query.order_by(Verification.timestamp.desc()).all()
    return render_template('index.html', records=records)

@app.route('/upload', methods=['POST'])
def upload_file():
    try:
        file = request.files['document']
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)

        text = ""

        if file.filename.lower().endswith(('.jpg', '.jpeg', '.png')):
            text = pytesseract.image_to_string(Image.open(filepath))
        elif file.filename.lower().endswith('.pdf'):
            images = convert_from_path(filepath)
            for img in images:
                text += pytesseract.image_to_string(img)
        else:
            return "Only JPG, PNG or PDF files are supported.", 400

        doc_type = identify_document(text)

        record = Verification(
            filename=file.filename,
            document_type=doc_type,
            extracted_text=text
        )
        db.session.add(record)
        db.session.commit()

        records = Verification.query.order_by(Verification.timestamp.desc()).all()
        return render_template('index.html', extracted=text, status=doc_type, records=records)

    except UnidentifiedImageError:
        return "❌ Invalid image format", 400
    except Exception as e:
        return f"❌ Error: {str(e)}", 500

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
