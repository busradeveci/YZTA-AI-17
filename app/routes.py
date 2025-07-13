"""
YZTA-AI-17 Tıbbi Tahmin Sistemi için Flask Route'ları
====================================================

Bu modül tıbbi tahmin sistemi için tüm web route'larını ve API endpoint'lerini içerir.
Kardiyovasküler hastalık, meme kanseri ve fetal sağlık tahminleri için route'ları içerir.
"""

from flask import Blueprint, render_template, request, jsonify, current_app
import logging
import traceback
from pathlib import Path

from app.utils import ModelManager, validate_input_data, format_prediction_response

# Create blueprints
main_bp = Blueprint('main', __name__)
api_bp = Blueprint('api', __name__)

# Initialize model manager
model_manager = ModelManager()

logger = logging.getLogger(__name__)


# Main web interface routes
@main_bp.route('/')
def index():
    """Mevcut tüm tahmin modellerini gösteren ana panel sayfası."""
    try:
        model_info = model_manager.get_models_info()
        return render_template('index.html', models=model_info)
    except Exception as e:
        logger.error(f"Ana sayfa yükleme hatası: {e}")
        return render_template('error.html', error="Uygulama yüklenemedi"), 500


@main_bp.route('/cardiovascular')
def cardiovascular_form():
    """Kardiyovasküler hastalık tahmin formu sayfası."""
    try:
        model_info = model_manager.get_model_info('cardiovascular')
        return render_template('cardiovascular.html', model_info=model_info)
    except Exception as e:
        logger.error(f"Kardiyovasküler form yükleme hatası: {e}")
        return render_template('error.html', error="Kardiyovasküler form yüklenemedi"), 500


@main_bp.route('/breast_cancer')
def breast_cancer_form():
    """Meme kanseri tahmin formu sayfası."""
    try:
        model_info = model_manager.get_model_info('breast_cancer')
        return render_template('breast_cancer.html', model_info=model_info)
    except Exception as e:
        logger.error(f"Meme kanseri formu yükleme hatası: {e}")
        return render_template('error.html', error="Meme kanseri formu yüklenemedi"), 500


@main_bp.route('/fetal_health')
def fetal_health_form():
    """Fetal sağlık tahmin formu sayfası."""
    try:
        model_info = model_manager.get_model_info('fetal_health')
        return render_template('fetal_health.html', model_info=model_info)
    except Exception as e:
        logger.error(f"Fetal sağlık formu yükleme hatası: {e}")
        return render_template('error.html', error="Fetal sağlık formu yüklenemedi"), 500


# API endpoints
@api_bp.route('/models', methods=['GET'])
def get_models():
    """Mevcut tüm modeller hakkında bilgi al."""
    try:
        models_info = model_manager.get_models_info()
        return jsonify({
            'success': True,
            'models': models_info
        })
    except Exception as e:
        logger.error(f"Model bilgisi alma hatası: {e}")
        return jsonify({
            'success': False,
            'error': 'Model bilgileri alınamadı'
        }), 500


@api_bp.route('/predict/cardiovascular', methods=['POST'])
def predict_cardiovascular():
    """Kardiyovasküler hastalık tahmin API endpoint'i."""
    try:
        # Request verilerini doğrula
        if not request.is_json:
            return jsonify({
                'success': False,
                'error': 'İstek JSON formatında olmalıdır'
            }), 400
        
        data = request.get_json()
        
        # Giriş verilerini doğrula
        validation_result = validate_input_data(data, 'cardiovascular')
        if not validation_result['valid']:
            return jsonify({
                'success': False,
                'error': validation_result['message']
            }), 400
        
        # Tahmin yap
        prediction = model_manager.predict('cardiovascular', data)
        
        # Yanıtı formatla
        response = format_prediction_response(prediction, 'cardiovascular')
        
        logger.info(f"Kardiyovasküler tahmin yapıldı: {response['risk_class']}")
        return jsonify(response)
        
    except Exception as e:
        logger.error(f"Kardiyovasküler tahmin hatası: {e}")
        logger.error(traceback.format_exc())
        return jsonify({
            'success': False,
            'error': 'Tahmin başarısız oldu'
        }), 500


@api_bp.route('/predict/breast_cancer', methods=['POST'])
def predict_breast_cancer():
    """Meme kanseri tahmin API endpoint'i."""
    try:
        # Request verilerini doğrula
        if not request.is_json:
            return jsonify({
                'success': False,
                'error': 'İstek JSON formatında olmalıdır'
            }), 400
        
        data = request.get_json()
        
        # Giriş verilerini doğrula
        validation_result = validate_input_data(data, 'breast_cancer')
        if not validation_result['valid']:
            return jsonify({
                'success': False,
                'error': validation_result['message']
            }), 400
        
        # Tahmin yap
        prediction = model_manager.predict('breast_cancer', data)
        
        # Format response
        response = format_prediction_response(prediction, 'breast_cancer')
        
        logger.info(f"Breast cancer prediction made: {response['diagnosis']}")
        return jsonify(response)
        
    except Exception as e:
        logger.error(f"Error in breast cancer prediction: {e}")
        logger.error(traceback.format_exc())
        return jsonify({
            'success': False,
            'error': 'Prediction failed'
        }), 500


