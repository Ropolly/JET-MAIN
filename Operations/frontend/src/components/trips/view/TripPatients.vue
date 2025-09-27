<template>
  <!--begin::Patients/PAX Content-->
  <div>
    <!--begin::Header-->
    <div class="d-flex justify-content-between align-items-center mb-6">
      <!--begin::Title-->
      <div>
        <h2 class="fw-bold">Patients & Passengers</h2>
      </div>
      <!--end::Title-->

      <!--begin::Toolbar-->
      <div>
        <button
          v-if="!trip?.patient"
          @click="showPatientSelectionModal"
          class="btn btn-primary btn-sm me-2"
        >
          <KTIcon icon-name="plus" icon-class="fs-6" />
          Add Patient
        </button>
        <button class="btn btn-light-primary btn-sm">
          <KTIcon icon-name="plus" icon-class="fs-6" />
          Add Passenger
        </button>
      </div>
      <!--end::Toolbar-->
    </div>
    <!--end::Header-->

    <!--begin::Content-->
    <div>
      <!--begin::Loading-->
      <div v-if="loading" class="d-flex justify-content-center py-5">
        <div class="spinner-border" role="status">
          <span class="visually-hidden">Loading...</span>
        </div>
      </div>
      <!--end::Loading-->

      <!--begin::Row-->
      <div v-if="!loading" class="row g-6 g-xl-9">
        <!--begin::Patient Card-->
        <div v-if="trip?.patient" class="col-md-6 col-xxl-4">
          <!--begin::Card-->
          <div class="card cursor-pointer" @click="openPatientDrawer">
            <!--begin::Card body-->
            <div class="card-body d-flex flex-center flex-column pt-12 p-9">
              <!--begin::Avatar-->
              <div class="symbol symbol-65px symbol-circle mb-5">
                <span class="symbol-label fs-2x fw-semibold text-danger bg-light-danger">
                  {{ getPatientInitials() }}
                </span>
              </div>
              <!--end::Avatar-->

              <!--begin::Name-->
              <a href="#" class="fs-4 text-gray-800 text-hover-primary fw-bold mb-0">{{ getPatientName() }}</a>
              <!--end::Name-->

              <!--begin::Position-->
              <div class="fw-semibold text-danger mb-6">Active Patient</div>
              <!--end::Position-->

              <!--begin::Info-->
              <div class="d-flex flex-center flex-wrap">
                <!--begin::Age-->
                <div v-if="trip.patient.info?.date_of_birth || trip.patient.info?.get_date_of_birth" class="border border-gray-300 border-dashed rounded min-w-80px py-3 px-4 mx-2 mb-3">
                  <div class="fs-6 fw-bold text-gray-700">{{ calculateAge(trip.patient.info?.get_date_of_birth || trip.patient.info?.date_of_birth) }}</div>
                  <div class="fw-semibold text-gray-500">Age</div>
                </div>
                <!--end::Age-->

                <!--begin::Origin Bed-->
                <div class="border border-gray-300 border-dashed rounded min-w-80px py-3 px-4 mx-2 mb-3">
                  <div class="fs-6 fw-bold">
                    <span v-if="trip.patient.bed_at_origin" class="text-success">✓</span>
                    <span v-else class="text-danger">✗</span>
                  </div>
                  <div class="fw-semibold text-gray-500">Origin Bed</div>
                </div>
                <!--end::Origin Bed-->

                <!--begin::Destination Bed-->
                <div class="border border-gray-300 border-dashed rounded min-w-80px py-3 px-4 mx-2 mb-3">
                  <div class="fs-6 fw-bold">
                    <span v-if="trip.patient.bed_at_destination" class="text-success">✓</span>
                    <span v-else class="text-danger">✗</span>
                  </div>
                  <div class="fw-semibold text-gray-500">Destination Bed</div>
                </div>
                <!--end::Destination Bed-->
              </div>
              <!--end::Info-->
            </div>
            <!--end::Card body-->
          </div>
          <!--end::Card-->
        </div>
        <!--end::Patient Card-->

        <!--begin::Passenger Cards-->
        <div v-for="(passenger, index) in getPassengers()" :key="passenger.id || index" class="col-md-6 col-xxl-4">
          <!--begin::Card-->
          <div class="card cursor-pointer" @click="openPassengerDrawer(passenger)">
            <!--begin::Card body-->
            <div class="card-body d-flex flex-center flex-column pt-12 p-9">
              <!--begin::Avatar-->
              <div class="symbol symbol-65px symbol-circle mb-5">
                <span class="symbol-label fs-2x fw-semibold text-info bg-light-info">
                  {{ getPassengerInitials(passenger) }}
                </span>
                <div class="bg-success position-absolute border border-4 border-body h-15px w-15px rounded-circle translate-middle start-100 top-100 ms-n3 mt-n3"></div>
              </div>
              <!--end::Avatar-->

              <!--begin::Name-->
              <a href="#" class="fs-4 text-gray-800 text-hover-primary fw-bold mb-0">{{ getPassengerName(passenger) }}</a>
              <!--end::Name-->

              <!--begin::Position-->
              <div class="fw-semibold text-gray-500 mb-6">{{ passenger.relationship || 'Passenger' }}</div>
              <!--end::Position-->

              <!--begin::Info-->
              <div class="d-flex flex-center flex-wrap">
                <!--begin::Age-->
                <div v-if="passenger.info?.date_of_birth || passenger.info?.get_date_of_birth" class="border border-gray-300 border-dashed rounded min-w-80px py-3 px-4 mx-2 mb-3">
                  <div class="fs-6 fw-bold text-gray-700">{{ calculateAge(passenger.info?.get_date_of_birth || passenger.info?.date_of_birth) }}</div>
                  <div class="fw-semibold text-gray-500">Age</div>
                </div>
                <!--end::Age-->

                <!--begin::Special Needs-->
                <div class="border border-gray-300 border-dashed rounded min-w-80px py-3 px-4 mx-2 mb-3">
                  <div class="fs-6 fw-bold text-gray-700">{{ passenger.special_needs ? 'Yes' : 'No' }}</div>
                  <div class="fw-semibold text-gray-500">Special Needs</div>
                </div>
                <!--end::Special Needs-->

                <!--begin::Contact-->
                <div v-if="(passenger.info?.phone || passenger.info?.email || passenger.info?.get_phone || passenger.info?.get_email)" class="border border-gray-300 border-dashed rounded min-w-80px py-3 px-4 mx-2 mb-3">
                  <div class="fs-6 fw-bold text-gray-700">{{ getPassengerContactCount(passenger) }}</div>
                  <div class="fw-semibold text-gray-500">Contact Info</div>
                </div>
                <!--end::Contact-->
              </div>
              <!--end::Info-->
            </div>
            <!--end::Card body-->
          </div>
          <!--end::Card-->
        </div>
        <!--end::Passenger Cards-->

        <!--begin::No Data Message-->
        <div v-if="!trip?.patient && !hasPassengers()" class="col-12">
          <div class="text-center py-10">
            <i class="fas fa-user-friends fs-3x text-muted mb-4"></i>
            <p class="text-muted">No patients or passengers assigned yet</p>
            <button @click="showPatientSelectionModal" type="button" class="btn btn-primary">
              <i class="fas fa-plus fs-4 me-2"></i>
              Add Patient
            </button>
          </div>
        </div>
        <!--end::No Data Message-->
      </div>
      <!--end::Row-->
    </div>
    <!--end::Content-->
  </div>
  <!--end::Patients/PAX Content-->

  <!--begin::Patient/Passenger Drawer-->
  <div
    v-if="showDrawer"
    class="bg-body drawer drawer-end drawer-on"
    id="patient_drawer"
    style="width: 400px;"
  >
    <!--begin::Card-->
    <div class="card w-100 rounded-0 border-0" id="patient_drawer_card">
      <!--begin::Card header-->
      <div class="card-header pe-5">
        <!--begin::Title-->
        <div class="card-title">
          <div class="d-flex justify-content-center flex-column me-3">
            <span class="fs-4 fw-bold text-gray-900 text-hover-primary me-1 lh-1">
              {{ drawerData?.type === 'patient' ? 'Patient Details' : 'Passenger Details' }}
            </span>
          </div>
        </div>
        <!--end::Title-->

        <!--begin::Card toolbar-->
        <div class="card-toolbar">
          <!--begin::Close-->
          <div class="btn btn-sm btn-icon btn-active-light-primary" @click="closeDrawer">
            <KTIcon icon-name="cross" icon-class="fs-2" />
          </div>
          <!--end::Close-->
        </div>
        <!--end::Card toolbar-->
      </div>
      <!--end::Card header-->

      <!--begin::Card body-->
      <div class="card-body hover-scroll-overlay-y pe-5 me-n5" style="height: calc(100vh - 95px)">
        <div v-if="drawerData">
          <!--begin::Avatar and Name-->
          <div class="d-flex flex-center flex-column mb-8">
            <div class="symbol symbol-100px symbol-circle mb-5">
              <span
                :class="drawerData.type === 'patient'
                  ? 'symbol-label fs-1 fw-semibold text-danger bg-light-danger'
                  : 'symbol-label fs-1 fw-semibold text-info bg-light-info'"
              >
                {{ drawerData.initials }}
              </span>
            </div>
            <h3 class="text-gray-900 fw-bold mb-1">{{ drawerData.name }}</h3>
            <div
              :class="drawerData.type === 'patient'
                ? 'fw-semibold text-danger'
                : 'fw-semibold text-gray-500'"
            >
              {{ drawerData.type === 'patient' ? 'Active Patient' : (drawerData.relationship || 'Passenger') }}
            </div>
          </div>
          <!--end::Avatar and Name-->

          <!--begin::Details-->
          <div class="separator separator-dashed my-6"></div>

          <!--begin::Personal Information-->
          <div class="mb-8">
            <h4 class="fw-bold text-gray-900 mb-4">Personal Information</h4>

            <div v-if="drawerData.age" class="d-flex align-items-center mb-3">
              <span class="fw-semibold text-gray-600 me-3" style="width: 80px;">Age:</span>
              <span class="text-gray-900">{{ drawerData.age }}</span>
            </div>

            <div v-if="drawerData.dateOfBirth" class="d-flex align-items-center mb-3">
              <span class="fw-semibold text-gray-600 me-3" style="width: 80px;">DOB:</span>
              <span class="text-gray-900">{{ formatDate(drawerData.dateOfBirth) }}</span>
            </div>

            <div v-if="drawerData.nationality" class="d-flex align-items-center mb-3">
              <span class="fw-semibold text-gray-600 me-3" style="width: 80px;">Nationality:</span>
              <span class="text-gray-900">{{ drawerData.nationality }}</span>
            </div>
          </div>
          <!--end::Personal Information-->

          <!--begin::Contact Information-->
          <div v-if="drawerData.phone || drawerData.email" class="mb-8">
            <h4 class="fw-bold text-gray-900 mb-4">Contact Information</h4>

            <div v-if="drawerData.phone" class="d-flex align-items-center mb-3">
              <span class="fw-semibold text-gray-600 me-3" style="width: 80px;">Phone:</span>
              <span class="text-gray-900">{{ drawerData.phone }}</span>
            </div>

            <div v-if="drawerData.email" class="d-flex align-items-center mb-3">
              <span class="fw-semibold text-gray-600 me-3" style="width: 80px;">Email:</span>
              <span class="text-gray-900">{{ drawerData.email }}</span>
            </div>
          </div>
          <!--end::Contact Information-->

          <!--begin::Medical Information (Patient only)-->
          <div v-if="drawerData.type === 'patient'" class="mb-8">
            <h4 class="fw-bold text-gray-900 mb-4">Medical Information</h4>

            <div class="d-flex align-items-center mb-3">
              <span class="fw-semibold text-gray-600 me-3" style="width: 120px;">Origin Bed:</span>
              <span v-if="drawerData.bedAtOrigin" class="badge badge-light-success">Required</span>
              <span v-else class="badge badge-light-danger">Not Required</span>
            </div>

            <div class="d-flex align-items-center mb-3">
              <span class="fw-semibold text-gray-600 me-3" style="width: 120px;">Destination Bed:</span>
              <span v-if="drawerData.bedAtDestination" class="badge badge-light-success">Required</span>
              <span v-else class="badge badge-light-danger">Not Required</span>
            </div>

            <div v-if="drawerData.specialInstructions" class="mb-3">
              <span class="fw-semibold text-gray-600 d-block mb-2">Special Instructions:</span>
              <div class="p-3 rounded bg-light">
                <span class="text-gray-900">{{ drawerData.specialInstructions }}</span>
              </div>
            </div>
          </div>
          <!--end::Medical Information-->

          <!--begin::Special Needs (Passenger only)-->
          <div v-if="drawerData.type === 'passenger'" class="mb-8">
            <h4 class="fw-bold text-gray-900 mb-4">Additional Information</h4>

            <div class="d-flex align-items-center mb-3">
              <span class="fw-semibold text-gray-600 me-3" style="width: 120px;">Special Needs:</span>
              <span v-if="drawerData.specialNeeds" class="badge badge-light-warning">Yes</span>
              <span v-else class="badge badge-light-success">No</span>
            </div>
          </div>
          <!--end::Special Needs-->
        </div>
      </div>
      <!--end::Card body-->
    </div>
    <!--end::Card-->
  </div>
  <!--end::Patient/Passenger Drawer-->

  <!--begin::Drawer Overlay-->
  <div
    v-if="showDrawer"
    class="drawer-overlay"
    @click="closeDrawer"
    style="position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.5); z-index: 104;"
  ></div>
  <!--end::Drawer Overlay-->

  <!--begin::Patient Selection Modal-->
  <PatientSelectionModal
    :trip="trip"
    :show="showPatientModal"
    @close="onPatientModalClose"
    @patient-assigned="onPatientAssigned"
  />
  <!--end::Patient Selection Modal-->
