"""
🤖 SIMPLE LLM INTEGRATION SERVICE FOR MEDICAL REPORT ENHANCEMENT
==================================================================

This is a simplified synchronous version of the LLM integration service
that works without async dependencies. Perfect for quick integration.

Features:
- 🎗️ Breast Cancer: Enhanced morphological analysis reports
- 🫀 Cardiovascular: Detailed cardiac risk assessment reports  
- 👶 Fetal Health: Comprehensive CTG analysis reports
- 🔬 PACE Methodology: Systematic report enhancement
- 🚀 Simple synchronous API calls
"""

import json
import logging
from datetime import datetime
from typing import Dict, Any, Optional
from dataclasses import dataclass
from enum import Enum
import os

# Optional imports with fallbacks
try:
    import requests
    REQUESTS_AVAILABLE = True
except ImportError:
    REQUESTS_AVAILABLE = False
    print("⚠️  requests not available. Install with: pip install requests")

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MedicalDomain(Enum):
    """Medical analysis domains."""
    BREAST_CANCER = "breast_cancer"
    CARDIOVASCULAR = "cardiovascular" 
    FETAL_HEALTH = "fetal_health"

@dataclass
class MedicalContext:
    """Medical context data for LLM enhancement."""
    domain: MedicalDomain
    patient_data: Dict[str, Any]
    prediction_result: Dict[str, Any]
    model_metadata: Dict[str, Any]
    analysis_timestamp: str

class SimpleLLMConfig:
    """Simple LLM service configuration."""
    
    def __init__(self):
        # Environment variables'dan API anahtarlarını al
        self.OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
        self.ANTHROPIC_API_KEY = os.getenv('ANTHROPIC_API_KEY')
        
        # Model configurations
        self.OPENAI_MODEL = "gpt-4"
        self.ANTHROPIC_MODEL = "claude-3-sonnet-20240229"
        self.MAX_TOKENS = 2000
        self.TEMPERATURE = 0.3  # Medical için düşük temperature
        
        # Default provider
        self.DEFAULT_PROVIDER = "openai"  # openai, anthropic
        
        # Timeout settings
        self.REQUEST_TIMEOUT = 60

class MedicalPromptTemplates:
    """Professional medical prompt templates for different domains."""
    
    BREAST_CANCER_TEMPLATE = """
Sen deneyimli bir onkoloji uzmanısın. Aşağıdaki meme kanseri analiz sonuçlarını değerlendirerek profesyonel bir rapor hazırla.

📊 HASTA VERİLERİ:
{patient_data}

🤖 MODEL TAHMİNİ:
{prediction_result}

📈 MODEL PERFORMANSI:
{model_metadata}

👤 KULLANICI TALEBİ:
{user_prompt}

🎯 RAPOR REHBERİ:
1. Sonuçları klinik perspektiften yorumla
2. Risk faktörlerini analiz et
3. Önerilen takip adımlarını belirt
4. Hasta için anlaşılır açıklamalar yap
5. Gerekirse ek testleri öner
6. Kullanıcının özel talebini de dikkate al

Lütfen profesyonel, net ve hastanın anlayabileceği bir dilde rapor hazırla.
"""
    
    CARDIOVASCULAR_TEMPLATE = """
Sen deneyimli bir kardiyoloji uzmanısın. Aşağıdaki kardiyovasküler risk analiz sonuçlarını değerlendirerek profesyonel bir rapor hazırla.

📊 HASTA VERİLERİ:
{patient_data}

🤖 MODEL TAHMİNİ:
{prediction_result}

📈 MODEL PERFORMANSI:
{model_metadata}

👤 KULLANICI TALEBİ:
{user_prompt}

🎯 RAPOR REHBERİ:
1. Kardiyovasküler risk seviyesini değerlendir
2. Yaşam tarzı önerilerini belirt
3. Medikal takip gereksinimlerini açıkla
4. Önleme stratejilerini öner
5. Acil duruma işaret eden faktörleri belirt
6. Kullanıcının özel talebini de dikkate al

Lütfen kardiyak sağlık odaklı, kanıt tabanlı bir rapor hazırla.
"""
    
    FETAL_HEALTH_TEMPLATE = """
Sen deneyimli bir perinatoloji uzmanısın. Aşağıdaki fetal sağlık CTG analiz sonuçlarını değerlendirerek profesyonel bir rapor hazırla.

📊 CTG VERİLERİ:
{patient_data}

🤖 MODEL TAHMİNİ:
{prediction_result}

📈 MODEL PERFORMANSI:
{model_metadata}

👤 KULLANICI TALEBİ:
{user_prompt}

🎯 RAPOR REHBERİ:
1. Fetal kalp hızı paternini yorumla
2. CTG bulgularının klinik anlamını açıkla
3. Gebelik takip önerilerini belirt
4. Risk durumlarını değerlendir
5. Anne adayı için rehberlik sağla
6. Kullanıcının özel talebini de dikkate al

Lütfen obstetrik bakış açısıyla, anne ve bebek sağlığı odaklı rapor hazırla.
"""
    
    @classmethod
    def get_template(cls, domain: MedicalDomain) -> str:
        """Get appropriate template for medical domain."""
        templates = {
            MedicalDomain.BREAST_CANCER: cls.BREAST_CANCER_TEMPLATE,
            MedicalDomain.CARDIOVASCULAR: cls.CARDIOVASCULAR_TEMPLATE,
            MedicalDomain.FETAL_HEALTH: cls.FETAL_HEALTH_TEMPLATE
        }
        return templates.get(domain, cls.BREAST_CANCER_TEMPLATE)

