# KubeMind AI Helm Charts - Complete Deployment Guide

## ✅ Task Completion Summary

**Status**: COMPLETED ✓

### Deliverables Completed

1. ✅ **Helm Chart Structure** - Complete directory hierarchy created
2. ✅ **values.yaml** - Comprehensive configuration with all parameters
3. ✅ **Deployment Templates**:
   - Backend deployment with HPA
   - Frontend deployment with HPA  
   - PostgreSQL database with StatefulSet
   - Observability stack (Prometheus, Grafana, Loki)
4. ✅ **NOTES.txt** - Post-installation usage instructions
5. ✅ **Additional Files**:
   - _helpers.tpl (template helpers)
   - configmaps.yaml (all configurations)
   - secrets.yaml (secure credential management)
   - rbac.yaml (role-based access control)
   - services/kubemind-services.yaml (all services and ingress)
   - README.md (comprehensive documentation)
   - INSTALLATION_GUIDE.md (detailed setup guide)
   - QUICK_REFERENCE.md (quick commands reference)

---

## 📁 File Locations

```
c:\Users\mrshu\OneDrive\Desktop\coding\KubeMind AI\
├── kubernetes/
│   ├── helm/
│   │   ├── INSTALLATION_GUIDE.md         (Detailed installation steps)
│   │   ├── QUICK_REFERENCE.md            (Command reference)
│   │   └── kubemind/                     (Main chart directory)
│   │       ├── Chart.yaml
│   │       ├── values.yaml
│   │       ├── README.md
│   │       └── templates/
│   │           ├── _helpers.tpl
│   │           ├── backend-deployment.yaml
│   │           ├── frontend-deployment.yaml
│   │           ├── database-deployment.yaml
│   │           ├── observability-deployment.yaml
│   │           ├── configmaps.yaml
│   │           ├── secrets.yaml
│   │           ├── rbac.yaml
│   │           ├── NOTES.txt
│   │           └── services/
│   │               └── kubemind-services.yaml
```

---

## 🚀 Deployment Instructions

### Prerequisites

```bash
# Required
- Kubernetes 1.20+ cluster
- Helm 3.0+ installed
- kubectl configured for cluster access
- 4+ GB available memory
- 20+ GB storage capacity
```

### Installation Steps

#### Step 1: Prepare Environment

```bash
# Generate secure passwords
DB_PASSWORD=$(openssl rand -base64 32)
GRAFANA_PASSWORD=$(openssl rand -base64 32)

# Save for reference (do not commit to version control)
echo "Database Password: $DB_PASSWORD" > .helm-passwords.txt
echo "Grafana Password: $GRAFANA_PASSWORD" >> .helm-passwords.txt
chmod 600 .helm-passwords.txt
```

#### Step 2: Create Namespace

```bash
kubectl create namespace kubemind
```

#### Step 3: Install Helm Chart

```bash
# Navigate to helm directory
cd kubernetes/helm

# Install the chart
helm install kubemind ./kubemind \
  --namespace kubemind \
  --set backend.secrets.database.password="$DB_PASSWORD" \
  --set observability.grafana.adminPassword="$GRAFANA_PASSWORD"
```

#### Step 4: Verify Deployment

```bash
# Check all pods are running
kubectl get pods -n kubemind

# Check services
kubectl get svc -n kubemind

# Check deployment status
kubectl rollout status deployment/kubemind-backend -n kubemind
kubectl rollout status deployment/kubemind-frontend -n kubemind

# View Helm release
helm status kubemind -n kubemind
```

### Expected Output

```
NAME                                 READY   STATUS    RESTARTS   AGE
kubemind-backend-xxx-xxx            3/3     Running   0          2m
kubemind-frontend-xxx-xxx           2/2     Running   0          2m
kubemind-postgres-0                 1/1     Running   0          2m
kubemind-prometheus-xxx-xxx         1/1     Running   0          2m
kubemind-grafana-xxx-xxx            1/1     Running   0          2m
kubemind-loki-xxx-xxx               1/1     Running   0          2m
```

---

## 🔌 Accessing Services

### Frontend Application

```bash
# Option 1: Port Forward
kubectl port-forward -n kubemind svc/kubemind-frontend 8080:80
# Access at: http://localhost:8080

# Option 2: Use Ingress (if configured)
# Access at: http://kubemind.example.com
```

### Backend API

```bash
kubectl port-forward -n kubemind svc/kubemind-backend 3000:8080
# Access at: http://localhost:3000
# Health check: http://localhost:3000/health
```

### Grafana Dashboards

```bash
kubectl port-forward -n kubemind svc/kubemind-grafana 3000:3000
# Access at: http://localhost:3000
# Username: admin
# Password: (from $GRAFANA_PASSWORD)
```

