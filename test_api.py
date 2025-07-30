#!/usr/bin/env python3
"""
API test script for YZTA-AI-17 Health Screening App
"""

import requests
import json

def test_api():
    """Test API endpoints"""
    base_url = "http://localhost:8000"
    
    print("🧪 YZTA-AI-17 API Test")
    print("=" * 50)
    
    # Test 1: Check if server is running
    try:
        response = requests.get(f"{base_url}/")
        print(f"✅ Server Status: {response.status_code}")
        if response.status_code == 200:
            print(f"   Response: {response.json()}")
    except Exception as e:
        print(f"❌ Server connection failed: {e}")
        return
    
    # Test 2: Get available tests
    try:
        response = requests.get(f"{base_url}/tests")
        print(f"✅ Available Tests: {response.status_code}")
        if response.status_code == 200:
            tests = response.json()
            print(f"   Found {len(tests['tests'])} test types")
            for test in tests['tests']:
                print(f"   - {test['id']}: {test['name']}")
    except Exception as e:
        print(f"❌ Tests endpoint failed: {e}")
    
    # Test 3: Get model info
    try:
        response = requests.get(f"{base_url}/models")
        print(f"✅ Model Info: {response.status_code}")
        if response.status_code == 200:
            models = response.json()
            print(f"   Loaded {len(models['models'])} models")
            for model_name, info in models['models'].items():
                print(f"   - {model_name}: {info['type']} (Accuracy: {info['accuracy']:.3f})")
    except Exception as e:
        print(f"❌ Models endpoint failed: {e}")
    
    # Test 4: Test cardiovascular prediction
    try:
        test_data = {
            "test_type": "cardiovascular",
            "form_data": {
                "age": 45,
                "gender": 1,
                "height": 170,
                "weight": 75,
                "ap_hi": 120,
                "ap_lo": 80,
                "cholesterol": 1,
                "gluc": 1,
                "smoke": 0,
                "alco": 0,
                "active": 1
            }
        }
        
        response = requests.post(
            f"{base_url}/predict",
            headers={"Content-Type": "application/json"},
            data=json.dumps(test_data)
        )
        
        print(f"✅ Cardiovascular Prediction: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print(f"   Risk: {result['risk']}")
            print(f"   Score: {result['score']:.3f}")
            print(f"   Message: {result['message']}")
            print(f"   Confidence: {result.get('confidence', 'N/A')}")
        else:
            print(f"   Error: {response.text}")
            
    except Exception as e:
        print(f"❌ Cardiovascular prediction failed: {e}")
    
    # Test 5: Test fetal health prediction
    try:
        test_data = {
            "test_type": "fetal-health",
            "form_data": {
                "accelerations": 0.002,
                "fetal_movement": 0.0,
                "uterine_contractions": 0.005,
                "light_decelerations": 0.003,
                "percentage_of_time_with_abnormal_long_term_variability": 20.0,
                "mean_value_of_long_term_variability": 35.0,
                "histogram_number_of_peaks": 5,
                "histogram_variance": 15,
                "histogram_tendency": 1
            }
        }
        
        response = requests.post(
            f"{base_url}/predict",
            headers={"Content-Type": "application/json"},
            data=json.dumps(test_data)
        )
        
        print(f"✅ Fetal Health Prediction: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print(f"   Risk: {result['risk']}")
            print(f"   Score: {result['score']:.3f}")
            print(f"   Message: {result['message']}")
        else:
            print(f"   Error: {response.text}")
            
    except Exception as e:
        print(f"❌ Fetal health prediction failed: {e}")
    
    print("\n🎉 API test completed!")
    print(f"📖 API Documentation: {base_url}/docs")

if __name__ == "__main__":
    test_api()
