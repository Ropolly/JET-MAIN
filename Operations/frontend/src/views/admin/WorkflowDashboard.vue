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
            placeholder="Search trips..."
          />
        </div>
        <!--end::Search-->
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
              href="#kt_tab_all_workflows"
            >
              All Workflows
              <span class="ms-1 badge" :class="activeTab === 'all' ? 'badge-secondary' : 'badge-light-secondary'">{{ getAllTripsCount() }}</span>
            </a>
          </li>
          <li class="nav-item" v-if="getStatusCount('active') > 0">
            <a
              class="nav-link"
              :class="{ active: activeTab === 'active' }"
              @click.prevent="handleTabChange('active')"
              data-bs-toggle="tab"
              href="#kt_tab_scheduled_workflows"
            >
              Scheduled
              <span class="ms-1 badge" :class="activeTab === 'active' ? 'badge-success' : 'badge-light-secondary'">{{ getStatusCount('active') }}</span>
            </a>
          </li>
          <li class="nav-item" v-if="getStatusCount('pending') > 0">
            <a
              class="nav-link"
              :class="{ active: activeTab === 'pending' }"
              @click.prevent="handleTabChange('pending')"
              data-bs-toggle="tab"
              href="#kt_tab_pending_workflows"
            >
              Pending
              <span class="ms-1 badge" :class="activeTab === 'pending' ? 'badge-warning' : 'badge-light-secondary'">{{ getStatusCount('pending') }}</span>
            </a>
          </li>
          <li class="nav-item" v-if="getStatusCount('completed') > 0">
            <a
              class="nav-link"
              :class="{ active: activeTab === 'completed' }"
              @click.prevent="handleTabChange('completed')"
              data-bs-toggle="tab"
              href="#kt_tab_completed_workflows"
            >
              Completed
              <span class="ms-1 badge" :class="activeTab === 'completed' ? 'badge-primary' : 'badge-light-secondary'">{{ getStatusCount('completed') }}</span>
            </a>
          </li>
          <li class="nav-item" v-if="getStatusCount('cancelled') > 0">
            <a
              class="nav-link"
              :class="{ active: activeTab === 'cancelled' }"
              @click.prevent="handleTabChange('cancelled')"
              data-bs-toggle="tab"
              href="#kt_tab_cancelled_workflows"
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
      <!--begin::Table-->
      <div class="table-responsive">
        <table class="table align-middle table-row-dashed fs-6 gy-5">
          <!--begin::Table head-->
          <thead>
            <tr class="text-start text-muted fw-bold fs-7 text-uppercase gs-0">
              <th class="min-w-175px">Trip</th>
              <th class="min-w-125px">Elements</th>
              <th class="min-w-100px">Status</th>
              <th class="min-w-125px">Crew</th>
              <th class="min-w-150px">Scheduled</th>
              <th class="text-end min-w-70px">Actions</th>
            </tr>
          </thead>
          <!--end::Table head-->

          <!--begin::Table body-->
          <tbody class="text-gray-600 fw-semibold">
            <tr v-if="loading">
              <td colspan="6" class="text-center py-10">
                <span class="spinner-border spinner-border-sm align-middle me-2"></span>
                Loading workflows...
              </td>
            </tr>
            <tr v-else-if="trips.length === 0">
              <td colspan="6" class="text-center py-10 text-muted">
                No workflows found
              </td>
            </tr>
            <tr v-for="trip in trips" :key="trip.trip_id" v-else>
              <!--begin::Trip info with flag-->
              <td class="min-w-175px">
                <div class="d-flex align-items-center">
                  <!--begin::Flag avatar-->
                  <div class="symbol symbol-circle symbol-35px me-3">
                    <img
                      v-if="getOriginCountryFlag(trip)"
                      :src="getOriginCountryFlag(trip)"
                      alt="Origin flag"
                    />
                    <div v-else class="symbol-label bg-light-primary">
                      <KTIcon icon-name="airplane-square" icon-class="fs-3 text-primary" />
                    </div>
                  </div>
                  <!--end::Flag avatar-->

                  <!--begin::Trip details-->
                  <div class="d-flex flex-column">
                    <a
                      :href="`/admin/trips/${trip.trip_id}/complete`"
                      class="text-gray-900 text-hover-primary fw-bold mb-1"
                    >
                      {{ trip.trip_number || 'DRAFT' }}
                    </a>
                    <div class="fs-7 text-muted fw-bold">
                      {{ getTripRoute(trip) }}
                    </div>
                  </div>
                  <!--end::Trip details-->
                </div>
              </td>
              <!--end::Trip info-->

              <!--begin::Elements-->
              <td>
                <!--begin::Icons-->
                <div class="d-flex gap-2 mb-2">
                  <!--Quote status-->
                  <span
                    :title="trip.has_quote ? 'Quote exists' : 'No quote'"
                    data-bs-toggle="tooltip"
                  >
                    <KTIcon
                      icon-name="price-tag"
                      :icon-class="`fs-2 ${trip.has_quote ? 'text-info' : 'text-gray-400'}`"
                    />
                  </span>

                  <!--Trip lines status-->
                  <span
                    :title="trip.has_trip_lines ? 'Trip lines exist' : 'No trip lines'"
                    data-bs-toggle="tooltip"
                  >
                    <KTIcon
                      icon-name="airplane"
                      :icon-class="`fs-2 ${trip.has_trip_lines ? 'text-primary' : 'text-gray-400'}`"
                    />
                  </span>

                  <!--Patient status-->
                  <span
                    :title="trip.has_patient ? 'Patient assigned' : 'No patient'"
                    data-bs-toggle="tooltip"
                  >
                    <KTIcon
                      icon-name="pulse"
                      :icon-class="`fs-2 ${trip.has_patient ? 'text-danger' : 'text-gray-400'}`"
                    />
                  </span>

                  <!--Payment status-->
                  <span
                    :title="getPaymentStatusTitle(trip.payment_status)"
                    data-bs-toggle="tooltip"
                  >
                    <KTIcon
                      icon-name="dollar"
                      :icon-class="`fs-2 ${getPaymentStatusClass(trip.payment_status)}`"
                    />
                  </span>
                </div>
                <!--end::Icons-->

                <div class="fs-7 text-muted fw-bold">{{ trip.trip_type || 'N/A' }}</div>
              </td>
              <!--end::Elements-->

              <!--begin::Status-->
              <td>
                <span
                  class="badge"
                  :class="getStatusBadgeClass(trip.trip_status)"
                >
                  {{ formatStatus(trip.trip_status) }}
                </span>
              </td>
              <!--end::Status-->

              <!--begin::Crew-->
              <td class="min-w-125px">
                <!--begin::Team members-->
                <div class="symbol-group symbol-hover mb-1">
                  <template v-if="getCrewMembers(trip).length > 0">
                    <div
                      v-for="(crew, idx) in getCrewMembers(trip).slice(0, 4)"
                      :key="idx"
                      class="symbol symbol-circle symbol-25px"
                      :title="crew.name + ' - ' + crew.role"
                      data-bs-toggle="tooltip"
                    >
                      <div class="symbol-label" :class="getCrewBadgeColor(crew.role)">
                        <span class="fs-7 text-white">{{ getCrewInitials(crew.name) }}</span>
                      </div>
                    </div>

                    <!--begin::More members-->
                    <div
                      v-if="getCrewMembers(trip).length > 4"
                      class="symbol symbol-circle symbol-25px"
                    >
                      <div class="symbol-label bg-dark">
                        <span class="fs-8 text-inverse-dark">+{{ getCrewMembers(trip).length - 4 }}</span>
                      </div>
                    </div>
                    <!--end::More members-->
                  </template>
                  <template v-else>
                    <div class="symbol symbol-circle symbol-25px">
                      <div class="symbol-label bg-light">
                        <span class="fs-7 text-muted">-</span>
                      </div>
                    </div>
                  </template>
                </div>
                <!--end::Team members-->

                <div class="fs-7 fw-bold text-muted">Crew Members</div>
              </td>
              <!--end::Crew-->

              <!--begin::Scheduled date-->
              <td class="min-w-150px">
                <div class="mb-2 fw-bold">
                  {{ formatScheduledDate(trip.departure_datetime) }}
                </div>
                <div class="fs-7 fw-bold text-muted">Departure</div>
              </td>
              <!--end::Scheduled date-->

              <!--begin::Actions-->
              <td class="text-end">
                <a
                  :href="`/admin/trips/${trip.trip_id}/complete`"
                  class="btn btn-icon btn-light btn-sm border-0"
                >
                  <KTIcon icon-name="arrow-right" icon-class="fs-2 text-dark" />
                </a>
              </td>
              <!--end::Actions-->
            </tr>
          </tbody>
          <!--end::Table body-->
        </table>
      </div>
      <!--end::Table-->

      <!--begin::Pagination-->
      <div v-if="totalItems > 0" class="row pt-10">
        <!--begin::Items count-->
        <div class="col-sm-12 col-md-5 d-flex align-items-center justify-content-center justify-content-md-start">
          <span class="text-gray-700 fw-semibold">
            Showing {{ totalItems }} entries
          </span>
        </div>
        <!--end::Items count-->

        <!--begin::Pagination info and controls-->
        <div class="col-sm-12 col-md-7 d-flex align-items-center justify-content-center justify-content-md-end">
          <div class="dataTables_paginate paging_simple_numbers">
            <ul class="pagination">
          <li class="page-item" :class="{ disabled: currentPage === 1 }">
            <a @click.prevent="fetchTrips(currentPage - 1)" href="#" class="page-link">
              <KTIcon icon-name="left" icon-class="fs-5" />
            </a>
          </li>
          <li
            v-for="page in totalPages"
            :key="page"
            class="page-item"
            :class="{ active: page === currentPage }"
          >
            <a @click.prevent="fetchTrips(page)" href="#" class="page-link">
              {{ page }}
            </a>
          </li>
          <li class="page-item" :class="{ disabled: currentPage === totalPages }">
            <a @click.prevent="fetchTrips(currentPage + 1)" href="#" class="page-link">
              <KTIcon icon-name="right" icon-class="fs-5" />
            </a>
          </li>
        </ul>
          </div>
        </div>
        <!--end::Pagination info and controls-->
      </div>
      <!--end::Pagination-->
    </div>
    <!--end::Card body-->
  </div>
  <!--end::Card-->
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted, watch } from "vue";
import { useToolbarStore } from "@/stores/toolbar";
import ApiService from "@/core/services/ApiService";
import Swal from "sweetalert2";
import { MenuComponent } from "@/assets/ts/components";

