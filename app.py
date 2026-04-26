from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os
import socket

app = Flask(__name__)

# Database Configuration
db_path = os.path.join(os.path.dirname(__file__), 'cloud_data.db')
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Database Model
class CloudResource(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    server_name = db.Column(db.String(100), nullable=False)
    ip_address = db.Column(db.String(50), nullable=False)
    status = db.Column(db.String(20), default='Checking...')

# Real-time Health Check using Socket
def check_health(ip):
    try:
        # Port 80 (HTTP) ya 443 (HTTPS) par connection check karein
        # Google (8.8.8.8) port 53 (DNS) par hamesha active hota hai
        ports = [53, 80, 443]
        for port in ports:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(1.5) # 1.5 seconds wait karein
                if s.connect_ex((ip, port)) == 0:
                    return "Healthy"
        return "Offline"
    except:
        return "Offline"

# Create database
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    resources = CloudResource.query.all()
    # Update status for each resource live
    for r in resources:
        r.status = check_health(r.ip_address)
    
    hostname = socket.gethostname()
    return render_template('index.html', resources=resources, hostname=hostname)

@app.route('/add', methods=['POST'])
def add():
    s_name = request.form.get('server_name')
    s_ip = request.form.get('ip_address')
    
    if s_name and s_ip:
        new_resource = CloudResource(server_name=s_name, ip_address=s_ip)
        db.session.add(new_resource)
        db.session.commit()
    
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)