<template>
  <!--begin::Card-->
  <div class="card card-flush pt-3 mb-5 mb-xl-10">
    <!--begin::Card header-->
    <div class="card-header">
      <!--begin::Card title-->
      <div class="card-title">
        <h2 class="fw-bold">{{ formatTripType(trip?.type) }}</h2>
      </div>
      <!--end::Card title-->
    </div>
    <!--end::Card header-->

    <!--begin::Card body-->
    <div class="card-body pt-3">
      <div class="row g-5">
        <!--begin::Col - Trip Info-->
        <div class="col-4">
          <div class="position-relative ps-6 py-3">
            <!--begin::Bar-->
            <div class="position-absolute h-100 w-4px rounded top-0 start-0 bg-light-secondary"></div>
            <!--end::Bar-->
            <div class="fs-6 fw-semibold text-gray-700">Trip <span class="fw-bold">{{ trip?.trip_number || '-' }}</span></div>
            <div class="fs-7 text-muted">Created {{ formatDate(trip?.created_on) }}</div>
          </div>
        </div>
        <!--end::Col-->

        <!--begin::Col - Patient Info-->
        <div class="col-4">
          <div class="position-relative ps-6 py-3">
            <!--begin::Bar-->
            <div class="position-absolute h-100 w-4px rounded top-0 start-0 bg-light-secondary"></div>
            <!--end::Bar-->
            
            <!-- Patient Assigned -->
            <div v-if="props.trip?.patient?.info" class="fs-6 fw-semibold text-gray-700">
              <span class="fw-bold">{{ getPatientName() }}</span>
            </div>
            
            <!-- No Patient Assigned - Show Add Patient button only for medical trips -->
            <div v-else-if="props.trip?.type === 'medical'" class="d-flex justify-content-center align-items-center">
              <button 
                @click="openAddPatientModal"
                class="btn btn-sm btn-light-primary"
                :disabled="loading"
              >
                <KTIcon icon-name="plus" icon-class="fs-6" />
                Add Patient
              </button>
            </div>
            
            <!-- Show Patient label only when patient is assigned -->
            <div v-if="props.trip?.patient?.info" class="fs-7 text-muted">Patient</div>
          </div>
        </div>
        <!--end::Col-->

        <!--begin::Col - Status-->
        <div class="col-4">
          <div class="position-relative ps-6 py-3">
            <!--begin::Bar-->
            <div class="position-absolute h-100 w-4px rounded top-0 start-0 bg-light-secondary"></div>
            <!--end::Bar-->
            <div>
              <select 
                :value="trip?.status || 'pending'"
                @change="updateTripStatus($event.target.value)"
                class="form-select form-select-sm bg-white"
                :class="`border-${getStatusColor()}`"
                :disabled="statusUpdating"
              >
                <option value="pending">Pending</option>
                <option value="active">Active</option>
                <option value="in_progress">In Progress</option>
                <option value="completed">Completed</option>
                <option value="cancelled">Cancelled</option>
              </select>
            </div>
          </div>
        </div>
        <!--end::Col-->
      </div>
    </div>
    <!--end::Card body-->
  </div>
  <!--end::Card-->

  <!-- Add Patient Modal -->
  <div
    class="modal fade"
    id="kt_modal_add_patient"
    ref="modalRef"
    tabindex="-1"
    aria-hidden="true"
    v-if="showAddPatientModal"
  >
    <div class="modal-dialog modal-dialog-centered mw-650px">
      <div class="modal-content">
        <div class="modal-header">
          <h2 class="fw-bold">Add Patient to Trip</h2>
          <div
            class="btn btn-icon btn-sm btn-active-icon-primary"
            @click="closeModal"
          >
            <KTIcon icon-name="cross" icon-class="fs-1" />
          </div>
        </div>

        <div class="modal-body scroll-y mx-5 mx-xl-15 my-7">
          <form @submit.prevent="submitPatient">
            <!-- Patient Selection -->
            <div class="fv-row mb-7">
              <label class="required fw-semibold fs-6 mb-2">Select Patient</label>
              <select
                v-model="selectedPatientId"
                class="form-select form-select-solid"
                required
              >
                <option value="">Select a patient...</option>
                <option v-for="patient in patients" :key="patient.id" :value="patient.id">
                  {{ formatPatientName(patient) }}
                </option>
              </select>
            </div>

            <!-- Action Buttons -->
            <div class="text-center pt-15">
              <button
                type="button"
                class="btn btn-light me-3"
                @click="closeModal"
              >
                Cancel
              </button>
              <button
                type="submit"
                class="btn btn-primary"
                :disabled="isSubmitting || !selectedPatientId"
              >
                <span v-if="!isSubmitting">Add Patient</span>
                <span v-else>
                  <span class="spinner-border spinner-border-sm me-2"></span>
                  Adding...
                </span>
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, nextTick } from 'vue';
import { Modal } from 'bootstrap';
import ApiService from '@/core/services/ApiService';
import Swal from 'sweetalert2';

interface Props {
  trip: any;
  loading: boolean;
}

interface Patient {
  id: string;
  info: {
    first_name: string;
    last_name: string;
  };
}

const props = defineProps<Props>();
const emit = defineEmits<{
  patientAdded: [];
  statusUpdated: [status: string];
}>();

// Modal state
const showAddPatientModal = ref(false);
const modalRef = ref<HTMLElement | null>(null);
const modal = ref<Modal | null>(null);
const patients = ref<Patient[]>([]);
const selectedPatientId = ref('');
const isSubmitting = ref(false);

