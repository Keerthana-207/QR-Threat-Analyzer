from flask import Flask, render_template, request, redirect, url_for
import os
# from qreader import QReader
from database import init_db, save_scan, get_all_scans

app = Flask(__name__)

# uploads folder
UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

init_db()

# qreader = QReader()

@app.route('/')
def home():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
