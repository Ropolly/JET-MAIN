<template>
  <!--begin::Modal - Add Trip Legs-->
  <div
    class="modal fade"
    id="kt_modal_add_trip_legs"
    ref="modalRef"
    tabindex="-1"
    aria-hidden="true"
  >
    <!--begin::Modal dialog-->
    <div class="modal-dialog modal-xl">
      <!--begin::Modal content-->
      <div class="modal-content">
        <!--begin::Modal header-->
        <div class="modal-header">
          <!--begin::Title-->
          <h2>Add Flight Legs - {{ getTripTitle() }}</h2>
          <!--end::Title-->

          <!--begin::Close-->
          <div
            class="btn btn-sm btn-icon btn-active-color-primary"
            data-bs-dismiss="modal"
            @click="closeModal"
          >
            <KTIcon icon-name="cross" icon-class="fs-1" />
          </div>
          <!--end::Close-->
        </div>
        <!--end::Modal header-->

        <!--begin::Modal body-->
        <div class="modal-body scroll-y mx-5 mx-xl-15 my-7">
          <!--begin::Trip Context-->
          <div class="alert alert-primary d-flex align-items-center mb-6">
            <KTIcon icon-name="information-5" icon-class="fs-2x text-primary me-4" />
            <div>
              <h5 class="mb-1 text-primary">Trip {{ trip?.trip_number }}</h5>
              <div class="text-gray-700">
                Add flight legs to this {{ trip?.type }} trip. A real trip number will be automatically generated when you save the legs.
              </div>
            </div>
          </div>
          <!--end::Trip Context-->

          <!--begin::Flight Legs Step-->
          <FlightLegsStep
            :legs="legs"
            :events="events"
            :trip-data="trip"
            :staff-members="staffMembers"
            @update:legs="onLegsUpdated"
            @update:events="onEventsUpdated"
          />
          <!--end::Flight Legs Step-->
        </div>
        <!--end::Modal body-->

        <!--begin::Modal footer-->
        <div class="modal-footer">
          <button
            type="button"
            class="btn btn-light"
            data-bs-dismiss="modal"
            @click="closeModal"
          >
            Cancel
          </button>
          <button
            type="button"
            class="btn btn-primary"
            @click="saveTripLegs"
            :disabled="saving || legs.length === 0"
          >
            <span v-if="!saving" class="indicator-label">
              Save Flight Legs
            </span>
            <span v-else class="indicator-progress">
              Saving...
              <span class="spinner-border spinner-border-sm align-middle ms-2"></span>
            </span>
          </button>
        </div>
        <!--end::Modal footer-->
      </div>
      <!--end::Modal content-->
    </div>
    <!--end::Modal dialog-->
  </div>
  <!--end::Modal - Add Trip Legs-->
</template>

<script setup lang="ts">
import { ref, computed, watch, onMounted } from 'vue';
import { hideModal } from '@/core/helpers/modal';
import FlightLegsStep from '@/components/modals/CreateTripSteps/FlightLegsStep.vue';
import ApiService from '@/core/services/ApiService';
import Swal from 'sweetalert2/dist/sweetalert2.js';

interface Props {
  trip?: any;
  show?: boolean;
}

const props = defineProps<Props>();
const emit = defineEmits(['close', 'trip-updated']);

const modalRef = ref<HTMLElement | null>(null);
const saving = ref(false);
const legs = ref<any[]>([]);
const events = ref<any[]>([]);
const staffMembers = ref<any[]>([]);
const loadingStaff = ref(false);

// Trip title for modal header
const getTripTitle = (): string => {
  if (!props.trip) return 'Trip';
  return props.trip.trip_number || 'New Trip';
};

// Handle legs and events updates from FlightLegsStep
const onLegsUpdated = (updatedLegs: any[]) => {
  console.log('Legs updated:', updatedLegs.length, updatedLegs);
  legs.value = updatedLegs;
};

const onEventsUpdated = (updatedEvents: any[]) => {
  console.log('Events updated:', updatedEvents.length, updatedEvents);
  events.value = updatedEvents;
};

// Load staff members for crew selection
const loadStaffMembers = async () => {
  loadingStaff.value = true;
  try {
    // Fetch all staff members by requesting a large page size
    const response = await ApiService.get('/staff/?page_size=100');
    staffMembers.value = response.data.results || response.data || [];
    console.log('Loaded staff members:', staffMembers.value.length);
    console.log('First staff member:', staffMembers.value[0]);
    console.log('Staff with role memberships:', staffMembers.value.filter(s => s.role_memberships?.length > 0).length);

    // Check for pilots
    const picStaff = staffMembers.value.filter(s => s.role_memberships?.some(m => m.role?.code === 'PIC'));
    const sicStaff = staffMembers.value.filter(s => s.role_memberships?.some(m => m.role?.code === 'SIC'));
    console.log('Staff with PIC role:', picStaff.length);
    console.log('Staff with SIC role:', sicStaff.length);
  } catch (error) {
    console.error('Error loading staff members:', error);
    staffMembers.value = [];
  } finally {
    loadingStaff.value = false;
  }
};

