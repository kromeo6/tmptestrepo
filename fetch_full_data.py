#!/usr/bin/env python3
"""
Minimalist script to fetch entire DataFrame from MinIO using the full_data view.
"""
import os
import pandas as pd
from datetime import datetime
from feast import FeatureStore

# Set MinIO credentials
os.environ.update({
    "AWS_ACCESS_KEY_ID": "minio",
    "AWS_SECRET_ACCESS_KEY": "minio123",
    "FEAST_S3_ENDPOINT_URL": "http://localhost:9001"
})

# Connect to Feast store
store = FeatureStore(repo_path="./feature_repo")

# Create a simple entity DataFrame with a wide time range
entity_df = pd.DataFrame({
    "driver_id": [1, 2, 3, 4, 5],  # Include more driver IDs
    "event_timestamp": [
        datetime(2020, 1, 1),      # Very old date to catch all data
        datetime(2021, 6, 15),
        datetime(2022, 12, 31),
        datetime(2023, 6, 1),
        datetime(2024, 1, 1),      # Recent date
    ]
})

print("Fetching all data from full_data view...")
print("Entity DataFrame:")
print(entity_df)

# Fetch using the minimalist view (let Feast auto-detect features)
features = store.get_historical_features(
    entity_df=entity_df,
    features=["full_data"]  # Just specify the view name
)

result = features.to_df()
print(f"\nResult shape: {result.shape}")
print("\nFull data:")
print(result) 