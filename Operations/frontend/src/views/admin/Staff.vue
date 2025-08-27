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
            placeholder="Search Staff"
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
          <!-- Add Staff button is in the main toolbar -->
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
            @click="deleteFewStaff()"
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
        @page-change="onPageChange"
        :data="staff"
        :header="headerConfig"
        :checkbox-enabled="true"
        :loading="loading"
        :total="totalItems"
        :current-page="currentPage"
        :items-per-page="pageSize"
      >
        <template v-slot:staff="{ row: staffMember }">
          <div class="d-flex align-items-center">
            <div class="symbol symbol-circle symbol-50px overflow-hidden me-3">
              <div class="symbol-label bg-light-info">
                <i class="ki-duotone ki-user fs-2x text-info">
                  <span class="path1"></span>
                  <span class="path2"></span>
                </i>
              </div>
            </div>
            <div class="d-flex flex-column">
              <a @click.prevent="navigateToStaff(staffMember.id)" href="#" class="text-gray-800 text-hover-primary mb-1 fs-6 fw-bold">
                {{ getStaffName(staffMember) }}
              </a>
              <span class="text-muted fs-7">{{ getContactInfo(staffMember) }}</span>
            </div>
          </div>
        </template>

        <template v-slot:roles="{ row: staffMember }">
          <div class="d-flex flex-wrap gap-2">
            <span 
              v-for="role in getActiveRoles(staffMember)" 
              :key="role.id" 
              :class="`badge badge-light-${getRoleColor(role.code)} fs-7 fw-bold`"
            >
              {{ role.name }}
            </span>
            <span v-if="getActiveRoles(staffMember).length === 0" class="text-muted fs-7">
              No roles assigned
            </span>
          </div>
        </template>

        <template v-slot:status="{ row: staffMember }">
          <span :class="`badge badge-light-${staffMember.active ? 'success' : 'danger'} fs-7 fw-bold`">
            {{ staffMember.active ? 'Active' : 'Inactive' }}
          </span>
        </template>

        <template v-slot:contact="{ row: staffMember }">
          <div v-if="staffMember.contact">
            <div class="fw-bold">{{ staffMember.contact.email || 'No email' }}</div>
            <div class="text-muted fs-7">{{ staffMember.contact.phone || 'No phone' }}</div>
          </div>
          <span v-else class="text-muted">No contact info</span>
        </template>

        <template v-slot:actions="{ row: staffMember }">
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
              <a @click="handleView(staffMember)" class="menu-link px-3">
                <KTIcon icon-name="eye" icon-class="fs-6 me-2" />
                View Details
              </a>
            </div>
            <!--end::Menu item-->
            <!--begin::Menu item-->
            <div class="menu-item px-3">
              <a @click="handleEdit(staffMember)" class="menu-link px-3">
                <KTIcon icon-name="pencil" icon-class="fs-6 me-2" />
                Edit Staff
              </a>
            </div>
            <!--end::Menu item-->
            <!--begin::Menu item-->
            <div class="menu-item px-3">
              <a @click="handleManageRoles(staffMember)" class="menu-link px-3">
                <KTIcon icon-name="user-tick" icon-class="fs-6 me-2" />
                Manage Roles
              </a>
            </div>
            <!--end::Menu item-->
            <!--begin::Separator-->
            <div class="separator my-2"></div>
            <!--end::Separator-->
            <!--begin::Menu item-->
            <div class="menu-item px-3">
              <a @click="handleToggleStatus(staffMember)" class="menu-link px-3">
                <KTIcon :icon-name="staffMember.active ? 'cross-circle' : 'check-circle'" icon-class="fs-6 me-2" />
                {{ staffMember.active ? 'Deactivate' : 'Activate' }}
              </a>
            </div>
            <!--end::Menu item-->
            <!--begin::Menu item-->
            <div class="menu-item px-3">
              <a @click="handleDelete(staffMember)" class="menu-link px-3 text-danger">
                <KTIcon icon-name="trash" icon-class="fs-6 me-2" />
                Delete Staff
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
  
  <!-- Create Staff Modal -->
  <CreateStaffModal @staffCreated="onStaffCreated" />
  <!-- Edit Staff Modal -->
  <EditStaffModal 
    v-if="editingStaff" 
    :staff="editingStaff" 
    @staffUpdated="onStaffUpdated"
    @close="editingStaff = null"
  />
  <!-- Manage Roles Modal -->
  <ManageStaffRolesModal 
    v-if="managingRolesStaff"
    :staff="managingRolesStaff"
    @rolesUpdated="onRolesUpdated"
    @close="managingRolesStaff = null"
  />
