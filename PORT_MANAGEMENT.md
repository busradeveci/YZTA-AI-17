# YZTA-AI-17 - Port Çakışması Otomatik Çözümü

## 🚀 Uygulamayı Başlatma

### Seçenek 1: Sadece Backend (Önerilen)
```bash
python run.py
```

### Seçenek 2: Full Stack (Backend + Frontend)
```bash
# Terminal 1 - Backend
python run.py

# Terminal 2 - Frontend  
PORT=3001 npm start
```

### Seçenek 3: Otomatik Script
```bash
./start.sh
```

## 🔧 Port Çakışması Çözümü

`run.py` scripti artık otomatik olarak port çakışmalarını çözer:

1. **Port 8000 müsait ise**: Normal şekilde port 8000'de başlar
2. **Port 8000 kullanımda ise**: 
   - Önce mevcut process'i sonlandırmaya çalışır
   - Başarısız olursa port 8001-8020 arasında müsait port bulur
   - package.json proxy'sini otomatik günceller

## 📱 Erişim Adresleri

- **Frontend**: http://localhost:3001
- **Backend**: http://localhost:8000 (veya müsait olan port)
- **API Docs**: http://localhost:8000/docs (veya müsait olan port)

## ⚡ Özellikler

- ✅ Otomatik port çakışması çözümü
- ✅ Mevcut process sonlandırma
- ✅ Alternatif port bulma (8001-8020)
- ✅ package.json proxy otomatik güncelleme
- ✅ Kullanıcı dostu hata mesajları
- ✅ 3 ML model otomatik yükleme

## 🛠 Sorun Giderme

**Port çakışması devam ederse:**
```bash
# Tüm ilgili process'leri manuel olarak sonlandır
pkill -f "python run.py"
pkill -f "uvicorn"
lsof -ti:8000 | xargs kill -9

# Sonra tekrar başlat
python run.py
```

**Frontend bağlantı sorunu:**
- Backend'in çalıştığı portu kontrol edin
- package.json'daki proxy ayarının doğru olduğundan emin olun
- Browser cache'ini temizleyin (Ctrl+Shift+R)
