import os
from pathlib import Path

class SimulationAdapter:
    def __init__(self, base_home_directory):
        self.base_dir = Path(base_home_directory)

    def test_connection(self):
        print("[ADAPTER] Simulation adapter initialized successfully. Local sandbox ready.")
        return True

    def provision_user(self, employee_data, credentials, dry_run=True):
        dept = employee_data["department"]
        username = credentials["username"]
        user_home = self.base_dir / dept / username

        if dry_run:
            print(f"  [DRY-RUN] Would create directory: {user_home}")
            print(f"  [DRY-RUN] Would assign email: {credentials['email']}")
            return {"status": "SUCCESS", "mode": "dry-run", "path": str(user_home)}
        else:
            os.makedirs(user_home, exist_ok=True)
            print(f"  [SIMULATED] Created home directory at: {user_home}")
            return {"status": "SUCCESS", "mode": "executed", "path": str(user_home)}
