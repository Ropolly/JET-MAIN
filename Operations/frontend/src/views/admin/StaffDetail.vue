<template>
  <div v-if="loading" class="d-flex justify-content-center py-10">
    <div class="spinner-border text-primary" role="status">
      <span class="visually-hidden">Loading...</span>
    </div>
  </div>

  <div v-else-if="error" class="alert alert-danger">
    {{ error }}
  </div>

  <div v-else-if="staff">
    <!--begin::Header-->
    <div class="card mb-5 mb-xl-10">
      <div class="card-body pt-9 pb-0">
        <!--begin::Details-->
        <div class="d-flex flex-wrap flex-sm-nowrap">
          <!--begin::Image-->
          <div class="me-7 mb-4">
            <div class="symbol symbol-100px symbol-lg-160px symbol-fixed position-relative">
              <div class="symbol-label bg-light-info">
                <i class="ki-duotone ki-user fs-2hx text-info">
                  <span class="path1"></span>
                  <span class="path2"></span>
                </i>
              </div>
              <div class="position-absolute translate-middle bottom-0 start-100 mb-6 bg-success rounded-circle border border-4 border-body h-20px w-20px"></div>
            </div>
          </div>
          <!--end::Image-->

          <!--begin::Wrapper-->
          <div class="flex-grow-1">
            <!--begin::Head-->
            <div class="d-flex justify-content-between align-items-start flex-wrap mb-2">
              <!--begin::Details-->
              <div class="d-flex flex-column">
                <!--begin::Name-->
                <div class="d-flex align-items-center mb-2">
                  <h1 class="text-gray-800 fs-2 fw-bold me-1">{{ getStaffName() }}</h1>
                  <span :class="`badge badge-light-${staff.active ? 'success' : 'danger'} fs-8 fw-bold ms-2`">
                    {{ staff.active ? 'Active' : 'Inactive' }}
                  </span>
                </div>
                <!--end::Name-->

                <!--begin::Info-->
                <div class="d-flex flex-wrap fw-semibold fs-6 mb-4 pe-2">
                  <span class="d-flex align-items-center text-gray-500 me-5 mb-2">
                    <KTIcon icon-name="profile-circle" icon-class="fs-4 me-1" />
                    Staff Member
                  </span>
                  <span v-if="staff.contact?.email" class="d-flex align-items-center text-gray-500 me-5 mb-2">
                    <KTIcon icon-name="sms" icon-class="fs-4 me-1" />
                    {{ staff.contact.email }}
                  </span>
                  <span v-if="staff.contact?.phone" class="d-flex align-items-center text-gray-500 me-5 mb-2">
                    <KTIcon icon-name="phone" icon-class="fs-4 me-1" />
                    {{ staff.contact.phone }}
                  </span>
                </div>
                <!--end::Info-->
              </div>
              <!--end::Details-->
            </div>
            <!--end::Head-->

            <!--begin::Stats-->
            <div class="d-flex flex-wrap flex-stack">
              <!--begin::Wrapper-->
              <div class="d-flex flex-column flex-grow-1 pe-8">
                <!--begin::Stats-->
                <div class="d-flex flex-wrap">
                  <!--begin::Stat-->
                  <div class="border border-gray-300 border-dashed rounded min-w-125px py-3 px-4 me-6 mb-3">
                    <div class="d-flex align-items-center">
                      <div class="fs-2 fw-bold text-gray-900 me-2">{{ getActiveRoles().length }}</div>
                      <div class="fs-6 fw-semibold text-gray-500">Active Roles</div>
                    </div>
                  </div>
                  <!--end::Stat-->

                  <!--begin::Stat-->
                  <div class="border border-gray-300 border-dashed rounded min-w-125px py-3 px-4 me-6 mb-3">
                    <div class="d-flex align-items-center">
                      <div class="fs-2 fw-bold text-gray-900 me-2">{{ getTotalAssignments() }}</div>
                      <div class="fs-6 fw-semibold text-gray-500">Total Assignments</div>
                    </div>
                  </div>
                  <!--end::Stat-->

                  <!--begin::Stat-->
                  <div class="border border-gray-300 border-dashed rounded min-w-125px py-3 px-4 me-6 mb-3">
                    <div class="d-flex align-items-center">
                      <div class="fs-2 fw-bold text-gray-900 me-2">{{ formatDate(staff.created_on) }}</div>
                      <div class="fs-6 fw-semibold text-gray-500">Joined</div>
                    </div>
                  </div>
                  <!--end::Stat-->
                </div>
                <!--end::Stats-->
              </div>
              <!--end::Wrapper-->
            </div>
            <!--end::Stats-->
          </div>
          <!--end::Wrapper-->
        </div>
        <!--end::Details-->

        <!--begin::Navs-->
        <ul class="nav nav-stretch nav-line-tabs nav-line-tabs-2x border-transparent fs-5 fw-bold">
          <li class="nav-item mt-2">
            <a
              class="nav-link text-active-primary ms-0 me-10 py-5"
              :class="{ active: activeTab === 'overview' }"
              @click="activeTab = 'overview'"
              href="#"
            >
              Overview
            </a>
          </li>
          <li class="nav-item mt-2">
            <a
              class="nav-link text-active-primary ms-0 me-10 py-5"
              :class="{ active: activeTab === 'roles' }"
              @click="activeTab = 'roles'"
              href="#"
            >
              Roles & History
            </a>
          </li>
          <li class="nav-item mt-2">
            <a
              class="nav-link text-active-primary ms-0 me-10 py-5"
              :class="{ active: activeTab === 'assignments' }"
              @click="activeTab = 'assignments'"
              href="#"
            >
              Trip Assignments
            </a>
          </li>
        </ul>
        <!--end::Navs-->
      </div>
    </div>
    <!--end::Header-->

    <!--begin::Content-->
    <div class="row gy-5 g-xl-8">
      <!--begin::Overview Tab-->
      <div v-if="activeTab === 'overview'" class="col-xl-12">
        <div class="row gy-5 g-xl-8">
          <!--begin::Contact Information-->
          <div class="col-xl-6">
            <div class="card card-flush h-xl-100">
              <div class="card-header">
                <h3 class="card-title">Contact Information</h3>
                <div class="card-toolbar">
                  <button 
                    class="btn btn-light-primary btn-sm"
                    @click="editContact"
                  >
                    <KTIcon icon-name="pencil" icon-class="fs-4 me-1" />
                    Edit
                  </button>
                </div>
              </div>
              <div class="card-body">
                <div class="mb-7">
                  <div class="fw-semibold text-gray-600 fs-7">Full Name</div>
                  <div class="fw-bold fs-6 text-gray-800">
                    {{ staff.contact_info?.business_name || 
                       `${staff.contact_info?.first_name || ''} ${staff.contact_info?.last_name || ''}`.trim() || 
                       'No name provided' }}
                  </div>
                </div>
                <div class="mb-7">
                  <div class="fw-semibold text-gray-600 fs-7">Email</div>
                  <div class="fw-bold fs-6 text-gray-800">{{ staff.contact_info?.email || 'No email' }}</div>
                </div>
                <div class="mb-7">
                  <div class="fw-semibold text-gray-600 fs-7">Phone</div>
                  <div class="fw-bold fs-6 text-gray-800">{{ staff.contact_info?.phone || 'No phone' }}</div>
                </div>
                <div class="mb-0">
                  <div class="fw-semibold text-gray-600 fs-7">Contact ID</div>
                  <div class="fw-bold fs-6 text-gray-800 font-monospace">{{ staff.contact_id }}</div>
                </div>
              </div>
            </div>
          </div>
          <!--end::Contact Information-->

          <!--begin::Staff Information-->
          <div class="col-xl-6">
            <div class="card card-flush h-xl-100">
              <div class="card-header">
                <h3 class="card-title">Staff Information</h3>
                <div class="card-toolbar">
                  <button 
                    class="btn btn-light-primary btn-sm"
                    @click="editStaff"
                  >
                    <KTIcon icon-name="pencil" icon-class="fs-4 me-1" />
                    Edit
                  </button>
                </div>
              </div>
              <div class="card-body">
                <div class="mb-7">
                  <div class="fw-semibold text-gray-600 fs-7">Status</div>
                  <div>
                    <span :class="`badge badge-light-${staff.active ? 'success' : 'danger'} fs-7 fw-bold`">
                      {{ staff.active ? 'Active' : 'Inactive' }}
                    </span>
                  </div>
                </div>
                <div class="mb-7">
                  <div class="fw-semibold text-gray-600 fs-7">Staff ID</div>
                  <div class="fw-bold fs-6 text-gray-800 font-monospace">{{ staff.id }}</div>
                </div>
                <div class="mb-7">
                  <div class="fw-semibold text-gray-600 fs-7">Created Date</div>
                  <div class="fw-bold fs-6 text-gray-800">{{ formatDate(staff.created_on) }}</div>
                </div>
                <div class="mb-0">
                  <div class="fw-semibold text-gray-600 fs-7">Notes</div>
                  <div class="fw-bold fs-6 text-gray-800">
                    {{ staff.notes || 'No notes provided' }}
                  </div>
                </div>
              </div>
            </div>
          </div>
          <!--end::Staff Information-->

          <!--begin::Current Roles-->
          <div class="col-xl-12">
            <div class="card card-flush">
              <div class="card-header">
                <h3 class="card-title">Current Active Roles</h3>
                <div class="card-toolbar">
                  <button 
                    class="btn btn-primary btn-sm"
                    @click="manageRoles"
                  >
                    <KTIcon icon-name="user-tick" icon-class="fs-4 me-1" />
                    Manage Roles
                  </button>
                </div>
              </div>
              <div class="card-body">
                <div v-if="getActiveRoles().length === 0" class="text-center py-10">
                  <div class="text-muted fs-4 mb-5">No active roles assigned</div>
                  <button 
                    class="btn btn-primary"
                    @click="manageRoles"
                  >
                    Assign First Role
                  </button>
                </div>
                <div v-else class="d-flex flex-wrap gap-3">
                  <div 
                    v-for="role in getActiveRoles()" 
                    :key="role.id"
                    class="d-flex align-items-center border border-gray-300 rounded p-4"
                  >
                    <span 
                      :class="`badge badge-light-${getRoleColor(role.code)} fs-7 fw-bold me-3`"
                    >
                      {{ role.code }}
                    </span>
                    <div>
                      <div class="fw-bold">{{ role.name }}</div>
                      <div class="text-muted fs-7">Active role</div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
          <!--end::Current Roles-->
        </div>
      </div>
      <!--end::Overview Tab-->

      <!--begin::Roles Tab-->
      <div v-if="activeTab === 'roles'" class="col-xl-12">
        <div class="card card-flush">
          <div class="card-header">
            <h3 class="card-title">Role Assignment History</h3>
            <div class="card-toolbar">
              <button 
                class="btn btn-primary btn-sm"
                @click="manageRoles"
              >
                <KTIcon icon-name="plus" icon-class="fs-4 me-1" />
                Add Role
              </button>
            </div>
          </div>
          <div class="card-body">
            <div v-if="staff.role_memberships?.length === 0" class="text-center py-10">
              <div class="text-muted fs-4 mb-5">No role assignments found</div>
              <button 
                class="btn btn-primary"
                @click="manageRoles"
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
                    <th>Duration</th>
                    <th>Status</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="membership in staff.role_memberships" :key="membership.id">
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
                      <span v-else class="text-success">Ongoing</span>
                    </td>
                    <td>
                      {{ getRoleDuration(membership) }}
                    </td>
                    <td>
                      <span :class="`badge badge-light-${getRoleStatusColor(membership)}`">
                        {{ getRoleStatus(membership) }}
                      </span>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </div>
      <!--end::Roles Tab-->

      <!--begin::Assignments Tab-->
      <div v-if="activeTab === 'assignments'" class="col-xl-12">
        <div class="card card-flush">
          <div class="card-header">
            <h3 class="card-title">Trip Assignments</h3>
          </div>
          <div class="card-body">
            <div class="text-center py-10">
              <div class="text-muted fs-4 mb-5">Trip assignments feature coming soon</div>
              <div class="text-gray-600">
                This will show all trips where this staff member was assigned as crew.
              </div>
            </div>
          </div>
        </div>
      </div>
      <!--end::Assignments Tab-->
    </div>
    <!--end::Content-->

    <!-- Modals -->
    <EditStaffModal 
      v-if="showEditModal" 
      :staff="staff" 
      @staffUpdated="onStaffUpdated"
      @close="showEditModal = false"
    />
    <ManageStaffRolesModal 
      v-if="showRolesModal"
      :staff="staff"
      @rolesUpdated="onRolesUpdated"
      @close="showRolesModal = false"
    />
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, onMounted } from "vue";
import { useRoute, useRouter } from "vue-router";
import ApiService from "@/core/services/ApiService";
import EditStaffModal from "@/components/modals/EditStaffModal.vue";
import ManageStaffRolesModal from "@/components/modals/ManageStaffRolesModal.vue";
import { useToolbar, createToolbarActions } from "@/core/helpers/toolbar";

