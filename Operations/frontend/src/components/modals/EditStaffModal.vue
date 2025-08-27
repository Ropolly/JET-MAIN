<template>
  <!--begin::Modal - Edit staff-->
  <div
    class="modal fade show"
    id="kt_modal_edit_staff"
    ref="modalRef"
    tabindex="-1"
    aria-hidden="false"
    style="display: block;"
  >
    <!--begin::Modal dialog-->
    <div class="modal-dialog modal-lg">
      <!--begin::Modal content-->
      <div class="modal-content">
        <!--begin::Modal header-->
        <div class="modal-header">
          <!--begin::Title-->
          <h2>Edit Staff Member</h2>
          <!--end::Title-->

          <!--begin::Close-->
          <div
            class="btn btn-sm btn-icon btn-active-color-primary"
            @click="closeModal"
          >
            <KTIcon icon-name="cross" icon-class="fs-1" />
          </div>
          <!--end::Close-->
        </div>
        <!--end::Modal header-->

        <!--begin::Modal body-->
        <div class="modal-body scroll-y mx-5 my-7">
          <!--begin::Form-->
          <form id="kt_modal_edit_staff_form" class="form">
            <!--begin::Staff Info Display-->
            <div class="card bg-light-info mb-8">
              <div class="card-body">
                <div class="d-flex align-items-center">
                  <div class="symbol symbol-circle symbol-50px me-5">
                    <div class="symbol-label bg-info">
                      <i class="ki-duotone ki-user fs-2x text-white">
                        <span class="path1"></span>
                        <span class="path2"></span>
                      </i>
                    </div>
                  </div>
                  <div class="flex-grow-1">
                    <h4 class="fw-bold mb-1">{{ getStaffName() }}</h4>
                    <div class="text-muted">{{ getContactInfo() }}</div>
                  </div>
                </div>
              </div>
            </div>
            <!--end::Staff Info Display-->

            <!--begin::Input group-->
            <div class="fv-row mb-8">
              <label class="fs-6 fw-semibold mb-2">Status</label>
              <div class="form-check form-switch">
                <input 
                  class="form-check-input" 
                  type="checkbox" 
                  v-model="formData.active"
                  id="staffActiveEditSwitch"
                  :disabled="isSubmitting"
                >
                <label class="form-check-label fw-semibold text-gray-700" for="staffActiveEditSwitch">
                  {{ formData.active ? 'Active' : 'Inactive' }}
                </label>
              </div>
            </div>
            <!--end::Input group-->

            <!--begin::Input group-->
            <div class="fv-row mb-8">
              <label class="fs-6 fw-semibold mb-2">Notes</label>
              <textarea
                class="form-control form-control-solid"
                rows="4"
                name="notes"
                placeholder="Additional notes about this staff member..."
                v-model="formData.notes"
                :disabled="isSubmitting"
              ></textarea>
            </div>
            <!--end::Input group-->

            <!--begin::Current Roles Section-->
            <div class="fv-row mb-8">
              <label class="fs-6 fw-semibold mb-2">Current Active Roles</label>
              <div class="d-flex flex-wrap gap-2 mb-3">
                <span 
                  v-for="role in getCurrentRoles()" 
                  :key="role.id" 
                  class="badge badge-light-primary fs-7 fw-bold"
                >
                  {{ role.name }} ({{ role.code }})
                </span>
                <span v-if="getCurrentRoles().length === 0" class="text-muted fs-7">
                  No active roles assigned
                </span>
              </div>
              <button 
                type="button"
                class="btn btn-light-primary btn-sm"
                @click="openRoleManagement"
                :disabled="isSubmitting"
              >
                <KTIcon icon-name="user-tick" icon-class="fs-4 me-2" />
                Manage Roles
              </button>
            </div>
            <!--end::Current Roles Section-->

            <!--begin::Contact Information Section-->
            <div class="separator separator-content my-10">
              <span class="w-250px fw-bold text-gray-600">Contact Information</span>
            </div>

            <div class="card bg-light-secondary mb-8">
              <div class="card-body">
                <div class="row g-5">
                  <div class="col-md-6">
                    <label class="fs-7 fw-bold text-gray-600 mb-1">Name</label>
                    <div class="fs-6 fw-bold text-gray-800">
                      {{ staff.contact?.business_name || 
                         `${staff.contact?.first_name || ''} ${staff.contact?.last_name || ''}`.trim() || 
                         'No name' }}
                    </div>
                  </div>
                  <div class="col-md-6">
                    <label class="fs-7 fw-bold text-gray-600 mb-1">Email</label>
                    <div class="fs-6 text-gray-700">{{ staff.contact?.email || 'No email' }}</div>
                  </div>
                  <div class="col-md-6">
                    <label class="fs-7 fw-bold text-gray-600 mb-1">Phone</label>
                    <div class="fs-6 text-gray-700">{{ staff.contact?.phone || 'No phone' }}</div>
                  </div>
                  <div class="col-md-6">
                    <label class="fs-7 fw-bold text-gray-600 mb-1">Contact ID</label>
                    <div class="fs-6 text-muted">{{ staff.contact_id }}</div>
                  </div>
                </div>
                <div class="mt-5">
                  <button 
                    type="button"
                    class="btn btn-light-secondary btn-sm"
                    @click="editContact"
                    :disabled="isSubmitting"
                  >
                    <KTIcon icon-name="pencil" icon-class="fs-4 me-2" />
                    Edit Contact Details
                  </button>
                </div>
              </div>
            </div>
            <!--end::Contact Information Section-->
          </form>
          <!--end::Form-->
        </div>
        <!--end::Modal body-->

        <!--begin::Modal footer-->
        <div class="modal-footer flex-center">
          <!--begin::Button-->
          <button
            type="button"
            class="btn btn-light me-3"
            @click="closeModal"
            :disabled="isSubmitting"
          >
            Cancel
          </button>
          <!--end::Button-->

          <!--begin::Button-->
          <button
            type="submit"
            class="btn btn-primary"
            @click="handleSubmit"
            :disabled="isSubmitting"
          >
            <span v-if="!isSubmitting" class="indicator-label">Update Staff</span>
            <span v-else class="indicator-progress">
              Please wait...
              <span
                class="spinner-border spinner-border-sm align-middle ms-2"
              ></span>
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
  <!--begin::Modal backdrop-->
  <div class="modal-backdrop fade show"></div>
  <!--end::Modal backdrop-->
  <!--end::Modal - Edit staff-->
