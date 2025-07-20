# MediRisk - Tıbbi Tahmin Sistemi Dosya Yapısı Rehberi

## 🗂️ Proje Genel Bakış

MediRisk, React TypeScript frontend ve FastAPI backend kullanarak tıbbi risk tahminleri yapan hibrit bir web uygulamasıdır. Bu rehber, projenin dosya yapısını sistematik olarak anlamanızı sağlar.

---

## 📋 1. BAŞLANGIÇ - Temel Belgeler

### Öncelikli İnceleme Sırası:
1. **`README.md`** - Proje tanıtımı ve takım bilgileri
2. **`DEPLOYMENT.md`** - Dağıtım kılavuzu  
3. **`requirements.txt`** - Python bağımlılıkları
4. **`tsconfig.json`** - TypeScript konfigürasyonu

---

## 🏗️ 2. MEVCUT PROJE YAPISI

### Ana Dizin Haritası:
```
MediRisk/
├── 📄 README.md                    # Proje dokümantasyonu
├── 📄 DEPLOYMENT.md               # Dağıtım rehberi
├── 📄 DOSYA_YAPISI_REHBERI.md     # Bu dosya
├── 📄 LLM_INTEGRATION.md          # LLM entegrasyon dokümantasyonu
├── 📄 requirements.txt            # Python bağımlılıkları
├── 📄 requirements_minimal.txt    # Minimal bağımlılıklar
├── 📄 requirements_llm.txt        # LLM dependencies
├── 📄 config.py                   # Sistem konfigürasyonu
├── 📄 run.py                      # Ana başlatma scripti
├── 📄 deploy.py                   # Dağıtım scripti
├── 📄 install.py                  # Kurulum scripti
├── 📄 generate_professional_models.py  # PACE model generation
├── 📄 test_models.py              # Model verification
├── 📄 deployment_report.py        # Deployment status
├── 📄 llm_report_enhancer.py      # Full async LLM service
├── 📄 simple_llm_enhancer.py      # Simple sync LLM service
├── 📄 llm_integration_examples.py # LLM usage examples
├── 📄 tsconfig.json               # TypeScript ayarları
├── 📄 package-lock.json           # NPM bağımlılık kilidi
├── 📄 start.sh                    # Unix başlatma scripti
├── 📄 start.bat                   # Windows başlatma scripti
├── 📄 clear_port.sh               # Port temizleme aracı
├── 📁 backend/                    # FastAPI backend
├── 📁 src/                        # React frontend
├── 📁 public/                     # React statik dosyaları
├── 📁 model/                      # ML modelleri (PACE compliant)
├── 📁 data/                       # Veri setleri
├── 📁 tests/                      # Test ve analiz dosyaları
└── 📁 sprintOne/                  # Sprint dokümantasyonu
```

---

## ⚙️ 3. SİSTEM YAPILANDIRMASI

### Core Dosyalar:
1. **`config.py`** - Sistem konfigürasyonu
   - API endpoint'leri ve port ayarları
   - Model yolları ve konfigürasyonları

2. **`run.py`** - Ana başlatma scripti
   - Port yönetimi ve çakışma kontrolü
   - Cross-platform başlatma desteği

3. **`deploy.py`** - Dağıtım ve kurulum
   - Otomatik deployment işlemleri
   - Environment hazırlama

4. **`install.py`** - Bağımlılık yönetimi
   - Paket kurulumu ve verifikasyon

5. **`generate_professional_models.py`** - PACE Model Generation
   - Sistematik model oluşturma (Plan-Analyze-Construct-Execute)
   - Profesyonel PKL dosyaları üretimi

6. **`test_models.py`** - Model Verification System
   - Model doğrulama ve test işlemleri

7. **`deployment_report.py`** - Deployment Status Reporter
   - Sistem durumu ve deployment raporlama

---

## 🤖 4. LLM INTEGRATION SYSTEM

