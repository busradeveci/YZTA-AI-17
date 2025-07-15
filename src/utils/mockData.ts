import { HealthTest, TestResult, User, Patient, Doctor, ChatMessage, DashboardStats } from '../types';

// Mock kullanıcılar
export const mockUsers: User[] = [
  {
    id: '1',
    email: 'hasta@example.com',
    name: 'Ahmet Yılmaz',
    userType: 'patient',
    createdAt: new Date('2024-01-15')
  } as Patient,
  {
    id: '2',
    email: 'doktor@example.com',
    name: 'Dr. Ayşe Kaya',
    userType: 'doctor',
    createdAt: new Date('2024-01-10')
  } as Doctor
];

// Sağlık testleri
export const healthTests: HealthTest[] = [
  {
    id: 'heart-disease',
    name: 'Kalp Hastalığı Risk Analizi',
    description: 'Kalp hastalığı risk faktörlerini değerlendirir ve koroner arter hastalığı riskini hesaplar.',
    icon: '❤️',
    category: 'cardiology',
    fields: [
      { name: 'age', label: 'Yaş', type: 'number', required: true, validation: { min: 18, max: 100 } },
      { name: 'gender', label: 'Cinsiyet', type: 'select', required: true, options: ['Erkek', 'Kadın'] },
      { name: 'chestPain', label: 'Göğüs Ağrısı', type: 'select', required: true, options: ['Yok', 'Hafif', 'Orta', 'Şiddetli'] },
      { name: 'bloodPressure', label: 'Sistolik Kan Basıncı (mmHg)', type: 'number', required: true, validation: { min: 70, max: 300 } },
      { name: 'cholesterol', label: 'Kolesterol (mg/dL)', type: 'number', required: true, validation: { min: 100, max: 600 } },
      { name: 'bloodSugar', label: 'Açlık Kan Şekeri (mg/dL)', type: 'number', required: true, validation: { min: 50, max: 400 } },
      { name: 'exerciseAngina', label: 'Egzersiz Anjini', type: 'checkbox', required: false },
      { name: 'smoking', label: 'Sigara Kullanımı', type: 'checkbox', required: false },
      { name: 'diabetes', label: 'Diyabet', type: 'checkbox', required: false },
      { name: 'familyHistory', label: 'Aile Geçmişi', type: 'checkbox', required: false }
    ]
  },
  {
    id: 'fetal-health',
    name: 'Fetal Sağlık Taraması',
    description: 'Hamilelik sırasında fetal sağlık durumunu değerlendirir ve risk faktörlerini analiz eder.',
    icon: '👶',
    category: 'obstetrics',
    fields: [
      { name: 'age', label: 'Anne Yaşı', type: 'number', required: true, validation: { min: 15, max: 50 } },
      { name: 'gestationalAge', label: 'Gebelik Haftası', type: 'number', required: true, validation: { min: 1, max: 42 } },
      { name: 'previousPregnancies', label: 'Önceki Gebelik Sayısı', type: 'number', required: true, validation: { min: 0, max: 10 } },
      { name: 'smoking', label: 'Sigara Kullanımı', type: 'checkbox', required: false },
      { name: 'alcohol', label: 'Alkol Kullanımı', type: 'checkbox', required: false },
      { name: 'diabetes', label: 'Gestasyonel Diyabet', type: 'checkbox', required: false },
      { name: 'hypertension', label: 'Gebelik Hipertansiyonu', type: 'checkbox', required: false },
      { name: 'bleeding', label: 'Vajinal Kanama', type: 'checkbox', required: false },
      { name: 'fetalMovement', label: 'Fetal Hareket Azalması', type: 'checkbox', required: false }
    ]
  },
  {
    id: 'breast-cancer',
    name: 'Meme Kanseri Risk Analizi',
    description: 'Meme kanseri risk faktörlerini değerlendirir ve erken teşhis için öneriler sunar.',
    icon: '🩺',
    category: 'oncology',
    fields: [
      { name: 'age', label: 'Yaş', type: 'number', required: true, validation: { min: 18, max: 100 } },
      { name: 'gender', label: 'Cinsiyet', type: 'select', required: true, options: ['Kadın', 'Erkek'] },
      { name: 'familyHistory', label: 'Aile Geçmişi', type: 'checkbox', required: false },
      { name: 'previousCancer', label: 'Önceki Kanser Geçmişi', type: 'checkbox', required: false },
      { name: 'hormoneTherapy', label: 'Hormon Tedavisi', type: 'checkbox', required: false },
      { name: 'alcohol', label: 'Alkol Kullanımı', type: 'checkbox', required: false },
      { name: 'obesity', label: 'Obezite', type: 'checkbox', required: false },
      { name: 'earlyMenarche', label: 'Erken Adet Başlangıcı (<12 yaş)', type: 'checkbox', required: false },
      { name: 'lateMenopause', label: 'Geç Menopoz (>55 yaş)', type: 'checkbox', required: false }
    ]
  },
  {
    id: 'depression',
    name: 'Depresyon Risk Değerlendirmesi',
    description: 'Depresyon risk faktörlerini analiz eder ve ruh sağlığı durumunu değerlendirir.',
    icon: '🧠',
    category: 'psychology',
    fields: [
      { name: 'age', label: 'Yaş', type: 'number', required: true, validation: { min: 12, max: 100 } },
      { name: 'gender', label: 'Cinsiyet', type: 'select', required: true, options: ['Erkek', 'Kadın', 'Diğer'] },
      { name: 'previousDepression', label: 'Önceki Depresyon Geçmişi', type: 'checkbox', required: false },
      { name: 'familyHistory', label: 'Aile Geçmişi', type: 'checkbox', required: false },
      { name: 'stressLevel', label: 'Stres Seviyesi', type: 'select', required: true, options: ['Düşük', 'Orta', 'Yüksek'] },
      { name: 'socialSupport', label: 'Sosyal Destek', type: 'select', required: true, options: ['Yok', 'Az', 'Orta', 'Yüksek'] },
      { name: 'sleepProblems', label: 'Uyku Problemleri', type: 'checkbox', required: false },
      { name: 'appetiteChanges', label: 'İştah Değişiklikleri', type: 'checkbox', required: false },
      { name: 'suicidalThoughts', label: 'İntihar Düşünceleri', type: 'checkbox', required: false }
    ]
  }
];

