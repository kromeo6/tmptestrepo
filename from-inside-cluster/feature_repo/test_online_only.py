# #!/usr/bin/env python3
# """
# Test script to verify online features from K8s materialization.
# This only tests online features (no S3 access needed).
# """

# import os
# import sys
# from datetime import datetime, timedelta
# import pandas as pd
# from feast import FeatureStore

# def test_online_features_only():
#     """Test only online feature retrieval from K8s via port-forwarding."""
#     print("🧪 Testing Online Features After K8s Materialization")
#     print("=" * 55)
    
#     try:
#         print("1. Connecting to port-forwarded Feast services...")
#         store = FeatureStore(repo_path=".")
#         print("✅ Connected to remote Feast feature store")
        
#         print("\n2. Listing available feature views...")
#         feature_views = store.list_feature_views()
#         for fv in feature_views:
#             print(f"   - {fv.name}: {fv.description}")
        
#         if not feature_views:
#             raise Exception("No feature views found.")
        
#         print("\n3. Testing online feature retrieval...")
#         online_features = store.get_online_features(
#             features=[
#                 "driver_stats_minio:conv_rate",
#                 "driver_stats_minio:avg_daily_trips"
#             ],
#             entity_rows=[
#                 {"driver_id": 1},
#                 {"driver_id": 2},
#                 {"driver_id": 3},
#                 {"driver_id": 4},
#                 {"driver_id": 5}
#             ]
#         )
        
#         online_df = online_features.to_df()
#         print("✅ Successfully retrieved online features from K8s!")
#         print("\nOnline features:")
#         print(online_df)
        
#         # Check if any features were actually materialized
#         has_materialized_features = any(
#             online_df[col].notna().any() 
#             for col in ['conv_rate', 'avg_daily_trips'] 
#             if col in online_df.columns
#         )
        
#         if has_materialized_features:
#             print("\n🎉 SUCCESS: Materialized features found in online store!")
#             print("   - K8s materialization: ✅ WORKING")
#             print("   - Online store: ✅ POPULATED")
#             print("   - Remote access: ✅ WORKING")
#         else:
#             print("\n⚠️  Online store connected but no materialized features found.")
#             print("   This could mean:")
#             print("   - Materialization time window didn't match entity timestamps")
#             print("   - Features need different entity IDs")
            
#         print("\n" + "=" * 55)
#         return True
        
#     except Exception as e:
#         print(f"\n❌ ERROR: {e}")
#         import traceback
#         traceback.print_exc()
#         return False

# if __name__ == "__main__":
#     success = test_online_features_only()
    
#     if success:
#         print("\n✅ Online feature test completed!")
#         sys.exit(0)
#     else:
#         print("\n❌ Online feature test failed!")
#         sys.exit(1) 