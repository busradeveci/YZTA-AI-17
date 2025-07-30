# YZTA-AI-17 Health Screening Application

AI tabanlı sağlık tarama uygulaması. Kardiyovasküler hastalıklar, meme kanseri ve fetal sağlık için makine öğrenmesi modelleri kullanır.

## 🚀 Hızlı Başlangıç

### 1. Uygulamayı Başlatma

```bash
python run.py
```

Bu komut:
- Backend API'yi `http://localhost:8000` adresinde başlatır
- Tüm ML modellerini otomatik yükler
- API dokümantasyonunu `http://localhost:8000/docs` adresinde sunar

### 2. Web Arayüzü (Frontend)

React frontend'i çalıştırmak için:

```bash
cd src/
npm install
npm start
```

Frontend `http://localhost:3000` adresinde çalışacaktır.

## 📊 Kullanılabilir Modeller

### Kardiyovasküler Hastalık Riski
- **Model**: Random Forest Classifier
- **Özellikler**: Yaş, cinsiyet, boy, kilo, kan basıncı, kolesterol, glikoz, sigara, alkol, aktivite
- **Çıktı**: Düşük/Yüksek risk sınıflandırması

### Meme Kanseri Sağkalım Tahmini  
- **Model**: Random Forest Classifier
- **Özellikler**: Yaş, ırk, medeni durum, T/N/6th Stage, derece, tümör boyutu, estrogen/progesteron durumu, lenf nodu sayıları, sağkalım süreleri
- **Çıktı**: Hayatta/Öldü sınıflandırması

### Fetal Sağlık Sınıflandırması
- **Model**: Random Forest Classifier  
- **Özellikler**: Akselerasyonlar, fetal hareket, uterin kontraksiyonlar, deselerasyonlar, variabilite ölçümleri, histogram özellikleri
- **Çıktı**: Normal/Şüpheli/Patolojik (3 sınıf)

## 🔧 API Kullanımı

### Tahmin Yapma

```bash
curl -X POST "http://localhost:8000/predict" \\
     -H "Content-Type: application/json" \\
     -d '{
       "test_type": "cardiovascular",
       "form_data": {
         "age": 45,
         "gender": 1,
         "height": 170,
         "weight": 75,
         "ap_hi": 120,
         "ap_lo": 80,
         "cholesterol": 1,
         "gluc": 1,
         "smoke": 0,
         "alco": 0,
         "active": 1
       }
     }'
```

### Mevcut Testleri Listeleme

```bash
curl "http://localhost:8000/tests"
```

### Model Bilgilerini Görme

```bash
curl "http://localhost:8000/models"
```

## 📝 API Test Etme

API'yi test etmek için:

```bash
python test_api.py
```

## 📁 Proje Yapısı

```
YZTA-AI-17/
├── app/
│   └── models/           # Eğitilmiş ML modelleri (.pkl)
├── backend/
│   ├── main.py          # FastAPI backend
│   └── requirements.txt # Python bağımlılıkları
├── src/                 # React frontend
├── tests/               # Jupyter notebook analizleri
├── data/                # Veri setleri
├── images/              # Analiz görselleri
├── run.py              # Ana uygulama başlatıcı
├── test_api.py         # API test scripti
└── create_demo_models.py # Demo model oluşturucu
```

## 🔬 Veri Analizi

Jupyter notebook'larında kapsamlı veri analizi yapılmıştır:

- `tests/cardiovascular_analysis.ipynb` - Kardiyovasküler hastalık analizi
- `tests/breast_cancer_analysis.ipynb` - Meme kanseri analizi  
- `tests/fetal_health_analysis.ipynb` - Fetal sağlık analizi

Her analiz PACE metodolojisi ile yapılmış ve şunları içerir:
- ✅ Eksik değer ve aykırı değer analizi
- ✅ VIF analizi ve çoklu doğrusal bağlantı kontrolü
- ✅ İstatistiksel hipotez testleri
- ✅ SMOTE ile veri dengeleme
- ✅ Model karşılaştırması ve seçimi
- ✅ Görselleştirmeler ve raporlama

## 🛠️ Gereksinimler

- Python 3.8+
- scikit-learn, pandas, numpy, fastapi, uvicorn
- Node.js 14+ (frontend için)

## 📖 API Dokümantasyonu

Uygulamayı başlattıktan sonra aşağıdaki adresten interaktif API dokümantasyonuna erişebilirsiniz:

**http://localhost:8000/docs**

## 🎯 Özellikler

- ✅ 3 farklı sağlık alanında AI tahmin modelleri
- ✅ RESTful API ile kolay entegrasyon
- ✅ Real-time model inference
- ✅ Kapsamlı API dokümantasyonu
- ✅ Test scriptleri ve örnekler
- ✅ PACE metodolojisi ile veri bilimi analizi
- ✅ Model performans metrikleri ve görselleştirmeler

## 👥 Geliştirici Notları

Yeni model eklemek için:
1. `create_demo_models.py` scriptine yeni model tanımı ekleyin
2. `backend/main.py` dosyasında model mapping'i güncelleyin
3. Gerekli ön işleme fonksiyonlarını ekleyin

Model formatı:
```python
{
    'model': sklearn_model,
    'scaler': standard_scaler,
    'features': feature_list,
    'metadata': {
        'model_name': 'Model Adı',
        'model_type': 'RandomForest',
        'problem_type': 'Classification',
        'class_mapping': {'0': 'Sınıf1', '1': 'Sınıf2'},
        'performance_metrics': {'test_accuracy': 0.85}
    }
}
```
