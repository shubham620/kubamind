# Kubernetes Manifest Validation & Best Practices

This document outlines the validation criteria and best practices implemented in the observability stack manifests.

## Manifest Validation Checklist

### ✅ Container Images

- [x] Specific version tags used (not `latest`)
  - Prometheus: `v2.45.0`
  - Grafana: `10.2.0`
  - Loki: `2.9.0`
  - Node Exporter: `v1.6.1`
  - Kube-state-metrics: `v2.10.0`
- [x] Public, well-maintained images from trusted registries
  - `prom/prometheus` - Official Prometheus
  - `grafana/grafana` - Official Grafana
  - `grafana/loki` - Official Grafana Loki
  - `prom/node-exporter` - Official Prometheus Node Exporter
  - `registry.k8s.io/kube-state-metrics` - Official Kubernetes

### ✅ Resource Management

#### Resource Requests
- [x] CPU requests defined for all containers
- [x] Memory requests defined for all containers
- [x] Requests appropriate for component size

#### Resource Limits
- [x] CPU limits defined for all containers
- [x] Memory limits defined for all containers
- [x] Limits prevent cluster resource exhaustion
- [x] Limits > requests to avoid throttling

**Defined Resources**:

| Component | CPU Request | CPU Limit | Memory Request | Memory Limit |
|-----------|-------------|-----------|----------------|--------------|
| Prometheus | 500m | 2000m | 512Mi | 2Gi |
| Grafana | 100m | 500m | 128Mi | 512Mi |
| Loki | 250m | 1000m | 256Mi | 1Gi |
| Node Exporter | 100m | 200m | 64Mi | 128Mi |
| Kube-state-metrics | 100m | 500m | 128Mi | 256Mi |

### ✅ Health Checks

#### Liveness Probes
- [x] Defined for all stateful components
- [x] Appropriate delay (30s for heavy components, 10-30s for others)
- [x] Reasonable period (10-30s)
- [x] Reasonable timeout (5s)
- [x] Failure threshold (3)

#### Readiness Probes
- [x] Defined for all components
- [x] Appropriate delay (5-10s)
- [x] Reasonable period (5-10s)
- [x] Reasonable timeout (5s)
- [x] Failure threshold (3)

**Probe Endpoints**:
- Prometheus: `/-/healthy` (liveness), `/-/ready` (readiness)
- Grafana: `/api/health` (both)
- Loki: `/ready` (both)
- Node Exporter: `/` (both)
- Kube-state-metrics: `/healthz` (liveness), `/` (readiness)

### ✅ Storage Configuration

#### Persistent Volumes
- [x] PVC for Prometheus (50Gi)
- [x] PVC for Grafana (10Gi)
- [x] PVC for Loki (50Gi)
- [x] Appropriate access modes (ReadWriteOnce)
- [x] Proper storage class (standard)

#### Volume Mounting
- [x] Volumes properly mounted
- [x] Mount paths appropriate
- [x] No overlapping mount points
- [x] RW access where needed, RO where possible

#### StatefulSet Configuration
- [x] StatefulSets use volumeClaimTemplates
- [x] Headless services for StatefulSets
- [x] Service names match StatefulSet names

### ✅ Security Configuration

#### SecurityContext
- [x] Non-root users where applicable
  - Prometheus: runAsUser 65534 (nobody)
  - Grafana: runAsUser 472
  - Loki: runAsUser 10001
  - Node Exporter: runAsUser 0 (required for host metrics)
- [x] fsGroup set appropriately
- [x] runAsNonRoot: true (except Node Exporter which needs host access)
- [x] No privileged containers

#### RBAC (Role-Based Access Control)
- [x] ServiceAccounts created
- [x] ClusterRoles with minimal permissions
  - Prometheus: read nodes, pods, services, endpoints
  - Node Exporter: read nodes
  - Kube-state-metrics: read all Kubernetes objects
- [x] ClusterRoleBindings properly configured
- [x] Least privilege principle applied

#### Host Access
- [x] Only Node Exporter has host network/PID/IPC access (by design)
- [x] Other containers restricted
- [x] Host paths mounted read-only where possible

### ✅ Networking

#### Service Configuration
- [x] Services properly defined
- [x] Selectors match pod labels
- [x] Port mappings correct
- [x] Service types appropriate
  - Prometheus: ClusterIP (internal)
  - Grafana: LoadBalancer (external) + ClusterIP (internal)
  - Loki: ClusterIP (internal)
  - Exporters: ClusterIP or headless services

#### Service Discovery
- [x] Kubernetes SD config for Prometheus
- [x] Annotation-based scraping supported
- [x] Endpoint discovery configured

#### DNS
- [x] Services use DNS names for discovery
- [x] Cross-namespace references use FQDN

### ✅ Labels and Annotations

#### Kubernetes Labels
- [x] app label on all resources
- [x] version label for tracking
- [x] Consistent label scheme
- [x] Labels enable selection

**Standard Labels**:
```yaml
labels:
  app: <component-name>
  version: v1
```

