<template>
  <!--begin::Modal - Create patient-->
  <div
    class="modal fade"
    id="kt_modal_create_patient"
    ref="modalRef"
    tabindex="-1"
    aria-hidden="true"
  >
    <!--begin::Modal dialog-->
    <div class="modal-dialog modal-xl">
      <!--begin::Modal content-->
      <div class="modal-content">
        <!--begin::Modal header-->
        <div class="modal-header">
          <!--begin::Title-->
          <h2>Add New Patient - Step 1 of 2</h2>
          <!--end::Title-->

          <!--begin::Close-->
          <div
            class="btn btn-sm btn-icon btn-active-color-primary"
            data-bs-dismiss="modal"
            @click="resetForm"
          >
            <KTIcon icon-name="cross" icon-class="fs-1" />
          </div>
          <!--end::Close-->
        </div>
        <!--end::Modal header-->

        <!--begin::Stepper-->
        <div class="stepper stepper-pills stepper-column d-flex flex-column flex-xl-row flex-row-fluid">
          <!--begin::Aside-->
          <div class="d-flex justify-content-center justify-content-xl-start flex-row-auto w-100 w-xl-300px w-xxl-400px me-9">
            <div class="px-6 px-lg-10 px-xxl-15 py-20">
              <!--begin::Nav-->
              <div class="stepper-nav">
                <!--begin::Step 1-->
                <div class="stepper-item current">
                  <div class="stepper-wrapper d-flex align-items-center">
                    <div class="stepper-icon w-40px h-40px">
                      <i class="stepper-check fas fa-check"></i>
                      <span class="stepper-number">1</span>
                    </div>
                    <div class="stepper-label">
                      <h3 class="stepper-title">Contact Information</h3>
                      <div class="stepper-desc">Create contact details</div>
                    </div>
                  </div>
                </div>
                <!--end::Step 1-->

                <!--begin::Step 2-->
                <div class="stepper-item">
                  <div class="stepper-wrapper d-flex align-items-center">
                    <div class="stepper-icon w-40px h-40px">
                      <i class="stepper-check fas fa-check"></i>
                      <span class="stepper-number">2</span>
                    </div>
                    <div class="stepper-label">
                      <h3 class="stepper-title">Patient Details</h3>
                      <div class="stepper-desc">Medical requirements</div>
                    </div>
                  </div>
                </div>
                <!--end::Step 2-->
              </div>
              <!--end::Nav-->
            </div>
          </div>
          <!--begin::Aside-->

          <!--begin::Content-->
          <div class="d-flex flex-row-fluid flex-center">
            <div class="py-20 w-100 w-lg-700px px-9">
              <!--begin::Loading State-->
              <div class="text-center">
                <div class="d-flex flex-column align-items-center">
                  <div class="spinner-border text-primary mb-4" role="status">
                    <span class="visually-hidden">Loading...</span>
                  </div>
                  <h4 class="text-gray-700">Opening Contact Form...</h4>
                  <p class="text-muted">Please wait while we prepare the contact creation form.</p>
                </div>
              </div>
              <!--end::Loading State-->
            </div>
          </div>
          <!--end::Content-->
        </div>
        <!--end::Stepper-->
      </div>
      <!--end::Modal content-->
    </div>
    <!--end::Modal dialog-->
  </div>
  <!--end::Modal - Create patient-->
</template>

<script setup lang="ts">
import { ref, onMounted } from "vue";

const emit = defineEmits(['openContactModal']);

const modalRef = ref<HTMLElement | null>(null);
const isSubmitting = ref(false);

const openContactModal = () => {
  // Close this modal and open contact modal
  const modalElement = modalRef.value;
  if (modalElement) {
    const modal = (window as any).bootstrap.Modal.getInstance(modalElement);
    if (modal) {
      modal.hide();
    }
  }
  
  // Emit to parent to open contact modal
  emit('openContactModal');
};

const resetForm = () => {
  // Nothing to reset in this simplified version
};

// Auto-open contact modal when this modal is shown
onMounted(() => {
  // Listen for when this modal is shown
  const modalElement = modalRef.value;
  if (modalElement) {
    modalElement.addEventListener('shown.bs.modal', () => {
      // Small delay to ensure modal is fully rendered
      setTimeout(() => {
        openContactModal();
      }, 300);
    });
  }
});
</script>

<style scoped>
.stepper-item.current .stepper-wrapper .stepper-icon {
  background-color: var(--bs-primary);
  color: white;
}

.stepper-item.completed .stepper-wrapper .stepper-icon {
  background-color: var(--bs-success);
  color: white;
}

.stepper-item.completed .stepper-wrapper .stepper-icon .stepper-number {
  display: none;
}

.stepper-item.completed .stepper-wrapper .stepper-icon .stepper-check {
  display: inline;
}

.stepper-item .stepper-wrapper .stepper-icon .stepper-check {
  display: none;
}
</style>