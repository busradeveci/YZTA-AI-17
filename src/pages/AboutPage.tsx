import React from 'react';
import {
  Container,
  Typography,
  Paper,
  Box,
  Card,
  CardContent,
  List,
  ListItem,
  ListItemIcon,
  ListItemText
} from '@mui/material';
import {
  HealthAndSafety,
  Psychology,
  Science,
  Security,
  Speed,
  Verified,
  FiberManualRecord
} from '@mui/icons-material';

const AboutPage: React.FC = () => {
  const features = [
    {
      icon: <HealthAndSafety sx={{ color: '#1B69DE', fontSize: 40 }} />,
      title: 'Sağlık Odaklı',
      description: 'Uzman doktorlar tarafından onaylanmış sağlık tarama algoritmaları'
    },
    {
      icon: <Science sx={{ color: '#0ED1B1', fontSize: 40 }} />,
      title: 'Yapay Zeka Destekli',
      description: 'Gelişmiş makine öğrenmesi modelleri ile hassas risk analizi'
    },
    {
      icon: <Speed sx={{ color: '#F9A825', fontSize: 40 }} />,
      title: 'Hızlı Sonuç',
      description: 'Saniyeler içinde detaylı sağlık risk değerlendirmesi'
    },
    {
      icon: <Security sx={{ color: '#4787E6', fontSize: 40 }} />,
      title: 'Güvenli',
      description: 'Kişisel verileriniz güvenle korunur, şifreli iletişim'
    },
    {
      icon: <Psychology sx={{ color: '#1B69DE', fontSize: 40 }} />,
      title: 'Kişiselleştirilmiş',
      description: 'Yaş, cinsiyet ve sağlık geçmişinize özel analiz'
    },
    {
      icon: <Verified sx={{ color: '#0ED1B1', fontSize: 40 }} />,
      title: 'Doğrulanmış',
      description: 'Bilimsel araştırmalara dayalı güvenilir sonuçlar'
    }
  ];

  const datasets = [
    {
      name: 'Fetal Health Classification',
      source: 'Mendeley Data',
      description: 'Hamilelik sırasında fetal sağlık durumunu değerlendiren kapsamlı veri seti'
    },
    {
      name: 'Breast Cancer Dataset',
      source: 'Kaggle',
      description: 'Meme kanseri risk faktörlerini analiz eden detaylı veri seti'
    },
    {
      name: 'Student Depression Dataset',
      source: 'Kaggle',
      description: 'Öğrenci depresyon risk faktörlerini inceleyen araştırma verisi'
    }
  ];

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
          Sağlık Tarama Merkezi Hakkında
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
          Yapay zeka teknolojisi ile sağlığınızı koruyun
        </Typography>
        <Typography
          variant="body1"
          sx={{
            opacity: 0.8,
            maxWidth: 800,
            mx: 'auto',
            fontFamily: 'Inter, Arial, sans-serif',
            color: '#0F3978',
          }}
        >
          Modern tıp ve yapay zeka teknolojilerini birleştirerek, kullanıcılarımıza güvenilir ve hızlı sağlık risk analizi sunuyoruz.
        </Typography>
      </Paper>

      {/* Features */}
      <Paper
        elevation={2}
        sx={{
          p: 4,
          mb: 6,
          background: '#F8FBFF',
          border: '1.5px solid #E0E7EF',
          boxShadow: '0 4px 24px 0 rgba(30, 89, 174, 0.10)',
          borderRadius: 4,
        }}
      >
        <Typography variant="h4" gutterBottom sx={{ fontWeight: 700, textAlign: 'center', mb: 4, color: '#0F3978', fontFamily: 'Manrope, Arial, sans-serif' }}>
          Özelliklerimiz
        </Typography>
        <Box sx={{
          display: 'grid',
          gridTemplateColumns: { xs: '1fr', md: 'repeat(2, 1fr)', lg: 'repeat(3, 1fr)' },
          gap: 4
        }}>
          {features.map((feature, index) => (
            <Card
              elevation={2}
              key={index}
              sx={{
                height: '100%',
                p: 2,
                background: '#FFFFFF',
                border: '1.5px solid #E0E7EF',
                boxShadow: '0 2px 12px 0 rgba(30, 89, 174, 0.07)',
                borderRadius: 4,
                textAlign: 'center'
              }}
            >
              <CardContent>
                <Box sx={{ mb: 2, display: 'flex', justifyContent: 'center' }}>
                  {feature.icon}
                </Box>
                <Typography variant="h6" gutterBottom sx={{ fontWeight: 600, color: '#0F3978', fontFamily: 'Manrope, Arial, sans-serif' }}>
                  {feature.title}
                </Typography>
                <Typography variant="body2" sx={{ color: '#4787E6', fontFamily: 'Inter, Arial, sans-serif' }}>
                  {feature.description}
                </Typography>
              </CardContent>
            </Card>
          ))}
        </Box>
      </Paper>

      {/* Mission & Vision */}
      <Paper
        elevation={2}
        sx={{
          p: 4,
          mb: 6,
          background: '#F8FBFF',
          border: '1.5px solid #E0E7EF',
          boxShadow: '0 4px 24px 0 rgba(30, 89, 174, 0.10)',
          borderRadius: 4,
        }}
      >
        <Typography variant="h4" gutterBottom sx={{ fontWeight: 700, textAlign: 'center', mb: 4, color: '#0F3978', fontFamily: 'Manrope, Arial, sans-serif' }}>
          Misyonumuz ve Vizyonumuz
        </Typography>
        <Box sx={{
          display: 'grid',
          gridTemplateColumns: { xs: '1fr', md: 'repeat(2, 1fr)' },
          gap: 4
        }}>
          <Box>
            <Typography variant="h5" gutterBottom sx={{ fontWeight: 600, color: '#1B69DE', fontFamily: 'Manrope, Arial, sans-serif' }}>
              Misyonumuz
            </Typography>
            <Typography variant="body1" paragraph sx={{ color: '#0F3978', fontFamily: 'Inter, Arial, sans-serif' }}>
              Herkesin kolayca erişebileceği, güvenilir ve bilimsel temelli sağlık risk analizi hizmeti sunarak, erken teşhis ve koruyucu sağlık hizmetlerine katkıda bulunmak.
            </Typography>
            <List>
              <ListItem>
                <ListItemIcon sx={{ minWidth: 28 }}>
                  <FiberManualRecord sx={{ fontSize: 10, color: '#1B69DE' }} />
                </ListItemIcon>
                <ListItemText primary="Sağlık okuryazarlığını artırmak" />
              </ListItem>
              <ListItem>
                <ListItemIcon sx={{ minWidth: 28 }}>
                  <FiberManualRecord sx={{ fontSize: 10, color: '#1B69DE' }} />
                </ListItemIcon>
                <ListItemText primary="Erken teşhis imkanları sağlamak" />
              </ListItem>
              <ListItem>
                <ListItemIcon sx={{ minWidth: 28 }}>
                  <FiberManualRecord sx={{ fontSize: 10, color: '#1B69DE' }} />
                </ListItemIcon>
                <ListItemText primary="Koruyucu sağlık hizmetlerini desteklemek" />
              </ListItem>
            </List>
          </Box>
          <Box>
            <Typography variant="h5" gutterBottom sx={{ fontWeight: 600, color: '#1B69DE', fontFamily: 'Manrope, Arial, sans-serif' }}>
              Vizyonumuz
            </Typography>
            <Typography variant="body1" paragraph sx={{ color: '#0F3978', fontFamily: 'Inter, Arial, sans-serif' }}>
              Yapay zeka teknolojilerini kullanarak, kişiselleştirilmiş sağlık hizmetlerinde öncü olmak ve global sağlık standartlarını yükseltmek.
            </Typography>
            <List>
              <ListItem>
                <ListItemIcon sx={{ minWidth: 28 }}>
                  <FiberManualRecord sx={{ fontSize: 10, color: '#1B69DE' }} />
                </ListItemIcon>
                <ListItemText primary="Yapay zeka ile sağlık teknolojilerinde liderlik" />
              </ListItem>
              <ListItem>
                <ListItemIcon sx={{ minWidth: 28 }}>
                  <FiberManualRecord sx={{ fontSize: 10, color: '#1B69DE' }} />
                </ListItemIcon>
                <ListItemText primary="Global sağlık erişimini kolaylaştırmak" />
              </ListItem>
              <ListItem>
                <ListItemIcon sx={{ minWidth: 28 }}>
                  <FiberManualRecord sx={{ fontSize: 10, color: '#1B69DE' }} />
                </ListItemIcon>
                <ListItemText primary="Sürekli yenilik ve gelişim" />
              </ListItem>
            </List>
          </Box>
        </Box>
      </Paper>

      {/* Data Sources */}
      <Paper
        elevation={2}
        sx={{
          p: 4,
          mb: 6,
          background: '#F8FBFF',
          border: '1.5px solid #E0E7EF',
          boxShadow: '0 4px 24px 0 rgba(30, 89, 174, 0.10)',
          borderRadius: 4,
        }}
      >
        <Typography variant="h4" gutterBottom sx={{ fontWeight: 700, textAlign: 'center', mb: 4, color: '#0F3978', fontFamily: 'Manrope, Arial, sans-serif' }}>
          Veri Kaynaklarımız
        </Typography>
        <Typography variant="body1" paragraph sx={{ textAlign: 'center', mb: 4, color: '#0F3978', fontFamily: 'Inter, Arial, sans-serif' }}>
          Algoritmalarımız, güvenilir ve bilimsel araştırmalara dayalı veri setleri kullanılarak geliştirilmiştir.
        </Typography>
        <Box sx={{
          display: 'grid',
          gridTemplateColumns: { xs: '1fr', md: 'repeat(3, 1fr)' },
          gap: 3
        }}>
          {datasets.map((dataset, index) => (
            <Card
              elevation={2}
              key={index}
              sx={{
                height: '100%',
                background: '#FFFFFF',
                border: '1.5px solid #E0E7EF',
                boxShadow: '0 2px 12px 0 rgba(30, 89, 174, 0.07)',
                borderRadius: 4,
              }}
            >
              <CardContent>
                <Typography variant="h6" gutterBottom sx={{ fontWeight: 600, color: '#1B69DE', fontFamily: 'Manrope, Arial, sans-serif' }}>
                  {dataset.name}
                </Typography>
                <Typography variant="body2" sx={{ color: '#4787E6', fontFamily: 'Inter, Arial, sans-serif', mb: 1 }}>
                  <strong>Kaynak:</strong> {dataset.source}
                </Typography>
                <Typography variant="body2" sx={{ color: '#0F3978', fontFamily: 'Inter, Arial, sans-serif' }}>
                  {dataset.description}
                </Typography>
              </CardContent>
            </Card>
          ))}
        </Box>
      </Paper>

      {/* Disclaimer */}
      <Paper
        elevation={2}
        sx={{
          p: 4,
          background: '#F8FBFF',
          border: '1.5px solid #E0E7EF',
          boxShadow: '0 4px 24px 0 rgba(30, 89, 174, 0.10)',
          borderRadius: 4,
        }}
      >
        <Typography variant="h6" gutterBottom sx={{ fontWeight: 600, color: '#F9A825', fontFamily: 'Manrope, Arial, sans-serif' }}>
          Önemli Uyarı
        </Typography>
        <Typography variant="body2" paragraph sx={{ color: '#0F3978', fontFamily: 'Inter, Arial, sans-serif' }}>
          Bu uygulama sadece bilgilendirme amaçlıdır ve tıbbi teşhis yerine geçmez.
          Sonuçlar profesyonel tıbbi değerlendirme gerektirir. Yüksek risk skoru alırsanız,
          mutlaka bir sağlık uzmanına başvurunuz.
        </Typography>
        <Typography variant="body2" sx={{ color: '#4787E6', fontFamily: 'Inter, Arial, sans-serif' }}>
          <strong>Geliştirici:</strong> YZTA Web App Team | <strong>Versiyon:</strong> 1.0.0 | <strong>Son Güncelleme:</strong> 2024
        </Typography>
      </Paper>
    </Container>
  );
};

export default AboutPage;