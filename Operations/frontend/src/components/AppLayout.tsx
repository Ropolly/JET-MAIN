import type { ReactNode } from 'react';
import { AppShell, Container, Paper, Box } from '@mantine/core';
import { Header } from './Header';

interface AppLayoutProps {
  children: ReactNode;
}

export function AppLayout({ children }: AppLayoutProps) {
  return (
    <AppShell
      header={{ height: 60 }}
      padding={0}
    >
      <AppShell.Header>
        <Header />
      </AppShell.Header>

      <AppShell.Main>
        <Box 
          style={{
            backgroundColor: 'var(--bg-secondary)',
            minHeight: 'calc(100vh - 60px)',
            padding: '24px 0'
          }}
        >
          <Container size="xl">
            <Paper 
              shadow="sm" 
              p={0}
              radius="md"
              style={{ 
                backgroundColor: 'var(--bg-primary)',
                overflow: 'hidden'
              }}
            >
              {children}
            </Paper>
          </Container>
        </Box>
      </AppShell.Main>
    </AppShell>
  );
}
