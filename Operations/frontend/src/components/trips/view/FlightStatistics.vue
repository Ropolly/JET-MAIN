<template>
  <!--begin::Card-->
  <div class="card card-flush pt-3 mb-5 mb-xl-10">
    <!--begin::Card header-->
    <div class="card-header">
      <!--begin::Card title-->
      <div class="card-title">
        <h2 class="fw-bold">Flight Statistics</h2>
      </div>
      <!--end::Card title-->
    </div>
    <!--end::Card header-->

    <!--begin::Card body-->
    <div class="card-body pt-3">
      <div class="row g-6" v-if="getTripLines().length > 0">
        <!--begin::Col-->
        <div class="col-sm-6 col-xl-3">
          <div class="border border-dashed border-gray-300 text-center min-w-125px rounded py-3 px-4">
            <span class="fs-6 fw-semibold text-gray-700">Total Distance</span>
            <div class="fs-2 fw-bold text-gray-800">{{ getTotalDistance() }} <span class="fs-7 text-muted">nm</span></div>
          </div>
        </div>
        <!--end::Col-->

        <!--begin::Col-->
        <div class="col-sm-6 col-xl-3">
          <div class="border border-dashed border-gray-300 text-center min-w-125px rounded py-3 px-4">
            <span class="fs-6 fw-semibold text-gray-700">Total Flight Time</span>
            <div class="fs-2 fw-bold text-gray-800">{{ getTotalFlightTime() }}</div>
          </div>
        </div>
        <!--end::Col-->

        <!--begin::Col-->
        <div class="col-sm-6 col-xl-3">
          <div class="border border-dashed border-gray-300 text-center min-w-125px rounded py-3 px-4">
            <span class="fs-6 fw-semibold text-gray-700">Flight Legs</span>
            <div class="fs-2 fw-bold text-gray-800">{{ getTripLines().length }}</div>
          </div>
        </div>
        <!--end::Col-->

        <!--begin::Col-->
        <div class="col-sm-6 col-xl-3">
          <div class="border border-dashed border-gray-300 text-center min-w-125px rounded py-3 px-4">
            <span class="fs-6 fw-semibold text-gray-700">Trip Status</span>
            <div class="fs-2 fw-bold">
              <span :class="`badge badge-light-${getStatusColor()} fs-6`">
                {{ trip?.status || 'Pending' }}
              </span>
            </div>
          </div>
        </div>
        <!--end::Col-->
      </div>
      
      <!-- Empty state when no trip lines -->
      <div v-else class="text-center py-10">
        <div class="text-muted">No flight statistics available</div>
      </div>
    </div>
    <!--end::Card body-->
  </div>
  <!--end::Card-->
</template>

<script setup lang="ts">
import { calculateTripDistance, formatDistance } from '@/core/helpers/distanceCalculator';

interface Props {
  trip: any;
  loading: boolean;
}

const props = defineProps<Props>();

// Get trip lines from the trip
const getTripLines = (): any[] => {
  return props.trip?.trip_lines || [];
};

// Calculate total distance from all trip lines using coordinates
const getTotalDistance = (): string => {
  const tripLines = getTripLines();
  const totalDistance = calculateTripDistance(tripLines);
  return formatDistance(totalDistance, false);
};

// Calculate total flight time from all trip lines
const getTotalFlightTime = (): string => {
  const tripLines = getTripLines();
  let totalMinutes = 0;
  
  tripLines.forEach(line => {
    if (line.flight_time) {
      // Parse flight_time which might be in format "HH:MM:SS" or minutes
      if (typeof line.flight_time === 'string' && line.flight_time.includes(':')) {
        const parts = line.flight_time.split(':');
        const hours = parseInt(parts[0]) || 0;
        const minutes = parseInt(parts[1]) || 0;
        totalMinutes += hours * 60 + minutes;
      } else if (typeof line.flight_time === 'number') {
        totalMinutes += line.flight_time;
      } else {
        totalMinutes += parseInt(line.flight_time) || 0;
      }
    }
  });
  
  if (totalMinutes === 0) return 'TBD';
  
  const hours = Math.floor(totalMinutes / 60);
  const minutes = totalMinutes % 60;
  
  if (hours === 0) {
    return `${minutes}m`;
  }
  return `${hours}h ${minutes}m`;
};

// Get status color based on trip status
const getStatusColor = (): string => {
  const status = props.trip?.status?.toLowerCase();
  switch (status) {
    case 'completed': return 'success';
    case 'active': case 'in_progress': return 'primary';
    case 'cancelled': return 'danger';
    case 'pending': return 'warning';
    default: return 'secondary';
  }
};
</script>