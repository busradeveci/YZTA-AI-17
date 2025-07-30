import React from 'react';
import {
  Container,
  Typography,
  Paper,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Chip,
  Box,
  Alert,
  Button
} from '@mui/material';
import { useNavigate } from 'react-router-dom';
import { TestHistory } from '../types';

const HistoryPage: React.FC = () => {
  const navigate = useNavigate();

  // Mock geçmiş veri
  const mockHistory: TestHistory[] = [
    {
      id: '1',
      testType: 'Fetal Sağlık Taraması',
      date: '2024-01-15',
      result: {
        risk: 'low',
        score: 25,
        message: 'Düşük risk seviyesi',
        recommendations: ['Düzenli kontroller', 'Sağlıklı beslenme']
      },
      formData: { age: 28, gestationalAge: 24 }
    },
    {
      id: '2',
      testType: 'Meme Kanseri Risk Analizi',
      date: '2024-01-10',
      result: {
        risk: 'medium',
        score: 45,
        message: 'Orta risk seviyesi',
        recommendations: ['Doktor kontrolü', 'Mamografi']
      },
      formData: { age: 45, gender: 'Kadın' }
    }
  ];

  const getRiskColor = (risk: string) => {
    switch (risk) {
      case 'low': return 'success';
      case 'medium': return 'warning';
      case 'high': return 'error';
      default: return 'default';
    }
  };

  const getRiskLabel = (risk: string) => {
    switch (risk) {
      case 'low': return 'Düşük';
      case 'medium': return 'Orta';
      case 'high': return 'Yüksek';
      default: return 'Bilinmiyor';
    }
  };

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('tr-TR');
  };

  if (mockHistory.length === 0) {
    return (
      <Container
        maxWidth="lg"
        sx={{
          py: 4,
          backgroundColor: '#FFFFFF', // Arka plan tamamen beyaz
          minHeight: '100vh',
          fontFamily: 'Inter, Arial, sans-serif'
        }}
      >
        <Paper elevation={3} sx={{
          p: 4,
          textAlign: 'center',
          background: '#F8FBFF',
          border: '1.5px solid #E0E7EF',
          boxShadow: '0 4px 24px 0 rgba(30, 89, 174, 0.10)',
          borderRadius: 4,
        }}>
          <Typography variant="h4" gutterBottom sx={{
            fontWeight: 700,
            fontFamily: 'Manrope, Arial, sans-serif',
            color: '#0F3978'
          }}>
            Test Geçmişi
          </Typography>
          <Alert severity="info" sx={{ mb: 3, fontFamily: 'Inter, Arial, sans-serif' }}>
            Henüz hiç test yapmadınız.
          </Alert>
          <Button
            variant="contained"
            size="large"
            onClick={() => navigate('/')}
            sx={{
              background: 'linear-gradient(90deg, #0ED1B1 0%, #1B69DE 100%)',
              color: '#fff',
              fontWeight: 600,
              fontFamily: 'Manrope, Arial, sans-serif',
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
            İlk Testinizi Yapın
          </Button>
        </Paper>
      </Container>
    );
  }

  return (
    <Container
      maxWidth="lg"
      sx={{
        py: 4,
        backgroundColor: '#FFFFFF', // Arka plan tamamen beyaz
        minHeight: '100vh',
        fontFamily: 'Inter, Arial, sans-serif'
      }}
    >
      <Paper elevation={3} sx={{
        p: 4,
        background: '#F8FBFF',
        border: '1.5px solid #E0E7EF',
        boxShadow: '0 4px 24px 0 rgba(30, 89, 174, 0.10)',
        borderRadius: 4,
      }}>
        <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 4 }}>
          <Typography variant="h4" sx={{
            fontWeight: 700,
            fontFamily: 'Manrope, Arial, sans-serif',
            color: '#0F3978'
          }}>
            Test Geçmişi
          </Typography>
          <Button
            variant="contained"
            onClick={() => navigate('/dashboard')}
            sx={{
              background: 'linear-gradient(90deg, #0ED1B1 0%, #1B69DE 100%)',
              color: '#fff',
              fontWeight: 600,
              fontFamily: 'Manrope, Arial, sans-serif',
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
            Yeni Test
          </Button>
        </Box>

        <TableContainer>
          <Table>
            <TableHead>
              <TableRow>
                <TableCell sx={{ fontWeight: 600, color: '#0F3978', fontFamily: 'Manrope, Arial, sans-serif', fontSize: '1rem' }}>Test Türü</TableCell>
                <TableCell sx={{ fontWeight: 600, color: '#0F3978', fontFamily: 'Manrope, Arial, sans-serif', fontSize: '1rem' }}>Tarih</TableCell>
                <TableCell sx={{ fontWeight: 600, color: '#0F3978', fontFamily: 'Manrope, Arial, sans-serif', fontSize: '1rem' }}>Risk Skoru</TableCell>
                <TableCell sx={{ fontWeight: 600, color: '#0F3978', fontFamily: 'Manrope, Arial, sans-serif', fontSize: '1rem' }}>Risk Seviyesi</TableCell>
                <TableCell sx={{ fontWeight: 600, color: '#0F3978', fontFamily: 'Manrope, Arial, sans-serif', fontSize: '1rem' }}>Durum</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {mockHistory.map((test) => (
                <TableRow key={test.id} hover sx={{
                  background: '#FFFFFF',
                  borderBottom: '1.5px solid #E0E7EF',
                  '&:hover': {
                    background: '#F0F6FF'
                  }
                }}>
                  <TableCell>
                    <Typography variant="body1" sx={{ fontWeight: 500, color: '#0F3978', fontFamily: 'Manrope, Arial, sans-serif' }}>
                      {test.testType}
                    </Typography>
                  </TableCell>
                  <TableCell>
                    <Typography variant="body2" sx={{ color: '#4787E6', fontFamily: 'Inter, Arial, sans-serif' }}>
                      {formatDate(test.date)}
                    </Typography>
                  </TableCell>
                  <TableCell>
                    <Typography variant="h6" sx={{ fontWeight: 700, color: '#1B69DE', fontFamily: 'Manrope, Arial, sans-serif' }}>
                      {test.result.score}%
                    </Typography>
                  </TableCell>
                  <TableCell>
                    <Chip
                      label={getRiskLabel(test.result.risk)}
                      color={getRiskColor(test.result.risk) as any}
                      variant="filled"
                      sx={{
                        fontWeight: 600,
                        fontFamily: 'Inter, Arial, sans-serif',
                        fontSize: '0.95rem',
                        px: 1.5,
                        borderRadius: 2,
                        letterSpacing: 0,
                      }}
                    />
                  </TableCell>
                  <TableCell>
                    <Typography variant="body2" sx={{ color: '#4787E6', fontFamily: 'Inter, Arial, sans-serif' }}>
                      {test.result.message}
                    </Typography>
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </TableContainer>

        <Box sx={{
          mt: 4,
          p: 3,
          background: '#FFFFFF',
          border: '1.5px solid #E0E7EF',
          borderRadius: 3,
          boxShadow: '0 2px 12px 0 rgba(30, 89, 174, 0.07)'
        }}>
          <Typography variant="h6" gutterBottom sx={{
            fontWeight: 700,
            color: '#0F3978',
            fontFamily: 'Manrope, Arial, sans-serif'
          }}>
            İstatistikler
          </Typography>
          <Box sx={{ display: 'grid', gridTemplateColumns: { xs: '1fr', md: 'repeat(3, 1fr)' }, gap: 3, mt: 2 }}>
            <Box sx={{ textAlign: 'center' }}>
              <Typography variant="h4" sx={{ color: '#1B69DE', fontWeight: 700, fontFamily: 'Manrope, Arial, sans-serif' }}>
                {mockHistory.length}
              </Typography>
              <Typography variant="body2" sx={{ color: '#4787E6', fontFamily: 'Inter, Arial, sans-serif' }}>
                Toplam Test
              </Typography>
            </Box>
            <Box sx={{ textAlign: 'center' }}>
              <Typography variant="h4" sx={{ color: '#2CB67D', fontWeight: 700, fontFamily: 'Manrope, Arial, sans-serif' }}>
                {mockHistory.filter(t => t.result.risk === 'low').length}
              </Typography>
              <Typography variant="body2" sx={{ color: '#4787E6', fontFamily: 'Inter, Arial, sans-serif' }}>
                Düşük Risk
              </Typography>
            </Box>
            <Box sx={{ textAlign: 'center' }}>
              <Typography variant="h4" sx={{ color: '#F9A825', fontWeight: 700, fontFamily: 'Manrope, Arial, sans-serif' }}>
                {mockHistory.filter(t => t.result.risk === 'medium').length}
              </Typography>
              <Typography variant="body2" sx={{ color: '#4787E6', fontFamily: 'Inter, Arial, sans-serif' }}>
                Orta Risk
              </Typography>
            </Box>
          </Box>
        </Box>
      </Paper>
    </Container>
  );
};

export default HistoryPage;