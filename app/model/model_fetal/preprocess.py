"""
Fetal Health Data Preprocessing Module
====================================

This module provides data preprocessing functionality for fetal health prediction.
"""

import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler

class FetalHealthPreprocessor:
    """Data preprocessing class for fetal health dataset."""
    
    def __init__(self):
        """Initialize the preprocessor."""
        self.scaler = StandardScaler()
        self.feature_names = None
        self.is_fitted = False
    
    def fit(self, X, y=None):
        """
        Fit the preprocessor to the training data.
        
        Args:
            X (DataFrame): Feature matrix
            y (Series, optional): Target vector
            
        Returns:
            self: Fitted preprocessor
        """
        self.feature_names = list(X.columns)
        self.scaler.fit(X)
        self.is_fitted = True
        return self
    
    def transform(self, X):
        """
        Transform the input data.
        
        Args:
            X (DataFrame): Feature matrix to transform
            
        Returns:
            numpy.ndarray: Transformed feature matrix
        """
        if not self.is_fitted:
            raise ValueError("Preprocessor must be fitted before transform")
        
        # Ensure all required features are present
        if self.feature_names and set(self.feature_names) != set(X.columns):
            missing = set(self.feature_names) - set(X.columns)
            extra = set(X.columns) - set(self.feature_names)
            if missing:
                raise ValueError(f"Missing features: {missing}")
            if extra:
                X = X[self.feature_names]
        
        return self.scaler.transform(X)
    
    def fit_transform(self, X, y=None):
        """
        Fit the preprocessor and transform the data.
        
        Args:
            X (DataFrame): Feature matrix
            y (Series, optional): Target vector
            
        Returns:
            numpy.ndarray: Transformed feature matrix
        """
        return self.fit(X, y).transform(X)
    
    def get_feature_names(self):
        """Get the feature names."""
        return self.feature_names if self.is_fitted else None
    
    def validate_input(self, data):
        """
        Validate input data for fetal health prediction.
        
        Args:
            data (dict): Input data dictionary
            
        Returns:
            dict: Validation results
        """
        required_features = [
            'baseline_value', 'accelerations', 'fetal_movement',
            'uterine_contractions', 'light_decelerations', 'severe_decelerations',
            'prolongued_decelerations', 'abnormal_short_term_variability',
            'mean_value_of_short_term_variability',
            'percentage_of_time_with_abnormal_long_term_variability',
            'mean_value_of_long_term_variability', 'histogram_width',
            'histogram_min', 'histogram_max', 'histogram_number_of_peaks',
            'histogram_number_of_zeroes', 'histogram_mode', 'histogram_mean',
            'histogram_median', 'histogram_variance', 'histogram_tendency'
        ]
        
        missing_features = [f for f in required_features if f not in data]
        
        if missing_features:
            return {
                'valid': False,
                'missing_features': missing_features,
                'message': f'Missing required features: {", ".join(missing_features)}'
            }
        
        # Validate ranges
        validation_rules = {
            'baseline_value': (50, 200),
            'histogram_min': (0, 200),
            'histogram_max': (0, 250),
            'abnormal_short_term_variability': (0, 100),
            'percentage_of_time_with_abnormal_long_term_variability': (0, 100)
        }
        
        range_errors = []
        for feature, (min_val, max_val) in validation_rules.items():
            if feature in data:
                value = data[feature]
                if not (min_val <= value <= max_val):
                    range_errors.append(f'{feature}: {value} not in range [{min_val}, {max_val}]')
        
        if range_errors:
            return {
                'valid': False,
                'range_errors': range_errors,
                'message': f'Value range errors: {"; ".join(range_errors)}'
            }
        
        return {'valid': True, 'message': 'Input data is valid'}
