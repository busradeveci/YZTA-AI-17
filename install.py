#!/usr/bin/env python3
"""
YZTA-AI-17 Simple Installation Script
====================================

Bu basit kurulum script'i projenin bağımlılıklarını kurar.
"""

import sys
import subprocess
import os
from pathlib import Path

def main():
    """Ana kurulum fonksiyonu."""
    print("🏥 YZTA-AI-17 Kurulum Script'i")
    print("=" * 40)
    
    # Python sürümünü kontrol et
    if sys.version_info < (3, 8):
        print(f"❌ Hata: Python 3.8 veya üstü gerekli.")
        print(f"   Mevcut sürüm: {sys.version}")
        return False
    
    print(f"✅ Python sürümü: {sys.version}")
    
    # Virtual environment oluştur
    venv_path = Path(__file__).parent / ".venv"
    
    if not venv_path.exists():
        print("📁 Virtual environment oluşturuluyor...")
        try:
            subprocess.check_call([sys.executable, "-m", "venv", str(venv_path)])
            print("✅ Virtual environment oluşturuldu.")
        except subprocess.CalledProcessError as e:
            print(f"❌ Virtual environment oluşturulamadı: {e}")
            return False
    else:
        print("✅ Virtual environment mevcut.")
    
    # Virtual environment python path'ini belirle
    if os.name == 'nt':  # Windows
        python_exe = venv_path / "Scripts" / "python.exe"
        pip_exe = venv_path / "Scripts" / "pip.exe"
    else:  # Unix/Linux/macOS
        python_exe = venv_path / "bin" / "python"
        pip_exe = venv_path / "bin" / "pip"
    
    # Pip'i güncelle
    print("📦 pip güncelleniyor...")
    try:
        subprocess.check_call([str(python_exe), "-m", "pip", "install", "--upgrade", "pip"])
        print("✅ pip güncellendi.")
    except subprocess.CalledProcessError as e:
        print(f"⚠️ pip güncellenemedi: {e}")
    
    # Requirements.txt'den paketleri kur
    requirements_file = Path(__file__).parent / "requirements.txt"
    
    if not requirements_file.exists():
        print("❌ requirements.txt dosyası bulunamadı.")
        return False
    
    print("📦 Bağımlılıklar kuruluyor...")
    print("   Bu işlem birkaç dakika sürebilir...")
    
    try:
        # Temel paketleri önce kur
        basic_packages = [
            "wheel",
            "setuptools",
            "Flask==2.3.3",
            "numpy==1.24.3",
            "pandas==2.0.3"
        ]
        
        for package in basic_packages:
            print(f"   Kuruluyor: {package}")
            subprocess.check_call([
                str(python_exe), "-m", "pip", "install", package
            ], stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
        
        # Tüm requirements'ları kur
        print("   Tüm bağımlılıklar kuruluyor...")
        result = subprocess.run([
            str(python_exe), "-m", "pip", "install", "-r", str(requirements_file)
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Tüm bağımlılıklar başarıyla kuruldu.")
        else:
            print("⚠️ Bazı paketler kurulamadı, devam ediliyor...")
            if result.stderr:
                print(f"Hatalar: {result.stderr[:500]}...")
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Kurulum hatası: {e}")
        return False
    except Exception as e:
        print(f"❌ Beklenmeyen hata: {e}")
        return False
    
    # Kurulumu test et
    print("🧪 Kurulum test ediliyor...")
    
    test_imports = [
        ("flask", "Flask"),
        ("pandas", "pandas"),
        ("numpy", "numpy"),
        ("sklearn", "scikit-learn"),
        ("joblib", "joblib")
    ]
    
    failed_imports = []
    
    for import_name, package_name in test_imports:
        try:
            subprocess.check_call([
                str(python_exe), "-c", f"import {import_name}"
            ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            print(f"   ✅ {package_name}")
        except subprocess.CalledProcessError:
            print(f"   ❌ {package_name}")
            failed_imports.append(package_name)
    
    if failed_imports:
        print(f"\n⚠️ Bazı paketler kurulamadı: {', '.join(failed_imports)}")
        print("   Manuel olarak kurmayı deneyin:")
        for package in failed_imports:
            print(f"   {str(python_exe)} -m pip install {package}")
    
    # Sonuç
    print("\n" + "=" * 40)
    print("✅ Kurulum tamamlandı!")
    print("\n🚀 Uygulamayı başlatmak için:")
    print(f"   {str(python_exe)} run.py")
    print("\n   veya:")
    print("   python run.py")
    
    return True

if __name__ == "__main__":
    try:
        success = main()
        if not success:
            sys.exit(1)
    except KeyboardInterrupt:
        print("\n\n👋 Kurulum kullanıcı tarafından durduruldu.")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Beklenmeyen hata: {e}")
        sys.exit(1)
