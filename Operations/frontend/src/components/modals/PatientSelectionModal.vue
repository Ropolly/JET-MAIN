<template>
  <!--begin::Modal - Select/Create Patient-->
  <div
    class="modal fade"
    id="kt_modal_patient_selection"
    ref="modalRef"
    tabindex="-1"
    aria-hidden="true"
  >
    <!--begin::Modal dialog-->
    <div class="modal-dialog modal-dialog-centered mw-650px">
      <!--begin::Modal content-->
      <div class="modal-content">
        <!--begin::Modal header-->
        <div class="modal-header">
          <!--begin::Title-->
          <h2>{{ modalTitle }}</h2>
          <!--end::Title-->

          <!--begin::Close-->
          <div
            class="btn btn-sm btn-icon btn-active-color-primary"
            data-bs-dismiss="modal"
            @click="closeModal"
          >
            <KTIcon icon-name="cross" icon-class="fs-1" />
          </div>
          <!--end::Close-->
        </div>
        <!--end::Modal header-->

        <!--begin::Modal body-->
        <div class="modal-body scroll-y mx-5 mx-xl-15 my-7">
          <!--begin::Mode Selection-->
          <div v-if="currentMode === 'selection'" class="text-center mb-10">
            <h3 class="text-gray-900 fw-bold mb-4">Add Patient to Trip</h3>
            <p class="text-gray-600 fs-6 mb-8">
              Choose how you would like to add a patient to this trip.
            </p>

            <!--begin::Options-->
            <div class="row g-6">
              <!--begin::Select Existing Patient-->
              <div class="col-md-6">
                <div
                  class="card card-dashed h-100 cursor-pointer patient-option-card"
                  @click="setMode('search')"
                >
                  <div class="card-body d-flex flex-column align-items-center text-center p-6">
                    <KTIcon icon-name="people" icon-class="fs-2x text-primary mb-4" />
                    <h4 class="text-gray-900 fw-bold mb-2">Select Existing Patient</h4>
                    <p class="text-gray-600 fs-7 mb-0">
                      Choose from existing patients in the system
                    </p>
                  </div>
                </div>
              </div>
              <!--end::Select Existing Patient-->

              <!--begin::Create New Patient-->
              <div class="col-md-6">
                <div
                  class="card card-dashed h-100 cursor-pointer patient-option-card"
                  @click="setMode('create')"
                >
                  <div class="card-body d-flex flex-column align-items-center text-center p-6">
                    <KTIcon icon-name="plus-circle" icon-class="fs-2x text-success mb-4" />
                    <h4 class="text-gray-900 fw-bold mb-2">Create New Patient</h4>
                    <p class="text-gray-600 fs-7 mb-0">
                      Add a new patient with contact information
                    </p>
                  </div>
                </div>
              </div>
              <!--end::Create New Patient-->
            </div>
            <!--end::Options-->
          </div>
          <!--end::Mode Selection-->

          <!--begin::Search Existing Patient-->
          <div v-if="currentMode === 'search'">
            <!--begin::Back Button-->
            <div class="d-flex align-items-center mb-6">
              <button @click="setMode('selection')" class="btn btn-sm btn-light-primary me-3">
                <KTIcon icon-name="arrow-left" icon-class="fs-6 me-1" />
                Back
              </button>
              <h3 class="text-gray-900 fw-bold mb-0">Select Existing Patient</h3>
            </div>
            <!--end::Back Button-->

            <!--begin::Patient Search-->
            <div class="mb-6">
              <PatientSearchSelect
                v-model="selectedPatientId"
                label="Search for Patient"
                placeholder="Search by name or email..."
                @patient-selected="onPatientSelected"
                :required="true"
              />
            </div>
            <!--end::Patient Search-->

            <!--begin::Selected Patient Info-->
            <div v-if="selectedPatient" class="alert alert-primary d-flex align-items-center mb-6">
              <KTIcon icon-name="information-5" icon-class="fs-2x text-primary me-4" />
              <div>
                <h5 class="mb-1 text-primary">{{ getPatientDisplayName(selectedPatient) }}</h5>
                <div class="text-gray-700">
                  <span v-if="selectedPatient.info?.email">{{ selectedPatient.info.email }}</span>
                  <span v-if="selectedPatient.info?.phone" class="ms-3">{{ selectedPatient.info.phone }}</span>
                </div>
              </div>
            </div>
            <!--end::Selected Patient Info-->
          </div>
          <!--end::Search Existing Patient-->

          <!--begin::Create New Patient-->
          <div v-if="currentMode === 'create'">
            <!--begin::Back Button-->
            <div class="d-flex align-items-center mb-6">
              <button @click="setMode('selection')" class="btn btn-sm btn-light-primary me-3">
                <KTIcon icon-name="arrow-left" icon-class="fs-6 me-1" />
                Back
              </button>
              <h3 class="text-gray-900 fw-bold mb-0">Create New Patient</h3>
            </div>
            <!--end::Back Button-->

            <!--begin::Creation Steps Info-->
            <div class="alert alert-info d-flex align-items-center mb-6">
              <KTIcon icon-name="information-5" icon-class="fs-2x text-info me-4" />
              <div>
                <div class="text-gray-700">
                  This will create a new contact and patient record. You'll be able to add medical details after the patient is created.
                </div>
              </div>
            </div>
            <!--end::Creation Steps Info-->

            <!--begin::Contact Form-->
            <div class="row">
              <!--begin::First Name-->
              <div class="col-md-6 mb-7">
                <label class="fs-6 fw-semibold mb-2 required">First Name</label>
                <input
                  v-model="newPatientData.first_name"
                  type="text"
                  class="form-control form-control-solid"
                  :class="{ 'is-invalid': errors.first_name }"
                  placeholder="First name"
                />
                <div v-if="errors.first_name" class="invalid-feedback">{{ errors.first_name }}</div>
              </div>
              <!--end::First Name-->

              <!--begin::Last Name-->
              <div class="col-md-6 mb-7">
                <label class="fs-6 fw-semibold mb-2 required">Last Name</label>
                <input
                  v-model="newPatientData.last_name"
                  type="text"
                  class="form-control form-control-solid"
                  :class="{ 'is-invalid': errors.last_name }"
                  placeholder="Last name"
                />
                <div v-if="errors.last_name" class="invalid-feedback">{{ errors.last_name }}</div>
              </div>
              <!--end::Last Name-->

              <!--begin::Email-->
              <div class="col-md-6 mb-7">
                <label class="fs-6 fw-semibold mb-2">Email</label>
                <input
                  v-model="newPatientData.email"
                  type="email"
                  class="form-control form-control-solid"
                  :class="{ 'is-invalid': errors.email }"
                  placeholder="Email address"
                />
                <div v-if="errors.email" class="invalid-feedback">{{ errors.email }}</div>
              </div>
              <!--end::Email-->

              <!--begin::Phone-->
              <div class="col-md-6 mb-7">
                <label class="fs-6 fw-semibold mb-2">Phone</label>
                <input
                  v-model="newPatientData.phone"
                  type="tel"
                  class="form-control form-control-solid"
                  :class="{ 'is-invalid': errors.phone }"
                  placeholder="Phone number"
                />
                <div v-if="errors.phone" class="invalid-feedback">{{ errors.phone }}</div>
              </div>
              <!--end::Phone-->

              <!--begin::Date of Birth-->
              <div class="col-md-6 mb-7">
                <label class="fs-6 fw-semibold mb-2">Date of Birth</label>
                <input
                  v-model="newPatientData.date_of_birth"
                  type="date"
                  class="form-control form-control-solid"
                  :class="{ 'is-invalid': errors.date_of_birth }"
                />
                <div v-if="errors.date_of_birth" class="invalid-feedback">{{ errors.date_of_birth }}</div>
              </div>
              <!--end::Date of Birth-->

              <!--begin::Nationality-->
              <div class="col-md-6 mb-7">
                <label class="fs-6 fw-semibold mb-2">Nationality</label>
                <input
                  v-model="newPatientData.nationality"
                  type="text"
                  class="form-control form-control-solid"
                  :class="{ 'is-invalid': errors.nationality }"
                  placeholder="Nationality"
                />
                <div v-if="errors.nationality" class="invalid-feedback">{{ errors.nationality }}</div>
              </div>
              <!--end::Nationality-->
            </div>
            <!--end::Contact Form-->
          </div>
          <!--end::Create New Patient-->
        </div>
        <!--end::Modal body-->

        <!--begin::Modal footer-->
        <div class="modal-footer">
          <button
            type="button"
            class="btn btn-light"
            data-bs-dismiss="modal"
            @click="closeModal"
          >
            Cancel
          </button>
          <button
            v-if="currentMode === 'search'"
            type="button"
            class="btn btn-primary"
            @click="assignExistingPatient"
            :disabled="!selectedPatient || assigning"
          >
            <span v-if="!assigning" class="indicator-label">
              Assign Patient to Trip
            </span>
            <span v-else class="indicator-progress">
              Assigning...
              <span class="spinner-border spinner-border-sm align-middle ms-2"></span>
            </span>
          </button>
          <button
            v-if="currentMode === 'create'"
            type="button"
            class="btn btn-primary"
            @click="createAndAssignPatient"
            :disabled="!isFormValid || creating"
          >
            <span v-if="!creating" class="indicator-label">
              Create & Assign Patient
            </span>
            <span v-else class="indicator-progress">
              Creating...
              <span class="spinner-border spinner-border-sm align-middle ms-2"></span>
            </span>
          </button>
        </div>
        <!--end::Modal footer-->
      </div>
      <!--end::Modal content-->
    </div>
    <!--end::Modal dialog-->
  </div>
  <!--end::Modal - Select/Create Patient-->
