import pandas as pd
import os
import sqlite3
import numpy as np

# Configuration
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(BASE_DIR)
DB_PATH = os.path.join(PROJECT_ROOT, "database.db")
TRIPS_FILE = os.path.join(PROJECT_ROOT, 'data', 'yellow_tripdata_2019-01.parquet')
# TRIPS_FILE = os.path.join(PROJECT_ROOT, 'data', 'yellow_tripdata_2019-01.csv')
ZONE_FILE = os.path.join(PROJECT_ROOT, 'data', 'taxi_zone_lookup.csv')
TRIPS_FILE = os.path.join(PROJECT_ROOT, 'data', 'yellow_tripdata_2019-01.parquet')
LOG_DIR = os.path.join(PROJECT_ROOT, 'output')
LOG_FILE = os.path.join(LOG_DIR, 'suspicious_records.log')


def run_pipeline():
    print(f"Starting ETL Pipeline...")
    print(f"Database Path: {DB_PATH}")

    # Ensure output directory exists
    if not os.path.exists(LOG_DIR):
        os.makedirs(LOG_DIR)

    conn = sqlite3.connect(DB_PATH)

    # 1. Load Zones
    valid_zones = set()
    try:
        print("Loading zones...")
        if os.path.exists(ZONE_FILE):
            zones_df = pd.read_csv(ZONE_FILE)
            # Create zones table if it doesn't exist
            zones_df.to_sql('zones', conn, if_exists='replace', index=False)
            valid_zones = set(zones_df['LocationID'].unique())
            print(f"Loaded {len(zones_df)} zones.")
        else:
            print(f"Warning: Zone file not found at {ZONE_FILE}. Skipping zone validation.")
    except Exception as e:
        print(f"Zone Error: {e}")
  
   # 2. Process Trips
    print("Processing Data...")
    try:
        # Load Data (Adjust for CSV or Parquet)
        if TRIPS_FILE.endswith('.parquet'):
            df = pd.read_parquet(TRIPS_FILE)
        else:
            df = pd.read_csv(TRIPS_FILE)

        # Precalculations
        df['tpep_pickup_datetime'] = pd.to_datetime(df['tpep_pickup_datetime'])
        df['tpep_dropoff_datetime'] = pd.to_datetime(df['tpep_dropoff_datetime'])

        # Calculate Duration (Seconds)
        df['trip_duration_seconds'] = (df['tpep_dropoff_datetime'] - df['tpep_pickup_datetime']).dt.total_seconds()

        # Calculate Speed (MPH)
        # Handle division by zero using numpy to avoid crash, then fill NA
        df['speed_mph'] = (df['trip_distance'] / (df['trip_duration_seconds'] / 3600))
        df['speed_mph'] = df['speed_mph'].replace([np.inf, -np.inf], 0).fillna(0)
        df['average_speed_mph'] = df['speed_mph']
