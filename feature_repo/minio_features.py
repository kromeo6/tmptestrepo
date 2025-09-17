from datetime import timedelta
from feast import Entity, FeatureView, Field, Project
from feast.types import Float64, Int64, ValueType
from feast.infra.offline_stores.file_source import FileSource

# Define a project for your features
project = Project(name="my_project", description="A project for driver statistics on K8s")

# Entity
driver = Entity(
    name="driver_id",
    description="Driver identifier",
    value_type=ValueType.INT64
)

# FileSource pointing to the MinIO service inside the Kubernetes cluster
minio_source = FileSource(
    name="driver_stats_k8s_source",
    path="s3://test-bucket/driver_stats.parquet",
    timestamp_field="event_timestamp",
    created_timestamp_column="created",
    description="Driver stats from MinIO S3 on Kubernetes",
    s3_endpoint_override="http://minio.kubeflow.svc.cluster.local:9000"
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