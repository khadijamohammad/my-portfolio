import json
import os
from datetime import datetime

class ReportGenerator:
    """Manages secure saving and retrieval of structured JSON scan logs."""
    def __init__(self, filename="scan_history.json"):
        self.filename = filename

    def save_report(self, analyst, score, threat_level, findings):
        """Saves scan execution metadata to the structured database."""
        report_data = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "analyst": analyst,
            "score": score,
            "threat": threat_level,
            "findings": findings
        }

        history = []
        if os.path.exists(self.filename):
            try:
                with open(self.filename, "r", encoding="utf-8") as f:
                    history = json.load(f)
            except (json.JSONDecodeError, FileNotFoundError):
                # Fallback if file is corrupted or empty
                history = []

        history.append(report_data)

        with open(self.filename, "w", encoding="utf-8") as f:
            json.dump(history, f, indent=4)