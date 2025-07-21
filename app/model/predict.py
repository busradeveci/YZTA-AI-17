
import joblib
import numpy as np
import json
import os

def load_model(model_dir, model_name):
    """Model ve gerekli dosyaları yükle"""
    try:
        model = joblib.load(os.path.join(model_dir, f'{model_name}_model.pkl'))
        scaler = joblib.load(os.path.join(model_dir, 'scaler.pkl'))
        features = joblib.load(os.path.join(model_dir, 'selected_features.pkl'))
        
        with open(os.path.join(model_dir, 'model_metadata.json'), 'r') as f:
            metadata = json.load(f)
            
        return model, scaler, features, metadata
    except Exception as e:
        print(f"Model yükleme hatası: {e}")
        return None, None, None, None

def predict_health(input_data, model_dir, model_name):
    """Sağlık tahmini yap"""
    model, scaler, features, metadata = load_model(model_dir, model_name)
    
    if model is None:
        return None
    
    try:
        # Input verisi hazırla
        if isinstance(input_data, dict):
            input_array = np.array([input_data[feature] for feature in features]).reshape(1, -1)
        else:
            input_array = np.array(input_data).reshape(1, -1)
        
        # Ölçeklendir
        input_scaled = scaler.transform(input_array)
        
        # Tahmin yap
        prediction = model.predict(input_scaled)[0]
        probabilities = model.predict_proba(input_scaled)[0]
        
        # Sonucu hazırla
        if metadata['model_type'] == 'Binary Classification':
            result = {
                'prediction': int(prediction),
                'prediction_label': metadata['class_mapping'][str(int(prediction))],
                'probability_positive': float(probabilities[1]),
                'probability_negative': float(probabilities[0]),
                'confidence': float(max(probabilities))
            }
        else:  # Multi-class
            class_probs = {metadata['class_mapping'][str(i+1)]: float(prob) 
                          for i, prob in enumerate(probabilities)}
            result = {
                'prediction': int(prediction),
                'prediction_label': metadata['class_mapping'][str(int(prediction))],
                'class_probabilities': class_probs,
                'confidence': float(max(probabilities))
            }
        
        return result
        
    except Exception as e:
        print(f"Tahmin hatası: {e}")
        return None

# Test fonksiyonları
def test_breast_cancer():
    model_dir = "/Users/erencice/Desktop/YZTA-AI-17/app/model/model_breast"
    # Örnek test verisi (normal değerler)
    test_data = [13.5, 14.2, 85.3, 568.2, 0.095, 0.08, 0.06, 0.04, 0.18, 0.06,
                 0.25, 0.8, 1.8, 18.5, 0.006, 0.015, 0.025, 0.01, 0.015, 0.002,
                 15.2, 18.9, 97.8, 711.0, 0.13, 0.22, 0.31, 0.15, 0.28, 0.08]
    return predict_health(test_data[:10], model_dir, 'breast_cancer')

def test_cardiovascular():
    model_dir = "/Users/erencice/Desktop/YZTA-AI-17/app/model/model_cad"
    # Örnek test verisi
    test_data = [50, 1, 170, 80, 0, 0, 1, 140, 200, 0, 1, 150, 0, 2.3, 0, 3, 0]
    return predict_health(test_data[:10], model_dir, 'cardiovascular')

def test_fetal_health():
    model_dir = "/Users/erencice/Desktop/YZTA-AI-17/app/model/model_fetal"
    # Örnek test verisi
    test_data = [120, 0, 0, 0, 0, 0, 0, 0, 0, 0, 
                 73, 0.5, 43, 182, 2.4, 0, 0, 10, 2, 0, 10]
    return predict_health(test_data[:10], model_dir, 'fetal_health')

if __name__ == "__main__":
    print("Sağlık Tahmin Modelleri Test Ediliyor...")
    
    print("\n1. Breast Cancer Test:")
    result1 = test_breast_cancer()
    if result1:
        print(f"   Sonuç: {result1}")
    
    print("\n2. Cardiovascular Test:")
    result2 = test_cardiovascular()
    if result2:
        print(f"   Sonuç: {result2}")
    
    print("\n3. Fetal Health Test:")
    result3 = test_fetal_health()
    if result3:
        print(f"   Sonuç: {result3}")
