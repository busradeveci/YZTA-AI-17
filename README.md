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
MediRisk uygulaması; kronik böbrek hastalığı, fetal sağlık ve meme kanseri gibi çeşitli sağlık durumları için farklı veri setlerini kullanarak, kullanıcıların kendi sağlık risklerini değerlendirmelerine olanak tanıyan bir web platformudur.  
Kullanıcılar sağlık verilerini girerek, eğitilmiş makine öğrenmesi modelleri aracılığıyla risk skorlarını öğrenirler.

## Gereksinimler

### Sistem Gereksinimleri
- **Python:** 3.8 veya üzeri
- **Node.js:** 14.0 veya üzeri
- **NPM:** 6.0 veya üzeri

### Backend Dependencies (Python)
```txt
fastapi==0.104.1
uvicorn[standard]==0.24.0
pydantic==2.5.0
pandas>=2.0.0
numpy>=1.24.0
scikit-learn>=1.3.0
python-multipart==0.0.6
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
sqlalchemy==2.0.23
alembic==1.13.1
psycopg2-binary==2.9.9
python-dotenv==1.0.0
requests==2.31.0
joblib==1.3.2
aiohttp==3.9.1
google-generativeai>=0.3.0
```

### Frontend Dependencies (React)
```json
{
  "@emotion/react": "^11.14.0",
  "@emotion/styled": "^11.14.1",
  "@mui/icons-material": "^7.2.0",
  "@mui/material": "^7.2.0",
  "@types/jspdf": "^1.3.3",
  "axios": "^0.27.2",
  "html2canvas": "^1.4.1",
  "jspdf": "^3.0.1",
  "react": "^18.2.0",
  "react-dom": "^18.2.0",
  "react-router-dom": "^6.3.0",
  "react-scripts": "5.0.1",
  "typescript": "^4.7.4"
}
```

### Hızlı Başlangıç
```bash
# 1. Projeyi klonlayın
git clone https://github.com/busradeveci/YZTA-AI-17.git
cd YZTA-AI-17

# 2. Otomatik kurulum ve başlatma
python run.py

# Manuel kurulum için:
# Backend: pip install -r backend/requirements.txt
# Frontend: npm install && npm start

# Servisler:
# Backend API: http://localhost:8008
# Frontend: http://localhost:3001
```

## Ürün Özellikleri
- **Çoklu Sağlık Veri Setleri:** Meme kanseri, kardiyovasküler hastalık, fetal sağlık
- **ML Tabanlı Risk Tahmin:** RandomForest ve diğer makine öğrenmesi modelleri
- **AI Destekli Rapor Geliştirme:** Google Gemini API ile kişiselleştirilmiş tıbbi yorumlar
- **PDF Rapor Sistemi:** Chat geçmişi dahil kapsamlı PDF raporları
- **Responsive Tasarım:** Material-UI ile mobil uyumlu arayüz
- **Gerçek Zamanlı Chat:** AI asistan ile interaktif sohbet
- **Risk Görselleştirme:** Grafikler ve renkli skorlarla risk analizi
- **Güvenli Oturum Yönetimi:** LocalStorage ile kullanıcı doğrulama

## Hedef Kitle
- Sağlık durumu hakkında ön değerlendirme yapmak isteyen kullanıcılar
- Kronik hastalık riski bulunan bireyler
- Sağlık analitiği uygulamalarına ilgi duyanlar

<details>
<summary> <h3> SPRINT 1 NOTLARI </h3> </summary>

- **Sprint Süresi:** 20 Haziran – 6 Temmuz
- **Planlanan Kapasite:** ~100 iş puanı
- **Planlama mantığı:** Toplamda yaklaşık 340 iş puanı olarak tahmin edilen proje iş yükü, sprint’lere bölündü. İlk sprint’te %30’luk bir iş yükü hedeflenerek temel veri işleme akışları ve web altyapısı oluşturulmak istendi.

---

### Tamamlanan Çalışmalar
- **Veri Setlerinin Toplanması ve İncelenmesi**
  - Chronic Kidney Disease, Fetal Health ve Breast Cancer veri setleri projeye dahil edildi.
  - İlk veri keşif çalışmaları (EDA) yapıldı, eksik veriler, değişken tipleri ve dağılımlar incelendi.

- **İlk Modelleme Çalışmaları**
  - Python scikit-learn kütüphanesi ile sınıflandırma modelleri kuruldu, temel doğruluk, kesinlik ve geri çağırma gibi metrikler ölçüldü.
  - Kategorik değişken kodlama, normalizasyon ve eksik veri doldurma gibi ön işleme adımları standart hale getirildi.

- **Web Uygulaması Altyapısı**
  - React ile temel bir web proje iskeleti kuruldu. Ana yönlendirmeler (routing) ve sayfa yapısı oluşturuldu.
  - Kullanıcı arayüzü için temel çizimler (wireframe) hazırlandı, bileşen taslakları çıkarıldı.

---

### Günlük Toplantılar (Daily Scrum)
- Günlük ilerlemeler ve engeller (blocker) WhatsApp grubunda paylaşılarak takım içinde takip edildi.
-  [WhatsApp görsellerine git](./sprintOne/wp_ss)

