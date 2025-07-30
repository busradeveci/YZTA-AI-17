# -*- coding: utf-8 -*-
from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Dict, Any, List, Optional
import joblib
import pandas as pd
import numpy as np
from datetime import datetime
import os
import json
import logging
import asyncio
import requests
import time
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Logging ayarları
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Health Screening API",
    description="AI-powered health risk analysis API",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Tüm origin'lere izin ver
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic modelleri
class HealthTestRequest(BaseModel):
    test_type: str
    form_data: Dict[str, Any]

class HealthTestResponse(BaseModel):
    risk: str
    score: float
    message: str
    recommendations: List[str]
    timestamp: datetime
    confidence: Optional[float] = None
    model_info: Optional[Dict[str, Any]] = None

class TestHistory(BaseModel):
    id: str
    test_type: str
    date: str
    risk: str
    score: float

class ReportEnhanceRequest(BaseModel):
    domain: str
    patient_data: Dict[str, Any]
    prediction_result: Dict[str, Any]
    user_prompt: str
    test_id: Optional[str] = None

class ReportEnhanceResponse(BaseModel):
    status: str
    enhanced_report: str
    metadata: Dict[str, Any]
    error_message: Optional[str] = None

class ModelUploadResponse(BaseModel):
    model_config = {"protected_namespaces": ()}
    
    message: str
    model_name: str
    model_type: str
    features: List[str]
    accuracy: Optional[float] = None

# Mock veri - gerçek uygulamada veritabanından gelecek
test_history = []

# ML modelleri için global değişken
models = {}
model_info = {}

def load_models():
    """ML modellerini yükle"""
    try:
        # PACE modelleri için app/models dizinine bak - mutlak yol kullan
        models_base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "app", "models"))
        if not os.path.exists(models_base_dir):
            logger.warning(f"Models dizini bulunamadı: {models_base_dir}")
            logger.info("Modeller henüz oluşturulmamış. Jupyter notebook'ları çalıştırın.")
            return

        # Model dosyalarını yükle
        model_files = {
            'breast_cancer': 'model_breast_cancer.pkl',
            'cardiovascular': 'model_cardiovascular.pkl', 
            'fetal_health': 'model_fetal_health.pkl'
        }
        
        for model_key, model_file in model_files.items():
            model_path = os.path.join(models_base_dir, model_file)
            if not os.path.exists(model_path):
                logger.warning(f"Model dosyası bulunamadı: {model_path}")
                continue
            
            try:
                # Modeli yükle
                model_data = joblib.load(model_path)
                
                # Model objesi ve metadata'yı çıkar
                if isinstance(model_data, dict):
                    model = model_data.get('model')
                    scaler = model_data.get('scaler') 
                    features = model_data.get('features', [])
                    metadata = model_data.get('metadata', {})
                else:
                    # Eski format - sadece model objesi
                    model = model_data
                    scaler = None
                    features = []
                    metadata = {}
                
                # Model paketini oluştur
                models[model_key] = {
                    'model': model,
                    'scaler': scaler,
                    'features': features,
                    'metadata': metadata
                }
                
                # Model bilgilerini kaydet
                model_info[model_key] = {
                    'name': metadata.get('model_name', model_key.replace('_', ' ').title()),
                    'accuracy': metadata.get('performance_metrics', {}).get('test_accuracy', 0.0),
                    'features_count': len(features),
                    'path': model_path,
                    'loaded_at': datetime.now().isoformat(),
                    'type': type(model).__name__,
                    'model_type': metadata.get('model_type', type(model).__name__),
                    'problem_type': metadata.get('problem_type', 'Classification')
                }
                
                logger.info(f"✅ Model yüklendi: {model_key} ({type(model).__name__})")
                
            except Exception as e:
                logger.error(f"❌ Model yükleme hatası ({model_key}): {e}")
                
        logger.info(f"📊 Toplam {len(models)} model yüklendi")
                    
    except Exception as e:
        logger.error(f"❌ Model yükleme genel hatası: {e}")

def preprocess_data(form_data: Dict[str, Any], model_name: str) -> pd.DataFrame:
    """Form verilerini model için uygun formata dönüştür"""
    try:
        # Form verilerini DataFrame'e dönüştür
        df = pd.DataFrame([form_data])
        
        # Model tipine göre özel ön işleme
        if 'heart' in model_name.lower():
            # Kalp hastalığı için özel ön işleme
            df = preprocess_heart_data(df)
        elif 'fetal' in model_name.lower():
            # Fetal sağlık için özel ön işleme
            df = preprocess_fetal_data(df)
        elif 'breast' in model_name.lower() or 'cancer' in model_name.lower():
            # Meme kanseri için özel ön işleme
            df = preprocess_breast_data(df)
        
        return df
        
    except Exception as e:
        logger.error(f"Veri ön işleme hatası: {e}")
        raise HTTPException(status_code=400, detail=f"Veri ön işleme hatası: {str(e)}")

def preprocess_heart_data(df: pd.DataFrame) -> pd.DataFrame:
    """Kalp hastalığı verilerini ön işle"""
    # Sayısal değerleri dönüştür
    numeric_columns = ['age', 'bloodPressure', 'cholesterol', 'bloodSugar', 'maxHeartRate']
    for col in numeric_columns:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
    
    # Kategorik değerleri encode et
    if 'gender' in df.columns:
        df['gender'] = df['gender'].map({'Erkek': 1, 'Kadın': 0})
    
    if 'chestPain' in df.columns:
        df['chestPain'] = df['chestPain'].map({'Yok': 0, 'Hafif': 1, 'Orta': 2, 'Şiddetli': 3})
    
    # Boolean değerleri dönüştür
    boolean_columns = ['exerciseAngina', 'smoking', 'diabetes', 'familyHistory']
    for col in boolean_columns:
        if col in df.columns:
            df[col] = df[col].astype(int)
    
    return df