</template>

<script setup lang="ts">
import { ref, computed, nextTick } from 'vue';
import { hideModal } from '@/core/helpers/modal';
import PatientSearchSelect from '@/components/form-controls/PatientSearchSelect.vue';
import ApiService from '@/core/services/ApiService';
import Swal from 'sweetalert2/dist/sweetalert2.js';

interface Props {
  trip?: any;
  show?: boolean;
}

const props = defineProps<Props>();
const emit = defineEmits(['close', 'patient-assigned']);

const modalRef = ref<HTMLElement | null>(null);
const currentMode = ref<'selection' | 'search' | 'create'>('selection');
const selectedPatientId = ref<string | null>(null);
const selectedPatient = ref<any>(null);
const assigning = ref(false);
const creating = ref(false);

// New patient form data
const newPatientData = ref({
  first_name: '',
  last_name: '',
  email: '',
  phone: '',
  date_of_birth: '',
  nationality: ''
});

const errors = ref<Record<string, string>>({});

// Computed properties
const modalTitle = computed(() => {
  switch (currentMode.value) {
    case 'search': return 'Select Existing Patient';
    case 'create': return 'Create New Patient';
    default: return 'Add Patient to Trip';
  }
});

const isFormValid = computed(() => {
  return newPatientData.value.first_name.trim() !== '' &&
         newPatientData.value.last_name.trim() !== '';
});

