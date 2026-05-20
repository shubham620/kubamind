# Docker Compose Quick Reference

## Start/Stop Commands

```bash
# Start all services in background
docker-compose up -d

# Start with specific environment file
docker-compose --env-file .env up -d

# Start specific service
docker-compose up -d postgres redis

# Start and view logs
docker-compose up

# Stop all services (preserve data)
docker-compose stop

# Stop specific service
docker-compose stop backend

# Remove containers (preserve data)
docker-compose down

# Remove everything (DELETE DATA)
docker-compose down -v
```

## Status & Logs

```bash
# View all services status
docker-compose ps

# View logs (all services)
docker-compose logs

# View logs with timestamps
docker-compose logs -t

# View last 100 lines
docker-compose logs --tail=100

# Follow logs (live)
docker-compose logs -f

# Follow logs for specific service
docker-compose logs -f backend

# View logs for multiple services
docker-compose logs -f postgres redis backend

# Clear logs
docker-compose logs --tail=0
```

## Service Management

```bash
# Restart service
docker-compose restart backend

# Rebuild service (if Dockerfile changed)
docker-compose up -d --build backend

# Execute command in service
docker-compose exec postgres psql -U kubemind_user -d kubemind

# Open shell in service
docker-compose exec backend bash
docker-compose exec postgres bash

# View service config
docker-compose config

# Validate config
docker-compose config --quiet

# View logs of specific service
docker-compose logs postgres -f
```

## Database Operations

```bash
# Access PostgreSQL
docker-compose exec postgres psql -U kubemind_user -d kubemind

# Create backup
docker-compose exec postgres pg_dump -U kubemind_user kubemind > backup.sql

# Restore backup
cat backup.sql | docker-compose exec -T postgres psql -U kubemind_user -d kubemind

# Access Redis
docker-compose exec redis redis-cli

# Flush Redis cache
docker-compose exec redis redis-cli FLUSHALL
```

## LLM Models (Ollama)

```bash
# List available models
docker-compose exec ollama ollama list

# Pull a model
docker-compose exec ollama ollama pull llama2
docker-compose exec ollama ollama pull neural-chat

# Remove a model
docker-compose exec ollama ollama rm llama2

# Run a model (interactive)
docker-compose exec ollama ollama run llama2
```

## Monitoring & Observability

```bash
# View real-time resource usage
docker stats

# View specific service stats
docker stats kubemind-backend

# Access Grafana
# http://localhost:3000 (admin/admin123)

# Access Prometheus
# http://localhost:9090

# Access Loki
# http://localhost:3100

# Query Prometheus metrics
# http://localhost:9090/api/query?query=up
```

## Backend Operations

```bash
# Access backend container
docker-compose exec backend bash

# View backend logs
docker-compose logs -f backend

# Health check
curl http://localhost:8000/health

# API request example
curl http://localhost:8000/api/clusters
```

## Environment Variables

```bash
# View current .env values
cat .env

# Update .env variable
# Edit .env file and restart services
docker-compose restart backend

# Use alternate .env file
docker-compose --env-file .env.production up -d
```

## Troubleshooting

```bash
# Check service is running
docker-compose ps

# View detailed service logs
docker-compose logs -f SERVICE_NAME

# Inspect service config
docker-compose config | grep -A 50 "service-name:"

# Check network
docker network ls
docker network inspect kubemind-network

# Check volumes
docker volume ls
docker volume inspect postgres_data

# Verify connectivity between services
docker-compose exec backend curl -v http://postgres:5432
docker-compose exec backend curl -v http://redis:6379
docker-compose exec backend curl -v http://qdrant:6333/health

# Check resource limits
docker stats

# View Docker events
docker events --filter container=$(docker-compose ps -q backend)
```

## Performance Tuning

```bash
# Reduce health check frequency (edit docker-compose.yml)
# Change interval from 10s to 30s for less frequent checks

# Increase resource limits
# Edit docker-compose.yml deploy resources section

# Monitor resource usage
watch docker stats

# Check log sizes
du -sh docker/*/logs/*

# Prune unused resources
docker system prune -a

# Prune volumes (careful!)
docker volume prune
```

