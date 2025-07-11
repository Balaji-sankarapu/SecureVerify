from flask import Flask, render_template, request
import pytesseract
from PIL import Image, UnidentifiedImageError
import os
import re

app = Flask(__name__)
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Create upload folder if it doesn't exist
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Function to check Aadhaar format
def verify_aadhaar(text):
    match = re.search(r"\d{4}\s\d{4}\s\d{4}", text)
    return "Valid Aadhaar" if match else "Invalid Document"

# Route for home page
@app.route('/')
def index():
    return render_template('index.html')

# Route to handle upload
@app.route('/upload', methods=['POST'])
def upload_file():
    try:
        file = request.files['document']
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)

        # OCR on image
        image = Image.open(filepath)
        text = pytesseract.image_to_string(image)

        result = verify_aadhaar(text)

        return render_template('index.html', extracted=text, status=result)

    except UnidentifiedImageError:
        return "⚠️ Only image files (JPG, PNG) are supported currently.", 400

    except Exception as e:
        return f"❌ Something went wrong: {str(e)}", 500

if __name__ == '__main__':
    app.run(debug=True)
