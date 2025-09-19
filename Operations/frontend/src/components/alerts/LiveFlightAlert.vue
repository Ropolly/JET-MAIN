<template>
  <div v-if="liveFlights.length > 0" class="mb-5">
    <div
      v-for="flight in liveFlights"
      :key="flight.trip_id"
      class="alert alert-info d-flex align-items-center border border-info border-dashed rounded mb-3"
      :class="getAlertColorClass(flight.phase)"
    >
      <!--begin::Icon-->
      <div class="me-4">
        <i class="ki-duotone ki-airplane fs-2x" :class="getPhaseIconClass(flight.phase)">
          <span class="path1"></span>
          <span class="path2"></span>
        </i>
      </div>
      <!--end::Icon-->

      <!--begin::Content-->
      <div class="flex-grow-1">
        <!--begin::Header-->
        <div class="d-flex align-items-center justify-content-between mb-2">
          <div class="d-flex align-items-center">
            <h5 class="mb-0 me-3">
              <strong>{{ flight.aircraft_tail }}</strong> - Trip {{ flight.trip_number }}
            </h5>
            <span
              class="badge fs-7 me-2"
              :class="getPhaseStatusClass(flight.phase)"
            >
              {{ flight.phase.toUpperCase() }}
            </span>
            <span class="badge badge-light-secondary fs-8">
              {{ flight.trip_type }}
            </span>
          </div>

          <!--begin::Progress-->
          <div class="text-end">
            <div class="text-muted fs-8 mb-1">
              {{ flight.progress_percentage }}% Complete
            </div>
            <div class="progress" style="height: 4px; width: 80px;">
              <div
                class="progress-bar"
                role="progressbar"
                :style="`width: ${flight.progress_percentage}%`"
                :class="getProgressBarClass(flight.phase)"
                :aria-valuenow="flight.progress_percentage"
                aria-valuemin="0"
                aria-valuemax="100"
              ></div>
            </div>
          </div>
          <!--end::Progress-->
        </div>
        <!--end::Header-->

        <!--begin::Flight Details-->
        <div class="d-flex align-items-center justify-content-between">
          <div class="d-flex align-items-center">
            <span class="fw-bold text-gray-800 me-2">{{ flight.origin_airport.ident }}</span>
            <i class="fas fa-arrow-right text-muted mx-2"></i>
            <span class="fw-bold text-gray-800 me-4">{{ flight.destination_airport.ident }}</span>

            <div class="text-muted fs-7 me-4">
              <div>Departed: {{ formatLocalTime(flight.departure_time_local) }}</div>
              <div>ETA: {{ formatLocalTime(flight.arrival_time_local) }}</div>
            </div>

            <div v-if="flight.patient_name" class="text-muted fs-7">
              Patient: {{ flight.patient_name }}
            </div>
          </div>

          <!--begin::Time Remaining-->
          <div class="text-end">
            <div class="text-gray-700 fw-bold fs-7">
              {{ getRemainingTimeText(flight.remaining_minutes) }}
            </div>
            <div class="text-muted fs-8">
              remaining
            </div>
          </div>
          <!--end::Time Remaining-->
        </div>
        <!--end::Flight Details-->
      </div>
      <!--end::Content-->

      <!--begin::Action-->
      <div class="ms-3">
        <router-link
          :to="`/admin/trips/${flight.trip_id}`"
          class="btn btn-sm btn-light-primary"
        >
          View Trip
        </router-link>
      </div>
      <!--end::Action-->
    </div>

    <!--begin::Auto-refresh indicator-->
    <div class="d-flex justify-content-between align-items-center text-muted fs-8 mb-3">
      <span>{{ liveFlights.length }} live flight{{ liveFlights.length !== 1 ? 's' : '' }}</span>
      <span v-if="lastUpdated">
        Last updated: {{ formatTime(lastUpdated) }}
        <span v-if="autoRefresh" class="text-success">
          <i class="fas fa-sync-alt fa-spin ms-1"></i>
          Auto-refreshing
        </span>
      </span>
    </div>
    <!--end::Auto-refresh indicator-->
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted } from 'vue';
import { format } from 'date-fns';
import ApiService from '@/core/services/ApiService';

