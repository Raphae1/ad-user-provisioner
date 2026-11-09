from pathlib import Path
import os

class SimulationAdapter:
    def __init__(self, config_or_path="./mock_shares"):
        if isinstance(config_or_path, dict):
            # Extract from config dictionary if passed directly
            base_home = config_or_path.get("base_home_directory", "./mock_shares")
            self.base_dir = Path(base_home)
        else:
            self.base_dir = Path(config_or_path)

    def test_connection(self):
        print("[ADAPTER] Simulation adapter initialized successfully. Local sandbox ready.")
        return True

    def provision_user(self, employee_data, credentials, dry_run=True):
        dept = employee_data.get("department", "General")
        username = credentials["username"]
        user_home = self.base_dir / dept / username

        if dry_run:
            return {"status": "SUCCESS", "mode": "dry-run", "path": str(user_home)}
        else:
            os.makedirs(user_home, exist_ok=True)
            return {"status": "SUCCESS", "mode": "executed", "path": str(user_home)}
