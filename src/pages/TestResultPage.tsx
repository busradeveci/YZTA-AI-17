import React, { useState, useEffect } from 'react';
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
  TextField
} from '@mui/material';
import {
  CheckCircle,
  Warning,
  Error,
  Visibility,
  Download,
  ArrowBack,
  Assessment,
  Send
} from '@mui/icons-material';
import { useNavigate, useParams } from 'react-router-dom';
import { healthTests, predictTestResult } from '../utils/mockData';
import { TestResult } from '../types';

const TestResultPage: React.FC = () => {
  const navigate = useNavigate();
  const { testId } = useParams<{ testId: string }>();
  const [testResult, setTestResult] = useState<TestResult | null>(null);
  const [loading, setLoading] = useState(true);
  const [showPDF, setShowPDF] = useState(false);
  const [showChat, setShowChat] = useState(false);
  const [chatInput, setChatInput] = useState('');
  const [chatHistory, setChatHistory] = useState<string[]>([]);

  useEffect(() => {
    const userData = localStorage.getItem('user');
    if (!userData) {
      navigate('/login');
      return;
    }

    // Test sonucunu localStorage'dan al veya yeni oluştur
    const savedResult = localStorage.getItem(`testResult_${testId}`);
    if (savedResult) {
      setTestResult(JSON.parse(savedResult));
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
      }
    }
    setLoading(false);
  }, [testId, navigate]);

  const handleDownloadPDF = () => {
    // PDF indirme simülasyonu
    alert('PDF raporu indiriliyor...');
  };

  const handleViewPDF = () => {
    setShowPDF(true);
  };

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

  // Chatbot simülasyonu (gerçek API ile değiştirilebilir)
  const handleChatSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!chatInput.trim()) return;
    // Kullanıcı mesajını ekle
    setChatHistory(prev => [...prev, `🧑‍💻 ${chatInput}`]);
    // Bot yanıtı simülasyonu
    setTimeout(() => {
      setChatHistory(prev => [...prev, `🤖 Rapor güncellendi: ${chatInput} (örnek yanıt)`]);
    }, 1000);
    setChatInput('');
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
    <Container maxWidth="lg" sx={{ py: 4 }}>
      {/* Başlık */}
      <Box sx={{ mb: 4 }}>
        <Button
          startIcon={<ArrowBack />}
          onClick={() => navigate('/dashboard')}
          sx={{ mb: 2 }}
        >
          Dashboard'a Dön
        </Button>
        
        <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
          <Typography variant="h3" sx={{ mr: 2 }}>
            {test?.icon}
          </Typography>
          <Box>
            <Typography variant="h4" component="h1" sx={{ fontWeight: 700 }}>
              {test?.name} - Sonuçlar
            </Typography>
            <Typography variant="h6" color="text.secondary">
              Test tamamlandı • {new Date(testResult.createdAt).toLocaleDateString('tr-TR')}
            </Typography>
          </Box>
        </Box>
      </Box>

      <Box sx={{ display: 'flex', flexDirection: { xs: 'column', lg: 'row' }, gap: 4 }}>
        {/* Sol Taraf - Ana Sonuçlar */}
        <Box sx={{ flex: { lg: 2 } }}>
          {/* Risk Değerlendirmesi */}
          <Card elevation={3} sx={{ mb: 4 }}>
            <CardContent>
              <Box sx={{ display: 'flex', alignItems: 'center', mb: 3 }}>
                <Avatar sx={{ bgcolor: `${getRiskColor(testResult.risk)}.main`, mr: 2, width: 56, height: 56 }}>
                  {getRiskIcon(testResult.risk)}
                </Avatar>
                <Box>
                  <Typography variant="h5" sx={{ fontWeight: 700 }}>
                    Risk Değerlendirmesi
                  </Typography>
                  <Chip
                    label={getRiskText(testResult.risk)}
                    color={getRiskColor(testResult.risk) as any}
                    size="medium"
                    sx={{ fontSize: '1rem', fontWeight: 600 }}
                  />
                </Box>
              </Box>

              <Alert severity={getRiskColor(testResult.risk) as any} sx={{ mb: 3 }}>
                <Typography variant="h6" sx={{ fontWeight: 600 }}>
                  {testResult.message}
                </Typography>
              </Alert>

              <Box sx={{ textAlign: 'center', mb: 3 }}>
                <Typography variant="h3" sx={{ fontWeight: 700, color: 'primary.main' }}>
                  {testResult.score}/100
                </Typography>
                <Typography variant="body1" color="text.secondary">
                  Risk Skoru
                </Typography>
                
                {testResult.confidence && (
                  <Box sx={{ mt: 2 }}>
                    <Typography variant="h6" sx={{ fontWeight: 600, color: 'success.main' }}>
                      {(testResult.confidence * 100).toFixed(1)}%
                    </Typography>
                    <Typography variant="body2" color="text.secondary">
                      Model Güven Skoru
                    </Typography>
                  </Box>
                )}
              </Box>

              <Divider sx={{ my: 3 }} />

              <Typography variant="h6" gutterBottom sx={{ fontWeight: 600 }}>
                📋 Öneriler
              </Typography>
              <List>
                {testResult.recommendations.map((recommendation, index) => (
                  <ListItem key={index} sx={{ px: 0 }}>
                    <ListItemIcon>
                      <CheckCircle color="primary" />
                    </ListItemIcon>
                    <ListItemText
                      primary={recommendation}
                      primaryTypographyProps={{ variant: 'body1' }}
                    />
                  </ListItem>
                ))}
              </List>
            </CardContent>
          </Card>

          {/* Test Verileri */}
          <Card elevation={2}>
            <CardContent>
              <Typography variant="h6" gutterBottom sx={{ fontWeight: 600, mb: 3 }}>
                📊 Test Verileri
              </Typography>
              <Box sx={{ display: 'grid', gridTemplateColumns: { xs: '1fr', sm: 'repeat(2, 1fr)', md: 'repeat(3, 1fr)' }, gap: 2 }}>
                {Object.entries(testResult.formData).map(([key, value]) => {
                  const field = test?.fields.find(f => f.name === key);
                  return (
                    <Paper key={key} variant="outlined" sx={{ p: 2 }}>
                      <Typography variant="body2" color="text.secondary" gutterBottom>
                        {field?.label || key}
                      </Typography>
                      <Typography variant="body1" sx={{ fontWeight: 600 }}>
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
              sx={{ mt: 3, fontWeight: 600 }}
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
                />
                <Button
                  type="submit"
                  variant="contained"
                  color="primary"
                  disabled={!chatInput.trim()}
                  sx={{ minWidth: 48 }}
                >
                  <Send />
                </Button>
              </form>
            </Box>
          )}

          {/* Eklenen chat tabanlı metinler */}
          {chatHistory.length > 0 && (
            <Box sx={{ mt: 3 }}>
              <Divider sx={{ mb: 2 }} />
              <Typography variant="h6" sx={{ fontWeight: 600, mb: 1 }}>
                💬 Rapor Geliştirme Geçmişi
              </Typography>
              {chatHistory.map((msg, idx) => (
                <Alert key={idx} severity={msg.startsWith('🧑‍💻') ? 'info' : 'success'} sx={{ mb: 1 }}>
                  {msg}
                </Alert>
              ))}
            </Box>
          )}
        </Box>

        {/* Sağ Taraf - PDF ve İşlemler */}
        <Box sx={{ flex: { lg: 1 } }}>
          {/* PDF İşlemleri */}
          <Card elevation={3} sx={{ mb: 4 }}>
            <CardContent>
              <Typography variant="h6" gutterBottom sx={{ fontWeight: 600, mb: 3 }}>
                📄 PDF Raporu
              </Typography>
              
              <Box sx={{ mb: 3 }}>
                <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
                  Test sonuçlarınızın detaylı PDF raporunu görüntüleyebilir veya indirebilirsiniz.
                </Typography>
              </Box>

              <Button
                fullWidth
                variant="contained"
                startIcon={<Visibility />}
                onClick={handleViewPDF}
                sx={{ mb: 2, py: 1.5, fontWeight: 600 }}
              >
                PDF Görüntüle
              </Button>

              <Button
                fullWidth
                variant="outlined"
                startIcon={<Download />}
                onClick={handleDownloadPDF}
                sx={{ py: 1.5, fontWeight: 600 }}
              >
                PDF İndir
              </Button>
            </CardContent>
          </Card>

          {/* Test Süreci */}
          <Card elevation={2}>
            <CardContent>
              <Typography variant="h6" gutterBottom sx={{ fontWeight: 600, mb: 3 }}>
                🔄 Test Süreci
              </Typography>
              
              <Stepper orientation="vertical">
                <Step active={true} completed={true}>
                  <StepLabel>
                    <Typography variant="body2" sx={{ fontWeight: 600 }}>
                      Test Seçildi
                    </Typography>
                    <Typography variant="body2" color="text.secondary">
                      {test?.name}
                    </Typography>
                  </StepLabel>
                </Step>
                <Step active={true} completed={true}>
                  <StepLabel>
                    <Typography variant="body2" sx={{ fontWeight: 600 }}>
                      Veriler Girildi
                    </Typography>
                    <Typography variant="body2" color="text.secondary">
                      {Object.keys(testResult.formData).length} alan
                    </Typography>
                  </StepLabel>
                </Step>
                <Step active={true} completed={true}>
                  <StepLabel>
                    <Typography variant="body2" sx={{ fontWeight: 600 }}>
                      Analiz Tamamlandı
                    </Typography>
                    <Typography variant="body2" color="text.secondary">
                      Risk skoru: {testResult.score}/100
                    </Typography>
                  </StepLabel>
                </Step>
                <Step active={true} completed={true}>
                  <StepLabel>
                    <Typography variant="body2" sx={{ fontWeight: 600 }}>
                      Rapor Hazırlandı
                    </Typography>
                    <Typography variant="body2" color="text.secondary">
                      PDF raporu oluşturuldu
                    </Typography>
                  </StepLabel>
                </Step>
              </Stepper>
            </CardContent>
          </Card>

          {/* Hızlı İşlemler */}
          <Card elevation={2} sx={{ mt: 4 }}>
            <CardContent>
              <Typography variant="h6" gutterBottom sx={{ fontWeight: 600, mb: 3 }}>
                ⚡ Hızlı İşlemler
              </Typography>
              
              <Button
                fullWidth
                variant="outlined"
                onClick={() => navigate('/dashboard')}
                sx={{ mb: 2 }}
              >
                Yeni Test Başlat
              </Button>
              
              <Button
                fullWidth
                variant="outlined"
                onClick={() => navigate('/history')}
                sx={{ mb: 2 }}
              >
                Test Geçmişi
              </Button>
              
              <Button
                fullWidth
                variant="outlined"
                onClick={() => navigate('/about')}
              >
                Hakkında
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
              position: 'relative'
            }}
            onClick={(e) => e.stopPropagation()}
          >
            <Typography variant="h5" gutterBottom sx={{ fontWeight: 600 }}>
              📄 {test?.name} - PDF Raporu
            </Typography>
            
            <Box sx={{ my: 3 }}>
              <Typography variant="h6" gutterBottom>
                Test Bilgileri
              </Typography>
              <Typography variant="body2" paragraph>
                <strong>Test Adı:</strong> {test?.name}
              </Typography>
              <Typography variant="body2" paragraph>
                <strong>Test Tarihi:</strong> {new Date(testResult.createdAt).toLocaleDateString('tr-TR')}
              </Typography>
              <Typography variant="body2" paragraph>
                <strong>Risk Seviyesi:</strong> {getRiskText(testResult.risk)}
              </Typography>
              <Typography variant="body2" paragraph>
                <strong>Risk Skoru:</strong> {testResult.score}/100
              </Typography>
            </Box>

            <Divider sx={{ my: 3 }} />

            <Typography variant="h6" gutterBottom>
              Analiz Sonucu
            </Typography>
            <Typography variant="body1" paragraph>
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

            <Box sx={{ mt: 3, textAlign: 'center' }}>
              <Button
                variant="contained"
                onClick={() => setShowPDF(false)}
                sx={{ mr: 2 }}
              >
                Kapat
              </Button>
              <Button
                variant="outlined"
                startIcon={<Download />}
                onClick={handleDownloadPDF}
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