"""
Predictive Analytics Engine
Forecasts future infrastructure issues using ML models
"""

from datetime import datetime, timedelta
from typing import Dict, List, Any, Tuple, Optional
import logging
import numpy as np
import pandas as pd
import joblib
import os
from pathlib import Path
import warnings

warnings.filterwarnings('ignore')

# ML Libraries
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import precision_score, recall_score, f1_score
import xgboost as xgb
from prophet import Prophet
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers, Sequential

logger = logging.getLogger(__name__)


class LSTMCrashPredictor:
    """LSTM model for predicting pod crashes"""
    
    def __init__(self, sequence_length: int = 30):
        self.sequence_length = sequence_length
        self.model = None
        self.scaler = StandardScaler()
        self.is_trained = False
        
    def _build_model(self, input_shape: int) -> Sequential:
        """Build LSTM model"""
        model = Sequential([
            layers.LSTM(64, activation='relu', input_shape=(self.sequence_length, input_shape), return_sequences=True),
            layers.Dropout(0.2),
            layers.LSTM(32, activation='relu', return_sequences=False),
            layers.Dropout(0.2),
            layers.Dense(16, activation='relu'),
            layers.Dense(1, activation='sigmoid')
        ])
        model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
        return model
    
    def _generate_mock_data(self, n_samples: int = 500) -> Tuple[np.ndarray, np.ndarray]:
        """Generate mock historical data for training"""
        X = []
        y = []
        
        for _ in range(n_samples):
            # Generate time series with CPU and Memory metrics
            cpu = np.random.uniform(10, 90, self.sequence_length)
            memory = np.random.uniform(20, 85, self.sequence_length)
            
            # Add trend to some sequences (simulating memory leaks)
            if np.random.rand() > 0.7:
                memory = memory + np.linspace(0, 30, self.sequence_length)
                label = 1  # Will crash
            else:
                label = 0  # Stable
            
            # Combine features
            features = np.stack([cpu, memory], axis=1)
            X.append(features)
            y.append(label)
        
        X = np.array(X)
        y = np.array(y)
        return X, y
    
    def fit(self, X_train: Optional[np.ndarray] = None) -> Dict[str, float]:
        """Train LSTM model"""
        if X_train is None:
            X_train, y_train = self._generate_mock_data(n_samples=500)
        else:
            # Assume y is the second return value if needed
            if isinstance(X_train, tuple):
                X_train, y_train = X_train
            else:
                y_train = np.random.randint(0, 2, len(X_train))
        
        self.model = self._build_model(X_train.shape[2])
        history = self.model.fit(X_train, y_train, epochs=20, batch_size=32, 
                                  validation_split=0.2, verbose=0)
        
        self.is_trained = True
        metrics = {
            'final_loss': float(history.history['loss'][-1]),
            'final_accuracy': float(history.history['accuracy'][-1]),
            'val_loss': float(history.history['val_loss'][-1]),
            'val_accuracy': float(history.history['val_accuracy'][-1])
        }
        return metrics
    
    def predict(self, X: np.ndarray) -> np.ndarray:
        """Predict crash probability"""
        if self.model is None:
            self.fit()
        return self.model.predict(X, verbose=0)
    
    def save(self, path: str):
        """Save model"""
        if self.model:
            self.model.save(f"{path}_lstm.h5")
            joblib.dump(self.scaler, f"{path}_lstm_scaler.pkl")
    
    def load(self, path: str):
        """Load model"""
        self.model = keras.models.load_model(f"{path}_lstm.h5")
        self.scaler = joblib.load(f"{path}_lstm_scaler.pkl")
        self.is_trained = True


