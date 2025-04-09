# data_handler.py

import pandas as pd
import json
import os
from config import SETTINGS_FILE, DATA_FILE

def load_settings():
    if os.path.exists(SETTINGS_FILE):
        with open(SETTINGS_FILE, "r") as file:
            return json.load(file)
    return {"vehicles": [], "circuits": [], "employees": [], "zones": {}, "salary": 0, "bonus_per_trip": 0}

def save_settings(settings):
    with open(SETTINGS_FILE, "w") as file:
        json.dump(settings, file)

def load_data():
    if os.path.exists(DATA_FILE):
        return pd.read_csv(DATA_FILE)
    return pd.DataFrame(columns=[
        'Date', 'Vehicle', 'Circuit', 'Trips', 'Start_Time', 'End_Time', 'Duration_Minutes',
        'Distance', 'Fuel_Consumption', 'Load_Tons', 'Receipt_No'
    ])

def save_data(data):
    data.to_csv(DATA_FILE, index=False)
