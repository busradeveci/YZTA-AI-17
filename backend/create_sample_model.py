#!/usr/bin/env python3
"""
Örnek model oluşturma scripti
Bu script, test amaçlı basit bir makine öğrenmesi modeli oluşturur.
"""

import joblib
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import pandas as pd

def create_sample_heart_disease_model():
    """Örnek kalp hastalığı modeli oluştur"""
    print("Kalp hastalığı modeli oluşturuluyor...")
    
    # Örnek veri oluştur
    np.random.seed(42)
    n_samples = 1000
    
    # Özellikler
    age = np.random.normal(55, 15, n_samples).astype(int)
    gender = np.random.choice([0, 1], n_samples)  # 0: Kadın, 1: Erkek
    chest_pain = np.random.choice([0, 1, 2, 3], n_samples)  # 0-3 arası
    blood_pressure = np.random.normal(130, 20, n_samples).astype(int)
    cholesterol = np.random.normal(200, 40, n_samples).astype(int)
    blood_sugar = np.random.normal(120, 30, n_samples).astype(int)
    exercise_angina = np.random.choice([0, 1], n_samples)
    smoking = np.random.choice([0, 1], n_samples)
    diabetes = np.random.choice([0, 1], n_samples)
    family_history = np.random.choice([0, 1], n_samples)
    max_heart_rate = np.random.normal(150, 20, n_samples).astype(int)
    
    # Veri seti oluştur
    data = pd.DataFrame({
        'age': age,
        'gender': gender,
        'chestPain': chest_pain,
        'bloodPressure': blood_pressure,
        'cholesterol': cholesterol,
        'bloodSugar': blood_sugar,
        'exerciseAngina': exercise_angina,
        'smoking': smoking,
        'diabetes': diabetes,
        'familyHistory': family_history,
        'maxHeartRate': max_heart_rate
    })
    
    # Hedef değişken oluştur (basit kurallar)
    target = np.zeros(n_samples)
    
    # Risk faktörleri
    high_risk = (
        (age > 65) |
        (gender == 1) |
        (chest_pain > 1) |
        (blood_pressure > 140) |
        (cholesterol > 240) |
        (blood_sugar > 126) |
        (exercise_angina == 1) |
        (smoking == 1) |
        (diabetes == 1) |
        (family_history == 1)
    )
    
    # Risk skoruna göre hedef belirle
    risk_score = (
        (age > 65).astype(int) * 2 +
        (gender == 1).astype(int) * 1 +
        (chest_pain > 1).astype(int) * 3 +
        (blood_pressure > 140).astype(int) * 2 +
        (cholesterol > 240).astype(int) * 1 +
        (blood_sugar > 126).astype(int) * 2 +
        (exercise_angina == 1).astype(int) * 3 +
        (smoking == 1).astype(int) * 1 +
        (diabetes == 1).astype(int) * 2 +
        (family_history == 1).astype(int) * 1
    )
    
    # Risk skoruna göre hedef belirle
    target = (risk_score > 8).astype(int)  # Yüksek risk eşiği
    
    # Veriyi böl
    X_train, X_test, y_train, y_test = train_test_split(
        data, target, test_size=0.2, random_state=42, stratify=target
    )
    
    # Model eğit
    model = RandomForestClassifier(
        n_estimators=100,
        max_depth=10,
        random_state=42
    )
    
    model.fit(X_train, y_train)
    
    # Model performansını değerlendir
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    
    print(f"Model doğruluğu: {accuracy:.3f}")
    
    # Modeli kaydet
    model_path = "models/heart_disease.pkl"
    joblib.dump(model, model_path)
    
    print(f"Model kaydedildi: {model_path}")
    
    return model, accuracy

