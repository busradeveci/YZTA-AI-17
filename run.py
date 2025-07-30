#!/usr/bin/env python3
"""
MediRisk AI - Hızlı Başlatıcı
Proje bağımlılıklarını kontrol eder ve otomatik olarak kurar.
"""

import sys
import os
import subprocess
import time
import webbrowser
from pathlib import Path

# ANSI renk kodları
class Colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    END = '\033[0m'

def print_banner():
    """Projenin başlangıç banner'ını yazdırır"""
    banner = f"""
{Colors.CYAN}{Colors.BOLD}
╔══════════════════════════════════════════════════════════════╗
║                    🏥 MediRisk AI Platform                   ║
║                  Hızlı Geliştirme Başlatıcısı               ║
╚══════════════════════════════════════════════════════════════╝
{Colors.END}
"""
    print(banner)

def check_python_version():
    """Python versiyonunu kontrol eder"""
    print(f"{Colors.BLUE}🐍 Python versiyonu kontrol ediliyor...{Colors.END}")
    
    if sys.version_info < (3, 8):
        print(f"{Colors.RED}❌ Hata: Python 3.8+ gerekli. Mevcut: {sys.version}{Colors.END}")
        return False
    
    print(f"{Colors.GREEN}✅ Python {sys.version_info.major}.{sys.version_info.minor} - Uygun{Colors.END}")
    return True

def check_node_version():
    """Node.js versiyonunu kontrol eder"""
    print(f"{Colors.BLUE}🟢 Node.js versiyonu kontrol ediliyor...{Colors.END}")
    
    try:
        result = subprocess.run(['node', '--version'], capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            version = result.stdout.strip()
            print(f"{Colors.GREEN}✅ Node.js {version} - Uygun{Colors.END}")
            return True
        else:
            print(f"{Colors.YELLOW}⚠️ Node.js bulunamadı veya erişilemiyor{Colors.END}")
            return False
    except (subprocess.TimeoutExpired, FileNotFoundError):
        print(f"{Colors.YELLOW}⚠️ Node.js kurulu değil veya PATH'de yok{Colors.END}")
        return False

def check_backend_dependencies():
    """Backend bağımlılıklarını kontrol eder"""
    print(f"{Colors.BLUE}📦 Backend bağımlılıkları kontrol ediliyor...{Colors.END}")
    
    backend_path = Path("backend")
    requirements_file = backend_path / "requirements.txt"
    
    if not requirements_file.exists():
        print(f"{Colors.YELLOW}⚠️ requirements.txt bulunamadı{Colors.END}")
        return False
    
    # Kritik kütüphaneleri hızlıca kontrol et
    critical_packages = ['fastapi', 'uvicorn', 'pandas', 'scikit-learn', 'numpy']
    missing_packages = []
    
    for package in critical_packages:
        try:
            __import__(package.replace('-', '_'))
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print(f"{Colors.YELLOW}⚠️ Eksik paketler: {', '.join(missing_packages)}{Colors.END}")
        return False
    
    print(f"{Colors.GREEN}✅ Backend bağımlılıkları mevcut{Colors.END}")
    return True

def check_frontend_dependencies():
    """Frontend bağımlılıklarını kontrol eder"""
    print(f"{Colors.BLUE}📦 Frontend bağımlılıkları kontrol ediliyor...{Colors.END}")
    
    node_modules = Path("node_modules")
    package_json = Path("package.json")
    
    if not package_json.exists():
        print(f"{Colors.YELLOW}⚠️ package.json bulunamadı{Colors.END}")
        return False
    
    if not node_modules.exists() or not any(node_modules.iterdir()):
        print(f"{Colors.YELLOW}⚠️ node_modules klasörü boş veya mevcut değil{Colors.END}")
        return False
    
    print(f"{Colors.GREEN}✅ Frontend bağımlılıkları mevcut{Colors.END}")
    return True

def install_backend_dependencies():
    """Backend bağımlılıklarını kurar"""
    print(f"{Colors.YELLOW}📥 Backend bağımlılıkları kuruluyor...{Colors.END}")
    
    try:
        result = subprocess.run([
            sys.executable, '-m', 'pip', 'install', '-r', 'backend/requirements.txt'
        ], timeout=300)  # 5 dakika timeout
        
        if result.returncode == 0:
            print(f"{Colors.GREEN}✅ Backend bağımlılıkları başarıyla kuruldu{Colors.END}")
            return True
        else:
            print(f"{Colors.RED}❌ Backend bağımlılıkları kurulamadı{Colors.END}")
            return False
    except subprocess.TimeoutExpired:
        print(f"{Colors.RED}❌ Backend kurulumu zaman aşımına uğradı{Colors.END}")
        return False

def install_frontend_dependencies():
    """Frontend bağımlılıklarını kurar"""
    print(f"{Colors.YELLOW}📥 Frontend bağımlılıkları kuruluyor...{Colors.END}")
    
    try:
        result = subprocess.run(['npm', 'install'], timeout=300)  # 5 dakika timeout
        
        if result.returncode == 0:
            print(f"{Colors.GREEN}✅ Frontend bağımlılıkları başarıyla kuruldu{Colors.END}")
            return True
        else:
            print(f"{Colors.RED}❌ Frontend bağımlılıkları kurulamadı{Colors.END}")
            return False
    except subprocess.TimeoutExpired:
        print(f"{Colors.RED}❌ Frontend kurulumu zaman aşımına uğradı{Colors.END}")
        return False

def start_services():
    """Servisleri başlatır"""
    print(f"{Colors.CYAN}{Colors.BOLD}🚀 Servisler otomatik olarak başlatılıyor...{Colors.END}")
    
    # Backend başlat
    print(f"{Colors.BLUE}🔧 Backend başlatılıyor...{Colors.END}")
    backend_cmd = [sys.executable, 'backend/auto_start.py']
    backend_process = subprocess.Popen(backend_cmd, cwd='.', 
                                     stdout=subprocess.DEVNULL, 
                                     stderr=subprocess.DEVNULL)
    
    # Backend'in başlaması için bekle
    print(f"{Colors.YELLOW}⏳ Backend başlatılması bekleniyor (3 saniye)...{Colors.END}")
    time.sleep(3)
    
    # Frontend başlat
    print(f"{Colors.BLUE}🌐 Frontend başlatılıyor...{Colors.END}")
    frontend_env = os.environ.copy()
    frontend_env['PORT'] = '3001'
    frontend_cmd = ['npm', 'start']
    frontend_process = subprocess.Popen(frontend_cmd, env=frontend_env, cwd='.', 
                                      stdout=subprocess.DEVNULL, 
                                      stderr=subprocess.DEVNULL)
    
    # Frontend'in başlaması için bekle
    print(f"{Colors.YELLOW}⏳ Frontend derleniyor (10 saniye)...{Colors.END}")
    time.sleep(10)
    
    # Tarayıcıyı aç
    try:
        print(f"{Colors.CYAN}🌐 Tarayıcı açılıyor: http://localhost:3001{Colors.END}")
        webbrowser.open('http://localhost:3001')
    except Exception as e:
        print(f"{Colors.YELLOW}⚠️ Tarayıcı açılamadı: {str(e)}{Colors.END}")
    
    print(f"""
{Colors.GREEN}{Colors.BOLD}✅ MediRisk AI Platform başarıyla başlatıldı!{Colors.END}

📊 Backend API:  http://localhost:8000
   - Health:     http://localhost:8000/
   - Docs:       http://localhost:8000/docs

🌐 Frontend App: http://localhost:3001

{Colors.YELLOW}💡 İpucu: Durdurmak için Ctrl+C tuşlayın{Colors.END}
{Colors.MAGENTA}🎉 Platform kullanıma hazır!{Colors.END}
""")
    
    try:
        # Process'leri bekle
        while True:
            if backend_process.poll() is not None or frontend_process.poll() is not None:
                print(f"{Colors.RED}❌ Bir servis beklenmedik şekilde durdu{Colors.END}")
                break
            time.sleep(1)
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}🛑 Servisler durduruluyor...{Colors.END}")
        backend_process.terminate()
        frontend_process.terminate()
        
        # Process'lerin temizlenmesini bekle
        time.sleep(2)
        
        # Force kill if still running
        try:
            backend_process.kill()
            frontend_process.kill()
        except:
            pass
            
        print(f"{Colors.GREEN}✅ Tüm servisler durduruldu{Colors.END}")

