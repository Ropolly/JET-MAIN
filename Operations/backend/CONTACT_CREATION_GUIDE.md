# Unified Contact Creation System

## Overview

This system provides a clean, consistent way to create contact records for patients, staff, passengers, and customers. All passport information, birth dates, and contact details are now stored on the Contact model to eliminate data duplication.

## Database Schema Changes

### Contact Model (Primary)
The `Contact` model now contains all shared fields:
- Personal info: `first_name`, `last_name`, `business_name`
- Contact info: `email`, `phone`
- Address info: `address_line1`, `address_line2`, `city`, `state`, `zip`, `country`
- **Personal details**: `nationality`, `date_of_birth`, `passport_number`, `passport_expiration_date`

### Related Models
- **Patient**: References Contact via `info` FK, has medical-specific fields
- **Staff**: References Contact via OneToOne, has role-specific fields  
- **Passenger**: References Contact via `info` FK, has travel-specific fields
- **Customer**: Uses Contact directly for quote contacts

## Backend Implementation

### 1. Contact Service (`api/contact_service.py`)

```python
from api.contact_service import ContactCreationService

# Create patient with contact
contact, patient = ContactCreationService.create_contact_with_related(
    contact_data={
        'first_name': 'John',
        'last_name': 'Doe',
        'email': 'john.doe@example.com',
        'date_of_birth': '1990-01-01',
        'passport_number': '123456789',
        'passport_expiration_date': '2030-01-01',
        'nationality': 'US'
    },
    related_type='patient',
    related_data={
        'special_instructions': 'Wheelchair required',
        'bed_at_origin': True,
        'status': 'confirmed'
    },
    created_by=request.user
)
```

### 2. API Endpoint

```bash
POST /api/contacts/create-with-related/

{
  "first_name": "John",
  "last_name": "Doe",
  "email": "john.doe@example.com",
  "phone": "+1234567890",
  "date_of_birth": "1990-01-01",
  "passport_number": "123456789",
  "passport_expiration_date": "2030-01-01",
  "nationality": "US",
  "related_type": "patient",
  "related_data": {
    "special_instructions": "Requires wheelchair assistance",
    "bed_at_origin": true,
    "status": "confirmed"
  }
}
```

Response:
```json
{
  "contact": { ... },
  "patient": { ... },
  "related_type": "patient",
  "success": true,
  "message": "Patient created successfully"
}
```

## Frontend Implementation

### 1. Contact Service (`services/contactService.ts`)

```typescript
import ContactService from '@/services/contactService';

// Create patient
const response = await ContactService.createPatientContact({
  first_name: 'John',
  last_name: 'Doe',
  email: 'john.doe@example.com',
  date_of_birth: '1990-01-01',
  passport_number: '123456789'
}, {
  special_instructions: 'Wheelchair required',
  bed_at_origin: true
});
```

### 2. Vue Composable (`composables/useContactCreation.ts`)

```vue
<script setup>
import { useContactCreation } from '@/composables/useContactCreation';

const {
  loading,
  formData,
  patientData,
  createPatient,
  clearForm
} = useContactCreation();

// Form data is reactive
formData.first_name = 'John';
formData.last_name = 'Doe';
patientData.special_instructions = 'Wheelchair required';

// Create patient
const response = await createPatient();
</script>
```

### 3. Unified Form Component

```vue
<template>
  <UnifiedContactForm 
    :defaultType="'patient'"
    @contactCreated="handleContactCreated"
    @success="handleSuccess"
  />
</template>

<script setup>
import UnifiedContactForm from '@/components/forms/UnifiedContactForm.vue';

const handleContactCreated = (contact) => {
  console.log('Created contact:', contact);
};
</script>
```

## Usage Examples

### Create Patient
```typescript
const patient = await ContactService.createPatientContact({
  first_name: 'Jane',
  last_name: 'Smith',
  email: 'jane.smith@example.com',
  date_of_birth: '1985-05-15',
  passport_number: 'AB1234567',
  passport_expiration_date: '2028-05-15',
  nationality: 'CA'
}, {
  special_instructions: 'Diabetic - insulin required',
  bed_at_origin: false,
  bed_at_destination: true,
  status: 'confirmed'
});
```

### Create Staff Member
```typescript
const staff = await ContactService.createStaffContact({
  first_name: 'Dr. Mike',
  last_name: 'Johnson',
  email: 'mike.johnson@jeticu.com',
  phone: '+1234567890',
  nationality: 'US'
}, {
  active: true,
  notes: 'Flight nurse, 10 years experience'
});
```

### Create Passenger
```typescript
const passenger = await ContactService.createPassengerContact({
  first_name: 'Robert',
  last_name: 'Wilson',
  email: 'robert.wilson@example.com',
  date_of_birth: '1975-12-01',
  passport_number: 'CD9876543',
  nationality: 'UK'
}, {
  contact_number: '+44123456789',
  notes: 'Family member accompanying patient',
  status: 'active'
});
```

### Create Customer (Quote Contact)
```typescript
const customer = await ContactService.createCustomerContact({
  business_name: 'Insurance Company Inc',
  email: 'claims@insurance.com',
  phone: '+1555123456',
  address_line1: '123 Insurance Blvd',
  city: 'New York',
  state: 'NY',
  country: 'USA'
});
```

## Migration Notes

### Data Consolidation
The system handles the migration gracefully:

1. **Existing records**: Patient/Passenger models still have their duplicate fields for backwards compatibility
2. **New records**: When creating through the unified system, Contact becomes the source of truth
3. **Serializers updated**: Write serializers now pull from Contact data as primary source

### Deprecated Fields
The following fields on Patient/Passenger models are deprecated:
- `date_of_birth` → Use `contact.date_of_birth`
- `nationality` → Use `contact.nationality`  
- `passport_number` → Use `contact.passport_number`
- `passport_expiration_date` → Use `contact.passport_expiration_date`

### Future Migration
A database migration will be created later to:
1. Copy data from Patient/Passenger to Contact for existing records
2. Remove duplicate fields from Patient/Passenger models
3. Update all code references

## Benefits

1. **Consistent Data**: All passport and personal info in one place
2. **Clean API**: Single endpoint for all contact types
3. **Reusable Components**: Unified forms work for all types
4. **Data Integrity**: No more duplicate or conflicting information
5. **Easy Maintenance**: One place to update contact logic

## Testing

```bash
# Test the API endpoint
curl -X POST http://localhost:8000/api/contacts/create-with-related/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <token>" \
  -d '{
    "first_name": "Test",
    "last_name": "Patient",
    "email": "test@example.com",
    "date_of_birth": "1990-01-01",
    "related_type": "patient",
    "related_data": {
      "special_instructions": "Test instructions"
    }
  }'
```

## Error Handling

The system provides comprehensive validation:
- Either personal name or business name required
- Valid email format validation
- Date validation (passport expiration > birth date)
- Duplicate staff contact prevention
- Database constraint validation