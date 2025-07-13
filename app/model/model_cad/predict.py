"""
Cardiovascular Disease Prediction Module
=======================================

This module provides cardiovascular disease prediction functionality using trained ML models.
Implements comprehensive risk assessment with clinical interpretation and recommendations.
"""

import joblib
import pandas as pd
import numpy as np
from pathlib import Path
from typing import Dict, Any, Optional, List

class CardiovascularPredictor:
    """Cardiovascular Disease prediction class using trained ML models."""
    
    def __init__(self, model_path: Optional[str] = None):
        """Initialize the predictor with a trained model."""
        if model_path is None:
            model_path = Path(__file__).parent / 'cardiovascular_model.pkl'
        
        try:
            self.model_data = joblib.load(model_path)
            self.model = self.model_data['model']
            self.scaler = self.model_data['scaler']
            self.feature_names = self.model_data['feature_names']
            self.target_names = self.model_data.get('target_names', ['Healthy', 'Cardiovascular Disease'])
            self.model_type = self.model_data.get('model_type', 'binary_classification')
        except Exception as e:
            raise ValueError(f"Failed to load cardiovascular model: {e}")
    
    def predict(self, patient_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Predict cardiovascular disease risk for a patient.
        
        Args:
            patient_data (dict): Dictionary containing cardiovascular risk factors
            
        Returns:
            dict: Prediction results with risk assessment and recommendations
        """
        try:
            # Convert to DataFrame
            input_df = pd.DataFrame([patient_data])
            
            # Ensure all features are present
            missing_features = set(self.feature_names) - set(input_df.columns)
            if missing_features:
                raise ValueError(f"Missing features: {missing_features}")
            
            # Ensure correct feature order
            input_df = input_df[self.feature_names]
            
            # Scale features
            input_scaled = self.scaler.transform(input_df)
            
            # Make prediction
            prediction = self.model.predict(input_scaled)[0]
            probabilities = self.model.predict_proba(input_scaled)[0]
            
            # Calculate risk metrics
            healthy_prob = float(probabilities[0])
            disease_prob = float(probabilities[1])
            risk_score = disease_prob * 100
            confidence = float(max(probabilities))
            
            # Determine risk level and category
            risk_level = self._get_risk_level(disease_prob)
            risk_category = self._get_risk_category(patient_data, disease_prob)
            
            return {
                'success': True,
                'prediction': int(prediction),
                'risk_class': self.target_names[prediction],
                'probabilities': {
                    'Healthy': healthy_prob,
                    'Cardiovascular Disease': disease_prob
                },
                'risk_score': risk_score,
                'confidence': confidence,
                'risk_level': risk_level,
                'risk_category': risk_category,
                'interpretation': self._get_interpretation(risk_score, risk_level),
                'risk_factors': self._analyze_risk_factors(patient_data),
                'recommendations': self._get_recommendations(risk_level, patient_data),
                'lifestyle_advice': self._get_lifestyle_advice(patient_data)
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def _get_risk_level(self, disease_probability: float) -> str:
        """Get risk level based on disease probability."""
        if disease_probability < 0.1:
            return 'Very Low'
        elif disease_probability < 0.3:
            return 'Low'
        elif disease_probability < 0.5:
            return 'Moderate'
        elif disease_probability < 0.7:
            return 'High'
        else:
            return 'Very High'
    
    def _get_risk_category(self, patient_data: Dict[str, Any], disease_prob: float) -> str:
        """Determine risk category based on patient profile."""
        age = patient_data.get('age', 0)
        gender = patient_data.get('gender', 0)  # 1 = Male, 0 = Female
        
        if disease_prob > 0.7:
            return 'Immediate Attention Required'
        elif disease_prob > 0.5:
            if age > 65 or gender == 1:
                return 'High Risk - Enhanced Monitoring'
            else:
                return 'Moderate-High Risk'
        elif disease_prob > 0.3:
            return 'Moderate Risk - Prevention Focus'
        else:
            return 'Low Risk - Maintenance'
    
    def _get_interpretation(self, risk_score: float, risk_level: str) -> str:
        """Get clinical interpretation of the prediction."""
        interpretations = {
            'Very Low': f"Very low cardiovascular risk ({risk_score:.1f}%). Excellent cardiovascular health profile.",
            'Low': f"Low cardiovascular risk ({risk_score:.1f}%). Good cardiovascular health with minimal risk factors.",
            'Moderate': f"Moderate cardiovascular risk ({risk_score:.1f}%). Some risk factors present requiring attention.",
            'High': f"High cardiovascular risk ({risk_score:.1f}%). Multiple risk factors present requiring intervention.",
            'Very High': f"Very high cardiovascular risk ({risk_score:.1f}%). Immediate medical evaluation recommended."
        }
        return interpretations.get(risk_level, f"Cardiovascular risk: {risk_score:.1f}%")
    
    def _analyze_risk_factors(self, patient_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze individual risk factors."""
        risk_factors = {
            'major': [],
            'moderate': [],
            'protective': []
        }
        
        age = patient_data.get('age', 0)
        gender = patient_data.get('gender', 0)
        resting_bp = patient_data.get('resting_blood_pressure', 0)
        cholesterol = patient_data.get('serum_cholesterol', 0)
        max_hr = patient_data.get('max_heart_rate', 0)
        chest_pain = patient_data.get('chest_pain_type', 0)
        exercise_angina = patient_data.get('exercise_angina', 0)
        
        # Major risk factors
        if age > 65:
            risk_factors['major'].append('Advanced age (>65 years)')
        if gender == 1 and age > 45:
            risk_factors['major'].append('Male gender with increased age')
        if resting_bp > 140:
            risk_factors['major'].append('Hypertension (BP >140 mmHg)')
        if cholesterol > 240:
            risk_factors['major'].append('High cholesterol (>240 mg/dL)')
        if exercise_angina == 1:
            risk_factors['major'].append('Exercise-induced angina')
        if chest_pain in [1, 2]:
            risk_factors['major'].append('Significant chest pain symptoms')
        
        # Moderate risk factors
        if 130 <= resting_bp <= 140:
            risk_factors['moderate'].append('Borderline hypertension')
        if 200 <= cholesterol <= 240:
            risk_factors['moderate'].append('Borderline high cholesterol')
        if max_hr < 100:
            risk_factors['moderate'].append('Low exercise capacity')
        if 55 <= age <= 65:
            risk_factors['moderate'].append('Intermediate age group')
        
        # Protective factors
        if max_hr > 160:
            risk_factors['protective'].append('Excellent exercise capacity')
        if resting_bp < 120:
            risk_factors['protective'].append('Optimal blood pressure')
        if cholesterol < 180:
            risk_factors['protective'].append('Optimal cholesterol levels')
        if age < 45:
            risk_factors['protective'].append('Young age')
        
        return risk_factors
    
    def _get_recommendations(self, risk_level: str, patient_data: Dict[str, Any]) -> List[str]:
        """Get personalized medical recommendations."""
        recommendations = []
        
        if risk_level in ['Very High', 'High']:
            recommendations.extend([
                "Immediate cardiology consultation recommended",
                "Comprehensive cardiac evaluation (ECG, echocardiogram, stress test)",
                "Consider cardiac catheterization if indicated",
                "Aggressive risk factor modification",
                "Medication review and optimization"
            ])
        elif risk_level == 'Moderate':
            recommendations.extend([
                "Cardiology consultation within 1-3 months",
                "Exercise stress test or cardiac imaging",
                "Lipid panel and diabetes screening",
                "Blood pressure monitoring",
                "Lifestyle modification counseling"
            ])
        else:  # Low or Very Low
            recommendations.extend([
                "Continue routine cardiovascular screening",
                "Annual health maintenance examination",
                "Lifestyle optimization for prevention",
                "Monitor emerging risk factors"
            ])
        
        # Specific recommendations based on risk factors
        resting_bp = patient_data.get('resting_blood_pressure', 0)
        cholesterol = patient_data.get('serum_cholesterol', 0)
        
        if resting_bp > 140:
            recommendations.append("Antihypertensive therapy consideration")
        if cholesterol > 240:
            recommendations.append("Statin therapy evaluation")
        
        return recommendations
    
    def _get_lifestyle_advice(self, patient_data: Dict[str, Any]) -> Dict[str, List[str]]:
        """Get personalized lifestyle recommendations."""
        advice = {
            'diet': [
                "Mediterranean diet with emphasis on fruits, vegetables, whole grains",
                "Limit saturated fat to <7% of total calories",
                "Reduce sodium intake to <2300mg daily",
                "Include omega-3 rich fish 2x weekly"
            ],
            'exercise': [
                "Moderate aerobic exercise 150 minutes/week",
                "Resistance training 2-3 times per week",
                "Daily walking or equivalent activity",
                "Consult physician before starting new exercise program"
            ],
            'lifestyle': [
                "Smoking cessation if applicable",
                "Limit alcohol consumption",
                "Stress management techniques",
                "Adequate sleep (7-9 hours nightly)",
                "Regular blood pressure monitoring"
            ]
        }
        
        # Personalize based on risk factors
        max_hr = patient_data.get('max_heart_rate', 0)
        if max_hr < 120:
            advice['exercise'].insert(0, "Gradual exercise progression under medical supervision")
        
        age = patient_data.get('age', 0)
        if age > 65:
            advice['exercise'].append("Balance and flexibility exercises for fall prevention")
        
        return advice
    
    def get_feature_importance(self) -> Optional[List[tuple]]:
        """Get feature importance if available."""
        if hasattr(self.model, 'feature_importances_'):
            importance_data = list(zip(self.feature_names, self.model.feature_importances_))
            return sorted(importance_data, key=lambda x: x[1], reverse=True)
        return None
    
    def batch_predict(self, patients_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Predict for multiple patients.
        
        Args:
            patients_data (list): List of patient data dictionaries
            
        Returns:
            list: List of prediction results
        """
        results = []
        for i, patient_data in enumerate(patients_data):
            try:
                result = self.predict(patient_data)
                result['patient_index'] = i
                results.append(result)
            except Exception as e:
                results.append({
                    'success': False,
                    'patient_index': i,
                    'error': str(e)
                })
        return results
    
    def calculate_10year_risk(self, patient_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Calculate 10-year cardiovascular risk using Framingham-style assessment.
        
        Args:
            patient_data (dict): Patient data
            
        Returns:
            dict: 10-year risk assessment
        """
        # Simplified 10-year risk calculation
        age = patient_data.get('age', 0)
        gender = patient_data.get('gender', 0)
        resting_bp = patient_data.get('resting_blood_pressure', 0)
        cholesterol = patient_data.get('serum_cholesterol', 0)
        
        # Base risk from current prediction
        current_prediction = self.predict(patient_data)
        base_risk = current_prediction.get('risk_score', 0) / 100
        
        # Age progression factor
        age_factor = 1.0 + (0.02 * min(10, max(0, 70 - age)))  # Risk increases with age
        
        # Risk factor multiplication
        risk_multiplier = 1.0
        if resting_bp > 160:
            risk_multiplier *= 1.5
        if cholesterol > 260:
            risk_multiplier *= 1.3
        if gender == 1:  # Male
            risk_multiplier *= 1.2
        
        ten_year_risk = min(0.95, base_risk * age_factor * risk_multiplier)
        
        return {
            'ten_year_risk_percentage': ten_year_risk * 100,
            'risk_category': self._categorize_10year_risk(ten_year_risk),
            'factors_considered': ['age', 'gender', 'blood_pressure', 'cholesterol', 'current_health_status']
        }
    
    def _categorize_10year_risk(self, risk: float) -> str:
        """Categorize 10-year cardiovascular risk."""
        if risk < 0.075:
            return 'Low (<7.5%)'
        elif risk < 0.20:
            return 'Borderline (7.5-20%)'
        elif risk < 0.40:
            return 'Intermediate (20-40%)'
        else:
            return 'High (>40%)'
