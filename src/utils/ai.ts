import { TestResult } from '../types';

const GEMINI_API_KEY = 'AIzaSyDI0izrWeB4e6XlTuiYgNUejvbpLrN1L4E';
const GEMINI_API_URL = 'https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent';

export interface AIResponse {
  response: string;
  confidence: number;
  sources?: string[];
}

// Resmi doktor prompt oluşturucusu
function buildDoctorPrompt(testResult: TestResult | null, userInput: string, context?: string): string {
  const isInitialAnalysis = context === 'initial_analysis';
  
  // Test sonuçlarını detaylı şekilde hazırla
  let testDetails = '';
  if (testResult) {
    testDetails = `
HASTA VERİLERİ (HAFIZADA TUTMANIZ GEREKEN BİLGİLER):
- Test ID: ${testResult.testId}
- Test Tarihi: ${new Date(testResult.createdAt).toLocaleDateString('tr-TR')}
- Risk Seviyesi: ${testResult.risk} 
- Risk Skoru: ${testResult.score}/100
- Form Verileri: ${JSON.stringify(testResult.formData, null, 2)}
- Önceki Değerlendirme: ${testResult.message}
- Verilen Öneriler: ${testResult.recommendations.join(' | ')}

Bu bilgileri hafızanızda tutun. Hasta soruları sorduğunda bu verilere dayanarak yanıt verin.
`;
  }
  
  return `
Siz deneyimli bir Türk doktorusunuz. Bu hastanın test sonuçlarını analiz etmiş ve hafızanızda tutuyorsunuz.

${testDetails}

HASTA SORUSU: "${userInput}"

GÖREVLER:
• Bu hastanın verilerini hafızanızda tutun
• Soruları bu test sonuçlarına göre yanıtlayın
• ${isInitialAnalysis ? 'İlk analizi yapın ve sonuçları özetleyin' : 'Mevcut veriler ışığında soruyu yanıtlayın'}
• Profesyonel ama anlaşılır dil kullanın
• Maksimum 150 kelime

${isInitialAnalysis ? `
İlk değerlendirmenizi yapın ve hastaya test sonuçlarını açıklayın.
` : `
Hastanın sorusunu bu test verilerine dayanarak yanıtlayın. Test sonuçlarını ve form verilerini dikkate alın.
`}

YANIT FORMATI:
{
  "response": "Test verilerinize göre detaylı, kişiselleştirilmiş yanıt",
  "confidence": 90,
  "sources": ["test_results", "medical_analysis"]
}

ÖNEMLİ: Sadece JSON formatında yanıt ver, başka hiçbir şey yazma!`;
}

// AI yanıt parse işlevi
function parseAIResponse(aiResponse: string): AIResponse {
  try {
    // JSON'u temizle
    const cleanResponse = aiResponse.trim();
    const jsonMatch = cleanResponse.match(/\{[\s\S]*\}/);
    
    if (jsonMatch) {
      const parsed = JSON.parse(jsonMatch[0]);
      return {
        response: parsed.response || "Yanıt alınamadı.",
        confidence: parsed.confidence || 70,
        sources: parsed.sources || ["general_medical"]
      };
    }
    
    throw new Error('JSON bulunamadı');
  } catch (error) {
    console.error('AI Response Parse Error:', error);
    return {
      response: aiResponse.includes('Sayın hasta') || aiResponse.includes('Klinik') 
        ? aiResponse 
        : `Sayın hasta, ${aiResponse}`,
      confidence: 60,
      sources: ["fallback"]
    };
  }
}

// Fallback yanıt oluşturucu
function generateFallbackResponse(userInput: string): AIResponse {
  const greetings = [
    "Sayın hasta,",
    "Sayın hasta, test sonuçlarınıza göre",
    "Klinik değerlendirmemize göre"
  ];
  
  const responses = [
    "Şu anda teknik bir sorun yaşanmaktadır. Lütfen daha sonra tekrar deneyiniz.",
    "Sistem geçici olarak erişilemez durumda. Sorularınızı daha sonra tekrar iletebilirsiniz.",
    "Bağlantı sorunu nedeniyle yanıt alınamadı. Lütfen tekrar deneyiniz.",
    "Geçici bir teknik sorun yaşanıyor. Sorularınızı tekrar iletebilirsiniz."
  ];
  
  const randomGreeting = greetings[Math.floor(Math.random() * greetings.length)];
  const randomResponse = responses[Math.floor(Math.random() * responses.length)];
  
  return {
    response: `${randomGreeting} ${randomResponse}`,
    confidence: 75,
    sources: ["system_fallback"]
  };
}

// Ana AI analiz işlevi
export async function analyzeWithAI(
  userInput: string, 
  testResult: TestResult | null = null, 
  context?: string
): Promise<AIResponse> {
  try {
    if (!userInput.trim()) {
      return generateFallbackResponse("Genel danışmanlık");
    }

    const prompt = buildDoctorPrompt(testResult, userInput, context);
    
    console.log('API çağrısı başlatılıyor...');
    console.log('Prompt:', prompt.substring(0, 200) + '...');
    
    const response = await fetch(GEMINI_API_URL + `?key=${GEMINI_API_KEY}`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        contents: [{
          parts: [{
            text: prompt
          }]
        }],
        generationConfig: {
          temperature: 0.7,
          topK: 40,
          topP: 0.95,
          maxOutputTokens: 1024,
        }
      })
    });

    console.log('API yanıt durumu:', response.status);
    
    if (!response.ok) {
      const errorText = await response.text();
      console.error('API Hatası:', errorText);
      throw new Error(`API Error: ${response.status} - ${errorText}`);
    }

    const data = await response.json();
    console.log('API yanıtı alındı:', data);
    
    const aiResponse = data.candidates[0]?.content?.parts[0]?.text || "Yanıt alınamadı.";
    console.log('AI Yanıt:', aiResponse);
    
    return parseAIResponse(aiResponse);
  } catch (error) {
    console.error('AI Analysis Error:', error);
    return generateFallbackResponse(userInput);
  }
}

// Test-specific AI analiz işlevi
export async function getTestSpecificAdvice(testResult: TestResult): Promise<AIResponse> {
  const question = `Bu test sonucumu değerlendirir misin? ${testResult.testId} ID'li testi yaptım ve sonuçlarım hakkında bilgi almak istiyorum.`;
  return analyzeWithAI(question, testResult, 'Test sonucu değerlendirme');
}

// Genel sağlık danışmanlığı
export async function getGeneralHealthAdvice(question: string): Promise<AIResponse> {
  return analyzeWithAI(question, null, 'Genel sağlık danışmanlığı');
}

const aiUtils = {
  analyzeWithAI,
  getTestSpecificAdvice,
  getGeneralHealthAdvice
};

export default aiUtils;
