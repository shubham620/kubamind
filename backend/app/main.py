"""
KubeMind AI FastAPI Application
Main entry point for the backend service
"""

import logging
from contextlib import asynccontextmanager
from datetime import datetime

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.config import settings
from app.api.routes import health, metrics, insights, chat, agents
from app.api.websocket_routes import router as websocket_router
from app.db.database import init_db
from app.websocket_manager import manager

# Import all 6 agents
from app.agents.cpu_agent import cpu_agent
from app.agents.memory_agent import memory_agent
from app.agents.storage_agent import storage_agent
from app.agents.network_agent import network_agent
from app.agents.log_agent import log_agent
from app.agents.dependency_agent import dependency_agent

# Import all engines
from app.reasoning.engine import reasoning_engine
from app.predictive.engine import predictive_engine
from app.nlp.explanation_engine import explanation_engine
from app.chat.assistant import chat_assistant

# Import orchestrator
from app.orchestrator import orchestrator

# Import schemas
from app.schemas import (
    AnalysisRunResponseSchema,
    AnalysisCycleSchema,
    HealthCheckSchema,
    AnalysisStatusSchema,
    AnalysisHistorySchema
)

# Configure logging
logging.basicConfig(level=settings.LOG_LEVEL)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Handle startup and shutdown events"""
    logger.info(f"🚀 Starting {settings.APP_NAME}")
    
    # Startup
    await init_db()
    logger.info("✓ Database initialized")
    
    # Initialize and start orchestrator
    await orchestrator.initialize()
    await orchestrator.start()
    logger.info("✓ Analysis Orchestrator started")
    
    # Log agent and engine initialization
    agents_list = [
        cpu_agent.name,
        memory_agent.name,
        storage_agent.name,
        network_agent.name,
        log_agent.name,
        dependency_agent.name
    ]
    logger.info(f"✓ Initialized 6 agents: {', '.join(agents_list)}")
    logger.info("✓ Initialized 4 engines: reasoning, predictive, nlp, chat")
    
    yield
    
    # Shutdown
    await orchestrator.stop()
    logger.info("🛑 Shutting down...")


# Create FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    description="AI-powered Kubernetes Infrastructure Intelligence Platform",
    version="0.1.0",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Health check endpoint
@app.get("/health", response_model=HealthCheckSchema)
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "app": settings.APP_NAME,
        "environment": settings.ENVIRONMENT,
        "orchestrator_running": orchestrator.is_running,
        "timestamp": datetime.utcnow().isoformat()
    }


# Root endpoint
@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": f"Welcome to {settings.APP_NAME}",
        "version": "0.1.0",
        "docs": "/docs",
        "health": "/health"
    }


# Include route modules
app.include_router(health.router, prefix="/api/health", tags=["health"])
app.include_router(metrics.router, prefix="/api/metrics", tags=["metrics"])
app.include_router(insights.router, prefix="/api/insights", tags=["insights"])
app.include_router(chat.router, prefix="/api/chat", tags=["chat"])
app.include_router(agents.router, prefix="/api/agents", tags=["agents"])
app.include_router(websocket_router, tags=["websocket"])


# ============================================================================
# Analysis API Endpoints
# ============================================================================

@app.get("/api/analysis/run", response_model=AnalysisRunResponseSchema)
async def trigger_analysis():
    """
    Trigger a complete analysis cycle immediately
    
    Runs all 6 agents through the reasoning engine, generates predictions,
    and produces NLP explanations. This runs independently of the scheduled cycle.
    """
    try:
        logger.info("📊 Manually triggered analysis cycle")
        cycle_result = await orchestrator.run_analysis_cycle()
        
        return {
            "status": "success",
            "cycle_id": cycle_result.get("cycle_id"),
            "timestamp": cycle_result.get("timestamp"),
            "duration_seconds": cycle_result.get("duration_seconds"),
            "message": "Analysis cycle completed successfully",
            "analysis": cycle_result
        }
    except Exception as e:
        logger.error(f"❌ Failed to trigger analysis: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Analysis cycle failed: {str(e)}"
        )


@app.get("/api/analysis/latest", response_model=AnalysisCycleSchema)
async def get_latest_analysis():
    """Get the latest analysis result"""
    latest = await orchestrator.get_latest_analysis()
    if latest.get("status") == "no_analysis_yet":
        raise HTTPException(
            status_code=404,
            detail="No analysis has been run yet"
        )
    return latest


@app.get("/api/analysis/status", response_model=AnalysisStatusSchema)
async def get_analysis_status():
    """Get orchestrator status and scheduling info"""
    return orchestrator.get_status()


@app.get("/api/analysis/history", response_model=AnalysisHistorySchema)
async def get_analysis_history(limit: int = 10):
    """Get recent analysis cycles"""
    if limit < 1 or limit > 100:
        limit = 10
    
    cycles = await orchestrator.get_analysis_history(limit=limit)
    return {
        "total": len(cycles),
        "limit": limit,
        "cycles": cycles
    }


@app.get("/api/agents/status")
async def get_agents_status():
    """Get status of all 6 agents"""
    return {
        "agents": [
            cpu_agent.get_status(),
            memory_agent.get_status(),
            storage_agent.get_status(),
            network_agent.get_status(),
            log_agent.get_status(),
            dependency_agent.get_status()
        ],
        "timestamp": datetime.utcnow().isoformat()
    }


# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global exception handler"""
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "detail": str(exc) if settings.DEBUG else "An error occurred"
        }
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=settings.BACKEND_HOST,
        port=settings.BACKEND_PORT,
        reload=settings.DEBUG
    )
