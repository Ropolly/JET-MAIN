<template>
  <div class="card">
    <!--begin::Card header-->
    <div class="card-header border-0 pt-5">
      <h3 class="card-title align-items-start flex-column">
        <span class="card-label fw-bold fs-3 mb-1">Aircraft Overview</span>
        <span class="text-muted mt-1 fw-semibold fs-7">Technical specifications and operational data</span>
      </h3>
    </div>
    <!--end::Card header-->

    <!--begin::Card body-->
    <div class="card-body py-3">
      <div v-if="loading" class="d-flex justify-content-center">
        <div class="spinner-border" role="status">
          <span class="visually-hidden">Loading...</span>
        </div>
      </div>

      <div v-else-if="aircraft" class="row">
        <!--begin::Col-->
        <div class="col-md-6">
          <!--begin::Aircraft Info-->
          <div class="mb-10">
            <h4 class="fw-bold text-dark mb-5">Aircraft Information</h4>
            
            <div class="row mb-3">
              <div class="col-4 fw-bold text-gray-600">Tail Number:</div>
              <div class="col-8 text-gray-800">{{ aircraft.tail_number }}</div>
            </div>
            
            <div class="row mb-3">
              <div class="col-4 fw-bold text-gray-600">Make:</div>
              <div class="col-8 text-gray-800">{{ aircraft.make }}</div>
            </div>
            
            <div class="row mb-3">
              <div class="col-4 fw-bold text-gray-600">Model:</div>
              <div class="col-8 text-gray-800">{{ aircraft.model }}</div>
            </div>
            
            <div class="row mb-3">
              <div class="col-4 fw-bold text-gray-600">Serial Number:</div>
              <div class="col-8 text-gray-800">{{ aircraft.serial_number }}</div>
            </div>
            
            <div class="row mb-3">
              <div class="col-4 fw-bold text-gray-600">Company:</div>
              <div class="col-8 text-gray-800">{{ aircraft.company }}</div>
            </div>
            
            <div class="row mb-3">
              <div class="col-4 fw-bold text-gray-600">MGTOW:</div>
              <div class="col-8 text-gray-800">{{ formatWeight(aircraft.mgtow) }}</div>
            </div>
          </div>
          <!--end::Aircraft Info-->
        </div>
        <!--end::Col-->

        <!--begin::Col-->
        <div class="col-md-6">
          <!--begin::Operational Stats-->
          <div class="mb-10">
            <h4 class="fw-bold text-dark mb-5">Operational Statistics</h4>
            
            <div class="row mb-3">
              <div class="col-4 fw-bold text-gray-600">Total Trips:</div>
              <div class="col-8 text-gray-800">{{ aircraft.total_trips || '0' }}</div>
            </div>
            
            <div class="row mb-3">
              <div class="col-4 fw-bold text-gray-600">Flight Hours:</div>
              <div class="col-8 text-gray-800">{{ aircraft.total_flight_hours || '0' }}h</div>
            </div>
            
            <div class="row mb-3">
              <div class="col-4 fw-bold text-gray-600">Last Flight:</div>
              <div class="col-8 text-gray-800">{{ formatDate(aircraft.last_flight_date) }}</div>
            </div>
            
            <div class="row mb-3">
              <div class="col-4 fw-bold text-gray-600">Status:</div>
              <div class="col-8">
                <span :class="`badge badge-light-${getStatusColor()}`">
                  {{ aircraft.status || 'Active' }}
                </span>
              </div>
            </div>
            
            <div class="row mb-3">
              <div class="col-4 fw-bold text-gray-600">Created:</div>
              <div class="col-8 text-gray-800">{{ formatDate(aircraft.created_on) }}</div>
            </div>
          </div>
          <!--end::Operational Stats-->
        </div>
        <!--end::Col-->
      </div>

      <div v-else class="text-center py-10">
        <div class="text-gray-400">No aircraft data available</div>
      </div>
    </div>
    <!--end::Card body-->
  </div>

  <!--begin::Upcoming Trips Card-->
  <div class="card mb-5">
    <div class="card-header border-0 pt-5">
      <h3 class="card-title align-items-start flex-column">
        <span class="card-label fw-bold fs-3 mb-1">Upcoming Trips</span>
        <span class="text-muted mt-1 fw-semibold fs-7">Scheduled flights for this aircraft</span>
      </h3>
    </div>
    <div class="card-body py-3">
      <div v-if="upcomingTrips.length > 0">
        <div v-for="trip in upcomingTrips" :key="trip.id" class="d-flex align-items-center mb-4">
          <div class="symbol symbol-40px me-4">
            <div class="symbol-label bg-light-primary">
              <i class="fas fa-plane text-primary"></i>
            </div>
          </div>
          <div class="flex-grow-1">
            <a @click="navigateToTrip(trip.id)" href="#" class="fw-bold text-gray-800 text-hover-primary fs-6">#{{ trip.trip_number || trip.id }}</a>
            <div class="text-muted fs-7">{{ formatTripRoute(trip) }}</div>
          </div>
          <div class="text-end">
            <div class="fw-bold text-gray-800 fs-6">{{ formatDate(trip.date) }}</div>
            <div class="text-muted fs-7">{{ trip.status }}</div>
          </div>
        </div>
      </div>
      <div v-else class="text-center py-6">
        <div class="text-gray-400">No upcoming trips scheduled</div>
      </div>
    </div>
  </div>
  <!--end::Upcoming Trips Card-->

  <!--begin::Recent Trips Card-->
  <div class="card mb-5">
    <div class="card-header border-0 pt-5">
      <h3 class="card-title align-items-start flex-column">
        <span class="card-label fw-bold fs-3 mb-1">Recent Trips</span>
        <span class="text-muted mt-1 fw-semibold fs-7">Last 5 completed flights</span>
      </h3>
    </div>
    <div class="card-body py-3">
      <div v-if="recentTrips.length > 0">
        <div v-for="trip in recentTrips" :key="trip.id" class="d-flex align-items-center mb-4">
          <div class="symbol symbol-40px me-4">
            <div class="symbol-label bg-light-success">
              <i class="fas fa-check text-success"></i>
            </div>
          </div>
          <div class="flex-grow-1">
            <a @click="navigateToTrip(trip.id)" href="#" class="fw-bold text-gray-800 text-hover-primary fs-6">#{{ trip.trip_number || trip.id }}</a>
            <div class="text-muted fs-7">{{ formatTripRoute(trip) }}</div>
          </div>
          <div class="text-end">
            <div class="fw-bold text-gray-800 fs-6">{{ formatDate(trip.date) }}</div>
            <div class="text-muted fs-7">{{ trip.status }}</div>
          </div>
        </div>
      </div>
      <div v-else class="text-center py-6">
        <div class="text-gray-400">No recent trips found</div>
      </div>
    </div>
  </div>
  <!--end::Recent Trips Card-->
