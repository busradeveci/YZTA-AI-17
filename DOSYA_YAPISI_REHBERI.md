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
├── 📄 DEVELOPMENT.md              # 3️⃣ Geliştirme talimatları
├── 📄 requirements.txt            # 4️⃣ Bağımlılıklar
├── 📄 requirements_minimal.txt    # 5️⃣ Minimal bağımlılıklar
├── 📄 config.py                   # 6️⃣ Sistem yapılandırması
├── 📄 run.py                      # 7️⃣ Ana başlatma scripti
├── 📄 deploy.py                   # 8️⃣ Dağıtım scripti
├── 📄 install.py                  # 9️⃣ Kurulum scripti
├── 📄 package.json                # 🔟 Node.js bağımlılıkları
├── 📄 tsconfig.json               # 1️⃣1️⃣ TypeScript konfigürasyonu
├── 📄 start.sh                    # 1️⃣2️⃣ Linux/macOS başlatma
├── 📄 start.bat                   # 1️⃣3️⃣ Windows başlatma
├── 📄 clear_port.sh               # 1️⃣4️⃣ Port temizleme
├── 📁 app/                        # 1️⃣5️⃣ Backend uygulama kodu
├── 📁 src/                        # 1️⃣6️⃣ Frontend React kodu
├── 📁 public/                     # 1️⃣7️⃣ Public React dosyaları
├── 📁 data/                       # 1️⃣8️⃣ Veri setleri
├── 📁 static/                     # 1️⃣9️⃣ Web arayüzü dosyaları
├── 📁 tests/                      # 2️⃣0️⃣ Test dosyaları ve analiz
└── 📁 sprintOne/                  # 2️⃣1️⃣ Sprint dokümantasyonu
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

3. **`deploy.py`** - Dağıtım scripti
   - Otomatik deployment işlemleri
   - Environment hazırlama

4. **`install.py`** - Kurulum scripti
   - Bağımlılık kurulumu
   - Sistem gereksinimlerini kontrol

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
├── 📁 model_cardiovascular/       # 2️⃣ Kardiyovasküler model
│   └── cardiovascular_model.pkl   #     Eğitilmiş model dosyası
├── 📁 model_cad/                  # 3️⃣ Koroner arter hastalığı modeli
│   ├── __init__.py
│   ├── predict.py                 #     Tahmin fonksiyonları
│   └── preprocess.py              #     Veri ön işleme
├── 📁 model_breast/               # 4️⃣ Meme kanseri modeli
│   ├── __init__.py
│   ├── predict.py
│   └── preprocess.py
└── 📁 model_fetal/                # 5️⃣ Fetal sağlık modeli
    ├── __init__.py
    ├── predict.py
    └── preprocess.py
```

---

## 🎨 5. KULLANICI ARAYÜZÜ

### Frontend (React TypeScript) İncelemesi:
```
src/
├── 📄 App.tsx                     # 1️⃣ Ana React bileşeni
├── 📄 App.css                     # 2️⃣ Ana CSS dosyası
├── 📄 index.tsx                   # 3️⃣ React giriş noktası
├── 📄 index.css                   # 4️⃣ Global CSS
├── 📄 react-app-env.d.ts          # 5️⃣ TypeScript tanımları
├── 📄 reportWebVitals.ts          # 6️⃣ Performans metrikleri
├── 📄 setupTests.ts               # 7️⃣ Test kurulumu
├── 📁 components/                 # 8️⃣ React bileşenleri
│   └── Navbar.tsx                 #     Navigasyon bileşeni
├── 📁 pages/                      # 9️⃣ Sayfa bileşenleri
│   ├── AboutPage.tsx              #     Hakkında sayfası
│   ├── HistoryPage.tsx            #     Geçmiş sayfası
│   ├── HomePage.tsx               #     Ana sayfa
│   └── TestPage.tsx               #     Test sayfası
├── 📁 types/                      # 🔟 TypeScript tipleri
│   └── index.ts                   #     Tip tanımları
└── 📁 utils/                      # 1️⃣1️⃣ Yardımcı fonksiyonlar
    ├── api.ts                     #     API iletişimi
    └── mockData.ts                #     Test verileri
