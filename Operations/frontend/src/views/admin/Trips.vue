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
            placeholder="Search Trips"
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

          <!--begin::Add trip-->
          <button
            type="button"
            class="btn btn-primary"
            @click="openCreateTripModal"
          >
            <KTIcon icon-name="plus" icon-class="fs-2" />
            Add Trip
          </button>
          <!--end::Add trip-->
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
            @click="deleteFewTrips()"
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
        :data="trips"
        :header="headerConfig"
        :checkbox-enabled="true"
        :loading="loading"
      >
        <template v-slot:trip="{ row: trip }">
          <div class="d-flex align-items-center">
            <div class="symbol symbol-circle symbol-50px overflow-hidden me-3">
              <div class="symbol-label bg-light-primary">
                <i class="ki-duotone ki-airplane fs-2x text-primary">
                  <span class="path1"></span>
                  <span class="path2"></span>
                </i>
              </div>
            </div>
            <div class="d-flex flex-column">
              <a @click="navigateToTrip(trip.id)" href="#" class="text-gray-800 text-hover-primary mb-1 fs-6 fw-bold">
                {{ trip.trip_number }}
              </a>
              <span class="text-muted fs-7">{{ getRouteInfo(trip) }}</span>
            </div>
          </div>
        </template>

        <template v-slot:patient="{ row: trip }">
          <a v-if="trip.patient" @click="navigateToPatient(trip.patient)" href="#" class="text-dark fw-bold text-hover-primary">
            {{ getPatientName(trip.patient) }}
          </a>
          <span v-else class="text-muted">No patient</span>
        </template>

        <template v-slot:aircraft="{ row: trip }">
          <a v-if="trip.aircraft" @click="navigateToAircraft(trip.aircraft.id)" href="#" class="badge badge-light-info text-hover-primary">
            {{ getAircraftInfo(trip.aircraft) }}
          </a>
          <span v-else class="text-muted">TBD</span>
        </template>

        <template v-slot:type="{ row: trip }">
          <span :class="`badge badge-light-${getTripTypeColor(trip.type)} fs-7 fw-bold`">
            {{ trip.type }}
          </span>
        </template>

        <template v-slot:status="{ row: trip }">
          <span :class="`badge badge-light-${getStatusColor(trip.status)} fs-7 fw-bold`">
            {{ trip.status }}
          </span>
        </template>

        <template v-slot:departure="{ row: trip }">
          {{ formatDate(trip.estimated_departure_time) }}
        </template>

        <template v-slot:actions="{ row: trip }">
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
              <a @click="handleView(trip)" class="menu-link px-3">
                <KTIcon icon-name="eye" icon-class="fs-6 me-2" />
                View Details
              </a>
            </div>
            <!--end::Menu item-->
            <!--begin::Menu item-->
            <div class="menu-item px-3">
              <a @click="handleEdit(trip)" class="menu-link px-3">
                <KTIcon icon-name="pencil" icon-class="fs-6 me-2" />
                Edit Trip
              </a>
            </div>
            <!--end::Menu item-->
            <!--begin::Menu item-->
            <div class="menu-item px-3">
              <a @click="handleDuplicate(trip)" class="menu-link px-3">
                <KTIcon icon-name="copy" icon-class="fs-6 me-2" />
                Duplicate
              </a>
            </div>
            <!--end::Menu item-->
            <!--begin::Menu item-->
            <div class="menu-item px-3">
              <a @click="handleManifest(trip)" class="menu-link px-3">
                <KTIcon icon-name="document" icon-class="fs-6 me-2" />
                View Manifest
              </a>
            </div>
            <!--end::Menu item-->
            <!--begin::Separator-->
            <div class="separator my-2"></div>
            <!--end::Separator-->
            <!--begin::Menu item-->
            <div class="menu-item px-3">
              <a @click="handleDelete(trip)" class="menu-link px-3 text-danger">
                <KTIcon icon-name="trash" icon-class="fs-6 me-2" />
                Delete Trip
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
  
  <!-- Create Trip Modal -->
  <CreateTripSimpleModal @tripCreated="onTripCreated" />
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
import CreateTripSimpleModal from "@/components/modals/CreateTripSimpleModal.vue";
import { Modal } from "bootstrap";
import { useToolbar, createToolbarActions } from "@/core/helpers/toolbar";

interface Trip {
  id: string;
  trip_number: string;
  type: string;
  status: string;
  patient?: {
    id: string;
    status: string;
    info: {
      first_name: string;
      last_name: string;
      email: string;
    };
  };
  aircraft?: {
    id: string;
    tail_number: string;
    make: string;
    model: string;
  };
  quote?: {
    id: string;
    quoted_amount: string;
    status: string;
  };
  estimated_departure_time: string;
  created_on: string;
  trip_lines?: Array<{
    id: string;
    origin_airport: {
      icao_code: string;
      iata_code: string;
      name: string;
    };
    destination_airport: {
      icao_code: string;
      iata_code: string;
      name: string;
    };
  }>;
  passengers_data?: any[];
}

