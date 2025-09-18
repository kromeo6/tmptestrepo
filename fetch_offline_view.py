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

# Connect to Feast store (point to feature_repo directory)
store = FeatureStore(repo_path="./feature_repo")

# Create entity DataFrame with timezone-aware timestamps
# Option 1: Use fixed timestamps (recommended for testing)
entity_df = pd.DataFrame({
    "driver_id": [1, 2, 3],
    "event_timestamp": [
        datetime(2021, 4, 12, 10, 59, 42),
        datetime(2021, 4, 12, 8, 12, 10),
        datetime(2021, 4, 12, 16, 40, 26),
    ]
})

# Option 2: If you need current timestamps, use this instead:
# entity_df = pd.DataFrame({
#     "driver_id": [1, 2, 3], 
#     "event_timestamp": [
#         pd.to_datetime("now", utc=True) - pd.Timedelta(days=1),
#         pd.to_datetime("now", utc=True) - pd.Timedelta(days=2),
#         pd.to_datetime("now", utc=True) - pd.Timedelta(days=3),
#     ]
# })

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