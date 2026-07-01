import sqlite3
from datetime import datetime
from json.decoder import scanstring

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
        scanned_at TEXT NOT NULL
     )
    """)

    conn.commit()
    conn.close()

# Save scanned results
def save_scan(qr_data, threat_score, verdict):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    scanned_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    cursor.execute("""
        INSERT INTO scans (qr_data, threat_score, verdict, scanned_at)
        VALUES(?, ?, ?, ?)
    """, (qr_data, threat_score, verdict, scanned_at))

    conn.commit()
    conn.close()

# Get all scans
def get_all_scans():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, qr_data, threat_score, verdict, scanned_at
        FROM scans
        ORDER BY id DESC
    """)

    scans = cursor.fetchall()

    conn.close()
    return scans

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

