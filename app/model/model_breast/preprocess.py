"""
Breast Cancer Data Preprocessing Module
=====================================

This module provides data preprocessing functionality for breast cancer prediction.
"""

import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler

class BreastCancerPreprocessor:
    """Data preprocessing class for breast cancer dataset."""
    
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
        if set(self.feature_names) != set(X.columns):
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
