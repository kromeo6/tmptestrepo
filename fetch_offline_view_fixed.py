#!/usr/bin/env python3
"""
Fixed version of fetch_offline_view.py that handles timezone-aware timestamps properly.

The original error occurred because Feast expects timezone-aware timestamps for TTL comparisons,
but datetime.now() returns timezone-naive timestamps causing comparison failures.
"""
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

def fetch_with_fixed_timestamps():
    """Approach 1: Use fixed timestamps (recommended for testing)"""
    print("=== APPROACH 1: Fixed Timestamps ===")
    
    entity_df = pd.DataFrame({
        "driver_id": [1, 2, 3],
        "event_timestamp": [
            datetime(2021, 4, 12, 10, 59, 42),
            datetime(2021, 4, 12, 8, 12, 10),
            datetime(2021, 4, 12, 16, 40, 26),
        ]
    })
    
    print("Entity DataFrame:")
    print(entity_df)
    print(f"Timestamp dtype: {entity_df['event_timestamp'].dtype}")
    
    try:
        features = store.get_historical_features(
            entity_df=entity_df,
            features=["driver_stats_minio:conv_rate", "driver_stats_minio:avg_daily_trips"]
        )
        
        result = features.to_df()
        print("\nOffline features:")
        print(result)
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False

def fetch_with_current_timestamps():
    """Approach 2: Use current timezone-aware timestamps"""
    print("\n=== APPROACH 2: Current UTC Timestamps ===")
    
    entity_df = pd.DataFrame({
        "driver_id": [1, 2, 3], 
        "event_timestamp": [
            pd.to_datetime("now", utc=True) - pd.Timedelta(days=1),
            pd.to_datetime("now", utc=True) - pd.Timedelta(days=2),
            pd.to_datetime("now", utc=True) - pd.Timedelta(days=3),
        ]
    })
    
    print("Entity DataFrame:")
    print(entity_df)
    print(f"Timestamp dtype: {entity_df['event_timestamp'].dtype}")
    
    try:
        features = store.get_historical_features(
            entity_df=entity_df,
            features=["driver_stats_minio:conv_rate", "driver_stats_minio:avg_daily_trips"]
        )
        
        result = features.to_df()
        print("\nOffline features:")
        print(result)
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False

def fetch_with_localized_timestamps():
    """Approach 3: Manually localize timezone-naive timestamps"""
    print("\n=== APPROACH 3: Localized Timestamps ===")
    
    # Create timezone-naive timestamps first
    naive_timestamps = [
        datetime.now() - timedelta(days=1),
        datetime.now() - timedelta(days=2),
        datetime.now() - timedelta(days=3),
    ]
    
    # Convert to timezone-aware timestamps
    entity_df = pd.DataFrame({
        "driver_id": [1, 2, 3],
        "event_timestamp": pd.to_datetime(naive_timestamps, utc=True)
    })
    
    print("Entity DataFrame:")
    print(entity_df)
    print(f"Timestamp dtype: {entity_df['event_timestamp'].dtype}")
    
    try:
        features = store.get_historical_features(
            entity_df=entity_df,
            features=["driver_stats_minio:conv_rate", "driver_stats_minio:avg_daily_trips"]
        )
        
        result = features.to_df()
        print("\nOffline features:")
        print(result)
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False

if __name__ == "__main__":
    print("Testing different approaches to fix datetime comparison issues in Feast...")
    
    # Try each approach
    success1 = fetch_with_fixed_timestamps()
    success2 = fetch_with_current_timestamps() 
    success3 = fetch_with_localized_timestamps()
    
    print(f"\n=== RESULTS ===")
    print(f"Fixed timestamps: {'✓' if success1 else '✗'}")
    print(f"Current UTC timestamps: {'✓' if success2 else '✗'}")
    print(f"Localized timestamps: {'✓' if success3 else '✗'}") 