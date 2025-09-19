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
            placeholder="Search Airports"
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
            @click="deleteFewAirports()"
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
        :data="airports"
        :header="headerConfig"
        :checkbox-enabled="true"
        :loading="loading"
        :total="totalItems"
        :current-page="currentPage"
        :items-per-page="pageSize"
      >
        <template v-slot:airport="{ row: airport }">
          <div class="d-flex align-items-center">
            <div class="symbol symbol-circle symbol-50px overflow-hidden me-3">
              <div class="symbol-label bg-light-primary">
                <i class="ki-duotone ki-geolocation fs-2x text-primary">
                  <span class="path1"></span>
                  <span class="path2"></span>
                </i>
              </div>
            </div>
            <div class="d-flex flex-column">
              <a href="#" @click="handleView(airport)" class="text-gray-800 text-hover-primary mb-1 fs-6 fw-bold">
                {{ airport.name || 'Unnamed Airport' }}
              </a>
              <span class="text-muted fs-7">{{ getAirportCode(airport) }}</span>
            </div>
          </div>
        </template>

        <template v-slot:location="{ row: airport }">
          <div class="d-flex flex-column">
            <span class="text-dark fw-semibold fs-6">
              {{ formatLocation(airport) }}
            </span>
            <span class="text-muted fs-7">{{ airport.iso_country }}</span>
          </div>
        </template>

        <template v-slot:codes="{ row: airport }">
          <div class="d-flex flex-column">
            <span class="text-dark fw-semibold fs-6">
              IATA: {{ airport.iata_code || 'N/A' }}
            </span>
            <span class="text-muted fs-7">ICAO: {{ airport.icao_code || 'N/A' }}</span>
          </div>
        </template>

        <template v-slot:elevation="{ row: airport }">
          <span class="text-dark fw-semibold">
            {{ formatElevation(airport.elevation) }}
          </span>
        </template>

        <template v-slot:services="{ row: airport }">
          <div class="d-flex flex-column">
            <span class="text-dark fw-semibold fs-6">
              FBOs: {{ airport.fbos_count || 0 }}
            </span>
            <span class="text-muted fs-7">Grounds: {{ airport.grounds_count || 0 }}</span>
          </div>
        </template>

        <template v-slot:actions="{ row: airport }">
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
              <a @click="handleEdit(airport)" class="menu-link px-3"
                >Edit Airport</a
              >
            </div>
            <!--end::Menu item-->
            <!--begin::Menu item-->
            <div class="menu-item px-3">
              <a @click="handleManageGrounds(airport)" class="menu-link px-3"
                >Manage Grounds</a
              >
            </div>
            <!--end::Menu item-->
            <div class="separator mt-3 opacity-75"></div>
            <!--begin::Menu item-->
            <div class="menu-item px-3">
              <a @click="handleDelete(airport)" class="menu-link px-3 text-danger"
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

  <!-- Create Airport Modal -->
  <CreateAirportModal @airport-created="onAirportCreated" />
</template>

<script lang="ts">
import { defineComponent, ref, onMounted, onUnmounted, nextTick } from "vue";
import { useRouter } from "vue-router";
import ApiService from "@/core/services/ApiService";
import KTDatatable from "@/components/kt-datatable/KTDataTable.vue";
import CreateAirportModal from "@/components/modals/CreateAirportModal.vue";
import type { Sort } from "@/components/kt-datatable/table-partials/models";
import arraySort from "array-sort";
import { MenuComponent } from "@/assets/ts/components";
import { Modal } from "bootstrap";
import Swal from "sweetalert2";
import { useToolbarStore } from "@/stores/toolbar";

interface Airport {
  id: string;
  ident: string;
  name: string;
  latitude: number;
  longitude: number;
  elevation?: number;
  iso_country: string;
  iso_region?: string;
  municipality?: string;
  icao_code?: string;
  iata_code?: string;
  local_code?: string;
  gps_code?: string;
  airport_type: string;
  timezone: string;
  fbos: string[];
  grounds: string[];
  fbos_count: number;
  grounds_count: number;
  created_on: string;
}

