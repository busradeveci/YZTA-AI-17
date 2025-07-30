import React, { useState, useEffect } from 'react';
import {
  AppBar,
  Toolbar,
  Typography,
  Button,
  Box,
  Avatar,
  Menu,
  MenuItem,
  IconButton,
  Divider
} from '@mui/material';
import {
  Dashboard,
  History,
  Person,
  Logout,
  Assessment
} from '@mui/icons-material';
import { useNavigate, useLocation } from 'react-router-dom';
import logo from '../images/login.png'; // LOGO EKLENDİ

const Navbar: React.FC = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const [user, setUser] = useState<any>(null);
  const [anchorEl, setAnchorEl] = useState<null | HTMLElement>(null);

  useEffect(() => {
    const userData = localStorage.getItem('user');
    if (userData) {
      setUser(JSON.parse(userData));
    }
  }, []);

  const handleMenuOpen = (event: React.MouseEvent<HTMLElement>) => {
    setAnchorEl(event.currentTarget);
  };

  const handleMenuClose = () => {
    setAnchorEl(null);
  };

  const handleLogout = () => {
    localStorage.removeItem('user');
    navigate('/login');
  };

  const handleNavigation = (path: string) => {
    navigate(path);
    handleMenuClose();
  };

  const isActive = (path: string) => {
    return location.pathname === path;
  };

  if (!user) {
    return null;
  }

  return (
    <AppBar
      position="sticky"
      elevation={2}
      sx={{
        backgroundColor: '#0F3978',
        borderRadius: 0, // Köşeler tamamen düz
        boxShadow: 'none', // İsterseniz gölgeyi de kaldırabilirsiniz
      }}
    >
      <Toolbar sx={{ borderRadius: 0, minHeight: 64 }}>
        {/* Logo ve Başlık */}
        <Box sx={{ display: 'flex', alignItems: 'center', flexGrow: 1 }}>
          <img
            src={logo}
            alt="MediRisk Logo"
            style={{
              width: 40,
              height: 40,
              objectFit: 'contain',
              marginRight: 12,
              userSelect: 'none',
              borderRadius: 0, // Logo da köşesiz
            }}
            draggable={false}
          />
          <Typography
            variant="h6"
            component="div"
            sx={{
              fontWeight: 700,
              mr: 2,
              color: '#fff',
              fontFamily: 'Manrope, Arial, sans-serif',
              letterSpacing: '-0.5px',
              borderRadius: 0, // Başlık da köşesiz
            }}
          >
            MediRisk
          </Typography>

          {/* Navigasyon Menüsü */}
          <Box sx={{ display: { xs: 'none', md: 'flex' }, ml: 4 }}>
            <Button
              color="inherit"
              startIcon={<Dashboard />}
              onClick={() => navigate('/dashboard')}
              sx={{
                mx: 1,
                bgcolor: isActive('/dashboard') ? 'rgba(255,255,255,0.1)' : 'transparent',
                color: '#fff',
                fontWeight: 600,
                fontFamily: 'Inter, Arial, sans-serif',
                borderRadius: 0, // Düz köşe
                '&:hover': {
                  bgcolor: 'rgba(255,255,255,0.1)',
                  borderRadius: 0,
                },
              }}
            >
              Dashboard
            </Button>
            <Button
              color="inherit"
              startIcon={<History />}
              onClick={() => navigate('/history')}
              sx={{
                mx: 1,
                bgcolor: isActive('/history') ? 'rgba(255,255,255,0.1)' : 'transparent',
                color: '#fff',
                fontWeight: 600,
                fontFamily: 'Inter, Arial, sans-serif',
                borderRadius: 0,
                '&:hover': {
                  bgcolor: 'rgba(255,255,255,0.1)',
                  borderRadius: 0,
                },
              }}
            >
              Geçmiş
            </Button>
            <Button
              color="inherit"
              startIcon={<Assessment />}
              onClick={() => navigate('/about')}
              sx={{
                mx: 1,
                bgcolor: isActive('/about') ? 'rgba(255,255,255,0.1)' : 'transparent',
                color: '#fff',
                fontWeight: 600,
                fontFamily: 'Inter, Arial, sans-serif',
                borderRadius: 0,
                '&:hover': {
                  bgcolor: 'rgba(255,255,255,0.1)',
                  borderRadius: 0,
                },
              }}
            >
              Hakkında
            </Button>
          </Box>
        </Box>

        {/* Kullanıcı Menüsü */}
        <Box sx={{ display: 'flex', alignItems: 'center' }}>
          <Typography variant="body2" sx={{ mr: 2, display: { xs: 'none', sm: 'block' }, color: '#fff' }}>
            {user.name}
          </Typography>

          <IconButton
            onClick={handleMenuOpen}
            sx={{ color: 'white', borderRadius: 0 }}
          >
            <Avatar sx={{ width: 32, height: 32, bgcolor: 'rgba(255,255,255,0.2)', borderRadius: 0 }}>
              <Person />
            </Avatar>
          </IconButton>

          <Menu
            anchorEl={anchorEl}
            open={Boolean(anchorEl)}
            onClose={handleMenuClose}
            PaperProps={{
              sx: {
                mt: 1,
                minWidth: 200,
                borderRadius: 0, // Menü de köşesiz
                '& .MuiMenuItem-root': {
                  py: 1.5,
                  px: 2,
                  borderRadius: 0,
                },
              },
            }}
          >
            <MenuItem onClick={handleMenuClose}>
              <Box sx={{ display: 'flex', alignItems: 'center' }}>
                <Avatar sx={{ width: 32, height: 32, mr: 2, bgcolor: 'primary.main', borderRadius: 0 }}>
                  <Person />
                </Avatar>
                <Box>
                  <Typography variant="body2" sx={{ fontWeight: 600 }}>
                    {user.name}
                  </Typography>
                  <Typography variant="caption" color="text.secondary">
                    Hasta
                  </Typography>
                </Box>
              </Box>
            </MenuItem>
            <Divider />
            <MenuItem onClick={() => handleNavigation('/dashboard')}>
              <Dashboard sx={{ mr: 2 }} />
              Dashboard
            </MenuItem>
            <MenuItem onClick={() => handleNavigation('/history')}>
              <History sx={{ mr: 2 }} />
              Test Geçmişi
            </MenuItem>
            <MenuItem onClick={() => handleNavigation('/about')}>
              <Assessment sx={{ mr: 2 }} />
              Hakkında
            </MenuItem>
            <Divider />
            <MenuItem onClick={handleLogout} sx={{ color: 'error.main' }}>
              <Logout sx={{ mr: 2 }} />
              Çıkış Yap
            </MenuItem>
          </Menu>
        </Box>
      </Toolbar>
    </AppBar>
  );
};

export default Navbar;