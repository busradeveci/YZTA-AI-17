"""
🤖 GEMINI API INTEGRATION FOR MEDICAL REPORT ENHANCEMENT
======================================================

This service handles Google Gemini API integration for enhancing medical analysis reports
with AI-powered insights and recommendations.

Features:
- 🎗️ Breast Cancer: Enhanced morphological analysis reports
- 🫀 Cardiovascular: Detailed cardiac risk assessment reports  
- 👶 Fetal Health: Comprehensive CTG analysis reports
- 🔬 PACE Methodology: Systematic report enhancement
- 🌟 Turkish Language: Native Turkish medical reporting

Integration Points:
- Frontend: "Raporu Geliştir (Chat ile)" button
- Backend: This Gemini service
- Output: Enhanced medical reports with AI insights
"""

import os
import json
import logging
from datetime import datetime
from typing import Dict, Any, Optional, List
from dataclasses import dataclass
from enum import Enum
import asyncio

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

try:
    from dotenv import load_dotenv
    load_dotenv()
    DOTENV_AVAILABLE = True
except ImportError:
    DOTENV_AVAILABLE = False

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class MedicalDomain(Enum):
    """Desteklenen medikal alanlar"""
    BREAST_CANCER = "breast_cancer"
    CARDIOVASCULAR = "cardiovascular"
    FETAL_HEALTH = "fetal_health"

class LLMProvider(Enum):
    """Desteklenen LLM sağlayıcıları"""
    GEMINI = "gemini"

@dataclass
class GeminiConfig:
    """Gemini API configuration"""
    
    # Gemini API settings
    GEMINI_API_KEY: str = os.getenv('GEMINI_API_KEY', '')
    GEMINI_MODEL: str = os.getenv('GEMINI_MODEL', 'gemini-1.5-flash')
    GEMINI_ENDPOINT: str = "https://generativelanguage.googleapis.com/v1beta/models"
    
    # Generation parameters
    TEMPERATURE: float = float(os.getenv('GEMINI_TEMPERATURE', '0.3'))
    MAX_TOKENS: int = int(os.getenv('GEMINI_MAX_TOKENS', '2000'))
    TOP_P: float = float(os.getenv('GEMINI_TOP_P', '0.8'))
    TOP_K: int = int(os.getenv('GEMINI_TOP_K', '40'))
    
    # Safety settings
    SAFETY_THRESHOLD: str = os.getenv('GEMINI_SAFETY_THRESHOLD', 'BLOCK_MEDIUM_AND_ABOVE')

class GeminiReportEnhancer:
    """Professional Gemini service for medical report enhancement."""
    
    def __init__(self, config: Optional[GeminiConfig] = None):
        self.config = config or GeminiConfig()
        self.session = None
        
        # API key kontrolü
        if not self.config.GEMINI_API_KEY:
            logger.warning("Gemini API key not configured. Set GEMINI_API_KEY environment variable.")
    
    async def __aenter__(self):
        """Async context manager entry"""
        if not AIOHTTP_AVAILABLE:
            raise ImportError("aiohttp not available. Install with: pip install aiohttp")
        
        self.session = aiohttp.ClientSession()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit"""
        if self.session:
            await self.session.close()
    
    def _create_medical_prompt(self, domain: str, patient_data: Dict[str, Any], 
                              prediction_result: Dict[str, Any], user_prompt: str) -> str:
        """Create domain-specific medical prompt for Gemini."""
        
        base_prompt = f"""
Sen uzman bir Türk doktorsun ve PACE metodolojisini kullanarak sistematik, kanıt tabanlı medikal raporlar hazırlarsın.

PACE Yaklaşımı:
- PLAN: Analiz planı ve hipotezler
- ANALYZE: Veri analizi ve bulgular  
- CONSTRUCT: Sonuç yapılandırması
- EXECUTE: Öneri ve takip planı

Hasta Verisi: {json.dumps(patient_data, ensure_ascii=False, indent=2)}
AI Tahmin Sonucu: {json.dumps(prediction_result, ensure_ascii=False, indent=2)}

Kullanıcının Sorusu: "{user_prompt}"

