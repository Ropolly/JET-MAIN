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
          <h2>Create New Patient</h2>
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
          <form id="kt_modal_create_patient_form" class="form" @submit.prevent="submitForm">

            <!--begin::Contact Information-->
            <div class="separator separator-content my-14">
              <span class="w-250px fw-bold text-gray-600">Contact Information</span>
            </div>

            <!--begin::Name and Email-->
            <div class="row g-9 mb-8">
              <div class="col-md-6 fv-row">
                <label class="required fs-6 fw-semibold mb-2">First Name</label>
                <input
                  type="text"
                  class="form-control form-control-solid"
                  placeholder="Enter first name"
                  v-model="formData.contact.first_name"
                  :disabled="isSubmitting"
                />
              </div>
              <div class="col-md-6 fv-row">
                <label class="required fs-6 fw-semibold mb-2">Last Name</label>
                <input
                  type="text"
                  class="form-control form-control-solid"
                  placeholder="Enter last name"
                  v-model="formData.contact.last_name"
                  :disabled="isSubmitting"
                />
              </div>
            </div>
            <!--end::Name and Email-->

            <!--begin::Email and Phone-->
            <div class="row g-9 mb-8">
              <div class="col-md-6 fv-row">
                <label class="fs-6 fw-semibold mb-2">Email</label>
                <input
                  type="email"
                  class="form-control form-control-solid"
                  placeholder="Enter email address"
                  v-model="formData.contact.email"
                  :disabled="isSubmitting"
                />
              </div>
              <div class="col-md-6 fv-row">
                <label class="fs-6 fw-semibold mb-2">Phone</label>
                <input
                  type="tel"
                  class="form-control form-control-solid"
                  placeholder="Enter phone number"
                  v-model="formData.contact.phone"
                  :disabled="isSubmitting"
                />
              </div>
            </div>
            <!--end::Email and Phone-->

            <!--begin::Date of Birth and Nationality-->
            <div class="row g-9 mb-8">
              <div class="col-md-6 fv-row">
                <label class="fs-6 fw-semibold mb-2">Date of Birth</label>
                <input
                  type="date"
                  class="form-control form-control-solid"
                  v-model="formData.contact.date_of_birth"
                  :disabled="isSubmitting"
                />
              </div>
              <div class="col-md-6 fv-row">
                <label class="fs-6 fw-semibold mb-2">Nationality</label>
                <input
                  type="text"
                  class="form-control form-control-solid"
                  placeholder="Enter nationality"
                  v-model="formData.contact.nationality"
                  :disabled="isSubmitting"
                />
              </div>
            </div>
            <!--end::Date of Birth and Nationality-->

            <!--begin::Passport Information-->
            <div class="row g-9 mb-8">
              <div class="col-md-6 fv-row">
                <label class="fs-6 fw-semibold mb-2">Passport Number</label>
                <input
                  type="text"
                  class="form-control form-control-solid"
                  placeholder="Enter passport number"
                  v-model="formData.contact.passport_number"
                  :disabled="isSubmitting"
                />
              </div>
              <div class="col-md-6 fv-row">
                <label class="fs-6 fw-semibold mb-2">Passport Expiration Date</label>
                <input
                  type="date"
                  class="form-control form-control-solid"
                  v-model="formData.contact.passport_expiration_date"
                  :disabled="isSubmitting"
                />
              </div>
            </div>
            <!--end::Passport Information-->

            <!--begin::Address-->
            <div class="row g-9 mb-8">
              <div class="col-md-12 fv-row">
                <label class="fs-6 fw-semibold mb-2">Address Line 1</label>
                <input
                  type="text"
                  class="form-control form-control-solid"
                  placeholder="Enter street address"
                  v-model="formData.contact.address_line1"
                  :disabled="isSubmitting"
                />
              </div>
            </div>
            <div class="row g-9 mb-8">
              <div class="col-md-6 fv-row">
                <label class="fs-6 fw-semibold mb-2">Address Line 2</label>
                <input
                  type="text"
                  class="form-control form-control-solid"
                  placeholder="Apartment, suite, etc. (optional)"
                  v-model="formData.contact.address_line2"
                  :disabled="isSubmitting"
                />
              </div>
              <div class="col-md-6 fv-row">
                <label class="fs-6 fw-semibold mb-2">City</label>
                <input
                  type="text"
                  class="form-control form-control-solid"
                  placeholder="Enter city"
                  v-model="formData.contact.city"
                  :disabled="isSubmitting"
                />
              </div>
            </div>
            <div class="row g-9 mb-8">
              <div class="col-md-4 fv-row">
                <label class="fs-6 fw-semibold mb-2">State/Province</label>
                <input
                  type="text"
                  class="form-control form-control-solid"
                  placeholder="Enter state/province"
                  v-model="formData.contact.state"
                  :disabled="isSubmitting"
                />
              </div>
              <div class="col-md-4 fv-row">
                <label class="fs-6 fw-semibold mb-2">Postal Code</label>
                <input
                  type="text"
                  class="form-control form-control-solid"
                  placeholder="Enter postal code"
                  v-model="formData.contact.postal_code"
                  :disabled="isSubmitting"
                />
              </div>
              <div class="col-md-4 fv-row">
                <label class="fs-6 fw-semibold mb-2">Country</label>
                <input
                  type="text"
                  class="form-control form-control-solid"
                  placeholder="Enter country"
                  v-model="formData.contact.country"
                  :disabled="isSubmitting"
                />
              </div>
            </div>
            <!--end::Address-->

            <!--begin::Patient Information-->
            <div class="separator separator-content my-14">
              <span class="w-250px fw-bold text-gray-600">Medical Information</span>
            </div>

            <!--begin::Patient Status-->
            <div class="fv-row mb-8">
              <label class="fs-6 fw-semibold mb-2">Patient Status</label>
              <select
                class="form-select form-select-solid"
                v-model="formData.patient.status"
                :disabled="isSubmitting"
              >
                <option value="">Select Patient Status</option>
                <option value="fit_to_fly">Fit To Fly</option>
                <option value="not_fit_to_fly">Not Fit To Fly</option>
              </select>
            </div>
            <!--end::Patient Status-->

            <!--begin::Bed Requirements-->
            <div class="row g-9 mb-8">
              <div class="col-md-6 fv-row">
                <label class="fs-6 fw-semibold mb-2">Bed at Origin</label>
                <select
                  class="form-select form-select-solid"
                  v-model="formData.patient.bed_at_origin"
                  :disabled="isSubmitting"
                >
                  <option value="">Select option</option>
                  <option value="yes">Yes</option>
                  <option value="no">No</option>
                </select>
              </div>
              <div class="col-md-6 fv-row">
                <label class="fs-6 fw-semibold mb-2">Bed at Destination</label>
                <select
                  class="form-select form-select-solid"
                  v-model="formData.patient.bed_at_destination"
                  :disabled="isSubmitting"
                >
                  <option value="">Select option</option>
                  <option value="yes">Yes</option>
                  <option value="no">No</option>
                </select>
              </div>
            </div>
            <!--end::Bed Requirements-->

            <!--begin::Special Instructions-->
            <div class="fv-row mb-8">
              <label class="fs-6 fw-semibold mb-2">Special Instructions</label>
              <textarea
                class="form-control form-control-solid"
                rows="4"
                placeholder="Enter any special medical instructions or requirements"
                v-model="formData.patient.special_instructions"
                :disabled="isSubmitting"
              ></textarea>
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
            :disabled="isSubmitting || !isFormValid"
          >
            <span v-if="!isSubmitting" class="indicator-label">Create Patient</span>
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
  <!--end::Modal - Create patient-->
