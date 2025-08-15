import { useState, useEffect } from 'react';
import { Table, Button, Group, Text, Loader, Box } from '@mantine/core';
import { patientAPI } from '../services/api';

interface Patient {
  id: string;
  first_name: string;
  last_name: string;
  date_of_birth: string;
  info: {
    email: string;
    phone: string;
  };
  medical_notes: string;
}

export function PatientsList() {
  const [patients, setPatients] = useState<Patient[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchPatients = async () => {
      try {
        setLoading(true);
        const data = await patientAPI.getAll();
        setPatients(data.results || []);
        setError(null);
      } catch (err: any) {
        console.error('Error fetching patients:', err);
        setError(err.message || 'Failed to load patients');
      } finally {
        setLoading(false);
      }
    };

    fetchPatients();
  }, []);

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
        <Text size="xl" fw={700}>Patients</Text>
        <Button>Add New Patient</Button>
      </Group>

      {patients.length === 0 ? (
        <Text ta="center" py="xl" c="var(--text-secondary)">
          No patients found. Add a new patient to get started.
        </Text>
      ) : (
        <Table striped highlightOnHover>
          <Table.Thead>
            <Table.Tr>
              <Table.Th>Name</Table.Th>
              <Table.Th>Date of Birth</Table.Th>
              <Table.Th>Contact</Table.Th>
              <Table.Th>Actions</Table.Th>
            </Table.Tr>
          </Table.Thead>
          <Table.Tbody>
            {patients.map((patient) => (
              <Table.Tr key={patient.id}>
                <Table.Td>{`${patient.first_name} ${patient.last_name}`}</Table.Td>
                <Table.Td>{new Date(patient.date_of_birth).toLocaleDateString()}</Table.Td>
                <Table.Td>
                  <div>{patient.info?.email || 'N/A'}</div>
                  <div>{patient.info?.phone || 'N/A'}</div>
                </Table.Td>
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
