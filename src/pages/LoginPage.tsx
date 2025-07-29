import React, { useState } from 'react';
import {
  Container,
  Typography,
  TextField,
  Button,
  Box,
  Alert,
  Link,
  Card,
  CardContent
} from '@mui/material';
import { useNavigate } from 'react-router-dom';
import { Login } from '@mui/icons-material';
import loginIcon from '../images/login.png';

const LoginPage: React.FC = () => {
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    email: '',
    password: ''
  });
  const [error, setError] = useState('');

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  const handleLogin = (e: React.FormEvent) => {
    e.preventDefault();
    setError('');

    if (!formData.email || !formData.password) {
      setError('Lütfen tüm alanları doldurun.');
      return;
    }

    if (formData.email === 'hasta@example.com' && formData.password === '123456') {
      localStorage.setItem('user', JSON.stringify({
        id: '1',
        email: formData.email,
        name: 'Ahmet Yılmaz',
        userType: 'patient'
      }));
      navigate('/dashboard');
    } else {
      setError('Geçersiz e-posta veya şifre.');
    }
  };

  return (
    <Container
      maxWidth={false}
      disableGutters
      sx={{
        width: '100vw',
        height: '100vh',
        backgroundColor: '#E8F4FD',
        display: 'flex',
        flexDirection: 'column',
        fontFamily: 'Inter, Arial, sans-serif',
        fontSize: '12px',
        position: 'relative',
        overflow: 'hidden',
      }}
    >
      {/* Logo ve MediRisk Yazısı Üst Sol Köşede Dikey */}
      <Box sx={{
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'flex-start',
        position: 'fixed',
        top: 24,
        left: 32,
        userSelect: 'none',
        zIndex: 10,
      }}>
        <Box
          sx={{
            width: 250,
            height: 250,
            cursor: 'default',
            mb: -2, // logo ile yazı arasındaki boşluk (isteğe göre ayarlayabilirsin)
          }}
        >
          <img
            src={loginIcon}
            alt="MediRisk Logo"
            style={{
              width: '100%',
              height: '100%',
              objectFit: 'contain',
              backgroundColor: 'transparent',
              userSelect: 'none',
            }}
            draggable={false}
          />
        </Box>
        <Typography
          variant="h2"
          component="h1"
          sx={{
            fontFamily: 'Manrope, Arial, sans-serif',
            fontWeight: 700,
            color: '#0F3978',
            fontSize: '2.8rem',
            letterSpacing: '-0.5px',
            userSelect: 'none',
            marginBottom: '4px',
            whiteSpace: 'nowrap',
          }}
        >
          MediRisk
        </Typography>
        <Typography
          variant="subtitle2"
          sx={{
            fontFamily: 'Inter, Arial, sans-serif',
            fontWeight: 400,
            color: '#4787E6',
            fontSize: '0.85rem',
            userSelect: 'none',
            marginTop: '-2px',
          }}
        >
          Geleceğin Sağlığı, Bugünün Analizi
        </Typography>
      </Box>

      {/* Hasta Girişi Kutusu Ortada */}
      <Box
        sx={{
          margin: 'auto',
          width: 700,         // ← Artık kutu 700px genişliğinde
          maxWidth: '100%',
          px: 4,
          pt: 0,
          pb: 6,
        }}
      >
        {/* Login Kart */}
        <Card
          elevation={16}
          sx={{
            borderRadius: 4,
            px: 5,
            py: 6,
            background: '#fff',
            boxShadow: '0 12px 40px 0 rgba(14,209,177,0.13)',
            width: '100%',
            transition: 'box-shadow 0.3s, transform 0.3s',
            '&:hover': {
              boxShadow: '0 16px 50px 0 rgba(14,209,177,0.20)',
              transform: 'translateY(-4px)',
            },
          }}
        >
          <CardContent sx={{ p: 0 }}>
            <Typography
              variant="h5"
              gutterBottom
              sx={{
                fontFamily: 'Manrope, Arial, sans-serif',
                fontWeight: 650, 
                textAlign: 'left',
                mb: 4,
                color: '#0F3978',
                fontSize: '2.2rem', // burada büyütüldü (ör: 2.2rem)
                userSelect: 'none',
                letterSpacing: '-0.5px',
              }}
            >
              Hasta Girişi
            </Typography>
            {error && (
              <Alert
                severity="error"
                sx={{
                  mb: 3,
                  fontSize: '12px',
                  borderRadius: 2,
                  background: '#FFEAEA',
                  color: '#D32F2F',
                }}
              >
                {error}
              </Alert>
            )}
            <Box
              component="form"
              onSubmit={handleLogin}
              sx={{
                display: 'flex',
                flexDirection: 'column',
                gap: 3,
              }}
            >
              <TextField
                fullWidth
                label="E-posta Adresi"
                name="email"
                type="email"
                value={formData.email}
                onChange={handleInputChange}
                margin="normal"
                required
                sx={{
                  fontSize: '12px',
                  fontFamily: 'Inter, Arial, sans-serif',
                  '& .MuiInputBase-root': {
                    borderRadius: 3,
                    background: '#F8FBFF',
                    fontSize: '12px',
                    transition: 'box-shadow 0.3s ease',
                  },
                  '& .MuiInputLabel-root': {
                    fontSize: '12px',
                  },
                  '& .MuiOutlinedInput-notchedOutline': {
                    borderColor: '#E0E7EF',
                  },
                  '& .MuiOutlinedInput-root.Mui-focused .MuiOutlinedInput-notchedOutline': {
                    borderColor: '#0ED1B1',
                  },
                  '& .MuiInputBase-root.Mui-focused': {
                    boxShadow: '0 0 0 3px #0ED1B133',
                  },
                }}
                InputProps={{
                  style: {
                    fontFamily: 'Inter, Arial, sans-serif',
                    fontSize: '12px',
                  },
                }}
                InputLabelProps={{
                  style: {
                    fontFamily: 'Inter, Arial, sans-serif',
                    fontSize: '12px',
                  },
                }}
              />
              <TextField
                fullWidth
                label="Şifre"
                name="password"
                type="password"
                value={formData.password}
                onChange={handleInputChange}
                margin="normal"
                required
                sx={{
                  fontSize: '12px',
                  fontFamily: 'Inter, Arial, sans-serif',
                  '& .MuiInputBase-root': {
                    borderRadius: 3,
                    background: '#F8FBFF',
                    fontSize: '12px',
                    transition: 'box-shadow 0.3s ease',
                  },
                  '& .MuiInputLabel-root': {
                    fontSize: '12px',
                  },
                  '& .MuiOutlinedInput-notchedOutline': {
                    borderColor: '#E0E7EF',
                  },
                  '& .MuiOutlinedInput-root.Mui-focused .MuiOutlinedInput-notchedOutline': {
                    borderColor: '#0ED1B1',
                  },
                  '& .MuiInputBase-root.Mui-focused': {
                    boxShadow: '0 0 0 3px #0ED1B133',
                  },
                }}
                InputProps={{
                  style: {
                    fontFamily: 'Inter, Arial, sans-serif',
                    fontSize: '12px',
                  },
                }}
                InputLabelProps={{
                  style: {
                    fontFamily: 'Inter, Arial, sans-serif',
                    fontSize: '12px',
                  },
                }}
              />
              <Button
                type="submit"
                fullWidth
                variant="contained"
                size="large"
                startIcon={<Login />}
                sx={{
                  py: 2,
                  fontSize: '1.2rem',
                  fontWeight: 600,
                  mb: 2,
                  mt: 1,
                  borderRadius: 3,
                  background: 'linear-gradient(90deg, #0ED1B1 0%, #1B69DE 100%)',
                  color: '#fff',
                  fontFamily: 'Manrope, Arial, sans-serif',
                  letterSpacing: '0.5px',
                  boxShadow: '0 4px 14px 0 rgba(14,209,177,0.25)',
                  transition: 'background 0.3s ease, box-shadow 0.3s ease',
                  '&:hover': {
                    background: 'linear-gradient(90deg, #1B69DE 0%, #0ED1B1 100%)',
                    boxShadow: '0 6px 20px 0 rgba(27,105,222,0.3)',
                  },
                }}
              >
                Giriş Yap
              </Button>
            </Box>
            <Box sx={{ textAlign: 'center', mt: 3 }}>
              <Typography
                variant="body2"
                color="text.secondary"
                sx={{
                  fontFamily: 'Inter, Arial, sans-serif',
                  fontSize: '12px',
                  userSelect: 'none',
                }}
              >
                Hesabınız yok mu?{' '}
                <Link
                  href="/register"
                  sx={{
                    fontWeight: 600,
                    color: '#0ED1B1',
                    fontFamily: 'Manrope, Arial, sans-serif',
                    fontSize: '12px',
                    textDecoration: 'none',
                    transition: 'color 0.3s ease',
                    '&:hover': {
                      color: '#1B69DE',
                      textDecoration: 'underline',
                    },
                  }}
                >
                  Kayıt Ol
                </Link>
              </Typography>
            </Box>
            <Alert
              severity="info"
              sx={{
                mt: 4,
                fontSize: '12px',
                borderRadius: 2,
                background: '#EAF3FA',
                color: '#0F3978',
                userSelect: 'none',
              }}
            >
              <strong>Demo Hasta:</strong><br />
              E-posta: <b>hasta@example.com</b><br />
              Şifre: <b>123456</b>
            </Alert>
          </CardContent>
        </Card>
      </Box>
    </Container>
  );
};

export default LoginPage;