@api_bp.route('/predict/fetal_health', methods=['POST'])
def predict_fetal_health():
    """Fetal health prediction API endpoint."""
    try:
        # Validate request data
        if not request.is_json:
            return jsonify({
                'success': False,
                'error': 'Request must be JSON'
            }), 400
        
        data = request.get_json()
        
        # Validate input data
        validation_result = validate_input_data(data, 'fetal_health')
        if not validation_result['valid']:
            return jsonify({
                'success': False,
                'error': validation_result['message']
            }), 400
        
        # Make prediction
        prediction = model_manager.predict('fetal_health', data)
        
        # Format response
        response = format_prediction_response(prediction, 'fetal_health')
        
        logger.info(f"Fetal health prediction made: {response['health_status']}")
        return jsonify(response)
        
    except Exception as e:
        logger.error(f"Error in fetal health prediction: {e}")
        logger.error(traceback.format_exc())
        return jsonify({
            'success': False,
            'error': 'Prediction failed'
        }), 500


@api_bp.route('/model/<model_name>/info', methods=['GET'])
def get_model_info(model_name):
    """Get detailed information about a specific model."""
    try:
        if model_name not in ['cardiovascular', 'breast_cancer', 'fetal_health']:
            return jsonify({
                'success': False,
                'error': 'Invalid model name'
            }), 400
        
        model_info = model_manager.get_model_info(model_name)
        
        return jsonify({
            'success': True,
            'model_info': model_info
        })
        
    except Exception as e:
        logger.error(f"Error getting model info for {model_name}: {e}")
        return jsonify({
            'success': False,
            'error': 'Failed to retrieve model information'
        }), 500


@api_bp.route('/model/<model_name>/features', methods=['GET'])
def get_model_features(model_name):
    """Get feature information for a specific model."""
    try:
        if model_name not in ['cardiovascular', 'breast_cancer', 'fetal_health']:
            return jsonify({
                'success': False,
                'error': 'Invalid model name'
            }), 400
        
        features = model_manager.get_model_features(model_name)
        
        return jsonify({
            'success': True,
            'features': features
        })
        
    except Exception as e:
        logger.error(f"Error getting features for {model_name}: {e}")
        return jsonify({
            'success': False,
            'error': 'Failed to retrieve model features'
        }), 500


# Batch prediction endpoint (for future enhancement)
@api_bp.route('/predict/batch', methods=['POST'])
def batch_predict():
    """Batch prediction endpoint for multiple samples."""
    try:
        if not request.is_json:
            return jsonify({
                'success': False,
                'error': 'Request must be JSON'
            }), 400
        
        data = request.get_json()
        
        if 'model_name' not in data or 'samples' not in data:
            return jsonify({
                'success': False,
                'error': 'Model name and samples are required'
            }), 400
        
        model_name = data['model_name']
        samples = data['samples']
        
        if model_name not in ['cardiovascular', 'breast_cancer', 'fetal_health']:
            return jsonify({
                'success': False,
                'error': 'Invalid model name'
            }), 400
        
        if not isinstance(samples, list) or len(samples) == 0:
            return jsonify({
                'success': False,
                'error': 'Samples must be a non-empty list'
            }), 400
        
        # Limit batch size
        if len(samples) > 100:
            return jsonify({
                'success': False,
                'error': 'Batch size limited to 100 samples'
            }), 400
        
        # Process batch predictions
        results = []
        for i, sample in enumerate(samples):
            try:
                validation_result = validate_input_data(sample, model_name)
                if not validation_result['valid']:
                    results.append({
                        'sample_index': i,
                        'success': False,
                        'error': validation_result['message']
                    })
                    continue
                
                prediction = model_manager.predict(model_name, sample)
                response = format_prediction_response(prediction, model_name)
                response['sample_index'] = i
                results.append(response)
                
            except Exception as e:
                results.append({
                    'sample_index': i,
                    'success': False,
                    'error': f'Prediction failed: {str(e)}'
                })
        
        return jsonify({
            'success': True,
            'batch_results': results,
            'total_samples': len(samples),
            'successful_predictions': sum(1 for r in results if r.get('success', False))
        })
        
    except Exception as e:
        logger.error(f"Error in batch prediction: {e}")
        logger.error(traceback.format_exc())
        return jsonify({
            'success': False,
            'error': 'Batch prediction failed'
        }), 500