GÖREV: Yukarıdaki verileri kullanarak profesyonel bir medikal rapor hazırla.
"""

        if domain == MedicalDomain.BREAST_CANCER.value:
            domain_prompt = """
MEME KANSERİ RAPOR GELİŞTİRME:

1. MORFOLOJİK ANALİZ:
   - Tümör boyutu ve grade değerlendirmesi
   - Lenf nodu tutulum durumu
   - Histopatolojik özellikler

2. MOLEKÜLER BELİRTEÇLER:
   - ER/PR reseptör durumu
   - HER2 ekspresyonu
   - Ki-67 proliferasyon indeksi

3. PROGNOZ DEĞERLENDİRMESİ:
   - TNM staging
   - Prognostik faktörler
   - 5-10 yıllık sağkalım oranları

4. TEDAVİ ÖNERİLERİ:
   - Cerrahi seçenekler
   - Adjuvan terapi
   - Hedefli tedaviler

Raporu Türkçe, anlaşılır ve empati dolu bir dille hazırla.
"""
        
        elif domain == MedicalDomain.CARDIOVASCULAR.value:
            domain_prompt = """
KARDİYOVASKÜLER RAPOR GELİŞTİRME:

1. RİSK FAKTÖRÜ ANALİZİ:
   - Yaş ve cinsiyet faktörleri
   - Kan basıncı değerlendirmesi
   - Kolesterol profili
   - Diyabet durumu

2. KARDİYAK RİSK SKORU:
   - Framingham Risk Skoru
   - ASCVD Risk Calculator
   - European SCORE sistemi

3. ÖNLEYİCİ TEDBİRLER:
   - Yaşam tarzı değişiklikleri
   - Diyet önerileri
   - Egzersiz programı
   - İlaç tedavisi gerekliliği

4. TAKİP PLANI:
   - Kontrol sıklığı
   - Laboratuvar testleri
   - Görüntüleme yöntemleri

Raporu hasta eğitimi odaklı ve motivasyonel dilde hazırla.
"""
        
        elif domain == MedicalDomain.FETAL_HEALTH.value:
            domain_prompt = """
FETAL SAĞLIK RAPOR GELİŞTİRME:

1. CTG ANALİZ SONUÇLARI:
   - Fetal kalp hızı bazal değeri
   - Variabilite değerlendirmesi
   - Akselerasyon ve deselerasyon analizi
   - Uterine kontraksiyon paternleri

2. FETAL REFAH DEĞERLENDİRMESİ:
   - Normal/şüpheli/patolojik sınıflandırma
   - Fetal asidoz riski
   - Intrauterin büyüme kısıtlılığı
   - Oligohidramniyos/polihidramniyos

3. OBSTETRİK YÖNETİM:
   - Doğum zamanlaması
   - Doğum şekli önerileri
   - Ek monitörizasyon gereksinimi
   - Yoğun bakım ihtiyacı

4. ANNE DANIŞMANLIĞI:
   - Dikkat edilmesi gereken belirtiler
   - Kontrol sıklığı
   - Yaşam tarzı önerileri

Raporu anne adayını rahatlatacak ve bilgilendirecek şekilde hazırla.
"""
        
        else:
            domain_prompt = """
GENEL MEDİKAL RAPOR GELİŞTİRME:

1. BULGULAR ÖZETİ
2. KLİNİK YORUMLAMA
3. ÖNERİLER VE TAKİP
4. HASTA EĞİTİMİ

