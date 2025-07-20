from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, Any, List, Optional
import joblib
import pandas as pd
import numpy as np
from datetime import datetime
import os
import logging

# Logging ayarları
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Sağlık Tarama API",
    description="Yapay zeka destekli sağlık risk analizi API'si",
    version="1.0.0"
)

# CORS ayarları - Frontend ile iletişim için
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React uygulaması
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
    result: HealthTestResponse
    form_data: Dict[str, Any]

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
        models_dir = "models"
        if not os.path.exists(models_dir):
            os.makedirs(models_dir)
            logger.info(f"Models dizini oluşturuldu: {models_dir}")
            return

        # Models dizinindeki tüm .pkl dosyalarını yükle
        for filename in os.listdir(models_dir):
            if filename.endswith('.pkl'):
                model_path = os.path.join(models_dir, filename)
                model_name = filename.replace('.pkl', '')
                
                try:
                    model = joblib.load(model_path)
                    models[model_name] = model
                    
                    # Model bilgilerini kaydet
                    model_info[model_name] = {
                        'path': model_path,
                        'loaded_at': datetime.now().isoformat(),
                        'type': type(model).__name__
                    }
                    
                    logger.info(f"Model yüklendi: {model_name}")
                    
                except Exception as e:
                    logger.error(f"Model yükleme hatası ({model_name}): {e}")
                    
    except Exception as e:
        logger.error(f"Model yükleme genel hatası: {e}")

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
        elif 'depression' in model_name.lower():
            # Depresyon için özel ön işleme
            df = preprocess_depression_data(df)
        
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

def preprocess_depression_data(df: pd.DataFrame) -> pd.DataFrame:
    """Depresyon verilerini ön işle"""
    # Sayısal değerleri dönüştür
    numeric_columns = ['age', 'sleepHours', 'stressLevel']
    for col in numeric_columns:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
    
    # Kategorik değerleri encode et
    if 'stressLevel' in df.columns:
        df['stressLevel'] = df['stressLevel'].map({'Düşük': 1, 'Orta': 2, 'Yüksek': 3})
    
    if 'socialSupport' in df.columns:
        df['socialSupport'] = df['socialSupport'].map({'Yok': 0, 'Az': 1, 'Orta': 2, 'Yüksek': 3})
    
    # Boolean değerleri dönüştür
    boolean_columns = ['previousDepression', 'familyHistory', 'anxiety', 'insomnia']
    for col in boolean_columns:
        if col in df.columns:
            df[col] = df[col].astype(int)
    
    return df

def predict_with_model(model, form_data: Dict[str, Any], model_name: str) -> Dict[str, Any]:
    """Eğitilmiş model ile tahmin yap"""
    try:
        # Veriyi ön işle
        df = preprocess_data(form_data, model_name)
        
        # Model tahmini yap
        if hasattr(model, 'predict_proba'):
            # Olasılık tahmini varsa
            probabilities = model.predict_proba(df)
            prediction = model.predict(df)[0]
            confidence = max(probabilities[0]) if len(probabilities) > 0 else 0.5
        else:
            # Sadece sınıf tahmini
            prediction = model.predict(df)[0]
            confidence = 0.5  # Varsayılan güven skoru
        
        # Tahmin sonucunu işle
        result = process_prediction_result(prediction, confidence, model_name)
        
        return result
        
    except Exception as e:
        logger.error(f"Model tahmin hatası ({model_name}): {e}")
        raise HTTPException(status_code=500, detail=f"Model tahmin hatası: {str(e)}")

def process_prediction_result(prediction, confidence: float, model_name: str) -> Dict[str, Any]:
    """Tahmin sonucunu işle ve uygun yanıt oluştur"""
    
    # Model tipine göre sonuç işleme
    if 'heart' in model_name.lower():
        return process_heart_result(prediction, confidence)
    elif 'fetal' in model_name.lower():
        return process_fetal_result(prediction, confidence)
    elif 'breast' in model_name.lower() or 'cancer' in model_name.lower():
        return process_breast_result(prediction, confidence)
    elif 'depression' in model_name.lower():
        return process_depression_result(prediction, confidence)
    else:
        # Genel sonuç işleme
        return process_general_result(prediction, confidence)

