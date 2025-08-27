<template>
  <div class="card">
    <div class="card-header border-0 pt-6">
      <div class="card-title">
        <div class="d-flex align-items-center position-relative my-1">
          <KTIcon icon-name="magnifier" icon-class="fs-1 position-absolute ms-6" />
          <input v-model="search" @input="searchItems()" type="text" class="form-control form-control-solid w-250px ps-14" placeholder="Search FBOs" />
        </div>
      </div>
      <div class="card-toolbar" v-if="selectedIds.length > 0">
        <div class="d-flex justify-content-end align-items-center">
          <div class="fw-bold me-5"><span class="me-2">{{ selectedIds.length }}</span>Selected</div>
          <button type="button" class="btn btn-danger" @click="deleteFewFbos()">Delete Selected</button>
        </div>
      </div>
    </div>
    <div class="card-body pt-0">
      <KTDatatable @on-sort="sort" @on-items-select="onItemSelect" @on-items-per-page-change="onItemsPerPageChange" :data="fbos" :header="headerConfig" :checkbox-enabled="true" :loading="loading">
        <template v-slot:fbo="{ row: fbo }">
          <div class="d-flex align-items-center">
            <div class="symbol symbol-circle symbol-50px overflow-hidden me-3">
              <div class="symbol-label bg-light-info"><i class="ki-duotone ki-home-2 fs-2x text-info"><span class="path1"></span><span class="path2"></span></i></div>
            </div>
            <div class="d-flex flex-column">
              <a href="#" @click="handleView(fbo)" class="text-gray-800 text-hover-primary mb-1 fs-6 fw-bold">{{ fbo.name || 'Unnamed FBO' }}</a>
              <span class="text-muted fs-7">{{ fbo.airport_name || 'Unknown airport' }}</span>
            </div>
          </div>
        </template>
        <template v-slot:contact="{ row: fbo }"><span class="text-dark fw-semibold">{{ fbo.contact_info || 'No contact' }}</span></template>
        <template v-slot:services="{ row: fbo }"><span class="text-dark fw-semibold">{{ fbo.services || 'Standard services' }}</span></template>
        <template v-slot:actions="{ row: fbo }">
          <a href="#" class="btn btn-sm btn-light btn-active-light-primary" data-kt-menu-trigger="click" data-kt-menu-placement="bottom-end">Actions <KTIcon icon-name="down" icon-class="fs-5 m-0" /></a>
          <div class="menu menu-sub menu-sub-dropdown menu-column menu-rounded menu-gray-600 menu-state-bg-light-primary fw-semibold fs-7 w-200px py-4" data-kt-menu="true">
            <div class="menu-item px-3"><a @click="handleView(fbo)" class="menu-link px-3">View Details</a></div>
            <div class="menu-item px-3"><a @click="handleEdit(fbo)" class="menu-link px-3">Edit FBO</a></div>
            <div class="menu-item px-3"><a @click="handleViewTrips(fbo)" class="menu-link px-3">View Trips</a></div>
            <div class="separator mt-3 opacity-75"></div>
            <div class="menu-item px-3"><a @click="handleDelete(fbo)" class="menu-link px-3 text-danger">Delete</a></div>
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
  name: "fbos-management", components: { KTDatatable },
  setup() {
    const router = useRouter(); const toolbarStore = useToolbarStore(); const fbos = ref([]); const loading = ref(false); const selectedIds = ref([]); const search = ref(""); const initData = ref([]);
    const headerConfig = ref([{ columnName: "FBO", columnLabel: "fbo", sortEnabled: true }, { columnName: "Contact", columnLabel: "contact", sortEnabled: false }, { columnName: "Services", columnLabel: "services", sortEnabled: false }, { columnName: "Actions", columnLabel: "actions" }]);
    const fetchFbos = async () => { try { loading.value = true; const { data } = await ApiService.get("/fbos/"); fbos.value = data.results || data; initData.value.splice(0, fbos.value.length, ...fbos.value); } catch (error) { console.error("Error fetching FBOs:", error); } finally { loading.value = false; } };
    const handleCreate = () => Swal.fire({ title: "Add FBO", text: "FBO creation form would open here", icon: "info" });
    const handleEdit = (fbo) => Swal.fire({ title: "Edit FBO", text: `Edit ${fbo.name}`, icon: "info" });
    const handleView = (fbo) => Swal.fire({ title: "FBO Details", html: `<div class="text-start"><p><strong>Name:</strong> ${fbo.name}</p><p><strong>Contact:</strong> ${fbo.contact_info}</p><p><strong>Services:</strong> ${fbo.services}</p></div>`, icon: "info" });
    const handleViewTrips = (fbo) => router.push(`/admin/trips?fbo=${fbo.id}`);
    const handleDelete = async (fbo) => { const result = await Swal.fire({ title: "Delete FBO", text: `Delete ${fbo.name}?`, icon: "warning", showCancelButton: true, confirmButtonText: "Yes, delete!" }); if (result.isConfirmed) { try { await ApiService.delete(`/fbos/${fbo.id}/`); await fetchFbos(); Swal.fire("Deleted!", "FBO deleted.", "success"); } catch (error) { Swal.fire("Error!", "Failed to delete FBO.", "error"); } } };
    const deleteFewFbos = () => { selectedIds.value.forEach(id => fbos.value = fbos.value.filter(f => f.id !== id)); selectedIds.value = []; };
    const sort = (sort) => { if (sort.label) arraySort(fbos.value, sort.label, { reverse: sort.order === "asc" }); }; const onItemSelect = (items) => selectedIds.value = items;
    const searchItems = () => { fbos.value.splice(0, fbos.value.length, ...initData.value); if (search.value) { const results = initData.value.filter(item => Object.values(item).some(val => val?.toString().toLowerCase().includes(search.value.toLowerCase()))); fbos.value.splice(0, fbos.value.length, ...results); } MenuComponent.reinitialization(); };
    const onItemsPerPageChange = () => setTimeout(() => MenuComponent.reinitialization(), 0);
    onMounted(async () => { await fetchFbos(); await nextTick(); setTimeout(() => MenuComponent.reinitialization(), 100); toolbarStore.setActions([{ id: 'add-fbo', label: 'Add FBO', icon: 'plus', variant: 'primary', handler: handleCreate }]); });
    onUnmounted(() => toolbarStore.clearActions());
    return { search, searchItems, fbos, headerConfig, loading, sort, onItemSelect, selectedIds, deleteFewFbos, onItemsPerPageChange, handleCreate, handleEdit, handleView, handleViewTrips, handleDelete };
  },
});
</script>