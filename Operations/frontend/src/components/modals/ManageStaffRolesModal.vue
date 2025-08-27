<template>
  <!--begin::Modal - Manage staff roles-->
  <div
    class="modal fade show"
    id="kt_modal_manage_staff_roles"
    ref="modalRef"
    tabindex="-1"
    aria-hidden="false"
    style="display: block;"
  >
    <!--begin::Modal dialog-->
    <div class="modal-dialog modal-xl">
      <!--begin::Modal content-->
      <div class="modal-content">
        <!--begin::Modal header-->
        <div class="modal-header">
          <!--begin::Title-->
          <div>
            <h2>Manage Staff Roles</h2>
            <div class="text-muted fs-6">{{ getStaffName() }}</div>
          </div>
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
          <!--begin::Current Roles Section-->
          <div class="card mb-8">
            <div class="card-header">
              <h3 class="card-title">Current Role Assignments</h3>
              <div class="card-toolbar">
                <button 
                  type="button"
                  class="btn btn-primary btn-sm"
                  @click="showAddRoleForm = true"
                  :disabled="isSubmitting"
                >
                  <KTIcon icon-name="plus" icon-class="fs-4 me-2" />
                  Add Role
                </button>
              </div>
            </div>
            <div class="card-body">
              <div v-if="roleMemberships.length === 0" class="text-center py-10">
                <div class="text-muted fs-4 mb-5">No roles assigned</div>
                <button 
                  type="button"
                  class="btn btn-primary"
                  @click="showAddRoleForm = true"
                >
                  Assign First Role
                </button>
              </div>
              
              <div v-else class="table-responsive">
                <table class="table table-row-dashed table-row-gray-300 gy-7">
                  <thead>
                    <tr class="fw-bold fs-6 text-gray-800">
                      <th>Role</th>
                      <th>Start Date</th>
                      <th>End Date</th>
                      <th>Status</th>
                      <th>Actions</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-for="membership in roleMemberships" :key="membership.id">
                      <td>
                        <div class="d-flex align-items-center">
                          <span 
                            :class="`badge badge-light-${getRoleColor(membership.role.code)} me-3`"
                          >
                            {{ membership.role.code }}
                          </span>
                          <div>
                            <div class="fw-bold">{{ membership.role.name }}</div>
                          </div>
                        </div>
                      </td>
                      <td>
                        <span v-if="membership.start_on" class="text-gray-600">
                          {{ formatDate(membership.start_on) }}
                        </span>
                        <span v-else class="text-muted">Not set</span>
                      </td>
                      <td>
                        <span v-if="membership.end_on" class="text-gray-600">
                          {{ formatDate(membership.end_on) }}
                        </span>
                        <span v-else class="text-success">Active</span>
                      </td>
                      <td>
                        <span :class="`badge badge-light-${getRoleStatus(membership) === 'active' ? 'success' : getRoleStatus(membership) === 'future' ? 'warning' : 'secondary'}`">
                          {{ getRoleStatus(membership) }}
                        </span>
                      </td>
                      <td>
                        <button 
                          class="btn btn-sm btn-light-primary me-2"
                          @click="editMembership(membership)"
                          :disabled="isSubmitting"
                        >
                          <KTIcon icon-name="pencil" icon-class="fs-5" />
                        </button>
                        <button 
                          class="btn btn-sm btn-light-danger"
                          @click="deleteMembership(membership)"
                          :disabled="isSubmitting"
                        >
                          <KTIcon icon-name="trash" icon-class="fs-5" />
                        </button>
                      </td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>
          </div>
          <!--end::Current Roles Section-->

          <!--begin::Add Role Form-->
          <div v-if="showAddRoleForm" class="card mb-8">
            <div class="card-header">
              <h3 class="card-title">Add New Role</h3>
              <div class="card-toolbar">
                <button 
                  type="button"
                  class="btn btn-light btn-sm"
                  @click="cancelAddRole"
                >
                  Cancel
                </button>
              </div>
            </div>
            <div class="card-body">
              <form @submit.prevent="addRole">
                <div class="row g-9 mb-8">
                  <div class="col-md-6 fv-row">
                    <label class="required fs-6 fw-semibold mb-2">Role</label>
                    <select 
                      class="form-select form-select-solid" 
                      v-model="addRoleForm.role_id"
                      :disabled="isSubmitting"
                    >
                      <option value="">Select role...</option>
                      <option 
                        v-for="role in availableRoles" 
                        :key="role.id" 
                        :value="role.id"
                      >
                        {{ role.name }} ({{ role.code }})
                      </option>
                    </select>
                  </div>
                  <div class="col-md-3 fv-row">
                    <label class="fs-6 fw-semibold mb-2">Start Date</label>
                    <input
                      type="date"
                      class="form-control form-control-solid"
                      v-model="addRoleForm.start_on"
                      :disabled="isSubmitting"
                    />
                  </div>
                  <div class="col-md-3 fv-row">
                    <label class="fs-6 fw-semibold mb-2">End Date</label>
                    <input
                      type="date"
                      class="form-control form-control-solid"
                      v-model="addRoleForm.end_on"
                      :disabled="isSubmitting"
                    />
                    <div class="form-text">Leave blank for ongoing role</div>
                  </div>
                </div>
                <div class="d-flex justify-content-end">
                  <button
                    type="submit"
                    class="btn btn-primary"
                    :disabled="isSubmitting || !addRoleForm.role_id"
                  >
                    <span v-if="!isSubmitting" class="indicator-label">Add Role</span>
                    <span v-else class="indicator-progress">
                      Adding...
                      <span class="spinner-border spinner-border-sm align-middle ms-2"></span>
                    </span>
                  </button>
                </div>
              </form>
            </div>
          </div>
          <!--end::Add Role Form-->

          <!--begin::Edit Role Form-->
          <div v-if="editingMembership" class="card mb-8">
            <div class="card-header">
              <h3 class="card-title">Edit Role Assignment</h3>
              <div class="card-toolbar">
                <button 
                  type="button"
                  class="btn btn-light btn-sm"
                  @click="cancelEdit"
                >
                  Cancel
                </button>
              </div>
            </div>
            <div class="card-body">
              <form @submit.prevent="updateMembership">
                <div class="row g-9 mb-8">
                  <div class="col-md-6 fv-row">
                    <label class="fs-6 fw-semibold mb-2">Role</label>
                    <div class="form-control form-control-solid bg-light">
                      {{ editingMembership.role.name }} ({{ editingMembership.role.code }})
                    </div>
                  </div>
                  <div class="col-md-3 fv-row">
                    <label class="fs-6 fw-semibold mb-2">Start Date</label>
                    <input
                      type="date"
                      class="form-control form-control-solid"
                      v-model="editRoleForm.start_on"
                      :disabled="isSubmitting"
                    />
                  </div>
                  <div class="col-md-3 fv-row">
                    <label class="fs-6 fw-semibold mb-2">End Date</label>
                    <input
                      type="date"
                      class="form-control form-control-solid"
                      v-model="editRoleForm.end_on"
                      :disabled="isSubmitting"
                    />
                    <div class="form-text">Leave blank for ongoing role</div>
                  </div>
                </div>
                <div class="d-flex justify-content-end">
                  <button
                    type="submit"
                    class="btn btn-primary"
                    :disabled="isSubmitting"
                  >
                    <span v-if="!isSubmitting" class="indicator-label">Update Role</span>
                    <span v-else class="indicator-progress">
                      Updating...
                      <span class="spinner-border spinner-border-sm align-middle ms-2"></span>
                    </span>
                  </button>
                </div>
              </form>
            </div>
          </div>
          <!--end::Edit Role Form-->
        </div>
        <!--end::Modal body-->

        <!--begin::Modal footer-->
        <div class="modal-footer flex-center">
          <button
            type="button"
            class="btn btn-light"
            @click="closeModal"
            :disabled="isSubmitting"
          >
            Close
          </button>
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
  <!--end::Modal - Manage staff roles-->