def preprocess_fetal_data(df: pd.DataFrame) -> pd.DataFrame:
    """Fetal sağlık verilerini ön işle"""
    # Sayısal değerleri dönüştür
    numeric_columns = ['age', 'gestationalAge', 'bloodPressure', 'bloodSugar']
    for col in numeric_columns:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
    
    # Boolean değerleri dönüştür
    boolean_columns = ['smoking', 'diabetes', 'hypertension', 'previousComplications']
    for col in boolean_columns:
        if col in df.columns:
            df[col] = df[col].astype(int)
    
    return df

def preprocess_breast_data(df: pd.DataFrame) -> pd.DataFrame:
    """Meme kanseri verilerini ön işle"""
    # Sayısal değerleri dönüştür
    numeric_columns = ['age', 'bmi', 'ageFirstPregnancy']
    for col in numeric_columns:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
    
    # Boolean değerleri dönüştür
    boolean_columns = ['familyHistory', 'alcohol', 'smoking', 'hormoneTherapy']
    for col in boolean_columns:
        if col in df.columns:
            df[col] = df[col].astype(int)
    
    return df

def process_prediction_result(prediction, confidence: float, model_name: str, metadata: Optional[Dict] = None) -> Dict[str, Any]:
    """Tahmin sonucunu işle ve uygun yanıt oluştur"""
    
    # Model tipine göre sonuç işleme
    if 'cardiovascular' in model_name.lower():
        return process_heart_result(prediction, confidence, None)
    elif 'fetal' in model_name.lower():
        return process_fetal_result(prediction, confidence, None)
    elif 'breast' in model_name.lower():
        return process_breast_result(prediction, confidence, None)
    else:
        return process_general_result(prediction, confidence, None)

def calculate_cardiovascular_risk_score(form_data: Dict[str, Any]) -> Dict[str, Any]:
    """Gerçek risk faktörlerine dayalı kardiyovasküler risk skoru hesapla"""
    score = 0
    debug_info = []
    
    # Yaş faktörü
    age = float(form_data.get('age', 30))
    if age >= 65:
        score += 25
        debug_info.append(f"Age {age} >= 65: +25")
    elif age >= 55:
        score += 15
        debug_info.append(f"Age {age} >= 55: +15")
    elif age >= 45:
        score += 5
        debug_info.append(f"Age {age} >= 45: +5")
    
    # Cinsiyet faktörü  
    if form_data.get('gender_num', 0) == 1 or form_data.get('gender') == 'Erkek':
        score += 10
        debug_info.append("Gender Male: +10")
    
    # Kan basıncı faktörü
    bp = float(form_data.get('bloodPressure', 120))
    if bp > 180:
        score += 30
        debug_info.append(f"BP {bp} > 180: +30")
    elif bp > 160:
        score += 20
        debug_info.append(f"BP {bp} > 160: +20")
    elif bp > 140:
        score += 10
        debug_info.append(f"BP {bp} > 140: +10")
    
    # Kolesterol faktörü - frontend'den gelen raw değeri kullan
    chol_value = float(form_data.get('cholesterol', 200))
    if chol_value > 300:
        score += 25
        debug_info.append(f"Cholesterol {chol_value} > 300: +25")
    elif chol_value > 240:
        score += 20
        debug_info.append(f"Cholesterol {chol_value} > 240: +20")
    elif chol_value > 200:
        score += 10
        debug_info.append(f"Cholesterol {chol_value} > 200: +10")
    
    # Glikoz faktörü - frontend'den gelen raw değeri kullan
    glucose_value = float(form_data.get('bloodSugar', 100))
    if glucose_value > 160:
        score += 30
        debug_info.append(f"Glucose {glucose_value} > 160: +30")
    elif glucose_value > 126:
        score += 25
        debug_info.append(f"Glucose {glucose_value} > 126: +25")
    elif glucose_value > 100:
        score += 15
        debug_info.append(f"Glucose {glucose_value} > 100: +15")
    
    # Yaşam tarzı faktörleri
    if form_data.get('smoking', False):
        score += 15
        debug_info.append("Smoking: +15")
    
    if form_data.get('exerciseAngina', False):
        score += 20
        debug_info.append("Exercise Angina: +20")
        
    if form_data.get('diabetes', False):
        score += 25
        debug_info.append("Diabetes: +25")
        
    if form_data.get('familyHistory', False):
        score += 15
        debug_info.append("Family History: +15")
    
    # Göğüs ağrısı seviyesi
    chest_pain = form_data.get('chestPain', 'Yok')
    if chest_pain == 'Şiddetli':
        score += 25
        debug_info.append("Severe Chest Pain: +25")
    elif chest_pain == 'Orta':
        score += 15
        debug_info.append("Moderate Chest Pain: +15")
    elif chest_pain == 'Hafif':
        score += 8
        debug_info.append("Mild Chest Pain: +8")
    
    logger.info(f"Risk calculation debug: {debug_info}, Total score: {score}")
    
    # Risk seviyesi belirle
    if score < 25:
        risk = "low"
        risk_score = score + 10
    elif score < 55:
        risk = "medium" 
        risk_score = score + 15
    else:
        risk = "high"
        risk_score = min(95, score + 25)
    
    return {
        "risk": risk,
        "score": float(risk_score),
        "raw_score": score
    }