</template>

<script setup lang="ts">
import { ref } from 'vue';
import PatientSelectionModal from '@/components/modals/PatientSelectionModal.vue';
import { showModal } from '@/core/helpers/modal';

interface Props {
  trip: any;
  loading: boolean;
}

const props = defineProps<Props>();
const emit = defineEmits(['trip-updated']);

// Drawer state
const showDrawer = ref(false);
const drawerData = ref<any>(null);

// Patient modal state
const showPatientModal = ref(false);

// Patient helper functions
const getPatientName = (): string => {
  if (!props.trip?.patient?.info) return 'Unknown Patient';

  // Try decrypted fields first, then fall back to regular fields
  const first = props.trip.patient.info.get_first_name || props.trip.patient.info.first_name || '';
  const last = props.trip.patient.info.get_last_name || props.trip.patient.info.last_name || '';

  return `${first} ${last}`.trim() || 'Unknown Patient';
};

const getPatientInitials = (): string => {
  if (!props.trip?.patient?.info) return '?';

  // Try decrypted fields first, then fall back to regular fields
  const first = props.trip.patient.info.get_first_name || props.trip.patient.info.first_name || '';
  const last = props.trip.patient.info.get_last_name || props.trip.patient.info.last_name || '';

  return `${first.charAt(0)}${last.charAt(0)}`.toUpperCase() || '?';
};