### LLM Entegrasyon Dosyaları:
```
📁 LLM Integration/
├── 📄 llm_report_enhancer.py      # Full async LLM service
├── 📄 simple_llm_enhancer.py      # Simple sync version  
├── � llm_integration_examples.py # Usage examples & tests
├── 📄 requirements_llm.txt        # LLM dependencies
└── 📄 LLM_INTEGRATION.md         # Complete documentation
```

**İnceleme Sırası:**
1. `LLM_INTEGRATION.md` - Kapsamlı dokümantasyon
2. `simple_llm_enhancer.py` - Basit kullanım için
3. `llm_integration_examples.py` - Örnek implementasyonlar
4. `llm_report_enhancer.py` - Gelişmiş async versiyon

**Özellikler:**
- 🎗️ **Meme Kanseri**: Morfololojik analiz raporları
- 🫀 **Kardiyovasküler**: Kardiyak risk değerlendirmeleri
- 👶 **Fetal Sağlık**: CTG analiz sonuçları
- 🔗 **Multi-Provider**: OpenAI, Anthropic, Ollama desteği

---

## �🚀 5. BACKEND SİSTEMİ (FastAPI)

### Backend Klasörü İncelemesi:
```
backend/
├── 📄 main.py                     # FastAPI ana uygulama
├── 📄 requirements.txt            # Backend bağımlılıkları  
├── 📄 create_sample_model.py      # Model oluşturma scripti
└── 📄 cardiovascular_model.pkl    # Eğitilmiş model dosyası
```

**İnceleme Sırası:**
1. `main.py` - API endpoints ve business logic
2. `requirements.txt` - Backend dependencies
3. `create_sample_model.py` - Model creation scripts

---

## 🤖 6. MAKİNE ÖĞRENMESİ MODELLERİ (PACE Methodology)

### Model Klasörü Yapısı:
```
model/
├── 📁 shared/                     # Ortak araçlar
│   └── preprocessing_utils.py     # Veri ön işleme fonksiyonları
├── 📁 model_breast/               # Meme Kanseri (PACE compliant)
│   ├── __init__.py
│   ├── breast_cancer_optimized_model.pkl     # Ana model
│   ├── feature_names.pkl                     # Feature tanımları
│   ├── feature_selector.pkl                  # Feature selection
│   ├── scaler.pkl                           # Data normalization
│   ├── model_metadata.pkl                   # Professional metadata
│   ├── predict.py                           # Prediction interface
│   └── preprocess.py                        # Data preprocessing
├── 📁 model_cad/                  # Kardiyovasküler (PACE compliant)
│   ├── __init__.py
│   ├── cardiovascular_optimized_model.pkl   # Ana model
│   ├── feature_names.pkl                     # Feature tanımları
│   ├── feature_selector.pkl                  # Feature selection
│   ├── scaler.pkl                           # Data normalization
│   ├── model_metadata.pkl                   # Professional metadata
│   ├── predict.py                           # Prediction interface
│   └── preprocess.py                        # Data preprocessing
├── 📁 model_fetal/                # Fetal Health (PACE compliant)
│   ├── __init__.py
│   ├── fetal_health_optimized_model.pkl     # Ana model
│   ├── feature_names.pkl                     # Feature tanımları
│   ├── feature_selector.pkl                  # Feature selection
│   ├── scaler.pkl                           # Data normalization
│   ├── model_metadata.pkl                   # Professional metadata
│   ├── predict.py                           # Prediction interface
│   └── preprocess.py                        # Data preprocessing
└── 📄 breast_cancer_model.pkl     # Legacy model (deprecated)
```

**PACE Methodology Components:**
- **Plan**: Systematic model planning and architecture
- **Analyze**: Data analysis and feature engineering  
- **Construct**: Professional model construction
- **Execute**: Deployment-ready execution

**Professional PKL Files (21 total):**
- 🎗️ **Breast Cancer**: 7 professional PKL components
- 🫀 **Cardiovascular**: 7 professional PKL components
- 👶 **Fetal Health**: 7 professional PKL components

