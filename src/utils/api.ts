const API_BASE_URL = 'http://localhost:8000';

export interface ApiResponse<T> {
  data?: T;
  error?: string;
}

export interface HealthTestRequest {
  test_type: string;
  form_data: Record<string, any>;
}

export interface HealthTestResponse {
  risk: 'low' | 'medium' | 'high';
  score: number;
  message: string;
  recommendations: string[];
  timestamp: string;
  confidence?: number;
  model_info?: {
    model_name: string;
    model_type: string;
    loaded_at: string;
  };
}

export interface TestHistory {
  id: string;
  test_type: string;
  date: string;
  result: HealthTestResponse;
  form_data: Record<string, any>;
}

export interface ModelInfo {
  name: string;
  type: string;
  loaded_at: string;
  path: string;
  accuracy?: number;
}

export interface ModelUploadResponse {
  message: string;
  model_name: string;
  model_type: string;
  features: string[];
  accuracy?: number;
}

export interface AvailableTest {
  id: string;
  name: string;
  description: string;
  model_available: boolean;
  estimated_duration: string;
  fields: Array<{
    name: string;
    type: string;
    label: string;
    required: boolean;
    options?: string[];
  }>;
}

class ApiService {
  private async request<T>(
    endpoint: string,
    options: RequestInit = {}
  ): Promise<ApiResponse<T>> {
    try {
      const response = await fetch(`${API_BASE_URL}${endpoint}`, {
        headers: {
          'Content-Type': 'application/json',
          ...options.headers,
        },
        ...options,
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.detail || `HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      return { data };
    } catch (error) {
      console.error('API request failed:', error);
      return { error: error instanceof Error ? error.message : 'Unknown error' };
    }
  }

  // Sağlık kontrolü
  async healthCheck(): Promise<ApiResponse<{ 
    status: string; 
    models_loaded: number;
    available_models: string[];
    timestamp: string; 
  }>> {
    return this.request('/health');
  }

  // Mevcut testleri getir
  async getAvailableTests(): Promise<ApiResponse<{ tests: AvailableTest[] }>> {
    return this.request('/tests');
  }

  // Yüklenen modelleri getir
  async getLoadedModels(): Promise<ApiResponse<{ models: ModelInfo[] }>> {
    return this.request('/models');
  }

  // Model yükle
  async uploadModel(
    file: File,
    modelType?: string,
    accuracy?: number
  ): Promise<ApiResponse<ModelUploadResponse>> {
    try {
      const formData = new FormData();
      formData.append('file', file);
      
      if (modelType) {
        formData.append('model_type', modelType);
      }
      
      if (accuracy) {
        formData.append('accuracy', accuracy.toString());
      }

      const response = await fetch(`${API_BASE_URL}/upload-model`, {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.detail || `HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      return { data };
    } catch (error) {
      console.error('Model upload failed:', error);
      return { error: error instanceof Error ? error.message : 'Unknown error' };
    }
  }

  // Model sil
  async deleteModel(modelName: string): Promise<ApiResponse<{ message: string }>> {
    return this.request(`/models/${modelName}`, {
      method: 'DELETE',
    });
  }

  // Sağlık riski tahmini
  async predictHealthRisk(
    testType: string,
    formData: Record<string, any>
  ): Promise<ApiResponse<HealthTestResponse>> {
    return this.request('/predict', {
      method: 'POST',
      body: JSON.stringify({
        test_type: testType,
        form_data: formData,
      }),
    });
  }

  // Test geçmişini getir
  async getTestHistory(): Promise<ApiResponse<TestHistory[]>> {
    return this.request('/history');
  }

  // Belirli bir testi getir
  async getTestById(testId: string): Promise<ApiResponse<TestHistory>> {
    return this.request(`/history/${testId}`);
  }

  // Backend bağlantısını kontrol et
  async checkBackendConnection(): Promise<boolean> {
    try {
      const response = await this.healthCheck();
      return !response.error;
    } catch {
      return false;
    }
  }
}

export const apiService = new ApiService();

// Mock API fallback - backend çalışmıyorsa kullanılacak
export const mockApiService = {
  async predictHealthRisk(
    testType: string,
    formData: Record<string, any>
  ): Promise<ApiResponse<HealthTestResponse>> {
    // Mock tahmin fonksiyonunu kullan
    const { predictTestResult } = await import('./mockData');

    try {
      const result = predictTestResult(testType, formData);
      return {
        data: {
          ...result,
          timestamp: new Date().toISOString(),
          confidence: 0.85, // Mock güven skoru
          model_info: {
            model_name: 'mock_model',
            model_type: 'MockModel',
            loaded_at: new Date().toISOString(),
          },
        },
      };
    } catch (error) {
      return { error: 'Mock prediction failed' };
    }
  },

  async getTestHistory(): Promise<ApiResponse<TestHistory[]>> {
    // Mock geçmiş verisi
    const mockHistory: TestHistory[] = [
      {
        id: '1',
        test_type: 'heart-disease',
        date: '2024-01-15T10:30:00Z',
        result: {
          risk: 'low',
          score: 25,
          message: 'Düşük kalp hastalığı riski',
          recommendations: ['Düzenli egzersiz yapın', 'Sağlıklı beslenin'],
          timestamp: '2024-01-15T10:30:00Z',
          confidence: 0.85,
          model_info: {
            model_name: 'mock_heart_model',
            model_type: 'MockModel',
            loaded_at: '2024-01-15T10:00:00Z',
          },
        },
        form_data: { age: 45, gender: 'Erkek' },
      },
    ];

    return { data: mockHistory };
  },

  async getAvailableTests(): Promise<ApiResponse<{ tests: AvailableTest[] }>> {
    const mockTests: AvailableTest[] = [
      {
        id: 'heart-disease',
        name: 'Kalp Hastalığı Risk Analizi',
        description: 'Kardiyovasküler risk faktörlerini değerlendirir',
        model_available: false,
        estimated_duration: '5-10 dakika',
        fields: [
          { name: 'age', type: 'number', label: 'Yaş', required: true },
          { name: 'gender', type: 'select', label: 'Cinsiyet', options: ['Erkek', 'Kadın'], required: true },
        ],
      },
    ];

    return { data: { tests: mockTests } };
  },

  async getLoadedModels(): Promise<ApiResponse<{ models: ModelInfo[] }>> {
    return { data: { models: [] } };
  },
}; 