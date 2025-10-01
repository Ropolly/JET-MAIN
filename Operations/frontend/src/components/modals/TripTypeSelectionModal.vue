<template>
  <!--begin::Modal - Select Trip Type-->
  <div
    class="modal fade"
    id="kt_modal_select_trip_type"
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
          <h2>Select Trip Type</h2>
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
          <!--begin::Description-->
          <div class="text-center mb-8">
            <p class="text-gray-600 fs-5">
              Choose the type of trip you want to create. This will help us provide the right options and workflow for your needs.
            </p>
          </div>
          <!--end::Description-->

          <!--begin::Trip Types-->
          <div class="row g-6">
            <!--begin::Medical Trip-->
            <div class="col-md-6">
              <div
                class="card card-dashed h-100 cursor-pointer trip-type-card"
                :class="{ 'border-primary': selectedType === 'medical' }"
                @click="selectTripType('medical')"
              >
                <div class="card-body d-flex flex-column align-items-center text-center p-6">
                  <KTIcon icon-name="heart" icon-class="fs-2x text-danger mb-4" />
                  <h4 class="text-gray-900 fw-bold mb-0">Medical Transport</h4>
                </div>
              </div>
            </div>
            <!--end::Medical Trip-->

            <!--begin::Charter Trip-->
            <div class="col-md-6">
              <div
                class="card card-dashed h-100 cursor-pointer trip-type-card"
                :class="{ 'border-primary': selectedType === 'charter' }"
                @click="selectTripType('charter')"
              >
                <div class="card-body d-flex flex-column align-items-center text-center p-6">
                  <KTIcon icon-name="airplane" icon-class="fs-2x text-primary mb-4" />
                  <h4 class="text-gray-900 fw-bold mb-0">Charter Flight</h4>
                </div>
              </div>
            </div>
            <!--end::Charter Trip-->

            <!--begin::Part 91 Trip-->
            <div class="col-md-6">
              <div
                class="card card-dashed h-100 cursor-pointer trip-type-card"
                :class="{ 'border-primary': selectedType === 'part 91' }"
                @click="selectTripType('part 91')"
              >
                <div class="card-body d-flex flex-column align-items-center text-center p-6">
                  <KTIcon icon-name="user" icon-class="fs-2x text-success mb-4" />
                  <h4 class="text-gray-900 fw-bold mb-0">Part 91 Flight</h4>
                </div>
              </div>
            </div>
            <!--end::Part 91 Trip-->

            <!--begin::Other Trip-->
            <div class="col-md-6">
              <div
                class="card card-dashed h-100 cursor-pointer trip-type-card"
                :class="{ 'border-primary': selectedType === 'other' }"
                @click="selectTripType('other')"
              >
                <div class="card-body d-flex flex-column align-items-center text-center p-6">
                  <KTIcon icon-name="setting-3" icon-class="fs-2x text-warning mb-4" />
                  <h4 class="text-gray-900 fw-bold mb-0">Other</h4>
                </div>
              </div>
            </div>
            <!--end::Other Trip-->
          </div>
          <!--end::Trip Types-->
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
            type="button"
            class="btn btn-primary"
            @click="createTrip"
            :disabled="!selectedType || creating"
          >
            <span v-if="!creating" class="indicator-label">
              Create {{ getTripTypeLabel() }} Trip
            </span>
            <span v-else class="indicator-progress">
              Creating Trip...
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
  <!--end::Modal - Select Trip Type-->
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { hideModal } from '@/core/helpers/modal';

interface Props {
  show?: boolean;
}

const props = defineProps<Props>();
const emit = defineEmits(['close', 'trip-type-selected']);

const modalRef = ref<HTMLElement | null>(null);
const selectedType = ref<string>('');
const creating = ref(false);

// Trip type selection
const selectTripType = (type: string) => {
  selectedType.value = type;
};

// Get trip type label for display
const getTripTypeLabel = (): string => {
  switch (selectedType.value) {
    case 'medical': return 'Medical Transport';
    case 'charter': return 'Charter';
    case 'part 91': return 'Part 91';
    case 'other': return 'Other';
    default: return '';
  }
};

// Create trip with selected type
const createTrip = () => {
  if (!selectedType.value) return;

  creating.value = true;
  // Emit the trip type BEFORE closing modal (which resets selectedType)
  emit('trip-type-selected', selectedType.value);
  // Close the modal after emitting
  closeModal();
};

// Close modal
const closeModal = () => {
  hideModal(modalRef.value);
  emit('close');

  // Reset state
  selectedType.value = '';
  creating.value = false;
};
</script>

<style scoped>
.trip-type-card {
  transition: all 0.15s ease;
  border: 2px dashed var(--bs-border-color);
}

.trip-type-card:hover {
  border-color: var(--bs-primary);
  transform: translateY(-2px);
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
}

.trip-type-card.border-primary {
  border-color: var(--bs-primary) !important;
  background-color: rgba(var(--bs-primary-rgb), 0.05);
}

.cursor-pointer {
  cursor: pointer;
}
</style>