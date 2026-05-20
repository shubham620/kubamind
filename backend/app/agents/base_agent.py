"""
Base Agent class - Foundation for all AI agents
"""

from abc import ABC, abstractmethod
from datetime import datetime
from typing import Dict, List, Any
import logging

logger = logging.getLogger(__name__)


class BaseAgent(ABC):
    """Abstract base class for AI agents"""

    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
        self.last_analysis = None
        self.insights = []

    @abstractmethod
    async def analyze(self) -> Dict[str, Any]:
        """Perform analysis - must be implemented by subclasses"""
        pass

    @abstractmethod
    async def get_insights(self) -> List[Dict[str, Any]]:
        """Get current insights - must be implemented by subclasses"""
        pass

    async def log_insight(self, insight: Dict[str, Any]):
        """Log an insight"""
        insight["timestamp"] = datetime.utcnow().isoformat()
        insight["agent"] = self.name
        self.insights.append(insight)
        logger.info(f"[{self.name}] New insight: {insight}")

    def get_status(self) -> Dict[str, Any]:
        """Get agent status"""
        return {
            "name": self.name,
            "description": self.description,
            "status": "active",
            "last_analysis": self.last_analysis,
            "insight_count": len(self.insights)
        }
