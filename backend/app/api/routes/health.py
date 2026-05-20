"""
Health check endpoints
"""

from fastapi import APIRouter

router = APIRouter()


@router.get("/")
async def health_check():
    """Overall health status"""
    return {
        "status": "healthy",
        "components": {
            "api": "healthy",
            "database": "healthy",
            "monitoring": "healthy"
        }
    }


@router.get("/detailed")
async def detailed_health():
    """Detailed health information"""
    return {
        "status": "healthy",
        "services": {
            "backend": "running",
            "database": "connected",
            "cache": "connected",
            "vector_db": "connected"
        }
    }
