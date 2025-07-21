# 🚀 YZTA AI-17 Hızlı Başlangıç

## 📋 Tek Komutla Başlatma

Bu proje artık tek bir komutla başlatılabilir! 

```bash
python run.py
```

Bu komut:
- ✅ Tüm Python bağımlılıklarını otomatik kontrol eder ve kurar
- ✅ Node.js/npm bağımlılıklarını otomatik kontrol eder ve kurar 
- ✅ React frontend'ini başlatır (http://localhost:3000)
- ✅ FastAPI backend'ini başlatır (http://localhost:8000)
- ✅ Tarayıcıyı otomatik açar

## 🛠️ Ön Gereksinimler

### Python (Gerekli)
- Python 3.8 veya üzeri
- pip paket yöneticisi

### Node.js (İsteğe bağlı - frontend için)
- Node.js 14 veya üzeri
- npm paket yöneticisi

Node.js yüklü değilse, sadece backend API çalışacaktır.

## 📱 Kullanım Seçenekleri

### Tam Sistem (Önerilen)
```bash
python run.py
```
- Frontend + Backend birlikte çalışır
- Ana uygulama: http://localhost:3000

### Sadece Backend
```bash
python run.py --backend-only
```
- Sadece API çalışır
- API: http://localhost:8000/docs

### Sadece Frontend
```bash
python run.py --frontend-only
```
- Sadece React uygulaması çalışır

### Özel Port
```bash
python run.py --port 8080
```

### Debug Modu
```bash
python run.py --debug
```

## 🔧 Manuel Kurulum (İsteğe bağlı)

Otomatik kurulum başarısız olursa:

```bash
# Python bağımlılıklarını kur
python run.py --install

# Node.js bağımlılıklarını kur (frontend için)
npm install
```

## ✅ Sistem Kontrolü

```bash
# Bağımlılıkları kontrol et
python run.py --check

# Sistem bilgilerini göster
python run.py --info
```

## 🚫 Sorun Giderme

### Port zaten kullanımda hatası
Sistem otomatik olarak boş port bulacaktır. Manuel olarak farklı port:
```bash
python run.py --port 9000
```

### Node.js bulunamadı
Frontend çalışmayacak, sadece backend API kullanılabilir.

### Python bağımlılık hatası
```bash
python run.py --install
```

## 📚 API Dokümantasyonu

Backend başladıktan sonra:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 🎯 Ana Özellikler

- 🫀 Kardiyovasküler Hastalık Tahmini
- 🎗️ Meme Kanseri Teşhisi
- 👶 Fetal Sağlık Değerlendirmesi
- 🤖 AI destekli tahminler
- 📊 Detaylı raporlar
- 💬 Chatbot asistanı

## 🔥 Hızlı Test

1. `python run.py` çalıştır
2. Tarayıcıda http://localhost:3000 aç
3. Hesap oluştur veya giriş yap
4. Test sayfasından birini seç
5. Form doldur ve tahminle!

---

**Not:** İlk çalıştırmada bağımlılık kurulumu nedeniyle biraz zaman alabilir. Sonraki çalıştırmalarda çok daha hızlı başlayacaktır.