</template>

<script lang="ts">
import { defineComponent, ref, watch, onMounted } from "vue";
import ApiService from "@/core/services/ApiService";

export default defineComponent({
  name: "AircraftOverview",
  props: {
    aircraft: {
      type: Object,
      default: null,
    },
    loading: {
      type: Boolean,
      default: false,
    },
  },
  setup(props) {
    const upcomingTrips = ref<any[]>([]);
    const recentTrips = ref<any[]>([]);
    const tripsLoading = ref(false);

    const fetchTrips = async () => {
      if (!props.aircraft?.id) return;
      
      try {
        tripsLoading.value = true;
        const response = await ApiService.get(`/trips/?aircraft=${props.aircraft.id}`);
        const trips = response.data.results || response.data || [];
        
        // Split trips into upcoming and recent
        const now = new Date();
        upcomingTrips.value = trips
          .filter((trip: any) => new Date(trip.estimated_departure_time || trip.created_on) > now)
          .slice(0, 5);
        
        recentTrips.value = trips
          .filter((trip: any) => new Date(trip.estimated_departure_time || trip.created_on) <= now)
          .slice(0, 5);
          
      } catch (error) {
        console.error("Error fetching trips:", error);
        upcomingTrips.value = [];
        recentTrips.value = [];
      } finally {
        tripsLoading.value = false;
      }
    };

    const formatWeight = (weight?: string | number): string => {
      if (!weight) return 'Not specified';
      const numWeight = typeof weight === 'string' ? parseFloat(weight) : weight;
      return `${numWeight.toLocaleString()} lbs`;
    };

    const formatDate = (dateString?: string): string => {
      if (!dateString) return 'Not provided';
      return new Date(dateString).toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'long',
        day: 'numeric',
      });
    };

    const formatTripRoute = (trip: any): string => {
      if (trip.trip_lines && trip.trip_lines.length > 0) {
        const firstLeg = trip.trip_lines[0];
        const lastLeg = trip.trip_lines[trip.trip_lines.length - 1];
        const origin = firstLeg.origin_airport?.iata_code || firstLeg.origin_airport?.icao_code || 'N/A';
        const destination = lastLeg.destination_airport?.iata_code || lastLeg.destination_airport?.icao_code || 'N/A';
        return `${origin} → ${destination}`;
      }
      return 'Route not specified';
    };

    const getStatusColor = (): string => {
      return 'success';
    };

    const navigateToTrip = (tripId: string) => {
      const url = `/admin/trips/${tripId}`;
      window.open(url, '_blank');
    };

    watch(() => props.aircraft, fetchTrips, { immediate: true });

    return {
      upcomingTrips,
      recentTrips,
      tripsLoading,
      formatWeight,
      formatDate,
      formatTripRoute,
      getStatusColor,
      navigateToTrip,
    };
  },
});
</script>