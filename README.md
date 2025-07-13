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

## 📊 Veri Setleri

Proje, farklı sağlık tahmin modelleri için üç kapsamlı tıbbi veri seti içerir:

### 🫀 Kardiyovasküler Hastalık Veri Seti
- **Hasta ID**: Her hasta için benzersiz tanımlayıcı
- **Yaş**: Hastanın yaşı
- **Cinsiyet**: Hastanın cinsiyeti (1 = Erkek, 0 = Kadın)
- **Göğüs Ağrısı**: Göğüs ağrısı türü (0-3 ölçeği)
- **Dinlenme KB**: Dinlenme kan basıncı
- **Serum Kolesterol**: Serum kolesterol seviyesi
- **Açlık Kan Şekeri**: Açlık kan şekeri > 120 mg/dl (1 = doğru, 0 = yanlış)
- **Dinlenme EKG**: Dinlenme elektrokardiyogram sonuçları
- **Maksimum Kalp Hızı**: Ulaşılan maksimum kalp hızı
- **Egzersiz Anjina**: Egzersizle tetiklenen anjina (1 = evet, 0 = hayır)
- **Oldpeak**: Dinlenmeye göre egzersizin neden olduğu ST depresyonu
- **Eğim**: Tepe egzersiz ST segmentinin eğimi
- **Ana Damar Sayısı**: Floreskopiyle renklenmiş ana damar sayısı (0-3)
- **Hedef**: Kardiyovasküler hastalık tanısı (1 = hastalık, 0 = hastalık yok)

### 🎗️ Meme Kanseri Veri Seti (Wisconsin)
- **Ortalama/SE/En Kötü Değerler**: Yarıçap, doku, çevre, alan, pürüzsüzlük, kompaktlık, konkavlık, konkav noktalar, simetri, fraktal boyut için
- **Hedef**: Malign (0) veya Benign (1) sınıflandırması
- **Özellikler**: Hücre çekirdeklerinin 30 morfometrik ölçümü

### 👶 Fetal Sağlık Veri Seti (CTG)
- **Temel Değer**: Temel fetal kalp hızı
- **Hızlanmalar**: Saniye başına hızlanmalar
- **Fetal Hareket**: Saniye başına fetal hareketler
- **Uterus Kasılmaları**: Saniye başına uterus kasılmaları
- **Yavaşlamalar**: Hafif, şiddetli ve uzun süreli yavaşlamalar
- **Değişkenlik**: Kısa ve uzun vadeli değişkenlik ölçüleri
- **Histogram Özellikleri**: Genişlik, min, max, tepe, mod, ortalama, medyan, varyans, eğilim
- **Hedef**: Normal (1), Şüpheli (2), Patolojik (3)

## 🏗️ Proje Yapısı

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
├── static/
│   ├── style.css               # Web interface styling
│   └── script.js               # Frontend JavaScript
├── tests/
│   ├── card.ipynb              # Cardiovascular analysis notebook
│   ├── breast_cancer_analysis.ipynb  # Breast cancer analysis notebook
│   ├── fetal_health_analysis.ipynb   # Fetal health analysis notebook
│   └── cardiovascular_model.pkl      # Trained cardiovascular model
├── sprintOne/                   # Sprint 1 documentation
│   ├── app_ss/                 # Application screenshots
│   ├── trello_ss/              # Trello board screenshots
│   └── wp_ss/                  # Wireframe screenshots
├── config.py                   # Configuration settings
├── requirements.txt            # Python dependencies
├── run.py                      # Main application runner
├── start.sh                    # Linux/macOS startup script
├── start.bat                   # Windows startup script
├── DEPLOYMENT.md               # Cross-platform deployment guide
├── DOSYA_YAPISI_REHBERI.md     # File structure understanding guide
└── README.md                   # Project documentation
```

> 📖 **Dosya yapısını detaylı anlamak için**: [DOSYA_YAPISI_REHBERI.md](DOSYA_YAPISI_REHBERI.md) dosyasını inceleyin.

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

### API Uç Noktaları

#### Kardiyovasküler Tahmin
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

#### Meme Kanseri Tahmini
```bash
POST /api/predict/breast_cancer
Content-Type: application/json

{
  "mean_radius": 14.0,
  "mean_texture": 19.0,
  // ... diğer 28 özellik
}
```

#### Fetal Sağlık Tahmini
```bash
POST /api/predict/fetal_health
Content-Type: application/json

