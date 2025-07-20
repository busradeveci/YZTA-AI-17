# 🫀 SYSTEMATIC CARDIOVASCULAR DISEASE DATA PREPROCESSING
# 🔬 PACE Methodology Implementation for Medical Diagnosis
# 📊 Binary Classification: CAD Risk vs No Risk

import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, LabelEncoder, OrdinalEncoder
import pickle
import os
from typing import Dict, List, Any, Tuple

class CardiovascularSystematicPreprocessor:
    """
    🫀 Systematic Cardiovascular Disease Data Preprocessor
    
    Based on PACE methodology:
    - Plan: Cardiovascular risk factor preprocessing framework
    - Analyze: Cardiac parameter quality assessment
    - Construct: Binary CAD risk preprocessing pipeline  
    - Execute: Production-ready cardiovascular data transformation
    """
    
    def __init__(self):
        """Initialize Cardiovascular Preprocessor with PACE methodology."""
        self.scaler = StandardScaler()
        self.encoders = {}
        self.feature_names = None
        self.is_fitted = False
        
        # Cardiovascular risk factor groups
        self.demographic_features = [
            'age', 'gender', 'height', 'weight', 'BMI'
        ]
        
        self.clinical_features = [
            'ap_hi', 'ap_lo', 'cholesterol', 'gluc', 'smoke', 
            'alco', 'active', 'cardio'
        ]
        
        self.derived_features = [
            'pulse_pressure', 'mean_arterial_pressure', 'cardiovascular_risk_score',
            'metabolic_syndrome_score', 'lifestyle_risk_score', 'age_risk_category'
        ]
        
        # Risk category mappings
        self.cholesterol_mapping = {1: 'normal', 2: 'above_normal', 3: 'well_above_normal'}
        self.glucose_mapping = {1: 'normal', 2: 'above_normal', 3: 'well_above_normal'}
    
    def plan_preprocessing(self, data: pd.DataFrame) -> Dict[str, Any]:
        """
        🔬 PACE: Plan - Systematic cardiovascular preprocessing planning.
        
        Analyzes cardiovascular data structure and plans preprocessing strategy.
        
        Args:
            data (pd.DataFrame): Raw cardiovascular risk data
            
        Returns:
            dict: Preprocessing plan and cardiac quality report
        """
        plan = {
            'data_shape': data.shape,
            'missing_values': data.isnull().sum().to_dict(),
            'feature_groups': {
                'demographic_features': self.demographic_features,
                'clinical_features': self.clinical_features,
                'derived_features': self.derived_features
            },
            'feature_ranges': {},
            'outliers': {},
            'preprocessing_steps': []
        }
        
        # Cardiovascular feature analysis
        all_features = self.demographic_features + self.clinical_features
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
            "1. Validate cardiovascular parameter ranges",
            "2. Handle missing values with medical defaults",
            "3. Remove physiological outliers",
            "4. Create derived cardiovascular risk features",
            "5. Encode categorical variables",
            "6. Scale cardiovascular parameters",
            "7. Feature selection and CAD risk assessment"
        ]
        
        return plan
    
    def analyze_cardiac_quality(self, data: pd.DataFrame) -> Dict[str, Any]:
        """
        🔍 PACE: Analyze - Comprehensive cardiovascular quality assessment.
        
        Clinical cardiovascular quality analysis for CAD risk assessment.
        
        Args:
            data (pd.DataFrame): Cardiovascular dataset
            
        Returns:
            dict: Cardiovascular quality analysis results
        """
        quality_report = {
            'cardiovascular_quality': {},
            'clinical_validity': {},
            'risk_distribution': {},
            'parameter_correlations': {}
        }
        
        # Cardiovascular quality metrics
        total_records = len(data)
        
        # Data completeness by feature group
        for group_name, features in [
            ('demographic', self.demographic_features),
            ('clinical', self.clinical_features)
        ]:
            group_completeness = []
            for feature in features:
                if feature in data.columns:
                    missing_count = data[feature].isnull().sum()
                    completeness = ((total_records - missing_count) / total_records) * 100
                    group_completeness.append(completeness)
            
            if group_completeness:
                quality_report['cardiovascular_quality'][f'{group_name}_completeness'] = {
                    'average_completeness': float(np.mean(group_completeness)),
                    'min_completeness': float(np.min(group_completeness)),
                    'features_count': len([f for f in features if f in data.columns])
                }
        
        # Clinical validity checks
        if 'ap_hi' in data.columns and 'ap_lo' in data.columns:
            # Blood pressure validity
            valid_bp = data[(data['ap_hi'] >= 70) & (data['ap_hi'] <= 250) & 
                           (data['ap_lo'] >= 40) & (data['ap_lo'] <= 150) &
                           (data['ap_hi'] > data['ap_lo'])]
            quality_report['clinical_validity']['blood_pressure_validity'] = {
                'valid_bp_count': len(valid_bp),
                'valid_bp_percentage': float((len(valid_bp) / total_records) * 100)
            }
        
        if 'age' in data.columns:
            # Age validity (realistic age range)
            valid_age = data[(data['age'] >= 18) & (data['age'] <= 100)]
            quality_report['clinical_validity']['age_validity'] = {
                'valid_age_count': len(valid_age),
                'valid_age_percentage': float((len(valid_age) / total_records) * 100)
            }
        
        # Risk distribution analysis
        if 'cardio' in data.columns:
            cardio_cases = data[data['cardio'] == 1]
            quality_report['risk_distribution'] = {
                'cardio_positive_count': len(cardio_cases),
                'cardio_positive_percentage': float((len(cardio_cases) / total_records) * 100),
                'cardio_negative_count': total_records - len(cardio_cases)
            }
        
        # Parameter correlations (numeric features only)
        numeric_features = [f for f in ['age', 'ap_hi', 'ap_lo', 'height', 'weight'] if f in data.columns]
        if len(numeric_features) > 1:
            corr_matrix = data[numeric_features].corr()
            high_corr_pairs = []
            for i in range(len(corr_matrix.columns)):
                for j in range(i+1, len(corr_matrix.columns)):
                    corr_value = corr_matrix.iloc[i, j]
                    if not pd.isna(corr_value):
                        corr_float = float(corr_value) if isinstance(corr_value, (int, float, np.number)) else 0.0
                        if abs(corr_float) > 0.7:
                            high_corr_pairs.append((
                                corr_matrix.columns[i], 
                                corr_matrix.columns[j], 
                                corr_float
                            ))
            
            quality_report['parameter_correlations']['high_correlation_pairs'] = high_corr_pairs
        
        return quality_report
    
    def construct_cardiovascular_features(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        📊 PACE: Construct - Systematic cardiovascular feature engineering.
        
        Creates cardiovascular-specific derived features for CAD risk assessment.
        
        Args:
            data (pd.DataFrame): Preprocessed cardiovascular data
            
        Returns:
            pd.DataFrame: Data with engineered cardiovascular features
        """
        data_with_features = data.copy()
        
        # BMI calculation if not present
        if 'BMI' not in data.columns and 'height' in data.columns and 'weight' in data.columns:
            # Convert height from cm to m for BMI calculation
            height_m = data['height'] / 100
            data_with_features['BMI'] = data['weight'] / (height_m ** 2)
        
        # Pulse pressure (systolic - diastolic)
        if 'ap_hi' in data.columns and 'ap_lo' in data.columns:
            data_with_features['pulse_pressure'] = data['ap_hi'] - data['ap_lo']
        
        # Mean arterial pressure
        if 'ap_hi' in data.columns and 'ap_lo' in data.columns:
            data_with_features['mean_arterial_pressure'] = (
                data['ap_lo'] + (data['ap_hi'] - data['ap_lo']) / 3
            )
        
        # Age risk categories
        if 'age' in data.columns:
            # Convert days to years if needed
            age_years = data['age'] if data['age'].max() <= 120 else data['age'] / 365.25
            
            conditions = [
                (age_years < 35),
                (age_years >= 35) & (age_years < 50),
                (age_years >= 50) & (age_years < 65),
                (age_years >= 65)
            ]
            choices = [0, 1, 2, 3]  # Low, Medium, High, Very High risk
            data_with_features['age_risk_category'] = np.select(conditions, choices, default=1)
        
        # Metabolic syndrome score
        metabolic_components = []
        
        # BMI component (obesity indicator)
        if 'BMI' in data_with_features.columns:
            obesity_score = (data_with_features['BMI'] >= 30).astype(int)
            metabolic_components.append(obesity_score)
        
        # Blood pressure component (hypertension indicator)
        if 'ap_hi' in data.columns and 'ap_lo' in data.columns:
            hypertension_score = ((data['ap_hi'] >= 140) | (data['ap_lo'] >= 90)).astype(int)
            metabolic_components.append(hypertension_score)
        
        # Glucose component
        if 'gluc' in data.columns:
            glucose_score = (data['gluc'] >= 2).astype(int)  # Above normal glucose
            metabolic_components.append(glucose_score)
        
        # Cholesterol component
        if 'cholesterol' in data.columns:
            cholesterol_score = (data['cholesterol'] >= 2).astype(int)  # Above normal cholesterol
            metabolic_components.append(cholesterol_score)
        
        if metabolic_components:
            data_with_features['metabolic_syndrome_score'] = np.sum(metabolic_components, axis=0)
        
        # Lifestyle risk score
        lifestyle_components = []
        
        if 'smoke' in data.columns:
            lifestyle_components.append(data['smoke'])
        
        if 'alco' in data.columns:
            lifestyle_components.append(data['alco'])
        
        if 'active' in data.columns:
            # Inverse of activity (sedentary = risk)
            lifestyle_components.append(1 - data['active'])
        
        if lifestyle_components:
            data_with_features['lifestyle_risk_score'] = np.sum(lifestyle_components, axis=0)
        
        # Comprehensive cardiovascular risk score
        risk_components = []
        
        # Age component (normalized)
        if 'age' in data.columns:
            age_years = data['age'] if data['age'].max() <= 120 else data['age'] / 365.25
            age_min, age_max = age_years.min(), age_years.max()
            if age_max > age_min:
                age_normalized = (age_years - age_min) / (age_max - age_min)
                risk_components.append(age_normalized)
        
        # Blood pressure component
        if 'ap_hi' in data.columns:
            bp_min, bp_max = data['ap_hi'].min(), data['ap_hi'].max()
            if bp_max > bp_min:
                bp_normalized = (data['ap_hi'] - bp_min) / (bp_max - bp_min)
                risk_components.append(bp_normalized)
        
        # BMI component
        if 'BMI' in data_with_features.columns:
            bmi_min, bmi_max = data_with_features['BMI'].min(), data_with_features['BMI'].max()
            if bmi_max > bmi_min:
                bmi_normalized = (data_with_features['BMI'] - bmi_min) / (bmi_max - bmi_min)
                risk_components.append(bmi_normalized)
        
        # Cholesterol and glucose components
        for feature in ['cholesterol', 'gluc']:
            if feature in data.columns:
                # Convert categorical to risk score (1=low, 2=medium, 3=high risk)
                feature_normalized = (data[feature] - 1) / 2  # Normalize to 0-1
                risk_components.append(feature_normalized)
        
        # Lifestyle components
        for feature in ['smoke', 'alco']:
            if feature in data.columns:
                risk_components.append(data[feature])
        
        # Physical activity (inverse - sedentary = risk)
        if 'active' in data.columns:
            risk_components.append(1 - data['active'])
        
        if risk_components:
            data_with_features['cardiovascular_risk_score'] = np.mean(risk_components, axis=0)
        
        # Blood pressure categories
        if 'ap_hi' in data.columns and 'ap_lo' in data.columns:
            # WHO blood pressure categories
            conditions = [
                (data['ap_hi'] < 120) & (data['ap_lo'] < 80),  # Normal
                (data['ap_hi'] < 130) & (data['ap_lo'] < 85),  # High normal
                (data['ap_hi'] < 140) & (data['ap_lo'] < 90),  # Grade 1 hypertension
                (data['ap_hi'] < 160) & (data['ap_lo'] < 100), # Grade 2 hypertension
                (data['ap_hi'] >= 160) | (data['ap_lo'] >= 100) # Grade 3 hypertension
            ]
            choices = [0, 1, 2, 3, 4]
            data_with_features['bp_category'] = np.select(conditions, choices, default=2)
        
        return data_with_features
    
    def execute_preprocessing(self, data: pd.DataFrame, fit_transform: bool = True) -> pd.DataFrame:
        """
        🎯 PACE: Execute - Complete cardiovascular preprocessing pipeline execution.
        
        Executes systematic cardiovascular data preprocessing.
        
        Args:
            data (pd.DataFrame): Raw cardiovascular data
            fit_transform (bool): Whether to fit transformers (True for training, False for prediction)
            
        Returns:
            pd.DataFrame: Fully preprocessed cardiovascular data ready for modeling
        """
        processed_data = data.copy()
        
        # Step 1: Handle missing values
        processed_data = self._handle_missing_values(processed_data)
        
        # Step 2: Remove outliers (only during training)
        if fit_transform:
            processed_data = self._remove_outliers(processed_data)
        
        # Step 3: Construct cardiovascular features
        processed_data = self.construct_cardiovascular_features(processed_data)
        
        # Step 4: Encode categorical variables
        processed_data = self._encode_categorical_features(processed_data, fit_transform)
        
        # Step 5: Scale cardiovascular features
        processed_data = self._scale_cardiovascular_features(processed_data, fit_transform)
        
        if fit_transform:
            self.is_fitted = True
            self.feature_names = processed_data.columns.tolist()
        
        return processed_data
    
    def _handle_missing_values(self, data: pd.DataFrame) -> pd.DataFrame:
        """Handle missing values with cardiovascular domain knowledge."""
        data_filled = data.copy()
        
        # Demographic features - use appropriate defaults
        if 'age' in data_filled.columns:
            median_age = data_filled['age'].median()
            data_filled['age'].fillna(median_age, inplace=True)
        
        if 'height' in data_filled.columns:
            median_height = data_filled['height'].median()
            data_filled['height'].fillna(median_height, inplace=True)
        
        if 'weight' in data_filled.columns:
            median_weight = data_filled['weight'].median()
            data_filled['weight'].fillna(median_weight, inplace=True)
        
        # Blood pressure - use median (more robust for medical data)
        for feature in ['ap_hi', 'ap_lo']:
            if feature in data_filled.columns:
                median_value = data_filled[feature].median()
                data_filled[feature].fillna(median_value, inplace=True)
        
        # Categorical features - use mode (most frequent)
        for feature in ['cholesterol', 'gluc', 'smoke', 'alco', 'active', 'gender']:
            if feature in data_filled.columns:
                mode_value = data_filled[feature].mode()[0] if not data_filled[feature].mode().empty else 1
                data_filled[feature].fillna(mode_value, inplace=True)
        
        return data_filled
    
    def _remove_outliers(self, data: pd.DataFrame) -> pd.DataFrame:
        """Remove outliers using cardiovascular medical thresholds."""
        cleaned_data = data.copy()
        
        # Cardiovascular outlier thresholds based on medical literature
        cardiovascular_ranges = {
            'age': (18, 100),  # realistic age range
            'ap_hi': (70, 250),  # systolic blood pressure range
            'ap_lo': (40, 150),  # diastolic blood pressure range
            'height': (120, 220),  # height in cm
            'weight': (30, 200),   # weight in kg
        }
        
        for feature, (min_val, max_val) in cardiovascular_ranges.items():
            if feature in cleaned_data.columns:
                # Use medical thresholds combined with IQR
                Q1 = cleaned_data[feature].quantile(0.25)
                Q3 = cleaned_data[feature].quantile(0.75)
                IQR = Q3 - Q1
                lower_bound = max(min_val, Q1 - 1.5 * IQR)
                upper_bound = min(max_val, Q3 + 1.5 * IQR)
                
                cleaned_data = cleaned_data[
                    (cleaned_data[feature] >= lower_bound) & 
                    (cleaned_data[feature] <= upper_bound)
                ]
        
        # Additional cardiovascular-specific outlier removal
        if 'ap_hi' in cleaned_data.columns and 'ap_lo' in cleaned_data.columns:
            # Remove cases where systolic <= diastolic (physiologically impossible)
            cleaned_data = cleaned_data[cleaned_data['ap_hi'] > cleaned_data['ap_lo']]
        
        return cleaned_data
    
    def _encode_categorical_features(self, data: pd.DataFrame, fit_transform: bool) -> pd.DataFrame:
        """Encode categorical features."""
        encoded_data = data.copy()
        
        # Binary categorical features
        binary_features = ['gender', 'smoke', 'alco', 'active']
        for feature in binary_features:
            if feature in encoded_data.columns:
                if fit_transform:
                    encoder = LabelEncoder()
                    encoded_data[feature] = encoder.fit_transform(encoded_data[feature])
                    self.encoders[feature] = encoder
                else:
                    if feature in self.encoders:
                        # Handle unseen categories
                        unique_values = encoded_data[feature].unique()
                        known_values = self.encoders[feature].classes_
                        
                        for val in unique_values:
                            if val not in known_values:
                                # Replace with most frequent class
                                encoded_data[feature] = encoded_data[feature].replace(val, known_values[0])
                        
                        encoded_data[feature] = self.encoders[feature].transform(encoded_data[feature])
        
        # Ordinal categorical features (cholesterol, glucose - have natural order)
        ordinal_features = ['cholesterol', 'gluc']
        for feature in ordinal_features:
            if feature in encoded_data.columns:
                if fit_transform:
                    # These are already ordinal encoded (1, 2, 3) so just ensure they're numeric
                    encoded_data[feature] = encoded_data[feature].astype(int)
                else:
                    encoded_data[feature] = encoded_data[feature].astype(int)
        
        # Target variable
        if 'cardio' in encoded_data.columns:
            encoded_data['cardio'] = encoded_data['cardio'].astype(int)
        
        return encoded_data
    
    def _scale_cardiovascular_features(self, data: pd.DataFrame, fit_transform: bool) -> pd.DataFrame:
        """Scale cardiovascular features."""
        scaled_data = data.copy()
        
        # Features to scale (exclude categorical and target)
        scale_features = ['age', 'height', 'weight', 'ap_hi', 'ap_lo']
        scale_features += [f for f in self.derived_features if f in scaled_data.columns]
        
        # Add BMI if present
        if 'BMI' in scaled_data.columns:
            scale_features.append('BMI')
        
        # Add blood pressure category if present
        if 'bp_category' in scaled_data.columns:
            scale_features.append('bp_category')
        
        # Remove features that shouldn't be scaled
        exclude_features = ['gender', 'smoke', 'alco', 'active', 'cholesterol', 'gluc', 'cardio']
        scale_features = [f for f in scale_features if f in scaled_data.columns and f not in exclude_features]
        
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
        
        print(f"✅ Cardiovascular preprocessor saved to {save_dir}")
    
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
            print(f"✅ Cardiovascular preprocessor loaded from {save_dir}")
            
        except Exception as e:
            print(f"❌ Error loading preprocessor: {e}")

# Convenience function for quick preprocessing
def preprocess_cardiovascular_data(data, save_dir=None, fit_transform=True):
    """
    Quick cardiovascular data preprocessing function.
    
    Args:
        data (pd.DataFrame): Raw cardiovascular data
        save_dir (str, optional): Directory to save preprocessor
        fit_transform (bool): Whether to fit or just transform
        
    Returns:
        pd.DataFrame: Preprocessed cardiovascular data
    """
    preprocessor = CardiovascularSystematicPreprocessor()
    
    if not fit_transform and save_dir:
        preprocessor.load_preprocessor(save_dir)
    
    processed_data = preprocessor.execute_preprocessing(data, fit_transform)
    
    if fit_transform and save_dir:
        preprocessor.save_preprocessor(save_dir)
    
    return processed_data

if __name__ == "__main__":
    # Test preprocessing with sample cardiovascular data
    sample_data = pd.DataFrame({
        'age': [22550, 18250, 27375, 19710, 24820],  # Age in days
        'gender': [2, 1, 1, 2, 1],  # 1=female, 2=male
        'height': [168, 156, 165, 169, 184],  # Height in cm
        'weight': [62, 85, 64, 82, 80],  # Weight in kg
        'ap_hi': [110, 140, 130, 150, 120],  # Systolic BP
        'ap_lo': [80, 90, 70, 100, 80],  # Diastolic BP
        'cholesterol': [1, 3, 1, 2, 1],  # 1=normal, 2=above, 3=well above
        'gluc': [1, 1, 1, 2, 1],  # 1=normal, 2=above, 3=well above
        'smoke': [0, 1, 0, 1, 0],  # 0=no, 1=yes
        'alco': [0, 0, 0, 1, 0],  # 0=no, 1=yes
        'active': [1, 1, 0, 0, 1],  # 0=no, 1=yes
        'cardio': [0, 1, 0, 1, 0]  # 0=no CVD, 1=CVD
    })
    
    print("🫀 Cardiovascular Preprocessing Test:")
    print("Sample cardiovascular data shape:", sample_data.shape)
    
    preprocessor = CardiovascularSystematicPreprocessor()
    
    # Plan preprocessing
    plan = preprocessor.plan_preprocessing(sample_data)
    print(f"Cardiovascular preprocessing plan: {len(plan['preprocessing_steps'])} steps")
    
    # Analyze cardiac quality
    quality = preprocessor.analyze_cardiac_quality(sample_data)
    print(f"Cardiac quality analysis completed")
    
    # Execute preprocessing
    processed_data = preprocessor.execute_preprocessing(sample_data)
    print(f"Processed cardiovascular data shape: {processed_data.shape}")
    print(f"New cardiovascular features: {[col for col in processed_data.columns if col not in sample_data.columns]}")
