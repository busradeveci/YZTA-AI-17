import React from 'react';
import {
  Container,
  Typography,
  Card,
  CardContent,
  CardActions,
  Button,
  Box,
  Paper
} from '@mui/material';
import { useNavigate } from 'react-router-dom';
import { healthTests } from '../utils/mockData';

const HomePage: React.FC = () => {
  const navigate = useNavigate();

  return (
    <Container maxWidth="lg" sx={{ py: 4 }}>
      {/* Hero Section */}
      <Paper
        elevation={3}
        sx={{
          p: 6,
          mb: 6,
          textAlign: 'center',
          background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
          color: 'white'
        }}
      >
        <Typography variant="h3" component="h1" gutterBottom sx={{ fontWeight: 700 }}>
          🏥 Sağlık Tarama Merkezi
        </Typography>
        <Typography variant="h6" sx={{ opacity: 0.9, mb: 3 }}>
          Yapay zeka destekli sağlık risk analizi ile geleceğinizi koruyun
        </Typography>
        <Typography variant="body1" sx={{ opacity: 0.8 }}>
          Hangi tarama veya risk analizi yapmak istersiniz?
        </Typography>
      </Paper>

      {/* Test Cards */}
      <Box sx={{ 
        display: 'grid', 
        gridTemplateColumns: { xs: '1fr', md: 'repeat(3, 1fr)' }, 
        gap: 4,
        mb: 6
      }}>
        {healthTests.map((test) => (
          <Card
            key={test.id}
            elevation={4}
            sx={{
              height: '100%',
              display: 'flex',
              flexDirection: 'column',
              transition: 'transform 0.2s ease-in-out, box-shadow 0.2s ease-in-out',
              '&:hover': {
                transform: 'translateY(-4px)',
                boxShadow: 8
              }
            }}
          >
            <CardContent sx={{ flexGrow: 1, textAlign: 'center' }}>
              <Box sx={{ fontSize: '4rem', mb: 2 }}>
                {test.icon}
              </Box>
              <Typography variant="h5" component="h2" gutterBottom sx={{ fontWeight: 600 }}>
                {test.name}
              </Typography>
              <Typography variant="body2" color="text.secondary" sx={{ mb: 3 }}>
                {test.description}
              </Typography>
              <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1, justifyContent: 'center' }}>
                {test.fields.slice(0, 3).map((field) => (
                  <Box
                    key={field.name}
                    sx={{
                      px: 1.5,
                      py: 0.5,
                      bgcolor: 'primary.light',
                      color: 'white',
                      borderRadius: 1,
                      fontSize: '0.75rem',
                      fontWeight: 500
                    }}
                  >
                    {field.label}
                  </Box>
                ))}
                {test.fields.length > 3 && (
                  <Box
                    sx={{
                      px: 1.5,
                      py: 0.5,
                      bgcolor: 'grey.300',
                      color: 'grey.700',
                      borderRadius: 1,
                      fontSize: '0.75rem',
                      fontWeight: 500
                    }}
                  >
                    +{test.fields.length - 3} daha
                  </Box>
                )}
              </Box>
            </CardContent>
            <CardActions sx={{ p: 3, pt: 0 }}>
              <Button
                fullWidth
                variant="contained"
                size="large"
                onClick={() => navigate(`/test/${test.id}`)}
                sx={{
                  py: 1.5,
                  fontWeight: 600,
                  fontSize: '1.1rem'
                }}
              >
                Teste Başla
              </Button>
            </CardActions>
          </Card>
        ))}
      </Box>

      {/* Info Section */}
      <Paper elevation={2} sx={{ p: 4, textAlign: 'center' }}>
        <Typography variant="h5" gutterBottom sx={{ fontWeight: 600 }}>
          💡 Nasıl Çalışır?
        </Typography>
        <Box sx={{ 
          display: 'grid', 
          gridTemplateColumns: { xs: '1fr', md: 'repeat(3, 1fr)' }, 
          gap: 3, 
          mt: 2 
        }}>
          <Box>
            <Typography variant="h6" gutterBottom color="primary">
              1. Test Seçin
            </Typography>
            <Typography variant="body2" color="text.secondary">
              İstediğiniz sağlık tarama testini seçin
            </Typography>
          </Box>
          <Box>
            <Typography variant="h6" gutterBottom color="primary">
              2. Bilgileri Girin
            </Typography>
            <Typography variant="body2" color="text.secondary">
              Basit formu doldurun ve verilerinizi girin
            </Typography>
          </Box>
          <Box>
            <Typography variant="h6" gutterBottom color="primary">
              3. Sonuçları Alın
            </Typography>
            <Typography variant="body2" color="text.secondary">
              Anında risk analizi ve öneriler alın
            </Typography>
          </Box>
        </Box>
      </Paper>
    </Container>
  );
};

export default HomePage; 