// Toolbar
const toolbarStore = useToolbarStore();

// State
const trips = ref<any[]>([]);
const loading = ref(false);
const search = ref("");
const currentPage = ref(1);
const totalItems = ref(0);
const itemsPerPage = ref(25);
const isMounted = ref(false);
const activeTab = ref<string>("all");
const statusCounts = ref<Record<string, number>>({
  all: 0,
  pending: 0,
  active: 0,
  completed: 0,
  cancelled: 0,
});

// Watch for itemsPerPage changes (only after component is mounted)
watch(itemsPerPage, (newValue, oldValue) => {
  if (!isMounted.value) return; // Don't run on initial mount

  console.log('Items per page changed from', oldValue, 'to', newValue);
  currentPage.value = 1;
  fetchTrips(1);
});

// Computed
const totalPages = computed(() => Math.ceil(totalItems.value / itemsPerPage.value));

// Helper functions for status counts
const getAllTripsCount = () => {
  return statusCounts.value.all;
};

const getStatusCount = (status: string) => {
  return statusCounts.value[status] || 0;
};

// Methods
const fetchTrips = async (page = 1) => {
  loading.value = true;
  try {
    const params = new URLSearchParams();
    params.append("page", page.toString());
    params.append("page_size", itemsPerPage.value.toString());

    if (search.value.trim()) {
      params.append("search", search.value.trim());
      console.log('🔍 Searching with term:', search.value.trim());
    } else {
      // Only add status filter if not searching and not showing all
      if (activeTab.value !== 'all') {
        params.append("status", activeTab.value);
        console.log('📑 Filtering by status:', activeTab.value);
      }
    }

    const url = `/workflows?${params}`;
    console.log('📡 Fetching from:', url);
    console.log('📦 Full URL will be:', `${import.meta.env.VITE_APP_API_URL || 'http://localhost:8001/api'}${url}`);
    console.log('🔗 Params object:', Object.fromEntries(params));

    // Use the new optimized workflows endpoint
    const { data } = await ApiService.get(url);

    console.log('✅ Workflow API response:', data);
    console.log('📊 Results count:', data.results?.length);
    console.log('📋 Results:', data.results);

    trips.value = data.results || [];
    totalItems.value = data.count || 0;
    currentPage.value = page;

    console.log('💾 trips.value set to:', trips.value.length, 'items');

    // Fetch status counts - pass the count if searching to avoid redundant API call
    if (search.value.trim()) {
      await fetchStatusCounts(data.count || 0);
    } else {
      await fetchStatusCounts();
    }
  } catch (err: any) {
    console.error("Error fetching workflows:", err);
    Swal.fire({
      text: err.response?.data?.detail || "Failed to fetch workflows",
      icon: "error",
      buttonsStyling: false,
      confirmButtonText: "Ok",
      customClass: {
        confirmButton: "btn btn-primary",
      },
    });
    trips.value = [];
    totalItems.value = 0;
  } finally {
    loading.value = false;
    // Reinitialize menu components
    setTimeout(() => {
      MenuComponent.reinitialization();
    }, 100);
  }
};

