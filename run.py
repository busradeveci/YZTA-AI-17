#!/usr/bin/env python3
"""
YZTA-AI-17 Medical Prediction System - Run Script
================================================

This script provides an easy way to start the medical prediction system.
"""

import os
import sys
import subprocess
import argparse
import signal
import socket
from pathlib import Path
from contextlib import closing

def check_python_version():
    """Check if Python version is compatible."""
    if sys.version_info < (3, 8):
        print("❌ Error: Python 3.8 or higher is required.")
        print(f"   Current version: {sys.version}")
        return False
    return True

def find_free_port(start_port=8000, max_attempts=50):
    """Boş port bul."""
    for port in range(start_port, start_port + max_attempts):
        with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as sock:
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            try:
                sock.bind(('', port))
                return port
            except OSError:
                continue
    return None

def kill_port_process(port):
    """Belirtilen portu kullanan process'i sonlandır."""
    try:
        # macOS/Linux için lsof kullan
        result = subprocess.run(['lsof', '-ti', f':{port}'], 
                            capture_output=True, text=True)
        
        if result.returncode == 0 and result.stdout.strip():
            pids = result.stdout.strip().split('\n')
            for pid in pids:
                if pid.strip():
                    print(f"🔄 Port {port}'u kullanan process (PID: {pid}) sonlandırılıyor...")
                    try:
                        os.kill(int(pid), signal.SIGTERM)
                        print(f"✅ Process {pid} sonlandırıldı")
                    except ProcessLookupError:
                        print(f"⚠️  Process {pid} zaten sonlanmış")
                    except PermissionError:
                        print(f"❌ Process {pid} sonlandırma izni yok")
            return True
        else:
            print(f"ℹ️  Port {port} zaten boş")
            return True
            
    except FileNotFoundError:
        print("⚠️  lsof komutu bulunamadı")
        return False
    except Exception as e:
        print(f"❌ Port temizleme hatası: {e}")
        return False

def is_port_available(host='0.0.0.0', port=8000):
    """Port'un kullanılabilir olup olmadığını kontrol et."""
    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as sock:
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            sock.bind((host, port))
            return True
        except OSError:
            return False

def get_local_ip():
    """Yerel IP adresini al."""
    try:
        # Internet'e bağlanmaya çalışarak yerel IP'yi bul
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.connect(("8.8.8.8", 80))
            local_ip = s.getsockname()[0]
        return local_ip
    except Exception:
        return "127.0.0.1"

def show_access_urls(host, port, frontend_port=None):
    """Erişim URL'lerini göster."""
    print(f"\n🌐 Sunucu Erişim Adresleri:")
    
    if frontend_port:
        print(f"   Frontend (React): http://localhost:{frontend_port}")
        print(f"   Backend API:     http://localhost:{port}")
    else:
        print(f"   Yerel: http://localhost:{port}")
        print(f"   Yerel: http://127.0.0.1:{port}")
    
    if host == '0.0.0.0' and not frontend_port:
        local_ip = get_local_ip()
        print(f"   Ağ:   http://{local_ip}:{port}")
        print(f"\n📱 QR Code için: http://{local_ip}:{port}")
        print(f"💡 Diğer cihazlardan erişim için ağ IP'sini kullanın: {local_ip}")
    elif host != '127.0.0.1' and not frontend_port:
        print(f"   Ana:  http://{host}:{port}")
    
    print(f"\n🔗 Tarayıcınızda yukarıdaki adreslerden birini açın")
    print("   Sunucuyu durdurmak için Ctrl+C tuşlayın\n")
    return True

