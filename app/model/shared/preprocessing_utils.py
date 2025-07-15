"""
Shared Preprocessing Utilities for YZTA-AI-17 Medical Prediction System
======================================================================

This module contains shared preprocessing utilities and functions that can be used
across different medical prediction models.
"""

import pandas as pd
import numpy as np
from typing import Dict, Any, List, Optional, Tuple, Union
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class BasePreprocessor:
    """Base preprocessing class with common functionality."""
    
    def __init__(self):
        """Initialize the base preprocessor."""
        self.is_fitted = False
        self.feature_names = None
        self.preprocessing_steps = []
    
    def log_preprocessing_step(self, step_name: str, description: str):
        """Log a preprocessing step."""
        self.preprocessing_steps.append({
            'step': step_name,
            'description': description,
            'timestamp': datetime.now().isoformat()
        })
        logger.info(f"Preprocessing step: {step_name} - {description}")
    
    def get_preprocessing_history(self) -> List[Dict[str, str]]:
        """Get the history of preprocessing steps."""
        return self.preprocessing_steps.copy()


class DataValidator:
    """Comprehensive data validation utilities for medical data."""
    
    @staticmethod
    def validate_numeric_range(value: Union[int, float], min_val: float, max_val: float, 
                              feature_name: str = "feature") -> Dict[str, Any]:
        """
        Validate that a numeric value is within the specified range.
        
        Args:
            value: The value to validate
            min_val: Minimum allowed value
            max_val: Maximum allowed value
            feature_name: Name of the feature for error messages
            
        Returns:
            dict: Validation result
        """
        result = {'valid': True, 'errors': [], 'warnings': []}
        
        if not isinstance(value, (int, float)):
            result['valid'] = False
            result['errors'].append(f"{feature_name} must be numeric")
            return result
        
        if np.isnan(value) or np.isinf(value):
            result['valid'] = False
            result['errors'].append(f"{feature_name} contains invalid numeric value")
            return result
        
        if value < min_val:
            result['valid'] = False
            result['errors'].append(f"{feature_name} ({value}) below minimum ({min_val})")
        
        if value > max_val:
            result['valid'] = False
            result['errors'].append(f"{feature_name} ({value}) above maximum ({max_val})")
        
        # Add warnings for extreme but valid values
        range_size = max_val - min_val
        if value < min_val + 0.05 * range_size:
            result['warnings'].append(f"{feature_name} is near minimum value")
        elif value > max_val - 0.05 * range_size:
            result['warnings'].append(f"{feature_name} is near maximum value")
        
        return result
    
    @staticmethod
    def validate_categorical(value: Any, valid_values: List[Any], 
                           feature_name: str = "feature") -> Dict[str, Any]:
        """
        Validate that a value is within the allowed categorical values.
        
        Args:
            value: The value to validate
            valid_values: List of valid categorical values
            feature_name: Name of the feature for error messages
            
        Returns:
            dict: Validation result
        """
        result = {'valid': True, 'errors': [], 'warnings': []}
        
        if value not in valid_values:
            result['valid'] = False
            result['errors'].append(
                f"{feature_name} ({value}) not in valid values {valid_values}"
            )
        
        return result
    
    @staticmethod
    def validate_medical_coherence(data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate medical coherence across multiple features.
        
        Args:
            data: Dictionary of feature values
            
        Returns:
            dict: Validation result with coherence checks
        """
        result = {'valid': True, 'errors': [], 'warnings': [], 'flags': []}
        
        # Age-related validations
        age = data.get('age')
        if age is not None:
            # Age vs other parameters coherence
            max_hr = data.get('max_heart_rate')
            if max_hr is not None and age > 0:
                predicted_max_hr = 220 - age
                if abs(max_hr - predicted_max_hr) > 50:
                    result['warnings'].append(
                        f"Maximum heart rate ({max_hr}) deviates significantly from age-predicted ({predicted_max_hr})"
                    )
            
            # Age-specific risk factors
            if age > 80:
                result['flags'].append("Advanced age (>80) - increased medical complexity")
            elif age < 20:
                result['warnings'].append("Very young age - verify data accuracy")
        
        # Blood pressure coherence
        systolic_bp = data.get('resting_blood_pressure') or data.get('systolic_bp')
        if systolic_bp is not None:
            if systolic_bp > 180:
                result['flags'].append("Hypertensive crisis range - immediate attention")
            elif systolic_bp < 90:
                result['flags'].append("Hypotensive - possible shock or cardiac issue")
        
        return result


class FeatureEngineer:
    """Feature engineering utilities for medical data."""
    
    @staticmethod
    def create_age_groups(age: float) -> str:
        """Create age group categories."""
        if age < 30:
            return "young"
        elif age < 50:
            return "middle_aged"
        elif age < 70:
            return "older"
        else:
            return "elderly"
    
    @staticmethod
    def create_bmi_category(weight_kg: float, height_m: float) -> str:
        """Create BMI categories."""
        bmi = weight_kg / (height_m ** 2)
        
        if bmi < 18.5:
            return "underweight"
        elif bmi < 25:
            return "normal"
        elif bmi < 30:
            return "overweight"
        else:
            return "obese"
    
    @staticmethod
    def create_bp_category(systolic: float, diastolic: float = None) -> str:
        """Create blood pressure categories."""
        if systolic < 120:
            return "normal"
        elif systolic < 130:
            return "elevated"
        elif systolic < 140:
            return "stage1_hypertension"
        elif systolic < 180:
            return "stage2_hypertension"
        else:
            return "hypertensive_crisis"
    
    @staticmethod
    def create_risk_interaction_features(data: Dict[str, Any]) -> Dict[str, Any]:
        """Create interaction features for risk assessment."""
        features = {}
        
        age = data.get('age', 0)
        gender = data.get('gender', 0)  # Assuming 1=male, 0=female
        
        # Age-gender interaction
        if age > 0 and gender is not None:
            if gender == 1:  # Male
                features['age_gender_risk'] = age * 1.2 if age > 45 else age
            else:  # Female
                features['age_gender_risk'] = age * 1.2 if age > 55 else age
        
        # Multiple risk factor score
        risk_score = 0
        if age > 65:
            risk_score += 1
        if data.get('resting_blood_pressure', 0) > 140:
            risk_score += 1
        if data.get('serum_cholesterol', 0) > 240:
            risk_score += 1
        if data.get('exercise_angina', 0) == 1:
            risk_score += 1
        
        features['multiple_risk_score'] = risk_score
        
        return features


class DataCleaner:
    """Data cleaning utilities for medical datasets."""
    
    @staticmethod
    def handle_missing_values(df: pd.DataFrame, strategy: str = 'median') -> pd.DataFrame:
        """
        Handle missing values in medical data.
        
        Args:
            df: DataFrame with potential missing values
            strategy: Strategy for imputation ('median', 'mean', 'mode', 'drop')
            
        Returns:
            DataFrame with missing values handled
        """
        df_clean = df.copy()
        
        numeric_columns = df_clean.select_dtypes(include=[np.number]).columns
        categorical_columns = df_clean.select_dtypes(exclude=[np.number]).columns
        
        if strategy == 'median':
            df_clean[numeric_columns] = df_clean[numeric_columns].fillna(
                df_clean[numeric_columns].median()
            )
        elif strategy == 'mean':
            df_clean[numeric_columns] = df_clean[numeric_columns].fillna(
                df_clean[numeric_columns].mean()
            )
        elif strategy == 'mode':
            for col in categorical_columns:
                mode_value = df_clean[col].mode().iloc[0] if not df_clean[col].mode().empty else 'Unknown'
                df_clean[col] = df_clean[col].fillna(mode_value)
        elif strategy == 'drop':
            df_clean = df_clean.dropna()
        
        return df_clean
    
    @staticmethod
    def detect_outliers(series: pd.Series, method: str = 'iqr') -> pd.Series:
        """
        Detect outliers in a pandas Series.
        
        Args:
            series: Data series to check for outliers
            method: Method for outlier detection ('iqr', 'zscore')
            
        Returns:
            Boolean series indicating outliers
        """
        if method == 'iqr':
            Q1 = series.quantile(0.25)
            Q3 = series.quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR
            return (series < lower_bound) | (series > upper_bound)
        
        elif method == 'zscore':
            z_scores = np.abs((series - series.mean()) / series.std())
            return z_scores > 3
        
        return pd.Series([False] * len(series), index=series.index)
    
    @staticmethod
    def cap_outliers(series: pd.Series, lower_percentile: float = 0.01, 
                     upper_percentile: float = 0.99) -> pd.Series:
        """
        Cap outliers at specified percentiles.
        
        Args:
            series: Data series to cap
            lower_percentile: Lower percentile for capping
            upper_percentile: Upper percentile for capping
            
        Returns:
            Series with capped outliers
        """
        lower_bound = series.quantile(lower_percentile)
        upper_bound = series.quantile(upper_percentile)
        
        return series.clip(lower=lower_bound, upper=upper_bound)


class ModelInputFormatter:
    """Utilities for formatting data for model input."""
    
    @staticmethod
    def ensure_feature_order(data: Dict[str, Any], expected_features: List[str]) -> Dict[str, Any]:
        """
        Ensure input data has the correct feature order for model prediction.
        
        Args:
            data: Input data dictionary
            expected_features: List of expected feature names in order
            
        Returns:
            Ordered dictionary with correct feature order
        """
        ordered_data = {}
        
        for feature in expected_features:
            if feature in data:
                ordered_data[feature] = data[feature]
            else:
                raise ValueError(f"Missing required feature: {feature}")
        
        return ordered_data
    
    @staticmethod
    def convert_to_model_format(data: Dict[str, Any], feature_types: Dict[str, str]) -> Dict[str, Any]:
        """
        Convert data types according to model requirements.
        
        Args:
            data: Input data dictionary
            feature_types: Dictionary mapping feature names to expected types
            
        Returns:
            Data with correct types
        """
        converted_data = {}
        
        for feature_name, value in data.items():
            expected_type = feature_types.get(feature_name, 'float')
            
            try:
                if expected_type == 'int':
                    converted_data[feature_name] = int(value)
                elif expected_type == 'float':
                    converted_data[feature_name] = float(value)
                elif expected_type == 'bool':
                    converted_data[feature_name] = bool(value)
                else:
                    converted_data[feature_name] = value
            except (ValueError, TypeError):
                raise ValueError(f"Cannot convert {feature_name} value '{value}' to {expected_type}")
        
        return converted_data


class MedicalDataQuality:
    """Medical data quality assessment utilities."""
    
    @staticmethod
    def assess_data_quality(df: pd.DataFrame) -> Dict[str, Any]:
        """
        Comprehensive data quality assessment for medical datasets.
        
        Args:
            df: DataFrame to assess
            
        Returns:
            Dictionary with quality metrics and recommendations
        """
        quality_report = {
            'total_samples': len(df),
            'total_features': len(df.columns),
            'missing_data': {},
            'duplicates': 0,
            'outliers': {},
            'data_types': {},
            'quality_score': 0,
            'recommendations': []
        }
        
        # Missing data analysis
        missing_counts = df.isnull().sum()
        quality_report['missing_data'] = {
            col: {
                'count': int(missing_counts[col]),
                'percentage': float(missing_counts[col] / len(df) * 100)
            }
            for col in df.columns if missing_counts[col] > 0
        }
        
        # Duplicate analysis
        quality_report['duplicates'] = int(df.duplicated().sum())
        
        # Outlier analysis for numeric columns
        numeric_columns = df.select_dtypes(include=[np.number]).columns
        for col in numeric_columns:
            outliers = DataCleaner.detect_outliers(df[col])
            outlier_count = outliers.sum()
            if outlier_count > 0:
                quality_report['outliers'][col] = {
                    'count': int(outlier_count),
                    'percentage': float(outlier_count / len(df) * 100)
                }
        
        # Data type analysis
        quality_report['data_types'] = {
            col: str(df[col].dtype) for col in df.columns
        }
        
        # Calculate quality score (0-100)
        quality_score = 100
        
        # Deduct for missing data
        missing_penalty = sum(
            info['percentage'] * 0.1 for info in quality_report['missing_data'].values()
        )
        quality_score -= min(missing_penalty, 30)
        
        # Deduct for duplicates
        duplicate_penalty = (quality_report['duplicates'] / len(df)) * 20
        quality_score -= min(duplicate_penalty, 20)
        
        # Deduct for excessive outliers
        outlier_penalty = sum(
            min(info['percentage'] * 0.05, 5) for info in quality_report['outliers'].values()
        )
        quality_score -= outlier_penalty
        
        quality_report['quality_score'] = max(0, quality_score)
        
        # Generate recommendations
        if quality_report['quality_score'] < 70:
            quality_report['recommendations'].append("Data quality requires improvement")
        
        if quality_report['missing_data']:
            quality_report['recommendations'].append("Address missing data through imputation or collection")
        
        if quality_report['duplicates'] > 0:
            quality_report['recommendations'].append("Remove duplicate records")
        
        if quality_report['outliers']:
            quality_report['recommendations'].append("Review and handle outliers appropriately")
        
        return quality_report
    
    @staticmethod
    def generate_data_profile(df: pd.DataFrame) -> Dict[str, Any]:
        """
        Generate a comprehensive data profile for medical datasets.
        
        Args:
            df: DataFrame to profile
            
        Returns:
            Dictionary with detailed data profile
        """
        profile = {
            'basic_info': {
                'samples': len(df),
                'features': len(df.columns),
                'memory_usage_mb': df.memory_usage(deep=True).sum() / 1024**2
            },
            'feature_profiles': {},
            'correlations': {},
            'statistical_summary': df.describe().to_dict()
        }
        
        # Individual feature profiles
        for col in df.columns:
            feature_profile = {
                'dtype': str(df[col].dtype),
                'missing_count': int(df[col].isnull().sum()),
                'unique_count': int(df[col].nunique()),
                'memory_usage': int(df[col].memory_usage(deep=True))
            }
            
            if df[col].dtype in ['int64', 'float64']:
                feature_profile.update({
                    'min': float(df[col].min()),
                    'max': float(df[col].max()),
                    'mean': float(df[col].mean()),
                    'std': float(df[col].std()),
                    'outlier_count': int(DataCleaner.detect_outliers(df[col]).sum())
                })
            
            profile['feature_profiles'][col] = feature_profile
        
        # Correlation analysis for numeric features
        numeric_df = df.select_dtypes(include=[np.number])
        if len(numeric_df.columns) > 1:
            correlation_matrix = numeric_df.corr()
            # Find high correlations (>0.7 or <-0.7)
            high_corr_pairs = []
            for i in range(len(correlation_matrix.columns)):
                for j in range(i+1, len(correlation_matrix.columns)):
                    corr_value = correlation_matrix.iloc[i, j]
                    if abs(corr_value) > 0.7:
                        high_corr_pairs.append({
                            'feature1': correlation_matrix.columns[i],
                            'feature2': correlation_matrix.columns[j],
                            'correlation': float(corr_value)
                        })
            
            profile['correlations'] = {
                'high_correlation_pairs': high_corr_pairs,
                'correlation_matrix': correlation_matrix.to_dict()
            }
        
        return profile


# Utility functions for common preprocessing tasks
def standardize_column_names(df: pd.DataFrame) -> pd.DataFrame:
    """Standardize column names to lowercase with underscores."""
    df_clean = df.copy()
    df_clean.columns = df_clean.columns.str.lower().str.replace(' ', '_').str.replace('-', '_')
    return df_clean

def convert_categorical_to_numeric(df: pd.DataFrame, mapping: Dict[str, Dict[str, int]]) -> pd.DataFrame:
    """Convert categorical variables to numeric using provided mapping."""
    df_converted = df.copy()
    
    for column, value_mapping in mapping.items():
        if column in df_converted.columns:
            df_converted[column] = df_converted[column].map(value_mapping)
    
    return df_converted

def create_medical_risk_score(patient_data: Dict[str, Any], risk_factors: List[str], 
                             weights: Optional[Dict[str, float]] = None) -> float:
    """
    Create a composite medical risk score.
    
    Args:
        patient_data: Patient data dictionary
        risk_factors: List of risk factor feature names
        weights: Optional weights for each risk factor
        
    Returns:
        Composite risk score
    """
    if weights is None:
        weights = {factor: 1.0 for factor in risk_factors}
    
    risk_score = 0.0
    total_weight = 0.0
    
    for factor in risk_factors:
        if factor in patient_data and factor in weights:
            # Normalize the value (assuming 0-1 scale for risk factors)
            normalized_value = min(1.0, max(0.0, float(patient_data[factor])))
            risk_score += normalized_value * weights[factor]
            total_weight += weights[factor]
    
    # Return normalized score (0-1 scale)
    return risk_score / total_weight if total_weight > 0 else 0.0
