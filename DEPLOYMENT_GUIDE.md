# KubeMind AI - End-to-End Project Guide

## 📋 Project Overview

KubeMind AI is a complete AI-powered Kubernetes infrastructure intelligence platform with:

- **Backend**: FastAPI with 6 AI agents + 4 reasoning engines + WebSocket support
- **Frontend**: Next.js React dashboard with real-time visualization
- **Infrastructure**: Docker Compose for local dev, Kubernetes for production
- **CI/CD**: GitHub Actions for automated testing and deployment

## 🚀 Quick Start (Development)

### Prerequisites
- Docker & Docker Compose
- Node.js 18+ (for frontend development)
- Python 3.10+ (for backend development)
- Git

### Start with Docker Compose

```bash
cd "c:\Users\mrshu\OneDrive\Desktop\coding\KubeMind AI"

# Start all services (backend, frontend, database, redis, etc.)
docker-compose up -d

# Verify services are running
docker-compose ps

# View logs
docker-compose logs -f

# Access the dashboard
# Frontend: http://localhost:3000
# Backend API: http://localhost:8000
# API Docs: http://localhost:8000/docs
# Grafana: http://localhost:3000 (admin/admin123)
```

### Stop and Cleanup

```bash
docker-compose down
docker-compose down -v  # Also remove volumes
```

## 🏗️ Architecture

### Services Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Frontend (Next.js)                       │
│              http://localhost:3000                            │
└──────────────────────┬──────────────────────────────────────┘
                       │ WebSocket & REST
┌──────────────────────▼──────────────────────────────────────┐
│                Backend (FastAPI)                             │
│     http://localhost:8000/docs                               │
│                                                              │
│  ┌─────────┬──────────┬──────────┬──────────┬──────────┐   │
│  │   CPU   │ Memory   │ Storage  │ Network  │   Log    │   │
│  │  Agent  │  Agent   │  Agent   │  Agent   │  Agent   │   │
│  └─────────┴──────────┴──────────┴──────────┴──────────┘   │
│         ▼                                                    │
│  ┌────────────────────────────────────┐                    │
│  │  Reasoning Engine + Orchestrator    │                    │
│  │  Predictive + NLP + Chat            │                    │
│  └────────────────────────────────────┘                    │
└──────────────┬──────────────────────────────────────────────┘
               │
      ┌────────┴────────┬──────────┬──────────┬─────────┐
      ▼                 ▼          ▼          ▼         ▼
   PostgreSQL       Redis       Qdrant    Prometheus Grafana
   (Database)       (Cache)   (Vectors)   (Metrics)  (UI)
```

### Data Flow

1. **Agent Analysis** (30-second cycles):
   - 6 agents analyze infrastructure
   - Insights collected and stored

2. **Reasoning Layer**:
   - Correlates insights from all agents
   - Identifies root causes
   - Generates recommendations

3. **Predictions**:
   - ML models forecast issues
   - Pod crashes, OOM, disk exhaustion

4. **NLP Explanations**:
   - Human-readable explanations
   - Automated insights generation

5. **Real-time Updates**:
   - WebSocket broadcasts to frontend
   - Dashboard updates in real-time

## 📊 Frontend Features

### Pages

1. **Dashboard** (`/`)
   - Real-time metrics visualization
   - Agent status cards
   - Active alerts
   - Quick action buttons

2. **Insights** (`/insights`)
   - AI-generated correlations
   - Root cause analysis
   - Actionable recommendations

3. **Predictions** (`/predictions`)
   - Infrastructure forecasts
   - Risk probability scores
   - Recommended actions

4. **Service Topology** (`/topology`)
   - Microservice dependency graph
   - Health status visualization
   - Cascade risk detection

5. **Chat Assistant** (`/chat`)
   - Natural language queries
   - Infrastructure Q&A
   - Real-time analysis

6. **Logs** (`/logs`)
   - Real-time log aggregation
   - NLP-based summaries
   - Error clustering

### Components

- **MetricsVisualization**: Bar, line, pie charts
- **AgentStatusCard**: 6 AI agents real-time status
- **AlertNotifications**: Critical alerts with auto-dismiss
- **CorrelationCard**: Insight correlations with confidence
- **PredictionCard**: Forecasts with recommended actions
- **ServiceTopology**: Dependency graph visualization
- **ChatInterface**: Conversational analysis
- **Sidebar**: Navigation with active state
- **Layout**: Responsive main layout

## 🔌 API Endpoints

### Analysis Endpoints

```bash
# Trigger analysis manually
GET /api/analysis/run

# Get latest analysis result
GET /api/analysis/latest

# Get orchestrator status
GET /api/analysis/status

