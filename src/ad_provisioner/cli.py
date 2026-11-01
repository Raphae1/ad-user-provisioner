import csv
from pathlib import Path
from ad_provisioner.config import load_config
from ad_provisioner.validation import validate_employee_record
from ad_provisioner.identity import generate_username, generate_email, generate_secure_password
from ad_provisioner.adapters.simulation import SimulationAdapter
from ad_provisioner.database import AuditDatabase

def main():
    print("==================================================")
    print("       AD USER PROVISIONER - PHASE 2 (AUDIT)")
    print("==================================================")

    # 1. Load Configuration
    try:
        config = load_config()
    except Exception as e:
        print(f"[ERROR] Configuration failed to load: {e}")
        return

    domain = config.get("company_domain", "corp.local")
    dry_run = config.get("dry_run_default", True)
    allowed_depts = config.get("allowed_departments", [])

    print(f"[*] Loaded Domain: {domain}")
    print(f"[*] Dry-Run Mode: {dry_run}")

    # 2. Initialize Audit Database
    db = AuditDatabase("audit.db")

    # 3. Initialize Adapter
    print("[*] Initializing Simulation Adapter...")
    adapter = SimulationAdapter(config)

    # 4. Process CSV Dataset
    csv_path = Path("samples/employees.example.csv")
    if not csv_path.exists():
        print(f"[ERROR] Sample dataset not found at {csv_path}")
        return

    print(f"[*] Processing employee records from {csv_path}...\n")

    successful_count = 0
    rejected_count = 0

    with open(csv_path, mode="r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row_num, row in enumerate(reader, start=1):
            full_name = f\"{row.get('first_name', '')} {row.get('last_name', '')}\".strip()
            emp_id = row.get('employee_id', 'UNKNOWN')
            dept = row.get('department', '')
            action = row.get('action', 'CREATE')

            print(f\"--------------------------------------------------\")
            print(f\"Processing Row {row_num}: {full_name or 'Unknown'} ({emp_id})\")

            # Validate Record
            is_valid, errors = validate_employee_record(row, allowed_depts)

            if not is_valid:
                print(f\"  [REJECTED] Validation failed for row {row_num}:\")
                for err in errors:
                    print(f\"    - {err}\")
                rejected_count += 1
                
                # Log Rejection to Database
                db.log_event(
                    employee_id=emp_id,
                    full_name=full_name,
                    department=dept,
                    action=action,
                    status=\"REJECTED\",
                    details=\"; \".join(errors)
                )
                continue

            print(f\"  [PASSED] Validation successful.\")

            # Generate Credentials & Identity
            username = generate_username(row['first_name'], row['last_name'], domain)
            email = generate_email(username, domain)
            password = generate_secure_password()

            credentials = {
                \"username\": username,
                \"email\": email,
                \"password\": password
            }

            # Execute Provisioning via Adapter
            result = adapter.provision_user(row, credentials, dry_run=dry_run)
            
            print(f\"  [IDENTITY] Generated Username: {username} | Email: {email}\")
            if dry_run:
                print(f\"  [DRY-RUN] Would create directory: {result['path']}\")
            else:
                print(f\"  [SIMULATED] Created directory at: {result['path']}\")

            successful_count += 1

            # Log Success to Database
            db.log_event(
                employee_id=emp_id,
                full_name=full_name,
                department=dept,
                action=action,
                status=\"SUCCESS\",
                details=f\"Provisioned user {username} at {result['path']}\"
            )

    print(f\"\n==================================================\")
    print(f\" Provisioning Job Complete & Audited.\")
    print(f\" Successful: {successful_count} | Rejected/Failed: {rejected_count}\")
    print(f" [AUDIT] Events successfully committed to audit.db")
    print(f\"==================================================\")

if __name__ == \"__main__\":
    main()
