"""
Breast Cancer Prediction Module
==============================

This module provides breast cancer prediction functionality using trained ML models.
"""

import joblib
import pandas as pd
import numpy as np
from pathlib import Path
from typing import Dict, Any, Optional, List

class BreastCancerPredictor:
    """Breast Cancer prediction class using trained ML models."""
    
    def __init__(self, model_path: Optional[str] = None):
        """Initialize the predictor with a trained model."""
        if model_path is None:
            model_path = Path(__file__).parent / 'breast_cancer_model.pkl'
        
        try:
            self.model_data = joblib.load(model_path)
            self.model = self.model_data['model']
            self.scaler = self.model_data['scaler']
            self.feature_names = self.model_data['feature_names']
            self.target_names = self.model_data['target_names']
            self.model_type = self.model_data.get('model_type', 'binary_classification')
        except Exception as e:
            raise ValueError(f"Failed to load breast cancer model: {e}")
    
    def predict(self, patient_data):
        """
        Predict breast cancer diagnosis for a patient.
        
        Args:
            patient_data (dict): Dictionary containing patient features
            
        Returns:
            dict: Prediction results with diagnosis and probabilities
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
            
            return {
                'success': True,
                'prediction': int(prediction),
                'diagnosis': self.target_names[prediction],
                'probability_malignant': float(probabilities[0]),
                'probability_benign': float(probabilities[1]),
                'confidence': float(max(probabilities)),
                'risk_level': 'High' if prediction == 0 else 'Low'
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
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
