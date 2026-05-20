"""
Chat Assistant - AI conversational interface
"""

from datetime import datetime
from typing import Dict, List, Any
import logging

logger = logging.getLogger(__name__)


class ChatAssistant:
    """AI Chat Assistant for infrastructure queries"""

    def __init__(self):
        self.conversation_history = []
        self.context = {}

    async def process_query(self, query: str, session_id: str = None) -> Dict[str, Any]:
        """Process user query and generate response"""
        logger.info(f"Processing query: {query}")

        # Classify query type
        query_type = await self._classify_query(query)

        # Route to appropriate handler
        if query_type == "status":
            response = await self._handle_status_query(query)
        elif query_type == "anomaly":
            response = await self._handle_anomaly_query(query)
        elif query_type == "prediction":
            response = await self._handle_prediction_query(query)
        elif query_type == "recommendation":
            response = await self._handle_recommendation_query(query)
        elif query_type == "dependency":
            response = await self._handle_dependency_query(query)
        else:
            response = await self._handle_general_query(query)

        return {
            "query": query,
            "query_type": query_type,
            "response": response,
            "timestamp": datetime.utcnow().isoformat()
        }

    async def _classify_query(self, query: str) -> str:
        """Classify the type of query"""
        query_lower = query.lower()

        if any(w in query_lower for w in ["status", "how is", "health", "everything", "current"]):
            return "status"
        elif any(w in query_lower for w in ["anomaly", "spike", "leak", "error", "issue"]):
            return "anomaly"
        elif any(w in query_lower for w in ["predict", "forecast", "upcoming", "future", "will"]):
            return "prediction"
        elif any(w in query_lower for w in ["recommend", "suggest", "fix", "optimize"]):
            return "recommendation"
        elif any(w in query_lower for w in ["depend", "connect", "relate", "service", "talk"]):
            return "dependency"
        else:
            return "general"

    async def _handle_status_query(self, query: str) -> str:
        """Handle status queries"""
        return """The infrastructure is operating with several issues:

**Critical Issues:**
- Database I/O bottleneck affecting multiple services
- Memory leak in analytics-service trending toward OOM

**Predictions:**
- Database pod crash predicted in ~5 hours
- Payment service performance degradation expected in 2 hours

**Recommendations:**
1. Optimize slow database queries immediately
2. Investigate memory leak in analytics-service
3. Consider horizontal scaling for payment-service"""

    async def _handle_anomaly_query(self, query: str) -> str:
        """Handle anomaly-related queries"""
        return """**Recent Anomalies Detected:**

1. **CPU Spike in payment-service-1** (High severity)
   - Current: 87.5% CPU usage
   - Threshold: 80%
   - Duration: 2 minutes
   - Likely cause: Traffic spike

2. **Memory Leak in analytics-service-1** (High severity)
   - Growth: 12.5 MB/hour
   - Current: 450 MB / 512 MB limit
   - Risk: OOM in ~5 hours

3. **Database Connection Pool Exhaustion** (Critical)
   - Current: 95/100 connections
   - Affecting: Backend, payment-service, user-service"""

    async def _handle_prediction_query(self, query: str) -> str:
        """Handle prediction queries"""
        return """**Infrastructure Predictions (Next 24 Hours):**

🔴 **Critical Predictions:**
- Database pod OOM event in ~5 hours (Confidence: 80%)
- Payment service performance degradation in ~2 hours (Confidence: 78%)

🟡 **High-Risk Predictions:**
- Log storage exhaustion in ~4 days (Confidence: 72%)
- Additional pod crashes if memory leak unaddressed (Confidence: 75%)

**Recommended Actions:**
1. Address memory leak immediately
2. Optimize database queries
3. Scale payment-service horizontally"""

    async def _handle_recommendation_query(self, query: str) -> str:
        """Handle recommendation queries"""
        return """**Top Recommendations for Infrastructure Improvement:**

**Priority: CRITICAL**
1. Fix memory leak in analytics-service
   - Impact: Prevent pod crashes and improve overall stability
   - Effort: High
   - Timeline: 2-3 hours

2. Optimize database queries
   - Impact: Reduce I/O bottleneck by 40%
   - Effort: High  
   - Timeline: 4-6 hours

**Priority: HIGH**
3. Horizontal scaling for payment-service
   - Impact: Distribute load, reduce CPU spikes
   - Effort: Low
   - Timeline: 30 minutes

4. Implement query caching
   - Impact: Reduce database load
   - Effort: Medium
   - Timeline: 2 hours"""

    async def _handle_dependency_query(self, query: str) -> str:
        """Handle dependency queries"""
        return """**Service Dependency Analysis:**

**Critical Dependencies:**
- Database is a single point of failure for: Backend, Payment-service, User-service, Analytics-service
- Auth-service is critical for: Frontend, Backend
- Cache is used by: Backend, Analytics-service

**Cascade Risk Analysis:**
- If Database fails → 4 services affected, Complete system degradation
- If Auth-service fails → 2 services affected, Users cannot authenticate
- If Backend fails → Payment and User services lose API connectivity

**Recommendations:**
- Implement database replication/failover
- Add circuit breakers for cross-service calls
- Implement graceful degradation for auth failures"""

    async def _handle_general_query(self, query: str) -> str:
        """Handle general queries"""
        return f"""I'm processing your query: "{query}"

I can help with:
- **Status queries**: "How is the infrastructure?" "What's the current health?"
- **Anomaly questions**: "What anomalies are detected?" "Any errors?"
- **Predictions**: "What issues are predicted?" "When will the database fail?"
- **Recommendations**: "What should I fix?" "How do I optimize?"
- **Dependencies**: "Which services depend on this?" "What's the cascade risk?"

Feel free to ask anything about your infrastructure!"""


# Singleton instance
chat_assistant = ChatAssistant()
