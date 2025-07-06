export interface HealthTest {
  id: string;
  name: string;
  description: string;
  icon: string;
  fields: FormField[];
}

export interface FormField {
  name: string;
  label: string;
  type: 'number' | 'select' | 'checkbox' | 'text';
  required?: boolean;
  options?: string[];
  min?: number;
  max?: number;
}

export interface TestResult {
  risk: 'low' | 'medium' | 'high';
  score: number;
  message: string;
  recommendations: string[];
}

export interface TestHistory {
  id: string;
  testType: string;
  date: string;
  result: TestResult;
  formData: Record<string, any>;
} 