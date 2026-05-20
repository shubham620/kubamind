# KubeMind AI Helm Chart Installation Guide

## Quick Start

### Prerequisites
- Kubernetes cluster (1.20+)
- Helm 3.0+
- kubectl configured to access your cluster
- At least 4GB free memory and 20GB storage

### Installation Steps

```bash
# 1. Create namespace
kubectl create namespace kubemind

# 2. Generate secure passwords
DB_PASSWORD=$(openssl rand -base64 32)
GRAFANA_PASSWORD=$(openssl rand -base64 32)

# 3. Install Helm chart
helm install kubemind ./kubemind \
  --namespace kubemind \
  --set backend.secrets.database.password="$DB_PASSWORD" \
  --set observability.grafana.adminPassword="$GRAFANA_PASSWORD"

# 4. Verify installation
kubectl get pods -n kubemind
kubectl get svc -n kubemind
```

## Installation Methods

### Method 1: Local Deployment (Development)

```bash
cd kubernetes/helm

helm install kubemind-dev ./kubemind \
  --namespace kubemind-dev \
  --create-namespace \
  --set backend.replicaCount=1 \
  --set frontend.replicaCount=1 \
  --set backend.secrets.database.password="dev-password" \
  --set observability.grafana.adminPassword="dev-admin"
```

### Method 2: Production Deployment

Create a `prod-values.yaml`:

```yaml
# prod-values.yaml
backend:
  replicaCount: 3
  autoscaling:
    enabled: true
    minReplicas: 3
    maxReplicas: 10
  resources:
    requests:
      cpu: 1000m
      memory: 1Gi
    limits:
      cpu: 2000m
      memory: 2Gi

frontend:
  replicaCount: 3
  ingress:
    enabled: true
    className: nginx
    hosts:
      - host: kubemind.example.com
        paths:
          - path: /
            pathType: Prefix
    tls:
      - secretName: kubemind-tls
        hosts:
          - kubemind.example.com

database:
  postgres:
    persistence:
      size: 50Gi
    backup:
      enabled: true
      schedule: "0 2 * * *"

observability:
  prometheus:
    retention: 30d
  grafana:
    persistence:
      size: 5Gi
```

Install:

```bash
helm install kubemind ./kubemind \
  --namespace kubemind \
  --create-namespace \
  --values prod-values.yaml \
  --set backend.secrets.database.password="$(openssl rand -base64 32)" \
  --set observability.grafana.adminPassword="$(openssl rand -base64 32)"
```

### Method 3: GitOps with ArgoCD

Create `argocd-application.yaml`:

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: kubemind
  namespace: argocd
spec:
  project: default
  source:
    repoURL: https://github.com/yourusername/kubemind-ai
    targetRevision: main
    path: kubernetes/helm/kubemind
    helm:
      values: |
        backend:
          secrets:
            database:
              password: "{{ secrets.dbPassword }}"
        observability:
          grafana:
            adminPassword: "{{ secrets.grafanaPassword }}"
  destination:
    server: https://kubernetes.default.svc
    namespace: kubemind
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
```

## Post-Installation

### Access Services

```bash
# Frontend
kubectl port-forward -n kubemind svc/kubemind-frontend 8080:80
# Visit: http://localhost:8080

# Backend API
kubectl port-forward -n kubemind svc/kubemind-backend 3000:8080
# Visit: http://localhost:3000

# Grafana
kubectl port-forward -n kubemind svc/kubemind-grafana 3000:3000
# Visit: http://localhost:3000
# Default user: admin
# Password: (your grafana password)

# Prometheus
kubectl port-forward -n kubemind svc/kubemind-prometheus 9090:9090
# Visit: http://localhost:9090
```

### Verify Services

```bash
# Check deployment status
kubectl get deployments -n kubemind

# Check pod status
kubectl get pods -n kubemind

# Check services
kubectl get svc -n kubemind

# Check persistent volumes
kubectl get pvc -n kubemind

# View Helm release
helm status kubemind -n kubemind

# View Helm values
helm get values kubemind -n kubemind
```

### Database Initialization

```bash
# Connect to database
kubectl run -it --rm psql --image=postgres:15-alpine --restart=Never -n kubemind -- \
  psql -h kubemind-postgres -U kubemind -d kubemind_db

# Or port-forward
kubectl port-forward -n kubemind svc/kubemind-postgres 5432:5432
# Then connect with: psql -h localhost -U kubemind -d kubemind_db
```

## Customization

### Custom Values

```bash
helm install kubemind ./kubemind \
  --namespace kubemind \
  --set backend.replicaCount=5 \
  --set backend.resources.limits.memory=2Gi \
  --set frontend.service.type=LoadBalancer \
  --set database.postgres.persistence.size=100Gi
```

### Helm Chart Overrides

```bash
# Override multiple values
helm install kubemind ./kubemind \
  --namespace kubemind \
  -f values.yaml \
  -f prod-overrides.yaml \
  --set backend.image.tag=v1.2.3
```

### Using Secrets Manager

```bash
# With External Secrets Operator
helm install kubemind ./kubemind \
  --namespace kubemind \
  --set externalSecrets.enabled=true \
  --set externalSecrets.backendStore=aws-secrets-manager
```

## Troubleshooting

### Check Pod Logs

```bash
# View logs for a specific pod
kubectl logs -n kubemind <pod-name>

# View logs for all pods matching a label
kubectl logs -n kubemind -l component=backend --all-containers=true

