import os
from dotenv import load_dotenv
from flask import Flask, render_template, request, jsonify, redirect, url_for, session
from database import init_db, save_scan, get_all_scans, get_scan_summary
# If database.py provides a function to fetch single items or delete them:
from database import get_scan_by_id

from qr_decoder import decode_qr
from upload_handler import save_upload
from threat_engine import analyze_payload

load_dotenv()
app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")
UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

init_db()

@app.route("/")
def home():
    summary = get_scan_summary()
    return render_template("index.html", summary=summary, title="Dashboard | QR Shield")

@app.route("/scan")
def scan_page():
    return render_template("scan.html", title="Scan Engine | QR Shield")

@app.route("/history")
def history():
    scans = get_all_scans()
    return render_template(
        "history.html",
        scans=scans,
        title="System Logs | QR Shield"
    )

@app.route("/view-scan", methods=["POST"])
def view_scan():
    scan_id = request.form.get("scan_id")

    session["current_scan_id"] = scan_id

    return redirect(url_for("scan_detail"))

@app.route("/scan-detail")
def scan_detail():
    scan_id = session.get("current_scan_id")

    if not scan_id:
        return redirect(url_for("history"))

    db_scan = get_scan_by_id(scan_id)

    if not db_scan:
        return redirect(url_for("history"))

    analysis_result = analyze_payload(db_scan[1])

    scan = {
        "id": db_scan[0],
        "time": db_scan[5],
        "url": db_scan[1],
        "score": db_scan[2],
        "status": db_scan[3],
        "domain": analysis_result["analysis"]["domain"],
        "transport": analysis_result["analysis"]["transport"],
        "https": analysis_result["analysis"]["https"],
        "shortened": any(
            "Shortener" in note for note in analysis_result["analysis"]["notes"]
        ),
        "keywords": [],
        "reasons": analysis_result["analysis"]["notes"]
    }

    return render_template("scan_detail.html", scan=scan)

@app.route("/delete/<int:scan_id>", methods=["POST"])
def delete_scan(scan_id):
    # delete_scan_by_id(scan_id)
    return redirect(url_for('history'))

@app.route("/api/analyze", methods=["POST"])
def api_analyze():
    payload = request.get_json(silent=True) or {}
    qr_data = payload.get("payload", "")
    if not qr_data or not isinstance(qr_data, str):
        return jsonify({"success": False, "message": "Please provide text or a URL to analyze."}), 400

    scan_result = analyze_payload(qr_data)
    save_scan(scan_result["payload"], scan_result["score"], scan_result["verdict"], scan_result["source_type"])
    return jsonify({"success": True, "result": scan_result})

@app.route("/api/upload", methods=["POST"])
def api_upload():
    if "file" not in request.files:
        return render_template(
            "scan.html",
            data={
                "decoded_url": "Upload Failed",
                "score": 0,
                "status": "Safe",
                "reasons": ["No file uploaded."]
            }
        )

    file = request.files["file"]
    save_result = save_upload(file, app.config["UPLOAD_FOLDER"])
    if not save_result["success"]:
        return render_template(
            "scan.html",
            data={
                "decoded_url": "Upload Failed",
                "score": 0,
                "status": "Safe",
                "reasons": ["No file uploaded."]
            }
        )

    decoded = decode_qr(save_result["path"])
    if not decoded["success"]:
        return render_template(
            "scan.html",
            data={
                "decoded_url": "Upload Failed",
                "score": 0,
                "status": "Safe",
                "reasons": ["No file uploaded."]
            }
        )

    qr_data = decoded["data"][0]
    scan_result = analyze_payload(qr_data)
    save_scan(scan_result["payload"], scan_result["score"], scan_result["verdict"], scan_result["source_type"])
    scan_result["decoded_image"] = os.path.basename(save_result["path"])
    return render_template(
        "scan.html",
        data={
            "decoded_url": scan_result["payload"],
            "score": scan_result["score"],
            "status": scan_result["verdict"],
            "reasons": scan_result["analysis"]["notes"]
        },
        title="Scan Result | QR Shield"
    )

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)