const fetchStatusCounts = async (searchCount?: number) => {
  try {
    // If we're searching and already have the count from fetchTrips, use it
    if (search.value.trim() && searchCount !== undefined) {
      statusCounts.value.all = searchCount;
      // When searching, set all status counts to 0 since we're showing all results
      statusCounts.value.pending = 0;
      statusCounts.value.active = 0;
      statusCounts.value.completed = 0;
      statusCounts.value.cancelled = 0;
      return;
    }

    // Only fetch status-specific counts if not searching
    if (!search.value.trim()) {
      // Fetch all count first
      const allParams = new URLSearchParams();
      allParams.append("page_size", "1");
      const allResponse = await ApiService.get(`/workflows?${allParams}`);
      statusCounts.value.all = allResponse.data.count || 0;

      // Fetch counts for each valid trip status
      const statuses = ['pending', 'active', 'completed', 'cancelled'];
      for (const status of statuses) {
        const statusParams = new URLSearchParams();
        statusParams.append("status", status);
        statusParams.append("page_size", "1");
        const response = await ApiService.get(`/workflows?${statusParams}`);
        statusCounts.value[status] = response.data.count || 0;
      }
    }
  } catch (error) {
    console.error('Error fetching status counts:', error);
  }
};

const handleTabChange = async (tab: string) => {
  activeTab.value = tab;
  currentPage.value = 1;
  await fetchTrips(1);
};