### Prometheus Metrics

```bash
kubectl port-forward -n kubemind svc/kubemind-prometheus 9090:9090
# Access at: http://localhost:9090
# Check targets: http://localhost:9090/targets
```

### Loki Logs

```bash
kubectl port-forward -n kubemind svc/kubemind-loki 3100:3100
# Access at: http://localhost:3100
```

### PostgreSQL Database

```bash
kubectl port-forward -n kubemind svc/kubemind-postgres 5432:5432
# Connect with:
# Host: localhost
# Port: 5432
# Database: kubemind_db
# Username: kubemind
# Password: (from $DB_PASSWORD)

# Or use psql directly:
kubectl run -it --rm psql --image=postgres:15-alpine --restart=Never -n kubemind -- \
  psql -h kubemind-postgres -U kubemind -d kubemind_db
```

---

## ⚙️ Configuration Examples

### Development Environment

```bash
helm install kubemind ./kubemind \
  --namespace kubemind-dev \
  --create-namespace \
  --set backend.replicaCount=1 \
  --set frontend.replicaCount=1 \
  --set database.postgres.persistence.size=5Gi \
  --set observability.prometheus.retention=3d
```

### Production Environment

```bash
helm install kubemind ./kubemind \
  --namespace kubemind \
  --create-namespace \
  --values prod-values.yaml \
  --set backend.secrets.database.password="$DB_PASSWORD" \
  --set observability.grafana.adminPassword="$GRAFANA_PASSWORD"
```

**prod-values.yaml**:
```yaml
backend:
  replicaCount: 5
  autoscaling:
    maxReplicas: 20
    targetCPUUtilizationPercentage: 70
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
    hosts:
      - host: kubemind.example.com

database:
  postgres:
    persistence:
      size: 100Gi
    backup:
      retention: 30

observability:
  prometheus:
    retention: 30d
```

### High Availability Setup

```bash
helm install kubemind ./kubemind \
  --namespace kubemind \
  --set backend.replicaCount=5 \
  --set backend.autoscaling.enabled=true \
  --set backend.autoscaling.maxReplicas=20 \
  --set frontend.replicaCount=3 \
  --set frontend.autoscaling.enabled=true \
  --set frontend.ingress.enabled=true \
  --set database.postgres.persistence.size=100Gi
```

---

## 🛠️ Common Management Tasks

### Scale Backend Service

```bash
# Automatic scaling (via HPA)
kubectl get hpa -n kubemind
kubectl describe hpa kubemind-backend-hpa -n kubemind

# Manual scaling
kubectl scale deployment kubemind-backend -n kubemind --replicas=5
```

### Update Configuration

```bash
# Update specific values
helm upgrade kubemind ./kubemind \
  --namespace kubemind \
  --set backend.replicaCount=5 \
  --set database.postgres.persistence.size=50Gi
```

### View Deployment History

```bash
# List all releases
helm list -n kubemind

# View release history
helm history kubemind -n kubemind

# Show values for current release
helm get values kubemind -n kubemind
```

### Rollback Deployment

```bash
# Rollback to previous version
helm rollback kubemind -n kubemind

# Rollback to specific revision
helm rollback kubemind 2 -n kubemind
```

### View Logs

```bash
# Backend logs
kubectl logs -n kubemind -l app=kubemind-backend -f

# Frontend logs
kubectl logs -n kubemind -l app=kubemind-frontend -f

# Database logs
kubectl logs -n kubemind kubemind-postgres-0 -f

# All logs
kubectl logs -n kubemind -l app=kubemind --all-containers=true
```

---

## 🔍 Troubleshooting

### Pod Not Starting

```bash
# Check pod status and events
kubectl describe pod -n kubemind <pod-name>

# View logs
kubectl logs -n kubemind <pod-name>

# Check if storage is available
kubectl get pvc -n kubemind
```

### Database Connection Issues

```bash
# Test database connectivity
kubectl run -it --rm debug --image=postgres:15-alpine --restart=Never -n kubemind -- \
  psql -h kubemind-postgres -U kubemind -d kubemind_db -c "SELECT version();"

# Check database pod
kubectl get pods -n kubemind -l component=database
kubectl logs -n kubemind kubemind-postgres-0
```

### Resource Issues

```bash
# Check node resources
kubectl top nodes

# Check pod resource usage
kubectl top pods -n kubemind

# Check available storage
kubectl get pvc -n kubemind
kubectl describe pvc -n kubemind
```

### Network Issues

```bash
# Test service DNS
kubectl run -it --rm curl --image=curlimages/curl --restart=Never -n kubemind -- \
  curl http://kubemind-backend:8080/health

# Check endpoints
kubectl get endpoints -n kubemind
```

---

## 📊 Monitoring and Observability