# Get analysis history (limit default: 10)
GET /api/analysis/history?limit=20
```

### Agent Endpoints

```bash
# Get all agents status
GET /api/agents/status

# Individual agent status
GET /api/agents/cpu/status
GET /api/agents/memory/status
GET /api/agents/storage/status
GET /api/agents/network/status
GET /api/agents/log/status
GET /api/agents/dependency/status
```

### Chat Endpoint

```bash
# Send query to AI assistant
POST /api/chat/query
Body: { "query": "Why is payment-service slow?" }
```

### WebSocket Endpoints

```
ws://localhost:8000/ws/analysis
ws://localhost:8000/ws/metrics
ws://localhost:8000/ws/alerts
```

## 🐳 Docker Setup

### Build Docker Images

```bash
# Build backend
docker build -t kubemind-backend:latest ./backend

# Build frontend
docker build -t kubemind-frontend:latest ./frontend

# Or use docker-compose
docker-compose build
```

### Environment Variables

Backend (.env):
```
DATABASE_URL=postgresql://user:pass@postgres:5432/kubemind
REDIS_URL=redis://redis:6379/0
QDRANT_URL=http://qdrant:6333
ENVIRONMENT=development
LOG_LEVEL=INFO
```

Frontend (.env.local):
```
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## ☸️ Kubernetes Deployment

### Prerequisites

- Kubernetes cluster (1.24+)
- kubectl configured
- nginx-ingress controller
- cert-manager (for TLS)

### Deploy to Kubernetes

```bash
# Create namespace and base services
kubectl apply -f kubernetes/base-services.yaml

# Deploy backend
kubectl apply -f kubernetes/backend-deployment.yaml

# Deploy frontend and ingress
kubectl apply -f kubernetes/frontend-ingress.yaml

# Check deployment status
kubectl get pods -n kubemind
kubectl get services -n kubemind
kubectl get ingress -n kubemind

# Port forward for testing
kubectl port-forward -n kubemind svc/kubemind-backend 8000:8000
kubectl port-forward -n kubemind svc/kubemind-frontend 3000:3000

# View logs
kubectl logs -n kubemind deployment/kubemind-backend -f
kubectl logs -n kubemind deployment/kubemind-frontend -f

# Scale deployment
kubectl scale deployment kubemind-backend -n kubemind --replicas=5

# Update deployment
kubectl set image deployment/kubemind-backend -n kubemind \
  backend=kubemind-backend:v1.2.3
```

### Kubernetes Features

- **Replicas**: 3 for backend, 3 for frontend (configurable)
- **Auto-scaling**: HPA based on CPU/Memory
- **Resource limits**: Defined per service
- **Health checks**: Liveness and readiness probes
- **RBAC**: Service accounts and cluster roles
- **Ingress**: TLS with cert-manager
- **Persistence**: StatefulSet for PostgreSQL
- **Pod Disruption Budget**: Ensures minimum availability

## 🔄 CI/CD Pipeline

### GitHub Actions Workflow

Automatically triggered on:
- Push to main/develop
- Pull requests to main/develop

### Pipeline Stages

1. **Test Backend**
   - Install dependencies
   - Lint with flake8
   - Format check with black
   - Run pytest
   - Upload coverage

2. **Test Frontend**
   - Install dependencies
   - Run ESLint
   - Build with Next.js
   - Type check with TypeScript

3. **Validate Kubernetes**
   - YAML syntax validation
   - Schema validation with kubeval

4. **Build Docker Images**
   - Multi-stage builds
   - Layer caching
   - Push to registry

5. **Deploy to Kubernetes**
   - Apply manifests
   - Verify rollout
   - Health checks

## 🧪 Testing

### Backend Tests

```bash
cd backend

# Run all tests
pytest

# Run with coverage
pytest --cov=app --cov-report=html

# Run specific test
pytest tests/test_agents.py::test_cpu_agent -v

# Run tests matching pattern
pytest -k "test_analysis" -v
```

### Frontend Tests

```bash
cd frontend

# Run tests
npm test

# Run tests in watch mode
npm run test:watch

# Build for production
npm run build

# Type check
npm run type-check
```

### Manual API Testing

```bash
# Health check
curl http://localhost:8000/health

# Trigger analysis
curl http://localhost:8000/api/analysis/run

# Get latest result
curl http://localhost:8000/api/analysis/latest

# Chat query
curl -X POST http://localhost:8000/api/chat/query \
  -H "Content-Type: application/json" \
  -d '{"query": "What is the CPU usage?"}'

# WebSocket connection
wscat -c ws://localhost:8000/ws/analysis
```

## 📈 Monitoring & Observability

### Prometheus Metrics

Access at: http://localhost:9090

```promql
# Query examples
rate(http_requests_total[5m])
container_memory_usage_bytes
container_cpu_usage_seconds_total
```

