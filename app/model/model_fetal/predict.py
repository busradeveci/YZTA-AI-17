"""
Fetal Health Prediction Module
=============================

This module provides fetal health prediction functionality using trained ML models.
"""

import joblib
import pandas as pd
import numpy as np
from pathlib import Path

class FetalHealthPredictor:
    """Fetal Health prediction class using trained ML models."""
    
    def __init__(self, model_path=None):
        """Initialize the predictor with a trained model."""
        if model_path is None:
            model_path = Path(__file__).parent / 'fetal_health_model.pkl'
        
        self.model_data = joblib.load(model_path)
        self.model = self.model_data['model']
        self.scaler = self.model_data['scaler']
        self.feature_names = self.model_data['feature_names']
        self.target_names = self.model_data['target_names']
    
    def predict(self, patient_data):
        """
        Predict fetal health status for a patient.
        
        Args:
            patient_data (dict): Dictionary containing fetal monitoring features
            
        Returns:
            dict: Prediction results with health status and probabilities
        """
        try:
            # Convert to DataFrame
            input_df = pd.DataFrame([patient_data])
            
            # Ensure all features are present
            missing_features = set(self.feature_names) - set(input_df.columns)
            if missing_features:
                raise ValueError(f"Missing features: {missing_features}")
            
            # Scale features
            input_scaled = self.scaler.transform(input_df[self.feature_names])
            
            # Make prediction
            prediction = self.model.predict(input_scaled)[0]
            probabilities = self.model.predict_proba(input_scaled)[0]
            
            # Map prediction to class name (predictions are 1,2,3)
            health_status = self.target_names[prediction - 1]
            
            return {
                'success': True,
                'prediction': int(prediction),
                'health_status': health_status,
                'probabilities': {
                    'Normal': float(probabilities[0]) if len(probabilities) > 0 else 0.0,
                    'Suspect': float(probabilities[1]) if len(probabilities) > 1 else 0.0,
                    'Pathological': float(probabilities[2]) if len(probabilities) > 2 else 0.0
                },
                'confidence': float(max(probabilities)),
                'risk_level': self._get_risk_level(health_status)
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def _get_risk_level(self, health_status):
        """Get risk level based on health status."""
        risk_mapping = {
            'Normal': 'Low',
            'Suspect': 'Medium',
            'Pathological': 'High'
        }
        return risk_mapping.get(health_status, 'Unknown')
    
    def get_feature_importance(self):
        """Get feature importance if available."""
        if hasattr(self.model, 'feature_importances_'):
            importance_data = {
                'features': self.feature_names,
                'importance': self.model.feature_importances_.tolist()
            }
            return sorted(zip(importance_data['features'], importance_data['importance']), 
                         key=lambda x: x[1], reverse=True)
        return None
