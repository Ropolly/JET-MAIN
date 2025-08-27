<template>
  <div>
    <!-- Pending Trips Card -->
    <div class="card mb-6 mb-xl-9">
      <!--begin::Card header-->
      <div class="card-header border-0">
        <div class="card-title">
          <h3 class="fw-bold m-0">Pending Trips</h3>
        </div>
        <div class="card-toolbar">
          <button @click="viewAllTrips" class="btn btn-sm btn-light">View All</button>
        </div>
      </div>
      <!--end::Card header-->

      <!--begin::Card body-->
      <div class="card-body pt-2">
        <div class="table-responsive">
          <table class="table table-row-dashed align-middle gs-0 gy-4 my-0">
            <thead>
              <tr class="fs-7 fw-bold text-gray-500 border-bottom-0">
                <th class="ps-0 min-w-200px">Trip</th>
                <th class="min-w-100px">Date</th>
                <th class="min-w-100px">Route</th>
                <th class="min-w-100px">Status</th>
                <th class="min-w-100px text-end">Amount</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="trip in pendingTrips" :key="trip.id">
                <td class="ps-0">
                  <div class="d-flex align-items-center">
                    <div class="symbol symbol-45px me-2">
                      <img :src="getAircraftImage(trip)" :alt="getAircraftModel(trip)" class="symbol-label object-fit-cover" style="width: 45px; height: 45px; border-radius: 8px;" />
                    </div>
                    <div class="d-flex flex-column">
                      <a @click.prevent="viewTrip(trip)" href="#" class="text-gray-800 text-hover-primary fw-bold fs-6">
                        {{ trip.trip_number }}
                      </a>
                      <span class="text-gray-600 fw-semibold fs-7">{{ trip.type }}</span>
                    </div>
                  </div>
                </td>
                <td>
                  <span class="text-gray-800 fw-bold fs-6">{{ formatDate(trip.departure_time || trip.scheduled_departure || trip.created_on) }}</span>
                </td>
                <td>
                  <span class="text-gray-800 fw-bold fs-6">{{ getRoute(trip) }}</span>
                </td>
                <td>
                  <span :class="`badge badge-light-${getStatusColor(trip.status)} fs-7`">
                    {{ trip.status }}
                  </span>
                </td>
                <td class="text-end">
                  <span class="text-gray-800 fw-bold fs-6">${{ trip.total_amount || '0' }}</span>
                </td>
              </tr>
              <tr v-if="pendingTrips.length === 0">
                <td colspan="5" class="text-center text-muted py-6">
                  No pending trips found for this contact
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
      <!--end::Card body-->
    </div>
    <!--end::Pending Trips Card-->

    <!-- Recent Trips Card -->
    <div class="card mb-6 mb-xl-9">
      <!--begin::Card header-->
      <div class="card-header border-0">
        <div class="card-title">
          <h3 class="fw-bold m-0">Recent Trips</h3>
        </div>
        <div class="card-toolbar">
          <button @click="viewAllTrips" class="btn btn-sm btn-light">View All</button>
        </div>
      </div>
      <!--end::Card header-->

      <!--begin::Card body-->
      <div class="card-body pt-2">
        <div class="table-responsive">
          <table class="table table-row-dashed align-middle gs-0 gy-4 my-0">
            <thead>
              <tr class="fs-7 fw-bold text-gray-500 border-bottom-0">
                <th class="ps-0 min-w-200px">Trip</th>
                <th class="min-w-100px">Date</th>
                <th class="min-w-100px">Route</th>
                <th class="min-w-100px">Status</th>
                <th class="min-w-100px text-end">Amount</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="trip in recentTrips" :key="trip.id">
                <td class="ps-0">
                  <div class="d-flex align-items-center">
                    <div class="symbol symbol-45px me-2">
                      <img :src="getAircraftImage(trip)" :alt="getAircraftModel(trip)" class="symbol-label object-fit-cover" style="width: 45px; height: 45px; border-radius: 8px;" />
                    </div>
                    <div class="d-flex flex-column">
                      <a @click.prevent="viewTrip(trip)" href="#" class="text-gray-800 text-hover-primary fw-bold fs-6">
                        {{ trip.trip_number }}
                      </a>
                      <span class="text-gray-600 fw-semibold fs-7">{{ trip.type }}</span>
                    </div>
                  </div>
                </td>
                <td>
                  <span class="text-gray-800 fw-bold fs-6">{{ formatDate(trip.created_on) }}</span>
                </td>
                <td>
                  <span class="text-gray-800 fw-bold fs-6">{{ getRoute(trip) }}</span>
                </td>
                <td>
                  <span :class="`badge badge-light-${getStatusColor(trip.status)} fs-7`">
                    {{ trip.status }}
                  </span>
                </td>
                <td class="text-end">
                  <span class="text-gray-800 fw-bold fs-6">${{ trip.total_amount || '0' }}</span>
                </td>
              </tr>
              <tr v-if="recentTrips.length === 0">
                <td colspan="5" class="text-center text-muted py-6">
                  No recent trips found for this contact
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
      <!--end::Card body-->
    </div>
    <!--end::Recent Trips Card-->


  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, watch } from "vue";
