<template>
  <!--begin::Card-->
  <div class="card card-flush pt-3 mb-5 mb-xl-10">
    <!--begin::Card header-->
    <div class="card-header">
      <!--begin::Card title-->
      <div class="card-title">
        <h3 class="fw-bold">Trip Notes</h3>
      </div>
      <!--end::Card title-->
      
      <!--begin::Card toolbar-->
      <div class="card-toolbar" v-if="!loading && (tripData?.notes?.trim() || editMode)">
        <button 
          v-if="!editMode"
          @click="startEdit"
          class="btn btn-sm btn-icon btn-light-primary"
          title="Edit notes"
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
      <div v-else-if="editMode" class="mb-4">
        <form @submit.prevent="saveNotes">
          <div class="mb-4">
            <label class="form-label fw-semibold">Notes</label>
            <textarea
              v-model="editedNotes"
              class="form-control form-control-solid"
              rows="5"
              placeholder="Add notes about this trip..."
            ></textarea>
          </div>
          
          <div class="d-flex justify-content-end gap-2">
            <button 
              type="button" 
              @click="cancelEdit"
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
              @click="startEdit"
              class="btn btn-sm btn-light-primary mt-3"
            >
              <KTIcon icon-name="plus" icon-class="fs-6 me-2" />
              Add Notes
            </button>
          </div>
        </div>
      </div>
    </div>
    <!--end::Card body-->
  </div>
  <!--end::Card-->
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
}>();

// Edit state
const editMode = ref(false);
const editedNotes = ref('');
const isSubmitting = ref(false);

const startEdit = () => {
  editMode.value = true;
  editedNotes.value = props.tripData?.notes || '';
};

const cancelEdit = () => {
  editMode.value = false;
  editedNotes.value = '';
};

const saveNotes = async () => {
  if (isSubmitting.value) return;
  
  isSubmitting.value = true;
  
  try {
    // Update the trip notes
    await ApiService.patch(`/trips/${props.tripId}/`, {
      notes: editedNotes.value
    });
    
    // Emit event to parent to refresh trip data
    emit('notesUpdated', editedNotes.value);
    
    // Exit edit mode
    editMode.value = false;
    
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
</script>