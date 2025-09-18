#!/usr/bin/env python3
"""
Analyze the uploaded California housing data to understand its structure
"""
import boto3
import pandas as pd
from io import BytesIO

def analyze_california_data():
    print("🔍 ANALYZING CALIFORNIA HOUSING DATA")
    print("=" * 50)
    
    # MinIO configuration
    s3_client = boto3.client(
        's3',
        endpoint_url="http://localhost:9001",
        aws_access_key_id="minio",
        aws_secret_access_key="minio123",
        region_name='us-east-1'
    )
    
    # Read the data from MinIO
    print("📖 Reading california_data.parquet from MinIO...")
    bucket_name = "test-bucket"
    key = "feast/data/california_data.parquet"
    
    try:
        response = s3_client.get_object(Bucket=bucket_name, Key=key)
        df = pd.read_parquet(BytesIO(response['Body'].read()))
        
        print(f"✅ Successfully read data!")
        print(f"   Shape: {df.shape}")
        print(f"   Columns: {list(df.columns)}")
        
        print("\n📊 Data Types:")
        for col, dtype in df.dtypes.items():
            print(f"   {col}: {dtype}")
        
        print("\n📈 Statistical Summary:")
        print(df.describe())
        
        print("\n🕐 Timestamp Analysis:")
        print(f"   event_timestamp range: {df['event_timestamp'].min()} to {df['event_timestamp'].max()}")
        print(f"   created range: {df['created'].min()} to {df['created'].max()}")
        
        print("\n🏠 Sample Data:")
        print(df.head())
        
        print("\n🎯 Target Analysis:")
        print(f"   Target range: ${df['target'].min():,.2f} - ${df['target'].max():,.2f}")
        print(f"   Target mean: ${df['target'].mean():,.2f}")
        
        print("\n🗂️ Entity Analysis:")
        print(f"   house_id range: {df['house_id'].min()} - {df['house_id'].max()}")
        print(f"   Unique house_ids: {df['house_id'].nunique()}")
        
        return df
        
    except Exception as e:
        print(f"❌ Error reading data: {e}")
        return None

if __name__ == "__main__":
    df = analyze_california_data() 