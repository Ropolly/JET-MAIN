<template>
  <div
    class="modal fade"
    id="kt_modal_lost_reason"
    ref="modalRef"
    tabindex="-1"
    aria-hidden="true"
  >
    <div class="modal-dialog modal-dialog-centered mw-650px">
      <div class="modal-content">
        <div class="modal-header">
          <h2 class="fw-bold">Mark Quote as Lost</h2>
          <div
            class="btn btn-icon btn-sm btn-active-icon-primary"
            data-bs-dismiss="modal"
          >
            <KTIcon icon-name="cross" icon-class="fs-1" />
          </div>
        </div>

        <div class="modal-body scroll-y mx-5 mx-xl-15 my-7">
          <form @submit.prevent="submitLostReason">
            <!-- Lost Reason Selection -->
            <div class="fv-row mb-7">
              <label class="required fw-semibold fs-6 mb-2">Lost Reason</label>
              <select
                v-if="!showNewReasonInput"
                v-model="selectedReasonId"
                class="form-select form-select-solid"
                required
              >
                <option value="">Select a reason...</option>
                <option v-for="reason in lostReasons" :key="reason.id" :value="reason.id">
                  {{ reason.reason }}
                </option>
                <option value="new">+ Add New Reason</option>
              </select>
              
              <div v-else class="d-flex gap-2">
                <input
                  v-model="newReason"
                  type="text"
                  class="form-control form-control-solid"
                  placeholder="Enter new reason (max 30 characters)"
                  maxlength="30"
                  required
                  @input="validateNewReason"
                />
                <button
                  type="button"
                  class="btn btn-light btn-active-light-primary"
                  @click="cancelNewReason"
                >
                  Cancel
                </button>
              </div>
              <div v-if="newReasonError" class="text-danger fs-7 mt-2">
                {{ newReasonError }}
              </div>
              <div v-if="showNewReasonInput" class="text-muted fs-7 mt-2">
                {{ newReason.length }}/30 characters
              </div>
            </div>

            <!-- Optional Comment -->
            <div class="fv-row mb-7">
              <label class="fw-semibold fs-6 mb-2">Additional Comments (Optional)</label>
              <textarea
                v-model="comment"
                class="form-control form-control-solid"
                rows="3"
                placeholder="Add any additional details about why this quote was lost..."
              ></textarea>
              <div class="text-muted fs-7 mt-2">
                This comment is optional and will be saved with the quote history.
              </div>
            </div>

            <!-- Action Buttons -->
            <div class="text-center pt-15">
              <button
                type="button"
                class="btn btn-light me-3"
                data-bs-dismiss="modal"
              >
                Cancel
              </button>
              <button
                type="submit"
                class="btn btn-danger"
                :disabled="isSubmitting || (!selectedReasonId && !newReason)"
              >
                <span v-if="!isSubmitting">Mark as Lost</span>
                <span v-else>
                  <span class="spinner-border spinner-border-sm me-2"></span>
                  Processing...
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
import { ref, onMounted, watch } from 'vue';
import { Modal } from 'bootstrap';
import ApiService from '@/core/services/ApiService';
import Swal from 'sweetalert2';

interface LostReason {
  id: string;
  reason: string;
  is_active: boolean;
}

const props = defineProps<{
  quoteId: string;
}>();

const emit = defineEmits<{
  confirmed: [reasonId: string, comment: string];
  cancelled: [];
}>();

const modalRef = ref<HTMLElement | null>(null);
const modal = ref<Modal | null>(null);
const lostReasons = ref<LostReason[]>([]);
const selectedReasonId = ref('');
const showNewReasonInput = ref(false);
const newReason = ref('');
const newReasonError = ref('');
const comment = ref('');
const isSubmitting = ref(false);

// Watch for selection changes
watch(selectedReasonId, (value) => {
  if (value === 'new') {
    showNewReasonInput.value = true;
    selectedReasonId.value = '';
    newReason.value = '';
  }
});

const validateNewReason = () => {
  newReasonError.value = '';
  if (newReason.value.length > 30) {
    newReasonError.value = 'Reason must be 30 characters or less';
  }
  // Check if reason already exists
  const exists = lostReasons.value.some(
    r => r.reason.toLowerCase() === newReason.value.toLowerCase()
  );
  if (exists) {
    newReasonError.value = 'This reason already exists';
  }
};

const cancelNewReason = () => {
  showNewReasonInput.value = false;
  newReason.value = '';
  newReasonError.value = '';
  selectedReasonId.value = '';
};

const loadLostReasons = async () => {
  try {
    const response = await ApiService.get('/lost-reasons/');
    lostReasons.value = response.data.results || response.data;
  } catch (error) {
    console.error('Error loading lost reasons:', error);
  }
};

const createNewReason = async (): Promise<string | null> => {
  try {
    const response = await ApiService.post('/lost-reasons/', {
      reason: newReason.value.trim()
    });
    // Add to local list
    lostReasons.value.push(response.data);
    return response.data.id;
  } catch (error: any) {
    console.error('Error creating new reason:', error);
    if (error.response?.data?.reason) {
      newReasonError.value = error.response.data.reason[0];
    } else {
      newReasonError.value = 'Failed to create new reason';
    }
    return null;
  }
};

const submitLostReason = async () => {
  if (!selectedReasonId.value && !newReason.value) {
    return;
  }

  isSubmitting.value = true;
  
  try {
    let reasonId = selectedReasonId.value;
    
    // If creating a new reason, do that first
    if (showNewReasonInput.value && newReason.value) {
      reasonId = await createNewReason() || '';
      if (!reasonId) {
        isSubmitting.value = false;
        return;
      }
    }
    
    // Emit the confirmation event with the reason ID and comment
    emit('confirmed', reasonId, comment.value);
    
    // Close the modal
    hideModal();
    
    // Reset form
    resetForm();
  } catch (error) {
    console.error('Error submitting lost reason:', error);
    Swal.fire({
      icon: 'error',
      title: 'Error',
      text: 'Failed to process lost reason. Please try again.'
    });
  } finally {
    isSubmitting.value = false;
  }
};

const showModal = () => {
  if (modal.value) {
    modal.value.show();
  }
};

const hideModal = () => {
  if (modal.value) {
    modal.value.hide();
  }
};

const resetForm = () => {
  selectedReasonId.value = '';
  showNewReasonInput.value = false;
  newReason.value = '';
  newReasonError.value = '';
  comment.value = '';
  isSubmitting.value = false;
};

onMounted(() => {
  if (modalRef.value) {
    modal.value = new Modal(modalRef.value);
    
    // Reset form when modal is hidden
    modalRef.value.addEventListener('hidden.bs.modal', () => {
      resetForm();
      emit('cancelled');
    });
  }
  
  // Load lost reasons
  loadLostReasons();
});

// Expose method to parent component
defineExpose({
  show: showModal,
  hide: hideModal
});
</script>