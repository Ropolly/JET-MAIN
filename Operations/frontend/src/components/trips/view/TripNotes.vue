<template>
  <!--begin::Trip Notes Card-->
  <div class="card card-flush pt-3 mb-5 mb-xl-10">
    <!--begin::Card header-->
    <div class="card-header">
      <!--begin::Card title-->
      <div class="card-title">
        <h3 class="fw-bold">Trip Notes</h3>
      </div>
      <!--end::Card title-->

      <!--begin::Card toolbar-->
      <div class="card-toolbar" v-if="!loading && (tripData?.notes?.trim() || tripEditMode)">
        <button
          v-if="!tripEditMode"
          @click="startTripEdit"
          class="btn btn-sm btn-icon btn-light-primary"
          title="Edit trip notes"
        >
          <KTIcon icon-name="pencil" icon-class="fs-6" />
        </button>
      </div>
      <!--end::Card toolbar-->
    </div>
    <!--end::Card header-->

    <!--begin::Card body-->
    <div class="card-body pt-3">
      <!-- Loading State -->
      <div v-if="loading" class="text-center py-5">
        <span class="spinner-border spinner-border-lg"></span>
        <div class="text-muted mt-3">Loading notes...</div>
      </div>

      <!-- Edit Mode -->
      <div v-else-if="tripEditMode" class="mb-4">
        <form @submit.prevent="saveTripNotes">
          <div class="mb-4">
            <label class="form-label fw-semibold">Trip Notes</label>
            <textarea
              v-model="editedTripNotes"
              class="form-control form-control-solid"
              rows="5"
              placeholder="Add notes about this trip..."
            ></textarea>
          </div>

          <div class="d-flex justify-content-end gap-2">
            <button
              type="button"
              @click="cancelTripEdit"
              class="btn btn-sm btn-light"
              :disabled="isSubmitting"
            >
              Cancel
            </button>
            <button
              type="submit"
              class="btn btn-sm btn-primary"
              :disabled="isSubmitting"
            >
              <span v-if="!isSubmitting">Save Notes</span>
              <span v-else>
                <span class="spinner-border spinner-border-sm me-2"></span>
                Saving...
              </span>
            </button>
          </div>
        </form>
      </div>

      <!-- View Mode -->
      <div v-else>
        <div v-if="tripData?.notes && tripData.notes.trim()" class="text-gray-800">
          <div class="fs-6" style="white-space: pre-wrap; word-wrap: break-word;">{{ tripData.notes }}</div>
        </div>

        <!-- No Notes -->
        <div v-else class="text-center py-8">
          <KTIcon icon-name="notepad" icon-class="fs-3x text-muted mb-4" />
          <div class="text-muted fs-6">No notes added to this trip</div>
          <div class="text-muted fs-7">
            <button
              @click="startTripEdit"
              class="btn btn-sm btn-light-primary mt-3"
            >
              <KTIcon icon-name="plus" icon-class="fs-6 me-2" />
              Add Trip Notes
            </button>
          </div>
        </div>
      </div>
    </div>
    <!--end::Card body-->
  </div>
  <!--end::Trip Notes Card-->

  <!--begin::Patient Notes Card-->
  <div v-if="tripData?.patient" class="card card-flush pt-3 mb-5 mb-xl-10">
    <!--begin::Card header-->
    <div class="card-header">
      <!--begin::Card title-->
      <div class="card-title">
        <h3 class="fw-bold">Patient Notes</h3>
        <div class="text-muted fs-7 ms-3" v-if="getPatientName()">
          {{ getPatientName() }}
        </div>
      </div>
      <!--end::Card title-->

      <!--begin::Card toolbar-->
      <div class="card-toolbar" v-if="!loading && (getPatientNotes()?.trim() || patientEditMode)">
        <button
          v-if="!patientEditMode"
          @click="startPatientEdit"
          class="btn btn-sm btn-icon btn-light-success"
          title="Edit patient notes"
        >
          <KTIcon icon-name="pencil" icon-class="fs-6" />
        </button>
      </div>
      <!--end::Card toolbar-->
    </div>
    <!--end::Card header-->

    <!--begin::Card body-->
    <div class="card-body pt-3">
      <!-- Loading State -->
      <div v-if="loading" class="text-center py-5">
        <span class="spinner-border spinner-border-lg"></span>
        <div class="text-muted mt-3">Loading patient notes...</div>
      </div>

      <!-- Edit Mode -->
      <div v-else-if="patientEditMode" class="mb-4">
        <form @submit.prevent="savePatientNotes">
          <div class="mb-4">
            <label class="form-label fw-semibold">Patient Special Instructions/Notes</label>
            <textarea
              v-model="editedPatientNotes"
              class="form-control form-control-solid"
              rows="5"
              placeholder="Add special instructions or notes about this patient..."
            ></textarea>
          </div>

          <div class="d-flex justify-content-end gap-2">
            <button
              type="button"
              @click="cancelPatientEdit"
              class="btn btn-sm btn-light"
              :disabled="isSubmitting"
            >
              Cancel
            </button>
            <button
              type="submit"
              class="btn btn-sm btn-success"
              :disabled="isSubmitting"
            >
              <span v-if="!isSubmitting">Save Patient Notes</span>
              <span v-else>
                <span class="spinner-border spinner-border-sm me-2"></span>
                Saving...
              </span>
            </button>
          </div>
        </form>
      </div>

      <!-- View Mode -->
      <div v-else>
        <div v-if="getPatientNotes() && getPatientNotes().trim()" class="text-gray-800">
          <div class="fs-6" style="white-space: pre-wrap; word-wrap: break-word;">{{ getPatientNotes() }}</div>
        </div>

        <!-- No Notes -->
        <div v-else class="text-center py-8">
          <KTIcon icon-name="people" icon-class="fs-3x text-muted mb-4" />
          <div class="text-muted fs-6">No special instructions added for this patient</div>
          <div class="text-muted fs-7">
            <button
              @click="startPatientEdit"
              class="btn btn-sm btn-light-success mt-3"
            >
              <KTIcon icon-name="plus" icon-class="fs-6 me-2" />
              Add Patient Notes
            </button>
          </div>
        </div>
      </div>
    </div>
    <!--end::Card body-->
  </div>
  <!--end::Patient Notes Card-->