**Performance Metrics:**
- **Average Accuracy**: 93.34%
- **Industry Standard**: ✅ Professional PKL files
- **Production Ready**: ✅ Deployment ready
│   └── preprocess.py              # Veri ön işleme
├── 📁 model_breast/               # Meme kanseri modeli
│   ├── __init__.py
│   ├── predict.py
│   └── preprocess.py
└── 📁 model_fetal/                # Fetal sağlık modeli
    ├── __init__.py
    ├── predict.py
    └── preprocess.py
```

**İnceleme Sırası:**
1. `shared/preprocessing_utils.py` - Ortak işlevler
2. Her model klasöründe: `__init__.py` → `preprocess.py` → `predict.py`

---

## 🎨 6. FRONTEND (React TypeScript)

### Src Klasörü Yapısı:
```
src/
├── 📄 App.tsx                     # Ana React komponenti
├── 📄 App.css                     # Ana stil dosyası
├── 📄 App.test.tsx                # Ana komponent testleri
├── 📄 index.tsx                   # React giriş noktası
├── 📄 index.css                   # Global stiller
├── 📄 react-app-env.d.ts          # TypeScript tanımları
├── 📄 reportWebVitals.ts          # Performans metrikleri
├── 📄 setupTests.ts               # Test kurulumu
├── 📁 components/                 # React komponentleri
│   └── Navbar.tsx                 # Navigasyon komponenti
├── 📁 pages/                      # Sayfa komponentleri
│   ├── AboutPage.tsx              # Hakkında sayfası
│   ├── DashboardPage.tsx          # Dashboard
│   ├── HistoryPage.tsx            # Geçmiş sayfası
│   ├── HomePage.tsx               # Ana sayfa
│   ├── LoginPage.tsx              # Giriş sayfası
│   ├── RegisterPage.tsx           # Kayıt sayfası
│   ├── TestPage.tsx               # Test sayfası
│   └── TestResultPage.tsx         # Sonuç sayfası
├── 📁 types/                      # TypeScript tip tanımları
│   └── index.ts
└── 📁 utils/                      # Yardımcı fonksiyonlar
    ├── api.ts                     # API iletişimi
    └── mockData.ts                # Test verileri