</template>

<script lang="ts">
import { defineComponent, ref, onMounted, onUnmounted } from "vue";
import ApiService from "@/core/services/ApiService";
import KTDatatable from "@/components/kt-datatable/KTDataTable.vue";
import type { Sort } from "@/components/kt-datatable/table-partials/models";
import arraySort from "array-sort";
import { MenuComponent } from "@/assets/ts/components";
import Swal from "sweetalert2";
import { useRouter } from "vue-router";
import CreateStaffModal from "@/components/modals/CreateStaffModal.vue";
import EditStaffModal from "@/components/modals/EditStaffModal.vue";
import ManageStaffRolesModal from "@/components/modals/ManageStaffRolesModal.vue";
import { useToolbar, createToolbarActions } from "@/core/helpers/toolbar";

interface Staff {
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
}

interface StaffRole {
  id: string;
  code: string;
  name: string;
}

export default defineComponent({
  name: "staff-management",
  components: {
    KTDatatable,
    CreateStaffModal,
    EditStaffModal,
    ManageStaffRolesModal,
  },
  setup() {
    const router = useRouter();
    const staff = ref<Staff[]>([]);
    const staffRoles = ref<StaffRole[]>([]);
    const loading = ref(false);
    const error = ref<string | null>(null);
    const editingStaff = ref<Staff | null>(null);
    const managingRolesStaff = ref<Staff | null>(null);
    const { setToolbarActions } = useToolbar();

    const headerConfig = ref([
      {
        columnName: "Staff",
        columnLabel: "staff",
        sortEnabled: true,
      },
      {
        columnName: "Roles",
        columnLabel: "roles",
        sortEnabled: false,
      },
      {
        columnName: "Status",
        columnLabel: "status",
        sortEnabled: true,
      },
      {
        columnName: "Contact",
        columnLabel: "contact",
        sortEnabled: false,
      },
      {
        columnName: "Actions",
        columnLabel: "actions",
      },
    ]);

    const selectedIds = ref<Array<string>>([]);
    const search = ref<string>("");
    const totalItems = ref(0);
    const currentPage = ref(1);
    const pageSize = ref(25);
    const searchTimeout = ref<NodeJS.Timeout | null>(null);

    // Methods
    const fetchStaff = async (page: number = 1, pageLimit: number = 25, searchQuery: string = '') => {
      try {
        loading.value = true;
        error.value = null;
        
        const params = new URLSearchParams();
        params.append('page', page.toString());
        params.append('page_size', pageLimit.toString());
        if (searchQuery.trim()) {
          params.append('search', searchQuery.trim());
        }
        
        const { data } = await ApiService.get(`/staff/?${params}`);
        staff.value = data.results || [];
        totalItems.value = data.count || 0;
        currentPage.value = page;
        console.log('Staff data loaded:', staff.value.length, 'items');
      } catch (err: any) {
        error.value = err.response?.data?.detail || "Failed to fetch staff";
        console.error("Error fetching staff:", err);
        staff.value = [];
        totalItems.value = 0;
      } finally {
        loading.value = false;
        setTimeout(() => {
          MenuComponent.reinitialization();
        }, 100);
      }
    };

    const fetchStaffRoles = async () => {
      try {
        const { data } = await ApiService.get("/staff-roles/");
        staffRoles.value = data.results || data;
      } catch (err: any) {
        console.error("Error fetching staff roles:", err);
      }
    };

    const openCreateStaffModal = () => {
      const modalElement = document.getElementById('kt_modal_create_staff');
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

    const getStaffName = (staffMember: Staff): string => {
      if (!staffMember.contact) return 'Unknown Staff';
      
      const { first_name, last_name, business_name } = staffMember.contact;
      
      if (business_name) return business_name;
      if (first_name || last_name) {
        return `${first_name || ''} ${last_name || ''}`.trim();
      }
      return 'Unknown Staff';
    };

    const getContactInfo = (staffMember: Staff): string => {
      if (!staffMember.contact) return 'No contact info';
      
      const email = staffMember.contact.email;
      const phone = staffMember.contact.phone;
      
      if (email && phone) return `${email} • ${phone}`;
      if (email) return email;
      if (phone) return phone;
      return 'No contact details';
    };

    const getActiveRoles = (staffMember: Staff): any[] => {
      if (!staffMember.role_memberships) return [];
      
      const today = new Date().toISOString().split('T')[0];
      
      return staffMember.role_memberships
        .filter(membership => {
          const startDate = membership.start_on;
          const endDate = membership.end_on;
          
          // If no start date or start date is in the past/today
          const startValid = !startDate || startDate <= today;
          // If no end date or end date is in the future/today
          const endValid = !endDate || endDate >= today;
          
          return startValid && endValid;
        })
        .map(membership => membership.role);
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

    const handleView = (staffMember: Staff) => {
      router.push(`/admin/staff/${staffMember.id}`);
    };

    const handleEdit = (staffMember: Staff) => {
      editingStaff.value = staffMember;
    };

    const handleManageRoles = (staffMember: Staff) => {
      managingRolesStaff.value = staffMember;
    };

    const handleToggleStatus = async (staffMember: Staff) => {
      const action = staffMember.active ? 'deactivate' : 'activate';
      const result = await Swal.fire({
        title: `${action.charAt(0).toUpperCase() + action.slice(1)} Staff`,
        text: `Are you sure you want to ${action} ${getStaffName(staffMember)}?`,
        icon: "question",
        showCancelButton: true,
        confirmButtonText: `Yes, ${action}!`,
        cancelButtonText: "Cancel"
      });

      if (result.isConfirmed) {
        try {
          await ApiService.patch(`/staff/${staffMember.id}/`, {
            active: !staffMember.active
          });
          
          Swal.fire(
            `${action.charAt(0).toUpperCase() + action.slice(1)}d!`,
            `Staff member has been ${action}d.`,
            "success"
          );
          
          fetchStaff(currentPage.value, pageSize.value, search.value);
        } catch (error) {
          Swal.fire("Error", `Failed to ${action} staff member.`, "error");
        }
      }
    };

    const handleDelete = async (staffMember: Staff) => {
      Swal.fire({
        title: "Delete Staff",
        text: `Are you sure you want to delete ${getStaffName(staffMember)}? This action cannot be undone.`,
        icon: "warning",
        showCancelButton: true,
        confirmButtonText: "Yes, delete it!",
        cancelButtonText: "Cancel",
        confirmButtonColor: "#d33"
      }).then(async (result) => {
        if (result.isConfirmed) {
          try {
            await ApiService.delete(`/staff/${staffMember.id}/`);
            
            Swal.fire({
              title: "Deleted!",
              text: "Staff member has been deleted successfully.",
              icon: "success"
            }).then(() => {
              fetchStaff(currentPage.value, pageSize.value, search.value);
            });
          } catch (error) {
            Swal.fire({
              title: "Error",
              text: "Failed to delete the staff member. Please try again.",
              icon: "error"
            });
          }
        }
      });
    };

    const deleteFewStaff = async () => {
      if (selectedIds.value.length === 0) return;
      
      const result = await Swal.fire({
        title: "Delete Staff Members",
        text: `Are you sure you want to delete ${selectedIds.value.length} staff member(s)? This action cannot be undone.`,
        icon: "warning",
        showCancelButton: true,
        confirmButtonText: "Yes, delete them!",
        cancelButtonText: "Cancel",
        confirmButtonColor: "#d33"
      });
      
      if (result.isConfirmed) {
        try {
          loading.value = true;
          
          for (const staffId of selectedIds.value) {
            await ApiService.delete(`/staff/${staffId}/`);
          }
          
          selectedIds.value.length = 0;
          
          Swal.fire({
            title: "Deleted!",
            text: "Selected staff members have been deleted successfully.",
            icon: "success"
          }).then(() => {
            fetchStaff(currentPage.value, pageSize.value, search.value);
          });
        } catch (error) {
          console.error("Error deleting staff:", error);
          Swal.fire({
            title: "Error",
            text: "Failed to delete some staff members. Please try again.",
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
        arraySort(staff.value, sort.label, { reverse });
      }
    };

    const onItemSelect = (selectedItems: Array<string>) => {
      selectedIds.value = selectedItems;
    };

    const searchItems = () => {
      if (searchTimeout.value) {
        clearTimeout(searchTimeout.value);
      }
      
      searchTimeout.value = setTimeout(async () => {
        currentPage.value = 1;
        await fetchStaff(1, pageSize.value, search.value);
        MenuComponent.reinitialization();
      }, 500);
    };

    const onItemsPerPageChange = async (newPageSize: number) => {
      pageSize.value = newPageSize;
      currentPage.value = 1;
      await fetchStaff(1, newPageSize, search.value);
      setTimeout(() => {
        MenuComponent.reinitialization();
      }, 0);
    };

    const onPageChange = async (page: number) => {
      await fetchStaff(page, pageSize.value, search.value);
      MenuComponent.reinitialization();
    };

    const navigateToStaff = (staffId: string) => {
      router.push(`/admin/staff/${staffId}`);
    };

    const onStaffCreated = (newStaff: Staff) => {
      console.log('New staff created:', newStaff);
      currentPage.value = 1;
      fetchStaff(1, pageSize.value, search.value);
    };

    const onStaffUpdated = (updatedStaff: Staff) => {
      console.log('Staff updated:', updatedStaff);
      editingStaff.value = null;
      fetchStaff(currentPage.value, pageSize.value, search.value);
    };

    const onRolesUpdated = () => {
      console.log('Staff roles updated');
      managingRolesStaff.value = null;
      fetchStaff(currentPage.value, pageSize.value, search.value);
    };

    onMounted(async () => {
      await fetchStaff(1, pageSize.value, '');
      fetchStaffRoles();
      setTimeout(() => {
        MenuComponent.reinitialization();
      }, 200);

      // Setup toolbar actions
      setToolbarActions([
        createToolbarActions.primary('add-staff', 'Add Staff', openCreateStaffModal, 'plus')
      ]);
    });

    onUnmounted(() => {
      if (searchTimeout.value) {
        clearTimeout(searchTimeout.value);
      }
    });

    return {
      search,
      searchItems,
      staff,
      staffRoles,
      headerConfig,
      loading,
      error,
      sort,
      onItemSelect,
      selectedIds,
      deleteFewStaff,
      onItemsPerPageChange,
      onPageChange,
      totalItems,
      currentPage,
      pageSize,
      openCreateStaffModal,
      handleView,
      handleEdit,
      handleManageRoles,
      handleToggleStatus,
      handleDelete,
      getStaffName,
      getContactInfo,
      getActiveRoles,
      getRoleColor,
      navigateToStaff,
      onStaffCreated,
      onStaffUpdated,
      onRolesUpdated,
      editingStaff,
      managingRolesStaff,
    };
  },
});
</script>