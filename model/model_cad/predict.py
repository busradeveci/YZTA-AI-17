# 🫀 SYSTEMATIC CARDIOVASCULAR RISK PREDICTION MODEL
# 🔬 PACE Methodology Implementation for Medical Diagnosis
# 📊 Binary Classification: Healthy vs Risk (CVD)

import pandas as pd
import numpy as np
import pickle
import os
from typing import Dict, List, Any

class CardiovascularSystematicPredictor:
    """
    🫀 Systematic Cardiovascular Risk Prediction Model
    
    Based on PACE methodology:
    - Plan: Clinical parameter analysis framework
    - Analyze: Risk factor assessment
    - Construct: Binary classification model (RandomForest)
    - Execute: Real-time cardiovascular risk prediction
    """
    
    def __init__(self, model_dir=None):
        """Initialize Cardiovascular Predictor with PACE methodology."""
        if model_dir is None:
            self.model_dir = os.path.dirname(os.path.abspath(__file__))
        else:
            self.model_dir = model_dir
            
        self.model = None
        self.scaler = None
        self.feature_names = None
        self.load_models()
    
    def load_models(self):
        """Load trained cardiovascular model and preprocessing components."""
        try:
            model_path = os.path.join(self.model_dir, 'cardiovascular_model.pkl')
            if os.path.exists(model_path):
                with open(model_path, 'rb') as f:
                    self.model = pickle.load(f)
                print("✅ Cardiovascular model loaded successfully")
            else:
                print("⚠️ Model file not found, using fallback prediction")
                
        except Exception as e:
            print(f"❌ Error loading model: {e}")
            print("📝 Using rule-based prediction method")
    
    def preprocess_data(self, patient_data: Dict) -> pd.DataFrame:
        """PACE: Plan - Systematic data preprocessing for cardiovascular assessment."""
        processed_data = {
            'age': patient_data.get('age', 50),
            'gender': patient_data.get('gender', 1),  # 1=Female, 2=Male
            'height': patient_data.get('height', 170),
            'weight': patient_data.get('weight', 70),
            'ap_hi': patient_data.get('ap_hi', 120),  # Systolic BP
            'ap_lo': patient_data.get('ap_lo', 80),   # Diastolic BP
            'cholesterol': patient_data.get('cholesterol', 1),  # 1=Normal, 2=Above, 3=Well above
            'gluc': patient_data.get('gluc', 1),     # 1=Normal, 2=Above, 3=Well above
            'smoke': patient_data.get('smoke', 0),   # 0=No, 1=Yes
            'alco': patient_data.get('alco', 0),     # 0=No, 1=Yes
            'active': patient_data.get('active', 1)  # 0=No, 1=Yes
        }
        
        # BMI hesaplama
        height_m = processed_data['height'] / 100
        processed_data['bmi'] = processed_data['weight'] / (height_m ** 2)
        
        # Hipertansiyon tanımlaması
        processed_data['hypertension'] = 1 if (processed_data['ap_hi'] >= 140 or processed_data['ap_lo'] >= 90) else 0
        
        return pd.DataFrame([processed_data])
    
    def analyze_risk_factors(self, patient_data: Dict) -> List[str]:
        """PACE: Analyze - Systematic risk factor identification."""
        risk_factors = []
        
        # Yaş riski
        age = patient_data.get('age', 50)
        if age >= 65:
            risk_factors.append("Yaşlı yetişkin (≥65)")
        elif age >= 45 and patient_data.get('gender', 1) == 2:  # Male
            risk_factors.append("45+ yaş erkek")
        elif age >= 55 and patient_data.get('gender', 1) == 1:  # Female
            risk_factors.append("55+ yaş kadın")
        
        # Hipertansiyon
        ap_hi = patient_data.get('ap_hi', 120)
        ap_lo = patient_data.get('ap_lo', 80)
        if ap_hi >= 140 or ap_lo >= 90:
            risk_factors.append("Hipertansiyon")
        
        # Kolesterol
        if patient_data.get('cholesterol', 1) >= 2:
            risk_factors.append("Yüksek kolesterol")
        
        # Diyabet riski
        if patient_data.get('gluc', 1) >= 2:
            risk_factors.append("Yüksek glukoz/Diyabet")
        
        # Sigara
        if patient_data.get('smoke', 0) == 1:
            risk_factors.append("Sigara kullanımı")
        
        # Alkol
        if patient_data.get('alco', 0) == 1:
            risk_factors.append("Alkol kullanımı")
        
        # Sedanter yaşam
        if patient_data.get('active', 1) == 0:
            risk_factors.append("Sedanter yaşam")
        
        # BMI hesaplama
        height = patient_data.get('height', 170) / 100
        weight = patient_data.get('weight', 70)
        bmi = weight / (height ** 2)
        if bmi >= 30:
            risk_factors.append("Obezite (BMI≥30)")
        elif bmi >= 25:
            risk_factors.append("Fazla kilo (BMI≥25)")
        
        return risk_factors
    
    def calculate_risk_score(self, patient_data: Dict) -> float:
        """PACE: Construct - Systematic risk score calculation."""
        risk_score = 0.0
        
        # Yaş faktörü (0-25 puan)
        age = patient_data.get('age', 50)
        if age >= 65:
            risk_score += 25
        elif age >= 55:
            risk_score += 20
        elif age >= 45:
            risk_score += 15
        elif age >= 35:
            risk_score += 10
        
        # Cinsiyet faktörü (0-10 puan)
        if patient_data.get('gender', 1) == 2:  # Male
            risk_score += 10
        
        # Hipertansiyon (0-20 puan)
        ap_hi = patient_data.get('ap_hi', 120)
        ap_lo = patient_data.get('ap_lo', 80)
        if ap_hi >= 180 or ap_lo >= 110:
            risk_score += 20  # Stage 2 hypertension
        elif ap_hi >= 140 or ap_lo >= 90:
            risk_score += 15  # Stage 1 hypertension
        elif ap_hi >= 130 or ap_lo >= 80:
            risk_score += 10  # High normal
        
        # Kolesterol (0-15 puan)
        cholesterol = patient_data.get('cholesterol', 1)
        if cholesterol == 3:
            risk_score += 15
        elif cholesterol == 2:
            risk_score += 10
        
        # Glukoz (0-15 puan)
        gluc = patient_data.get('gluc', 1)
        if gluc == 3:
            risk_score += 15
        elif gluc == 2:
            risk_score += 10
        
        # Yaşam tarzı faktörleri (0-15 puan)
        if patient_data.get('smoke', 0) == 1:
            risk_score += 10
        if patient_data.get('alco', 0) == 1:
            risk_score += 5
        if patient_data.get('active', 1) == 0:
            risk_score += 5
        
        # BMI faktörü (0-10 puan)
        height = patient_data.get('height', 170) / 100
        weight = patient_data.get('weight', 70)
        bmi = weight / (height ** 2)
        if bmi >= 35:
            risk_score += 10
        elif bmi >= 30:
            risk_score += 8
        elif bmi >= 25:
            risk_score += 5
        
        return min(risk_score, 100.0)  # Max 100%
    
    def predict(self, patient_data: Dict) -> Dict[str, Any]:
        """PACE: Execute - Comprehensive cardiovascular risk prediction."""
        try:
            # Veri ön işleme
            processed_df = self.preprocess_data(patient_data)
            
            # Risk faktörlerini analiz et
            risk_factors = self.analyze_risk_factors(patient_data)
            
            # Risk skorunu hesapla
            risk_score = self.calculate_risk_score(patient_data)
            
            # Model tahmini (varsa)
            model_prediction = None
            model_probability = None
            
            if self.model is not None:
                try:
                    model_features = ['age', 'gender', 'height', 'weight', 'ap_hi', 'ap_lo', 
                                    'cholesterol', 'gluc', 'smoke', 'alco', 'active']
                    model_df = processed_df[model_features]
                    
                    model_prediction = self.model.predict(model_df)[0]
                    model_probability = self.model.predict_proba(model_df)[0]
                    
                except Exception as e:
                    print(f"Model prediction error: {e}")
            
            # Risk seviyesi belirleme
            if risk_score >= 70:
                risk_level = "Yüksek Risk"
                health_status = "Kardiyovasküler Hastalık Riski"
            elif risk_score >= 40:
                risk_level = "Orta Risk"
                health_status = "Şüpheli - Takip Gerekli"
            else:
                risk_level = "Düşük Risk"
                health_status = "Sağlıklı"
            
            result = {
                'health_status': health_status,
                'risk_level': risk_level,
                'risk_score': risk_score,
                'risk_factors': risk_factors,
                'model_prediction': model_prediction,
                'model_probability': model_probability,
                'bmi': processed_df['bmi'].iloc[0],
                'hypertension': processed_df['hypertension'].iloc[0]
            }
            
            return result
            
        except Exception as e:
            return {
                'error': f"Prediction error: {str(e)}",
                'health_status': 'Analiz Hatası',
                'risk_score': 0.0,
                'risk_factors': [],
            }

# Kolay kullanım için yardımcı fonksiyon
def predict_cardiovascular_risk(patient_data, model_dir=None):
    """Tek satırda kardiyovasküler risk tahmini yapmak için yardımcı fonksiyon."""
    predictor = CardiovascularSystematicPredictor(model_dir)
    return predictor.predict(patient_data)

if __name__ == "__main__":
    # Test örneği
    test_data = {
        'age': 50, 'gender': 2, 'height': 175, 'weight': 80,
        'ap_hi': 140, 'ap_lo': 90, 'cholesterol': 2, 'gluc': 1,
        'smoke': 1, 'alco': 0, 'active': 1
    }
    
    result = predict_cardiovascular_risk(test_data)
    print("🫀 Cardiovascular Risk Prediction Test:")
    print(f"Status: {result['health_status']}")
    print(f"Risk Score: {result['risk_score']:.1f}%")
    print(f"Risk Level: {result['risk_level']}")
    print(f"Risk Factors: {result['risk_factors']}")
