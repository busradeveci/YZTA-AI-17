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
import { Login, Person } from '@mui/icons-material';

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

    // Basit validasyon
    if (!formData.email || !formData.password) {
      setError('Lütfen tüm alanları doldurun.');
      return;
    }

    // Mock giriş - gerçek uygulamada API çağrısı yapılacak
    if (formData.email === 'hasta@example.com' && formData.password === '123456') {
      // Hasta girişi
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
    <Container maxWidth="sm" sx={{ py: 8 }}>
      {/* Logo ve Başlık */}
      <Box sx={{ textAlign: 'center', mb: 4 }}>
        <Typography variant="h3" component="h1" gutterBottom sx={{ fontWeight: 700, color: 'primary.main' }}>
          🏥 MediRisk
        </Typography>
        <Typography variant="h6" color="text.secondary">
          Yapay Zeka Destekli Sağlık Risk Analizi Platformu
        </Typography>
      </Box>

      {/* Giriş Kartı */}
      <Card elevation={8} sx={{ borderRadius: 3 }}>
        <CardContent>
          <Typography variant="h5" gutterBottom sx={{ fontWeight: 600, textAlign: 'center', mb: 3 }}>
            Hasta Girişi
          </Typography>
          {error && (
            <Alert severity="error" sx={{ mb: 2 }}>
              {error}
            </Alert>
          )}
          <Box component="form" onSubmit={handleLogin}>
            <TextField
              fullWidth
              label="E-posta Adresi"
              name="email"
              type="email"
              value={formData.email}
              onChange={handleInputChange}
              margin="normal"
              required
              sx={{ mb: 2 }}
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
              sx={{ mb: 3 }}
            />
            <Button
              type="submit"
              fullWidth
              variant="contained"
              size="large"
              startIcon={<Login />}
              sx={{
                py: 1.5,
                fontSize: '1.1rem',
                fontWeight: 600,
                mb: 2
              }}
            >
              Giriş Yap
            </Button>
          </Box>
          <Box sx={{ textAlign: 'center' }}>
            <Typography variant="body2" color="text.secondary">
              Hesabınız yok mu?{' '}
              <Link href="/register" sx={{ fontWeight: 600 }}>
                Kayıt Ol
              </Link>
            </Typography>
          </Box>
          {/* Demo Bilgileri */}
          <Alert severity="info" sx={{ mt: 3 }}>
            <strong>Demo Hasta:</strong><br />
            E-posta: <b>hasta@example.com</b><br />
            Şifre: <b>123456</b>
          </Alert>
        </CardContent>
      </Card>
    </Container>
  );
};

export default LoginPage; 