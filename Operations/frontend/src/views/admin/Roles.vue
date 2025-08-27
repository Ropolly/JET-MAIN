<template>
  <div class="card">
    <div class="card-header border-0 pt-6">
      <div class="card-title">
        <div class="d-flex align-items-center position-relative my-1">
          <KTIcon icon-name="magnifier" icon-class="fs-1 position-absolute ms-6" />
          <input v-model="search" @input="searchItems()" type="text" class="form-control form-control-solid w-250px ps-14" placeholder="Search Roles" />
        </div>
      </div>
      <div class="card-toolbar" v-if="selectedIds.length > 0">
        <div class="d-flex justify-content-end align-items-center">
          <div class="fw-bold me-5"><span class="me-2">{{ selectedIds.length }}</span>Selected</div>
          <button type="button" class="btn btn-danger" @click="deleteFewRoles()">Delete Selected</button>
        </div>
      </div>
    </div>
    <div class="card-body pt-0">
      <KTDatatable @on-sort="sort" @on-items-select="onItemSelect" @on-items-per-page-change="onItemsPerPageChange" :data="roles" :header="headerConfig" :checkbox-enabled="true" :loading="loading">
        <template v-slot:role="{ row: role }">
          <div class="d-flex align-items-center">
            <div class="symbol symbol-circle symbol-50px overflow-hidden me-3">
              <div class="symbol-label bg-light-danger"><i class="ki-duotone ki-security-user fs-2x text-danger"><span class="path1"></span><span class="path2"></span></i></div>
            </div>
            <div class="d-flex flex-column">
              <a href="#" @click="handleView(role)" class="text-gray-800 text-hover-primary mb-1 fs-6 fw-bold">{{ role.name || 'Unnamed Role' }}</a>
              <span class="text-muted fs-7">{{ role.description || 'No description' }}</span>
            </div>
          </div>
        </template>
        <template v-slot:permissions="{ row: role }"><span class="text-dark fw-semibold">{{ role.permissions_count || 0 }} permissions</span></template>
        <template v-slot:users="{ row: role }"><span class="text-dark fw-semibold">{{ role.users_count || 0 }} users</span></template>
        <template v-slot:status="{ row: role }">
          <span :class="`badge badge-light-${getStatusColor(role.is_active)} fs-7 fw-bold`">
            {{ role.is_active ? 'Active' : 'Inactive' }}
          </span>
        </template>
        <template v-slot:actions="{ row: role }">
          <a href="#" class="btn btn-sm btn-light btn-active-light-primary" data-kt-menu-trigger="click" data-kt-menu-placement="bottom-end">Actions <KTIcon icon-name="down" icon-class="fs-5 m-0" /></a>
          <div class="menu menu-sub menu-sub-dropdown menu-column menu-rounded menu-gray-600 menu-state-bg-light-primary fw-semibold fs-7 w-200px py-4" data-kt-menu="true">
            <div class="menu-item px-3"><a @click="handleView(role)" class="menu-link px-3">View Details</a></div>
            <div class="menu-item px-3"><a @click="handleEdit(role)" class="menu-link px-3">Edit Role</a></div>
            <div class="menu-item px-3"><a @click="handleManagePermissions(role)" class="menu-link px-3">Manage Permissions</a></div>
            <div class="menu-item px-3"><a @click="handleViewUsers(role)" class="menu-link px-3">View Users</a></div>
            <div class="separator mt-3 opacity-75"></div>
            <div class="menu-item px-3"><a @click="handleDelete(role)" class="menu-link px-3 text-danger">Delete</a></div>
          </div>
        </template>
      </KTDatatable>
    </div>
  </div>
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

export default defineComponent({
  name: "roles-management", components: { KTDatatable },
  setup() {
    const router = useRouter(); const toolbarStore = useToolbarStore(); const roles = ref([]); const loading = ref(false); const selectedIds = ref([]); const search = ref(""); const initData = ref([]);
    const headerConfig = ref([{ columnName: "Role", columnLabel: "role", sortEnabled: true }, { columnName: "Permissions", columnLabel: "permissions", sortEnabled: false }, { columnName: "Users", columnLabel: "users", sortEnabled: false }, { columnName: "Status", columnLabel: "status", sortEnabled: true }, { columnName: "Actions", columnLabel: "actions" }]);
    const fetchRoles = async () => { try { loading.value = true; const { data } = await ApiService.get("/roles/"); roles.value = data.results || data; initData.value.splice(0, roles.value.length, ...roles.value); } catch (error) { console.error("Error fetching roles:", error); } finally { loading.value = false; } };
    const handleCreate = () => Swal.fire({ title: "Add Role", text: "Role creation form would open here", icon: "info" });
    const handleEdit = (role) => Swal.fire({ title: "Edit Role", text: `Edit ${role.name}`, icon: "info" });
    const handleView = (role) => Swal.fire({ title: "Role Details", html: `<div class="text-start"><p><strong>Name:</strong> ${role.name}</p><p><strong>Description:</strong> ${role.description}</p><p><strong>Permissions:</strong> ${role.permissions_count}</p><p><strong>Users:</strong> ${role.users_count}</p></div>`, icon: "info" });
    const handleManagePermissions = (role) => router.push(`/admin/roles/${role.id}/permissions`);
    const handleViewUsers = (role) => router.push(`/admin/users?role=${role.id}`);
    const handleDelete = async (role) => { const result = await Swal.fire({ title: "Delete Role", text: `Delete ${role.name}?`, icon: "warning", showCancelButton: true, confirmButtonText: "Yes, delete!" }); if (result.isConfirmed) { try { await ApiService.delete(`/roles/${role.id}/`); await fetchRoles(); Swal.fire("Deleted!", "Role deleted.", "success"); } catch (error) { Swal.fire("Error!", "Failed to delete role.", "error"); } } };
    const getStatusColor = (isActive) => isActive ? 'success' : 'danger';
    const deleteFewRoles = () => { selectedIds.value.forEach(id => roles.value = roles.value.filter(r => r.id !== id)); selectedIds.value = []; };
    const sort = (sort) => { if (sort.label) arraySort(roles.value, sort.label, { reverse: sort.order === "asc" }); }; const onItemSelect = (items) => selectedIds.value = items;
    const searchItems = () => { roles.value.splice(0, roles.value.length, ...initData.value); if (search.value) { const results = initData.value.filter(item => Object.values(item).some(val => val?.toString().toLowerCase().includes(search.value.toLowerCase()))); roles.value.splice(0, roles.value.length, ...results); } MenuComponent.reinitialization(); };
    const onItemsPerPageChange = () => setTimeout(() => MenuComponent.reinitialization(), 0);
    onMounted(async () => { await fetchRoles(); await nextTick(); setTimeout(() => MenuComponent.reinitialization(), 100); toolbarStore.setActions([{ id: 'add-role', label: 'Add Role', icon: 'plus', variant: 'primary', handler: handleCreate }]); });
    onUnmounted(() => toolbarStore.clearActions());
    return { search, searchItems, roles, headerConfig, loading, sort, onItemSelect, selectedIds, deleteFewRoles, onItemsPerPageChange, handleCreate, handleEdit, handleView, handleManagePermissions, handleViewUsers, handleDelete, getStatusColor };
  },
});
</script>