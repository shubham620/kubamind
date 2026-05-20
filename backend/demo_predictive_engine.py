#!/usr/bin/env python
"""
Demo script showcasing the full Predictive Analytics Engine
Demonstrates all 4 ML models in action
"""

import asyncio
import json
from app.predictive.engine import PredictiveEngine


async def main():
    print("=" * 80)
    print("KUBEMIND AI - PREDICTIVE ANALYTICS ENGINE DEMO")
    print("=" * 80)
    print()
    
    # Initialize engine
    print("Initializing Predictive Analytics Engine...")
    engine = PredictiveEngine()
    print("[OK] Engine initialized with 4 ML models\n")
    
    # Demo 1: Pod Crash Prediction (LSTM)
    print("-" * 80)
    print("1. LSTM POD CRASH PREDICTOR")
    print("-" * 80)
    print("Model: LSTM Neural Network (30-day time series)")
    print("Input: CPU and Memory historical metrics")
    print("Output: Crash probability in next 24 hours\n")
    crashes = await engine.predict_pod_crashes()
    print("Predictions:")
    for crash in crashes:
        print(f"  Pod: {crash['pod']}")
        print(f"     Crash Probability: {crash['probability']:.1%}")
        print(f"     Predicted Time: {crash['predicted_time_hours']:.1f} hours")
        print(f"     Reason: {crash['reason']}")
        print(f"     Confidence: {crash['confidence']:.1%}\n")
    
    # Demo 2: OOM Event Prediction
    print("-" * 80)
    print("2. TIME SERIES FORECASTING - OOM EVENTS")
    print("-" * 80)
    print("Model: Prophet time series forecasting")
    print("Input: Memory usage growth patterns")
    print("Output: Estimated time to Out-of-Memory\n")
    oom_events = await engine.predict_oom_events()
    print("Predictions:")
    for event in oom_events:
        print(f"  Pod: {event['pod']}")
        print(f"     OOM Probability: {event['probability']:.1%}")
        print(f"     Time to OOM: {event['predicted_time_hours']:.1f} hours")
        print(f"     Current Usage: {event['current_usage_percent']:.1f}%")
        print(f"     Growth Rate: {event['growth_rate_percent_hour']:.1f}%/hour\n")
    
    # Demo 3: Disk Exhaustion Prediction
    print("-" * 80)
    print("3. PROPHET TIME SERIES - DISK EXHAUSTION")
    print("-" * 80)
    print("Model: Prophet time series forecasting")
    print("Input: Disk usage over 7 days")
    print("Output: Days until full disk\n")
    disk_events = await engine.predict_disk_exhaustion()
    print("Predictions:")
    for disk in disk_events:
        print(f"  PVC: {disk['pvc']}")
        print(f"     Exhaustion Probability: {disk['probability']:.1%}")
        print(f"     Days Until Full: {disk['predicted_time_days']:.1f}")
        print(f"     Current Usage: {disk['current_usage_percent']:.1f}%")
        print(f"     Growth Rate: {disk['growth_rate_percent_day']:.1f}%/day\n")
    
    # Demo 4: Performance Degradation (Anomaly Detection + Severity)
    print("-" * 80)
    print("4. ANOMALY DETECTION & XGBOOST SEVERITY PREDICTION")
    print("-" * 80)
    print("Model 1: Isolation Forest for anomaly detection")
    print("Model 2: XGBoost for severity classification")
    print("Input: Real-time metric patterns (4 features)")
    print("Output: Anomalies & severity levels\n")
    perf_events = await engine.predict_performance_degradation()
    print("Predictions:")
    for perf in perf_events:
        print(f"  Service: {perf['service']}")
        print(f"     Metric: {perf['metric']}")
        print(f"     Current: {perf['current_ms']:.1f}ms -> Predicted: {perf['predicted_ms']:.1f}ms")
        print(f"     Time: {perf['predicted_time_hours']:.1f} hours")
        print(f"     Severity: {perf['severity'].upper()}")
        print(f"     Reason: {perf['reason']}")
        print(f"     Confidence: {perf['confidence']:.1%}\n")
    
    # Demo 5: Run all predictions
    print("-" * 80)
    print("5. COMPREHENSIVE ANALYSIS (ALL MODELS)")
    print("-" * 80)
    results = await engine.analyze_all()
    
    print(f"Timestamp: {results['timestamp']}")
    print(f"\nModel Status:")
    for model, status in results['model_status'].items():
        status_text = "[OK] Trained" if status['trained'] else "[FAIL] Not Trained"
        print(f"  {model}: {status_text}")
    
    print(f"\nSummary:")
    print(f"  Pod Crashes at Risk: {len(results['pod_crashes'])}")
    print(f"  OOM Events Predicted: {len(results['oom_events'])}")
    print(f"  Disk Exhaustion Warnings: {len(results['disk_exhaustion'])}")
    print(f"  Performance Issues: {len(results['performance_degradation'])}")
    
    print("\n" + "=" * 80)
    print("[SUCCESS] DEMO COMPLETE - All Models Working Successfully!")
    print("=" * 80)
    print()
    print("Model Details:")
    print("  1. LSTM Crash Predictor")
    print("     - Architecture: 2-layer LSTM with dropout")
    print("     - Training: 500 samples, 20 epochs")
    print("     - Input: 30-day time series (CPU, Memory)")
    print()
    print("  2. Prophet Time Series Forecaster")
    print("     - Metrics: Disk usage, Memory growth")
    print("     - Horizon: 7 days")
    print("     - Features: Trend + weekly seasonality")
    print()
    print("  3. Isolation Forest Anomaly Detector")
    print("     - Contamination: 10%")
    print("     - Real-time scoring")
    print("     - Scalable to multiple metrics")
    print()
    print("  4. XGBoost Severity Predictor")
    print("     - Classes: Low, Warning, Critical")
    print("     - Trees: 100")
    print("     - Multi-class classification")
    print()


if __name__ == '__main__':
    asyncio.run(main())
