"""
🚀 LLM REPORT ENHANCER - INTEGRATION EXAMPLES
===========================================

Bu dosya LLM entegrasyonunun nasıl kullanılacağına dair örnekler içerir.
Frontend'den backend'e nasıl entegre edileceğini gösterir.

Integration Flow:
Frontend → API Request → LLM Enhancement → Enhanced Report → Frontend
"""

import os
import json
from datetime import datetime

# Simple LLM enhancer'ı import et
from simple_llm_enhancer import (
    SimpleMedicalReportAPI, 
    MedicalDomain, 
    MedicalContext,
    SimpleLLMConfig
)

def test_llm_integration():
    """Test LLM integration with sample data."""
    
    print("🧪 LLM INTEGRATION TEST")
    print("=" * 40)
    
    # API instance oluştur
    api = SimpleMedicalReportAPI()
    
    # Test cases for each medical domain
    test_cases = [
        {
            "name": "Breast Cancer Enhancement",
            "domain": "breast_cancer",
            "patient_data": {
                "age": 48,
                "tumor_size": 1.8,
                "lymph_nodes": 0,
                "grade": 1,
                "estrogen_receptor": "positive",
                "progesterone_receptor": "positive",
                "her2": "negative"
            },
            "prediction_result": {
                "prediction": "malignant",
                "confidence": 0.89,
                "risk_level": "moderate",
                "accuracy_score": 0.8907
            },
            "user_prompt": "Bu sonuçlara göre hastanın prognozunu ve tedavi seçeneklerini detaylı olarak açıklar mısınız?"
        },
        {
            "name": "Cardiovascular Risk Enhancement", 
            "domain": "cardiovascular",
            "patient_data": {
                "age": 55,
                "blood_pressure_systolic": 145,
                "blood_pressure_diastolic": 95,
                "cholesterol": 280,
                "smoking": True,
                "diabetes": False,
                "family_history": True,
                "bmi": 28.5
            },
            "prediction_result": {
                "prediction": "high_risk",
                "confidence": 0.76,
                "risk_score": 7.8,
                "accuracy_score": 0.8765
            },
            "user_prompt": "Bu kardiyovasküler risk seviyesi için acil müdahale gerekli mi? Hangi yaşam tarzı değişikliklerini önerirsiniz?"
        },
        {
            "name": "Fetal Health Enhancement",
            "domain": "fetal_health", 
            "patient_data": {
                "baseline_fetal_heart_rate": 140,
                "accelerations": 2,
                "fetal_movement": 8,
                "uterine_contractions": 3,
                "severe_decelerations": 0,
                "prolonged_decelerations": 0,
                "abnormal_short_term_variability": 0.5,
                "mean_value_of_short_term_variability": 1.2
            },
            "prediction_result": {
                "prediction": "normal",
                "confidence": 0.92,
                "fetal_state": "healthy",
                "accuracy_score": 0.9234
            },
            "user_prompt": "Bu CTG sonuçları normal görünüyor ama annenin endişeleri var. Nasıl güven verebiliriz ve takip nasıl olmalı?"
        }
    ]
    
    # Her test case'i çalıştır
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n🔬 TEST {i}: {test_case['name']}")
        print("-" * 50)
        
        # Request data hazırla
        request_data = {
            "domain": test_case["domain"],
            "patient_data": test_case["patient_data"],
            "prediction_result": test_case["prediction_result"],
            "model_metadata": {
                "model_name": f"{test_case['domain']}_model",
                "version": "1.0.0",
                "accuracy": test_case["prediction_result"]["accuracy_score"]
            },
            "user_prompt": test_case["user_prompt"],
            "llm_provider": "openai"  # veya "anthropic"
        }
        
        # API call yap
        result = api.enhance_report(request_data)
        
        # Sonuçları göster
        print(f"Status: {result['status']}")
        if result['status'] == 'success':
            print(f"Enhanced Report:\n{result['enhanced_report'][:500]}...")
            print(f"\nProvider: {result['metadata']['provider']}")
            print(f"Timestamp: {result['metadata']['enhancement_timestamp']}")
        else:
            print(f"Error: {result['error_message']}")
        
        print("\n" + "="*50)

def frontend_integration_example():
    """Frontend integration example - JSON API format."""
    
    print("🌐 FRONTEND INTEGRATION EXAMPLE")
    print("=" * 40)
    
    # Bu JavaScript/React frontend'den gelecek request format örneği
    frontend_request = {
        "method": "POST",
        "url": "/api/enhance-report",
        "headers": {
            "Content-Type": "application/json",
            "Authorization": "Bearer your-jwt-token"
        },
        "body": {
            "domain": "breast_cancer",
            "patient_data": {
                "age": 45,
                "tumor_size": 2.1,
                "lymph_nodes": 1,
                "grade": 2
            },
            "prediction_result": {
                "prediction": "malignant", 
                "confidence": 0.85
            },
            "user_prompt": "Bu sonuçlar ne anlama geliyor? Tedavi seçenekleri nelerdir?",
            "llm_provider": "openai"
        }
    }
    
    print("Frontend Request Format:")
    print(json.dumps(frontend_request, indent=2, ensure_ascii=False))
    
    # Backend processing
    api = SimpleMedicalReportAPI()
    result = api.enhance_report(frontend_request["body"])
    
    print("\nBackend Response:")
    print(json.dumps(result, indent=2, ensure_ascii=False))

