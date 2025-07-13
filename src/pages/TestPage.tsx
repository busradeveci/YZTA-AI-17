import React, { useState } from 'react';
import {
  Container,
  Typography,
  Paper,
  TextField,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  FormControlLabel,
  Checkbox,
  Button,
  Box,
  Stepper,
  Step,
  StepLabel,
  Alert,
  CircularProgress
} from '@mui/material';
import { useParams, useNavigate } from 'react-router-dom';
import { healthTests } from '../utils/mockData';
import { TestResult } from '../types';
import { apiService, mockApiService } from '../utils/api';

const TestPage: React.FC = () => {
  const { testId } = useParams<{ testId: string }>();
  const navigate = useNavigate();
  const [formData, setFormData] = useState<Record<string, any>>({});
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<TestResult | null>(null);
  const [errors, setErrors] = useState<Record<string, string>>({});

  const test = healthTests.find(t => t.id === testId);

  if (!test) {
    return (
      <Container maxWidth="md" sx={{ py: 4 }}>
        <Alert severity="error">
          Test bulunamadı. Lütfen ana sayfaya dönün.
        </Alert>
        <Button onClick={() => navigate('/')} sx={{ mt: 2 }}>
          Ana Sayfaya Dön
        </Button>
      </Container>
    );
  }

  const handleInputChange = (fieldName: string, value: any) => {
    setFormData(prev => ({
      ...prev,
      [fieldName]: value
    }));
    
    // Clear error when user starts typing
    if (errors[fieldName]) {
      setErrors(prev => ({
        ...prev,
        [fieldName]: ''
      }));
    }
  };

  const validateForm = (): boolean => {
    const newErrors: Record<string, string> = {};
    
    test.fields.forEach(field => {
      if (field.required && !formData[field.name]) {
        newErrors[field.name] = 'Bu alan zorunludur';
      }
      
      if (field.type === 'number' && formData[field.name]) {
        const num = Number(formData[field.name]);
        if (field.min && num < field.min) {
          newErrors[field.name] = `Minimum değer: ${field.min}`;
        }
        if (field.max && num > field.max) {
          newErrors[field.name] = `Maksimum değer: ${field.max}`;
        }
      }
    });
    
    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = async () => {
    if (!validateForm()) return;
    
    setLoading(true);
    
    try {
      // Önce gerçek API'yi dene
      const response = await apiService.predictHealthRisk(testId!, formData);
      
      if (response.error) {
        // API çalışmıyorsa mock servisi kullan
        console.log('API çalışmıyor, mock servis kullanılıyor...');
        const mockResponse = await mockApiService.predictHealthRisk(testId!, formData);
        
        if (mockResponse.data) {
          setResult(mockResponse.data);
        } else {
          throw new Error('Mock prediction failed');
        }
      } else if (response.data) {
        setResult(response.data);
      }
    } catch (error) {
      console.error('Prediction error:', error);
      // Hata durumunda mock servisi kullan
      const mockResponse = await mockApiService.predictHealthRisk(testId!, formData);
      if (mockResponse.data) {
        setResult(mockResponse.data);
      }
    } finally {
      setLoading(false);
    }
  };

  const renderField = (field: any) => {
    const value = formData[field.name] || '';
    const error = errors[field.name];

    switch (field.type) {
      case 'number':
        return (
          <TextField
            key={field.name}
            fullWidth
            label={field.label}
            type="number"
            value={value}
            onChange={(e) => handleInputChange(field.name, e.target.value)}
            error={!!error}
            helperText={error}
            inputProps={{
              min: field.min,
              max: field.max
            }}
            sx={{ mb: 2 }}
          />
        );
      
      case 'select':
        return (
          <FormControl key={field.name} fullWidth sx={{ mb: 2 }} error={!!error}>
            <InputLabel>{field.label}</InputLabel>
            <Select
              value={value}
              label={field.label}
              onChange={(e) => handleInputChange(field.name, e.target.value)}
            >
              {field.options?.map((option: string) => (
                <MenuItem key={option} value={option}>
                  {option}
                </MenuItem>
              ))}
            </Select>
            {error && (
              <Typography variant="caption" color="error" sx={{ mt: 0.5, ml: 1.5 }}>
                {error}
              </Typography>
            )}
          </FormControl>
        );
      
      case 'checkbox':
        return (
          <FormControlLabel
            key={field.name}
            control={
              <Checkbox
                checked={value}
                onChange={(e) => handleInputChange(field.name, e.target.checked)}
              />
            }
            label={field.label}
            sx={{ mb: 1 }}
          />
        );
      
      default:
        return (
          <TextField
            key={field.name}
            fullWidth
            label={field.label}
            value={value}
            onChange={(e) => handleInputChange(field.name, e.target.value)}
            error={!!error}
            helperText={error}
            sx={{ mb: 2 }}
          />
        );
    }
  };

  const getRiskColor = (risk: string) => {
    switch (risk) {
      case 'low': return 'success';
      case 'medium': return 'warning';
      case 'high': return 'error';
      default: return 'info';
    }
  };

  if (result) {
    return (
      <Container maxWidth="md" sx={{ py: 4 }}>
        <Paper elevation={3} sx={{ p: 4, textAlign: 'center' }}>
          <Typography variant="h4" gutterBottom sx={{ fontWeight: 700 }}>
            {test.name} - Sonuçlar
          </Typography>
          
          <Box sx={{ my: 4 }}>
            <Typography variant="h2" sx={{ fontWeight: 700, mb: 2 }}>
              {result.score}%
            </Typography>
            <Alert 
              severity={getRiskColor(result.risk) as any}
              sx={{ mb: 3, fontSize: '1.1rem' }}
            >
              {result.message}
            </Alert>
          </Box>

          <Box sx={{ textAlign: 'left', mb: 4 }}>
            <Typography variant="h6" gutterBottom sx={{ fontWeight: 600 }}>
              Öneriler:
            </Typography>
            <ul>
              {result.recommendations.map((rec, index) => (
                <li key={index}>
                  <Typography variant="body1">
                    {rec}
                  </Typography>
                </li>
              ))}
            </ul>
          </Box>

          <Box sx={{ display: 'flex', gap: 2, justifyContent: 'center' }}>
            <Button
              variant="contained"
              size="large"
              onClick={() => {
                setResult(null);
                setFormData({});
              }}
            >
              Yeni Test
            </Button>
            <Button
              variant="outlined"
              size="large"
              onClick={() => navigate('/')}
            >
              Ana Sayfa
            </Button>
          </Box>
        </Paper>
      </Container>
    );
  }

  return (
    <Container maxWidth="md" sx={{ py: 4 }}>
      <Paper elevation={3} sx={{ p: 4 }}>
        <Box sx={{ textAlign: 'center', mb: 4 }}>
          <Typography variant="h3" gutterBottom sx={{ fontWeight: 700 }}>
            {test.icon} {test.name}
          </Typography>
          <Typography variant="body1" color="text.secondary">
            {test.description}
          </Typography>
        </Box>

        <Stepper activeStep={0} sx={{ mb: 4 }}>
          <Step>
            <StepLabel>Bilgileri Girin</StepLabel>
          </Step>
          <Step>
            <StepLabel>Analiz</StepLabel>
          </Step>
          <Step>
            <StepLabel>Sonuçlar</StepLabel>
          </Step>
        </Stepper>

        <form onSubmit={(e) => { e.preventDefault(); handleSubmit(); }}>
          <Box sx={{ mb: 4 }}>
            {test.fields.map(renderField)}
          </Box>

          <Box sx={{ display: 'flex', gap: 2, justifyContent: 'center' }}>
            <Button
              variant="outlined"
              size="large"
              onClick={() => navigate('/')}
              disabled={loading}
            >
              İptal
            </Button>
            <Button
              type="submit"
              variant="contained"
              size="large"
              disabled={loading}
              startIcon={loading ? <CircularProgress size={20} /> : null}
            >
              {loading ? 'Analiz Ediliyor...' : 'Tahminle'}
            </Button>
          </Box>
        </form>
      </Paper>
    </Container>
  );
};

export default TestPage; 