def create_sample_fetal_health_model():
    """Örnek fetal sağlık modeli oluştur"""
    print("Fetal sağlık modeli oluşturuluyor...")
    
    # Örnek veri oluştur
    np.random.seed(42)
    n_samples = 800
    
    # Özellikler
    age = np.random.normal(30, 8, n_samples).astype(int)
    gestational_age = np.random.normal(28, 8, n_samples).astype(int)
    blood_pressure = np.random.normal(120, 15, n_samples).astype(int)
    blood_sugar = np.random.normal(100, 20, n_samples).astype(int)
    smoking = np.random.choice([0, 1], n_samples, p=[0.8, 0.2])
    diabetes = np.random.choice([0, 1], n_samples, p=[0.9, 0.1])
    hypertension = np.random.choice([0, 1], n_samples, p=[0.85, 0.15])
    previous_complications = np.random.choice([0, 1], n_samples, p=[0.7, 0.3])
    
    # Veri seti oluştur
    data = pd.DataFrame({
        'age': age,
        'gestationalAge': gestational_age,
        'bloodPressure': blood_pressure,
        'bloodSugar': blood_sugar,
        'smoking': smoking,
        'diabetes': diabetes,
        'hypertension': hypertension,
        'previousComplications': previous_complications
    })
    
    # Hedef değişken oluştur
    risk_score = (
        (age > 35).astype(int) * 2 +
        (gestational_age < 20).astype(int) * 3 +
        (blood_pressure > 140).astype(int) * 2 +
        (blood_sugar > 126).astype(int) * 2 +
        (smoking == 1).astype(int) * 3 +
        (diabetes == 1).astype(int) * 3 +
        (hypertension == 1).astype(int) * 2 +
        (previous_complications == 1).astype(int) * 2
    )
    
    target = (risk_score > 6).astype(int)
    
    # Veriyi böl
    X_train, X_test, y_train, y_test = train_test_split(
        data, target, test_size=0.2, random_state=42, stratify=target
    )
    
    # Model eğit
    model = RandomForestClassifier(
        n_estimators=100,
        max_depth=8,
        random_state=42
    )
    
    model.fit(X_train, y_train)
    
    # Model performansını değerlendir
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    
    print(f"Model doğruluğu: {accuracy:.3f}")
    
    # Modeli kaydet
    model_path = "models/fetal_health.pkl"
    joblib.dump(model, model_path)
    
    print(f"Model kaydedildi: {model_path}")
    
    return model, accuracy

def create_sample_breast_cancer_model():
    """Örnek meme kanseri modeli oluştur"""
    print("Meme kanseri modeli oluşturuluyor...")
    
    # Örnek veri oluştur
    np.random.seed(42)
    n_samples = 600
    
    # Özellikler
    age = np.random.normal(55, 12, n_samples).astype(int)
    bmi = np.random.normal(25, 5, n_samples)
    age_first_pregnancy = np.random.normal(28, 6, n_samples).astype(int)
    family_history = np.random.choice([0, 1], n_samples, p=[0.8, 0.2])
    alcohol = np.random.choice([0, 1], n_samples, p=[0.7, 0.3])
    smoking = np.random.choice([0, 1], n_samples, p=[0.8, 0.2])
    hormone_therapy = np.random.choice([0, 1], n_samples, p=[0.6, 0.4])
    
    # Veri seti oluştur
    data = pd.DataFrame({
        'age': age,
        'bmi': bmi,
        'ageFirstPregnancy': age_first_pregnancy,
        'familyHistory': family_history,
        'alcohol': alcohol,
        'smoking': smoking,
        'hormoneTherapy': hormone_therapy
    })
    
    # Hedef değişken oluştur
    risk_score = (
        (age > 50).astype(int) * 2 +
        (bmi > 30).astype(int) * 1 +
        (age_first_pregnancy > 35).astype(int) * 2 +
        (family_history == 1).astype(int) * 4 +
        (alcohol == 1).astype(int) * 1 +
        (smoking == 1).astype(int) * 1 +
        (hormone_therapy == 1).astype(int) * 1
    )
    
    target = (risk_score > 5).astype(int)
    
    # Veriyi böl
    X_train, X_test, y_train, y_test = train_test_split(
        data, target, test_size=0.2, random_state=42, stratify=target
    )
    
    # Model eğit
    model = RandomForestClassifier(
        n_estimators=100,
        max_depth=8,
        random_state=42
    )
    
    model.fit(X_train, y_train)
    
    # Model performansını değerlendir
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    
    print(f"Model doğruluğu: {accuracy:.3f}")
    
    # Modeli kaydet
    model_path = "models/breast_cancer.pkl"
    joblib.dump(model, model_path)
    
    print(f"Model kaydedildi: {model_path}")
    
    return model, accuracy

def main():
    """Ana fonksiyon"""
    print("🚀 Örnek modeller oluşturuluyor...")
    print("=" * 50)
    
    # Models klasörünü oluştur
    import os
    os.makedirs("models", exist_ok=True)
    
    # Tüm modelleri oluştur
    models = {}
    
    try:
        models['heart_disease'], acc1 = create_sample_heart_disease_model()
        print()
        
        models['fetal_health'], acc2 = create_sample_fetal_health_model()
        print()
        
        models['breast_cancer'], acc3 = create_sample_breast_cancer_model()
        print()
        
        print("=" * 50)
        print("✅ Tüm modeller başarıyla oluşturuldu!")
        print(f"📊 Model Performansları:")
        print(f"   • Kalp Hastalığı: {acc1:.3f}")
        print(f"   • Fetal Sağlık: {acc2:.3f}")
        print(f"   • Meme Kanseri: {acc3:.3f}")
        print()
        print("📁 Modeller 'models/' klasörüne kaydedildi:")
        print("   • models/heart_disease.pkl")
        print("   • models/fetal_health.pkl")
        print("   • models/breast_cancer.pkl")
        print()
        print("🎯 Bu modelleri API'de kullanabilirsiniz!")
        
    except Exception as e:
        print(f"❌ Hata oluştu: {e}")
        return False
    
    return True

if __name__ == "__main__":
    main() 