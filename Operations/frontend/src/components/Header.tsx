import { useState } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import './Header.css';
import { 
  Group, 
  Title, 
  Menu, 
  Text,
  Divider,
  Box,
  Container,
  Burger,
  Drawer,
  UnstyledButton,
  Stack
} from '@mantine/core';
import { useAuth } from '../contexts/AuthContext';
import { useTheme } from '../contexts/ThemeContext';
import type { ColorPalette } from '../contexts/ThemeContext';

export function Header() {
  const { isAuthenticated, user, logout } = useAuth();
  const { currentPalette, setPalette, availablePalettes } = useTheme();
  const navigate = useNavigate();
  const location = useLocation();
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  // Define navigation structure with dropdowns
  const navStructure = [
    { 
      label: 'Home', 
      path: '/',
      exact: true
    },
    { 
      label: 'Operations', 
      items: [
        { label: 'Dashboard', path: '/dashboard' },
        { label: 'Quotes', path: '/quotes' },
        { label: 'Trips', path: '/trips' },
        { label: 'Patients', path: '/patients' }
      ] 
    },
    { 
      label: 'Admin', 
      items: [
        { label: 'Users', path: '/admin/users' },
        { label: 'Settings', path: '/admin/settings' },
        { label: 'Reports', path: '/admin/reports' }
      ] 
    },
    { 
      label: 'Maintenance', 
      items: [
        { label: 'Aircraft', path: '/maintenance/aircraft' },
        { label: 'Equipment', path: '/maintenance/equipment' },
        { label: 'Schedules', path: '/maintenance/schedules' }
      ] 
    },
    { 
      label: 'Self', 
      items: [
        { label: 'Profile', path: '/profile' },
        { label: 'Preferences', path: '/preferences' },
        { label: 'Tasks', path: '/tasks' }
      ] 
    }
  ];

  const isActive = (path: string, exact = false) => {
    if (exact) {
      return location.pathname === path;
    }
    return location.pathname.startsWith(path);
  };

  const isMenuActive = (items: Array<{path: string}>) => {
    return items.some(item => location.pathname === item.path);
  };

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  const ColorPaletteItem = ({ palette, onClick }: { palette: ColorPalette, onClick: () => void }) => (
    <UnstyledButton 
      onClick={onClick}
      style={{
        display: 'flex',
        alignItems: 'center',
        width: '100%',
        padding: '8px 12px',
        borderRadius: '4px',
      }}
    >
      <Group>
        <Box 
          style={{ 
            width: 20, 
            height: 20, 
            borderRadius: '50%', 
            backgroundColor: palette.colors.accentPrimary,
            border: currentPalette.id === palette.id ? '2px solid var(--text-primary)' : 'none'
          }} 
        />
        <Text>{palette.name}</Text>
      </Group>
    </UnstyledButton>
  );

  // Get display name for user
  const getUserDisplayName = () => {
    if (!user) return '';
    if (user.first_name && user.last_name) {
      return `${user.first_name} ${user.last_name}`;
    }
    return user.username;
  };

  // Get user initials for avatar
  const getUserInitials = () => {
    if (!user) return '';
    if (user.first_name) {
      return user.first_name.charAt(0).toUpperCase();
    }
    return user.username.charAt(0).toUpperCase();
  };

  return (
    <Box
      component="header"
      style={{
        height: '60px',
        width: '100%',
        borderBottom: '1px solid var(--border-color)',
        backgroundColor: 'var(--bg-primary)',
        boxShadow: '0 1px 3px rgba(0,0,0,0.05)'
      }}
    >
      <Container size="xl" h="100%">
        <Group justify="space-between" h="100%">
          <Title order={4} className="logo">JET ICU</Title>
          
          <div className="nav-links">
            {isAuthenticated && navStructure.map((item) => (
              item.items ? (
                <Menu key={item.label} trigger="hover" openDelay={100} closeDelay={400}>
                  <Menu.Target>
                    <UnstyledButton
                      className="nav-link"
                      style={{
                        color: isMenuActive(item.items) ? 'var(--accent-primary)' : 'var(--text-primary)',
                        borderBottom: isMenuActive(item.items) ? '2px solid var(--accent-primary)' : '2px solid transparent'
                      }}
                    >
                      {item.label}
                    </UnstyledButton>
                  </Menu.Target>
                  <Menu.Dropdown>
                    {item.items.map((subItem) => (
                      <Menu.Item
                        key={subItem.path}
                        onClick={() => navigate(subItem.path)}
                        style={{
                          backgroundColor: isActive(subItem.path) ? 'var(--bg-secondary)' : undefined,
                          color: isActive(subItem.path) ? 'var(--accent-primary)' : undefined
                        }}
                      >
                        {subItem.label}
                      </Menu.Item>
                    ))}
                  </Menu.Dropdown>
                </Menu>
              ) : (
                <UnstyledButton
                  key={item.path}
                  className="nav-link"
                  style={{
                    color: isActive(item.path, item.exact) ? 'var(--accent-primary)' : 'var(--text-primary)',
                    borderBottom: isActive(item.path, item.exact) ? '2px solid var(--accent-primary)' : '2px solid transparent'
                  }}
                  onClick={() => navigate(item.path)}
                >
                  {item.label}
                </UnstyledButton>
              )
            ))}
          </div>

          <Group>
            {isAuthenticated && (
              <Menu position="bottom-end">
                <Menu.Target>
                  <UnstyledButton className="user-button">
                    <Group gap="xs">
                      <Box
                        style={{
                          width: '36px',
                          height: '36px',
                          borderRadius: '50%',
                          backgroundColor: 'var(--accent-primary)',
                          color: 'var(--button-text)',
                          display: 'flex',
                          alignItems: 'center',
                          justifyContent: 'center',
                          fontWeight: 'bold',
                          fontSize: '18px'
                        }}
                      >
                        {getUserInitials()}
                      </Box>
                      <Text fw={500} visibleFrom="sm" size="sm">{getUserDisplayName()}</Text>
                    </Group>
                  </UnstyledButton>
                </Menu.Target>

                <Menu.Dropdown>
                  <Menu.Label>Profile</Menu.Label>
                  <Menu.Item onClick={() => navigate('/profile')}>Account Settings</Menu.Item>
                  <Menu.Item onClick={() => navigate('/preferences')}>Preferences</Menu.Item>
                  
                  <Menu.Divider />
                  
                  <Menu.Label>Theme</Menu.Label>
                  {availablePalettes.map((palette) => (
                    <Menu.Item key={palette.id} p={0}>
                      <ColorPaletteItem 
                        palette={palette} 
                        onClick={() => setPalette(palette.id)} 
                      />
                    </Menu.Item>
                  ))}
                  
                  <Menu.Divider />
                  
                  <Menu.Item color="red" onClick={handleLogout}>Logout</Menu.Item>
                </Menu.Dropdown>
              </Menu>
            )}

            {!isAuthenticated && (
              <UnstyledButton
                onClick={() => navigate('/login')}
                style={{
                  backgroundColor: 'var(--accent-primary)',
                  color: 'var(--button-text)',
                  padding: '8px 16px',
                  borderRadius: '4px',
                  fontWeight: 500
                }}
              >
                Login
              </UnstyledButton>
            )}

            {/* Mobile Menu Button */}
            <Burger
              opened={mobileMenuOpen}
              onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
              hiddenFrom="sm"
              size="sm"
            />
          </Group>
        </Group>
      </Container>

      {/* Mobile Navigation Drawer */}
      <Drawer
        opened={mobileMenuOpen}
        onClose={() => setMobileMenuOpen(false)}
        title="Menu"
        padding="xl"
        size="xs"
      >
        <Stack>
          {isAuthenticated && (
            <>
              <Group mb="md">
                <Box
                  style={{
                    width: 40,
                    height: 40,
                    borderRadius: '50%',
                    backgroundColor: 'var(--accent-primary)',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    color: 'var(--bg-primary)',
                    fontWeight: 'bold',
                    fontSize: '18px'
                  }}
                >
                  {getUserInitials()}
                </Box>
                <Box>
                  <Text fw={700}>{getUserDisplayName()}</Text>
                  <Text size="xs" c="var(--text-secondary)">{user?.username}</Text>
                </Box>
              </Group>

              <Divider mb="md" />

              {navStructure.map((category) => (
                <div key={category.label}>
                  {category.items ? (
                    <>
                      <Text fw={700} mb="xs">{category.label}</Text>
                      <Stack gap="xs" mb="md">
                        {category.items.map((item) => (
                          <UnstyledButton
                            key={item.path}
                            onClick={() => {
                              navigate(item.path);
                              setMobileMenuOpen(false);
                            }}
                            className="mobile-nav-link"
                            style={{
                              color: isActive(item.path) ? 'var(--accent-primary)' : 'var(--text-primary)',
                              padding: '8px 12px',
                              borderRadius: '4px',
                              backgroundColor: isActive(item.path) ? 'var(--bg-secondary)' : 'transparent'
                            }}
                          >
                            {item.label}
                          </UnstyledButton>
                        ))}
                      </Stack>
                    </>
                  ) : (
                    <UnstyledButton
                      key={category.path}
                      onClick={() => {
                        navigate(category.path);
                        setMobileMenuOpen(false);
                      }}
                      className="mobile-nav-link"
                      style={{
                        color: isActive(category.path, category.exact) ? 'var(--accent-primary)' : 'var(--text-primary)',
                        padding: '8px 12px',
                        borderRadius: '4px',
                        backgroundColor: isActive(category.path, category.exact) ? 'var(--bg-secondary)' : 'transparent',
                        marginBottom: '12px'
                      }}
                    >
                      {category.label}
                    </UnstyledButton>
                  )}
                </div>
              ))}

              <Divider my="md" label="Theme" labelPosition="center" />

              <Stack gap="xs">
                {availablePalettes.map((palette) => (
                  <ColorPaletteItem 
                    key={palette.id}
                    palette={palette} 
                    onClick={() => setPalette(palette.id)} 
                  />
                ))}
              </Stack>

              <Divider my="md" />

              <UnstyledButton 
                onClick={handleLogout}
                style={{
                  color: 'var(--error)',
                  padding: '8px 12px',
                  borderRadius: '4px',
                  width: '100%',
                  textAlign: 'center',
                  fontWeight: 500
                }}
              >
                Logout
              </UnstyledButton>
            </>
          )}

          {!isAuthenticated && (
            <UnstyledButton
              onClick={() => {
                navigate('/login');
                setMobileMenuOpen(false);
              }}
              style={{
                backgroundColor: 'var(--accent-primary)',
                color: 'var(--button-text)',
                padding: '10px 16px',
                borderRadius: '4px',
                width: '100%',
                textAlign: 'center',
                fontWeight: 500
              }}
            >
              Login
            </UnstyledButton>
          )}
        </Stack>
      </Drawer>
    </Box>
  );
}
