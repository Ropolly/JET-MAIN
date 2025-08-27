<template>
  <!--begin::Modal - Create staff from contact-->
  <div
    class="modal fade"
    id="kt_modal_create_staff_from_contact"
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
          <h2>Create Staff Record</h2>
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
          <form id="kt_modal_create_staff_from_contact_form" class="form" @submit.prevent="submitForm">
            
            <!--begin::Contact Info Display-->
            <div class="d-flex align-items-center bg-light-primary rounded p-6 mb-8">
              <div class="symbol symbol-50px me-5">
                <div class="symbol-label bg-primary">
                  <i class="ki-duotone ki-user fs-2x text-white">
                    <span class="path1"></span>
                    <span class="path2"></span>
                  </i>
                </div>
              </div>
              <div class="flex-grow-1">
                <div class="fw-bold text-gray-800 fs-6">{{ contactDisplayName }}</div>
                <div class="text-muted fs-7">Creating staff record for this contact</div>
              </div>
            </div>
            <!--end::Contact Info Display-->

            <!--begin::Staff Status-->
            <div class="fv-row mb-8">
              <label class="required fs-6 fw-semibold mb-2">Staff Status</label>
              <div class="row g-3">
                <div class="col-md-6">
                  <div class="form-check form-check-custom form-check-solid">
                    <input 
                      class="form-check-input" 
                      type="radio" 
                      v-model="formData.active"
                      :value="true"
                      id="activeTrue"
                      :disabled="isSubmitting"
                    >
                    <label class="form-check-label fw-semibold text-gray-700" for="activeTrue">
                      <span class="badge badge-light-success fs-7 fw-bold me-2">Active</span>
                      Currently working staff member
                    </label>
                  </div>
                </div>
                <div class="col-md-6">
                  <div class="form-check form-check-custom form-check-solid">
                    <input 
                      class="form-check-input" 
                      type="radio" 
                      v-model="formData.active"
                      :value="false"
                      id="activeFalse"
                      :disabled="isSubmitting"
                    >
                    <label class="form-check-label fw-semibold text-gray-700" for="activeFalse">
                      <span class="badge badge-light-warning fs-7 fw-bold me-2">Inactive</span>
                      Not currently active
                    </label>
                  </div>
                </div>
              </div>
            </div>
            <!--end::Staff Status-->

            <!--begin::Staff Roles-->
            <div class="fv-row mb-8">
              <label class="fs-6 fw-semibold mb-4">Staff Roles</label>
              <div class="text-muted fs-7 mb-4">Select the roles this staff member will perform:</div>
              
              <div class="row g-3">
                <!--begin::Pilot Roles-->
                <div class="col-md-6">
                  <h6 class="fw-bold text-gray-800 mb-3">Pilot Roles</h6>
                  <div v-for="role in pilotRoles" :key="role.code" class="form-check form-check-custom form-check-solid mb-2">
                    <input 
                      class="form-check-input" 
                      type="checkbox" 
                      v-model="formData.selectedRoles"
                      :value="role.code"
                      :id="`role_${role.code}`"
                      :disabled="isSubmitting"
                    >
                    <label class="form-check-label fw-semibold text-gray-700" :for="`role_${role.code}`">
                      <span class="badge badge-light-primary fs-8 fw-bold me-2">{{ role.code }}</span>
                      {{ role.name }}
                    </label>
                  </div>
                </div>
                <!--end::Pilot Roles-->

                <!--begin::Medical Roles-->
                <div class="col-md-6">
                  <h6 class="fw-bold text-gray-800 mb-3">Medical Roles</h6>
                  <div v-for="role in medicalRoles" :key="role.code" class="form-check form-check-custom form-check-solid mb-2">
                    <input 
                      class="form-check-input" 
                      type="checkbox" 
                      v-model="formData.selectedRoles"
                      :value="role.code"
                      :id="`role_${role.code}`"
                      :disabled="isSubmitting"
                    >
                    <label class="form-check-label fw-semibold text-gray-700" :for="`role_${role.code}`">
                      <span class="badge badge-light-success fs-8 fw-bold me-2">{{ role.code }}</span>
                      {{ role.name }}
                    </label>
                  </div>
                </div>
                <!--end::Medical Roles-->
              </div>
              <div class="form-text">You can modify role assignments later through the Staff Management page.</div>
            </div>
            <!--end::Staff Roles-->

            <!--begin::Notes-->
            <div class="fv-row mb-8">
              <label class="fs-6 fw-semibold mb-2">Staff Notes</label>
              <textarea
                class="form-control form-control-solid"
                rows="4"
                name="notes"
                placeholder="Enter any notes about this staff member (certifications, specialties, schedule preferences, etc.)"
                v-model="formData.notes"
                :disabled="isSubmitting"
              ></textarea>
              <div class="form-text">Include certifications, specialties, schedule preferences, or other relevant information about this staff member.</div>
            </div>
            <!--end::Notes-->
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
              Create Staff Record
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
  <!--end::Modal - Create staff from contact-->
