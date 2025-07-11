# app.py
from flask import Flask, render_template, request
from extensions import db
from models import Verification

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///your_database.db'
db.init_app(app)

@app.route('/')
def home():
    return render_template('index.html')

# More routes here...

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
