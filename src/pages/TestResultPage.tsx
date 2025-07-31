import React, { useState, useEffect, useCallback } from 'react';
import {
  Container,
  Typography,
  Card,
  CardContent,
  Box,
  Paper,
  Chip,
  Button,
  Alert,
  List,
  ListItem,
  ListItemIcon,
  ListItemText,
  Divider,
  Stepper,
  Step,
  StepLabel,
  Avatar,
  TextField,
  CircularProgress
} from '@mui/material';
import {
  CheckCircle,
  Warning,
  Error,
  FileDownload,
  Visibility,
  ArrowBack,
  Assessment,
  Send,
  AutoAwesome
} from '@mui/icons-material';
import { useNavigate, useParams } from 'react-router-dom';
import { healthTests } from '../utils/mockData';
import { TestResult } from '../types';
import { analyzeWithAI } from '../utils/ai';

interface ChatMessage {
  id: string;
  type: 'user' | 'ai';
  content: string;
  timestamp: Date;
}

const TestResultPage: React.FC = () => {
  const navigate = useNavigate();
  const { id } = useParams<{ id: string }>();
  const [testResult, setTestResult] = useState<TestResult | null>(null);
  const [loading, setLoading] = useState(true);
  const [showPDF, setShowPDF] = useState(false);
  const [chatMessages, setChatMessages] = useState<ChatMessage[]>([]);
  const [chatInput, setChatInput] = useState('');
  const [isAIResponding, setIsAIResponding] = useState(false);
  const [aiInitialized, setAiInitialized] = useState(false);

  // AI'ya test sonuçlarını tanıt
  const initializeAI = useCallback(async (testResult: TestResult) => {
    if (aiInitialized) return;
    
    try {
      setIsAIResponding(true);
      
      const initialPrompt = "Test sonuçlarımı incele ve değerlendir. Sonrasında sorularımı bu verilere göre yanıtla.";
      const aiResponse = await analyzeWithAI(initialPrompt, testResult, 'initial_analysis');
      
      const welcomeMessage: ChatMessage = {
        id: 'ai-init',
        type: 'ai',
        content: `Merhaba! Test sonuçlarınızı inceledim ve hafızama aldım. Size bu veriler ışığında yardımcı olabilirim. ${aiResponse.response}`,
        timestamp: new Date()
      };
      
      setChatMessages([welcomeMessage]);
      setAiInitialized(true);
    } catch (error) {
      console.error('AI başlatma hatası:', error);
      const errorMessage: ChatMessage = {
        id: 'ai-error',
        type: 'ai',
        content: 'Test sonuçlarınız analiz edildi. Sorularınızı sorabilirsiniz.',
        timestamp: new Date()
      };
      setChatMessages([errorMessage]);
    } finally {
      setIsAIResponding(false);
    }
  }, [aiInitialized]);

  useEffect(() => {
    const loadTestResult = (resultId: string) => {
      try {
        // Yeni sistem - testResults array'inde ara
        const savedResults = JSON.parse(localStorage.getItem('testResults') || '[]');
        const result = savedResults.find((r: TestResult) => r.id === resultId);
        
        if (result) {
          // LocalStorage'dan gelen veriyi doğru formata dönüştür
          const formattedResult: TestResult = {
            ...result,
            patientId: result.patientId || 'patient-1',
            formData: result.data || result.formData || {},
            createdAt: new Date(result.createdAt)
          };
          setTestResult(formattedResult);
          
          // AI'ya test sonuçlarını tanıt
          setTimeout(() => initializeAI(formattedResult), 1000);
        } else {
          // Eski sistem de kontrol et
          const oldResult = localStorage.getItem(`testResult_${resultId}`);
          if (oldResult) {
            const parsedResult = JSON.parse(oldResult);
            setTestResult(parsedResult);
            setTimeout(() => initializeAI(parsedResult), 1000);
          } else {
            // Test sonucu bulunamazsa dashboard'a yönlendir
            console.log('Test sonucu bulunamadı, dashboard\'a yönlendiriliyor...');
            navigate('/dashboard');
          }
        }
      } catch (error) {
        console.error('Test sonucu yüklenirken hata:', error);
        navigate('/dashboard');
      }
      setLoading(false);
    };

    const userData = localStorage.getItem('user');
    if (!userData) {
      navigate('/login');
      return;
    }

    if (id) {
      // id parametresini kullan
      loadTestResult(id);
    } else {
      console.log('Test ID bulunamadı');
      navigate('/dashboard');
    }
  }, [id, navigate, initializeAI]);

  const getRiskColor = (risk: string) => {
    switch (risk) {
      case 'low': return 'success';
      case 'medium': return 'warning';
      case 'high': return 'error';
      default: return 'default';
    }
  };

  const getRiskText = (risk: string) => {
    switch (risk) {
      case 'low': return 'Düşük';
      case 'medium': return 'Orta';
      case 'high': return 'Yüksek';
      default: return 'Bilinmiyor';
    }
  };

  const getRiskIcon = (risk: string) => {
    switch (risk) {
      case 'low': return <CheckCircle color="success" />;
      case 'medium': return <Warning color="warning" />;
      case 'high': return <Error color="error" />;
      default: return <Assessment />;
    }
  };

  const handleSendMessage = async () => {
    if (!chatInput.trim() || !testResult) return;

    const userMessage: ChatMessage = {
      id: Date.now().toString(),
      type: 'user',
      content: chatInput.trim(),
      timestamp: new Date()
    };

    setChatMessages(prev => [...prev, userMessage]);
    setChatInput('');
    setIsAIResponding(true);

    try {
      const aiResponse = await analyzeWithAI(chatInput.trim(), testResult);
      
      const aiMessage: ChatMessage = {
        id: (Date.now() + 1).toString(),
        type: 'ai',
        content: aiResponse.response,
        timestamp: new Date()
      };

      setChatMessages(prev => [...prev, aiMessage]);
    } catch (error) {
      console.error('AI cevap hatası:', error);
      const errorMessage: ChatMessage = {
        id: (Date.now() + 1).toString(),
        type: 'ai',
        content: 'Üzgünüm, şu anda bir teknik sorun yaşıyorum. Lütfen daha sonra tekrar deneyin.',
        timestamp: new Date()
      };
      setChatMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsAIResponding(false);
    }
  };

  const downloadPDF = () => {
    const pdfContent = generateReportContent();
    
    const printWindow = window.open('', '_blank');
    if (printWindow) {
      printWindow.document.write(`
        <html>
          <head>
            <title>Test Raporu - ${testResult?.testId || 'Test'}</title>
            <style>
              body { 
                font-family: 'Inter', 'Manrope', Arial, sans-serif; 
                margin: 40px; 
                line-height: 1.6; 
                color: #0F3978;
                background: #fff;
              }
              .header { 
                text-align: center; 
                margin-bottom: 40px; 
                border-bottom: 3px solid #1B69DE; 
                padding-bottom: 30px; 
              }
              .header h1 {
                font-family: 'Manrope', Arial, sans-serif;
                font-weight: 600;
                font-size: 28px;
                color: #0F3978;
                margin-bottom: 10px;
              }
              .header h2 {
                font-family: 'Inter', Arial, sans-serif;
                font-weight: 500;
                color: #4787E6;
                font-size: 18px;
              }
              .section { 
                margin-bottom: 30px; 
                background: #F8FBFF;
                padding: 25px;
                border-radius: 12px;
                border: 1px solid #E0E7EF;
              }
              .section h3 { 
                font-family: 'Manrope', Arial, sans-serif;
                font-weight: 600;
                color: #0F3978; 
                border-bottom: 2px solid #0ED1B1; 
                padding-bottom: 10px;
                font-size: 20px;
                margin-bottom: 20px;
              }
              .chat-message { 
                margin: 15px 0; 
                padding: 15px; 
                border-radius: 12px; 
                font-family: 'Inter', Arial, sans-serif;
              }
              .user-message { 
                background: linear-gradient(90deg, #0ED1B1 0%, #1B69DE 100%);
                color: white;
                text-align: right; 
              }
              .ai-message { 
                background: #F0F6FF;
                border: 1px solid #E0E7EF;
                color: #0F3978;
              }
              .message-time { 
                font-size: 12px; 
                color: #4787E6; 
                margin-top: 8px; 
                opacity: 0.8;
              }
              .risk-high { color: #d32f2f; font-weight: 600; }
              .risk-medium { color: #f57c00; font-weight: 600; }
              .risk-low { color: #388e3c; font-weight: 600; }
              ul { padding-left: 25px; }
              li { 
                margin-bottom: 8px; 
                font-family: 'Inter', Arial, sans-serif;
                line-height: 1.5;
              }
              .logo-area {
                text-align: center;
                margin-bottom: 20px;
                color: #0ED1B1;
                font-family: 'Manrope', Arial, sans-serif;
                font-weight: 700;
                font-size: 24px;
              }
            </style>
          </head>
          <body>
            <div class="logo-area">MediRisk</div>
            ${pdfContent}
          </body>
        </html>
      `);
      printWindow.document.close();
      printWindow.print();
    }
  };

  const downloadWord = () => {
    const wordContent = generateReportContent();
    
    const htmlContent = `
      <html>
        <head>
          <meta charset="utf-8">
          <title>Test Raporu - ${testResult?.testId || 'Test'}</title>
          <style>
            body { 
              font-family: 'Inter', 'Manrope', Arial, sans-serif; 
              margin: 40px; 
              line-height: 1.6; 
              color: #0F3978;
              background: #fff;
            }
            .header { 
              text-align: center; 
              margin-bottom: 40px; 
              border-bottom: 3px solid #1B69DE; 
              padding-bottom: 30px; 
            }
            .header h1 {
              font-family: 'Manrope', Arial, sans-serif;
              font-weight: 600;
              font-size: 28px;
              color: #0F3978;
              margin-bottom: 10px;
            }
            .header h2 {
              font-family: 'Inter', Arial, sans-serif;
              font-weight: 500;
              color: #4787E6;
              font-size: 18px;
            }
            .section { 
              margin-bottom: 30px; 
              background: #F8FBFF;
              padding: 25px;
              border-radius: 12px;
              border: 1px solid #E0E7EF;
            }
            .section h3 { 
              font-family: 'Manrope', Arial, sans-serif;
              font-weight: 600;
              color: #0F3978; 
              border-bottom: 2px solid #0ED1B1; 
              padding-bottom: 10px;
              font-size: 20px;
              margin-bottom: 20px;
            }
            .chat-message { 
              margin: 15px 0; 
              padding: 15px; 
              border-radius: 12px; 
              font-family: 'Inter', Arial, sans-serif;
            }
            .user-message { 
              background: linear-gradient(90deg, #0ED1B1 0%, #1B69DE 100%);
              color: white;
              text-align: right; 
            }
            .ai-message { 
              background: #F0F6FF;
              border: 1px solid #E0E7EF;
              color: #0F3978;
            }
            .message-time { 
              font-size: 12px; 
              color: #4787E6; 
              margin-top: 8px; 
              opacity: 0.8;
            }
            .risk-high { color: #d32f2f; font-weight: 600; }
            .risk-medium { color: #f57c00; font-weight: 600; }
            .risk-low { color: #388e3c; font-weight: 600; }
            ul { padding-left: 25px; }
            li { 
              margin-bottom: 8px; 
              font-family: 'Inter', Arial, sans-serif;
              line-height: 1.5;
            }
            .logo-area {
              text-align: center;
              margin-bottom: 20px;
              color: #0ED1B1;
              font-family: 'Manrope', Arial, sans-serif;
              font-weight: 700;
              font-size: 24px;
            }
          </style>
        </head>
        <body>
          <div class="logo-area">MediRisk</div>
          ${wordContent}
        </body>
      </html>
    `;

    const blob = new Blob([htmlContent], { type: 'application/vnd.ms-word' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `Test-Raporu-${testResult?.testId || 'Test'}.doc`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  };

  const generateReportContent = () => {
    if (!testResult) return '';

    const riskClass = `risk-${testResult.risk}`;
    
    return `
      <div class="header">
        <h1>Tıbbi Test Raporu</h1>
        <h2>${testResult.testId}</h2>
        <p><strong>Test Tarihi:</strong> ${testResult.createdAt instanceof Date 
          ? testResult.createdAt.toLocaleDateString('tr-TR')
          : new Date(testResult.createdAt).toLocaleDateString('tr-TR')
        }</p>
      </div>

      <div class="section">
        <h3>Test Sonuçları Özeti</h3>
        <p><strong>Risk Seviyesi:</strong> <span class="${riskClass}">${getRiskText(testResult.risk)}</span></p>
        <p><strong>Risk Skoru:</strong> ${testResult.score}/100</p>
      </div>

      <div class="section">
        <h3>Doktor Değerlendirmesi</h3>
        <p>${testResult.message}</p>
      </div>

      <div class="section">
        <h3>Öneriler</h3>
        <ul>
          ${testResult.recommendations.map(rec => `<li>${rec}</li>`).join('')}
        </ul>
      </div>

      ${chatMessages.length > 0 ? `
        <div class="section">
          <h3>AI Tıbbi Danışman Sohbeti</h3>
          ${chatMessages.map(message => `
            <div class="chat-message ${message.type}-message">
              <strong>${message.type === 'user' ? 'Hasta' : 'AI Doktor'}:</strong>
              <p>${message.content}</p>
              <div class="message-time">${message.timestamp.toLocaleString('tr-TR')}</div>
            </div>
          `).join('')}
        </div>
      ` : ''}

      <div class="section">
        <h3>Önemli Notlar</h3>
        <p><em>Bu rapor yalnızca bilgilendirme amaçlıdır. Kesin tanı ve tedavi için bir sağlık profesyoneline danışınız.</em></p>
        <p><small>Rapor Oluşturma Tarihi: ${new Date().toLocaleString('tr-TR')}</small></p>
      </div>
    `;
  };

  if (loading) {
    return (
      <Container maxWidth="lg" sx={{ py: 8, textAlign: 'center' }}>
        <Typography variant="h5">Yükleniyor...</Typography>
      </Container>
    );
  }

  if (!testResult) {
    return (
      <Container maxWidth="lg" sx={{ py: 8, textAlign: 'center' }}>
        <Typography variant="h5" color="error">Test sonucu bulunamadı</Typography>
        <Button onClick={() => navigate('/dashboard')} sx={{ mt: 2 }}>
          Dashboard'a Dön
        </Button>
      </Container>
    );
  }

  const test = healthTests.find(t => t.id === (testResult?.testId || id));

  return (
    <Container maxWidth="lg" sx={{ py: 4, backgroundColor: '#FFFFFF', minHeight: '100vh', fontFamily: 'Inter, Arial, sans-serif' }}>
      {/* Başlık */}
      <Box sx={{ mb: 4 }}>
        <Button
          startIcon={<ArrowBack />}
          onClick={() => navigate('/dashboard')}
          sx={{
            mb: 2,
            color: '#0F3978',
            fontWeight: 600,
            fontFamily: 'Manrope, Arial, sans-serif',
            borderRadius: 2,
            background: '#F8FBFF',
            border: '1.5px solid #E0E7EF',
            boxShadow: '0 2px 8px 0 rgba(30, 89, 174, 0.08)',
            '&:hover': {
              background: '#E0E7EF',
            }
          }}
        >
          Dashboard'a Dön
        </Button>
        <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
          {test?.icon && (
            <img
              src={test.icon}
              alt={test.name}
              style={{
                width: 48,
                height: 48,
                objectFit: 'contain',
                marginRight: 16,
                background: 'transparent',
                userSelect: 'none'
              }}
              draggable={false}
            />
          )}
          <Box>
            <Typography variant="h4" component="h1" sx={{
              fontWeight: 700,
              fontFamily: 'Manrope, Arial, sans-serif',
              color: '#0F3978',
              letterSpacing: '-0.5px'
            }}>
              {test?.name} - Sonuçlar
            </Typography>
            <Typography variant="h6" sx={{
              color: '#4787E6',
              fontFamily: 'Inter, Arial, sans-serif'
            }}>
              Test tamamlandı • {new Date(testResult.createdAt).toLocaleDateString('tr-TR')}
            </Typography>
          </Box>
        </Box>
      </Box>

      <Box sx={{ display: 'flex', flexDirection: { xs: 'column', lg: 'row' }, gap: 4 }}>
        {/* Sol Taraf - Ana Sonuçlar */}
        <Box sx={{ flex: { lg: 2 } }}>
          {/* Risk Değerlendirmesi */}
          <Card elevation={3} sx={{
            mb: 4,
            background: '#F8FBFF',
            border: '1.5px solid #E0E7EF',
            boxShadow: '0 4px 24px 0 rgba(30, 89, 174, 0.10)',
            borderRadius: 4,
          }}>
            <CardContent>
              <Box sx={{ display: 'flex', alignItems: 'center', mb: 3 }}>
                <Avatar sx={{
                  bgcolor: `${getRiskColor(testResult.risk)}.main`,
                  mr: 2,
                  width: 56,
                  height: 56,
                  fontSize: 36
                }}>
                  {getRiskIcon(testResult.risk)}
                </Avatar>
                <Box>
                  <Typography variant="h5" sx={{
                    fontWeight: 700,
                    fontFamily: 'Manrope, Arial, sans-serif',
                    color: '#0F3978'
                  }}>
                    Risk Değerlendirmesi
                  </Typography>
                  <Chip
                    label={getRiskText(testResult.risk)}
                    color={getRiskColor(testResult.risk) as any}
                    size="medium"
                    sx={{
                      fontSize: '1rem',
                      fontWeight: 600,
                      fontFamily: 'Inter, Arial, sans-serif',
                      borderRadius: 2
                    }}
                  />
                </Box>
              </Box>

              <Alert severity={getRiskColor(testResult.risk) as any} sx={{
                mb: 3,
                fontFamily: 'Inter, Arial, sans-serif',
                borderRadius: 2
              }}>
                <Typography variant="h6" sx={{
                  fontWeight: 600,
                  fontFamily: 'Manrope, Arial, sans-serif'
                }}>
                  {testResult.message}
                </Typography>
              </Alert>

              <Box sx={{ textAlign: 'center', mb: 3 }}>
                <Typography variant="h3" sx={{
                  fontWeight: 700,
                  color: '#1B69DE',
                  fontFamily: 'Manrope, Arial, sans-serif'
                }}>
                  {testResult.score}/100
                </Typography>
                <Typography variant="body1" sx={{
                  color: '#4787E6',
                  fontFamily: 'Inter, Arial, sans-serif'
                }}>
                  Risk Skoru
                </Typography>
                {testResult.confidence && (
                  <Box sx={{ mt: 2 }}>
                    <Typography variant="h6" sx={{
                      fontWeight: 600,
                      color: '#2CB67D',
                      fontFamily: 'Manrope, Arial, sans-serif'
                    }}>
                      {(testResult.confidence * 100).toFixed(1)}%
                    </Typography>
                    <Typography variant="body2" sx={{
                      color: '#4787E6',
                      fontFamily: 'Inter, Arial, sans-serif'
                    }}>
                      Model Güven Skoru
                    </Typography>
                  </Box>
                )}
              </Box>

              <Divider sx={{ my: 3 }} />

              <Typography variant="h6" gutterBottom sx={{
                fontWeight: 600,
                fontFamily: 'Manrope, Arial, sans-serif',
                color: '#0F3978'
              }}>
                Öneriler
              </Typography>
              <List>
                {testResult.recommendations.map((recommendation, index) => (
                  <ListItem key={index} sx={{ px: 0 }}>
                    <ListItemIcon>
                      <CheckCircle color="primary" />
                    </ListItemIcon>
                    <ListItemText
                      primary={recommendation}
                      primaryTypographyProps={{
                        variant: 'body1',
                        sx: { fontFamily: 'Inter, Arial, sans-serif' }
                      }}
                    />
                  </ListItem>
                ))}
              </List>
            </CardContent>
          </Card>

          {/* Test Verileri */}
          <Card elevation={2} sx={{
            background: '#F8FBFF',
            border: '1.5px solid #E0E7EF',
            boxShadow: '0 2px 12px 0 rgba(30, 89, 174, 0.07)',
            borderRadius: 4,
          }}>
            <CardContent>
              <Typography variant="h6" gutterBottom sx={{
                fontWeight: 600,
                mb: 3,
                fontFamily: 'Manrope, Arial, sans-serif',
                color: '#0F3978'
              }}>
                Test Verileri
              </Typography>
              <Box sx={{
                display: 'grid',
                gridTemplateColumns: { xs: '1fr', sm: 'repeat(2, 1fr)', md: 'repeat(3, 1fr)' },
                gap: 2
              }}>
                {Object.entries(testResult.formData).map(([key, value]) => {
                  const field = test?.fields.find(f => f.name === key);
                  return (
                    <Paper key={key} variant="outlined" sx={{
                      p: 2,
                      background: '#fff',
                      border: '1.5px solid #E0E7EF',
                      borderRadius: 2,
                      boxShadow: '0 1px 4px 0 rgba(30, 89, 174, 0.04)'
                    }}>
                      <Typography variant="body2" sx={{
                        color: '#4787E6',
                        fontFamily: 'Inter, Arial, sans-serif'
                      }} gutterBottom>
                        {field?.label || key}
                      </Typography>
                      <Typography variant="body1" sx={{
                        fontWeight: 600,
                        fontFamily: 'Manrope, Arial, sans-serif',
                        color: '#0F3978'
                      }}>
                        {typeof value === 'boolean' ? (value ? 'Evet' : 'Hayır') : value}
                      </Typography>
                    </Paper>
                  );
                })}
              </Box>
            </CardContent>
          </Card>

          {/* AI Tıbbi Danışman */}
          <Card elevation={3} sx={{
            mt: 3,
            background: '#F8FBFF',
            border: '1.5px solid #E0E7EF',
            boxShadow: '0 4px 24px 0 rgba(30, 89, 174, 0.10)',
            borderRadius: 4,
          }}>
            <CardContent>
              <Box sx={{ display: 'flex', alignItems: 'center', mb: 3 }}>
                <AutoAwesome sx={{ fontSize: 32, color: 'primary.main', mr: 2 }} />
                <Typography variant="h6" sx={{ 
                  fontWeight: 600,
                  fontFamily: 'Manrope, Arial, sans-serif',
                  color: '#0F3978'
                }}>
                  AI Tıbbi Danışman
                </Typography>
              </Box>

              {/* Chat Mesajları */}
              <Box
                sx={{
                  minHeight: 300,
                  maxHeight: 500,
                  overflowY: 'auto',
                  mb: 3,
                  border: '1px solid',
                  borderColor: 'divider',
                  borderRadius: 2,
                  p: 3,
                  backgroundColor: 'grey.50'
                }}
              >
                {chatMessages.length === 0 ? (
                  <Box sx={{ textAlign: 'center', py: 6 }}>
                    <AutoAwesome sx={{ fontSize: 48, color: 'primary.main', mb: 2 }} />
                    <Typography variant="h6" gutterBottom>
                      AI Tıbbi Danışmanınız Test Sonuçlarınızı İnceliyor...
                    </Typography>
                    <Typography variant="body2" color="text.secondary">
                      {isAIResponding ? 'Test verileriniz analiz ediliyor...' : 'Test sonuçlarınız hazır. Sorularınızı sorabilirsiniz.'}
                    </Typography>
                  </Box>
                ) : (
                  chatMessages.map((message) => (
                    <Box
                      key={message.id}
                      sx={{
                        display: 'flex',
                        justifyContent: message.type === 'user' ? 'flex-end' : 'flex-start',
                        mb: 3
                      }}
                    >
                      <Paper
                        elevation={2}
                        sx={{
                          p: 3,
                          maxWidth: '80%',
                          backgroundColor: message.type === 'user' ? 'primary.main' : 'white',
                          color: message.type === 'user' ? 'white' : 'text.primary',
                          borderRadius: 3
                        }}
                      >
                        <Typography variant="body1" sx={{ lineHeight: 1.6 }}>
                          {message.content}
                        </Typography>
                        <Typography
                          variant="caption"
                          sx={{
                            display: 'block',
                            mt: 1,
                            opacity: 0.7
                          }}
                        >
                          {message.timestamp.toLocaleTimeString('tr-TR', {
                            hour: '2-digit',
                            minute: '2-digit'
                          })}
                        </Typography>
                      </Paper>
                    </Box>
                  ))
                )}

                {isAIResponding && (
                  <Box sx={{ display: 'flex', justifyContent: 'flex-start', mb: 3 }}>
                    <Paper
                      elevation={2}
                      sx={{
                        p: 3,
                        backgroundColor: 'white',
                        borderRadius: 3
                      }}
                    >
                      <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                        <CircularProgress size={16} />
                        <Typography variant="body1" color="text.secondary">
                          AI cevap yazıyor...
                        </Typography>
                      </Box>
                    </Paper>
                  </Box>
                )}
              </Box>

              {/* Chat Input */}
              <Box sx={{ display: 'flex', gap: 2 }}>
                <TextField
                  fullWidth
                  variant="outlined"
                  placeholder="Örnek: 'Bu sonuçlara göre ne yapmalıyım?', 'Risk faktörlerim neler?', 'Kolesterol değerim normal mi?'"
                  value={chatInput}
                  onChange={(e) => setChatInput(e.target.value)}
                  onKeyPress={(e) => {
                    if (e.key === 'Enter' && !e.shiftKey) {
                      e.preventDefault();
                      handleSendMessage();
                    }
                  }}
                  multiline
                  maxRows={3}
                  sx={{ 
                    '& .MuiOutlinedInput-root': {
                      borderRadius: 3
                    }
                  }}
                />
                <Button
                  variant="contained"
                  onClick={handleSendMessage}
                  disabled={!chatInput.trim() || isAIResponding}
                  sx={{ 
                    minWidth: 60,
                    borderRadius: 3,
                    height: 'fit-content',
                    alignSelf: 'flex-end'
                  }}
                >
                  <Send />
                </Button>
              </Box>
            </CardContent>
          </Card>
        </Box>

        {/* Sağ Taraf - PDF ve İşlemler */}
        <Box sx={{ flex: { lg: 1 } }}>
          {/* PDF İşlemleri */}
          <Card elevation={3} sx={{
            mb: 4,
            background: '#F8FBFF',
            border: '1.5px solid #E0E7EF',
            boxShadow: '0 4px 24px 0 rgba(30, 89, 174, 0.10)',
            borderRadius: 4,
          }}>
            <CardContent>
              <Typography variant="h6" gutterBottom sx={{
                fontWeight: 600,
                mb: 3,
                fontFamily: 'Manrope, Arial, sans-serif',
                color: '#0F3978'
              }}>
                PDF Raporu
              </Typography>
              <Box sx={{ mb: 3 }}>
                <Typography variant="body2" sx={{
                  color: '#4787E6',
                  fontFamily: 'Inter, Arial, sans-serif',
                  mb: 2
                }}>
                  Test sonuçlarınızın detaylı PDF raporunu görüntüleyebilir veya indirebilirsiniz.
                </Typography>
              </Box>
              <Button
                fullWidth
                variant="contained"
                startIcon={<Visibility />}
                onClick={() => setShowPDF(true)}
                sx={{
                  mb: 2,
                  py: 1.5,
                  fontWeight: 600,
                  fontFamily: 'Manrope, Arial, sans-serif',
                  borderRadius: 2,
                  background: 'linear-gradient(90deg, #0ED1B1 0%, #1B69DE 100%)',
                  color: '#fff',
                  boxShadow: '0 2px 8px 0 rgba(14,209,177,0.08)',
                  '&:hover': {
                    background: 'linear-gradient(90deg, #1B69DE 0%, #0ED1B1 100%)',
                  }
                }}
              >
                PDF Görüntüle
              </Button>
              <Button
                fullWidth
                variant="outlined"
                startIcon={<FileDownload />}
                onClick={() => downloadPDF()}
                sx={{
                  py: 1.5,
                  fontWeight: 600,
                  fontFamily: 'Manrope, Arial, sans-serif',
                  borderRadius: 2,
                  color: '#0F3978',
                  borderColor: '#0ED1B1',
                  background: '#fff',
                  mb: 2,
                  '&:hover': {
                    borderColor: '#1B69DE',
                    background: '#F0F6FF'
                  }
                }}
              >
                PDF İndir
              </Button>
              <Button
                fullWidth
                variant="outlined"
                startIcon={<FileDownload />}
                onClick={() => downloadWord()}
                sx={{
                  py: 1.5,
                  fontWeight: 600,
                  fontFamily: 'Manrope, Arial, sans-serif',
                  borderRadius: 2,
                  color: '#0F3978',
                  borderColor: '#4787E6',
                  background: '#fff',
                  '&:hover': {
                    borderColor: '#1B69DE',
                    background: '#F0F6FF'
                  }
                }}
              >
                Word İndir
              </Button>
            </CardContent>
          </Card>

          {/* Test Süreci */}
          <Card elevation={2} sx={{
            background: '#F8FBFF',
            border: '1.5px solid #E0E7EF',
            boxShadow: '0 2px 12px 0 rgba(30, 89, 174, 0.07)',
            borderRadius: 4,
          }}>
            <CardContent>
              <Typography variant="h6" gutterBottom sx={{
                fontWeight: 600,
                mb: 3,
                fontFamily: 'Manrope, Arial, sans-serif',
                color: '#0F3978'
              }}>
                Test Süreci
              </Typography>
              <Stepper orientation="vertical">
                <Step active={true} completed={true}>
                  <StepLabel>
                    <Typography variant="body2" sx={{
                      fontWeight: 600,
                      fontFamily: 'Inter, Arial, sans-serif',
                      color: '#0F3978'
                    }}>
                      Test Seçildi
                    </Typography>
                    <Typography variant="body2" sx={{
                      color: '#4787E6',
                      fontFamily: 'Inter, Arial, sans-serif'
                    }}>
                      {test?.name}
                    </Typography>
                  </StepLabel>
                </Step>
                <Step active={true} completed={true}>
                  <StepLabel>
                    <Typography variant="body2" sx={{
                      fontWeight: 600,
                      fontFamily: 'Inter, Arial, sans-serif',
                      color: '#0F3978'
                    }}>
                      Veriler Girildi
                    </Typography>
                    <Typography variant="body2" sx={{
                      color: '#4787E6',
                      fontFamily: 'Inter, Arial, sans-serif'
                    }}>
                      {Object.keys(testResult.formData).length} alan
                    </Typography>
                  </StepLabel>
                </Step>
                <Step active={true} completed={true}>
                  <StepLabel>
                    <Typography variant="body2" sx={{
                      fontWeight: 600,
                      fontFamily: 'Inter, Arial, sans-serif',
                      color: '#0F3978'
                    }}>
                      Analiz Tamamlandı
                    </Typography>
                    <Typography variant="body2" sx={{
                      color: '#4787E6',
                      fontFamily: 'Inter, Arial, sans-serif'
                    }}>
                      Risk skoru: {testResult.score}/100
                    </Typography>
                  </StepLabel>
                </Step>
                <Step active={true} completed={true}>
                  <StepLabel>
                    <Typography variant="body2" sx={{
                      fontWeight: 600,
                      fontFamily: 'Inter, Arial, sans-serif',
                      color: '#0F3978'
                    }}>
                      Rapor Hazırlandı
                    </Typography>
                    <Typography variant="body2" sx={{
                      color: '#4787E6',
                      fontFamily: 'Inter, Arial, sans-serif'
                    }}>
                      PDF raporu oluşturuldu
                    </Typography>
                  </StepLabel>
                </Step>
              </Stepper>
            </CardContent>
          </Card>

          {/* Hızlı İşlemler */}
          <Card elevation={2} sx={{
            mt: 4,
            background: '#F8FBFF',
            border: '1.5px solid #E0E7EF',
            boxShadow: '0 2px 12px 0 rgba(30, 89, 174, 0.07)',
            borderRadius: 4,
          }}>
            <CardContent>
              <Typography variant="h6" gutterBottom sx={{
                fontWeight: 600,
                mb: 3,
                fontFamily: 'Manrope, Arial, sans-serif',
                color: '#0F3978'
              }}>
                Hızlı İşlemler
              </Typography>
              <Button
                fullWidth
                variant="contained"
                color="primary"
                startIcon={<FileDownload />}
                onClick={() => downloadPDF()}
                sx={{
                  mb: 2,
                  borderRadius: 2,
                  fontFamily: 'Manrope, Arial, sans-serif',
                  fontWeight: 600,
                  background: '#1B69DE',
                  '&:hover': {
                    background: '#0F3978'
                  }
                }}
              >
                PDF İndir
              </Button>
              <Button
                fullWidth
                variant="contained"
                startIcon={<FileDownload />}
                onClick={() => downloadWord()}
                sx={{
                  mb: 2,
                  borderRadius: 2,
                  fontFamily: 'Manrope, Arial, sans-serif',
                  fontWeight: 600,
                  background: '#4787E6',
                  '&:hover': {
                    background: '#0F3978'
                  }
                }}
              >
                Word İndir
              </Button>
              <Button
                fullWidth
                variant="contained"
                color="secondary"
                startIcon={<Visibility />}
                onClick={() => setShowPDF(true)}
                sx={{
                  borderRadius: 2,
                  fontFamily: 'Manrope, Arial, sans-serif',
                  fontWeight: 600,
                  background: '#ff6b35',
                  '&:hover': {
                    background: '#ff5722'
                  }
                }}
              >
                PDF Görüntüle
              </Button>
            </CardContent>
          </Card>
        </Box>
      </Box>

      {/* PDF Görüntüleme Dialog */}
      {showPDF && (
        <Box
          sx={{
            position: 'fixed',
            top: 0,
            left: 0,
            right: 0,
            bottom: 0,
            bgcolor: 'rgba(0,0,0,0.8)',
            zIndex: 1300,
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            p: 2
          }}
          onClick={() => setShowPDF(false)}
        >
          <Paper
            sx={{
              maxWidth: '90%',
              maxHeight: '90%',
              overflow: 'auto',
              p: 4,
              position: 'relative',
              background: '#fff',
              borderRadius: 4,
              fontFamily: 'Inter, Arial, sans-serif'
            }}
            onClick={(e) => e.stopPropagation()}
          >
            <Typography variant="h5" gutterBottom sx={{
              fontWeight: 600,
              fontFamily: 'Manrope, Arial, sans-serif',
              color: '#0F3978'
            }}>
              {test?.name} - PDF Raporu
            </Typography>
            <Box sx={{ my: 3 }}>
              <Typography variant="h6" gutterBottom sx={{
                fontWeight: 600,
                fontFamily: 'Manrope, Arial, sans-serif',
                color: '#0F3978'
              }}>
                Test Bilgileri
              </Typography>
              <Typography variant="body2" paragraph sx={{
                fontFamily: 'Inter, Arial, sans-serif'
              }}>
                <strong>Test Adı:</strong> {test?.name}
              </Typography>
              <Typography variant="body2" paragraph sx={{
                fontFamily: 'Inter, Arial, sans-serif'
              }}>
                <strong>Test Tarihi:</strong> {new Date(testResult.createdAt).toLocaleDateString('tr-TR')}
              </Typography>
              <Typography variant="body2" paragraph sx={{
                fontFamily: 'Inter, Arial, sans-serif'
              }}>
                <strong>Risk Seviyesi:</strong> {getRiskText(testResult.risk)}
              </Typography>
              <Typography variant="body2" paragraph sx={{
                fontFamily: 'Inter, Arial, sans-serif'
              }}>
                <strong>Risk Skoru:</strong> {testResult.score}/100
              </Typography>
            </Box>
            <Divider sx={{ my: 3 }} />
            <Typography variant="h6" gutterBottom sx={{
              fontWeight: 600,
              fontFamily: 'Manrope, Arial, sans-serif',
              color: '#0F3978'
            }}>
              Analiz Sonucu
            </Typography>
            <Typography variant="body1" paragraph sx={{
              fontFamily: 'Inter, Arial, sans-serif'
            }}>
              {testResult.message}
            </Typography>
            <Typography variant="h6" gutterBottom sx={{
              fontWeight: 600,
              fontFamily: 'Manrope, Arial, sans-serif',
              color: '#0F3978'
            }}>
              Öneriler
            </Typography>
            <List dense>
              {testResult.recommendations.map((rec, index) => (
                <ListItem key={index} sx={{ px: 0 }}>
                  <ListItemIcon>
                    <CheckCircle color="primary" fontSize="small" />
                  </ListItemIcon>
                  <ListItemText primary={rec} />
                </ListItem>
              ))}
            </List>
            
            {/* AI Tıbbi Danışman Sohbetleri */}
            {chatMessages.length > 0 && (
              <>
                <Divider sx={{ my: 3 }} />
                <Typography variant="h6" gutterBottom sx={{
                  fontWeight: 600,
                  fontFamily: 'Manrope, Arial, sans-serif',
                  color: '#0F3978'
                }}>
                  AI Tıbbi Danışman Sohbeti
                </Typography>
                <Box sx={{ maxHeight: 300, overflowY: 'auto', border: '1px solid #e0e0e0', borderRadius: 1, p: 2 }}>
                  {chatMessages.map((message) => (
                    <Box key={message.id} sx={{ mb: 2 }}>
                      <Typography variant="subtitle2" sx={{ fontWeight: 600, color: message.type === 'user' ? 'primary.main' : 'secondary.main' }}>
                        {message.type === 'user' ? 'Hasta:' : 'AI Doktor:'}
                      </Typography>
                      <Typography variant="body2" sx={{ ml: 1, mb: 1 }}>
                        {message.content}
                      </Typography>
                      <Typography variant="caption" color="text.secondary" sx={{ ml: 1 }}>
                        {message.timestamp.toLocaleString('tr-TR')}
                      </Typography>
                      {message.id !== chatMessages[chatMessages.length - 1].id && <Divider sx={{ mt: 1 }} />}
                    </Box>
                  ))}
                </Box>
              </>
            )}
            
            <Divider sx={{ my: 3 }} />
            <Typography variant="caption" color="text.secondary" sx={{ fontStyle: 'italic' }}>
              Bu rapor yalnızca bilgilendirme amaçlıdır. Kesin tanı ve tedavi için bir sağlık profesyoneline danışınız.
            </Typography>
            <Box sx={{ mt: 3, textAlign: 'center' }}>
              <Button
                variant="contained"
                onClick={() => setShowPDF(false)}
                sx={{
                  mr: 2,
                  borderRadius: 2,
                  background: 'linear-gradient(90deg, #0ED1B1 0%, #1B69DE 100%)',
                  color: '#fff',
                  fontFamily: 'Manrope, Arial, sans-serif',
                  fontWeight: 600,
                  '&:hover': {
                    background: 'linear-gradient(90deg, #1B69DE 0%, #0ED1B1 100%)',
                  }
                }}
              >
                Kapat
              </Button>
              <Button
                variant="outlined"
                startIcon={<FileDownload />}
                onClick={() => downloadPDF()}
                sx={{
                  mr: 2,
                  borderRadius: 2,
                  borderColor: '#0ED1B1',
                  color: '#0F3978',
                  background: '#fff',
                  fontFamily: 'Manrope, Arial, sans-serif',
                  fontWeight: 600,
                  '&:hover': {
                    borderColor: '#1B69DE',
                    background: '#F0F6FF'
                  }
                }}
              >
                PDF İndir
              </Button>
              <Button
                variant="outlined"
                startIcon={<FileDownload />}
                onClick={() => downloadWord()}
                sx={{
                  borderRadius: 2,
                  borderColor: '#4787E6',
                  color: '#0F3978',
                  background: '#fff',
                  fontFamily: 'Manrope, Arial, sans-serif',
                  fontWeight: 600,
                  '&:hover': {
                    borderColor: '#1B69DE',
                    background: '#F0F6FF'
                  }
                }}
              >
                Word İndir
              </Button>
            </Box>
          </Paper>
        </Box>
      )}
    </Container>
  );
};

export default TestResultPage;