</template>

<script setup lang="ts">
import { ref, reactive, computed } from "vue";
import Swal from "sweetalert2";
import ApiService from "@/core/services/ApiService";
import { hideModal } from "@/core/helpers/modal";

const emit = defineEmits(['patientCreated', 'close']);

const modalRef = ref<HTMLElement | null>(null);
const isSubmitting = ref(false);

// Form data
const formData = reactive({
  contact: {
    first_name: '',
    last_name: '',
    email: '',
    phone: '',
    date_of_birth: '',
    nationality: '',
    passport_number: '',
    passport_expiration_date: '',
    address_line1: '',
    address_line2: '',
    city: '',
    state: '',
    postal_code: '',
    country: ''
  },
  patient: {
    status: '',
    bed_at_origin: '',
    bed_at_destination: '',
    special_instructions: ''
  }
});

// Computed validation
const isFormValid = computed(() => {
  // Check required fields
  if (!formData.contact.first_name || !formData.contact.last_name) {
    return false;
  }

  return true;
});

const resetForm = () => {
  Object.assign(formData.contact, {
    first_name: '',
    last_name: '',
    email: '',
    phone: '',
    date_of_birth: '',
    nationality: '',
    passport_number: '',
    passport_expiration_date: '',
    address_line1: '',
    address_line2: '',
    city: '',
    state: '',
    postal_code: '',
    country: ''
  });

  Object.assign(formData.patient, {
    status: '',
    bed_at_origin: '',
    bed_at_destination: '',
    special_instructions: ''
  });
};

