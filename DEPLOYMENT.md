# YZTA-AI-17 Çapraz Platform Dağıtım Kılavuzu

## 🌍 Farklı Bilgisayarlarda Çalıştırma

Bu sistem farklı işletim sistemlerinde ve bilgisayarlarda çalışacak şekilde tasarlanmıştır.

### 📋 Ön Gereksinimler
- Python 3.8 veya üzeri
- İnternet bağlantısı (ilk kurulum için)
- En az 2GB RAM
- 1GB boş disk alanı

### 🚀 Hızlı Başlangıç

#### Windows'ta:
```cmd
# 1. Dosyaları bilgisayara kopyalayın
# 2. Komut satırını açın
# 3. Proje klasörüne gidin
cd path\to\YZTA-AI-17

# 4. Çalıştırın
start.bat

# Veya direkt:
python run.py
```

#### macOS/Linux'ta:
```bash
# 1. Dosyaları bilgisayara kopyalayın
# 2. Terminal açın
# 3. Proje klasörüne gidin
cd /path/to/YZTA-AI-17

# 4. Çalıştırın
./start.sh

# Veya direkt:
python3 run.py
```

### 🔧 Kurulum Seçenekleri

#### Otomatik Kurulum (Önerilen):
```bash
python run.py --install
```

#### Manuel Kurulum:
```bash
# Virtual environment oluştur
python -m venv .venv

# Windows'ta aktifleştir:
.venv\Scripts\activate

# macOS/Linux'ta aktifleştir:
source .venv/bin/activate

# Bağımlılıkları yükle
pip install -r requirements.txt
```

### 🌐 Ağ Erişimi

#### Yerel Kullanım (Sadece bu bilgisayar):
```bash
python run.py --host 127.0.0.1
```

#### Ağ Erişimi (Diğer cihazlardan erişim):
```bash
python run.py --host 0.0.0.0
```

#### Özel Port:
```bash
python run.py --port 8080
```

### 📱 Diğer Cihazlardan Erişim

Sistem `--host 0.0.0.0` ile başlatıldığında:

1. **Bilgisayarın IP adresini bulun:**
   - Windows: `ipconfig`
   - macOS/Linux: `ifconfig` veya `ip addr`

2. **Diğer cihazlardan erişin:**
   - `http://[IP-ADRESİ]:5000`
   - Örnek: `http://192.168.1.100:5000`

3. **Mobil cihazlardan:**
   - Aynı WiFi ağında olduğunuzdan emin olun
   - Tarayıcıda IP adresini girin

### 🔒 Güvenlik

#### Güvenlik Duvarı Ayarları:
- **Windows Defender:** Port 5000'i açın
- **macOS:** Sistem Tercihleri > Güvenlik > Güvenlik Duvarı
- **Linux:** `ufw allow 5000` veya iptables kuralları

#### Güvenli Erişim:
```bash
# Sadece belirli IP'lerden erişim için nginx/apache proxy kullanın
# Veya VPN bağlantısı kurun
```

### 🐳 Docker ile Dağıtım

#### Dockerfile oluşturun:
```dockerfile
FROM python:3.12-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 5000

CMD ["python", "run.py", "--host", "0.0.0.0"]
```

#### Çalıştırın:
```bash
# Image oluştur
docker build -t yzta-ai-17 .

# Çalıştır
docker run -p 5000:5000 yzta-ai-17
```

### 🔧 Sorun Giderme

#### Port Kullanımda:
```bash
# Başka port kullan
python run.py --port 5001

# Veya otomatik port seçimi aktif (varsayılan)
python run.py
```

#### Python Bulunamadı:
```bash
# Windows'ta:
py -3 run.py

# Veya tam yol:
C:\Python39\python.exe run.py
```

#### Bağımlılık Hataları:
```bash
# Önce upgrade edin
pip install --upgrade pip

# Sonra yeniden yükleyin
pip install -r requirements.txt --force-reinstall
```

#### Ağ Erişim Problemleri:
```bash
# Güvenlik duvarını kontrol edin
# Windows'ta:
netsh advfirewall firewall add rule name="YZTA-AI-17" dir=in action=allow protocol=TCP localport=5000

# Ağ bağlantısını test edin:
python run.py --host 0.0.0.0 --debug
```

### 📋 Sistem Gereksinimleri

#### Minimum:
- CPU: 1 core, 1GHz
- RAM: 2GB
- Disk: 1GB

#### Önerilen:
- CPU: 2+ cores, 2GHz+
- RAM: 4GB+
- Disk: 2GB+
- SSD önerilir

### 🌍 Bulut Dağıtımı

#### Heroku:
```bash
# Procfile oluşturun:
echo "web: python run.py --host 0.0.0.0 --port \$PORT" > Procfile

# Git deploy:
git add .
git commit -m "Deploy to Heroku"
git push heroku main
```

#### AWS EC2:
```bash
# EC2 instance'ında:
sudo yum update -y
sudo yum install python3 python3-pip -y
git clone [your-repo]
cd YZTA-AI-17
python3 run.py --host 0.0.0.0
```

#### Google Cloud:
```bash
# App Engine için app.yaml:
runtime: python39
entrypoint: python run.py --host 0.0.0.0 --port $PORT

# Deploy:
gcloud app deploy
```

### 📞 Destek

Sorun yaşadığınızda:

1. **Log'ları kontrol edin:**
   ```bash
   python run.py --debug
   ```

2. **Sistem bilgilerini kontrol edin:**
   ```bash
   python run.py --info
   ```

3. **Test çalıştırın:**
   ```bash
   python run.py --test
   ```

4. **Yeniden başlatın:**
   ```bash
   # Mevcut serveri durdurun (Ctrl+C)
   # Portu temizleyin ve yeniden başlatın
   python run.py
   ```