def check_frontend_dependencies():
    """Check if Node.js and npm are available for React frontend."""
    try:
        # Check Node.js
        node_result = subprocess.run(['node', '--version'], 
                                   capture_output=True, text=True)
        if node_result.returncode != 0:
            print("❌ Node.js not found")
            return False
        
        # Check npm
        npm_result = subprocess.run(['npm', '--version'], 
                                  capture_output=True, text=True)
        if npm_result.returncode != 0:
            print("❌ npm not found")
            return False
        
        # Check if package.json exists
        package_json = Path(__file__).parent / "package.json"
        if not package_json.exists():
            print("❌ package.json not found")
            return False
        
        print(f"✅ Node.js {node_result.stdout.strip()} - OK")
        print(f"✅ npm {npm_result.stdout.strip()} - OK")
        return True
        
    except FileNotFoundError:
        print("❌ Node.js/npm not found")
        return False
    except Exception as e:
        print(f"❌ Frontend dependency check failed: {e}")
        return False

def start_frontend():
    """Start React frontend in background."""
    try:
        print("🔄 Starting React frontend...")
        
        # Check if node_modules exists, if not run npm install
        node_modules = Path(__file__).parent / "node_modules"
        if not node_modules.exists():
            print("📦 Installing frontend dependencies...")
            npm_install = subprocess.run(['npm', 'install'], 
                                       cwd=Path(__file__).parent,
                                       capture_output=True, text=True)
            if npm_install.returncode != 0:
                print(f"❌ npm install failed: {npm_install.stderr}")
                return False
            print("✅ Frontend dependencies installed")
        
        # Start React development server
        subprocess.Popen(['npm', 'start'], 
                        cwd=Path(__file__).parent,
                        stdout=subprocess.DEVNULL,
                        stderr=subprocess.DEVNULL)
        
        print("✅ React frontend starting on http://localhost:3000")
        return True
        
    except Exception as e:
        print(f"❌ Failed to start frontend: {e}")
        return False

def check_dependencies(auto_install=False):
    """Check if required dependencies are installed."""
    required_packages = [
        ('fastapi', 'fastapi'),
        ('uvicorn', 'uvicorn'),
        ('pandas', 'pandas'),
        ('numpy', 'numpy'), 
        ('sklearn', 'scikit-learn'),
        ('joblib', 'joblib')
    ]
    
    missing_packages = []
    
    print("🔍 Checking dependencies...")
    for import_name, package_name in required_packages:
        try:
            __import__(import_name)
            print(f"✅ {package_name} - OK")
        except ImportError:
            missing_packages.append(package_name)
            print(f"❌ {package_name} - Missing")
    
    if missing_packages:
        if auto_install:
            print(f"\n📦 Missing packages detected: {', '.join(missing_packages)}")
            print("🔄 Installing missing dependencies automatically...")
            
            if install_dependencies():
                print("✅ Dependencies installed successfully.")
                print("🔄 Please restart the application to complete the setup.")
                print("   Run: python run.py")
                return False  # Return False to restart the application
            else:
                print("❌ Failed to install dependencies automatically.")
                print("\n💡 Try installing manually with:")
                print(f"   python run.py --install")
                return False
        else:
            print(f"\n❌ Missing required packages: {', '.join(missing_packages)}")
            print("\n💡 Install missing packages with:")
            print(f"   python run.py --install")
            print(f"   or manually: pip install {' '.join(missing_packages)}")
            return False
    
    print("\n✅ All required dependencies are installed.")
    return True

def install_dependencies():
    """Install dependencies from requirements.txt."""
    requirements_file = Path(__file__).parent / "requirements.txt"
    
    if not requirements_file.exists():
        print("❌ Error: requirements.txt not found.")
        return False
    
    try:
        print("📦 Installing dependencies...")
        
        # Use current Python executable directly
        python_exe = sys.executable
        
        cmd = [str(python_exe), "-m", "pip", "install", "-r", str(requirements_file)]
        print(f"Running: {' '.join(cmd)}")
        
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=300  # 5 minutes timeout
        )
        
        if result.returncode == 0:
            print("✅ Dependencies installed successfully.")
            # Clear import cache to force reimport of newly installed packages
            import importlib
            for module in list(sys.modules.keys()):
                if any(pkg in module for pkg in ['fastapi', 'uvicorn', 'pandas', 'numpy', 'sklearn', 'joblib']):
                    if module in sys.modules:
                        del sys.modules[module]
            return True
        else:
            print(f"❌ Error installing dependencies:")
            print(f"Return code: {result.returncode}")
            if result.stdout:
                print(f"STDOUT: {result.stdout}")
            if result.stderr:
                print(f"STDERR: {result.stderr}")
            return False
            
    except subprocess.TimeoutExpired:
        print("❌ Installation timed out after 5 minutes.")
        return False
    except Exception as e:
        print(f"❌ Unexpected error installing dependencies: {e}")
        return False