let searchTimeout: number | null = null;
const searchItems = () => {
  if (searchTimeout) clearTimeout(searchTimeout);
  searchTimeout = setTimeout(() => {
    fetchTrips(1);
  }, 300);
};

const deleteTrip = async (id: string) => {
  const result = await Swal.fire({
    text: "Are you sure you want to delete this trip?",
    icon: "warning",
    showCancelButton: true,
    buttonsStyling: false,
    confirmButtonText: "Yes, delete it!",
    cancelButtonText: "No, cancel",
    customClass: {
      confirmButton: "btn btn-danger",
      cancelButton: "btn btn-active-light",
    },
  });

  if (result.isConfirmed) {
    try {
      await ApiService.delete(`/trips/${id}`);
      Swal.fire({
        text: "Trip deleted successfully!",
        icon: "success",
        buttonsStyling: false,
        confirmButtonText: "Ok",
        customClass: {
          confirmButton: "btn btn-primary",
        },
      });
      fetchTrips(currentPage.value);
    } catch (err: any) {
      Swal.fire({
        text: err.response?.data?.detail || "Failed to delete trip",
        icon: "error",
        buttonsStyling: false,
        confirmButtonText: "Ok",
        customClass: {
          confirmButton: "btn btn-primary",
        },
      });
    }
  }
};