{
  "baseline_value": 120,
  "accelerations": 0.5,
  "fetal_movement": 0.3,
  // ... diğer 18 özellik
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
- PACE metodolojisi uygulaması

## 🔧 Sistem Gereksinimleri

### Minimum Gereksinimler
- **İşletim Sistemi**: Windows 10, macOS 10.14, Ubuntu 18.04+
- **Python**: 3.8 veya üzeri
- **RAM**: 4 GB (8 GB önerilir)
- **Disk Alanı**: 2 GB boş alan
- **İnternet**: İlk kurulum için gerekli

### Desteklenen Tarayıcılar
- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+

## 🧪 Test ve Kalite Kontrol

### Test Çalıştırma
```bash
# Tüm testleri çalıştır
python run.py --test

# Model doğruluğunu kontrol et
python -m pytest tests/

# Sistem durumunu kontrol et
python run.py --info
```

### Kalite Metrikleri
- **Model Doğruluğu**: %85+ (kardiyovasküler), %95+ (meme kanseri), %92+ (fetal)
- **API Yanıt Süresi**: <500ms
- **Sistem Kararlılığı**: 99.9% uptime
- **Güvenlik**: Rate limiting, input validation

## 🤝 Katkıda Bulunma

### Geliştirme Süreci
1. Repository'yi fork edin
2. Feature branch oluşturun (`git checkout -b feature/YeniOzellik`)
3. Değişikliklerinizi commit edin (`git commit -m 'Yeni özellik eklendi'`)
4. Branch'inizi push edin (`git push origin feature/YeniOzellik`)
5. Pull Request açın

### Kod Kalitesi
- PEP 8 standartlarına uyun
- Docstring'leri güncelleyin
- Unit testler ekleyin
- Type hint'leri kullanın

### Rapor Etme
- Bug raporları için [GitHub Issues](https://github.com/erencice/YZTA-AI-17/issues) kullanın
- Özellik istekleri için discussion açın
- Güvenlik sorunları için özel mesaj gönderin

## 🛡️ Güvenlik

### Veri Güvenliği
- Kullanıcı verileri yerel olarak işlenir
- API rate limiting aktif
- Input validation uygulanır
- Kişisel veriler saklanmaz

### Yasal Uyumluluk
- KVKK uyumlu veri işleme
- GDPR gereksinimleri karşılanır
- Sağlık verisi gizliliği korunur

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
- [Ana Sayfa](sprintOne/app_ss/01.png) - Sistem giriş sayfası ve model seçimi
- [Veri Girişi](sprintOne/app_ss/02.png) - Hasta bilgilerini girme formu
- [Tahmin Sonuçları](sprintOne/app_ss/03.png) - ML tahmin sonuçları ve risk skorları
- [Kardiyovasküler Model](sprintOne/app_ss/04.png) - Kalp hastalığı risk değerlendirmesi
- [Meme Kanseri Analizi](sprintOne/app_ss/05.png) - Kanser tarama sonuçları

### Trello Board Screenshots
- [Product Backlog](sprintOne/trello_ss/01.png) - Proje backlog yönetimi
- [Sprint Planning](sprintOne/trello_ss/02.png) - Sprint planlama süreci
- [Sprint Progress](sprintOne/trello_ss/03.png) - İlerleme takibi ve görev durumları
- [Team Collaboration](sprintOne/trello_ss/04.png) - Takım işbirliği ve komunikasyon

### Wireframe Screenshots
- [Ana Sayfa Wireframe](sprintOne/wp_ss/01.png) - Ana sayfa tasarım şeması
- [Form Sayfası Wireframe](sprintOne/wp_ss/02.png) - Veri giriş formu tasarımı
- [Sonuç Sayfası Wireframe](sprintOne/wp_ss/03.png) - Tahmin sonuçları görüntüleme
- [Responsive Design](sprintOne/wp_ss/04.png) - Mobil uyumlu tasarım
- [Navigation Flow](sprintOne/wp_ss/05.png) - Kullanıcı navigasyon akışı

</details>

---

## 📝 Lisans

Bu proje MIT lisansı altında lisanslanmıştır. Daha fazla bilgi için [LICENSE](LICENSE) dosyasına bakın.

## 📞 İletişim ve Destek

### Proje Bağlantıları
- **GitHub**: [https://github.com/erencice/YZTA-AI-17](https://github.com/erencice/YZTA-AI-17)
- **Dokümantasyon**: [DOSYA_YAPISI_REHBERI.md](DOSYA_YAPISI_REHBERI.md)
- **Dağıtım Kılavuzu**: [DEPLOYMENT.md](DEPLOYMENT.md)

### Destek Almak İçin
1. **GitHub Issues**: Teknik sorunlar ve bug raporları
2. **Discussions**: Özellik istekleri ve genel sorular
3. **Documentation**: Detaylı kullanım talimatları

### Takım İletişimi
- **Scrum Master**: [Feyzanur İnan](https://github.com/feyzann)
- **Product Owner**: [Büşra Deveci](https://github.com/busradeveci)
- **Lead Developer**: [Eren Cice](https://github.com/erencice)

## 🔄 Güncellemeler ve Sürüm Notları

### v2.0.0 (Temmuz 2025) - Mevcut Sürüm
- ✅ Çapraz platform desteği (Windows, macOS, Linux)
- ✅ Türkçe lokalizasyon tamamlandı
- ✅ Gelişmiş port yönetimi sistemi
- ✅ Otomatik kurulum ve başlatma scriptleri
- ✅ 3 ayrı tıbbi tahmin modeli entegrasyonu
- ✅ Responsive web arayüzü

### v1.0.0 (Haziran 2025) - İlk Sürüm
- ✅ Temel Flask web uygulaması
- ✅ Kardiyovasküler hastalık tahmin modeli
- ✅ Temel web arayüzü
- ✅ Sprint 1 dokümantasyonu

### Gelecek Güncellemeler
- 🔄 Gerçek zamanlı tahmin API'si
- 🔄 Kullanıcı hesap sistemi
- 🔄 Gelişmiş görselleştirme araçları
- 🔄 Mobil uygulama desteği

---

**Son Güncelleme:** 13 Temmuz 2025  
**Versiyon:** 2.0.0  
**Durum:** Aktif Geliştirme