def run_fastapi_app(host='127.0.0.1', port=8000, debug=False, auto_port=True, open_browser=True):
    """FastAPI uygulamasını çalıştır."""
    try:
        # Port kontrolü ve temizleme
        if not is_port_available('0.0.0.0', port):
            print(f"⚠️  Port {port} kullanımda!")
            
            if auto_port:
                print("🔄 Port temizleniyor...")
                kill_port_process(port)
                
                # Kısa süre bekle
                import time
                time.sleep(2)
                
                # Hala kullanımda mı kontrol et
                if not is_port_available('0.0.0.0', port):
                    print(f"⚠️  Port {port} hala kullanımda, alternatif port aranıyor...")
                    free_port = find_free_port(port)
                    if free_port:
                        port = free_port
                        print(f"✅ Alternatif port bulundu: {port}")
                    else:
                        print("❌ Boş port bulunamadı!")
                        return False
                else:
                    print(f"✅ Port {port} temizlendi")
            else:
                print(f"❌ Port {port} kullanımda ve auto_port kapalı")
                return False
        
        # Check if we're in virtual environment and adjust Python path
        venv_path = Path(__file__).parent / ".venv"
        if venv_path.exists():
            # Add virtual environment to Python path
            venv_site_packages = venv_path / "lib" / "python3.12" / "site-packages"
            if venv_site_packages.exists():
                sys.path.insert(0, str(venv_site_packages))
        
        print(f"🚀 MediRisk - Tıbbi Tahmin Sistemi başlatılıyor...")
        
        # Check if Node.js and npm are available for React frontend
        frontend_available = check_frontend_dependencies()
        
        if frontend_available:
            # Start React frontend in a separate process
            start_frontend()
            frontend_port = 3000
        else:
            print("⚠️  Frontend dependencies not found. Only backend will be started.")
            frontend_port = None
        
        # Erişim URL'lerini göster
        show_access_urls(host, port, frontend_port)
        
        print("📊 Mevcut tahmin modelleri:")
        print("   - Kardiyovasküler Hastalık Tahmini")
        print("   - Meme Kanseri Teşhisi")
        print("   - Fetal Sağlık Değerlendirmesi")
        print("   Sunucuyu durdurmak için Ctrl+C tuşlayın\n")
        
        # Try to run FastAPI app with uvicorn
        try:
            import uvicorn
            
            # Tarayıcıyı otomatik aç
            if open_browser and frontend_available:
                import webbrowser
                import threading
                import time
                def open_browser_delayed():
                    time.sleep(5)  # Frontend'in başlaması için daha fazla bekle
                    webbrowser.open(f'http://localhost:3000')
                
                thread = threading.Thread(target=open_browser_delayed)
                thread.daemon = True
                thread.start()
            elif open_browser:
                import webbrowser
                import threading
                import time
                def open_browser_delayed():
                    time.sleep(2)  # Sunucunun başlaması için bekle
                    webbrowser.open(f'http://localhost:{port}')
                
                thread = threading.Thread(target=open_browser_delayed)
                thread.daemon = True
                thread.start()
            
            # FastAPI backend'i başlat
            backend_path = Path(__file__).parent / "backend"
            if backend_path.exists():
                # Backend klasörünü sys.path'e ekle
                sys.path.insert(0, str(backend_path))
                uvicorn.run(
                    "backend.main:app", 
                    host=host, 
                    port=port, 
                    reload=debug, 
                    log_level="info" if debug else "warning"
                )
            else:
                print("❌ Backend klasörü bulunamadı!")
                return False
            return True
        except ImportError as e:
            print(f"❌ FastAPI/Uvicorn yüklenemedi: {e}")
            print("💡 Bağımlılıkları kurmak için şunu çalıştırın:")
            print("   python install.py")
            print("   veya")
            print("   python run.py --install")
            return False
        except OSError as e:
            if "Address already in use" in str(e):
                print(f"❌ Port {port} hala kullanımda. Lütfen farklı bir port deneyin.")
                return False
            else:
                print(f"❌ Sunucu başlatılamadı: {e}")
                return False
        except Exception as e:
            print(f"❌ Sunucu başlatılamadı: {e}")
            return False
            
    except Exception as e:
        print(f"❌ Beklenmeyen hata: {e}")
        return False