// Helper functions - now using pre-computed fields from API
const getOriginCountryFlag = (trip: any): string | null => {
  if (!trip.origin_flag || !trip.origin_flag.country) return null;

  // Map country codes to flag file names
  const countryMap: Record<string, string> = {
    'us': 'united-states',
    'gb': 'united-kingdom',
    'ca': 'canada',
    'mx': 'mexico',
    'fr': 'france',
    'de': 'germany',
    'it': 'italy',
    'es': 'spain',
    'br': 'brazil',
    'ar': 'argentina',
    'jp': 'japan',
    'cn': 'china',
    'in': 'india',
    'au': 'australia',
    'nz': 'new-zealand',
    'tt': 'trinidad-and-tobago',
    'ru': 'russia',
    'kr': 'south-korea',
    'za': 'south-africa',
    // Add more as needed
  };

  const countryCode = trip.origin_flag.country.toLowerCase();
  const flagName = countryMap[countryCode] || countryCode;
  return `/media/flags/${flagName}.svg`;
};

const getTripRoute = (trip: any): string => {
  // Route is pre-computed by the API
  return trip.route || "TBD";
};

const getStatusBadgeClass = (status: string): string => {
  const statusMap: Record<string, string> = {
    'active': 'badge-success',
    'pending': 'badge-warning',
    'completed': 'badge-primary',
    'cancelled': 'badge-secondary',
  };
  return statusMap[status] || 'badge-light';
};

const formatStatus = (status: string): string => {
  if (!status) return 'N/A';
  return status.charAt(0).toUpperCase() + status.slice(1);
};

const getPaymentStatusClass = (paymentStatus: string): string => {
  const statusMap: Record<string, string> = {
    'paid': 'text-success',
    'partial': 'text-warning',
    'pending': 'text-gray-400',
  };
  return statusMap[paymentStatus] || 'text-gray-400';
};

const getPaymentStatusTitle = (paymentStatus: string): string => {
  const titleMap: Record<string, string> = {
    'paid': 'Paid in full',
    'partial': 'Partially paid',
    'pending': 'Payment pending',
  };
  return titleMap[paymentStatus] || 'No payment';
};

const getCrewMembers = (trip: any): Array<{ name: string; role: string }> => {
  // Crew members are pre-computed by the API
  return trip.crew_members || [];
};

const getCrewInitials = (name: string): string => {
  if (!name) return '?';
  const parts = name.trim().split(' ');
  if (parts.length >= 2) {
    return (parts[0][0] + parts[1][0]).toUpperCase();
  }
  return name.substring(0, 2).toUpperCase();
};

const getCrewBadgeColor = (role: string): string => {
  const roleMap: Record<string, string> = {
    'PIC': 'bg-primary',
    'SIC': 'bg-info',
    'Medical': 'bg-danger',
  };
  return roleMap[role] || 'bg-secondary';
};

const formatScheduledDate = (dateStr: string): string => {
  if (!dateStr || dateStr === 'TBD') return 'TBD';

  const date = new Date(dateStr);
  // Check if date is valid
  if (isNaN(date.getTime())) return 'TBD';

  const options: Intl.DateTimeFormatOptions = {
    month: 'short',
    day: 'numeric',
    year: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
  };

  return date.toLocaleDateString('en-US', options);
};

// Lifecycle
onMounted(() => {
  // Set mounted flag before first fetch to prevent watcher from firing
  isMounted.value = true;
  fetchTrips(1);

  // Set toolbar actions
  toolbarStore.setActions([
    {
      id: 'new-workflow',
      label: 'New Workflow',
      icon: 'plus',
      variant: 'primary',
      handler: () => {
        window.location.href = '/#/dashboard';
        setTimeout(() => {
          const newWorkflowBtn = document.querySelector('[data-action="new-workflow"]') as HTMLElement;
          if (newWorkflowBtn) {
            newWorkflowBtn.click();
          }
        }, 100);
      }
    }
  ]);
});

onUnmounted(() => {
  // Clear toolbar actions when component is destroyed
  toolbarStore.clearActions();
});
</script>

<style scoped>
.table-responsive {
  overflow-x: auto;
}
</style>