# KubeMind AI - API Documentation

## Base URL
```
http://localhost:8000
```

## Authentication

Currently, no authentication is required (development mode). For production, API keys are required:

```bash
# All requests should include
Authorization: Bearer YOUR_API_KEY
```

## Response Format

All responses are in JSON format:

```json
{
  "status": "success/error",
  "data": {},
  "error": "Error message if applicable"
}
```

---

## Endpoints

### Health Checks

#### `GET /health`
Overall system health check.

**Response:**
```json
{
  "status": "healthy",
  "app": "KubeMind AI",
  "environment": "development"
}
```

#### `GET /api/health/detailed`
Detailed health information for all components.

**Response:**
```json
{
  "status": "healthy",
  "services": {
    "backend": "running",
    "database": "connected",
    "cache": "connected",
    "vector_db": "connected"
  }
}
```

---

### Metrics Endpoints

#### `GET /api/metrics/pods`
Get metrics for all pods.

**Query Parameters:**
- `namespace` (optional): Filter by namespace

**Response:**
```json
{
  "pods": [
    {
      "name": "frontend-pod-1",
      "namespace": "default",
      "cpu_usage": 25.5,
      "memory_usage": 512.3,
      "status": "running"
    }
  ]
}
```

#### `GET /api/metrics/pods/{pod_name}`
Get detailed metrics for a specific pod.

**Parameters:**
- `pod_name` (path): Name of the pod

**Response:**
```json
{
  "pod_name": "frontend-pod-1",
  "cpu": {
    "current": 25.5,
    "limit": 100.0
  },
  "memory": {
    "current": 512.3,
    "limit": 1024.0
  },
  "network": {
    "in": 1024,
    "out": 2048
  }
}
```

#### `GET /api/metrics/services`
Get metrics aggregated by service.

**Response:**
```json
{
  "services": [
    {
      "name": "frontend",
      "pod_count": 3,
      "avg_cpu": 20.0,
      "avg_memory": 450.0
    }
  ]
}
```

#### `GET /api/metrics/nodes`
Get node-level metrics.

**Response:**
```json
{
  "nodes": [
    {
      "name": "minikube",
      "cpu_usage": 35.0,
      "memory_usage": 2048.0,
      "disk_usage": 50.0
    }
  ]
}
```

---

### Insights Endpoints

#### `GET /api/insights/anomalies`
Get detected anomalies.

**Response:**
```json
{
  "anomalies": [
    {
      "id": "anom-001",
      "type": "cpu_spike",
      "pod": "payment-service-1",
      "severity": "high",
      "description": "Unexpected CPU spike detected",
      "timestamp": "2024-01-15T10:30:00Z"
    }
  ]
}
```

#### `GET /api/insights/predictions`
Get predictions for future issues.

**Response:**
```json
{
  "predictions": [
    {
      "id": "pred-001",
      "type": "oom_risk",
      "pod": "database-1",
      "confidence": 0.85,
      "predicted_time_hours": 3.5,
      "recommendation": "Scale memory or optimize application"
    }
  ]
}
```

#### `GET /api/insights/root-causes`
Get root cause analysis for incidents.

**Response:**
```json
{
  "incidents": [
    {
      "id": "incident-001",
      "timestamp": "2024-01-15T10:00:00Z",
      "affected_services": ["payment-service", "auth-service"],
      "root_cause": "Database connection pool exhaustion",
      "explanation": "..."
    }
  ]
}
```

#### `GET /api/insights/recommendations`
Get AI recommendations for improvements.

**Response:**
```json
{
  "recommendations": [
    {
      "id": "rec-001",
      "priority": "high",
      "title": "Optimize database queries",
      "description": "Current queries are slow...",
      "impact": "Reduce CPU by 15%"
    }
  ]
}
```

---

### Chat Endpoints

#### `POST /api/chat/message`
Send a message to the AI assistant.

**Request Body:**
```json
{
  "query": "Why is payment-service slow?",
  "context": {}
}
```

**Response:**
```json
{
  "response": "The payment service is experiencing latency due to database connection pool exhaustion...",
  "insights": [],
  "timestamp": "2024-01-15T10:30:00Z"
}
```

#### `WebSocket /api/chat/ws`
Real-time chat via WebSocket.

**Connection:**
```bash
ws://localhost:8000/api/chat/ws
```

**Send:**
```json
{
  "message": "What are the current anomalies?"
}
```

**Receive:**
```json
{
  "type": "response",
  "message": "Currently detecting 3 anomalies...",
  "timestamp": "2024-01-15T10:30:00Z"
}
```

