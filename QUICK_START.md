# 🚀 YZTA AI-17 Hızlı Başlangıç - PACE Metodolojisi

## 🎯 PACE Projesi Özeti

Bu proje **PACE (Plan, Analyze, Construct, Execute)** metodolojisi kullanılarak geliştirilmiş 3 ayrı sağlık tahmin modelini içerir:

- 🎗️ **Breast Cancer Detection** (Binary Classification)
- 🫀 **Cardiovascular Disease Prediction** (Binary Classification)
- 👶 **Fetal Health Assessment** (Multi-class Classification)

**Önemli:** Tüm Flask bağımlılıkları kaldırılmış, sadece **FastAPI** kullanılmaktadır.

## 📋 Hızlı Başlangıç

### 1. 🧪 Modelleri Oluştur ve Test Et
```bash
# Tüm notebook'ları çalıştır ve modelleri oluştur
python run_all_notebooks.py

# Veya sadece modelleri oluştur
python create_all_models.py
```

### 2. 🚀 FastAPI Backend'i Başlat
```bash
# Backend'i başlat
python run.py

# Veya manuel olarak
cd backend
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### 3. 📡 API'yi Test Et
```bash
# API dokümantasyonu
http://localhost:8000/docs

# Health check
curl http://localhost:8000/health
```

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