class SimpleLLMReportEnhancer:
    """Simple synchronous LLM service for medical report enhancement."""
    
    def __init__(self, config: Optional[SimpleLLMConfig] = None):
        """Initialize simple LLM service."""
        self.config = config or SimpleLLMConfig()
        
        # Check dependencies
        if not REQUESTS_AVAILABLE:
            raise RuntimeError("requests library is required. Install with: pip install requests")
    
    def _prepare_prompt(self, medical_context: MedicalContext, user_prompt: str) -> str:
        """Prepare comprehensive prompt for LLM."""
        
        # Get domain-specific template
        template = MedicalPromptTemplates.get_template(medical_context.domain)
        
        # Fill template with medical context
        enhanced_prompt = template.format(
            patient_data=json.dumps(medical_context.patient_data, indent=2, ensure_ascii=False),
            prediction_result=json.dumps(medical_context.prediction_result, indent=2, ensure_ascii=False),
            model_metadata=json.dumps(medical_context.model_metadata, indent=2, ensure_ascii=False),
            user_prompt=user_prompt
        )
        
        return enhanced_prompt
    
    def _call_openai_api(self, prompt: str) -> str:
        """Call OpenAI API for report enhancement."""
        if not self.config.OPENAI_API_KEY:
            raise ValueError("OpenAI API key not configured. Set OPENAI_API_KEY environment variable.")
            
        headers = {
            "Authorization": f"Bearer {self.config.OPENAI_API_KEY}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": self.config.OPENAI_MODEL,
            "messages": [
                {
                    "role": "system", 
                    "content": "Sen uzman bir doktor ve medikal rapor yazarısın. PACE metodolojisini kullanarak sistematik, kanıt tabanlı raporlar hazırlarsın."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "max_tokens": self.config.MAX_TOKENS,
            "temperature": self.config.TEMPERATURE,
            "top_p": 1,
            "frequency_penalty": 0,
            "presence_penalty": 0
        }
        
        try:
            response = requests.post(
                "https://api.openai.com/v1/chat/completions",
                headers=headers,
                json=payload,
                timeout=self.config.REQUEST_TIMEOUT
            )
            
            if response.status_code == 200:
                result = response.json()
                return result["choices"][0]["message"]["content"]
            else:
                raise Exception(f"OpenAI API error: {response.status_code} - {response.text}")
                
        except requests.RequestException as e:
            raise Exception(f"OpenAI API request failed: {str(e)}")
    
    def _call_anthropic_api(self, prompt: str) -> str:
        """Call Anthropic Claude API for report enhancement."""
        if not self.config.ANTHROPIC_API_KEY:
            raise ValueError("Anthropic API key not configured. Set ANTHROPIC_API_KEY environment variable.")
            
        headers = {
            "x-api-key": self.config.ANTHROPIC_API_KEY,
            "Content-Type": "application/json",
            "anthropic-version": "2023-06-01"
        }
        
        payload = {
            "model": self.config.ANTHROPIC_MODEL,
            "max_tokens": self.config.MAX_TOKENS,
            "temperature": self.config.TEMPERATURE,
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        }
        
        try:
            response = requests.post(
                "https://api.anthropic.com/v1/messages",
                headers=headers,
                json=payload,
                timeout=self.config.REQUEST_TIMEOUT
            )
            
            if response.status_code == 200:
                result = response.json()
                return result["content"][0]["text"]
            else:
                raise Exception(f"Anthropic API error: {response.status_code} - {response.text}")
                
        except requests.RequestException as e:
            raise Exception(f"Anthropic API request failed: {str(e)}")
    
    def enhance_medical_report(self, 
                             medical_context: MedicalContext,
                             user_prompt: str,
                             provider: Optional[str] = None) -> Dict[str, Any]:
        """
        Enhance medical report using LLM.
        
        Args:
            medical_context: Medical data and prediction context
            user_prompt: User's specific enhancement request
            provider: LLM provider to use (openai, anthropic)
            
        Returns:
            Enhanced report with metadata
        """
        try:
            # Prepare comprehensive prompt
            enhanced_prompt = self._prepare_prompt(medical_context, user_prompt)
            
            # Choose LLM provider
            provider = provider or self.config.DEFAULT_PROVIDER
            
            # Call appropriate LLM API
            if provider == "openai":
                enhanced_content = self._call_openai_api(enhanced_prompt)
            elif provider == "anthropic":
                enhanced_content = self._call_anthropic_api(enhanced_prompt)
            else:
                raise ValueError(f"Unsupported LLM provider: {provider}")
            
            # Prepare response
            response = {
                "status": "success",
                "enhanced_report": enhanced_content,
                "metadata": {
                    "domain": medical_context.domain.value,
                    "provider": provider,
                    "enhancement_timestamp": datetime.now().isoformat(),
                    "user_prompt": user_prompt,
                    "original_prediction": medical_context.prediction_result,
                    "processing_info": {
                        "model_used": getattr(self.config, f"{provider.upper()}_MODEL", "unknown"),
                        "temperature": self.config.TEMPERATURE,
                        "max_tokens": self.config.MAX_TOKENS
                    }
                }
            }
            
            logger.info(f"Successfully enhanced {medical_context.domain.value} report using {provider}")
            return response
            
        except Exception as e:
            logger.error(f"Error enhancing medical report: {str(e)}")
            return {
                "status": "error",
                "error_message": str(e),
                "enhanced_report": "Rapor geliştirme sırasında bir hata oluştu. Lütfen tekrar deneyiniz.",
                "metadata": {
                    "domain": medical_context.domain.value,
                    "provider": provider or self.config.DEFAULT_PROVIDER,
                    "enhancement_timestamp": datetime.now().isoformat(),
                    "error_details": str(e)
                }
            }

class SimpleMedicalReportAPI:
    """Simple API handler for medical report enhancement requests."""
    
    def __init__(self):
        """Initialize simple API handler."""
        self.llm_enhancer = SimpleLLMReportEnhancer()
    
    def enhance_report(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Handle report enhancement request from frontend.
        
        Expected request_data format:
        {
            "domain": "breast_cancer" | "cardiovascular" | "fetal_health",
            "patient_data": {...},
            "prediction_result": {...},
            "model_metadata": {...},
            "user_prompt": "Kullanıcının rapor geliştirme talebi",
            "llm_provider": "openai" | "anthropic" (optional)
        }
        """
        try:
            # Validate request data
            required_fields = ["domain", "patient_data", "prediction_result", "user_prompt"]
            for field in required_fields:
                if field not in request_data:
                    return {
                        "status": "error",
                        "error_message": f"Missing required field: {field}"
                    }
            
            # Create medical context
            medical_context = MedicalContext(
                domain=MedicalDomain(request_data["domain"]),
                patient_data=request_data["patient_data"],
                prediction_result=request_data["prediction_result"],
                model_metadata=request_data.get("model_metadata", {}),
                analysis_timestamp=datetime.now().isoformat()
            )
            
            # Enhance report using LLM
            result = self.llm_enhancer.enhance_medical_report(
                medical_context=medical_context,
                user_prompt=request_data["user_prompt"],
                provider=request_data.get("llm_provider")
            )
            
            return result
            
        except Exception as e:
            logger.error(f"Error in API handler: {str(e)}")
            return {
                "status": "error",
                "error_message": f"API işleme hatası: {str(e)}"
            }

# Example usage functions
def example_breast_cancer_enhancement():
    """Example breast cancer report enhancement."""
    
    # Sample data (bu veriler frontend'den gelecek)
    sample_context = MedicalContext(
        domain=MedicalDomain.BREAST_CANCER,
        patient_data={
            "age": 52,
            "tumor_size": 2.3,
            "lymph_nodes": 1,
            "grade": 2,
            "estrogen_receptor": "positive"
        },
        prediction_result={
            "prediction": "malignant",
            "confidence": 0.87,
            "risk_factors": ["age", "tumor_size"]
        },
        model_metadata={
            "model_name": "BreastCancerSystematicPredictor",
            "accuracy": 0.8907
        },
        analysis_timestamp=datetime.now().isoformat()
    )
    
    user_prompt = "Bu sonuçlara göre hastanın takip edilmesi gereken durumları ve önerilen tedavi seçeneklerini detaylandırır mısınız?"
    
    enhancer = SimpleLLMReportEnhancer()
    result = enhancer.enhance_medical_report(sample_context, user_prompt)
    
    print("Enhanced Report:")
    print("=" * 50)
    print(result["enhanced_report"])
    print("\nMetadata:")
    print(json.dumps(result["metadata"], indent=2, ensure_ascii=False))

def example_api_usage():
    """Example API usage."""
    
    # Sample request data (bu frontend'den gelecek)
    request_data = {
        "domain": "cardiovascular",
        "patient_data": {
            "age": 45,
            "blood_pressure": "140/90",
            "cholesterol": 250,
            "smoking": "yes",
            "family_history": "yes"
        },
        "prediction_result": {
            "prediction": "high_risk",
            "confidence": 0.78,
            "risk_score": 8.5
        },
        "model_metadata": {
            "model_name": "CardiovascularSystematicPredictor",
            "accuracy": 0.8765
        },
        "user_prompt": "Bu risk seviyesi için hangi yaşam tarzı değişikliklerini önerirsiniz ve ne kadar süre sonra kontrol edilmeli?",
        "llm_provider": "openai"
    }
    
    api = SimpleMedicalReportAPI()
    result = api.enhance_report(request_data)
    
    print("API Response:")
    print("=" * 50)
    print(f"Status: {result['status']}")
    if result['status'] == 'success':
        print(f"Enhanced Report:\n{result['enhanced_report']}")
    else:
        print(f"Error: {result['error_message']}")

def setup_environment():
    """Setup guide for environment variables."""
    env_guide = """
🔧 ENVIRONMENT SETUP
==================

1. .env dosyası oluştur:
   touch .env

2. API anahtarlarını ekle:
   echo "OPENAI_API_KEY=sk-your-openai-api-key-here" >> .env
   echo "ANTHROPIC_API_KEY=sk-ant-your-anthropic-key-here" >> .env

3. Python'da yükle:
   from dotenv import load_dotenv
   load_dotenv()

4. Test et:
   python simple_llm_enhancer.py
    """
    print(env_guide)

if __name__ == "__main__":
    print("🤖 Simple LLM Medical Report Enhancement Service")
    print("=" * 55)
    print("1. Bu servis medikal raporları LLM ile geliştirir")
    print("2. Frontend'den gelen prompt'ları işler") 
    print("3. Geliştirilmiş raporları döndürür")
    print("4. Synchronous API - async dependencies yok")
    
    print("\n📋 Environment variables rehberi:")
    setup_environment()
    
    print("\n🧪 Test etmek için:")
    print("example_breast_cancer_enhancement()")
    print("example_api_usage()")
    
    # API anahtarı kontrolü
    config = SimpleLLMConfig()
    if config.OPENAI_API_KEY:
        print(f"\n✅ OpenAI API Key: ***{config.OPENAI_API_KEY[-4:]}")
    else:
        print("\n❌ OpenAI API Key: Not configured")
        
    if config.ANTHROPIC_API_KEY:
        print(f"✅ Anthropic API Key: ***{config.ANTHROPIC_API_KEY[-4:]}")
    else:
        print("❌ Anthropic API Key: Not configured")
