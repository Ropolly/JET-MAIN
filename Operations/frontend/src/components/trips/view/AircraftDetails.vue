<template>
  <!--begin::Card-->
  <div class="card card-flush pt-3 mb-5 mb-xl-10">
    <!--begin::Card header-->
    <div class="card-header">
      <!--begin::Card title-->
      <div class="card-title">
        <h2 class="fw-bold">Aircraft & Crew</h2>
      </div>
      <!--end::Card title-->

      <!--begin::Card toolbar-->
      <div class="card-toolbar">
        <button class="btn btn-light-primary">
          <KTIcon icon-name="airplane" icon-class="fs-3" />
          View Aircraft Details
        </button>
      </div>
      <!--end::Card toolbar-->
    </div>
    <!--end::Card header-->

    <!--begin::Card body-->
    <div class="card-body pt-3">
      <!--begin::Aircraft Section-->
      <div class="mb-10">
        <!--begin::Title-->
        <h5 class="mb-4">Aircraft Information:</h5>
        <!--end::Title-->

        <!--begin::Aircraft Card-->
        <div class="card card-bordered mb-6">
          <div class="card-body p-6">
            <div class="d-flex align-items-center">
              <!--begin::Aircraft Icon-->
              <div class="symbol symbol-60px symbol-circle me-4">
                <div class="symbol-label bg-light-primary">
                  <KTIcon icon-name="airplane" icon-class="fs-1 text-primary" />
                </div>
              </div>
              <!--end::Aircraft Icon-->

              <!--begin::Aircraft Info-->
              <div class="flex-grow-1">
                <div class="d-flex flex-wrap align-items-center mb-2">
                  <div class="fs-4 fw-bold text-gray-900 me-4">
                    {{ getAircraftRegistration() }}
                  </div>
                  <span class="badge badge-light-success fs-7">Available</span>
                </div>
                <div class="fs-6 fw-semibold text-gray-700 mb-1">
                  {{ getAircraftModel() }}
                </div>
                <div class="fs-7 text-gray-600">
                  Last Inspection: {{ getLastInspectionDate() }}
                </div>
              </div>
              <!--end::Aircraft Info-->

              <!--begin::Aircraft Stats-->
              <div class="text-end">
                <div class="fs-7 text-gray-600 mb-1">Max Range</div>
                <div class="fs-6 fw-bold text-gray-900">{{ getAircraftRange() }}</div>
              </div>
              <!--end::Aircraft Stats-->
            </div>
          </div>
        </div>
        <!--end::Aircraft Card-->

        <!--begin::Aircraft Specs-->
        <div class="row g-6">
          <!--begin::Spec-->
          <div class="col-md-3">
            <div class="border border-dashed border-gray-300 text-center min-w-125px rounded py-3 px-4">
              <span class="fs-7 fw-semibold text-gray-700 d-block mb-1">Max Passengers</span>
              <div class="fs-6 fw-bold text-gray-800">{{ getAircraftCapacity() }}</div>
            </div>
          </div>
          <!--end::Spec-->

          <!--begin::Spec-->
          <div class="col-md-3">
            <div class="border border-dashed border-gray-300 text-center min-w-125px rounded py-3 px-4">
              <span class="fs-7 fw-semibold text-gray-700 d-block mb-1">Cruise Speed</span>
              <div class="fs-6 fw-bold text-gray-800">{{ getAircraftSpeed() }}</div>
            </div>
          </div>
          <!--end::Spec-->

          <!--begin::Spec-->
          <div class="col-md-3">
            <div class="border border-dashed border-gray-300 text-center min-w-125px rounded py-3 px-4">
              <span class="fs-7 fw-semibold text-gray-700 d-block mb-1">Medical Config</span>
              <div class="fs-6 fw-bold text-gray-800">{{ getMedicalConfig() }}</div>
            </div>
          </div>
          <!--end::Spec-->

          <!--begin::Spec-->
          <div class="col-md-3">
            <div class="border border-dashed border-gray-300 text-center min-w-125px rounded py-3 px-4">
              <span class="fs-7 fw-semibold text-gray-700 d-block mb-1">Fuel Capacity</span>
              <div class="fs-6 fw-bold text-gray-800">{{ getFuelCapacity() }}</div>
            </div>
          </div>
          <!--end::Spec-->
        </div>
        <!--end::Aircraft Specs-->
      </div>
      <!--end::Aircraft Section-->

      <!--begin::Crew Section-->
      <div class="mb-10">
        <!--begin::Title-->
        <h5 class="mb-4">Flight Crew:</h5>
        <!--end::Title-->

        <!--begin::Crew List-->
        <div class="row g-6">
          <!--begin::Pilot in Command-->
          <div class="col-md-6">
            <div class="d-flex align-items-center p-4 bg-light-primary rounded">
              <div class="symbol symbol-45px me-3">
                <div class="symbol-label bg-primary">
                  <span class="text-white fw-bold fs-6">JS</span>
                </div>
              </div>
              <div class="flex-grow-1">
                <div class="fw-bold text-gray-900 fs-6">Capt. John Smith</div>
                <div class="text-gray-700 fs-7">Pilot in Command (PIC)</div>
                <div class="text-gray-600 fs-8">ATP, Type Rated</div>
              </div>
              <div class="text-end">
                <span class="badge badge-light-success fs-8">Active</span>
              </div>
            </div>
          </div>
          <!--end::Pilot in Command-->

          <!--begin::Second in Command-->
          <div class="col-md-6">
            <div class="d-flex align-items-center p-4 bg-light-info rounded">
              <div class="symbol symbol-45px me-3">
                <div class="symbol-label bg-info">
                  <span class="text-white fw-bold fs-6">SJ</span>
                </div>
              </div>
              <div class="flex-grow-1">
                <div class="fw-bold text-gray-900 fs-6">Sarah Johnson</div>
                <div class="text-gray-700 fs-7">Second in Command (SIC)</div>
                <div class="text-gray-600 fs-8">Commercial, Multi-Engine</div>
              </div>
              <div class="text-end">
                <span class="badge badge-light-success fs-8">Active</span>
              </div>
            </div>
          </div>
          <!--end::Second in Command-->
        </div>
        <!--end::Crew List-->
      </div>
      <!--end::Crew Section-->

      <!--begin::Medical Crew Section-->
      <div class="mb-0">
        <!--begin::Title-->
        <h5 class="mb-4">Medical Crew:</h5>
        <!--end::Title-->

        <!--begin::Medical Crew List-->
        <div class="row g-6">
          <!--begin::Flight Nurse-->
          <div class="col-md-6">
            <div class="d-flex align-items-center p-4 bg-light-success rounded">
              <div class="symbol symbol-45px me-3">
                <div class="symbol-label bg-success">
                  <KTIcon icon-name="medical-08" icon-class="fs-3 text-white" />
                </div>
              </div>
              <div class="flex-grow-1">
                <div class="fw-bold text-gray-900 fs-6">Jennifer White, RN</div>
                <div class="text-gray-700 fs-7">Flight Nurse</div>
                <div class="text-gray-600 fs-8">CEN, CFRN Certified</div>
              </div>
              <div class="text-end">
                <span class="badge badge-light-success fs-8">On Duty</span>
              </div>
            </div>
          </div>
          <!--end::Flight Nurse-->

          <!--begin::Flight Paramedic-->
          <div class="col-md-6">
            <div class="d-flex align-items-center p-4 bg-light-warning rounded">
              <div class="symbol symbol-45px me-3">
                <div class="symbol-label bg-warning">
                  <KTIcon icon-name="heart" icon-class="fs-3 text-white" />
                </div>
              </div>
              <div class="flex-grow-1">
                <div class="fw-bold text-gray-900 fs-6">James Miller, EMT-P</div>
                <div class="text-gray-700 fs-7">Flight Paramedic</div>
                <div class="text-gray-600 fs-8">FP-C Certified</div>
              </div>
              <div class="text-end">
                <span class="badge badge-light-success fs-8">On Duty</span>
              </div>
            </div>
          </div>
          <!--end::Flight Paramedic-->
        </div>
        <!--end::Medical Crew List-->
      </div>
      <!--end::Medical Crew Section-->
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

const getAircraftRegistration = (): string => {
  return props.trip?.aircraft?.registration || 
         props.trip?.aircraft?.tail_number || 
         'N123JM';
};

const getAircraftModel = (): string => {
  return props.trip?.aircraft?.model || 
         props.trip?.aircraft?.aircraft_type || 
         'Cessna Citation CJ4';
};

const getLastInspectionDate = (): string => {
  const date = props.trip?.aircraft?.last_inspection || '2024-12-15';
  return new Date(date).toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
  });
};

const getAircraftRange = (): string => {
  return props.trip?.aircraft?.max_range || '2,165 nm';
};

const getAircraftCapacity = (): string => {
  return props.trip?.aircraft?.max_passengers || '8';
};

const getAircraftSpeed = (): string => {
  return props.trip?.aircraft?.cruise_speed || '451 kts';
};

const getMedicalConfig = (): string => {
  return props.trip?.aircraft?.medical_config || 'Full Stretcher';
};

const getFuelCapacity = (): string => {
  return props.trip?.aircraft?.fuel_capacity || '1,800 lbs';
};
</script>