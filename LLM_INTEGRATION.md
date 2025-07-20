# 🤖 LLM Report Enhancer - Medikal Rapor Geliştirme Entegrasyonu

## 📋 Genel Bakış

Bu sistem, medikal analiz sonuçlarını LLM (Large Language Model) teknolojisi ile geliştirmek için tasarlanmış profesyonel bir entegrasyon çözümüdür. Kullanıcıların "Raporu Geliştir (Chat ile)" butonuna girdikleri prompt'ları alır ve AI destekli medikal raporlar üretir.

## 🎯 Özellikler

- **🎗️ Meme Kanseri**: Morfololojik analiz raporlarının geliştirilmesi
- **🫀 Kardiyovasküler**: Kardiyak risk değerlendirme raporları
- **👶 Fetal Sağlık**: CTG analiz sonuçlarının detaylandırılması
- **🔬 PACE Metodolojisi**: Sistematik rapor geliştirme yaklaşımı
- **🌐 Multi-Provider**: OpenAI, Anthropic, Ollama desteği
- **🚀 Async/Sync**: Hem asenkron hem senkron API desteği

## 📁 Dosya Yapısı

```
llm_report_enhancer.py          # Ana LLM entegrasyon servisi (async)
simple_llm_enhancer.py          # Basit senkron versiyon
llm_integration_examples.py     # Kullanım örnekleri ve testler
requirements_llm.txt            # LLM dependencies
LLM_INTEGRATION.md             # Bu dokümantasyon
```

## 🚀 Hızlı Başlangıç

### 1. Bağımlılıkları Yükle

```bash
# Minimal dependencies
pip install requests python-dotenv

# Tam özellikler için
pip install -r requirements_llm.txt
```

### 2. Environment Variables Ayarla

```bash
# .env dosyası oluştur
touch .env

# API anahtarlarını ekle
echo "OPENAI_API_KEY=sk-your-openai-api-key-here" >> .env
echo "ANTHROPIC_API_KEY=sk-ant-your-anthropic-key-here" >> .env
```

### 3. Basit Kullanım

```python
from simple_llm_enhancer import SimpleMedicalReportAPI, MedicalDomain

# API instance oluştur
api = SimpleMedicalReportAPI()

# Request data hazırla
request_data = {
    "domain": "breast_cancer",
    "patient_data": {
        "age": 52,
        "tumor_size": 2.3,
        "lymph_nodes": 1,
        "grade": 2
    },
    "prediction_result": {
        "prediction": "malignant",
        "confidence": 0.87
    },
    "user_prompt": "Bu sonuçları detaylı olarak açıklar mısınız?",
    "llm_provider": "openai"
}

# Rapor geliştir
result = api.enhance_report(request_data)

if result["status"] == "success":
    print(result["enhanced_report"])
else:
    print(f"Error: {result['error_message']}")
```

## 🔧 API Entegrasyonu

### Frontend'den Backend'e Veri Akışı

```javascript
// Frontend (JavaScript/React)
const enhanceReport = async (reportData, userPrompt) => {
    const response = await fetch('/api/enhance-report', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${authToken}`
        },
        body: JSON.stringify({
            domain: reportData.domain,
            patient_data: reportData.patientData,
            prediction_result: reportData.predictionResult,
            model_metadata: reportData.modelMetadata,
            user_prompt: userPrompt,
            llm_provider: "openai"
        })
    });
    
    return await response.json();
};
```

### Backend API Endpoint (FastAPI)

```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from simple_llm_enhancer import SimpleMedicalReportAPI

app = FastAPI()
api_handler = SimpleMedicalReportAPI()

class ReportRequest(BaseModel):
    domain: str
    patient_data: dict
    prediction_result: dict
    user_prompt: str
    llm_provider: str = "openai"

@app.post("/api/enhance-report")
async def enhance_report(request: ReportRequest):
    result = api_handler.enhance_report(request.dict())
    
    if result["status"] == "success":
        return result
    else:
        raise HTTPException(status_code=500, detail=result["error_message"])