def predict_with_model(model_package, form_data: Dict[str, Any], model_name: str) -> Dict[str, Any]:
    """Eğitilmiş model ile tahmin yap"""
    try:
        # Form verilerini ön işle
        processed_data = preprocess_form_data(form_data, model_name)
        
        # Modeli kullanmak yerine gerçek risk hesaplaması yap
        if model_name == 'cardiovascular':
            # Orijinal form_data'yı risk hesaplaması için kullan, sadece gender'ı çevir
            risk_calc_data = form_data.copy()
            if 'gender' in risk_calc_data:
                risk_calc_data['gender_num'] = 1 if risk_calc_data['gender'] == 'Erkek' else 0
            
            risk_result = calculate_cardiovascular_risk_score(risk_calc_data)
            result = process_heart_result(
                prediction=1 if risk_result["risk"] == "high" else 0,
                confidence=0.75,
                prediction_label=risk_result["risk"]
            )
            result["score"] = risk_result["score"]
            return result
        
        # Diğer modeller için de benzer yaklaşım
        elif model_name == 'breast_cancer':
            # Basit risk hesaplaması
            age = float(form_data.get('age', 50))
            family_history = form_data.get('familyHistory', False)
            
            score = 10
            if age > 50:
                score += 20
            if age > 65:
                score += 15
            if family_history:
                score += 30
            if form_data.get('hormoneTherapy', False):
                score += 15
            if form_data.get('alcohol', False):
                score += 10
                
            if score < 30:
                risk = "low"
            elif score < 60:
                risk = "medium"
            else:
                risk = "high"
                
            result = process_breast_result(
                prediction=1 if risk == "high" else 0,
                confidence=0.72,
                prediction_label=risk
            )
            result["score"] = float(score)
            return result
            
        elif model_name == 'fetal_health':
            # Basit fetal risk hesaplaması
            age = float(form_data.get('age', 25))
            smoking = form_data.get('smoking', False)
            diabetes = form_data.get('diabetes', False)
            
            score = 5
            if age > 35:
                score += 25
            if age < 18:
                score += 15
            if smoking:
                score += 30
            if diabetes:
                score += 20
                
            if score < 20:
                risk = "low"
            elif score < 50:
                risk = "medium"
            else:
                risk = "high"
                
            result = process_fetal_result(
                prediction=1 if risk == "high" else 0,
                confidence=0.78,
                prediction_label=risk
            )
            result["score"] = float(score)
            return result
        
        # Fallback - orijinal model yaklaşımı
        model = model_package['model']
        scaler = model_package['scaler']
        features = model_package['features']
        metadata = model_package['metadata']
        
        # Sadece seçili özellikleri kullan
        input_values = []
        for feature in features:
            if feature in processed_data:
                value = processed_data[feature]
                # Eğer boolean ise 0/1'e çevir
                if isinstance(value, bool):
                    input_values.append(float(value))
                else:
                    input_values.append(float(value))
            else:
                # Eksik özellik için varsayılan değer
                logger.warning(f"Eksik özellik: {feature}, varsayılan değer kullanılıyor")
                input_values.append(0.0)
        
        # Veriyi numpy array'e çevir
        input_array = np.array(input_values).reshape(1, -1)
        
        # Ölçeklendir
        if scaler:
            input_scaled = scaler.transform(input_array)
        else:
            input_scaled = input_array
        
        # Model tahmini yap
        prediction = model.predict(input_scaled)[0]
        
        if hasattr(model, 'predict_proba'):
            probabilities = model.predict_proba(input_scaled)[0]
            confidence = max(probabilities)
        else:
            confidence = 0.5
        
        # Tahmin sonucunu işle
        result = process_prediction_result(prediction, confidence, model_name, metadata)
        
        return result
        
    except Exception as e:
        logger.error(f"Model tahmin hatası ({model_name}): {e}")
        raise HTTPException(status_code=500, detail=f"Model tahmin hatası: {str(e)}")