## Port Reference

| Service | Port | URL |
|---------|------|-----|
| Backend | 8000 | http://localhost:8000 |
| PostgreSQL | 5432 | postgres://localhost:5432 |
| Redis | 6379 | redis://localhost:6379 |
| Qdrant | 6333 | http://localhost:6333 |
| Prometheus | 9090 | http://localhost:9090 |
| Grafana | 3000 | http://localhost:3000 |
| Loki | 3100 | http://localhost:3100 |
| Node-Exporter | 9100 | http://localhost:9100 |
| Ollama | 11434 | http://localhost:11434 |

## Service Dependencies

```
backend (8000)
├── postgres (5432) [healthy]
├── redis (6379) [healthy]
└── qdrant (6333) [healthy]

grafana (3000)
└── prometheus (9090) [healthy]

node-exporter (9100)
└── [standalone]

ollama (11434)
└── [standalone]

loki (3100)
└── [standalone]

prometheus (9090)
└── [standalone]
```

## Health Check Status

```bash
# Check all health statuses
docker-compose ps

# Output shows:
# SERVICE         STATUS
# postgres        Up ... (healthy)
# redis           Up ... (healthy)
# qdrant          Up ... (healthy)
# prometheus      Up ... (healthy)
# grafana         Up ... (healthy)
# loki            Up ... (healthy)
# backend         Up ... (healthy)
# node-exporter   Up ...
# ollama          Up ...
```

## Clean Start

```bash
# Full clean start (removes everything)
docker-compose down -v

# Start fresh
docker-compose up -d

# Verify all services are healthy
docker-compose ps

# Initialize database
docker-compose exec backend python manage.py migrate

# Pull LLM model
docker-compose exec ollama ollama pull llama2
```

## Common Workflows

### Development Setup
```bash
# Start all services
docker-compose up -d

# Follow backend logs
docker-compose logs -f backend

# Make code changes, service auto-reloads
# Edit files in ./backend/

# Restart if needed
docker-compose restart backend
```

### Testing
```bash
# Start services
ENVIRONMENT=test docker-compose up -d

# Run tests
docker-compose exec backend pytest

# Check logs for errors
docker-compose logs

# Stop services
docker-compose stop
```

### Debugging
```bash
# Start services
docker-compose up -d

# Shell into failing service
docker-compose exec SERVICE_NAME bash

# Check logs
docker-compose logs -f SERVICE_NAME

# Verify connectivity
docker-compose exec backend curl -v http://postgres:5432
```

### Data Persistence
```bash
# Volumes are automatically persisted
docker-compose stop      # Stop (data remains)

# Later...
docker-compose start     # Start (data restored)

# Complete removal
docker-compose down -v   # Remove everything
```

## Advanced Usage

### Custom Docker Compose Files
```bash
# Use multiple compose files
docker-compose -f docker-compose.yml -f docker-compose.override.yml up -d

# Use production config
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d
```

### Service Scaling (not recommended for this setup)
```bash
# Typically not needed, but possible
docker-compose up -d --scale backend=2  # Creates 2 backend instances
```

### Manual Updates
```bash
# Pull latest images
docker-compose pull

# Rebuild from source
docker-compose build --no-cache

# Restart with new images
docker-compose up -d
```

## Useful Tips

1. **Always use -d flag** for background operation
2. **Check `.env` file** before running services
3. **Monitor logs** during first startup
4. **Use container names** for inter-service communication
5. **Name your docker-compose commands** for clarity
6. **Regularly check resource usage** with `docker stats`
7. **Clean up occasionally** with `docker system prune`
8. **Back up data** from volumes periodically
9. **Update images** regularly for security patches
10. **Document custom changes** to docker-compose.yml

## Documentation

- Full setup guide: `DOCKER_SETUP.md`
- Summary: `DOCKER_COMPOSE_SUMMARY.md`
- Configuration validation: `validate_compose.py`
- Test suite: `test_docker_setup.py`
