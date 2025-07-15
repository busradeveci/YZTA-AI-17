# YZTA-AI-17 Development Guide

## 🏥 Project Overview

YZTA-AI-17 is a comprehensive medical prediction system that uses machine learning to assess health risks across three critical domains:

- **Cardiovascular Disease**: Risk assessment based on clinical parameters
- **Breast Cancer**: Malignancy detection using tissue measurements  
- **Fetal Health**: Wellbeing assessment through CTG data analysis

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Installation & Setup

1. **Clone or navigate to the project directory**
```bash
cd /path/to/YZTA-AI-17
```

2. **Install dependencies**
```bash
python run.py --install
# OR manually:
pip install -r requirements.txt
```

3. **Start the application**
```bash
python run.py
# OR with custom settings:
python run.py --host 0.0.0.0 --port 8080 --debug
```

4. **Open your browser**
Navigate to `http://127.0.0.1:5000`

## 📁 Project Structure

```
YZTA-AI-17/
├── app/                          # Flask application
│   ├── __init__.py              # App factory
│   ├── routes.py                # API endpoints
│   ├── utils.py                 # Model manager
│   ├── model/                   # ML models
│   │   ├── model_cad/          # Cardiovascular model
│   │   ├── model_breast/       # Breast cancer model
│   │   ├── model_fetal/        # Fetal health model
│   │   └── shared/             # Shared utilities
│   └── templates/              # HTML templates
├── data/                        # Training datasets
├── static/                      # CSS, JS, images
├── tests/                       # Test suite
├── notebooks/                   # Jupyter analysis
├── config.py                    # Configuration
├── requirements.txt             # Dependencies
├── run.py                      # Run script
└── README.md                   # Documentation
```

## 🔬 Model Architecture

### PACE Methodology
All models follow the PACE (Plan, Analyze, Construct, Execute) methodology:

1. **Plan**: Define objectives and success criteria
2. **Analyze**: Explore data and identify patterns
3. **Construct**: Build and validate models
4. **Execute**: Deploy and monitor performance

### Model Pipeline
Each prediction model includes:

- **Preprocessing**: Data validation and feature engineering
- **Prediction**: ML model inference
- **Interpretation**: Clinical analysis and recommendations
- **Validation**: Medical coherence checks

## 🛠️ Development

### Adding a New Model

1. **Create model directory**
```bash
mkdir app/model/model_new
touch app/model/model_new/__init__.py
```

2. **Implement predictor class**
```python
# app/model/model_new/predict.py
from ..shared.preprocessing_utils import BasePreprocessor

class NewPreprocessor(BasePreprocessor):
    def __init__(self):
        super().__init__()
        # Define feature ranges and validation rules
    
    def validate_input(self, data):
        # Implement validation logic
        pass
    
    def preprocess(self, data):
        # Implement preprocessing logic
        pass

class NewPredictor:
    def __init__(self):
        self.preprocessor = NewPreprocessor()
    
    def predict(self, data):
        # Implement prediction logic
        pass
```

3. **Add API endpoint**
```python
# app/routes.py
@bp.route('/api/predict/new', methods=['POST'])
def predict_new():
    # Implement endpoint logic
    pass
```

4. **Update configuration**
```python
# config.py
MODEL_CONFIGS = {
    'new': {
        'name': 'New Model',
        'path': 'app/model/model_new/new_model.pkl',
        'features': [...],
        'target': 'prediction'
    }
}
```

### Testing

Run the test suite:
```bash
python run.py --test
# OR specific tests:
python tests/test_system.py --test cardiovascular
```

### Code Quality

The project follows these standards:
- **Type hints**: All functions have type annotations
- **Docstrings**: Comprehensive documentation
- **Error handling**: Robust exception management
- **Logging**: Structured logging throughout
- **Validation**: Input validation at all levels

## 🔧 Configuration

### Environment Variables
```bash
# Development
export FLASK_ENV=development
export FLASK_DEBUG=1

# Production
export FLASK_ENV=production
export SECRET_KEY=your-secret-key
```

### Model Configuration
Edit `config.py` to modify:
- Model file paths
- Feature schemas
- Validation rules
- Clinical thresholds

## 📊 API Reference

### Endpoints

#### Health Check
```http
GET /health
```

#### Model Information
```http
GET /api/models/info
```

