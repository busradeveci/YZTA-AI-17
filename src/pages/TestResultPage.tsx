import React, { useState, useEffect, useCallback } from 'react';
import { 
  Container, 
  Paper, 
  Typography, 
  Box, 
  Card, 
  CardContent, 
  Chip, 
  Button, 
  TextField,
  List,
  ListItem,
  ListItemIcon,
  ListItemText,
  Divider,
  Alert,
  CircularProgress
} from '@mui/material';
import { 
  CheckCircle, 
  Warning, 
  Error, 
  FileDownload, 
  Visibility,
  AutoAwesome,
  Send,
  TrendingUp,
  Assessment,
  HealthAndSafety
} from '@mui/icons-material';
import { useParams, useNavigate } from 'react-router-dom';
import { analyzeWithAI } from '../utils/ai';
import { TestResult } from '../types';

interface ChatMessage {
  id: string;
  type: 'user' | 'ai';
  content: string;
  timestamp: Date;
}

const TestResultPage: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
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
          navigate('/dashboard');
        }
      } catch (error) {
        console.error('Test sonucu yüklenirken hata:', error);
        navigate('/dashboard');
      }
      setLoading(false);
    };

    if (id) {
      loadTestResult(id);
    }
  }, [id, navigate, initializeAI]);

  const getRiskColor = (risk: string) => {
    switch (risk) {
      case 'low': return 'success';
      case 'medium': return 'warning';
      case 'high': return 'error';
      default: return 'info';
    }
  };

  const getRiskText = (risk: string) => {
    switch (risk) {
      case 'low': return 'Düşük Risk';
      case 'medium': return 'Orta Risk';
      case 'high': return 'Yüksek Risk';
      default: return 'Belirsiz';
    }
  };

  const getRiskIcon = (risk: string) => {
    switch (risk) {
      case 'low': return <CheckCircle />;
      case 'medium': return <Warning />;
      case 'high': return <Error />;
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
      <Container maxWidth="lg" sx={{ py: 4 }}>
        <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: 400 }}>
          <CircularProgress />
        </Box>
      </Container>
    );
  }

  if (!testResult) {
    return (
      <Container maxWidth="lg" sx={{ py: 4 }}>
        <Alert severity="error">Test sonucu bulunamadı.</Alert>
      </Container>
    );
  }

  return (
    <Container maxWidth="lg" sx={{ py: 4 }}>
      {/* Ana Test Sonucu Bölümü */}
      <Box sx={{ mb: 4 }}>
        <Paper elevation={3} sx={{ p: 4, borderRadius: 3 }}>
          {/* Başlık */}
          <Box sx={{ display: 'flex', alignItems: 'center', mb: 3 }}>
            <HealthAndSafety sx={{ fontSize: 40, color: 'primary.main', mr: 2 }} />
            <Box>
              <Typography variant="h4" sx={{ fontWeight: 700, mb: 1 }}>
                Test Sonucu Raporu
              </Typography>
              <Typography variant="body1" color="text.secondary">
                {testResult.testId} • {testResult.createdAt instanceof Date 
                  ? testResult.createdAt.toLocaleDateString('tr-TR')
                  : new Date(testResult.createdAt).toLocaleDateString('tr-TR')
                }
              </Typography>
            </Box>
          </Box>

          {/* Risk Kartları */}
          <Box sx={{ display: 'grid', gridTemplateColumns: { xs: '1fr', md: '1fr 1fr 1fr' }, gap: 3, mb: 4 }}>
            <Card sx={{ textAlign: 'center', p: 3 }}>
              <CardContent>
                <Box sx={{ display: 'flex', justifyContent: 'center', mb: 2 }}>
                  {getRiskIcon(testResult.risk)}
                </Box>
                <Typography variant="h6" gutterBottom>
                  Risk Durumu
                </Typography>
                <Chip
                  label={getRiskText(testResult.risk)}
                  color={getRiskColor(testResult.risk) as any}
                  sx={{ fontWeight: 600 }}
                />
              </CardContent>
            </Card>

            <Card sx={{ textAlign: 'center', p: 3 }}>
              <CardContent>
                <TrendingUp sx={{ fontSize: 32, color: 'primary.main', mb: 2 }} />
                <Typography variant="h6" gutterBottom>
                  Risk Skoru
                </Typography>
                <Typography variant="h4" sx={{ fontWeight: 700, color: 'primary.main' }}>
                  {testResult.score}
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  / 100
                </Typography>
              </CardContent>
            </Card>

            <Card sx={{ textAlign: 'center', p: 3 }}>
              <CardContent>
                <Assessment sx={{ fontSize: 32, color: 'primary.main', mb: 2 }} />
                <Typography variant="h6" gutterBottom>
                  Test Türü
                </Typography>
                <Typography variant="body1" sx={{ fontWeight: 600 }}>
                  {testResult.testId}
                </Typography>
              </CardContent>
            </Card>
          </Box>

          {/* Doktor Değerlendirmesi */}
          <Card sx={{ mb: 4 }}>
            <CardContent>
              <Typography variant="h6" gutterBottom sx={{ display: 'flex', alignItems: 'center' }}>
                <HealthAndSafety sx={{ mr: 1 }} />
                Doktor Değerlendirmesi
              </Typography>
              <Typography variant="body1" sx={{ lineHeight: 1.8 }}>
                {testResult.message}
              </Typography>
            </CardContent>
          </Card>

          {/* Öneriler */}
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom sx={{ display: 'flex', alignItems: 'center' }}>
                <CheckCircle sx={{ mr: 1, color: 'success.main' }} />
                Öneriler
              </Typography>
              <List>
                {testResult.recommendations.map((recommendation, index) => (
                  <ListItem key={index} sx={{ px: 0 }}>
                    <ListItemIcon>
                      <CheckCircle color="success" fontSize="small" />
                    </ListItemIcon>
                    <ListItemText primary={recommendation} />
                  </ListItem>
                ))}
              </List>
            </CardContent>
          </Card>

          {/* Hızlı İşlemler */}
          <Box sx={{ mt: 4 }}>
            <Typography variant="h6" gutterBottom sx={{ fontWeight: 600 }}>
              Hızlı İşlemler
            </Typography>
            <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 2 }}>
              <Button
                variant="contained"
                color="primary"
                startIcon={<FileDownload />}
                onClick={() => downloadPDF()}
              >
                PDF İndir
              </Button>
              <Button
                variant="contained"
                color="secondary"
                startIcon={<Visibility />}
                onClick={() => setShowPDF(true)}
                sx={{ backgroundColor: '#ff6b35', '&:hover': { backgroundColor: '#ff5722' } }}
              >
                PDF Görüntüle
              </Button>
            </Box>
          </Box>
        </Paper>
      </Box>

      {/* AI Tıbbi Danışman */}
      <Box sx={{ mb: 4 }}>
        <Paper elevation={3} sx={{ p: 4, borderRadius: 3 }}>
          <Box sx={{ display: 'flex', alignItems: 'center', mb: 3 }}>
            <AutoAwesome sx={{ fontSize: 32, color: 'primary.main', mr: 2 }} />
            <Typography variant="h5" sx={{ fontWeight: 600 }}>
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
        </Paper>
      </Box>

      {/* PDF Modal */}
      {showPDF && (
        <Box
          sx={{
            position: 'fixed',
            top: 0,
            left: 0,
            right: 0,
            bottom: 0,
            backgroundColor: 'rgba(0, 0, 0, 0.7)',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            zIndex: 1300,
            p: 2
          }}
          onClick={() => setShowPDF(false)}
        >
          <Paper
            sx={{
              width: '90%',
              maxWidth: 800,
              height: '90%',
              p: 3,
              display: 'flex',
              flexDirection: 'column',
              borderRadius: 3
            }}
            onClick={(e) => e.stopPropagation()}
          >
            <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
              <Typography variant="h6">Test Raporu</Typography>
              <Button onClick={() => setShowPDF(false)} variant="outlined">
                Kapat
              </Button>
            </Box>
            <Box sx={{ flex: 1, border: '1px solid #ccc', borderRadius: 2, p: 3, overflow: 'auto' }}>
              <Typography variant="h6" gutterBottom>
                {testResult.testId} Test Sonucu
              </Typography>
              <Typography variant="body2" paragraph>
                <strong>Test Tarihi:</strong> {testResult.createdAt instanceof Date 
                  ? testResult.createdAt.toLocaleDateString('tr-TR')
                  : new Date(testResult.createdAt).toLocaleDateString('tr-TR')
                }
              </Typography>
              <Typography variant="body2" paragraph>
                <strong>Risk Seviyesi:</strong> {getRiskText(testResult.risk)}
              </Typography>
              <Typography variant="body2" paragraph>
                <strong>Risk Skoru:</strong> {testResult.score}/100
              </Typography>
              <Divider sx={{ my: 2 }} />
              <Typography variant="h6" gutterBottom>
                Doktor Değerlendirmesi
              </Typography>
              <Typography variant="body2" paragraph>
                {testResult.message}
              </Typography>
              <Typography variant="h6" gutterBottom>
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
                  <Divider sx={{ my: 2 }} />
                  <Typography variant="h6" gutterBottom>
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
              
              <Divider sx={{ my: 2 }} />
              <Typography variant="caption" color="text.secondary" sx={{ fontStyle: 'italic' }}>
                Bu rapor yalnızca bilgilendirme amaçlıdır. Kesin tanı ve tedavi için bir sağlık profesyoneline danışınız.
              </Typography>
            </Box>
          </Paper>
        </Box>
      )}
    </Container>
  );
};

export default TestResultPage;