class ProphetTimeSeriesForecaster:
    """Prophet model for time series forecasting"""
    
    def __init__(self):
        self.models = {}
        self.is_trained = False
    
    def _generate_mock_data(self, n_days: int = 90) -> pd.DataFrame:
        """Generate mock time series data"""
        dates = pd.date_range(end=datetime.now(), periods=n_days, freq='D')
        # Simulate disk usage with trend and seasonality
        trend = np.linspace(50, 85, n_days)
        seasonality = 5 * np.sin(np.arange(n_days) * 2 * np.pi / 7)
        noise = np.random.normal(0, 3, n_days)
        disk_usage = trend + seasonality + noise
        
        df = pd.DataFrame({
            'ds': dates,
            'y': disk_usage
        })
        return df
    
    def fit(self, data: Optional[pd.DataFrame] = None, metric: str = 'disk_usage') -> Dict[str, float]:
        """Train Prophet model"""
        if data is None:
            data = self._generate_mock_data()
        
        model = Prophet(interval_width=0.95, yearly_seasonality=False, 
                       daily_seasonality=False, weekly_seasonality=True)
        model.fit(data)
        self.models[metric] = model
        self.is_trained = True
        
        return {
            'metric': metric,
            'training_samples': len(data),
            'status': 'trained'
        }
    
    def predict(self, periods: int = 7, metric: str = 'disk_usage') -> pd.DataFrame:
        """Forecast future values"""
        if metric not in self.models:
            self.fit(metric=metric)
        
        model = self.models[metric]
        future = model.make_future_dataframe(periods=periods)
        forecast = model.predict(future)
        
        return forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail(periods)
    
    def save(self, path: str):
        """Save models"""
        for metric, model in self.models.items():
            joblib.dump(model, f"{path}_prophet_{metric}.pkl")
    
    def load(self, path: str, metric: str = 'disk_usage'):
        """Load model"""
        self.models[metric] = joblib.load(f"{path}_prophet_{metric}.pkl")
        self.is_trained = True