#### Annotations
- [x] Prometheus scrape annotations on pods
- [x] Annotation values correct types
- [x] Compatible with Prometheus service discovery

**Prometheus Annotations**:
```yaml
prometheus.io/scrape: "true"
prometheus.io/port: "8080"
prometheus.io/path: "/metrics"
```

### ✅ Namespace & Environment

#### Namespace Configuration
- [x] All resources in kubemind namespace
- [x] Namespace references explicit
- [x] No cluster-wide permissions for namespace-scoped resources

#### Environment Variables
- [x] TZ set to UTC for consistency
- [x] Sensitive data in Secrets, not ConfigMaps
- [x] Appropriate default values

### ✅ Configuration Management

#### ConfigMaps
- [x] Prometheus scrape configs in ConfigMap
- [x] Alert and recording rules in ConfigMap
- [x] Grafana datasources in ConfigMap
- [x] Grafana dashboards in ConfigMap
- [x] Loki configuration in ConfigMap

#### Secrets
- [x] Grafana admin password in Secret
- [x] Secret type: Opaque
- [x] Using stringData for plaintext

### ✅ Deployment Strategies

#### StatefulSets
- [x] Prometheus (stateful - TSDB)
- [x] Loki (stateful - storage)
- [x] Service names specified
- [x] PVC templates defined
- [x] Replicas set appropriately (1 for single instance)

#### DaemonSets
- [x] Node Exporter (node-level collection)
- [x] Proper selector
- [x] Tolerations for node taints

#### Deployments
- [x] Grafana (stateless from infrastructure perspective)
- [x] Kube-state-metrics (stateless)
- [x] RollingUpdate strategy
- [x] maxSurge: 1, maxUnavailable: 0

### ✅ Scheduling & Affinity

#### Node Selection
- [x] Tolerations for Node Exporter (all nodes)
- [x] No NodeSelector (allows any node)
- [x] Pod anti-affinity optional (can be added)

#### Taints & Tolerations
- [x] Node Exporter tolerates all taints
- [x] Other components have no special tolerations

### ✅ Data Management

#### TSDB Retention (Prometheus)
- [x] Time-based retention: 30 days
- [x] Size-based retention: 50GB
- [x] Both limits prevent unbounded storage

#### Log Retention (Loki)
- [x] 30-day (720h) retention configured
- [x] Max ingestion rate: 100MB/s
- [x] Burst size: 200MB/s

#### Volume Cleanup
- [x] Unused PVCs can be deleted
- [x] PVC reclaim policy should be Delete

### ✅ Logging & Monitoring

#### Prometheus Metrics
- [x] All components expose metrics
- [x] Correct metric paths
- [x] Prometheus discovery configured

#### Component Logging
- [x] Logs sent to stdout (Kubernetes captures)
- [x] Log levels appropriate
- [x] JSON format option available (Prometheus)

### ✅ API Versions

- [x] All resources use v1 or v1 for stable APIs
  - `v1` for ConfigMap, Secret, Service, PersistentVolumeClaim
  - `apps/v1` for Deployment, StatefulSet, DaemonSet
  - `rbac.authorization.k8s.io/v1` for RBAC
  - `storage.k8s.io/v1` for StorageClass

## Kubernetes Best Practices Scorecard

### Core Best Practices

| Practice | Status | Details |
|----------|--------|---------|
| Use specific image tags | ✅ | v2.45.0, 10.2.0, etc. |
| Use resource requests/limits | ✅ | All containers defined |
| Implement health checks | ✅ | Liveness and readiness probes |
| Use non-root users | ✅ | Except Node Exporter (required) |
| Implement RBAC | ✅ | Minimal permissions |
| Use persistent volumes | ✅ | Stateful data persisted |
| Use ConfigMaps/Secrets | ✅ | Configuration externalized |
| Use StatefulSets for state | ✅ | Prometheus and Loki |
| Use DaemonSets for node-level | ✅ | Node Exporter |
| Label resources | ✅ | Standard app/version labels |
| Update strategy | ✅ | RollingUpdate configured |
| Namespace isolation | ✅ | kubemind namespace |
| API stability | ✅ | Only stable API versions |

### Security Best Practices

| Practice | Status | Details |
|----------|--------|---------|
| SecurityContext | ✅ | Non-root, fsGroup set |
| RBAC | ✅ | Least privilege |
| Network policies | ⚠️ | Optional, can be added |
| Pod security policies | ⚠️ | Optional, can be added |
| Secret management | ✅ | Credentials in Secrets |
| Resource quotas | ⚠️ | Can be added to namespace |
| NetworkPolicy | ⚠️ | Recommended |

### Operational Best Practices

| Practice | Status | Details |
|----------|--------|---------|
| Readiness probes | ✅ | Prevents traffic to unready pods |
| Liveness probes | ✅ | Automatic recovery |
| Logging | ✅ | stdout/stderr |
| Monitoring | ✅ | Prometheus metrics |
| Alerting | ✅ | Alert rules defined |
| Retention policies | ✅ | TSDB and logs |
| Backup strategy | ⚠️ | Recommended to add |

