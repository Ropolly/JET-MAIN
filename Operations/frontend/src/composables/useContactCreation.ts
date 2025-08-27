/**
 * Vue Composable for Contact Creation
 * 
 * Provides reactive state management for contact creation forms
 */

import { ref, reactive, computed, readonly } from 'vue';
import ContactService, { 
  type ContactData, 
  type ContactCreationRequest, 
  type ContactCreationResponse,
  type PatientData,
  type StaffData,
  type PassengerData
} from '@/services/contactService';
import Swal from 'sweetalert2';

export function useContactCreation() {
  // Reactive state
  const loading = ref(false);
  const errors = ref<string[]>([]);
  const lastCreatedContact = ref<any>(null);
  
  // Form data reactive object
  const formData = reactive({
    // Personal Information
    first_name: '',
    last_name: '',
    business_name: '',
    
    // Contact Information
    email: '',
    phone: '',
    
    // Address Information
    address_line1: '',
    address_line2: '',
    city: '',
    state: '',
    zip: '',
    country: '',
    
    // Personal Details
    nationality: '',
    date_of_birth: '',
    passport_number: '',
    passport_expiration_date: '',
  });
  
  // Related data for specific types
  const patientData = reactive({
    special_instructions: '',
    bed_at_origin: false,
    bed_at_destination: false,
    status: 'pending'
  });
  
  const staffData = reactive({
    active: true,
    notes: ''
  });
  
  const passengerData = reactive({
    contact_number: '',
    notes: '',
    status: 'active'
  });
  
  // Computed properties
  const hasErrors = computed(() => errors.value.length > 0);
  const isFormValid = computed(() => {
    const validationErrors = ContactService.validateContactData(formData);
    return validationErrors.length === 0;
  });
  
  // Methods
  const clearForm = () => {
    // Reset contact form
    Object.keys(formData).forEach(key => {
      if (typeof (formData as any)[key] === 'boolean') {
        (formData as any)[key] = false;
      } else {
        (formData as any)[key] = '';
      }
    });
    
    // Reset related data
    Object.keys(patientData).forEach(key => {
      if (typeof (patientData as any)[key] === 'boolean') {
        (patientData as any)[key] = false;
      } else if (key === 'status') {
        (patientData as any)[key] = 'pending';
      } else {
        (patientData as any)[key] = '';
      }
    });
    
    Object.keys(staffData).forEach(key => {
      if (typeof (staffData as any)[key] === 'boolean') {
        (staffData as any)[key] = key === 'active'; // active defaults to true
      } else {
        (staffData as any)[key] = '';
      }
    });
    
    Object.keys(passengerData).forEach(key => {
      if (typeof (passengerData as any)[key] === 'boolean') {
        (passengerData as any)[key] = false;
      } else if (key === 'status') {
        (passengerData as any)[key] = 'active';
      } else {
        (passengerData as any)[key] = '';
      }
    });
    
    // Clear errors and last created contact
    errors.value = [];
    lastCreatedContact.value = null;
  };
  
  const validateForm = (): boolean => {
    errors.value = ContactService.validateContactData(formData);
    return !hasErrors.value;
  };
  
  const createContact = async (
    relatedType: 'patient' | 'staff' | 'passenger' | 'customer',
    showSuccessMessage = true
  ): Promise<ContactCreationResponse | null> => {
    if (!validateForm()) {
      return null;
    }
    
    loading.value = true;
    
    try {
      let relatedData = {};
      
      // Get appropriate related data based on type
      switch (relatedType) {
        case 'patient':
          relatedData = { ...patientData };
          break;
        case 'staff':
          relatedData = { ...staffData };
          break;
        case 'passenger':
          relatedData = { ...passengerData };
          break;
        case 'customer':
          relatedData = {};
          break;
      }
      
      const request: ContactCreationRequest = {
        ...formData,
        related_type: relatedType,
        related_data: relatedData
      };
      
      const response = await ContactService.createContactWithRelated(request);
      
      lastCreatedContact.value = response;
      
      if (showSuccessMessage) {
        await Swal.fire({
          icon: 'success',
          title: 'Success!',
          text: response.message,
          confirmButtonText: 'OK'
        });
      }
      
      // Clear form after successful creation
      clearForm();
      
      return response;
      
    } catch (error: any) {
      const errorMessage = error.message || 'Failed to create contact';
      errors.value = [errorMessage];
      
      await Swal.fire({
        icon: 'error',
        title: 'Error',
        text: errorMessage,
        confirmButtonText: 'OK'
      });
      
      return null;
    } finally {
      loading.value = false;
    }
  };
  
  // Specific creation methods
  const createPatient = (showSuccessMessage = true) => createContact('patient', showSuccessMessage);
  const createStaff = (showSuccessMessage = true) => createContact('staff', showSuccessMessage);
  const createPassenger = (showSuccessMessage = true) => createContact('passenger', showSuccessMessage);
  const createCustomer = (showSuccessMessage = true) => createContact('customer', showSuccessMessage);
  
  // Utility methods
  const prefillForm = (contactData: Partial<ContactData>) => {
    Object.keys(contactData).forEach(key => {
      if (key in formData) {
        (formData as any)[key] = (contactData as any)[key] || '';
      }
    });
  };
  
  const getDisplayName = () => {
    return ContactService.getContactDisplayName(formData);
  };
  
  return {
    // State
    loading: readonly(loading),
    errors: readonly(errors),
    hasErrors,
    isFormValid,
    lastCreatedContact: readonly(lastCreatedContact),
    
    // Form data
    formData,
    patientData,
    staffData, 
    passengerData,
    
    // Methods
    clearForm,
    validateForm,
    createContact,
    createPatient,
    createStaff,
    createPassenger,
    createCustomer,
    prefillForm,
    getDisplayName
  };
}

export default useContactCreation;