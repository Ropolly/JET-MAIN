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
            placeholder="Search Aircraft"
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
            @click="deleteFewAircraft()"
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
        :data="aircraft"
        :header="headerConfig"
        :checkbox-enabled="true"
        :loading="loading"
      >
        <template v-slot:aircraft="{ row: plane }">
          <div class="d-flex align-items-center">
            <div class="symbol symbol-circle symbol-50px overflow-hidden me-3">
              <img :src="getAircraftImage(plane)" :alt="getAircraftModel(plane)" class="symbol-label object-fit-cover" style="width: 50px; height: 50px; border-radius: 50%;" />
            </div>
            <div class="d-flex flex-column">
              <a href="#" @click="navigateToAircraft(plane.id)" class="text-gray-800 text-hover-primary mb-1 fs-6 fw-bold">
                {{ plane.tail_number || 'No tail number' }}
              </a>
              <span class="text-muted fs-7">{{ getAircraftModel(plane) }}</span>
            </div>
          </div>
        </template>

        <template v-slot:specifications="{ row: plane }">
          <div class="d-flex flex-column">
            <span class="text-dark fw-semibold fs-6">
              {{ plane.make }} {{ plane.model }}
            </span>
            <span class="text-muted fs-7">MGTOW: {{ formatWeight(plane.mgtow) }}</span>
          </div>
        </template>

        <template v-slot:company="{ row: plane }">
          <span class="text-dark fw-semibold">
            {{ plane.company || 'Not specified' }}
          </span>
        </template>

        <template v-slot:serial="{ row: plane }">
          <span class="text-dark fw-semibold">
            {{ plane.serial_number || 'Not specified' }}
          </span>
        </template>

        <template v-slot:status="{ row: plane }">
          <span :class="`badge badge-light-${getStatusColor(plane.status)} fs-7 fw-bold`">
            {{ plane.status || 'Active' }}
          </span>
        </template>

        <template v-slot:actions="{ row: plane }">
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
              <a @click="handleView(plane)" class="menu-link px-3"
                >View Details</a
              >
            </div>
            <!--end::Menu item-->
            <!--begin::Menu item-->
            <div class="menu-item px-3">
              <a @click="handleEdit(plane)" class="menu-link px-3"
                >Edit Aircraft</a
              >
            </div>
            <!--end::Menu item-->
            <!--begin::Menu item-->
            <div class="menu-item px-3">
              <a @click="handleViewTrips(plane)" class="menu-link px-3"
                >View Trips</a
              >
            </div>
            <!--end::Menu item-->
            <!--begin::Menu item-->
            <div class="menu-item px-3">
              <a @click="handleMaintenanceLog(plane)" class="menu-link px-3"
                >Maintenance Log</a
              >
            </div>
            <!--end::Menu item-->
            <div class="separator mt-3 opacity-75"></div>
            <!--begin::Menu item-->
            <div class="menu-item px-3">
              <a @click="handleDelete(plane)" class="menu-link px-3 text-danger"
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

interface Aircraft {
  id: string;
  tail_number: string;
  company: string;
  mgtow: string;
  make: string;
  model: string;
  serial_number: string;
  status?: string;
  created_on: string;
}

