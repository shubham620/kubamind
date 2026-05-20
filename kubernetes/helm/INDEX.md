# KubeMind AI Helm Charts - Index & Documentation Hub

## 📑 Documentation Index

Welcome to the KubeMind AI Helm Charts documentation. This index will guide you through all available resources.

---

## 🚀 Quick Start (Choose Your Path)

### I just want to deploy it (5 minutes)
👉 Start here: **[QUICK_REFERENCE.md](./QUICK_REFERENCE.md)**
- Chart overview
- Installation command
- Common commands
- Key ports and access methods

### I want detailed setup instructions (15 minutes)
👉 Go here: **[INSTALLATION_GUIDE.md](./INSTALLATION_GUIDE.md)**
- Prerequisites checklist
- Step-by-step installation
- Three installation methods (Dev, Prod, GitOps)
- Troubleshooting section
- Advanced configuration

### I want complete understanding (30 minutes)
👉 Read this: **[DEPLOYMENT_GUIDE.md](./DEPLOYMENT_GUIDE.md)**
- Full deployment walkthrough
- All configuration examples
- Management tasks
- Monitoring setup
- Security considerations
- Backup and recovery

### I want in-depth chart documentation (Reference)
👉 Check: **[kubemind/README.md](./kubemind/README.md)**
- Complete feature list
- All configuration parameters
- Usage examples
- Architecture diagram
- Performance tuning
- Security implementation

---

## 📁 Chart Structure Overview

```
kubernetes/
└── helm/
    ├── QUICK_REFERENCE.md              ← Quick commands
    ├── INSTALLATION_GUIDE.md           ← Setup instructions
    ├── DEPLOYMENT_GUIDE.md             ← Complete walkthrough
    ├── INDEX.md                        ← You are here
    └── kubemind/                       ← Main Helm chart
        ├── Chart.yaml                  ← Chart metadata
        ├── values.yaml                 ← Configuration (5.6 KB)
        ├── README.md                   ← Full documentation
        └── templates/                  ← Kubernetes templates
            ├── _helpers.tpl            ← Helpers
            ├── backend-deployment.yaml ← Backend service
            ├── frontend-deployment.yaml← Frontend service
            ├── database-deployment.yaml← PostgreSQL
            ├── observability-deployment.yaml ← Prometheus/Grafana/Loki
            ├── configmaps.yaml         ← Configurations
            ├── secrets.yaml            ← Secrets
            ├── rbac.yaml               ← Security
            ├── NOTES.txt               ← Installation notes
            └── services/
                └── kubemind-services.yaml ← Services & Ingress
```

---

## 📋 File Descriptions

### Documentation Files

| File | Purpose | Audience | Time |
|------|---------|----------|------|
| **QUICK_REFERENCE.md** | Command reference & quick start | All | 5 min |
| **INSTALLATION_GUIDE.md** | Detailed setup & troubleshooting | DevOps/Operators | 15 min |
| **DEPLOYMENT_GUIDE.md** | Complete deployment walkthrough | Engineers | 30 min |
| **kubemind/README.md** | Full technical documentation | Developers | Reference |

### Chart Files

| File | Purpose | Size |
|------|---------|------|
| `Chart.yaml` | Chart metadata and version info | 396 B |
| `values.yaml` | Default configuration parameters | 5.6 KB |
| `_helpers.tpl` | Helm template helper functions | 1.7 KB |

### Template Files

| File | Components | Features |
|------|------------|----------|
| `backend-deployment.yaml` | Backend pod + HPA | Scaling, health checks, metrics |
| `frontend-deployment.yaml` | Frontend pod + HPA | Scaling, liveness probes |
| `database-deployment.yaml` | PostgreSQL + backups | Persistence, automated backups |
| `observability-deployment.yaml` | Prometheus, Grafana, Loki | Monitoring, logging, visualization |
| `configmaps.yaml` | All configurations | Prometheus, Loki, app config |
| `secrets.yaml` | Password management | DB password, Grafana admin |
| `rbac.yaml` | ServiceAccount, roles | Security, permissions |
| `services/kubemind-services.yaml` | All services + Ingress | Networking, load balancing |
| `NOTES.txt` | Post-install instructions | Setup verification |

---

## 🎯 Common Tasks

### Installation & Deployment

```bash
# Quick install
helm install kubemind ./kubemind --namespace kubemind \
  --set backend.secrets.database.password=pwd \
  --set observability.grafana.adminPassword=pwd

# See detailed instructions
→ INSTALLATION_GUIDE.md → "Installation Steps"
```