```

### Public Dosyaları:
```
public/
├── 📄 index.html                  # Ana HTML şablonu
├── 📄 manifest.json               # PWA manifest
├── 📄 robots.txt                  # SEO direktifleri
├── 📄 favicon.ico                 # Site ikonu
├── 📄 logo192.png                 # App logo (192x192)
└── 📄 logo512.png                 # App logo (512x512)
```

**İnceleme Sırası:**
1. `App.tsx` → `index.tsx` → `pages/HomePage.tsx`
2. `components/Navbar.tsx` 
3. `pages/` klasöründeki diğer sayfalar
4. `utils/api.ts` → `types/index.ts`

---

## 📊 7. VERİ SETLERİ

### Data Klasörü:
```
data/
├── 📄 Breast_Cancer.csv           # Meme kanseri veri seti
├── 📄 Cardiovascular_Disease_Dataset.csv  # Kardiyovasküler veri
└── 📄 fetal_health.csv            # Fetal sağlık veri seti
```

---

## 🧪 8. TEST VE ANALİZ

### Tests Klasörü:
```
tests/
├── 📄 test_system.py              # Sistem testleri
├── 📄 test.ipynb                  # Genel test notebook
├── 📄 breast_cancer_analysis.ipynb # Meme kanseri analizi
├── 📄 card.ipynb                  # Kardiyovasküler analiz  
├── 📄 fetal_health_analysis.ipynb # Fetal sağlık analizi
└── 📄 cardiovascular_model.pkl    # Test modeli
```

**İnceleme Sırası:**
1. `test_system.py` - Sistemik testler
2. Jupyter notebook'ları - Veri analizi süreçleri

---

## �️ 9. PLATFORM DESTEĞİ

### Script Dosyaları:
- **`start.sh`** - Unix/Linux/macOS başlatma
- **`start.bat`** - Windows başlatma  
- **`clear_port.sh`** - Port temizleme aracı
- **`deploy.py`** - Otomatik dağıtım
- **`install.py`** - Kurulum ve bağımlılık yönetimi

---

## � 10. PROJE YAŞAM DÖNGÜSÜ

### Geliştirme Süreci:
1. **Veri Analizi**: `tests/*.ipynb` dosyalarında
2. **Model Geliştirme**: `model/*/` klasörlerinde  
3. **Backend API**: `backend/main.py` dosyasında
4. **Frontend UI**: `src/` klasöründe
5. **Konfigürasyon**: `config.py` dosyasında
6. **Dağıtım**: Platform scriptleri ile

---

## 🔍 11. ÖNEM SIRASI İLE İNCELEME REHBERİ

### A) Sistem Anlama (1. Gün):
1. `README.md` - Proje tanıtımı
2. `config.py` - Sistem ayarları
3. `run.py` - Başlatma mantığı
4. `tsconfig.json` - TypeScript konfigürasyonu

### B) Backend Logic (2. Gün):
1. `backend/main.py` - FastAPI ana uygulama
2. `backend/requirements.txt` - Backend bağımlılıkları
3. `model/shared/preprocessing_utils.py` - Ortak işlevler

### C) Frontend Yapısı (3. Gün):
1. `src/App.tsx` - Ana React komponenti
2. `src/pages/HomePage.tsx` - Ana sayfa
3. `src/utils/api.ts` - API iletişimi
4. `src/types/index.ts` - TypeScript tipleri

### D) Model Detayları (4. Gün):
1. Her model klasöründeki dosyalar
2. `tests/*.ipynb` - Jupyter analiz dosyaları
3. Model performans değerlendirmeleri

---

## 🎯 12. KRİTİK DOSYALAR

### En Önemli Dosyalar:
1. **`backend/main.py`** - FastAPI ana backend uygulama
2. **`src/App.tsx`** - React ana komponent
3. **`config.py`** - Tüm sistem ayarları
4. **`run.py`** - Başlatma ve port yönetimi
5. **`src/utils/api.ts`** - Frontend-Backend iletişimi
6. **`model/shared/preprocessing_utils.py`** - Ortak model araçları

### Dikkat Edilmesi Gerekenler:
- **Port Yönetimi**: Cross-platform uyumluluk
- **API İletişimi**: Frontend-Backend entegrasyonu  
- **TypeScript Tipleri**: Frontend tip güvenliği
- **Model Loading**: Dinamik model yükleme sistemi

---

## 📚 13. SONUÇ VE TAVSİYELER

### Dosya İnceleme Stratejisi:
1. **Yukarıdan Aşağıya**: README → Config → Ana uygulamalar
2. **İçten Dışa**: Core logic → API layer → UI layer
3. **Frontend-Backend Ayrımı**: React (src/) ve FastAPI (backend/)

### Son Tavsiyeler:
- Her dosyayı okumadan önce açıklamaları inceleyin
- Jupyter notebook'ları çalıştırarak veri analizi sürecini anlayın
- React frontend ve FastAPI backend'i test edin
- TypeScript tiplerini inceleyerek veri akışını anlayın
- Cross-platform script'leri test edin

---

## 🔄 14. TEKNOLOJİ STACK'İ

### Mevcut Teknolojiler:
```
Frontend:
├── React 18+ (TypeScript)
├── Modern CSS & Responsive Design  
├── User Authentication System
└── RESTful API Integration

Backend:
├── Python FastAPI
├── Scikit-learn ML Models
├── Pandas/NumPy Data Processing
└── RESTful API Design

DevOps:
├── Cross-platform Scripts
├── Automated Deployment  
└── Environment Management
```

Bu MediRisk projesi, modern web teknolojileri kullanarak tıbbi risk tahminleri yapan profesyonel bir hibrit uygulamadır. Bu rehber sayesinde projenin tüm bileşenlerini sistematik olarak anlayabilir ve etkili geliştirme yapabilirsiniz.
