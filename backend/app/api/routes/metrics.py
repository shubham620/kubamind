"""
Metrics endpoints - Real-time Kubernetes metrics
"""

from fastapi import APIRouter
from typing import List, Optional

router = APIRouter()


@router.get("/pods")
async def get_pod_metrics(namespace: Optional[str] = None):
    """Get metrics for all pods"""
    return {
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


@router.get("/pods/{pod_name}")
async def get_pod_metrics_detail(pod_name: str):
    """Get detailed metrics for a specific pod"""
    return {
        "pod_name": pod_name,
        "cpu": {"current": 25.5, "limit": 100.0},
        "memory": {"current": 512.3, "limit": 1024.0},
        "network": {"in": 1024, "out": 2048}
    }


@router.get("/services")
async def get_service_metrics():
    """Get metrics aggregated by service"""
    return {
        "services": [
            {
                "name": "frontend",
                "pod_count": 3,
                "avg_cpu": 20.0,
                "avg_memory": 450.0
            }
        ]
    }


@router.get("/nodes")
async def get_node_metrics():
    """Get node-level metrics"""
    return {
        "nodes": [
            {
                "name": "minikube",
                "cpu_usage": 35.0,
                "memory_usage": 2048.0,
                "disk_usage": 50.0
            }
        ]
    }