import { useRouter } from "vue-router";
import ApiService from "@/core/services/ApiService";

interface Props {
  contact: any;
  loading: boolean;
}

const props = defineProps<Props>();
const router = useRouter();

const recentTrips = ref<any[]>([]);
const pendingTrips = ref<any[]>([]);

const fetchRecentTrips = async () => {
  if (!props.contact?.id) return;
  
  try {
    // For patients, we need to filter by patient ID, for others by contact ID
    const response = await ApiService.get(`/trips/?page_size=50`);
    const allTrips = response.data.results || response.data || [];
    
    let relevantTrips = [];
    if (props.contact?.type === 'patients') {
      // Filter trips where patient ID matches this contact ID
      relevantTrips = allTrips.filter(trip => 
        trip.patient && trip.patient.id === props.contact.id
      );
    } else {
      // Filter trips where the quote's contact matches this contact
      relevantTrips = allTrips.filter(trip => 
        trip.quote && trip.quote.contact && trip.quote.contact.id === props.contact.id
      );
    }
    
    // Separate completed and pending trips
    recentTrips.value = relevantTrips
      .filter(trip => ['completed', 'cancelled'].includes(trip.status?.toLowerCase()))
      .sort((a, b) => new Date(b.created_on).getTime() - new Date(a.created_on).getTime())
      .slice(0, 5);
      
    pendingTrips.value = relevantTrips
      .filter(trip => ['pending', 'active', 'in_progress', 'scheduled'].includes(trip.status?.toLowerCase()))
      .sort((a, b) => new Date(b.created_on).getTime() - new Date(a.created_on).getTime())
      .slice(0, 5);
  } catch (error) {
    console.error('Error fetching recent trips:', error);
  }
};

const getContactFilterParam = (): string => {
  switch (props.contact?.type) {
    case 'patients': return 'patient_id';
    case 'customers': return 'customer_id';
    default: return 'contact_id';
  }
};

const formatDate = (dateString?: string): string => {
  if (!dateString) return 'N/A';
  return new Date(dateString).toLocaleDateString('en-US', {
    month: 'short',
    day: 'numeric',
    year: 'numeric',
  });
};

const getRoute = (trip: any): string => {
  // Try different field combinations for route information
  const departure = trip.pickup_airport?.name || trip.pickup_airport?.ident || 
                   trip.departure_airport?.name || trip.departure_airport?.ident ||
                   trip.departure_airport;
  const arrival = trip.dropoff_airport?.name || trip.dropoff_airport?.ident || 
                 trip.arrival_airport?.name || trip.arrival_airport?.ident ||
                 trip.arrival_airport;
  
  if (departure && arrival) {
    return `${departure} → ${arrival}`;
  } else if (departure) {
    return `${departure} → TBD`;
  } else if (arrival) {
    return `TBD → ${arrival}`;
  }
  return 'Route TBD';
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

const viewTrip = (trip: any) => {
  if (trip.id) {
    router.push(`/admin/trips/${trip.id}`);
  }
};

const viewAllTrips = () => {
  router.push('/admin/trips');
};

// Watch for contact changes
watch(() => props.contact, (newContact) => {
  if (newContact?.id) {
    fetchRecentTrips();
  }
}, { immediate: true });

const getAircraftImage = (trip: any): string => {
  const aircraft = trip?.aircraft;
  if (!aircraft) return '/media/aircraft/Learjet35A.jpg';
  
  // Build full model name for matching image files
  const make = aircraft.make || '';
  const model = aircraft.model || '';
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

const getAircraftModel = (trip: any): string => {
  const aircraft = trip?.aircraft;
  if (!aircraft) return 'Aircraft';
  return `${aircraft.make} ${aircraft.model}` || 'Aircraft';
};

onMounted(() => {
  if (props.contact?.id) {
    fetchRecentTrips();
  }
});
</script>