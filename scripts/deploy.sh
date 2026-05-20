#!/bin/bash

# Deploy to Kubernetes

echo "🚀 Deploying KubeMind AI to Kubernetes"
echo "======================================"

# Check kubectl
if ! command -v kubectl &> /dev/null; then
    echo "❌ kubectl is not installed. Please install kubectl first."
    exit 1
fi

# Check if Minikube is running
if ! minikube status > /dev/null 2>&1; then
    echo "Starting Minikube..."
    minikube start
fi

echo "✓ Kubernetes is ready"

# Create namespace
echo "Creating kubemind namespace..."
kubectl apply -f kubernetes/manifests/namespace.yaml

# Apply configurations
echo "Applying configurations..."
kubectl apply -f kubernetes/manifests/config/configmap.yaml

# Create storage
echo "Creating storage resources..."
kubectl apply -f kubernetes/manifests/storage/pvc.yaml

# Deploy services
echo "Deploying services..."
kubectl apply -f kubernetes/manifests/services/frontend.yaml
kubectl apply -f kubernetes/manifests/services/auth.yaml
kubectl apply -f kubernetes/manifests/services/database.yaml

# Deploy monitoring
echo "Deploying monitoring stack..."
kubectl apply -f kubernetes/manifests/monitoring/prometheus.yaml
kubectl apply -f kubernetes/manifests/monitoring/grafana.yaml

echo ""
echo "======================================"
echo "✅ Deployment complete!"
echo ""
echo "Check pod status:"
echo "kubectl get pods -n kubemind"
echo ""
echo "To access services:"
echo "kubectl port-forward -n kubemind svc/frontend-service 80:80"
echo "kubectl port-forward -n kubemind svc/grafana 3000:3000"
