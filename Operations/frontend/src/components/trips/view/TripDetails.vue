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
        <div class="d-flex flex-wrap py-5">
          <!--begin::Row-->
          <div class="flex-equal me-5">
            <!--begin::Details-->
            <table class="table fs-6 fw-semibold gs-0 gy-2 gx-2 m-0">
              <!--begin::Row-->
              <tr>
                <td class="text-gray-500 min-w-175px w-175px">Patient Name:</td>
                <td class="text-gray-800 min-w-200px">
                  <span class="text-gray-800">
                    {{ getPatientName() }}
                  </span>
                </td>
              </tr>
              <!--end::Row-->

              <!--begin::Row-->
              <tr>
                <td class="text-gray-500">Date of Birth:</td>
                <td class="text-gray-800">{{ trip?.patient?.date_of_birth || 'Not specified' }}</td>
              </tr>
              <!--end::Row-->

              <!--begin::Row-->
              <tr>
                <td class="text-gray-500">Medical Condition:</td>
                <td class="text-gray-800">
                  {{ trip?.patient?.medical_condition || trip?.notes || 'Not specified' }}
                </td>
              </tr>
              <!--end::Row-->

              <!--begin::Row-->
              <tr>
                <td class="text-gray-500">Contact:</td>
                <td class="text-gray-800">{{ trip?.patient?.phone || 'Not specified' }}</td>
              </tr>
              <!--end::Row-->
            </table>
            <!--end::Details-->
          </div>
          <!--end::Row-->

          <!--begin::Row-->
          <div class="flex-equal">
            <!--begin::Details-->
            <table class="table fs-6 fw-semibold gs-0 gy-2 gx-2 m-0">
              <!--begin::Row-->
              <tr>
                <td class="text-gray-500 min-w-175px w-175px">Trip Type:</td>
                <td class="text-gray-800 min-w-200px">
                  <span class="text-gray-800">{{ trip?.type || 'Not specified' }}</span>
                </td>
              </tr>
              <!--end::Row-->

              <!--begin::Row-->
              <tr>
                <td class="text-gray-500">Service Level:</td>
                <td class="text-gray-800">{{ trip?.service_level || 'Standard' }}</td>
              </tr>
              <!--end::Row-->

              <!--begin::Row-->
              <tr>
                <td class="text-gray-500">Priority:</td>
                <td class="text-gray-800">
                  <span :class="`badge badge-light-${getPriorityColor()} fs-7`">
                    {{ trip?.priority || 'Normal' }}
                  </span>
                </td>
              </tr>
              <!--end::Row-->

              <!--begin::Row-->
              <tr>
                <td class="text-gray-500">Created By:</td>
                <td class="text-gray-800">{{ trip?.created_by || 'System' }}</td>
              </tr>
              <!--end::Row-->
            </table>
            <!--end::Details-->
          </div>
          <!--end::Row-->
        </div>
        <!--end::Details-->
      </div>
      <!--end::Section-->

      <!--begin::Section-->
      <div class="mb-10">
        <!--begin::Title-->
        <h5 class="mb-4">Medical Requirements:</h5>
        <!--end::Title-->

        <!--begin::Equipment List-->
        <div class="d-flex flex-wrap gap-3">
          <span class="badge badge-light-info fs-7 fw-bold">
            <KTIcon icon-name="medical-08" icon-class="fs-6 me-1" />
            Oxygen Supply
          </span>
          <span class="badge badge-light-success fs-7 fw-bold">
            <KTIcon icon-name="heart" icon-class="fs-6 me-1" />
            Cardiac Monitor
          </span>
          <span class="badge badge-light-warning fs-7 fw-bold">
            <KTIcon icon-name="pill" icon-class="fs-6 me-1" />
            IV Pump
          </span>
          <span class="badge badge-light-primary fs-7 fw-bold">
            <KTIcon icon-name="user-square" icon-class="fs-6 me-1" />
            Stretcher Configuration
          </span>
        </div>
        <!--end::Equipment List-->
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
  if (props.trip?.patient) {
    const first = props.trip.patient.first_name || '';
    const last = props.trip.patient.last_name || '';
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
</script>