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
  <div class="d-flex flex-column flex-lg-row align-items-lg-start">
    <!--begin::Content-->
    <div class="flex-lg-row-fluid me-lg-5 order-2 order-lg-1 mb-10 mb-lg-0">
      <!-- Trip Summary Card -->
      <FlightStatistics :trip="trip" :loading="loading" @patientAdded="fetchTrip" @status-updated="handleStatusUpdated" />

      <!-- Aircraft Details Card -->
      <AircraftDetails :trip="trip" :loading="loading" />

      <!-- Combined Itinerary & Timeline Card -->
      <TripItinerary :trip="trip" :loading="loading" />


      <!-- Trip Documents Card -->
      <div data-kt-element="documents">
        <TripDocuments v-if="trip?.id" :trip-id="trip.id" :trip="trip" />
      </div>

      <!-- Trip Contracts Card -->
      <div data-kt-element="contracts" class="mt-8">
        <TripContracts v-if="trip?.id" :trip-id="trip.id" :trip-data="trip" />
      </div>
    </div>
    <!--end::Content-->

    <!--begin::Sidebar-->
    <div
      class="flex-column flex-lg-row-auto w-lg-350px w-xl-400px mb-10 order-1 order-lg-2"
    >
      <!-- Trip Comments Card -->
      <TripComments v-if="trip?.id" :trip-id="trip.id" :trip-data="trip" />
      
      <!-- Trip Notes Card -->
      <TripNotes v-if="trip?.id" :trip-id="trip.id" :trip-data="trip" :loading="loading" @notes-updated="handleNotesUpdated" />
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
import Swal from "sweetalert2";
import FlightStatistics from "@/components/trips/view/FlightStatistics.vue";
import TripItinerary from "@/components/trips/view/TripItinerary.vue";
import AircraftDetails from "@/components/trips/view/AircraftDetails.vue";
import TripDocuments from "@/components/trips/view/TripDocuments.vue";
import TripContracts from "@/components/trips/view/TripContracts.vue";
import TripComments from "@/components/trips/view/TripComments.vue";
import TripNotes from "@/components/trips/view/TripNotes.vue";

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
    TripDocuments,
    TripContracts,
    TripComments,
    TripNotes,
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

    const setupToolbarActions = () => {
      const actions = [];
      
      // Build dropdown items
      const dropdownItems = [
        {
          id: 'edit-trip',
          label: 'Edit Trip',
          icon: 'pencil',
          handler: handleEditTrip
        },
        { divider: true },
        {
          id: 'delete-trip',
          label: 'Delete Trip',
          icon: 'trash',
          handler: handleDeleteTrip,
          className: 'text-danger'
        }
      ];
      
      // Add Actions dropdown
      actions.push({
        id: 'trip-actions-dropdown',
        label: 'Actions',
        variant: 'dark',
        isDropdown: true,
        dropdownItems: dropdownItems
      });
      
      setToolbarActions(actions);
    };

    const handleDeleteTrip = () => {
      if (!trip.value) return;
      
      Swal.fire({
        title: 'Delete Trip',
        text: 'Are you sure you want to delete this trip? This action cannot be undone.',
        icon: 'warning',
        showCancelButton: true,
        confirmButtonText: 'Yes, Delete',
        cancelButtonText: 'Cancel',
        confirmButtonColor: '#d33'
      }).then(async (result) => {
        if (result.isConfirmed) {
          try {
            await ApiService.delete(`/trips/${trip.value!.id}/`);
            
            Swal.fire({
              title: 'Deleted!',
              text: 'Trip has been deleted successfully.',
              icon: 'success',
              confirmButtonText: 'OK'
            }).then(() => {
              router.push('/admin/trips');
            });
          } catch (error) {
            console.error('Error deleting trip:', error);
            Swal.fire({
              title: 'Error!',
              text: 'Failed to delete the trip. Please try again.',
              icon: 'error',
              confirmButtonText: 'OK'
            });
          }
        }
      });
    };

    const handleNotesUpdated = (updatedNotes: string) => {
      // Update the trip data with the new notes
      if (trip.value) {
        trip.value.notes = updatedNotes;
      }
    };

    const handleStatusUpdated = (updatedStatus: string) => {
      // Update the trip data with the new status
      if (trip.value) {
        trip.value.status = updatedStatus;
      }
    };


    onMounted(() => {
      fetchTrip();
      setupToolbarActions();
    });

    return {
      trip,
      loading,
      error,
      formatQuoteAmount,
      viewQuote,
      handleDeleteTrip,
      setupToolbarActions,
      handleNotesUpdated,
      handleStatusUpdated,
    };
  },
});
</script>