import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { TextInput, PasswordInput, Button, Box, Title, Text, Center, Stack } from '@mantine/core';
import { useAuth } from '../contexts/AuthContext';

export function LoginPage() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const { login } = useAuth();
  const navigate = useNavigate();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      await login(username, password);
      navigate('/dashboard');
    } catch (err) {
      setError('Invalid username or password');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="login-page">
      <Box className="login-container">
        <Center mb="xl">
          <Title order={2} c="var(--text-primary)">JET ICU Operations</Title>
        </Center>
        
        <form onSubmit={handleSubmit}>
          <Stack>
            {error && (
              <Text c="var(--accent-secondary)" fw={500} ta="center">
                {error}
              </Text>
            )}
            
            <TextInput
              label="Username"
              placeholder="Enter your username"
              value={username}
              onChange={(e) => setUsername(e.currentTarget.value)}
              required
            />
            
            <PasswordInput
              label="Password"
              placeholder="Your password"
              value={password}
              onChange={(e) => setPassword(e.currentTarget.value)}
              required
            />
            
            <Button
              type="submit"
              loading={loading}
              fullWidth
              style={{
                backgroundColor: 'var(--button-primary)',
                color: 'var(--button-text)',
              }}
            >
              Log in
            </Button>
          </Stack>
        </form>
      </Box>
    </div>
  );
}