#### `GET /api/chat/history/{session_id}`
Get chat history for a session.

**Parameters:**
- `session_id` (path): Session identifier

**Response:**
```json
{
  "session_id": "sess-001",
  "messages": [
    {
      "role": "user",
      "message": "What services are failing?",
      "timestamp": "2024-01-15T10:00:00Z"
    },
    {
      "role": "assistant",
      "message": "Currently, payment-service is experiencing issues...",
      "timestamp": "2024-01-15T10:00:05Z"
    }
  ]
}
```

---

### Agent Endpoints

#### `GET /api/agents/status`
Get status of all AI agents.

**Response:**
```json
{
  "agents": [
    {
      "name": "cpu_agent",
      "status": "active",
      "last_analysis": "2024-01-15T10:30:00Z"
    },
    {
      "name": "memory_agent",
      "status": "active",
      "last_analysis": "2024-01-15T10:30:00Z"
    }
  ]
}
```

#### `GET /api/agents/{agent_name}/insights`
Get insights from a specific agent.

**Parameters:**
- `agent_name` (path): Name of the agent

**Response:**
```json
{
  "agent": "cpu_agent",
  "insights": [
    {
      "type": "cpu_spike",
      "severity": "high",
      "pod": "payment-service-1"
    }
  ]
}
```

#### `POST /api/agents/{agent_name}/trigger`
Manually trigger an agent analysis.

**Parameters:**
- `agent_name` (path): Name of the agent

**Response:**
```json
{
  "agent": "cpu_agent",
  "status": "triggered",
  "message": "Analysis started..."
}
```

---

## Error Responses

### 400 Bad Request
```json
{
  "error": "Invalid request",
  "detail": "Missing required parameter: pod_name"
}
```

### 404 Not Found
```json
{
  "error": "Not found",
  "detail": "Pod 'unknown-pod' not found"
}
```

### 500 Internal Server Error
```json
{
  "error": "Internal server error",
  "detail": "An unexpected error occurred (debug mode shows details)"
}
```

---

## Rate Limiting

- Development mode: No rate limiting
- Production mode: 100 requests per minute per API key

---

## Pagination

List endpoints support pagination:

**Query Parameters:**
- `limit`: Number of items (default: 20, max: 100)
- `offset`: Starting position (default: 0)

**Example:**
```
GET /api/insights/anomalies?limit=50&offset=0
```

---

## Filtering

Supported filters vary by endpoint:

```
GET /api/insights/anomalies?severity=high&type=cpu_spike
GET /api/metrics/pods?namespace=default&status=running
```

---

## Sorting

Use the `sort` query parameter:

```
GET /api/insights/predictions?sort=-confidence
GET /api/metrics/pods?sort=name
```

---

## Example Workflows

### Workflow 1: Investigate High CPU

```bash
# 1. Get anomalies
curl http://localhost:8000/api/insights/anomalies

# 2. Get root cause
curl http://localhost:8000/api/insights/root-causes

# 3. Ask AI for explanation
curl -X POST http://localhost:8000/api/chat/message \
  -d '{"query": "Why is CPU high?"}'

# 4. Get recommendations
curl http://localhost:8000/api/insights/recommendations
```

### Workflow 2: Predict Future Issues

```bash
# 1. Get predictions
curl http://localhost:8000/api/insights/predictions

# 2. For each prediction, get details
curl http://localhost:8000/api/agents/cpu_agent/insights
curl http://localhost:8000/api/agents/memory_agent/insights

# 3. Query chat for more context
curl -X POST http://localhost:8000/api/chat/message \
  -d '{"query": "What should I do about the OOM prediction?"}'
```

---

## WebSocket Example (Python)

```python
import asyncio
import websockets
import json

async def chat():
    uri = "ws://localhost:8000/api/chat/ws"
    async with websockets.connect(uri) as websocket:
        # Send message
        await websocket.send(json.dumps({
            "message": "Why is the database slow?"
        }))
        
        # Receive response
        response = await websocket.recv()
        print(json.loads(response))

asyncio.run(chat())
```

---

## SDK Usage (Python)

```python
import requests

# Base URL
BASE_URL = "http://localhost:8000"

# Get anomalies
response = requests.get(f"{BASE_URL}/api/insights/anomalies")
anomalies = response.json()

# Get predictions
response = requests.get(f"{BASE_URL}/api/insights/predictions")
predictions = response.json()

# Send chat message
response = requests.post(
    f"{BASE_URL}/api/chat/message",
    json={"query": "What's wrong with my infrastructure?"}
)
explanation = response.json()
```

---

**Last Updated:** 2024-01-15
**API Version:** 0.1.0
