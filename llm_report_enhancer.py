"""
🤖 LLM INTEGRATION SERVICE FOR MEDICAL REPORT ENHANCEMENT
========================================================

This service handles LLM integration for enhancing medical analysis reports
with AI-powered insights and recommendations.

Features:
- 🎗️ Breast Cancer: Enhanced morphological analysis reports
- 🫀 Cardiovascular: Detailed cardiac risk assessment reports  
- 👶 Fetal Health: Comprehensive CTG analysis reports
- 🔬 PACE Methodology: Systematic report enhancement

Integration Points:
- Frontend: "Raporu Geliştir (Chat ile)" button
- Backend: This LLM service
- Output: Enhanced medical reports with AI insights
"""

import json
import logging
from datetime import datetime
from typing import Dict, Any, Optional, List, Union
from dataclasses import dataclass
import asyncio
from enum import Enum

# Import handling for optional dependencies
try:
    import aiohttp
    AIOHTTP_AVAILABLE = True
except ImportError:
    AIOHTTP_AVAILABLE = False
    aiohttp = None

try:
    import requests
    REQUESTS_AVAILABLE = True
except ImportError:
    REQUESTS_AVAILABLE = False
    requests = None

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MedicalDomain(Enum):
    """Medical analysis domains."""
    BREAST_CANCER = "breast_cancer"
    CARDIOVASCULAR = "cardiovascular" 
    FETAL_HEALTH = "fetal_health"

class ReportType(Enum):
    """Types of medical reports."""
    DIAGNOSTIC = "diagnostic"
    RISK_ASSESSMENT = "risk_assessment"
    RECOMMENDATION = "recommendation"
    COMPREHENSIVE = "comprehensive"

@dataclass
class MedicalContext:
    """Medical context data for LLM enhancement."""
    domain: MedicalDomain
    patient_data: Dict[str, Any]
    prediction_result: Dict[str, Any]
    model_metadata: Dict[str, Any]
    analysis_timestamp: str
    
class LLMConfig:
    """LLM service configuration."""
    
    # OpenAI Configuration (örnek)
    OPENAI_API_KEY = None  # Environment variable'dan alınacak
    OPENAI_MODEL = "gpt-4"
    OPENAI_MAX_TOKENS = 2000
    OPENAI_TEMPERATURE = 0.3  # Medical için düşük temperature
    
    # Alternative LLM providers
    ANTHROPIC_API_KEY = None
    ANTHROPIC_MODEL = "claude-3-sonnet"
    
    # Local LLM options
    OLLAMA_ENDPOINT = "http://localhost:11434"
    OLLAMA_MODEL = "llama2-medical"
    
    # Default provider
    DEFAULT_PROVIDER = "openai"  # openai, anthropic, ollama
    
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

    🎯 GÖREV:
    1. Sonuçları klinik perspektiften yorumla
    2. Risk faktörlerini analiz et
    3. Önerilen takip adımlarını belirt
    4. Hasta için anlaşılır açıklamalar yap
    5. Gerekirse ek testleri öner

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

    🎯 GÖREV:
    1. Kardiyovasküler risk seviyesini değerlendir
    2. Yaşam tarzı önerilerini belirt
    3. Medikal takip gereksinimlerini açıkla
    4. Önleme stratejilerini öner
    5. Acil duruma işaret eden faktörleri belirt

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

    🎯 GÖREV:
    1. Fetal kalp hızı paternini yorumla
    2. CTG bulgularının klinik anlamını açıkla
    3. Gebelik takip önerilerini belirt
    4. Risk durumlarını değerlendir
    5. Anne adayı için rehberlik sağla

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

