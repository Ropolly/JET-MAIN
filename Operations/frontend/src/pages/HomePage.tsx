import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { 
  Container, 
  Title, 
  Text, 
  Button, 
  TextInput, 
  Textarea, 
  SimpleGrid, 
  Card, 
  Stack,
  Group,
  Select
} from '@mantine/core';

export function HomePage() {
  const navigate = useNavigate();
  const [formSubmitted, setFormSubmitted] = useState(false);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    setFormSubmitted(true);
    setTimeout(() => setFormSubmitted(false), 3000);
  };

  return (
    <Container size="lg" py="xl">
      <Stack spacing="xl">
        <div style={{ textAlign: 'center', marginBottom: '2rem' }}>
          <Title 
            order={1} 
            c="var(--text-primary)"
            style={{ fontSize: '2.5rem', marginBottom: '1rem' }}
          >
            JET ICU Air Ambulance Services
          </Title>
          <Text size="lg" c="var(--text-secondary)" maw={700} mx="auto">
            Providing worldwide air ambulance and medical transport services with the highest standards of patient care and safety.
          </Text>
          <Group position="center" mt="xl">
            <Button 
              size="lg"
              style={{
                backgroundColor: 'var(--button-primary)',
                color: 'var(--button-text)',
              }}
              onClick={() => navigate('/login')}
            >
              Login to Operations
            </Button>
          </Group>
        </div>

        <SimpleGrid cols={{ base: 1, md: 2 }} spacing="xl">
          <Card withBorder shadow="sm" padding="lg" radius="md">
            <Card.Section withBorder inheritPadding py="xs">
              <Title order={3} c="var(--text-primary)">Request a Quote</Title>
            </Card.Section>
            
            <form onSubmit={handleSubmit}>
              <Stack spacing="md" mt="md">
                <TextInput
                  label="Full Name"
                  placeholder="John Smith"
                  required
                />
                
                <TextInput
                  label="Email"
                  placeholder="your@email.com"
                  required
                />
                
                <TextInput
                  label="Phone"
                  placeholder="+1 (555) 123-4567"
                  required
                />
                
                <SimpleGrid cols={2}>
                  <Select
                    label="Pickup Country"
                    placeholder="Select country"
                    data={[
                      { value: 'us', label: 'United States' },
                      { value: 'ca', label: 'Canada' },
                      { value: 'mx', label: 'Mexico' },
                      { value: 'uk', label: 'United Kingdom' },
                      { value: 'other', label: 'Other' },
                    ]}
                    required
                  />
                  
                  <TextInput
                    label="Pickup City"
                    placeholder="Miami"
                    required
                  />
                </SimpleGrid>
                
                <Textarea
                  label="Additional Information"
                  placeholder="Please provide any additional details about the patient's condition, required medical equipment, etc."
                  minRows={4}
                />
                
                <Button 
                  type="submit"
                  fullWidth
                  style={{
                    backgroundColor: 'var(--button-primary)',
                    color: 'var(--button-text)',
                  }}
                  disabled={formSubmitted}
                >
                  {formSubmitted ? 'Request Submitted!' : 'Submit Quote Request'}
                </Button>
              </Stack>
            </form>
          </Card>
          
          <Stack spacing="lg">
            <Card withBorder shadow="sm" padding="lg" radius="md">
              <Title order={4} c="var(--text-primary)" mb="md">Why Choose JET ICU?</Title>
              <Text>
                JET ICU is a leading provider of global air ambulance services, offering bedside-to-bedside medical transport with a fleet of dedicated aircraft and experienced medical teams.
              </Text>
              <ul style={{ marginTop: '1rem', paddingLeft: '1.5rem' }}>
                <li>24/7 worldwide service</li>
                <li>Dedicated medical flight crews</li>
                <li>State-of-the-art medical equipment</li>
                <li>Dual patient capability</li>
                <li>Insurance assistance</li>
              </ul>
            </Card>
            
            <Card withBorder shadow="sm" padding="lg" radius="md">
              <Title order={4} c="var(--text-primary)" mb="md">Contact Information</Title>
              <Text><strong>Phone:</strong> 1-800-JET-ICUU (538-4288)</Text>
              <Text><strong>International:</strong> +1-727-344-1900</Text>
              <Text><strong>Email:</strong> operations@jeticu.com</Text>
              <Text><strong>Address:</strong> 2561 Rescue Way, Clearwater, FL 33762</Text>
            </Card>
          </Stack>
        </SimpleGrid>
      </Stack>
    </Container>
  );
}
