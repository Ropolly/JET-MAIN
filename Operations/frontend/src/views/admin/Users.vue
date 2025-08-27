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
            placeholder="Search Users"
          />
        </div>
        <!--end::Search-->
      </div>
      <!--begin::Card title-->

      <!--begin::Card toolbar-->
      <div class="card-toolbar" v-if="selectedIds.length > 0">
        <!--begin::Group actions-->
        <div class="d-flex justify-content-end align-items-center">
          <div class="fw-bold me-5">
            <span class="me-2">{{ selectedIds.length }}</span>Selected
          </div>
          <button
            type="button"
            class="btn btn-danger"
            @click="deleteFewUsers()"
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
        :data="users"
        :header="headerConfig"
        :checkbox-enabled="true"
        :loading="loading"
      >
        <template v-slot:user="{ row: user }">
          <div class="d-flex align-items-center">
            <div class="symbol symbol-circle symbol-50px overflow-hidden me-3">
              <div class="symbol-label bg-light-primary">
                <i class="ki-duotone ki-profile-circle fs-2x text-primary">
                  <span class="path1"></span>
                  <span class="path2"></span>
                  <span class="path3"></span>
                </i>
              </div>
            </div>
            <div class="d-flex flex-column">
              <a href="#" @click="handleView(user)" class="text-gray-800 text-hover-primary mb-1 fs-6 fw-bold">
                {{ getUserName(user) }}
              </a>
              <span class="text-muted fs-7">{{ user.username }}</span>
            </div>
          </div>
        </template>

        <template v-slot:email="{ row: user }">
          <span class="text-dark fw-semibold">
            {{ user.email || 'No email' }}
          </span>
        </template>

        <template v-slot:role="{ row: user }">
          <div class="d-flex flex-column">
            <span class="text-dark fw-semibold fs-6">
              {{ getUserRole(user) }}
            </span>
            <span class="text-muted fs-7">{{ getUserPermissions(user) }}</span>
          </div>
        </template>

        <template v-slot:status="{ row: user }">
          <span :class="`badge badge-light-${getStatusColor(user)} fs-7 fw-bold`">
            {{ getUserStatus(user) }}
          </span>
        </template>

        <template v-slot:last_login="{ row: user }">
          <span class="text-dark fw-semibold">
            {{ formatDate(user.last_login) }}
          </span>
        </template>

        <template v-slot:actions="{ row: user }">
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
            class="menu menu-sub menu-sub-dropdown menu-column menu-rounded menu-gray-600 menu-state-bg-light-primary fw-semibold fs-7 w-200px py-4"
            data-kt-menu="true"
          >
            <!--begin::Menu item-->
            <div class="menu-item px-3">
              <a @click="handleView(user)" class="menu-link px-3"
                >View Details</a
              >
            </div>
            <!--end::Menu item-->
            <!--begin::Menu item-->
            <div class="menu-item px-3">
              <a @click="handleEdit(user)" class="menu-link px-3"
                >Edit User</a
              >
            </div>
            <!--end::Menu item-->
            <!--begin::Menu item-->
            <div class="menu-item px-3">
              <a @click="handleManageRoles(user)" class="menu-link px-3"
                >Manage Roles</a
              >
            </div>
            <!--end::Menu item-->
            <!--begin::Menu item-->
            <div class="menu-item px-3">
              <a @click="handleResetPassword(user)" class="menu-link px-3"
                >Reset Password</a
              >
            </div>
            <!--end::Menu item-->
            <!--begin::Menu item-->
            <div class="menu-item px-3">
              <a @click="handleToggleActive(user)" class="menu-link px-3">
                {{ user.is_active ? 'Deactivate' : 'Activate' }}
              </a>
            </div>
            <!--end::Menu item-->
            <div class="separator mt-3 opacity-75"></div>
            <!--begin::Menu item-->
            <div class="menu-item px-3">
              <a @click="handleDelete(user)" class="menu-link px-3 text-danger"
                >Delete</a
              >
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
</template>

