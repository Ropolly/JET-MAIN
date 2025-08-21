<template>
  <div>
    <!-- All Trips Card -->
    <div class="card mb-6 mb-xl-9">
      <!--begin::Card header-->
      <div class="card-header border-0">
        <div class="card-title">
          <h3 class="fw-bold m-0">Trip History</h3>
        </div>
        <div class="card-toolbar">
          <div class="d-flex gap-2">
            <button class="btn btn-sm btn-light">Export</button>
            <button class="btn btn-sm btn-primary">Book New Trip</button>
          </div>
        </div>
      </div>
      <!--end::Card header-->

      <!--begin::Card body-->
      <div class="card-body pt-2">
        <!--begin::Search-->
        <div class="d-flex align-items-center mb-6">
          <div class="position-relative w-md-400px me-md-2">
            <KTIcon
              icon-name="magnifier"
              icon-class="fs-3 text-gray-500 position-absolute top-50 translate-middle ms-6"
            />
            <input
              type="text"
              class="form-control form-control-solid ps-10"
              placeholder="Search trips..."
              v-model="searchTerm"
            />
          </div>
          <button class="btn btn-light btn-active-light-primary" @click="searchTrips">
            Search
          </button>
        </div>
        <!--end::Search-->

        <!--begin::Table wrapper-->
        <div class="table-responsive">
          <table class="table table-row-dashed align-middle gs-0 gy-4 my-0">
            <thead>
              <tr class="fs-7 fw-bold text-gray-500 border-bottom-0">
                <th class="ps-0 min-w-200px">Trip Details</th>
                <th class="min-w-140px">Date & Time</th>
                <th class="min-w-120px">Route</th>
                <th class="min-w-100px">Aircraft</th>
                <th class="min-w-100px">Status</th>
                <th class="min-w-100px text-end">Amount</th>
                <th class="min-w-70px text-end">Actions</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="trip in paginatedTrips" :key="trip.id">
                <td class="ps-0">
                  <div class="d-flex align-items-center">
                    <div class="symbol symbol-45px me-2">
                      <div :class="`symbol-label bg-light-${getTripTypeColor(trip.type)}`">
                        <KTIcon 
                          :icon-name="getTripTypeIcon(trip.type)" 
                          :icon-class="`fs-3 text-${getTripTypeColor(trip.type)}`" 
                        />
                      </div>
                    </div>
                    <div class="d-flex flex-column">
                      <a 
                        href="#" 
                        class="text-gray-800 text-hover-primary fw-bold fs-6"
                        @click="viewTrip(trip.id)"
                      >
                        {{ trip.trip_number }}
                      </a>
                      <span class="text-gray-600 fw-semibold fs-7">{{ trip.type }}</span>
                    </div>
                  </div>
                </td>
                <td>
                  <div class="d-flex flex-column">
                    <span class="text-gray-800 fw-bold fs-6">{{ formatDate(trip.departure_time) }}</span>
                    <span class="text-gray-600 fs-7">{{ formatTime(trip.departure_time) }}</span>
                  </div>
                </td>
                <td>
                  <div class="d-flex flex-column">
                    <span class="text-gray-800 fw-bold fs-6">{{ getRoute(trip) }}</span>
                    <span class="text-gray-600 fs-7">{{ getDuration(trip) }}</span>
                  </div>
                </td>
                <td>
                  <div class="d-flex flex-column">
                    <span class="text-gray-800 fw-bold fs-6">{{ trip.aircraft?.tail_number || 'TBD' }}</span>
                    <span class="text-gray-600 fs-7">{{ trip.aircraft?.model || 'Not assigned' }}</span>
                  </div>
                </td>
                <td>
                  <span :class="`badge badge-light-${getStatusColor(trip.status)} fs-7`">
                    {{ trip.status }}
                  </span>
                </td>
                <td class="text-end">
                  <span class="text-gray-800 fw-bold fs-6">${{ formatAmount(trip.total_amount) }}</span>
                </td>
                <td class="text-end">
                  <div class="dropdown">
                    <button 
                      class="btn btn-sm btn-light btn-active-light-primary" 
                      type="button" 
                      data-bs-toggle="dropdown"
                    >
                      <KTIcon icon-name="dots-horizontal" icon-class="fs-3" />
                    </button>
                    <ul class="dropdown-menu">
                      <li>
                        <a class="dropdown-item" href="#" @click="viewTrip(trip.id)">View Details</a>
                      </li>
                      <li>
                        <a class="dropdown-item" href="#" @click="editTrip(trip.id)">Edit Trip</a>
                      </li>
                      <li>
                        <a class="dropdown-item" href="#" @click="duplicateTrip(trip.id)">Duplicate</a>
                      </li>
                      <li><hr class="dropdown-divider"></li>
                      <li>
                        <a class="dropdown-item text-danger" href="#" @click="cancelTrip(trip.id)">Cancel</a>
                      </li>
                    </ul>
                  </div>
                </td>
              </tr>
              <tr v-if="trips.length === 0 && !loading">
                <td colspan="7" class="text-center text-muted py-6">
                  No trips found for this contact
                </td>
              </tr>
              <tr v-if="loading">
                <td colspan="7" class="text-center py-6">
                  <div class="spinner-border spinner-border-sm" role="status">
                    <span class="visually-hidden">Loading...</span>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
        <!--end::Table wrapper-->

        <!--begin::Pagination-->
        <div class="d-flex flex-stack flex-wrap pt-6" v-if="totalPages > 1">
          <div class="fs-6 fw-semibold text-gray-700">
            Showing {{ (currentPage - 1) * itemsPerPage + 1 }} to {{ Math.min(currentPage * itemsPerPage, trips.length) }} of {{ trips.length }} entries
          </div>
          <ul class="pagination">
            <li class="page-item previous" :class="{ disabled: currentPage === 1 }">
              <a href="#" class="page-link" @click.prevent="currentPage > 1 && (currentPage--)">
                <i class="previous"></i>
              </a>
            </li>
            <li 
              v-for="page in visiblePages" 
              :key="page" 
              class="page-item" 
              :class="{ active: page === currentPage }"
            >
              <a href="#" class="page-link" @click.prevent="currentPage = page">{{ page }}</a>
            </li>
            <li class="page-item next" :class="{ disabled: currentPage === totalPages }">
              <a href="#" class="page-link" @click.prevent="currentPage < totalPages && (currentPage++)">
                <i class="next"></i>
              </a>
            </li>
          </ul>
        </div>
        <!--end::Pagination-->
      </div>
      <!--end::Card body-->
    </div>
    <!--end::All Trips Card-->

    <!-- Trip Statistics Card -->
    <div class="card mb-6 mb-xl-9">
      <!--begin::Card header-->
      <div class="card-header border-0">
        <div class="card-title">
          <h3 class="fw-bold m-0">Trip Statistics</h3>
        </div>
      </div>
      <!--end::Card header-->

      <!--begin::Card body-->
      <div class="card-body pt-2">
        <div class="row g-6">
          <!--begin::Col-->
          <div class="col-sm-6 col-xl-3">
            <div class="border border-dashed border-gray-300 text-center min-w-125px rounded py-4 px-3">
              <span class="fs-6 fw-semibold text-gray-700 d-block mb-2">Total Trips</span>
              <div class="fs-2 fw-bold text-gray-800">{{ getTotalTrips() }}</div>
            </div>
          </div>
          <!--end::Col-->

          <!--begin::Col-->
          <div class="col-sm-6 col-xl-3">
            <div class="border border-dashed border-gray-300 text-center min-w-125px rounded py-4 px-3">
              <span class="fs-6 fw-semibold text-gray-700 d-block mb-2">Completed</span>
              <div class="fs-2 fw-bold text-success">{{ getCompletedTrips() }}</div>
            </div>
          </div>
          <!--end::Col-->

          <!--begin::Col-->
          <div class="col-sm-6 col-xl-3">
            <div class="border border-dashed border-gray-300 text-center min-w-125px rounded py-4 px-3">
              <span class="fs-6 fw-semibold text-gray-700 d-block mb-2">Total Miles</span>
              <div class="fs-2 fw-bold text-primary">{{ getTotalMiles() }}</div>
            </div>
          </div>
          <!--end::Col-->

          <!--begin::Col-->
          <div class="col-sm-6 col-xl-3">
            <div class="border border-dashed border-gray-300 text-center min-w-125px rounded py-4 px-3">
              <span class="fs-6 fw-semibold text-gray-700 d-block mb-2">Avg Trip Cost</span>
              <div class="fs-2 fw-bold text-info">${{ getAverageTripCost() }}</div>
            </div>
          </div>
          <!--end::Col-->
        </div>
      </div>
      <!--end::Card body-->
    </div>
    <!--end::Trip Statistics Card-->
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from "vue";
import ApiService from "@/core/services/ApiService";
import Swal from "sweetalert2";

