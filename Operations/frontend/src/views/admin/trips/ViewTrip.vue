<template>
  <!--begin::Associated Quote Alert-->
  <div v-if="trip?.quote?.id" class="alert alert-warning d-flex align-items-center justify-content-between mb-5">
    <div class="d-flex align-items-center">
      <KTIcon icon-name="price-tag" icon-class="fs-2x text-warning me-4" />
      <div>
        <div class="fw-bold fs-6">This trip was converted from a quote</div>
        <div class="text-gray-700 fs-7">
          Quote #{{ trip.quote.id?.slice(0, 8) }}
          <span class="mx-2">•</span>
          Amount: ${{ formatQuoteAmount(trip.quote.quoted_amount) }}
          <span class="mx-2">•</span>
          <span class="badge badge-warning fs-8">
            {{ trip.quote.status }}
          </span>
        </div>
      </div>
    </div>
    <button @click="viewQuote" class="btn btn-sm btn-warning">
      View Quote
      <KTIcon icon-name="arrow-right" icon-class="fs-5 ms-1" />
    </button>
  </div>
  <!--end::Associated Quote Alert-->

  <!--begin::Layout-->
  <div class="d-flex flex-column flex-lg-row">
    <!--begin::Content-->
    <div class="flex-lg-row-fluid me-lg-15 order-2 order-lg-1 mb-10 mb-lg-0">
      <!-- Flight Statistics Card -->
      <FlightStatistics :trip="trip" :loading="loading" />

      <!-- Aircraft Details Card -->
      <AircraftDetails :trip="trip" :loading="loading" />

      <!-- Combined Itinerary & Timeline Card -->
      <TripItinerary :trip="trip" :loading="loading" />
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
import { useRoute, useRouter } from "vue-router";
import ApiService from "@/core/services/ApiService";
import { useToolbar, createToolbarActions } from "@/core/helpers/toolbar";
import FlightStatistics from "@/components/trips/view/FlightStatistics.vue";
import TripItinerary from "@/components/trips/view/TripItinerary.vue";
import AircraftDetails from "@/components/trips/view/AircraftDetails.vue";
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
  quote?: {
    id: string;
    quoted_amount: string;
    status?: string;
  };
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
    FlightStatistics,
    TripItinerary,
    AircraftDetails,
    TripSummary,
  },
  setup() {
    const route = useRoute();
    const router = useRouter();
    const trip = ref<Trip | null>(null);
    const loading = ref(true);
    const error = ref<string | null>(null);
    const { setToolbarActions } = useToolbar();

    const formatQuoteAmount = (amount: string | number): string => {
      if (!amount) return '0';
      const numAmount = typeof amount === 'string' ? parseFloat(amount) : amount;
      return numAmount.toLocaleString();
    };

    const viewQuote = () => {
      if (trip.value?.quote?.id) {
        window.open(`/admin/quotes/${trip.value.quote.id}`, '_blank');
      }
    };

    const fetchTrip = async () => {
      try {
        loading.value = true;
        error.value = null;
        const tripId = route.params.id as string;
        
        // Fetch trip details - the TripReadSerializer already includes patient and aircraft data
        const response = await ApiService.get(`/trips/${tripId}/`);
        trip.value = response.data;
        
        console.log('Trip data received:', response.data);
        console.log('Patient data:', response.data.patient);
        console.log('Trip lines data:', response.data.trip_lines);
        if (response.data.trip_lines && response.data.trip_lines.length > 0) {
          console.log('First trip line airports:', {
            origin: response.data.trip_lines[0].origin_airport,
            destination: response.data.trip_lines[0].destination_airport,
            departure_timezone_info: response.data.trip_lines[0].departure_timezone_info,
            arrival_timezone_info: response.data.trip_lines[0].arrival_timezone_info
          });
        }
        
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

    const handleEditTrip = () => {
      // Navigate back to trips page and trigger edit modal
      if (trip.value?.id) {
        // Store edit data in sessionStorage for the trips page to pick up
        sessionStorage.setItem('editTripData', JSON.stringify({
          mode: 'edit',
          tripId: trip.value.id,
          tripData: trip.value
        }));
        
        // Navigate to trips page with a flag to open edit modal
        router.push('/admin/trips?edit=' + trip.value.id);
      }
    };

    const handleGenerateManifest = () => {
      // Generate manifest for trip
      console.log('Generate manifest for trip:', trip.value?.trip_number);
    };

    onMounted(() => {
      fetchTrip();
      
      // Setup toolbar actions
      setToolbarActions([
        createToolbarActions.primary('edit-trip', 'Edit Trip', handleEditTrip, 'pencil'),
        createToolbarActions.secondary('generate-manifest', 'Generate Manifest', handleGenerateManifest, 'printer')
      ]);
    });

    return {
      trip,
      loading,
      error,
      formatQuoteAmount,
      viewQuote,
    };
  },
});
</script>