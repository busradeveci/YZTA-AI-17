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
  CircularProgress,
  Card,
  Avatar,
  IconButton,
  List,
  ListItem,
  ListItemText,
  ListItemAvatar,
  Collapse
} from '@mui/material';
import { useParams, useNavigate } from 'react-router-dom';
import { healthTests, predictTestResult, mockChatMessages } from '../utils/mockData';
import { TestResult, ChatMessage } from '../types';
import { Send, SmartToy, Person, ExpandMore, ExpandLess } from '@mui/icons-material';
import robotIcon from '../images/robot.png'; // en üste ekleyin

const TestPage: React.FC = () => {
  const { testId } = useParams<{ testId: string }>();
  const navigate = useNavigate();
  const [formData, setFormData] = useState<Record<string, any>>({});
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<TestResult | null>(null);
  const [errors, setErrors] = useState<Record<string, string>>({});
  const [chatMessages, setChatMessages] = useState<ChatMessage[]>(mockChatMessages);
  const [chatInput, setChatInput] = useState('');
  const [isChatExpanded, setIsChatExpanded] = useState(false);

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
        if (field.validation?.min && num < field.validation.min) {
          newErrors[field.name] = `Minimum değer: ${field.validation.min}`;
        }
        if (field.validation?.max && num > field.validation.max) {
          newErrors[field.name] = `Maksimum değer: ${field.validation.max}`;
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
      // Mock API çağrısı simülasyonu
      await new Promise(resolve => setTimeout(resolve, 2000));
      
      const resultData = predictTestResult(testId!, formData);
      
      // Test sonucunu localStorage'a kaydet
      const fullResult: TestResult = {
        id: Date.now().toString(),
        testId: testId!,
        patientId: '1', // Mock hasta ID
        formData: { ...formData },
        risk: resultData.risk,
        score: resultData.score,
        message: resultData.message,
        recommendations: resultData.recommendations,
        createdAt: new Date()
      };
      localStorage.setItem(`testResult_${testId}`, JSON.stringify(fullResult));
      
      // Test sonuç sayfasına yönlendir
      navigate(`/test-result/${testId}`);
    } catch (error) {
      console.error('Test hatası:', error);
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
              min: field.validation?.min,
              max: field.validation?.max
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

  const handleChatSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!chatInput.trim()) return;

    // Kullanıcı mesajını ekle
    const userMessage: ChatMessage = {
      id: Date.now().toString(),
      type: 'user',
      content: chatInput,
      timestamp: new Date()
    };

    setChatMessages(prev => [...prev, userMessage]);

    // Chatbot yanıtını simüle et
    setTimeout(() => {
      const lowerInput = chatInput.toLowerCase();
      let response = 'Üzgünüm, bu konuda size yardımcı olamıyorum.';

      if (lowerInput.includes('test') || lowerInput.includes('nasıl')) {
        response = `Bu ${test?.name} testi hakkında bilgi verebilirim. Test ${test?.description}`;
      } else if (lowerInput.includes('süre') || lowerInput.includes('ne kadar')) {
        response = 'Test yaklaşık 5-10 dakika sürer. Tüm soruları dikkatlice cevaplamanız önemlidir.';
      } else if (lowerInput.includes('sonuç') || lowerInput.includes('rapor')) {
        response = 'Test tamamlandıktan sonra detaylı sonuç raporunuzu görebilir ve PDF olarak indirebilirsiniz.';
      } else if (lowerInput.includes('güvenli') || lowerInput.includes('güvenlik')) {
        response = 'Tüm verileriniz güvenle korunur. Test sonuçları sadece size özeldir.';
      } else if (lowerInput.includes('yardım') || lowerInput.includes('help')) {
        response = 'Size şu konularda yardımcı olabilirim:\n• Test hakkında bilgi\n• Test süresi\n• Sonuç raporları\n• Güvenlik';
      }

      const botMessage: ChatMessage = {
        id: (Date.now() + 1).toString(),
        type: 'bot',
        content: response,
        timestamp: new Date()
      };

      setChatMessages(prev => [...prev, botMessage]);
    }, 1000);

    setChatInput('');
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
    <Container
      maxWidth="lg"
      sx={{
        py: 4,
        backgroundColor: '#FFFFFF', // Arka plan beyaz (FFFFF)
        minHeight: '100vh',
        fontFamily: 'Inter, Arial, sans-serif'
      }}
    >
      <Box sx={{ display: 'flex', flexDirection: { xs: 'column', lg: 'row' }, gap: 4 }}>
        {/* Sol Taraf - Test Formu */}
        <Box sx={{ flex: { lg: 2 } }}>
          <Paper
            elevation={3}
            sx={{
              p: 4,
              background: '#F8FBFF',
              border: '1.5px solid #E0E7EF',
              boxShadow: '0 4px 24px 0 rgba(30, 89, 174, 0.10)',
              borderRadius: 4,
            }}
          >
            <Box sx={{ textAlign: 'center', mb: 4 }}>
              <Box sx={{ display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 1 }}>
                <img
                  src={test.icon}
                  alt={test.name}
                  style={{
                    width: 48,
                    height: 48,
                    objectFit: 'contain',
                    background: 'transparent',
                    marginBottom: 8,
                    userSelect: 'none'
                  }}
                  draggable={false}
                />
                <Typography
                  variant="h3"
                  gutterBottom
                  sx={{
                    fontWeight: 700,
                    fontFamily: 'Manrope, Arial, sans-serif',
                    color: '#0F3978',
                    letterSpacing: '-0.5px',
                    userSelect: 'none'
                  }}
                >
                  {test.name}
                </Typography>
              </Box>
              <Typography
                variant="body1"
                sx={{
                  color: '#4787E6',
                  fontFamily: 'Inter, Arial, sans-serif',
                  mb: 2,
                }}
              >
                {test.description}
              </Typography>
            </Box>

            <Stepper activeStep={0} sx={{ mb: 4 }}>
              <Step>
                <StepLabel
                  sx={{
                    '& .MuiStepLabel-label': {
                      fontFamily: 'Manrope, Arial, sans-serif',
                      color: '#0F3978',
                      fontWeight: 600,
                    }
                  }}
                >
                  Bilgileri Girin
                </StepLabel>
              </Step>
              <Step>
                <StepLabel
                  sx={{
                    '& .MuiStepLabel-label': {
                      fontFamily: 'Manrope, Arial, sans-serif',
                      color: '#0F3978',
                      fontWeight: 600,
                    }
                  }}
                >
                  Analiz
                </StepLabel>
              </Step>
              <Step>
                <StepLabel
                  sx={{
                    '& .MuiStepLabel-label': {
                      fontFamily: 'Manrope, Arial, sans-serif',
                      color: '#0F3978',
                      fontWeight: 600,
                    }
                  }}
                >
                  Sonuçlar
                </StepLabel>
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
                  onClick={() => navigate('/dashboard')}
                  disabled={loading}
                  sx={{
                    borderRadius: 2,
                    fontWeight: 600,
                    fontFamily: 'Manrope, Arial, sans-serif',
                    color: '#0F3978',
                    borderColor: '#0ED1B1',
                    '&:hover': {
                      borderColor: '#1B69DE',
                      background: '#F0F6FF'
                    }
                  }}
                >
                  İptal
                </Button>
                <Button
                  type="submit"
                  variant="contained"
                  size="large"
                  disabled={loading}
                  startIcon={loading ? <CircularProgress size={20} /> : null}
                  sx={{
                    borderRadius: 2,
                    fontWeight: 600,
                    fontFamily: 'Manrope, Arial, sans-serif',
                    background: 'linear-gradient(90deg, #0ED1B1 0%, #1B69DE 100%)',
                    color: '#fff',
                    boxShadow: '0 2px 8px 0 rgba(14,209,177,0.08)',
                    transition: 'background 0.2s, box-shadow 0.2s, transform 0.2s',
                    '&:hover': {
                      background: 'linear-gradient(90deg, #1B69DE 0%, #0ED1B1 100%)',
                      boxShadow: '0 4px 16px 0 rgba(27,105,222,0.12)',
                      transform: 'translateY(-2px) scale(1.03)'
                    }
                  }}
                >
                  {loading ? 'Analiz Ediliyor...' : 'Analizi Başlat'}
                </Button>
              </Box>
            </form>
          </Paper>
        </Box>

        {/* Sağ Taraf - Chatbot */}
        <Box sx={{ flex: { lg: 1 } }}>
          <Card
            elevation={3}
            sx={{
              height: 'fit-content',
              position: 'sticky',
              top: 20,
              borderRadius: 4,
              background: '#F8FBFF',
              border: '1.5px solid #E0E7EF',
              boxShadow: '0 4px 24px 0 rgba(30, 89, 174, 0.10)',
            }}
          >
            <Box sx={{ p: 2, borderBottom: 1, borderColor: 'divider' }}>
              <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
                <Box sx={{ display: 'flex', alignItems: 'center' }}>
                  <Box
                    sx={{
                      width: 32,
                      height: 32,
                      mr: 2,
                      display: 'flex',
                      alignItems: 'center',
                      justifyContent: 'center',
                    }}
                  >
                    <img
                      src={robotIcon}
                      alt="Asistan"
                      style={{
                        width: 32,
                        height: 32,
                        objectFit: 'contain',
                        background: 'transparent',
                        borderRadius: 0,
                        userSelect: 'none',
                        display: 'block',
                      }}
                      draggable={false}
                    />
                  </Box>
                  <Box>
                    <Typography variant="h6" sx={{
                      fontWeight: 600,
                      fontFamily: 'Manrope, Arial, sans-serif',
                      color: '#0F3978'
                    }}>
                      MediRisk Asistan
                    </Typography>
                    <Typography variant="body2" sx={{
                      color: '#4787E6',
                      fontFamily: 'Inter, Arial, sans-serif'
                    }}>
                      Test hakkında sorularınızı sorun
                    </Typography>
                  </Box>
                </Box>
                <IconButton
                  onClick={() => setIsChatExpanded(!isChatExpanded)}
                  size="small"
                  sx={{
                    color: '#0F3978'
                  }}
                >
                  {isChatExpanded ? <ExpandLess /> : <ExpandMore />}
                </IconButton>
              </Box>
            </Box>

            {/* Chat Mesajları */}
            <Collapse in={isChatExpanded}>
              <Box sx={{ height: 300, overflowY: 'auto', p: 2 }}>
                <List sx={{ p: 0 }}>
                  {chatMessages.map((message) => (
                    <ListItem key={message.id} sx={{ px: 0 }}>
                      <ListItemAvatar>
                        <Avatar
                          sx={{
                            bgcolor: message.type === 'user' ? '#0F3978' : '#E0E7EF',
                            color: message.type === 'user' ? '#fff' : '#0F3978',
                            fontFamily: 'Manrope, Arial, sans-serif'
                          }}
                        >
                          {message.type === 'user' ? (
                            <Person sx={{ fontSize: 22 }} />
                          ) : (
                            <img
                              src={robotIcon}
                              alt="Asistan"
                              style={{
                                width: 22,
                                height: 22,
                                objectFit: 'contain',
                                background: 'transparent',
                                borderRadius: 0,
                                userSelect: 'none',
                                display: 'block',
                              }}
                              draggable={false}
                            />
                          )}
                        </Avatar>
                      </ListItemAvatar>
                      <ListItemText
                        primary={
                          <Box sx={{
                            bgcolor: message.type === 'user' ? '#0F3978' : '#F8FBFF',
                            color: message.type === 'user' ? '#fff' : '#0F3978',
                            p: 1.5,
                            borderRadius: 2,
                            maxWidth: '80%',
                            fontFamily: 'Inter, Arial, sans-serif'
                          }}>
                            <Typography variant="body2" sx={{ fontFamily: 'Inter, Arial, sans-serif' }}>
                              {message.content}
                            </Typography>
                          </Box>
                        }
                      />
                    </ListItem>
                  ))}
                </List>
              </Box>

              {/* Chat Input */}
              <Box sx={{ p: 2, borderTop: 1, borderColor: 'divider' }}>
                <Box component="form" onSubmit={handleChatSubmit} sx={{ display: 'flex', gap: 1 }}>
                  <TextField
                    fullWidth
                    size="small"
                    placeholder="Test hakkında soru sorun..."
                    value={chatInput}
                    onChange={(e) => setChatInput(e.target.value)}
                    sx={{
                      '& .MuiOutlinedInput-root': { borderRadius: 3, background: '#fff' },
                      fontFamily: 'Inter, Arial, sans-serif'
                    }}
                    InputProps={{
                      style: {
                        fontFamily: 'Inter, Arial, sans-serif',
                        fontSize: '12px',
                      },
                    }}
                  />
                  <IconButton
                    type="submit"
                    color="primary"
                    disabled={!chatInput.trim()}
                    sx={{
                      background: 'linear-gradient(90deg, #0ED1B1 0%, #1B69DE 100%)',
                      color: '#fff',
                      borderRadius: 2,
                      '&:hover': {
                        background: 'linear-gradient(90deg, #1B69DE 0%, #0ED1B1 100%)',
                      }
                    }}
                  >
                    <Send />
                  </IconButton>
                </Box>
              </Box>
            </Collapse>
          </Card>
        </Box>
      </Box>
    </Container>
  );
};

export default TestPage;