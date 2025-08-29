<template>
  <!--begin::Modal - Edit passenger-->
  <div
    class="modal fade"
    id="kt_modal_edit_passenger"
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
          <h2>Edit Passenger</h2>
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
          <form id="kt_modal_edit_passenger_form" class="form" @submit.prevent="submitForm">
            
            <!--begin::Passenger Info Display-->
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
                <div class="fw-bold text-gray-800 fs-6">{{ passengerDisplayName }}</div>
                <div class="text-muted fs-7">{{ passengerDisplayEmail }}</div>
              </div>
            </div>
            <!--end::Passenger Info Display-->

            <!--begin::Contact Information-->
            <div class="separator separator-content my-8">
              <span class="w-250px fw-bold text-gray-600">Contact Information</span>
            </div>

            <!--begin::Name Fields-->
            <div class="row g-6 mb-8">
              <div class="col-md-6">
                <div class="fv-row">
                  <label class="required fs-6 fw-semibold mb-2">First Name</label>
                  <input 
                    type="text" 
                    class="form-control form-control-solid" 
                    v-model="contactData.first_name"
                    :disabled="isSubmitting"
                    placeholder="Enter first name"
                    required
                  />
                </div>
              </div>
              <div class="col-md-6">
                <div class="fv-row">
                  <label class="required fs-6 fw-semibold mb-2">Last Name</label>
                  <input 
                    type="text" 
                    class="form-control form-control-solid" 
                    v-model="contactData.last_name"
                    :disabled="isSubmitting"
                    placeholder="Enter last name"
                    required
                  />
                </div>
              </div>
            </div>
            <!--end::Name Fields-->

            <!--begin::Email and Phone-->
            <div class="row g-6 mb-8">
              <div class="col-md-6">
                <div class="fv-row">
                  <label class="fs-6 fw-semibold mb-2">Email</label>
                  <input 
                    type="email" 
                    class="form-control form-control-solid" 
                    v-model="contactData.email"
                    :disabled="isSubmitting"
                    placeholder="Enter email address"
                  />
                </div>
              </div>
              <div class="col-md-6">
                <div class="fv-row">
                  <label class="fs-6 fw-semibold mb-2">Phone</label>
                  <input 
                    type="tel" 
                    class="form-control form-control-solid" 
                    v-model="contactData.phone"
                    :disabled="isSubmitting"
                    placeholder="Enter phone number"
                  />
                </div>
              </div>
            </div>
            <!--end::Email and Phone-->

            <!--begin::Address-->
            <div class="fv-row mb-8">
              <label class="fs-6 fw-semibold mb-2">Address</label>
              <input 
                type="text" 
                class="form-control form-control-solid" 
                v-model="contactData.address_line1"
                :disabled="isSubmitting"
                placeholder="Enter address"
              />
            </div>
            <!--end::Address-->

            <!--begin::City, State, Country-->
            <div class="row g-6 mb-8">
              <div class="col-md-4">
                <div class="fv-row">
                  <label class="fs-6 fw-semibold mb-2">City</label>
                  <input 
                    type="text" 
                    class="form-control form-control-solid" 
                    v-model="contactData.city"
                    :disabled="isSubmitting"
                    placeholder="Enter city"
                  />
                </div>
              </div>
              <div class="col-md-4">
                <div class="fv-row">
                  <label class="fs-6 fw-semibold mb-2">State</label>
                  <input 
                    type="text" 
                    class="form-control form-control-solid" 
                    v-model="contactData.state"
                    :disabled="isSubmitting"
                    placeholder="Enter state"
                  />
                </div>
              </div>
              <div class="col-md-4">
                <div class="fv-row">
                  <label class="fs-6 fw-semibold mb-2">Country</label>
                  <input 
                    type="text" 
                    class="form-control form-control-solid" 
                    v-model="contactData.country"
                    :disabled="isSubmitting"
                    placeholder="Enter country"
                  />
                </div>
              </div>
            </div>
            <!--end::City, State, Country-->

            <!--begin::Passenger Status-->
            <div class="separator separator-content my-8">
              <span class="w-250px fw-bold text-gray-600">Passenger Information</span>
            </div>

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
                  <div class="form-text">Required for domestic and international travel</div>
                </div>
              </div>
              <div class="col-md-6">
                <div class="fv-row">
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
                  <div class="form-text">Passenger's nationality</div>
                </div>
              </div>
            </div>

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
                  <div class="form-text">Required for international travel</div>
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
                  <div class="form-text">Must be valid for duration of travel</div>
                </div>
              </div>
            </div>
            <!--end::Travel Information-->

            <!--begin::Emergency Contact-->
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
            <!--end::Emergency Contact-->

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
                  Update Passenger
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