</template>

<script setup lang="ts">
import { ref, reactive, computed, onMounted } from "vue";
import Swal from "sweetalert2";
import ApiService from "@/core/services/ApiService";

interface Props {
  staff: {
    id: string;
    contact?: {
      first_name: string;
      last_name: string;
      business_name?: string;
    };
  };
}

const props = defineProps<Props>();
const emit = defineEmits(['rolesUpdated', 'close']);

const modalRef = ref<HTMLElement | null>(null);
const isSubmitting = ref(false);
const showAddRoleForm = ref(false);
const editingMembership = ref<any>(null);

// Data
const roleMemberships = ref<any[]>([]);
const staffRoles = ref<any[]>([]);

// Forms
const addRoleForm = reactive({
  role_id: '',
  start_on: '',
  end_on: '',
});

const editRoleForm = reactive({
  start_on: '',
  end_on: '',
});

// Computed
const availableRoles = computed(() => {
  // Show all roles, but could filter out already assigned active roles
  return staffRoles.value;
});

// Methods
const getStaffName = (): string => {
  if (!props.staff.contact) return 'Unknown Staff';
  
  const { first_name, last_name, business_name } = props.staff.contact;
  
  if (business_name) return business_name;
  if (first_name || last_name) {
    return `${first_name || ''} ${last_name || ''}`.trim();
  }
  return 'Unknown Staff';
};