```

## 🎯 Medikal Domain'ler

### Meme Kanseri (Breast Cancer)

```python
request_data = {
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
        "risk_level": "moderate"
    },
    "user_prompt": "Prognoz ve tedavi seçeneklerini açıklar mısınız?"
}
```

### Kardiyovasküler (Cardiovascular)

```python
request_data = {
    "domain": "cardiovascular",
    "patient_data": {
        "age": 55,
        "blood_pressure_systolic": 145,
        "blood_pressure_diastolic": 95,
        "cholesterol": 280,
        "smoking": True,
        "diabetes": False,
        "family_history": True
    },
    "prediction_result": {
        "prediction": "high_risk",
        "confidence": 0.76,
        "risk_score": 7.8
    },
    "user_prompt": "Risk azaltma stratejileri nelerdir?"
}
```

### Fetal Sağlık (Fetal Health)

```python
request_data = {
    "domain": "fetal_health",
    "patient_data": {
        "baseline_fetal_heart_rate": 140,
        "accelerations": 2,
        "fetal_movement": 8,
        "uterine_contractions": 3,
        "severe_decelerations": 0
    },
    "prediction_result": {
        "prediction": "normal",
        "confidence": 0.92,
        "fetal_state": "healthy"
    },
    "user_prompt": "CTG sonuçları normal ama anne endişeli, nasıl açıklarım?"
}
```

## 🔒 Güvenlik Considerasyonları

### API Key Güvenliği

```python
import os
from dotenv import load_dotenv

# Environment variables'ı güvenli şekilde yükle
load_dotenv()

# API key'leri asla kod içinde yazmayın
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
ANTHROPIC_API_KEY = os.getenv('ANTHROPIC_API_KEY')

# API key kontrolü
if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY environment variable not set")
```

### Medikal Veri Güvenliği

- **HIPAA/GDPR Uyumluluk**: Hasta verilerini log'lamayın
- **HTTPS**: Tüm API çağrıları HTTPS üzerinden
- **Şifreleme**: Request/response şifreleme
- **Rate Limiting**: API limitlerini uygulayın

### Input Validation

```python
def validate_request_data(data):
    required_fields = ["domain", "patient_data", "prediction_result", "user_prompt"]
    
    for field in required_fields:
        if field not in data:
            raise ValueError(f"Missing required field: {field}")
    
    # Domain validation
    valid_domains = ["breast_cancer", "cardiovascular", "fetal_health"]
    if data["domain"] not in valid_domains:
        raise ValueError(f"Invalid domain: {data['domain']}")
    
    # Prompt injection protection
    if len(data["user_prompt"]) > 2000:
        raise ValueError("User prompt too long")
```

## 📊 Response Format

### Başarılı Response

```json
{
    "status": "success",
    "enhanced_report": "Detaylı medikal rapor metni...",
    "metadata": {
        "domain": "breast_cancer",
        "provider": "openai",
        "enhancement_timestamp": "2024-01-15T10:30:00",
        "user_prompt": "Kullanıcının sorusu",
        "original_prediction": {
            "prediction": "malignant",
            "confidence": 0.87
        },
        "processing_info": {
            "model_used": "gpt-4",
            "temperature": 0.3,
            "max_tokens": 2000
        }
    }
}
```

### Error Response

```json
{
    "status": "error",
    "error_message": "API key not configured",
    "enhanced_report": "Rapor geliştirme sırasında bir hata oluştu. Lütfen tekrar deneyiniz.",
    "metadata": {
        "domain": "breast_cancer",
        "provider": "openai",
        "enhancement_timestamp": "2024-01-15T10:30:00",
        "error_details": "OpenAI API key not configured"
    }
}
```

## 🧪 Test ve Debugging

### Unit Testing

```python
import unittest
from simple_llm_enhancer import SimpleMedicalReportAPI

class TestLLMIntegration(unittest.TestCase):
    
    def setUp(self):
        self.api = SimpleMedicalReportAPI()
        
    def test_breast_cancer_enhancement(self):
        request_data = {
            "domain": "breast_cancer",
            "patient_data": {"age": 45, "tumor_size": 2.0},
            "prediction_result": {"prediction": "malignant", "confidence": 0.8},
            "user_prompt": "Test prompt"
        }
        
        result = self.api.enhance_report(request_data)
        self.assertEqual(result["status"], "success")
        self.assertIn("enhanced_report", result)

if __name__ == '__main__':
    unittest.main()
```

### Debug Mode

```python
import logging

# Debug logging'i etkinleştir
logging.basicConfig(level=logging.DEBUG)

# API çağrılarını izle
logger = logging.getLogger(__name__)
logger.debug(f"Enhancing report for domain: {domain}")
logger.debug(f"User prompt: {user_prompt}")
```

## 📈 Performance ve Monitoring

### Response Time Monitoring

```python
import time
from datetime import datetime

