#!/usr/bin/env python3
import boto3
import pandas as pd
import numpy as np
from io import BytesIO
import tensorflow.keras as keras

def upload_california_data_to_minio():
    print("🚀 Loading California housing data and uploading to MinIO...")
    
    # Load California housing dataset from Keras
    print("📊 Loading California housing dataset from Keras...")
    (x_train, y_train), (x_test, y_test) = keras.datasets.california_housing.load_data(
        version="small", 
        path="california_housing.npz", 
        test_split=0.2, 
        seed=109
    )
    
    print(f"✅ Loaded training data: {x_train.shape}, target: {y_train.shape}")
    print(f"✅ Loaded test data: {x_test.shape}, target: {y_test.shape}")
    
    # Combine train and test data
    print("🔄 Combining train and test data...")
    x_all = np.vstack([x_train, x_test])
    y_all = np.hstack([y_train, y_test])
    
    # Create feature names (California housing has 8 features)
    feature_names = [
        'MedInc',        # Median income in block group
        'HouseAge',      # Median house age in block group  
        'AveRooms',      # Average number of rooms per household
        'AveBedrms',     # Average number of bedrooms per household
        'Population',    # Block group population
        'AveOccup',      # Average number of household members
        'Latitude',      # Block group latitude
        'Longitude'      # Block group longitude
    ]
    
    # Convert to pandas DataFrame
    print("📋 Converting to pandas DataFrame...")
    df = pd.DataFrame(x_all, columns=feature_names)
    df['target'] = y_all  # Add target column (median house value)
    
    # Add some required columns for Feast
    df['house_id'] = range(len(df))  # Entity column
    df['event_timestamp'] = pd.date_range('2020-01-01', periods=len(df), freq='H')
    df['created'] = pd.date_range('2020-01-01', periods=len(df), freq='H')
    
    print(f"✅ Created DataFrame with {len(df)} rows, {len(df.columns)} columns")
    print("📋 Columns:", list(df.columns))
    print("\n📊 First few rows:")
    print(df.head())
    
    # MinIO configuration
    print("\n🔧 Configuring MinIO client...")
    s3_client = boto3.client(
        's3',
        endpoint_url="http://localhost:9001",
        aws_access_key_id="minio",
        aws_secret_access_key="minio123",
        region_name='us-east-1'
    )
    
    # Convert to parquet bytes
    print("💾 Converting to parquet bytes...")
    parquet_buffer = BytesIO()
    df.to_parquet(parquet_buffer, index=False)
    parquet_buffer.seek(0)
    
    # Upload to MinIO
    bucket_name = "test-bucket"
    key = "feast/data/california_data.parquet"
    
    print(f"⬆️  Uploading to s3://{bucket_name}/{key}")
    s3_client.put_object(
        Bucket=bucket_name,
        Key=key,
        Body=parquet_buffer.getvalue(),
        ContentType='application/octet-stream'
    )
    
    print("✅ Upload successful!")
    
    # Verify the upload
    print("🔍 Verifying upload...")
    response = s3_client.head_object(Bucket=bucket_name, Key=key)
    size = response['ContentLength']
    print(f"✅ File uploaded successfully! Size: {size} bytes")
    
    # Show data info
    print(f"\n📈 Dataset summary:")
    print(f"   - Total samples: {len(df)}")
    print(f"   - Features: {len(feature_names)}")
    print(f"   - Target range: {df['target'].min():.2f} - {df['target'].max():.2f}")
    print(f"   - Time range: {df['event_timestamp'].min()} to {df['event_timestamp'].max()}")

if __name__ == "__main__":
    upload_california_data_to_minio() 