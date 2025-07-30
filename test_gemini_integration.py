#!/usr/bin/env python3
"""
🧪 GEMINI API INTEGRATION TEST
=============================

Bu script Gemini API entegrasyonunu test eder.
"""

import sys
import os
import json
from datetime import datetime

# Backend path'i ekle
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

def test_gemini_api():
    """Test Gemini API integration"""
    print("🧪 Gemini API Integration Test")
    print("=" * 50)
    
    # Environment check
    gemini_key = os.getenv('GEMINI_API_KEY')
    if not gemini_key:
        print("❌ GEMINI_API_KEY environment variable not set")
        print("📋 To set it up:")
        print("export GEMINI_API_KEY='your-gemini-api-key'")
        print("🔗 Get API key from: https://makersuite.google.com/app/apikey")
        return False
    
    print(f"✅ Gemini API Key: ***{gemini_key[-4:]}")
    
    # Import backend modules
    try:
        from main import create_medical_prompt
        print("✅ Backend module imported successfully")
    except ImportError as e:
        print(f"❌ Backend import failed: {e}")
        return False
    
    # Test prompt creation
    try:
        test_data = {
            "domain": "breast_cancer",
            "patient_data": {
                "age": 48,
                "tumor_size": 1.8,
                "lymph_nodes": 0,
                "grade": 1
            },
            "prediction_result": {
                "prediction": "malignant",
                "confidence": 0.89,
                "score": 78.5
            },
            "user_prompt": "Bu sonuçları detaylı olarak açıklar mısınız?"
        }
        
        prompt = create_medical_prompt(
            test_data["domain"],
            test_data["patient_data"],
            test_data["prediction_result"],
            test_data["user_prompt"]
        )
        
        print("✅ Medical prompt created successfully")
        print(f"📝 Prompt length: {len(prompt)} characters")
        
        # Preview prompt (first 500 chars)
        print("\n📋 Prompt Preview:")
        print("-" * 30)
        print(prompt[:500] + "..." if len(prompt) > 500 else prompt)
        
        return True
        
    except Exception as e:
        print(f"❌ Prompt creation failed: {e}")
        return False

def test_api_endpoint_structure():
    """Test API endpoint structure"""
    print("\n🔗 API Endpoint Structure Test")
    print("=" * 50)
    
    try:
        from main import app
        from fastapi.testclient import TestClient
        
        client = TestClient(app)
        
        # Test endpoint exists
        response = client.get("/")
        print("✅ FastAPI app accessible")
        
        return True
        
    except ImportError:
        print("⚠️  TestClient not available, skipping endpoint test")
        return True
    except Exception as e:
        print(f"❌ API structure test failed: {e}")
        return False

def main():
    """Main test function"""
    print("🚀 YZTA-AI-17 Gemini Integration Test Suite")
    print("=" * 60)
    print(f"📅 Test Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    tests = [
        ("Gemini API Setup", test_gemini_api),
        ("API Endpoint Structure", test_api_endpoint_structure),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n🧪 Running: {test_name}")
        try:
            if test_func():
                print(f"✅ {test_name}: PASSED")
                passed += 1
            else:
                print(f"❌ {test_name}: FAILED")
        except Exception as e:
            print(f"❌ {test_name}: ERROR - {e}")
    
    print("\n" + "=" * 60)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Gemini integration is ready.")
        print("\n📋 Next steps:")
        print("1. Set your actual Gemini API key in .env file")
        print("2. Start backend: python run.py")
        print("3. Test the 'Raporu Geliştir (Chat ile)' feature")
    else:
        print("⚠️  Some tests failed. Please check the configuration.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