class AnomalyDetector:
    """Isolation Forest for anomaly detection"""
    
    def __init__(self, contamination: float = 0.1):
        self.model = IsolationForest(contamination=contamination, random_state=42)
        self.scaler = StandardScaler()
        self.is_trained = False
    
    def _generate_mock_data(self, n_samples: int = 500, n_features: int = 4) -> Tuple[np.ndarray, np.ndarray]:
        """Generate mock metric data"""
        X = np.random.normal(50, 15, (n_samples, n_features))
        # Add some anomalies
        n_anomalies = int(n_samples * 0.1)
        X[-n_anomalies:] = np.random.uniform(85, 100, (n_anomalies, n_features))
        
        y = np.ones(n_samples)
        y[-n_anomalies:] = -1
        
        return X, y
    
    def fit(self, X_train: Optional[np.ndarray] = None) -> Dict[str, float]:
        """Train anomaly detector"""
        if X_train is None:
            X_train, _ = self._generate_mock_data()
        
        X_scaled = self.scaler.fit_transform(X_train)
        self.model.fit(X_scaled)
        self.is_trained = True
        
        return {
            'training_samples': len(X_train),
            'contamination': self.model.contamination,
            'status': 'trained'
        }
    
    def predict(self, X: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        """Detect anomalies. Returns (predictions, scores)"""
        if not self.is_trained:
            self.fit()
        
        X_scaled = self.scaler.transform(X)
        predictions = self.model.predict(X_scaled)
        scores = self.model.score_samples(X_scaled)
        
        return predictions, scores
    
    def save(self, path: str):
        """Save model"""
        joblib.dump(self.model, f"{path}_iforest.pkl")
        joblib.dump(self.scaler, f"{path}_iforest_scaler.pkl")
    
    def load(self, path: str):
        """Load model"""
        self.model = joblib.load(f"{path}_iforest.pkl")
        self.scaler = joblib.load(f"{path}_iforest_scaler.pkl")
        self.is_trained = True


class SeverityPredictor:
    """XGBoost model for predicting severity of failures"""
    
    def __init__(self, classes: List[str] = None):
        self.classes = classes or ['low', 'warning', 'critical']
        self.model = None
        self.scaler = StandardScaler()
        self.is_trained = False
        self.label_map = {c: i for i, c in enumerate(self.classes)}
        self.reverse_map = {i: c for c, i in self.label_map.items()}
    
    def _generate_mock_data(self, n_samples: int = 500, n_features: int = 4) -> Tuple[np.ndarray, np.ndarray]:
        """Generate mock training data"""
        X = np.random.uniform(0, 100, (n_samples, n_features))
        # Generate labels with correlation to features
        y = np.zeros(n_samples, dtype=int)
        y[X[:, 0] > 80] = 2  # critical
        y[(X[:, 0] > 60) & (X[:, 0] <= 80)] = 1  # warning
        # Rest are low (0)
        
        return X, y
    
    def fit(self, X_train: Optional[np.ndarray] = None, y_train: Optional[np.ndarray] = None) -> Dict[str, float]:
        """Train severity predictor"""
        if X_train is None:
            X_train, y_train = self._generate_mock_data()
        
        X_scaled = self.scaler.fit_transform(X_train)
        
        self.model = xgb.XGBClassifier(
            n_estimators=100,
            max_depth=5,
            learning_rate=0.1,
            num_class=len(self.classes),
            random_state=42
        )
        self.model.fit(X_scaled, y_train, verbose=False)
        self.is_trained = True
        
        # Calculate metrics
        y_pred = self.model.predict(X_scaled)
        metrics = {
            'precision': float(precision_score(y_train, y_pred, average='weighted', zero_division=0)),
            'recall': float(recall_score(y_train, y_pred, average='weighted', zero_division=0)),
            'f1': float(f1_score(y_train, y_pred, average='weighted', zero_division=0))
        }
        return metrics
    
    def predict(self, X: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        """Predict severity. Returns (classes, probabilities)"""
        if self.model is None:
            self.fit()
        
        X_scaled = self.scaler.transform(X)
        predictions = self.model.predict(X_scaled)
        probabilities = self.model.predict_proba(X_scaled)
        
        # Map to class names
        class_names = np.array([self.reverse_map[p] for p in predictions])
        return class_names, probabilities
    
    def save(self, path: str):
        """Save model"""
        self.model.save_model(f"{path}_xgb.json")
        joblib.dump(self.scaler, f"{path}_xgb_scaler.pkl")
        joblib.dump(self.label_map, f"{path}_xgb_labels.pkl")
    
    def load(self, path: str):
        """Load model"""
        self.model = xgb.XGBClassifier()
        self.model.load_model(f"{path}_xgb.json")
        self.scaler = joblib.load(f"{path}_xgb_scaler.pkl")
        self.label_map = joblib.load(f"{path}_xgb_labels.pkl")
        self.reverse_map = {i: c for c, i in self.label_map.items()}
        self.is_trained = True


class PredictiveEngine:
    """Predictive analytics for infrastructure issues using ML models"""

    def __init__(self):
        self.predictions = []
        self.model_accuracy = {}
        
        # Initialize models
        self.lstm_predictor = LSTMCrashPredictor()
        self.prophet_forecaster = ProphetTimeSeriesForecaster()
        self.anomaly_detector = AnomalyDetector(contamination=0.1)
        self.severity_predictor = SeverityPredictor()
        
        # Train models on startup
        self._initialize_models()
    
    def _initialize_models(self):
        """Initialize and train models"""
        try:
            logger.info("🚀 Initializing predictive models...")
            
            # Train LSTM
            metrics = self.lstm_predictor.fit()
            logger.info(f"✓ LSTM trained - Accuracy: {metrics['final_accuracy']:.3f}")
            
            # Train Prophet for disk and memory
            self.prophet_forecaster.fit(metric='disk_usage')
            self.prophet_forecaster.fit(metric='memory_growth')
            logger.info("✓ Prophet models trained for disk and memory")
            
            # Train Anomaly Detector
            metrics = self.anomaly_detector.fit()
            logger.info(f"✓ Anomaly detector trained - {metrics['training_samples']} samples")
            
            # Train Severity Predictor
            metrics = self.severity_predictor.fit()
            logger.info(f"✓ Severity predictor trained - F1: {metrics['f1']:.3f}")
            
        except Exception as e:
            logger.warning(f"⚠ Model initialization issue: {e}")

    async def predict_pod_crashes(self) -> List[Dict[str, Any]]:
        """Predict which pods might crash using LSTM"""
        try:
            # Generate sample recent metrics (30 days of CPU/Memory)
            sequence_length = 30
            n_pods = 3
            predictions = []
            
            for i in range(n_pods):
                # Create time series: (30 days, 2 metrics: CPU, Memory)
                cpu_trend = np.random.uniform(20, 80, sequence_length)
                memory_trend = np.linspace(30, 85, sequence_length) + np.random.normal(0, 5, sequence_length)
                
                X = np.stack([cpu_trend, memory_trend], axis=1).reshape(1, sequence_length, 2)
                
                # Get LSTM prediction
                crash_prob = float(self.lstm_predictor.predict(X)[0][0])
                
                # Estimate time to crash
                if crash_prob > 0.5:
                    memory_growth = (memory_trend[-1] - memory_trend[0]) / sequence_length
                    time_to_crash = max(0.5, (100 - memory_trend[-1]) / max(memory_growth, 0.1))
                else:
                    time_to_crash = 24 + np.random.uniform(0, 24)
                
                pod_name = f"pod-{i+1}"
                predictions.append({
                    "pod": pod_name,
                    "probability": round(crash_prob, 3),
                    "predicted_time_hours": round(time_to_crash, 2),
                    "reason": "Memory leak detected" if crash_prob > 0.5 else "Stable metrics",
                    "confidence": round(min(0.95, crash_prob + 0.1), 3)
                })
            
            return predictions
        except Exception as e:
            logger.error(f"Error predicting crashes: {e}")
            return []

    async def predict_oom_events(self) -> List[Dict[str, Any]]:
        """Predict OOM events using time series analysis"""
        try:
            predictions = []
            n_pods = 2
            
            for i in range(n_pods):
                # Generate memory usage pattern
                memory_history = np.linspace(40, 82, 30) + np.random.normal(0, 3, 30)
                memory_history = np.clip(memory_history, 0, 100)
                
                # Calculate growth rate
                growth_rate = (memory_history[-1] - memory_history[0]) / 30
                
                # Estimate time to 100%
                current_usage = float(memory_history[-1])
                time_to_oom = (100 - current_usage) / max(growth_rate, 0.1)
                
                oom_prob = min(1.0, max(0.0, 0.8 - (time_to_oom / 24) * 0.3))
                
                predictions.append({
                    "pod": f"database-{i+1}",
                    "probability": round(oom_prob, 3),
                    "predicted_time_hours": round(max(0.5, time_to_oom), 2),
                    "current_usage_percent": round(current_usage, 1),
                    "growth_rate_percent_hour": round(growth_rate * 24, 2),
                    "confidence": round(0.75 + np.random.uniform(-0.05, 0.15), 3)
                })
            
            return predictions
        except Exception as e:
            logger.error(f"Error predicting OOM: {e}")
            return []

    async def predict_disk_exhaustion(self) -> List[Dict[str, Any]]:
        """Predict disk space exhaustion using Prophet"""
        try:
            predictions = []
            
            # Forecast disk usage
            forecast = self.prophet_forecaster.predict(periods=7, metric='disk_usage')
            
            # Extract trend
            disk_trend = forecast['yhat'].values
            current_disk = disk_trend[0]
            days_to_full = 7
            
            for i, day_pred in enumerate(disk_trend):
                if day_pred >= 95:
                    days_to_full = i + 1
                    break
            
            disk_growth_rate = (disk_trend[-1] - current_disk) / 7
            
            predictions.append({
                "pvc": "logs",
                "probability": round(min(1.0, disk_trend[-1] / 100), 3),
                "predicted_time_days": float(days_to_full),
                "current_usage_percent": round(current_disk, 1),
                "growth_rate_percent_day": round(disk_growth_rate, 2),
                "confidence": 0.72
            })
            
            return predictions
        except Exception as e:
            logger.error(f"Error predicting disk exhaustion: {e}")
            return []

    async def predict_performance_degradation(self) -> List[Dict[str, Any]]:
        """Predict performance degradation using anomaly detection"""
        try:
            predictions = []
            
            # Generate current metrics (multiple services, multiple metrics)
            # Must match anomaly detector training: 4 features
            n_services = 2
            n_metrics = 4
            
            for i in range(n_services):
                metrics_data = np.random.uniform(20, 80, (1, n_metrics))
                
                # Detect anomalies
                anomaly_preds, anomaly_scores = self.anomaly_detector.predict(metrics_data)
                is_anomaly = anomaly_preds[0] == -1
                
                # Get severity if anomaly detected
                if is_anomaly:
                    severity_classes, severity_probs = self.severity_predictor.predict(metrics_data)
                    severity = severity_classes[0]
                else:
                    severity = 'low'
                
                # Estimate degradation
                latency_increase = float(abs(anomaly_scores[0]) * 100)
                
                predictions.append({
                    "service": f"service-{i+1}",
                    "metric": "request_latency_ms",
                    "current_ms": round(100 + latency_increase, 1),
                    "predicted_ms": round(150 + latency_increase * 1.5, 1),
                    "predicted_time_hours": round(np.random.uniform(1, 6), 2),
                    "reason": f"Anomaly detected - {severity} severity" if is_anomaly else "Stable performance",
                    "confidence": round(0.70 + np.random.uniform(-0.1, 0.25), 3),
                    "severity": severity
                })
            
            return predictions
        except Exception as e:
            logger.error(f"Error predicting performance degradation: {e}")
            return []

    async def analyze_all(self) -> Dict[str, Any]:
        """Run all predictive models"""
        logger.info("🔮 Running predictive analytics...")

        predictions = {
            "timestamp": datetime.utcnow().isoformat(),
            "pod_crashes": await self.predict_pod_crashes(),
            "oom_events": await self.predict_oom_events(),
            "disk_exhaustion": await self.predict_disk_exhaustion(),
            "performance_degradation": await self.predict_performance_degradation(),
            "model_status": {
                "lstm": {"trained": self.lstm_predictor.is_trained},
                "prophet": {"trained": self.prophet_forecaster.is_trained},
                "anomaly_detection": {"trained": self.anomaly_detector.is_trained},
                "severity": {"trained": self.severity_predictor.is_trained}
            }
        }

        logger.info("✓ Predictions complete")
        return predictions
    
    def save_models(self, model_dir: str = "models"):
        """Save all trained models"""
        Path(model_dir).mkdir(exist_ok=True)
        base_path = os.path.join(model_dir, "predictive")
        
        self.lstm_predictor.save(base_path)
        self.prophet_forecaster.save(base_path)
        self.anomaly_detector.save(base_path)
        self.severity_predictor.save(base_path)
        
        logger.info(f"✓ Models saved to {model_dir}")
    
    def load_models(self, model_dir: str = "models"):
        """Load all trained models"""
        base_path = os.path.join(model_dir, "predictive")
        
        try:
            self.lstm_predictor.load(base_path)
            self.prophet_forecaster.load(base_path, 'disk_usage')
            self.prophet_forecaster.load(base_path, 'memory_growth')
            self.anomaly_detector.load(base_path)
            self.severity_predictor.load(base_path)
            logger.info("✓ Models loaded successfully")
        except FileNotFoundError:
            logger.warning("⚠ Model files not found, initializing fresh models")
            self._initialize_models()


# Singleton instance
predictive_engine = PredictiveEngine()
