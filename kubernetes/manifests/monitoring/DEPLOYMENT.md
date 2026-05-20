# Observability Stack Deployment Guide

## Overview

This observability stack provides comprehensive monitoring and logging for the KubeMind AI Kubernetes cluster:

- **Prometheus**: Metrics collection and time-series database
- **Grafana**: Visualization and dashboard management
- **Loki**: Log aggregation and querying
- **Node Exporter**: System-level metrics (CPU, memory, disk, network)
- **Kube-state-metrics**: Kubernetes state metrics (pods, deployments, etc.)

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                   Monitoring Stack                          │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌─────────────┐  ┌──────────┐  ┌──────┐                   │
│  │ Prometheus  │  │ Grafana  │  │ Loki │                   │
│  │ (TSDB)      │  │ (UI)     │  │(Logs)│                   │
│  └──────┬──────┘  └────┬─────┘  └──┬───┘                   │
│         │              │           │                        │
│  ┌──────▼──────────────▼───────────▼────────┐              │
│  │  Scrape Targets & Log Collectors         │              │
│  │  ├─ Node Exporter (system metrics)       │              │
│  │  ├─ Kube-state-metrics (K8s objects)     │              │
│  │  ├─ Kubernetes API server                │              │
│  │  ├─ Pods with prometheus.io annotations  │              │
│  │  └─ Log shipper (Promtail) → Loki       │              │
│  └─────────────────────────────────────────┘              │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

## Namespace Setup

All components run in the `kubemind` namespace:

```bash
kubectl create namespace kubemind
```

## File Structure

```
kubernetes/manifests/monitoring/
├── prometheus-deployment.yaml       # Prometheus with scrape configs
├── prometheus-rules.yaml            # Alert and recording rules
├── grafana-deployment.yaml          # Grafana with datasources
├── loki-deployment.yaml             # Loki log aggregation
├── node-exporter.yaml               # Node metrics (DaemonSet)
├── kube-state-metrics.yaml          # K8s state metrics
└── DEPLOYMENT.md                    # This file
```

## Component Details

### 1. Prometheus Deployment

**File**: `prometheus-deployment.yaml`

- **Type**: StatefulSet with persistent storage (50Gi)
- **Replicas**: 1
- **Port**: 9090
- **Storage**: TSDB with 30-day retention
- **Scrape Configs**:
  - Kubernetes API server
  - Node metrics
  - Pod annotations (`prometheus.io/scrape=true`)
  - Node Exporter
  - Kube-state-metrics
  - cAdvisor metrics from kubelet

**Resources**:
- Request: 500m CPU, 512Mi memory
- Limit: 2000m CPU, 2Gi memory

**Health Checks**:
- Liveness: `/-/healthy` (30s delay, 10s interval)
- Readiness: `/-/ready` (5s delay, 5s interval)

### 2. Grafana Deployment

**File**: `grafana-deployment.yaml`

- **Type**: Deployment with persistent storage (10Gi)
- **Replicas**: 1
- **Port**: 3000
- **Default Admin**: admin / kubemind-admin-2024
- **Service Type**: LoadBalancer (external access)

