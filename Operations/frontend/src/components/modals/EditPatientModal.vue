<template>
  <!--begin::Modal - Edit patient-->
  <div
    class="modal fade"
    id="kt_modal_edit_patient"
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
          <h2>Edit Patient</h2>
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
          <form id="kt_modal_edit_patient_form" class="form" @submit.prevent="submitForm">
            
            <!--begin::Patient Info Display-->
            <div class="d-flex align-items-center bg-light-success rounded p-6 mb-8">
              <div class="symbol symbol-50px me-5">
                <div class="symbol-label bg-success">
                  <i class="ki-duotone ki-profile-user fs-2x text-white">
                    <span class="path1"></span>
                    <span class="path2"></span>
                    <span class="path3"></span>
                    <span class="path4"></span>
                  </i>
                </div>
              </div>
              <div class="flex-grow-1">
                <div class="fw-bold text-gray-800 fs-6">{{ patientDisplayName }}</div>
                <div class="text-muted fs-7">{{ patientDisplayEmail }}</div>
              </div>
            </div>
            <!--end::Patient Info Display-->

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

            <!--begin::Patient Details-->
            <div class="row g-6 mb-8">
              <div class="col-md-6">
                <div class="fv-row">
                  <label class="fs-6 fw-semibold mb-2">Date of Birth</label>
                  <input 
                    type="date" 
                    class="form-control form-control-solid" 
                    v-model="formData.date_of_birth"
                    :disabled="isSubmitting"
                  />
                  <div class="form-text">Patient's date of birth</div>
                </div>
              </div>
              <div class="col-md-6">
                <div class="fv-row">
                  <label class="fs-6 fw-semibold mb-2">Nationality</label>
                  <input 
                    type="text" 
                    class="form-control form-control-solid" 
                    v-model="formData.nationality"
                    :disabled="isSubmitting"
                    placeholder="Enter nationality"
                  />
                  <div class="form-text">Patient's nationality</div>
                </div>
              </div>
            </div>
            <!--end::Patient Details-->

            <!--begin::Passport Information-->
            <div class="row g-6 mb-8">
              <div class="col-md-6">
                <div class="fv-row">
                  <label class="fs-6 fw-semibold mb-2">Passport Number</label>
                  <input 
                    type="text" 
                    class="form-control form-control-solid" 
                    v-model="formData.passport_number"
                    :disabled="isSubmitting"
                    placeholder="Enter passport number"
                  />
                  <div class="form-text">Patient's passport number</div>
                </div>
              </div>
              <div class="col-md-6">
                <div class="fv-row">
                  <label class="fs-6 fw-semibold mb-2">Passport Expiration</label>
                  <input 
                    type="date" 
                    class="form-control form-control-solid" 
                    v-model="formData.passport_expiration_date"
                    :disabled="isSubmitting"
                  />
                  <div class="form-text">When the passport expires</div>
                </div>
              </div>
            </div>
            <!--end::Passport Information-->

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
                      id="editBedOriginCheck"
                      :disabled="isSubmitting"
                    >
                    <label class="form-check-label fw-semibold text-gray-700" for="editBedOriginCheck">
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
                      id="editBedDestinationCheck"
                      :disabled="isSubmitting"
                    >
                    <label class="form-check-label fw-semibold text-gray-700" for="editBedDestinationCheck">
                      Bed required at destination
                    </label>
                  </div>
                  <div class="form-text text-muted fs-8">Patient needs bed/stretcher at drop-off location</div>
                </div>
              </div>
            </div>
            <!--end::Bed Requirements-->

            <!--begin::Special Instructions-->
            <div class="fv-row mb-8">
              <label class="fs-6 fw-semibold mb-2">Special Instructions</label>
              <textarea 
                class="form-control form-control-solid" 
                rows="4"
                v-model="formData.special_instructions"
                :disabled="isSubmitting"
                placeholder="Enter any special instructions for this patient's care and transport"
              ></textarea>
              <div class="form-text">Any special medical or transport instructions</div>
            </div>
            <!--end::Special Instructions-->

            <!--begin::Actions-->
            <div class="d-flex justify-content-end">
              <button
                type="button"
                class="btn btn-light me-3"
                data-bs-dismiss="modal"
                @click="resetForm"
                :disabled="isSubmitting"
              >
                Cancel
              </button>
              <button
                type="submit"
                class="btn btn-primary"
                :disabled="isSubmitting"
              >
                <span v-if="!isSubmitting" class="indicator-label">
                  Update Patient
                </span>
                <span v-if="isSubmitting" class="indicator-progress">
                  Please wait...
                  <span class="spinner-border spinner-border-sm align-middle ms-2"></span>
                </span>
              </button>
            </div>
            <!--end::Actions-->

          </form>
          <!--end::Form-->
        </div>
        <!--end::Modal body-->
      </div>
      <!--end::Modal content-->
    </div>
    <!--end::Modal dialog-->
  </div>
  <!--end::Modal-->