# Stream logs
kubectl logs -n kubemind -l component=backend -f
```

### Describe Resources

```bash
# Describe deployment
kubectl describe deployment -n kubemind kubemind-backend

# Describe pod
kubectl describe pod -n kubemind <pod-name>

# Describe service
kubectl describe svc -n kubemind kubemind-backend
```

### Check Events

```bash
# Get recent events
kubectl get events -n kubemind --sort-by='.lastTimestamp'

# Watch events in real-time
kubectl get events -n kubemind --watch
```

### Debug Pod

```bash
# Execute command in pod
kubectl exec -it -n kubemind <pod-name> -- /bin/bash

# Port forward for debugging
kubectl port-forward -n kubemind <pod-name> 8000:8000
```

### Common Issues

#### Pods stuck in Pending

```bash
# Check node resources
kubectl top nodes
kubectl describe node <node-name>

# Check PVC status
kubectl get pvc -n kubemind
kubectl describe pvc -n kubemind <pvc-name>
```

#### Database connection errors

```bash
# Check database pod
kubectl get pods -n kubemind -l component=database

# View database logs
kubectl logs -n kubemind kubemind-postgres-0

# Test connection
kubectl run -it --rm psql --image=postgres:15-alpine --restart=Never -n kubemind -- \
  psql -h kubemind-postgres -U kubemind -d kubemind_db -c "SELECT 1"
```

#### Image pull errors

```bash
# Check ImagePullBackOff errors
kubectl describe pod -n kubemind <pod-name>

# Verify image repository and tag
kubectl get pod -n kubemind <pod-name> -o yaml | grep image:
```

## Upgrade Procedure

### Minor Version Upgrade

```bash
# Update Helm chart values
helm upgrade kubemind ./kubemind \
  --namespace kubemind \
  -f values.yaml

# Verify upgrade
helm status kubemind -n kubemind
kubectl rollout status deployment/kubemind-backend -n kubemind
```

### Major Version Upgrade

```bash
# Create backup
kubectl get all -n kubemind -o yaml > kubemind-backup.yaml

# Upgrade with new values
helm upgrade kubemind ./kubemind \
  --namespace kubemind \
  -f new-prod-values.yaml

# Monitor rollout
kubectl rollout status deployment/kubemind-backend -n kubemind
kubectl rollout status deployment/kubemind-frontend -n kubemind
```

### Rollback

```bash
# View release history
helm history kubemind -n kubemind

# Rollback to previous version
helm rollback kubemind <revision> -n kubemind

# Verify rollback
helm status kubemind -n kubemind
```

## Uninstallation

```bash
# Uninstall Helm release
helm uninstall kubemind -n kubemind

# Delete namespace (optional)
kubectl delete namespace kubemind

# Check for remaining resources
kubectl get all -n kubemind
```

## Advanced Configuration

### Enable TLS/SSL

```bash
# Install cert-manager (if not already installed)
kubectl apply -f https://github.com/cert-manager/cert-manager/releases/download/v1.13.0/cert-manager.yaml

# Create Ingress with TLS
helm upgrade kubemind ./kubemind \
  --namespace kubemind \
  --set frontend.ingress.tls[0].secretName=kubemind-tls \
  --set frontend.ingress.tls[0].hosts[0]=kubemind.example.com
```

### Enable External Database

```bash
helm install kubemind ./kubemind \
  --namespace kubemind \
  --set database.enabled=false \
  --set backend.secrets.database.host=external-postgres.example.com \
  --set backend.secrets.database.port=5432
```

### Custom Storage Classes

```bash
helm install kubemind ./kubemind \
  --namespace kubemind \
  --set database.postgres.persistence.storageClass=fast-ssd \
  --set observability.prometheus.persistence.storageClass=standard
```

## Monitoring and Logging

### Prometheus Metrics

Access Prometheus dashboard for:
- Pod CPU and memory usage
- Network traffic
- Custom application metrics

### Grafana Dashboards

Pre-configured dashboards:
- Kubernetes cluster overview
- Pod resource usage
- Database metrics
- Application performance

### Loki Logs

Query logs from all containers:
- Backend application logs
- Frontend server logs
- Database logs
- System logs

## Performance Optimization

### Resource Limits

Adjust based on your workload:

```yaml
backend:
  resources:
    requests:
      cpu: 2000m
      memory: 2Gi
    limits:
      cpu: 4000m
      memory: 4Gi
```

### Autoscaling

Configure HPA for automatic scaling:

```yaml
backend:
  autoscaling:
    targetCPUUtilizationPercentage: 70
    maxReplicas: 20
```

### Caching with Redis (Optional)

```bash
helm upgrade kubemind ./kubemind \
  --namespace kubemind \
  --set redis.enabled=true
```

## Support and Documentation

- Helm Chart Documentation: See README.md
- Kubernetes Documentation: https://kubernetes.io/docs/
- KubeMind AI Repository: https://github.com/yourusername/kubemind-ai

## Additional Resources

- [Helm Official Documentation](https://helm.sh/docs/)
- [Kubernetes Best Practices](https://kubernetes.io/docs/concepts/configuration/overview/)
- [PostgreSQL on Kubernetes](https://www.postgresql.org/docs/)
- [Prometheus Monitoring](https://prometheus.io/docs/)
- [Grafana Dashboards](https://grafana.com/docs/grafana/latest/)