// Status update state
const statusUpdating = ref(false);

const getPatientInitials = (): string => {
  if (props.trip?.patient?.info) {
    const first = props.trip.patient.info.first_name?.charAt(0) || '';
    const last = props.trip.patient.info.last_name?.charAt(0) || '';
    return (first + last).toUpperCase() || 'P';
  }
  return 'P';
};

const getPatientName = (): string => {
  if (props.trip?.patient?.info) {
    const first = props.trip.patient.info.first_name || '';
    const last = props.trip.patient.info.last_name || '';
    return `${first} ${last}`.trim() || 'Unknown Patient';
  }
  return 'No Patient Assigned';
};

const getStatusColor = (): string => {
  const status = props.trip?.status?.toLowerCase();
  switch (status) {
    case 'completed': return 'success';
    case 'active': case 'in_progress': return 'primary';
    case 'cancelled': return 'danger';
    case 'pending': return 'warning';
    default: return 'secondary';
  }
};

const formatDate = (dateString?: string): string => {
  if (!dateString) return '-';
  return new Date(dateString).toLocaleDateString('en-US', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
  });
};

// Format trip type to title case
const formatTripType = (type?: string): string => {
  if (!type) return 'Medical Transport';
  
  // Handle special cases
  const typeMap: { [key: string]: string } = {
    'medical': 'Medical Transport',
    'charter': 'Charter',
    'part 91': 'Part 91',
    'part_91': 'Part 91',
    'maintenance': 'Maintenance',
    'other': 'Other'
  };
  
  const lowerType = type.toLowerCase();
  if (typeMap[lowerType]) {
    return typeMap[lowerType];
  }
  
  // Default: convert to title case
  return type.split(/[_\s]+/)
    .map(word => word.charAt(0).toUpperCase() + word.slice(1).toLowerCase())
    .join(' ');
};

const viewPatient = () => {
  if (props.trip?.patient?.id) {
    window.open(`/admin/contacts/patients/${props.trip.patient.id}`, '_blank');
  }
};

// Modal functions
const loadPatients = async () => {
  try {
    const response = await ApiService.get('/patients/?page_size=100');
    patients.value = response.data.results || response.data;
  } catch (error) {
    console.error('Error loading patients:', error);
    Swal.fire({
      icon: 'error',
      title: 'Error',
      text: 'Failed to load patients. Please try again.'
    });
  }
};

const formatPatientName = (patient: Patient): string => {
  const first = patient.info?.first_name || '';
  const last = patient.info?.last_name || '';
  return `${first} ${last}`.trim() || 'Unknown Patient';
};

const closeModal = () => {
  showAddPatientModal.value = false;
  selectedPatientId.value = '';
  isSubmitting.value = false;
};

const submitPatient = async () => {
  if (!selectedPatientId.value || !props.trip?.id) return;

  isSubmitting.value = true;

  try {
    // Update the trip with the selected patient
    await ApiService.patch(`/trips/${props.trip.id}/`, {
      patient: selectedPatientId.value,
      type: props.trip.type // Include required type field for validation
    });

    Swal.fire({
      icon: 'success',
      title: 'Success',
      text: 'Patient has been added to the trip successfully!'
    });

    // Emit event to refresh trip data
    emit('patientAdded');
    
    closeModal();
  } catch (error: any) {
    console.error('Error adding patient to trip:', error);
    Swal.fire({
      icon: 'error',
      title: 'Error',
      text: error.response?.data?.message || 'Failed to add patient. Please try again.'
    });
  } finally {
    isSubmitting.value = false;
  }
};

// Watch for modal show/hide
onMounted(() => {
  nextTick(() => {
    // Initialize Bootstrap modal when modal element is available
    if (modalRef.value) {
      modal.value = new Modal(modalRef.value);
      
      modalRef.value.addEventListener('show.bs.modal', () => {
        loadPatients();
      });
      
      modalRef.value.addEventListener('hidden.bs.modal', () => {
        closeModal();
      });
    }
  });
});

// Modal controls
const openAddPatientModal = async () => {
  showAddPatientModal.value = true;
  
  // Wait for DOM update
  await nextTick();
  
  // Initialize and show modal if not already initialized
  if (modalRef.value && !modal.value) {
    modal.value = new Modal(modalRef.value);
  }
  
  if (modal.value) {
    loadPatients();
    modal.value.show();
  }
};

// Status update function
const updateTripStatus = async (newStatus: string) => {
  if (!props.trip?.id || statusUpdating.value) return;
  
  statusUpdating.value = true;
  
  try {
    // Update the trip status
    await ApiService.patch(`/trips/${props.trip.id}/`, {
      status: newStatus,
      type: props.trip.type // Include required type field for validation
    });
    
    // Emit event to parent to update the trip data
    emit('statusUpdated', newStatus);
    
    // Show success notification
    Swal.fire({
      title: 'Success',
      text: `Trip status updated to ${newStatus.charAt(0).toUpperCase() + newStatus.slice(1)}`,
      icon: 'success',
      timer: 2000,
      showConfirmButton: false
    });
    
  } catch (error: any) {
    console.error('Error updating trip status:', error);
    
    Swal.fire({
      title: 'Error',
      text: error.response?.data?.message || 'Failed to update trip status. Please try again.',
      icon: 'error',
      confirmButtonText: 'OK'
    });
  } finally {
    statusUpdating.value = false;
  }
};
</script>