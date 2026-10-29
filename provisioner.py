import csv
import json
import os
import sqlite3
import random
import string
from pathlib import Path
from datetime import datetime

DB_NAME = "onboarding_audit.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS audit_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            username TEXT,
            email TEXT,
            department TEXT,
            role TEXT,
            status TEXT
        )
    ''')
    conn.commit()
    conn.close()

def log_provisioning(username, email, department, role, status):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO audit_log (timestamp, username, email, department, role, status)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (datetime.now().isoformat(), username, email, department, role, status))
    conn.commit()
    conn.close()

def generate_username(first, last, format_type):
    clean_first = first.lower().strip()
    clean_last = last.lower().strip()
    if format_type == "first_initial + last_name":
        return f"{clean_first[0]}{clean_last}"
    return f"{clean_first}.{clean_last}"

def generate_temp_password():
    alphabet = string.ascii_letters + string.digits + "!@#$"
    return ''.join(random.choice(alphabet) for i in range(12))

def process_onboarding():
    init_db()
    
    # Load Configuration
    with open("config.json", "r") as f:
        config = json.load(f)
        
    domain = config["company_domain"]
    naming_convention = config["username_format"]
    base_dir = Path(config["base_home_directory"])
    
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Starting User Provisioning Job...")
    
    # Read CSV
    try:
        with open("employees.csv", mode="r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                first = row["first_name"]
                last = row["last_name"]
                dept = row["department"]
                role = row["role"]
                
                username = generate_username(first, last, naming_convention)
                email = f"{username}@{domain}"
                temp_pwd = generate_temp_password()
                
                # Create simulated home directory structure
                user_home = base_dir / dept / username
                os.makedirs(user_home, exist_ok=True)
                
                # Log to database
                log_provisioning(username, email, dept, role, "SUCCESS")
                
                print(f"  [CREATED] User: {username} | Email: {email} | Dept: {dept} | Home Folder: {user_home}")
                
        print("\nProvisioning completed successfully! Audit logs written to SQLite database.")
        
    except Exception as e:
        print(f"  [ERROR] Failed to process onboarding CSV: {e}")

if __name__ == "__main__":
    process_onboarding()