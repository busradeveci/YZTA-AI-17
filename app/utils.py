"""
YZTA-AI-17 Tıbbi Tahmin Sistemi için Yardımcı Fonksiyonlar
=========================================================

Bu modül model yönetimi, veri doğrulama ve yanıt formatlama için
yardımcı sınıflar ve fonksiyonlar içerir.
"""

import joblib
import pandas as pd
import numpy as np
import json
import logging
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime

from config import MODEL_CONFIGS, FEATURE_SCHEMAS, PERFORMANCE_THRESHOLDS

logger = logging.getLogger(__name__)


class ModelManager:
    """
    ML modellerin yüklenmesi, önbelleğe alınması ve kullanılması için merkezi model yönetim sınıfı.
    """
    
    def __init__(self):
        """Model yöneticisini başlat."""
        self.models = {}
        self.model_metadata = {}
        self._load_all_models()
    
    def _load_all_models(self):
        """Mevcut tüm modelleri ve metadata'larını yükle."""
        for model_name, config in MODEL_CONFIGS.items():
            try:
                self._load_model(model_name, config)
                logger.info(f"{model_name} modeli başarıyla yüklendi")
            except Exception as e:
                logger.error(f"{model_name} modeli yüklenemedi: {e}")
    
    def _load_model(self, model_name: str, config: Dict[str, Any]):
        """Belirli bir modeli ve metadata'sını yükle."""
        model_path = config['model_path']
        
        if not model_path.exists():
            logger.warning(f"Model dosyası bulunamadı: {model_path}")
            return
        
        # Load model data
        model_data = joblib.load(model_path)
        self.models[model_name] = model_data
        
        # Load metadata if available
        metadata_path = model_path.parent / 'model_metadata.json'
        if metadata_path.exists():
            with open(metadata_path, 'r', encoding='utf-8') as f:
                self.model_metadata[model_name] = json.load(f)
        else:
            # Create default metadata
            self.model_metadata[model_name] = {
                'model_name': model_name,
                'model_type': config['model_type'],
                'target_classes': config['target_classes'],
                'loaded_at': datetime.now().isoformat()
            }
    
    def predict(self, model_name: str, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Make a prediction using the specified model.
        
        Args:
            model_name (str): Name of the model to use
            input_data (dict): Input features for prediction
            
        Returns:
            dict: Prediction results
        """
        if model_name not in self.models:
            raise ValueError(f"Model '{model_name}' not available")
        
        model_data = self.models[model_name]
        model = model_data['model']
        scaler = model_data['scaler']
        feature_names = model_data['feature_names']
        
        # Prepare input data
        input_df = pd.DataFrame([input_data])
        
        # Ensure all features are present and in correct order
        missing_features = set(feature_names) - set(input_df.columns)
        if missing_features:
            raise ValueError(f"Missing features: {missing_features}")
        
        # Select and order features
        input_df = input_df[feature_names]
        
        # Scale features
        input_scaled = scaler.transform(input_df)
        
        # Make prediction
        prediction = model.predict(input_scaled)[0]
        probabilities = model.predict_proba(input_scaled)[0]
        
        # Format results based on model type
        if model_name == 'cardiovascular':
            return self._format_cardiovascular_result(prediction, probabilities)
        elif model_name == 'breast_cancer':
            return self._format_breast_cancer_result(prediction, probabilities)
        elif model_name == 'fetal_health':
            return self._format_fetal_health_result(prediction, probabilities)
        else:
            raise ValueError(f"Unknown model type for {model_name}")
    
    def _format_cardiovascular_result(self, prediction: int, probabilities: np.ndarray) -> Dict[str, Any]:
        """Format cardiovascular prediction results."""
        return {
            'success': True,
            'prediction': int(prediction),
            'risk_class': 'Cardiovascular Disease' if prediction == 1 else 'Healthy',
            'probability_healthy': float(probabilities[0]),
            'probability_disease': float(probabilities[1]),
            'risk_score': float(probabilities[1] * 100),
            'confidence': float(max(probabilities)),
            'risk_level': self._get_risk_level(probabilities[1])
        }
    
    def _format_breast_cancer_result(self, prediction: int, probabilities: np.ndarray) -> Dict[str, Any]:
        """Format breast cancer prediction results."""
        return {
            'success': True,
            'prediction': int(prediction),
            'diagnosis': 'Benign' if prediction == 1 else 'Malignant',
            'probability_malignant': float(probabilities[0]),
            'probability_benign': float(probabilities[1]),
            'confidence': float(max(probabilities)),
            'risk_level': 'Low' if prediction == 1 else 'High'
        }
    
    def _format_fetal_health_result(self, prediction: int, probabilities: np.ndarray) -> Dict[str, Any]:
        """Format fetal health prediction results."""
        health_classes = ['Normal', 'Suspect', 'Pathological']
        health_status = health_classes[prediction - 1] if prediction in [1, 2, 3] else 'Unknown'
        
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
            'risk_level': self._get_fetal_risk_level(health_status)
        }
    
    def _get_risk_level(self, probability: float) -> str:
        """Get risk level based on probability."""
        if probability < 0.3:
            return 'Low'
        elif probability < 0.7:
            return 'Medium'
        else:
            return 'High'
    
    def _get_fetal_risk_level(self, health_status: str) -> str:
        """Get fetal risk level based on health status."""
        risk_mapping = {
            'Normal': 'Low',
            'Suspect': 'Medium',
            'Pathological': 'High'
        }
        return risk_mapping.get(health_status, 'Unknown')
    
    def get_models_info(self) -> Dict[str, Any]:
        """Get information about all loaded models."""
        models_info = {}
        for model_name in self.models.keys():
            models_info[model_name] = self.get_model_info(model_name)
        return models_info
    
    def get_model_info(self, model_name: str) -> Dict[str, Any]:
        """Get detailed information about a specific model."""
        if model_name not in self.models:
            raise ValueError(f"Model '{model_name}' not available")
        
        model_data = self.models[model_name]
        metadata = self.model_metadata.get(model_name, {})
        
        return {
            'model_name': model_name,
            'model_type': metadata.get('model_type', 'unknown'),
            'target_classes': metadata.get('target_classes', []),
            'feature_count': len(model_data.get('feature_names', [])),
            'accuracy': metadata.get('accuracy', 'unknown'),
            'precision': metadata.get('precision', 'unknown'),
            'recall': metadata.get('recall', 'unknown'),
            'f1_score': metadata.get('f1_score', 'unknown'),
            'model_version': metadata.get('model_version', '1.0'),
            'training_date': metadata.get('training_date', 'unknown'),
            'features': model_data.get('feature_names', [])
        }
    
    def get_model_features(self, model_name: str) -> List[str]:
        """Get feature names for a specific model."""
        if model_name not in self.models:
            raise ValueError(f"Model '{model_name}' not available")
        
        return self.models[model_name].get('feature_names', [])
    
    def is_model_available(self, model_name: str) -> bool:
        """Check if a model is available."""
        return model_name in self.models
    
    def reload_model(self, model_name: str):
        """Reload a specific model."""
        if model_name in MODEL_CONFIGS:
            config = MODEL_CONFIGS[model_name]
            self._load_model(model_name, config)
            logger.info(f"Reloaded {model_name} model")
        else:
            raise ValueError(f"Unknown model: {model_name}")


def validate_input_data(data: Dict[str, Any], model_name: str) -> Dict[str, Any]:
    """
    Validate input data against the model's feature schema.
    
    Args:
        data (dict): Input data to validate
        model_name (str): Name of the model
        
    Returns:
        dict: Validation result with 'valid' flag and error messages
    """
    if model_name not in FEATURE_SCHEMAS:
        return {
            'valid': False,
            'message': f'Unknown model: {model_name}'
        }
    
    schema = FEATURE_SCHEMAS[model_name]
    
    # Handle dynamic validation for breast cancer
    if schema.get('dynamic_validation'):
        return _validate_breast_cancer_features(data, schema)
    
    # Regular validation
    errors = []
    
    # Check for missing features
    missing_features = []
    for feature_name, feature_schema in schema.items():
        if feature_name not in data:
            missing_features.append(feature_name)
    
    if missing_features:
        errors.append(f"Missing features: {', '.join(missing_features)}")
    
    # Validate feature values
    for feature_name, value in data.items():
        if feature_name in schema:
            feature_schema = schema[feature_name]
            validation_error = _validate_feature_value(feature_name, value, feature_schema)
            if validation_error:
                errors.append(validation_error)
    
    if errors:
        return {
            'valid': False,
            'message': '; '.join(errors)
        }
    
    return {
        'valid': True,
        'message': 'Input data is valid'
    }


def _validate_breast_cancer_features(data: Dict[str, Any], schema: Dict[str, Any]) -> Dict[str, Any]:
    """Validate breast cancer features dynamically."""
    expected_count = schema.get('feature_count', 30)
    prefixes = schema.get('feature_prefix', ['mean', 'se', 'worst'])
    
    if len(data) != expected_count:
        return {
            'valid': False,
            'message': f'Expected {expected_count} features, got {len(data)}'
        }
    
    # Basic numeric validation
    for feature_name, value in data.items():
        if not isinstance(value, (int, float)):
            return {
                'valid': False,
                'message': f'Feature {feature_name} must be numeric'
            }
        
        if value < 0:
            return {
                'valid': False,
                'message': f'Feature {feature_name} must be non-negative'
            }
    
    return {
        'valid': True,
        'message': 'Input data is valid'
    }


def _validate_feature_value(feature_name: str, value: Any, schema: Dict[str, Any]) -> Optional[str]:
    """
    Validate a single feature value against its schema.
    
    Args:
        feature_name (str): Name of the feature
        value (Any): Value to validate
        schema (dict): Feature schema
        
    Returns:
        str or None: Error message if invalid, None if valid
    """
    feature_type = schema.get('type', 'numeric')
    
    # Type validation
    if feature_type == 'numeric':
        if not isinstance(value, (int, float)):
            return f'{feature_name} must be numeric'
        
        # Range validation
        if 'min' in schema and value < schema['min']:
            return f'{feature_name} must be >= {schema["min"]}'
        
        if 'max' in schema and value > schema['max']:
            return f'{feature_name} must be <= {schema["max"]}'
    
    elif feature_type == 'categorical':
        if 'values' in schema and value not in schema['values']:
            return f'{feature_name} must be one of {schema["values"]}'
    
    return None


def format_prediction_response(prediction: Dict[str, Any], model_name: str) -> Dict[str, Any]:
    """
    Format prediction response with additional metadata.
    
    Args:
        prediction (dict): Raw prediction results
        model_name (str): Name of the model used
        
    Returns:
        dict: Formatted response
    """
    response = prediction.copy()
    
    # Add metadata
    response['model_name'] = model_name
    response['timestamp'] = datetime.now().isoformat()
    response['model_type'] = MODEL_CONFIGS[model_name]['model_type']
    
    # Add interpretation
    if model_name == 'cardiovascular':
        response['interpretation'] = _get_cardiovascular_interpretation(prediction)
    elif model_name == 'breast_cancer':
        response['interpretation'] = _get_breast_cancer_interpretation(prediction)
    elif model_name == 'fetal_health':
        response['interpretation'] = _get_fetal_health_interpretation(prediction)
    
    return response


def _get_cardiovascular_interpretation(prediction: Dict[str, Any]) -> str:
    """Get interpretation for cardiovascular prediction."""
    risk_score = prediction.get('risk_score', 0)
    
    if risk_score < 30:
        return "Low risk of cardiovascular disease. Continue with regular health maintenance."
    elif risk_score < 70:
        return "Moderate risk of cardiovascular disease. Consider lifestyle modifications and regular monitoring."
    else:
        return "High risk of cardiovascular disease. Recommend immediate medical consultation and intervention."


def _get_breast_cancer_interpretation(prediction: Dict[str, Any]) -> str:
    """Get interpretation for breast cancer prediction."""
    diagnosis = prediction.get('diagnosis', '')
    confidence = prediction.get('confidence', 0)
    
    if diagnosis == 'Benign':
        return f"Tumor appears to be benign (confidence: {confidence:.1%}). Regular follow-up recommended."
    else:
        return f"Tumor appears to be malignant (confidence: {confidence:.1%}). Immediate medical consultation required."


def _get_fetal_health_interpretation(prediction: Dict[str, Any]) -> str:
    """Get interpretation for fetal health prediction."""
    health_status = prediction.get('health_status', '')
    confidence = prediction.get('confidence', 0)
    
    interpretations = {
        'Normal': f"Fetal health appears normal (confidence: {confidence:.1%}). Continue routine monitoring.",
        'Suspect': f"Fetal health is suspect (confidence: {confidence:.1%}). Increased monitoring recommended.",
        'Pathological': f"Fetal health shows pathological signs (confidence: {confidence:.1%}). Immediate medical attention required."
    }
    
    return interpretations.get(health_status, "Unable to determine fetal health status.")


def calculate_model_performance(y_true: np.ndarray, y_pred: np.ndarray, y_pred_proba: np.ndarray = None) -> Dict[str, float]:
    """
    Calculate comprehensive model performance metrics.
    
    Args:
        y_true (array): True labels
        y_pred (array): Predicted labels
        y_pred_proba (array, optional): Prediction probabilities
        
    Returns:
        dict: Performance metrics
    """
    from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score
    
    metrics = {
        'accuracy': accuracy_score(y_true, y_pred),
        'precision': precision_score(y_true, y_pred, average='weighted'),
        'recall': recall_score(y_true, y_pred, average='weighted'),
        'f1_score': f1_score(y_true, y_pred, average='weighted')
    }
    
    # Add ROC-AUC for binary classification
    if y_pred_proba is not None and len(np.unique(y_true)) == 2:
        metrics['roc_auc'] = roc_auc_score(y_true, y_pred_proba[:, 1])
    
    return metrics


def check_model_drift(current_performance: Dict[str, float]) -> Dict[str, Any]:
    """
    Check if model performance has drifted below acceptable thresholds.
    
    Args:
        current_performance (dict): Current model performance metrics
        
    Returns:
        dict: Drift analysis results
    """
    drift_detected = False
    issues = []
    
    for metric, threshold in PERFORMANCE_THRESHOLDS.items():
        metric_key = metric.replace('min_', '')
        if metric_key in current_performance:
            current_value = current_performance[metric_key]
            if current_value < threshold:
                drift_detected = True
                issues.append(f"{metric_key}: {current_value:.3f} < {threshold}")
    
    return {
        'drift_detected': drift_detected,
        'issues': issues,
        'recommendation': 'Model retraining recommended' if drift_detected else 'Model performance acceptable'
    }


class DataLogger:
    """Logger for prediction requests and responses."""
    
    def __init__(self, log_file: str = None):
        """Initialize the data logger."""
        self.log_file = Path(log_file) if log_file else Path('logs/predictions.jsonl')
        self.log_file.parent.mkdir(parents=True, exist_ok=True)
    
    def log_prediction(self, model_name: str, input_data: Dict[str, Any], 
                      prediction: Dict[str, Any], user_id: str = None):
        """
        Log a prediction request and response.
        
        Args:
            model_name (str): Name of the model used
            input_data (dict): Input features
            prediction (dict): Prediction results
            user_id (str, optional): User identifier
        """
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'model_name': model_name,
            'user_id': user_id,
            'input_data': input_data,
            'prediction': prediction
        }
        
        try:
            with open(self.log_file, 'a', encoding='utf-8') as f:
                f.write(json.dumps(log_entry) + '\n')
        except Exception as e:
            logger.error(f"Failed to log prediction: {e}")


# Global data logger instance
data_logger = DataLogger()
