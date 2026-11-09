import sqlite3
from datetime import datetime
from pathlib import Path

class AuditDatabase:
    def __init__(self, db_path="audit.db"):
        self.db_path = db_path
        self._initialize_db()

    def _initialize_db(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS audit_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                employee_id TEXT,
                full_name TEXT,
                department TEXT,
                action TEXT,
                status TEXT,
                details TEXT
            )
        """)
        conn.commit()
        conn.close()

    def log_event(self, employee_id, full_name, department, action, status, details):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        timestamp = datetime.utcnow().isoformat()
        cursor.execute("""
            INSERT INTO audit_logs (timestamp, employee_id, full_name, department, action, status, details)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (timestamp, employee_id, full_name, department, action, status, details))
        conn.commit()
        conn.close()
