<template>
  <!--begin::Modal - Create patient from contact-->
  <div
    class="modal fade"
    id="kt_modal_create_patient_from_contact"
    ref="modalRef"
    tabindex="-1"
    aria-hidden="true"
  >
    <!--begin::Modal dialog-->
    <div class="modal-dialog modal-lg">
      <!--begin::Modal content-->
      <div class="modal-content">
        <!--begin::Modal header-->
        <div class="modal-header">
          <!--begin::Title-->
          <h2>Create Patient Record</h2>
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

        <!--begin::Modal body-->
        <div class="modal-body scroll-y mx-5 my-7">
          <!--begin::Form-->
          <form id="kt_modal_create_patient_from_contact_form" class="form" @submit.prevent="submitForm">
            
            <!--begin::Contact Info Display-->
            <div class="d-flex align-items-center bg-light-primary rounded p-6 mb-8">
              <div class="symbol symbol-50px me-5">
                <div class="symbol-label bg-primary">
                  <i class="ki-duotone ki-profile-user fs-2x text-white">
                    <span class="path1"></span>
                    <span class="path2"></span>
                    <span class="path3"></span>
                    <span class="path4"></span>
                  </i>
                </div>
              </div>
              <div class="flex-grow-1">
                <div class="fw-bold text-gray-800 fs-6">{{ contactDisplayName }}</div>
                <div class="text-muted fs-7">Creating patient record for this contact</div>
              </div>
            </div>
            <!--end::Contact Info Display-->

            <!--begin::Patient Status-->
            <div class="fv-row mb-8">
              <label class="required fs-6 fw-semibold mb-2">Patient Status</label>
              <select 
                name="status" 
                class="form-select form-select-solid" 
                v-model="formData.status"
                :disabled="isSubmitting"
              >
                <option value="pending">Pending</option>
                <option value="confirmed">Confirmed</option>
                <option value="active">Active</option>
                <option value="completed">Completed</option>
                <option value="cancelled">Cancelled</option>
              </select>
              <div class="form-text">Current status of this patient in the system</div>
            </div>
            <!--end::Patient Status-->

            <!--begin::Bed Requirements-->
            <div class="fv-row mb-8">
              <label class="fs-6 fw-semibold mb-4">Bed Requirements</label>
              <div class="row g-3">
                <div class="col-md-6">
                  <div class="form-check form-check-custom form-check-solid">
                    <input 
                      class="form-check-input" 
                      type="checkbox" 
                      v-model="formData.bed_at_origin"
                      id="bedOriginCheck"
                      :disabled="isSubmitting"
                    >
                    <label class="form-check-label fw-semibold text-gray-700" for="bedOriginCheck">
                      Bed required at origin
                    </label>
                  </div>
                  <div class="form-text text-muted fs-8">Patient needs bed/stretcher at pickup location</div>
                </div>
                <div class="col-md-6">
                  <div class="form-check form-check-custom form-check-solid">
                    <input 
                      class="form-check-input" 
                      type="checkbox" 
                      v-model="formData.bed_at_destination"
                      id="bedDestinationCheck"
                      :disabled="isSubmitting"
                    >
                    <label class="form-check-label fw-semibold text-gray-700" for="bedDestinationCheck">
                      Bed required at destination
                    </label>
                  </div>
                  <div class="form-text text-muted fs-8">Patient needs bed/stretcher at delivery location</div>
                </div>
              </div>
            </div>
            <!--end::Bed Requirements-->

            <!--begin::Special Instructions-->
            <div class="fv-row mb-8">
              <label class="fs-6 fw-semibold mb-2">Special Instructions</label>
              <textarea
                class="form-control form-control-solid"
                rows="6"
                name="special_instructions"
                placeholder="Enter any special medical instructions, requirements, or notes about this patient..."
                v-model="formData.special_instructions"
                :disabled="isSubmitting"
              ></textarea>
              <div class="form-text">Include any medical conditions, mobility requirements, equipment needs, or other important information for the medical team and crew.</div>
            </div>
            <!--end::Special Instructions-->
          </form>
          <!--end::Form-->
        </div>
        <!--end::Modal body-->

        <!--begin::Modal footer-->
        <div class="modal-footer flex-center">
          <!--begin::Button-->
          <button
            type="reset"
            class="btn btn-light me-3"
            data-bs-dismiss="modal"
            :disabled="isSubmitting"
            @click="resetForm"
          >
            Cancel
          </button>
          <!--end::Button-->

          <!--begin::Button-->
          <button
            type="submit"
            class="btn btn-primary"
            @click="submitForm"
            :disabled="isSubmitting"
          >
            <span v-if="!isSubmitting" class="indicator-label">
              Create Patient Record
              <KTIcon icon-name="arrow-right" icon-class="fs-3 ms-2" />
            </span>
            <span v-else class="indicator-progress">
              Creating...
              <span class="spinner-border spinner-border-sm align-middle ms-2"></span>
            </span>
          </button>
          <!--end::Button-->
        </div>
        <!--end::Modal footer-->
      </div>
      <!--end::Modal content-->
    </div>
    <!--end::Modal dialog-->
  </div>
  <!--end::Modal - Create patient from contact-->
</template>