<script lang="ts">
import { defineComponent, ref, onMounted, onUnmounted, nextTick } from "vue";
import { useRouter } from "vue-router";
import ApiService from "@/core/services/ApiService";
import KTDatatable from "@/components/kt-datatable/KTDataTable.vue";
import type { Sort } from "@/components/kt-datatable/table-partials/models";
import arraySort from "array-sort";
import { MenuComponent } from "@/assets/ts/components";
import Swal from "sweetalert2";
import { useToolbarStore } from "@/stores/toolbar";

interface User {
  id: number;
  username: string;
  email: string;
  first_name: string;
  last_name: string;
  is_active: boolean;
  is_staff: boolean;
  is_superuser: boolean;
  date_joined: string;
  last_login: string | null;
}

export default defineComponent({
  name: "users-management",
  components: {
    KTDatatable,
  },
  setup() {
    const router = useRouter();
    const toolbarStore = useToolbarStore();
    const users = ref<User[]>([]);
    const loading = ref(false);
    const error = ref<string | null>(null);

    const headerConfig = ref([
      {
        columnName: "User",
        columnLabel: "user",
        sortEnabled: true,
      },
      {
        columnName: "Email",
        columnLabel: "email",
        sortEnabled: true,
      },
      {
        columnName: "Role",
        columnLabel: "role",
        sortEnabled: false,
      },
      {
        columnName: "Status",
        columnLabel: "status",
        sortEnabled: true,
      },
      {
        columnName: "Last Login",
        columnLabel: "last_login",
        sortEnabled: true,
      },
      {
        columnName: "Actions",
        columnLabel: "actions",
      },
    ]);

    const initData = ref<Array<User>>([]);
    const selectedIds = ref<Array<number>>([]);
    const search = ref<string>("");

    // Methods
    const fetchUsers = async () => {
      try {
        loading.value = true;
        error.value = null;
        const { data } = await ApiService.get("/users/");
        users.value = data.results || data;
        initData.value.splice(0, users.value.length, ...users.value);
      } catch (err: any) {
        error.value = err.response?.data?.detail || "Failed to fetch users";
        console.error("Error fetching users:", err);
      } finally {
        loading.value = false;
      }
    };

    const handleCreate = () => {
      Swal.fire({
        title: "Add User",
        text: "User creation form would open here",
        icon: "info",
        confirmButtonText: "OK"
      });
    };

    const handleEdit = (user: User) => {
      Swal.fire({
        title: "Edit User",
        text: `Edit form for ${getUserName(user)} would open here`,
        icon: "info",
        confirmButtonText: "OK"
      });
    };

    const handleView = (user: User) => {
      Swal.fire({
        title: "User Details",
        html: `
          <div class="text-start">
            <p><strong>Name:</strong> ${getUserName(user)}</p>
            <p><strong>Username:</strong> ${user.username}</p>
            <p><strong>Email:</strong> ${user.email || 'Not set'}</p>
            <p><strong>Role:</strong> ${getUserRole(user)}</p>
            <p><strong>Status:</strong> ${getUserStatus(user)}</p>
            <p><strong>Joined:</strong> ${formatDate(user.date_joined)}</p>
            <p><strong>Last Login:</strong> ${formatDate(user.last_login)}</p>
          </div>
        `,
        icon: "info",
        confirmButtonText: "OK"
      });
    };

    const handleManageRoles = (user: User) => {
      router.push(`/admin/users/${user.id}/roles`);
    };

    const handleResetPassword = (user: User) => {
      Swal.fire({
        title: "Reset Password",
        text: `Send password reset email to ${getUserName(user)}?`,
        icon: "question",
        showCancelButton: true,
        confirmButtonText: "Yes, send reset email",
        cancelButtonText: "Cancel"
      }).then((result) => {
        if (result.isConfirmed) {
          Swal.fire("Email Sent!", "Password reset email has been sent.", "success");
        }
      });
    };

    const handleToggleActive = async (user: User) => {
      const action = user.is_active ? 'deactivate' : 'activate';
      const result = await Swal.fire({
        title: `${action.charAt(0).toUpperCase() + action.slice(1)} User`,
        text: `Are you sure you want to ${action} ${getUserName(user)}?`,
        icon: "question",
        showCancelButton: true,
        confirmButtonText: `Yes, ${action}!`,
        cancelButtonText: "Cancel"
      });
      
      if (result.isConfirmed) {
        try {
          await ApiService.patch(`/users/${user.id}/`, { is_active: !user.is_active });
          await fetchUsers(); // Refresh the list
          Swal.fire("Updated!", `User has been ${action}d.`, "success");
        } catch (error: any) {
          console.error('Error updating user:', error);
          Swal.fire("Error!", "Failed to update user. Please try again.", "error");
        }
      }
    };

    const handleDelete = async (user: User) => {
      const result = await Swal.fire({
        title: "Delete User",
        text: `Are you sure you want to delete ${getUserName(user)}? This action cannot be undone.`,
        icon: "warning",
        showCancelButton: true,
        confirmButtonText: "Yes, delete it!",
        cancelButtonText: "Cancel"
      });
      
      if (result.isConfirmed) {
        try {
          await ApiService.delete(`/users/${user.id}/`);
          await fetchUsers(); // Refresh the list
          Swal.fire("Deleted!", "User has been deleted.", "success");
        } catch (error: any) {
          console.error('Error deleting user:', error);
          Swal.fire("Error!", "Failed to delete user. Please try again.", "error");
        }
      }
    };

    const getUserName = (user: User): string => {
      const fullName = `${user.first_name || ''} ${user.last_name || ''}`.trim();
      return fullName || user.username;
    };

    const getUserRole = (user: User): string => {
      if (user.is_superuser) return 'Super Admin';
      if (user.is_staff) return 'Staff';
      return 'User';
    };

    const getUserPermissions = (user: User): string => {
      const permissions = [];
      if (user.is_superuser) permissions.push('All permissions');
      else if (user.is_staff) permissions.push('Staff access');
      else permissions.push('Basic access');
      return permissions.join(', ');
    };

    const getUserStatus = (user: User): string => {
      return user.is_active ? 'Active' : 'Inactive';
    };

    const getStatusColor = (user: User): string => {
      return user.is_active ? 'success' : 'danger';
    };

    const formatDate = (dateString: string | null): string => {
      if (!dateString) return 'Never';
      return new Date(dateString).toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
      });
    };

    const deleteFewUsers = () => {
      selectedIds.value.forEach((item) => {
        deleteUser(item);
      });
      selectedIds.value.length = 0;
    };

    const deleteUser = (id: number) => {
      for (let i = 0; i < users.value.length; i++) {
        if (users.value[i].id === id) {
          users.value.splice(i, 1);
        }
      }
    };

    const sort = (sort: Sort) => {
      const reverse: boolean = sort.order === "asc";
      if (sort.label) {
        arraySort(users.value, sort.label, { reverse });
      }
    };

    const onItemSelect = (selectedItems: Array<number>) => {
      selectedIds.value = selectedItems;
    };

    const searchItems = () => {
      users.value.splice(0, users.value.length, ...initData.value);
      if (search.value !== "") {
        let results: Array<User> = [];
        for (let j = 0; j < initData.value.length; j++) {
          if (searchingFunc(initData.value[j], search.value)) {
            results.push(initData.value[j]);
          }
        }
        users.value.splice(0, users.value.length, ...results);
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

    onMounted(async () => {
      await fetchUsers();
      // Ensure menus are properly initialized
      await nextTick();
      setTimeout(() => {
        MenuComponent.reinitialization();
      }, 100);
      
      // Set toolbar actions
      toolbarStore.setActions([
        {
          id: 'add-user',
          label: 'Add User',
          icon: 'plus',
          variant: 'primary',
          handler: handleCreate
        }
      ]);
    });
    
    onUnmounted(() => {
      // Clear toolbar actions when component is destroyed
      toolbarStore.clearActions();
    });

    return {
      search,
      searchItems,
      users,
      headerConfig,
      loading,
      error,
      sort,
      onItemSelect,
      selectedIds,
      deleteFewUsers,
      deleteUser,
      onItemsPerPageChange,
      handleCreate,
      handleEdit,
      handleView,
      handleManageRoles,
      handleResetPassword,
      handleToggleActive,
      handleDelete,
      getUserName,
      getUserRole,
      getUserPermissions,
      getUserStatus,
      getStatusColor,
      formatDate,
    };
  },
});
</script>