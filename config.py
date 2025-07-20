"""
MediRisk Tıbbi Tahmin Sistemi için Yapılandırma Ayarları
==============================================================

Bu modül kardiyovasküler hastalık, meme kanseri ve fetal sağlık tahminlerini
içeren çok alanli tıbbi tahmin sistemi için yapılandırma ayarlarını içerir.
FastAPI backend için optimize edilmiştir.
"""

import os
from pathlib import Path

# Base directory
BASE_DIR = Path(__file__).parent.absolute()

# Model configurations
MODEL_CONFIGS = {
    'cardiovascular': {
        'model_path': BASE_DIR / 'model' / 'model_cardiovascular' / 'cardiovascular_model.pkl',
        'data_path': BASE_DIR / 'data' / 'Cardiovascular_Disease_Dataset.csv',
        'model_type': 'binary_classification',
        'target_classes': ['Sağlıklı', 'Kardiyovasküler Hastalık'],
        'threshold': 0.5,
        'api_endpoint': '/api/predict/cardiovascular'
    },
    'breast_cancer': {
        'model_path': BASE_DIR / 'model' / 'model_breast' / 'breast_cancer_model.pkl',
        'data_path': BASE_DIR / 'data' / 'Breast_Cancer.csv',
        'model_type': 'binary_classification',
        'target_classes': ['Malign', 'Benign'],
        'threshold': 0.5,
        'api_endpoint': '/api/predict/breast_cancer'
    },
    'fetal_health': {
        'model_path': BASE_DIR / 'model' / 'model_fetal' / 'fetal_health_model.pkl',
        'data_path': BASE_DIR / 'data' / 'fetal_health.csv',
        'model_type': 'multiclass_classification',
        'target_classes': ['Normal', 'Şüpheli', 'Patolojik'],
        'api_endpoint': '/api/predict/fetal_health'
    }
}

# FastAPI configuration
class Config:
    """Temel yapılandırma sınıfı - FastAPI için."""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'medirisk-medical-prediction-system'
    DEBUG = False
    TESTING = False
    # Database configuration (if needed in future)
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Upload configuration
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    UPLOAD_FOLDER = BASE_DIR / 'uploads'
    
    # Logging configuration
    LOG_LEVEL = 'INFO'
    LOG_FILE = BASE_DIR / 'logs' / 'app.log'
    
    # Model cache settings
    MODEL_CACHE_TIMEOUT = 3600  # 1 hour
    
    # API rate limiting
    RATELIMIT_STORAGE_URL = 'memory://'
    RATELIMIT_DEFAULT = "100 per hour"
    
    # CORS settings for FastAPI
    CORS_ORIGINS = ['http://localhost:3000', 'http://127.0.0.1:3000']
    
    # FastAPI specific settings
    API_V1_STR = "/api/v1"
    PROJECT_NAME = "MediRisk API"
    VERSION = "1.0.0"

class DevelopmentConfig(Config):
    """Development configuration."""
    DEBUG = True
    LOG_LEVEL = 'DEBUG'

class ProductionConfig(Config):
    """Production configuration for FastAPI."""
    DEBUG = False
    LOG_LEVEL = 'WARNING'
    
    # Security headers for production
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'

class TestingConfig(Config):
    """Testing configuration."""
    TESTING = True
    DEBUG = True
    LOG_LEVEL = 'DEBUG'

# Configuration mapping
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}

# Feature validation schemas
FEATURE_SCHEMAS = {
    'cardiovascular': {
        'age': {'type': 'numeric', 'min': 20, 'max': 100},
        'gender': {'type': 'categorical', 'values': [0, 1]},
        'chest_pain_type': {'type': 'categorical', 'values': [0, 1, 2, 3]},
        'resting_blood_pressure': {'type': 'numeric', 'min': 80, 'max': 200},
        'serum_cholesterol': {'type': 'numeric', 'min': 100, 'max': 500},
        'fasting_blood_sugar': {'type': 'categorical', 'values': [0, 1]},
        'resting_ecg': {'type': 'categorical', 'values': [0, 1, 2]},
        'max_heart_rate': {'type': 'numeric', 'min': 60, 'max': 220},
        'exercise_angina': {'type': 'categorical', 'values': [0, 1]},
        'oldpeak': {'type': 'numeric', 'min': 0, 'max': 10},
        'slope': {'type': 'categorical', 'values': [0, 1, 2]},
        'num_major_vessels': {'type': 'categorical', 'values': [0, 1, 2, 3]}
    },
    'breast_cancer': {
        # Features will be dynamically validated based on sklearn dataset
        'dynamic_validation': True,
        'feature_count': 30,
        'feature_prefix': ['mean', 'se', 'worst']
    },
    'fetal_health': {
        'baseline_value': {'type': 'numeric', 'min': 50, 'max': 200},
        'accelerations': {'type': 'numeric', 'min': 0, 'max': 1},
        'fetal_movement': {'type': 'numeric', 'min': 0, 'max': 1},
        'uterine_contractions': {'type': 'numeric', 'min': 0, 'max': 1},
        'light_decelerations': {'type': 'numeric', 'min': 0, 'max': 1},
        'severe_decelerations': {'type': 'numeric', 'min': 0, 'max': 1},
        'prolongued_decelerations': {'type': 'numeric', 'min': 0, 'max': 1},
        'abnormal_short_term_variability': {'type': 'numeric', 'min': 0, 'max': 100},
        'mean_value_of_short_term_variability': {'type': 'numeric', 'min': 0, 'max': 20},
        'percentage_of_time_with_abnormal_long_term_variability': {'type': 'numeric', 'min': 0, 'max': 100},
        'mean_value_of_long_term_variability': {'type': 'numeric', 'min': 0, 'max': 100},
        'histogram_width': {'type': 'numeric', 'min': 0, 'max': 300},
        'histogram_min': {'type': 'numeric', 'min': 0, 'max': 200},
        'histogram_max': {'type': 'numeric', 'min': 50, 'max': 300},
        'histogram_number_of_peaks': {'type': 'numeric', 'min': 0, 'max': 20},
        'histogram_number_of_zeroes': {'type': 'numeric', 'min': 0, 'max': 10},
        'histogram_mode': {'type': 'numeric', 'min': 50, 'max': 200},
        'histogram_mean': {'type': 'numeric', 'min': 50, 'max': 200},
        'histogram_median': {'type': 'numeric', 'min': 50, 'max': 200},
        'histogram_variance': {'type': 'numeric', 'min': 0, 'max': 2000},
        'histogram_tendency': {'type': 'categorical', 'values': [-1, 0, 1]}
    }
}

# Model performance thresholds
PERFORMANCE_THRESHOLDS = {
    'min_accuracy': 0.80,
    'min_precision': 0.75,
    'min_recall': 0.75,
    'min_f1_score': 0.75
}

# Logging configuration
LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
        },
        'detailed': {
            'format': '%(asctime)s [%(levelname)s] %(name)s:%(lineno)d: %(message)s'
        }
    },
    'handlers': {
        'default': {
            'level': 'INFO',
            'formatter': 'standard',
            'class': 'logging.StreamHandler',
        },
        'file': {
            'level': 'INFO',
            'formatter': 'detailed',
            'class': 'logging.FileHandler',
            'filename': 'logs/app.log',
            'mode': 'a',
        },
    },
    'loggers': {
        '': {
            'handlers': ['default', 'file'],
            'level': 'INFO',
            'propagate': False
        }
    }
}
