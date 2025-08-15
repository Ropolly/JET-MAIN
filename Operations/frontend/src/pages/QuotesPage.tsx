import { useState, useEffect } from 'react';
import { Title, Card, Text, Button, Group, Stack, Table, Badge, Loader } from '@mantine/core';
import { quoteAPI } from '../services/api';

interface Quote {
  id: string;
  quote_number: string;
  status: string;
  created_on: string;
  contact: {
    first_name: string;
    last_name: string;
    email: string;
    phone: string;
  };
  pickup_location: string;
  destination_location: string;
  estimated_price: number;
}

export function QuotesPage() {
  const [quotes, setQuotes] = useState<Quote[]>([]);
  const [selectedQuote, setSelectedQuote] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchQuotes = async () => {
      try {
        setLoading(true);
        const data = await quoteAPI.getAll();
        setQuotes(data.results || []);
        setError(null);
      } catch (err: any) {
        console.error('Error fetching quotes:', err);
        setError(err.message || 'Failed to load quotes');
      } finally {
        setLoading(false);
      }
    };

    fetchQuotes();
  }, []);

  const getStatusBadgeColor = (status: string) => {
    switch (status.toLowerCase()) {
      case 'pending': return 'yellow';
      case 'sent': return 'blue';
      case 'approved': return 'green';
      case 'accepted': return 'green';
      case 'declined': return 'red';
      case 'rejected': return 'red';
      default: return 'gray';
    }
  };

  return (
    <Stack gap="lg">
      <Group justify="space-between">
        <Title order={2} c="var(--text-primary)">Quotes</Title>
        <Button 
          style={{
            backgroundColor: 'var(--button-primary)',
            color: 'var(--button-text)',
          }}
        >
          New Quote
        </Button>
      </Group>
      
      <Card withBorder shadow="sm" padding="lg" radius="md">
        {loading ? (
          <Group justify="center" py="xl">
            <Loader size="lg" />
          </Group>
        ) : error ? (
          <Text ta="center" py="xl" c="var(--accent-secondary)">
            {error}
            <Button mt="md" onClick={() => window.location.reload()}>
              Try Again
            </Button>
          </Text>
        ) : quotes.length === 0 ? (
          <Text ta="center" py="xl" c="var(--text-secondary)">
            No quotes found. Create a new quote to get started.
          </Text>
        ) : (
          <Table striped highlightOnHover>
            <Table.Thead>
              <Table.Tr>
                <Table.Th>Quote #</Table.Th>
                <Table.Th>Client</Table.Th>
                <Table.Th>From</Table.Th>
                <Table.Th>To</Table.Th>
                <Table.Th>Est. Price</Table.Th>
                <Table.Th>Date</Table.Th>
                <Table.Th>Status</Table.Th>
                <Table.Th>Actions</Table.Th>
              </Table.Tr>
            </Table.Thead>
            <Table.Tbody>
              {quotes.map((quote) => (
                <Table.Tr key={quote.id} bg={selectedQuote === quote.id ? 'var(--bg-secondary)' : undefined}>
                  <Table.Td>{quote.quote_number}</Table.Td>
                  <Table.Td>{`${quote.contact?.first_name || ''} ${quote.contact?.last_name || ''}`}</Table.Td>
                  <Table.Td>{quote.pickup_location}</Table.Td>
                  <Table.Td>{quote.destination_location}</Table.Td>
                  <Table.Td>${quote.estimated_price?.toLocaleString() || 'N/A'}</Table.Td>
                  <Table.Td>{new Date(quote.created_on).toLocaleDateString()}</Table.Td>
                  <Table.Td>
                    <Badge color={getStatusBadgeColor(quote.status)}>
                      {quote.status.charAt(0).toUpperCase() + quote.status.slice(1)}
                    </Badge>
                  </Table.Td>
                  <Table.Td>
                    <Group gap="xs">
                      <Button 
                        size="xs" 
                        variant="outline"
                        onClick={() => setSelectedQuote(quote.id === selectedQuote ? null : quote.id)}
                      >
                        View
                      </Button>
                      <Button 
                        size="xs" 
                        variant="outline"
                        color="blue"
                      >
                        Edit
                      </Button>
                    </Group>
                  </Table.Td>
                </Table.Tr>
              ))}
            </Table.Tbody>
          </Table>
        )}
      </Card>
      
      {selectedQuote && (
        <Card withBorder shadow="sm" padding="lg" radius="md">
          <Card.Section withBorder inheritPadding py="xs">
            <Text fw={500}>Quote Details</Text>
          </Card.Section>
          {loading ? (
            <Group justify="center" py="xl">
              <Loader size="lg" />
            </Group>
          ) : (
            <Stack gap="md" mt="md">
              {quotes.filter(q => q.id === selectedQuote).map(quote => (
                <div key={quote.id}>
                  <Group mb="md">
                    <div>
                      <Text fw={700} size="lg">{quote.quote_number}</Text>
                      <Text size="sm" c="var(--text-secondary)">
                        Created on {new Date(quote.created_on).toLocaleDateString()}
                      </Text>
                    </div>
                    <Badge ml="auto" size="lg" color={getStatusBadgeColor(quote.status)}>
                      {quote.status.charAt(0).toUpperCase() + quote.status.slice(1)}
                    </Badge>
                  </Group>

                  <Text fw={700} mb="xs">Client Information</Text>
                  <Card withBorder mb="md" p="sm">
                    <Text>{`${quote.contact?.first_name || ''} ${quote.contact?.last_name || ''}`}</Text>
                    <Text size="sm">{quote.contact?.email || 'No email provided'}</Text>
                    <Text size="sm">{quote.contact?.phone || 'No phone provided'}</Text>
                  </Card>

                  <Text fw={700} mb="xs">Route Information</Text>
                  <Card withBorder mb="md" p="sm">
                    <Group>
                      <div>
                        <Text fw={500}>From</Text>
                        <Text>{quote.pickup_location}</Text>
                      </div>
                      <div>
                        <Text fw={500}>To</Text>
                        <Text>{quote.destination_location}</Text>
                      </div>
                    </Group>
                  </Card>

                  <Text fw={700} mb="xs">Pricing</Text>
                  <Card withBorder mb="md" p="sm">
                    <Text fw={500} size="lg">${quote.estimated_price?.toLocaleString() || 'N/A'}</Text>
                  </Card>
                </div>
              ))}

              <Group justify="flex-end" mt="md">
                <Button variant="outline" color="red">Decline</Button>
                <Button variant="outline" color="blue">Send to Client</Button>
                <Button 
                  style={{
                    backgroundColor: 'var(--button-primary)',
                    color: 'var(--button-text)',
                  }}
                >
                  Convert to Trip
                </Button>
              </Group>
            </Stack>
          )}
        </Card>
      )}
    </Stack>
  );
}