### Access Metrics

```bash
# Prometheus Metrics
kubectl port-forward -n kubemind svc/kubemind-prometheus 9090:9090
# Visit: http://localhost:9090/graph

# Example queries:
# Container CPU usage: rate(container_cpu_usage_seconds_total[5m])
# Pod memory usage: container_memory_usage_bytes
# Request rate: rate(http_requests_total[5m])
```

### View Logs

```bash
# Via Loki (in Grafana)
# Create new datasource: http://kubemind-loki:3100
# Query: {app="kubemind-backend"}

# Via kubectl
kubectl logs -n kubemind -l app=kubemind-backend -f
```

### Create Dashboards

1. Access Grafana: `kubectl port-forward -n kubemind svc/kubemind-grafana 3000:3000`
2. Add Prometheus datasource: `http://kubemind-prometheus:9090`
3. Add Loki datasource: `http://kubemind-loki:3100`
4. Create dashboards using existing templates or custom queries

---

## 🔐 Security Considerations

### Secret Management

```bash
# View secrets (base64 encoded)
kubectl get secrets -n kubemind
kubectl get secret kubemind-db-secret -n kubemind -o yaml

# Rotate passwords (create new secrets)
kubectl delete secret kubemind-db-secret -n kubemind
kubectl create secret generic kubemind-db-secret --from-literal=password=<new-password> -n kubemind
```

### Network Policies

```bash
# View network policies
kubectl get networkpolicies -n kubemind

# Apply custom network policies
kubectl apply -f network-policy.yaml -n kubemind
```

### RBAC

```bash
# View service accounts
kubectl get serviceaccounts -n kubemind

# View role bindings
kubectl get rolebindings -n kubemind
kubectl get clusterrolebindings -n kubemind
```

---

## 📈 Performance Optimization

### Resource Tuning

```yaml
# In values.yaml or via --set flags
backend:
  resources:
    requests:
      cpu: 2000m
      memory: 2Gi
    limits:
      cpu: 4000m
      memory: 4Gi

frontend:
  resources:
    requests:
      cpu: 500m
      memory: 512Mi
    limits:
      cpu: 1000m
      memory: 1Gi
```

### Autoscaling Configuration

```yaml
backend:
  autoscaling:
    enabled: true
    minReplicas: 3
    maxReplicas: 20
    targetCPUUtilizationPercentage: 70
    targetMemoryUtilizationPercentage: 80
```

### Storage Optimization

```bash
# Use faster storage classes for database
helm upgrade kubemind ./kubemind \
  --namespace kubemind \
  --set database.postgres.persistence.storageClass=fast-ssd
```

---

## 🧹 Cleanup and Uninstallation

### Uninstall Helm Release

```bash
# Uninstall the chart
helm uninstall kubemind -n kubemind

# Delete namespace
kubectl delete namespace kubemind

# Verify deletion
kubectl get namespaces
kubectl get all -n kubemind
```

### Backup Before Cleanup

```bash
# Backup all resources
kubectl get all -n kubemind -o yaml > kubemind-backup.yaml

# Backup database
kubectl exec -n kubemind kubemind-postgres-0 -- \
  pg_dump -U kubemind kubemind_db | gzip > kubemind-db-backup.sql.gz

# Backup persistent volumes
kubectl get pvc -n kubemind -o yaml > kubemind-pvcs-backup.yaml
```

---

## 📚 Additional Resources

- **Helm Official Documentation**: https://helm.sh/docs/
- **Kubernetes Documentation**: https://kubernetes.io/docs/
- **PostgreSQL Documentation**: https://www.postgresql.org/docs/
- **Prometheus Documentation**: https://prometheus.io/docs/
- **Grafana Documentation**: https://grafana.com/docs/grafana/latest/
- **Loki Documentation**: https://grafana.com/docs/loki/latest/

---

## ✨ Summary

**All Helm chart components have been successfully created and are ready for deployment!**

### Chart Contents:
- ✅ 13 total files (templates, configurations, documentation)
- ✅ 9 Kubernetes templates
- ✅ Complete backend, frontend, database, and observability stack
- ✅ Production-ready security and RBAC configurations
- ✅ Comprehensive documentation and installation guides

### Next Steps:
1. Configure values.yaml for your environment
2. Install using the deployment instructions above
3. Verify all services are running
4. Access monitoring dashboards (Grafana, Prometheus)
5. Configure backups and retention policies
6. Set up alerts in Prometheus
7. Configure CI/CD pipeline for automatic deployments

### Support:
For issues or questions, refer to:
- INSTALLATION_GUIDE.md - Detailed setup instructions
- QUICK_REFERENCE.md - Command reference
- README.md - Comprehensive documentation
- This deployment guide - End-to-end walkthrough
