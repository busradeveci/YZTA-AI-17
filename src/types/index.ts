export interface User {
  id: string;
  email: string;
  name: string;
  userType: 'patient' | 'doctor';
  createdAt: Date;
}

export interface Patient extends User {
  userType: 'patient';
  age?: number;
  gender?: 'male' | 'female' | 'other';
  phone?: string;
}

export interface Doctor extends User {
  userType: 'doctor';
  specialization?: string;
  licenseNumber?: string;
}

export interface HealthTest {
  id: string;
  name: string;
  description: string;
  icon: string;
  fields: TestField[];
  category: 'cardiology' | 'obstetrics' | 'oncology' | 'psychology';
}

export interface TestField {
  name: string;
  label: string;
  type: 'text' | 'number' | 'select' | 'radio' | 'checkbox';
  required: boolean;
  options?: string[];
  validation?: {
    min?: number;
    max?: number;
    pattern?: string;
  };
}

export interface TestResult {
  id: string;
  testId: string;
  patientId: string;
  doctorId?: string;
  formData: Record<string, any>;
  risk: 'low' | 'medium' | 'high';
  score: number;
  message: string;
  recommendations: string[];
  createdAt: Date;
  pdfUrl?: string;
  confidence?: number;
  model_info?: {
    model_name: string;
    model_type: string;
    loaded_at: string;
  };
}

export interface ChatMessage {
  id: string;
  type: 'user' | 'bot';
  content: string;
  timestamp: Date;
  action?: 'add_test' | 'show_results' | 'navigate';
}

export interface DashboardStats {
  totalTests: number;
  completedTests: number;
  pendingTests: number;
  averageScore: number;
}

export interface AuthState {
  user: User | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  error: string | null;
}

export interface TestHistory {
  id: string;
  testType: string;
  date: string;
  result: {
    risk: string;
    score: number;
    message: string;
    recommendations: string[];
  };
  formData: Record<string, any>;
} 