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
  patient_id?: string;
  patient?: any;
  aircraft_id?: string;
  aircraft?: any;
  quote_id?: string;
  quote?: any;
  // Removed priority and departure_airport as they don't exist in backend Trip model
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
        
        // Fetch trip details - the TripReadSerializer already includes patient and aircraft data
        const response = await ApiService.get(`/trips/${tripId}/`);
        trip.value = response.data;
        
        // No need for additional API calls - patient and aircraft data are already included in the response
        // The TripReadSerializer includes:
        // - patient: serialized patient data if patient_id exists
        // - aircraft: serialized aircraft data if aircraft_id exists
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