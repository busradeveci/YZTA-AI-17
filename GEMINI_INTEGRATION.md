# 🤖 Gemini API Entegrasyonu - YZTA-AI-17

## 📋 Genel Bakış

Bu doküman, YZTA-AI-17 projesine Google Gemini API'nın entegre edilmesini ve "Raporu Geliştir" özelliğinin geliştirilmesini açıklar.

## 🎯 Özellikler

- **🎗️ Meme Kanseri**: Morfokoksal analiz raporlarının AI ile geliştirilmesi
- **🫀 Kardiyovasküler**: Kardiyak risk değerlendirme raporlarının zenginleştirilmesi  
- **👶 Fetal Sağlık**: CTG analiz sonuçlarının detaylandırılması
- **🔬 PACE Metodolojisi**: Sistematik rapor geliştirme yaklaşımı
- **🇹🇷 Türkçe Dil Desteği**: Native Türkçe medikal raporlama
- **🚀 Real-time Processing**: Anlık AI destekli rapor geliştirme

## 📁 Dosya Yapısı

```
YZTA-AI-17/
├── gemini_report_enhancer.py      # Ana Gemini entegrasyon servisi
├── backend/
│   └── main.py                    # FastAPI endpoint (/api/enhance-report)
├── src/
│   ├── pages/
│   │   └── TestResultPage.tsx     # Frontend "Raporu Geliştir" butonu
│   └── utils/
│       └── api.ts                 # API client fonksiyonları
├── .env                          # Environment variables
├── .env.example                  # Environment template
└── test_gemini_integration.py    # Test script
```

## 🚀 Kurulum ve Yapılandırma

### 1. Environment Variables Ayarlama

```bash
# .env dosyası oluşturun
cp .env.example .env

# Gemini API anahtarınızı ekleyin
echo 'GEMINI_API_KEY=your-actual-gemini-api-key-here' >> .env
```

### 2. Gemini API Key Alma

1. [Google AI Studio](https://makersuite.google.com/app/apikey) adresine gidin
2. Google hesabınızla giriş yapın
3. "Create API Key" butonuna tıklayın
4. API anahtarını kopyalayın ve `.env` dosyasına ekleyin

### 3. Bağımlılıkları Yükleme

```bash
# Backend bağımlılıkları
cd backend
pip install -r requirements.txt

# Opsiyonel: Test için
pip install aiohttp python-dotenv
```

## 🔧 API Kullanımı

### Backend Endpoint

```http
POST /api/enhance-report
Content-Type: application/json

{
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
  "user_prompt": "Bu sonuçları detaylı olarak açıklar mısınız?",
  "test_id": "test_12345"
}
```

### Frontend Entegrasyonu

```typescript
// TestResultPage.tsx içinde
const handleChatSubmit = async (e: React.FormEvent) => {
  const requestData = {
    domain: 'breast_cancer',
    patient_data: testResult.form_data || {},
    prediction_result: {
      prediction: testResult.risk,
      confidence: testResult.confidence,
      score: testResult.score,
      message: testResult.message
    },
    user_prompt: chatInput
  };

  const result = await api.enhanceReport(requestData);
  // AI yanıtını göster
};
```

## 🎯 Domain-Specific Prompt Engineering

### Meme Kanseri (Breast Cancer)

```
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
```

### Kardiyovasküler (Cardiovascular)

```
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
```

### Fetal Sağlık (Fetal Health)

```
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
```

## 🧪 Test Etme

```bash
# Entegrasyon testini çalıştır
python test_gemini_integration.py

# Backend'i başlat
python run.py

# Frontend'de "Raporu Geliştir (Chat ile)" butonunu test et
```

## 📊 Response Format

### Başarılı Response

```json
{
  "status": "success",
  "enhanced_report": "Detaylı AI destekli medikal rapor metni...",
  "metadata": {
    "domain": "breast_cancer",
    "provider": "gemini",
    "model": "gemini-1.5-flash",
    "enhancement_timestamp": "2024-01-15T10:30:00",
    "user_prompt": "Kullanıcının sorusu",
    "original_prediction": {
      "prediction": "malignant",
      "confidence": 0.89
    },
    "processing_info": {
      "model_used": "gemini-1.5-flash",
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
  "enhanced_report": "Rapor geliştirme sırasında bir hata oluştu. Lütfen tekrar deneyiniz.",
  "error_message": "Gemini API error: 401",
  "metadata": {
    "domain": "breast_cancer",
    "provider": "gemini",
    "enhancement_timestamp": "2024-01-15T10:30:00",
    "error_details": "API key not valid"
  }
}
```

## 🔒 Güvenlik Considerations

### API Key Güvenliği

- API anahtarlarını asla kod içinde yazmayın
- `.env` dosyasını `.gitignore`'a ekleyin
- Production'da environment variables kullanın

### Medikal Veri Güvenliği

- **HIPAA/GDPR Uyumluluk**: Hasta verilerini log'lamayın
- **HTTPS**: Tüm API çağrıları HTTPS üzerinden
- **Rate Limiting**: API limitlerini uygulayın

## 🚀 Production Deployment

### Environment Variables

```bash
# Production .env
GEMINI_API_KEY=your-production-api-key
GEMINI_MODEL=gemini-1.5-flash
GEMINI_TEMPERATURE=0.3
GEMINI_MAX_TOKENS=2000
DEBUG=false
```

### Backend Başlatma

```bash
# Production modunda
cd backend
python -m uvicorn main:app --host 0.0.0.0 --port 8000

# Veya run.py ile
python run.py
```

## 📈 Performance Metrikleri

- **Response Time**: ~2-5 saniye (Gemini API'ye bağlı)
- **Token Usage**: ~500-2000 token per request
- **Success Rate**: %95+ (API anahtarı geçerli olduğunda)
- **Error Handling**: Graceful fallback mesajları

## 🎯 Kullanım Akışı

1. **Hasta testi tamamlar** → Test sonuç sayfasına yönlendirilir
2. **"Raporu Geliştir (Chat ile)" butonuna tıklar** → Chat alanı açılır
3. **Sorusunu yazar** (örn: "Prognoz hakkında detay verir misiniz?")
4. **Frontend API'ye request gönderir** → Backend Gemini API'yi çağırır
5. **AI destekli rapor döner** → Kullanıcıya gösterilir

## 🔮 Gelecek Geliştirmeler

- [ ] Streaming responses (real-time typing effect)
- [ ] Multi-language support (English, Turkish)
- [ ] Advanced prompt templates
- [ ] Integration with FHIR standards
- [ ] Advanced analytics and reporting
- [ ] Conversation history
- [ ] PDF export with AI insights

## 📞 Support

- **Configuration Issues**: Environment variables kontrol edin
- **API Errors**: Gemini API key ve quota kontrol edin
- **Integration Problems**: Test script çalıştırın

---

**🎯 Bu entegrasyon sayesinde medikal raporlarınız Gemini AI destekli profesyonel içerikle zenginleştirilir!**
