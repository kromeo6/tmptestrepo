#!/usr/bin/env python3
"""
Create sample California housing data for testing
"""
import boto3
import pandas as pd
import numpy as np
from io import BytesIO
from datetime import datetime, timedelta
from botocore.client import Config

def create_sample_data():
    print("📊 Creating sample California housing data...")
    
    # Generate sample data (600 records like California housing dataset)
    np.random.seed(42)
    n_samples = 600
    
    data = {
        'house_id': range(n_samples),
        'longitude': np.random.uniform(-124.3, -114.3, n_samples),
        'latitude': np.random.uniform(32.5, 42.0, n_samples),
        'housing_median_age': np.random.uniform(1, 52, n_samples),
        'total_rooms': np.random.uniform(100, 5000, n_samples),
        'total_bedrooms': np.random.uniform(20, 1000, n_samples),
        'population': np.random.uniform(100, 8000, n_samples),
        'households': np.random.uniform(50, 2000, n_samples),
        'median_income': np.random.uniform(0.5, 15.0, n_samples),
        'median_house_value': np.random.uniform(15000, 500000, n_samples),
    }
    
    # Add timestamps - initially different for each record
    base_time = datetime(2020, 1, 1)
    data['event_timestamp'] = [base_time + timedelta(days=i) for i in range(n_samples)]
    data['created'] = [base_time + timedelta(days=i) for i in range(n_samples)]
    
    df = pd.DataFrame(data)
    
    print(f"✅ Generated {len(df)} sample records")
    print(f"   house_id range: {df['house_id'].min()} - {df['house_id'].max()}")
    print(f"   Timestamp range: {df['event_timestamp'].min()} to {df['event_timestamp'].max()}")
    
    # Upload to MinIO
    print("\n💾 Converting to parquet...")
    parquet_buffer = BytesIO()
    df.to_parquet(parquet_buffer, index=False)
    parquet_buffer.seek(0)
    
    # MinIO configuration
    s3_client = boto3.client(
        's3',
        endpoint_url="http://localhost:9001",
        aws_access_key_id="minio",
        aws_secret_access_key="minio123",
        config=Config(signature_version='s3v4'),
        region_name='us-east-1'
    )
    
    bucket_name = "test-bucket"
    key = "feast/data/california_data.parquet"
    
    print("⬆️  Uploading to MinIO...")
    s3_client.put_object(
        Bucket=bucket_name,
        Key=key,
        Body=parquet_buffer.getvalue(),
        ContentType='application/octet-stream'
    )
    
    print("✅ Successfully uploaded sample California housing data!")
    print(f"   Location: s3://{bucket_name}/{key}")
    print(f"   Records: {len(df)}")
    
    return True

if __name__ == "__main__":
    create_sample_data() 