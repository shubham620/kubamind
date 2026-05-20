# KubeMind AI Helm Chart - Quick Reference

## Chart Overview

**Location**: `kubernetes/helm/kubemind/`

**Version**: 1.0.0

**Type**: application

## Directory Structure

```
kubemind/
├── Chart.yaml                          # Chart metadata
├── values.yaml                          # Default configuration values
├── README.md                            # Comprehensive documentation
├── templates/
│   ├── _helpers.tpl                    # Helm template helpers
│   ├── backend-deployment.yaml         # Backend service deployment & HPA
│   ├── frontend-deployment.yaml        # Frontend service deployment & HPA
│   ├── database-deployment.yaml        # PostgreSQL StatefulSet with backups
│   ├── observability-deployment.yaml   # Prometheus, Grafana, Loki
│   ├── services/
│   │   └── kubemind-services.yaml      # All Kubernetes services & Ingress
│   ├── configmaps.yaml                 # Configuration for all services
│   ├── secrets.yaml                    # Database & admin passwords
│   ├── rbac.yaml                       # Service account & role bindings
│   └── NOTES.txt                       # Post-installation instructions
```

## Quick Start Commands

### Installation

```bash
# 1. Create namespace
kubectl create namespace kubemind

# 2. Install chart
helm install kubemind ./kubemind \
  --namespace kubemind \
  --set backend.secrets.database.password="secure-password" \
  --set observability.grafana.adminPassword="admin-password"

# 3. Verify
kubectl get pods -n kubemind
```

### Access Services

```bash
# Frontend
kubectl port-forward -n kubemind svc/kubemind-frontend 8080:80

# Backend API
kubectl port-forward -n kubemind svc/kubemind-backend 3000:8080

# Grafana
kubectl port-forward -n kubemind svc/kubemind-grafana 3000:3000

# Prometheus
kubectl port-forward -n kubemind svc/kubemind-prometheus 9090:9090

# Database
kubectl port-forward -n kubemind svc/kubemind-postgres 5432:5432
```

### Management

```bash
# Upgrade
helm upgrade kubemind ./kubemind --namespace kubemind

# Rollback
helm rollback kubemind <revision> --namespace kubemind

# Uninstall
helm uninstall kubemind --namespace kubemind

# Get values
helm get values kubemind --namespace kubemind

# Get manifest
helm get manifest kubemind --namespace kubemind
```

## Configurable Components

### Backend Service
- **Replicas**: 3 (configurable)
- **Image**: kubemind/backend:latest
- **Port**: 8080 (internal)
- **Resources**: 500m CPU, 512Mi Memory (requests)
- **Autoscaling**: 2-10 replicas based on CPU/Memory
- **Health Checks**: Liveness & Readiness probes

### Frontend Service
- **Replicas**: 2 (configurable)
- **Image**: kubemind/frontend:latest
- **Port**: 3000 (internal), 80 (external)
- **Ingress**: Optional (configure host and TLS)
- **Resources**: 250m CPU, 256Mi Memory (requests)
- **Load Balancer**: Optional

### PostgreSQL Database
- **Storage**: 10GB persistent volume
- **Backup**: Daily at 2 AM (configurable)
- **High Availability**: StatefulSet with headless service
- **Security**: Non-root user, read-only filesystem
- **Connection**: Port 5432

### Observability Stack

#### Prometheus
- **Retention**: 15 days (configurable)
- **Storage**: 5GB persistent volume
- **Port**: 9090
- **Scrape Interval**: 15 seconds

#### Grafana
- **Admin User**: admin (default)
- **Port**: 3000
- **Storage**: 1GB persistent volume
- **Data Sources**: Pre-configured Prometheus & Loki

#### Loki
- **Storage**: 5GB persistent volume
- **Port**: 3100
- **Log Retention**: Configurable

## Key Configuration Parameters

### Global
```yaml
global:
  environment: production          # Environment type
  namespace: kubemind             # Kubernetes namespace
  imagePullPolicy: IfNotPresent   # Image pull policy
```

### Backend
```yaml
backend:
  replicaCount: 3
  resources:
    requests:
      cpu: 500m
      memory: 512Mi
    limits:
      cpu: 1000m
      memory: 1Gi
  autoscaling:
    enabled: true
    minReplicas: 2
    maxReplicas: 10
    targetCPUUtilizationPercentage: 80
```

### Frontend
```yaml
frontend:
  replicaCount: 2
  ingress:
    enabled: true
    className: nginx
    hosts:
      - host: kubemind.example.com
        paths:
          - path: /
            pathType: Prefix
```

### Database
```yaml
database:
  postgres:
    persistence:
      enabled: true
      size: 10Gi
      storageClass: standard
    backup:
      enabled: true
      schedule: "0 2 * * *"
      retention: 7
```

### Observability
```yaml
observability:
  enabled: true
  prometheus:
    retention: 15d
  grafana:
    adminUser: admin
  loki:
    enabled: true
```

## Common Helm Commands

