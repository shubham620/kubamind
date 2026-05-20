# KubeMind AI - Getting Started Guide

## Prerequisites

Before you start, ensure you have:

- **Docker** (version 20.10+)
  ```bash
  docker --version
  ```

- **Docker Compose** (version 2.0+)
  ```bash
  docker-compose --version
  ```

- **Git**
  ```bash
  git --version
  ```

- **Python 3.11+** (for running scripts)
  ```bash
  python --version
  ```

- **kubectl** (for Kubernetes deployment)
  ```bash
  kubectl version --client
  ```

- **Minikube** or **K3s** (for local Kubernetes)

## Quick Start (Docker Compose)

The fastest way to get started:

### Step 1: Clone Repository
```bash
git clone https://github.com/your-org/kubemind-ai.git
cd kubemind-ai
```

### Step 2: Configure Environment
```bash
cp .env.example .env
# Edit .env if needed for your environment
```

### Step 3: Start Services
```bash
docker-compose up -d
```

This starts:
- PostgreSQL (database)
- Redis (cache)
- Qdrant (vector DB)
- Prometheus (metrics)
- Grafana (visualization)
- Loki (logs)
- KubeMind Backend (API)
- Node Exporter (system metrics)
- Ollama (local LLM)

### Step 4: Wait for Startup
```bash
# Wait 30-60 seconds for services to start
sleep 60

# Check service health
docker-compose ps
```

### Step 5: Verify Services

**Backend API:**
```bash
curl http://localhost:8000/health
# Should return: {"status": "healthy"}
```

**API Documentation:**
- Open http://localhost:8000/docs in your browser

**Prometheus:**
- Visit http://localhost:9090
- Query: `up` should show all targets

**Grafana:**
- Visit http://localhost:3000
- Login: admin / admin123
- Add Prometheus datasource

**Loki:**
- Accessible at http://localhost:3100

### Step 6: Run Failure Simulations

Trigger sample failures to see AI in action:

```bash
# Run all simulations
python simulations/failure_simulator.py

# Or run individually
python -c "from simulations.failure_simulator import *; 
import asyncio; asyncio.run(simulate_cpu_spike(60, 0.85))"
```

## Kubernetes Deployment

### Prerequisites
```bash
# Install Minikube
brew install minikube  # macOS
# or scoop install minikube  # Windows
# or apt-get install minikube  # Linux

# Start Minikube
minikube start --cpus 4 --memory 8192
minikube addons enable metrics-server
```

### Deploy Steps

```bash
# 1. Run deployment script
./scripts/deploy.sh

# 2. Create namespace
kubectl apply -f kubernetes/manifests/namespace.yaml

# 3. Apply configurations
kubectl apply -f kubernetes/manifests/config/configmap.yaml

# 4. Create storage
kubectl apply -f kubernetes/manifests/storage/pvc.yaml

# 5. Deploy services
kubectl apply -f kubernetes/manifests/services/frontend.yaml
kubectl apply -f kubernetes/manifests/services/auth.yaml
kubectl apply -f kubernetes/manifests/services/database.yaml

# 6. Deploy monitoring
kubectl apply -f kubernetes/manifests/monitoring/prometheus.yaml
kubectl apply -f kubernetes/manifests/monitoring/grafana.yaml
```

### Verify Deployment
```bash
# Check pods
kubectl get pods -n kubemind

# Check services
kubectl get svc -n kubemind

# Check logs
kubectl logs -n kubemind deployment/backend
```

### Access Services

```bash
# Frontend
kubectl port-forward -n kubemind svc/frontend-service 3000:80

# Grafana
kubectl port-forward -n kubemind svc/grafana 3000:3000

# Backend
kubectl port-forward -n kubemind svc/backend 8000:8000

# Prometheus
kubectl port-forward -n kubemind svc/prometheus 9090:9090
```

## API Usage Examples

### Get Pod Metrics
```bash
curl -s http://localhost:8000/api/metrics/pods | jq
```

### Get Detected Anomalies
```bash
curl -s http://localhost:8000/api/insights/anomalies | jq
```

### Get Predictions
```bash
curl -s http://localhost:8000/api/insights/predictions | jq
```

### Send Chat Message
```bash
curl -X POST http://localhost:8000/api/chat/message \
  -H "Content-Type: application/json" \
  -d '{"query": "Why is payment-service slow?"}'
```

### WebSocket Chat (requires wscat)
```bash
npm install -g wscat

wscat -c ws://localhost:8000/api/chat/ws
# Connected, now type messages...
```

## Common Tasks

### Stop Services
```bash
# Docker Compose
docker-compose down

# Kubernetes
kubectl delete namespace kubemind
```

### View Logs
```bash
# Docker Compose
docker-compose logs -f backend

# Kubernetes
kubectl logs -n kubemind -f deployment/backend
```

### Access Database
```bash
# Docker Compose PostgreSQL
docker exec -it kubemind-postgres psql -U kubemind_user -d kubemind

# Query example:
# SELECT * FROM metric_snapshots LIMIT 10;
```

### Configure Alerts

Edit `kubernetes/manifests/monitoring/prometheus.yaml` to add alerting rules:

```yaml
groups:
  - name: kubemind-alerts
    rules:
    - alert: HighCPUUsage
      expr: cpu_usage > 80
      for: 5m
      annotations:
        summary: "High CPU usage detected"
```

## Troubleshooting

### Services Not Starting
```bash
# Check logs
docker-compose logs

# Rebuild
docker-compose build --no-cache

# Restart
docker-compose restart
```

### Backend API Not Responding
```bash
# Check if container is running
docker ps | grep kubemind

# Check logs
docker logs kubemind-backend

# Check port availability
lsof -i :8000
```

### Database Connection Error
```bash
# Check PostgreSQL is running
docker ps | grep postgres

# Test connection
docker exec kubemind-postgres psql -U kubemind_user -d kubemind -c "SELECT 1"
```

### High Memory Usage
```bash
# Check memory limits in docker-compose.yml
# Reduce memory for Prometheus/Grafana if needed
# Or use swap: docker update --memory 2g container_name
```

## Performance Tuning

### For High Traffic
- Increase Prometheus scrape intervals
- Reduce dashboard update frequency
- Enable API caching in backend

### For Large Environments
- Distribute agents across multiple nodes
- Use Redis for distributed caching
- Implement metrics sampling

### For Development
- Set `DEBUG=true` in .env
- Enable verbose logging
- Use local LLM instead of cloud API

## Next Steps

1. **Review Architecture** - Read `docs/ARCHITECTURE.md`
2. **Explore API** - Visit http://localhost:8000/docs
3. **Setup Monitoring** - Configure Grafana dashboards
4. **Run Simulations** - Try failure scenarios
5. **Try Chat** - Ask the AI assistant questions
6. **Customize** - Modify thresholds in `.env`

## Additional Resources

- **Backend API Docs**: http://localhost:8000/docs
- **Prometheus Query Language**: https://prometheus.io/docs/prometheus/latest/querying
- **Grafana Dashboards**: https://grafana.com/grafana/dashboards
- **Kubernetes Docs**: https://kubernetes.io/docs
- **LangChain Docs**: https://python.langchain.com

## Support

For issues:
1. Check `logs/` directory for error details
2. Review service logs: `docker-compose logs`
3. Check individual component health endpoints
4. Consult documentation in `/docs`

---

**Happy monitoring with KubeMind AI! 🚀**
