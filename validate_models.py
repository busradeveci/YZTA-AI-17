#!/usr/bin/env python3
"""
Model Test ve Validation Scripti
Oluşturulan pkl dosyalarını test eder
"""

import joblib
import numpy as np
import json
import os

def test_model(model_dir, model_name, test_description):
    """Belirli bir modeli test et"""
    print(f"\n🧪 {test_description} Model Testi")
    print("-" * 40)
    
    try:
        # Model dosyalarını yükle
        model_file = f"{model_name}_model.pkl"
        model = joblib.load(os.path.join(model_dir, model_file))
        scaler = joblib.load(os.path.join(model_dir, 'scaler.pkl'))
        features = joblib.load(os.path.join(model_dir, 'selected_features.pkl'))
        
        with open(os.path.join(model_dir, 'model_metadata.json'), 'r') as f:
            metadata = json.load(f)
        
        print(f"✅ Model başarıyla yüklendi")
        print(f"   📊 Model tipi: {metadata['model_name']}")
        print(f"   🎯 Problem tipi: {metadata['problem_type']}")
        print(f"   ⚖️ Özellik sayısı: {metadata['feature_count']}")
        print(f"   📈 Test Accuracy: {metadata['performance_metrics']['test_accuracy']:.4f}")
        
        # Dummy test verisi oluştur (model beklediği boyutta)
        feature_count = len(features)
        dummy_data = np.random.random((1, feature_count))
        
        # Test tahmini
        dummy_scaled = scaler.transform(dummy_data)
        prediction = model.predict(dummy_scaled)[0]
        probabilities = model.predict_proba(dummy_scaled)[0]
        
        print(f"✅ Dummy test başarılı")
        print(f"   🎯 Tahmin: {prediction}")
        print(f"   📊 Olasılıklar: {probabilities.round(3)}")
        
        return True
        
    except Exception as e:
        print(f"❌ Test hatası: {e}")
        return False

def validate_all_models():
    """Tüm modelleri doğrula"""
    print("🔬 TÜM MODELLER VALİDASYON TESTİ")
    print("=" * 50)
    
    base_dir = "/Users/erencice/Desktop/YZTA-AI-17/app/model"
    
    models_to_test = [
        {
            'dir': os.path.join(base_dir, 'model_breast'),
            'name': 'breast_cancer',
            'description': 'Breast Cancer'
        },
        {
            'dir': os.path.join(base_dir, 'model_cad'),
            'name': 'cardiovascular',
            'description': 'Cardiovascular Disease'
        },
        {
            'dir': os.path.join(base_dir, 'model_fetal'),
            'name': 'fetal_health',
            'description': 'Fetal Health'
        }
    ]
    
    success_count = 0
    total_count = len(models_to_test)
    
    for model_info in models_to_test:
        if os.path.exists(model_info['dir']):
            success = test_model(
                model_info['dir'], 
                model_info['name'], 
                model_info['description']
            )
            if success:
                success_count += 1
        else:
            print(f"\n❌ {model_info['description']} model dizini bulunamadı!")
    
    print(f"\n📊 VALİDASYON SONUÇLARI")
    print("=" * 30)
    print(f"✅ Başarılı testler: {success_count}/{total_count}")
    print(f"📈 Başarı oranı: {(success_count/total_count)*100:.1f}%")
    
    if success_count == total_count:
        print(f"\n🎉 TÜM MODELLER BAŞARILI!")
        print(f"🚀 Production ortamında kullanıma hazır!")
    else:
        print(f"\n⚠️ Bazı modellerde sorun var!")
    
    return success_count == total_count

def check_model_files():
    """Model dosyalarının varlığını kontrol et"""
    print("📁 MODEL DOSYA KONTROLÜ")
    print("=" * 30)
    
    base_dir = "/Users/erencice/Desktop/YZTA-AI-17/app/model"
    expected_files = ['scaler.pkl', 'selected_features.pkl', 'model_metadata.json']
    
    model_dirs = ['model_breast', 'model_cad', 'model_fetal']
    model_files = ['breast_cancer_model.pkl', 'cardiovascular_model.pkl', 'fetal_health_model.pkl']
    
    all_files_exist = True
    
    for i, model_dir in enumerate(model_dirs):
        full_dir = os.path.join(base_dir, model_dir)
        print(f"\n📂 {model_dir}:")
        
        if not os.path.exists(full_dir):
            print(f"   ❌ Dizin mevcut değil!")
            all_files_exist = False
            continue
        
        # Model dosyası kontrolü
        model_file = os.path.join(full_dir, model_files[i])
        if os.path.exists(model_file):
            print(f"   ✅ {model_files[i]}")
        else:
            print(f"   ❌ {model_files[i]} eksik!")
            all_files_exist = False
        
        # Diğer dosyalar
        for file_name in expected_files:
            file_path = os.path.join(full_dir, file_name)
            if os.path.exists(file_path):
                print(f"   ✅ {file_name}")
            else:
                print(f"   ❌ {file_name} eksik!")
                all_files_exist = False
    
    return all_files_exist

def main():
    """Ana işlem"""
    print("🎗️ YZTA-AI-17 MODEL VALİDASYON RAPORU")
    print("=" * 60)
    
    # 1. Dosya varlığını kontrol et
    files_ok = check_model_files()
    
    if not files_ok:
        print(f"\n❌ Bazı model dosyaları eksik!")
        return False
    
    # 2. Modelleri test et
    validation_ok = validate_all_models()
    
    # 3. Final rapor
    print(f"\n📋 FİNAL RAPOR")
    print("=" * 20)
    print(f"📁 Dosya kontrolü: {'✅ BAŞARILI' if files_ok else '❌ BAŞARISIZ'}")
    print(f"🧪 Model validasyonu: {'✅ BAŞARILI' if validation_ok else '❌ BAŞARISIZ'}")
    
    if files_ok and validation_ok:
        print(f"\n🎉 TÜM KONTROLLER BAŞARILI!")
        print(f"📊 3 adet sağlık tahmin modeli hazır:")
        print(f"   🎗️ Breast Cancer Classification")
        print(f"   🫀 Cardiovascular Disease Prediction") 
        print(f"   👶 Fetal Health Assessment")
        print(f"\n🚀 Modeller Flask uygulamasında kullanılabilir!")
        return True
    else:
        print(f"\n❌ Bazı kontroller başarısız!")
        return False

if __name__ == "__main__":
    main()
