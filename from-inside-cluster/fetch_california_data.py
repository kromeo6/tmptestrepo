#!/usr/bin/env python3
"""
Fetch entire California housing dataset using the california_housing feature view.
UPDATED FOR KUBERNETES: Uses cluster-internal service names.
"""
import os
import pandas as pd
from datetime import datetime
from feast import FeatureStore

# Set MinIO credentials for cluster access
os.environ.update({
    "AWS_ACCESS_KEY_ID": "minio",
    "AWS_SECRET_ACCESS_KEY": "minio123",
    "FEAST_S3_ENDPOINT_URL": "http://minio-service.kubeflow.svc.cluster.local:9000"  # Cross-namespace service
})

# Connect to Feast store
store = FeatureStore(repo_path="./feature_repo")

def fetch_california_housing_data():
    print("🏠 FETCHING ALL CALIFORNIA HOUSING DATA FROM KUBERNETES POD")
    print("=" * 60)
    
    # Create entity DataFrame with all house IDs and the fixed timestamp
    # All records now have the same timestamp: 2020-01-15 12:00:00
    entity_df = pd.DataFrame({
        "house_id": list(range(600)),  # All house IDs: 0, 1, 2, ..., 599
        "event_timestamp": [datetime(2020, 1, 15, 12, 0, 0)] * 600  # Same timestamp for all
    })
    
    print(f"📋 Entity DataFrame shape: {entity_df.shape}")
    print(f"🏠 House ID range: {entity_df['house_id'].min()} - {entity_df['house_id'].max()}")
    print(f"🕐 Timestamp: {entity_df['event_timestamp'].iloc[0]} (same for all records)")
    print(f"🔧 MinIO Endpoint: {os.environ.get('FEAST_S3_ENDPOINT_URL')}")
    
    # Fetch all California housing features
    features = [
        "california_housing:MedInc",
        "california_housing:HouseAge", 
        "california_housing:AveRooms",
        "california_housing:AveBedrms",
        "california_housing:Population",
        "california_housing:AveOccup",
        "california_housing:Latitude",
        "california_housing:Longitude",
        "california_housing:target"
    ]
    
    print(f"\n🔍 Requesting features: {len(features)} features")
    
    try:
        print("\n⏳ Fetching historical features from Kubernetes pod...")
        historical_features = store.get_historical_features(
            entity_df=entity_df,
            features=features
        )
        
        result = historical_features.to_df()
        
        print("✅ Successfully fetched California housing data from pod!")
        print(f"\n📊 Result shape: {result.shape}")
        print(f"📋 Columns: {list(result.columns)}")
        
        # Display sample data
        print("\n🏠 Sample California housing data (first 5 records):")
        print(result.head(5))
        
        # Show statistics
        if len(result) > 0:
            print(f"\n📈 Data Statistics:")
            print(f"   - Total records: {len(result)}")
            print(f"   - House ID range: {result['house_id'].min()} - {result['house_id'].max()}")
            print(f"   - Unique house IDs: {result['house_id'].nunique()}")
            
            if 'target' in result.columns:
                print(f"   - House value range: ${result['target'].min():,.2f} - ${result['target'].max():,.2f}")
                print(f"   - Average house value: ${result['target'].mean():,.2f}")
                print(f"   - Median house value: ${result['target'].median():,.2f}")
            
            # Check for any missing data
            missing_data = result.isnull().sum()
            if missing_data.sum() > 0:
                print(f"\n⚠️  Missing data found:")
                for col, missing in missing_data.items():
                    if missing > 0:
                        print(f"   - {col}: {missing} missing values")
            else:
                print("\n✅ No missing data found!")
                
            print(f"\n🎉 SUCCESS: Fetched complete dataset with {len(result)} records from Kubernetes pod!")
        else:
            print("\n⚠️  No data returned - check TTL settings and timestamp ranges")
            
        return result
        
    except Exception as e:
        print(f"\n❌ Error fetching data: {e}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    result = fetch_california_housing_data()
 