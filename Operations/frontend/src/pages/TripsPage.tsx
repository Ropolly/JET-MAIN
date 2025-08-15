import { useState } from 'react';
import { Title, Card, Text, Button, Group, Stack, Table, Badge, Tabs } from '@mantine/core';

// Mock data for trips
const mockTrips = [
  { id: 567, client: 'John Smith', from: 'Miami, USA', to: 'Mexico City, Mexico', date: '2025-05-14', status: 'scheduled' },
  { id: 566, client: 'Sarah Johnson', from: 'London, UK', to: 'New York, USA', date: '2025-05-15', status: 'in-progress' },
  { id: 565, client: 'Ahmed Hassan', from: 'Dubai, UAE', to: 'Singapore', date: '2025-05-16', status: 'scheduled' },
  { id: 564, client: 'Maria Garcia', from: 'Los Angeles, USA', to: 'Tokyo, Japan', date: '2025-05-18', status: 'scheduled' },
  { id: 563, client: 'Robert Chen', from: 'Sydney, Australia', to: 'Auckland, NZ', date: '2025-05-12', status: 'completed' },
];

export function TripsPage() {
  const [selectedTrip, setSelectedTrip] = useState<number | null>(null);
  const [activeTab, setActiveTab] = useState<string | null>('details');

  const getStatusBadgeColor = (status: string) => {
    switch (status) {
      case 'scheduled': return 'blue';
      case 'in-progress': return 'yellow';
      case 'completed': return 'green';
      case 'cancelled': return 'red';
      default: return 'gray';
    }
  };

  return (
    <Stack spacing="lg">
      <Group position="apart">
        <Title order={2} c="var(--text-primary)">Trips</Title>
        <Button 
          style={{
            backgroundColor: 'var(--button-primary)',
            color: 'var(--button-text)',
          }}
        >
          New Trip
        </Button>
      </Group>
      
      <Card withBorder shadow="sm" padding="lg" radius="md">
        <Table striped highlightOnHover>
          <Table.Thead>
            <Table.Tr>
              <Table.Th>ID</Table.Th>
              <Table.Th>Client</Table.Th>
              <Table.Th>From</Table.Th>
              <Table.Th>To</Table.Th>
              <Table.Th>Date</Table.Th>
              <Table.Th>Status</Table.Th>
              <Table.Th>Actions</Table.Th>
            </Table.Tr>
          </Table.Thead>
          <Table.Tbody>
            {mockTrips.map((trip) => (
              <Table.Tr key={trip.id} bg={selectedTrip === trip.id ? 'var(--bg-secondary)' : undefined}>
                <Table.Td>#{trip.id}</Table.Td>
                <Table.Td>{trip.client}</Table.Td>
                <Table.Td>{trip.from}</Table.Td>
                <Table.Td>{trip.to}</Table.Td>
                <Table.Td>{trip.date}</Table.Td>
                <Table.Td>
                  <Badge color={getStatusBadgeColor(trip.status)}>
                    {trip.status.split('-').map(word => word.charAt(0).toUpperCase() + word.slice(1)).join(' ')}
                  </Badge>
                </Table.Td>
                <Table.Td>
                  <Group spacing="xs">
                    <Button 
                      size="xs" 
                      variant="outline"
                      onClick={() => setSelectedTrip(trip.id === selectedTrip ? null : trip.id)}
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
      </Card>
      
      {selectedTrip && (
        <Card withBorder shadow="sm" padding="lg" radius="md">
          <Card.Section withBorder inheritPadding py="xs">
            <Group position="apart">
              <Text fw={500}>Trip Details - #{selectedTrip}</Text>
              <Button 
                size="xs" 
                variant="outline" 
                color="red"
              >
                Cancel Trip
              </Button>
            </Group>
          </Card.Section>
          
          <Tabs value={activeTab} onChange={setActiveTab} mt="md">
            <Tabs.List>
              <Tabs.Tab value="details">Details</Tabs.Tab>
              <Tabs.Tab value="itinerary">Itinerary</Tabs.Tab>
              <Tabs.Tab value="passengers">Passengers</Tabs.Tab>
              <Tabs.Tab value="files">Files</Tabs.Tab>
            </Tabs.List>

            <Tabs.Panel value="details" pt="md">
              <Stack spacing="sm">
                <Text>
                  <strong>Client:</strong> {mockTrips.find(t => t.id === selectedTrip)?.client}
                </Text>
                <Text>
                  <strong>From:</strong> {mockTrips.find(t => t.id === selectedTrip)?.from}
                </Text>
                <Text>
                  <strong>To:</strong> {mockTrips.find(t => t.id === selectedTrip)?.to}
                </Text>
                <Text>
                  <strong>Date:</strong> {mockTrips.find(t => t.id === selectedTrip)?.date}
                </Text>
                <Text>
                  <strong>Status:</strong> {mockTrips.find(t => t.id === selectedTrip)?.status}
                </Text>
                <Text>
                  <strong>Aircraft:</strong> Learjet 45XR
                </Text>
                <Text>
                  <strong>Medical Staff:</strong> Dr. James Wilson, Nurse Sarah Miller
                </Text>
                <Text>
                  <strong>Flight Crew:</strong> Capt. Michael Johnson, First Officer Robert Davis
                </Text>
              </Stack>
            </Tabs.Panel>

            <Tabs.Panel value="itinerary" pt="md">
              <Stack spacing="sm">
                <Text fw={500}>Flight Schedule</Text>
                <Text>
                  <strong>Departure:</strong> May 14, 2025 - 08:00 AM EDT
                </Text>
                <Text>
                  <strong>Arrival:</strong> May 14, 2025 - 10:30 AM CDT
                </Text>
                <Text>
                  <strong>Flight Duration:</strong> 2h 30m
                </Text>
                <Text fw={500} mt="md">Ground Transportation</Text>
                <Text>
                  <strong>Pickup:</strong> Miami General Hospital - 06:30 AM EDT
                </Text>
                <Text>
                  <strong>Dropoff:</strong> Mexico City Specialty Hospital - 11:00 AM CDT
                </Text>
              </Stack>
            </Tabs.Panel>

            <Tabs.Panel value="passengers" pt="md">
              <Stack spacing="sm">
                <Text fw={500}>Patient Information</Text>
                <Text>
                  <strong>Name:</strong> John Smith
                </Text>
                <Text>
                  <strong>Age:</strong> 58
                </Text>
                <Text>
                  <strong>Medical Condition:</strong> Cardiac patient requiring specialized care
                </Text>
                <Text>
                  <strong>Special Requirements:</strong> Oxygen supply, cardiac monitoring
                </Text>
                
                <Text fw={500} mt="md">Accompanying Passengers</Text>
                <Text>
                  <strong>Name:</strong> Mary Smith (spouse)
                </Text>
                <Text>
                  <strong>Contact:</strong> +1 (305) 555-1234
                </Text>
              </Stack>
            </Tabs.Panel>

            <Tabs.Panel value="files" pt="md">
              <Stack spacing="sm">
                <Text>Medical Records.pdf</Text>
                <Text>Flight Manifest.pdf</Text>
                <Text>Insurance Documentation.pdf</Text>
                <Text>Consent Forms.pdf</Text>
                <Button 
                  size="sm" 
                  variant="outline" 
                  mt="md"
                >
                  Upload New File
                </Button>
              </Stack>
            </Tabs.Panel>
          </Tabs>
        </Card>
      )}
    </Stack>
  );
}