export default defineComponent({
  name: "aircraft-management",
  components: {
    KTDatatable,
  },
  setup() {
    const router = useRouter();
    const toolbarStore = useToolbarStore();
    const aircraft = ref<Aircraft[]>([]);
    const loading = ref(false);
    const error = ref<string | null>(null);

    const headerConfig = ref([
      {
        columnName: "Aircraft",
        columnLabel: "aircraft",
        sortEnabled: true,
      },
      {
        columnName: "Specifications",
        columnLabel: "specifications",
        sortEnabled: false,
      },
      {
        columnName: "Company",
        columnLabel: "company",
        sortEnabled: true,
      },
      {
        columnName: "Serial Number",
        columnLabel: "serial",
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

    const initData = ref<Array<Aircraft>>([]);
    const selectedIds = ref<Array<number>>([]);
    const search = ref<string>("");

    // Methods
    const fetchAircraft = async () => {
      try {
        loading.value = true;
        error.value = null;
        const { data } = await ApiService.get("/aircraft/");
        aircraft.value = data.results || data;
        initData.value.splice(0, aircraft.value.length, ...aircraft.value);
      } catch (err: any) {
        error.value = err.response?.data?.detail || "Failed to fetch aircraft";
        console.error("Error fetching aircraft:", err);
      } finally {
        loading.value = false;
      }
    };

    const handleCreate = () => {
      Swal.fire({
        title: "Add Aircraft",
        text: "Aircraft creation form would open here",
        icon: "info",
        confirmButtonText: "OK"
      });
    };

    const handleEdit = (plane: Aircraft) => {
      Swal.fire({
        title: "Edit Aircraft",
        text: `Edit form for ${plane.tail_number} would open here`,
        icon: "info",
        confirmButtonText: "OK"
      });
    };

    const handleView = (plane: Aircraft) => {
      navigateToAircraft(plane.id);
    };

    const handleViewTrips = (plane: Aircraft) => {
      router.push(`/admin/trips?aircraft=${plane.id}`);
    };

    const handleMaintenanceLog = (plane: Aircraft) => {
      Swal.fire({
        title: "Maintenance Log",
        text: `Maintenance log for ${plane.tail_number} would open here`,
        icon: "info",
        confirmButtonText: "OK"
      });
    };

    const handleDelete = async (plane: Aircraft) => {
      const result = await Swal.fire({
        title: "Delete Aircraft",
        text: `Are you sure you want to delete ${plane.tail_number}?`,
        icon: "warning",
        showCancelButton: true,
        confirmButtonText: "Yes, delete it!",
        cancelButtonText: "Cancel"
      });
      
      if (result.isConfirmed) {
        try {
          await ApiService.delete(`/aircraft/${plane.id}/`);
          await fetchAircraft(); // Refresh the list
          Swal.fire("Deleted!", "Aircraft has been deleted.", "success");
        } catch (error: any) {
          console.error('Error deleting aircraft:', error);
          Swal.fire("Error!", "Failed to delete aircraft. Please try again.", "error");
        }
      }
    };

    const navigateToAircraft = (aircraftId: string) => {
      router.push(`/admin/aircraft/${aircraftId}`);
    };

    const getAircraftModel = (plane: Aircraft): string => {
      return `${plane.make} ${plane.model}` || 'Unknown model';
    };

    const getAircraftImage = (plane: Aircraft): string => {
      if (!plane) return '/media/aircraft/Learjet35A.jpg';
      
      // Build full model name for matching image files
      const make = plane.make || '';
      const model = plane.model || '';
      const fullModel = `${make} ${model}`.trim();
      
      // Map known aircraft to their image filenames
      const imageMap: Record<string, string> = {
        'Kodiak Kodiak 100': 'kodiak100.jpg',
        'Learjet 35A': 'Learjet35A.jpg',
        'Learjet 36A': 'learjet36a.jpeg',
        'Learjet 31': 'learjet30.jpg', // Using learjet30 as fallback for 31
        'Learjet 60': 'Learjet60.jpg',
      };
      
      // Return specific image or fallback to generic
      const imageName = imageMap[fullModel] || 'Learjet35A.jpg'; // Default fallback
      return `/media/aircraft/${imageName}`;
    };

    const formatWeight = (weight: string): string => {
      if (!weight) return 'Not specified';
      return `${parseFloat(weight).toLocaleString()} lbs`;
    };

    const getStatusColor = (status: string): string => {
      const colors: Record<string, string> = {
        active: 'success',
        inactive: 'secondary',
        maintenance: 'warning',
        retired: 'danger',
      };
      return colors[status?.toLowerCase()] || 'primary';
    };

    const deleteFewAircraft = () => {
      selectedIds.value.forEach((item) => {
        deleteAircraft(item);
      });
      selectedIds.value.length = 0;
    };

    const deleteAircraft = (id: number) => {
      for (let i = 0; i < aircraft.value.length; i++) {
        if (aircraft.value[i].id === id.toString()) {
          aircraft.value.splice(i, 1);
        }
      }
    };

    const sort = (sort: Sort) => {
      const reverse: boolean = sort.order === "asc";
      if (sort.label) {
        arraySort(aircraft.value, sort.label, { reverse });
      }
    };

    const onItemSelect = (selectedItems: Array<number>) => {
      selectedIds.value = selectedItems;
    };

    const searchItems = () => {
      aircraft.value.splice(0, aircraft.value.length, ...initData.value);
      if (search.value !== "") {
        let results: Array<Aircraft> = [];
        for (let j = 0; j < initData.value.length; j++) {
          if (searchingFunc(initData.value[j], search.value)) {
            results.push(initData.value[j]);
          }
        }
        aircraft.value.splice(0, aircraft.value.length, ...results);
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
      await fetchAircraft();
      // Ensure menus are properly initialized
      await nextTick();
      setTimeout(() => {
        MenuComponent.reinitialization();
      }, 100);
      
      // Set toolbar actions
      toolbarStore.setActions([
        {
          id: 'add-aircraft',
          label: 'Add Aircraft',
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
      aircraft,
      headerConfig,
      loading,
      error,
      sort,
      onItemSelect,
      selectedIds,
      deleteFewAircraft,
      deleteAircraft,
      onItemsPerPageChange,
      handleCreate,
      handleEdit,
      handleView,
      handleViewTrips,
      handleMaintenanceLog,
      handleDelete,
      navigateToAircraft,
      getAircraftModel,
      getAircraftImage,
      formatWeight,
      getStatusColor,
    };
  },
});
</script>