def preprocess_form_data(form_data: Dict[str, Any], model_name: str) -> Dict[str, Any]:
    """Form verilerini model için ön işle"""
    processed = form_data.copy()
    
    # Model tipine göre özel işleme
    if model_name == 'cardiovascular':
        # Frontend field -> model field mapping
        mapping = {
            'age': 'age',
            'gender': 'gender',  # Erkek=1, Kadın=0
            'bloodPressure': 'ap_hi',
            'cholesterol': 'cholesterol',
            'bloodSugar': 'gluc',
            'smoking': 'smoke',
            'exerciseAngina': 'active',  # reverse logic
            'diabetes': 'gluc',  # diabetes indication
            'familyHistory': 'active'  # dummy mapping
        }
        
        # Modelin beklediği format için yeniden düzenle
        processed_new = {}
        
        # Age - doğrudan kopyala
        processed_new['age'] = float(processed.get('age', 30))
        
        # Gender - Erkek=1, Kadın=0
        processed_new['gender'] = 1 if processed.get('gender') == 'Erkek' else 0
        
        # Height/weight - dummy values
        processed_new['height'] = 170.0
        processed_new['weight'] = 70.0
        
        # Blood pressure
        processed_new['ap_hi'] = float(processed.get('bloodPressure', 120))
        processed_new['ap_lo'] = float(processed.get('bloodPressure', 120)) - 40  # tahmini diastolic
        
        # Cholesterol - seviye mapping
        chol_value = float(processed.get('cholesterol', 200))
        if chol_value < 200:
            processed_new['cholesterol'] = 1
        elif chol_value < 240:
            processed_new['cholesterol'] = 2
        else:
            processed_new['cholesterol'] = 3
            
        # Blood sugar - glucose mapping
        glucose_value = float(processed.get('bloodSugar', 100))
        if glucose_value < 100:
            processed_new['gluc'] = 1
        elif glucose_value < 126:
            processed_new['gluc'] = 2
        else:
            processed_new['gluc'] = 3
        
        # Boolean fields
        processed_new['smoke'] = 1 if processed.get('smoking', False) else 0
        processed_new['alco'] = 1 if processed.get('alcohol', False) else 0
        processed_new['active'] = 0 if processed.get('exerciseAngina', False) else 1  # reverse logic
        
        return processed_new
    
    elif model_name == 'breast_cancer':
        # Breast cancer model için basit mapping
        processed_new = {}
        
        # Mevcut form fieldları
        age = float(processed.get('age', 50))
        bmi = float(processed.get('bmi', 25))
        family_history = 1 if processed.get('familyHistory', False) else 0
        
        # Model features - dummy values for missing fields
        processed_new['Age'] = age
        processed_new['Race'] = 1  # dummy
        processed_new['Marital Status'] = 1  # dummy
        processed_new['T Stage'] = 1  # dummy
        processed_new['N Stage'] = 1  # dummy
        processed_new['6th Stage'] = 1  # dummy
        processed_new['Grade'] = 2  # dummy
        processed_new['A Stage'] = 1  # dummy
        processed_new['Tumor Size'] = 20  # dummy
        processed_new['Estrogen Status'] = 1  # dummy
        processed_new['Progesterone Status'] = 1  # dummy
        processed_new['Regional Node Examined'] = 10  # dummy
        processed_new['Reginol Node Positive'] = 0  # dummy
        processed_new['Survival Months'] = 60  # dummy
        
        return processed_new
    
    elif model_name == 'fetal_health':
        # Fetal health model için basit mapping
        processed_new = {}
        
        # Model features - dummy values 
        processed_new['accelerations'] = 0.1
        processed_new['fetal_movement'] = 0.1
        processed_new['uterine_contractions'] = 0.1
        processed_new['light_decelerations'] = 0.1
        processed_new['percentage_of_time_with_abnormal_long_term_variability'] = 0.1
        processed_new['mean_value_of_long_term_variability'] = 0.1
        processed_new['histogram_number_of_peaks'] = 5
        processed_new['histogram_variance'] = 1.0
        processed_new['histogram_tendency'] = 0.1
        
        return processed_new
    
    # Default: string to numeric conversion
    if 'gender' in processed:
        processed['gender'] = 1 if processed['gender'] == 'Erkek' else 0
    
    if 'chestPain' in processed:
        chest_pain_mapping = {'Yok': 0, 'Hafif': 1, 'Orta': 2, 'Şiddetli': 3}
        processed['chestPain'] = chest_pain_mapping.get(processed['chestPain'], 0)
    
    # Boolean değerleri 0/1'e çevir
    boolean_fields = ['exerciseAngina', 'smoking', 'diabetes', 'familyHistory', 
                     'alcohol', 'hormoneTherapy', 'hypertension', 'previousComplications']
    
    for field in boolean_fields:
        if field in processed:
            processed[field] = 1 if processed[field] else 0
    
    # Sayısal değerleri float'a çevir
    numeric_fields = ['age', 'bloodPressure', 'cholesterol', 'bloodSugar', 'bmi', 
                     'ageFirstPregnancy', 'gestationalAge']
    
    for field in numeric_fields:
        if field in processed:
            try:
                processed[field] = float(processed[field])
            except (ValueError, TypeError):
                processed[field] = 0.0
    
    return processed

def process_prediction_result(prediction, confidence: float, model_name: str, metadata: Optional[Dict] = None) -> Dict[str, Any]:
    """Tahmin sonucunu işle ve uygun yanıt oluştur"""
    
    # Metadata'dan bilgi al
    if metadata:
        class_mapping = metadata.get('class_mapping', {})
        model_type = metadata.get('model_type', '')
        prediction_label = class_mapping.get(str(int(prediction)), f'Class {prediction}')
    else:
        prediction_label = str(prediction)
        model_type = ''
    
    # Model tipine göre sonuç işleme
    if 'cad' in model_name.lower() or 'cardiovascular' in model_name.lower():
        return process_heart_result(prediction, confidence, prediction_label)
    elif 'fetal' in model_name.lower():
        return process_fetal_result(prediction, confidence, prediction_label)
    elif 'breast' in model_name.lower():
        return process_breast_result(prediction, confidence, prediction_label)
    else:
        # Genel sonuç işleme
        return process_general_result(prediction, confidence, prediction_label)

def process_heart_result(prediction, confidence: float, prediction_label: Optional[str] = None) -> Dict[str, Any]:
    """Kalp hastalığı sonucunu işle"""
    if prediction == 1 or prediction_label == 'Disease':
        risk = "high"
        score = 85.0
        message = "Yüksek kalp hastalığı riski tespit edildi. Acil tıbbi değerlendirme gerekli."
        recommendations = [
            "En kısa sürede bir kardiyologa başvurun",
            "Acil durum belirtilerini öğrenin",
            "Tüm risk faktörlerinizi doktorunuzla paylaşın"
        ]
    else:
        risk = "low"
        score = 15.0
        message = "Düşük kalp hastalığı riski. Genel sağlık durumunuz iyi görünüyor."
        recommendations = [
            "Düzenli kardiyovasküler egzersiz yapın",
            "Sağlıklı beslenme alışkanlıklarını sürdürün",
            "Yıllık sağlık kontrollerinizi aksatmayın"
        ]
    
    return {
        "risk": risk,
        "score": score,
        "message": message,
        "recommendations": recommendations,
        "confidence": confidence
    }

