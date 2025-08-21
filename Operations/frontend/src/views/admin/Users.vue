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
      <div class="card-toolbar">
        <!--begin::Toolbar-->
        <div
          v-if="selectedIds.length === 0"
          class="d-flex justify-content-end"
        >
          <!--begin::Export-->
          <button
            type="button"
            class="btn btn-light-primary me-3"
            @click="exportUsers"
          >
            <KTIcon icon-name="exit-up" icon-class="fs-2" />
            Export
          </button>
          <!--end::Export-->

          <!--begin::Add user-->
          <button
            type="button"
            class="btn btn-primary"
            @click="handleCreate"
          >
            <KTIcon icon-name="plus" icon-class="fs-2" />
            Add User
          </button>
          <!--end::Add user-->
        </div>
        <!--end::Toolbar-->

        <!--begin::Group actions-->
        <div v-else class="d-flex justify-content-end align-items-center">
          <div class="fw-bold me-5">
            <span class="me-2">{{ selectedIds.length }}</span
            >Selected
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
                <span class="text-primary fw-bold fs-6">
                  {{ getUserInitials(user) }}
                </span>
              </div>
            </div>
            <div class="d-flex flex-column">
              <a href="#" class="text-gray-800 text-hover-primary mb-1 fs-6 fw-bold">
                {{ user.first_name }} {{ user.last_name }}
              </a>
              <span class="text-muted fs-7">{{ user.user?.username || user.email }}</span>
            </div>
          </div>
        </template>

        <template v-slot:email="{ row: user }">
          <span class="text-dark fw-semibold">{{ user.email }}</span>
        </template>

        <template v-slot:roles="{ row: user }">
          <div class="d-flex flex-wrap">
            <span v-for="role in user.roles" :key="role.id" class="badge badge-light-info me-1 mb-1">
              {{ role.name }}
            </span>
            <span v-if="!user.roles || user.roles.length === 0" class="text-muted">No roles</span>
          </div>
        </template>

        <template v-slot:department="{ row: user }">
          <span v-if="user.departments && user.departments.length > 0" class="badge badge-light-secondary">
            {{ user.departments[0].name }}
          </span>
          <span v-else class="text-muted">No department</span>
        </template>

        <template v-slot:status="{ row: user }">
          <span :class="`badge badge-light-${user.status === 'active' || user.user?.is_active ? 'success' : 'danger'} fs-7 fw-bold`">
            {{ user.status === 'active' || user.user?.is_active ? 'Active' : 'Inactive' }}
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
            class="menu menu-sub menu-sub-dropdown menu-column menu-rounded menu-gray-600 menu-state-bg-light-primary fw-semibold fs-7 w-125px py-4"
            data-kt-menu="true"
          >
            <!--begin::Menu item-->
            <div class="menu-item px-3">
              <a @click="handleView(user)" class="menu-link px-3"
                >View</a
              >
            </div>
            <!--end::Menu item-->
            <!--begin::Menu item-->
            <div class="menu-item px-3">
              <a @click="handleEdit(user)" class="menu-link px-3"
                >Edit</a
              >
            </div>
            <!--end::Menu item-->
            <!--begin::Menu item-->
            <div class="menu-item px-3">
              <a @click="handleDelete(user)" class="menu-link px-3"
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

  <!-- Create/Edit User Modal -->
  <UserFormModal
    :show="showModal"
    :user="selectedUser"
    :is-edit="isEdit"
    @close="handleModalClose"
    @save="handleSave"
  />

  <!-- Delete Confirmation Modal -->
  <DeleteConfirmationModal
    :show="showDeleteModal"
    :item-name="selectedUser ? `${selectedUser.first_name} ${selectedUser.last_name}` : ''"
    item-type="user"
    @close="showDeleteModal = false"
    @confirm="confirmDelete"
  />
</template>

<script lang="ts">
import { defineComponent, ref, onMounted } from "vue";
import { getAssetPath } from "@/core/helpers/assets";
import ApiService from "@/core/services/ApiService";
import KTDatatable from "@/components/kt-datatable/KTDataTable.vue";
import UserFormModal from "@/components/admin/modals/UserFormModal.vue";
import DeleteConfirmationModal from "@/components/admin/modals/DeleteConfirmationModal.vue";
import type { Sort } from "@/components/kt-datatable/table-partials/models";
import arraySort from "array-sort";
import { MenuComponent } from "@/assets/ts/components";
import Swal from "sweetalert2";

