<template>
  <!--begin::Card-->
  <div class="card">
    <!--begin::Card header-->
    <div class="card-header border-0 pt-6">
      <!--begin::Card title with search-->
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
            placeholder="Search by trip number, patient or passenger name..."
          />
        </div>
        <!--end::Search-->

        <!--begin::Selected actions (when items selected)-->
        <div v-if="selectedIds.length > 0" class="d-flex align-items-center ms-5">
          <div class="fw-bold me-5">
            <span class="me-2">{{ selectedIds.length }}</span>Selected
          </div>
          <button
            type="button"
            class="btn btn-danger btn-sm"
            @click="deleteFewTrips()"
          >
            Delete Selected
          </button>
        </div>
        <!--end::Selected actions-->
      </div>
      <!--end::Card title with search-->

      <!--begin::Card toolbar with tabs-->
      <div class="card-toolbar">
        <ul class="nav nav-tabs nav-line-tabs nav-stretch fs-6 border-0">
          <li class="nav-item">
            <a 
              class="nav-link"
              :class="{ active: activeTab === 'all' }"
              @click.prevent="handleTabChange('all')"
              data-bs-toggle="tab"
              href="#kt_tab_all_trips"
            >
              All Trips
              <span class="ms-1 badge" :class="activeTab === 'all' ? 'badge-secondary' : 'badge-light-secondary'">{{ getAllTripsCount() }}</span>
            </a>
          </li>
          <li class="nav-item">
            <a 
              class="nav-link"
              :class="{ active: activeTab === 'active' }"
              @click.prevent="handleTabChange('active')"
              data-bs-toggle="tab"
              href="#kt_tab_scheduled_trips"
            >
              Scheduled
              <span class="ms-1 badge" :class="activeTab === 'active' ? 'badge-success' : 'badge-light-secondary'">{{ getStatusCount('active') }}</span>
            </a>
          </li>
          <li class="nav-item">
            <a 
              class="nav-link"
              :class="{ active: activeTab === 'pending' }"
              @click.prevent="handleTabChange('pending')"
              data-bs-toggle="tab"
              href="#kt_tab_pending_trips"
            >
              Pending
              <span class="ms-1 badge" :class="activeTab === 'pending' ? 'badge-warning' : 'badge-light-secondary'">{{ getStatusCount('pending') }}</span>
            </a>
          </li>
          <li class="nav-item">
            <a 
              class="nav-link"
              :class="{ active: activeTab === 'completed' }"
              @click.prevent="handleTabChange('completed')"
              data-bs-toggle="tab"
              href="#kt_tab_completed_trips"
            >
              Completed
              <span class="ms-1 badge" :class="activeTab === 'completed' ? 'badge-primary' : 'badge-light-secondary'">{{ getStatusCount('completed') }}</span>
            </a>
          </li>
          <li class="nav-item">
            <a 
              class="nav-link"
              :class="{ active: activeTab === 'cancelled' }"
              @click.prevent="handleTabChange('cancelled')"
              data-bs-toggle="tab"
              href="#kt_tab_cancelled_trips"
            >
              Canceled
              <span class="ms-1 badge" :class="activeTab === 'cancelled' ? 'badge-danger' : 'badge-light-secondary'">{{ getStatusCount('cancelled') }}</span>
            </a>
          </li>
        </ul>
      </div>
      <!--end::Card toolbar with tabs-->
    </div>
    <!--end::Card header-->

    <!--begin::Card body-->
    <div class="card-body pt-0">
      <!-- Single KTDatatable with filtered data based on active tab -->
      <KTDatatable
        @on-sort="sort"
        @on-items-select="onItemSelect"
        @on-items-per-page-change="onItemsPerPageChange"
        @page-change="onPageChange"
        :data="filteredTrips"
        :header="headerConfig"
        :checkbox-enabled="true"
        :loading="loading"
        :total="totalItems"
        :current-page="currentPage"
        :items-per-page="pageSize"
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
              <a @click.prevent="navigateToTrip(trip.id)" href="#" class="text-gray-800 text-hover-primary mb-1 fs-6 fw-bold">
                {{ trip.trip_number }}
              </a>
              <span class="text-muted fs-7">{{ getRouteInfo(trip) }}</span>
            </div>
          </div>
        </template>

        <template v-slot:patient="{ row: trip }">
          <a v-if="trip.patient" @click.prevent="navigateToPatient(trip.patient)" href="#" class="text-dark fw-bold text-hover-primary">
            {{ getPatientName(trip.patient) }}
          </a>
          <span v-else class="text-muted">No patient</span>
        </template>

        <template v-slot:aircraft="{ row: trip }">
          <a v-if="trip.aircraft" @click.prevent="navigateToAircraft(trip.aircraft.id)" href="#" class="badge badge-light-info text-hover-primary">
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
  
  <!-- Create Trip Modals -->
  <CreateTripSimpleModal @tripCreated="onTripCreated" />
  <CreateTripMultiStepModal @tripCreated="onTripCreated" />
</template>