---

### Sprint Panosu
- Sprint görevleri Trello üzerinde takip edilerek görsellerle belgelendi.
-  [Trello görsellerine git](./sprintOne/trello_ss)

---

### Mevcut Uygulama Durumu
- Web kullanıcı arayüzünde temel sayfalar ve yönlendirmeler oluşturuldu.
- Makine öğrenmesi API’leri için temel sözleşmeler (endpoint planı) belirlendi.
-  [Web görsellerine git](./sprintOne/app_ss)

---

### Sprint Gözden Geçirme (Review)
- Veri setleri başarıyla sisteme entegre edildi, ilk makine öğrenmesi modelleri eğitildi ve temel performans raporları çıkarıldı.
- Frontend (React) ve backend (FastAPI + scikit-learn) teknolojilerine kesin olarak karar verildi.
- Son toplantıda, bir sonraki sprint için öncelikli işlerin tahmin ve veri tahmin servisleri olmasına karar verildi.

---

### Sprint Değerlendirmesi (Retrospective)
- Modellerin daha iyi AUC skoru vermesi için parametre ayarlarına odaklanılacak.
- Web özelliklerinin daha hızlı tamamlanabilmesi için haftasonu ek geliştirme oturumları yapılacak.
- Test kapsamının artırılması ve sürekli entegrasyon (CI) süreçlerinin başlatılması için backlog’a yeni işler eklendi.

---

## Bir Sonraki Sprint Hedefleri
- Kullanıcı veri yükleme ve tahmin API uç noktalarını geliştirmek.
- Eğitim modellerinin kapsamlı testlerini yaparak doğruluk ve güvenilirliklerini sağlamak.
- Kullanıcı risk skorlarını grafiklerle görselleştirecek bileşenleri oluşturmak.
- Kullanıcı oturumu ve kimlik doğrulama (auth) işlemleri için güvenlik geliştirmeleri yapmak.

---

## Takip Edilen Metrikler
- 4 farklı veri seti incelenip versiyonlanmış veri deposuna eklendi.
- İlk modeller eğitildi ve performans metrikleri kaydedildi.
- Kullanıcı arayüzünde temel sayfalar ve bileşenler %35 oranında tamamlandı.

</details>

<details>
<summary> <h3> SPRINT 2 NOTLARI </h3> </summary>

- **Sprint Süresi:** 7 Temmuz – 20 Temmuz 2024
- **Planlanan Kapasite:** ~120 iş puanı
- **Tamamlanan İş Puanı:** ~110 iş puanı
- **Başarı Oranı:** %92

---

### Tamamlanan Çalışmalar

#### Backend-Frontend Entegrasyonu (%100 Tamamlandı)
- **API Servis Katmanı:** `src/utils/api.ts` ile kapsamlı API katmanı oluşturuldu
- **FastAPI Backend:** `backend/main.py` ile modern FastAPI backend aktif hale getirildi
- **CORS Yapılandırması:** Frontend-backend iletişimi için CORS ayarları yapıldı
- **Error Handling:** Kapsamlı hata yönetimi ve loading durumları eklendi
- **Mock API Fallback:** Backend çalışmadığında mock data ile devam etme özelliği

#### Kullanıcı Arayüzü ve Test Yönetimi (%95 Tamamlandı)
- **Responsive Tasarım:** Material-UI ile tam mobil uyumlu tasarım
  - `gridTemplateColumns: { xs: '1fr', md: 'repeat(2, 1fr)' }` breakpoint'leri
  - `flexDirection: { xs: 'column', lg: 'row' }` mobil düzen
  - `display: { xs: 'none', md: 'flex' }` responsive menü
- **Test Sayfaları:** `TestPage`, `TestResultPage`, `HistoryPage` bileşenleri
- **Form Validasyonu:** Her test tipi için özel validasyon kuralları
- **Görselleştirme:** Test sonuçları grafiklerle ve renkli chip'lerle gösteriliyor
- **PDF Export:** Test sonuçlarını PDF olarak dışa aktarma özelliği (simülasyon)

#### Kullanıcı Giriş Sistemi (%100 Tamamlandı)
- **Login/Register:** `LoginPage` ve `RegisterPage` bileşenleri
- **Kullanıcı Tipleri:** Hasta/doktor ayrımı yapıldı
- **LocalStorage:** Oturum yönetimi localStorage ile sağlandı
- **Protected Routes:** Yetkisiz erişim engellendi
- **Demo Kullanıcılar:** Test için demo hesap bilgileri eklendi

#### Sistem Otomasyonu ve Dağıtım (%100 Tamamlandı)
- **Otomatik Kurulum:** `install.py` ile tek komutla kurulum
- **Dağıtım Scripti:** `deploy.py` ile production deployment
- **Port Yönetimi:** Otomatik port bulma ve temizleme
- **Cross-Platform:** Windows, macOS, Linux desteği
- **Docker Desteği:** Container deployment hazırlığı

