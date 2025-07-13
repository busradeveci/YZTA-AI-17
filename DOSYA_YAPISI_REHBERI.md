# YZTA-AI-17 Tıbbi Tahmin Sistemi - Dosya Yapısı Rehberi

## 🗂️ Dosya Yapısını Anlama Sırası

Bu rehber, YZTA-AI-17 projesi dosya yapısını sistematik olarak anlamak için hangi dosyaları hangi sırayla incelemeniz gerektiğini gösterir.

---

## 📋 1. BAŞLANGIÇ - Ana Belgeleri Okuyun

### İlk İnceleme Sırası:
1. **`README.md`** - Projenin genel tanıtımı, kurulum talimatları
2. **`DEPLOYMENT.md`** - Çapraz platform dağıtım kılavuzu
3. **`requirements.txt`** - Proje bağımlılıkları
4. **`.gitignore`** - Git tarafından görmezden gelinen dosyalar

---

## 🏗️ 2. PROJE YAPISINI ANLAYIŞ

### Ana Dizin İncelemesi:
```
YZTA-AI-17/
├── 📄 README.md                    # 1️⃣ İlk oku
├── 📄 DEPLOYMENT.md               # 2️⃣ Dağıtım talimatları
├── 📄 requirements.txt            # 3️⃣ Bağımlılıklar
├── 📄 config.py                   # 4️⃣ Sistem yapılandırması
├── 📄 run.py                      # 5️⃣ Ana başlatma scripti
├── 📁 app/                        # 6️⃣ Ana uygulama kodu
├── 📁 data/                       # 7️⃣ Veri setleri
├── 📁 static/                     # 8️⃣ Web arayüzü dosyaları
├── 📁 tests/                      # 9️⃣ Test dosyaları ve analiz notebook'ları
└── 📁 sprintOne/                  # 🔟 Sprint dokümantasyonu
```

---

## ⚙️ 3. SİSTEM YAPILANDIRMASI

### İnceleme Sırası:
1. **`config.py`** - Sistem konfigürasyonu
   - Model yolları ve ayarları
   - Flask yapılandırması
   - API endpoint'leri

2. **`run.py`** - Ana başlatma scripti
   - Port yönetimi
   - Virtual environment kontrolü
   - Çapraz platform desteği

---

## 🎯 4. ANA UYGULAMA KODU (app/ klasörü)

### İnceleme Sırası:
```
app/
├── 📄 __init__.py                 # 1️⃣ Flask app factory
├── 📄 routes.py                   # 2️⃣ Web rotaları ve API endpoints
├── 📄 utils.py                    # 3️⃣ Yardımcı fonksiyonlar
├── 📁 model/                      # 4️⃣ ML modelleri (aşağıda detay)
└── 📁 templates/                  # 5️⃣ HTML şablonları
```

### Model Klasörü İncelemesi:
```
app/model/
├── 📁 shared/                     # 1️⃣ Ortak işlevler
│   └── preprocessing_utils.py     #     Veri ön işleme
├── 📁 model_cad/                  # 2️⃣ Kardiyovasküler model
│   ├── __init__.py
│   ├── predict.py                 #     Tahmin fonksiyonları
│   └── preprocess.py              #     Veri ön işleme
├── 📁 model_breast/               # 3️⃣ Meme kanseri modeli
│   ├── __init__.py
│   ├── predict.py
│   └── preprocess.py
└── 📁 model_fetal/                # 4️⃣ Fetal sağlık modeli
    ├── __init__.py
    ├── predict.py
    └── preprocess.py
```

---

## 🎨 5. KULLANICI ARAYÜZÜ

### İnceleme Sırası:
```
static/
├── 📄 style.css                   # 1️⃣ CSS stilleri (Türkçe arayüz)
└── 📄 script.js                   # 2️⃣ JavaScript (form validasyon)

app/templates/
└── 📄 index.html                  # 3️⃣ Ana HTML şablonu
```

---

## 📊 6. VERİ SETLERİ

### İnceleme Sırası:
```
data/
├── 📄 Cardiovascular_Disease_Dataset.csv    # 1️⃣ Kardiyovasküler veri
├── 📁 breast_cancer/
│   └── 📄 breast_cancer_dataset.csv         # 2️⃣ Meme kanseri veri
└── 📁 fetal_health/
    └── 📄 fetal_health_dataset.csv          # 3️⃣ Fetal sağlık veri
```

---

## 🧪 7. TESTLER VE ANALİZ

### İnceleme Sırası:
```
tests/
├── 📄 card.ipynb                           # 1️⃣ Kardiyovasküler analiz
├── 📄 breast_cancer_analysis.ipynb         # 2️⃣ Meme kanseri analiz
├── 📄 fetal_health_analysis.ipynb          # 3️⃣ Fetal sağlık analiz
└── 📄 cardiovascular_model.pkl             # 4️⃣ Eğitilmiş model
```