def monitor_enhancement_performance(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        
        duration = end_time - start_time
        logger.info(f"Enhancement completed in {duration:.2f} seconds")
        
        # Performance metadata'ya ekle
        if "metadata" in result:
            result["metadata"]["processing_time"] = duration
            
        return result
    return wrapper
```

### Cost Tracking

```python
class CostTracker:
    def __init__(self):
        self.total_tokens = 0
        self.total_cost = 0.0
        
    def track_usage(self, provider, tokens_used):
        # Token costs (example prices)
        token_costs = {
            "openai": 0.002 / 1000,      # $0.002 per 1K tokens
            "anthropic": 0.008 / 1000    # $0.008 per 1K tokens  
        }
        
        cost = tokens_used * token_costs.get(provider, 0)
        self.total_tokens += tokens_used
        self.total_cost += cost
        
        logger.info(f"Used {tokens_used} tokens, cost: ${cost:.4f}")
```

## 🔄 Production Deployment

### Environment Configuration

```bash
# Production .env
OPENAI_API_KEY=sk-production-key
ANTHROPIC_API_KEY=sk-production-key
LLM_DEFAULT_PROVIDER=openai
LLM_REQUEST_TIMEOUT=60
LLM_MAX_RETRIES=3
LLM_RATE_LIMIT=100  # requests per minute
```

### Docker Deployment

```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements_llm.txt .
RUN pip install -r requirements_llm.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Health Check Endpoint

```python
@app.get("/health")
async def health_check():
    """System health check."""
    try:
        # Test LLM connectivity
        config = SimpleLLMConfig()
        api_status = "configured" if config.OPENAI_API_KEY else "not_configured"
        
        return {
            "status": "healthy",
            "service": "LLM Report Enhancer",
            "timestamp": datetime.now().isoformat(),
            "api_status": api_status,
            "version": "1.0.0"
        }
    except Exception as e:
        raise HTTPException(status_code=503, detail=str(e))
```

## 🎯 Best Practices

### 1. Prompt Engineering

```python
# İyi prompt örneği
prompt = f"""
Sen uzman bir {domain} doktorusun. Aşağıdaki analiz sonuçlarını değerlendirerek:

1. Klinik önemi açıkla
2. Risk faktörlerini belirt  
3. Önerilen yaklaşımları listele
4. Hasta için anlaşılır dil kullan
5. Kullanıcının özel sorusunu yanıtla: {user_prompt}

Veriler: {patient_data}
Sonuçlar: {prediction_result}
"""
```

### 2. Error Handling

```python
def robust_api_call(func):
    def wrapper(*args, **kwargs):
        max_retries = 3
        for attempt in range(max_retries):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                if attempt == max_retries - 1:
                    logger.error(f"API call failed after {max_retries} attempts: {e}")
                    raise
                else:
                    logger.warning(f"API call attempt {attempt + 1} failed: {e}")
                    time.sleep(2 ** attempt)  # Exponential backoff
        return wrapper
```

### 3. Caching

```python
from functools import lru_cache
import hashlib

def get_cache_key(patient_data, prediction_result, user_prompt):
    """Generate cache key for similar requests."""
    data_str = json.dumps({
        "patient": patient_data,
        "prediction": prediction_result, 
        "prompt": user_prompt
    }, sort_keys=True)
    return hashlib.md5(data_str.encode()).hexdigest()

@lru_cache(maxsize=100)
def cached_enhancement(cache_key, *args):
    """Cache enhanced reports for similar requests."""
    return actual_enhancement_function(*args)
```

## 📞 Support ve İletişim

- **Dokümantasyon**: Bu dosya
- **Kod Örnekleri**: `llm_integration_examples.py`
- **Test Dosyası**: `python llm_integration_examples.py`
- **Issue Reporting**: Hata durumlarında log dosyalarını kontrol edin

## 🔮 Gelecek Geliştirmeler

- [ ] Multi-language support (English, Turkish)
- [ ] Custom medical model integration
- [ ] Advanced prompt templates
- [ ] Real-time streaming responses
- [ ] Integration with FHIR standards
- [ ] Advanced analytics and reporting

---

**🎯 Bu entegrasyon sayesinde medikal raporlarınız AI destekli profesyonel içerikle zenginleştirilir!**
