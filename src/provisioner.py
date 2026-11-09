import csv
import json
import os
from validator import UserValidator

class ADProvisioner:
    def __init__(self, config_path):
        with open(config_path, 'r', encoding='utf-8-sig') as f:
            self.config = json.load(f)
        self.validator = UserValidator(self.config)

    def process_csv(self, csv_path, dry_run=True):
        print(f"[INFO] Starting user provisioning run (Dry Run: {dry_run})...")
        
        if not os.path.exists(csv_path):
            print(f"[ERROR] CSV file not found: {csv_path}")
            return

        success_count = 0
        error_count = 0

        with open(csv_path, mode='r', encoding='utf-8-sig') as file:
            reader = csv.DictReader(file)
            for row_num, row in enumerate(reader, start=1):
                errors = self.validator.validate_user(row)
                
                if errors:
                    print(f"[ERROR] Row {row_num} validation failed for {row.get('Email', 'Unknown')}:")
                    for err in errors:
                        print(f"  - {err}")
                    error_count += 1
                else:
                    upn = row.get('Email')
                    ou = self.config.get('default_ou')
                    if dry_run:
                        print(f"[DRY-RUN] Would create AD User -> UPN: {upn} | OU: {ou}")
                    else:
                        # Production LDAP connection hook would go here
                        print(f"[PROD] Creating AD User -> UPN: {upn}")
                    success_count += 1

        print(f"[SUMMARY] Processing complete. Success: {success_count} | Errors: {error_count}")