<script lang="ts">
import { defineComponent, ref, computed, onMounted, onUnmounted } from "vue";
import ApiService from "@/core/services/ApiService";
import KTDatatable from "@/components/kt-datatable/KTDataTable.vue";
import type { Sort } from "@/components/kt-datatable/table-partials/models";
import arraySort from "array-sort";
import { MenuComponent } from "@/assets/ts/components";
import Swal from "sweetalert2";
import { useRouter } from "vue-router";
import CreateTripSimpleModal from "@/components/modals/CreateTripSimpleModal.vue";
import CreateTripMultiStepModal from "@/components/modals/CreateTripMultiStepModal.vue";
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
    CreateTripMultiStepModal,
  },
  setup() {
    const router = useRouter();
    const trips = ref<Trip[]>([]);
    const loading = ref(false);
    const error = ref<string | null>(null);
    const { setToolbarActions } = useToolbar();
    const totalItems = ref(0);
    const currentPage = ref(1);
    const pageSize = ref(25);
    const searchTimeout = ref<NodeJS.Timeout | null>(null);

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

    const selectedIds = ref<Array<number>>([]);
    const search = ref<string>("");
    const activeTab = ref<string>("all");

    // Store counts for each status
    const statusCounts = ref<Record<string, number>>({
      all: 0,
      pending: 0,
      confirmed: 0,
      active: 0,
      completed: 0,
      cancelled: 0,
      paid: 0
    });

    // Computed properties
    const filteredTrips = computed(() => {
      return trips.value;
    });

    // Tab count methods
    const getAllTripsCount = () => statusCounts.value.all;
    
    const getStatusCount = (status: string) => {
      return statusCounts.value[status] || 0;
    };

    // Methods
    const fetchTrips = async (page: number = 1, pageLimit: number = 25, searchQuery: string = '', statusFilter: string = 'all') => {
      try {
        loading.value = true;
        error.value = null;
        
        const params = new URLSearchParams();
        params.append('page', page.toString());
        params.append('page_size', pageLimit.toString());
        if (searchQuery.trim()) {
          params.append('search', searchQuery.trim());
        }
        if (statusFilter !== 'all') {
          params.append('status', statusFilter);
        }
        
        const { data } = await ApiService.get(`/trips/?${params}`);
        trips.value = data.results || [];
        totalItems.value = data.count || 0;
        currentPage.value = page;
        
        // Update status counts if we're on the 'all' tab
        if (statusFilter === 'all' && !searchQuery) {
          // Fetch counts for each status
          await fetchStatusCounts();
        }
      } catch (err: any) {
        error.value = err.response?.data?.detail || "Failed to fetch trips";
        console.error("Error fetching trips:", err);
        trips.value = [];
        totalItems.value = 0;
      } finally {
        loading.value = false;
        // Reinitialize menu components after data loads
        setTimeout(() => {
          MenuComponent.reinitialization();
        }, 100);
      }
    };

    const fetchStatusCounts = async () => {
      try {
        // Fetch total count
        const allResponse = await ApiService.get('/trips/?page_size=1');
        statusCounts.value.all = allResponse.data.count || 0;
        
        // Fetch counts for each status
        const statuses = ['pending', 'confirmed', 'active', 'completed', 'cancelled', 'paid'];
        for (const status of statuses) {
          const response = await ApiService.get(`/trips/?status=${status}&page_size=1`);
          statusCounts.value[status] = response.data.count || 0;
        }
      } catch (err) {
        console.error('Error fetching status counts:', err);
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

    const openMultiStepTripModal = () => {
      const modalElement = document.getElementById('kt_modal_create_trip_multistep');
      
      if (modalElement) {
        try {
          const modal = new Modal(modalElement);
          modal.show();
        } catch (error) {
          console.error('Error opening multi-step modal:', error);
          Swal.fire({
            title: "Error", 
            text: "Unable to open multi-step trip creation modal. Please refresh and try again.",
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
            await ApiService.delete(`/trips/${trip.id}/`);
            
            Swal.fire({
              title: "Deleted!",
              text: "Trip has been deleted successfully.",
              icon: "success"
            }).then(() => {
              // Refresh the trips list
              fetchTrips(currentPage.value, pageSize.value, search.value, activeTab.value);
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
      // First check if trip_lines exist
      if (!trip.trip_lines || trip.trip_lines.length === 0) {
        // No trip lines, show type as fallback
        return `${trip.type || 'No Route'}`.toUpperCase();
      }
      
      // Get first and last leg for route
      const firstLeg = trip.trip_lines[0];
      const lastLeg = trip.trip_lines[trip.trip_lines.length - 1];
      
      // Try to get airport codes - check multiple possible field names
      let originCode = 'UNK';
      let destCode = 'UNK';
      
      if (firstLeg.origin_airport) {
        originCode = firstLeg.origin_airport.iata_code || 
                    firstLeg.origin_airport.icao_code || 
                    firstLeg.origin_airport.code ||
                    firstLeg.origin_airport.airport_code || 'UNK';
      }
      
      if (lastLeg.destination_airport) {
        destCode = lastLeg.destination_airport.iata_code || 
                  lastLeg.destination_airport.icao_code || 
                  lastLeg.destination_airport.code ||
                  lastLeg.destination_airport.airport_code || 'UNK';
      }
      
      // Format the route display
      if (trip.trip_lines.length === 1) {
        return `${originCode} → ${destCode}`;
      } else {
        return `${originCode} → ${destCode} (${trip.trip_lines.length} legs)`;
      }
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

    const deleteFewTrips = async () => {
      if (selectedIds.value.length === 0) return;
      
      const result = await Swal.fire({
        title: "Delete Trips",
        text: `Are you sure you want to delete ${selectedIds.value.length} trip(s)? This action cannot be undone.`,
        icon: "warning",
        showCancelButton: true,
        confirmButtonText: "Yes, delete them!",
        cancelButtonText: "Cancel",
        confirmButtonColor: "#d33"
      });
      
      if (result.isConfirmed) {
        try {
          loading.value = true;
          
          // Delete each selected trip via API
          for (const tripId of selectedIds.value) {
            await ApiService.delete(`/trips/${tripId}/`);
          }
          
          selectedIds.value.length = 0;
          
          Swal.fire({
            title: "Deleted!",
            text: "Selected trips have been deleted successfully.",
            icon: "success"
          }).then(() => {
            // Refresh the trips list
            fetchTrips(currentPage.value, pageSize.value, search.value, activeTab.value);
          });
        } catch (error) {
          console.error("Error deleting trips:", error);
          Swal.fire({
            title: "Error",
            text: "Failed to delete some trips. Please try again.",
            icon: "error"
          });
        } finally {
          loading.value = false;
        }
      }
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
      // Clear existing timeout
      if (searchTimeout.value) {
        clearTimeout(searchTimeout.value);
      }
      
      // Debounce search by 500ms
      searchTimeout.value = setTimeout(async () => {
        currentPage.value = 1; // Reset to first page when searching
        await fetchTrips(1, pageSize.value, search.value, activeTab.value);
        MenuComponent.reinitialization();
      }, 500);
    };
    
    const onPageChange = async (page: number) => {
      await fetchTrips(page, pageSize.value, search.value, activeTab.value);
      MenuComponent.reinitialization();
    };

    const onItemsPerPageChange = async (newPageSize: number) => {
      pageSize.value = newPageSize;
      currentPage.value = 1; // Reset to first page
      await fetchTrips(1, newPageSize, search.value, activeTab.value);
      setTimeout(() => {
        MenuComponent.reinitialization();
      }, 0);
    };

    // Navigation methods
    const navigateToTrip = (tripId: string) => {
      router.push(`/admin/trips/${tripId}`);
    };

    const navigateToPatient = (patient: any) => {
      if (patient && patient.id) {
        // Navigate to the patient details using patient ID
        router.push(`/admin/contacts/patients/${patient.id}`);
      } else {
        // Fallback to patients list page
        router.push('/admin/patients');
      }
    };

    const navigateToAircraft = (aircraftId: string) => {
      const url = router.resolve(`/admin/aircraft/${aircraftId}`).href;
      window.open(url, '_blank');
    };

    // New action methods

    // Handle tab change
    const handleTabChange = async (tab: string) => {
      activeTab.value = tab;
      currentPage.value = 1; // Reset to first page when changing tabs
      await fetchTrips(1, pageSize.value, search.value, tab);
    };

    // Handle trip created event from modal
    const onTripCreated = async (newTrip: Trip) => {
      console.log('New trip created:', newTrip);
      // Refresh the trips list
      await fetchTrips(1, pageSize.value, search.value, activeTab.value);
    };

    onMounted(async () => {
      await fetchTrips(1, pageSize.value, '', 'all');
      // Initialize menu components
      setTimeout(() => {
        MenuComponent.reinitialization();
      }, 200);

      // Setup toolbar actions for trips page
      setToolbarActions([
        createToolbarActions.primary('add-trip', 'Create Trip', openMultiStepTripModal, 'plus'),
        createToolbarActions.secondary('add-simple-trip', 'Quick Trip', openCreateTripModal, 'rocket')
      ]);
    });
    
    onUnmounted(() => {
      // Clear search timeout
      if (searchTimeout.value) {
        clearTimeout(searchTimeout.value);
      }
    });

    return {
      search,
      searchItems,
      trips,
      filteredTrips,
      activeTab,
      headerConfig,
      loading,
      error,
      totalItems,
      currentPage,
      pageSize,
      sort,
      onItemSelect,
      selectedIds,
      deleteFewTrips,
      deleteTrip,
      onItemsPerPageChange,
      onPageChange,
      openCreateTripModal,
      openMultiStepTripModal,
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
      getAllTripsCount,
      getStatusCount,
      handleTabChange,
      navigateToTrip,
      navigateToPatient,
      navigateToAircraft,
      onTripCreated,
    };
  },
});
</script>