const getPatientAddress = (): string => {
  if (!props.trip?.patient) return '';

  const address = props.trip.patient.address;
  if (typeof address === 'string') {
    return address;
  }

  if (typeof address === 'object' && address) {
    const parts = [
      address.street,
      address.city,
      address.state,
      address.zip_code
    ].filter(Boolean);

    return parts.join(', ');
  }

  return '';
};

const hasSpecialInstructions = (): boolean => {
  return !!(props.trip?.patient?.special_instructions);
};

// Passenger helper functions
const getPassengers = (): any[] => {
  return props.trip?.passengers || [];
};

const hasPassengers = (): boolean => {
  return getPassengers().length > 0;
};

const getPassengerCount = (): number => {
  return getPassengers().length;
};

const getPassengerName = (passenger: any): string => {
  if (!passenger?.info) return 'Unknown';

  // Try decrypted fields first, then fall back to regular fields
  const first = passenger.info.get_first_name || passenger.info.first_name || '';
  const last = passenger.info.get_last_name || passenger.info.last_name || '';

  return `${first} ${last}`.trim() || 'Unknown';
};

const getPassengerInitials = (passenger: any): string => {
  if (!passenger?.info) return '?';

  // Try decrypted fields first, then fall back to regular fields
  const first = passenger.info.get_first_name || passenger.info.first_name || '';
  const last = passenger.info.get_last_name || passenger.info.last_name || '';

  return `${first.charAt(0)}${last.charAt(0)}`.toUpperCase() || '?';
};