def run_backend_only(host='127.0.0.1', port=8000, debug=False, open_browser=True):
    """Sadece FastAPI backend'ini çalıştır."""
    try:
        # Port kontrolü ve temizleme
        if not is_port_available('0.0.0.0', port):
            print(f"⚠️  Port {port} kullanımda!")
            print("🔄 Port temizleniyor...")
            kill_port_process(port)
            
            # Kısa süre bekle
            import time
            time.sleep(2)
            
            # Hala kullanımda mı kontrol et
            if not is_port_available('0.0.0.0', port):
                print(f"⚠️  Port {port} hala kullanımda, alternatif port aranıyor...")
                free_port = find_free_port(port)
                if free_port:
                    port = free_port
                    print(f"✅ Alternatif port bulundu: {port}")
                else:
                    print("❌ Boş port bulunamadı!")
                    return False
            else:
                print(f"✅ Port {port} temizlendi")
        
        print(f"🚀 MediRisk - Backend API başlatılıyor...")
        
        # Backend-only erişim URL'lerini göster
        show_access_urls(host, port, frontend_port=None)
        
        print("📊 Mevcut tahmin modelleri:")
        print("   - Kardiyovasküler Hastalık Tahmini")
        print("   - Meme Kanseri Teşhisi")
        print("   - Fetal Sağlık Değerlendirmesi")
        print("   Sunucuyu durdurmak için Ctrl+C tuşlayın\n")
        
        # Tarayıcıyı otomatik aç (backend API'ye)
        if open_browser:
            import webbrowser
            import threading
            import time
            def open_browser_delayed():
                time.sleep(2)  # Sunucunun başlaması için bekle
                webbrowser.open(f'http://localhost:{port}')
            
            thread = threading.Thread(target=open_browser_delayed)
            thread.daemon = True
            thread.start()
        
        # FastAPI backend'i başlat
        backend_path = Path(__file__).parent / "backend"
        if backend_path.exists():
            sys.path.insert(0, str(backend_path))
            import uvicorn
            uvicorn.run(
                "backend.main:app", 
                host=host, 
                port=port, 
                reload=debug, 
                log_level="info" if debug else "warning"
            )
        else:
            print("❌ Backend klasörü bulunamadı!")
            return False
        return True
        
    except Exception as e:
        print(f"❌ Backend başlatılamadı: {e}")
        return False

def run_tests():
    """Run the test suite."""
    test_file = Path(__file__).parent / "tests" / "test_system.py"
    
    if not test_file.exists():
        print("❌ Error: Test file not found.")
        return False
    
    try:
        print("🧪 Running test suite...")
        result = subprocess.run([
            sys.executable, str(test_file), "--all"
        ], capture_output=True, text=True)
        
        print(result.stdout)
        if result.stderr:
            print("Errors:", result.stderr)
        
        return result.returncode == 0
    except Exception as e:
        print(f"❌ Error running tests: {e}")
        return False

