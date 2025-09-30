#!/bin/bash

echo "🐳 Building Feast California Housing Docker Image..."
echo "=================================================="

# Build the Docker image
docker build -t feast-california:latest .

if [ $? -eq 0 ]; then
    echo "✅ Docker image built successfully!"
else
    echo "❌ Docker build failed!"
    exit 1
fi

echo ""
echo "🚀 Deploying to Kubernetes..."
echo "=============================="

# Delete existing pod if it exists
kubectl delete pod feast-california-fetcher --ignore-not-found=true

# Wait a moment for cleanup
sleep 5

# Deploy the new pod
kubectl apply -f pod.yaml

if [ $? -eq 0 ]; then
    echo "✅ Pod deployed successfully!"
    echo ""
    echo "📋 Waiting for pod to be ready..."
    kubectl wait --for=condition=Ready pod/feast-california-fetcher --timeout=60s
    
    if [ $? -eq 0 ]; then
        echo "✅ Pod is ready!"
        echo ""
        echo "🔍 Pod status:"
        kubectl get pod feast-california-fetcher
        echo ""
        echo "📝 To exec into the pod and run the fetch script:"
        echo "   kubectl exec -it feast-california-fetcher -- python fetch_california_data.py"
        echo ""
        echo "📝 To get a shell in the pod:"
        echo "   kubectl exec -it feast-california-fetcher -- /bin/bash"
    else
        echo "⚠️  Pod is not ready yet. Check status with:"
        echo "   kubectl get pod feast-california-fetcher"
        echo "   kubectl describe pod feast-california-fetcher"
    fi
else
    echo "❌ Pod deployment failed!"
    exit 1
fi 