### Access Services

```bash
# Port forward to services
kubectl port-forward -n kubemind svc/kubemind-frontend 8080:80
kubectl port-forward -n kubemind svc/kubemind-backend 3000:8080

# See all access methods
→ QUICK_REFERENCE.md → "Common Helm Commands"
```

### Troubleshooting

```bash
# Check pod status
kubectl get pods -n kubemind

# View logs
kubectl logs -n kubemind <pod-name>

# See detailed troubleshooting
→ INSTALLATION_GUIDE.md → "Troubleshooting"
→ QUICK_REFERENCE.md → "Troubleshooting Guide"
```

### Configuration Changes

```bash
# Update deployment
helm upgrade kubemind ./kubemind --namespace kubemind \
  --set backend.replicaCount=5

# See configuration options
→ kubemind/README.md → "Configuration"
→ kubemind/values.yaml → All parameters
```

### Monitoring & Logs

```bash
# Access Grafana
kubectl port-forward -n kubemind svc/kubemind-grafana 3000:3000

# See full setup
→ DEPLOYMENT_GUIDE.md → "Monitoring and Observability"
```

---

## 📚 Learning Path

### For Complete Beginners
1. Read: QUICK_REFERENCE.md (5 min)
2. Read: INSTALLATION_GUIDE.md (15 min)
3. Do: Follow installation steps
4. Explore: Access services via port-forward
5. Reference: Use QUICK_REFERENCE.md for commands

### For Experienced DevOps Engineers
1. Skim: QUICK_REFERENCE.md (2 min)
2. Review: kubemind/values.yaml (5 min)
3. Check: kubemind/templates/ (understand structure)
4. Deploy: Run installation command
5. Customize: Modify values.yaml for your environment

### For Developers/Integrators
1. Read: kubemind/README.md (full understanding)
2. Review: DEPLOYMENT_GUIDE.md (complete workflow)
3. Study: Template files (implementation details)
4. Test: Deploy to development cluster
5. Integrate: CI/CD pipeline setup

### For Operations/SREs
1. Read: INSTALLATION_GUIDE.md (full setup)
2. Read: DEPLOYMENT_GUIDE.md (management tasks)
3. Study: Backup & recovery procedures
4. Setup: Monitoring and alerting
5. Document: Custom runbooks for your environment

---

## 🔍 Feature Reference

### By Category

**Scaling & Performance**
- Horizontal Pod Autoscaler (HPA)
- Resource requests and limits
- Multi-replica deployments
- Load balancing

👉 See: kubemind/README.md → "Performance Tuning"

**Security**
- RBAC configuration
- Secret management
- Non-root users
- Read-only filesystems
- Network policies

👉 See: kubemind/README.md → "Security Considerations"

**Observability**
- Prometheus metrics collection
- Grafana dashboards
- Loki log aggregation
- Health checks

👉 See: DEPLOYMENT_GUIDE.md → "Monitoring and Observability"

**Persistence**
- PostgreSQL with StatefulSet
- Persistent volume claims
- Automated backups
- Data retention policies

👉 See: kubemind/values.yaml → database section

**Networking**
- Service discovery
- Ingress support
- Load balancer option
- Port forwarding access

👉 See: QUICK_REFERENCE.md → "Important Ports"

---

## 💾 Configuration Quick Links

### values.yaml Sections

```yaml
# Global settings
global:
  environment: production
  namespace: kubemind

# Backend service (3 replicas, 8080 port)
backend:
  replicaCount: 3
  resources: ...
  autoscaling: ...

# Frontend service (2 replicas, 80 port)
frontend:
  replicaCount: 2
  ingress:
    enabled: true

# PostgreSQL database (10GB storage)
database:
  postgres:
    persistence:
      size: 10Gi
    backup:
      schedule: "0 2 * * *"

# Observability stack
observability:
  prometheus:
    retention: 15d
  grafana:
    adminUser: admin
  loki:
    enabled: true
```

👉 See: kubemind/values.yaml → All parameters with descriptions

---

## 🚨 Troubleshooting Quick Map

| Problem | Solution |
|---------|----------|
| Pods not starting | INSTALLATION_GUIDE.md → "Check Pod Status" |
| Can't connect to backend | QUICK_REFERENCE.md → "Port Forward Commands" |
| Database connection failed | INSTALLATION_GUIDE.md → "Database Issues" |
| Out of storage | INSTALLATION_GUIDE.md → "Resource Issues" |
| Helm install fails | DEPLOYMENT_GUIDE.md → "Troubleshooting" |
| Need password reset | DEPLOYMENT_GUIDE.md → "Secret Management" |