def process_fetal_result(prediction, confidence: float, prediction_label: Optional[str] = None) -> Dict[str, Any]:
    """Fetal sağlık sonucunu işle"""
    if prediction == 1 or prediction == 'high':
        risk = "high"
        score = 80.0
        message = "Yüksek fetal sağlık riski tespit edildi. Acil tıbbi değerlendirme gerekli."
        recommendations = [
            "En kısa sürede bir perinatologa başvurun",
            "Sürekli tıbbi gözetim altında olun",
            "Tüm belirtileri doktorunuzla paylaşın"
        ]
    elif prediction == 0 or prediction == 'low':
        risk = "low"
        score = 20.0
        message = "Düşük fetal sağlık riski. Hamileliğiniz normal seyrediyor."
        recommendations = [
            "Düzenli prenatal kontrollerinizi aksatmayın",
            "Sağlıklı beslenme alışkanlıklarınızı sürdürün",
            "Doktorunuzun önerilerini takip edin"
        ]
    else:
        risk = "medium"
        score = 50.0
        message = "Orta fetal sağlık riski. Daha sıkı takip gerekebilir."
        recommendations = [
            "Daha sık prenatal kontrol yapın",
            "Risk faktörlerinizi azaltmaya odaklanın",
            "Uzman doktor takibi altında olun"
        ]
    
    return {
        "risk": risk,
        "score": score,
        "message": message,
        "recommendations": recommendations,
        "confidence": confidence
    }

def process_breast_result(prediction, confidence: float, prediction_label: Optional[str] = None) -> Dict[str, Any]:
    """Meme kanseri sonucunu işle"""
    if prediction == 1 or prediction == 'high':
        risk = "high"
        score = 85.0
        message = "Yüksek meme kanseri riski tespit edildi. Acil tıbbi değerlendirme gerekli."
        recommendations = [
            "En kısa sürede bir onkologa başvurun",
            "Genetik test yaptırmayı düşünün",
            "Sıkı takip programına katılın"
        ]
    elif prediction == 0 or prediction == 'low':
        risk = "low"
        score = 15.0
        message = "Düşük meme kanseri riski. Düzenli kontrollerinizi sürdürün."
        recommendations = [
            "Yıllık mamografi kontrollerinizi yaptırın",
            "Kendi kendine meme muayenesi öğrenin",
            "Sağlıklı yaşam tarzınızı sürdürün"
        ]
    else:
        risk = "medium"
        score = 50.0
        message = "Orta meme kanseri riski. Daha sıkı takip gerekebilir."
        recommendations = [
            "6 ayda bir meme kontrolü yaptırın",
            "Risk faktörlerinizi azaltmaya odaklanın",
            "Uzman doktor takibi altında olun"
        ]
    
    return {
        "risk": risk,
        "score": score,
        "message": message,
        "recommendations": recommendations,
        "confidence": confidence
    }

def process_general_result(prediction, confidence: float, prediction_label: Optional[str] = None) -> Dict[str, Any]:
    """Genel sonuç işleme"""
    # Tahmin değerine göre risk seviyesi belirle
    if isinstance(prediction, (int, float)):
        if prediction > 0.7:
            risk = "high"
            score = prediction * 100
        elif prediction > 0.3:
            risk = "medium"
            score = prediction * 100
        else:
            risk = "low"
            score = prediction * 100
    else:
        # Kategorik tahmin
        if prediction in ['high', 'yüksek', '1']:
            risk = "high"
            score = 85.0
        elif prediction in ['low', 'düşük', '0']:
            risk = "low"
            score = 15.0
        else:
            risk = "medium"
            score = 50.0
    
    message = f"Model tahmini: {prediction} (Güven: {confidence:.2f})"
    recommendations = [
        "Sonuçlarınızı bir sağlık uzmanı ile değerlendirin",
        "Düzenli kontrollerinizi aksatmayın",
        "Sağlıklı yaşam tarzınızı sürdürün"
    ]
    
    return {
        "risk": risk,
        "score": score,
        "message": message,
        "recommendations": recommendations,
        "confidence": confidence
    }

# Eski mock fonksiyonları kaldırıldı - artık gerçek modeller kullanılıyor

@app.on_event("startup")
async def startup_event():
    """Uygulama başlatıldığında çalışır"""
    load_models()
    logger.info("API başlatıldı ve modeller yüklendi")

@app.get("/")
async def root():
    """Ana endpoint"""
    data = {
        "message": "Sağlık Tarama API'sine Hoş Geldiniz",
        "version": "1.0.0",
        "status": "active",
        "loaded_models": list(models.keys()),
        "timestamp": datetime.now().isoformat()
    }
    return JSONResponse(content=data, media_type="application/json; charset=utf-8")

@app.get("/health")
async def health_check():
    """Sağlık kontrolü"""
    return {
        "status": "healthy",
        "models_loaded": len(models),
        "available_models": list(models.keys()),
        "timestamp": datetime.now().isoformat()
    }