def process_heart_result(prediction, confidence: float) -> Dict[str, Any]:
    """Kalp hastalığı sonucunu işle"""
    if prediction == 1 or prediction == 'high':
        risk = "high"
        score = 85.0
        message = "Yüksek kalp hastalığı riski tespit edildi. Acil tıbbi değerlendirme gerekli."
        recommendations = [
            "En kısa sürede bir kardiyologa başvurun",
            "Acil durum belirtilerini öğrenin",
            "Tüm risk faktörlerinizi doktorunuzla paylaşın"
        ]
    elif prediction == 0 or prediction == 'low':
        risk = "low"
        score = 15.0
        message = "Düşük kalp hastalığı riski. Genel sağlık durumunuz iyi görünüyor."
        recommendations = [
            "Düzenli kardiyovasküler egzersiz yapın",
            "Sağlıklı beslenme alışkanlıklarını sürdürün",
            "Yıllık sağlık kontrollerinizi aksatmayın"
        ]
    else:
        risk = "medium"
        score = 50.0
        message = "Orta kalp hastalığı riski. Dikkatli olmanız gereken durumlar var."
        recommendations = [
            "Bir kardiyolog ile görüşün",
            "Kan basıncınızı düzenli takip edin",
            "Kolesterol seviyelerinizi kontrol ettirin"
        ]
    
    return {
        "risk": risk,
        "score": score,
        "message": message,
        "recommendations": recommendations,
        "confidence": confidence
    }

def process_fetal_result(prediction, confidence: float) -> Dict[str, Any]:
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

def process_breast_result(prediction, confidence: float) -> Dict[str, Any]:
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

def process_depression_result(prediction, confidence: float) -> Dict[str, Any]:
    """Depresyon sonucunu işle"""
    if prediction == 1 or prediction == 'high':
        risk = "high"
        score = 80.0
        message = "Yüksek depresyon riski tespit edildi. Profesyonel yardım almanız önerilir."
        recommendations = [
            "En kısa sürede bir psikiyatriste başvurun",
            "Acil durum hatlarını öğrenin",
            "Güvenilir kişilerle duygularınızı paylaşın"
        ]
    elif prediction == 0 or prediction == 'low':
        risk = "low"
        score = 20.0
        message = "Düşük depresyon riski. Ruh sağlığınız iyi görünüyor."
        recommendations = [
            "Sosyal bağlantılarınızı güçlü tutun",
            "Düzenli egzersiz yapın",
            "Stres yönetimi tekniklerini öğrenin"
        ]
    else:
        risk = "medium"
        score = 50.0
        message = "Orta depresyon riski. Dikkatli olmanız gereken durumlar var."
        recommendations = [
            "Bir psikolog ile görüşmeyi düşünün",
            "Stres yönetimi tekniklerini uygulayın",
            "Sosyal destek ağınızı genişletin"
        ]
    
    return {
        "risk": risk,
        "score": score,
        "message": message,
        "recommendations": recommendations,
        "confidence": confidence
    }

def process_general_result(prediction, confidence: float) -> Dict[str, Any]:
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
    return {
        "message": "Sağlık Tarama API'sine Hoş Geldiniz",
        "version": "1.0.0",
        "status": "active",
        "loaded_models": list(models.keys()),
        "timestamp": datetime.now().isoformat()
    }

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
        },
        {
            "id": "depression",
            "name": "Depresyon Risk Değerlendirmesi",
            "description": "Ruh sağlığı analizi",
            "model_available": "depression" in models,
            "estimated_duration": "5-10 dakika",
            "fields": [
                {"name": "age", "type": "number", "label": "Yaş", "required": True},
                {"name": "sleepHours", "type": "number", "label": "Günlük Uyku Saati", "required": True},
                {"name": "stressLevel", "type": "select", "label": "Stres Seviyesi", "options": ["Düşük", "Orta", "Yüksek"], "required": True},
                {"name": "socialSupport", "type": "select", "label": "Sosyal Destek", "options": ["Yok", "Az", "Orta", "Yüksek"], "required": True},
                {"name": "previousDepression", "type": "boolean", "label": "Önceki Depresyon", "required": True},
                {"name": "familyHistory", "type": "boolean", "label": "Aile Geçmişi", "required": True},
                {"name": "anxiety", "type": "boolean", "label": "Anksiyete", "required": True},
                {"name": "insomnia", "type": "boolean", "label": "Uykusuzluk", "required": True}
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
            "heart-disease": "heart_disease",
            "fetal-health": "fetal_health", 
            "breast-cancer": "breast_cancer",
            "depression": "depression"
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
    model_type: str = None,
    accuracy: float = None
):
    """Yeni model yükle"""
    try:
        if not file.filename.endswith('.pkl'):
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

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 