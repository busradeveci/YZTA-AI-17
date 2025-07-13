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
}

export interface TestHistory {
  id: string;
  test_type: string;
  date: string;
  result: HealthTestResponse;
  form_data: Record<string, any>;
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
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      return { data };
    } catch (error) {
      console.error('API request failed:', error);
      return { error: error instanceof Error ? error.message : 'Unknown error' };
    }
  }

  // Sağlık kontrolü
  async healthCheck(): Promise<ApiResponse<{ status: string; timestamp: string }>> {
    return this.request('/health');
  }

  // Mevcut testleri getir
  async getAvailableTests(): Promise<ApiResponse<{ tests: any[] }>> {
    return this.request('/tests');
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
}

export const apiService = new ApiService();

// Mock API fallback - backend çalışmıyorsa kullanılacak
export const mockApiService = {
  async predictHealthRisk(
    testType: string,
    formData: Record<string, any>
  ): Promise<ApiResponse<HealthTestResponse>> {
    // Mock tahmin fonksiyonunu kullan
    const { mockPrediction } = await import('./mockData');
    
    try {
      const result = mockPrediction(testType, formData);
      return {
        data: {
          ...result,
          timestamp: new Date().toISOString(),
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
        },
        form_data: { age: 45, gender: 'Erkek' },
      },
    ];

    return { data: mockHistory };
  },
}; 