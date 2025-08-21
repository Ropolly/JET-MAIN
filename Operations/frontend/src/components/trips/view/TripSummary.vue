<template>
  <!--begin::Card-->
  <div
    class="card card-flush mb-0"
    id="kt_trip_summary"
    data-kt-sticky="true"
    data-kt-sticky-name="trip-summary"
    data-kt-sticky-offset="{default: false, lg: '200px'}"
    data-kt-sticky-width="{lg: '250px', xl: '300px'}"
    data-kt-sticky-left="auto"
    data-kt-sticky-top="150px"
    data-kt-sticky-animation="false"
    data-kt-sticky-zindex="95"
  >
    <!--begin::Card header-->
    <div class="card-header">
      <!--begin::Card title-->
      <div class="card-title">
        <h2>Trip Summary</h2>
      </div>
      <!--end::Card title-->

      <!--begin::Card toolbar-->
      <div class="card-toolbar">
        <a
          href="#"
          class="btn btn-sm btn-light btn-icon"
          data-kt-menu-trigger="click"
          data-kt-menu-placement="bottom-end"
        >
          <KTIcon icon-name="dots-horizontal" icon-class="fs-3" />
        </a>
        <!--begin::Menu-->
        <div
          class="menu menu-sub menu-sub-dropdown menu-column menu-rounded menu-gray-600 menu-state-bg-light-primary fw-semibold fs-7 w-200px py-4"
          data-kt-menu="true"
        >
          <div class="menu-item px-3">
            <a href="#" class="menu-link px-3">Edit Trip</a>
          </div>
          <div class="menu-item px-3">
            <a href="#" class="menu-link px-3">Duplicate Trip</a>
          </div>
          <div class="menu-item px-3">
            <a href="#" class="menu-link px-3">Generate Manifest</a>
          </div>
          <div class="separator my-2"></div>
          <div class="menu-item px-3">
            <a href="#" class="menu-link px-3 text-danger">Cancel Trip</a>
          </div>
        </div>
        <!--end::Menu-->
      </div>
      <!--end::Card toolbar-->
    </div>
    <!--end::Card header-->

    <!--begin::Card body-->
    <div class="card-body pt-0 fs-6">
      <!--begin::Patient Section-->
      <div class="mb-7" v-if="trip?.patient">
        <!--begin::Details-->
        <div class="d-flex align-items-center">
          <!--begin::Avatar-->
          <div class="symbol symbol-60px symbol-circle me-3">
            <div class="symbol-label bg-light-primary">
              <span class="text-primary fw-bold fs-3">
                {{ getPatientInitials() }}
              </span>
            </div>
          </div>
          <!--end::Avatar-->

          <!--begin::Info-->
          <div class="d-flex flex-column">
            <!--begin::Name-->
            <a
              href="#"
              class="fs-4 fw-bold text-gray-900 text-hover-primary me-2"
            >
              {{ getPatientName() }}
            </a>
            <!--end::Name-->

            <!--begin::Details-->
            <span class="fw-semibold text-gray-600">Patient</span>
            <!--end::Details-->
          </div>
          <!--end::Info-->
        </div>
        <!--end::Details-->
      </div>
      <!--end::Patient Section-->

      <!--begin::Separator-->
      <div class="separator separator-dashed mb-7"></div>
      <!--end::Separator-->

      <!--begin::Trip Status-->
      <div class="mb-7">
        <!--begin::Title-->
        <h5 class="mb-3">Trip Status</h5>
        <!--end::Title-->

        <!--begin::Badge-->
        <div class="mb-5">
          <span :class="`badge badge-light-${getStatusColor()} fs-base`">
            <KTIcon icon-name="abstract-24" icon-class="fs-7 me-2" />
            {{ trip?.status || 'Unknown' }}
          </span>
        </div>
        <!--end::Badge-->
      </div>
      <!--end::Trip Status-->

      <!--begin::Trip Details-->
      <div class="mb-7">
        <!--begin::Title-->
        <h5 class="mb-3">Trip Details</h5>
        <!--end::Title-->

        <!--begin::Details-->
        <div class="mb-0">
          <!--begin::Item-->
          <div class="d-flex flex-stack mb-3">
            <div class="text-gray-700 fw-semibold fs-6 me-2">Trip Number:</div>
            <div class="text-gray-800 fw-bold fs-6">{{ trip?.trip_number || '-' }}</div>
          </div>
          <!--end::Item-->

          <!--begin::Item-->
          <div class="d-flex flex-stack mb-3">
            <div class="text-gray-700 fw-semibold fs-6 me-2">Type:</div>
            <div class="text-gray-800 fw-bold fs-6">{{ trip?.type || '-' }}</div>
          </div>
          <!--end::Item-->

          <!--begin::Item-->
          <div class="d-flex flex-stack mb-3">
            <div class="text-gray-700 fw-semibold fs-6 me-2">Priority:</div>
            <div class="text-gray-800 fw-bold fs-6">{{ trip?.priority || 'Normal' }}</div>
          </div>
          <!--end::Item-->

          <!--begin::Item-->
          <div class="d-flex flex-stack mb-3">
            <div class="text-gray-700 fw-semibold fs-6 me-2">Created:</div>
            <div class="text-gray-800 fw-bold fs-6">{{ formatDate(trip?.created_on) }}</div>
          </div>
          <!--end::Item-->
        </div>
        <!--end::Details-->
      </div>
      <!--end::Trip Details-->

      <!--begin::Progress-->
      <div class="mb-7">
        <!--begin::Title-->
        <h5 class="mb-3">Progress</h5>
        <!--end::Title-->

        <!--begin::Progress-->
        <div class="h-8px bg-light rounded mb-3">
          <div
            class="bg-primary rounded h-8px"
            role="progressbar"
            :style="`width: ${getProgressPercentage()}%`"
            :aria-valuenow="getProgressPercentage()"
            aria-valuemin="0"
            aria-valuemax="100"
          ></div>
        </div>
        <!--end::Progress-->

        <!--begin::Stats-->
        <div class="fw-semibold text-gray-600 fs-7">{{ getProgressText() }}</div>
        <!--end::Stats-->
      </div>
      <!--end::Progress-->
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

const getPatientInitials = (): string => {
  if (props.trip?.patient) {
    const first = props.trip.patient.first_name?.charAt(0) || '';
    const last = props.trip.patient.last_name?.charAt(0) || '';
    return (first + last).toUpperCase() || 'P';
  }
  return 'P';
};

const getPatientName = (): string => {
  if (props.trip?.patient) {
    const first = props.trip.patient.first_name || '';
    const last = props.trip.patient.last_name || '';
    return `${first} ${last}`.trim() || 'Unknown Patient';
  }
  return 'No Patient Assigned';
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

const getProgressPercentage = (): number => {
  const status = props.trip?.status?.toLowerCase();
  switch (status) {
    case 'pending': return 25;
    case 'confirmed': return 50;
    case 'in_progress': case 'active': return 75;
    case 'completed': return 100;
    case 'cancelled': return 0;
    default: return 0;
  }
};

const getProgressText = (): string => {
  const status = props.trip?.status?.toLowerCase();
  switch (status) {
    case 'pending': return 'Trip scheduled, awaiting confirmation';
    case 'confirmed': return 'Trip confirmed, preparing for departure';
    case 'in_progress': case 'active': return 'Trip in progress';
    case 'completed': return 'Trip completed successfully';
    case 'cancelled': return 'Trip has been cancelled';
    default: return 'Status unknown';
  }
};

const formatDate = (dateString?: string): string => {
  if (!dateString) return '-';
  return new Date(dateString).toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
  });
};
</script>