---

## 🔑 Key Commands

### Installation
```bash
# Basic install
helm install kubemind ./kubemind --namespace kubemind

# With custom values
helm install kubemind ./kubemind -f prod-values.yaml

# Dry run
helm install kubemind ./kubemind --dry-run --debug
```

### Management
```bash
# Check status
helm status kubemind -n kubemind

# Upgrade
helm upgrade kubemind ./kubemind -n kubemind

# Rollback
helm rollback kubemind -n kubemind

# Uninstall
helm uninstall kubemind -n kubemind
```

### Verification
```bash
# Check pods
kubectl get pods -n kubemind

# Check services
kubectl get svc -n kubemind

# View logs
kubectl logs -n kubemind <pod-name>

# Port forward
kubectl port-forward -n kubemind svc/<service-name> <local>:<remote>
```

👉 See: QUICK_REFERENCE.md → "Common Helm Commands"

---

## 📞 Support & Resources

### Internal Documentation
- **QUICK_REFERENCE.md** - Commands and quick lookup
- **INSTALLATION_GUIDE.md** - Step-by-step setup
- **DEPLOYMENT_GUIDE.md** - Complete workflow
- **kubemind/README.md** - Technical reference
- **kubemind/values.yaml** - All configuration options

### External Resources
- Helm: https://helm.sh/docs/
- Kubernetes: https://kubernetes.io/docs/
- PostgreSQL: https://www.postgresql.org/docs/
- Prometheus: https://prometheus.io/docs/
- Grafana: https://grafana.com/docs/grafana/latest/
- Loki: https://grafana.com/docs/loki/latest/

### Common Issues Links
- Pod not starting: INSTALLATION_GUIDE.md → Troubleshooting
- Network errors: QUICK_REFERENCE.md → Troubleshooting Guide
- Database issues: DEPLOYMENT_GUIDE.md → Troubleshooting

---

## ✨ Chart Highlights

**What's Included:**
- ✅ Production-ready Helm chart v1.0.0
- ✅ 13 template files covering all components
- ✅ Complete observability stack
- ✅ Automated database backups
- ✅ RBAC security configuration
- ✅ Horizontal Pod Autoscaler
- ✅ Ingress support
- ✅ 4 comprehensive documentation files

**What You Get:**
- 🚀 Fast deployment in minutes
- 📊 Built-in monitoring and logging
- 🔒 Security best practices
- 📈 Automatic scaling
- 💾 Data persistence
- 🔄 Easy upgrades and rollbacks

---

## 🎬 Getting Started (Choose One)

### Fastest Route (Just Deploy)
1. `helm install kubemind ./kubemind --namespace kubemind`
2. `kubectl get pods -n kubemind`
3. Done! ✅

### Recommended Route (Best Understanding)
1. Read: QUICK_REFERENCE.md (5 min)
2. Read: INSTALLATION_GUIDE.md (15 min)
3. Deploy: Follow installation steps
4. Verify: Check all pods and services
5. Reference: Keep QUICK_REFERENCE.md handy

### Deep Dive Route (Complete Mastery)
1. Read: INSTALLATION_GUIDE.md
2. Read: DEPLOYMENT_GUIDE.md
3. Study: kubemind/README.md
4. Review: kubemind/values.yaml
5. Explore: Template files
6. Deploy: With custom configuration
7. Monitor: Set up dashboards

---

## 📝 Document Versions

| Document | Version | Updated | Purpose |
|----------|---------|---------|---------|
| QUICK_REFERENCE.md | 1.0 | 2024 | Quick commands |
| INSTALLATION_GUIDE.md | 1.0 | 2024 | Setup guide |
| DEPLOYMENT_GUIDE.md | 1.0 | 2024 | Full workflow |
| Helm Chart | 1.0.0 | 2024 | Application |

---

## 📌 Important Notes

⚠️ **Before Deploying:**
- Review values.yaml for your environment
- Generate secure passwords for database and Grafana
- Ensure sufficient cluster resources (4GB+ memory)
- Check storage class availability for persistence

🔐 **Security Reminders:**
- Never commit passwords to version control
- Use external secret management in production
- Review RBAC permissions for your needs
- Enable network policies if required
- Keep database backups secure

📈 **Scale Considerations:**
- Adjust replica counts based on workload
- Monitor resource usage after deployment
- Configure autoscaling thresholds
- Plan capacity for growth

---

**Happy Deploying! 🚀**

For questions or issues, refer to the appropriate documentation file above.