```

### Public Dosyaları:
```
public/
├── 📄 index.html                  # 1️⃣ Ana HTML şablonu
├── 📄 manifest.json               # 2️⃣ PWA manifest
├── 📄 robots.txt                  # 3️⃣ Arama motoru direktifleri
├── 📄 favicon.ico                 # 4️⃣ Site ikonu
├── 📄 logo192.png                 # 5️⃣ Logo (192x192)
└── 📄 logo512.png                 # 6️⃣ Logo (512x512)
```

### Backend Web Arayüzü (Flask):
```
static/
├── 📄 style.css                   # 1️⃣ CSS stilleri (Türkçe arayüz)
└── 📄 script.js                   # 2️⃣ JavaScript (form validasyon)

app/templates/
└── 📄 index.html                  # 3️⃣ Flask HTML şablonu
```

---

## 📊 6. VERİ SETLERİ

### İnceleme Sırası:
```
data/
├── 📄 Breast_Cancer.csv                     # 1️⃣ Meme kanseri veri seti
├── � Cardiovascular_Disease_Dataset.csv    # 2️⃣ Kardiyovasküler veri
└── � fetal_health.csv                      # 3️⃣ Fetal sağlık veri
```

---

## 🧪 7. TESTLER VE ANALİZ

### İnceleme Sırası:
```
tests/
├── 📄 test_system.py                        # 1️⃣ Sistem testleri
├── 📄 test.ipynb                            # 2️⃣ Genel test notebook'u
├── 📄 breast_cancer_analysis.ipynb          # 3️⃣ Meme kanseri analiz
├── 📄 cardiovascular_model.pkl              # 4️⃣ Eğitilmiş kardiyovasküler model
├── 📄 card.ipynb                            # 5️⃣ Kardiyovasküler analiz
└── 📄 fetal_health_analysis.ipynb           # 6️⃣ Fetal sağlık analiz
```

---

## 🚀 8. PLATFORM DESTEĞİ

### İnceleme Sırası:
1. **`start.sh`** - Linux/macOS başlatma scripti
2. **`start.bat`** - Windows başlatma scripti
3. **`clear_port.sh`** - Port temizleme aracı
4. **`deploy.py`** - Otomatik dağıtım scripti
5. **`install.py`** - Kurulum ve bağımlılık yönetimi
6. **`package.json`** - Node.js/React proje yapılandırması
7. **`tsconfig.json`** - TypeScript compiler ayarları

---

## 📝 9. PROJE YAŞAM DÖNGÜSÜ İNCELEMESİ

### Geliştirme Süreci:
1. **Veri Analizi**: `tests/*.ipynb` notebook'larında
2. **Backend Model Geliştirme**: `app/model/*/` klasörlerinde
3. **Frontend React Geliştirme**: `src/` klasöründe
4. **Backend Web API**: `app/routes.py` dosyasında
5. **Konfigürasyon**: `config.py` dosyasında
6. **Dağıtım**: `deploy.py` ve platform scriptleri ile

---

## 🔍 10. DETAYLI İNCELEME REHBERİ

### Her Dosyayı İnceleme Sırası:

#### A) Sistem Anlama Aşaması:
1. `README.md` - Proje tanıtımı
2. `DEVELOPMENT.md` - Geliştirme süreci
3. `config.py` - Sistem konfigürasyonu
4. `run.py` - Başlatma mantığı
5. `app/__init__.py` - Flask factory pattern
6. `package.json` - Node.js/React yapılandırması
7. `tsconfig.json` - TypeScript ayarları

#### B) İş Mantığı Anlama:
1. `app/routes.py` - Backend API rotaları
2. `app/utils.py` - Yardımcı fonksiyonlar
3. `app/model/shared/preprocessing_utils.py` - Ortak işlevler
4. `src/utils/api.ts` - Frontend API iletişimi

#### C) Model Detayları:
1. Her model klasöründe: `__init__.py` → `preprocess.py` → `predict.py`
2. Test dosyaları: `tests/*.ipynb` (Jupyter notebook'lar)
3. Eğitilmiş modeller: `app/model_cardiovascular/cardiovascular_model.pkl`

#### D) Kullanıcı Deneyimi:
1. **React Frontend**: `src/App.tsx` → `src/pages/*.tsx` → `src/components/*.tsx`
2. **Flask Backend**: `app/templates/index.html` → `static/style.css` → `static/script.js`

---

## 📊 11. VERİ AKIŞI TAKİBİ

### Sistemdeki Veri Akışı:

#### Frontend (React) Akışı:
```
1. Kullanıcı → React Sayfası (HomePage.tsx)
2. Form → TypeScript Validasyon (src/utils/)
3. API İsteği → Backend API (src/utils/api.ts)
4. Response → React State → UI Güncelleme
```

#### Backend (Flask) Akışı:
```
1. API İsteği → Flask Routes (routes.py)
2. Routes → Model Utils (utils.py)
3. Utils → Preprocessing (model/*/preprocess.py)
4. Preprocessing → Prediction (model/*/predict.py)
5. Prediction → JSON Response → Frontend
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
- DEVELOPMENT.md
- Proje yapısını genel olarak incele

#### 2. Gün - Sistem Mimarisi:
- config.py
- run.py
- deploy.py
- install.py
- app/__init__.py

#### 3. Gün - Frontend (React):
- package.json
- tsconfig.json
- src/App.tsx
- src/pages/ klasörü
- src/components/ klasörü

#### 4. Gün - Backend (Flask):
- app/routes.py
- app/utils.py
- app/templates/index.html
- static/ dosyaları

#### 5. Gün - İş Mantığı:
- app/model/shared/preprocessing_utils.py
- Her model klasörünü sırayla incele

#### 6. Gün - Test ve Analiz:
- tests/test_system.py
- İlgili test notebook'larını çalıştır
- Model performanslarını analiz et

---

## 🎯 14. KRİTİK NOKTALARIN ANALİZİ

### Dikkat Edilmesi Gereken Dosyalar:
1. **`config.py`** - Tüm sistem ayarları burada
2. **`app/routes.py`** - Backend API endpoints
3. **`app/utils.py`** - Model yükleme ve tahmin mantığı
4. **`run.py`** - Başlatma ve port yönetimi
5. **`src/App.tsx`** - Ana React bileşeni
6. **`src/utils/api.ts`** - Frontend-Backend iletişimi
7. **`package.json`** - Node.js bağımlılıkları
8. **`tsconfig.json`** - TypeScript konfigürasyonu

### Anlaşılması Zor Olabilecek Kısımlar:
1. **PACE Metodolojisi** - Model geliştirme süreci
2. **Port Yönetimi** - Çapraz platform uyumluluk
3. **Model Factory Pattern** - Dinamik model yükleme
4. **React-Flask İletişimi** - API entegrasyonu
5. **TypeScript Tipleri** - Frontend tip güvenliği

---

## 📚 15. SONUÇ VE ÖNERİLER

### Dosya Yapısını Anlama Stratejisi:
1. **Yukarıdan Aşağıya**: README → Config → Main App
2. **İçten Dışa**: Core Logic → Web Layer → UI
3. **Kronolojik**: Geliştirme süreci sırasına göre
4. **Frontend-Backend Ayrımı**: React (src/) ve Flask (app/) katmanları

### Son Tavsiyeler:
- Her dosyayı okumadan önce açıklamaları (docstring) okuyun
- Jupyter notebook'ları çalıştırarak veri analizi sürecini anlayın
- Hem React frontend'i hem Flask backend'i test edin
- TypeScript tiplerini inceleyerek frontend-backend veri akışını anlayın
- Log dosyalarını kontrol ederek sistem davranışını anlayın

---

## 🔄 16. HİBRİT MİMARİ YAPISI

### Proje Mimarisi:
Bu proje hibrit bir yapıya sahiptir:
- **Frontend**: Modern React TypeScript SPA
- **Backend**: Python Flask REST API
- **Integration**: API tabanlı iletişim

### Teknoloji Stack'i:
```
Frontend:
├── React 18+ (TypeScript)
├── Modern CSS
├── Responsive Design
└── API Integration

Backend:
├── Python Flask
├── Scikit-learn ML Models
├── Pandas/NumPy
└── RESTful API Design

DevOps:
├── Cross-platform Scripts
├── Automated Deployment
└── Environment Management
```

Bu rehber sayesinde YZTA-AI-17 projesinin tüm bileşenlerini sistematik olarak anlayabilir ve hem frontend hem backend geliştirme süreçlerinde etkili çalışabilirsiniz.