const submitForm = async () => {
  if (!isFormValid.value || isSubmitting.value) return;

  isSubmitting.value = true;

  try {
    // Step 1: Create the contact
    const contactData = { ...formData.contact };

    // Remove empty date fields to avoid backend validation errors
    if (!contactData.date_of_birth) {
      delete contactData.date_of_birth;
    }
    if (!contactData.passport_expiration_date) {
      delete contactData.passport_expiration_date;
    }

    const contactResponse = await ApiService.post("/contacts/", contactData);
    const newContact = contactResponse.data;

    if (!newContact || !newContact.id) {
      throw new Error('Contact was created but response is missing contact ID');
    }

    // Step 2: Create the patient using the contact ID
    const patientData = {
      info: newContact.id,
      status: formData.patient.status || 'fit_to_fly',
      bed_at_origin: formData.patient.bed_at_origin || null,
      bed_at_destination: formData.patient.bed_at_destination || null,
      special_instructions: formData.patient.special_instructions || ''
    };

    const patientResponse = await ApiService.post("/patients/", patientData);
    const newPatient = patientResponse.data;

    if (!newPatient || !newPatient.id) {
      throw new Error('Patient was created but response is missing patient ID');
    }

    // Step 3: Attach the contact info to the patient object for the parent component
    newPatient.info = newContact;

    // Show success message
    await Swal.fire({
      title: "Success!",
      text: `Patient ${newContact.first_name} ${newContact.last_name} has been created successfully!`,
      icon: "success",
      timer: 2000,
      showConfirmButton: false
    });

    // Emit the created patient to parent
    emit('patientCreated', newPatient);

    // Reset form and close modal
    resetForm();
    closeModal();

  } catch (error: any) {
    console.error('Error creating patient:', error);

    let errorMessage = "Failed to create patient. Please try again.";

    // Handle specific errors
    if (error.message && !error.response) {
      errorMessage = error.message;
    } else if (error.response?.data?.detail) {
      errorMessage = error.response.data.detail;
    } else if (error.response?.data) {
      // Handle field-specific errors from Django
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
    } else if (error.response?.status === 400) {
      errorMessage = "Invalid data submitted. Please check all fields and try again.";
    } else if (error.response?.status === 401) {
      errorMessage = "Authentication error. Please refresh the page and try again.";
    } else if (error.response?.status >= 500) {
      errorMessage = "Server error. Please contact support if this persists.";
    }

    await Swal.fire({
      title: "Error!",
      text: errorMessage,
      icon: "error",
      confirmButtonText: "OK"
    });
  } finally {
    isSubmitting.value = false;
  }
};

const closeModal = () => {
  hideModal(modalRef.value);
  emit('close');
};
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