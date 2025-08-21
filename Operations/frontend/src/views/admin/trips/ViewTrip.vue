<template>
  <!--begin::Layout-->
  <div class="d-flex flex-column flex-lg-row">
    <!--begin::Content-->
    <div class="flex-lg-row-fluid me-lg-15 order-2 order-lg-1 mb-10 mb-lg-0">
      <!-- Trip Details Card -->
      <TripDetails :trip="trip" :loading="loading" />

      <!-- Itinerary Card -->
      <TripItinerary :trip="trip" :loading="loading" />

      <!-- Aircraft Details Card -->
      <AircraftDetails :trip="trip" :loading="loading" />

      <!-- Quote & Billing Card -->
      <QuoteBilling :trip="trip" :loading="loading" />
    </div>
    <!--end::Content-->

    <!--begin::Sidebar-->
    <div
      class="flex-column flex-lg-row-auto w-lg-250px w-xl-300px mb-10 order-1 order-lg-2"
    >
      <!-- Trip Summary Card -->
      <TripSummary :trip="trip" :loading="loading" />
    </div>
    <!--end::Sidebar-->
  </div>
  <!--end::Layout-->
</template>

<script lang="ts">
import { defineComponent, ref, onMounted } from "vue";
import { useRoute } from "vue-router";
import ApiService from "@/core/services/ApiService";
import TripDetails from "@/components/trips/view/TripDetails.vue";
import TripItinerary from "@/components/trips/view/TripItinerary.vue";
import AircraftDetails from "@/components/trips/view/AircraftDetails.vue";
import QuoteBilling from "@/components/trips/view/QuoteBilling.vue";
import TripSummary from "@/components/trips/view/TripSummary.vue";

interface Trip {
  id: string;
  trip_number: string;
  type: string;
  status: string;
  priority?: string;
  patient_id?: string;
  patient?: any;
  aircraft_id?: string;
  aircraft?: any;
  departure_airport?: string;
  arrival_airport?: string;
  estimated_departure_time?: string;
  estimated_arrival_time?: string;
  actual_departure_time?: string;
  actual_arrival_time?: string;
  distance?: number;
  flight_time?: number;
  fuel_required?: number;
  crew?: any[];
  quote?: any;
  notes?: string;
  created_on?: string;
  modified_on?: string;
}

export default defineComponent({
  name: "view-trip",
  components: {
    TripDetails,
    TripItinerary,
    AircraftDetails,
    QuoteBilling,
    TripSummary,
  },
  setup() {
    const route = useRoute();
    const trip = ref<Trip | null>(null);
    const loading = ref(true);
    const error = ref<string | null>(null);

    const fetchTrip = async () => {
      try {
        loading.value = true;
        error.value = null;
        const tripId = route.params.id as string;
        
        // Fetch trip details
        const response = await ApiService.get(`/trips/${tripId}/`);
        trip.value = response.data;
        
        // If patient_id exists, fetch patient details
        if (trip.value?.patient_id) {
          try {
            const patientResponse = await ApiService.get(`/patients/${trip.value.patient_id}/`);
            trip.value.patient = patientResponse.data;
          } catch (err) {
            console.error('Error fetching patient:', err);
          }
        }
        
        // If aircraft_id exists, fetch aircraft details
        if (trip.value?.aircraft_id) {
          try {
            const aircraftResponse = await ApiService.get(`/aircraft/${trip.value.aircraft_id}/`);
            trip.value.aircraft = aircraftResponse.data;
          } catch (err) {
            console.error('Error fetching aircraft:', err);
          }
        }
      } catch (err: any) {
        error.value = err.response?.data?.detail || "Failed to fetch trip details";
        console.error("Error fetching trip:", err);
      } finally {
        loading.value = false;
      }
    };

    onMounted(() => {
      fetchTrip();
    });

    return {
      trip,
      loading,
      error,
    };
  },
});
</script>