import json
from pathlib import Path

def load_config(config_path="config/config.example.json"):
    path = Path(config_path)
    if not path.exists():
        raise FileNotFoundError(f"Configuration file not found at {path}")
    
    # Use 'utf-8-sig' to automatically strip out any Windows BOM artifacts
    with open(path, "r", encoding="utf-8-sig") as f:
        config = json.load(f)
    return config