interface Props {
  contact: any;
  loading: boolean;
}

const props = defineProps<Props>();

const trips = ref<any[]>([]);
const searchTerm = ref('');
const currentPage = ref(1);
const itemsPerPage = 10;

const fetchTrips = async () => {
  if (!props.contact?.id) return;
  
  try {
    const response = await ApiService.get(`/trips/?${getContactFilterParam()}=${props.contact.id}`);
    trips.value = response.data.results || response.data || [];
  } catch (error) {
    console.error('Error fetching trips:', error);
  }
};

const getContactFilterParam = (): string => {
  switch (props.contact?.type) {
    case 'patients': return 'patient_id';
    case 'customers': return 'customer_id';
    default: return 'contact_id';
  }
};

const filteredTrips = computed(() => {
  if (!searchTerm.value) return trips.value;
  
  return trips.value.filter(trip => 
    trip.trip_number?.toLowerCase().includes(searchTerm.value.toLowerCase()) ||
    trip.departure_airport?.toLowerCase().includes(searchTerm.value.toLowerCase()) ||
    trip.arrival_airport?.toLowerCase().includes(searchTerm.value.toLowerCase()) ||
    trip.aircraft?.tail_number?.toLowerCase().includes(searchTerm.value.toLowerCase())
  );
});

const totalPages = computed(() => Math.ceil(filteredTrips.value.length / itemsPerPage));