## Optional Enhancements

### 1. Pod Disruption Budgets (PDB)

Add PDB for critical components:

```yaml
apiVersion: policy/v1
kind: PodDisruptionBudget
metadata:
  name: prometheus-pdb
  namespace: kubemind
spec:
  minAvailable: 1
  selector:
    matchLabels:
      app: prometheus
```

### 2. Network Policies

Restrict traffic to monitoring stack:

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: monitoring-network-policy
  namespace: kubemind
spec:
  podSelector:
    matchLabels:
      app: prometheus
  policyTypes:
  - Ingress
  - Egress
  ingress:
  - from:
    - podSelector:
        matchLabels:
          app: grafana
```

### 3. Pod Security Policy (if using)

```yaml
apiVersion: policy/v1beta1
kind: PodSecurityPolicy
metadata:
  name: monitoring-restricted
spec:
  privileged: false
  allowPrivilegeEscalation: false
  requiredDropCapabilities:
  - ALL
  runAsUser:
    rule: MustRunAsNonRoot
  seLinux:
    rule: MustRunAs
  fsGroup:
    rule: MustRunAs
```

### 4. Resource Quotas

```yaml
apiVersion: v1
kind: ResourceQuota
metadata:
  name: monitoring-quota
  namespace: kubemind
spec:
  hard:
    requests.cpu: "4"
    requests.memory: "4Gi"
    limits.cpu: "8"
    limits.memory: "8Gi"
    pods: "20"
```

### 5. Horizontal Pod Autoscaling

For stateless components (Grafana, Kube-state-metrics):

```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: grafana-hpa
  namespace: kubemind
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: grafana
  minReplicas: 1
  maxReplicas: 3
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 80
```

### 6. TLS for External Access

Add Ingress with TLS:

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: monitoring-ingress
  namespace: kubemind
spec:
  tls:
  - hosts:
    - grafana.example.com
    secretName: grafana-tls
  rules:
  - host: grafana.example.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: grafana
            port:
              number: 3000
```

## Validation Commands

### Syntax Validation

```bash
# Validate YAML syntax
kubectl apply -f prometheus-deployment.yaml --validate=client -o yaml
kubectl apply -f grafana-deployment.yaml --validate=client -o yaml
kubectl apply -f loki-deployment.yaml --validate=client -o yaml
kubectl apply -f node-exporter.yaml --validate=client -o yaml
kubectl apply -f kube-state-metrics.yaml --validate=client -o yaml
kubectl apply -f prometheus-rules.yaml --validate=client -o yaml
```

### API Validation

```bash
# Validate against API server
kubectl apply -f *.yaml --validate=true --dry-run=server
```

### Lint with kubelint

```bash
kubelint prometheus-deployment.yaml
kubelint grafana-deployment.yaml
kubelint loki-deployment.yaml
kubelint node-exporter.yaml
kubelint kube-state-metrics.yaml
```

### Check Resource Requests

```bash
# After deployment
kubectl describe nodes -n kubemind
kubectl top nodes
kubectl top pods -n kubemind
```

## Verification Checklist After Deployment

- [ ] All pods in Running state: `kubectl get pods -n kubemind`
- [ ] All PVCs Bound: `kubectl get pvc -n kubemind`
- [ ] All services created: `kubectl get svc -n kubemind`
- [ ] Prometheus targets healthy: `kubectl port-forward -n kubemind svc/prometheus 9090:9090` → http://localhost:9090/targets
- [ ] Prometheus scraping data: http://localhost:9090/graph
- [ ] Grafana accessible: http://localhost:3000
- [ ] Grafana can reach Prometheus datasource
- [ ] Loki accessible: http://localhost:3100/ready
- [ ] Node Exporter metrics available: http://localhost:9100/metrics
- [ ] Kube-state-metrics available: http://localhost:8080/metrics
- [ ] Pod logs clean (no errors): `kubectl logs -n kubemind <pod-name>`
- [ ] Storage is being used: `kubectl exec -n kubemind prometheus-0 -- df /prometheus`

## Performance Metrics

Expected resource usage (with default scrape interval of 15s):

| Component | CPU (avg) | Memory (avg) | Disk/Storage |
|-----------|-----------|--------------|--------------|
| Prometheus | 100-300m | 400-600Mi | 50GB (configured) |
| Grafana | 50-100m | 150-250Mi | 10Gi (configured) |
| Loki | 50-150m | 200-400Mi | 50GB (configured) |
| Node Exporter | 10-50m | 30-60Mi | None |
| Kube-state-metrics | 20-80m | 100-200Mi | None |

*Note: These are estimates and will vary based on cluster size and configuration*

## Conclusion

This observability stack follows Kubernetes best practices for:
- Container orchestration
- Security
- Resource management
- Reliability and availability
- Scalability and performance
- Operational excellence

All manifests are production-ready with recommended enhancements documented for further hardening.
