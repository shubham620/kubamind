# Docker Compose Setup Documentation

## Overview

KubeMind AI uses Docker Compose to orchestrate 9 containerized services for local development and testing. This setup provides a complete development environment with databases, caching, monitoring, logging, and the main backend application.

## Services

### 1. **PostgreSQL** (`postgres`)
- **Image**: `postgres:16-alpine`
- **Purpose**: Relational database for application data
- **Port**: 5432
- **Features**:
  - Health checks enabled
  - Persistent volume: `postgres_data`
  - Resource limits: 1 CPU, 512MB RAM
  - Automatic restart policy
  - JSON logging with rotation

### 2. **Redis** (`redis`)
- **Image**: `redis:7-alpine`
- **Purpose**: In-memory data store for caching
- **Port**: 6379
- **Features**:
  - AOF persistence enabled
  - Health checks enabled
  - Persistent volume: `redis_data`
  - Resource limits: 0.5 CPU, 256MB RAM

### 3. **Qdrant** (`qdrant`)
- **Image**: `qdrant/qdrant:latest`
- **Purpose**: Vector database for semantic search
- **Port**: 6333
- **Features**:
  - Health checks enabled
  - API key authentication
  - Persistent volume: `qdrant_data`
  - Resource limits: 1 CPU, 768MB RAM

### 4. **Prometheus** (`prometheus`)
- **Image**: `prom/prometheus:latest`
- **Purpose**: Metrics collection and time-series storage
- **Port**: 9090
- **Features**:
  - Configuration: `./docker/prometheus.yml`
  - 30-day retention policy
  - Health checks enabled
  - Persistent volume: `prometheus_data`
  - Resource limits: 1 CPU, 512MB RAM

### 5. **Grafana** (`grafana`)
- **Image**: `grafana/grafana:latest`
- **Purpose**: Visualization and dashboards
- **Port**: 3000
- **Features**:
  - Auto-configured Prometheus datasource
  - Admin credentials via environment variables
  - Dashboards: `./monitoring/grafana-dashboards`
  - Persistent volume: `grafana_data`
  - Resource limits: 0.5 CPU, 256MB RAM

### 6. **Loki** (`loki`)
- **Image**: `grafana/loki:latest`
- **Purpose**: Log aggregation and analysis
- **Port**: 3100
- **Features**:
  - Configuration: `./docker/loki-config.yml`
  - Health checks enabled
  - Persistent volume: `loki_data`
  - Resource limits: 0.5 CPU, 256MB RAM

### 7. **KubeMind Backend** (`backend`)
- **Image**: `kubemind-backend:latest` (built from `./backend/Dockerfile`)
- **Purpose**: Main application API service
- **Port**: 8000
- **Features**:
  - Dependencies on all infrastructure services
  - Environment-aware configuration
  - Persistent volume for logs
  - Resource limits: 2 CPU, 1GB RAM
  - Health checks with 20s start period

### 8. **Node Exporter** (`node-exporter`)
- **Image**: `prom/node-exporter:latest`
- **Purpose**: System metrics collection
- **Port**: 9100
- **Features**:
  - Exports CPU, memory, disk, network metrics
  - Minimal resource footprint

### 9. **Ollama** (`ollama`)
- **Image**: `ollama/ollama:latest`
- **Purpose**: Local LLM inference service
- **Port**: 11434
- **Features**:
  - Persistent volume: `ollama_data`
  - Resource limits: 2 CPU, 2GB RAM
  - Models stored locally

## Configuration

### Environment Variables

Create a `.env` file in the project root with the following variables:

