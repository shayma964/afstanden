# -*- coding: utf-8 -*-
"""
Created on Wed Mar 11 15:10:01 2026

@author: Gebruiker
"""

import pandas as pd
from geopy.distance import geodesic
import numpy as np

df = pd.read_excel("D:/data_folders/work/Mobility/work_woon.xlsx", 
                   dtype={"UGent ID": str})

df.columns = df.columns.str.strip()

def calc_distance(row):
    # Check if ID is missing
    if pd.isna(row['UGent ID']):
        print("Warning: Row with missing ID found, skipping...")
        return None
    
    # Check if coordinates are missing
    try:
        # Check for NaN values in coordinates
        if pd.isna(row['lat_1']) or pd.isna(row['long_1']) or pd.isna(row['lat_2']) or pd.isna(row['long_2']):
            print(f"Warning: Missing coordinates for ID {row['UGent ID']}")
            return None
            
        point1 = (row['lat_1'], row['long_1'])
        point2 = (row['lat_2'], row['long_2'])
        return geodesic(point1, point2).km
        
    except Exception as e:
        print(f"Error calculating distance for ID {row.get('UGent ID', 'Unknown')}: {e}")
        return None

# Apply with better error handling
df['distance_km'] = df.apply(calc_distance, axis=1)

# Check how many missing values you have
print(f"Total rows: {len(df)}")
print(f"Rows with missing ID: {df['UGent ID'].isna().sum()}")
print(f"Rows with missing distance: {df['distance_km'].isna().sum()}")

# Save results
df.to_excel("D:/data_folders/work/Mobility/distance_results.xlsx", index=False)