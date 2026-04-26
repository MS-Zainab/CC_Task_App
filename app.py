from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# Database Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cloud_data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Database Model
class Visitor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

# Create the database locally
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    visitors = Visitor.query.all()
    return render_template('index.html', visitors=visitors)

@app.route('/add', methods=['POST'])
def add_visitor():
    name = request.form.get('name')
    if name:
        new_visitor = Visitor(name=name)
        db.session.add(new_visitor)
        db.session.commit()
    return redirect('/')

if __name__ == '__main__':
    # Critical for Cloud/Docker: Bind to 0.0.0.0
    app.run(host='0.0.0.0', port=5000, debug=True)