interface Passenger {
  id: string;
  info: {
    id: string;
    first_name: string;
    last_name: string;
    business_name?: string;
    email?: string;
    phone?: string;
    address_line1?: string;
    city?: string;
    state?: string;
    country?: string;
  };
  date_of_birth: string;
  nationality: string;
  passport_number: string;
  passport_expiration_date: string;
  contact_number: string;
  notes?: string;
  status: string;
}

interface ContactData {
  first_name: string;
  last_name: string;
  email: string;
  phone: string;
  address_line1: string;
  city: string;
  state: string;
  country: string;
}

interface FormData {
  status: string;
  date_of_birth: string;
  nationality: string;
  passport_number: string;
  passport_expiration_date: string;
  contact_number: string;
  notes: string;
}

export default defineComponent({
  name: "EditPassengerModal",
  emits: ["passengerUpdated"],
  setup(props, { emit }) {
    const modalRef = ref<HTMLElement>();
    const isSubmitting = ref(false);
    const currentPassenger = ref<Passenger | null>(null);

    // Contact data
    const contactData = ref<ContactData>({
      first_name: '',
      last_name: '',
      email: '',
      phone: '',
      address_line1: '',
      city: '',
      state: '',
      country: '',
    });

    // Form data
    const formData = ref<FormData>({
      status: 'active',
      date_of_birth: '',
      nationality: '',
      passport_number: '',
      passport_expiration_date: '',
      contact_number: '',
      notes: '',
    });

    const passengerDisplayName = computed(() => {
      if (!currentPassenger.value?.info) return 'Unknown Passenger';
      const { first_name, last_name, business_name } = currentPassenger.value.info;
      if (business_name) return business_name;
      if (first_name || last_name) {
        return `${first_name || ''} ${last_name || ''}`.trim();
      }
      return 'Unknown Passenger';
    });

    const passengerDisplayEmail = computed(() => {
      return currentPassenger.value?.info?.email || 'No email';
    });

    const setPassenger = (passenger: Passenger) => {
      currentPassenger.value = passenger;
      
      // Populate contact data
      contactData.value = {
        first_name: passenger.info?.first_name || '',
        last_name: passenger.info?.last_name || '',
        email: passenger.info?.email || '',
        phone: passenger.info?.phone || '',
        address_line1: passenger.info?.address_line1 || '',
        city: passenger.info?.city || '',
        state: passenger.info?.state || '',
        country: passenger.info?.country || '',
      };
      
      // Populate form with passenger data
      formData.value = {
        status: passenger.status || 'active',
        date_of_birth: passenger.date_of_birth || '',
        nationality: passenger.nationality || '',
        passport_number: passenger.passport_number || '',
        passport_expiration_date: passenger.passport_expiration_date || '',
        contact_number: passenger.contact_number || '',
        notes: passenger.notes || '',
      };
    };

    const resetForm = () => {
      currentPassenger.value = null;
      
      contactData.value = {
        first_name: '',
        last_name: '',
        email: '',
        phone: '',
        address_line1: '',
        city: '',
        state: '',
        country: '',
      };
      
      formData.value = {
        status: 'active',
        date_of_birth: '',
        nationality: '',
        passport_number: '',
        passport_expiration_date: '',
        contact_number: '',
        notes: '',
      };
      
      isSubmitting.value = false;
    };

    const submitForm = async () => {
      if (!currentPassenger.value) return;

      try {
        isSubmitting.value = true;

        // Update contact information first
        const contactUpdateData = {
          ...contactData.value
        };

        await ApiService.patch(`/contacts/${currentPassenger.value.info.id}/`, contactUpdateData);

        // Update passenger information
        const passengerUpdateData = {
          ...formData.value
        };

        await ApiService.patch(`/passengers/${currentPassenger.value.id}/`, passengerUpdateData);

        Swal.fire({
          title: "Success!",
          text: "Passenger and contact information has been updated successfully.",
          icon: "success",
          confirmButtonText: "OK"
        });

        emit("passengerUpdated", { 
          ...currentPassenger.value, 
          ...passengerUpdateData,
          info: { ...currentPassenger.value.info, ...contactUpdateData }
        });
        
        // Close modal
        const modal = modalRef.value;
        if (modal) {
          const bsModal = (window as any).bootstrap.Modal.getInstance(modal) || new (window as any).bootstrap.Modal(modal);
          bsModal.hide();
        }

        resetForm();

      } catch (error: any) {
        console.error('Error updating passenger:', error);
        Swal.fire({
          title: "Error",
          text: error.response?.data?.detail || "Failed to update passenger. Please try again.",
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
      contactData,
      formData,
      passengerDisplayName,
      passengerDisplayEmail,
      setPassenger,
      resetForm,
      submitForm,
    };
  },
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
</style>