</template>

<script lang="ts">
import { defineComponent, ref, computed } from "vue";
import ApiService from "@/core/services/ApiService";
import Swal from "sweetalert2";

interface Patient {
  id: string;
  info: {
    id: string;
    first_name: string;
    last_name: string;
    business_name?: string;
    email?: string;
    phone?: string;
  };
  date_of_birth: string;
  nationality: string;
  passport_number: string;
  passport_expiration_date: string;
  special_instructions?: string;
  status: string;
  bed_at_origin: boolean;
  bed_at_destination: boolean;
}

interface FormData {
  status: string;
  date_of_birth: string;
  nationality: string;
  passport_number: string;
  passport_expiration_date: string;
  special_instructions: string;
  bed_at_origin: boolean;
  bed_at_destination: boolean;
}

export default defineComponent({
  name: "EditPatientModal",
  emits: ["patientUpdated"],
  setup(props, { emit }) {
    const modalRef = ref<HTMLElement>();
    const isSubmitting = ref(false);
    const currentPatient = ref<Patient | null>(null);

    // Form data
    const formData = ref<FormData>({
      status: 'pending',
      date_of_birth: '',
      nationality: '',
      passport_number: '',
      passport_expiration_date: '',
      special_instructions: '',
      bed_at_origin: false,
      bed_at_destination: false,
    });

    const patientDisplayName = computed(() => {
      if (!currentPatient.value?.info) return 'Unknown Patient';
      const { first_name, last_name, business_name } = currentPatient.value.info;
      if (business_name) return business_name;
      if (first_name || last_name) {
        return `${first_name || ''} ${last_name || ''}`.trim();
      }
      return 'Unknown Patient';
    });

    const patientDisplayEmail = computed(() => {
      return currentPatient.value?.info?.email || 'No email';
    });

    const setPatient = (patient: Patient) => {
      currentPatient.value = patient;
      
      // Populate form with patient data
      formData.value = {
        status: patient.status || 'pending',
        date_of_birth: patient.date_of_birth || '',
        nationality: patient.nationality || '',
        passport_number: patient.passport_number || '',
        passport_expiration_date: patient.passport_expiration_date || '',
        special_instructions: patient.special_instructions || '',
        bed_at_origin: patient.bed_at_origin || false,
        bed_at_destination: patient.bed_at_destination || false,
      };
    };

    const resetForm = () => {
      currentPatient.value = null;
      formData.value = {
        status: 'pending',
        date_of_birth: '',
        nationality: '',
        passport_number: '',
        passport_expiration_date: '',
        special_instructions: '',
        bed_at_origin: false,
        bed_at_destination: false,
      };
      isSubmitting.value = false;
    };

    const submitForm = async () => {
      if (!currentPatient.value) return;

      try {
        isSubmitting.value = true;

        const updateData = {
          ...formData.value
        };

        await ApiService.patch(`/patients/${currentPatient.value.id}/`, updateData);

        Swal.fire({
          title: "Success!",
          text: "Patient has been updated successfully.",
          icon: "success",
          confirmButtonText: "OK"
        });

        emit("patientUpdated", { ...currentPatient.value, ...updateData });
        
        // Close modal
        const modal = modalRef.value;
        if (modal) {
          const bsModal = (window as any).bootstrap.Modal.getInstance(modal) || new (window as any).bootstrap.Modal(modal);
          bsModal.hide();
        }

        resetForm();

      } catch (error: any) {
        console.error('Error updating patient:', error);
        Swal.fire({
          title: "Error",
          text: error.response?.data?.detail || "Failed to update patient. Please try again.",
          icon: "error",
          confirmButtonText: "OK"
        });
      } finally {
        isSubmitting.value = false;
      }
    };

    return {
      modalRef,
      isSubmitting,
      formData,
      patientDisplayName,
      patientDisplayEmail,
      setPatient,
      resetForm,
      submitForm,
    };
  },
});
</script>