```env
# Backend
BACKEND_HOST=0.0.0.0
BACKEND_PORT=8000
ENVIRONMENT=development
DEBUG=true

# Database
POSTGRES_HOST=postgres
POSTGRES_PORT=5432
POSTGRES_DB=kubemind
POSTGRES_USER=kubemind_user
POSTGRES_PASSWORD=kubemind_secure_password

# Redis
REDIS_HOST=redis
REDIS_PORT=6379
REDIS_DB=0

# Vector Database
QDRANT_HOST=qdrant
QDRANT_PORT=6333
QDRANT_API_KEY=test_api_key

# Prometheus
PROMETHEUS_URL=http://prometheus:9090
PROMETHEUS_PORT=9090

# Grafana
GRAFANA_PORT=3000
GF_SECURITY_ADMIN_USER=admin
GF_SECURITY_ADMIN_PASSWORD=admin123

# Loki
LOKI_URL=http://loki:3100
LOKI_PORT=3100

# Ollama
OLLAMA_URL=http://ollama:11434
OLLAMA_PORT=11434

# Logging
LOG_LEVEL=INFO
```

### Network Architecture

All services are connected via a single `kubemind-network` bridge network with the subnet `172.20.0.0/16`. This ensures:
- All services can communicate by container name
- Isolated network from host
- Predictable IP addressing

### Volumes

Persistent data is stored in named volumes:

| Volume | Service | Purpose |
|--------|---------|---------|
| `postgres_data` | PostgreSQL | Database files |
| `redis_data` | Redis | Cache persistence |
| `qdrant_data` | Qdrant | Vector embeddings |
| `prometheus_data` | Prometheus | Metrics database |
| `grafana_data` | Grafana | Dashboards and configurations |
| `loki_data` | Loki | Log files |
| `ollama_data` | Ollama | LLM models |

## Health Checks

All services include health checks with the following configuration:
- **Interval**: 10-15 seconds
- **Timeout**: 5-10 seconds
- **Retries**: 5 attempts
- **Start Period**: 10-20 seconds (grace period before health checks start)

## Resource Limits

Each service has defined CPU and memory limits to prevent resource exhaustion:

| Service | CPU Limit | Memory Limit | CPU Reserved | Memory Reserved |
|---------|-----------|--------------|--------------|-----------------|
| PostgreSQL | 1 | 512MB | 0.5 | 256MB |
| Redis | 0.5 | 256MB | 0.25 | 128MB |
| Qdrant | 1 | 768MB | 0.5 | 512MB |
| Prometheus | 1 | 512MB | 0.5 | 256MB |
| Grafana | 0.5 | 256MB | 0.25 | 128MB |
| Loki | 0.5 | 256MB | 0.25 | 128MB |
| Backend | 2 | 1GB | 1 | 512MB |
| Node-Exporter | 0.25 | 128MB | 0.1 | 64MB |
| Ollama | 2 | 2GB | 1 | 1GB |

## Logging Configuration

All services use JSON file logging driver with rotation:
- **Max size**: 10-50MB per file
- **Max files**: 3-5 rotations
- Prevents disk space issues from log accumulation

## Restart Policies

- **Backend, Databases, Caches**: `unless-stopped` (restart on failure, except manual stop)
- **Monitoring/Observability**: `unless-stopped`
- **System Tools**: `unless-stopped`

## Usage

### Start All Services

```bash
# Using .env file for configuration
docker-compose up -d

# With specific environment
docker-compose --env-file .env up -d
```

### View Logs

```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f backend

# Last 100 lines
docker-compose logs --tail=100 backend
```

### Stop Services

```bash
# Stop all (preserves data)
docker-compose stop

# Stop specific service
docker-compose stop backend

# Remove containers (data persists in volumes)
docker-compose down

# Remove everything including volumes (WARNING: deletes data)
docker-compose down -v
```

### Access Services

| Service | URL | Credentials |
|---------|-----|-------------|
| Backend API | http://localhost:8000 | - |
| Prometheus | http://localhost:9090 | - |
| Grafana | http://localhost:3000 | admin / admin123 |
| Loki | http://localhost:3100 | - |
| PostgreSQL | localhost:5432 | kubemind_user / kubemind_secure_password |
| Redis | localhost:6379 | - |
| Qdrant | http://localhost:6333 | API Key: test_api_key |
| Ollama | http://localhost:11434 | - |

