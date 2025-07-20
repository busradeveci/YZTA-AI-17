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

<details>
<summary> <h3> SPRINT 1 NOTLARI </h3> </summary>

- **Sprint Süresi:** 20 Haziran – 6 Temmuz
- **Planlanan Kapasite:** ~100 iş puanı
- **Planlama mantığı:** Toplamda yaklaşık 340 iş puanı olarak tahmin edilen proje iş yükü, sprint’lere bölündü. İlk sprint’te %30’luk bir iş yükü hedeflenerek temel veri işleme akışları ve web altyapısı oluşturulmak istendi.

---

### Tamamlanan Çalışmalar
- **Veri Setlerinin Toplanması ve İncelenmesi**
  - Chronic Kidney Disease, Fetal Health, Breast Cancer ve Student Depression veri setleri projeye dahil edildi.
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

## Sprint 2 Puanlama Sistemi

**Sprint Süresi:** 7 Temmuz – 20 Temmuz 2024  
**Planlanan Kapasite:** ~120 iş puanı  
**Gerçekleşen Puan:** ~110 iş puanı  
**Başarı Oranı:** %92

### Puanlama Mantığı

Toplam proje iş yükü yaklaşık 340 iş puanı olarak planlanmıştır.  
Sprint 1'de toplam iş yükünün %30'una denk gelen yaklaşık 100 iş puanı tamamlanmıştır.  

Sprint 2'nin öncelikli hedefleri altyapının kurulması, temel API bağlantılarının sağlanması ve kullanıcı arayüzünün şekillendirilmesidir. Bu kapsamda 120 iş puanı hedeflenmiş, 110 iş puanı başarıyla tamamlanmıştır.  

Sprint 3’te ise kalan yaklaşık 130 iş puanlık iş planlanmaktadır. Bu sprintte veritabanı entegrasyonu, üretim ortamına geçiş ve yapay zeka destekli chatbot geliştirme işleri ön planda olacaktır.

### Tamamlanan Çalışmalar

- Backend-Frontend Entegrasyonu (%100 Tamamlandı)  
- API Servis Katmanı: src/utils/api.ts ile kapsamlı API katmanı oluşturuldu  
- FastAPI Backend: backend/main.py ile modern FastAPI backend aktif hale getirildi  
  
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
