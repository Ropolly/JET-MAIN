<template>
  <!--begin::Card-->
  <div class="card">
    <!--begin::Card header-->
    <div class="card-header border-0 pt-6">
      <!--begin::Card title-->
      <div class="card-title">
        <!--begin::Search-->
        <div class="d-flex align-items-center position-relative my-1">
          <KTIcon icon-name="magnifier" icon-class="fs-1 position-absolute ms-6" />
          <input
            v-model="search"
            @input="searchItems()"
            type="text"
            class="form-control form-control-solid w-250px ps-14"
            placeholder="Search Passengers"
          />
        </div>
        <!--end::Search-->
      </div>

      <!--begin::Card toolbar-->
      <div class="card-toolbar" v-if="selectedIds.length > 0">
        <div class="d-flex justify-content-end align-items-center">
          <div class="fw-bold me-5">
            <span class="me-2">{{ selectedIds.length }}</span>Selected
          </div>
          <button type="button" class="btn btn-danger" @click="deleteFewPassengers()">
            Delete Selected
          </button>
        </div>
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
        :data="passengers"
        :header="headerConfig"
        :checkbox-enabled="true"
        :loading="loading"
      >
        <template v-slot:passenger="{ row: passenger }">
          <div class="d-flex align-items-center">
            <div class="symbol symbol-circle symbol-50px overflow-hidden me-3">
              <div class="symbol-label bg-light-warning">
                <i class="ki-duotone ki-profile-user fs-2x text-warning">
                  <span class="path1"></span>
                  <span class="path2"></span>
                  <span class="path3"></span>
                  <span class="path4"></span>
                </i>
              </div>
            </div>
            <div class="d-flex flex-column">
              <a href="#" @click="handleView(passenger)" class="text-gray-800 text-hover-primary mb-1 fs-6 fw-bold">
                {{ getPassengerName(passenger) }}
              </a>
              <span class="text-muted fs-7">{{ passenger.nationality || 'Unknown nationality' }}</span>
            </div>
          </div>
        </template>

        <template v-slot:passport="{ row: passenger }">
          <div class="d-flex flex-column">
            <span class="text-dark fw-semibold fs-6">{{ passenger.passport_number || 'N/A' }}</span>
            <span class="text-muted fs-7">Exp: {{ formatDate(passenger.passport_expiration_date) }}</span>
          </div>
        </template>

        <template v-slot:contact="{ row: passenger }">
          <span class="text-dark fw-semibold">{{ passenger.contact_number || 'No contact' }}</span>
        </template>

        <template v-slot:status="{ row: passenger }">
          <span :class="`badge badge-light-${getStatusColor(passenger.status)} fs-7 fw-bold`">
            {{ passenger.status || 'Active' }}
          </span>
        </template>

        <template v-slot:actions="{ row: passenger }">
          <a
            href="#"
            class="btn btn-sm btn-light btn-active-light-primary"
            data-kt-menu-trigger="click"
            data-kt-menu-placement="bottom-end"
            data-kt-menu-flip="top-end"
            >Actions
            <KTIcon icon-name="down" icon-class="fs-5 m-0" />
          </a>
          <div class="menu menu-sub menu-sub-dropdown menu-column menu-rounded menu-gray-600 menu-state-bg-light-primary fw-semibold fs-7 w-200px py-4" data-kt-menu="true">
            <div class="menu-item px-3"><a @click="handleView(passenger)" class="menu-link px-3">View Details</a></div>
            <div class="menu-item px-3"><a @click="handleEdit(passenger)" class="menu-link px-3">Edit Passenger</a></div>
            <div class="menu-item px-3"><a @click="handleViewTrips(passenger)" class="menu-link px-3">View Trips</a></div>
            <div class="separator mt-3 opacity-75"></div>
            <div class="menu-item px-3"><a @click="handleDelete(passenger)" class="menu-link px-3 text-danger">Delete</a></div>
          </div>
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