// Methods
const setMode = (mode: 'selection' | 'search' | 'create') => {
  currentMode.value = mode;
  clearErrors();
};

const clearErrors = () => {
  errors.value = {};
};

const clearForm = () => {
  newPatientData.value = {
    first_name: '',
    last_name: '',
    email: '',
    phone: '',
    date_of_birth: '',
    nationality: ''
  };
  clearErrors();
};

const onPatientSelected = (patient: any) => {
  selectedPatient.value = patient;
};

const getPatientDisplayName = (patient: any): string => {
  if (!patient?.info) return 'Unknown Patient';

  const first = patient.info.first_name || patient.info.get_first_name || '';
  const last = patient.info.last_name || patient.info.get_last_name || '';

  return `${first} ${last}`.trim() || 'Unknown Patient';
};

const assignExistingPatient = async () => {
  if (!selectedPatient.value || !props.trip?.id) return;

  assigning.value = true;

  try {
    // Update the trip with the selected patient
    await ApiService.patch(`/trips/${props.trip.id}/`, {
      patient: selectedPatient.value.id,
      type: props.trip.type // Include required type field for validation
    });

    await Swal.fire({
      title: 'Success!',
      text: `${getPatientDisplayName(selectedPatient.value)} has been assigned to this trip.`,
      icon: 'success',
      confirmButtonText: 'OK'
    });

    emit('patient-assigned', selectedPatient.value);
    closeModal();

  } catch (error) {
    console.error('Error assigning patient to trip:', error);

    let errorMessage = 'Failed to assign patient to trip. Please try again.';
    if (error.response?.data) {
      if (typeof error.response.data === 'object') {
        errorMessage = JSON.stringify(error.response.data);
      } else {
        errorMessage = error.response.data.detail || error.response.data.message || error.response.data.toString();
      }
    }

    await Swal.fire({
      title: 'Error',
      text: errorMessage,
      icon: 'error',
      confirmButtonText: 'OK'
    });
  } finally {
    assigning.value = false;
  }
};

