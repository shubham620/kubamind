"""
AI Reasoning Engine
Correlates insights from all agents to generate root cause analysis
"""

from datetime import datetime
from typing import Dict, List, Any
import logging

from app.agents.cpu_agent import cpu_agent
from app.agents.memory_agent import memory_agent
from app.agents.storage_agent import storage_agent
from app.agents.network_agent import network_agent
from app.agents.log_agent import log_agent
from app.agents.dependency_agent import dependency_agent

logger = logging.getLogger(__name__)


class ReasoningEngine:
    """Central AI reasoning engine that correlates agent insights"""

    def __init__(self):
        self.agents = [
            cpu_agent,
            memory_agent,
            storage_agent,
            network_agent,
            log_agent,
            dependency_agent
        ]
        self.correlation_rules = []
        self.incidents = []

    async def analyze_all(self) -> Dict[str, Any]:
        """Run all agents and correlate their insights"""
        logger.info("🤖 Running all agents...")

        # Collect insights from all agents
        agent_insights = {}
        for agent in self.agents:
            insights = await agent.analyze()
            agent_insights[agent.name] = insights

        # Correlate insights
        correlations = await self._correlate_insights(agent_insights)
        root_causes = await self._identify_root_causes(correlations)
        recommendations = await self._generate_recommendations(root_causes)

        result = {
            "timestamp": datetime.utcnow().isoformat(),
            "agent_insights": agent_insights,
            "correlations": correlations,
            "root_causes": root_causes,
            "recommendations": recommendations
        }

        logger.info(f"✓ Analysis complete: {len(correlations)} correlations found")
        return result

    async def _correlate_insights(self, agent_insights: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Correlate insights from multiple agents"""
        correlations = []

        # Example correlation: If CPU Agent detects spike AND Log Agent detects errors
        cpu_insights = agent_insights.get("cpu_agent", {})
        log_insights = agent_insights.get("log_agent", {})
        network_insights = agent_insights.get("network_agent", {})

        if cpu_insights.get("anomalies") and log_insights.get("error_patterns"):
            correlations.append({
                "type": "cpu_driven_errors",
                "agents": ["cpu_agent", "log_agent"],
                "description": "High CPU usage correlates with increased error rates",
                "confidence": 0.85,
                "affected_services": ["payment-service"],
                "severity": "high"
            })

        # Correlation: If Memory Agent detects leak AND Network Agent detects latency
        memory_insights = agent_insights.get("memory_agent", {})
        if memory_insights.get("leaks") and network_insights.get("latency_issues"):
            correlations.append({
                "type": "memory_leak_cascade",
                "agents": ["memory_agent", "network_agent"],
                "description": "Memory leak causes GC pauses, leading to increased latency",
                "confidence": 0.75,
                "affected_services": ["analytics-service"],
                "severity": "high"
            })

        # Correlation: Database bottleneck (Storage + Network)
        storage_insights = agent_insights.get("storage_agent", {})
        if storage_insights.get("bottlenecks") and network_insights.get("bottlenecks"):
            correlations.append({
                "type": "database_bottleneck",
                "agents": ["storage_agent", "network_agent", "dependency_agent"],
                "description": "Database I/O bottleneck causing connection pool exhaustion",
                "confidence": 0.90,
                "affected_services": ["backend", "payment-service", "user-service"],
                "severity": "critical"
            })

        return correlations

    async def _identify_root_causes(self, correlations: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Identify root causes from correlations"""
        root_causes = []

        for correlation in correlations:
            if correlation["type"] == "cpu_driven_errors":
                root_causes.append({
                    "id": "rc-001",
                    "title": "High request volume causing CPU spikes",
                    "description": "Payment service experiencing unusual traffic spike",
                    "probability": 0.85,
                    "affected_components": ["payment-service", "backend"],
                    "timeline": "Started 2 hours ago"
                })

            elif correlation["type"] == "memory_leak_cascade":
                root_causes.append({
                    "id": "rc-002",
                    "title": "Memory leak in analytics service",
                    "description": "Unbounded growth in cache causing excessive GC pauses",
                    "probability": 0.75,
                    "affected_components": ["analytics-service"],
                    "timeline": "Gradual degradation over 24 hours"
                })

            elif correlation["type"] == "database_bottleneck":
                root_causes.append({
                    "id": "rc-003",
                    "title": "Database I/O bottleneck",
                    "description": "Inefficient queries on large table causing lock contention",
                    "probability": 0.90,
                    "affected_components": ["database", "backend"],
                    "timeline": "Recurring every night at peak hours"
                })

        return root_causes

    async def _generate_recommendations(self, root_causes: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Generate actionable recommendations"""
        recommendations = []

        for root_cause in root_causes:
            if "CPU" in root_cause["title"]:
                recommendations.extend([
                    {
                        "priority": "high",
                        "action": "Scale payment-service horizontally",
                        "impact": "Distribute load across more pods",
                        "effort": "low"
                    },
                    {
                        "priority": "medium",
                        "action": "Implement request rate limiting",
                        "impact": "Prevent traffic spikes",
                        "effort": "medium"
                    }
                ])

            elif "memory" in root_cause["title"].lower():
                recommendations.extend([
                    {
                        "priority": "high",
                        "action": "Investigate cache size growth",
                        "impact": "Identify memory leak source",
                        "effort": "medium"
                    },
                    {
                        "priority": "medium",
                        "action": "Implement cache eviction policy",
                        "impact": "Prevent unbounded growth",
                        "effort": "low"
                    }
                ])

            elif "database" in root_cause["title"].lower():
                recommendations.extend([
                    {
                        "priority": "critical",
                        "action": "Optimize slow queries",
                        "impact": "Reduce I/O bottleneck by 40%",
                        "effort": "high"
                    },
                    {
                        "priority": "high",
                        "action": "Add database index on frequently queried columns",
                        "impact": "Reduce query time by 60%",
                        "effort": "medium"
                    }
                ])

        return recommendations

    async def get_status(self) -> Dict[str, Any]:
        """Get status of all agents"""
        return {
            "agents": [agent.get_status() for agent in self.agents],
            "last_analysis": datetime.utcnow().isoformat()
        }


# Singleton instance
reasoning_engine = ReasoningEngine()