def show_quick_commands():
    """Hızlı komutları gösterir"""
    commands = f"""
{Colors.CYAN}{Colors.BOLD}⚡ Hızlı Komutlar:{Colors.END}

{Colors.YELLOW}Sadece Backend:{Colors.END}
  cd backend && python auto_start.py

{Colors.YELLOW}Sadece Frontend:{Colors.END}
  npm start

{Colors.YELLOW}Production Build:{Colors.END}
  npm run build

{Colors.YELLOW}Test:{Colors.END}
  cd backend && python -m pytest
  npm test
"""
    print(commands)

def main():
    """Ana fonksiyon - Otomatik başlatma modu"""
    start_time = time.time()
    
    print_banner()
    
    # Hızlı kontroller
    if not check_python_version():
        sys.exit(1)
    
    has_node = check_node_version()
    has_backend_deps = check_backend_dependencies()
    has_frontend_deps = check_frontend_dependencies() if has_node else False
    
    # Eksik bağımlılıkları kur
    need_install = False
    
    if not has_backend_deps:
        print(f"{Colors.YELLOW}🔄 Backend bağımlılıkları eksik, otomatik kuruluyor...{Colors.END}")
        if not install_backend_dependencies():
            print(f"{Colors.RED}❌ Backend kurulumu başarısız{Colors.END}")
            sys.exit(1)
        need_install = True
    
    if has_node and not has_frontend_deps:
        print(f"{Colors.YELLOW}🔄 Frontend bağımlılıkları eksik, otomatik kuruluyor...{Colors.END}")
        if not install_frontend_dependencies():
            print(f"{Colors.RED}❌ Frontend kurulumu başarısız, sadece backend başlatılacak{Colors.END}")
            has_node = False
    
    elapsed_time = time.time() - start_time
    
    if need_install:
        print(f"{Colors.GREEN}✅ Otomatik kurulum tamamlandı ({elapsed_time:.1f}s){Colors.END}")
    else:
        print(f"{Colors.GREEN}✅ Tüm bağımlılıklar hazır ({elapsed_time:.1f}s){Colors.END}")
    
    # Node.js yoksa sadece backend'i başlat
    if not has_node:
        print(f"{Colors.BLUE}🔧 Sadece Backend başlatılıyor (Node.js bulunamadı)...{Colors.END}")
        subprocess.run([sys.executable, 'backend/auto_start.py'])
        return
    
    # Otomatik olarak tüm servisleri başlat
    print(f"{Colors.MAGENTA}🎯 Otomatik mod: Tüm servisler başlatılıyor...{Colors.END}")
    start_services()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}🛑 İşlem kullanıcı tarafından iptal edildi{Colors.END}")
        sys.exit(0)
    except Exception as e:
        print(f"{Colors.RED}❌ Beklenmeyen hata: {str(e)}{Colors.END}")
        sys.exit(1)
