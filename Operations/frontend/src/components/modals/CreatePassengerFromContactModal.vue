<template>
  <!--begin::Modal - Create passenger from contact-->
  <div
    class="modal fade"
    id="kt_modal_create_passenger_from_contact"
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
          <h2>Create Passenger Record</h2>
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
          <form id="kt_modal_create_passenger_from_contact_form" class="form" @submit.prevent="submitForm">
            
            <!--begin::Contact Info Display-->
            <div class="d-flex align-items-center bg-light-primary rounded p-6 mb-8">
              <div class="symbol symbol-50px me-5">
                <div class="symbol-label bg-primary">
                  <i class="ki-duotone ki-people fs-2x text-white">
                    <span class="path1"></span>
                    <span class="path2"></span>
                    <span class="path3"></span>
                    <span class="path4"></span>
                    <span class="path5"></span>
                  </i>
                </div>
              </div>
              <div class="flex-grow-1">
                <div class="fw-bold text-gray-800 fs-6">{{ contactDisplayName }}</div>
                <div class="text-muted fs-7">Creating passenger record for this contact</div>
              </div>
            </div>
            <!--end::Contact Info Display-->

            <!--begin::Passenger Status-->
            <div class="fv-row mb-8">
              <label class="required fs-6 fw-semibold mb-2">Passenger Status</label>
              <select 
                name="status" 
                class="form-select form-select-solid" 
                v-model="formData.status"
                :disabled="isSubmitting"
              >
                <option value="active">Active</option>
                <option value="inactive">Inactive</option>
                <option value="pending">Pending</option>
                <option value="confirmed">Confirmed</option>
              </select>
              <div class="form-text">Current status of this passenger in the system</div>
            </div>
            <!--end::Passenger Status-->

            <!--begin::Travel Information-->
            <div class="separator separator-content my-8">
              <span class="w-250px fw-bold text-gray-600">Travel Information</span>
            </div>

            <div class="row g-9 mb-8">
              <div class="col-md-6 fv-row">
                <label class="fs-6 fw-semibold mb-2">Date of Birth</label>
                <input
                  type="date"
                  class="form-control form-control-solid"
                  v-model="formData.date_of_birth"
                  :disabled="isSubmitting"
                />
                <div class="form-text">Required for domestic and international travel</div>
              </div>
              <div class="col-md-6 fv-row">
                <label class="fs-6 fw-semibold mb-2">Nationality</label>
                <select
                  class="form-select form-select-solid"
                  v-model="formData.nationality"
                  :disabled="isSubmitting"
                >
                  <option value="">Select nationality</option>
                  <option value="American">American</option>
                  <option value="Canadian">Canadian</option>
                  <option value="British">British</option>
                  <option value="French">French</option>
                  <option value="German">German</option>
                  <option value="Spanish">Spanish</option>
                  <option value="Italian">Italian</option>
                  <option value="Australian">Australian</option>
                  <option value="Mexican">Mexican</option>
                  <option value="Other">Other</option>
                </select>
              </div>
            </div>

            <div class="row g-9 mb-8">
              <div class="col-md-6 fv-row">
                <label class="fs-6 fw-semibold mb-2">Passport Number</label>
                <input
                  type="text"
                  class="form-control form-control-solid"
                  placeholder="Passport number"
                  v-model="formData.passport_number"
                  :disabled="isSubmitting"
                />
                <div class="form-text">Required for international travel</div>
              </div>
              <div class="col-md-6 fv-row">
                <label class="fs-6 fw-semibold mb-2">Passport Expiration</label>
                <input
                  type="date"
                  class="form-control form-control-solid"
                  v-model="formData.passport_expiration_date"
                  :disabled="isSubmitting"
                />
                <div class="form-text">Must be valid for duration of travel</div>
              </div>
            </div>
            <!--end::Travel Information-->

            <!--begin::Contact Information-->
            <div class="separator separator-content my-8">
              <span class="w-250px fw-bold text-gray-600">Contact Information</span>
            </div>

            <div class="fv-row mb-8">
              <label class="fs-6 fw-semibold mb-2">Emergency Contact Number</label>
              <input
                type="tel"
                class="form-control form-control-solid"
                placeholder="Emergency contact phone number"
                v-model="formData.contact_number"
                :disabled="isSubmitting"
              />
              <div class="form-text">Alternative contact for emergencies during travel</div>
            </div>
            <!--end::Contact Information-->

            <!--begin::Notes-->
            <div class="fv-row mb-8">
              <label class="fs-6 fw-semibold mb-2">Passenger Notes</label>
              <textarea
                class="form-control form-control-solid"
                rows="4"
                name="notes"
                placeholder="Enter any special notes about this passenger (dietary restrictions, mobility requirements, medical considerations, etc.)"
                v-model="formData.notes"
                :disabled="isSubmitting"
              ></textarea>
              <div class="form-text">Include any special requirements, dietary restrictions, or other important information for travel arrangements.</div>
            </div>
            <!--end::Notes-->

            <!--begin::Info Notice-->
            <div class="notice d-flex bg-light-info rounded border-info border border-dashed p-6">
              <i class="ki-duotone ki-information fs-2tx text-info me-4">
                <span class="path1"></span>
                <span class="path2"></span>
                <span class="path3"></span>
              </i>
              <div class="d-flex flex-stack flex-grow-1">
                <div class="fw-semibold">
                  <h4 class="text-gray-900 fw-bold">Travel Documentation</h4>
                  <div class="fs-6 text-gray-700">Passport documents can be uploaded later through the Passenger Management page. Ensure all travel documents are current and valid.</div>
                </div>
              </div>
            </div>
            <!--end::Info Notice-->
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
              Create Passenger Record
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
  <!--end::Modal - Create passenger from contact-->
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

