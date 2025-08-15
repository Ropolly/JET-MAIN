import { Container, Title, Box } from '@mantine/core';
import { PatientsList } from '../components/PatientsList';

export function PatientsPage() {
  return (
    <Container size="xl" py="xl">
      <Title order={2} mb="lg">Patients Management</Title>
      <Box>
        <PatientsList />
      </Box>
    </Container>
  );
}