</template>

<script setup lang="ts">
import { ref } from 'vue';
import ApiService from '@/core/services/ApiService';
import Swal from 'sweetalert2';

interface Props {
  tripId: string;
  tripData?: any;
  loading?: boolean;
}

const props = defineProps<Props>();
const emit = defineEmits<{
  notesUpdated: [notes: string];
  patientUpdated: [patient: any];
}>();

// Trip notes edit state
const tripEditMode = ref(false);
const editedTripNotes = ref('');

// Patient notes edit state
const patientEditMode = ref(false);
const editedPatientNotes = ref('');

const isSubmitting = ref(false);

// Trip notes methods
const startTripEdit = () => {
  tripEditMode.value = true;
  editedTripNotes.value = props.tripData?.notes || '';
};

const cancelTripEdit = () => {
  tripEditMode.value = false;
  editedTripNotes.value = '';
};

const saveTripNotes = async () => {
  if (isSubmitting.value) return;

  isSubmitting.value = true;

  try {
    // Update the trip notes
    await ApiService.patch(`/trips/${props.tripId}/`, {
      notes: editedTripNotes.value,
      type: props.tripData?.type // Include required type field for validation
    });

    // Emit event to parent to refresh trip data
    emit('notesUpdated', editedTripNotes.value);

    // Exit edit mode
    tripEditMode.value = false;

    // Show success message
    Swal.fire({
      title: 'Success',
      text: 'Trip notes have been updated successfully',
      icon: 'success',
      timer: 2000,
      showConfirmButton: false
    });

  } catch (error: any) {
    console.error('Error updating trip notes:', error);

    Swal.fire({
      title: 'Error',
      text: error.response?.data?.message || 'Failed to update trip notes. Please try again.',
      icon: 'error',
      confirmButtonText: 'OK'
    });
  } finally {
    isSubmitting.value = false;
  }
};

// Patient notes methods
const startPatientEdit = () => {
  patientEditMode.value = true;
  editedPatientNotes.value = getPatientNotes() || '';
};

const cancelPatientEdit = () => {
  patientEditMode.value = false;
  editedPatientNotes.value = '';
};

const savePatientNotes = async () => {
  if (isSubmitting.value || !props.tripData?.patient?.id) return;

  isSubmitting.value = true;

  try {
    // Update the patient special instructions
    await ApiService.patch(`/patients/${props.tripData.patient.id}/`, {
      special_instructions: editedPatientNotes.value
    });

    // Update local data
    if (props.tripData?.patient) {
      props.tripData.patient.special_instructions = editedPatientNotes.value;
    }

    // Emit event to parent
    emit('patientUpdated', props.tripData.patient);

    // Exit edit mode
    patientEditMode.value = false;

    // Show success message
    Swal.fire({
      title: 'Success',
      text: 'Patient notes have been updated successfully',
      icon: 'success',
      timer: 2000,
      showConfirmButton: false
    });

  } catch (error: any) {
    console.error('Error updating patient notes:', error);

    Swal.fire({
      title: 'Error',
      text: error.response?.data?.message || 'Failed to update patient notes. Please try again.',
      icon: 'error',
      confirmButtonText: 'OK'
    });
  } finally {
    isSubmitting.value = false;
  }
};

// Helper methods
const getPatientName = (): string => {
  const patient = props.tripData?.patient;
  if (!patient?.info) return '';

  const firstName = patient.info.first_name || '';
  const lastName = patient.info.last_name || '';

  return `${firstName} ${lastName}`.trim() || patient.info.email || 'Patient';
};

const getPatientNotes = (): string => {
  return props.tripData?.patient?.special_instructions || '';
};

// Legacy compatibility - keeping old method names for backward compatibility
const startEdit = startTripEdit;
const cancelEdit = cancelTripEdit;
const saveNotes = saveTripNotes;
</script>