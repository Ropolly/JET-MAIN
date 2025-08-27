<template>
  <!--begin::Modal - Edit staff role-->
  <div
    class="modal fade show"
    id="kt_modal_edit_staff_role"
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
          <h2>Edit Staff Role</h2>
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
          <form id="kt_modal_edit_staff_role_form" class="form">
            <!--begin::Current Role Display-->
            <div class="card bg-light-info mb-8">
              <div class="card-body">
                <div class="d-flex align-items-center">
                  <span 
                    :class="`badge badge-light-${getRoleColor(role.code)} fs-6 fw-bold me-3`"
                  >
                    {{ role.code }}
                  </span>
                  <div>
                    <h4 class="fw-bold mb-1">{{ role.name }}</h4>
                    <div class="text-muted">Current role configuration</div>
                  </div>
                </div>
              </div>
            </div>
            <!--end::Current Role Display-->

            <!--begin::Input group-->
            <div class="fv-row mb-8">
              <label class="required fs-6 fw-semibold mb-2">Role Code</label>
              <input
                type="text"
                class="form-control form-control-solid"
                placeholder="Enter role code (e.g., PIC, SIC, RN)"
                name="code"
                v-model="formData.code"
                :disabled="isSubmitting"
                @input="formatCode"
              />
              <div class="form-text">
                Short code for the role. Will be automatically converted to uppercase.
                <span class="text-warning">Changing this may affect existing assignments.</span>
              </div>
            </div>
            <!--end::Input group-->

            <!--begin::Input group-->
            <div class="fv-row mb-8">
              <label class="required fs-6 fw-semibold mb-2">Role Name</label>
              <input
                type="text"
                class="form-control form-control-solid"
                placeholder="Enter full role name (e.g., Pilot in Command)"
                name="name"
                v-model="formData.name"
                :disabled="isSubmitting"
              />
              <div class="form-text">
                Full descriptive name for the role.
              </div>
            </div>
            <!--end::Input group-->

            <!--begin::Updated Role Preview-->
            <div v-if="formData.code || formData.name" class="card bg-light-success mb-8">
              <div class="card-body">
                <h5 class="card-title">Updated Role Preview</h5>
                <div class="d-flex align-items-center">
                  <span 
                    :class="`badge badge-light-${getRoleColor(formData.code)} fs-6 fw-bold me-3`"
                  >
                    {{ formData.code || 'CODE' }}
                  </span>
                  <div>
                    <div class="fw-bold">{{ formData.name || 'Role Name' }}</div>
                    <div class="text-muted fs-7">{{ formData.code || 'CODE' }}</div>
                  </div>
                </div>
              </div>
            </div>
            <!--end::Updated Role Preview-->

            <!--begin::Usage Warning-->
            <div v-if="roleUsage > 0" class="alert alert-warning mb-8">
              <div class="d-flex align-items-center">
                <KTIcon icon-name="warning-2" icon-class="fs-2 me-3" />
                <div>
                  <h4 class="alert-heading">Active Assignments Found</h4>
                  <p class="mb-0">
                    This role is currently assigned to <strong>{{ roleUsage }}</strong> staff member(s).
                    Changes will be reflected in their active assignments.
                  </p>
                </div>
              </div>
            </div>
            <!--end::Usage Warning-->
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
            :disabled="isSubmitting || !formData.code || !formData.name"
          >
            <span v-if="!isSubmitting" class="indicator-label">Update Role</span>
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
  <!--end::Modal - Edit staff role-->
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from "vue";
import Swal from "sweetalert2";
import ApiService from "@/core/services/ApiService";

interface Props {
  role: {
    id: string;
    code: string;
    name: string;
    created_on: string;
  };
}

const props = defineProps<Props>();
const emit = defineEmits(['roleUpdated', 'close']);

const modalRef = ref<HTMLElement | null>(null);
const isSubmitting = ref(false);
const roleUsage = ref(0);

// Form data
const formData = reactive({
  code: props.role.code,
  name: props.role.name,
});

const getRoleColor = (roleCode: string): string => {
  const colors: Record<string, string> = {
    PIC: 'primary',
    SIC: 'info',
    RN: 'success',
    PARAMEDIC: 'warning',
    MD: 'danger',
    RT: 'secondary',
    EMT: 'dark',
    DISPATCHER: 'info',
  };
  return colors[roleCode] || 'secondary';
};

const formatCode = () => {
  // Convert to uppercase and remove spaces/special characters
  formData.code = formData.code.toUpperCase().replace(/[^A-Z0-9]/g, '');
};

const fetchRoleUsage = async () => {
  try {
    const response = await ApiService.get(`/staff-role-memberships/?role_id=${props.role.id}`);
    const memberships = response.data.results || response.data || [];
    
    // Count active assignments
    const today = new Date().toISOString().split('T')[0];
    roleUsage.value = memberships.filter((membership: any) => {
      const startDate = membership.start_on;
      const endDate = membership.end_on;
      
      const startValid = !startDate || startDate <= today;
      const endValid = !endDate || endDate >= today;
      
      return startValid && endValid;
    }).length;
  } catch (error) {
    console.error('Error fetching role usage:', error);
  }
};

const handleSubmit = async (e: Event) => {
  e.preventDefault();
  
  // Basic validation
  if (!formData.code || !formData.name) {
    Swal.fire({
      title: "Validation Error",
      text: "Please fill in both role code and name",
      icon: "warning",
      confirmButtonText: "OK"
    });
    return;
  }

  // Check if anything changed
  if (formData.code === props.role.code && formData.name === props.role.name) {
    Swal.fire({
      title: "No Changes",
      text: "No changes were made to the role",
      icon: "info",
      confirmButtonText: "OK"
    });
    return;
  }

  // Confirm changes if role has active assignments
  if (roleUsage.value > 0) {
    const result = await Swal.fire({
      title: "Confirm Changes",
      text: `This role has ${roleUsage.value} active assignment(s). Are you sure you want to update it?`,
      icon: "question",
      showCancelButton: true,
      confirmButtonText: "Yes, update it!",
      cancelButtonText: "Cancel"
    });

    if (!result.isConfirmed) return;
  }

  isSubmitting.value = true;
  
  try {
    const updateData = {
      code: formData.code.trim(),
      name: formData.name.trim(),
    };

    console.log('Updating staff role with data:', updateData);
    const response = await ApiService.patch(`/staff-roles/${props.role.id}/`, updateData);
    console.log('Staff role updated successfully:', response.data);
    
    Swal.fire({
      title: "Success!",
      text: "Staff role updated successfully!",
      icon: "success",
      confirmButtonText: "OK"
    }).then(() => {
      emit('roleUpdated', response.data);
    });
  } catch (error: any) {
    console.error('Error updating staff role:', error);
    
    let errorMessage = "Failed to update staff role. Please try again.";
    
    if (error.response?.data) {
      if (error.response.data.code && error.response.data.code.includes('already exists')) {
        errorMessage = `A role with the code "${formData.code}" already exists. Please use a different code.`;
      } else if (typeof error.response.data === 'object') {
        const errors = Object.values(error.response.data).flat();
        errorMessage = errors.join('. ');
      } else {
        errorMessage = error.response.data.detail || error.response.data.message || errorMessage;
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

const closeModal = () => {
  emit('close');
};

onMounted(() => {
  fetchRoleUsage();
  
  // Handle escape key
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