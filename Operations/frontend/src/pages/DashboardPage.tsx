import { Title, Grid, Card, Text, Group, SimpleGrid, Stack, Box, Container, Divider } from '@mantine/core';
import { useAuth } from '../contexts/AuthContext';

export function DashboardPage() {
  const { user } = useAuth();

  return (
    <Box>
      {/* Header Section */}
      <Box 
        style={{ 
          backgroundColor: 'var(--accent-primary)', 
          padding: '24px', 
          color: 'var(--button-text)',
          borderTopLeftRadius: '8px',
          borderTopRightRadius: '8px'
        }}
      >
        <Container size="xl">
          <Title order={2}>Operations Dashboard</Title>
          <Text size="lg" mt="xs">
            Welcome back, {user?.name || 'User'}
          </Text>
        </Container>
      </Box>
      
      {/* Stats Section */}
      <Box style={{ padding: '24px' }}>
        <Container size="xl">
          <SimpleGrid cols={{ base: 1, sm: 2, lg: 4 }} spacing="md">
            <Card withBorder shadow="sm" padding="lg" radius="md">
              <Card.Section withBorder inheritPadding py="xs" bg="var(--bg-secondary)">
                <Text fw={500}>Active Trips</Text>
              </Card.Section>
              <Group justify="space-between" mt="md" mb="xs">
                <Text size="xl" fw={700} c="var(--accent-primary)">12</Text>
              </Group>
            </Card>
            
            <Card withBorder shadow="sm" padding="lg" radius="md">
              <Card.Section withBorder inheritPadding py="xs" bg="var(--bg-secondary)">
                <Text fw={500}>Pending Quotes</Text>
              </Card.Section>
              <Group justify="space-between" mt="md" mb="xs">
                <Text size="xl" fw={700} c="var(--accent-secondary)">8</Text>
              </Group>
            </Card>
            
            <Card withBorder shadow="sm" padding="lg" radius="md">
              <Card.Section withBorder inheritPadding py="xs" bg="var(--bg-secondary)">
                <Text fw={500}>Completed Trips</Text>
              </Card.Section>
              <Group justify="space-between" mt="md" mb="xs">
                <Text size="xl" fw={700} c="var(--text-primary)">145</Text>
              </Group>
            </Card>
            
            <Card withBorder shadow="sm" padding="lg" radius="md">
              <Card.Section withBorder inheritPadding py="xs" bg="var(--bg-secondary)">
                <Text fw={500}>Conversion Rate</Text>
              </Card.Section>
              <Group justify="space-between" mt="md" mb="xs">
                <Text size="xl" fw={700} c="var(--tertiary)">68%</Text>
              </Group>
            </Card>
          </SimpleGrid>
        </Container>
      </Box>
      
      <Divider />
      
      {/* Content Section */}
      <Box style={{ padding: '24px' }}>
        <Container size="xl">
          <Grid gutter="md">
            <Grid.Col span={{ base: 12, md: 8 }}>
              <Card withBorder shadow="sm" padding="lg" radius="md" h="100%">
                <Card.Section withBorder inheritPadding py="xs" bg="var(--bg-secondary)">
                  <Text fw={500}>Recent Activity</Text>
                </Card.Section>
                <Stack gap="xs" mt="md">
                  <Text size="sm">Quote #1089 was approved - 2 hours ago</Text>
                  <Text size="sm">Trip #567 completed successfully - 5 hours ago</Text>
                  <Text size="sm">New quote request from John Doe - 1 day ago</Text>
                  <Text size="sm">Trip #566 scheduled for tomorrow - 1 day ago</Text>
                  <Text size="sm">Quote #1088 was sent to client - 2 days ago</Text>
                </Stack>
              </Card>
            </Grid.Col>
            
            <Grid.Col span={{ base: 12, md: 4 }}>
              <Card withBorder shadow="sm" padding="lg" radius="md" h="100%">
                <Card.Section withBorder inheritPadding py="xs" bg="var(--bg-secondary)">
                  <Text fw={500}>Upcoming Trips</Text>
                </Card.Section>
                <Stack gap="xs" mt="md">
                  <Text size="sm">Trip #567: Miami to Mexico City - May 14</Text>
                  <Text size="sm">Trip #568: London to New York - May 15</Text>
                  <Text size="sm">Trip #569: Dubai to Singapore - May 16</Text>
                  <Text size="sm">Trip #570: Los Angeles to Tokyo - May 18</Text>
                </Stack>
              </Card>
            </Grid.Col>
          </Grid>
        </Container>
      </Box>
    </Box>
  );
}