const emit = defineEmits(['passengerCreated', 'modalClosed']);

const modalRef = ref<HTMLElement | null>(null);
const isSubmitting = ref(false);
const contact = ref<Contact | null>(null);

// Form data
const formData = reactive({
  status: 'active',
  date_of_birth: '',
  nationality: '',
  passport_number: '',
  passport_expiration_date: '',
  contact_number: '',
  notes: '',
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
  
  // Pre-populate form with contact data if available
  if (contactData.date_of_birth) {
    formData.date_of_birth = contactData.date_of_birth;
  }
  if (contactData.nationality) {
    formData.nationality = contactData.nationality;
  }
  if (contactData.passport_number) {
    formData.passport_number = contactData.passport_number;
  }
  if (contactData.passport_expiration_date) {
    formData.passport_expiration_date = contactData.passport_expiration_date;
  }
};

const resetForm = () => {
  Object.assign(formData, {
    status: 'active',
    date_of_birth: '',
    nationality: '',
    passport_number: '',
    passport_expiration_date: '',
    contact_number: '',
    notes: '',
  });
  
  contact.value = null;
};

const submitForm = async () => {
  if (!contact.value || isSubmitting.value) return;
  
  isSubmitting.value = true;
  
  try {
    const passengerData = {
      info: contact.value.id,
      status: formData.status,
      date_of_birth: formData.date_of_birth || null,
      nationality: formData.nationality || null,
      passport_number: formData.passport_number || null,
      passport_expiration_date: formData.passport_expiration_date || null,
      contact_number: formData.contact_number || null,
      notes: formData.notes?.trim() || null,
    };
    
    console.log('Creating passenger from contact:', passengerData);
    
    const response = await ApiService.post("/passengers/", passengerData);
    const newPassenger = response.data;
    
    // Force close modal using multiple methods
    const modalElement = document.getElementById('kt_modal_create_passenger_from_contact');
    if (modalElement) {
      // Method 1: Try Bootstrap modal instance
      try {
        if ((window as any).bootstrap?.Modal) {
          const modal = (window as any).bootstrap.Modal.getInstance(modalElement) || 
                       new (window as any).bootstrap.Modal(modalElement);
          modal.hide();
        }
      } catch (error) {
        console.log('Bootstrap passenger modal hide failed:', error);
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
    emit('passengerCreated', newPassenger);
    emit('modalClosed');
    
    // Show success message after modal is closed
    setTimeout(() => {
      Swal.fire({
        title: "Success!",
        text: `Passenger record created successfully for ${contactDisplayName.value}!`,
        icon: "success",
        confirmButtonText: "OK"
      });
    }, 200);
    
  } catch (error: any) {
    console.error('Error creating passenger from contact:', error);
    console.error('Error response:', error.response?.data);
    
    let errorMessage = "Failed to create passenger record. Please try again.";
    
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

.separator-content {
  position: relative;
  z-index: 1;
}

.separator-content span {
  background: var(--bs-body-bg);
  padding: 0 1rem;
}

.notice {
  background-color: rgba(var(--bs-info-rgb), 0.1) !important;
}
</style>