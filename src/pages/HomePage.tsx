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
    <Container
      maxWidth="xl"
      sx={{
        py: 4,
        backgroundColor: '#FFFFFF',
        minHeight: '100vh',
        fontFamily: 'Inter, Arial, sans-serif',
        fontSize: '12px',
      }}
    >
      {/* Hero Section */}
      <Paper
        elevation={2}
        sx={{
          p: 6,
          mb: 6,
          textAlign: 'center',
          background: '#F8FBFF',
          color: '#0F3978',
          border: '1.5px solid #E0E7EF',
          boxShadow: '0 4px 24px 0 rgba(30, 89, 174, 0.10)',
          borderRadius: 4,
        }}
      >
        <Typography
          variant="h3"
          component="h1"
          gutterBottom
          sx={{
            fontWeight: 700,
            fontFamily: 'Manrope, Arial, sans-serif',
            color: '#0F3978',
            letterSpacing: '-0.5px',
            mb: 2,
            userSelect: 'none',
          }}
        >
          Sağlık Tarama Merkezi
        </Typography>
        <Typography
          variant="h6"
          sx={{
            opacity: 0.9,
            mb: 3,
            fontFamily: 'Inter, Arial, sans-serif',
            color: '#4787E6',
            fontWeight: 500,
          }}
        >
          Yapay zeka destekli sağlık risk analizi ile geleceğinizi koruyun
        </Typography>
        <Typography
          variant="body1"
          sx={{
            opacity: 0.8,
            fontFamily: 'Inter, Arial, sans-serif',
            color: '#0F3978',
          }}
        >
          Hangi tarama veya risk analizi yapmak istersiniz?
        </Typography>
      </Paper>

      {/* Test Cards */}
      <Box
        sx={{
          display: 'grid',
          gridTemplateColumns: { xs: '1fr', md: 'repeat(3, 1fr)' },
          gap: 4,
          mb: 6,
        }}
      >
        {healthTests.map((test) => (
          <Card
            key={test.id}
            elevation={3}
            sx={{
              height: '100%',
              display: 'flex',
              flexDirection: 'column',
              borderRadius: 4,
              background: '#F8FBFF',
              border: '1.5px solid #E0E7EF',
              boxShadow: '0 4px 24px 0 rgba(30, 89, 174, 0.10)',
              transition: 'transform 0.2s, box-shadow 0.2s',
              '&:hover': {
                transform: 'translateY(-4px) scale(1.02)',
                boxShadow: '0 12px 32px 0 rgba(14,209,177,0.13)',
              },
            }}
          >
            <CardContent sx={{ flexGrow: 1, textAlign: 'center' }}>
              <Box sx={{ mb: 2 }}>
                <img
                  src={test.icon}
                  alt={test.name}
                  style={{
                    width: 32,
                    height: 32,
                    objectFit: 'contain',
                    display: 'inline-block',
                  }}
                  draggable={false}
                />
              </Box>
              <Typography
                variant="h5"
                component="h2"
                gutterBottom
                sx={{
                  fontWeight: 600,
                  fontFamily: 'Manrope, Arial, sans-serif',
                  color: '#0F3978',
                  mb: 1,
                }}
              >
                {test.name}
              </Typography>
              <Typography
                variant="body2"
                sx={{
                  mb: 3,
                  color: '#4787E6',
                  fontFamily: 'Inter, Arial, sans-serif',
                }}
              >
                {test.description}
              </Typography>
              <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1, justifyContent: 'center' }}>
                {test.fields.slice(0, 3).map((field) => (
                  <Box
                    key={field.name}
                    sx={{
                      px: 1.5,
                      py: 0.5,
                      bgcolor: '#E8F4FD',
                      color: '#0F3978',
                      borderRadius: 1,
                      fontSize: '0.75rem',
                      fontWeight: 500,
                      fontFamily: 'Inter, Arial, sans-serif',
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
                      bgcolor: '#E0E7EF',
                      color: '#1B69DE',
                      borderRadius: 1,
                      fontSize: '0.75rem',
                      fontWeight: 500,
                      fontFamily: 'Inter, Arial, sans-serif',
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
                  fontSize: '1.1rem',
                  background: 'linear-gradient(90deg, #0ED1B1 0%, #1B69DE 100%)',
                  color: '#fff',
                  borderRadius: 2,
                  boxShadow: '0 2px 8px 0 rgba(14,209,177,0.08)',
                  fontFamily: 'Manrope, Arial, sans-serif',
                  transition: 'background 0.2s, box-shadow 0.2s, transform 0.2s',
                  '&:hover': {
                    background: 'linear-gradient(90deg, #1B69DE 0%, #0ED1B1 100%)',
                    boxShadow: '0 4px 16px 0 rgba(27,105,222,0.12)',
                    transform: 'translateY(-2px) scale(1.03)',
                  },
                }}
              >
                Teste Başla
              </Button>
            </CardActions>
          </Card>
        ))}
      </Box>

      {/* Info Section */}
      <Paper
        elevation={2}
        sx={{
          p: 4,
          textAlign: 'center',
          background: '#F8FBFF',
          border: '1.5px solid #E0E7EF',
          boxShadow: '0 4px 24px 0 rgba(30, 89, 174, 0.10)',
          borderRadius: 4,
        }}
      >
        <Typography
          variant="h5"
          gutterBottom
          sx={{
            fontWeight: 600,
            fontFamily: 'Manrope, Arial, sans-serif',
            color: '#0F3978',
            mb: 2,
          }}
        >
          Nasıl Çalışır?
        </Typography>
        <Box
          sx={{
            display: 'grid',
            gridTemplateColumns: { xs: '1fr', md: 'repeat(3, 1fr)' },
            gap: 3,
            mt: 2,
          }}
        >
          <Box>
            <Typography
              variant="h6"
              gutterBottom
              sx={{
                color: '#1B69DE',
                fontFamily: 'Manrope, Arial, sans-serif',
                fontWeight: 600,
              }}
            >
              1. Test Seçin
            </Typography>
            <Typography
              variant="body2"
              sx={{
                color: '#4787E6',
                fontFamily: 'Inter, Arial, sans-serif',
              }}
            >
              İstediğiniz sağlık tarama testini seçin
            </Typography>
          </Box>
          <Box>
            <Typography
              variant="h6"
              gutterBottom
              sx={{
                color: '#1B69DE',
                fontFamily: 'Manrope, Arial, sans-serif',
                fontWeight: 600,
              }}
            >
              2. Bilgileri Girin
            </Typography>
            <Typography
              variant="body2"
              sx={{
                color: '#4787E6',
                fontFamily: 'Inter, Arial, sans-serif',
              }}
            >
              Basit formu doldurun ve verilerinizi girin
            </Typography>
          </Box>
          <Box>
            <Typography
              variant="h6"
              gutterBottom
              sx={{
                color: '#1B69DE',
                fontFamily: 'Manrope, Arial, sans-serif',
                fontWeight: 600,
              }}
            >
              3. Sonuçları Alın
            </Typography>
            <Typography
              variant="body2"
              sx={{
                color: '#4787E6',
                fontFamily: 'Inter, Arial, sans-serif',
              }}
            >
              Anında risk analizi ve öneriler alın
            </Typography>
          </Box>
        </Box>
      </Paper>
    </Container>
  );
};

export default HomePage;