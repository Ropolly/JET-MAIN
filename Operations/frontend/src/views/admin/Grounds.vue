<template>
  <div class="card">
    <div class="card-header border-0 pt-6">
      <div class="card-title">
        <div class="d-flex align-items-center position-relative my-1">
          <KTIcon icon-name="magnifier" icon-class="fs-1 position-absolute ms-6" />
          <input v-model="search" @input="searchItems()" type="text" class="form-control form-control-solid w-250px ps-14" placeholder="Search Ground Transportation" />
        </div>
      </div>
      <div class="card-toolbar" v-if="selectedIds.length > 0">
        <div class="d-flex justify-content-end align-items-center">
          <div class="fw-bold me-5"><span class="me-2">{{ selectedIds.length }}</span>Selected</div>
          <button type="button" class="btn btn-danger" @click="deleteFewGrounds()">Delete Selected</button>
        </div>
      </div>
    </div>
    <div class="card-body pt-0">
      <KTDatatable @on-sort="sort" @on-items-select="onItemSelect" @on-items-per-page-change="onItemsPerPageChange" :data="grounds" :header="headerConfig" :checkbox-enabled="true" :loading="loading">
        <template v-slot:ground="{ row: ground }">
          <div class="d-flex align-items-center">
            <div class="symbol symbol-circle symbol-50px overflow-hidden me-3">
              <div class="symbol-label bg-light-success"><i class="ki-duotone ki-car fs-2x text-success"><span class="path1"></span><span class="path2"></span><span class="path3"></span></i></div>
            </div>
            <div class="d-flex flex-column">
              <a href="#" @click="handleView(ground)" class="text-gray-800 text-hover-primary mb-1 fs-6 fw-bold">{{ ground.name || 'Unnamed Ground Service' }}</a>
              <span class="text-muted fs-7">{{ ground.service_type || 'Unknown type' }}</span>
            </div>
          </div>
        </template>
        <template v-slot:contact="{ row: ground }"><span class="text-dark fw-semibold">{{ ground.contact_info || 'No contact' }}</span></template>
        <template v-slot:coverage="{ row: ground }"><span class="text-dark fw-semibold">{{ ground.coverage_area || 'Not specified' }}</span></template>
        <template v-slot:actions="{ row: ground }">
          <a href="#" class="btn btn-sm btn-light btn-active-light-primary" data-kt-menu-trigger="click" data-kt-menu-placement="bottom-end">Actions <KTIcon icon-name="down" icon-class="fs-5 m-0" /></a>
          <div class="menu menu-sub menu-sub-dropdown menu-column menu-rounded menu-gray-600 menu-state-bg-light-primary fw-semibold fs-7 w-200px py-4" data-kt-menu="true">
            <div class="menu-item px-3"><a @click="handleView(ground)" class="menu-link px-3">View Details</a></div>
            <div class="menu-item px-3"><a @click="handleEdit(ground)" class="menu-link px-3">Edit Ground Service</a></div>
            <div class="menu-item px-3"><a @click="handleViewTrips(ground)" class="menu-link px-3">View Trips</a></div>
            <div class="separator mt-3 opacity-75"></div>
            <div class="menu-item px-3"><a @click="handleDelete(ground)" class="menu-link px-3 text-danger">Delete</a></div>
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
  name: "grounds-management", components: { KTDatatable },
  setup() {
    const router = useRouter(); const toolbarStore = useToolbarStore(); const grounds = ref([]); const loading = ref(false); const selectedIds = ref([]); const search = ref(""); const initData = ref([]);
    const headerConfig = ref([{ columnName: "Ground Service", columnLabel: "ground", sortEnabled: true }, { columnName: "Contact", columnLabel: "contact", sortEnabled: false }, { columnName: "Coverage Area", columnLabel: "coverage", sortEnabled: false }, { columnName: "Actions", columnLabel: "actions" }]);
    const fetchGrounds = async () => { try { loading.value = true; const { data } = await ApiService.get("/grounds/"); grounds.value = data.results || data; initData.value.splice(0, grounds.value.length, ...grounds.value); } catch (error) { console.error("Error fetching grounds:", error); } finally { loading.value = false; } };
    const handleCreate = () => Swal.fire({ title: "Add Ground Service", text: "Ground service creation form would open here", icon: "info" });
    const handleEdit = (ground) => Swal.fire({ title: "Edit Ground Service", text: `Edit ${ground.name}`, icon: "info" });
    const handleView = (ground) => Swal.fire({ title: "Ground Service Details", html: `<div class="text-start"><p><strong>Name:</strong> ${ground.name}</p><p><strong>Type:</strong> ${ground.service_type}</p><p><strong>Contact:</strong> ${ground.contact_info}</p><p><strong>Coverage:</strong> ${ground.coverage_area}</p></div>`, icon: "info" });
    const handleViewTrips = (ground) => router.push(`/admin/trips?ground=${ground.id}`);
    const handleDelete = async (ground) => { const result = await Swal.fire({ title: "Delete Ground Service", text: `Delete ${ground.name}?`, icon: "warning", showCancelButton: true, confirmButtonText: "Yes, delete!" }); if (result.isConfirmed) { try { await ApiService.delete(`/grounds/${ground.id}/`); await fetchGrounds(); Swal.fire("Deleted!", "Ground service deleted.", "success"); } catch (error) { Swal.fire("Error!", "Failed to delete ground service.", "error"); } } };
    const deleteFewGrounds = () => { selectedIds.value.forEach(id => grounds.value = grounds.value.filter(g => g.id !== id)); selectedIds.value = []; };
    const sort = (sort) => { if (sort.label) arraySort(grounds.value, sort.label, { reverse: sort.order === "asc" }); }; const onItemSelect = (items) => selectedIds.value = items;
    const searchItems = () => { grounds.value.splice(0, grounds.value.length, ...initData.value); if (search.value) { const results = initData.value.filter(item => Object.values(item).some(val => val?.toString().toLowerCase().includes(search.value.toLowerCase()))); grounds.value.splice(0, grounds.value.length, ...results); } MenuComponent.reinitialization(); };
    const onItemsPerPageChange = () => setTimeout(() => MenuComponent.reinitialization(), 0);
    onMounted(async () => { await fetchGrounds(); await nextTick(); setTimeout(() => MenuComponent.reinitialization(), 100); toolbarStore.setActions([{ id: 'add-ground', label: 'Add Ground Service', icon: 'plus', variant: 'primary', handler: handleCreate }]); });
    onUnmounted(() => toolbarStore.clearActions());
    return { search, searchItems, grounds, headerConfig, loading, sort, onItemSelect, selectedIds, deleteFewGrounds, onItemsPerPageChange, handleCreate, handleEdit, handleView, handleViewTrips, handleDelete };
  },
});
</script>