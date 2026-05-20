# KubeMind AI Helm Chart

A comprehensive Helm chart for deploying KubeMind AI on Kubernetes clusters.

## Overview

This Helm chart provides a complete solution for deploying KubeMind AI with:
- **Backend Service**: FastAPI/Python backend with automatic scaling
- **Frontend Service**: React/Node.js frontend with load balancing
- **Database**: PostgreSQL with persistent storage and automated backups
- **Observability Stack**: Prometheus, Grafana, and Loki for monitoring and logging
- **RBAC**: Role-based access control for Kubernetes security
- **Network Policies**: Optional network segmentation

## Prerequisites

- Kubernetes 1.20+
- Helm 3.0+
- kubectl configured to access your cluster
- At least 4GB of available memory
- Persistent volume support (for database and observability stack)

## Installation

### 1. Add the Helm Repository (if hosted)

```bash
helm repo add kubemind https://your-helm-repo-url
helm repo update
```

### 2. Create Namespace

```bash
kubectl create namespace kubemind
```

### 3. Install the Chart

#### Basic Installation

```bash
helm install kubemind ./kubemind \
  --namespace kubemind \
  --set backend.secrets.database.password=your-secure-password \
  --set observability.grafana.adminPassword=your-grafana-password
```

#### Production Installation

```bash
helm install kubemind ./kubemind \
  --namespace kubemind \
  --values values.yaml \
  --set backend.image.tag=v1.0.0 \
  --set frontend.image.tag=v1.0.0 \
  --set backend.secrets.database.password=$(openssl rand -base64 32) \
  --set observability.grafana.adminPassword=$(openssl rand -base64 32)
```

### 4. Verify Installation

```bash
# Check deployment status
kubectl get deployments -n kubemind

# Check all pods
kubectl get pods -n kubemind

# Check services
kubectl get svc -n kubemind

# View Helm release
helm status kubemind -n kubemind
```

## Configuration

### Key Configuration Options

#### Global Settings

```yaml
global:
  environment: production          # Environment type
  namespace: kubemind             # Kubernetes namespace
  imagePullPolicy: IfNotPresent   # Image pull policy
```

#### Backend Configuration

```yaml
backend:
  enabled: true
  replicaCount: 3                 # Number of replicas
  image:
    tag: latest                   # Container image tag
  resources:
    requests:
      cpu: 500m                   # CPU request
      memory: 512Mi               # Memory request
    limits:
      cpu: 1000m                  # CPU limit
      memory: 1Gi                 # Memory limit
  autoscaling:
    enabled: true
    minReplicas: 2                # Minimum pods
    maxReplicas: 10               # Maximum pods
```

#### Frontend Configuration

```yaml
frontend:
  enabled: true
  replicaCount: 2
  ingress:
    enabled: true
    hosts:
      - host: kubemind.example.com
        paths:
          - path: /
            pathType: Prefix
    tls:
      - secretName: kubemind-tls
        hosts:
          - kubemind.example.com
```

#### Database Configuration

```yaml
database:
  postgres:
    persistence:
      enabled: true
      size: 10Gi                  # Storage size
      storageClass: standard      # Storage class
    backup:
      enabled: true
      schedule: "0 2 * * *"       # Daily at 2 AM
      retention: 7                # Keep 7 days of backups
```

#### Observability Stack

```yaml
observability:
  enabled: true
  prometheus:
    enabled: true
    retention: 15d                # Data retention
  grafana:
    enabled: true
  loki:
    enabled: true
```

### Custom Values

Create a custom `values.yaml` file:

```yaml
backend:
  replicaCount: 5
  resources:
    requests:
      cpu: 1000m
      memory: 1Gi
    limits:
      cpu: 2000m
      memory: 2Gi

database:
  postgres:
    persistence:
      size: 50Gi

observability:
  prometheus:
    retention: 30d
```

Install with custom values:

```bash
helm install kubemind ./kubemind \
  --namespace kubemind \
  --values custom-values.yaml
```

## Usage

### Accessing Services

#### Frontend

```bash
# With Ingress
# Access directly via the configured hostname (e.g., kubemind.example.com)

# Without Ingress
kubectl port-forward -n kubemind svc/kubemind-frontend 8080:80
# Access at http://localhost:8080
```

#### Backend API

```bash
kubectl port-forward -n kubemind svc/kubemind-backend 3000:8080
# Access at http://localhost:3000
```

#### Grafana Dashboards

```bash
kubectl port-forward -n kubemind svc/kubemind-grafana 3000:3000
# Access at http://localhost:3000
# Login with configured admin credentials
```

#### Prometheus Metrics

```bash
kubectl port-forward -n kubemind svc/kubemind-prometheus 9090:9090
# Access at http://localhost:9090
```

#### Loki Logs

```bash
kubectl port-forward -n kubemind svc/kubemind-loki 3100:3100
# Access at http://localhost:3100
```

