<template>
  <!--begin::Card-->
  <div class="card card-flush pt-3 mb-5 mb-xl-10">
    <!--begin::Card header-->
    <div class="card-header">
      <!--begin::Card title-->
      <div class="card-title">
        <h2 class="fw-bold">Trip Summary</h2>
      </div>
      <!--end::Card title-->
    </div>
    <!--end::Card header-->

    <!--begin::Card body-->
    <div class="card-body pt-3">
      <div class="row g-5">
        <!--begin::Col - Trip Info-->
        <div class="col-4">
          <div class="position-relative ps-6 py-3">
            <!--begin::Bar-->
            <div class="position-absolute h-100 w-4px rounded top-0 start-0 bg-light-secondary"></div>
            <!--end::Bar-->
            <div class="fs-6 fw-semibold text-gray-700">Trip <span class="fw-bold">{{ trip?.trip_number || '-' }}</span></div>
            <div class="fs-7 text-muted">Created {{ formatDate(trip?.created_on) }}</div>
          </div>
        </div>
        <!--end::Col-->

        <!--begin::Col - Patient Info-->
        <div class="col-4">
          <div class="position-relative ps-6 py-3">
            <!--begin::Bar-->
            <div class="position-absolute h-100 w-4px rounded top-0 start-0 bg-light-secondary"></div>
            <!--end::Bar-->
            <div class="fs-6 fw-semibold text-gray-700"><span class="fw-bold">{{ getPatientName() }}</span></div>
            <div class="fs-7 text-muted">Patient</div>
          </div>
        </div>
        <!--end::Col-->

        <!--begin::Col - Trip Type & Status-->
        <div class="col-4">
          <div class="position-relative ps-6 py-3">
            <!--begin::Bar-->
            <div class="position-absolute h-100 w-4px rounded top-0 start-0 bg-light-secondary"></div>
            <!--end::Bar-->
            <div class="fs-6 fw-semibold text-gray-700"><span class="fw-bold">{{ formatTripType(trip?.type) }}</span></div>
            <div class="fs-7 text-muted">
              <span :class="`badge badge-light-${getStatusColor()} fs-7`">
                {{ trip?.status || 'Pending' }}
              </span>
            </div>
          </div>
        </div>
        <!--end::Col-->
      </div>
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
  if (props.trip?.patient?.info) {
    const first = props.trip.patient.info.first_name?.charAt(0) || '';
    const last = props.trip.patient.info.last_name?.charAt(0) || '';
    return (first + last).toUpperCase() || 'P';
  }
  return 'P';
};

const getPatientName = (): string => {
  if (props.trip?.patient?.info) {
    const first = props.trip.patient.info.first_name || '';
    const last = props.trip.patient.info.last_name || '';
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

const formatDate = (dateString?: string): string => {
  if (!dateString) return '-';
  return new Date(dateString).toLocaleDateString('en-US', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
  });
};

// Format trip type to title case
const formatTripType = (type?: string): string => {
  if (!type) return 'Medical Transport';
  
  // Handle special cases
  const typeMap: { [key: string]: string } = {
    'medical': 'Medical Transport',
    'charter': 'Charter',
    'part 91': 'Part 91',
    'part_91': 'Part 91',
    'maintenance': 'Maintenance',
    'other': 'Other'
  };
  
  const lowerType = type.toLowerCase();
  if (typeMap[lowerType]) {
    return typeMap[lowerType];
  }
  
  // Default: convert to title case
  return type.split(/[_\s]+/)
    .map(word => word.charAt(0).toUpperCase() + word.slice(1).toLowerCase())
    .join(' ');
};

const viewPatient = () => {
  if (props.trip?.patient?.id) {
    window.open(`/admin/contacts/patients/${props.trip.patient.id}`, '_blank');
  }
};
</script>