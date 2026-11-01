# Active Directory User Provisioning Simulator (\d-user-provisioner\)

An enterprise-grade, modular Identity and Access Management (IAM) automation tool built in Python. This tool securely parses HR input files, validates corporate governance policies, generates standardized identities, and safely executes provisioning workflows via pluggable adapters.

---

## Project Architecture

\\\
ad-user-provisioner/
├── config/
│   └── config.example.json      # Governance policies and domain configurations
├── mock_shares/                 # Local sandbox directory for simulated file shares
├── samples/
│   └── employees.example.csv    # Untrusted raw HR onboarding input dataset
├── src/
│   └── ad_provisioner/
│       ├── adapters/
│       │   └── simulation.py    # Local file-share simulation adapter
│       ├── __init__.py
│       ├── cli.py               # Command-line interface driver
│       ├── config.py            # Configuration loader with UTF-8 BOM handling
│       ├── identity.py          # Cryptographic username and password generator
│       └── validation.py        # Strict security and schema validation engine
├── .gitignore                   # Excludes local shares, caches, and databases
├── requirements.txt             # Project dependencies and testing frameworks
└── README.md                    # Project documentation
\\\

---

## Security & Governance Controls
- **Untrusted Input Validation:** Enforces strict regex validation for employee IDs (\EMP####\), ISO date standards (\YYYY-MM-DD\), and required fields.
- **Department Authorization:** Rejects onboarding attempts for departments outside approved corporate policies.
- **Cryptographic Credentials:** Utilizes Python's \secrets\ module to generate secure temporary passwords containing mixed case letters, numbers, and special symbols.
- **Safe Simulation Sandbox:** Evaluates workflows in dry-run mode to map directory structures without impacting live infrastructure.

---

## Phase 1 Implementation & Test Results

Phase 1 establishes the core simulation and validation pipeline. A test run executing against the sample dataset yielded the following results:
- **Total Records Processed:** 3 (\Sarah Jenkins\, \Marcus Vance\, \Elena Rostova\)
- **Validation Status:** 100% Passed (\Successful: 3 | Rejected/Failed: 0\)
- **Execution Mode:** Local Dry-Run Simulation (Verified sandbox directory mapping under \mock_shares/\)

### Sample Test Output
\\\	ext
[--------------------------------------------------]
Processing Row 1: Sarah Jenkins (EMP1001)
  [PASSED] Validation successful.
  [IDENTITY] Generated Username: sjenkins | Email: sjenkins@corp.local
  [DRY-RUN] Would create directory: mock_shares\\Engineering\\sjenkins
--------------------------------------------------
Provisioning Job Complete.
Successful: 3 | Rejected/Failed: 0
\\\

---

## Quick Start Guide

1. **Clone the repository:**
   \\\ash
   git clone https://github.com/YOUR_USERNAME/ad-user-provisioner.git
   cd ad-user-provisioner
   \\\

2. **Run the simulation CLI:**
   \\\powershell
   \="src"
   python -m ad_provisioner.cli
   \\\
"@ | Out-File -FilePath "README.md" -Encoding utf8
git add .
git commit -m "Complete Phase 1 IAM Provisioning Simulator"
git tag -a v1.0.0 -m "Milestone: Phase 1 complete - modular architecture, validation engine, and simulation adapter verified."
git push -u origin main --tags

@"
import sqlite3
from pathlib import Path
from datetime import datetime

class AuditDatabase:
    def __init__(self, db_path="audit.db"):
        self.db_path = Path(db_path)
        self._initialize_db()

    def _initialize_db(self):
        """Creates the audit logs table if it doesn't already exist."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS audit_logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT NOT NULL,
                    employee_id TEXT,
                    full_name TEXT,
                    department TEXT,
                    action TEXT,
                    status TEXT NOT NULL,
                    details TEXT
                )
            ''')
            conn.commit()

    def log_event(self, employee_id, full_name, department, action, status, details):
        """Records a provisioning event to the SQLite database."""
        timestamp = datetime.utcnow().isoformat()
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO audit_logs (timestamp, employee_id, full_name, department, action, status, details)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (timestamp, employee_id, full_name, department, action, status, details))
            conn.commit()
