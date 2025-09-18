#!/usr/bin/env python3
"""
Debug script to inspect the actual data in MinIO bucket
to understand the timestamp format causing comparison issues.
"""
import os
import pandas as pd
import s3fs
from datetime import datetime

# MinIO configuration
os.environ.update({
    "AWS_ACCESS_KEY_ID": "minio",
    "AWS_SECRET_ACCESS_KEY": "minio123",
    "FEAST_S3_ENDPOINT_URL": "http://localhost:9001"
})

def inspect_minio_data():
    """Inspect the actual data stored in MinIO"""
    print("🔍 INSPECTING MINIO DATA STRUCTURE")
    print("=" * 50)
    
    # Create S3 filesystem
    s3 = s3fs.S3FileSystem(
        key='minio',
        secret='minio123',
        client_kwargs={'endpoint_url': 'http://localhost:9001'},
        use_ssl=False
    )
    
    try:
        # List files in bucket
        print("1. Listing files in test-bucket:")
        files = s3.ls('test-bucket/')
        for file in files:
            print(f"   - {file}")
        
        # Read the parquet file directly
        print("\n2. Reading driver_stats.parquet directly:")
        if 'test-bucket/driver_stats.parquet' in files:
            # Read with s3fs
            with s3.open('test-bucket/driver_stats.parquet', 'rb') as f:
                df = pd.read_parquet(f)
            
            print(f"   Shape: {df.shape}")
            print(f"   Columns: {list(df.columns)}")
            print("\n   Data types:")
            for col, dtype in df.dtypes.items():
                print(f"      {col}: {dtype}")
            
            print("\n   First few rows:")
            print(df.head())
            
            # Check timestamp columns specifically
            if 'event_timestamp' in df.columns:
                print(f"\n3. Event timestamp analysis:")
                print(f"   Type: {type(df['event_timestamp'].iloc[0])}")
                print(f"   Dtype: {df['event_timestamp'].dtype}")
                print(f"   Sample values:")
                for i, ts in enumerate(df['event_timestamp'].head(3)):
                    print(f"      [{i}] {ts} (type: {type(ts)})")
                
                # Check timezone info
                if hasattr(df['event_timestamp'].dtype, 'tz'):
                    print(f"   Timezone: {df['event_timestamp'].dtype.tz}")
                else:
                    print("   Timezone: None (timezone-naive)")
            
            if 'created' in df.columns:
                print(f"\n4. Created timestamp analysis:")
                print(f"   Type: {type(df['created'].iloc[0])}")
                print(f"   Dtype: {df['created'].dtype}")
                print(f"   Sample values:")
                for i, ts in enumerate(df['created'].head(3)):
                    print(f"      [{i}] {ts} (type: {type(ts)})")
                
                # Check timezone info
                if hasattr(df['created'].dtype, 'tz'):
                    print(f"   Timezone: {df['created'].dtype.tz}")
                else:
                    print("   Timezone: None (timezone-naive)")
        else:
            print("   ❌ driver_stats.parquet not found!")
            
    except Exception as e:
        print(f"   ❌ Error reading data: {e}")
        import traceback
        traceback.print_exc()

def test_timestamp_comparisons():
    """Test different timestamp formats for comparison"""
    print("\n" + "=" * 50)
    print("🧪 TESTING TIMESTAMP COMPARISONS")
    print("=" * 50)
    
    # Test different timestamp formats
    test_timestamps = [
        ("Timezone-naive datetime", datetime(2021, 4, 12, 10, 59, 42)),
        ("Timezone-aware UTC", pd.to_datetime("2021-04-12 10:59:42", utc=True)),
        ("Current UTC", pd.to_datetime("now", utc=True)),
        ("Pandas timestamp", pd.Timestamp("2021-04-12 10:59:42")),
        ("Pandas timestamp UTC", pd.Timestamp("2021-04-12 10:59:42", tz='UTC')),
    ]
    
    for name, ts in test_timestamps:
        print(f"\n{name}:")
        print(f"   Value: {ts}")
        print(f"   Type: {type(ts)}")
        print(f"   Dtype: {ts if hasattr(ts, 'dtype') else 'N/A'}")
        if hasattr(ts, 'tz'):
            print(f"   Timezone: {ts.tz}")
        elif hasattr(ts, 'tzinfo'):
            print(f"   Timezone: {ts.tzinfo}")

if __name__ == "__main__":
    inspect_minio_data()
    test_timestamp_comparisons() 