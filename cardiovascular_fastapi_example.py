# 🌐 FastAPI Cardiovascular Disease Prediction Application
# Model Integration Example for CardIovascular Disease Prediction

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, validator
from typing import Optional, List, Dict, Any
import joblib
import pandas as pd
import numpy as np
import logging
from datetime import datetime

# FastAPI app initialization
app = FastAPI(
    title="Cardiovascular Disease Prediction API",
    description="AI-powered cardiovascular disease risk assessment API",
    version="1.0.0"
)

# CORS middleware for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load model and preprocessing components
try:
    model_data = joblib.load('app/model/model_cad/cardiovascular_model.pkl')
    scaler = joblib.load('app/model/model_cad/scaler.pkl')
    metadata = joblib.load('app/model/model_cad/model_metadata.pkl')
    
    best_model = model_data if isinstance(model_data, object) else model_data['best_model']
    feature_names = metadata.get('features', [])
    
    logging.info("✅ Cardiovascular model loaded successfully")
except FileNotFoundError as e:
    logging.error(f"❌ Model files not found: {e}")
    best_model = None
    scaler = None

# Pydantic models for request/response
class CardiovascularPredictionRequest(BaseModel):
    """Cardiovascular disease prediction request model"""
    age: int
    sex: int  # 1: male, 0: female
    chest_pain_type: int  # 0-3
    resting_bp: int
    cholesterol: int
    fasting_bs: int  # 1: >120mg/dl, 0: <=120mg/dl
    resting_ecg: int  # 0-2
    max_hr: int
    exercise_angina: int  # 1: yes, 0: no
    oldpeak: float
    st_slope: int  # 0-2
    
    @validator('age')
    def validate_age(cls, v):
        if not 18 <= v <= 100:
            raise ValueError('Age must be between 18 and 100')
        return v
    
    @validator('resting_bp')
    def validate_bp(cls, v):
        if not 80 <= v <= 250:
            raise ValueError('Resting BP must be between 80 and 250')
        return v
    
    @validator('max_hr')
    def validate_hr(cls, v):
        if not 60 <= v <= 220:
            raise ValueError('Max HR must be between 60 and 220')
        return v

class CardiovascularPredictionResponse(BaseModel):
    """Cardiovascular disease prediction response model"""
    risk_level: str
    probability: float
    risk_percentage: float
    confidence: float
    recommendations: List[str]
    risk_factors: List[str]
    timestamp: datetime
    model_info: Dict[str, Any]

# API Endpoints
@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "message": "Cardiovascular Disease Prediction API", 
        "status": "active",
        "version": "1.0.0"
    }

@app.get("/health")
async def health_check():
    """Detailed health check"""
    model_status = "loaded" if best_model is not None else "not_loaded"
    return {
        "api_status": "healthy",
        "model_status": model_status,
        "timestamp": datetime.now(),
        "features_count": len(feature_names) if feature_names else 0
    }

@app.post("/predict/cardiovascular", response_model=CardiovascularPredictionResponse)
async def predict_cardiovascular_disease(request: CardiovascularPredictionRequest):
    """
    Predict cardiovascular disease risk based on patient data
    """
    if best_model is None or scaler is None:
        raise HTTPException(status_code=503, detail="Model not available")
    
    try:
        # Prepare input data
        input_data = pd.DataFrame([[
            request.age,
            request.sex,
            request.chest_pain_type,
            request.resting_bp,
            request.cholesterol,
            request.fasting_bs,
            request.resting_ecg,
            request.max_hr,
            request.exercise_angina,
            request.oldpeak,
            request.st_slope
        ]], columns=feature_names)
        
        # Scale features
        input_scaled = scaler.transform(input_data)
        
        # Make prediction
        prediction = best_model.predict(input_scaled)[0]
        probability = best_model.predict_proba(input_scaled)[0]
        
        # Calculate risk metrics
        risk_prob = probability[1]  # Probability of heart disease
        risk_percentage = risk_prob * 100
        
        # Determine risk level
        if risk_percentage < 30:
            risk_level = "Low Risk"
            confidence = 0.85
        elif risk_percentage < 60:
            risk_level = "Moderate Risk"
            confidence = 0.80
        else:
            risk_level = "High Risk"
            confidence = 0.90
        
        # Generate recommendations
        recommendations = generate_recommendations(request, risk_level)
        risk_factors = identify_risk_factors(request)
        
        return CardiovascularPredictionResponse(
            risk_level=risk_level,
            probability=float(risk_prob),
            risk_percentage=float(risk_percentage),
            confidence=confidence,
            recommendations=recommendations,
            risk_factors=risk_factors,
            timestamp=datetime.now(),
            model_info={
                "model_type": metadata.get('model_type', 'Unknown'),
                "accuracy": metadata.get('accuracy', 0.0),
                "features_used": len(feature_names)
            }
        )
        
    except Exception as e:
        logging.error(f"Prediction error: {e}")
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")