interface User {
  id: string;
  user?: {
    id: number;
    username: string;
    email: string;
    is_active: boolean;
  };
  first_name: string;
  last_name: string;
  email: string;
  phone: string;
  roles: Array<{ id: string; name: string }>;
  departments: Array<{ id: string; name: string }>;
  status: string;
  created_on: string;
}

export default defineComponent({
  name: "users-management",
  components: {
    KTDatatable,
    UserFormModal,
    DeleteConfirmationModal,
  },
  setup() {
    const users = ref<User[]>([]);
    const loading = ref(false);
    const error = ref<string | null>(null);
    const showModal = ref(false);
    const showDeleteModal = ref(false);
    const selectedUser = ref<User | null>(null);
    const isEdit = ref(false);

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
        columnName: "Roles",
        columnLabel: "roles",
        sortEnabled: false,
      },
      {
        columnName: "Department",
        columnLabel: "department",
        sortEnabled: false,
      },
      {
        columnName: "Status",
        columnLabel: "status",
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
      selectedUser.value = null;
      isEdit.value = false;
      showModal.value = true;
    };

    const handleEdit = (user: User) => {
      selectedUser.value = user;
      isEdit.value = true;
      showModal.value = true;
    };

    const handleView = (user: User) => {
      Swal.fire({
        title: "User Details",
        html: `
          <div class="text-start">
            <p><strong>Name:</strong> ${user.first_name} ${user.last_name}</p>
            <p><strong>Email:</strong> ${user.email}</p>
            <p><strong>Phone:</strong> ${user.phone || 'Not set'}</p>
            <p><strong>Status:</strong> ${user.status || (user.user?.is_active ? 'Active' : 'Inactive')}</p>
            <p><strong>Roles:</strong> ${user.roles?.map(r => r.name).join(', ') || 'None'}</p>
          </div>
        `,
        icon: "info",
        confirmButtonText: "OK"
      });
    };

    const handleDelete = (user: User) => {
      selectedUser.value = user;
      showDeleteModal.value = true;
    };

    const handleModalClose = () => {
      showModal.value = false;
      selectedUser.value = null;
    };

    const handleSave = async (userData: any) => {
      try {
        if (isEdit.value && selectedUser.value) {
          await ApiService.put(`/users/${selectedUser.value.id}/`, userData);
          Swal.fire({
            title: "Success!",
            text: "User updated successfully",
            icon: "success",
            confirmButtonText: "OK"
          });
        } else {
          await ApiService.post("/users/", userData);
          Swal.fire({
            title: "Success!",
            text: "User created successfully",
            icon: "success",
            confirmButtonText: "OK"
          });
        }
        
        showModal.value = false;
        await fetchUsers();
      } catch (err: any) {
        Swal.fire({
          title: "Error!",
          text: err.response?.data?.detail || "Failed to save user",
          icon: "error",
          confirmButtonText: "OK"
        });
      }
    };

    const confirmDelete = async () => {
      if (!selectedUser.value) return;
      
      try {
        await ApiService.delete(`/users/${selectedUser.value.id}/`);
        showDeleteModal.value = false;
        
        Swal.fire({
          title: "Deleted!",
          text: "User has been deleted successfully",
          icon: "success",
          confirmButtonText: "OK"
        });
        
        await fetchUsers();
      } catch (err: any) {
        Swal.fire({
          title: "Error!",
          text: err.response?.data?.detail || "Failed to delete user",
          icon: "error",
          confirmButtonText: "OK"
        });
      }
    };

    const getUserInitials = (user: User): string => {
      const first = user.first_name?.charAt(0) || '';
      const last = user.last_name?.charAt(0) || '';
      return (first + last).toUpperCase() || user.email?.charAt(0).toUpperCase() || 'U';
    };

    const deleteFewUsers = () => {
      selectedIds.value.forEach((item) => {
        deleteUser(item);
      });
      selectedIds.value.length = 0;
    };

    const deleteUser = (id: number) => {
      for (let i = 0; i < users.value.length; i++) {
        if (users.value[i].id === id.toString()) {
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

    const exportUsers = () => {
      Swal.fire({
        title: "Export Users",
        text: "Export functionality would be implemented here",
        icon: "info",
        confirmButtonText: "OK"
      });
    };

    onMounted(() => {
      fetchUsers();
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
      exportUsers,
      showModal,
      showDeleteModal,
      selectedUser,
      isEdit,
      handleCreate,
      handleEdit,
      handleView,
      handleDelete,
      handleModalClose,
      handleSave,
      confirmDelete,
      getUserInitials,
    };
  },
});
</script>