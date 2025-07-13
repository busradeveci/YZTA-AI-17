"""
YZTA-AI-17 Medical Prediction System
===================================

A comprehensive Flask application for multi-domain medical predictions including:
- Cardiovascular Disease Prediction
- Breast Cancer Diagnosis
- Fetal Health Classification

This application uses machine learning models trained with the PACE methodology
to provide real-time medical risk assessments.
"""

from flask import Flask
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import logging
import os
from pathlib import Path

from config import config, LOGGING_CONFIG


def create_app(config_name=None):
    """
    Application factory pattern for creating Flask app instances.
    
    Args:
        config_name (str): Configuration environment name
        
    Returns:
        Flask: Configured Flask application instance
    """
    app = Flask(__name__, 
                static_folder='../static',
                static_url_path='/static')
    
    # Load configuration
    config_name = config_name or os.environ.get('FLASK_ENV', 'development')
    app.config.from_object(config[config_name])
    
    # Initialize extensions
    CORS(app, origins=app.config['CORS_ORIGINS'])
    
    # Initialize rate limiting
    limiter = Limiter(
        key_func=get_remote_address,
        default_limits=[app.config['RATELIMIT_DEFAULT']]
    )
    limiter.init_app(app)
    
    # Setup logging
    setup_logging(app)
    
    # Create necessary directories
    create_directories(app)
    
    # Register blueprints
    register_blueprints(app)
    
    # Register error handlers
    register_error_handlers(app)
    
    # Health check endpoint
    @app.route('/health')
    def health_check():
        """Application health check endpoint."""
        return {
            'status': 'healthy',
            'version': '1.0.0',
            'models': ['cardiovascular', 'breast_cancer', 'fetal_health']
        }
    
    app.logger.info('YZTA-AI-17 Medical Prediction System initialized successfully')
    return app


def setup_logging(app):
    """Setup application logging configuration."""
    import logging.config
    
    # Create logs directory if it doesn't exist
    log_dir = Path(app.config['LOG_FILE']).parent
    log_dir.mkdir(parents=True, exist_ok=True)
    
    # Apply logging configuration
    logging.config.dictConfig(LOGGING_CONFIG)
    
    # Set Flask app logger level
    app.logger.setLevel(getattr(logging, app.config['LOG_LEVEL']))


def create_directories(app):
    """Create necessary application directories."""
    directories = [
        app.config['UPLOAD_FOLDER'],
        Path(app.config['LOG_FILE']).parent,
        Path(app.instance_path)
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)


def register_blueprints(app):
    """Register application blueprints."""
    from app.routes import main_bp, api_bp
    
    app.register_blueprint(main_bp)
    app.register_blueprint(api_bp, url_prefix='/api')


def register_error_handlers(app):
    """Register application error handlers."""
    
    @app.errorhandler(404)
    def not_found_error(error):
        return {
            'error': 'Resource not found',
            'status': 404
        }, 404
    
    @app.errorhandler(500)
    def internal_error(error):
        app.logger.error(f'Internal server error: {error}')
        return {
            'error': 'Internal server error',
            'status': 500
        }, 500
    
    @app.errorhandler(400)
    def bad_request_error(error):
        return {
            'error': 'Bad request',
            'status': 400
        }, 400
    
    @app.errorhandler(429)
    def ratelimit_handler(error):
        return {
            'error': 'Rate limit exceeded',
            'status': 429
        }, 429


# Global variable for development server
app = None

if __name__ == '__main__':
    app = create_app('development')
    app.run(host='0.0.0.0', port=5000, debug=True)
