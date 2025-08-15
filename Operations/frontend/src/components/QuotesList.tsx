import { useState, useEffect } from 'react';
import { Table, Button, Group, Text, Loader, Box, Badge } from '@mantine/core';
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

export function QuotesList() {
  const [quotes, setQuotes] = useState<Quote[]>([]);
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

  const getStatusColor = (status: string) => {
    switch (status.toLowerCase()) {
      case 'pending':
        return 'yellow';
      case 'approved':
        return 'green';
      case 'rejected':
        return 'red';
      case 'in progress':
        return 'blue';
      default:
        return 'gray';
    }
  };

  if (loading) {
    return (
      <Box p="xl" style={{ display: 'flex', justifyContent: 'center' }}>
        <Loader size="lg" />
      </Box>
    );
  }

  if (error) {
    return (
      <Box p="xl" style={{ textAlign: 'center' }}>
        <Text c="var(--accent-secondary)" size="lg">{error}</Text>
        <Button mt="md" onClick={() => window.location.reload()}>
          Try Again
        </Button>
      </Box>
    );
  }

  return (
    <div>
      <Group justify="space-between" mb="md">
        <Text size="xl" fw={700}>Quotes</Text>
        <Button>Create New Quote</Button>
      </Group>

      {quotes.length === 0 ? (
        <Text ta="center" py="xl" c="var(--text-secondary)">
          No quotes found. Create a new quote to get started.
        </Text>
      ) : (
        <Table striped highlightOnHover>
          <Table.Thead>
            <Table.Tr>
              <Table.Th>Quote #</Table.Th>
              <Table.Th>Contact</Table.Th>
              <Table.Th>Route</Table.Th>
              <Table.Th>Est. Price</Table.Th>
              <Table.Th>Status</Table.Th>
              <Table.Th>Created On</Table.Th>
              <Table.Th>Actions</Table.Th>
            </Table.Tr>
          </Table.Thead>
          <Table.Tbody>
            {quotes.map((quote) => (
              <Table.Tr key={quote.id}>
                <Table.Td>{quote.quote_number}</Table.Td>
                <Table.Td>
                  <div>{`${quote.contact?.first_name || ''} ${quote.contact?.last_name || ''}`}</div>
                  <Text size="xs" c="var(--text-secondary)">{quote.contact?.email || 'N/A'}</Text>
                </Table.Td>
                <Table.Td>
                  <div>{quote.pickup_location}</div>
                  <Text size="xs">→</Text>
                  <div>{quote.destination_location}</div>
                </Table.Td>
                <Table.Td>${quote.estimated_price?.toLocaleString() || 'N/A'}</Table.Td>
                <Table.Td>
                  <Badge color={getStatusColor(quote.status)}>{quote.status}</Badge>
                </Table.Td>
                <Table.Td>{new Date(quote.created_on).toLocaleDateString()}</Table.Td>
                <Table.Td>
                  <Group gap="xs">
                    <Button size="xs" variant="outline">View</Button>
                    <Button size="xs" variant="outline">Edit</Button>
                  </Group>
                </Table.Td>
              </Table.Tr>
            ))}
          </Table.Tbody>
        </Table>
      )}
    </div>
  );
}