class LLMReportEnhancer:
    """Professional LLM service for medical report enhancement."""
    
    def __init__(self, config: Optional[LLMConfig] = None):
        """Initialize LLM service."""
        self.config = config or LLMConfig()
        self.session = None
        
        # Check dependencies
        if not AIOHTTP_AVAILABLE:
            logger.warning("aiohttp not available. Async functionality will be limited.")
            
    async def __aenter__(self):
        """Async context manager entry."""
        if AIOHTTP_AVAILABLE and aiohttp:
            self.session = aiohttp.ClientSession()
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        if self.session:
            await self.session.close()
    
    def _prepare_prompt(self, medical_context: MedicalContext, 
                       user_prompt: str) -> str:
        """Prepare comprehensive prompt for LLM."""
        
        # Get domain-specific template
        template = MedicalPromptTemplates.get_template(medical_context.domain)
        
        # Fill template with medical context
        base_prompt = template.format(
            patient_data=json.dumps(medical_context.patient_data, indent=2, ensure_ascii=False),
            prediction_result=json.dumps(medical_context.prediction_result, indent=2, ensure_ascii=False),
            model_metadata=json.dumps(medical_context.model_metadata, indent=2, ensure_ascii=False)
        )
        
        # Add user's specific prompt
        enhanced_prompt = f"""
        {base_prompt}

        👤 KULLANICI TALEBİ:
        {user_prompt}

        🎯 EK TALİMATLAR:
        - Yukarıdaki kullanıcı talebini de dikkate alarak raporunu geliştir
        - Medikal terminolojiyi uygun yerlerde kullan ama açıklamalarını da ekle
        - Raporu yapılandırılmış ve okunabilir formatta hazırla
        - Önemli noktaları vurgula
        - Gerekirse kaynak önerilerinde bulun
        """
        
        return enhanced_prompt
    
    async def _call_openai_api(self, prompt: str) -> str:
        """Call OpenAI API for report enhancement."""
        if not self.config.OPENAI_API_KEY:
            raise ValueError("OpenAI API key not configured")
            
        if not self.session:
            raise RuntimeError("Session not initialized. Use async context manager.")
            
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
            "max_tokens": self.config.OPENAI_MAX_TOKENS,
            "temperature": self.config.OPENAI_TEMPERATURE,
            "top_p": 1,
            "frequency_penalty": 0,
            "presence_penalty": 0
        }
        
        async with self.session.post(
            "https://api.openai.com/v1/chat/completions",
            headers=headers,
            json=payload
        ) as response:
            if response.status == 200:
                result = await response.json()
                return result["choices"][0]["message"]["content"]
            else:
                error_text = await response.text()
                raise Exception(f"OpenAI API error: {response.status} - {error_text}")
    
    async def _call_anthropic_api(self, prompt: str) -> str:
        """Call Anthropic Claude API for report enhancement."""
        if not self.config.ANTHROPIC_API_KEY:
            raise ValueError("Anthropic API key not configured")
            
        if not self.session:
            raise RuntimeError("Session not initialized. Use async context manager.")
            
        headers = {
            "x-api-key": self.config.ANTHROPIC_API_KEY,
            "Content-Type": "application/json",
            "anthropic-version": "2023-06-01"
        }
        
        payload = {
            "model": self.config.ANTHROPIC_MODEL,
            "max_tokens": self.config.OPENAI_MAX_TOKENS,
            "temperature": self.config.OPENAI_TEMPERATURE,
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        }
        
        async with self.session.post(
            "https://api.anthropic.com/v1/messages",
            headers=headers,
            json=payload
        ) as response:
            if response.status == 200:
                result = await response.json()
                return result["content"][0]["text"]
            else:
                error_text = await response.text()
                raise Exception(f"Anthropic API error: {response.status} - {error_text}")
    
    async def _call_ollama_api(self, prompt: str) -> str:
        """Call local Ollama API for report enhancement."""
        if not self.session:
            raise RuntimeError("Session not initialized. Use async context manager.")
            
        payload = {
            "model": self.config.OLLAMA_MODEL,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": self.config.OPENAI_TEMPERATURE,
                "top_p": 1,
                "top_k": 40
            }
        }
        
        async with self.session.post(
            f"{self.config.OLLAMA_ENDPOINT}/api/generate",
            json=payload
        ) as response:
            if response.status == 200:
                result = await response.json()
                return result["response"]
            else:
                error_text = await response.text()
                raise Exception(f"Ollama API error: {response.status} - {error_text}")
    
    async def enhance_medical_report(self, 
                                   medical_context: MedicalContext,
                                   user_prompt: str,
                                   provider: Optional[str] = None) -> Dict[str, Any]:
        """
        Enhance medical report using LLM.
        
        Args:
            medical_context: Medical data and prediction context
            user_prompt: User's specific enhancement request
            provider: LLM provider to use (openai, anthropic, ollama)
            
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
                enhanced_content = await self._call_openai_api(enhanced_prompt)
            elif provider == "anthropic":
                enhanced_content = await self._call_anthropic_api(enhanced_prompt)
            elif provider == "ollama":
                enhanced_content = await self._call_ollama_api(enhanced_prompt)
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
                        "temperature": self.config.OPENAI_TEMPERATURE,
                        "max_tokens": self.config.OPENAI_MAX_TOKENS
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

class MedicalReportAPIHandler:
    """API handler for medical report enhancement requests."""
    
    def __init__(self):
        """Initialize API handler."""
        self.llm_enhancer = LLMReportEnhancer()
    
    async def handle_report_enhancement_request(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Handle incoming report enhancement request from frontend.
        
        Expected request_data format:
        {
            "domain": "breast_cancer" | "cardiovascular" | "fetal_health",
            "patient_data": {...},
            "prediction_result": {...},
            "model_metadata": {...},
            "user_prompt": "Kullanıcının rapor geliştirme talebi",
            "llm_provider": "openai" | "anthropic" | "ollama" (optional)
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
            async with self.llm_enhancer:
                result = await self.llm_enhancer.enhance_medical_report(
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
async def example_breast_cancer_enhancement():
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
    
    async with LLMReportEnhancer() as enhancer:
        result = await enhancer.enhance_medical_report(sample_context, user_prompt)
        print("Enhanced Report:")
        print(result["enhanced_report"])

def setup_environment_variables():
    """Setup guide for environment variables."""
    env_guide = """
    # .env dosyasına eklenecek LLM API anahtarları:
    
    # OpenAI
    OPENAI_API_KEY=sk-your-openai-api-key-here
    
    # Anthropic Claude
    ANTHROPIC_API_KEY=sk-ant-your-anthropic-key-here
    
    # Ollama (Local)
    OLLAMA_ENDPOINT=http://localhost:11434
    OLLAMA_MODEL=llama2-medical
    
    # Default provider
    LLM_DEFAULT_PROVIDER=openai
    """
    print(env_guide)

if __name__ == "__main__":
    print("🤖 LLM Medical Report Enhancement Service")
    print("=" * 50)
    print("1. Bu servis medikal raporları LLM ile geliştirir")
    print("2. Frontend'den gelen prompt'ları işler") 
    print("3. Geliştirilmiş raporları döndürür")
    print("\n📋 Environment variables rehberi:")
    setup_environment_variables()
    
    print("\n🧪 Test etmek için:")
    print("asyncio.run(example_breast_cancer_enhancement())")
