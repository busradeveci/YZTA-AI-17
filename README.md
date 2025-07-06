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
<summary> <h3> SPRINT 1 </h3> </summary>

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