// Mock test sonuçları
export const mockTestResults: TestResult[] = [
  {
    id: '1',
    testId: 'heart-disease',
    patientId: '1',
    formData: {
      age: 45,
      gender: 'Erkek',
      chestPain: 'Hafif',
      bloodPressure: 140,
      cholesterol: 220,
      bloodSugar: 110,
      exerciseAngina: false,
      smoking: true,
      diabetes: false,
      familyHistory: true
    },
    risk: 'medium',
    score: 65.5,
    message: 'Orta kalp hastalığı riski. Dikkatli olmanız gereken durumlar var.',
    recommendations: [
      'Bir kardiyolog ile görüşün',
      'Kan basıncınızı düzenli takip edin',
      'Kolesterol seviyelerinizi kontrol ettirin',
      'Sigara kullanımını bırakın'
    ],
    createdAt: new Date('2024-01-20'),
    pdfUrl: '/reports/heart-disease-1.pdf'
  },
  {
    id: '2',
    testId: 'depression',
    patientId: '1',
    formData: {
      age: 45,
      gender: 'Erkek',
      previousDepression: false,
      familyHistory: false,
      stressLevel: 'Orta',
      socialSupport: 'Orta',
      sleepProblems: true,
      appetiteChanges: false,
      suicidalThoughts: false
    },
    risk: 'low',
    score: 25.0,
    message: 'Düşük depresyon riski. Ruh sağlığınız iyi görünüyor.',
    recommendations: [
      'Sosyal bağlantılarınızı güçlü tutun',
      'Düzenli egzersiz yapın',
      'Stres yönetimi tekniklerini öğrenin'
    ],
    createdAt: new Date('2024-01-18'),
    pdfUrl: '/reports/depression-2.pdf'
  }
];

// Dashboard istatistikleri
export const mockDashboardStats: DashboardStats = {
  totalTests: 4,
  completedTests: 2,
  pendingTests: 2,
  averageScore: 45.3
};

