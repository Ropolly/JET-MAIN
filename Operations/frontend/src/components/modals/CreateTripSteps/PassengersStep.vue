<template>
  <div class="w-100">
    <!--begin::Heading-->
    <div class="pb-10 pb-lg-12">
      <!--begin::Title-->
      <h2 class="fw-bold text-dark">Passengers & Patient</h2>
      <!--end::Title-->

      <!--begin::Notice-->
      <div class="text-muted fw-semibold fs-6">
        Add a patient and up to 8 passengers for this trip. Both are optional.
      </div>
      <!--end::Notice-->
    </div>
    <!--end::Heading-->

    <!--begin::Patient Section-->
    <div class="mb-10">
      <h4 class="fw-bold text-gray-900 mb-5">Patient</h4>
      
      <div class="fv-row mb-6">
        <label class="fs-6 fw-semibold mb-2">Select Patient</label>
        <select v-model="patient" class="form-select form-select-solid">
          <option value="">No patient for this trip...</option>
          <option v-for="patientItem in patients" :key="patientItem.id" :value="patientItem.id">
            {{ patientItem.info.first_name }} {{ patientItem.info.last_name }}
            <span v-if="patientItem.info.email"> - {{ patientItem.info.email }}</span>
          </option>
        </select>
        <div class="form-text">
          Select a patient if this is a medical transport. Leave empty for charter or other flight types.
        </div>
      </div>
    </div>
    <!--end::Patient Section-->

    <!--begin::Passengers Section-->
    <div class="mb-10">
      <div class="d-flex align-items-center justify-content-between mb-5">
        <h4 class="fw-bold text-gray-900">Passengers</h4>
        <button 
          type="button" 
          class="btn btn-sm btn-primary"
          @click="addPassenger"
          :disabled="passengers.length >= 8"
        >
          <KTIcon icon-name="plus" icon-class="fs-4 me-1" />
          Add Passenger
        </button>
      </div>

      <!--begin::Passenger Limit Notice-->
      <div v-if="passengers.length >= 8" class="alert alert-warning mb-5">
        <KTIcon icon-name="warning" icon-class="fs-2x text-warning me-3" />
        <div>
          <strong>Passenger limit reached.</strong> A maximum of 8 passengers can be added per trip.
        </div>
      </div>
      <!--end::Passenger Limit Notice-->

      <!--begin::Passengers List-->
      <div v-if="passengers.length === 0" class="text-center text-muted py-5">
        <KTIcon icon-name="people" icon-class="fs-2x text-muted mb-3" />
        <p class="mb-0">No passengers added yet. Passengers are optional for all trip types.</p>
      </div>

      <div v-else class="d-flex flex-column gap-4">
        <div
          v-for="(passenger, index) in passengers"
          :key="passenger.id"
          class="card"
        >
          <div class="card-header py-3">
            <div class="d-flex align-items-center justify-content-between">
              <h6 class="card-title mb-0">
                <KTIcon icon-name="user" icon-class="fs-5 me-2" />
                Passenger {{ index + 1 }}
              </h6>
              <button
                type="button"
                class="btn btn-sm btn-icon btn-light-danger"
                @click="removePassenger(index)"
              >
                <KTIcon icon-name="trash" icon-class="fs-6" />
              </button>
            </div>
          </div>
          <div class="card-body">
            <div class="fv-row">
              <label class="fs-6 fw-semibold mb-2">Select Contact</label>
              <select 
                v-model="passenger.contact_id" 
                @change="updatePassengerFromContact(passenger)"
                class="form-select form-select-solid"
                :disabled="loadingContacts"
              >
                <option value="">Select a contact...</option>
                <option 
                  v-for="contact in getAvailableContactsForPassenger(passenger)" 
                  :key="contact.id" 
                  :value="contact.id"
                >
                  {{ getContactDisplayName(contact) }}
                </option>
              </select>
              <div v-if="passenger.contact_id" class="mt-3">
                <div class="d-flex flex-column gap-1 text-muted fs-7">
                  <span v-if="passenger.contact_name">
                    <strong>Name:</strong> {{ passenger.contact_name }}
                  </span>
                  <span v-if="passenger.contact_email">
                    <strong>Email:</strong> {{ passenger.contact_email }}
                  </span>
                  <span v-if="passenger.contact_phone">
                    <strong>Phone:</strong> {{ passenger.contact_phone }}
                  </span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    <!--end::Passengers Section-->

    <!--begin::Summary-->
    <div v-if="patient || passengers.length > 0" class="alert alert-info d-flex align-items-center">
      <KTIcon icon-name="information-5" icon-class="fs-2x text-info me-4" />
      <div>
        <h5 class="mb-1 text-info">Manifest Summary</h5>
        <div class="text-gray-700">
          <span v-if="patient">
            <strong>1</strong> patient
          </span>
          <span v-if="patient && passengers.length > 0"> and </span>
          <span v-if="passengers.length > 0">
            <strong>{{ passengers.length }}</strong> passenger{{ passengers.length > 1 ? 's' : '' }}
          </span>
          will be on this trip.
        </div>
      </div>
    </div>
    <!--end::Summary-->

    <!--begin::No Manifest Notice-->
    <div v-if="!patient && passengers.length === 0" class="alert alert-secondary d-flex align-items-center">
      <KTIcon icon-name="information" icon-class="fs-2x text-secondary me-4" />
      <div>
        <h6 class="mb-1 text-secondary">Empty Manifest</h6>
        <div class="text-gray-600">
          This trip has no patient or passengers assigned. This is normal for positioning flights, maintenance flights, or crew-only operations.
        </div>
      </div>
    </div>
    <!--end::No Manifest Notice-->
  </div>
