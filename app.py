from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

# Initialize Flask app and configure database
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

# Define the model directly in this file to avoid circular imports
class Verification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    document_type = db.Column(db.String(50), nullable=False)
    document_text = db.Column(db.Text, nullable=False)

# Create the database tables (only needed once or conditionally)
with app.app_context():
    db.create_all()

# Example route
@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        doc_type = request.form['doc_type']
        doc_text = request.form['doc_text']
        new_verification = Verification(document_type=doc_type, document_text=doc_text)
        db.session.add(new_verification)
        db.session.commit()
        return 'Document saved!'
    return '''
        <form method="post">
            Document Type: <input type="text" name="doc_type"><br>
            Document Text: <textarea name="doc_text"></textarea><br>
            <input type="submit">
        </form>
    '''

if __name__ == '__main__':
    app.run(debug=True)
