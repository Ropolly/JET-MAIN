<template>
  <!--begin::Card-->
  <div class="card">
    <!--begin::Card header-->
    <div class="card-header border-0 pt-6">
      <!--begin::Card title-->
      <div class="card-title">
        <!--begin::Search-->
        <div class="d-flex align-items-center position-relative my-1">
          <KTIcon
            icon-name="magnifier"
            icon-class="fs-1 position-absolute ms-6"
          />
          <input
            v-model="search"
            @input="searchItems()"
            type="text"
            class="form-control form-control-solid w-250px ps-14"
            placeholder="Search Staff Roles"
          />
        </div>
        <!--end::Search-->
      </div>
      <!--begin::Card title-->

      <!--begin::Card toolbar-->
      <div class="card-toolbar">
        <!--begin::Toolbar-->
        <div
          v-if="selectedIds.length === 0"
          class="d-flex justify-content-end"
        >
          <!-- Add Staff Role button is in the main toolbar -->
        </div>
        <!--end::Toolbar-->

        <!--begin::Group actions-->
        <div v-else class="d-flex justify-content-end align-items-center">
          <div class="fw-bold me-5">
            <span class="me-2">{{ selectedIds.length }}</span>Selected
          </div>
          <button
            type="button"
            class="btn btn-danger"
            @click="deleteFewRoles()"
          >
            Delete Selected
          </button>
        </div>
        <!--end::Group actions-->
      </div>
      <!--end::Card toolbar-->
    </div>
    <!--end::Card header-->

    <!--begin::Card body-->
    <div class="card-body pt-0">
      <KTDatatable
        @on-sort="sort"
        @on-items-select="onItemSelect"
        @on-items-per-page-change="onItemsPerPageChange"
        :data="staffRoles"
        :header="headerConfig"
        :checkbox-enabled="true"
        :loading="loading"
      >
        <template v-slot:role="{ row: role }">
          <div class="d-flex align-items-center">
            <span 
              :class="`badge badge-light-${getRoleColor(role.code)} fs-6 fw-bold me-3`"
            >
              {{ role.code }}
            </span>
            <div class="d-flex flex-column">
              <div class="text-gray-800 fs-6 fw-bold">{{ role.name }}</div>
              <div class="text-muted fs-7">{{ role.code }}</div>
            </div>
          </div>
        </template>

        <template v-slot:usage="{ row: role }">
          <div class="d-flex align-items-center">
            <div class="fs-6 fw-bold text-gray-900 me-2">{{ getRoleUsage(role) }}</div>
            <div class="fs-7 text-gray-500">active assignments</div>
          </div>
        </template>

        <template v-slot:created="{ row: role }">
          {{ formatDate(role.created_on) }}
        </template>

        <template v-slot:actions="{ row: role }">
          <a
            href="#"
            class="btn btn-sm btn-light btn-active-light-primary"
            data-kt-menu-trigger="click"
            data-kt-menu-placement="bottom-end"
            data-kt-menu-flip="top-end"
            >Actions
            <KTIcon icon-name="down" icon-class="fs-5 m-0" />
          </a>
          <!--begin::Menu-->
          <div
            class="menu menu-sub menu-sub-dropdown menu-column menu-rounded menu-gray-600 menu-state-bg-light-primary fw-semibold fs-7 w-175px py-4"
            data-kt-menu="true"
          >
            <!--begin::Menu item-->
            <div class="menu-item px-3">
              <a @click="handleView(role)" class="menu-link px-3">
                <KTIcon icon-name="eye" icon-class="fs-6 me-2" />
                View Details
              </a>
            </div>
            <!--end::Menu item-->
            <!--begin::Menu item-->
            <div class="menu-item px-3">
              <a @click="handleEdit(role)" class="menu-link px-3">
                <KTIcon icon-name="pencil" icon-class="fs-6 me-2" />
                Edit Role
              </a>
            </div>
            <!--end::Menu item-->
            <!--begin::Menu item-->
            <div class="menu-item px-3">
              <a @click="handleViewAssignments(role)" class="menu-link px-3">
                <KTIcon icon-name="people" icon-class="fs-6 me-2" />
                View Assignments
              </a>
            </div>
            <!--end::Menu item-->
            <!--begin::Separator-->
            <div class="separator my-2"></div>
            <!--end::Separator-->
            <!--begin::Menu item-->
            <div class="menu-item px-3">
              <a @click="handleDelete(role)" class="menu-link px-3 text-danger">
                <KTIcon icon-name="trash" icon-class="fs-6 me-2" />
                Delete Role
              </a>
            </div>
            <!--end::Menu item-->
          </div>
          <!--end::Menu-->
        </template>
      </KTDatatable>
    </div>
    <!--end::Card body-->
  </div>
  <!--end::Card-->
  
  <!-- Create Staff Role Modal -->
  <CreateStaffRoleModal @roleCreated="onRoleCreated" />
  <!-- Edit Staff Role Modal -->
  <EditStaffRoleModal 
    v-if="editingRole" 
    :role="editingRole" 
    @roleUpdated="onRoleUpdated"
    @close="editingRole = null"
  />
  <!-- View Role Assignments Modal -->
  <ViewRoleAssignmentsModal 
    v-if="viewingAssignmentsRole"
    :role="viewingAssignmentsRole"
    @close="viewingAssignmentsRole = null"
  />