#### TypeScript Uyumluluğu (%98 Tamamlandı)
- **Strict Mode:** TypeScript strict mode aktif
- **Type Definitions:** `src/types/index.ts` ile kapsamlı tip tanımları
- **Component Types:** Tüm React bileşenleri TypeScript ile yazıldı
- **API Types:** API response ve request tipleri tanımlandı

---

### Sprint 2 Görsel Belgeleri

#### Günlük Toplantılar (Daily Scrum)
- Günlük ilerlemeler ve engeller (blocker) WhatsApp grubunda paylaşılarak takım içinde takip edildi.
- [WhatsApp görsellerine git](./sprintTwo/wp_ss)

#### Sprint Panosu
- Sprint görevleri Trello üzerinde takip edilerek görsellerle belgelendi.
- [Trello görsellerine git](./sprintTwo/trello_ss)

#### Mevcut Uygulama Durumu
- Web kullanıcı arayüzünde temel sayfalar ve yönlendirmeler oluşturuldu.
- Makine öğrenmesi API’leri için temel sözleşmeler belirlendi.
- [Web görsellerine git](./sprintTwo/app_ss)

---

### Teknik Detaylar

#### Backend (FastAPI)
```python
# backend/main.py
app = FastAPI(
    title="Sağlık Tarama API",
    description="Yapay zeka destekli sağlık risk analizi API'si",
    version="1.0.0"
)

# CORS ayarları
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

#### Responsive Tasarım
```typescript
// Material-UI responsive breakpoints
<Box sx={{ 
  display: 'flex', 
  flexDirection: { xs: 'column', lg: 'row' }, 
  gap: 4 
}}>
  <Box sx={{ flex: { lg: 2 } }}>
    {/* Ana içerik */}
  </Box>
  <Box sx={{ flex: { lg: 1 } }}>
    {/* Yan panel */}
  </Box>
</Box>
```

---

### Test Edilen Özellikler

#### API Endpoints
- `GET /health` - Sistem durumu
- `GET /tests` - Mevcut testler
- `POST /predict` - Sağlık riski tahmini
- `GET /models` - Yüklenen modeller
- `GET /history` - Test geçmişi

#### Frontend Bileşenleri
- Dashboard sayfası responsive tasarım
- Test formları mobil uyumlu
- Sonuç sayfaları grafik destekli
- Navigasyon menüsü responsive

#### Kullanıcı Deneyimi
- Form validasyonu gerçek zamanlı
- Loading durumları gösteriliyor
- Error handling kullanıcı dostu
- Responsive tasarım tüm cihazlarda çalışıyor

---

### Eksik Kalan İşler

#### Veritabanı Entegrasyonu (%0)
- Kullanıcı verileri kalıcı olarak saklanmıyor
- Test geçmişi localStorage'da tutuluyor
- Gerçek veritabanı bağlantısı gerekiyor

#### Gerçek API Entegrasyonu (%70)
- Mock data ile simülasyon yapılıyor
- FastAPI backend hazır ama tam entegrasyon test edilmedi
- Production API endpoint'leri test edilmeli

#### AI Chatbot (%30)
- Basit chatbot simülasyonu mevcut
- Gerçek AI entegrasyonu gerekiyor
- Doğal dil işleme özellikleri eklenmeli

---

### Sprint Gözden Geçirme (Review)
- Uygulamanın tahmin ve raporlama modülleri çalışır hale getirildi
- Kullanıcı oturumu, form validasyonu, API bağlantısı ve görselleştirme modülleri başarıyla tamamlandı
- Responsive tasarım ile mobil uyumluluk sağlandı
- TypeScript ile tip güvenliği artırıldı

---

### Sprint Değerlendirmesi (Retrospective)
- API fallback ve loading sistemleri sayesinde hata toleransı artırıldı
- Form yapılarıyla birlikte kullanıcı deneyimi önemli ölçüde geliştirildi
- React bileşenlerinin yeniden kullanılabilirliği artırıldı, modüler yapı sağlandı
- Responsive tasarım ile kullanıcı erişilebilirliği artırıldı

---

## Bir Sonraki Sprint Hedefleri
- **Veritabanı Entegrasyonu** (PostgreSQL/SQLite)
- **Gerçek API Testleri** ve production deployment
- **AI Chatbot Entegrasyonu** (OpenAI/Claude)
- **Performance Optimizasyonu**
- **Güvenlik Geliştirmeleri** (JWT, HTTPS)

---

## Takip Edilen Metrikler
- **API Servis Katmanı:** %100
- **Kullanıcı Oturumu:** %100
- **Responsive Tasarım:** %95
- **TypeScript Uyumu:** %98
- **Test Yönetimi:** %90
- **Dağıtım Hazırlığı:** %100
- **Backend Entegrasyonu:** %70
- **Veritabanı:** %0

## Sonuç

Sprint 2 başarıyla tamamlandı. Temel sistem altyapısı hazır, kullanıcı arayüzü responsive ve modern. Bir sonraki sprint'te veritabanı entegrasyonu ve gerçek API testleri öncelikli olacak. 

</details>