Raporu medikal terminolojiyi açıklayarak ve anlaşılır dilde hazırla.
"""
        
        return base_prompt + "\n" + domain_prompt

    async def _call_gemini_api(self, prompt: str) -> str:
        """Call Gemini API for report enhancement."""
        if not self.config.GEMINI_API_KEY:
            raise ValueError("Gemini API key not configured. Set GEMINI_API_KEY environment variable.")
            
        if not self.session:
            raise RuntimeError("Session not initialized. Use async context manager.")
            
        url = f"{self.config.GEMINI_ENDPOINT}/{self.config.GEMINI_MODEL}:generateContent"
        
        headers = {
            "Content-Type": "application/json",
        }
        
        # Gemini API request format
        payload = {
            "contents": [
                {
                    "parts": [
                        {
                            "text": prompt
                        }
                    ]
                }
            ],
            "generationConfig": {
                "temperature": self.config.TEMPERATURE,
                "topK": self.config.TOP_K,
                "topP": self.config.TOP_P,
                "maxOutputTokens": self.config.MAX_TOKENS,
            },
            "safetySettings": [
                {
                    "category": "HARM_CATEGORY_HARASSMENT",
                    "threshold": self.config.SAFETY_THRESHOLD
                },
                {
                    "category": "HARM_CATEGORY_HATE_SPEECH", 
                    "threshold": self.config.SAFETY_THRESHOLD
                },
                {
                    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                    "threshold": self.config.SAFETY_THRESHOLD
                },
                {
                    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                    "threshold": self.config.SAFETY_THRESHOLD
                }
            ]
        }
        
        # Add API key to URL
        url = f"{url}?key={self.config.GEMINI_API_KEY}"
        
        try:
            async with self.session.post(url, headers=headers, json=payload) as response:
                if response.status == 200:
                    result = await response.json()
                    
                    # Extract text from Gemini response
                    if "candidates" in result and len(result["candidates"]) > 0:
                        candidate = result["candidates"][0]
                        if "content" in candidate and "parts" in candidate["content"]:
                            parts = candidate["content"]["parts"]
                            if len(parts) > 0 and "text" in parts[0]:
                                return parts[0]["text"]
                    
                    # Fallback if structure is different
                    logger.warning(f"Unexpected Gemini response structure: {result}")
                    return "Gemini API'den beklenmeyen yanıt formatı alındı."
                    
                else:
                    error_text = await response.text()
                    logger.error(f"Gemini API error: {response.status} - {error_text}")
                    raise Exception(f"Gemini API error: {response.status} - {error_text}")
                    
        except Exception as e:
            logger.error(f"Gemini API call failed: {str(e)}")
            raise

    async def enhance_medical_report(self, domain: str, patient_data: Dict[str, Any], 
                                   prediction_result: Dict[str, Any], user_prompt: str) -> Dict[str, Any]:
        """Enhance medical report using Gemini API."""
        
        start_time = datetime.now()
        
        try:
            # Validate domain
            valid_domains = [d.value for d in MedicalDomain]
            if domain not in valid_domains:
                raise ValueError(f"Invalid domain: {domain}. Valid domains: {valid_domains}")
            
            # Create medical prompt
            prompt = self._create_medical_prompt(domain, patient_data, prediction_result, user_prompt)
            
            # Call Gemini API
            enhanced_report = await self._call_gemini_api(prompt)
            
            # Calculate processing time
            processing_time = (datetime.now() - start_time).total_seconds()
            
            return {
                "status": "success",
                "enhanced_report": enhanced_report,
                "metadata": {
                    "domain": domain,
                    "provider": "gemini",
                    "model": self.config.GEMINI_MODEL,
                    "enhancement_timestamp": datetime.now().isoformat(),
                    "user_prompt": user_prompt,
                    "original_prediction": prediction_result,
                    "processing_time_seconds": processing_time,
                    "processing_info": {
                        "model_used": self.config.GEMINI_MODEL,
                        "temperature": self.config.TEMPERATURE,
                        "max_tokens": self.config.MAX_TOKENS,
                        "top_p": self.config.TOP_P,
                        "top_k": self.config.TOP_K
                    }
                }
            }
            
        except Exception as e:
            error_message = str(e)
            logger.error(f"Report enhancement failed: {error_message}")
            
            return {
                "status": "error",
                "error_message": error_message,
                "enhanced_report": f"Rapor geliştirme sırasında bir hata oluştu: {error_message}\n\nLütfen tekrar deneyiniz veya sistem yöneticisi ile iletişime geçiniz.",
                "metadata": {
                    "domain": domain,
                    "provider": "gemini",
                    "enhancement_timestamp": datetime.now().isoformat(),
                    "error_details": error_message,
                    "processing_time_seconds": (datetime.now() - start_time).total_seconds()
                }
            }

class SimpleGeminiMedicalAPI:
    """Simple synchronous Gemini API for medical report enhancement."""
    
    def __init__(self, config: Optional[GeminiConfig] = None):
        self.config = config or GeminiConfig()
        
        if not REQUESTS_AVAILABLE:
            raise ImportError("requests not available. Install with: pip install requests")
    
    def _call_gemini_api_sync(self, prompt: str) -> str:
        """Call Gemini API synchronously."""
        if not self.config.GEMINI_API_KEY:
            raise ValueError("Gemini API key not configured. Set GEMINI_API_KEY environment variable.")
        
        url = f"{self.config.GEMINI_ENDPOINT}/{self.config.GEMINI_MODEL}:generateContent"
        url = f"{url}?key={self.config.GEMINI_API_KEY}"
        
        headers = {
            "Content-Type": "application/json",
        }
        
        payload = {
            "contents": [
                {
                    "parts": [
                        {
                            "text": prompt
                        }
                    ]
                }
            ],
            "generationConfig": {
                "temperature": self.config.TEMPERATURE,
                "topK": self.config.TOP_K,
                "topP": self.config.TOP_P,
                "maxOutputTokens": self.config.MAX_TOKENS,
            },
            "safetySettings": [
                {
                    "category": "HARM_CATEGORY_HARASSMENT",
                    "threshold": self.config.SAFETY_THRESHOLD
                },
                {
                    "category": "HARM_CATEGORY_HATE_SPEECH", 
                    "threshold": self.config.SAFETY_THRESHOLD
                },
                {
                    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                    "threshold": self.config.SAFETY_THRESHOLD
                },
                {
                    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                    "threshold": self.config.SAFETY_THRESHOLD
                }
            ]
        }
        
        try:
            response = requests.post(url, headers=headers, json=payload, timeout=30)
            
            if response.status_code == 200:
                result = response.json()
                
                # Extract text from Gemini response
                if "candidates" in result and len(result["candidates"]) > 0:
                    candidate = result["candidates"][0]
                    if "content" in candidate and "parts" in candidate["content"]:
                        parts = candidate["content"]["parts"]
                        if len(parts) > 0 and "text" in parts[0]:
                            return parts[0]["text"]
                
                # Fallback if structure is different
                logger.warning(f"Unexpected Gemini response structure: {result}")
                return "Gemini API'den beklenmeyen yanıt formatı alındı."
                
            else:
                error_text = response.text
                logger.error(f"Gemini API error: {response.status_code} - {error_text}")
                raise Exception(f"Gemini API error: {response.status_code} - {error_text}")
                
        except Exception as e:
            logger.error(f"Gemini API call failed: {str(e)}")
            raise
    
    def enhance_report(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """Enhance medical report synchronously."""
        
        start_time = datetime.now()
        
        try:
            # Extract data
            domain = request_data.get("domain", "")
            patient_data = request_data.get("patient_data", {})
            prediction_result = request_data.get("prediction_result", {})
            user_prompt = request_data.get("user_prompt", "Bu sonuçları detaylı olarak açıklar mısınız?")
            
            # Validate domain
            valid_domains = [d.value for d in MedicalDomain]
            if domain not in valid_domains:
                raise ValueError(f"Invalid domain: {domain}. Valid domains: {valid_domains}")
            
            # Create enhancer instance to use prompt creation method
            enhancer = GeminiReportEnhancer(self.config)
            prompt = enhancer._create_medical_prompt(domain, patient_data, prediction_result, user_prompt)
            
            # Call Gemini API
            enhanced_report = self._call_gemini_api_sync(prompt)
            
            # Calculate processing time
            processing_time = (datetime.now() - start_time).total_seconds()
            
            return {
                "status": "success",
                "enhanced_report": enhanced_report,
                "metadata": {
                    "domain": domain,
                    "provider": "gemini",
                    "model": self.config.GEMINI_MODEL,
                    "enhancement_timestamp": datetime.now().isoformat(),
                    "user_prompt": user_prompt,
                    "original_prediction": prediction_result,
                    "processing_time_seconds": processing_time,
                    "processing_info": {
                        "model_used": self.config.GEMINI_MODEL,
                        "temperature": self.config.TEMPERATURE,
                        "max_tokens": self.config.MAX_TOKENS,
                        "top_p": self.config.TOP_P,
                        "top_k": self.config.TOP_K
                    }
                }
            }
            
        except Exception as e:
            error_message = str(e)
            logger.error(f"Report enhancement failed: {error_message}")
            
            return {
                "status": "error",
                "error_message": error_message,
                "enhanced_report": f"Rapor geliştirme sırasında bir hata oluştu: {error_message}\n\nLütfen tekrar deneyiniz veya sistem yöneticisi ile iletişime geçiniz.",
                "metadata": {
                    "domain": request_data.get("domain", "unknown"),
                    "provider": "gemini",
                    "enhancement_timestamp": datetime.now().isoformat(),
                    "error_details": error_message,
                    "processing_time_seconds": (datetime.now() - start_time).total_seconds()
                }
            }

def setup_environment_variables():
    """Setup environment variables guide"""
    print("🔧 Environment Variables Setup:")
    print("================================")
    print("# .env dosyası oluşturun:")
    print("touch .env")
    print()
    print("# Gemini API anahtarını ekleyin:")
    print("echo 'GEMINI_API_KEY=your-gemini-api-key-here' >> .env")
    print()
    print("# Opsiyonel ayarlar:")
    print("echo 'GEMINI_MODEL=gemini-1.5-flash' >> .env")
    print("echo 'GEMINI_TEMPERATURE=0.3' >> .env")
    print("echo 'GEMINI_MAX_TOKENS=2000' >> .env")
    print()
    print("🔑 Gemini API Key almak için:")
    print("https://makersuite.google.com/app/apikey")

# Test fonksiyonları
async def example_breast_cancer_enhancement():
    """Example breast cancer report enhancement"""
    
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
    
    async with GeminiReportEnhancer() as enhancer:
        result = await enhancer.enhance_medical_report(
            request_data["domain"],
            request_data["patient_data"],
            request_data["prediction_result"],
            request_data["user_prompt"]
        )
        
        print("🎗️ Meme Kanseri Rapor Geliştirme Örneği")
        print("=" * 50)
        print(f"Status: {result['status']}")
        if result['status'] == 'success':
            print(f"Enhanced Report:\n{result['enhanced_report']}")
            print(f"\nProcessing Time: {result['metadata']['processing_time_seconds']:.2f}s")
        else:
            print(f"Error: {result['error_message']}")

def example_sync_api_usage():
    """Example synchronous API usage"""
    
    try:
        api = SimpleGeminiMedicalAPI()
        
        request_data = {
            "domain": "cardiovascular",
            "patient_data": {
                "age": 55,
                "systolic_bp": 140,
                "diastolic_bp": 90,
                "cholesterol": 240,
                "smoking": True
            },
            "prediction_result": {
                "prediction": "high_risk",
                "confidence": 0.75,
                "risk_score": 8.2
            },
            "user_prompt": "Risk faktörlerimi ve yapabileceğim değişiklikleri anlat."
        }
        
        result = api.enhance_report(request_data)
        
        print("🫀 Kardiyovasküler Rapor Geliştirme Örneği")
        print("=" * 50)
        print(f"Status: {result['status']}")
        if result['status'] == 'success':
            print(f"Enhanced Report:\n{result['enhanced_report']}")
            print(f"\nProcessing Time: {result['metadata']['processing_time_seconds']:.2f}s")
        else:
            print(f"Error: {result['error_message']}")
            
    except Exception as e:
        print(f"❌ Test failed: {str(e)}")

if __name__ == "__main__":
    print("🤖 Gemini Medical Report Enhancer")
    print("=" * 50)
    print("1. Bu servis medikal raporları Gemini AI ile geliştirir")
    print("2. Frontend'den gelen prompt'ları işler") 
    print("3. Geliştirilmiş raporları döndürür")
    print("\n📋 Environment variables rehberi:")
    setup_environment_variables()
    
    print("\n🧪 Test etmek için:")
    print("asyncio.run(example_breast_cancer_enhancement())")
    print("example_sync_api_usage()")
    
    # API anahtarı kontrolü
    config = GeminiConfig()
    if config.GEMINI_API_KEY:
        print(f"\n✅ Gemini API Key: ***{config.GEMINI_API_KEY[-4:]}")
    else:
        print("\n❌ Gemini API Key: Not configured")
        print("Set GEMINI_API_KEY environment variable")
