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
import dashboardIcon from '../images/dashboard.png'; // Eğer bir dashboard ikonun varsa ekleyebilirsin
import logo from '../images/login.png';
import robotIcon from '../images/robot.png'; // en üstte ekleyin

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
    <Container
      maxWidth="xl"
      sx={{
        py: 4,
        backgroundColor: '#FFFFFF', // Arka plan rengi kırık beyaz yapıldı
        minHeight: '100vh',
        fontFamily: 'Inter, Arial, sans-serif',
        fontSize: '12px',
      }}
    >
      {/* Hoş Geldin Mesajı */}
      <Box sx={{ mb: 4 }}>
        <Typography
          variant="h4"
          component="h1"
          gutterBottom
          sx={{
            fontFamily: 'Manrope, Arial, sans-serif',
            fontWeight: 700,
            color: '#0F3978',
            fontSize: '2.2rem',
            letterSpacing: '-0.5px',
            userSelect: 'none',
            display: 'flex',
            alignItems: 'center',
            gap: 2,
          }}
        >
          {/* İsteğe bağlı ikon */}
          {/* <img src={dashboardIcon} alt="" style={{ width: 48, height: 48, objectFit: 'contain' }} /> */}
          Hoş geldin, {user.name}!
        </Typography>
        <Typography
          variant="h6"
          color="text.secondary"
          sx={{
            fontFamily: 'Inter, Arial, sans-serif',
            fontWeight: 400,
            color: '#4787E6',
            fontSize: '1.1rem',
            mb: 1,
            userSelect: 'none',
          }}
        >
          Sağlık durumunuzu takip etmek ve risk analizi yapmak için hazırız.
        </Typography>
      </Box>

      <Box sx={{ display: 'flex', flexDirection: { xs: 'column', lg: 'row' }, gap: 4 }}>
        {/* Sol Taraf - Ana İçerik */}
        <Box sx={{ flex: { lg: 2 } }}>
          {/* İstatistikler */}
          <Paper
            elevation={2}
            sx={{
              p: 3,
              mb: 4,
              borderRadius: 4,
              background: '#F8FBFF', // Kutucukların arka planı hafif kırık beyaz
              border: '1.5px solid #E0E7EF', // Kenar belirgin ve hafif kırık beyaz
              boxShadow: '0 4px 24px 0 rgba(30, 89, 174, 0.10)', // Daha belirgin gölge
            }}
          >
            <Typography
              variant="h6"
              gutterBottom
              sx={{
                fontFamily: 'Manrope, Arial, sans-serif',
                fontWeight: 600,
                color: '#1B69DE',
                mb: 3,
                fontSize: '1.15rem',
                userSelect: 'none',
              }}
            >
              Genel İstatistikler
            </Typography>
            <Box sx={{ display: 'grid', gridTemplateColumns: { xs: 'repeat(2, 1fr)', md: 'repeat(4, 1fr)' }, gap: 3 }}>
              <Box sx={{ textAlign: 'center' }}>
                <Typography variant="h4" sx={{ fontWeight: 700, color: '#0ED1B1', fontFamily: 'Manrope, Arial, sans-serif', fontSize: '2rem' }}>
                  {mockDashboardStats.totalTests}
                </Typography>
                <Typography variant="body2" color="text.secondary" sx={{ fontFamily: 'Inter, Arial, sans-serif', fontSize: '12px' }}>
                  Toplam Test
                </Typography>
              </Box>
              <Box sx={{ textAlign: 'center' }}>
                <Typography variant="h4" sx={{ fontWeight: 700, color: '#1B69DE', fontFamily: 'Manrope, Arial, sans-serif', fontSize: '2rem' }}>
                  {mockDashboardStats.completedTests}
                </Typography>
                <Typography variant="body2" color="text.secondary" sx={{ fontFamily: 'Inter, Arial, sans-serif', fontSize: '12px' }}>
                  Tamamlanan
                </Typography>
              </Box>
              <Box sx={{ textAlign: 'center' }}>
                <Typography variant="h4" sx={{ fontWeight: 700, color: '#F9A825', fontFamily: 'Manrope, Arial, sans-serif', fontSize: '2rem' }}>
                  {mockDashboardStats.pendingTests}
                </Typography>
                <Typography variant="body2" color="text.secondary" sx={{ fontFamily: 'Inter, Arial, sans-serif', fontSize: '12px' }}>
                  Bekleyen
                </Typography>
              </Box>
              <Box sx={{ textAlign: 'center' }}>
                <Typography variant="h4" sx={{ fontWeight: 700, color: '#4787E6', fontFamily: 'Manrope, Arial, sans-serif', fontSize: '2rem' }}>
                  {mockDashboardStats.averageScore}
                </Typography>
                <Typography variant="body2" color="text.secondary" sx={{ fontFamily: 'Inter, Arial, sans-serif', fontSize: '12px' }}>
                  Ortalama Skor
                </Typography>
              </Box>
            </Box>
          </Paper>

          {/* Test Kartları */}
          <Typography
            variant="h5"
            gutterBottom
            sx={{
              fontFamily: 'Manrope, Arial, sans-serif',
              fontWeight: 600,
              color: '#0F3978',
              mb: 3,
              fontSize: '1.4rem',
              userSelect: 'none',
            }}
          >
            Mevcut Testler
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
                  borderRadius: 4,
                  background: '#F8FBFF', // Kutucukların arka planı hafif kırık beyaz
                  border: '1.5px solid #E0E7EF', // Kenar belirgin ve hafif kırık beyaz
                  boxShadow: '0 4px 24px 0 rgba(30, 89, 174, 0.10)', // Daha belirgin gölge
                  transition: 'transform 0.2s, box-shadow 0.2s',
                  '&:hover': {
                    transform: 'translateY(-4px) scale(1.02)',
                    boxShadow: '0 12px 32px 0 rgba(14,209,177,0.13)',
                  }
                }}
              >
                <CardContent sx={{ flexGrow: 1 }}>
                  <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                    <Box sx={{ mr: 2 }}>
                      <img
                        src={test.icon}
                        alt={test.name}
                        style={{
                          width: 48,
                          height: 48,
                          objectFit: 'contain',
                          display: 'inline-block'
                        }}
                        draggable={false}
                      />
                    </Box>
                    <Box>
                      <Typography variant="h6" component="h3" sx={{
                        fontWeight: 600,
                        fontFamily: 'Manrope, Arial, sans-serif',
                        color: '#0F3978'
                      }}>
                        {test.name}
                      </Typography>
                      <Chip
                        label={test.category}
                        size="small"
                        color="primary"
                        variant="outlined"
                        sx={{
                          fontFamily: 'Inter, Arial, sans-serif',
                          fontSize: '11px'
                        }}
                      />
                    </Box>
                  </Box>
                  <Typography variant="body2" color="text.secondary" sx={{
                    mb: 3,
                    fontFamily: 'Inter, Arial, sans-serif',
                    fontSize: '12px'
                  }}>
                    {test.description}
                  </Typography>
                  {/* Test Metrikleri */}
                  <Box sx={{ mb: 3 }}>
                    <Typography variant="body2" color="text.secondary" sx={{
                      mb: 1,
                      fontFamily: 'Inter, Arial, sans-serif',
                      fontSize: '12px'
                    }}>
                      Test Metrikleri:
                    </Typography>
                    <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1 }}>
                      {test.fields.slice(0, 4).map((field) => (
                        <Chip
                          key={field.name}
                          label={field.label}
                          size="small"
                          variant="outlined"
                          sx={{ fontSize: '0.7rem', fontFamily: 'Inter, Arial, sans-serif' }}
                        />
                      ))}
                      {test.fields.length > 4 && (
                        <Chip
                          label={`+${test.fields.length - 4} daha`}
                          size="small"
                          variant="outlined"
                          sx={{ fontSize: '0.7rem', fontFamily: 'Inter, Arial, sans-serif' }}
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
                    sx={{
                      fontWeight: 600,
                      fontFamily: 'Manrope, Arial, sans-serif',
                      fontSize: '1rem',
                      background: 'linear-gradient(90deg, #0ED1B1 0%, #1B69DE 100%)',
                      color: '#fff',
                      borderRadius: 2,
                      boxShadow: '0 2px 8px 0 rgba(14,209,177,0.08)',
                      transition: 'background 0.2s, box-shadow 0.2s, transform 0.2s',
                      '&:hover': {
                        background: 'linear-gradient(90deg, #1B69DE 0%, #0ED1B1 100%)',
                        boxShadow: '0 4px 16px 0 rgba(27,105,222,0.12)',
                        transform: 'translateY(-2px) scale(1.03)'
                      }
                    }}
                  >
                    Teste Başla
                  </Button>
                </CardActions>
              </Card>
            ))}
          </Box>

          {/* Son Test Sonuçları */}
          {mockTestResults.length > 0 && (
            <Paper
              elevation={2}
              sx={{
                p: 3,
                borderRadius: 4,
                background: '#F8FBFF',
                border: '1.5px solid #E0E7EF',
                boxShadow: '0 4px 24px 0 rgba(30, 89, 174, 0.10)',
              }}
            >
              <Typography
                variant="h6"
                gutterBottom
                sx={{
                  fontFamily: 'Manrope, Arial, sans-serif',
                  fontWeight: 600,
                  color: '#1B69DE',
                  mb: 3,
                  fontSize: '1.15rem',
                  userSelect: 'none',
                }}
              >
                Son Test Sonuçları
              </Typography>
              <Box sx={{ display: 'grid', gridTemplateColumns: { xs: '1fr', md: 'repeat(2, 1fr)' }, gap: 2 }}>
                {mockTestResults.slice(0, 2).map((result) => {
                  const test = healthTests.find(t => t.id === result.testId);
                  return (
                    <Card key={result.id} variant="outlined" sx={{
                      borderRadius: 3,
                      background: '#F8FBFF',
                      border: '1.5px solid #E0E7EF',
                      boxShadow: '0 4px 24px 0 rgba(30, 89, 174, 0.10)',
                    }}>
                      <CardContent>
                        <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
                          <Typography variant="h6" sx={{
                            fontWeight: 600,
                            fontFamily: 'Manrope, Arial, sans-serif',
                            color: '#0F3978'
                          }}>
                            {test?.name}
                          </Typography>
                          <Chip
                            label={getRiskText(result.risk)}
                            color={getRiskColor(result.risk) as any}
                            size="small"
                            sx={{ fontFamily: 'Inter, Arial, sans-serif', fontSize: '11px' }}
                          />
                        </Box>
                        <Typography variant="body2" color="text.secondary" sx={{
                          mb: 2,
                          fontFamily: 'Inter, Arial, sans-serif',
                          fontSize: '12px'
                        }}>
                          Skor: {result.score}/100
                        </Typography>
                        <Typography variant="body2" sx={{
                          mb: 2,
                          fontFamily: 'Inter, Arial, sans-serif',
                          fontSize: '12px'
                        }}>
                          {result.message}
                        </Typography>
                        <Box sx={{ display: 'flex', gap: 1 }}>
                          <Button
                            size="small"
                            startIcon={<Visibility />}
                            variant="outlined"
                            sx={{
                              fontFamily: 'Manrope, Arial, sans-serif',
                              fontWeight: 600,
                              fontSize: '12px',
                              color: '#1B69DE',
                              borderColor: '#1B69DE',
                              '&:hover': {
                                background: '#EAF3FA',
                                borderColor: '#0ED1B1',
                                color: '#0ED1B1'
                              }
                            }}
                          >
                            Görüntüle
                          </Button>
                          <Button
                            size="small"
                            startIcon={<Download />}
                            variant="outlined"
                            sx={{
                              fontFamily: 'Manrope, Arial, sans-serif',
                              fontWeight: 600,
                              fontSize: '12px',
                              color: '#0F3978',
                              borderColor: '#0F3978',
                              '&:hover': {
                                background: '#EAF3FA',
                                borderColor: '#0ED1B1',
                                color: '#0ED1B1'
                              }
                            }}
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
          <Paper
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
                  <div>
                    <div className="font-semibold font-poppins text-white text-base">MediRisk Asistan</div>
                    <div className="text-xs text-[#7f5af0] font-poppins">Size nasıl yardımcı olabilirim?</div>
                  </div>
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
                          bgcolor: message.type === 'user' ? '#1B69DE' : '#EAF3FA',
                          color: message.type === 'user' ? 'white' : '#0F3978',
                          fontFamily: 'Manrope, Arial, sans-serif'
                        }}>
                          {message.type === 'user' ? <Person /> : <SmartToy />}
                        </Avatar>
                      </ListItemAvatar>
                      <ListItemText
                        primary={
                          <Box sx={{
                            bgcolor: message.type === 'user' ? '#1B69DE' : '#F8FBFF',
                            color: message.type === 'user' ? 'white' : '#0F3978',
                            p: 1.5,
                            borderRadius: 2,
                            maxWidth: '80%',
                            fontFamily: 'Inter, Arial, sans-serif',
                            fontSize: '12px'
                          }}>
                            <Typography variant="body2" sx={{
                              fontFamily: 'Inter, Arial, sans-serif',
                              fontSize: '12px'
                            }}>
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
                    sx={{
                      '& .MuiOutlinedInput-root': { borderRadius: 3 },
                      fontFamily: 'Inter, Arial, sans-serif',
                      fontSize: '12px'
                    }}
                  />
                  <IconButton
                    type="submit"
                    color="primary"
                    disabled={!chatInput.trim()}
                    sx={{
                      background: '#0ED1B1',
                      color: '#fff',
                      borderRadius: 2,
                      transition: 'background 0.2s',
                      '&:hover': {
                        background: '#1B69DE'
                      }
                    }}
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