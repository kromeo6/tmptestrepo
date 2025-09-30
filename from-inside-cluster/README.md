# Feast California Housing Fetcher - From Inside Kubernetes Cluster

This setup allows you to fetch California housing data using Feast from inside a Kubernetes pod, accessing cross-namespace services.

## 🏗️ Architecture

- **Pod Namespace**: `default`
- **MinIO Service**: `minio-service.kubeflow.svc.cluster.local:9000` (kubeflow namespace)
- **PostgreSQL Service**: `postgres.feast.svc.cluster.local:5432` (feast namespace)
- **Redis Service**: `redis.feast.svc.cluster.local:6379` (feast namespace)

## 📁 Files Structure

```
from-inside-cluster/
├── Dockerfile              # Python 3.11 + Feast dependencies
├── requirements.txt         # Python packages
├── fetch_california_data.py # Updated script for cross-namespace access
├── feature_store.yaml       # Cross-namespace service endpoints  
├── feature_repo/
│   ├── feature_store.yaml   # Feature store config
│   └── minio_features.py    # Feature definitions with cross-namespace MinIO
├── pod.yaml                 # Kubernetes pod manifest
├── build-and-deploy.sh      # Build & deploy script
└── README.md               # This file
```

## 🚀 Quick Start

### 1. Build and Deploy
```bash
cd from-inside-cluster
chmod +x build-and-deploy.sh
./build-and-deploy.sh
```

### 2. Execute Commands in Pod
```bash
# Run the California housing data fetch
kubectl exec -it feast-california-fetcher -- python fetch_california_data.py

# Get a shell in the pod
kubectl exec -it feast-california-fetcher -- /bin/bash

# Apply feature definitions from inside pod
kubectl exec -it feast-california-fetcher -- bash -c "cd feature_repo && feast apply"
```

## 🔧 Manual Steps

### Build Docker Image
```bash
docker build -t feast-california:latest .
```

### Deploy Pod
```bash
kubectl apply -f pod.yaml
```

### Check Pod Status
```bash
kubectl get pod feast-california-fetcher
kubectl describe pod feast-california-fetcher
```

## 🌐 Cross-Namespace Service Access

The configuration uses full DNS names for cross-namespace service access:

- **MinIO**: `minio-service.kubeflow.svc.cluster.local:9000`
- **PostgreSQL**: `postgres.feast.svc.cluster.local:5432` 
- **Redis**: `redis.feast.svc.cluster.local:6379`

## 📊 Expected Output

When running the fetch script from inside the pod, you should see:
- 600 California housing records fetched
- All 9 features (MedInc, HouseAge, etc.)
- House values ranging from $60K to $500K
- Cross-namespace service connectivity confirmed

## 🐛 Troubleshooting

### Pod Won't Start
```bash
kubectl describe pod feast-california-fetcher
kubectl logs feast-california-fetcher
```

### Service Connectivity Issues
```bash
# Test MinIO connectivity from pod
kubectl exec -it feast-california-fetcher -- nslookup minio-service.kubeflow.svc.cluster.local

# Test PostgreSQL connectivity
kubectl exec -it feast-california-fetcher -- nslookup postgres.feast.svc.cluster.local
```

### Feature Store Issues
```bash
# Check feature store config
kubectl exec -it feast-california-fetcher -- cat feature_repo/feature_store.yaml

# Apply features manually
kubectl exec -it feast-california-fetcher -- bash -c "cd feature_repo && feast apply"
```

## 🧹 Cleanup

```bash
kubectl delete pod feast-california-fetcher
docker rmi feast-california:latest
``` 