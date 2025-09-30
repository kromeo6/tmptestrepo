#!/usr/bin/env python3
"""
Create MinIO bucket for testing
"""
import boto3
from botocore.client import Config

def create_bucket():
    print("🪣 Creating MinIO bucket...")
    
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
    
    try:
        # Check if bucket exists
        s3_client.head_bucket(Bucket=bucket_name)
        print(f"✅ Bucket '{bucket_name}' already exists")
    except:
        # Create bucket
        try:
            s3_client.create_bucket(Bucket=bucket_name)
            print(f"✅ Created bucket '{bucket_name}'")
        except Exception as e:
            print(f"❌ Failed to create bucket: {e}")
            return False
    
    # List buckets to confirm
    response = s3_client.list_buckets()
    print(f"📋 Available buckets: {[b['Name'] for b in response['Buckets']]}")
    return True

if __name__ == "__main__":
    create_bucket() 