</template>

<script lang="ts">
import { defineComponent, ref, onMounted } from "vue";
import ApiService from "@/core/services/ApiService";
import KTDatatable from "@/components/kt-datatable/KTDataTable.vue";
import type { Sort } from "@/components/kt-datatable/table-partials/models";
import arraySort from "array-sort";
import { MenuComponent } from "@/assets/ts/components";
import Swal from "sweetalert2";
import { useRouter } from "vue-router";
import CreateStaffRoleModal from "@/components/modals/CreateStaffRoleModal.vue";
import EditStaffRoleModal from "@/components/modals/EditStaffRoleModal.vue";
import ViewRoleAssignmentsModal from "@/components/modals/ViewRoleAssignmentsModal.vue";
import { useToolbar, createToolbarActions } from "@/core/helpers/toolbar";

interface StaffRole {
  id: string;
  code: string;
  name: string;
  created_on: string;
  usage_count?: number;
}

export default defineComponent({
  name: "staff-roles-management",
  components: {
    KTDatatable,
    CreateStaffRoleModal,
    EditStaffRoleModal,
    ViewRoleAssignmentsModal,
  },
  setup() {
    const router = useRouter();
    const staffRoles = ref<StaffRole[]>([]);
    const roleMemberships = ref<any[]>([]);
    const loading = ref(false);
    const error = ref<string | null>(null);
    const editingRole = ref<StaffRole | null>(null);
    const viewingAssignmentsRole = ref<StaffRole | null>(null);
    const { setToolbarActions } = useToolbar();

    const headerConfig = ref([
      {
        columnName: "Role",
        columnLabel: "role",
        sortEnabled: true,
      },
      {
        columnName: "Usage",
        columnLabel: "usage",
        sortEnabled: false,
      },
      {
        columnName: "Created",
        columnLabel: "created",
        sortEnabled: true,
      },
      {
        columnName: "Actions",
        columnLabel: "actions",
      },
    ]);

    const initData = ref<Array<StaffRole>>([]);
    const selectedIds = ref<Array<string>>([]);
    const search = ref<string>("");

    // Methods
    const fetchStaffRoles = async () => {
      try {
        loading.value = true;
        error.value = null;
        
        // Fetch roles
        const { data } = await ApiService.get("/staff-roles/");
        staffRoles.value = data.results || data;
        
        // Fetch role memberships for usage count
        const membershipsResponse = await ApiService.get("/staff-role-memberships/");
        roleMemberships.value = membershipsResponse.data.results || membershipsResponse.data;
        
        initData.value.splice(0, staffRoles.value.length, ...staffRoles.value);
      } catch (err: any) {
        error.value = err.response?.data?.detail || "Failed to fetch staff roles";
        console.error("Error fetching staff roles:", err);
      } finally {
        loading.value = false;
        setTimeout(() => {
          MenuComponent.reinitialization();
        }, 100);
      }
    };

    const openCreateRoleModal = () => {
      const modalElement = document.getElementById('kt_modal_create_staff_role');
      if (modalElement) {
        try {
          const { Modal } = require('bootstrap');
          const modal = new Modal(modalElement);
          modal.show();
        } catch (error) {
          console.error('Error opening modal:', error);
          // Fallback: trigger modal via data attributes
          modalElement.classList.add('show');
          modalElement.style.display = 'block';
          document.body.classList.add('modal-open');
        }
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
        EMT: 'dark',
        DISPATCHER: 'info',
      };
      return colors[roleCode] || 'secondary';
    };

    const getRoleUsage = (role: StaffRole): number => {
      const today = new Date().toISOString().split('T')[0];
      
      return roleMemberships.value.filter(membership => {
        if (membership.role_id !== role.id) return false;
        
        const startDate = membership.start_on;
        const endDate = membership.end_on;
        
        const startValid = !startDate || startDate <= today;
        const endValid = !endDate || endDate >= today;
        
        return startValid && endValid;
      }).length;
    };

    const formatDate = (dateString: string): string => {
      if (!dateString) return '';
      return new Date(dateString).toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
      });
    };

    const handleView = (role: StaffRole) => {
      // Show role details in a modal or navigate to detail page
      Swal.fire({
        title: role.name,
        html: `
          <div class="text-start">
            <p><strong>Code:</strong> ${role.code}</p>
            <p><strong>Name:</strong> ${role.name}</p>
            <p><strong>Active Assignments:</strong> ${getRoleUsage(role)}</p>
            <p><strong>Created:</strong> ${formatDate(role.created_on)}</p>
          </div>
        `,
        icon: "info",
        confirmButtonText: "OK"
      });
    };

    const handleEdit = (role: StaffRole) => {
      editingRole.value = role;
    };

    const handleViewAssignments = (role: StaffRole) => {
      viewingAssignmentsRole.value = role;
    };

    const handleDelete = async (role: StaffRole) => {
      const usage = getRoleUsage(role);
      
      let confirmText = `Are you sure you want to delete the "${role.name}" role?`;
      if (usage > 0) {
        confirmText += ` This role is currently assigned to ${usage} staff member(s).`;
      }
      confirmText += ' This action cannot be undone.';
      
      Swal.fire({
        title: "Delete Staff Role",
        text: confirmText,
        icon: "warning",
        showCancelButton: true,
        confirmButtonText: "Yes, delete it!",
        cancelButtonText: "Cancel",
        confirmButtonColor: "#d33"
      }).then(async (result) => {
        if (result.isConfirmed) {
          try {
            await ApiService.delete(`/staff-roles/${role.id}/`);
            
            Swal.fire({
              title: "Deleted!",
              text: "Staff role has been deleted successfully.",
              icon: "success"
            }).then(() => {
              fetchStaffRoles();
            });
          } catch (error: any) {
            const errorMessage = error.response?.data?.detail || "Failed to delete the staff role.";
            Swal.fire({
              title: "Error",
              text: errorMessage,
              icon: "error"
            });
          }
        }
      });
    };

    const deleteFewRoles = async () => {
      if (selectedIds.value.length === 0) return;
      
      // Check usage for selected roles
      const rolesWithUsage = selectedIds.value.map(id => {
        const role = staffRoles.value.find(r => r.id === id);
        return { role, usage: role ? getRoleUsage(role) : 0 };
      });
      
      const totalUsage = rolesWithUsage.reduce((sum, item) => sum + item.usage, 0);
      
      let confirmText = `Are you sure you want to delete ${selectedIds.value.length} staff role(s)?`;
      if (totalUsage > 0) {
        confirmText += ` These roles have a total of ${totalUsage} active assignments.`;
      }
      confirmText += ' This action cannot be undone.';
      
      const result = await Swal.fire({
        title: "Delete Staff Roles",
        text: confirmText,
        icon: "warning",
        showCancelButton: true,
        confirmButtonText: "Yes, delete them!",
        cancelButtonText: "Cancel",
        confirmButtonColor: "#d33"
      });
      
      if (result.isConfirmed) {
        try {
          loading.value = true;
          
          for (const roleId of selectedIds.value) {
            await ApiService.delete(`/staff-roles/${roleId}/`);
          }
          
          selectedIds.value.length = 0;
          
          Swal.fire({
            title: "Deleted!",
            text: "Selected staff roles have been deleted successfully.",
            icon: "success"
          }).then(() => {
            fetchStaffRoles();
          });
        } catch (error) {
          console.error("Error deleting staff roles:", error);
          Swal.fire({
            title: "Error",
            text: "Failed to delete some staff roles. Please try again.",
            icon: "error"
          });
        } finally {
          loading.value = false;
        }
      }
    };

    const sort = (sort: Sort) => {
      const reverse: boolean = sort.order === "asc";
      if (sort.label) {
        arraySort(staffRoles.value, sort.label, { reverse });
      }
    };

    const onItemSelect = (selectedItems: Array<string>) => {
      selectedIds.value = selectedItems;
    };

    const searchItems = () => {
      staffRoles.value.splice(0, staffRoles.value.length, ...initData.value);
      if (search.value !== "") {
        let results: Array<StaffRole> = [];
        for (let j = 0; j < initData.value.length; j++) {
          if (searchingFunc(initData.value[j], search.value)) {
            results.push(initData.value[j]);
          }
        }
        staffRoles.value.splice(0, staffRoles.value.length, ...results);
      }
      MenuComponent.reinitialization();
    };

    const searchingFunc = (obj: any, value: string): boolean => {
      for (let key in obj) {
        if (!Number.isInteger(obj[key]) && !(typeof obj[key] === "object")) {
          if (obj[key]?.toString().toLowerCase().indexOf(value.toLowerCase()) != -1) {
            return true;
          }
        }
      }
      return false;
    };

    const onItemsPerPageChange = () => {
      setTimeout(() => {
        MenuComponent.reinitialization();
      }, 0);
    };

    const onRoleCreated = (newRole: StaffRole) => {
      console.log('New staff role created:', newRole);
      fetchStaffRoles();
    };

    const onRoleUpdated = (updatedRole: StaffRole) => {
      console.log('Staff role updated:', updatedRole);
      editingRole.value = null;
      fetchStaffRoles();
    };

    onMounted(() => {
      fetchStaffRoles();
      setTimeout(() => {
        MenuComponent.reinitialization();
      }, 200);

      // Setup toolbar actions
      setToolbarActions([
        createToolbarActions.primary('add-staff-role', 'Add Staff Role', openCreateRoleModal, 'plus')
      ]);
    });

    return {
      search,
      searchItems,
      staffRoles,
      headerConfig,
      loading,
      error,
      sort,
      onItemSelect,
      selectedIds,
      deleteFewRoles,
      onItemsPerPageChange,
      openCreateRoleModal,
      handleView,
      handleEdit,
      handleViewAssignments,
      handleDelete,
      getRoleColor,
      getRoleUsage,
      formatDate,
      onRoleCreated,
      onRoleUpdated,
      editingRole,
      viewingAssignmentsRole,
    };
  },
});
</script>