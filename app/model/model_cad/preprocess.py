"""
Cardiovascular Disease Data Preprocessing Module
===============================================

This module provides data preprocessing functionality for cardiovascular disease prediction.
"""

import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from typing import Dict, Any, List, Optional, Tuple

class CardiovascularPreprocessor:
    """Data preprocessing class for cardiovascular disease dataset."""
    
    def __init__(self):
        """Initialize the preprocessor."""
        self.scaler = StandardScaler()
        self.feature_names = None
        self.is_fitted = False
        self.feature_mappings = self._get_feature_mappings()
    
    def _get_feature_mappings(self) -> Dict[str, Dict]:
        """Get feature mappings and validation rules."""
        return {
            'age': {'type': 'numeric', 'min': 20, 'max': 100, 'description': 'Age in years'},
            'gender': {'type': 'categorical', 'values': [0, 1], 'description': '0: Female, 1: Male'},
            'chest_pain_type': {
                'type': 'categorical', 
                'values': [0, 1, 2, 3],
                'description': '0: Typical angina, 1: Atypical angina, 2: Non-anginal pain, 3: Asymptomatic'
            },
            'resting_blood_pressure': {
                'type': 'numeric', 
                'min': 80, 
                'max': 200,
                'description': 'Resting blood pressure in mmHg'
            },
            'serum_cholesterol': {
                'type': 'numeric', 
                'min': 100, 
                'max': 500,
                'description': 'Serum cholesterol in mg/dL'
            },
            'fasting_blood_sugar': {
                'type': 'categorical', 
                'values': [0, 1],
                'description': '0: ≤120 mg/dL, 1: >120 mg/dL'
            },
            'resting_ecg': {
                'type': 'categorical', 
                'values': [0, 1, 2],
                'description': '0: Normal, 1: ST-T abnormality, 2: LV hypertrophy'
            },
            'max_heart_rate': {
                'type': 'numeric', 
                'min': 60, 
                'max': 220,
                'description': 'Maximum heart rate achieved'
            },
            'exercise_angina': {
                'type': 'categorical', 
                'values': [0, 1],
                'description': '0: No, 1: Yes'
            },
            'oldpeak': {
                'type': 'numeric', 
                'min': 0, 
                'max': 10,
                'description': 'ST depression induced by exercise'
            },
            'slope': {
                'type': 'categorical', 
                'values': [0, 1, 2],
                'description': '0: Upsloping, 1: Flat, 2: Downsloping'
            },
            'num_major_vessels': {
                'type': 'categorical', 
                'values': [0, 1, 2, 3],
                'description': 'Number of major vessels colored by fluoroscopy'
            }
        }
    
    def fit(self, X: pd.DataFrame, y: Optional[pd.Series] = None):
        """
        Fit the preprocessor to the training data.
        
        Args:
            X (DataFrame): Feature matrix
            y (Series, optional): Target vector
            
        Returns:
            self: Fitted preprocessor
        """
        self.feature_names = list(X.columns)
        
        # Validate feature names
        expected_features = set(self.feature_mappings.keys())
        provided_features = set(self.feature_names)
        
        if expected_features != provided_features:
            missing = expected_features - provided_features
            extra = provided_features - expected_features
            
            warning_msg = []
            if missing:
                warning_msg.append(f"Missing expected features: {missing}")
            if extra:
                warning_msg.append(f"Extra features found: {extra}")
            
            if warning_msg:
                print(f"Warning: {'; '.join(warning_msg)}")
        
        # Fit the scaler only on numerical features
        numerical_features = self._get_numerical_features()
        if numerical_features:
            self.scaler.fit(X[numerical_features])
        
        self.is_fitted = True
        return self
    
    def transform(self, X: pd.DataFrame) -> np.ndarray:
        """
        Transform the input data.
        
        Args:
            X (DataFrame): Feature matrix to transform
            
        Returns:
            numpy.ndarray: Transformed feature matrix
        """
        if not self.is_fitted:
            raise ValueError("Preprocessor must be fitted before transform")
        
        # Create a copy to avoid modifying original data
        X_transformed = X.copy()
        
        # Ensure all required features are present
        if self.feature_names:
            missing_features = set(self.feature_names) - set(X_transformed.columns)
            if missing_features:
                raise ValueError(f"Missing features: {missing_features}")
            
            # Select and order features correctly
            X_transformed = X_transformed[self.feature_names]
        
        # Scale numerical features
        numerical_features = self._get_numerical_features()
        if numerical_features:
            numerical_mask = [col in numerical_features for col in X_transformed.columns]
            X_transformed.loc[:, numerical_features] = self.scaler.transform(X_transformed[numerical_features])
        
        return X_transformed.values
    
    def fit_transform(self, X: pd.DataFrame, y: Optional[pd.Series] = None) -> np.ndarray:
        """
        Fit the preprocessor and transform the data.
        
        Args:
            X (DataFrame): Feature matrix
            y (Series, optional): Target vector
            
        Returns:
            numpy.ndarray: Transformed feature matrix
        """
        return self.fit(X, y).transform(X)
    
    def _get_numerical_features(self) -> List[str]:
        """Get list of numerical features."""
        numerical_features = []
        for feature_name, feature_info in self.feature_mappings.items():
            if feature_info.get('type') == 'numeric' and feature_name in (self.feature_names or []):
                numerical_features.append(feature_name)
        return numerical_features
    
    def validate_input(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Comprehensive validation of input data for cardiovascular prediction.
        
        Args:
            data (dict): Input data dictionary
            
        Returns:
            dict: Validation results with detailed feedback
        """
        validation_result = {
            'valid': True,
            'errors': [],
            'warnings': [],
            'corrections': [],
            'risk_flags': []
        }
        
        # Check for missing features
        missing_features = []
        for feature_name in self.feature_mappings.keys():
            if feature_name not in data:
                missing_features.append(feature_name)
        
        if missing_features:
            validation_result['errors'].append(
                f"Missing required features: {', '.join(missing_features)}"
            )
            validation_result['valid'] = False
        
        # Validate each feature
        for feature_name, value in data.items():
            if feature_name in self.feature_mappings:
                feature_validation = self._validate_single_feature(feature_name, value)
                
                if feature_validation['errors']:
                    validation_result['errors'].extend(feature_validation['errors'])
                    validation_result['valid'] = False
                
                if feature_validation['warnings']:
                    validation_result['warnings'].extend(feature_validation['warnings'])
                
                if feature_validation['risk_flags']:
                    validation_result['risk_flags'].extend(feature_validation['risk_flags'])
        
        # Additional clinical validation
        clinical_validation = self._clinical_validation(data)
        validation_result['warnings'].extend(clinical_validation.get('warnings', []))
        validation_result['risk_flags'].extend(clinical_validation.get('risk_flags', []))
        
        return validation_result
    
    def _validate_single_feature(self, feature_name: str, value: Any) -> Dict[str, List[str]]:
        """Validate a single feature value."""
        result = {'errors': [], 'warnings': [], 'risk_flags': []}
        
        feature_info = self.feature_mappings[feature_name]
        feature_type = feature_info.get('type', 'numeric')
        
        # Type validation
        if feature_type == 'numeric':
            if not isinstance(value, (int, float)):
                result['errors'].append(f"{feature_name} must be numeric")
                return result
            
            # Range validation
            min_val = feature_info.get('min')
            max_val = feature_info.get('max')
            
            if min_val is not None and value < min_val:
                result['errors'].append(f"{feature_name} must be >= {min_val}")
            
            if max_val is not None and value > max_val:
                result['errors'].append(f"{feature_name} must be <= {max_val}")
            
            # Clinical warnings for extreme but valid values
            self._add_clinical_warnings(feature_name, value, result)
        
        elif feature_type == 'categorical':
            valid_values = feature_info.get('values', [])
            if value not in valid_values:
                result['errors'].append(f"{feature_name} must be one of {valid_values}")
        
        return result
    
    def _add_clinical_warnings(self, feature_name: str, value: float, result: Dict[str, List[str]]):
        """Add clinical warnings for extreme but valid values."""
        warnings_map = {
            'age': {
                'ranges': [(80, float('inf'), 'Very advanced age - increased cardiovascular risk')],
            },
            'resting_blood_pressure': {
                'ranges': [
                    (160, float('inf'), 'Severe hypertension - immediate medical attention'),
                    (140, 160, 'Stage 1 hypertension'),
                    (90, 100, 'Hypotension - may indicate cardiac issues')
                ]
            },
            'serum_cholesterol': {
                'ranges': [
                    (300, float('inf'), 'Very high cholesterol - urgent intervention needed'),
                    (240, 300, 'High cholesterol'),
                    (0, 120, 'Unusually low cholesterol - verify measurement')
                ]
            },
            'max_heart_rate': {
                'ranges': [
                    (0, 100, 'Very low maximum heart rate - possible cardiac limitation'),
                    (200, float('inf'), 'Unusually high maximum heart rate')
                ]
            },
            'oldpeak': {
                'ranges': [
                    (4, float('inf'), 'Severe ST depression - high risk indicator')
                ]
            }
        }
        
        if feature_name in warnings_map:
            for min_val, max_val, warning in warnings_map[feature_name]['ranges']:
                if min_val <= value < max_val:
                    result['warnings'].append(f"{feature_name}: {warning}")
                    if 'high risk' in warning.lower() or 'severe' in warning.lower():
                        result['risk_flags'].append(f"High risk: {feature_name} = {value}")
    
    def _clinical_validation(self, data: Dict[str, Any]) -> Dict[str, List[str]]:
        """Perform clinical cross-feature validation."""
        result = {'warnings': [], 'risk_flags': []}
        
        age = data.get('age', 0)
        gender = data.get('gender', 0)
        max_hr = data.get('max_heart_rate', 0)
        resting_bp = data.get('resting_blood_pressure', 0)
        cholesterol = data.get('serum_cholesterol', 0)
        
        # Age-adjusted maximum heart rate check
        if age > 0 and max_hr > 0:
            predicted_max_hr = 220 - age
            if max_hr > predicted_max_hr * 1.1:
                result['warnings'].append(
                    f"Maximum heart rate ({max_hr}) higher than age-predicted ({predicted_max_hr})"
                )
            elif max_hr < predicted_max_hr * 0.7:
                result['warnings'].append(
                    f"Maximum heart rate ({max_hr}) significantly lower than age-predicted ({predicted_max_hr})"
                )
        
        # Multiple risk factor combinations
        risk_factors = 0
        if age > 65:
            risk_factors += 1
        if gender == 1 and age > 45:  # Male over 45
            risk_factors += 1
        if resting_bp > 140:
            risk_factors += 1
        if cholesterol > 240:
            risk_factors += 1
        if data.get('exercise_angina', 0) == 1:
            risk_factors += 1
        
        if risk_factors >= 3:
            result['risk_flags'].append(f"Multiple risk factors present ({risk_factors})")
        
        return result
    
    def get_feature_names(self) -> Optional[List[str]]:
        """Get the feature names."""
        return self.feature_names if self.is_fitted else None
    
    def get_feature_descriptions(self) -> Dict[str, str]:
        """Get descriptions for all features."""
        return {name: info.get('description', 'No description available') 
                for name, info in self.feature_mappings.items()}
    
    def preprocess_for_web_form(self, form_data: Dict[str, str]) -> Dict[str, Any]:
        """
        Preprocess data from web form (string values) to model input format.
        
        Args:
            form_data (dict): Form data with string values
            
        Returns:
            dict: Processed data with correct types
        """
        processed_data = {}
        
        for feature_name, feature_info in self.feature_mappings.items():
            if feature_name in form_data:
                raw_value = form_data[feature_name]
                
                try:
                    if feature_info.get('type') == 'numeric':
                        processed_data[feature_name] = float(raw_value)
                    else:  # categorical
                        processed_data[feature_name] = int(raw_value)
                except (ValueError, TypeError):
                    raise ValueError(f"Invalid value for {feature_name}: {raw_value}")
        
        return processed_data
