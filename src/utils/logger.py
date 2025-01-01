import csv
import os
from datetime import datetime

class TrafficLogger:
    def __init__(self, log_dir="logs", filename="traffic.csv"):
        """
        Initializes the traffic logger.
        """
        self.log_path = os.path.join(log_dir, filename)
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
            
        # Initialize CSV with headers if it doesn't exist
        if not os.path.exists(self.log_path):
            with open(self.log_path, mode='w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(["Timestamp", "Session_Total", "Current_Count", "Peak_Count"])

    def log_event(self, session_total, current_count, peak_count):
        """
        Logs a detection event to the CSV file.
        """
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(self.log_path, mode='a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([timestamp, session_total, current_count, peak_count])

    def get_log_path(self):
        return os.path.abspath(self.log_path)
