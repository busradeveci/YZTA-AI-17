import React, { useState, useEffect } from 'react';
import {
  Container,
  Typography,
  Card,
  CardContent,
  CardActions,
  Button,
  Box,
  Paper,
  Chip,
  Avatar,
  TextField,
  IconButton,
  List,
  ListItem,
  ListItemText,
  ListItemAvatar,
  Collapse
} from '@mui/material';

import {
  PlayArrow,
  Person,
  Send,
  SmartToy,
  Visibility,
  Download,
  ExpandMore,
  ExpandLess
} from '@mui/icons-material';
import { useNavigate } from 'react-router-dom';
import { healthTests, mockDashboardStats, mockTestResults, mockChatMessages, chatbotResponses } from '../utils/mockData';
import { ChatMessage } from '../types';

const DashboardPage: React.FC = () => {
  const navigate = useNavigate();
  const [user, setUser] = useState<any>(null);
  const [chatMessages, setChatMessages] = useState<ChatMessage[]>(mockChatMessages);
  const [chatInput, setChatInput] = useState('');
  const [isChatExpanded, setIsChatExpanded] = useState(false);

  useEffect(() => {
    const userData = localStorage.getItem('user');
    if (userData) {
      setUser(JSON.parse(userData));
    } else {
      navigate('/login');
    }
  }, [navigate]);

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

      if (lowerInput.includes('yeni test') || lowerInput.includes('test ekle')) {
        response = chatbotResponses['yeni test'].message;
      } else if (lowerInput.includes('tansiyon')) {
        response = chatbotResponses['tansiyon'].message;
      } else if (lowerInput.includes('sonuç') || lowerInput.includes('rapor')) {
        response = chatbotResponses['sonuçlar'].message;
      } else if (lowerInput.includes('yardım') || lowerInput.includes('help')) {
        response = chatbotResponses['yardım'].message;
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

  if (!user) {
    return <div>Yükleniyor...</div>;
  }

  return (
    <Container maxWidth="xl" sx={{ py: 4 }}>
      {/* Hoş Geldin Mesajı */}
      <Box sx={{ mb: 4 }}>
        <Typography variant="h4" component="h1" gutterBottom sx={{ fontWeight: 700 }}>
          Hoş geldin, {user.name}! 👋
        </Typography>
        <Typography variant="h6" color="text.secondary">
          Sağlık durumunuzu takip etmek ve risk analizi yapmak için hazırız.
        </Typography>
      </Box>

      <Box sx={{ display: 'flex', flexDirection: { xs: 'column', lg: 'row' }, gap: 4 }}>
        {/* Sol Taraf - Ana İçerik */}
        <Box sx={{ flex: { lg: 2 } }}>
          {/* İstatistikler */}
          <Paper elevation={2} sx={{ p: 3, mb: 4 }}>
            <Typography variant="h6" gutterBottom sx={{ fontWeight: 600, mb: 3 }}>
              📊 Genel İstatistikler
            </Typography>
            <Box sx={{ display: 'grid', gridTemplateColumns: { xs: 'repeat(2, 1fr)', md: 'repeat(4, 1fr)' }, gap: 3 }}>
              <Box sx={{ textAlign: 'center' }}>
                <Typography variant="h4" color="primary" sx={{ fontWeight: 700 }}>
                  {mockDashboardStats.totalTests}
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  Toplam Test
                </Typography>
              </Box>
              <Box sx={{ textAlign: 'center' }}>
                <Typography variant="h4" color="success.main" sx={{ fontWeight: 700 }}>
                  {mockDashboardStats.completedTests}
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  Tamamlanan
                </Typography>
              </Box>
              <Box sx={{ textAlign: 'center' }}>
                <Typography variant="h4" color="warning.main" sx={{ fontWeight: 700 }}>
                  {mockDashboardStats.pendingTests}
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  Bekleyen
                </Typography>
              </Box>
              <Box sx={{ textAlign: 'center' }}>
                <Typography variant="h4" color="info.main" sx={{ fontWeight: 700 }}>
                  {mockDashboardStats.averageScore}
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  Ortalama Skor
                </Typography>
              </Box>
            </Box>
          </Paper>

          {/* Test Kartları */}
          <Typography variant="h5" gutterBottom sx={{ fontWeight: 600, mb: 3 }}>
            🧪 Mevcut Testler
          </Typography>
          <Box sx={{ display: 'grid', gridTemplateColumns: { xs: '1fr', md: 'repeat(2, 1fr)' }, gap: 3, mb: 4 }}>
            {healthTests.map((test) => (
              <Card
                key={test.id}
                elevation={3}
                sx={{
                  height: '100%',
                  display: 'flex',
                  flexDirection: 'column',
                  transition: 'transform 0.2s ease-in-out, box-shadow 0.2s ease-in-out',
                  '&:hover': {
                    transform: 'translateY(-4px)',
                    boxShadow: 6
                  }
                }}
              >
                <CardContent sx={{ flexGrow: 1 }}>
                  <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                    <Typography variant="h3" sx={{ mr: 2 }}>
                      {test.icon}
                    </Typography>
                    <Box>
                      <Typography variant="h6" component="h3" sx={{ fontWeight: 600 }}>
                        {test.name}
                      </Typography>
                      <Chip 
                        label={test.category} 
                        size="small" 
                        color="primary" 
                        variant="outlined"
                      />
                    </Box>
                  </Box>
                  
                  <Typography variant="body2" color="text.secondary" sx={{ mb: 3 }}>
                    {test.description}
                  </Typography>

                  {/* Test Metrikleri */}
                  <Box sx={{ mb: 3 }}>
                    <Typography variant="body2" color="text.secondary" sx={{ mb: 1 }}>
                      Test Metrikleri:
                    </Typography>
                    <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1 }}>
                      {test.fields.slice(0, 4).map((field) => (
                        <Chip
                          key={field.name}
                          label={field.label}
                          size="small"
                          variant="outlined"
                          sx={{ fontSize: '0.7rem' }}
                        />
                      ))}
                      {test.fields.length > 4 && (
                        <Chip
                          label={`+${test.fields.length - 4} daha`}
                          size="small"
                          variant="outlined"
                          sx={{ fontSize: '0.7rem' }}
                        />
                      )}
                    </Box>
                  </Box>
                </CardContent>
                
                <CardActions sx={{ p: 2, pt: 0 }}>
                  <Button
                    fullWidth
                    variant="contained"
                    startIcon={<PlayArrow />}
                    onClick={() => navigate(`/test/${test.id}`)}
                    sx={{ fontWeight: 600 }}
                  >
                    Teste Başla
                  </Button>
                </CardActions>
              </Card>
            ))}
          </Box>

          {/* Son Test Sonuçları */}
          {mockTestResults.length > 0 && (
            <Paper elevation={2} sx={{ p: 3 }}>
              <Typography variant="h6" gutterBottom sx={{ fontWeight: 600, mb: 3 }}>
                📋 Son Test Sonuçları
              </Typography>
              <Box sx={{ display: 'grid', gridTemplateColumns: { xs: '1fr', md: 'repeat(2, 1fr)' }, gap: 2 }}>
                {mockTestResults.slice(0, 2).map((result) => {
                  const test = healthTests.find(t => t.id === result.testId);
                  return (
                    <Card key={result.id} variant="outlined">
                      <CardContent>
                        <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
                          <Typography variant="h6" sx={{ fontWeight: 600 }}>
                            {test?.name}
                          </Typography>
                          <Chip
                            label={getRiskText(result.risk)}
                            color={getRiskColor(result.risk) as any}
                            size="small"
                          />
                        </Box>
                        <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
                          Skor: {result.score}/100
                        </Typography>
                        <Typography variant="body2" sx={{ mb: 2 }}>
                          {result.message}
                        </Typography>
                        <Box sx={{ display: 'flex', gap: 1 }}>
                          <Button
                            size="small"
                            startIcon={<Visibility />}
                            variant="outlined"
                          >
                            Görüntüle
                          </Button>
                          <Button
                            size="small"
                            startIcon={<Download />}
                            variant="outlined"
                          >
                            PDF İndir
                          </Button>
                        </Box>
                      </CardContent>
                    </Card>
                  );
                })}
              </Box>
            </Paper>
          )}
        </Box>

        {/* Sağ Taraf - Chatbot */}
        <Box sx={{ flex: { lg: 1 } }}>
          <Paper elevation={3} sx={{ height: 'fit-content', position: 'sticky', top: 20 }}>
            <Box sx={{ p: 2, borderBottom: 1, borderColor: 'divider' }}>
              <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
                <Box sx={{ display: 'flex', alignItems: 'center' }}>
                  <Avatar sx={{ bgcolor: 'primary.main', mr: 2 }}>
                    <SmartToy />
                  </Avatar>
                  <Box>
                    <Typography variant="h6" sx={{ fontWeight: 600 }}>
                      MediRisk Asistan
                    </Typography>
                    <Typography variant="body2" color="text.secondary">
                      Size nasıl yardımcı olabilirim?
                    </Typography>
                  </Box>
                </Box>
                <IconButton
                  onClick={() => setIsChatExpanded(!isChatExpanded)}
                  size="small"
                >
                  {isChatExpanded ? <ExpandLess /> : <ExpandMore />}
                </IconButton>
              </Box>
            </Box>

            {/* Chat Mesajları */}
            <Collapse in={isChatExpanded}>
              <Box sx={{ height: 400, overflowY: 'auto', p: 2 }}>
                <List sx={{ p: 0 }}>
                  {chatMessages.map((message) => (
                    <ListItem key={message.id} sx={{ px: 0 }}>
                      <ListItemAvatar>
                        <Avatar sx={{ 
                          bgcolor: message.type === 'user' ? 'primary.main' : 'grey.300',
                          color: message.type === 'user' ? 'white' : 'grey.700'
                        }}>
                          {message.type === 'user' ? <Person /> : <SmartToy />}
                        </Avatar>
                      </ListItemAvatar>
                      <ListItemText
                        primary={
                          <Box sx={{ 
                            bgcolor: message.type === 'user' ? 'primary.main' : 'grey.100',
                            color: message.type === 'user' ? 'white' : 'text.primary',
                            p: 1.5,
                            borderRadius: 2,
                            maxWidth: '80%'
                          }}>
                            <Typography variant="body2">
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
                    placeholder="Mesajınızı yazın..."
                    value={chatInput}
                    onChange={(e) => setChatInput(e.target.value)}
                    sx={{ '& .MuiOutlinedInput-root': { borderRadius: 3 } }}
                  />
                  <IconButton 
                    type="submit" 
                    color="primary"
                    disabled={!chatInput.trim()}
                  >
                    <Send />
                  </IconButton>
                </Box>
              </Box>
            </Collapse>
          </Paper>
        </Box>
      </Box>
    </Container>
  );
};

export default DashboardPage; 