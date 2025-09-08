<template>
  <div>
    <!--begin::Airport Location-->
    <div v-if="eventData.event_type === 'CREW_CHANGE'" class="fv-row mb-5">
      <AirportSearchSelect
        v-model="eventData.airport_id"
        label="Crew Change Location"
        placeholder="Search airport..."
        help-text="Location where the crew change takes place (typically arrival airport of preceding leg)."
        required
        @airport-selected="onAirportSelected"
      />
    </div>
    <div v-else class="fv-row mb-5">
      <label class="fs-6 fw-semibold mb-2">Airport Location</label>
      <input
        type="text"
        class="form-control form-control-solid"
        :value="airportDisplayName"
        readonly
      />
      <div class="form-text">Auto-set to arrival airport of preceding flight leg</div>
    </div>
    <!--end::Airport Location-->

    <!--begin::Start Date-->
    <div v-if="eventData.event_type === 'CREW_CHANGE'" class="fv-row mb-5">
      <label class="required fs-6 fw-semibold mb-2">Start Date</label>
      <input
        v-model="eventData.start_date"
        type="date"
        class="form-control form-control-solid"
      />
    </div>
    <div v-else class="fv-row mb-5">
      <label class="fs-6 fw-semibold mb-2">Start Date</label>
      <input
        v-model="eventData.start_date"
        type="date"
        class="form-control form-control-solid"
        readonly
      />
      <div class="form-text">Auto-set to arrival date of preceding flight leg</div>
    </div>
    <!--end::Start Date-->

    <!--begin::Event Info-->
    <div class="mt-4">
      <div v-if="eventData.event_type === 'OVERNIGHT'" class="d-flex align-items-center text-muted fs-7">
        <KTIcon icon-name="moon" icon-class="fs-6 me-2" />
        <span>Overnight stay automatically uses arrival airport and date from preceding flight leg.</span>
      </div>
      <div v-else-if="eventData.event_type === 'CREW_CHANGE'" class="d-flex align-items-center text-muted fs-7">
        <KTIcon icon-name="people" icon-class="fs-6 me-2" />
        <span>Crew change event created automatically when different crew are assigned to consecutive legs.</span>
      </div>
    </div>
    <!--end::Event Info-->
  </div>
</template>

<script setup lang="ts">
import { watch, computed, ref } from 'vue';
import AirportSearchSelect from '@/components/form-controls/AirportSearchSelect.vue';
import ApiService from '@/core/services/ApiService';

const props = defineProps({
  modelValue: {
    type: Object,
    required: true
  },
  staffMembers: {
    type: Array,
    default: () => []
  },
  defaultAirportId: {
    type: String,
    default: ''
  },
  arrivalDate: {
    type: String,
    default: ''
  },
  arrivalTime: {
    type: String,
    default: ''
  }
});

const emit = defineEmits(['update:modelValue']);

const eventData = props.modelValue;

// Airport display name for read-only field
const airportDisplayName = ref('Loading...');

// Fetch airport display name when airport ID changes
const fetchAirportDisplayName = async () => {
  if (eventData.airport_id) {
    try {
      const response = await ApiService.get(`/airports/${eventData.airport_id}/`);
      const airport = response.data;
      airportDisplayName.value = `${airport.ident} - ${airport.name}`;
    } catch (error) {
      console.error('Error loading airport:', error);
      airportDisplayName.value = 'Unknown Airport';
    }
  } else {
    airportDisplayName.value = 'No airport selected';
  }
};

// Track if user manually selected an airport
let userSelectedAirport = false;

// Set event type based on data or default to OVERNIGHT for manually created events
if (!eventData.event_type) {
  eventData.event_type = 'OVERNIGHT';
}

// Calculate overnight end time (+8 hours from start)
const calculateOvernightEndTime = () => {
  if (eventData.event_type === 'OVERNIGHT' && eventData.start_date && eventData.start_time) {
    try {
      const startDateTime = new Date(`${eventData.start_date}T${eventData.start_time}:00`);
      const endDateTime = new Date(startDateTime.getTime() + (8 * 60 * 60 * 1000)); // +8 hours
      
      eventData.end_date = endDateTime.toISOString().split('T')[0];
      eventData.end_time = endDateTime.toTimeString().slice(0, 5);
      
      console.log('Calculated overnight end time:', {
        start: `${eventData.start_date} ${eventData.start_time}`,
        end: `${eventData.end_date} ${eventData.end_time}`
      });
    } catch (error) {
      console.error('Error calculating overnight end time:', error);
    }
  }
};

// Initialize overnight event data
if (props.defaultAirportId && eventData.event_type === 'OVERNIGHT' && (!eventData.airport_id || eventData.airport_id !== props.defaultAirportId)) {
  if (!userSelectedAirport) {
    eventData.airport_id = props.defaultAirportId;
    fetchAirportDisplayName();
    
    // Set start date and time from arrival data
    if (props.arrivalDate) {
      eventData.start_date = props.arrivalDate;
    }
    if (props.arrivalTime) {
      eventData.start_time = props.arrivalTime;
    }
    
    // Calculate end time
    calculateOvernightEndTime();
  }
}

// Airport selection handler
const onAirportSelected = (airport: any) => {
  // Mark that user has manually selected an airport
  userSelectedAirport = true;
  console.log('TripEventForm: User manually selected airport:', airport);
};

// Watch for changes in arrival date/time to update overnight start date/time
watch(() => [props.arrivalDate, props.arrivalTime], ([newArrivalDate, newArrivalTime]) => {
  if (eventData.event_type === 'OVERNIGHT' && !userSelectedAirport) {
    if (newArrivalDate) {
      eventData.start_date = newArrivalDate;
    }
    if (newArrivalTime) {
      eventData.start_time = newArrivalTime;
    }
    
    // Recalculate end time after updating start time
    calculateOvernightEndTime();
  }
}, { immediate: true });

// Watch for changes in default airport prop
watch(() => props.defaultAirportId, (newDefaultAirport) => {
  // Only apply auto-defaults to OVERNIGHT events
  if (newDefaultAirport && eventData.event_type === 'OVERNIGHT' && newDefaultAirport !== eventData.airport_id && !userSelectedAirport) {
    eventData.airport_id = newDefaultAirport;
    fetchAirportDisplayName();
    
    // Set start date and time from arrival data
    if (props.arrivalDate) {
      eventData.start_date = props.arrivalDate;
    }
    if (props.arrivalTime) {
      eventData.start_time = props.arrivalTime;
    }
    
    // Recalculate end time
    calculateOvernightEndTime();
  }
});

// Watch for airport ID changes to update display name
watch(() => eventData.airport_id, () => {
  if (eventData.airport_id) {
    fetchAirportDisplayName();
  }
}, { immediate: true });
</script>