// Utility functions
const calculateAge = (dateOfBirth: string): number | string => {
  if (!dateOfBirth) return 'Unknown';

  try {
    const birthDate = new Date(dateOfBirth);
    const today = new Date();
    let age = today.getFullYear() - birthDate.getFullYear();
    const monthDiff = today.getMonth() - birthDate.getMonth();

    if (monthDiff < 0 || (monthDiff === 0 && today.getDate() < birthDate.getDate())) {
      age--;
    }

    return age;
  } catch (error) {
    return 'Unknown';
  }
};

const getTotalPeople = (): number => {
  let count = 0;

  if (props.trip?.patient) count++;
  count += getPassengerCount();

  return count;
};

const getMedicalNeedsCount = (): number => {
  let count = 0;

  if (props.trip?.patient) {
    if (props.trip.patient.bed_at_origin) count++;
    if (props.trip.patient.bed_at_destination) count++;
    if (hasSpecialInstructions()) count++;
  }

  // Count passengers with special needs
  getPassengers().forEach(passenger => {
    if (passenger.special_needs) count++;
  });

  return count;
};

const getSpecialRequirementsCount = (): number => {
  let count = 0;

  if (hasSpecialInstructions()) count++;

  getPassengers().forEach(passenger => {
    if (passenger.special_needs) count++;
  });

  return count;
};