---

## 🚀 8. PLATFORM DESTEĞİ

### İnceleme Sırası:
1. **`start.sh`** - Linux/macOS başlatma scripti
2. **`start.bat`** - Windows başlatma scripti
3. **`clear_port.sh`** - Port temizleme aracı

---

## 📝 9. PROJE YAŞAM DÖNGÜSÜ İNCELEMESİ

### Geliştirme Süreci:
1. **Veri Analizi**: `tests/*.ipynb` notebook'larında
2. **Model Geliştirme**: `app/model/*/` klasörlerinde
3. **Web Arayüzü**: `app/templates/` ve `static/` klasörlerinde
4. **API Geliştirme**: `app/routes.py` dosyasında
5. **Konfigürasyon**: `config.py` dosyasında

---

## 🔍 10. DETAYLI İNCELEME REHBERİ

### Her Dosyayı İnceleme Sırası:

#### A) Sistem Anlama Aşaması:
1. `README.md` - Proje tanıtımı
2. `config.py` - Sistem konfigürasyonu
3. `run.py` - Başlatma mantığı
4. `app/__init__.py` - Flask factory pattern

#### B) İş Mantığı Anlama:
1. `app/routes.py` - Web rotaları ve API
2. `app/utils.py` - Yardımcı fonksiyonlar
3. `app/model/shared/preprocessing_utils.py` - Ortak işlevler

#### C) Model Detayları:
1. Her model klasöründe: `__init__.py` → `preprocess.py` → `predict.py`
2. Test dosyaları: `tests/*.ipynb` (Jupyter notebook'lar)

#### D) Kullanıcı Deneyimi:
1. `app/templates/index.html` - HTML yapısı
2. `static/style.css` - Görsel tasarım
3. `static/script.js` - İnteraktif özellikler

---

## 📊 11. VERİ AKIŞI TAKİBİ

### Sistemdeki Veri Akışı:
```
1. Kullanıcı → Web Formu (index.html)
2. Form → JavaScript Validasyon (script.js)
3. POST İsteği → Flask Routes (routes.py)
4. Routes → Model Utils (utils.py)
5. Utils → Preprocessing (model/*/preprocess.py)
6. Preprocessing → Prediction (model/*/predict.py)
7. Prediction → Response → Kullanıcı
```

---

## 🛠️ 12. GELIŞTIRME VE HATA AYIKLAMA

### Problem Çözme Sırası:
1. **Log Dosyaları**: `logs/` klasörü
2. **Hata Ayıklama**: `run.py --debug`
3. **Test Çalıştırma**: `run.py --test`
4. **Sistem Bilgisi**: `run.py --info`

---

## 📋 13. ÖNERİLEN İNCELEME PLANI

### Günlük İnceleme Planı:

#### 1. Gün - Genel Bakış:
- README.md
- DEPLOYMENT.md
- Proje yapısını genel olarak incele

#### 2. Gün - Sistem Mimarisi:
- config.py
- run.py
- app/__init__.py

#### 3. Gün - Web Katmanı:
- app/routes.py
- app/templates/index.html
- static/ dosyaları

#### 4. Gün - İş Mantığı:
- app/utils.py
- app/model/shared/preprocessing_utils.py

#### 5. Gün - Model Detayları:
- Her model klasörünü sırayla incele
- İlgili test notebook'larını çalıştır

---

## 🎯 14. KRİTİK NOKTALARIN ANALİZİ

### Dikkat Edilmesi Gereken Dosyalar:
1. **`config.py`** - Tüm sistem ayarları burada
2. **`app/routes.py`** - API ve web endpoints
3. **`app/utils.py`** - Model yükleme ve tahmin mantığı
4. **`run.py`** - Başlatma ve port yönetimi

### Anlaşılması Zor Olabilecek Kısımlar:
1. **PACE Metodolojisi** - Model geliştirme süreci
2. **Port Yönetimi** - Çapraz platform uyumluluk
3. **Model Factory Pattern** - Dinamik model yükleme

---

## 📚 15. SONUÇ VE ÖNERİLER

### Dosya Yapısını Anlama Stratejisi:
1. **Yukarıdan Aşağıya**: README → Config → Main App
2. **İçten Dışa**: Core Logic → Web Layer → UI
3. **Kronolojik**: Geliştirme süreci sırasına göre

### Son Tavsiyeler:
- Her dosyayı okumadan önce açıklamaları (docstring) okuyun
- Jupyter notebook'ları çalıştırarak veri analizi sürecini anlayın
- Sistemi çalıştırarak web arayüzünü test edin
- Log dosyalarını kontrol ederek sistem davranışını anlayın

Bu rehber sayesinde YZTA-AI-17 projesinin tüm bileşenlerini sistematik olarak anlayabilirsiniz.
