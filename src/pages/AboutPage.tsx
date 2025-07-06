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
  Verified
} from '@mui/icons-material';

const AboutPage: React.FC = () => {
  const features = [
    {
      icon: <HealthAndSafety color="primary" />,
      title: 'Sağlık Odaklı',
      description: 'Uzman doktorlar tarafından onaylanmış sağlık tarama algoritmaları'
    },
    {
      icon: <Science color="primary" />,
      title: 'Yapay Zeka Destekli',
      description: 'Gelişmiş makine öğrenmesi modelleri ile hassas risk analizi'
    },
    {
      icon: <Speed color="primary" />,
      title: 'Hızlı Sonuç',
      description: 'Saniyeler içinde detaylı sağlık risk değerlendirmesi'
    },
    {
      icon: <Security color="primary" />,
      title: 'Güvenli',
      description: 'Kişisel verileriniz güvenle korunur, şifreli iletişim'
    },
    {
      icon: <Psychology color="primary" />,
      title: 'Kişiselleştirilmiş',
      description: 'Yaş, cinsiyet ve sağlık geçmişinize özel analiz'
    },
    {
      icon: <Verified color="primary" />,
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
          🏥 Sağlık Tarama Merkezi Hakkında
        </Typography>
        <Typography variant="h6" sx={{ opacity: 0.9, mb: 3 }}>
          Yapay zeka teknolojisi ile sağlığınızı koruyun
        </Typography>
        <Typography variant="body1" sx={{ opacity: 0.8, maxWidth: 800, mx: 'auto' }}>
          Modern tıp ve yapay zeka teknolojilerini birleştirerek, 
          kullanıcılarımıza güvenilir ve hızlı sağlık risk analizi sunuyoruz.
        </Typography>
      </Paper>

      {/* Features */}
      <Paper elevation={3} sx={{ p: 4, mb: 6 }}>
        <Typography variant="h4" gutterBottom sx={{ fontWeight: 700, textAlign: 'center', mb: 4 }}>
          Özelliklerimiz
        </Typography>
        <Box sx={{ 
          display: 'grid', 
          gridTemplateColumns: { xs: '1fr', md: 'repeat(2, 1fr)', lg: 'repeat(3, 1fr)' }, 
          gap: 4 
        }}>
          {features.map((feature, index) => (
            <Card elevation={2} key={index} sx={{ height: '100%', p: 2 }}>
              <CardContent sx={{ textAlign: 'center' }}>
                <Box sx={{ fontSize: '3rem', mb: 2 }}>
                  {feature.icon}
                </Box>
                <Typography variant="h6" gutterBottom sx={{ fontWeight: 600 }}>
                  {feature.title}
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  {feature.description}
                </Typography>
              </CardContent>
            </Card>
          ))}
        </Box>
      </Paper>

      {/* Mission & Vision */}
      <Paper elevation={3} sx={{ p: 4, mb: 6 }}>
        <Typography variant="h4" gutterBottom sx={{ fontWeight: 700, textAlign: 'center', mb: 4 }}>
          Misyonumuz ve Vizyonumuz
        </Typography>
        <Box sx={{ 
          display: 'grid', 
          gridTemplateColumns: { xs: '1fr', md: 'repeat(2, 1fr)' }, 
          gap: 4 
        }}>
          <Box>
            <Typography variant="h5" gutterBottom sx={{ fontWeight: 600, color: 'primary.main' }}>
              🎯 Misyonumuz
            </Typography>
            <Typography variant="body1" paragraph>
              Herkesin kolayca erişebileceği, güvenilir ve bilimsel temelli sağlık risk analizi 
              hizmeti sunarak, erken teşhis ve koruyucu sağlık hizmetlerine katkıda bulunmak.
            </Typography>
            <List>
              <ListItem>
                <ListItemIcon>•</ListItemIcon>
                <ListItemText primary="Sağlık okuryazarlığını artırmak" />
              </ListItem>
              <ListItem>
                <ListItemIcon>•</ListItemIcon>
                <ListItemText primary="Erken teşhis imkanları sağlamak" />
              </ListItem>
              <ListItem>
                <ListItemIcon>•</ListItemIcon>
                <ListItemText primary="Koruyucu sağlık hizmetlerini desteklemek" />
              </ListItem>
            </List>
          </Box>
          <Box>
            <Typography variant="h5" gutterBottom sx={{ fontWeight: 600, color: 'primary.main' }}>
              🔮 Vizyonumuz
            </Typography>
            <Typography variant="body1" paragraph>
              Yapay zeka teknolojilerini kullanarak, kişiselleştirilmiş sağlık hizmetlerinde 
              öncü olmak ve global sağlık standartlarını yükseltmek.
            </Typography>
            <List>
              <ListItem>
                <ListItemIcon>•</ListItemIcon>
                <ListItemText primary="Yapay zeka ile sağlık teknolojilerinde liderlik" />
              </ListItem>
              <ListItem>
                <ListItemIcon>•</ListItemIcon>
                <ListItemText primary="Global sağlık erişimini kolaylaştırmak" />
              </ListItem>
              <ListItem>
                <ListItemIcon>•</ListItemIcon>
                <ListItemText primary="Sürekli yenilik ve gelişim" />
              </ListItem>
            </List>
          </Box>
        </Box>
      </Paper>

      {/* Data Sources */}
      <Paper elevation={3} sx={{ p: 4, mb: 6 }}>
        <Typography variant="h4" gutterBottom sx={{ fontWeight: 700, textAlign: 'center', mb: 4 }}>
          Veri Kaynaklarımız
        </Typography>
        <Typography variant="body1" paragraph sx={{ textAlign: 'center', mb: 4 }}>
          Algoritmalarımız, güvenilir ve bilimsel araştırmalara dayalı veri setleri kullanılarak geliştirilmiştir.
        </Typography>
        <Box sx={{ 
          display: 'grid', 
          gridTemplateColumns: { xs: '1fr', md: 'repeat(3, 1fr)' }, 
          gap: 3 
        }}>
          {datasets.map((dataset, index) => (
            <Card elevation={2} key={index} sx={{ height: '100%' }}>
              <CardContent>
                <Typography variant="h6" gutterBottom sx={{ fontWeight: 600, color: 'primary.main' }}>
                  {dataset.name}
                </Typography>
                <Typography variant="body2" color="text.secondary" gutterBottom>
                  <strong>Kaynak:</strong> {dataset.source}
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  {dataset.description}
                </Typography>
              </CardContent>
            </Card>
          ))}
        </Box>
      </Paper>

      {/* Disclaimer */}
      <Paper elevation={2} sx={{ p: 4, bgcolor: 'grey.50' }}>
        <Typography variant="h6" gutterBottom sx={{ fontWeight: 600, color: 'warning.main' }}>
          ⚠️ Önemli Uyarı
        </Typography>
        <Typography variant="body2" paragraph>
          Bu uygulama sadece bilgilendirme amaçlıdır ve tıbbi teşhis yerine geçmez. 
          Sonuçlar profesyonel tıbbi değerlendirme gerektirir. Yüksek risk skoru alırsanız, 
          mutlaka bir sağlık uzmanına başvurunuz.
        </Typography>
        <Typography variant="body2" color="text.secondary">
          <strong>Geliştirici:</strong> YZTA Web App Team | 
          <strong> Versiyon:</strong> 1.0.0 | 
          <strong> Son Güncelleme:</strong> 2024
        </Typography>
      </Paper>
    </Container>
  );
};

export default AboutPage; 