### Pull LLM Models

```bash
# Pull Llama2 model
docker-compose exec ollama ollama pull llama2

# Pull other models
docker-compose exec ollama ollama list
```

## Database Initialization

PostgreSQL automatically initializes with:
- UUID and text search extensions
- `kubemind` schema
- Audit logging table
- Proper role permissions

The initialization script is located at `./docker/init-postgres.sql`

## Monitoring & Observability

### Prometheus Scrape Targets
- `prometheus`: Self-monitoring
- `node-exporter`: System metrics (9100)
- `backend`: Application metrics (8000)
- `qdrant`: Vector DB metrics (6333)
- `postgres`: Database metrics (5432)
- `redis`: Cache metrics (6379)

### Grafana Dashboards
Pre-configured dashboards for:
- System metrics (CPU, memory, disk)
- Application performance
- Database queries
- Cache hit rates
- Vector database operations

### Log Aggregation
- Loki collects logs from all services
- Query logs through Grafana UI
- Label-based filtering by service and level

## Troubleshooting

### Service won't start
```bash
# Check service logs
docker-compose logs <service-name>

# Inspect service configuration
docker-compose config | grep -A 20 "service-name:"
```

### Health check failures
```bash
# Check container status
docker-compose ps

# Test service connectivity
docker-compose exec backend curl http://postgres:5432
```

### Port conflicts
If ports are already in use:
1. Edit `.env` file to change port mappings
2. Or stop conflicting services: `docker-compose stop <service>`

### Volume permission issues
```bash
# Fix volume permissions
docker-compose exec postgres chown -R postgres:postgres /var/lib/postgresql/data
```

### Memory issues
- Reduce resource limits in docker-compose.yml
- Or increase Docker desktop memory allocation
- Check `docker stats` for real-time usage

## Performance Tuning

### For development:
- Smaller resource limits are acceptable
- Health check intervals can be increased
- Logging verbosity can be higher

### For testing:
- Ensure resource limits match production-like scenarios
- Reduce health check intervals for faster failure detection
- Enable detailed logging for debugging

### For production (use Kubernetes instead):
- Increase resource reservations
- Use production container images with security scanning
- Implement proper secret management
- Enable audit logging

## Development Workflow

### Local Development
```bash
# 1. Start services
docker-compose up -d

# 2. View backend logs
docker-compose logs -f backend

# 3. Access API
curl http://localhost:8000/health

# 4. View monitoring
# Open http://localhost:3000 (Grafana)
# Open http://localhost:9090 (Prometheus)

# 5. Stop when done
docker-compose stop
```

### Testing
```bash
# Run with test environment
ENVIRONMENT=test docker-compose up -d

# Run tests against live services
pytest tests/

# Cleanup
docker-compose down
```

## Security Considerations

### Current Setup (Development Only)
- Default credentials used (change for production)
- No encryption for inter-service communication
- Debug mode enabled
- No API authentication

### For Production
1. Use strong passwords and API keys (stored in secrets manager)
2. Enable TLS for all inter-service communication
3. Disable debug mode
4. Implement proper authentication
5. Use network policies and firewalls
6. Regular security scanning of images
7. Implement audit logging
8. Use secrets management (Vault, AWS Secrets Manager, etc.)

## Documentation Files

- `./docker/prometheus.yml`: Prometheus configuration
- `./docker/loki-config.yml`: Loki configuration
- `./docker/init-postgres.sql`: PostgreSQL initialization
- `.env`: Environment variables
- `./monitoring/grafana-dashboards/`: Grafana dashboard JSON files

## References

- Docker Compose: https://docs.docker.com/compose/
- Docker Networking: https://docs.docker.com/network/
- Prometheus: https://prometheus.io/docs/
- Grafana: https://grafana.com/docs/
- Loki: https://grafana.com/docs/loki/
- Qdrant: https://qdrant.tech/documentation/
- Ollama: https://ollama.ai/
