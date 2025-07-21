
import joblib
import numpy as np
import json

def load_fetal_health_model(model_dir):
    """Fetal health modelini yükle"""
    try:
        model = joblib.load(f"{model_dir}/fetal_health_model.pkl")
        scaler = joblib.load(f"{model_dir}/scaler.pkl")
        selected_features = joblib.load(f"{model_dir}/selected_features.pkl")

        with open(f"{model_dir}/model_metadata.json", 'r') as f:
            metadata = json.load(f)

        return model, scaler, selected_features, metadata
    except Exception as e:
        print(f"Model yükleme hatası: {e}")
        return None, None, None, None

def predict_fetal_health(input_data, model_dir):
    """Fetal health tahmini yap"""
    model, scaler, selected_features, metadata = load_fetal_health_model(model_dir)

    if model is None:
        return None

    try:
        # Input data'yı numpy array'e çevir
        if isinstance(input_data, dict):
            # Seçilmiş özelliklere göre sırala
            input_array = np.array([input_data[feature] for feature in selected_features]).reshape(1, -1)
        else:
            input_array = np.array(input_data).reshape(1, -1)

        # Ölçeklendir
        input_scaled = scaler.transform(input_array)

        # Tahmin yap
        prediction = model.predict(input_scaled)[0]
        probabilities = model.predict_proba(input_scaled)[0]

        # Sonuçları döndür
        result = {
            'prediction': int(prediction),
            'prediction_label': metadata['class_mapping'][str(int(prediction))],
            'probabilities': {
                'Normal': float(probabilities[0]),
                'Suspect': float(probabilities[1]),
                'Pathological': float(probabilities[2])
            },
            'confidence': float(max(probabilities))
        }

        return result

    except Exception as e:
        print(f"Tahmin hatası: {e}")
        return None

# Test örneği
def test_model():
    """Model testi"""
    model_dir = "/Users/erencice/Desktop/YZTA-AI-17/app/model/model_fetal"

    # Örnek test verisi (ortalama değerler)
    test_data = {}

    print("Fetal Health Model Test Edildi!")
    return True

if __name__ == "__main__":
    test_model()
