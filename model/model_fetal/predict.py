"""
Fetal Health Systematic Prediction Module
=========================================

Bu modül fetal_health_systematic_analysis.ipynb dosyasında geliştirilen 
sistematik PACE metodolojisi ile eğitilmiş modeli kullanarak 
CTG (Kardiyotokografi) verilerinden fetal sağlık durumu tahmini yapar.

Model özellikleri:
- PACE (Plan-Analyze-Construct-Execute) metodolojisi
- 3 sınıflı classification: Normal, Şüpheli, Patolojik
- RandomForest/LogisticRegression optimized model
- 15 seçilmiş CTG parametresi
- StandardScaler normalizasyon
"""

import pickle
import pandas as pd
import numpy as np
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

class FetalHealthSystematicPredictor:
    """
    Fetal Health Systematic Prediction Class
    
    Bu sınıf fetal_health_systematic_analysis.ipynb notebook'unda 
    geliştirilen sistematik yaklaşım ile eğitilmiş modeli kullanır.
    """
    
    def __init__(self, model_dir=None):
        """Initialize the systematic predictor with trained components."""
        if model_dir is None:
            model_dir = Path(__file__).parent
        
        # Systematic analysis'ten kayıtlı model bileşenlerini yükle
        self.model = self._load_component(model_dir / 'fetal_health_optimized_model.pkl')
        self.scaler = self._load_component(model_dir / 'scaler.pkl')
        self.feature_selector = self._load_component(model_dir / 'feature_selector.pkl')
        self.metadata = self._load_component(model_dir / 'model_metadata.pkl')
        
        # Model bilgileri
        self.model_type = self.metadata.get('model_type', 'Unknown')
        self.selected_features = self.metadata.get('selected_features', [])
        self.classes = self.metadata.get('classes', ['Normal', 'Şüpheli', 'Patolojik'])
        self.accuracy = self.metadata.get('accuracy', 0.0)
    
    def _load_component(self, path):
        """Load a pickled model component."""
        try:
            with open(path, 'rb') as f:
                return pickle.load(f)
        except FileNotFoundError:
            raise FileNotFoundError(f"Model bileşeni bulunamadı: {path}")
        except Exception as e:
            raise Exception(f"Model yükleme hatası: {str(e)}")
    
    def predict(self, patient_data):
        """
        CTG verilerinden fetal sağlık durumu tahmini yapar.
        
        Args:
            patient_data (dict): CTG parametrelerini içeren sözlük
                Örnek: {
                    'baseline value': 120.0,
                    'accelerations': 0.0,
                    'fetal_movement': 0.0,
                    'uterine_contractions': 0.003,
                    'light_decelerations': 0.0,
                    'severe_decelerations': 0.0,
                    'prolongued_decelerations': 0.0,
                    'abnormal_short_term_variability': 73.0,
                    'mean_value_of_short_term_variability': 0.5,
                    'percentage_of_time_with_abnormal_long_term_variability': 43.0,
                    'mean_value_of_long_term_variability': 2.4,
                    'histogram_width': 64.0,
                    'histogram_min': 62.0,
                    'histogram_max': 126.0,
                    'histogram_number_of_peaks': 2.0,
                    'histogram_number_of_zeroes': 0.0,
                    'histogram_mode': 120.0,
                    'histogram_mean': 137.0,
                    'histogram_median': 121.0,
                    'histogram_variance': 73.0,
                    'histogram_tendency': 1.0
                }
                
        Returns:
            dict: Tahmin sonuçları
                {
                    'success': True,
                    'prediction': int,  # 1: Normal, 2: Şüpheli, 3: Patolojik
                    'health_status': str,  # 'Normal', 'Şüpheli', 'Patolojik'
                    'probabilities': {
                        'Normal': float,
                        'Şüpheli': float, 
                        'Patolojik': float
                    },
                    'risk_level': str,  # 'Düşük', 'Orta', 'Yüksek'
                    'recommendations': list,
                    'model_info': dict
                }
        """
        try:
            # DataFrame'e dönüştür
            input_df = pd.DataFrame([patient_data])
            
            # Tüm özelliklerin mevcut olup olmadığını kontrol et
            expected_features = [
                'baseline value', 'accelerations', 'fetal_movement', 
                'uterine_contractions', 'light_decelerations', 'severe_decelerations',
                'prolongued_decelerations', 'abnormal_short_term_variability',
                'mean_value_of_short_term_variability', 
                'percentage_of_time_with_abnormal_long_term_variability',
                'mean_value_of_long_term_variability', 'histogram_width',
                'histogram_min', 'histogram_max', 'histogram_number_of_peaks',
                'histogram_number_of_zeroes', 'histogram_mode', 'histogram_mean',
                'histogram_median', 'histogram_variance', 'histogram_tendency'
            ]
            
            # Eksik özellikleri default değerlerle doldur
            for feature in expected_features:
                if feature not in input_df.columns:
                    input_df[feature] = 0.0
            
            # Veriyi ölçeklendir
            input_scaled = self.scaler.transform(input_df[expected_features])
            
            # Özellik seçimi uygula
            input_selected = self.feature_selector.transform(input_scaled)
            
            # Tahmin yap
            prediction = self.model.predict(input_selected)[0]
            probabilities = self.model.predict_proba(input_selected)[0]
            
            # Sınıf ismine dönüştür (1: Normal, 2: Şüpheli, 3: Patolojik)
            health_status = self.classes[prediction - 1] if prediction <= len(self.classes) else 'Belirsiz'
            
            # Risk seviyesi belirle
            max_prob = max(probabilities)
            if prediction == 1 and max_prob > 0.8:
                risk_level = 'Düşük'
            elif prediction == 2 or (prediction == 1 and max_prob <= 0.8):
                risk_level = 'Orta'
            else:
                risk_level = 'Yüksek'
            
            # Öneriler
            recommendations = self._generate_recommendations(prediction, probabilities)
            
            return {
                'success': True,
                'prediction': int(prediction),
                'health_status': health_status,
                'probabilities': {
                    'Normal': float(probabilities[0]),
                    'Şüpheli': float(probabilities[1]),
                    'Patolojik': float(probabilities[2])
                },
                'risk_level': risk_level,
                'recommendations': recommendations,
                'model_info': {
                    'model_type': self.model_type,
                    'accuracy': self.accuracy,
                    'selected_features_count': len(self.selected_features),
                    'methodology': 'PACE Systematic Analysis'
                }
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'prediction': None,
                'health_status': 'Hata',
                'probabilities': {'Normal': 0.0, 'Şüpheli': 0.0, 'Patolojik': 0.0}
            }
    
    def _generate_recommendations(self, prediction, probabilities):
        """Tahmin sonucuna göre öneriler üret."""
        recommendations = []
        
        if prediction == 1:  # Normal
            recommendations.extend([
                "Fetal sağlık durumu normal görünüyor",
                "Rutin takipleri sürdürün",
                "Sağlıklı yaşam tarzını devam ettirin"
            ])
        elif prediction == 2:  # Şüpheli
            recommendations.extend([
                "Yakın takip gerekebilir",
                "Ek testler düşünülebilir",
                "Doktor kontrolünü artırın",
                "Fetal hareket sayımına dikkat edin"
            ])
        else:  # Patolojik
            recommendations.extend([
                "Acil tıbbi değerlendirme gerekli",
                "Derhal doktora başvurun",
                "Hastane takibi gerekebilir",
                "Doğum öncesi yoğun izlem önerilir"
            ])
        
        # Olasılık bazlı ek öneriler
        if max(probabilities) < 0.7:
            recommendations.append("Tahmin güvenilirliği düşük, ek testler önerilir")
        
        return recommendations
    
    def get_model_info(self):
        """Model hakkında detaylı bilgi döndür."""
        return {
            'model_type': self.model_type,
            'accuracy': self.accuracy,
            'classes': self.classes,
            'selected_features': self.selected_features,
            'methodology': 'PACE Systematic Analysis',
            'notebook_source': 'fetal_health_systematic_analysis.ipynb'
        }
    
    def validate_input(self, patient_data):
        """Giriş verilerini doğrula."""
        required_features = [
            'baseline value', 'accelerations', 'fetal_movement', 
            'uterine_contractions', 'light_decelerations', 'severe_decelerations'
        ]
        
        missing = [f for f in required_features if f not in patient_data]
        if missing:
            return False, f"Eksik özellikler: {missing}"
            
        # Değer aralıklarını kontrol et
        validations = {
            'baseline value': (50, 200),
            'accelerations': (0, 1),
            'fetal_movement': (0, 1),
            'uterine_contractions': (0, 1)
        }
        
        for feature, (min_val, max_val) in validations.items():
            if feature in patient_data:
                value = patient_data[feature]
                if not min_val <= value <= max_val:
                    return False, f"{feature} değeri {min_val}-{max_val} aralığında olmalı"
        
        return True, "Geçerli"