**Datasources Pre-configured**:
- Prometheus (http://prometheus:9090)
- Loki (http://loki:3100)

**Resources**:
- Request: 100m CPU, 128Mi memory
- Limit: 500m CPU, 512Mi memory

**Health Checks**:
- Liveness: `/api/health` (30s delay, 10s interval)
- Readiness: `/api/health` (10s delay, 5s interval)

### 3. Loki Deployment

**File**: `loki-deployment.yaml`

- **Type**: StatefulSet with persistent storage (50Gi)
- **Replicas**: 1
- **Port**: 3100
- **Storage**: Filesystem-based (BoltDB + filesystem)
- **Retention**: 30 days
- **Max ingestion rate**: 100MB/s with 200MB/s burst

**Resources**:
- Request: 250m CPU, 256Mi memory
- Limit: 1000m CPU, 1Gi memory

**Health Checks**:
- Liveness: `/ready` (30s delay, 10s interval)
- Readiness: `/ready` (10s delay, 5s interval)

### 4. Node Exporter DaemonSet

**File**: `node-exporter.yaml`

- **Type**: DaemonSet (runs on all nodes)
- **Port**: 9100
- **Access**: Host network, PID, IPC
- **Tolerations**: All taints to ensure universal deployment

**Metrics Collected**:
- CPU, memory, disk usage
- Network I/O
- System load
- File descriptor usage
- Process counts

**Resources**:
- Request: 100m CPU, 64Mi memory
- Limit: 200m CPU, 128Mi memory

### 5. Kube-state-metrics Deployment

**File**: `kube-state-metrics.yaml`

- **Type**: Deployment
- **Replicas**: 1
- **Port**: 8080 (metrics), 8081 (telemetry)
- **ServiceAccount**: Has cluster-wide read access

**Metrics Collected**:
- Deployment replicas and status
- Pod phases and conditions
- StatefulSet status
- DaemonSet status
- Job completions
- Node capacity and conditions
- PVC usage
- Service endpoints

**Resources**:
- Request: 100m CPU, 128Mi memory
- Limit: 500m CPU, 256Mi memory

### 6. Alert and Recording Rules

**File**: `prometheus-rules.yaml`

**Alert Rules**:
- Pod health alerts
- Memory/CPU usage warnings
- Node disk/memory pressure
- Node readiness
- PVC usage
- Prometheus scrape failures

**Recording Rules**:
- CPU utilization
- Memory utilization
- Container resource usage aggregations

## Deployment Instructions

### Prerequisites

1. Kubernetes cluster running (1.20+)
2. kubectl configured to access cluster
3. `kubemind` namespace exists
4. Storage provisioner available (or manual PVs created)

### Step 1: Create Namespace (if not exists)

```bash
kubectl create namespace kubemind
```

### Step 2: Apply Prometheus Rules and Secrets

```bash
kubectl apply -f prometheus-rules.yaml
```

This creates:
- Alert and recording rules ConfigMap
- Grafana credentials Secret
- Storage classes and PVCs

### Step 3: Deploy Prometheus

```bash
kubectl apply -f prometheus-deployment.yaml
```

Verify:
```bash
kubectl get statefulsets -n kubemind
kubectl get pods -n kubemind | grep prometheus
kubectl get pvc -n kubemind | grep prometheus
```

### Step 4: Deploy Loki

```bash
kubectl apply -f loki-deployment.yaml
```

Verify:
```bash
kubectl get statefulsets -n kubemind
kubectl get pods -n kubemind | grep loki
kubectl get pvc -n kubemind | grep loki
```

### Step 5: Deploy Node Exporter

```bash
kubectl apply -f node-exporter.yaml
```

Verify:
```bash
kubectl get daemonsets -n kubemind
kubectl get pods -n kubemind | grep node-exporter
```

### Step 6: Deploy Kube-state-metrics

```bash
kubectl apply -f kube-state-metrics.yaml
```

Verify:
```bash
kubectl get deployments -n kubemind
kubectl get pods -n kubemind | grep kube-state-metrics
```

### Step 7: Deploy Grafana

```bash
kubectl apply -f grafana-deployment.yaml
```

Verify:
```bash
kubectl get deployments -n kubemind
kubectl get pods -n kubemind | grep grafana
kubectl get svc -n kubemind grafana
```

### Complete Deployment

Deploy all at once:

```bash
kubectl apply -f prometheus-rules.yaml \
  -f prometheus-deployment.yaml \
  -f loki-deployment.yaml \
  -f node-exporter.yaml \
  -f kube-state-metrics.yaml \
  -f grafana-deployment.yaml
```

## Accessing Services

### Prometheus

```bash
kubectl port-forward -n kubemind svc/prometheus 9090:9090
# Access: http://localhost:9090
```

### Grafana

```bash
kubectl port-forward -n kubemind svc/grafana 3000:3000
# Access: http://localhost:3000
# Login: admin / kubemind-admin-2024
```

Or via LoadBalancer (if available):
```bash
kubectl get svc -n kubemind grafana
# Use EXTERNAL-IP:3000
```

### Loki

```bash
kubectl port-forward -n kubemind svc/loki 3100:3100
# Access: http://localhost:3100/loki/api/v1/label
```

### Node Exporter

```bash
kubectl port-forward -n kubemind svc/node-exporter 9100:9100
# Access: http://localhost:9100/metrics
```

### Kube-state-metrics

```bash
kubectl port-forward -n kubemind svc/kube-state-metrics 8080:8080
# Access: http://localhost:8080/metrics
```

## Monitoring Health

### Check Pod Status

```bash
kubectl get pods -n kubemind -l app in (prometheus,grafana,loki,node-exporter,kube-state-metrics) -w
```

### Check Pod Logs

```bash
# Prometheus
kubectl logs -n kubemind -l app=prometheus --tail=100 -f

# Grafana
kubectl logs -n kubemind -l app=grafana --tail=100 -f

# Loki
kubectl logs -n kubemind -l app=loki --tail=100 -f

# Node Exporter
kubectl logs -n kubemind -l app=node-exporter --tail=50 -f

# Kube-state-metrics
kubectl logs -n kubemind -l app=kube-state-metrics --tail=100 -f
```

### Check PVC Status

```bash
kubectl get pvc -n kubemind
kubectl describe pvc -n kubemind
```

## Grafana Configuration

### Step 1: Add Prometheus Datasource

Already pre-configured, but to verify/reconfigure:

1. Access Grafana: http://localhost:3000
2. Login: admin / kubemind-admin-2024
3. Configuration → Datasources
4. Check Prometheus datasource pointing to `http://prometheus:9090`

### Step 2: Add Loki Datasource

Already pre-configured, but to verify/reconfigure:

1. Configuration → Datasources
2. Check Loki datasource pointing to `http://loki:3100`

### Step 3: Import Dashboards

Pre-built dashboard options:

1. Go to Dashboards → Import
2. Import by ID (examples):
   - 3662: Prometheus 2.0 Stats
   - 1471: Node Exporter Full
   - 7645: Kubernetes Cluster Monitoring

Or create custom dashboards using:
- Prometheus metrics (node_*, container_*, kube_*)
- Loki log queries

## Prometheus Scrape Config Details

### Pod Annotations

For Prometheus to scrape pods, add annotations:

```yaml
pod:
  metadata:
    annotations:
      prometheus.io/scrape: "true"      # Enable scraping
      prometheus.io/port: "8080"        # Metrics port
      prometheus.io/path: "/metrics"    # Metrics path (optional, default: /metrics)
```

### Kubernetes Objects

Prometheus discovers and scrapes:
- **Pods**: Using pod service discovery and annotations
- **Nodes**: Via kubelet /metrics/cadvisor endpoints
- **API Server**: Via Kubernetes API server metrics
- **Exporters**: Node Exporter, Kube-state-metrics via service discovery

## Troubleshooting

### Prometheus Not Scraping Targets

1. Check pod annotations:
```bash
kubectl get pods -A -o json | grep -A5 'prometheus.io'
```

2. Check Prometheus targets: http://prometheus:9090/targets

3. Verify network connectivity:
```bash
kubectl run -it debug --image=busybox --restart=Never -- sh
# Inside pod:
wget http://prometheus:9090/metrics
wget http://node-exporter:9100/metrics
```

### Grafana Can't Connect to Prometheus

1. Check Prometheus is running:
```bash
kubectl get pods -n kubemind | grep prometheus
```

2. Check Prometheus service:
```bash
kubectl get svc -n kubemind prometheus
```

3. Test DNS resolution:
```bash
kubectl run -it debug --image=busybox --restart=Never -- nslookup prometheus.kubemind
```

### High Memory Usage

1. Check Prometheus TSDB retention:
```yaml
args:
  - '--storage.tsdb.retention.size=50GB'  # Adjust size
```

2. Check Loki retention:
```yaml
retention_period: 720h  # Adjust retention period
```

3. Reduce scrape interval if needed:
```yaml
scrape_interval: 30s  # Increase from 15s
```

### Storage Issues

1. Check PVC status:
```bash
kubectl get pvc -n kubemind
kubectl describe pvc -n kubemind prometheus-pvc
```

2. Check node disk space:
```bash
kubectl get nodes -o json | grep -A5 "allocatable"
```

3. Resize PVC if needed:
```bash
kubectl patch pvc prometheus-pvc -n kubemind -p '{"spec":{"resources":{"requests":{"storage":"100Gi"}}}}'
```

## Kubernetes Best Practices Implemented

### Security

- ✅ Non-root containers (runAsUser: 65534 for Prometheus)
- ✅ ReadOnly root filesystem where possible
- ✅ RBAC with minimal required permissions
- ✅ Service accounts with restricted cluster roles
- ✅ Network policies (can be added)
- ✅ Resource quotas (recommended to add)
- ✅ Pod security policies (recommended to add)

### Reliability

- ✅ StatefulSets for stateful services (Prometheus, Loki)
- ✅ DaemonSets for node-level collection (Node Exporter)
- ✅ Persistent volumes for data durability
- ✅ Resource requests and limits
- ✅ Health checks (liveness, readiness)
- ✅ Rolling update strategy
- ✅ PVC claim templates

### Observability

- ✅ Prometheus metrics exposure
- ✅ Service annotations for Prometheus discovery
- ✅ Comprehensive alert rules
- ✅ Recording rules for performance
- ✅ Structured logging
- ✅ Proper labeling

### Scalability

- ✅ StatefulSet replicas (can be scaled)
- ✅ DaemonSet for node-level collection
- ✅ Configurable retention policies
- ✅ Persistent storage with size limits
- ✅ Resource requests prevent overallocation

### Configuration

- ✅ ConfigMaps for configuration
- ✅ Secrets for credentials
- ✅ Environment variables
- ✅ Service discovery
- ✅ Namespace isolation

## Performance Tuning

### For Large Clusters (100+ nodes)

1. Increase Prometheus resources:
```yaml
resources:
  requests:
    cpu: 2000m
    memory: 2Gi
  limits:
    cpu: 4000m
    memory: 4Gi
```

2. Increase scrape interval:
```yaml
scrape_interval: 30s
evaluation_interval: 30s
```

3. Increase storage:
```yaml
storage.tsdb.retention.size: 100GB
```

4. Consider Prometheus federation or clustering

### For Resource-Constrained Environments

1. Reduce resources:
```yaml
resources:
  requests:
    cpu: 100m
    memory: 128Mi
  limits:
    cpu: 500m
    memory: 256Mi
```

2. Reduce retention:
```yaml
storage.tsdb.retention.time: 7d
```

3. Reduce scrape targets
4. Disable unnecessary collectors in Node Exporter

## Next Steps

1. Configure alert routing (Alertmanager)
2. Set up log aggregation with Promtail
3. Create custom dashboards
4. Set up backup procedures for Prometheus TSDB
5. Configure TLS for service communication
6. Set up persistent volume backups
7. Implement network policies
8. Add pod security policies
9. Set up audit logging
10. Configure cost monitoring

## Cleanup

To remove all monitoring components:

```bash
kubectl delete namespace kubemind
```

Or selectively:

```bash
kubectl delete -n kubemind deployment grafana
kubectl delete -n kubemind statefulset prometheus loki
kubectl delete -n kubemind daemonset node-exporter
kubectl delete -n kubemind configmap prometheus-config prometheus-rules
kubectl delete -n kubemind secret grafana-credentials
```

## Support

For issues, check:
1. Pod logs: `kubectl logs -n kubemind <pod-name>`
2. Pod events: `kubectl describe pod -n kubemind <pod-name>`
3. Prometheus targets: http://prometheus:9090/targets
4. Prometheus configuration: http://prometheus:9090/config
5. Grafana error logs: Grafana UI → Configuration → Logs

## References

- [Prometheus Documentation](https://prometheus.io/docs/)
- [Grafana Documentation](https://grafana.com/docs/)
- [Loki Documentation](https://grafana.com/docs/loki/)
- [Node Exporter README](https://github.com/prometheus/node_exporter)
- [Kube-state-metrics README](https://github.com/kubernetes/kube-state-metrics)