// Chatbot mesajları
export const mockChatMessages: ChatMessage[] = [
  {
    id: '1',
    type: 'bot',
    content: 'Merhaba! Size nasıl yardımcı olabilirim? Yeni test eklemek, sonuçları görüntülemek veya başka bir konuda yardım almak istiyorsanız söyleyin.',
    timestamp: new Date()
  }
];

// Chatbot yanıtları
export const chatbotResponses = {
  'yeni test': {
    message: 'Hangi testi eklemek istiyorsunuz? Mevcut testlerimiz: Kalp Hastalığı, Fetal Sağlık, Meme Kanseri, Depresyon.',
    action: 'add_test'
  },
  'tansiyon': {
    message: 'Tansiyon testi için Kalp Hastalığı Risk Analizi testini öneriyorum. Bu test kan basıncı değerlerinizi de değerlendirir.',
    action: 'navigate'
  },
  'sonuçlar': {
    message: 'Test sonuçlarınızı görüntülemek için geçmiş sayfasına yönlendiriliyorsunuz.',
    action: 'show_results'
  },
  'yardım': {
    message: 'Size şu konularda yardımcı olabilirim:\n• Yeni test ekleme\n• Test sonuçlarını görüntüleme\n• PDF rapor indirme\n• Genel sağlık bilgileri',
    action: null
  }
};