const fetchData = async () => {
  try {
    // Fetch staff role memberships
    const membershipsResponse = await ApiService.get(`/staff-role-memberships/?staff_id=${props.staff.id}`);
    roleMemberships.value = membershipsResponse.data.results || membershipsResponse.data || [];
    
    // Fetch all staff roles
    const rolesResponse = await ApiService.get('/staff-roles/');
    staffRoles.value = rolesResponse.data.results || rolesResponse.data || [];
  } catch (error) {
    console.error('Error fetching data:', error);
  }
};

const getRoleColor = (roleCode: string): string => {
  const colors: Record<string, string> = {
    PIC: 'primary',
    SIC: 'info',
    RN: 'success',
    PARAMEDIC: 'warning',
    MD: 'danger',
    RT: 'secondary',
  };
  return colors[roleCode] || 'secondary';
};

const getRoleStatus = (membership: any): string => {
  const today = new Date().toISOString().split('T')[0];
  
  if (membership.start_on && membership.start_on > today) {
    return 'future';
  }
  
  if (membership.end_on && membership.end_on < today) {
    return 'expired';
  }
  
  return 'active';
};

const formatDate = (dateString: string): string => {
  if (!dateString) return '';
  return new Date(dateString).toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
  });
};

const addRole = async () => {
  if (!addRoleForm.role_id) return;
  
  isSubmitting.value = true;
  
  try {
    const membershipData = {
      staff_id: props.staff.id,
      role_id: addRoleForm.role_id,
      start_on: addRoleForm.start_on || null,
      end_on: addRoleForm.end_on || null,
    };
    
    console.log('Creating role membership:', membershipData);
    await ApiService.post('/staff-role-memberships/', membershipData);
    
    Swal.fire({
      title: "Success!",
      text: "Role assigned successfully!",
      icon: "success",
      timer: 1500,
      showConfirmButton: false
    });
    
    // Refresh data
    await fetchData();
    cancelAddRole();
  } catch (error: any) {
    console.error('Error adding role:', error);
    const errorMessage = error.response?.data?.detail || 
                        error.response?.data?.message || 
                        error.message || 
                        "Failed to assign role. Please try again.";
    
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

const editMembership = (membership: any) => {
  editingMembership.value = membership;
  editRoleForm.start_on = membership.start_on || '';
  editRoleForm.end_on = membership.end_on || '';
  showAddRoleForm.value = false;
};

const updateMembership = async () => {
  if (!editingMembership.value) return;
  
  isSubmitting.value = true;
  
  try {
    const updateData = {
      start_on: editRoleForm.start_on || null,
      end_on: editRoleForm.end_on || null,
    };
    
    console.log('Updating role membership:', updateData);
    await ApiService.patch(`/staff-role-memberships/${editingMembership.value.id}/`, updateData);
    
    Swal.fire({
      title: "Success!",
      text: "Role assignment updated successfully!",
      icon: "success",
      timer: 1500,
      showConfirmButton: false
    });
    
    // Refresh data
    await fetchData();
    cancelEdit();
  } catch (error: any) {
    console.error('Error updating role:', error);
    const errorMessage = error.response?.data?.detail || 
                        error.response?.data?.message || 
                        error.message || 
                        "Failed to update role assignment. Please try again.";
    
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

const deleteMembership = async (membership: any) => {
  const result = await Swal.fire({
    title: "Remove Role Assignment",
    text: `Are you sure you want to remove the ${membership.role.name} role from this staff member?`,
    icon: "warning",
    showCancelButton: true,
    confirmButtonText: "Yes, remove it!",
    cancelButtonText: "Cancel",
    confirmButtonColor: "#d33"
  });
  
  if (result.isConfirmed) {
    try {
      isSubmitting.value = true;
      await ApiService.delete(`/staff-role-memberships/${membership.id}/`);
      
      Swal.fire({
        title: "Removed!",
        text: "Role assignment has been removed.",
        icon: "success",
        timer: 1500,
        showConfirmButton: false
      });
      
      // Refresh data
      await fetchData();
    } catch (error) {
      Swal.fire("Error", "Failed to remove role assignment.", "error");
    } finally {
      isSubmitting.value = false;
    }
  }
};

const cancelAddRole = () => {
  showAddRoleForm.value = false;
  addRoleForm.role_id = '';
  addRoleForm.start_on = '';
  addRoleForm.end_on = '';
};

const cancelEdit = () => {
  editingMembership.value = null;
  editRoleForm.start_on = '';
  editRoleForm.end_on = '';
};

const closeModal = () => {
  emit('rolesUpdated');
};

onMounted(() => {
  fetchData();
  
  // Set default start date to today
  addRoleForm.start_on = new Date().toISOString().split('T')[0];
  
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