#### Cardiovascular Prediction
```http
POST /api/predict/cardiovascular
Content-Type: application/json

{
  "age": 63,
  "gender": 1,
  "chest_pain_type": 3,
  "resting_blood_pressure": 145,
  ...
}
```

#### Breast Cancer Prediction
```http
POST /api/predict/breast-cancer
Content-Type: application/json

{
  "radius_mean": 17.99,
  "texture_mean": 10.38,
  "perimeter_mean": 122.8,
  ...
}
```

#### Fetal Health Prediction
```http
POST /api/predict/fetal-health
Content-Type: application/json

{
  "baseline_value": 120,
  "accelerations": 0.000,
  "fetal_movement": 0.0,
  ...
}
```

### Response Format
```json
{
  "prediction": 1,
  "confidence": 0.95,
  "risk_level": "High Risk",
  "clinical_recommendations": [...],
  "key_findings": [...],
  "timestamp": "2024-01-15T10:30:00"
}
```

## 🧪 Data Science Workflow

### Training New Models

1. **Data Preparation**
```python
import pandas as pd
from sklearn.model_selection import train_test_split

# Load and clean data
df = pd.read_csv('data/new_dataset.csv')
X, y = prepare_features(df)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
```

2. **Model Training**
```python
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler

# Scale features
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)

# Train model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train_scaled, y_train)
```

3. **Model Evaluation**
```python
from sklearn.metrics import classification_report, confusion_matrix

# Evaluate performance
y_pred = model.predict(X_test_scaled)
print(classification_report(y_test, y_pred))
```

4. **Model Serialization**
```python
import joblib

# Save model and scaler
model_data = {
    'model': model,
    'scaler': scaler,
    'feature_names': X.columns.tolist(),
    'target_names': ['class_0', 'class_1']
}
joblib.dump(model_data, 'app/model/model_new/new_model.pkl')
```

### Jupyter Notebooks

The `notebooks/` directory contains analysis notebooks:
- `card.ipynb`: Cardiovascular disease analysis
- `breast_cancer_analysis.ipynb`: Breast cancer analysis
- `fetal_health_analysis.ipynb`: Fetal health analysis

## 🔒 Security Considerations

- **Input Validation**: All inputs are validated before processing
- **Rate Limiting**: API endpoints have rate limiting enabled
- **CORS**: Configured for secure cross-origin requests
- **Data Privacy**: No patient data is stored permanently
- **Error Handling**: Sensitive information is not exposed in errors

## 🚀 Deployment

### Local Development
```bash
python run.py --debug
```

### Production Deployment
```bash
# Using Gunicorn
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:8000 "app:create_app()"

# Using Docker (create Dockerfile)
docker build -t yzta-ai-17 .
docker run -p 8000:8000 yzta-ai-17
```

### Environment Configuration
```python
# Production settings in config.py
class ProductionConfig(Config):
    DEBUG = False
    TESTING = False
    # Add production-specific settings
```

## 📈 Monitoring and Logging

- **Application Logs**: Structured logging with different levels
- **Performance Metrics**: Request timing and model inference metrics
- **Error Tracking**: Comprehensive error logging and reporting
- **Health Checks**: Built-in health check endpoints

## 🤝 Contributing

1. **Fork the repository**
2. **Create a feature branch**
3. **Make your changes**
4. **Add tests for new functionality**
5. **Run the test suite**
6. **Submit a pull request**

### Code Style
- Follow PEP 8 Python style guide
- Use type hints for all functions
- Write comprehensive docstrings
- Add unit tests for new features

## 📝 Troubleshooting

### Common Issues

**Import Errors**
```bash
# Check Python path
python -c "import sys; print(sys.path)"

# Reinstall dependencies
python run.py --install
```

**Model Loading Errors**
```bash
# Check model files exist
ls -la app/model/*/
```

**Port Already in Use**
```bash
# Use different port
python run.py --port 8080
```

### Debug Mode
```bash
# Enable detailed error messages
python run.py --debug
```

## 📚 Additional Resources

- **Flask Documentation**: https://flask.palletsprojects.com/
- **Scikit-learn**: https://scikit-learn.org/
- **Pandas**: https://pandas.pydata.org/
- **Medical ML Best Practices**: https://www.fda.gov/medical-devices/software-medical-device-samd/artificial-intelligence-and-machine-learning-software-medical-device

## ⚠️ Disclaimer

This system is for research and educational purposes only. It should not be used as a substitute for professional medical advice, diagnosis, or treatment. Always consult with qualified healthcare providers for medical decisions.