# Kolay kullanım için yardımcı fonksiyon
def predict_fetal_health(patient_data, model_dir=None):
    """
    Tek satırda fetal sağlık tahmini yapmak için yardımcı fonksiyon.
    
    Args:
        patient_data (dict): CTG parametreleri
        model_dir (str, optional): Model klasörü yolu
        
    Returns:
        dict: Tahmin sonuçları
    """
    predictor = FetalHealthSystematicPredictor(model_dir)
    return predictor.predict(patient_data)


if __name__ == "__main__":
    # Test örneği
    test_data = {
        'baseline value': 120.0,
        'accelerations': 0.0,
        'fetal_movement': 0.0,
        'uterine_contractions': 0.003,
        'light_decelerations': 0.0,
        'severe_decelerations': 0.0,
        'prolongued_decelerations': 0.0,
        'abnormal_short_term_variability': 73.0,
        'mean_value_of_short_term_variability': 0.5,
        'percentage_of_time_with_abnormal_long_term_variability': 43.0,
        'mean_value_of_long_term_variability': 2.4,
        'histogram_width': 64.0,
        'histogram_min': 62.0,
        'histogram_max': 126.0,
        'histogram_number_of_peaks': 2.0,
        'histogram_number_of_zeroes': 0.0,
        'histogram_mode': 120.0,
        'histogram_mean': 137.0,
        'histogram_median': 121.0,
        'histogram_variance': 73.0,
        'histogram_tendency': 1.0
    }
    
    result = predict_fetal_health(test_data)
    print("🫀 Fetal Health Prediction Test:")
    print(f"Status: {result['health_status']}")
    print(f"Risk Level: {result['risk_level']}")
    print(f"Probabilities: {result['probabilities']}")
