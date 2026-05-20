"""
Comprehensive tests for the Predictive Analytics Engine
Tests all 4 ML models: LSTM, Prophet, Isolation Forest, XGBoost
"""

import pytest
import numpy as np
import pandas as pd
import asyncio
from datetime import datetime, timedelta
import sys
import os

# Configure pytest-asyncio
pytest_plugins = ('pytest_asyncio',)

# Set asyncio mode to auto
pytestmark = pytest.mark.asyncio

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from app.predictive.engine import (
    PredictiveEngine,
    LSTMCrashPredictor,
    ProphetTimeSeriesForecaster,
    AnomalyDetector,
    SeverityPredictor
)


@pytest.fixture(scope="session")
def event_loop():
    """Create an event loop for async tests"""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


class TestLSTMCrashPredictor:
    """Test LSTM model for pod crash prediction"""
    
    def test_lstm_initialization(self):
        """Test LSTM model initialization"""
        predictor = LSTMCrashPredictor(sequence_length=30)
        assert predictor.sequence_length == 30
        assert predictor.model is None
        assert not predictor.is_trained
    
    def test_lstm_mock_data_generation(self):
        """Test mock data generation"""
        predictor = LSTMCrashPredictor()
        X, y = predictor._generate_mock_data(n_samples=100)
        
        assert X.shape == (100, 30, 2)  # 100 samples, 30 timesteps, 2 features
        assert y.shape == (100,)
        assert set(y) <= {0, 1}
    
    def test_lstm_training(self):
        """Test LSTM model training"""
        predictor = LSTMCrashPredictor()
        metrics = predictor.fit()
        
        assert predictor.is_trained
        assert predictor.model is not None
        assert 'final_loss' in metrics
        assert 'final_accuracy' in metrics
        assert 0 <= metrics['final_accuracy'] <= 1
    
    def test_lstm_prediction(self):
        """Test LSTM predictions"""
        predictor = LSTMCrashPredictor()
        predictor.fit()
        
        # Create test data: (5 samples, 30 timesteps, 2 features)
        X_test = np.random.uniform(10, 90, (5, 30, 2))
        predictions = predictor.predict(X_test)
        
        assert predictions.shape == (5, 1)
        assert np.all((predictions >= 0) & (predictions <= 1))
    
    def test_lstm_prediction_without_training(self):
        """Test LSTM prediction triggers training if needed"""
        predictor = LSTMCrashPredictor()
        X_test = np.random.uniform(10, 90, (2, 30, 2))
        predictions = predictor.predict(X_test)
        
        assert predictor.is_trained
        assert predictions.shape == (2, 1)


class TestProphetTimeSeriesForecaster:
    """Test Prophet time series forecasting model"""
    
    def test_prophet_initialization(self):
        """Test Prophet model initialization"""
        forecaster = ProphetTimeSeriesForecaster()
        assert len(forecaster.models) == 0
        assert not forecaster.is_trained
    
    def test_prophet_mock_data_generation(self):
        """Test mock time series data generation"""
        forecaster = ProphetTimeSeriesForecaster()
        df = forecaster._generate_mock_data(n_days=90)
        
        assert len(df) == 90
        assert 'ds' in df.columns
        assert 'y' in df.columns
        assert df['ds'].dtype == 'datetime64[ns]'
    
    def test_prophet_training(self):
        """Test Prophet model training"""
        forecaster = ProphetTimeSeriesForecaster()
        metrics = forecaster.fit(metric='disk_usage')
        
        assert forecaster.is_trained
        assert 'disk_usage' in forecaster.models
        assert metrics['metric'] == 'disk_usage'
        assert metrics['status'] == 'trained'
    
    def test_prophet_prediction(self):
        """Test Prophet forecasting"""
        forecaster = ProphetTimeSeriesForecaster()
        forecaster.fit(metric='disk_usage')
        
        forecast = forecaster.predict(periods=7, metric='disk_usage')
        
        assert len(forecast) == 7
        assert 'ds' in forecast.columns
        assert 'yhat' in forecast.columns
        assert 'yhat_lower' in forecast.columns
        assert 'yhat_upper' in forecast.columns
    
    def test_prophet_multiple_metrics(self):
        """Test Prophet with multiple metrics"""
        forecaster = ProphetTimeSeriesForecaster()
        forecaster.fit(metric='disk_usage')
        forecaster.fit(metric='memory_growth')
        
        assert len(forecaster.models) == 2
        assert 'disk_usage' in forecaster.models
        assert 'memory_growth' in forecaster.models