def generate_recommendations(request: CardiovascularPredictionRequest, risk_level: str) -> List[str]:
    """Generate personalized health recommendations"""
    recommendations = []
    
    # Age-based recommendations
    if request.age > 50:
        recommendations.append("🏥 Regular cardiology check-ups recommended due to age")
    
    # Blood pressure recommendations
    if request.resting_bp > 140:
        recommendations.append("🩺 High blood pressure detected - consult doctor for management")
    
    # Cholesterol recommendations  
    if request.cholesterol > 240:
        recommendations.append("🥗 High cholesterol - consider dietary changes and medication")
    
    # Exercise recommendations
    if request.max_hr < 100:
        recommendations.append("🏃‍♂️ Low exercise capacity - gradually increase physical activity")
    
    # General recommendations based on risk
    if risk_level == "High Risk":
        recommendations.extend([
            "🚨 Immediate medical consultation recommended",
            "💊 Discuss preventive medications with cardiologist",
            "📊 Regular monitoring of cardiac biomarkers"
        ])
    elif risk_level == "Moderate Risk":
        recommendations.extend([
            "⚖️ Lifestyle modifications strongly recommended",
            "🔄 Follow-up in 3-6 months",
            "📈 Monitor blood pressure and cholesterol regularly"
        ])
    else:
        recommendations.extend([
            "✅ Continue healthy lifestyle habits",
            "🔄 Annual check-ups sufficient",
            "💪 Maintain current activity level"
        ])
    
    return recommendations

def identify_risk_factors(request: CardiovascularPredictionRequest) -> List[str]:
    """Identify specific risk factors"""
    risk_factors = []
    
    if request.age > 55:
        risk_factors.append("Advanced age")
    if request.sex == 1:  # Male
        risk_factors.append("Male gender")
    if request.resting_bp > 140:
        risk_factors.append("High blood pressure")
    if request.cholesterol > 240:
        risk_factors.append("High cholesterol")
    if request.fasting_bs == 1:
        risk_factors.append("Elevated fasting blood sugar")
    if request.exercise_angina == 1:
        risk_factors.append("Exercise-induced angina")
    if request.max_hr < 100:
        risk_factors.append("Low exercise capacity")
    
    return risk_factors

# Additional utility endpoints
@app.get("/model/info")
async def get_model_info():
    """Get model information and metadata"""
    if best_model is None:
        raise HTTPException(status_code=503, detail="Model not available")
    
    return {
        "model_metadata": metadata,
        "feature_names": feature_names,
        "model_loaded": True,
        "last_updated": datetime.now()
    }

@app.get("/features")
async def get_feature_info():
    """Get information about required features"""
    feature_info = {
        "age": "Patient age (18-100 years)",
        "sex": "Gender (1: Male, 0: Female)", 
        "chest_pain_type": "Chest pain type (0-3)",
        "resting_bp": "Resting blood pressure (mmHg)",
        "cholesterol": "Serum cholesterol (mg/dl)",
        "fasting_bs": "Fasting blood sugar >120mg/dl (1: Yes, 0: No)",
        "resting_ecg": "Resting ECG results (0-2)",
        "max_hr": "Maximum heart rate achieved",
        "exercise_angina": "Exercise induced angina (1: Yes, 0: No)",
        "oldpeak": "ST depression induced by exercise",
        "st_slope": "Slope of peak exercise ST segment (0-2)"
    }
    
    return {
        "required_features": feature_info,
        "total_features": len(feature_info)
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