export default defineComponent({
  name: "passengers-management",
  components: { KTDatatable },
  setup() {
    const router = useRouter();
    const toolbarStore = useToolbarStore();
    const passengers = ref([]);
    const loading = ref(false);
    const selectedIds = ref([]);
    const search = ref("");
    const initData = ref([]);

    const headerConfig = ref([
      { columnName: "Passenger", columnLabel: "passenger", sortEnabled: true },
      { columnName: "Passport", columnLabel: "passport", sortEnabled: false },
      { columnName: "Contact", columnLabel: "contact", sortEnabled: false },
      { columnName: "Status", columnLabel: "status", sortEnabled: true },
      { columnName: "Actions", columnLabel: "actions" },
    ]);

    const fetchPassengers = async () => {
      try {
        loading.value = true;
        const { data } = await ApiService.get("/passengers/");
        passengers.value = data.results || data;
        initData.value.splice(0, passengers.value.length, ...passengers.value);
      } catch (error) {
        console.error("Error fetching passengers:", error);
      } finally {
        loading.value = false;
      }
    };

    const handleCreate = () => Swal.fire({ title: "Add Passenger", text: "Passenger creation form would open here", icon: "info" });
    const handleEdit = (passenger) => Swal.fire({ title: "Edit Passenger", text: `Edit ${getPassengerName(passenger)}`, icon: "info" });
    const handleView = (passenger) => Swal.fire({ title: "Passenger Details", html: `<div class="text-start"><p><strong>Name:</strong> ${getPassengerName(passenger)}</p><p><strong>Nationality:</strong> ${passenger.nationality}</p><p><strong>Passport:</strong> ${passenger.passport_number}</p><p><strong>Contact:</strong> ${passenger.contact_number}</p></div>`, icon: "info" });
    const handleViewTrips = (passenger) => router.push(`/admin/trips?passenger=${passenger.id}`);
    const handleDelete = async (passenger) => {
      const result = await Swal.fire({ title: "Delete Passenger", text: `Delete ${getPassengerName(passenger)}?`, icon: "warning", showCancelButton: true, confirmButtonText: "Yes, delete!" });
      if (result.isConfirmed) {
        try { await ApiService.delete(`/passengers/${passenger.id}/`); await fetchPassengers(); Swal.fire("Deleted!", "Passenger deleted.", "success"); }
        catch (error) { Swal.fire("Error!", "Failed to delete passenger.", "error"); }
      }
    };

    const formatDate = (date) => date ? new Date(date).toLocaleDateString() : 'N/A';
    const getStatusColor = (status) => ({ active: 'success', inactive: 'secondary' }[status?.toLowerCase()] || 'primary');
    
    const getPassengerName = (passenger) => {
      if (passenger?.info) {
        const first = passenger.info.first_name || '';
        const last = passenger.info.last_name || '';
        const fullName = `${first} ${last}`.trim();
        return fullName || passenger.info.business_name || passenger.info.email || 'Unnamed Passenger';
      }
      return 'Unnamed Passenger';
    };
    const deleteFewPassengers = () => { selectedIds.value.forEach(id => passengers.value = passengers.value.filter(p => p.id !== id)); selectedIds.value = []; };

    const sort = (sort) => { if (sort.label) arraySort(passengers.value, sort.label, { reverse: sort.order === "asc" }); };
    const onItemSelect = (items) => selectedIds.value = items;
    const searchItems = () => {
      passengers.value.splice(0, passengers.value.length, ...initData.value);
      if (search.value) {
        const results = initData.value.filter(item => Object.values(item).some(val => val?.toString().toLowerCase().includes(search.value.toLowerCase())));
        passengers.value.splice(0, passengers.value.length, ...results);
      }
      MenuComponent.reinitialization();
    };
    const onItemsPerPageChange = () => setTimeout(() => MenuComponent.reinitialization(), 0);

    onMounted(async () => {
      await fetchPassengers();
      await nextTick();
      setTimeout(() => MenuComponent.reinitialization(), 100);
      toolbarStore.setActions([{ id: 'add-passenger', label: 'Add Passenger', icon: 'plus', variant: 'primary', handler: handleCreate }]);
    });

    onUnmounted(() => toolbarStore.clearActions());

    return {
      search, searchItems, passengers, headerConfig, loading, sort, onItemSelect, selectedIds, deleteFewPassengers, onItemsPerPageChange,
      handleCreate, handleEdit, handleView, handleViewTrips, handleDelete, formatDate, getStatusColor, getPassengerName,
    };
  },
});
</script>