// Test tahmin fonksiyonları
export const predictTestResult = (testId: string, formData: Record<string, any>): Omit<TestResult, 'id' | 'patientId' | 'createdAt'> => {
  const test = healthTests.find(t => t.id === testId);
  if (!test) {
    throw new Error('Test bulunamadı');
  }

  let baseScore = Math.random() * 100;
  let risk: 'low' | 'medium' | 'high';
  let message: string;
  let recommendations: string[];

  switch (testId) {
    case 'heart-disease':
      if (formData.age > 65) baseScore += 25;
      if (formData.gender === 'Erkek') baseScore += 15;
      if (formData.chestPain !== 'Yok') baseScore += 30;
      if (formData.bloodPressure > 140) baseScore += 20;
      if (formData.cholesterol > 240) baseScore += 15;
      if (formData.bloodSugar > 126) baseScore += 20;
      if (formData.exerciseAngina) baseScore += 35;
      if (formData.smoking) baseScore += 25;
      if (formData.diabetes) baseScore += 30;
      if (formData.familyHistory) baseScore += 20;

      if (baseScore < 30) {
        risk = 'low';
        message = 'Düşük kalp hastalığı riski. Genel sağlık durumunuz iyi görünüyor.';
        recommendations = [
          'Düzenli kardiyovasküler egzersiz yapın',
          'Sağlıklı beslenme alışkanlıklarını sürdürün',
          'Yıllık sağlık kontrollerinizi aksatmayın'
        ];
      } else if (baseScore < 70) {
        risk = 'medium';
        message = 'Orta kalp hastalığı riski. Dikkatli olmanız gereken durumlar var.';
        recommendations = [
          'Bir kardiyolog ile görüşün',
          'Kan basıncınızı düzenli takip edin',
          'Kolesterol seviyelerinizi kontrol ettirin'
        ];
      } else {
        risk = 'high';
        message = 'Yüksek kalp hastalığı riski. Acil tıbbi değerlendirme gerekli.';
        recommendations = [
          'En kısa sürede bir kardiyologa başvurun',
          'Acil durum belirtilerini öğrenin',
          'Tüm risk faktörlerinizi doktorunuzla paylaşın'
        ];
      }
      break;

    case 'fetal-health':
      if (formData.age > 35) baseScore += 20;
      if (formData.smoking) baseScore += 30;
      if (formData.diabetes) baseScore += 25;
      if (formData.hypertension) baseScore += 35;
      if (formData.bleeding) baseScore += 40;
      if (formData.fetalMovement) baseScore += 45;

      if (baseScore < 30) {
        risk = 'low';
        message = 'Düşük fetal sağlık riski. Hamileliğiniz normal seyrediyor.';
        recommendations = [
          'Düzenli prenatal kontrollerinizi aksatmayın',
          'Sağlıklı beslenme alışkanlıklarınızı sürdürün',
          'Doktorunuzun önerilerini takip edin'
        ];
      } else if (baseScore < 70) {
        risk = 'medium';
        message = 'Orta fetal sağlık riski. Daha sıkı takip gerekebilir.';
        recommendations = [
          'Daha sık prenatal kontrol yapın',
          'Risk faktörlerinizi azaltmaya odaklanın',
          'Uzman doktor takibi altında olun'
        ];
      } else {
        risk = 'high';
        message = 'Yüksek fetal sağlık riski. Acil tıbbi değerlendirme gerekli.';
        recommendations = [
          'En kısa sürede bir perinatologa başvurun',
          'Sürekli tıbbi gözetim altında olun',
          'Tüm belirtileri doktorunuzla paylaşın'
        ];
      }
      break;

    case 'breast-cancer':
      if (formData.familyHistory) baseScore += 40;
      if (formData.previousCancer) baseScore += 50;
      if (formData.hormoneTherapy) baseScore += 25;
      if (formData.alcohol) baseScore += 15;
      if (formData.obesity) baseScore += 20;
      if (formData.earlyMenarche) baseScore += 15;
      if (formData.lateMenopause) baseScore += 15;

      if (baseScore < 30) {
        risk = 'low';
        message = 'Düşük meme kanseri riski. Düzenli kontrollerinizi sürdürün.';
        recommendations = [
          'Yıllık mamografi kontrollerinizi yaptırın',
          'Kendi kendine meme muayenesi öğrenin',
          'Sağlıklı yaşam tarzınızı sürdürün'
        ];
      } else if (baseScore < 70) {
        risk = 'medium';
        message = 'Orta meme kanseri riski. Daha sıkı takip gerekebilir.';
        recommendations = [
          '6 ayda bir meme kontrolü yaptırın',
          'Risk faktörlerinizi azaltmaya odaklanın',
          'Uzman doktor takibi altında olun'
        ];
      } else {
        risk = 'high';
        message = 'Yüksek meme kanseri riski. Acil tıbbi değerlendirme gerekli.';
        recommendations = [
          'En kısa sürede bir onkologa başvurun',
          'Genetik test yaptırmayı düşünün',
          'Sıkı takip programına katılın'
        ];
      }
      break;

    case 'depression':
      if (formData.previousDepression) baseScore += 35;
      if (formData.familyHistory) baseScore += 25;
      if (formData.stressLevel === 'Yüksek') baseScore += 20;
      if (formData.socialSupport === 'Yok') baseScore += 15;
      if (formData.sleepProblems) baseScore += 15;
      if (formData.appetiteChanges) baseScore += 10;
      if (formData.suicidalThoughts) baseScore += 50;

      if (baseScore < 30) {
        risk = 'low';
        message = 'Düşük depresyon riski. Ruh sağlığınız iyi görünüyor.';
        recommendations = [
          'Sosyal bağlantılarınızı güçlü tutun',
          'Düzenli egzersiz yapın',
          'Stres yönetimi tekniklerini öğrenin'
        ];
      } else if (baseScore < 70) {
        risk = 'medium';
        message = 'Orta depresyon riski. Dikkatli olmanız gereken durumlar var.';
        recommendations = [
          'Bir psikolog ile görüşmeyi düşünün',
          'Stres yönetimi tekniklerini uygulayın',
          'Sosyal destek ağınızı genişletin'
        ];
      } else {
        risk = 'high';
        message = 'Yüksek depresyon riski. Profesyonel yardım almanız önerilir.';
        recommendations = [
          'En kısa sürede bir psikiyatriste başvurun',
          'Acil durum hatlarını öğrenin',
          'Güvenilir kişilerle duygularınızı paylaşın'
        ];
      }
      break;

    default:
      risk = 'low';
      message = 'Test sonucu değerlendirilemedi.';
      recommendations = ['Lütfen tekrar deneyin.'];
  }

  return {
    testId,
    formData,
    risk,
    score: Math.round(baseScore * 10) / 10,
    message,
    recommendations,
    pdfUrl: `/reports/${testId}-${Date.now()}.pdf`
  };
}; 