// Props
interface LiveFlight {
  trip_id: string;
  trip_number: string;
  aircraft_tail: string;
  origin_airport: {
    ident: string;
    name: string;
  };
  destination_airport: {
    ident: string;
    name: string;
  };
  departure_time_local: string;
  arrival_time_local: string;
  estimated_arrival_utc: string;
  phase: 'departed' | 'enroute' | 'approaching';
  phase_icon: string;
  progress_percentage: number;
  remaining_minutes: number;
  patient_name?: string;
  trip_type: string;
}

interface LiveFlightsResponse {
  live_flights: LiveFlight[];
  count: number;
  timestamp: string;
}

// Reactive data
const liveFlights = ref<LiveFlight[]>([]);
const lastUpdated = ref<Date | null>(null);
const autoRefresh = ref(true);
const refreshInterval = ref<number | null>(null);

// Props (with defaults)
interface Props {
  refreshIntervalSeconds?: number;
  showAutoRefresh?: boolean;
}

const props = withDefaults(defineProps<Props>(), {
  refreshIntervalSeconds: 60, // 1 minute default
  showAutoRefresh: true
});

// Methods
const fetchLiveFlights = async () => {
  try {
    const response = await ApiService.get('/trips/live/');
    const data: LiveFlightsResponse = response.data;

    liveFlights.value = data.live_flights;
    lastUpdated.value = new Date();
  } catch (error) {
    console.error('Error fetching live flights:', error);
    // Don't show error to user for auto-refresh failures
  }
};

const getAlertColorClass = (phase: string) => {
  switch (phase) {
    case 'departed':
      return 'alert-warning border-warning';
    case 'approaching':
      return 'alert-success border-success';
    default: // enroute
      return 'alert-info border-info';
  }
};

const getPhaseStatusClass = (phase: string) => {
  switch (phase) {
    case 'departed':
      return 'badge-warning';
    case 'approaching':
      return 'badge-success';
    default: // enroute
      return 'badge-info';
  }
};

const getProgressBarClass = (phase: string) => {
  switch (phase) {
    case 'departed':
      return 'bg-warning';
    case 'approaching':
      return 'bg-success';
    default: // enroute
      return 'bg-info';
  }
};

const getPhaseIconClass = (phase: string) => {
  switch (phase) {
    case 'departed':
      return 'text-warning';
    case 'approaching':
      return 'text-success';
    default: // enroute
      return 'text-info';
  }
};

const formatLocalTime = (timeString: string) => {
  try {
    const date = new Date(timeString);
    return format(date, 'MMM d, h:mm a');
  } catch (error) {
    return timeString;
  }
};

const formatTime = (date: Date) => {
  return format(date, 'h:mm:ss a');
};

const getRemainingTimeText = (minutes: number) => {
  if (minutes < 60) {
    return `${Math.round(minutes)}m`;
  } else {
    const hours = Math.floor(minutes / 60);
    const remainingMinutes = Math.round(minutes % 60);
    return `${hours}h ${remainingMinutes}m`;
  }
};

const startAutoRefresh = () => {
  if (props.refreshIntervalSeconds > 0) {
    refreshInterval.value = window.setInterval(
      fetchLiveFlights,
      props.refreshIntervalSeconds * 1000
    );
  }
};

const stopAutoRefresh = () => {
  if (refreshInterval.value) {
    clearInterval(refreshInterval.value);
    refreshInterval.value = null;
  }
};

// Lifecycle
onMounted(() => {
  fetchLiveFlights();
  if (props.showAutoRefresh) {
    startAutoRefresh();
  }
});

onUnmounted(() => {
  stopAutoRefresh();
});

// Expose methods for parent component use
defineExpose({
  refresh: fetchLiveFlights,
  startAutoRefresh,
  stopAutoRefresh
});
</script>

<style scoped>
.progress {
  background-color: rgba(0, 0, 0, 0.1);
}

.alert {
  border-width: 1px;
}

.fs-2x {
  font-size: 2rem;
}
</style>