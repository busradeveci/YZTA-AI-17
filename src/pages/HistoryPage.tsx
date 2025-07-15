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
    },
    {
      id: '3',
      testType: 'Depresyon Risk Değerlendirmesi',
      date: '2024-01-05',
      result: {
        risk: 'high',
        score: 78,
        message: 'Yüksek risk seviyesi',
        recommendations: ['Psikolog görüşmesi', 'Acil değerlendirme']
      },
      formData: { age: 32, stressLevel: 'Yüksek' }
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
      <Container maxWidth="lg" sx={{ py: 4 }}>
        <Paper elevation={3} sx={{ p: 4, textAlign: 'center' }}>
          <Typography variant="h4" gutterBottom sx={{ fontWeight: 700 }}>
            Test Geçmişi
          </Typography>
          <Alert severity="info" sx={{ mb: 3 }}>
            Henüz hiç test yapmadınız.
          </Alert>
          <Button
            variant="contained"
            size="large"
            onClick={() => navigate('/')}
          >
            İlk Testinizi Yapın
          </Button>
        </Paper>
      </Container>
    );
  }

  return (
    <Container maxWidth="lg" sx={{ py: 4 }}>
      <Paper elevation={3} sx={{ p: 4 }}>
        <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 4 }}>
          <Typography variant="h4" sx={{ fontWeight: 700 }}>
            Test Geçmişi
          </Typography>
          <Button
            variant="contained"
            onClick={() => navigate('/dashboard')}
          >
            Yeni Test
          </Button>
        </Box>

        <TableContainer>
          <Table>
            <TableHead>
              <TableRow>
                <TableCell sx={{ fontWeight: 600 }}>Test Türü</TableCell>
                <TableCell sx={{ fontWeight: 600 }}>Tarih</TableCell>
                <TableCell sx={{ fontWeight: 600 }}>Risk Skoru</TableCell>
                <TableCell sx={{ fontWeight: 600 }}>Risk Seviyesi</TableCell>
                <TableCell sx={{ fontWeight: 600 }}>Durum</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {mockHistory.map((test) => (
                <TableRow key={test.id} hover>
                  <TableCell>
                    <Typography variant="body1" sx={{ fontWeight: 500 }}>
                      {test.testType}
                    </Typography>
                  </TableCell>
                  <TableCell>
                    <Typography variant="body2" color="text.secondary">
                      {formatDate(test.date)}
                    </Typography>
                  </TableCell>
                  <TableCell>
                    <Typography variant="h6" sx={{ fontWeight: 700 }}>
                      {test.result.score}%
                    </Typography>
                  </TableCell>
                  <TableCell>
                    <Chip
                      label={getRiskLabel(test.result.risk)}
                      color={getRiskColor(test.result.risk) as any}
                      variant="filled"
                      sx={{ fontWeight: 600 }}
                    />
                  </TableCell>
                  <TableCell>
                    <Typography variant="body2" color="text.secondary">
                      {test.result.message}
                    </Typography>
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </TableContainer>

        <Box sx={{ mt: 4, p: 3, bgcolor: 'grey.50', borderRadius: 2 }}>
          <Typography variant="h6" gutterBottom sx={{ fontWeight: 600 }}>
            📊 İstatistikler
          </Typography>
          <Box sx={{ display: 'grid', gridTemplateColumns: { xs: '1fr', md: 'repeat(3, 1fr)' }, gap: 3, mt: 2 }}>
            <Box sx={{ textAlign: 'center' }}>
              <Typography variant="h4" color="primary" sx={{ fontWeight: 700 }}>
                {mockHistory.length}
              </Typography>
              <Typography variant="body2" color="text.secondary">
                Toplam Test
              </Typography>
            </Box>
            <Box sx={{ textAlign: 'center' }}>
              <Typography variant="h4" color="success.main" sx={{ fontWeight: 700 }}>
                {mockHistory.filter(t => t.result.risk === 'low').length}
              </Typography>
              <Typography variant="body2" color="text.secondary">
                Düşük Risk
              </Typography>
            </Box>
            <Box sx={{ textAlign: 'center' }}>
              <Typography variant="h4" color="warning.main" sx={{ fontWeight: 700 }}>
                {mockHistory.filter(t => t.result.risk === 'medium').length}
              </Typography>
              <Typography variant="body2" color="text.secondary">
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