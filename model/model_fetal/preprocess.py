# 👶 SYSTEMATIC FETAL HEALTH DATA PREPROCESSING
# 🔬 PACE Methodology Implementation for Medical Diagnosis
# 📊 Multi-class Classification: Normal, Suspect, Pathological

import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, LabelEncoder, RobustScaler
import pickle
import os
from typing import Dict, List, Any, Tuple

class FetalHealthSystematicPreprocessor:
    """
    👶 Systematic Fetal Health Data Preprocessor
    
    Based on PACE methodology:
    - Plan: CTG feature preprocessing framework
    - Analyze: Fetal monitoring quality assessment
    - Construct: Multi-class classification preprocessing pipeline  
    - Execute: Production-ready fetal health data transformation
    """
    
    def __init__(self):
        """Initialize Fetal Health Preprocessor with PACE methodology."""
        self.scaler = RobustScaler()  # More robust to outliers for medical data
        self.encoders = {}
        self.feature_names = None
        self.is_fitted = False
        
        # CTG feature groups
        self.baseline_features = [
            'baseline_value', 'accelerations', 'fetal_movement'
        ]
        
        self.variability_features = [
            'uterine_contractions', 'light_decelerations', 'severe_decelerations',
            'prolongued_decelerations', 'abnormal_short_term_variability',
            'mean_value_of_short_term_variability', 'percentage_of_time_with_abnormal_long_term_variability',
            'mean_value_of_long_term_variability'
        ]
        
        self.morphological_features = [
            'histogram_width', 'histogram_min', 'histogram_max', 'histogram_number_of_peaks',
            'histogram_number_of_zeroes', 'histogram_mode', 'histogram_mean', 'histogram_median',
            'histogram_variance', 'histogram_tendency'
        ]
        
        self.derived_features = [
            'baseline_stability', 'variability_score', 'deceleration_burden',
            'morphological_complexity', 'fetal_distress_score', 'risk_category'
        ]
    
    def plan_preprocessing(self, data: pd.DataFrame) -> Dict[str, Any]:
        """
        🔬 PACE: Plan - Systematic CTG preprocessing planning.
        
        Analyzes fetal health data structure and plans preprocessing strategy.
        
        Args:
            data (pd.DataFrame): Raw fetal health CTG data
            
        Returns:
            dict: Preprocessing plan and CTG quality report
        """
        plan = {
            'data_shape': data.shape,
            'missing_values': data.isnull().sum().to_dict(),
            'feature_groups': {
                'baseline_features': self.baseline_features,
                'variability_features': self.variability_features,
                'morphological_features': self.morphological_features,
                'derived_features': self.derived_features
            },
            'feature_ranges': {},
            'outliers': {},
            'preprocessing_steps': []
        }
        
        # CTG feature analysis
        all_features = self.baseline_features + self.variability_features + self.morphological_features
        for feature in all_features:
            if feature in data.columns and pd.api.types.is_numeric_dtype(data[feature]):
                plan['feature_ranges'][feature] = {
                    'min': float(data[feature].min()),
                    'max': float(data[feature].max()),
                    'mean': float(data[feature].mean()),
                    'std': float(data[feature].std()),
                    'median': float(data[feature].median())
                }
                
                # Outlier detection using IQR
                Q1 = data[feature].quantile(0.25)
                Q3 = data[feature].quantile(0.75)
                IQR = Q3 - Q1
                outliers = data[(data[feature] < Q1 - 1.5*IQR) | (data[feature] > Q3 + 1.5*IQR)]
                plan['outliers'][feature] = len(outliers)
        
        # Preprocessing steps
        plan['preprocessing_steps'] = [
            "1. Validate CTG parameter ranges",
            "2. Handle missing values with clinical defaults",
            "3. Remove physiological outliers",
            "4. Create derived fetal monitoring features",
            "5. Encode categorical variables",
            "6. Scale CTG parameters (robust scaling)",
            "7. Feature selection and fetal health assessment"
        ]
        
        return plan
    
    def analyze_ctg_quality(self, data: pd.DataFrame) -> Dict[str, Any]:
        """
        🔍 PACE: Analyze - Comprehensive CTG quality assessment.
        
        Clinical CTG quality analysis for fetal health monitoring.
        
        Args:
            data (pd.DataFrame): Fetal health CTG dataset
            
        Returns:
            dict: CTG quality analysis results
        """
        quality_report = {
            'ctg_quality': {},
            'clinical_validity': {},
            'fetal_health_distribution': {},
            'parameter_correlations': {}
        }
        
        # CTG quality metrics
        total_records = len(data)
        
        # Data completeness by feature group
        for group_name, features in [
            ('baseline', self.baseline_features),
            ('variability', self.variability_features),
            ('morphological', self.morphological_features)
        ]:
            group_completeness = []
            for feature in features:
                if feature in data.columns:
                    missing_count = data[feature].isnull().sum()
                    completeness = ((total_records - missing_count) / total_records) * 100
                    group_completeness.append(completeness)
            
            if group_completeness:
                quality_report['ctg_quality'][f'{group_name}_completeness'] = {
                    'average_completeness': float(np.mean(group_completeness)),
                    'min_completeness': float(np.min(group_completeness)),
                    'features_count': len([f for f in features if f in data.columns])
                }
        
        # Clinical validity checks
        if 'baseline_value' in data.columns:
            # Normal fetal heart rate baseline (110-160 bpm)
            normal_baseline = data[(data['baseline_value'] >= 110) & (data['baseline_value'] <= 160)]
            quality_report['clinical_validity']['baseline_validity'] = {
                'normal_baseline_count': len(normal_baseline),
                'normal_baseline_percentage': float((len(normal_baseline) / total_records) * 100)
            }
        
        if 'accelerations' in data.columns:
            # Accelerations should be positive or zero
            valid_accelerations = data[data['accelerations'] >= 0]
            quality_report['clinical_validity']['acceleration_validity'] = {
                'valid_acceleration_count': len(valid_accelerations),
                'valid_acceleration_percentage': float((len(valid_accelerations) / total_records) * 100)
            }
        
        # Fetal health distribution analysis
        if 'fetal_health' in data.columns:
            health_distribution = data['fetal_health'].value_counts().to_dict()
            total = sum(health_distribution.values())
            quality_report['fetal_health_distribution'] = {
                'class_counts': health_distribution,
                'class_percentages': {k: float((v/total)*100) for k, v in health_distribution.items()}
            }
        
        # Parameter correlations (key CTG features)
        key_features = ['baseline_value', 'accelerations', 'uterine_contractions', 'light_decelerations']
        numeric_features = [f for f in key_features if f in data.columns and pd.api.types.is_numeric_dtype(data[f])]
        
        if len(numeric_features) > 1:
            corr_matrix = data[numeric_features].corr()
            high_corr_pairs = []
            for i in range(len(corr_matrix.columns)):
                for j in range(i+1, len(corr_matrix.columns)):
                    corr_value = corr_matrix.iloc[i, j]
                    if not pd.isna(corr_value):
                        corr_float = float(corr_value) if isinstance(corr_value, (int, float, np.number)) else 0.0
                        if abs(corr_float) > 0.6:
                            high_corr_pairs.append((
                                corr_matrix.columns[i], 
                                corr_matrix.columns[j], 
                                corr_float
                            ))
            
            quality_report['parameter_correlations']['high_correlation_pairs'] = high_corr_pairs
        
        return quality_report
    
    def construct_fetal_features(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        📊 PACE: Construct - Systematic fetal health feature engineering.
        
        Creates fetal health-specific derived features for CTG analysis.
        
        Args:
            data (pd.DataFrame): Preprocessed CTG data
            
        Returns:
            pd.DataFrame: Data with engineered fetal health features
        """
        data_with_features = data.copy()
        
        # Baseline stability score
        if 'baseline_value' in data.columns:
            # Categorize baseline as: bradycardia (<110), normal (110-160), tachycardia (>160)
            conditions = [
                (data['baseline_value'] < 110),  # Bradycardia
                (data['baseline_value'] >= 110) & (data['baseline_value'] <= 160),  # Normal
                (data['baseline_value'] > 160)  # Tachycardia
            ]
            choices = [2, 0, 1]  # 0=normal, 1=mild concern, 2=concern
            data_with_features['baseline_stability'] = np.select(conditions, choices, default=0)
        
        # Variability score (combines different variability measures)
        variability_components = []
        
        if 'abnormal_short_term_variability' in data.columns:
            variability_components.append(data['abnormal_short_term_variability'])
        
        if 'percentage_of_time_with_abnormal_long_term_variability' in data.columns:
            # Normalize percentage to 0-1 scale
            ltv_normalized = data['percentage_of_time_with_abnormal_long_term_variability'] / 100
            variability_components.append(ltv_normalized)
        
        if variability_components:
            data_with_features['variability_score'] = np.mean(variability_components, axis=0)
        
        # Deceleration burden (combines different types of decelerations)
        deceleration_components = []
        
        deceleration_features = ['light_decelerations', 'severe_decelerations', 'prolongued_decelerations']
        for feature in deceleration_features:
            if feature in data.columns:
                deceleration_components.append(data[feature])
        
        if deceleration_components:
            data_with_features['deceleration_burden'] = np.sum(deceleration_components, axis=0)
        
        # Morphological complexity (histogram-based features)
        morphological_components = []
        
        # Histogram width and variance indicate complexity
        if 'histogram_width' in data.columns:
            width_min, width_max = data['histogram_width'].min(), data['histogram_width'].max()
            if width_max > width_min:
                width_normalized = (data['histogram_width'] - width_min) / (width_max - width_min)
                morphological_components.append(width_normalized)
        
        if 'histogram_variance' in data.columns:
            var_min, var_max = data['histogram_variance'].min(), data['histogram_variance'].max()
            if var_max > var_min:
                var_normalized = (data['histogram_variance'] - var_min) / (var_max - var_min)
                morphological_components.append(var_normalized)
        
        if 'histogram_number_of_peaks' in data.columns:
            peaks_min, peaks_max = data['histogram_number_of_peaks'].min(), data['histogram_number_of_peaks'].max()
            if peaks_max > peaks_min:
                peaks_normalized = (data['histogram_number_of_peaks'] - peaks_min) / (peaks_max - peaks_min)
                morphological_components.append(peaks_normalized)
        
        if morphological_components:
            data_with_features['morphological_complexity'] = np.mean(morphological_components, axis=0)
        
        # Comprehensive fetal distress score
        distress_components = []
        
        # Baseline component (deviation from normal)
        if 'baseline_value' in data.columns:
            # Distance from normal range (110-160)
            baseline_distress = np.where(
                data['baseline_value'] < 110, 
                (110 - data['baseline_value']) / 110,  # Bradycardia severity
                np.where(
                    data['baseline_value'] > 160,
                    (data['baseline_value'] - 160) / 160,  # Tachycardia severity
                    0  # Normal range
                )
            )
            distress_components.append(baseline_distress)
        
        # Acceleration deficit (lack of accelerations is concerning)
        if 'accelerations' in data.columns:
            # Normal should have some accelerations, lack of them is concerning
            acceleration_deficit = np.where(
                data['accelerations'] == 0, 
                1.0,  # No accelerations = high concern
                1.0 / (data['accelerations'] + 1)  # Fewer accelerations = more concern
            )
            distress_components.append(acceleration_deficit)
        
        # Deceleration severity
        if 'deceleration_burden' in data_with_features.columns:
            decel_min = data_with_features['deceleration_burden'].min()
            decel_max = data_with_features['deceleration_burden'].max()
            if decel_max > decel_min:
                decel_normalized = (data_with_features['deceleration_burden'] - decel_min) / (decel_max - decel_min)
                distress_components.append(decel_normalized)
        
        # Variability abnormality
        if 'variability_score' in data_with_features.columns:
            distress_components.append(data_with_features['variability_score'])
        
        if distress_components:
            data_with_features['fetal_distress_score'] = np.mean(distress_components, axis=0)
        
        # Risk category based on distress score
        if 'fetal_distress_score' in data_with_features.columns:
            # Categorize into risk levels
            conditions = [
                (data_with_features['fetal_distress_score'] <= 0.3),  # Low risk
                (data_with_features['fetal_distress_score'] <= 0.6),  # Medium risk
                (data_with_features['fetal_distress_score'] > 0.6)    # High risk
            ]
            choices = [0, 1, 2]
            data_with_features['risk_category'] = np.select(conditions, choices, default=1)
        
        # Acceleration to deceleration ratio
        if 'accelerations' in data.columns and 'deceleration_burden' in data_with_features.columns:
            data_with_features['accel_decel_ratio'] = (
                data['accelerations'] / (data_with_features['deceleration_burden'] + 1e-8)
            )
        
        # Histogram pattern indicators
        if 'histogram_mode' in data.columns and 'histogram_mean' in data.columns:
            # Mode-mean difference indicates skewness
            data_with_features['histogram_skewness'] = abs(data['histogram_mode'] - data['histogram_mean'])
        
        # Uterine activity score
        if 'uterine_contractions' in data.columns:
            # Categorize uterine contraction levels
            uc_conditions = [
                (data['uterine_contractions'] <= 0.002),  # Low activity
                (data['uterine_contractions'] <= 0.005),  # Normal activity
                (data['uterine_contractions'] > 0.005)    # High activity
            ]
            uc_choices = [0, 1, 2]
            data_with_features['uterine_activity_level'] = np.select(uc_conditions, uc_choices, default=1)
        
        return data_with_features
    
    def execute_preprocessing(self, data: pd.DataFrame, fit_transform: bool = True) -> pd.DataFrame:
        """
        🎯 PACE: Execute - Complete CTG preprocessing pipeline execution.
        
        Executes systematic fetal health data preprocessing.
        
        Args:
            data (pd.DataFrame): Raw CTG data
            fit_transform (bool): Whether to fit transformers (True for training, False for prediction)
            
        Returns:
            pd.DataFrame: Fully preprocessed CTG data ready for modeling
        """
        processed_data = data.copy()
        
        # Step 1: Handle missing values
        processed_data = self._handle_missing_values(processed_data)
        
        # Step 2: Remove outliers (only during training)
        if fit_transform:
            processed_data = self._remove_outliers(processed_data)
        
        # Step 3: Construct fetal health features
        processed_data = self.construct_fetal_features(processed_data)
        
        # Step 4: Encode categorical variables
        processed_data = self._encode_categorical_features(processed_data, fit_transform)
        
        # Step 5: Scale CTG features
        processed_data = self._scale_ctg_features(processed_data, fit_transform)
        
        if fit_transform:
            self.is_fitted = True
            self.feature_names = processed_data.columns.tolist()
        
        return processed_data
    
    def _handle_missing_values(self, data: pd.DataFrame) -> pd.DataFrame:
        """Handle missing values with CTG domain knowledge."""
        data_filled = data.copy()
        
        # CTG features - use median (more robust for medical data)
        all_features = self.baseline_features + self.variability_features + self.morphological_features
        for feature in all_features:
            if feature in data_filled.columns:
                median_value = data_filled[feature].median()
                data_filled[feature].fillna(median_value, inplace=True)
        
        # Target variable - use mode if missing
        if 'fetal_health' in data_filled.columns:
            mode_value = data_filled['fetal_health'].mode()[0] if not data_filled['fetal_health'].mode().empty else 1
            data_filled['fetal_health'].fillna(mode_value, inplace=True)
        
        return data_filled
    
    def _remove_outliers(self, data: pd.DataFrame) -> pd.DataFrame:
        """Remove outliers using CTG medical thresholds."""
        cleaned_data = data.copy()
        
        # CTG outlier thresholds based on medical literature
        ctg_ranges = {
            'baseline_value': (50, 200),  # Fetal heart rate baseline (bpm)
            'accelerations': (0, 0.1),    # Accelerations per second
            'uterine_contractions': (0, 0.02),  # Uterine contractions per second
            'histogram_width': (0, 300),  # Histogram width
            'histogram_min': (0, 200),    # Histogram minimum
            'histogram_max': (0, 200),    # Histogram maximum
        }
        
        for feature, (min_val, max_val) in ctg_ranges.items():
            if feature in cleaned_data.columns:
                # Use medical thresholds combined with IQR
                Q1 = cleaned_data[feature].quantile(0.25)
                Q3 = cleaned_data[feature].quantile(0.75)
                IQR = Q3 - Q1
                lower_bound = max(min_val, Q1 - 2.0 * IQR)  # Use 2.0 instead of 1.5 for medical data
                upper_bound = min(max_val, Q3 + 2.0 * IQR)
                
                cleaned_data = cleaned_data[
                    (cleaned_data[feature] >= lower_bound) & 
                    (cleaned_data[feature] <= upper_bound)
                ]
        
        return cleaned_data
    
    def _encode_categorical_features(self, data: pd.DataFrame, fit_transform: bool) -> pd.DataFrame:
        """Encode categorical features."""
        encoded_data = data.copy()
        
        # Target variable encoding
        if 'fetal_health' in encoded_data.columns:
            if fit_transform:
                # Ensure it's properly encoded (1, 2, 3) -> (0, 1, 2)
                encoder = LabelEncoder()
                encoded_data['fetal_health'] = encoder.fit_transform(encoded_data['fetal_health'])
                self.encoders['fetal_health'] = encoder
            else:
                if 'fetal_health' in self.encoders:
                    # Handle unseen categories
                    unique_values = encoded_data['fetal_health'].unique()
                    known_values = self.encoders['fetal_health'].classes_
                    
                    for val in unique_values:
                        if val not in known_values:
                            # Replace with most frequent class (normal = 1)
                            encoded_data['fetal_health'] = encoded_data['fetal_health'].replace(val, known_values[0])
                    
                    encoded_data['fetal_health'] = self.encoders['fetal_health'].transform(encoded_data['fetal_health'])
        
        # Derived categorical features
        categorical_features = ['baseline_stability', 'risk_category', 'uterine_activity_level']
        for feature in categorical_features:
            if feature in encoded_data.columns:
                encoded_data[feature] = encoded_data[feature].astype(int)
        
        return encoded_data
    
    def _scale_ctg_features(self, data: pd.DataFrame, fit_transform: bool) -> pd.DataFrame:
        """Scale CTG features using robust scaling."""
        scaled_data = data.copy()
        
        # Features to scale (exclude categorical and target)
        all_features = self.baseline_features + self.variability_features + self.morphological_features
        scale_features = [f for f in all_features if f in scaled_data.columns]
        
        # Add derived numeric features
        derived_numeric = [f for f in self.derived_features if f in scaled_data.columns 
                          and f not in ['baseline_stability', 'risk_category', 'uterine_activity_level']]
        scale_features += derived_numeric
        
        # Add additional engineered features
        additional_features = ['accel_decel_ratio', 'histogram_skewness']
        scale_features += [f for f in additional_features if f in scaled_data.columns]
        
        # Remove target and categorical features
        exclude_features = ['fetal_health', 'baseline_stability', 'risk_category', 'uterine_activity_level']
        scale_features = [f for f in scale_features if f not in exclude_features]
        
        if scale_features:
            if fit_transform:
                scaled_data[scale_features] = self.scaler.fit_transform(scaled_data[scale_features])
            else:
                scaled_data[scale_features] = self.scaler.transform(scaled_data[scale_features])
        
        return scaled_data
    
    def save_preprocessor(self, save_dir: str):
        """Save preprocessing components."""
        os.makedirs(save_dir, exist_ok=True)
        
        # Save scaler
        with open(os.path.join(save_dir, 'scaler.pkl'), 'wb') as f:
            pickle.dump(self.scaler, f)
        
        # Save encoders
        with open(os.path.join(save_dir, 'encoders.pkl'), 'wb') as f:
            pickle.dump(self.encoders, f)
        
        # Save feature names
        with open(os.path.join(save_dir, 'feature_names.pkl'), 'wb') as f:
            pickle.dump(self.feature_names, f)
        
        print(f"✅ Fetal health preprocessor saved to {save_dir}")
    
    def load_preprocessor(self, save_dir: str):
        """Load preprocessing components."""
        try:
            # Load scaler
            with open(os.path.join(save_dir, 'scaler.pkl'), 'rb') as f:
                self.scaler = pickle.load(f)
            
            # Load encoders
            with open(os.path.join(save_dir, 'encoders.pkl'), 'rb') as f:
                self.encoders = pickle.load(f)
            
            # Load feature names
            with open(os.path.join(save_dir, 'feature_names.pkl'), 'rb') as f:
                self.feature_names = pickle.load(f)
            
            self.is_fitted = True
            print(f"✅ Fetal health preprocessor loaded from {save_dir}")
            
        except Exception as e:
            print(f"❌ Error loading preprocessor: {e}")

# Convenience function for quick preprocessing
def preprocess_fetal_health_data(data, save_dir=None, fit_transform=True):
    """
    Quick fetal health data preprocessing function.
    
    Args:
        data (pd.DataFrame): Raw CTG data
        save_dir (str, optional): Directory to save preprocessor
        fit_transform (bool): Whether to fit or just transform
        
    Returns:
        pd.DataFrame: Preprocessed CTG data
    """
    preprocessor = FetalHealthSystematicPreprocessor()
    
    if not fit_transform and save_dir:
        preprocessor.load_preprocessor(save_dir)
    
    processed_data = preprocessor.execute_preprocessing(data, fit_transform)
    
    if fit_transform and save_dir:
        preprocessor.save_preprocessor(save_dir)
    
    return processed_data

if __name__ == "__main__":
    # Test preprocessing with sample CTG data
    sample_data = pd.DataFrame({
        'baseline_value': [120, 140, 110, 160, 135],
        'accelerations': [0.000, 0.006, 0.001, 0.002, 0.000],
        'fetal_movement': [0.0, 0.0, 0.0, 0.0, 0.0],
        'uterine_contractions': [0.000, 0.005, 0.003, 0.001, 0.007],
        'light_decelerations': [0.000, 0.000, 0.000, 0.001, 0.002],
        'severe_decelerations': [0.0, 0.0, 0.0, 0.0, 0.0],
        'prolongued_decelerations': [0.0, 0.0, 0.0, 0.0, 0.0],
        'abnormal_short_term_variability': [73, 17, 16, 21, 28],
        'mean_value_of_short_term_variability': [0.5, 2.1, 2.4, 2.4, 3.4],
        'percentage_of_time_with_abnormal_long_term_variability': [43, 0, 0, 0, 2],
        'mean_value_of_long_term_variability': [2.4, 10.4, 13.4, 13.4, 6.8],
        'histogram_width': [64, 130, 142, 117, 198],
        'histogram_min': [62, 68, 68, 53, 53],
        'histogram_max': [126, 198, 210, 170, 251],
        'histogram_number_of_peaks': [2, 6, 4, 11, 3],
        'histogram_number_of_zeroes': [0, 1, 0, 0, 0],
        'histogram_mode': [120, 141, 109, 144, 187],
        'histogram_mean': [137, 136, 127, 121, 148],
        'histogram_median': [121, 140, 108, 123, 148],
        'histogram_variance': [73, 12, 13, 57, 25],
        'histogram_tendency': [1, 0, 1, -1, 0],
        'fetal_health': [2, 1, 1, 1, 3]  # 1=Normal, 2=Suspect, 3=Pathological
    })
    
    print("👶 Fetal Health Preprocessing Test:")
    print("Sample CTG data shape:", sample_data.shape)
    
    preprocessor = FetalHealthSystematicPreprocessor()
    
    # Plan preprocessing
    plan = preprocessor.plan_preprocessing(sample_data)
    print(f"CTG preprocessing plan: {len(plan['preprocessing_steps'])} steps")
    
    # Analyze CTG quality
    quality = preprocessor.analyze_ctg_quality(sample_data)
    print(f"CTG quality analysis completed")
    
    # Execute preprocessing
    processed_data = preprocessor.execute_preprocessing(sample_data)
    print(f"Processed CTG data shape: {processed_data.shape}")
    print(f"New fetal health features: {[col for col in processed_data.columns if col not in sample_data.columns]}")