const getPatientMedicalNeedsCount = (): number => {
  let count = 0;

  if (props.trip?.patient) {
    if (props.trip.patient.bed_at_origin) count++;
    if (props.trip.patient.bed_at_destination) count++;
    if (hasSpecialInstructions()) count++;
  }

  return count;
};

const getPatientContactCount = (): number => {
  let count = 0;

  if (props.trip?.patient?.info) {
    // Check both encrypted and regular fields
    if (props.trip.patient.info.get_phone || props.trip.patient.info.phone) count++;
    if (props.trip.patient.info.get_email || props.trip.patient.info.email) count++;
  }

  return count;
};

const getPassengerContactCount = (passenger: any): number => {
  let count = 0;

  if (!passenger?.info) return count;

  // Check both encrypted and regular fields
  if (passenger.info.get_phone || passenger.info.phone) count++;
  if (passenger.info.get_email || passenger.info.email) count++;

  return count;
};

// Drawer methods
const openPatientDrawer = () => {
  if (!props.trip?.patient) return;

  const patient = props.trip.patient;
  const patientInfo = patient.info;

  drawerData.value = {
    type: 'patient',
    name: getPatientName(),
    initials: getPatientInitials(),
    age: patientInfo?.get_date_of_birth || patientInfo?.date_of_birth ? calculateAge(patientInfo?.get_date_of_birth || patientInfo?.date_of_birth) : null,
    dateOfBirth: patientInfo?.get_date_of_birth || patientInfo?.date_of_birth,
    nationality: patientInfo?.get_nationality || patientInfo?.nationality,
    phone: patientInfo?.get_phone || patientInfo?.phone,
    email: patientInfo?.get_email || patientInfo?.email,
    bedAtOrigin: patient.bed_at_origin,
    bedAtDestination: patient.bed_at_destination,
    specialInstructions: patient.get_special_instructions || patient.special_instructions
  };

  showDrawer.value = true;
};

const openPassengerDrawer = (passenger: any) => {
  if (!passenger?.info) return;

  const passengerInfo = passenger.info;

  drawerData.value = {
    type: 'passenger',
    name: getPassengerName(passenger),
    initials: getPassengerInitials(passenger),
    relationship: passenger.relationship,
    age: passengerInfo?.get_date_of_birth || passengerInfo?.date_of_birth ? calculateAge(passengerInfo?.get_date_of_birth || passengerInfo?.date_of_birth) : null,
    dateOfBirth: passengerInfo?.get_date_of_birth || passengerInfo?.date_of_birth,
    nationality: passengerInfo?.get_nationality || passengerInfo?.nationality,
    phone: passengerInfo?.get_phone || passengerInfo?.phone,
    email: passengerInfo?.get_email || passengerInfo?.email,
    specialNeeds: passenger.special_needs
  };

  showDrawer.value = true;
};

const closeDrawer = () => {
  showDrawer.value = false;
  drawerData.value = null;
};

const formatDate = (dateString: string): string => {
  if (!dateString) return '';

  try {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'long',
      day: 'numeric'
    });
  } catch (error) {
    return dateString;
  }
};

// Patient modal functions
const showPatientSelectionModal = async () => {
  showPatientModal.value = true;
  // Use showModal helper to show the modal
  const modalElement = document.getElementById('kt_modal_patient_selection');
  if (modalElement) {
    showModal(modalElement);
  }
};

const onPatientModalClose = () => {
  showPatientModal.value = false;
};

const onPatientAssigned = (patient: any) => {
  console.log('Patient assigned:', patient);
  showPatientModal.value = false;
  // Emit event to parent to refresh trip data
  emit('trip-updated');
};
</script>

<style scoped>
.symbol-label {
  font-size: 0.875rem;
}

.cursor-pointer {
  cursor: pointer;
}

.drawer {
  position: fixed;
  top: 0;
  right: 0;
  height: 100vh;
  z-index: 105;
  overflow-y: auto;
  box-shadow: -5px 0 15px rgba(0, 0, 0, 0.1);
}

.card:hover {
  transform: translateY(-2px);
  transition: transform 0.2s ease-in-out;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}
</style>