class TestAnomalyDetector:
    """Test Isolation Forest anomaly detection"""
    
    def test_anomaly_detector_initialization(self):
        """Test anomaly detector initialization"""
        detector = AnomalyDetector(contamination=0.1)
        assert detector.model is not None
        assert detector.model.contamination == 0.1
        assert not detector.is_trained
    
    def test_anomaly_detector_mock_data(self):
        """Test mock anomaly data generation"""
        detector = AnomalyDetector()
        X, y = detector._generate_mock_data(n_samples=200, n_features=4)
        
        assert X.shape == (200, 4)
        assert y.shape == (200,)
        assert np.sum(y == -1) == 20  # 10% anomalies
    
    def test_anomaly_detector_training(self):
        """Test anomaly detector training"""
        detector = AnomalyDetector()
        metrics = detector.fit()
        
        assert detector.is_trained
        assert metrics['contamination'] == 0.1
        assert metrics['training_samples'] == 500
    
    def test_anomaly_detector_prediction(self):
        """Test anomaly detection predictions"""
        detector = AnomalyDetector()
        detector.fit()
        
        # Normal data
        X_normal = np.random.normal(50, 10, (10, 4))
        predictions, scores = detector.predict(X_normal)
        
        assert predictions.shape == (10,)
        assert scores.shape == (10,)
        assert set(predictions) <= {-1, 1}
    
    def test_anomaly_detector_identifies_anomalies(self):
        """Test anomaly detector identifies actual anomalies"""
        detector = AnomalyDetector(contamination=0.2)
        detector.fit()
        
        # Mix of normal and anomalous data
        X_normal = np.random.normal(50, 10, (20, 4))
        X_anomaly = np.random.uniform(85, 100, (5, 4))
        X_mixed = np.vstack([X_normal, X_anomaly])
        
        predictions, _ = detector.predict(X_mixed)
        
        # Should detect some anomalies
        assert np.sum(predictions == -1) > 0


class TestSeverityPredictor:
    """Test XGBoost severity prediction model"""
    
    def test_severity_predictor_initialization(self):
        """Test severity predictor initialization"""
        predictor = SeverityPredictor()
        assert predictor.classes == ['low', 'warning', 'critical']
        assert predictor.model is None
        assert not predictor.is_trained
    
    def test_severity_predictor_custom_classes(self):
        """Test with custom severity classes"""
        custom_classes = ['minor', 'major', 'severe']
        predictor = SeverityPredictor(classes=custom_classes)
        assert predictor.classes == custom_classes
    
    def test_severity_predictor_mock_data(self):
        """Test mock severity data generation"""
        predictor = SeverityPredictor()
        X, y = predictor._generate_mock_data(n_samples=300)
        
        assert X.shape == (300, 5)
        assert y.shape == (300,)
        assert set(y) <= {0, 1, 2}
    
    def test_severity_predictor_training(self):
        """Test severity predictor training"""
        predictor = SeverityPredictor()
        metrics = predictor.fit()
        
        assert predictor.is_trained
        assert predictor.model is not None
        assert 'precision' in metrics
        assert 'recall' in metrics
        assert 'f1' in metrics
        assert 0 <= metrics['f1'] <= 1
    
    def test_severity_predictor_prediction(self):
        """Test severity predictions"""
        predictor = SeverityPredictor()
        predictor.fit()
        
        X_test = np.random.uniform(0, 100, (5, 5))
        classes, probabilities = predictor.predict(X_test)
        
        assert len(classes) == 5
        assert all(c in ['low', 'warning', 'critical'] for c in classes)
        assert probabilities.shape == (5, 3)
        assert np.allclose(probabilities.sum(axis=1), 1.0)