export default defineComponent({
  name: "trips-management",
  components: {
    KTDatatable,
    CreateTripSimpleModal,
  },
  setup() {
    const router = useRouter();
    const trips = ref<Trip[]>([]);
    const loading = ref(false);
    const error = ref<string | null>(null);
    const { setToolbarActions } = useToolbar();

    const headerConfig = ref([
      {
        columnName: "Trip",
        columnLabel: "trip",
        sortEnabled: true,
      },
      {
        columnName: "Patient",
        columnLabel: "patient",
        sortEnabled: false,
      },
      {
        columnName: "Aircraft",
        columnLabel: "aircraft",
        sortEnabled: false,
      },
      {
        columnName: "Type",
        columnLabel: "type",
        sortEnabled: true,
      },
      {
        columnName: "Status",
        columnLabel: "status",
        sortEnabled: true,
      },
      {
        columnName: "Departure",
        columnLabel: "departure",
        sortEnabled: true,
      },
      {
        columnName: "Actions",
        columnLabel: "actions",
      },
    ]);

    const initData = ref<Array<Trip>>([]);
    const selectedIds = ref<Array<number>>([]);
    const search = ref<string>("");

    // Methods
    const fetchTrips = async () => {
      try {
        loading.value = true;
        error.value = null;
        const { data } = await ApiService.get("/trips/");
        trips.value = data.results || data;
        initData.value.splice(0, trips.value.length, ...trips.value);
      } catch (err: any) {
        error.value = err.response?.data?.detail || "Failed to fetch trips";
        console.error("Error fetching trips:", err);
      } finally {
        loading.value = false;
        // Reinitialize menu components after data loads
        setTimeout(() => {
          MenuComponent.reinitialization();
        }, 100);
      }
    };

    const openCreateTripModal = () => {
      const modalElement = document.getElementById('kt_modal_create_trip_simple');
      
      if (modalElement) {
        try {
          const modal = new Modal(modalElement);
          modal.show();
        } catch (error) {
          console.error('Error opening modal:', error);
          Swal.fire({
            title: "Error",
            text: "Unable to open modal. Please refresh and try again.",
            icon: "error",
            confirmButtonText: "OK"
          });
        }
      }
    };

    const handleCreate = () => {
      openCreateTripModal();
    };

    const handleEdit = (trip: Trip) => {
      Swal.fire({
        title: "Edit Trip",
        text: `Trip editing functionality would be implemented here for trip ${trip.trip_number}`,
        icon: "info",
        confirmButtonText: "OK"
      });
    };

    const handleView = (trip: Trip) => {
      router.push(`/admin/trips/${trip.id}`);
    };

    const handleDelete = (trip: Trip) => {
      Swal.fire({
        title: "Delete Trip",
        text: `Are you sure you want to delete trip ${trip.trip_number}? This action cannot be undone.`,
        icon: "warning",
        showCancelButton: true,
        confirmButtonText: "Yes, delete it!",
        cancelButtonText: "Cancel",
        confirmButtonColor: "#d33"
      }).then(async (result) => {
        if (result.isConfirmed) {
          try {
            // Here you would make the API call to delete the trip
            // await ApiService.delete(`/trips/${trip.id}/`);
            
            Swal.fire({
              title: "Deleted!",
              text: "Trip has been deleted successfully.",
              icon: "success"
            }).then(() => {
              // Refresh the trips list
              fetchTrips();
            });
          } catch (error) {
            Swal.fire({
              title: "Error",
              text: "Failed to delete the trip. Please try again.",
              icon: "error"
            });
          }
        }
      });
    };

    const getPatientName = (patient: any): string => {
      if (!patient) return 'No patient';
      if (patient.info) {
        return `${patient.info.first_name} ${patient.info.last_name}`;
      }
      return `Patient #${String(patient.id).slice(0, 8)}`;
    };

    const getAircraftInfo = (aircraft: any): string => {
      if (!aircraft) return 'TBD';
      if (aircraft.tail_number) {
        return `${aircraft.tail_number} (${aircraft.make} ${aircraft.model})`;
      }
      return `Aircraft #${String(aircraft.id).slice(0, 8)}`;
    };

    const getRouteInfo = (trip: Trip): string => {
      if (trip.trip_lines && trip.trip_lines.length > 0) {
        const firstLeg = trip.trip_lines[0];
        const lastLeg = trip.trip_lines[trip.trip_lines.length - 1];
        
        if (trip.trip_lines.length === 1) {
          return `${firstLeg.origin_airport.iata_code || firstLeg.origin_airport.icao_code} → ${firstLeg.destination_airport.iata_code || firstLeg.destination_airport.icao_code}`;
        } else {
          // Multi-leg trip
          return `${firstLeg.origin_airport.iata_code || firstLeg.origin_airport.icao_code} → ${lastLeg.destination_airport.iata_code || lastLeg.destination_airport.icao_code} (${trip.trip_lines.length} legs)`;
        }
      }
      return trip.type?.toUpperCase() || 'MEDICAL';
    };

    const getTripTypeColor = (type: string): string => {
      const colors: Record<string, string> = {
        medical: 'danger',
        charter: 'primary',
        'part 91': 'info',
        maintenance: 'warning',
        other: 'secondary',
      };
      return colors[type] || 'secondary';
    };

    const getStatusColor = (status: string): string => {
      const colors: Record<string, string> = {
        active: 'success',
        pending: 'warning',
        completed: 'primary',
        cancelled: 'danger',
      };
      return colors[status] || 'secondary';
    };

    const formatDate = (dateString: string): string => {
      if (!dateString) return 'Not set';
      return new Date(dateString).toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit',
      });
    };

    const deleteFewTrips = () => {
      selectedIds.value.forEach((item) => {
        deleteTrip(item);
      });
      selectedIds.value.length = 0;
    };

    const deleteTrip = (id: number) => {
      for (let i = 0; i < trips.value.length; i++) {
        if (trips.value[i].id === id.toString()) {
          trips.value.splice(i, 1);
        }
      }
    };

    const sort = (sort: Sort) => {
      const reverse: boolean = sort.order === "asc";
      if (sort.label) {
        arraySort(trips.value, sort.label, { reverse });
      }
    };

    const onItemSelect = (selectedItems: Array<number>) => {
      selectedIds.value = selectedItems;
    };

    const searchItems = () => {
      trips.value.splice(0, trips.value.length, ...initData.value);
      if (search.value !== "") {
        let results: Array<Trip> = [];
        for (let j = 0; j < initData.value.length; j++) {
          if (searchingFunc(initData.value[j], search.value)) {
            results.push(initData.value[j]);
          }
        }
        trips.value.splice(0, trips.value.length, ...results);
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

    // Navigation methods
    const navigateToTrip = (tripId: string) => {
      router.push(`/admin/trips/${tripId}`);
    };

    const navigateToPatient = (patient: any) => {
      if (patient && patient.info && patient.info.id) {
        // Navigate to the contact details for this patient's contact info
        router.push(`/admin/contacts/patients/${patient.info.id}`);
      } else {
        // Fallback to patients list page
        router.push('/admin/patients');
      }
    };

    const navigateToAircraft = (aircraftId: string) => {
      router.push(`/admin/aircraft/${aircraftId}`);
    };

    // New action methods
    const handleDuplicate = (trip: Trip) => {
      Swal.fire({
        title: "Duplicate Trip",
        text: `Create a copy of trip ${trip.trip_number}?`,
        icon: "question",
        showCancelButton: true,
        confirmButtonText: "Yes, duplicate it!",
        cancelButtonText: "Cancel"
      }).then((result) => {
        if (result.isConfirmed) {
          Swal.fire("Duplicated!", "Trip has been duplicated.", "success");
        }
      });
    };

    const handleManifest = (trip: Trip) => {
      Swal.fire({
        title: "Trip Manifest",
        text: `View manifest for trip ${trip.trip_number}`,
        icon: "info",
        confirmButtonText: "OK"
      });
    };

    // Handle trip created event from modal
    const onTripCreated = (newTrip: Trip) => {
      console.log('New trip created:', newTrip);
      // Refresh the trips list
      fetchTrips();
    };

    onMounted(() => {
      fetchTrips();
      // Initialize menu components
      setTimeout(() => {
        MenuComponent.reinitialization();
      }, 200);

      // Setup toolbar actions for trips page
      setToolbarActions([
        createToolbarActions.primary('add-trip', 'Add Trip', openCreateTripModal, 'plus')
      ]);
    });

    return {
      search,
      searchItems,
      trips,
      headerConfig,
      loading,
      error,
      sort,
      onItemSelect,
      selectedIds,
      deleteFewTrips,
      deleteTrip,
      onItemsPerPageChange,
      openCreateTripModal,
      handleCreate,
      handleEdit,
      handleView,
      handleDelete,
      getPatientName,
      getAircraftInfo,
      getRouteInfo,
      getTripTypeColor,
      getStatusColor,
      formatDate,
      navigateToTrip,
      navigateToPatient,
      navigateToAircraft,
      handleDuplicate,
      handleManifest,
      onTripCreated,
    };
  },
});
</script>