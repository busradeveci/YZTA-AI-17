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
import loginIcon from '../images/login.png';

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
    <Container
      maxWidth={false}
      disableGutters
      sx={{
        width: '100vw',
        minHeight: '100vh',
        backgroundColor: '#E8F4FD',
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        fontFamily: 'Inter, Arial, sans-serif',
        fontSize: '12px',
        py: { xs: 6, md: 8 },
      }}
    >
      {/* Logo ve MediRisk Yazısı Sola Alındı */}
      <Box
        sx={{
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'flex-start',
          width: { xs: '100%', sm: 480, md: 560, lg: 640 },
          maxWidth: '98vw',
          mt: 0, // üst boşluk tamamen kaldırıldı
          mb: 1, // alt boşluk da azaltıldı
          ml: { xs: 0, sm: 2, md: 4 },
          userSelect: 'none',
        }}
      >
        <Box
          sx={{
            width: 145,
            height: 145,
            mr: 1,
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
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
        <Box>
          <Typography
            variant="h2"
            component="h1"
            sx={{
              fontFamily: 'Manrope, Arial, sans-serif',
              fontWeight: 700,
              color: '#0F3978',
              fontSize: '2.4rem',
              letterSpacing: '-0.5px',
              mb: 0.5,
              whiteSpace: 'nowrap',
              lineHeight: 1.1,
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
              fontSize: '0.95rem',
              mt: '-2px',
            }}
          >
            Geleceğin Sağlığı, Bugünün Analizi
          </Typography>
        </Box>
      </Box>

      {/* Kayıt Kartı Ortada ve Yana Geniş */}
      <Box
        sx={{
          margin: 'auto',
          width: { xs: '100%', sm: 480, md: 560, lg: 640 },
          maxWidth: '98vw',
          px: { xs: 1, sm: 3, md: 0 },
          pt: { xs: 1, md: 2 }, // üst padding azaltıldı
          pb: { xs: 2, md: 3 }, // alt padding azaltıldı
          display: 'flex',
          flexDirection: 'column',
          justifyContent: 'center',
          alignItems: 'center',
        }}
      >
        <Card
          elevation={16}
          sx={{
            borderRadius: 4,
            px: { xs: 2, sm: 5, md: 8 },
            py: { xs: 4, sm: 5, md: 6 },
            background: '#fff',
            boxShadow: '0 12px 40px 0 rgba(14,209,177,0.13)',
            width: '100%',
            maxWidth: { xs: 480, sm: 560, md: 640 },
            transition: 'box-shadow 0.3s, transform 0.3s',
            '&:hover': {
              boxShadow: '0 16px 50px 0 rgba(14,209,177,0.20)',
              transform: 'translateY(-4px)',
            },
            display: 'flex',
            flexDirection: 'column',
            justifyContent: 'center',
            alignItems: 'center',
          }}
        >
          <CardContent sx={{ p: 0, width: '100%' }}>
            <Typography
              variant="h5"
              gutterBottom
              sx={{
                fontFamily: 'Manrope, Arial, sans-serif',
                fontWeight: 650,
                textAlign: 'left',
                mb: 4,
                color: '#0F3978',
                fontSize: '2.2rem',
                userSelect: 'none',
                letterSpacing: '-0.5px',
              }}
            >
              Hasta Kaydı
            </Typography>
            {error && (
              <Alert
                severity="error"
                sx={{
                  mb: 2,
                  fontSize: '12px',
                  borderRadius: 2,
                  background: '#FFEAEA',
                  color: '#D32F2F',
                }}
              >
                {error}
              </Alert>
            )}
            {success && (
              <Alert
                severity="success"
                sx={{
                  mb: 2,
                  fontSize: '12px',
                  borderRadius: 2,
                  background: '#EAF3FA',
                  color: '#2CB67D',
                }}
              >
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
                sx={{
                  mb: 2,
                  fontSize: '12px',
                  fontFamily: 'Inter, Arial, sans-serif',
                  '& .MuiInputBase-root': {
                    borderRadius: 3,
                    background: '#F8FBFF',
                    fontSize: '12px',
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
                label="E-posta Adresi"
                name="email"
                type="email"
                value={formData.email}
                onChange={handleInputChange}
                margin="normal"
                required
                sx={{
                  mb: 2,
                  fontSize: '12px',
                  fontFamily: 'Inter, Arial, sans-serif',
                  '& .MuiInputBase-root': {
                    borderRadius: 3,
                    background: '#F8FBFF',
                    fontSize: '12px',
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
                  mb: 2,
                  fontSize: '12px',
                  fontFamily: 'Inter, Arial, sans-serif',
                  '& .MuiInputBase-root': {
                    borderRadius: 3,
                    background: '#F8FBFF',
                    fontSize: '12px',
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
                label="Şifre (Tekrar)"
                name="confirmPassword"
                type="password"
                value={formData.confirmPassword}
                onChange={handleInputChange}
                margin="normal"
                required
                sx={{
                  mb: 2,
                  fontSize: '12px',
                  fontFamily: 'Inter, Arial, sans-serif',
                  '& .MuiInputBase-root': {
                    borderRadius: 3,
                    background: '#F8FBFF',
                    fontSize: '12px',
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
                label="Yaş"
                name="age"
                type="number"
                value={formData.age}
                onChange={handleInputChange}
                margin="normal"
                required
                sx={{
                  mb: 2,
                  fontSize: '12px',
                  fontFamily: 'Inter, Arial, sans-serif',
                  '& .MuiInputBase-root': {
                    borderRadius: 3,
                    background: '#F8FBFF',
                    fontSize: '12px',
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
              <FormControl fullWidth required sx={{ mb: 2 }}>
                <InputLabel
                  sx={{
                    fontFamily: 'Inter, Arial, sans-serif',
                    fontSize: '13px', // 13px olarak güncellendi
                  }}
                >
                  Cinsiyet
                </InputLabel>
                <Select
                  name="gender"
                  value={formData.gender}
                  label="Cinsiyet"
                  onChange={handleSelectChange}
                  sx={{
                    fontFamily: 'Inter, Arial, sans-serif',
                    fontSize: '13px', // 13px olarak güncellendi
                    borderRadius: 3,
                    background: '#F8FBFF',
                    '& .MuiOutlinedInput-notchedOutline': {
                      borderColor: '#E0E7EF',
                    },
                    '&.Mui-focused .MuiOutlinedInput-notchedOutline': {
                      borderColor: '#0ED1B1',
                    },
                  }}
                  MenuProps={{
                    PaperProps: {
                      sx: {
                        fontFamily: 'Inter, Arial, sans-serif',
                        fontSize: '13px', // Açılır menüde de 13px
                      }
                    }
                  }}
                >
                  <MenuItem
                    value="Erkek"
                    sx={{
                      fontFamily: 'Inter, Arial, sans-serif',
                      fontSize: '13px', // 13px olarak güncellendi
                    }}
                  >
                    Erkek
                  </MenuItem>
                  <MenuItem
                    value="Kadın"
                    sx={{
                      fontFamily: 'Inter, Arial, sans-serif',
                      fontSize: '13px', // 13px olarak güncellendi
                    }}
                  >
                    Kadın
                  </MenuItem>
                </Select>
              </FormControl>
              <TextField
                fullWidth
                label="Telefon (opsiyonel)"
                name="phone"
                value={formData.phone}
                onChange={handleInputChange}
                margin="normal"
                sx={{
                  mb: 2,
                  fontSize: '12px',
                  fontFamily: 'Inter, Arial, sans-serif',
                  '& .MuiInputBase-root': {
                    borderRadius: 3,
                    background: '#F8FBFF',
                    fontSize: '12px',
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
                startIcon={<PersonAdd />}
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
                Kayıt Ol
              </Button>
            </Box>
            <Box sx={{ textAlign: 'center', mt: 2 }}>
              <Typography
                variant="body2"
                color="text.secondary"
                sx={{
                  fontFamily: 'Inter, Arial, sans-serif',
                  fontSize: '12px',
                  userSelect: 'none',
                }}
              >
                Zaten hesabınız var mı?{' '}
                <Link
                  href="/login"
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
                  Giriş Yap
                </Link>
              </Typography>
            </Box>
          </CardContent>
        </Card>
      </Box>
    </Container>
  );
};

export default RegisterPage;