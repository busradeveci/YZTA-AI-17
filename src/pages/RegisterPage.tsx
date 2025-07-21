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
  CardContent,
  FormControl,
  InputLabel,
  Select,
  MenuItem
} from '@mui/material';
import { useNavigate } from 'react-router-dom';
import { PersonAdd } from '@mui/icons-material';

const RegisterPage: React.FC = () => {
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    password: '',
    confirmPassword: '',
    age: '',
    gender: '',
    phone: ''
  });
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  const handleSelectChange = (e: any) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  const handleRegister = (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setSuccess('');

    // Validasyon
    if (!formData.name || !formData.email || !formData.password || !formData.confirmPassword) {
      setError('Lütfen tüm zorunlu alanları doldurun.');
      return;
    }

    if (formData.password !== formData.confirmPassword) {
      setError('Şifreler eşleşmiyor.');
      return;
    }

    if (formData.password.length < 6) {
      setError('Şifre en az 6 karakter olmalıdır.');
      return;
    }

    if (!formData.age || !formData.gender) {
      setError('Yaş ve cinsiyet zorunludur.');
      return;
    }

    // Mock kayıt - gerçek uygulamada API çağrısı yapılacak
    const userId = Date.now().toString();
    const newUser = {
      id: userId,
      email: formData.email,
      name: formData.name,
      userType: 'patient',
      createdAt: new Date(),
      age: parseInt(formData.age),
      gender: formData.gender,
      phone: formData.phone
    };

    // Kullanıcıyı localStorage'a kaydet
    localStorage.setItem('user', JSON.stringify(newUser));
    setSuccess('Hasta kaydınız başarıyla oluşturuldu!');
    // 2 saniye sonra yönlendir
    setTimeout(() => {
      navigate('/dashboard');
    }, 2000);
  };

  return (
    <Container maxWidth="sm" sx={{ py: 8 }}>
      {/* Logo ve Başlık */}
      <Box sx={{ textAlign: 'center', mb: 4 }}>
        <Typography variant="h3" component="h1" gutterBottom sx={{ fontWeight: 700, color: 'primary.main' }}>
          🏥 MediRisk
        </Typography>
        <Typography variant="h6" color="text.secondary">
          Hesap Oluştur
        </Typography>
      </Box>
      {/* Kayıt Kartı */}
      <Card elevation={8} sx={{ borderRadius: 3 }}>
        <CardContent>
          <Typography variant="h5" gutterBottom sx={{ fontWeight: 600, textAlign: 'center', mb: 3 }}>
            Hasta Kaydı
          </Typography>
          {error && (
            <Alert severity="error" sx={{ mb: 2 }}>
              {error}
            </Alert>
          )}
          {success && (
            <Alert severity="success" sx={{ mb: 2 }}>
              {success}
            </Alert>
          )}
          <Box component="form" onSubmit={handleRegister}>
            <TextField
              fullWidth
              label="Ad Soyad"
              name="name"
              value={formData.name}
              onChange={handleInputChange}
              margin="normal"
              required
              sx={{ mb: 2 }}
            />
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
              sx={{ mb: 2 }}
            />
            <TextField
              fullWidth
              label="Şifre (Tekrar)"
              name="confirmPassword"
              type="password"
              value={formData.confirmPassword}
              onChange={handleInputChange}
              margin="normal"
              required
              sx={{ mb: 2 }}
            />
            <TextField
              fullWidth
              label="Yaş"
              name="age"
              type="number"
              value={formData.age}
              onChange={handleInputChange}
              margin="normal"
              required
              sx={{ mb: 2 }}
            />
            <FormControl fullWidth required sx={{ mb: 2 }}>
              <InputLabel>Cinsiyet</InputLabel>
              <Select
                name="gender"
                value={formData.gender}
                label="Cinsiyet"
                onChange={handleSelectChange}
              >
                <MenuItem value="Erkek">Erkek</MenuItem>
                <MenuItem value="Kadın">Kadın</MenuItem>
              </Select>
            </FormControl>
            <TextField
              fullWidth
              label="Telefon (opsiyonel)"
              name="phone"
              value={formData.phone}
              onChange={handleInputChange}
              margin="normal"
              sx={{ mb: 2 }}
            />
            <Button
              type="submit"
              fullWidth
              variant="contained"
              size="large"
              startIcon={<PersonAdd />}
              sx={{
                py: 1.5,
                fontSize: '1.1rem',
                fontWeight: 600,
                mb: 2
              }}
            >
              Kayıt Ol
            </Button>
          </Box>
          <Box sx={{ textAlign: 'center' }}>
            <Typography variant="body2" color="text.secondary">
              Zaten hesabınız var mı?{' '}
              <Link href="/login" sx={{ fontWeight: 600 }}>
                Giriş Yap
              </Link>
            </Typography>
          </Box>
        </CardContent>
      </Card>
    </Container>
  );
};

export default RegisterPage; 