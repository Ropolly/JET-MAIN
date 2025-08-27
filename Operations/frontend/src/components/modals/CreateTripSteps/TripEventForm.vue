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

    <!--begin::Start Time-->
    <div v-if="eventData.event_type === 'CREW_CHANGE'" class="row g-9 mb-5">
      <div class="col-md-6 fv-row">
        <label class="required fs-6 fw-semibold mb-2">Start Date</label>
        <input
          v-model="eventData.start_date"
          type="date"
          class="form-control form-control-solid"
        />
      </div>
      <div class="col-md-6 fv-row">
        <label class="required fs-6 fw-semibold mb-2">Start Time</label>
        <input
          v-model="eventData.start_time"
          type="time"
          class="form-control form-control-solid"
        />
      </div>
    </div>
    <div v-else class="row g-9 mb-5">
      <div class="col-md-6 fv-row">
        <label class="fs-6 fw-semibold mb-2">Start Date</label>
        <input
          v-model="eventData.start_date"
          type="date"
          class="form-control form-control-solid"
          readonly
        />
        <div class="form-text">Auto-set to arrival date of preceding flight leg</div>
      </div>
      <div class="col-md-6 fv-row">
        <label class="fs-6 fw-semibold mb-2">Start Time</label>
        <input
          v-model="eventData.start_time"
          type="time"
          class="form-control form-control-solid"
          readonly
        />
        <div class="form-text">Auto-set to arrival time of preceding flight leg</div>
      </div>
    </div>
    <!--end::Start Time-->

    <!--begin::End Time (only for overnight stays)-->
    <div v-if="eventData.event_type === 'OVERNIGHT'" class="row g-9 mb-5">
      <div class="col-md-6 fv-row">
        <label class="fs-6 fw-semibold mb-2">End Date</label>
        <input
          v-model="eventData.end_date"
          type="date"
          class="form-control form-control-solid"
          readonly
        />
        <div class="form-text">Auto-calculated: start date +8 hours (+1 day if needed)</div>
      </div>
      <div class="col-md-6 fv-row">
        <label class="fs-6 fw-semibold mb-2">End Time</label>
        <input
          v-model="eventData.end_time"
          type="time"
          class="form-control form-control-solid"
          readonly
        />
        <div class="form-text">Auto-calculated: start time +8 hours</div>
      </div>
    </div>
    <!--end::End Time-->


    <!--begin::Notes-->
    <div class="fv-row">
      <label class="fs-6 fw-semibold mb-2">Event Notes</label>
      <textarea
        v-model="eventData.notes"
        class="form-control form-control-solid"
        rows="2"
        placeholder="Additional notes for this event..."
      ></textarea>
    </div>
    <!--end::Notes-->

    <!--begin::Event Info-->
    <div class="mt-4">
      <div v-if="eventData.event_type === 'OVERNIGHT'" class="d-flex align-items-center text-muted fs-7">
        <KTIcon icon-name="moon" icon-class="fs-6 me-2" />
        <span>Overnight stay automatically uses arrival airport, date and time from preceding leg. End time is calculated as +8 hours from start time.</span>
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

// Auto-calculate overnight event times
const calculateOvernightTimes = () => {
  if (eventData.event_type === 'OVERNIGHT' && props.arrivalDate && props.arrivalTime) {
    // Set start date/time to arrival date/time
    eventData.start_date = props.arrivalDate;
    eventData.start_time = props.arrivalTime;
    
    // Calculate end time (+8 hours from start time)
    try {
      const startDateTime = new Date(`${props.arrivalDate}T${props.arrivalTime}:00`);
      const endDateTime = new Date(startDateTime.getTime() + (8 * 60 * 60 * 1000)); // +8 hours
      
      eventData.end_date = endDateTime.toISOString().split('T')[0];
      eventData.end_time = endDateTime.toTimeString().slice(0, 5);
      
      console.log('Calculated overnight times:', {
        start: startDateTime.toString(),
        end: endDateTime.toString()
      });
    } catch (error) {
      console.error('Error calculating overnight times:', error);
    }
  }
};

// Initialize overnight event data
if (props.defaultAirportId && eventData.event_type === 'OVERNIGHT' && (!eventData.airport_id || eventData.airport_id !== props.defaultAirportId)) {
  if (!userSelectedAirport) {
    eventData.airport_id = props.defaultAirportId;
    fetchAirportDisplayName();
    calculateOvernightTimes();
  }
}

// Airport selection handler
const onAirportSelected = (airport: any) => {
  // Mark that user has manually selected an airport
  userSelectedAirport = true;
  console.log('TripEventForm: User manually selected airport:', airport);
};

// Watch for changes in arrival data to recalculate overnight times
watch(() => [props.arrivalDate, props.arrivalTime], () => {
  if (eventData.event_type === 'OVERNIGHT') {
    calculateOvernightTimes();
  }
}, { immediate: true });

// Watch for changes in default airport prop
watch(() => props.defaultAirportId, (newDefaultAirport) => {
  // Only apply auto-defaults to OVERNIGHT events
  if (newDefaultAirport && eventData.event_type === 'OVERNIGHT' && newDefaultAirport !== eventData.airport_id && !userSelectedAirport) {
    eventData.airport_id = newDefaultAirport;
    fetchAirportDisplayName();
    calculateOvernightTimes();
  }
});

// Watch for airport ID changes to update display name
watch(() => eventData.airport_id, () => {
  if (eventData.airport_id) {
    fetchAirportDisplayName();
  }
}, { immediate: true });
</script>