import pandas as pd
import matplotlib.pyplot as plt
import os
from src.utils.config_loader import load_config

def plot_traffic(log_path="logs/traffic.csv"):
    """
    Generates a graph of traffic trends from the CSV log.
    """
    if not os.path.exists(log_path):
        print(f"Error: Log file not found at {log_path}")
        return

    try:
        df = pd.read_csv(log_path)
        if df.empty:
            print("Log file is empty.")
            return

        df['Timestamp'] = pd.to_datetime(df['Timestamp'])
        
        plt.figure(figsize=(10, 6))
        plt.plot(df['Timestamp'], df['Current_Count'], label='Current Occupancy', color='cyan', linewidth=2)
        plt.fill_between(df['Timestamp'], df['Current_Count'], color='cyan', alpha=0.1)
        
        plt.plot(df['Timestamp'], df['Peak_Count'], label='Peak Count', color='red', linestyle='--', alpha=0.7)
        
        plt.title('People Traffic Analysis - Deep Remaster', fontsize=14, fontweight='bold', color='#333333')
        plt.xlabel('Time', fontsize=12)
        plt.ylabel('People Count', fontsize=12)
        plt.legend()
        plt.grid(True, linestyle=':', alpha=0.6)
        plt.xticks(rotation=45)
        plt.tight_layout()

        output_path = "logs/traffic_analysis.png"
        plt.savefig(output_path)
        print(f"Analysis complete! Graph saved to: {os.path.abspath(output_path)}")
        plt.show()

    except Exception as e:
        print(f"Visualization Error: {e}")

if __name__ == "__main__":
    config = load_config()
    log_file = os.path.join(config['logging']['log_dir'], config['logging']['filename'])
    plot_traffic(log_file)
