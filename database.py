import sqlite3
from datetime import datetime

DB_NAME = "qr_scans.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS scans (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        qr_data TEXT NOT NULL,
        threat_score INTEGER NOT NULL,
        verdict TEXT NOT NULL,
        source_type TEXT NOT NULL DEFAULT 'Direct String',
        scanned_at TEXT NOT NULL
    )
    """)
    conn.commit()

    cursor.execute("PRAGMA table_info(scans)")
    columns = [row[1] for row in cursor.fetchall()]
    if "source_type" not in columns:
        cursor.execute("ALTER TABLE scans ADD COLUMN source_type TEXT NOT NULL DEFAULT 'Direct String'")
        conn.commit()

    conn.close()

def save_scan(qr_data, threat_score, verdict, source_type="Direct String"):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    scanned_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    cursor.execute("""
        INSERT INTO scans (qr_data, threat_score, verdict, source_type, scanned_at)
        VALUES(?, ?, ?, ?, ?)
    """, (qr_data, threat_score, verdict, source_type, scanned_at))

    conn.commit()
    conn.close()

def get_all_scans():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, qr_data, threat_score, verdict, source_type, scanned_at
        FROM scans
        ORDER BY id DESC
    """)

    scans = cursor.fetchall()
    conn.close()
    return scans

def get_scan_summary():
    scans = get_all_scans()
    total = len(scans)
    malicious = sum(1 for _, _, _, verdict, _, _ in scans if verdict == "Malicious")
    suspicious = sum(1 for _, _, _, verdict, _, _ in scans if verdict == "Suspicious")
    clean = total - malicious - suspicious
    return {
        "total": total,
        "malicious": malicious,
        "suspicious": suspicious,
        "clean": clean
    }

def get_scan_by_id(scan_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
    SELECT * FROM scans 
    WHERE id = ?
    """, (scan_id, ))

    scan = cursor.fetchone()
    conn.close()
    return scan


def delete_scan(scan_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM scans
        WHERE id = ?
    """, (scan_id, ))

    conn.commit()
    conn.close()

