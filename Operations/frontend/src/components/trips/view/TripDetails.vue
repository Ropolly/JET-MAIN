<template>
  <!--begin::Card-->
  <div class="card card-flush pt-3 mb-5 mb-xl-10">
    <!--begin::Card header-->
    <div class="card-header">
      <!--begin::Card title-->
      <div class="card-title">
        <h2 class="fw-bold">Trip Details</h2>
      </div>
      <!--end::Card title-->

      <!--begin::Card toolbar-->
      <div class="card-toolbar">
        <button class="btn btn-light-primary me-3">
          <KTIcon icon-name="pencil" icon-class="fs-3" />
          Edit Trip
        </button>
        <button class="btn btn-primary">
          <KTIcon icon-name="printer" icon-class="fs-3" />
          Generate Manifest
        </button>
      </div>
      <!--end::Card toolbar-->
    </div>
    <!--end::Card header-->

    <!--begin::Card body-->
    <div class="card-body pt-3">
      <!--begin::Section-->
      <div class="mb-10">
        <!--begin::Title-->
        <h5 class="mb-4">Patient Information:</h5>
        <!--end::Title-->

        <!--begin::Details-->
        <div class="row g-6">
          <!--begin::Col-->
          <div class="col-lg-6">
            <!--begin::Details-->
            <div class="table-responsive">
              <table class="table align-middle fs-6 fw-semibold">
                <tbody>
                  <!--begin::Row-->
                  <tr>
                    <td class="text-gray-600 pe-4" style="width: 40%;">Patient Name:</td>
                    <td class="text-gray-800 fw-bold">{{ getPatientName() }}</td>
                  </tr>
                  <!--end::Row-->

                  <!--begin::Row-->
                  <tr>
                    <td class="text-gray-600 pe-4">Date of Birth:</td>
                    <td class="text-gray-800 fw-bold">{{ formatDate(trip?.patient?.date_of_birth) || 'Not specified' }}</td>
                  </tr>
                  <!--end::Row-->

                  <!--begin::Row-->
                  <tr>
                    <td class="text-gray-600 pe-4">Special Instructions:</td>
                    <td class="text-gray-800 fw-bold">{{ trip?.patient?.special_instructions || trip?.notes || 'None' }}</td>
                  </tr>
                  <!--end::Row-->

                  <!--begin::Row-->
                  <tr>
                    <td class="text-gray-600 pe-4">Contact:</td>
                    <td class="text-gray-800 fw-bold">{{ trip?.patient?.info?.phone || 'Not provided' }}</td>
                  </tr>
                  <!--end::Row-->
                </tbody>
              </table>
            </div>
            <!--end::Details-->
          </div>
          <!--end::Col-->

          <!--begin::Col-->
          <div class="col-lg-6">
            <!--begin::Details-->
            <div class="table-responsive">
              <table class="table align-middle fs-6 fw-semibold">
                <tbody>
                  <!--begin::Row-->
                  <tr>
                    <td class="text-gray-600 pe-4" style="width: 40%;">Trip Type:</td>
                    <td class="text-gray-800 fw-bold">{{ formatTripType(trip?.type) }}</td>
                  </tr>
                  <!--end::Row-->

                  <!--begin::Row-->
                  <tr>
                    <td class="text-gray-600 pe-4">Service Level:</td>
                    <td class="text-gray-800 fw-bold">{{ trip?.service_level || 'Standard' }}</td>
                  </tr>
                  <!--end::Row-->

                  <!--begin::Row-->
                  <tr>
                    <td class="text-gray-600 pe-4">Priority:</td>
                    <td class="text-gray-800">
                      <span :class="`badge badge-light-${getPriorityColor()} fs-7`">
                        {{ trip?.priority || 'Normal' }}
                      </span>
                    </td>
                  </tr>
                  <!--end::Row-->

                  <!--begin::Row-->
                  <tr>
                    <td class="text-gray-600 pe-4">Created By:</td>
                    <td class="text-gray-800 fw-bold">{{ trip?.created_by || 'System' }}</td>
                  </tr>
                  <!--end::Row-->
                </tbody>
              </table>
            </div>
            <!--end::Details-->
          </div>
          <!--end::Col-->
        </div>
        <!--end::Details-->
      </div>
      <!--end::Section-->

      <!--begin::Section-->
      <div class="mb-0" v-if="trip?.notes">
        <!--begin::Title-->
        <h5 class="mb-4">Additional Notes:</h5>
        <!--end::Title-->

        <!--begin::Notes-->
        <div class="p-5 bg-light-info rounded border-info border border-dashed">
          <div class="text-gray-700 fw-semibold fs-6">
            {{ trip.notes }}
          </div>
        </div>
        <!--end::Notes-->
      </div>
      <!--end::Section-->
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

const getPatientName = (): string => {
  if (props.trip?.patient?.info) {
    const first = props.trip.patient.info.first_name || '';
    const last = props.trip.patient.info.last_name || '';
    return `${first} ${last}`.trim() || 'Unknown Patient';
  }
  return 'No Patient Assigned';
};

const getPriorityColor = (): string => {
  const priority = props.trip?.priority?.toLowerCase();
  switch (priority) {
    case 'emergency': case 'critical': return 'danger';
    case 'urgent': return 'warning';
    case 'routine': case 'normal': return 'success';
    default: return 'secondary';
  }
};

const formatDate = (dateString?: string): string => {
  if (!dateString) return 'Not specified';
  return new Date(dateString).toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
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
</script>