import { HealthTest, TestResult } from '../types';

export const healthTests: HealthTest[] = [
  {
    id: 'heart-disease',
    name: 'Kalp Hastalığı Risk Analizi',
    description: 'Kardiyovasküler hastalık risk faktörlerini değerlendirin',
    icon: '❤️',
    fields: [
      { name: 'age', label: 'Yaş', type: 'number', required: true, min: 18, max: 100 },
      { name: 'gender', label: 'Cinsiyet', type: 'select', required: true, options: ['Erkek', 'Kadın'] },
      { name: 'chestPain', label: 'Göğüs Ağrısı Tipi', type: 'select', required: true, options: ['Yok', 'Angina', 'Atypical Angina', 'Non-anginal Pain'] },
      { name: 'bloodPressure', label: 'Sistolik Kan Basıncı (mmHg)', type: 'number', required: true, min: 90, max: 200 },
      { name: 'cholesterol', label: 'Kolesterol (mg/dl)', type: 'number', required: true, min: 100, max: 600 },
      { name: 'bloodSugar', label: 'Açlık Kan Şekeri (mg/dl)', type: 'number', required: true, min: 70, max: 400 },
      { name: 'ecg', label: 'EKG Sonucu', type: 'select', required: true, options: ['Normal', 'ST-T Wave Abnormality', 'Left Ventricular Hypertrophy'] },
      { name: 'maxHeartRate', label: 'Maksimum Kalp Atış Hızı', type: 'number', required: true, min: 60, max: 202 },
      { name: 'exerciseAngina', label: 'Egzersiz Anginası', type: 'checkbox' },
      { name: 'stDepression', label: 'ST Depresyonu', type: 'number', required: true, min: 0, max: 6.2 },
      { name: 'slope', label: 'ST Segment Eğimi', type: 'select', required: true, options: ['Yükselen', 'Düz', 'İnen'] },
      { name: 'vessels', label: 'Tıkalı Damar Sayısı', type: 'select', required: true, options: ['0', '1', '2', '3'] },
      { name: 'thalassemia', label: 'Talasemi', type: 'select', required: true, options: ['Normal', 'Sabit Defekt', 'Tersinir Defekt'] }
    ]
  },
  {
    id: 'fetal-health',
    name: 'Fetal Sağlık Taraması',
    description: 'Hamilelik sırasında fetal sağlık risklerini değerlendirin',
    icon: '👶',
    fields: [
      { name: 'age', label: 'Yaş', type: 'number', required: true, min: 15, max: 50 },
      { name: 'gestationalAge', label: 'Gebelik Haftası', type: 'number', required: true, min: 1, max: 42 },
      { name: 'bloodPressure', label: 'Kan Basıncı (mmHg)', type: 'number', required: true, min: 60, max: 200 },
      { name: 'heartRate', label: 'Kalp Atış Hızı', type: 'number', required: true, min: 60, max: 200 },
      { name: 'fetalMovement', label: 'Fetal Hareket', type: 'select', required: true, options: ['Normal', 'Az', 'Çok'] },
      { name: 'diabetes', label: 'Diyabet', type: 'checkbox' },
      { name: 'smoking', label: 'Sigara Kullanımı', type: 'checkbox' }
    ]
  },
  {
    id: 'breast-cancer',
    name: 'Meme Kanseri Risk Analizi',
    description: 'Meme kanseri risk faktörlerini değerlendirin',
    icon: '🏥',
    fields: [
      { name: 'age', label: 'Yaş', type: 'number', required: true, min: 20, max: 100 },
      { name: 'gender', label: 'Cinsiyet', type: 'select', required: true, options: ['Kadın', 'Erkek'] },
      { name: 'familyHistory', label: 'Aile Geçmişi', type: 'checkbox' },
      { name: 'bmi', label: 'Vücut Kitle İndeksi', type: 'number', required: true, min: 15, max: 50 },
      { name: 'alcohol', label: 'Alkol Kullanımı', type: 'checkbox' },
      { name: 'hormoneTherapy', label: 'Hormon Tedavisi', type: 'checkbox' }
    ]
  },
  {
    id: 'depression',
    name: 'Depresyon Risk Değerlendirmesi',
    description: 'Depresyon risk faktörlerini analiz edin',
    icon: '🧠',
    fields: [
      { name: 'age', label: 'Yaş', type: 'number', required: true, min: 12, max: 100 },
      { name: 'gender', label: 'Cinsiyet', type: 'select', required: true, options: ['Kadın', 'Erkek', 'Diğer'] },
      { name: 'sleepHours', label: 'Günlük Uyku Saati', type: 'number', required: true, min: 0, max: 24 },
      { name: 'stressLevel', label: 'Stres Seviyesi', type: 'select', required: true, options: ['Düşük', 'Orta', 'Yüksek'] },
      { name: 'socialSupport', label: 'Sosyal Destek', type: 'select', required: true, options: ['Var', 'Yok', 'Sınırlı'] },
      { name: 'previousDepression', label: 'Geçmiş Depresyon', type: 'checkbox' },
      { name: 'familyHistory', label: 'Aile Geçmişi', type: 'checkbox' }
    ]
  }
];

