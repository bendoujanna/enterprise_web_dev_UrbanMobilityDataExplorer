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