</template>

<script setup lang="ts">
import { ref, reactive, computed, onMounted } from "vue";
import Swal from "sweetalert2";
import ApiService from "@/core/services/ApiService";
import { useRouter } from "vue-router";

interface Props {
  staff: {
    id: string;
    contact_id: string;
    contact?: {
      id: string;
      first_name: string;
      last_name: string;
      business_name?: string;
      email: string;
      phone: string;
    };
    active: boolean;
    notes: string;
    created_on: string;
    role_memberships?: Array<{
      id: string;
      role: {
        id: string;
        code: string;
        name: string;
      };
      start_on: string;
      end_on?: string;
    }>;
  };
}

const props = defineProps<Props>();
const emit = defineEmits(['staffUpdated', 'close']);
const router = useRouter();

const modalRef = ref<HTMLElement | null>(null);
const isSubmitting = ref(false);

// Form data
const formData = reactive({
  active: props.staff.active,
  notes: props.staff.notes || '',
});

const getStaffName = (): string => {
  if (!props.staff.contact) return 'Unknown Staff';
  
  const { first_name, last_name, business_name } = props.staff.contact;
  
  if (business_name) return business_name;
  if (first_name || last_name) {
    return `${first_name || ''} ${last_name || ''}`.trim();
  }
  return 'Unknown Staff';
};

const getContactInfo = (): string => {
  if (!props.staff.contact) return 'No contact info';
  
  const email = props.staff.contact.email;
  const phone = props.staff.contact.phone;
  
  if (email && phone) return `${email} • ${phone}`;
  if (email) return email;
  if (phone) return phone;
  return 'No contact details';
};

const getCurrentRoles = () => {
  if (!props.staff.role_memberships) return [];
  
  const today = new Date().toISOString().split('T')[0];
  
  return props.staff.role_memberships
    .filter(membership => {
      const startDate = membership.start_on;
      const endDate = membership.end_on;
      
      const startValid = !startDate || startDate <= today;
      const endValid = !endDate || endDate >= today;
      
      return startValid && endValid;
    })
    .map(membership => membership.role);
};

const openRoleManagement = () => {
  // Close this modal and emit event to open role management
  closeModal();
  // Let the parent handle opening the role management modal
  setTimeout(() => {
    emit('close', 'openRoleManagement');
  }, 100);
};

const editContact = () => {
  if (props.staff.contact_id) {
    // Navigate to contact edit page
    router.push(`/admin/contacts/${props.staff.contact_id}`);
  }
};

const handleSubmit = async (e: Event) => {
  e.preventDefault();
  
  isSubmitting.value = true;
  
  try {
    const updateData = {
      active: formData.active,
      notes: formData.notes
    };

    console.log('Updating staff with data:', updateData);
    const response = await ApiService.patch(`/staff/${props.staff.id}/`, updateData);
    console.log('Staff updated successfully:', response.data);
    
    Swal.fire({
      title: "Success!",
      text: "Staff member updated successfully!",
      icon: "success",
      confirmButtonText: "OK"
    }).then(() => {
      emit('staffUpdated', response.data);
    });
  } catch (error: any) {
    console.error('Error updating staff:', error);
    const errorMessage = error.response?.data?.detail || 
                        error.response?.data?.message || 
                        error.message || 
                        "Failed to update staff member. Please try again.";
    
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

const closeModal = () => {
  emit('close');
};

// Handle escape key
onMounted(() => {
  const handleEscape = (e: KeyboardEvent) => {
    if (e.key === 'Escape') {
      closeModal();
    }
  };
  
  document.addEventListener('keydown', handleEscape);
  
  return () => {
    document.removeEventListener('keydown', handleEscape);
  };
});
</script>