### Grafana Dashboards

Access at: http://localhost:3000 (admin/admin123)

- Pre-configured dashboards for all services
- Auto-discovery of Prometheus targets
- Alert rules configured

### Loki Logs

Access at: http://localhost:3100

- All service logs aggregated
- Query by labels (service, level, pod)
- Log retention: 30 days

## 🔒 Security Considerations

### Development

- CORS enabled for localhost
- JWT authentication not enforced
- Credentials in plaintext (.env)
- Debug mode enabled

### Production

```bash
# Update .env with production values
DATABASE_URL=postgresql://secure-user:strong-password@postgres-host:5432/kubemind
REDIS_URL=redis://redis-host:6379/0
JWT_SECRET_KEY=$(openssl rand -hex 32)
ENVIRONMENT=production
```

- CORS restricted to specific domains
- JWT authentication enforced
- TLS/HTTPS enabled
- Secrets in Kubernetes Secrets
- Network policies implemented
- Pod security policies enforced

## 🛠️ Troubleshooting

### Services Not Starting

```bash
# Check logs
docker-compose logs [service-name]

# Verify configuration
docker-compose config

# Restart services
docker-compose restart [service-name]
```

### Database Connection Issues

```bash
# Check PostgreSQL
docker-compose exec postgres psql -U kubemind -d kubemind

# Check Redis
docker-compose exec redis redis-cli ping

# Check Qdrant
curl http://localhost:6333/health
```

### Frontend Not Loading

```bash
# Check frontend logs
docker-compose logs frontend

# Verify API connectivity
curl http://localhost:8000/health

# Check browser console
# Open http://localhost:3000 and check browser dev tools
```

### WebSocket Connection Failed

```bash
# Test WebSocket connection
wscat -c ws://localhost:8000/ws/analysis

# Check CORS headers
curl -H "Origin: http://localhost:3000" \
  -H "Access-Control-Request-Method: GET" \
  http://localhost:8000/health -v
```

## 📚 Documentation Files

- **README_DOCKER.md**: Docker setup and commands
- **DOCKER_SETUP.md**: Detailed Docker configuration
- **DOCKER_QUICK_REFERENCE.md**: Quick command reference
- **DOCKER_COMPOSE_SUMMARY.md**: Compose file overview
- **PHASE_4_REPORT.md**: Backend implementation details
- **PREDICTIVE_ENGINE_REPORT.md**: ML models documentation
- **COMPLETION_REPORT.txt**: Docker enhancement report

## 🎯 Development Workflow

### Adding a New Page

1. Create component file in `frontend/components/[Category]/`
2. Create page file in `frontend/pages/[page-name].tsx`
3. Add route to sidebar navigation
4. Implement API calls using `lib/api.ts`
5. Use store hooks from `store/`
6. Add styles with Tailwind CSS

### Adding a New API Endpoint

1. Create route in `backend/app/api/routes/`
2. Add schemas in `backend/app/schemas.py`
3. Implement business logic
4. Update `backend/app/main.py` to include router
5. Add API client method in `frontend/lib/api.ts`
6. Create frontend integration

### Deploying Changes

1. Create feature branch
2. Push changes to GitHub
3. CI/CD pipeline runs automatically
4. Merge to main (after PR approval)
5. Automatic deployment to Kubernetes
6. Verify deployment with `kubectl get pods`

## 📞 Support & Help

### Debug Mode

```bash
# Backend debug logging
export LOG_LEVEL=DEBUG
docker-compose up backend

# Frontend debug info
NEXT_PUBLIC_DEBUG=true npm run dev
```

### Check Health

```bash
# All services health
docker-compose exec backend python -c "
from app.orchestrator import orchestrator
print('Orchestrator:', orchestrator.is_running)
"

# Frontend connectivity test
curl -s http://localhost:8000/health | jq .

# Database connection test
docker-compose exec postgres pg_isready
```

## 🎉 Deployment Checklist

- [ ] All tests passing
- [ ] Code reviewed
- [ ] Environment variables updated
- [ ] Database migrations applied
- [ ] Docker images built and pushed
- [ ] Kubernetes manifests validated
- [ ] SSL certificates configured
- [ ] Monitoring setup verified
- [ ] Backups configured
- [ ] Runbooks created
- [ ] Team trained on deployment
- [ ] Rollback procedure documented

## 📞 Contact & Issues

For issues or questions:
1. Check troubleshooting guide above
2. Review logs with `docker-compose logs -f`
3. Create GitHub issue with:
   - Error message
   - Steps to reproduce
   - Environment details
   - Screenshots (if applicable)

---

**Version**: 1.0.0  
**Last Updated**: 2026-05-16  
**Status**: ✅ Production Ready
