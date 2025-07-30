#!/usr/bin/env python3
"""
Otomatik Port Bulma ve Backend Başlatma Script'i
Bu script available port bulur ve backend'i otomatik olarak başlatır.
"""

import socket
import subprocess
import sys
import os
import time
import json
from pathlib import Path

def is_port_available(port):
    """Port'un kullanılabilir olup olmadığını kontrol eder"""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(1)
            result = s.connect_ex(('localhost', port))
            return result != 0
    except Exception:
        return False

def find_available_port(start_port=8000, end_port=8010):
    """Kullanılabilir port aralığında boş port bulur"""
    for port in range(start_port, end_port + 1):
        if is_port_available(port):
            return port
    return None

def update_port_config(port):
    """Port bilgisini config dosyasına yazar"""
    config_path = Path(__file__).parent / "port_config.json"
    config = {
        "port": port,
        "timestamp": time.time(),
        "host": "0.0.0.0"
    }
    
    try:
        with open(config_path, 'w') as f:
            json.dump(config, f, indent=2)
        print(f"✅ Port konfigürasyonu güncellendi: {port}")
    except Exception as e:
        print(f"⚠️  Port konfigürasyonu yazılamadı: {e}")

def start_backend(port):
    """Backend'i belirtilen port'ta başlatır"""
    try:
        print(f"🚀 Backend port {port}'da başlatılıyor...")
        
        # Update port configuration
        update_port_config(port)
        
        # Start uvicorn server
        cmd = [
            sys.executable, "-m", "uvicorn", 
            "main:app", 
            "--reload", 
            "--host", "0.0.0.0", 
            "--port", str(port)
        ]
        
        print(f"📝 Komut: {' '.join(cmd)}")
        
        # Change to backend directory
        backend_dir = Path(__file__).parent
        os.chdir(backend_dir)
        
        # Start the process
        process = subprocess.Popen(cmd)
        
        # Wait a moment to check if it started successfully
        time.sleep(2)
        
        if process.poll() is None:
            print(f"✅ Backend başarıyla başlatıldı!")
            print(f"🌐 API URL: http://localhost:{port}")
            print(f"📊 Health Check: http://localhost:{port}/")
            print(f"📚 API Docs: http://localhost:{port}/docs")
            print(f"🛑 Durdurmak için Ctrl+C tuşlayın")
            
            # Wait for the process to finish
            try:
                process.wait()
            except KeyboardInterrupt:
                print("\n🛑 Backend kapatılıyor...")
                process.terminate()
                try:
                    process.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    process.kill()
                print("✅ Backend kapatıldı")
        else:
            print("❌ Backend başlatılamadı!")
            return False
            
    except Exception as e:
        print(f"❌ Backend başlatma hatası: {e}")
        return False
    
    return True

def main():
    """Ana fonksiyon"""
    print("🔍 MediRisk Backend Otomatik Başlatıcı")
    print("=" * 50)
    
    # Find available port
    print("🔍 Kullanılabilir port aranıyor...")
    available_port = find_available_port()
    
    if available_port is None:
        print("❌ 8000-8010 aralığında kullanılabilir port bulunamadı!")
        print("💡 Mevcut port'ları kontrol edin:")
        for port in range(8000, 8011):
            if not is_port_available(port):
                print(f"   - Port {port}: ⚠️  Kullanımda")
            else:
                print(f"   - Port {port}: ✅ Kullanılabilir")
        sys.exit(1)
    
    print(f"✅ Kullanılabilir port bulundu: {available_port}")
    
    # Start backend
    success = start_backend(available_port)
    
    if not success:
        sys.exit(1)

if __name__ == "__main__":
    main()
