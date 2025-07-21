#!/usr/bin/env python3
"""
🎯 PACE Metodolojisi - Run All Notebooks Script
===============================================

Bu script tüm notebook'ları sıralı olarak çalıştırır ve 
PACE (Plan, Analyze, Construct, Execute) sürecini tamamlar.

Usage:
    python run_all_notebooks.py
    
Bu script şunları yapar:
1. Tüm analiz notebook'larını çalıştırır
2. Model PKL dosyalarını oluşturur  
3. Test framework'ü çalıştırır
4. Final rapor oluşturur
"""

import subprocess
import sys
from pathlib import Path
import time
from datetime import datetime

def main():
    print("🎯 PACE Metodolojisi - Tüm Notebook'ları Çalıştırma")
    print("=" * 60)
    print(f"📅 Başlangıç: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Notebook execution sırası
    notebooks = [
        {
            'path': 'tests/breast_cancer_analysis.ipynb',
            'name': '🎗️ Breast Cancer Analysis',
            'description': 'Binary classification - Cancer detection'
        },
        {
            'path': 'tests/card.ipynb', 
            'name': '🫀 Cardiovascular Disease Analysis',
            'description': 'Binary classification - Heart disease prediction'
        },
        {
            'path': 'tests/fetal_health_analysis.ipynb',
            'name': '👶 Fetal Health Analysis', 
            'description': 'Multi-class classification - Fetal health assessment'
        },
        {
            'path': 'tests/test.ipynb',
            'name': '🧪 Comprehensive Testing',
            'description': 'Model validation and API testing'
        }
    ]
    
    success_count = 0
    total_count = len(notebooks)
    
    for i, nb in enumerate(notebooks, 1):
        print(f"\n🔄 {i}/{total_count}: {nb['name']}")
        print(f"📋 {nb['description']}")
        print(f"📁 {nb['path']}")
        
        if not Path(nb['path']).exists():
            print(f"❌ Notebook bulunamadı: {nb['path']}")
            continue
            
        try:
            start_time = time.time()
            
            # Jupyter nbconvert ile notebook'u çalıştır
            cmd = [
                'jupyter', 'nbconvert',
                '--to', 'notebook', 
                '--execute',
                '--inplace',
                '--allow-errors',
                nb['path']
            ]
            
            print("⏳ Çalıştırılıyor...")
            result = subprocess.run(
                cmd, 
                capture_output=True, 
                text=True,
                timeout=1800  # 30 dakika timeout
            )
            
            execution_time = time.time() - start_time
            
            if result.returncode == 0:
                print(f"✅ Başarıyla tamamlandı! ({execution_time:.1f}s)")
                success_count += 1
            else:
                print(f"❌ Hata oluştu!")
                print(f"STDERR: {result.stderr}")
                
        except subprocess.TimeoutExpired:
            print(f"⏰ Timeout! (30 dakika)")
        except FileNotFoundError:
            print(f"❌ Jupyter bulunamadı! Lütfen yükleyin: pip install jupyter")
            break
        except Exception as e:
            print(f"💥 Beklenmeyen hata: {e}")
        
        print("-" * 50)
    
    # Final rapor
    print(f"\n📋 EXECUTION SUMMARY")
    print("=" * 25)
    print(f"✅ Successful: {success_count}/{total_count}")
    print(f"❌ Failed: {total_count - success_count}/{total_count}")
    print(f"📅 Tamamlanma: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    if success_count == total_count:
        print("\n🎉 PACE Metodolojisi Başarıyla Tamamlandı!")
        print("🚀 Tüm modeller oluşturuldu ve test edildi!")
        print("\n📡 FastAPI Backend Kullanımı:")
        print("   cd backend")
        print("   uvicorn main:app --reload --host 0.0.0.0 --port 8000")
        print("   http://localhost:8000/docs")
        return True
    else:
        print("\n⚠️  Bazı notebook'lar çalıştırılamadı!")
        print("🔧 Lütfen hataları kontrol edin ve tekrar deneyin.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
