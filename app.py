import os
from flask import Flask, render_template, request, jsonify
from database import init_db, save_scan, get_all_scans, get_scan_summary
from qr_decoder import decode_qr
from upload_handler import save_upload
from threat_engine import analyze_payload

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Initialize database on startup
init_db()

@app.route("/")
def home():
    summary = get_scan_summary()
    return render_template("index.html", summary=summary, page_title="Dashboard", title="QR Threat Analyzer")

@app.route("/scan")
def scan_page():
    return render_template("scan.html", page_title="Analyze QR Code", title="Scan | QR Threat Analyzer")

@app.route("/history")
def history():
    scans = get_all_scans()
    return render_template("history.html", scans=scans, page_title="Analysis Log", title="History | QR Threat Analyzer")

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
        return jsonify({"success": False, "message": "No file uploaded."}), 400

    file = request.files["file"]
    save_result = save_upload(file, app.config["UPLOAD_FOLDER"])
    if not save_result["success"]:
        return jsonify({"success": False, "message": save_result["message"]}), 400

    decoded = decode_qr(save_result["path"])
    if not decoded["success"]:
        return jsonify({"success": False, "message": decoded["message"]}), 400

    qr_data = decoded["data"][0]
    scan_result = analyze_payload(qr_data)
    save_scan(scan_result["payload"], scan_result["score"], scan_result["verdict"], scan_result["source_type"])
    scan_result["decoded_image"] = os.path.basename(save_result["path"])
    return jsonify({"success": True, "result": scan_result})

if __name__ == "__main__":
    # Force host='0.0.0.0' to ensure local firewalls don't block the connection
    app.run(host='0.0.0.0', port=5000, debug=True)