export const mockPrediction = (testId: string, formData: Record<string, any>): TestResult => {
  // Sahte tahmin algoritması
  let baseScore = Math.random() * 100;
  
  // Test tipine göre farklı hesaplamalar
  switch (testId) {
    case 'heart-disease':
      if (formData.age > 65) baseScore += 25;
      if (formData.gender === 'Erkek') baseScore += 15;
      if (formData.chestPain !== 'Yok') baseScore += 30;
      if (formData.bloodPressure > 140) baseScore += 20;
      if (formData.cholesterol > 240) baseScore += 15;
      if (formData.bloodSugar > 126) baseScore += 20;
      if (formData.ecg !== 'Normal') baseScore += 25;
      if (formData.exerciseAngina) baseScore += 35;
      if (formData.stDepression > 2) baseScore += 20;
      if (formData.vessels !== '0') baseScore += 30;
      break;
    case 'fetal-health':
      if (formData.age > 35) baseScore += 20;
      if (formData.smoking) baseScore += 30;
      if (formData.diabetes) baseScore += 25;
      break;
    case 'breast-cancer':
      if (formData.familyHistory) baseScore += 40;
      if (formData.age > 50) baseScore += 20;
      if (formData.alcohol) baseScore += 15;
      break;
    case 'depression':
      if (formData.previousDepression) baseScore += 35;
      if (formData.familyHistory) baseScore += 25;
      if (formData.stressLevel === 'Yüksek') baseScore += 20;
      if (formData.socialSupport === 'Yok') baseScore += 15;
      break;
  }
  
  const score = Math.min(100, Math.max(0, baseScore));
  
  let risk: 'low' | 'medium' | 'high';
  let message: string;
  let recommendations: string[];
  
  if (score < 30) {
    risk = 'low';
    message = 'Düşük risk seviyesi. Genel sağlık durumunuz iyi görünüyor.';
    recommendations = [
      'Düzenli sağlık kontrollerinizi aksatmayın',
      'Sağlıklı yaşam tarzınızı sürdürün'
    ];
  } else if (score < 70) {
    risk = 'medium';
    message = 'Orta risk seviyesi. Dikkatli olmanız gereken durumlar var.';
    recommendations = [
      'Bir sağlık uzmanına danışmanızı öneririz',
      'Risk faktörlerinizi azaltmaya odaklanın'
    ];
  } else {
    risk = 'high';
    message = 'Yüksek risk seviyesi. Acil tıbbi değerlendirme gerekli.';
    recommendations = [
      'En kısa sürede bir doktora başvurun',
      'Tüm risk faktörlerinizi doktorunuzla paylaşın',
      'Düzenli takip planı oluşturun'
    ];
  }
  
  return {
    risk,
    score: Math.round(score),
    message,
    recommendations
  };
}; 