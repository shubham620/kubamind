"""
Pydantic schemas for API responses and request validation
"""

from typing import Dict, List, Any, Optional
from datetime import datetime
from pydantic import BaseModel, Field


# ============================================================================
# Agent Analysis Schemas
# ============================================================================

class AnomalySchema(BaseModel):
    """Schema for infrastructure anomalies"""
    type: str
    severity: str
    pod: Optional[str] = None
    current_usage: Optional[float] = None
    threshold: Optional[float] = None
    duration_seconds: Optional[int] = None
    
    class Config:
        extra = "allow"


class ForecastSchema(BaseModel):
    """Schema for forecasts"""
    pod: Optional[str] = None
    current: Optional[float] = None
    predicted_1h: Optional[float] = None
    predicted_2h: Optional[float] = None
    risk_level: Optional[str] = None
    
    class Config:
        extra = "allow"


class AgentInsightSchema(BaseModel):
    """Schema for agent insights"""
    timestamp: str
    anomalies: List[AnomalySchema] = []
    forecasts: List[ForecastSchema] = []
    recommendations: List[str] = []
    leaks: List[Dict[str, Any]] = []
    oom_risks: List[Dict[str, Any]] = []
    usage: Dict[str, Any] = {}
    bottlenecks: List[Dict[str, Any]] = []
    error_patterns: List[Dict[str, Any]] = []
    dependencies: List[Dict[str, Any]] = []
    latency_issues: List[Dict[str, Any]] = []
    traffic: Dict[str, Any] = {}
    
    class Config:
        extra = "allow"


class CorrelationSchema(BaseModel):
    """Schema for insight correlations"""
    type: str
    agents: List[str]
    description: str
    confidence: float
    affected_services: List[str] = []
    severity: str


class RootCauseSchema(BaseModel):
    """Schema for root causes"""
    id: str
    title: str
    description: str
    probability: float
    affected_components: List[str] = []
    timeline: str


class RecommendationSchema(BaseModel):
    """Schema for recommendations"""
    priority: str
    action: str
    impact: str
    effort: str


class ReasoningResultSchema(BaseModel):
    """Schema for reasoning engine results"""
    timestamp: str
    agent_insights: Dict[str, AgentInsightSchema]
    correlations: List[CorrelationSchema] = []
    root_causes: List[RootCauseSchema] = []
    recommendations: List[RecommendationSchema] = []


# ============================================================================
# Predictive Engine Schemas
# ============================================================================

class PredictionSchema(BaseModel):
    """Base schema for predictions"""
    pod: Optional[str] = None
    pvc: Optional[str] = None
    service: Optional[str] = None
    probability: float
    confidence: float
    predicted_time_hours: Optional[float] = None
    predicted_time_days: Optional[float] = None
    reason: Optional[str] = None
    
    class Config:
        extra = "allow"


class PredictiveResultSchema(BaseModel):
    """Schema for predictive engine results"""
    timestamp: str
    pod_crashes: List[PredictionSchema] = []
    oom_events: List[PredictionSchema] = []
    disk_exhaustion: List[PredictionSchema] = []
    performance_degradation: List[PredictionSchema] = []


# ============================================================================
# Explanation Engine Schemas
# ============================================================================

class ExplanationsSchema(BaseModel):
    """Schema for NLP explanations"""
    correlations: List[str] = []
    root_causes: List[str] = []
    predictions: List[str] = []


# ============================================================================
# Chat Assistant Schemas
# ============================================================================

class ChatResponseSchema(BaseModel):
    """Schema for chat responses"""
    query: str
    query_type: str
    response: str
    timestamp: str


# ============================================================================
# Analysis Cycle Schemas
# ============================================================================

class AnalysisCycleSchema(BaseModel):
    """Schema for complete analysis cycle"""
    cycle_id: str
    timestamp: str
    duration_seconds: float
    status: str = Field(..., pattern="^(success|error)$")
    reasoning: Optional[ReasoningResultSchema] = None
    predictions: Optional[PredictiveResultSchema] = None
    explanations: Optional[ExplanationsSchema] = None
    summary: Optional[str] = None
    error: Optional[str] = None


# ============================================================================
# API Response Schemas
# ============================================================================

class HealthCheckSchema(BaseModel):
    """Schema for health check response"""
    status: str
    app: str
    environment: str
    orchestrator_running: bool
    timestamp: str = Field(default_factory=lambda: datetime.utcnow().isoformat())


class AnalysisRunResponseSchema(BaseModel):
    """Schema for analysis run endpoint response"""
    status: str
    cycle_id: str
    timestamp: str
    duration_seconds: Optional[float] = None
    message: str
    analysis: Optional[AnalysisCycleSchema] = None
    error: Optional[str] = None


class AnalysisStatusSchema(BaseModel):
    """Schema for orchestrator status"""
    running: bool
    scheduler_running: bool
    last_analysis: Optional[str] = None
    total_cycles: int
    latest_cycle_status: Optional[str] = None


class AnalysisHistorySchema(BaseModel):
    """Schema for analysis history"""
    total: int
    limit: int
    cycles: List[AnalysisCycleSchema]


class ErrorResponseSchema(BaseModel):
    """Schema for error responses"""
    status: str = "error"
    error: str
    detail: Optional[str] = None
    timestamp: str = Field(default_factory=lambda: datetime.utcnow().isoformat())


# ============================================================================
# Utility Schemas
# ============================================================================

class PaginationSchema(BaseModel):
    """Schema for pagination"""
    limit: int = Field(default=10, ge=1, le=100)
    offset: int = Field(default=0, ge=0)