### Chart Management
```bash
# Lint chart for errors
helm lint ./kubemind

# Dry run (preview changes)
helm install kubemind ./kubemind --dry-run --debug

# Get release history
helm history kubemind -n kubemind

# Get deployment status
helm status kubemind -n kubemind
```

### Customization
```bash
# Install with custom values file
helm install kubemind ./kubemind -f custom-values.yaml

# Override specific values
helm install kubemind ./kubemind \
  --set backend.replicaCount=5 \
  --set database.postgres.persistence.size=50Gi

# Show all template variables
helm template kubemind ./kubemind
```

### Debugging
```bash
# Show rendered templates
helm template kubemind ./kubemind -f values.yaml

# Get rendered manifest
helm get manifest kubemind -n kubemind

# Check chart dependencies
helm dependency list ./kubemind
```

## Troubleshooting Guide

### Check Status
```bash
# Pod status
kubectl get pods -n kubemind

# Service endpoints
kubectl get endpoints -n kubemind

# Persistent volumes
kubectl get pvc -n kubemind

# Helm status
helm status kubemind -n kubemind
```

### View Logs
```bash
# Pod logs
kubectl logs -n kubemind <pod-name>

# Follow logs
kubectl logs -n kubemind <pod-name> -f

# Previous logs (crashed pod)
kubectl logs -n kubemind <pod-name> --previous

# All logs for a deployment
kubectl logs -n kubemind -l app=kubemind-backend
```

### Debug Pod
```bash
# Execute command
kubectl exec -it -n kubemind <pod-name> -- /bin/bash

# Describe pod
kubectl describe pod -n kubemind <pod-name>

# Check events
kubectl get events -n kubemind --sort-by='.lastTimestamp'
```

### Database Issues
```bash
# Connect to database
kubectl run -it --rm psql --image=postgres:15-alpine --restart=Never -n kubemind -- \
  psql -h kubemind-postgres -U kubemind -d kubemind_db

# Backup database
kubectl exec -n kubemind kubemind-postgres-0 -- \
  pg_dump -U kubemind kubemind_db > backup.sql

# Test connectivity
kubectl run -it --rm curl --image=curlimages/curl --restart=Never -n kubemind -- \
  curl http://kubemind-backend:8080/health
```

## Performance Tuning

### Scale Up
```bash
helm upgrade kubemind ./kubemind --namespace kubemind \
  --set backend.replicaCount=5 \
  --set frontend.replicaCount=3 \
  --set backend.resources.requests.memory=1Gi
```

### Optimize Storage
```bash
helm upgrade kubemind ./kubemind --namespace kubemind \
  --set database.postgres.persistence.size=100Gi \
  --set observability.prometheus.persistence.size=10Gi
```

### Adjust Autoscaling
```bash
helm upgrade kubemind ./kubemind --namespace kubemind \
  --set backend.autoscaling.maxReplicas=20 \
  --set backend.autoscaling.targetCPUUtilizationPercentage=70
```

## Important Ports

| Service | Internal Port | External Port | Protocol |
|---------|---------------|---------------|----------|
| Backend | 8080 | ClusterIP:8080 | HTTP |
| Frontend | 3000 | 80 (via Ingress) | HTTP |
| Prometheus | 9090 | ClusterIP:9090 | HTTP |
| Grafana | 3000 | ClusterIP:3000 | HTTP |
| Loki | 3100 | ClusterIP:3100 | HTTP |
| PostgreSQL | 5432 | ClusterIP:5432 | TCP |

## Best Practices

1. **Security**
   - Use external secret management for credentials
   - Enable RBAC (included by default)
   - Configure network policies
   - Use TLS/SSL for Ingress

2. **High Availability**
   - Enable autoscaling
   - Use multiple replicas
   - Configure pod disruption budgets
   - Enable database backups

3. **Monitoring**
   - Enable Prometheus metrics scraping
   - Configure Grafana dashboards
   - Set up Loki log aggregation
   - Create alerts for critical metrics

4. **Resource Management**
   - Set resource requests and limits
   - Monitor node usage
   - Use appropriate storage classes
   - Plan capacity ahead

5. **Backup and Recovery**
   - Enable database backups
   - Test restore procedures
   - Document recovery process
   - Store backups securely

## Additional Resources

- **Helm Documentation**: https://helm.sh/docs/
- **Kubernetes Documentation**: https://kubernetes.io/docs/
- **PostgreSQL**: https://www.postgresql.org/docs/
- **Prometheus**: https://prometheus.io/docs/
- **Grafana**: https://grafana.com/docs/grafana/latest/
- **Loki**: https://grafana.com/docs/loki/latest/

## Support

For issues or questions about the Helm chart:
1. Check INSTALLATION_GUIDE.md for detailed setup
2. Review README.md for configuration options
3. Check template files for implementation details
4. Review Kubernetes events: `kubectl get events -n kubemind`
5. Check pod logs: `kubectl logs -n kubemind -l app=kubemind-backend`
