<template>
  <!--begin::Card-->
  <div class="card card-flush pt-3 mb-5 mb-xl-10">
    <!--begin::Card header-->
    <div class="card-header">
      <!--begin::Card title-->
      <div class="card-title">
        <h2 class="fw-bold">Flight Itinerary</h2>
      </div>
      <!--end::Card title-->

      <!--begin::Card toolbar-->
      <div class="card-toolbar">
        <button class="btn btn-light-primary">
          <KTIcon icon-name="geolocation" icon-class="fs-3" />
          Track Flight
        </button>
      </div>
      <!--end::Card toolbar-->
    </div>
    <!--end::Card header-->

    <!--begin::Card body-->
    <div class="card-body pt-3">
      <!--begin::Timeline-->
      <div class="timeline-wrapper">
        <!--begin::Timeline-->
        <div class="timeline ms-3">
          <!--begin::Timeline item-->
          <div class="timeline-item align-items-center mb-7">
            <!--begin::Timeline line-->
            <div class="timeline-line w-40px mt-6 mb-n12"></div>
            <!--end::Timeline line-->

            <!--begin::Timeline icon-->
            <div class="timeline-icon" style="margin-left: 11px">
              <div class="d-flex align-items-center justify-content-center w-50px h-50px">
                <KTIcon icon-name="geolocation" icon-class="fs-2 text-success" />
              </div>
            </div>
            <!--end::Timeline icon-->

            <!--begin::Timeline content-->
            <div class="timeline-content m-0">
              <!--begin::Label-->
              <span class="fs-8 fw-bolder text-success text-uppercase">Departure</span>
              <!--end::Label-->

              <!--begin::Title-->
              <div class="fs-6 fw-bold text-gray-800">
                {{ getDepartureAirportName() }}
                <span class="text-muted ms-2">({{ trip?.departure_airport }})</span>
              </div>
              <!--end::Title-->

              <!--begin::Details-->
              <div class="fw-semibold text-gray-700 fs-7">
                <div class="mb-2">
                  <strong>Scheduled:</strong> {{ formatDateTime(trip?.estimated_departure_time) }}
                </div>
                <div v-if="trip?.actual_departure_time">
                  <strong>Actual:</strong> {{ formatDateTime(trip?.actual_departure_time) }}
                </div>
              </div>
              <!--end::Details-->
            </div>
            <!--end::Timeline content-->
          </div>
          <!--end::Timeline item-->

          <!--begin::Timeline item-->
          <div class="timeline-item align-items-center">
            <!--begin::Timeline icon-->
            <div class="timeline-icon" style="margin-left: 11px">
              <div class="d-flex align-items-center justify-content-center w-50px h-50px">
                <KTIcon icon-name="airplane" icon-class="fs-2 text-primary" />
              </div>
            </div>
            <!--end::Timeline icon-->

            <!--begin::Timeline content-->
            <div class="timeline-content m-0">
              <!--begin::Label-->
              <span class="fs-8 fw-bolder text-primary text-uppercase">Arrival</span>
              <!--end::Label-->

              <!--begin::Title-->
              <div class="fs-6 fw-bold text-gray-800">
                {{ getArrivalAirportName() }}
                <span class="text-muted ms-2">({{ trip?.arrival_airport }})</span>
              </div>
              <!--end::Title-->

              <!--begin::Details-->
              <div class="fw-semibold text-gray-700 fs-7">
                <div class="mb-2">
                  <strong>Estimated:</strong> {{ formatDateTime(trip?.estimated_arrival_time) }}
                </div>
                <div v-if="trip?.actual_arrival_time">
                  <strong>Actual:</strong> {{ formatDateTime(trip?.actual_arrival_time) }}
                </div>
              </div>
              <!--end::Details-->
            </div>
            <!--end::Timeline content-->
          </div>
          <!--end::Timeline item-->
        </div>
        <!--end::Timeline-->
      </div>
      <!--end::Timeline-->

      <!--begin::Stats-->
      <div class="row g-6 g-xl-9 mt-7">
        <!--begin::Col-->
        <div class="col-sm-6 col-xl-3">
          <div class="border border-dashed border-gray-300 text-center min-w-125px rounded py-3 px-4 me-6 mb-3">
            <span class="fs-6 fw-semibold text-gray-700">Distance</span>
            <div class="fs-2 fw-bold text-gray-800">{{ trip?.distance || 0 }} <span class="fs-7 text-muted">nm</span></div>
          </div>
        </div>
        <!--end::Col-->

        <!--begin::Col-->
        <div class="col-sm-6 col-xl-3">
          <div class="border border-dashed border-gray-300 text-center min-w-125px rounded py-3 px-4 me-6 mb-3">
            <span class="fs-6 fw-semibold text-gray-700">Flight Time</span>
            <div class="fs-2 fw-bold text-gray-800">{{ formatFlightTime() }}</div>
          </div>
        </div>
        <!--end::Col-->

        <!--begin::Col-->
        <div class="col-sm-6 col-xl-3">
          <div class="border border-dashed border-gray-300 text-center min-w-125px rounded py-3 px-4 me-6 mb-3">
            <span class="fs-6 fw-semibold text-gray-700">Fuel Required</span>
            <div class="fs-2 fw-bold text-gray-800">{{ trip?.fuel_required || 0 }} <span class="fs-7 text-muted">lbs</span></div>
          </div>
        </div>
        <!--end::Col-->

        <!--begin::Col-->
        <div class="col-sm-6 col-xl-3">
          <div class="border border-dashed border-gray-300 text-center min-w-125px rounded py-3 px-4 me-6 mb-3">
            <span class="fs-6 fw-semibold text-gray-700">Status</span>
            <div class="fs-2 fw-bold">
              <span :class="`badge badge-light-${getStatusColor()} fs-6`">
                {{ trip?.status || 'Pending' }}
              </span>
            </div>
          </div>
        </div>
        <!--end::Col-->
      </div>
      <!--end::Stats-->

      <!--begin::Weather Info-->
      <div class="mt-10" v-if="showWeatherInfo()">
        <!--begin::Title-->
        <h5 class="mb-4">Weather Conditions</h5>
        <!--end::Title-->

        <!--begin::Weather Cards-->
        <div class="row g-6">
          <!--begin::Departure Weather-->
          <div class="col-md-6">
            <div class="card card-bordered">
              <div class="card-body p-6">
                <div class="d-flex align-items-center mb-3">
                  <KTIcon icon-name="weather-cloudy" icon-class="fs-1 text-primary me-3" />
                  <div>
                    <div class="fw-bold fs-6">{{ trip?.departure_airport }} Weather</div>
                    <div class="text-muted fs-7">Departure Airport</div>
                  </div>
                </div>
                <div class="fs-7 text-gray-700">
                  <div>Visibility: 10+ miles</div>
                  <div>Wind: 10 kts from 270°</div>
                  <div>Ceiling: Clear</div>
                </div>
              </div>
            </div>
          </div>
          <!--end::Departure Weather-->

          <!--begin::Arrival Weather-->
          <div class="col-md-6">
            <div class="card card-bordered">
              <div class="card-body p-6">
                <div class="d-flex align-items-center mb-3">
                  <KTIcon icon-name="weather-sunny" icon-class="fs-1 text-warning me-3" />
                  <div>
                    <div class="fw-bold fs-6">{{ trip?.arrival_airport }} Weather</div>
                    <div class="text-muted fs-7">Arrival Airport</div>
                  </div>
                </div>
                <div class="fs-7 text-gray-700">
                  <div>Visibility: 8 miles</div>
                  <div>Wind: 5 kts from 180°</div>
                  <div>Ceiling: 2,500 ft</div>
                </div>
              </div>
            </div>
          </div>
          <!--end::Arrival Weather-->
        </div>
        <!--end::Weather Cards-->
      </div>
      <!--end::Weather Info-->
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