def flask_api_example():
    """Flask API endpoint örneği."""
    
    flask_code = '''
from flask import Flask, request, jsonify
from simple_llm_enhancer import SimpleMedicalReportAPI

app = Flask(__name__)
api_handler = SimpleMedicalReportAPI()

@app.route('/api/enhance-report', methods=['POST'])
def enhance_report():
    """LLM report enhancement endpoint."""
    try:
        request_data = request.get_json()
        
        # Validate request
        if not request_data:
            return jsonify({
                "status": "error",
                "error_message": "No data provided"
            }), 400
        
        # Process with LLM
        result = api_handler.enhance_report(request_data)
        
        # Return response
        if result["status"] == "success":
            return jsonify(result), 200
        else:
            return jsonify(result), 500
            
    except Exception as e:
        return jsonify({
            "status": "error",
            "error_message": str(e)
        }), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({
        "status": "healthy",
        "service": "LLM Report Enhancer",
        "timestamp": datetime.now().isoformat()
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)
'''
    
    print("🐍 FLASK API ENDPOINT EXAMPLE")
    print("=" * 40)
    print(flask_code)

def fastapi_example():
    """FastAPI endpoint örneği."""
    
    fastapi_code = '''
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, Any, Optional
from simple_llm_enhancer import SimpleMedicalReportAPI

app = FastAPI(title="LLM Medical Report Enhancer")
api_handler = SimpleMedicalReportAPI()

class ReportEnhancementRequest(BaseModel):
    domain: str
    patient_data: Dict[str, Any]
    prediction_result: Dict[str, Any]
    model_metadata: Optional[Dict[str, Any]] = {}
    user_prompt: str
    llm_provider: Optional[str] = "openai"

@app.post("/api/enhance-report")
async def enhance_report(request: ReportEnhancementRequest):
    """LLM report enhancement endpoint."""
    try:
        request_data = request.dict()
        result = api_handler.enhance_report(request_data)
        
        if result["status"] == "success":
            return result
        else:
            raise HTTPException(status_code=500, detail=result["error_message"])
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "service": "LLM Report Enhancer", 
        "timestamp": datetime.now().isoformat()
    }

# Run with: uvicorn main:app --reload --port 8000
'''
    
    print("⚡ FASTAPI ENDPOINT EXAMPLE")
    print("=" * 40)
    print(fastapi_code)

def environment_setup_guide():
    """Environment setup rehberi."""
    
    setup_guide = '''
🔧 ENVIRONMENT SETUP GUIDE
========================

1. Install Dependencies:
   pip install requests python-dotenv

2. Create .env file:
   touch .env

3. Add API Keys to .env:
   OPENAI_API_KEY=sk-your-openai-api-key-here
   ANTHROPIC_API_KEY=sk-ant-your-anthropic-key-here

4. Load environment in Python:
   from dotenv import load_dotenv
   load_dotenv()

5. Test the service:
   python llm_integration_examples.py

6. Optional Dependencies:
   pip install flask fastapi uvicorn  # for web API
   pip install aiohttp                # for async version
   
7. Environment Variables Check:
   import os
   print("OpenAI Key:", "✅" if os.getenv('OPENAI_API_KEY') else "❌")
   print("Anthropic Key:", "✅" if os.getenv('ANTHROPIC_API_KEY') else "❌")
'''
    
    print(setup_guide)

def security_considerations():
    """Security ve best practices."""
    
    security_guide = '''
🔒 SECURITY CONSIDERATIONS
========================

1. API Key Security:
   - Never commit API keys to version control
   - Use environment variables
   - Rotate keys regularly
   - Monitor API usage

2. Data Privacy:
   - Medical data is sensitive (HIPAA/GDPR)
   - Log carefully - avoid logging patient data
   - Use HTTPS for all API calls
   - Implement request/response encryption

3. Rate Limiting:
   - Implement API rate limiting
   - Monitor LLM API costs
   - Set usage quotas per user

4. Input Validation:
   - Validate all input data
   - Sanitize user prompts
   - Implement prompt injection protection

5. Error Handling:
   - Don't expose internal errors to users
   - Log errors securely
   - Provide user-friendly error messages

6. Monitoring:
   - Monitor API response times
   - Track enhancement quality
   - Alert on failures
'''
    
    print(security_guide)

if __name__ == "__main__":
    print("🤖 LLM REPORT ENHANCER - INTEGRATION EXAMPLES")
    print("=" * 55)
    
    # Environment check
    config = SimpleLLMConfig()
    openai_configured = bool(config.OPENAI_API_KEY)
    anthropic_configured = bool(config.ANTHROPIC_API_KEY) 
    
    print(f"OpenAI API: {'✅ Configured' if openai_configured else '❌ Not configured'}")
    print(f"Anthropic API: {'✅ Configured' if anthropic_configured else '❌ Not configured'}")
    
    if not (openai_configured or anthropic_configured):
        print("\n⚠️  No API keys configured! Set up environment variables first.")
        environment_setup_guide()
    else:
        print("\n🧪 Running integration tests...")
        test_llm_integration()
        
        print("\n🌐 Frontend integration example:")
        frontend_integration_example()
    
    print("\n📋 Additional examples:")
    print("- flask_api_example()")
    print("- fastapi_example()")
    print("- environment_setup_guide()")
    print("- security_considerations()")
