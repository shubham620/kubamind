"""
Orchestrator - Coordinates execution of all AI agents and engines
Runs analysis on a 30-second schedule
"""

import asyncio
import logging
from datetime import datetime
from typing import Dict, List, Any
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from app.reasoning.engine import reasoning_engine
from app.predictive.engine import predictive_engine
from app.nlp.explanation_engine import explanation_engine
from app.chat.assistant import chat_assistant

logger = logging.getLogger(__name__)


class AnalysisOrchestrator:
    """Orchestrates all analysis components"""

    def __init__(self):
        self.scheduler = None
        self.is_running = False
        self.last_analysis = None
        self.analysis_results = []
        self.max_results_history = 100

    async def initialize(self):
        """Initialize the orchestrator"""
        logger.info("🚀 Initializing Analysis Orchestrator")
        
        self.scheduler = AsyncIOScheduler()
        self.scheduler.add_job(
            self.run_analysis_cycle,
            "interval",
            seconds=30,
            id="analysis_cycle",
            misfire_grace_time=10,
            coalesce=True
        )
        
        logger.info("✓ Orchestrator initialized with 30-second cycle")

    async def start(self):
        """Start the orchestrator scheduler"""
        if not self.scheduler:
            await self.initialize()
        
        if not self.scheduler.running:
            self.scheduler.start()
            self.is_running = True
            logger.info("✓ Orchestrator scheduler started")

    async def stop(self):
        """Stop the orchestrator scheduler"""
        if self.scheduler and self.scheduler.running:
            self.scheduler.shutdown(wait=False)
            self.is_running = False
            logger.info("✓ Orchestrator scheduler stopped")

    async def run_analysis_cycle(self) -> Dict[str, Any]:
        """Execute complete analysis cycle"""
        cycle_start = datetime.utcnow()
        logger.info("🔄 Starting analysis cycle...")
        
        try:
            # Phase 1: Reasoning Engine - Correlate all agent insights
            logger.info("📊 Phase 1: Running Reasoning Engine...")
            reasoning_result = await reasoning_engine.analyze_all()
            
            # Phase 2: Predictive Engine - Generate predictions
            logger.info("🔮 Phase 2: Running Predictive Engine...")
            predictions = await predictive_engine.analyze_all()
            
            # Phase 3: NLP Engine - Generate explanations
            logger.info("💬 Phase 3: Running NLP Engine...")
            explanations = await self._generate_explanations(
                reasoning_result,
                predictions
            )
            
            # Phase 4: Chat Assistant - Generate summary
            logger.info("🤖 Phase 4: Running Chat Assistant...")
            summary_query = "What is the current infrastructure status?"
            chat_response = await chat_assistant.process_query(summary_query)
            
            # Compile complete result
            cycle_result = {
                "cycle_id": cycle_start.isoformat(),
                "timestamp": datetime.utcnow().isoformat(),
                "duration_seconds": (datetime.utcnow() - cycle_start).total_seconds(),
                "status": "success",
                "reasoning": reasoning_result,
                "predictions": predictions,
                "explanations": explanations,
                "summary": chat_response["response"]
            }
            
            # Store result
            self.last_analysis = cycle_result
            self.analysis_results.append(cycle_result)
            
            # Keep only last N results to prevent memory bloat
            if len(self.analysis_results) > self.max_results_history:
                self.analysis_results = self.analysis_results[-self.max_results_history:]
            
            logger.info(f"✓ Analysis cycle complete in {cycle_result['duration_seconds']:.2f}s")
            return cycle_result
            
        except Exception as e:
            logger.error(f"❌ Analysis cycle failed: {e}", exc_info=True)
            error_result = {
                "cycle_id": cycle_start.isoformat(),
                "timestamp": datetime.utcnow().isoformat(),
                "duration_seconds": (datetime.utcnow() - cycle_start).total_seconds(),
                "status": "error",
                "error": str(e)
            }
            self.analysis_results.append(error_result)
            return error_result

    async def _generate_explanations(
        self,
        reasoning_result: Dict[str, Any],
        predictions: Dict[str, Any]
    ) -> Dict[str, List[str]]:
        """Generate NLP explanations for analysis results"""
        explanations = {
            "correlations": [],
            "root_causes": [],
            "predictions": []
        }
        
        try:
            # Explain correlations
            for correlation in reasoning_result.get("correlations", []):
                exp = await explanation_engine.explain_correlation(correlation)
                explanations["correlations"].append(exp)
            
            # Explain root causes
            for root_cause in reasoning_result.get("root_causes", []):
                exp = await explanation_engine.explain_root_cause(root_cause)
                explanations["root_causes"].append(exp)
            
            # Explain predictions
            all_predictions = [
                p for pred_list in [
                    predictions.get("pod_crashes", []),
                    predictions.get("oom_events", []),
                    predictions.get("disk_exhaustion", []),
                    predictions.get("performance_degradation", [])
                ]
                for p in pred_list
            ]
            
            for prediction in all_predictions[:3]:  # Limit to top 3
                exp = await explanation_engine.explain_prediction({
                    "pod": prediction.get("pod") or prediction.get("pvc") or prediction.get("service"),
                    "predicted_time_hours": prediction.get("predicted_time_hours"),
                    "reason": prediction.get("reason"),
                    "prediction_type": list(prediction.keys())[0]
                })
                explanations["predictions"].append(exp)
            
        except Exception as e:
            logger.warning(f"Error generating explanations: {e}")
        
        return explanations

    async def get_latest_analysis(self) -> Dict[str, Any]:
        """Get the latest analysis result"""
        if not self.last_analysis:
            return {
                "status": "no_analysis_yet",
                "message": "No analysis has been run yet"
            }
        return self.last_analysis

    async def get_analysis_history(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get recent analysis results"""
        return self.analysis_results[-limit:]

    def get_status(self) -> Dict[str, Any]:
        """Get orchestrator status"""
        return {
            "running": self.is_running,
            "scheduler_running": self.scheduler.running if self.scheduler else False,
            "last_analysis": self.last_analysis.get("timestamp") if self.last_analysis else None,
            "total_cycles": len(self.analysis_results),
            "latest_cycle_status": self.last_analysis.get("status") if self.last_analysis else None
        }


# Singleton instance
orchestrator = AnalysisOrchestrator()