export default defineComponent({
  name: "airports-management",
  components: {
    KTDatatable,
    CreateAirportModal,
  },
  setup() {
    const router = useRouter();
    const toolbarStore = useToolbarStore();
    const airports = ref<Airport[]>([]);
    const loading = ref(false);
    const error = ref<string | null>(null);
    const totalItems = ref(0);
    const currentPage = ref(1);
    const pageSize = ref(25);

    const headerConfig = ref([
      {
        columnName: "Airport",
        columnLabel: "airport",
        sortEnabled: true,
      },
      {
        columnName: "Location",
        columnLabel: "location",
        sortEnabled: true,
      },
      {
        columnName: "Codes",
        columnLabel: "codes",
        sortEnabled: false,
      },
      {
        columnName: "Elevation",
        columnLabel: "elevation",
        sortEnabled: true,
      },
      {
        columnName: "Services",
        columnLabel: "services",
        sortEnabled: false,
      },
      {
        columnName: "Actions",
        columnLabel: "actions",
      },
    ]);

    const selectedIds = ref<Array<number>>([]);
    const search = ref<string>("");
    const searchTimeout = ref<NodeJS.Timeout | null>(null);

    // Methods
    const fetchAirports = async (page: number = 1, pageLimit: number = 25, searchQuery: string = '') => {
      try {
        loading.value = true;
        error.value = null;
        
        const params = new URLSearchParams();
        params.append('page', page.toString());
        params.append('page_size', pageLimit.toString());
        if (searchQuery.trim()) {
          params.append('search', searchQuery.trim());
        }
        
        const { data } = await ApiService.get(`/airports/?${params}`);
        airports.value = data.results || [];
        totalItems.value = data.count || 0;
        currentPage.value = page;
      } catch (err: any) {
        error.value = err.response?.data?.detail || "Failed to fetch airports";
        console.error("Error fetching airports:", err);
        airports.value = [];
        totalItems.value = 0;
      } finally {
        loading.value = false;
      }
    };

    const handleCreate = () => {
      const modalElement = document.getElementById('kt_modal_create_airport');
      if (modalElement) {
        const modal = new Modal(modalElement);
        modal.show();
      }
    };

    const handleEdit = (airport: Airport) => {
      console.log('Edit clicked for Airport:', airport);

      Swal.fire({
        title: `Edit Airport: ${airport.name}`,
        html: `
          <div class="text-start">
            <div class="row">
              <div class="col-lg-6">
                <h6 class="mb-3 fw-bold">Basic Information</h6>
                <div class="mb-3">
                  <label class="form-label fw-bold">Airport Name <span class="text-danger">*</span></label>
                  <input id="edit-name" class="form-control" value="${airport.name || ''}" required>
                </div>
                <div class="mb-3">
                  <label class="form-label fw-bold">Airport Identifier <span class="text-danger">*</span></label>
                  <input id="edit-ident" class="form-control" value="${airport.ident || ''}" maxlength="10" required>
                </div>
                <div class="mb-3">
                  <label class="form-label fw-bold">Airport Type <span class="text-danger">*</span></label>
                  <select id="edit-airport-type" class="form-select" required>
                    <option value="">Select airport type</option>
                    <option value="large_airport" ${airport.airport_type === 'large_airport' ? 'selected' : ''}>Large Airport</option>
                    <option value="medium_airport" ${airport.airport_type === 'medium_airport' ? 'selected' : ''}>Medium Airport</option>
                    <option value="small_airport" ${airport.airport_type === 'small_airport' ? 'selected' : ''}>Small Airport</option>
                  </select>
                </div>
                <div class="mb-3">
                  <label class="form-label fw-bold">Timezone <span class="text-danger">*</span></label>
                  <input id="edit-timezone" class="form-control" value="${airport.timezone || ''}" placeholder="e.g., America/New_York" required>
                </div>
              </div>
              <div class="col-lg-6">
                <h6 class="mb-3 fw-bold">Location Information</h6>
                <div class="row mb-3">
                  <div class="col-6">
                    <label class="form-label fw-bold">Latitude <span class="text-danger">*</span></label>
                    <input id="edit-latitude" class="form-control" type="number" step="0.000001" value="${airport.latitude || ''}" required>
                  </div>
                  <div class="col-6">
                    <label class="form-label fw-bold">Longitude <span class="text-danger">*</span></label>
                    <input id="edit-longitude" class="form-control" type="number" step="0.000001" value="${airport.longitude || ''}" required>
                  </div>
                </div>
                <div class="mb-3">
                  <label class="form-label fw-bold">Elevation (ft)</label>
                  <input id="edit-elevation" class="form-control" type="number" value="${airport.elevation || ''}">
                </div>
                <div class="mb-3">
                  <label class="form-label fw-bold">Country <span class="text-danger">*</span></label>
                  <input id="edit-country" class="form-control" value="${airport.iso_country || ''}" placeholder="e.g., US" required>
                </div>
                <div class="mb-3">
                  <label class="form-label fw-bold">Region/State</label>
                  <input id="edit-region" class="form-control" value="${airport.iso_region || ''}">
                </div>
                <div class="mb-3">
                  <label class="form-label fw-bold">Municipality/City</label>
                  <input id="edit-municipality" class="form-control" value="${airport.municipality || ''}">
                </div>
              </div>
            </div>
            <div class="row mt-3">
              <div class="col-lg-12">
                <h6 class="mb-3 fw-bold">Airport Codes</h6>
              </div>
              <div class="col-3">
                <div class="mb-3">
                  <label class="form-label fw-bold">ICAO Code</label>
                  <input id="edit-icao" class="form-control" value="${airport.icao_code || ''}" maxlength="4" placeholder="4-letter">
                </div>
              </div>
              <div class="col-3">
                <div class="mb-3">
                  <label class="form-label fw-bold">IATA Code</label>
                  <input id="edit-iata" class="form-control" value="${airport.iata_code || ''}" maxlength="3" placeholder="3-letter">
                </div>
              </div>
              <div class="col-3">
                <div class="mb-3">
                  <label class="form-label fw-bold">Local Code</label>
                  <input id="edit-local" class="form-control" value="${airport.local_code || ''}" maxlength="10">
                </div>
              </div>
              <div class="col-3">
                <div class="mb-3">
                  <label class="form-label fw-bold">GPS Code</label>
                  <input id="edit-gps" class="form-control" value="${airport.gps_code || ''}" maxlength="20">
                </div>
              </div>
            </div>
          </div>
        `,
        width: '800px',
        showCancelButton: true,
        confirmButtonText: 'Save Changes',
        cancelButtonText: 'Cancel',
        allowOutsideClick: false,
        allowEscapeKey: false,
        focusConfirm: false,
        preConfirm: () => {
          const name = (document.getElementById('edit-name') as HTMLInputElement)?.value?.trim();
          const ident = (document.getElementById('edit-ident') as HTMLInputElement)?.value?.trim();
          const latitude = (document.getElementById('edit-latitude') as HTMLInputElement)?.value;
          const longitude = (document.getElementById('edit-longitude') as HTMLInputElement)?.value;
          const country = (document.getElementById('edit-country') as HTMLInputElement)?.value?.trim();
          const airportType = (document.getElementById('edit-airport-type') as HTMLSelectElement)?.value;
          const timezone = (document.getElementById('edit-timezone') as HTMLInputElement)?.value?.trim();

          if (!name || !ident || !latitude || !longitude || !country || !airportType || !timezone) {
            Swal.showValidationMessage('Please fill in all required fields');
            return false;
          }

          return {
            name: name,
            ident: ident,
            latitude: parseFloat(latitude),
            longitude: parseFloat(longitude),
            elevation: (document.getElementById('edit-elevation') as HTMLInputElement)?.value ? parseFloat((document.getElementById('edit-elevation') as HTMLInputElement).value) : null,
            iso_country: country,
            iso_region: (document.getElementById('edit-region') as HTMLInputElement)?.value || '',
            municipality: (document.getElementById('edit-municipality') as HTMLInputElement)?.value || '',
            icao_code: (document.getElementById('edit-icao') as HTMLInputElement)?.value || '',
            iata_code: (document.getElementById('edit-iata') as HTMLInputElement)?.value || '',
            local_code: (document.getElementById('edit-local') as HTMLInputElement)?.value || '',
            gps_code: (document.getElementById('edit-gps') as HTMLInputElement)?.value || '',
            airport_type: airportType,
            timezone: timezone
          };
        }
      }).then(async (result) => {
        if (result.isConfirmed && result.value) {
          console.log('Saving Airport with data:', result.value);

          try {
            // Convert empty strings to null for optional fields
            const submitData = { ...result.value };
            Object.keys(submitData).forEach(key => {
              if (submitData[key] === '') {
                submitData[key] = null;
              }
            });

            await ApiService.put(`/airports/${airport.id}/`, submitData);

            Swal.fire({
              icon: 'success',
              title: 'Success!',
              text: 'Airport updated successfully.',
              timer: 2000,
              showConfirmButton: false
            });

            // Refresh the list
            await fetchAirports(currentPage.value, pageSize.value, search.value);
          } catch (error: any) {
            console.error('Error updating airport:', error);
            Swal.fire({
              icon: 'error',
              title: 'Error',
              text: error.response?.data?.detail || 'Failed to update airport.'
            });
          }
        }
      });
    };

    const handleView = (airport: Airport) => {
      Swal.fire({
        title: "Airport Details",
        html: `
          <div class="text-start">
            <p><strong>Name:</strong> ${airport.name}</p>
            <p><strong>Identifier:</strong> ${airport.ident}</p>
            <p><strong>Location:</strong> ${formatLocation(airport)}</p>
            <p><strong>Country:</strong> ${airport.iso_country}</p>
            <p><strong>IATA:</strong> ${airport.iata_code || 'N/A'}</p>
            <p><strong>ICAO:</strong> ${airport.icao_code || 'N/A'}</p>
            <p><strong>Type:</strong> ${formatAirportType(airport.airport_type)}</p>
            <p><strong>Elevation:</strong> ${formatElevation(airport.elevation)}</p>
            <p><strong>Coordinates:</strong> ${airport.latitude}, ${airport.longitude}</p>
            <p><strong>Timezone:</strong> ${airport.timezone}</p>
            <p><strong>Services:</strong> ${airport.fbos_count} FBOs, ${airport.grounds_count} Ground services</p>
          </div>
        `,
        icon: "info",
        confirmButtonText: "OK"
      });
    };

    const handleViewTrips = (airport: Airport) => {
      router.push(`/admin/trips?airport=${airport.id}`);
    };

    const handleManageFBOs = (airport: Airport) => {
      router.push(`/admin/fbos?airport=${airport.id}`);
    };

    const handleManageGrounds = (airport: Airport) => {
      router.push(`/admin/grounds?airport=${airport.id}`);
    };

    const handleDelete = async (airport: Airport) => {
      const result = await Swal.fire({
        title: "Delete Airport",
        text: `Are you sure you want to delete ${airport.name}?`,
        icon: "warning",
        showCancelButton: true,
        confirmButtonText: "Yes, delete it!",
        cancelButtonText: "Cancel"
      });
      
      if (result.isConfirmed) {
        try {
          await ApiService.delete(`/airports/${airport.id}/`);
          await fetchAirports(currentPage.value, pageSize.value, search.value); // Refresh the list
          Swal.fire("Deleted!", "Airport has been deleted.", "success");
        } catch (error: any) {
          console.error('Error deleting airport:', error);
          Swal.fire("Error!", "Failed to delete airport. Please try again.", "error");
        }
      }
    };

    const getAirportCode = (airport: Airport): string => {
      return airport.iata_code || airport.icao_code || 'No code';
    };

    const formatElevation = (elevation?: number): string => {
      if (!elevation && elevation !== 0) return 'Unknown';
      return `${elevation.toLocaleString()} ft`;
    };

    const formatLocation = (airport: Airport): string => {
      const parts = [];
      if (airport.municipality) parts.push(airport.municipality);
      if (airport.iso_region) parts.push(airport.iso_region);
      return parts.length > 0 ? parts.join(', ') : 'Unknown location';
    };

    const formatAirportType = (type: string): string => {
      const typeMap: Record<string, string> = {
        'large_airport': 'Large Airport',
        'medium_airport': 'Medium Airport', 
        'small_airport': 'Small Airport'
      };
      return typeMap[type] || type;
    };

    const deleteFewAirports = async () => {
      const result = await Swal.fire({
        title: "Delete Selected Airports",
        text: `Are you sure you want to delete ${selectedIds.value.length} airports?`,
        icon: "warning",
        showCancelButton: true,
        confirmButtonText: "Yes, delete them!",
        cancelButtonText: "Cancel"
      });
      
      if (result.isConfirmed) {
        try {
          // Delete each selected airport
          await Promise.all(
            selectedIds.value.map(id => ApiService.delete(`/airports/${id}/`))
          );
          
          // Refresh the list
          await fetchAirports(currentPage.value, pageSize.value, search.value);
          selectedIds.value = [];
          
          Swal.fire("Deleted!", "Selected airports have been deleted.", "success");
        } catch (error: any) {
          console.error('Error deleting airports:', error);
          Swal.fire("Error!", "Failed to delete some airports. Please try again.", "error");
        }
      }
    };

    const sort = async (sort: Sort) => {
      // For server-side sorting, we would need to implement ordering in the API call
      // For now, we'll do client-side sorting on the current page
      const reverse: boolean = sort.order === "asc";
      if (sort.label) {
        arraySort(airports.value, sort.label, { reverse });
      }
      await nextTick();
      MenuComponent.reinitialization();
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
        await fetchAirports(1, pageSize.value, search.value);
        await nextTick();
        MenuComponent.reinitialization();
      }, 500);
    };
    
    const onPageChange = async (page: number) => {
      await fetchAirports(page, pageSize.value, search.value);
      await nextTick();
      MenuComponent.reinitialization();
    };

    const onItemsPerPageChange = async (newPageSize: number) => {
      pageSize.value = newPageSize;
      currentPage.value = 1; // Reset to first page
      await fetchAirports(1, newPageSize, search.value);
      setTimeout(() => {
        MenuComponent.reinitialization();
      }, 0);
    };

    const onAirportCreated = async () => {
      // Refresh the airports list after creating a new one
      await fetchAirports(currentPage.value, pageSize.value, search.value);
    };

    onMounted(async () => {
      await fetchAirports(1, pageSize.value, '');
      // Ensure menus are properly initialized
      await nextTick();
      setTimeout(() => {
        MenuComponent.reinitialization();
      }, 100);
      
      // Set toolbar actions
      toolbarStore.setActions([
        {
          id: 'add-airport',
          label: 'Add Airport',
          icon: 'plus',
          variant: 'primary',
          handler: handleCreate
        }
      ]);
    });
    
    onUnmounted(() => {
      // Clear search timeout
      if (searchTimeout.value) {
        clearTimeout(searchTimeout.value);
      }
      // Clear toolbar actions
      toolbarStore.clearActions();
    });

    return {
      search,
      searchItems,
      airports,
      headerConfig,
      loading,
      error,
      totalItems,
      currentPage,
      pageSize,
      sort,
      onItemSelect,
      selectedIds,
      deleteFewAirports,
      onItemsPerPageChange,
      onPageChange,
      handleCreate,
      handleEdit,
      handleView,
      handleViewTrips,
      handleManageFBOs,
      handleManageGrounds,
      handleDelete,
      getAirportCode,
      formatElevation,
      formatLocation,
      formatAirportType,
      onAirportCreated,
    };
  },
});
</script>