</template>

<script setup lang="ts">
import { watch, onMounted, computed, ref } from 'vue';
import { v4 as uuidv4 } from 'uuid';
import ApiService from '@/core/services/ApiService';

interface TripPassenger {
  id: string;
  contact_id: string;
  contact_name: string;
  contact_email?: string;
  contact_phone?: string;
}

const props = defineProps({
  patient: {
    type: String,
    default: ''
  },
  passengers: {
    type: Array as () => TripPassenger[],
    default: () => []
  },
  patients: {
    type: Array,
    default: () => []
  }
});

const emit = defineEmits(['update:patient', 'update:passengers', 'stepValidated']);

const patient = computed({
  get: () => props.patient,
  set: (value) => emit('update:patient', value)
});
const passengers = props.passengers;

// Available contacts for passenger selection
const availableContacts = ref<any[]>([]);
const loadingContacts = ref(false);

// Fetch and filter contacts (exclude patients and staff)
const fetchAvailableContacts = async () => {
  loadingContacts.value = true;
  try {
    // Fetch all contacts
    const contactsResponse = await ApiService.get("/contacts/?page_size=1000");
    const allContacts = contactsResponse.data.results || contactsResponse.data || [];
    
    // Fetch patients to exclude
    const patientsResponse = await ApiService.get("/patients/?page_size=1000");
    const patients = patientsResponse.data.results || patientsResponse.data || [];
    const patientContactIds = new Set(patients.map((p: any) => p.info?.id || p.info));
    
    // Fetch staff to exclude  
    const staffResponse = await ApiService.get("/staff/?page_size=1000");
    const staffMembers = staffResponse.data.results || staffResponse.data || [];
    const staffContactIds = new Set(staffMembers.map((s: any) => s.contact?.id || s.contact));
    
    // Filter contacts - exclude patients, staff, and already selected passengers
    const selectedContactIds = new Set(passengers.map(p => p.contact_id));
    
    availableContacts.value = allContacts.filter((contact: any) => 
      !patientContactIds.has(contact.id) && 
      !staffContactIds.has(contact.id) &&
      !selectedContactIds.has(contact.id)
    );
  } catch (error) {
    console.error('Error fetching contacts:', error);
    availableContacts.value = [];
  } finally {
    loadingContacts.value = false;
  }
};

// Get contact display name
const getContactDisplayName = (contact: any): string => {
  if (!contact) return 'Unknown Contact';
  
  const firstName = contact.first_name || '';
  const lastName = contact.last_name || '';
  const businessName = contact.business_name || '';
  const email = contact.email || '';
  
  if (businessName) return businessName;
  if (firstName || lastName) {
    const name = `${firstName} ${lastName}`.trim();
    return email ? `${name} - ${email}` : name;
  }
  
  return email || 'Contact ' + contact.id;
};

// Add new passenger
const addPassenger = () => {
  if (passengers.length >= 8) {
    return; // Max limit reached
  }

  const newPassenger: TripPassenger = {
    id: uuidv4(),
    contact_id: '',
    contact_name: '',
    contact_email: '',
    contact_phone: ''
  };

  passengers.push(newPassenger);
  emit('update:passengers', passengers);
  
  // Refresh available contacts to exclude newly added passenger
  fetchAvailableContacts();
  validateStep();
};

// Update passenger details when contact is selected
const updatePassengerFromContact = (passenger: TripPassenger) => {
  const contact = availableContacts.value.find(c => c.id === passenger.contact_id);
  if (contact) {
    passenger.contact_name = getContactDisplayName(contact);
    passenger.contact_email = contact.email || '';
    passenger.contact_phone = contact.phone || '';
  } else {
    passenger.contact_name = '';
    passenger.contact_email = '';
    passenger.contact_phone = '';
  }
  
  // Refresh available contacts when selection changes
  fetchAvailableContacts();
  validateStep();
};

// Get available contacts for a specific passenger (include their current selection)
const getAvailableContactsForPassenger = (passenger: TripPassenger) => {
  // Include the currently selected contact for this passenger plus all unselected contacts
  const otherSelectedIds = new Set(
    passengers
      .filter(p => p.id !== passenger.id && p.contact_id)
      .map(p => p.contact_id)
  );
  
  return availableContacts.value.filter(contact => 
    contact.id === passenger.contact_id || !otherSelectedIds.has(contact.id)
  );
};

// Remove passenger
const removePassenger = (index: number) => {
  passengers.splice(index, 1);
  emit('update:passengers', passengers);
  
  // Refresh available contacts when passenger is removed
  fetchAvailableContacts();
  validateStep();
};

// Validation - this step is always valid since both patient and passengers are optional
const validateStep = () => {
  // Check if all added passengers have selected a contact
  let allPassengersValid = true;
  
  for (const passenger of passengers) {
    if (!passenger.contact_id) {
      allPassengersValid = false;
      break;
    }
  }
  
  emit('stepValidated', allPassengersValid);
  return allPassengersValid;
};

// Watch for changes
watch(() => [patient, passengers], () => {
  emit('update:patient', patient);
  emit('update:passengers', passengers);
  validateStep();
}, { deep: true });

onMounted(() => {
  fetchAvailableContacts();
  validateStep();
});
</script>