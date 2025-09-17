#!/usr/bin/env python3
import os
import pandas as pd
from datetime import datetime, timedelta
from feast import FeatureStore

# Set MinIO credentials for local access
os.environ.update({
    "AWS_ACCESS_KEY_ID": "minio",
    "AWS_SECRET_ACCESS_KEY": "minio123",
    "FEAST_S3_ENDPOINT_URL": "http://localhost:9001"
})

# Connect to Feast store
store = FeatureStore(repo_path=".")

# Create entity DataFrame
entity_df = pd.DataFrame({
    "driver_id": [1, 2, 3],
    "event_timestamp": [
        datetime.now() - timedelta(days=1),
        datetime.now() - timedelta(days=2),  
        datetime.now() - timedelta(days=3),
    ]
})

print("Fetching offline features using Feast offline store...")
print(entity_df)

# Use Feast offline store properly
features = store.get_historical_features(
    entity_df=entity_df,
    features=["driver_stats_minio:conv_rate", "driver_stats_minio:avg_daily_trips"]
)

result = features.to_df()
print("\nOffline features:")
print(result)