# MediRisk

## Takım İsmi
**MedOps Takımı**

## Takım Üyeleri
- [Feyzanur İnan](https://github.com/feyzann) - Scrum Master
- [Büşra Deveci](https://github.com/busradeveci) - Product Owner
- [Eren Cice](https://github.com/erencice) - Developer
- [Rabia Yaşa](https://github.com/rabiayasa4) - Developer
- [Onur Kayabaş](https://github.com/Onurkayabas1) - Developer

## Ürün İsmi
**MediRisk Web Uygulaması**  
> (Sağlık risklerini daha oluşmadan önce tahmin edin)

## Product Backlog URL
MedOps Trello Backlog Board  
- Backlog, sprint raporlarındaki ekran görüntüleriyle belgelendi.

## Ürün Açıklaması
MediRisk uygulaması; kronik böbrek hastalığı, fetal sağlık, meme kanseri ve depresyon gibi çeşitli sağlık durumları için farklı veri setlerini kullanarak, kullanıcıların kendi sağlık risklerini değerlendirmelerine olanak tanıyan bir web platformudur.  
Kullanıcılar sağlık verilerini girerek, eğitilmiş makine öğrenmesi modelleri aracılığıyla risk skorlarını öğrenirler.

## Ürün Özellikleri
- Çoklu sağlık veri setleri (Chronic Kidney Disease, Fetal Health, Breast Cancer, Student Depression)
- ML tabanlı risk tahmin modelleri
- Kullanıcı dostu arayüz
- Risk skorlarını grafiklerle görselleştirme
- Güvenli oturum yönetimi ve kullanıcı doğrulama

## Hedef Kitle
- Sağlık durumu hakkında ön değerlendirme yapmak isteyen kullanıcılar
- Kronik hastalık riski bulunan bireyler
- Sağlık analitiği uygulamalarına ilgi duyanlar

## 📊 Datasets

The project encompasses three comprehensive medical datasets for different health prediction models:

### 🫀 Cardiovascular Disease Dataset
- **Patient ID**: Unique identifier for each patient
- **Age**: Patient's age
- **Gender**: Patient's gender (1 = Male, 0 = Female)
- **Chest Pain**: Type of chest pain (0-3 scale)
- **Resting BP**: Resting blood pressure
- **Serum Cholesterol**: Serum cholesterol level
- **Fasting Blood Sugar**: Fasting blood sugar > 120 mg/dl (1 = true, 0 = false)
- **Resting Electrocardiogram**: Resting electrocardiographic results
- **Max Heart Rate**: Maximum heart rate achieved
- **Exercise Angina**: Exercise induced angina (1 = yes, 0 = no)
- **Oldpeak**: ST depression induced by exercise relative to rest
- **Slope**: Slope of the peak exercise ST segment
- **Number of Major Vessels**: Number of major vessels colored by flourosopy (0-3)
- **Target**: Cardiovascular disease diagnosis (1 = disease, 0 = no disease)

### 🎗️ Breast Cancer Dataset (Wisconsin)
- **Mean/SE/Worst Values**: For radius, texture, perimeter, area, smoothness, compactness, concavity, concave points, symmetry, fractal dimension
- **Target**: Malignant (0) or Benign (1) classification
- **Features**: 30 morphometric measurements of cell nuclei

### 👶 Fetal Health Dataset (CTG)
- **Baseline Value**: Baseline fetal heart rate
- **Accelerations**: Accelerations per second
- **Fetal Movement**: Fetal movements per second
- **Uterine Contractions**: Uterine contractions per second
- **Decelerations**: Light, severe, and prolonged decelerations
- **Variability**: Short-term and long-term variability measures
- **Histogram Features**: Width, min, max, peaks, mode, mean, median, variance, tendency
- **Target**: Normal (1), Suspect (2), Pathological (3)

## 🏗️ Project Structure

```
YZTA-AI-17/
├── app/
│   ├── __init__.py              # Flask app initialization
│   ├── routes.py                # Web application routes
│   ├── utils.py                 # Utility functions
│   ├── model/
│   │   ├── model_cad/
│   │   │   ├── __init__.py
│   │   │   ├── predict.py       # Cardiovascular prediction logic
│   │   │   └── preprocess.py    # Cardiovascular preprocessing
│   │   ├── model_breast/
│   │   │   ├── __init__.py
│   │   │   ├── predict.py       # Breast cancer prediction logic
│   │   │   └── preprocess.py    # Breast cancer preprocessing
│   │   ├── model_fetal/
│   │   │   ├── __init__.py
│   │   │   ├── predict.py       # Fetal health prediction logic
│   │   │   └── preprocess.py    # Fetal health preprocessing
│   │   └── shared/
│   │       └── preprocessing_utils.py  # Shared preprocessing utilities
│   └── templates/
│       └── index.html           # Web interface template
├── data/
│   ├── Cardiovascular_Disease_Dataset.csv  # Cardiovascular dataset
│   ├── breast_cancer/
│   │   └── breast_cancer_dataset.csv       # Breast cancer dataset
│   └── fetal_health/
│       └── fetal_health_dataset.csv        # Fetal health dataset
├── notebooks/                   # Jupyter notebooks for analysis
├── static/
│   └── style.css               # Web interface styling
├── tests/
│   ├── card.ipynb              # Cardiovascular analysis notebook
│   ├── breast_cancer_analysis.ipynb  # Breast cancer analysis notebook
│   ├── fetal_health_analysis.ipynb   # Fetal health analysis notebook
│   └── cardiovascular_model.pkl      # Trained cardiovascular model
├── config.py                   # Configuration settings
├── requirements.txt            # Python dependencies
├── run.py                      # Main application runner
├── start.sh                    # Linux/macOS startup script
├── start.bat                   # Windows startup script
├── DEPLOYMENT.md               # Cross-platform deployment guide
└── README.md                   # Project documentation
```

## 🚀 Hızlı Başlangıç

### Ön Gereksinimler
- Python 3.8+
- pip paket yöneticisi

### Otomatik Kurulum (Önerilen)
```bash
# Bağımlılıkları otomatik yükle
python run.py --install

# Sunucuyu başlat
python run.py
```

### Platform-Spesifik Başlatma

#### Windows:
```cmd
start.bat
```

#### macOS/Linux:
```bash
./start.sh
```

### Manuel Kurulum
```bash
# 1. Proje dizinine gidin
cd YZTA-AI-17

# 2. Virtual environment oluşturun (önerilen)
python -m venv .venv

# 3. Virtual environment'ı aktifleştirin
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

# 4. Bağımlılıkları yükleyin
pip install -r requirements.txt
```

### Uygulamayı Çalıştırma

```bash
# Sunucuyu başlatın
python run.py

# Debug modunda:
python run.py --debug

# Ağ erişimi için:
python run.py --host 0.0.0.0

# Özel port:
python run.py --port 8080
```

### 🌐 Erişim Adresleri
- **Yerel**: `http://localhost:5000`
- **Ağ**: `http://[IP-ADRESİNİZ]:5000`
- **Mobil**: Aynı WiFi ağında ağ adresini kullanın

### 📱 Çapraz Platform Dağıtım
Detaylı kurulum ve farklı bilgisayarlarda çalıştırma talimatları için [DEPLOYMENT.md](DEPLOYMENT.md) dosyasına bakın.

## 🔧 Kullanım

1. **Web Arayüzü**: Hasta verilerini girmek ve kardiyovasküler risk tahminleri almak için web uygulamasına erişin
2. **API Uç Noktaları**: Tahmin modeline programatik erişim için REST API'yi kullanın
3. **Jupyter Notebook'ları**: `notebooks/` dizinindeki veri analizi ve model geliştirme sürecini keşfedin

## 🧠 Model Bilgileri

Proje, farklı tıbbi tahmin görevleri için üç özelleşmiş makine öğrenmesi modeli içerir:

### 🫀 Kardiyovasküler Hastalık Modeli
- **Algoritma**: Random Forest Classifier
- **Özellikler**: 13 klinik parametre
- **Doğruluk**: ~85%
- **Kullanım**: Kardiyovasküler hastalık riski tahmini

### 🎗️ Meme Kanseri Modeli
- **Algoritma**: Support Vector Machine (SVM)
- **Özellikler**: 30 morfometrik ölçüm
- **Doğruluk**: ~95%
- **Kullanım**: Malign/benign tümör sınıflandırması

### 👶 Fetal Sağlık Modeli
- **Algoritma**: Gradient Boosting Classifier
- **Özellikler**: 21 CTG parametresi
- **Doğruluk**: ~92%
- **Kullanım**: Normal/şüpheli/patolojik fetal durum sınıflandırması

## 🛠️ Teknik Detaylar

### Teknoloji Yığını
- **Backend**: Flask (Python 3.8+)
- **Machine Learning**: scikit-learn, pandas, numpy
- **Frontend**: HTML5, CSS3, JavaScript
- **Visualization**: Chart.js
- **Database**: SQLite (geliştirme), PostgreSQL (üretim)

### API Endpoints

#### Cardiovascular Prediction
```bash
POST /api/predict/cardiovascular
Content-Type: application/json

{
  "age": 50,
  "sex": 1,
  "cp": 2,
  "trestbps": 120,
  "chol": 200,
  "fbs": 0,
  "restecg": 0,
  "thalach": 150,
  "exang": 0,
  "oldpeak": 1.0,
  "slope": 1,
  "ca": 0,
  "thal": 2
}
```

#### Breast Cancer Prediction
```bash
POST /api/predict/breast_cancer
Content-Type: application/json

{
  "mean_radius": 14.0,
  "mean_texture": 19.0,
  // ... other 28 features
}
```

#### Fetal Health Prediction
```bash
POST /api/predict/fetal_health
Content-Type: application/json

{
  "baseline_value": 120,
  "accelerations": 0.5,
  "fetal_movement": 0.3,
  // ... other 18 features
}
```

## 📊 Performans Metrikleri

### Model Değerlendirme
- Doğruluk (Accuracy)
- Hassasiyet (Precision)
- Geri çağırma (Recall)
- F1 Skoru
- ROC-AUC Skoru

### Analiz Özellikleri
- Özellik korelasyon analizi
- Model performans değerlendirmesi
- Veri görselleştirme

## 🤝 Katkıda Bulunma

1. Repository'yi fork edin
2. Feature branch oluşturun (`git checkout -b feature/AmazingFeature`)
3. Değişikliklerinizi commit edin (`git commit -m 'Add some AmazingFeature'`)
4. Branch'inizi push edin (`git push origin feature/AmazingFeature`)
5. Pull Request açın

## 🏥 Yasal Uyarı

Bu araç yalnızca eğitim ve araştırma amaçlıdır. Profesyonel tıbbi tavsiye, tanı veya tedavinin yerine geçmez. Tıbbi kararlar için her zaman nitelikli sağlık uzmanlarına danışın.

<details>
<summary> <h3> SPRINT 1 </h3> </summary>

- **Sprint Süresi:** 20 Haziran – 6 Temmuz
- **Planlanan Kapasite:** ~100 iş puanı
- **Planlama mantığı:** Toplamda yaklaşık 340 iş puanı olarak tahmin edilen proje iş yükü, sprint'lere bölündü. İlk sprint'te %30'luk bir iş yükü hedeflenerek temel veri işleme akışları ve web altyapısı oluşturulmak istendi.

---

### Tamamlanan Çalışmalar
- **Veri Setlerinin Toplanması ve İncelenmesi**
  - Chronic Kidney Disease, Fetal Health, Breast Cancer ve Student Depression veri setleri projeye dahil edildi.
  - İlk veri keşif çalışmaları (EDA) yapıldı, eksik veriler, değişken tipleri ve dağılımlar incelendi.

- **Flask Web Altyapısı**
  - Temel Flask uygulaması kuruldu.
  - Routes ve template yapısı oluşturuldu.
  - Bootstrap ile responsive tasarım entegre edildi.

- **Makine Öğrenmesi Model Geliştirme**
  - Her veri seti için temel classification algoritmaları (Random Forest, SVM, Logistic Regression) test edildi.
  - Cross-validation ile model performansları karşılaştırıldı.
  - En başarılı modeller seçildi ve pkl formatında kaydedildi.

### Sprint Review
- **Tamamlanan İş Puanı:** 95/100
- **Sprint Hedefi:** Başarıyla tamamlandı
- **Demo:** Web uygulaması temel tahmin fonksiyonları ile çalışır durumda

### Sprint Retrospective
**İyi Gidenler:**
- Takım iletişimi etkili oldu
- Veri analizi süreçleri verimli tamamlandı
- Flask altyapısı planlanan şekilde kuruldu

**Geliştirilecekler:**
- Model accuracy'lerinin artırılması gerekiyor
- UI/UX tasarımının iyileştirilmesi
- Test coverage'ının artırılması

**Öğrenilen Dersler:**
- Veri temizleme işlemlerinin model performansına büyük etkisi var
- Cross-validation önemli, overfitting'i önlüyor
- Erken prototipleme kullanıcı feedback'i için çok değerli

---

**Sprint 1 Ekran Görüntüleri:**

### App Screenshots
- [Ana Sayfa](sprintOne/app_ss/01.png)
- [Veri Girişi](sprintOne/app_ss/02.png)
- [Tahmin Sonuçları](sprintOne/app_ss/03.png)

### Trello Board Screenshots
- [Product Backlog](sprintOne/trello_ss/01.png)
- [Sprint Planning](sprintOne/trello_ss/02.png)
- [Sprint Progress](sprintOne/trello_ss/03.png)

### Wireframe Screenshots
- [Ana Sayfa Wireframe](sprintOne/wp_ss/01.png)
- [Form Sayfası Wireframe](sprintOne/wp_ss/02.png)
- [Sonuç Sayfası Wireframe](sprintOne/wp_ss/03.png)

</details>

---

## 📝 Lisans

Bu proje MIT lisansı altında lisanslanmıştır. Daha fazla bilgi için [LICENSE](LICENSE) dosyasına bakın.

## 📞 İletişim

Proje bağlantısı: [https://github.com/erencice/YZTA-AI-17](https://github.com/erencice/YZTA-AI-17)

---

**Son Güncelleme:** Temmuz 2025