const paginatedTrips = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage;
  const end = start + itemsPerPage;
  return filteredTrips.value.slice(start, end);
});

const visiblePages = computed(() => {
  const pages = [];
  const startPage = Math.max(1, currentPage.value - 2);
  const endPage = Math.min(totalPages.value, currentPage.value + 2);
  
  for (let i = startPage; i <= endPage; i++) {
    pages.push(i);
  }
  return pages;
});

const searchTrips = () => {
  currentPage.value = 1;
};

const formatDate = (dateString?: string): string => {
  if (!dateString) return 'TBD';
  return new Date(dateString).toLocaleDateString('en-US', {
    month: 'short',
    day: 'numeric',
    year: 'numeric',
  });
};

const formatTime = (dateString?: string): string => {
  if (!dateString) return '';
  return new Date(dateString).toLocaleTimeString('en-US', {
    hour: 'numeric',
    minute: '2-digit',
    hour12: true,
  });
};

const getRoute = (trip: any): string => {
  if (trip.departure_airport && trip.arrival_airport) {
    return `${trip.departure_airport} → ${trip.arrival_airport}`;
  }
  return 'Route TBD';
};

const getDuration = (trip: any): string => {
  if (trip.departure_time && trip.arrival_time) {
    const departure = new Date(trip.departure_time);
    const arrival = new Date(trip.arrival_time);
    const durationMs = arrival.getTime() - departure.getTime();
    const hours = Math.floor(durationMs / (1000 * 60 * 60));
    const minutes = Math.floor((durationMs % (1000 * 60 * 60)) / (1000 * 60));
    return `${hours}h ${minutes}m`;
  }
  return 'Duration TBD';
};

const getTripTypeIcon = (type: string): string => {
  switch (type?.toLowerCase()) {
    case 'medical': return 'cross';
    case 'emergency': return 'flash';
    case 'transport': return 'airplane';
    default: return 'airplane';
  }
};

const getTripTypeColor = (type: string): string => {
  switch (type?.toLowerCase()) {
    case 'medical': return 'danger';
    case 'emergency': return 'warning';
    case 'transport': return 'primary';
    default: return 'primary';
  }
};

const getStatusColor = (status: string): string => {
  switch (status?.toLowerCase()) {
    case 'completed': return 'success';
    case 'active': case 'in_progress': return 'primary';
    case 'cancelled': return 'danger';
    case 'pending': return 'warning';
    default: return 'secondary';
  }
};

const formatAmount = (amount?: number): string => {
  if (!amount) return '0';
  return amount.toLocaleString();
};

const getTotalTrips = (): string => {
  return trips.value.length.toString();
};

const getCompletedTrips = (): string => {
  return trips.value.filter(trip => trip.status?.toLowerCase() === 'completed').length.toString();
};

const getTotalMiles = (): string => {
  const totalMiles = trips.value.reduce((sum, trip) => sum + (trip.distance || 0), 0);
  return totalMiles.toLocaleString();
};

const getAverageTripCost = (): string => {
  const totalCost = trips.value.reduce((sum, trip) => sum + (trip.total_amount || 0), 0);
  const avgCost = trips.value.length > 0 ? totalCost / trips.value.length : 0;
  return avgCost.toLocaleString();
};

const viewTrip = (tripId: string) => {
  Swal.fire({
    title: 'Navigate to Trip',
    text: `Would navigate to trip details for ID: ${tripId}`,
    icon: 'info'
  });
};

const editTrip = (tripId: string) => {
  Swal.fire({
    title: 'Edit Trip',
    text: `Would open edit form for trip ID: ${tripId}`,
    icon: 'info'
  });
};

const duplicateTrip = (tripId: string) => {
  Swal.fire({
    title: 'Duplicate Trip',
    text: `Would create a copy of trip ID: ${tripId}`,
    icon: 'info'
  });
};

const cancelTrip = (tripId: string) => {
  Swal.fire({
    title: 'Cancel Trip',
    text: `Are you sure you want to cancel trip ID: ${tripId}?`,
    icon: 'warning',
    showCancelButton: true,
    confirmButtonText: 'Yes, cancel it!'
  }).then((result) => {
    if (result.isConfirmed) {
      Swal.fire('Cancelled!', 'The trip has been cancelled.', 'success');
    }
  });
};

onMounted(() => {
  if (props.contact?.id) {
    fetchTrips();
  }
});
</script>