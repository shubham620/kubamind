"""
NLP Explanation Engine
Generates human-readable explanations for infrastructure issues
"""

from datetime import datetime
from typing import Dict, List, Any
import logging

logger = logging.getLogger(__name__)


class ExplanationEngine:
    """Generates NLP explanations"""

    def __init__(self):
        self.explanation_templates = {}

    async def explain_anomaly(self, anomaly: Dict[str, Any]) -> str:
        """Generate explanation for an anomaly"""
        anomaly_type = anomaly.get("type", "unknown")
        pod = anomaly.get("pod", "unknown pod")
        severity = anomaly.get("severity", "unknown")

        if anomaly_type == "cpu_spike":
            return f"The {pod} experienced an unexpected CPU spike to {anomaly.get('current_usage', 'N/A')}%. This is typically caused by sudden traffic increase or inefficient processing. Recommendation: Check recent deployments or scaling policies."

        elif anomaly_type == "memory_leak":
            pod = anomaly.get("pod", "unknown pod")
            growth = anomaly.get("growth_rate_mb_per_hour", "N/A")
            return f"Memory leak detected in {pod} growing at {growth} MB/hour. The service may crash due to OOM in the next few hours. Immediate action: Review recent code changes for memory management issues."

        else:
            return f"Detected {anomaly_type} in {pod} with severity {severity}. Automatic diagnosis requires more context."

    async def explain_correlation(self, correlation: Dict[str, Any]) -> str:
        """Generate explanation for a correlation"""
        corr_type = correlation.get("type", "unknown")

        if corr_type == "cpu_driven_errors":
            return "High CPU utilization is causing timeouts and errors. The system is overloaded. Scaling or performance optimization is needed."

        elif corr_type == "memory_leak_cascade":
            return "A memory leak is causing garbage collection pauses, which increases latency and timeouts across dependent services. Root cause must be fixed in the leaking service."

        elif corr_type == "database_bottleneck":
            return "Database I/O throughput is saturated, causing connection pool exhaustion. This cascades to all dependent services. Query optimization or database scaling is required."

        else:
            return f"Correlation detected: {corr_type}. Multiple infrastructure components are affected."

    async def explain_root_cause(self, root_cause: Dict[str, Any]) -> str:
        """Generate detailed explanation for a root cause"""
        title = root_cause.get("title", "Unknown issue")
        description = root_cause.get("description", "")
        probability = root_cause.get("probability", 0) * 100
        components = ", ".join(root_cause.get("affected_components", []))

        return f"**{title}** (Probability: {probability:.1f}%)\n\n{description}\n\nAffected components: {components}"

    async def explain_prediction(self, prediction: Dict[str, Any]) -> str:
        """Generate explanation for a prediction"""
        pred_type = prediction.get("prediction_type", "unknown")
        pod = prediction.get("pod", "unknown")
        hours = prediction.get("predicted_time_hours", "unknown")
        reason = prediction.get("reason", "")

        if pred_type == "oom_risk":
            return f"⚠️ **OOM Risk** for {pod} in approximately {hours} hours. Reason: {reason}. Recommended action: Increase memory limit or optimize application."

        elif pred_type == "pod_crash":
            return f"🚨 **Pod Crash Predicted** for {pod}. Reason: {reason}. Recommended action: Investigate and address the underlying issue immediately."

        else:
            return f"Prediction for {pod}: {pred_type} in {hours} hours."

    async def generate_executive_summary(self, analysis_result: Dict[str, Any]) -> str:
        """Generate executive summary of system health"""
        root_causes = analysis_result.get("root_causes", [])
        predictions = analysis_result.get("predictions", {})

        if not root_causes:
            return "✅ Infrastructure is operating normally. No critical issues detected."

        summary_lines = ["📊 Infrastructure Health Summary:\n"]

        for i, rc in enumerate(root_causes[:3], 1):
            summary_lines.append(f"{i}. {rc.get('title', 'Issue')}")

        if predictions.get("pod_crashes"):
            summary_lines.append(f"\n⚠️ {len(predictions['pod_crashes'])} pod crashes predicted")

        if predictions.get("oom_events"):
            summary_lines.append(f"⚠️ {len(predictions['oom_events'])} OOM events predicted")

        return "\n".join(summary_lines)


# Singleton instance
explanation_engine = ExplanationEngine()
