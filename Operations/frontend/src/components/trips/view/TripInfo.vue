<template>
  <!--begin::Card-->
  <div class="card card-flush pt-3 mb-5 mb-xl-10">
    <!--begin::Card header-->
    <div class="card-header">
      <!--begin::Card title-->
      <div class="card-title">
        <h2>Additional Information</h2>
      </div>
      <!--end::Card title-->
    </div>
    <!--end::Card header-->

    <!--begin::Card body-->
    <div class="card-body pt-0 fs-6">
      <!--begin::Section-->
      <div class="mb-5">
        <!--begin::Item-->
        <div class="d-flex flex-stack mb-3">
          <div class="text-gray-700 fw-semibold fs-6 me-2">Aircraft:</div>
          <div class="text-gray-800 fw-bold fs-6">{{ getAircraft() }}</div>
        </div>
        <!--end::Item-->

        <!--begin::Item-->
        <div class="d-flex flex-stack mb-3">
          <div class="text-gray-700 fw-semibold fs-6 me-2">Tail Number:</div>
          <div class="text-gray-800 fw-bold fs-6">{{ getTailNumber() }}</div>
        </div>
        <!--end::Item-->

        <!--begin::Item-->
        <div class="d-flex flex-stack mb-3" v-if="trip?.pre_flight_duty_time">
          <div class="text-gray-700 fw-semibold fs-6 me-2">Pre-flight Duty:</div>
          <div class="text-gray-800 fw-bold fs-6">{{ formatDuration(trip.pre_flight_duty_time) }}</div>
        </div>
        <!--end::Item-->

        <!--begin::Item-->
        <div class="d-flex flex-stack mb-3" v-if="trip?.post_flight_duty_time">
          <div class="text-gray-700 fw-semibold fs-6 me-2">Post-flight Duty:</div>
          <div class="text-gray-800 fw-bold fs-6">{{ formatDuration(trip.post_flight_duty_time) }}</div>
        </div>
        <!--end::Item-->
      </div>
      <!--end::Section-->

      <!--begin::Notes Section-->
      <div v-if="trip?.notes">
        <div class="separator separator-dashed mb-5"></div>
        <div>
          <h6 class="text-gray-700 fw-semibold mb-3">Notes:</h6>
          <div class="text-gray-800 fs-7">{{ trip.notes }}</div>
        </div>
      </div>
      <!--end::Notes Section-->
    </div>
    <!--end::Card body-->
  </div>
  <!--end::Card-->
</template>

<script setup lang="ts">
interface Props {
  trip: any;
  loading: boolean;
}

const props = defineProps<Props>();

const getAircraft = (): string => {
  if (props.trip?.aircraft) {
    const make = props.trip.aircraft.make || '';
    const model = props.trip.aircraft.model || '';
    return `${make} ${model}`.trim() || 'Not Assigned';
  }
  return 'Not Assigned';
};

const getTailNumber = (): string => {
  return props.trip?.aircraft?.tail_number || 'N/A';
};

const formatDuration = (duration: string): string => {
  if (!duration) return 'N/A';
  
  // Parse duration string (format: "HH:MM:SS" or ISO duration)
  if (typeof duration === 'string') {
    const parts = duration.split(':');
    if (parts.length >= 2) {
      const hours = parseInt(parts[0]);
      const minutes = parseInt(parts[1]);
      if (hours > 0) {
        return `${hours} hour${hours > 1 ? 's' : ''} ${minutes} min`;
      }
      return `${minutes} minutes`;
    }
  }
  return duration;
};
</script>