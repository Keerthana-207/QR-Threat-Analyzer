from flask import Flask, render_template, request, redirect, url_for
import os
from datetime import datetime
# from qreader import QReader
# Assuming your database.py has these functions ready:
# from database import init_db, save_scan, get_all_scans

app = Flask(__name__)

# Configure uploads folder path
UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Initialize database on startup
# init_db()

# qreader = QReader()

@app.route('/')
def home():
    """Renders your animated index.html file."""
    return render_template("index.html")

@app.route('/upload', methods=['POST'])
def upload():
    """Handles the file upload when 'Initialize Assessment Engine' is clicked."""
    if 'qr_file' not in request.files:
        return redirect(url_for('home'))
        
    file = request.files['qr_file']
    if file.filename == '':
        return redirect(url_for('home'))

    if file:
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)

        # -------------------------------------------------------------
        # MOCK DATA: Simulating what your teammate's code will produce
        # -------------------------------------------------------------
        mock_backend_response = {
            "decoded_url": "https://paypal-login-security.xyz",
            "score": 85,
            "status": "High Risk", 
            "reasons": [
                "Uses insecure HTTP rules instead of HTTPS",
                "Suspicious top-level domain extension (.xyz)",
                "URL path string contains explicit phishing keywords"
            ]
        }
        
        # Save to database if ready:
        # save_scan(mock_backend_response["decoded_url"], mock_backend_response["score"], mock_backend_response["status"])

        return render_template("scan.html", data=mock_backend_response)

@app.route('/history')
def history():
    """Renders the historical table logs."""
    # Simulating what get_all_scans() would fetch from Member 4's DB
    mock_history_data = [
        {"time": "2026-07-01 10:45", "url": "https://www.google.com", "score": 2, "status": "Safe"},
        {"time": "2026-07-01 10:47", "url": "https://paypal-login-security.xyz", "score": 85, "status": "High Risk"}
    ]
    return render_template("history.html", history_data=mock_history_data)

if __name__ == "__main__":
    # Force host='0.0.0.0' to ensure local firewalls don't block the connection
    app.run(host='0.0.0.0', port=5000, debug=True)