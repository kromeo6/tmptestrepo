from datetime import timedelta
from feast import Entity, FeatureView, Field, Project
from feast.types import Float32, Float64, Int64, ValueType
from feast.infra.offline_stores.file_source import FileSource

# Define a project for your features
project = Project(name="my_project", description="A project for driver statistics on K8s")

# Entity
driver = Entity(
    name="driver_id",
    description="Driver identifier",
    value_type=ValueType.INT64
)

# Entity for California housing data
house = Entity(
    name="house_id",
    description="House identifier",
    value_type=ValueType.INT64
)

# FileSource pointing to the MinIO service via localhost port-forward
minio_source = FileSource(
    name="driver_stats_k8s_source",
    path="s3://test-bucket/feast/data/driver_stats.parquet",
    timestamp_field="event_timestamp",
    created_timestamp_column="created",
    description="Driver stats from MinIO S3 via localhost",
    s3_endpoint_override="http://localhost:9001"
)

# California housing data source
california_source = FileSource(
    name="california_housing_source",
    path="s3://test-bucket/feast/data/california_data.parquet",
    timestamp_field="event_timestamp",
    created_timestamp_column="created",
    description="California housing data from MinIO S3",
    s3_endpoint_override="http://localhost:9001"
)

# FeatureView
driver_stats_view = FeatureView(
    name="driver_stats_minio",
    entities=[driver],
    ttl=timedelta(days=1),
    schema=[
        Field(name="conv_rate", dtype=Float64),
        Field(name="avg_daily_trips", dtype=Int64),
    ],
    source=minio_source,
    description="Driver statistics from MinIO S3 on Kubernetes",
)

# Minimalist view with explicit schema to avoid file reading during apply
full_data_view = FeatureView(
    name="full_data",
    entities=[driver],
    ttl=timedelta(days=365),  # Very long TTL to include all data
    schema=[
        Field(name="conv_rate", dtype=Float64),
        Field(name="avg_daily_trips", dtype=Int64),
    ],
    source=minio_source,  # Reuse existing source
)

# California housing feature view - fetches entire dataset
california_housing_view = FeatureView(
    name="california_housing",
    entities=[house],
    ttl=timedelta(days=365),  # Long TTL to include all historical data
    schema=[
        # All 8 California housing features
        Field(name="MedInc", dtype=Float32),        # Median income
        Field(name="HouseAge", dtype=Float32),      # House age
        Field(name="AveRooms", dtype=Float32),      # Average rooms
        Field(name="AveBedrms", dtype=Float32),     # Average bedrooms
        Field(name="Population", dtype=Float32),    # Population
        Field(name="AveOccup", dtype=Float32),      # Average occupancy
        Field(name="Latitude", dtype=Float32),      # Latitude
        Field(name="Longitude", dtype=Float32),     # Longitude
        Field(name="target", dtype=Float32),        # Target (house value)
    ],
    source=california_source,
    description="California housing data with all features and target values",
)