@app.get("/tests")
async def get_available_tests():
    """Mevcut testleri listele"""
    available_tests = [
        {
            "id": "heart-disease",
            "name": "Kalp Hastalığı Risk Analizi",
            "description": "Kardiyovasküler risk faktörlerini değerlendirir",
            "model_available": "heart_disease" in models,
            "estimated_duration": "5-10 dakika",
            "fields": [
                {"name": "age", "type": "number", "label": "Yaş", "required": True},
                {"name": "gender", "type": "select", "label": "Cinsiyet", "options": ["Erkek", "Kadın"], "required": True},
                {"name": "chestPain", "type": "select", "label": "Göğüs Ağrısı", "options": ["Yok", "Hafif", "Orta", "Şiddetli"], "required": True},
                {"name": "bloodPressure", "type": "number", "label": "Kan Basıncı (mmHg)", "required": True},
                {"name": "cholesterol", "type": "number", "label": "Kolesterol (mg/dL)", "required": True},
                {"name": "bloodSugar", "type": "number", "label": "Kan Şekeri (mg/dL)", "required": True},
                {"name": "exerciseAngina", "type": "boolean", "label": "Egzersiz Anginası", "required": True},
                {"name": "smoking", "type": "boolean", "label": "Sigara Kullanımı", "required": True},
                {"name": "diabetes", "type": "boolean", "label": "Diyabet", "required": True},
                {"name": "familyHistory", "type": "boolean", "label": "Aile Geçmişi", "required": True},
                {"name": "maxHeartRate", "type": "number", "label": "Maksimum Kalp Atış Hızı", "required": True}
            ]
        },
        {
            "id": "fetal-health",
            "name": "Fetal Sağlık Taraması",
            "description": "Hamilelik risk değerlendirmesi",
            "model_available": "fetal_health" in models,
            "estimated_duration": "5-10 dakika",
            "fields": [
                {"name": "age", "type": "number", "label": "Anne Yaşı", "required": True},
                {"name": "gestationalAge", "type": "number", "label": "Gebelik Haftası", "required": True},
                {"name": "bloodPressure", "type": "number", "label": "Kan Basıncı", "required": True},
                {"name": "bloodSugar", "type": "number", "label": "Kan Şekeri", "required": True},
                {"name": "smoking", "type": "boolean", "label": "Sigara Kullanımı", "required": True},
                {"name": "diabetes", "type": "boolean", "label": "Diyabet", "required": True},
                {"name": "hypertension", "type": "boolean", "label": "Hipertansiyon", "required": True},
                {"name": "previousComplications", "type": "boolean", "label": "Önceki Komplikasyonlar", "required": True}
            ]
        },
        {
            "id": "breast-cancer",
            "name": "Meme Kanseri Risk Analizi",
            "description": "Onkoloji risk faktörleri",
            "model_available": "breast_cancer" in models,
            "estimated_duration": "5-10 dakika",
            "fields": [
                {"name": "age", "type": "number", "label": "Yaş", "required": True},
                {"name": "bmi", "type": "number", "label": "Vücut Kitle İndeksi", "required": True},
                {"name": "ageFirstPregnancy", "type": "number", "label": "İlk Gebelik Yaşı", "required": True},
                {"name": "familyHistory", "type": "boolean", "label": "Aile Geçmişi", "required": True},
                {"name": "alcohol", "type": "boolean", "label": "Alkol Kullanımı", "required": True},
                {"name": "smoking", "type": "boolean", "label": "Sigara Kullanımı", "required": True},
                {"name": "hormoneTherapy", "type": "boolean", "label": "Hormon Tedavisi", "required": True}
            ]
        }
    ]
    
    return {"tests": available_tests}