export default defineComponent({
  name: "staff-detail",
  components: {
    EditStaffModal,
    ManageStaffRolesModal,
  },
  setup() {
    const route = useRoute();
    const router = useRouter();
    const { setToolbarActions } = useToolbar();
    
    const staff = ref<any>(null);
    const loading = ref(false);
    const error = ref<string | null>(null);
    const activeTab = ref('overview');
    const showEditModal = ref(false);
    const showRolesModal = ref(false);

    const fetchStaff = async () => {
      try {
        loading.value = true;
        error.value = null;
        const { data } = await ApiService.get(`/staff/${route.params.id}/`);
        staff.value = data;
        console.log('Staff loaded:', data);
      } catch (err: any) {
        error.value = err.response?.data?.detail || "Failed to fetch staff details";
        console.error("Error fetching staff:", err);
      } finally {
        loading.value = false;
      }
    };

    const getStaffName = (): string => {
      if (!staff.value?.contact) return 'Unknown Staff';
      
      const { first_name, last_name, business_name } = staff.value.contact;
      
      if (business_name) return business_name;
      if (first_name || last_name) {
        return `${first_name || ''} ${last_name || ''}`.trim();
      }
      return 'Unknown Staff';
    };

    const getActiveRoles = () => {
      if (!staff.value?.role_memberships) return [];
      
      const today = new Date().toISOString().split('T')[0];
      
      return staff.value.role_memberships
        .filter((membership: any) => {
          const startDate = membership.start_on;
          const endDate = membership.end_on;
          
          const startValid = !startDate || startDate <= today;
          const endValid = !endDate || endDate >= today;
          
          return startValid && endValid;
        })
        .map((membership: any) => membership.role);
    };

    const getTotalAssignments = (): number => {
      return staff.value?.role_memberships?.length || 0;
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
        return 'Future';
      }
      
      if (membership.end_on && membership.end_on < today) {
        return 'Expired';
      }
      
      return 'Active';
    };

    const getRoleStatusColor = (membership: any): string => {
      const status = getRoleStatus(membership);
      const colors: Record<string, string> = {
        Active: 'success',
        Future: 'warning',
        Expired: 'secondary',
      };
      return colors[status] || 'secondary';
    };

    const getRoleDuration = (membership: any): string => {
      const startDate = membership.start_on ? new Date(membership.start_on) : null;
      const endDate = membership.end_on ? new Date(membership.end_on) : new Date();
      
      if (!startDate) return 'Unknown';
      
      const diffTime = endDate.getTime() - startDate.getTime();
      const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
      
      if (diffDays < 30) return `${diffDays} days`;
      if (diffDays < 365) return `${Math.floor(diffDays / 30)} months`;
      return `${Math.floor(diffDays / 365)} years`;
    };

    const formatDate = (dateString: string): string => {
      if (!dateString) return '';
      return new Date(dateString).toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
      });
    };

    const editStaff = () => {
      showEditModal.value = true;
    };

    const editContact = () => {
      if (staff.value?.contact_id) {
        router.push(`/admin/contacts/contacts/${staff.value.contact_id}`);
      }
    };

    const manageRoles = () => {
      showRolesModal.value = true;
    };

    const onStaffUpdated = () => {
      showEditModal.value = false;
      fetchStaff();
    };

    const onRolesUpdated = () => {
      showRolesModal.value = false;
      fetchStaff();
    };

    const goBack = () => {
      router.push('/admin/staff');
    };

    onMounted(() => {
      fetchStaff();
      
      // Setup toolbar actions
      setToolbarActions([
        createToolbarActions.secondary('back', 'Back to Staff', goBack, 'arrow-left'),
        createToolbarActions.primary('edit', 'Edit Staff', editStaff, 'pencil'),
        createToolbarActions.secondary('manage-roles', 'Manage Roles', manageRoles, 'user-tick'),
      ]);
    });

    return {
      staff,
      loading,
      error,
      activeTab,
      showEditModal,
      showRolesModal,
      getStaffName,
      getActiveRoles,
      getTotalAssignments,
      getRoleColor,
      getRoleStatus,
      getRoleStatusColor,
      getRoleDuration,
      formatDate,
      editStaff,
      editContact,
      manageRoles,
      onStaffUpdated,
      onRolesUpdated,
    };
  },
});
</script>