const createAndAssignPatient = async () => {
  if (!isFormValid.value || !props.trip?.id) return;

  creating.value = true;
  clearErrors();

  try {
    // Step 1: Create the contact
    const contactData = {
      first_name: newPatientData.value.first_name.trim(),
      last_name: newPatientData.value.last_name.trim(),
      email: newPatientData.value.email.trim() || null,
      phone: newPatientData.value.phone.trim() || null,
      date_of_birth: newPatientData.value.date_of_birth || null,
      nationality: newPatientData.value.nationality.trim() || null
    };

    const contactResponse = await ApiService.post('/contacts/', contactData);
    const createdContact = contactResponse.data;

    // Step 2: Create the patient from the contact
    const patientData = {
      info: createdContact.id,
      status: 'active',
      bed_at_origin: false,
      bed_at_destination: false,
      special_instructions: ''
    };

    const patientResponse = await ApiService.post('/patients/', patientData);
    const createdPatient = patientResponse.data;

    // Step 3: Assign the patient to the trip
    await ApiService.patch(`/trips/${props.trip.id}/`, {
      patient: createdPatient.id,
      type: props.trip.type // Include required type field for validation
    });

    await Swal.fire({
      title: 'Success!',
      text: `New patient ${getPatientDisplayName({ info: createdContact })} has been created and assigned to this trip.`,
      icon: 'success',
      confirmButtonText: 'OK'
    });

    // Emit the created patient with contact info
    const patientWithContact = {
      ...createdPatient,
      info: createdContact
    };

    emit('patient-assigned', patientWithContact);
    closeModal();

  } catch (error) {
    console.error('Error creating and assigning patient:', error);

    // Handle validation errors
    if (error.response?.status === 400 && error.response?.data) {
      const validationErrors = error.response.data;
      errors.value = validationErrors;
    } else {
      let errorMessage = 'Failed to create patient. Please try again.';
      if (error.response?.data) {
        if (typeof error.response.data === 'object') {
          errorMessage = JSON.stringify(error.response.data);
        } else {
          errorMessage = error.response.data.detail || error.response.data.message || error.response.data.toString();
        }
      }

      await Swal.fire({
        title: 'Error',
        text: errorMessage,
        icon: 'error',
        confirmButtonText: 'OK'
      });
    }
  } finally {
    creating.value = false;
  }
};

const closeModal = () => {
  hideModal(modalRef.value);
  emit('close');

  // Reset state
  currentMode.value = 'selection';
  selectedPatientId.value = null;
  selectedPatient.value = null;
  clearForm();
};
</script>

<style scoped>
.patient-option-card {
  transition: all 0.15s ease;
  border: 2px dashed var(--bs-border-color);
}

.patient-option-card:hover {
  border-color: var(--bs-primary);
  transform: translateY(-2px);
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
}

.cursor-pointer {
  cursor: pointer;
}
</style>