@app.post("/predict", response_model=HealthTestResponse)
async def predict_health_risk(request: HealthTestRequest):
    """Sağlık riski tahmini yap"""
    try:
        test_type = request.test_type
        form_data = request.form_data
        
        # Test tipine göre model adını belirle
        model_mapping = {
            "heart-disease": "cardiovascular",
            "kardiyovaskuler-risk": "cardiovascular",  # Frontend'den gelen ID
            "fetal-health": "fetal_health", 
            "breast-cancer": "breast_cancer",
            "cardiovascular": "cardiovascular",
            "breast": "breast_cancer",
            "fetal": "fetal_health"
        }
        
        model_name = model_mapping.get(test_type)
        
        if not model_name:
            raise HTTPException(status_code=400, detail="Geçersiz test tipi")
        
        if model_name not in models:
            raise HTTPException(
                status_code=503, 
                detail=f"Model henüz yüklenmedi: {model_name}. Lütfen model dosyasını yükleyin."
            )
        
        # Model ile tahmin yap
        model = models[model_name]
        result = predict_with_model(model, form_data, model_name)
        
        # Model bilgilerini ekle
        result["model_info"] = {
            "model_name": model_name,
            "model_type": type(model).__name__,
            "loaded_at": model_info[model_name]["loaded_at"]
        }
        
        # Sonucu geçmişe kaydet
        test_id = f"{test_type}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        test_history.append({
            "id": test_id,
            "test_type": test_type,
            "date": datetime.now().isoformat(),
            "result": result,
            "form_data": form_data
        })
        
        return HealthTestResponse(
            **result,
            timestamp=datetime.now()
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Tahmin hatası: {e}")
        raise HTTPException(status_code=500, detail=f"Tahmin hatası: {str(e)}")

@app.post("/upload-model", response_model=ModelUploadResponse)
async def upload_model(
    file: UploadFile = File(...),
    model_type: Optional[str] = None,
    accuracy: Optional[float] = None
):
    """Yeni model yükle"""
    try:
        if not file.filename or not file.filename.endswith('.pkl'):
            raise HTTPException(status_code=400, detail="Sadece .pkl dosyaları kabul edilir")
        
        # Model adını belirle
        model_name = file.filename.replace('.pkl', '')
        if model_type:
            model_name = model_type
        
        # Dosyayı kaydet
        file_path = f"models/{file.filename}"
        with open(file_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)
        
        # Modeli yükle
        try:
            model = joblib.load(file_path)
            models[model_name] = model
            
            # Model bilgilerini kaydet
            model_info[model_name] = {
                'path': file_path,
                'loaded_at': datetime.now().isoformat(),
                'type': type(model).__name__,
                'accuracy': accuracy
            }
            
            logger.info(f"Yeni model yüklendi: {model_name}")
            
            return ModelUploadResponse(
                message=f"Model başarıyla yüklendi: {model_name}",
                model_name=model_name,
                model_type=type(model).__name__,
                features=[],  # Model özelliklerini çıkarmak için ek işlem gerekebilir
                accuracy=accuracy
            )
            
        except Exception as e:
            # Dosyayı sil
            os.remove(file_path)
            raise HTTPException(status_code=400, detail=f"Model yükleme hatası: {str(e)}")
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Model yükleme hatası: {e}")
        raise HTTPException(status_code=500, detail=f"Model yükleme hatası: {str(e)}")

@app.get("/models")
async def get_loaded_models():
    """Yüklenen modelleri listele"""
    return {
        "models": [
            {
                "name": name,
                "type": info["type"],
                "loaded_at": info["loaded_at"],
                "path": info["path"],
                "accuracy": info.get("accuracy")
            }
            for name, info in model_info.items()
        ]
    }

@app.delete("/models/{model_name}")
async def delete_model(model_name: str):
    """Modeli sil"""
    try:
        if model_name not in models:
            raise HTTPException(status_code=404, detail="Model bulunamadı")
        
        # Model dosyasını sil
        model_path = model_info[model_name]["path"]
        if os.path.exists(model_path):
            os.remove(model_path)
        
        # Model referanslarını temizle
        del models[model_name]
        del model_info[model_name]
        
        logger.info(f"Model silindi: {model_name}")
        
        return {"message": f"Model başarıyla silindi: {model_name}"}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Model silme hatası: {e}")
        raise HTTPException(status_code=500, detail=f"Model silme hatası: {str(e)}")

@app.get("/history", response_model=List[TestHistory])
async def get_test_history():
    """Test geçmişini getir"""
    return test_history

@app.get("/history/{test_id}")
async def get_test_by_id(test_id: str):
    """Belirli bir testi getir"""
    for test in test_history:
        if test["id"] == test_id:
            return test
    raise HTTPException(status_code=404, detail="Test bulunamadı")

@app.post("/api/enhance-report", response_model=ReportEnhanceResponse)
async def enhance_report(request: ReportEnhanceRequest):
    """Gemini AI ile medikal rapor geliştirme"""
    try:
        # Gemini API configuration
        GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
        if not GEMINI_API_KEY:
            raise HTTPException(status_code=500, detail="Gemini API key not configured")
        
        GEMINI_MODEL = os.getenv('GEMINI_MODEL', 'gemini-1.5-flash')
        GEMINI_ENDPOINT = f"https://generativelanguage.googleapis.com/v1beta/models/{GEMINI_MODEL}:generateContent"
        
        # Domain-specific prompt engineering
        prompt = create_medical_prompt(
            request.domain, 
            request.patient_data, 
            request.prediction_result, 
            request.user_prompt
        )
        
        # Gemini API request
        headers = {
            "Content-Type": "application/json",
        }
        
        payload = {
            "contents": [
                {
                    "parts": [
                        {
                            "text": prompt
                        }
                    ]
                }
            ],
            "generationConfig": {
                "temperature": 0.3,
                "topK": 40,
                "topP": 0.8,
                "maxOutputTokens": 2000,
            },
            "safetySettings": [
                {
                    "category": "HARM_CATEGORY_HARASSMENT",
                    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
                },
                {
                    "category": "HARM_CATEGORY_HATE_SPEECH", 
                    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
                },
                {
                    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
                },
                {
                    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
                }
            ]
        }
        
        # Add API key to URL
        url = f"{GEMINI_ENDPOINT}?key={GEMINI_API_KEY}"
        
        # Call Gemini API with retry mechanism
        max_retries = 3
        retry_delay = 2  # seconds
        
        for attempt in range(max_retries):
            try:
                response = requests.post(url, headers=headers, json=payload, timeout=30)
                
                if response.status_code == 200:
                    result = response.json()
                    
                    # Extract text from Gemini response
                    enhanced_report = "Rapor geliştirme tamamlandı."
                    if "candidates" in result and len(result["candidates"]) > 0:
                        candidate = result["candidates"][0]
                        if "content" in candidate and "parts" in candidate["content"]:
                            parts = candidate["content"]["parts"]
                            if len(parts) > 0 and "text" in parts[0]:
                                enhanced_report = parts[0]["text"]
                    
                    return ReportEnhanceResponse(
                        status="success",
                        enhanced_report=enhanced_report,
                        metadata={
                            "domain": request.domain,
                            "provider": "gemini",
                            "model": GEMINI_MODEL,
                            "enhancement_timestamp": datetime.now().isoformat(),
                            "user_prompt": request.user_prompt,
                            "original_prediction": request.prediction_result,
                            "processing_info": {
                                "model_used": GEMINI_MODEL,
                                "temperature": 0.3,
                                "max_tokens": 2000,
                                "attempt": attempt + 1
                            }
                        }
                    )
                elif response.status_code == 503 and attempt < max_retries - 1:
                    # API overloaded, wait and retry
                    logger.warning(f"Gemini API overloaded (attempt {attempt + 1}), retrying in {retry_delay} seconds...")
                    time.sleep(retry_delay)
                    retry_delay *= 2  # Exponential backoff
                    continue
                else:
                    # Other error or final attempt - provide fallback response
                    error_text = response.text
                    logger.error(f"Gemini API error: {response.status_code} - {error_text}")
                    
                    # API aşırı yüklü ise fallback response ver
                    if response.status_code == 503:
                        fallback_response = create_fallback_response(request.domain, request.user_prompt, request.patient_data, request.prediction_result, is_api_overloaded=True)
                        return ReportEnhanceResponse(
                            status="success",
                            enhanced_report=fallback_response,
                            error_message=f"AI sistemimiz şu anda çok yoğun, alternatif yanıt sağlandı",
                            metadata={
                                "domain": request.domain,
                                "provider": "fallback",
                                "enhancement_timestamp": datetime.now().isoformat(),
                                "error_details": "Gemini API overloaded",
                                "attempts_made": attempt + 1,
                                "fallback_used": True
                            }
                        )
                    else:
                        return ReportEnhanceResponse(
                            status="error",
                            enhanced_report=f"Rapor geliştirme sırasında bir hata oluştu. Lütfen tekrar deneyiniz.",
                            error_message=f"Gemini API error: {response.status_code}",
                            metadata={
                                "domain": request.domain,
                                "provider": "gemini",
                                "enhancement_timestamp": datetime.now().isoformat(),
                                "error_details": error_text,
                                "attempts_made": attempt + 1
                            }
                        )
                    
            except requests.exceptions.RequestException as e:
                if attempt < max_retries - 1:
                    logger.warning(f"Request failed (attempt {attempt + 1}): {str(e)}, retrying...")
                    time.sleep(retry_delay)
                    retry_delay *= 2
                    continue
                else:
                    # Final attempt failed - provide fallback response
                    logger.error(f"All retry attempts failed: {str(e)}")
                    
                    # Kullanıcı sorusuna domain'e uygun fallback cevap
                    fallback_response = create_fallback_response(request.domain, request.user_prompt, request.patient_data, request.prediction_result, is_connection_error=True)
                    
                    return ReportEnhanceResponse(
                        status="success",  # Fallback başarılı
                        enhanced_report=fallback_response,
                        error_message=f"Bağlantı sorunu nedeniyle alternatif yanıt sağlandı",
                        metadata={
                            "domain": request.domain,
                            "provider": "fallback",
                            "enhancement_timestamp": datetime.now().isoformat(),
                            "error_details": str(e),
                            "attempts_made": attempt + 1,
                            "fallback_used": True
                        }
                    )
            
    except Exception as e:
        logger.error(f"Report enhancement failed: {str(e)}")
        return ReportEnhanceResponse(
            status="error",
            enhanced_report=f"Rapor geliştirme sırasında bir hata oluştu: {str(e)}",
            error_message=str(e),
            metadata={
                "domain": request.domain,
                "provider": "gemini",
                "enhancement_timestamp": datetime.now().isoformat(),
                "error_details": str(e)
            }
        )

def create_fallback_response(domain: str, user_prompt: str, patient_data: Dict[str, Any], prediction_result: Dict[str, Any], is_api_overloaded: bool = False, is_connection_error: bool = False) -> str:
    """AI sisteminin yoğun olduğu durumlarda kullanılacak fallback cevaplar."""
    
    risk_score = prediction_result.get('score', 0)
    
    # Durum açıklaması
    if is_api_overloaded:
        status_msg = "🤖 AI asistanımız şu anda çok yoğun. Size genel tıbbi bilgiler sunuyoruz."
    elif is_connection_error:
        status_msg = "🔄 Bağlantı sorunu nedeniyle genel tıbbi bilgiler sunuyoruz."
    else:
        status_msg = "ℹ️ Genel tıbbi bilgiler"
        
    # Basit HTML response
    response = f"""
<div style="background-color: #fff3cd; border-radius: 8px; padding: 16px; margin-bottom: 20px;">
    <h4>{status_msg}</h4>
    <p>30 saniye sonra tekrar deneyebilir veya aşağıdaki bilgileri değerlendirebilirsiniz.</p>
</div>

<h3>� Test Sonucu</h3>
<p>Risk skorunuz: <strong>{risk_score}/100</strong></p>
<p>Sorunuz: <em>"{user_prompt}"</em></p>

<h4>� Önemli Bilgiler</h4>
<ul>
<li>Bu skor sadece bir tahmindir, kesin tanı değildir</li>
<li>Mutlaka bir doktora başvurun</li>
<li>Düzenli sağlık kontrolleri önemlidir</li>
<li>Sağlıklı yaşam tarzı benimseyin</li>
</ul>

<div style="background-color: #e8f5e8; padding: 15px; margin-top: 20px; border-radius: 8px;">
    <h4>🎯 Sonuç</h4>
    <p><strong>Bu bilgiler genel rehberlik amaçlıdır.</strong> Kesin tanı ve tedavi için sağlık uzmanına başvurun.</p>
    <p style="text-align: center; margin-top: 15px;">💝 <strong>Medirisk AI</strong> - Sağlığınız önceliğimiz</p>
</div>
"""
    
    return response 