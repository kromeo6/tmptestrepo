#!/usr/bin/env python3
"""
Fix California housing data to have same timestamp for all records
so Feast can fetch all data in one query.
"""
import boto3
import pandas as pd
from io import BytesIO
from datetime import datetime

def fix_california_timestamps():
    print("🔧 FIXING CALIFORNIA HOUSING TIMESTAMPS")
    print("=" * 50)
    
    # MinIO configuration
    s3_client = boto3.client(
        's3',
        endpoint_url="http://localhost:9001",
        aws_access_key_id="minio",
        aws_secret_access_key="minio123",
        region_name='us-east-1'
    )
    
    # Read existing data
    bucket_name = "test-bucket"
    key = "feast/data/california_data.parquet"
    
    print("📖 Reading existing data...")
    response = s3_client.get_object(Bucket=bucket_name, Key=key)
    df = pd.read_parquet(BytesIO(response['Body'].read()))
    
    print(f"Original data shape: {df.shape}")
    print(f"Original timestamp range: {df['event_timestamp'].min()} to {df['event_timestamp'].max()}")
    
    # Fix the data:
    # 1. Set all timestamps to the same value
    # 2. Reset house_id to be sequential 0, 1, 2, etc.
    
    fixed_timestamp = datetime(2020, 1, 15, 12, 0, 0)  # Single timestamp for all
    
    df['house_id'] = range(len(df))  # 0, 1, 2, 3, ... 599
    df['event_timestamp'] = fixed_timestamp
    df['created'] = fixed_timestamp
    
    print(f"\n✅ Fixed data:")
    print(f"   Shape: {df.shape}")
    print(f"   house_id range: {df['house_id'].min()} - {df['house_id'].max()}")
    print(f"   All timestamps: {df['event_timestamp'].iloc[0]}")
    print(f"   Unique timestamps: {df['event_timestamp'].nunique()}")
    
    # Upload fixed data
    print("\n💾 Converting to parquet...")
    parquet_buffer = BytesIO()
    df.to_parquet(parquet_buffer, index=False)
    parquet_buffer.seek(0)
    
    print("⬆️  Uploading fixed data to MinIO...")
    s3_client.put_object(
        Bucket=bucket_name,
        Key=key,
        Body=parquet_buffer.getvalue(),
        ContentType='application/octet-stream'
    )
    
    print("✅ Successfully uploaded fixed California housing data!")
    print(f"   - All 600 records have the same timestamp: {fixed_timestamp}")
    print(f"   - house_id now ranges from 0 to 599")
    print("   - Now Feast should fetch all records when queried!")

if __name__ == "__main__":
    fix_california_timestamps() 