<script setup lang="ts">
import { ref, reactive, computed } from "vue";
import Swal from "sweetalert2";
import ApiService from "@/core/services/ApiService";

interface Contact {
  id: string;
  first_name?: string;
  last_name?: string;
  business_name?: string;
  email?: string;
  phone?: string;
  date_of_birth?: string;
  nationality?: string;
  passport_number?: string;
  passport_expiration_date?: string;
}

const emit = defineEmits(['patientCreated', 'modalClosed']);

const modalRef = ref<HTMLElement | null>(null);
const isSubmitting = ref(false);
const contact = ref<Contact | null>(null);

// Form data
const formData = reactive({
  status: 'pending',
  bed_at_origin: false,
  bed_at_destination: false,
  special_instructions: '',
});

// Computed
const contactDisplayName = computed(() => {
  if (!contact.value) return 'Unknown Contact';
  
  const { first_name, last_name, business_name } = contact.value;
  
  if (business_name) return business_name;
  if (first_name || last_name) {
    return `${first_name || ''} ${last_name || ''}`.trim();
  }
  return contact.value.email || 'Unknown Contact';
});

// Methods
const setContact = (contactData: Contact) => {
  contact.value = contactData;
};

const resetForm = () => {
  Object.assign(formData, {
    status: 'pending',
    bed_at_origin: false,
    bed_at_destination: false,
    special_instructions: '',
  });
  
  contact.value = null;
};

const submitForm = async () => {
  if (!contact.value || isSubmitting.value) return;
  
  isSubmitting.value = true;
  
  try {
    // Use contact data to fill patient requirements
    const patientData = {
      info: contact.value.id,
      status: formData.status,
      bed_at_origin: formData.bed_at_origin,
      bed_at_destination: formData.bed_at_destination,
      special_instructions: formData.special_instructions?.trim() || null,
      // Use contact data for required fields, with fallbacks
      date_of_birth: contact.value.date_of_birth || new Date().toISOString().split('T')[0],
      nationality: contact.value.nationality || 'TBD',
      passport_number: contact.value.passport_number || 'TBD',
      passport_expiration_date: contact.value.passport_expiration_date || 
        new Date(Date.now() + 365*24*60*60*1000).toISOString().split('T')[0],
    };
    
    console.log('Creating patient from contact:', patientData);
    
    const response = await ApiService.post("/patients/", patientData);
    const newPatient = response.data;
    
    // Force close modal using multiple methods
    const modalElement = document.getElementById('kt_modal_create_patient_from_contact');
    if (modalElement) {
      // Method 1: Try Bootstrap modal instance
      try {
        if ((window as any).bootstrap?.Modal) {
          const modal = (window as any).bootstrap.Modal.getInstance(modalElement) || 
                       new (window as any).bootstrap.Modal(modalElement);
          modal.hide();
        }
      } catch (error) {
        console.log('Bootstrap patient modal hide failed:', error);
      }
      
      // Method 2: Force hide with direct DOM manipulation
      modalElement.classList.remove('show');
      modalElement.style.display = 'none';
      modalElement.setAttribute('aria-hidden', 'true');
      modalElement.removeAttribute('aria-modal');
      modalElement.removeAttribute('role');
    }
    
    // Method 3: Clean up all modal artifacts immediately
    setTimeout(() => {
      // Remove all modal backdrops
      const backdrops = document.querySelectorAll('.modal-backdrop');
      backdrops.forEach(backdrop => backdrop.remove());
      
      // Remove modal-open class from body and reset styles
      document.body.classList.remove('modal-open');
      document.body.style.removeProperty('overflow');
      document.body.style.removeProperty('padding-right');
      
      // Remove any aria-hidden from app
      const app = document.getElementById('app');
      if (app) {
        app.removeAttribute('aria-hidden');
      }
    }, 50);
    
    // Reset form
    resetForm();
    
    // Emit events
    emit('patientCreated', newPatient);
    emit('modalClosed');
    
    // Show success message after modal is closed
    setTimeout(() => {
      Swal.fire({
        title: "Success!",
        text: `Patient record created successfully for ${contactDisplayName.value}!`,
        icon: "success",
        confirmButtonText: "OK"
      });
    }, 200);
    
  } catch (error: any) {
    console.error('Error creating patient from contact:', error);
    console.error('Error response:', error.response?.data);
    
    let errorMessage = "Failed to create patient record. Please try again.";
    
    if (error.response?.data?.detail) {
      errorMessage = error.response.data.detail;
    } else if (error.response?.data) {
      const errors = error.response.data;
      const errorMessages = [];
      
      for (const field in errors) {
        if (Array.isArray(errors[field])) {
          errorMessages.push(`${field}: ${errors[field].join(', ')}`);
        } else {
          errorMessages.push(`${field}: ${errors[field]}`);
        }
      }
      
      if (errorMessages.length > 0) {
        errorMessage = errorMessages.join('\n');
      }
    }
    
    Swal.fire({
      title: "Error!",
      text: errorMessage,
      icon: "error",
      confirmButtonText: "OK"
    });
  } finally {
    isSubmitting.value = false;
  }
};

// Expose methods for parent components
defineExpose({
  setContact,
  resetForm
});
</script>

<style scoped>
.form-text {
  color: var(--bs-gray-600);
}
</style>