### Scaling

#### Manual Scaling

```bash
# Scale backend deployment
kubectl scale deployment kubemind-backend -n kubemind --replicas=5

# Scale frontend deployment
kubectl scale deployment kubemind-frontend -n kubemind --replicas=3
```

#### Automatic Scaling

Horizontal Pod Autoscaler (HPA) is configured to automatically scale based on CPU and memory metrics:

```bash
# View HPA status
kubectl get hpa -n kubemind

# Describe HPA
kubectl describe hpa kubemind-backend-hpa -n kubemind
```

### Database Backups

PostgreSQL backups are automatically created according to the schedule:

```bash
# View backup CronJob
kubectl get cronjob -n kubemind

# Manually trigger a backup
kubectl create job --from=cronjob/kubemind-postgres-backup manual-backup -n kubemind

# View backup job logs
kubectl logs -n kubemind -l job-name=manual-backup
```

## Upgrading

### Upgrade to a New Version

```bash
helm upgrade kubemind ./kubemind \
  --namespace kubemind \
  --values values.yaml
```

### Rollback to Previous Version

```bash
# View release history
helm history kubemind -n kubemind

# Rollback to previous release
helm rollback kubemind 1 -n kubemind
```

## Uninstalling

```bash
helm uninstall kubemind -n kubemind

# Optional: Delete the namespace
kubectl delete namespace kubemind
```

## Troubleshooting

### Pod Not Starting

```bash
# Check pod status
kubectl describe pod <pod-name> -n kubemind

# View pod logs
kubectl logs <pod-name> -n kubemind

# Check events
kubectl get events -n kubemind --sort-by='.lastTimestamp'
```

### Database Connection Issues

```bash
# Check database pod
kubectl get pods -n kubemind -l component=database

# Test database connection
kubectl run -it --rm debug --image=postgres:15-alpine --restart=Never -n kubemind -- psql -h kubemind-postgres -U kubemind -d kubemind_db
```

### Resource Issues

```bash
# View resource usage
kubectl top pods -n kubemind

# View node resource usage
kubectl top nodes

# Check PVC status
kubectl get pvc -n kubemind
```

### Common Issues

**Issue**: Pods stuck in Pending state
- **Solution**: Check available resources (`kubectl top nodes`) and node selectors

**Issue**: Database pod not starting
- **Solution**: Verify storage class exists (`kubectl get storageclass`)

**Issue**: Frontend cannot reach backend
- **Solution**: Check service DNS name and network policies

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                      Kubernetes                         │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐ │
│  │   Frontend   │  │   Backend    │  │  Database    │ │
│  │  (React)     │  │  (FastAPI)   │  │  (PostgreSQL)│ │
│  └──────────────┘  └──────────────┘  └──────────────┘ │
│         │                  │                  │        │
│  ┌──────────────────────────────────────────────────┐  │
│  │            Observability Stack                   │  │
│  │  ┌────────────┐ ┌────────────┐ ┌─────────────┐  │  │
│  │  │ Prometheus │ │  Grafana   │ │    Loki     │  │  │
│  │  └────────────┘ └────────────┘ └─────────────┘  │  │
│  └──────────────────────────────────────────────────┘  │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

## Security Considerations

1. **Secrets Management**
   - Database passwords and API keys should be managed via external secret managers (e.g., HashiCorp Vault, AWS Secrets Manager)
   - Never commit secrets to version control

2. **RBAC**
   - ServiceAccounts have minimal required permissions
   - Review and adjust roles based on your security requirements

3. **Network Policies**
   - Optional network policies can be enabled to restrict traffic
   - Configure based on your network architecture

4. **Pod Security**
   - Non-root user (UID 1000)
   - Read-only root filesystem
   - No privilege escalation

## Performance Tuning

### Resource Requests and Limits

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

### Autoscaling Policies

```yaml
backend:
  autoscaling:
    targetCPUUtilizationPercentage: 70
    targetMemoryUtilizationPercentage: 80
    maxReplicas: 20
```

### Database Optimization

```yaml
database:
  postgres:
    persistence:
      size: 100Gi
    backup:
      schedule: "0 3 * * *"
      retention: 30
```

## Contributing

For issues, feature requests, or improvements to the Helm chart, please create an issue or submit a pull request in the repository.

## License

This Helm chart is part of the KubeMind AI project and follows the same license terms.

## Support

For support, documentation, and updates:
- GitHub: https://github.com/yourusername/kubemind-ai
- Issues: https://github.com/yourusername/kubemind-ai/issues
- Documentation: https://docs.kubemind.ai

## Changelog

### Version 1.0.0
- Initial release
- Backend, Frontend, and Database deployments
- Observability stack (Prometheus, Grafana, Loki)
- RBAC configuration
- Network policies support
- Automated database backups
