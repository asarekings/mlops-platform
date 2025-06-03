#!/usr/bin/env python3
# Advanced Model Monitoring System
# Author: asarekings  
# Date: 2025-06-03 19:12:59 UTC

import json
import time
import threading
from datetime import datetime, timedelta
import numpy as np
from collections import defaultdict
import logging

class ModelMonitor:
    """Advanced monitoring for asarekings MLOps Platform"""
    
    def __init__(self):
        self.prediction_logs = defaultdict(list)
        self.performance_metrics = defaultdict(dict)
        self.drift_alerts = []
        self.setup_logging()
        
    def setup_logging(self):
        """Setup comprehensive logging"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('logs/mlops_platform.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger('MLOps_Monitor')
    
    def log_prediction(self, model_name, input_data, prediction, confidence, response_time):
        """Log every prediction for monitoring"""
        log_entry = {
            'timestamp': datetime.utcnow().isoformat(),
            'model': model_name,
            'input': input_data,
            'prediction': prediction,
            'confidence': confidence,
            'response_time_ms': response_time,
            'user': 'asarekings'
        }
        
        self.prediction_logs[model_name].append(log_entry)
        self.logger.info(f"Prediction logged for {model_name}: {prediction}")
        
        # Keep only last 1000 predictions per model
        if len(self.prediction_logs[model_name]) > 1000:
            self.prediction_logs[model_name] = self.prediction_logs[model_name][-1000:]
    
    def detect_model_drift(self, model_name):
        """Detect potential model drift"""
        if model_name not in self.prediction_logs:
            return {"status": "no_data"}
        
        predictions = self.prediction_logs[model_name]
        if len(predictions) < 100:
            return {"status": "insufficient_data", "count": len(predictions)}
        
        # Analyze recent vs historical predictions
        recent = predictions[-50:]
        historical = predictions[-200:-50] if len(predictions) >= 200 else predictions[:-50]
        
        recent_avg = np.mean([p['confidence'] for p in recent])
        historical_avg = np.mean([p['confidence'] for p in historical])
        
        drift_threshold = 0.1
        drift_detected = abs(recent_avg - historical_avg) > drift_threshold
        
        return {
            "status": "drift_detected" if drift_detected else "stable",
            "recent_confidence": recent_avg,
            "historical_confidence": historical_avg,
            "drift_magnitude": abs(recent_avg - historical_avg),
            "threshold": drift_threshold
        }
    
    def get_model_performance_summary(self, model_name, hours=24):
        """Get performance summary for last N hours"""
        if model_name not in self.prediction_logs:
            return {"error": "No data for model"}
        
        cutoff_time = datetime.utcnow() - timedelta(hours=hours)
        recent_predictions = [
            p for p in self.prediction_logs[model_name]
            if datetime.fromisoformat(p['timestamp'].replace('Z', '+00:00')) > cutoff_time
        ]
        
        if not recent_predictions:
            return {"error": "No recent predictions"}
        
        return {
            "model": model_name,
            "time_period_hours": hours,
            "total_predictions": len(recent_predictions),
            "avg_confidence": np.mean([p['confidence'] for p in recent_predictions]),
            "avg_response_time": np.mean([p['response_time_ms'] for p in recent_predictions]),
            "predictions_per_hour": len(recent_predictions) / hours,
            "author": "asarekings"
        }

# Global monitor instance
model_monitor = ModelMonitor()