const getDepartureAirportName = (): string => {
  // In a real app, you'd have a lookup table or API call
  const airportNames: Record<string, string> = {
    'KORD': 'Chicago O\'Hare International',
    'KMDW': 'Chicago Midway International',
    'KLAX': 'Los Angeles International',
    'KJFK': 'John F. Kennedy International',
    'KDEN': 'Denver International',
  };
  return airportNames[props.trip?.departure_airport || ''] || 'Unknown Airport';
};

const getArrivalAirportName = (): string => {
  const airportNames: Record<string, string> = {
    'KORD': 'Chicago O\'Hare International',
    'KMDW': 'Chicago Midway International',
    'KLAX': 'Los Angeles International',
    'KJFK': 'John F. Kennedy International',
    'KDEN': 'Denver International',
  };
  return airportNames[props.trip?.arrival_airport || ''] || 'Unknown Airport';
};

const formatDateTime = (dateString?: string): string => {
  if (!dateString) return 'Not scheduled';
  return new Date(dateString).toLocaleString('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
  });
};

const formatFlightTime = (): string => {
  if (!props.trip?.flight_time) return '0h 0m';
  const hours = Math.floor(props.trip.flight_time / 60);
  const minutes = props.trip.flight_time % 60;
  return `${hours}h ${minutes}m`;
};

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

const showWeatherInfo = (): boolean => {
  return !!(props.trip?.departure_airport && props.trip?.arrival_airport);
};
</script>

<style scoped>
  .timeline-line {
  left: 9px;
  bottom: 10px;
  }
</style>