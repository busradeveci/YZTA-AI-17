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
import { healthTests, predictTestResult } from '../utils/mockData';
import { TestResult } from '../types';
import { analyzeWithAI } from '../utils/ai';
import robotIcon from '../images/robot.png';

interface ChatMessage {
  id: string;
  type: 'user' | 'ai';
  content: string;
  timestamp: Date;
}

const TestResultPage: React.FC = () => {
  const navigate = useNavigate();
  const { testId } = useParams<{ testId: string }>();
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
    const userData = localStorage.getItem('user');
    if (!userData) {
      navigate('/login');
      return;
    }

    // Test sonucunu localStorage'dan al veya yeni oluştur
    const savedResult = localStorage.getItem(`testResult_${testId}`);
    if (savedResult) {
      const result = JSON.parse(savedResult);
      setTestResult(result);
      // AI'ya test sonuçlarını tanıt
      setTimeout(() => initializeAI(result), 1000);
    } else {
      // Mock test sonucu oluştur
      const test = healthTests.find(t => t.id === testId);
      if (test) {
        const mockFormData: Record<string, any> = {};
        test.fields.forEach(field => {
          if (field.type === 'number') {
            mockFormData[field.name] = Math.floor(Math.random() * 50) + 20;
          } else if (field.type === 'select') {
            mockFormData[field.name] = field.options?.[0] || '';
          } else if (field.type === 'checkbox') {
            mockFormData[field.name] = Math.random() > 0.5;
          }
        });

        const result = predictTestResult(testId!, mockFormData);
        const fullResult: TestResult = {
          id: Date.now().toString(),
          patientId: JSON.parse(userData).id,
          ...result,
          createdAt: new Date()
        };
        
        localStorage.setItem(`testResult_${testId}`, JSON.stringify(fullResult));
        setTestResult(fullResult);
        // AI'ya test sonuçlarını tanıt
        setTimeout(() => initializeAI(fullResult), 1000);
      }
    }
    setLoading(false);
  }, [testId, navigate, initializeAI]);

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
    // PDF içeriğini oluştur
    const pdfContent = generatePDFContent();
    
    // Basit bir şekilde window.print() kullanarak PDF oluştur
    const printWindow = window.open('', '_blank');
    if (printWindow) {
      printWindow.document.write(`
        <html>
          <head>
            <title>Test Raporu - ${testResult?.testId || 'Test'}</title>
            <style>
              body { font-family: Arial, sans-serif; margin: 20px; line-height: 1.6; }
              .header { text-align: center; margin-bottom: 30px; border-bottom: 2px solid #333; padding-bottom: 20px; }
              .section { margin-bottom: 25px; }
              .section h3 { color: #333; border-bottom: 1px solid #ccc; padding-bottom: 5px; }
              .chat-message { margin: 10px 0; padding: 10px; border-radius: 5px; }
              .user-message { background-color: #e3f2fd; text-align: right; }
              .ai-message { background-color: #f5f5f5; }
              .message-time { font-size: 12px; color: #666; margin-top: 5px; }
              .risk-high { color: #d32f2f; }
              .risk-medium { color: #f57c00; }
              .risk-low { color: #388e3c; }
              ul { padding-left: 20px; }
              li { margin-bottom: 5px; }
            </style>
          </head>
          <body>
            ${pdfContent}
          </body>
        </html>
      `);
      printWindow.document.close();
      printWindow.print();
    }
  };

  const generatePDFContent = () => {
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

  const test = healthTests.find(t => t.id === testResult.testId);

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

          {/* Raporu Geliştir Butonu */}
          {!showChat && (
            <Button
              variant="outlined"
              color="primary"
              fullWidth
              sx={{
                mt: 3,
                fontWeight: 600,
                fontFamily: 'Manrope, Arial, sans-serif',
                borderRadius: 2,
                borderColor: '#0ED1B1',
                color: '#0F3978',
                background: '#fff',
                '&:hover': {
                  borderColor: '#1B69DE',
                  background: '#F0F6FF'
                }
              }}
              onClick={() => setShowChat(true)}
            >
              Raporu Geliştir (Chat ile)
            </Button>
          )}
          {/* Chat Alanı */}
          {showChat && (
            <Box sx={{ mt: 3 }}>
              <form onSubmit={handleChatSubmit} style={{ display: 'flex', gap: 8 }}>
                <TextField
                  fullWidth
                  placeholder="Raporu geliştirmek için bir şey yazın..."
                  value={chatInput}
                  onChange={e => setChatInput(e.target.value)}
                  size="small"
                  sx={{
                    fontFamily: 'Inter, Arial, sans-serif',
                    background: '#fff',
                    borderRadius: 2
                  }}
                  InputProps={{
                    style: {
                      fontFamily: 'Inter, Arial, sans-serif',
                      fontSize: '12px',
                    },
                  }}
                />
                <Button
                  type="submit"
                  variant="contained"
                  color="primary"
                  disabled={!chatInput.trim()}
                  sx={{
                    minWidth: 48,
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
                  <Send />
                </Button>
              </form>
              {/* Chat geçmişi */}
              {chatHistory.length > 0 && (
                <Box sx={{ mt: 3 }}>
                  <Divider sx={{ mb: 2 }} />
                  <Typography variant="h6" sx={{
                    fontWeight: 600,
                    mb: 1,
                    fontFamily: 'Manrope, Arial, sans-serif',
                    color: '#0F3978'
                  }}>
                    Rapor Geliştirme Geçmişi
                  </Typography>
                  {chatHistory.map((msg, idx) => (
                    <Alert key={idx} severity={idx % 2 === 0 ? 'info' : 'success'} sx={{
                      mb: 1,
                      fontFamily: 'Inter, Arial, sans-serif',
                      borderRadius: 2
                    }}>
                      {msg}
                    </Alert>
                  ))}
                </Box>
              )}
            </Box>
          )}
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
                onClick={handleViewPDF}
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
                  '&:hover': {
                    borderColor: '#1B69DE',
                    background: '#F0F6FF'
                  }
                }}
              >
                PDF İndir
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
                İndir
              </Button>
            </Box>
          </Paper>
        </Box>
      )}
    </Container>
  );
};

export default TestResultPage;