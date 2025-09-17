#!/usr/bin/env python3
"""
Test script to retrieve features from Kubernetes-deployed Feast via port-forwarding.
"""

import os
import sys
from datetime import datetime, timedelta
import pandas as pd
from feast import FeatureStore

os.environ.update({
    "AWS_ACCESS_KEY_ID": "minio",
    "AWS_SECRET_ACCESS_KEY": "minio123",
    "AWS_DEFAULT_REGION": "us-east-1",
    "FEAST_S3_ENDPOINT_URL": "http://localhost:9001"
})

def test_k8s_remote_features():
    """Test retrieving features from Kubernetes-deployed Feast via port-forwarding."""
    print("🧪 Testing Remote Feast Feature Retrieval from K8s")
    print("=" * 55)
    
    try:
        print("1. Connecting to port-forwarded Feast services...")
        store = FeatureStore(repo_path=".")
        print("✅ Connected to remote Feast feature store")
        
        print("\n2. Listing available feature views...")
        feature_views = store.list_feature_views()
        for fv in feature_views:
            print(f"   - {fv.name}: {fv.description}")
        
        if not feature_views:
            raise Exception("No feature views found.")
        
        print("\n3. Creating test entity DataFrame...")
        entity_df = pd.DataFrame({
            "driver_id": [1, 2, 3, 4, 5],
            "event_timestamp": [
                datetime.now() - timedelta(days=1),
                datetime.now() - timedelta(days=2),
                datetime.now() - timedelta(days=3),
                datetime.now() - timedelta(days=4),
                datetime.now() - timedelta(days=5),
            ]
        })
        
        print("Entity DataFrame:")
        print(entity_df)
        
        print("\n4. Retrieving historical features from K8s MinIO...")
        feature_vector = store.get_historical_features(
            entity_df=entity_df,
            features=[
                "driver_stats_minio:conv_rate",
                "driver_stats_minio:avg_daily_trips"
            ]
        )
        
        historical_df = feature_vector.to_df()
        print("✅ Successfully retrieved historical features from K8s!")
        print("\nHistorical features:")
        print(historical_df)
        
        print("\n5. Testing online feature retrieval...")
        online_features = store.get_online_features(
            features=[
                "driver_stats_minio:conv_rate",
                "driver_stats_minio:avg_daily_trips"
            ],
            entity_rows=[
                {"driver_id": 1},
                {"driver_id": 2},
                {"driver_id": 3}
            ]
        )
        
        online_df = online_features.to_df()
        print("✅ Successfully retrieved online features from K8s!")
        print("\nOnline features:")
        print(online_df)
        
        print("\n" + "=" * 55)
        print("🎉 SUCCESS: K8s Remote MinIO Integration Works!")
        
        return True
        
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("Make sure you have port-forwarding active...")
    print("")
    
    success = test_k8s_remote_features()
    
    if success:
        print("\n✅ All tests passed!")
        sys.exit(0)
    else:
        print("\n❌ Tests failed!")
        sys.exit(1) 