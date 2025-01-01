import json
import os

def load_config(path="config.json"):
    """
    Loads configuration from a JSON file.
    """
    default_config = {
        "detection": {"min_confidence": 0.4, "model_complexity": 1},
        "audio": {"enabled": true, "slow": false},
        "ui": {
            "hud_color": [0, 255, 255],
            "text_color": [255, 255, 255],
            "stats_color": [0, 255, 0],
            "peak_color": [0, 0, 255],
            "alpha": 0.6
        },
        "logging": {
            "enabled": true,
            "interval_seconds": 5,
            "log_dir": "logs",
            "filename": "traffic.csv"
        }
    }
    
    if os.path.exists(path):
        try:
            with open(path, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading config: {e}. Using defaults.")
            
    return default_config
