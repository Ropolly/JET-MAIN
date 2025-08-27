<template>
  <!--begin::Card-->
  <div class="card card-flush pt-3 mb-5 mb-xl-10">
    <!--begin::Card body-->
    <div class="card-body pt-3">
      <!--begin::Aircraft Info-->
      <div class="d-flex align-items-center">
        <!--begin::Aircraft Icon-->
        <div class="symbol symbol-60px symbol-circle me-4">
          <img :src="getAircraftImage()" :alt="getAircraftModel()" class="symbol-label object-fit-cover" style="width: 60px; height: 60px; border-radius: 50%;" />
        </div>
        <!--end::Aircraft Icon-->

        <!--begin::Aircraft Details-->
        <div class="flex-grow-1">
          <div class="d-flex flex-wrap align-items-center mb-2">
            <span class="fs-4 fw-bold text-gray-900 me-4">
              {{ getAircraftRegistration() }}
            </span>
            <span class="badge badge-light-success fs-7">Available</span>
          </div>
          <div class="fs-6 fw-semibold text-gray-700 mb-1">
            {{ getAircraftModel() }}
          </div>
          <div class="fs-7 text-gray-600">
            Serial Number: {{ getSerialNumber() }}
          </div>
        </div>
        <!--end::Aircraft Details-->
      </div>
      <!--end::Aircraft Info-->
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

const getSerialNumber = (): string => {
  return props.trip?.aircraft?.serial_number || 'N/A';
};

const getAircraftImage = (): string => {
  const aircraft = props.trip?.aircraft;
  if (!aircraft) return '/media/aircraft/default.jpg';
  
  // Build full model name for matching image files
  const make = aircraft.make || '';
  const model = aircraft.model || '';
  const fullModel = `${make} ${model}`.trim();
  
  // Map known aircraft to their image filenames
  const imageMap: Record<string, string> = {
    'Kodiak Kodiak 100': 'kodiak100.jpg',
    'Learjet 35A': 'Learjet35A.jpg',
    'Learjet 36A': 'learjet36a.jpeg',
    'Learjet 31': 'learjet30.jpg', // Using learjet30 as fallback for 31
    'Learjet 60': 'Learjet60.jpg',
  };
  
  // Return specific image or fallback to generic
  const imageName = imageMap[fullModel] || 'Learjet35A.jpg'; // Default fallback
  return `/media/aircraft/${imageName}`;
};

const viewAircraftDetails = () => {
  if (props.trip?.aircraft?.id) {
    window.open(`/admin/aircraft/${props.trip.aircraft.id}`, '_blank');
  } else {
    console.log('No aircraft assigned to this trip');
  }
};
</script>