class TestPredictiveEngine:
    """Test the main Predictive Engine"""
    
    @pytest.fixture
    def engine(self):
        """Create engine instance"""
        return PredictiveEngine()
    
    def test_engine_initialization(self, engine):
        """Test engine initialization"""
        assert engine.lstm_predictor is not None
        assert engine.prophet_forecaster is not None
        assert engine.anomaly_detector is not None
        assert engine.severity_predictor is not None
    
    def test_engine_models_trained(self, engine):
        """Test all models are trained on init"""
        assert engine.lstm_predictor.is_trained
        assert engine.prophet_forecaster.is_trained
        assert engine.anomaly_detector.is_trained
        assert engine.severity_predictor.is_trained
    
    @pytest.mark.asyncio(scope="function")
    async def test_predict_pod_crashes(self, engine):
        """Test pod crash predictions"""
        predictions = await engine.predict_pod_crashes()
        
        assert len(predictions) > 0
        for pred in predictions:
            assert 'pod' in pred
            assert 'probability' in pred
            assert 'predicted_time_hours' in pred
            assert 'reason' in pred
            assert 'confidence' in pred
            assert 0 <= pred['probability'] <= 1
            assert 0 <= pred['confidence'] <= 1
            assert pred['predicted_time_hours'] > 0
    
    @pytest.mark.asyncio(scope="function")
    async def test_predict_oom_events(self, engine):
        """Test OOM event predictions"""
        predictions = await engine.predict_oom_events()
        
        assert len(predictions) > 0
        for pred in predictions:
            assert 'pod' in pred
            assert 'probability' in pred
            assert 'predicted_time_hours' in pred
            assert 'current_usage_percent' in pred
            assert 'growth_rate_percent_hour' in pred
            assert 'confidence' in pred
            assert 0 <= pred['current_usage_percent'] <= 100
    
    @pytest.mark.asyncio(scope="function")
    async def test_predict_disk_exhaustion(self, engine):
        """Test disk exhaustion predictions"""
        predictions = await engine.predict_disk_exhaustion()
        
        assert len(predictions) > 0
        for pred in predictions:
            assert 'pvc' in pred
            assert 'probability' in pred
            assert 'predicted_time_days' in pred
            assert 'current_usage_percent' in pred
            assert 'growth_rate_percent_day' in pred
            assert 'confidence' in pred
            assert pred['predicted_time_days'] > 0
    
    @pytest.mark.asyncio(scope="function")
    async def test_predict_performance_degradation(self, engine):
        """Test performance degradation predictions"""
        predictions = await engine.predict_performance_degradation()
        
        assert len(predictions) > 0
        for pred in predictions:
            assert 'service' in pred
            assert 'metric' in pred
            assert 'current_ms' in pred
            assert 'predicted_ms' in pred
            assert 'predicted_time_hours' in pred
            assert 'reason' in pred
            assert 'confidence' in pred
            assert 'severity' in pred
            assert pred['severity'] in ['low', 'warning', 'critical']
    
    @pytest.mark.asyncio(scope="function")
    async def test_analyze_all(self, engine):
        """Test comprehensive analysis"""
        results = await engine.analyze_all()
        
        assert 'timestamp' in results
        assert 'pod_crashes' in results
        assert 'oom_events' in results
        assert 'disk_exhaustion' in results
        assert 'performance_degradation' in results
        assert 'model_status' in results
        
        # Verify all models are trained
        assert results['model_status']['lstm']['trained']
        assert results['model_status']['prophet']['trained']
        assert results['model_status']['anomaly_detection']['trained']
        assert results['model_status']['severity']['trained']
    
    def test_model_persistence(self, engine, tmp_path):
        """Test saving and loading models"""
        model_dir = str(tmp_path / "models")
        
        # Save
        engine.save_models(model_dir)
        assert os.path.exists(model_dir)
        
        # Create new engine
        new_engine = PredictiveEngine.__new__(PredictiveEngine)
        new_engine.predictions = []
        new_engine.model_accuracy = {}
        new_engine.lstm_predictor = LSTMCrashPredictor()
        new_engine.prophet_forecaster = ProphetTimeSeriesForecaster()
        new_engine.anomaly_detector = AnomalyDetector()
        new_engine.severity_predictor = SeverityPredictor()
        
        # Load
        new_engine.load_models(model_dir)
        assert new_engine.lstm_predictor.is_trained
        assert new_engine.prophet_forecaster.is_trained


class TestModelPerformance:
    """Test model performance metrics"""
    
    def test_lstm_performance_metrics(self):
        """Test LSTM produces reasonable accuracy"""
        predictor = LSTMCrashPredictor()
        metrics = predictor.fit()
        
        # Should have decent accuracy
        assert metrics['final_accuracy'] > 0.5
        assert metrics['val_accuracy'] > 0.4
    
    def test_severity_predictor_metrics(self):
        """Test severity predictor quality metrics"""
        predictor = SeverityPredictor()
        metrics = predictor.fit()
        
        # All metrics should be valid
        assert 0 <= metrics['precision'] <= 1
        assert 0 <= metrics['recall'] <= 1
        assert 0 <= metrics['f1'] <= 1
    
    def test_anomaly_detector_sensitivity(self):
        """Test anomaly detector sensitivity"""
        detector = AnomalyDetector(contamination=0.1)
        detector.fit()
        
        # Create anomalous data
        X_anomaly = np.random.uniform(90, 100, (100, 4))
        predictions, _ = detector.predict(X_anomaly)
        
        # Should detect many anomalies
        anomaly_rate = np.sum(predictions == -1) / len(predictions)
        assert anomaly_rate > 0.05


@pytest.mark.asyncio(scope="function")
async def test_engine_async_compatibility():
    """Test async/await compatibility"""
    engine = PredictiveEngine()
    
    # All methods should be awaitable
    results = await engine.analyze_all()
    assert isinstance(results, dict)
    
    crashes = await engine.predict_pod_crashes()
    assert isinstance(crashes, list)


def test_data_validation():
    """Test that predictions contain valid data types"""
    engine = PredictiveEngine()
    
    async def validate():
        # Pod crashes
        crashes = await engine.predict_pod_crashes()
        for crash in crashes:
            assert isinstance(crash['probability'], (int, float))
            assert isinstance(crash['predicted_time_hours'], (int, float))
        
        # OOM events
        oom = await engine.predict_oom_events()
        for event in oom:
            assert isinstance(event['current_usage_percent'], (int, float))
            assert 0 <= event['current_usage_percent'] <= 100
        
        # Disk exhaustion
        disk = await engine.predict_disk_exhaustion()
        for d in disk:
            assert isinstance(d['predicted_time_days'], (int, float))
    
    asyncio.run(validate())


if __name__ == '__main__':
    pytest.main([__file__, '-v', '--tb=short'])