</template>

<script setup lang="ts">
import { ref, reactive, computed, onMounted } from "vue";
import Swal from "sweetalert2";
import ApiService from "@/core/services/ApiService";

interface Contact {
  id: string;
  first_name?: string;
  last_name?: string;
  business_name?: string;
  email?: string;
  phone?: string;
}

interface StaffRole {
  id: string;
  code: string;
  name: string;
}

const emit = defineEmits(['staffCreated', 'modalClosed']);

const modalRef = ref<HTMLElement | null>(null);
const isSubmitting = ref(false);
const contact = ref<Contact | null>(null);
const availableRoles = ref<StaffRole[]>([]);

// Form data
const formData = reactive({
  active: true,
  notes: '',
  selectedRoles: [] as string[],
});

// Computed role groups
const pilotRoles = computed(() => 
  availableRoles.value.filter(role => ['PIC', 'SIC'].includes(role.code))
);

const medicalRoles = computed(() => 
  availableRoles.value.filter(role => ['RN', 'PARAMEDIC', 'MD', 'RT'].includes(role.code))
);

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

const fetchStaffRoles = async () => {
  try {
    const { data } = await ApiService.get("/staff-roles/");
    availableRoles.value = data.results || data;
  } catch (error) {
    console.error("Error fetching staff roles:", error);
  }
};

const resetForm = () => {
  Object.assign(formData, {
    active: true,
    notes: '',
    selectedRoles: [],
  });
  
  contact.value = null;
};

const submitForm = async () => {
  if (!contact.value || isSubmitting.value) return;
  
  isSubmitting.value = true;
  
  try {
    const staffData = {
      contact_id: contact.value.id,
      active: formData.active,
      notes: formData.notes?.trim() || '',
    };
    
    console.log('Creating staff from contact:', staffData);
    
    const response = await ApiService.post("/staff/", staffData);
    const newStaff = response.data;
    
    // Create staff role memberships for selected roles
    const roleMembershipPromises = formData.selectedRoles.map(async (roleCode) => {
      const role = availableRoles.value.find(r => r.code === roleCode);
      if (role) {
        const membershipData = {
          staff_id: newStaff.id,
          role_id: role.id,
          start_on: new Date().toISOString().split('T')[0], // Today's date
          end_on: null, // No end date (active membership)
        };
        
        try {
          await ApiService.post("/staff-role-memberships/", membershipData);
          console.log(`Created role membership: ${roleCode} for staff ${newStaff.id}`);
        } catch (membershipError) {
          console.error(`Error creating role membership for ${roleCode}:`, membershipError);
        }
      }
    });
    
    // Wait for all role memberships to be created
    await Promise.allSettled(roleMembershipPromises);
    
    // Force close modal using multiple methods
    const modalElement = document.getElementById('kt_modal_create_staff_from_contact');
    if (modalElement) {
      // Method 1: Try Bootstrap modal instance
      try {
        if ((window as any).bootstrap?.Modal) {
          const modal = (window as any).bootstrap.Modal.getInstance(modalElement) || 
                       new (window as any).bootstrap.Modal(modalElement);
          modal.hide();
        }
      } catch (error) {
        console.log('Bootstrap staff modal hide failed:', error);
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
    emit('staffCreated', newStaff);
    emit('modalClosed');
    
    // Show success message after modal is closed
    setTimeout(() => {
      Swal.fire({
        title: "Success!",
        text: `Staff record created successfully for ${contactDisplayName.value}!`,
        icon: "success",
        confirmButtonText: "OK"
      });
    }, 200);
    
  } catch (error: any) {
    console.error('Error creating staff from contact:', error);
    console.error('Error response:', error.response?.data);
    
    let errorMessage = "Failed to create staff record. Please try again.";
    
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

// Load staff roles on mount
onMounted(() => {
  fetchStaffRoles();
});

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

.notice {
  background-color: rgba(var(--bs-info-rgb), 0.1) !important;
}
</style>