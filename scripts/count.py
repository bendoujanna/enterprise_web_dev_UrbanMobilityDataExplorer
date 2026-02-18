import pandas as pd
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
log_path = os.path.join('output', 'suspicious_records.log')

try:
    print(f"Reading log file from: {log_path}...")

    # Read the log file
    log_df = pd.read_csv(log_path)

    # Count the occurrences of each specific reason
    counts = log_df['rejection_reason'].value_counts()

    print(f"\n--- Data Quality Report (Real-Time) ---")