def show_system_info():
    """Show system information."""
    print("🏥 MediRisk Medical Prediction System")
    print("=" * 50)
    print(f"Python version: {sys.version}")
    print(f"Platform: {sys.platform}")
    print(f"Working directory: {os.getcwd()}")
    
    # Check if in virtual environment
    if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        print("Virtual environment: Active")
    else:
        print("Virtual environment: Not detected")
    
    # Check project structure
    project_files = [
        "backend/main.py",
        "config.py",
        "requirements.txt",
        "README.md"
    ]
    
    print("\nProject structure:")
    for file_path in project_files:
        if Path(file_path).exists():
            print(f"  ✅ {file_path}")
        else:
            print(f"  ❌ {file_path}")

def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="MediRisk Medical Prediction System Runner",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
python run.py                    # Start both frontend and backend
python run.py --backend-only     # Start only backend API
python run.py --frontend-only    # Start only React frontend
python run.py --port 8080       # Start server on port 8080
python run.py --debug           # Start server in debug mode
python run.py --install         # Install dependencies
python run.py --test            # Run tests
python run.py --info            # Show system information
        """
    )
    
    parser.add_argument('--host', default='0.0.0.0', 
                    help='Host to run the server on (default: 0.0.0.0 for network access)')
    parser.add_argument('--port', type=int, default=8000,
                    help='Port to run the server on (default: 8000)')
    parser.add_argument('--debug', action='store_true',
                    help='Run in debug mode')
    parser.add_argument('--install', action='store_true',
                    help='Install dependencies from requirements.txt')
    parser.add_argument('--test', action='store_true',
                    help='Run the test suite')
    parser.add_argument('--info', action='store_true',
                    help='Show system information')
    parser.add_argument('--check', action='store_true',
                    help='Check dependencies without starting server')
    parser.add_argument('--no-browser', action='store_true',
                    help='Do not automatically open browser')
    parser.add_argument('--frontend-only', action='store_true',
                    help='Start only the React frontend (for development)')
    parser.add_argument('--backend-only', action='store_true',
                    help='Start only the FastAPI backend')
    
    args = parser.parse_args()
    
    # Show system info
    if args.info:
        show_system_info()
        return
    
    # Install dependencies
    if args.install:
        if not check_python_version():
            return
        install_dependencies()
        return
    
    # Run tests
    if args.test:
        if not check_python_version():
            return
        if not check_dependencies(auto_install=False):
            return
        success = run_tests()
        if not success:
            sys.exit(1)
        return
    
    # Check dependencies
    if args.check:
        if not check_python_version():
            return
        if check_dependencies(auto_install=False):
            print("✅ All dependencies are satisfied.")
        return
    
    # Start frontend only
    if args.frontend_only:
        if check_frontend_dependencies():
            start_frontend()
            print("🌐 Frontend running at: http://localhost:3000")
            print("Press Ctrl+C to stop")
            try:
                import time
                while True:
                    time.sleep(1)
            except KeyboardInterrupt:
                print("\n👋 Frontend stopped.")
        return
    
    # Start server (default action or backend-only)
    if not check_python_version():
        return
    
    # Check dependencies with auto-install for production use
    if not check_dependencies(auto_install=True):
        print("\n❌ Cannot start server due to missing dependencies.")
        print("💡 If automatic installation failed, try: python run.py --install")
        return
    
    # Modify the function call based on backend-only flag
    if args.backend_only:
        # Force disable frontend for backend-only mode
        success = run_backend_only(
            host=args.host, 
            port=args.port, 
            debug=args.debug,
            open_browser=not args.no_browser
        )
    else:
        success = run_fastapi_app(
            host=args.host, 
            port=args.port, 
            debug=args.debug,
            open_browser=not args.no_browser
        )
    if not success:
        sys.exit(1)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Server stopped by user.")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        sys.exit(1)