// Save trip legs to the backend
const saveTripLegs = async () => {
  if (!props.trip?.id || legs.value.length === 0) {
    await Swal.fire({
      title: 'No Flight Legs',
      text: 'Please add at least one flight leg before saving.',
      icon: 'warning',
      confirmButtonText: 'OK'
    });
    return;
  }

  saving.value = true;

  try {
    // Create trip lines via API
    const tripLinePromises = legs.value.map(async (leg) => {
      const tripLineData = {
        trip: props.trip.id,
        origin_airport: leg.origin_airport,
        destination_airport: leg.destination_airport,
        departure_time_local: `${leg.departure_date}T${leg.departure_time}`,
        departure_time_utc: `${leg.departure_date}T${leg.departure_time}`, // Will be converted by backend
        arrival_time_local: leg.arrival_date && leg.arrival_time ? `${leg.arrival_date}T${leg.arrival_time}` : null,
        arrival_time_utc: leg.arrival_date && leg.arrival_time ? `${leg.arrival_date}T${leg.arrival_time}` : null, // Will be converted by backend
        distance: 0, // Will be calculated by backend
        flight_time: '01:00:00', // Default, will be calculated by backend
        ground_time: '00:30:00', // Default
        passenger_leg: true,
        crew_line: leg.crew_line_id || null,
        departure_fbo: leg.departure_fbo_id || null,
        arrival_fbo: leg.arrival_fbo_id || null
      };

      return ApiService.post('/trip-lines/', tripLineData);
    });

    // Create all trip lines
    await Promise.all(tripLinePromises);

    // Create trip events if any
    if (events.value.length > 0) {
      const eventPromises = events.value.map(async (event) => {
        const eventData = {
          trip_id: props.trip.id,
          airport_id: event.airport_id,
          event_type: event.event_type,
          start_time_local: `${event.start_date}T${event.start_time}`,
          start_time_utc: `${event.start_date}T${event.start_time}`, // Will be converted by backend
          end_time_local: event.end_date && event.end_time ? `${event.end_date}T${event.end_time}` : null,
          end_time_utc: event.end_date && event.end_time ? `${event.end_date}T${event.end_time}` : null, // Will be converted by backend
          crew_line_id: event.crew_line_id || null,
          notes: event.notes || ''
        };

        return ApiService.post('/trip-events/', eventData);
      });

      await Promise.all(eventPromises);
    }

    // Update trip to generate real trip number (by sending empty trip_number)
    await ApiService.put(`/trips/${props.trip.id}/`, {
      trip_number: '', // This triggers the backend to generate a real trip number
      type: props.trip.type // Include existing type to satisfy required field validation
    });

    // Show success message
    await Swal.fire({
      title: 'Success!',
      text: `Flight legs have been added and a trip number has been generated.`,
      icon: 'success',
      confirmButtonText: 'OK'
    });

    // Emit trip updated event to parent
    emit('trip-updated');
    closeModal();

  } catch (error) {
    console.error('Error saving trip legs:', error);

    let errorMessage = 'Failed to save flight legs. Please try again.';
    if (error.response?.data) {
      if (typeof error.response.data === 'object') {
        errorMessage = JSON.stringify(error.response.data);
      } else {
        errorMessage = error.response.data.detail || error.response.data.message || error.response.data.toString();
      }
    } else if (error.message) {
      errorMessage = error.message;
    }

    await Swal.fire({
      title: 'Error',
      text: errorMessage,
      icon: 'error',
      confirmButtonText: 'OK'
    });
  } finally {
    saving.value = false;
  }
};

// Close modal
const closeModal = () => {
  hideModal(modalRef.value);
  emit('close');

  // Reset data
  legs.value = [];
  events.value = [];
};

// Load staff data when component is mounted
onMounted(() => {
  console.log('AddTripLegsModal mounted, loading staff members...');
  loadStaffMembers();
});

// Watch for show prop changes to reset data
watch(() => props.show, (newShow) => {
  console.log('AddTripLegsModal show prop changed:', newShow);
  if (newShow) {
    // Reset data when modal opens
    legs.value = [];
    events.value = [];
    // Load staff members for crew selection if not already loaded
    if (staffMembers.value.length === 0) {
      console.log('Staff members not loaded, loading now...');
      loadStaffMembers();
    }
  }
});
</script>

<style scoped>
.modal-xl {
  max-width: 90%;
}

.indicator-progress .spinner-border {
  width: 1rem;
  height: 1rem;
}
</style>