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

def find_free_port(start_port=5000, max_attempts=50):
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

def is_port_available(host='0.0.0.0', port=5000):
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

def show_access_urls(host, port):
    """Erişim URL'lerini göster."""
    print(f"\n🌐 Sunucu Erişim Adresleri:")
    print(f"   Yerel: http://localhost:{port}")
    print(f"   Yerel: http://127.0.0.1:{port}")
    
    if host == '0.0.0.0':
        local_ip = get_local_ip()
        print(f"   Ağ:   http://{local_ip}:{port}")
        print(f"\n📱 QR Code için: http://{local_ip}:{port}")
        print(f"💡 Diğer cihazlardan erişim için ağ IP'sini kullanın: {local_ip}")
    else:
        print(f"   Ana:  http://{host}:{port}")
    
    print(f"\n🔗 Tarayıcınızda yukarıdaki adreslerden birini açın")
    print("   Sunucuyu durdurmak için Ctrl+C tuşlayın\n")
    return True

def check_dependencies():
    """Check if required dependencies are installed."""
    required_packages = [
        ('flask', 'Flask'),
        ('pandas', 'pandas'),
        ('numpy', 'numpy'), 
        ('sklearn', 'scikit-learn'),
        ('joblib', 'joblib')
    ]
    
    missing_packages = []
    
    for import_name, package_name in required_packages:
        try:
            __import__(import_name)
            print(f"✅ {package_name} - OK")
        except ImportError:
            missing_packages.append(package_name)
            print(f"❌ {package_name} - Missing")
    
    if missing_packages:
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
        
        # Check if we're in a virtual environment
        venv_path = Path(__file__).parent / ".venv"
        if venv_path.exists():
            # Use virtual environment python
            python_exe = venv_path / "bin" / "python"
            if not python_exe.exists():
                python_exe = venv_path / "Scripts" / "python.exe"  # Windows
        else:
            # Use system python
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

def run_flask_app(host='127.0.0.1', port=5000, debug=False, auto_port=True, open_browser=True):
    """Flask uygulamasını çalıştır."""
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
        
        os.environ['FLASK_APP'] = 'app'
        
        if debug:
            os.environ['FLASK_ENV'] = 'development'
            os.environ['FLASK_DEBUG'] = '1'
        
        print(f"🚀 YZTA-AI-17 Tıbbi Tahmin Sistemi başlatılıyor...")
        
        # Erişim URL'lerini göster
        show_access_urls(host, port)
        
        print("📊 Mevcut tahmin modelleri:")
        print("   - Kardiyovasküler Hastalık Tahmini")
        print("   - Meme Kanseri Teşhisi")
        print("   - Fetal Sağlık Değerlendirmesi")
        print("   Sunucuyu durdurmak için Ctrl+C tuşlayın\n")
        
        # Try to import and run the Flask app
        try:
            from app import create_app
            app = create_app()
            
            # Tarayıcıyı otomatik aç
            if open_browser:
                import webbrowser
                import threading
                import time
                def open_browser_delayed():
                    time.sleep(1.5)  # Sunucunun başlaması için bekle
                    webbrowser.open(f'http://localhost:{port}')
                
                thread = threading.Thread(target=open_browser_delayed)
                thread.daemon = True
                thread.start()
            
            app.run(host=host, port=port, debug=debug, use_reloader=False)
            return True
        except ImportError as e:
            print(f"❌ Flask uygulaması yüklenemedi: {e}")
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
    print("🏥 YZTA-AI-17 Medical Prediction System")
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
        "app/__init__.py",
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
        description="YZTA-AI-17 Medical Prediction System Runner",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python run.py                    # Start server with default settings
  python run.py --port 8080       # Start server on port 8080
  python run.py --debug           # Start server in debug mode
  python run.py --install         # Install dependencies
  python run.py --test            # Run tests
  python run.py --info            # Show system information
        """
    )
    
    parser.add_argument('--host', default='0.0.0.0', 
                       help='Host to run the server on (default: 0.0.0.0 for network access)')
    parser.add_argument('--port', type=int, default=5000,
                       help='Port to run the server on (default: 5000)')
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
        if not check_dependencies():
            return
        success = run_tests()
        if not success:
            sys.exit(1)
        return
    
    # Check dependencies
    if args.check:
        if not check_python_version():
            return
        if check_dependencies():
            print("✅ All dependencies are satisfied.")
        return
    
    # Start server (default action)
    if not check_python_version():
        return
    
    if not check_dependencies():
        print("\n💡 Try running: python run.py --install")
        return
    
    success = run_flask_app(
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
