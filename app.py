from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
import os
import socket

app = Flask(__name__)

# Database configuration
db_path = os.path.join(os.path.dirname(__file__), 'cloud_data.db')
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Database Model
class CloudResource(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    server_name = db.Column(db.String(100), nullable=False)
    ip_address = db.Column(db.String(50), nullable=False)
    status = db.Column(db.String(20), default='Online')

# Create database inside the container
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    resources = CloudResource.query.all()
    # Live info about the host running the app
    hostname = socket.gethostname()
    return render_template('index.html', resources=resources, hostname=hostname)

@app.route('/add', list=['POST'])
def add():
    s_name = request.form.get('server_name')
    s_ip = request.form.get('ip_address')
    new_resource = CloudResource(server_name=s_name, ip_address=s_ip)
    db.session.add(new_resource)
    db.session.commit()
    return redirect('/')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)