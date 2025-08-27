<template>
  <!--begin::Upcoming Trips Widget-->
  <div class="card" :class="widgetClasses">
    <!--begin::Header-->
    <div class="card-header border-0 pt-5">
      <h3 class="card-title align-items-start flex-column">
        <span class="card-label fw-bold text-gray-900">Upcoming Trips</span>
        <span class="text-muted mt-1 fw-semibold fs-7">{{ upcomingTrips.length }} trips scheduled</span>
      </h3>

      <div class="card-toolbar">
        <button @click="viewAllTrips" class="btn btn-sm btn-light">View All</button>
      </div>
    </div>
    <!--end::Header-->

    <!--begin::Body-->
    <div class="card-body pt-5">
      <template v-for="(trip, index) in upcomingTrips" :key="trip.id">
        <!--begin::Item-->
        <div
          :class="{ 'mb-7': upcomingTrips.length - 1 !== index }"
          class="d-flex align-items-center"
        >
          <!--begin::Symbol-->
          <div class="symbol symbol-50px me-5">
            <img :src="getAircraftImage(trip)" :alt="getAircraftModel(trip)" class="symbol-label object-fit-cover" style="width: 50px; height: 50px; border-radius: 8px;" />
          </div>
          <!--end::Symbol-->

          <!--begin::Text-->
          <div class="d-flex flex-column">
            <a @click.prevent="viewTrip(trip)" href="#" class="text-gray-900 text-hover-primary fs-6 fw-bold">{{
              trip.trip_number
            }}</a>
            <span class="text-muted fw-semibold fs-7">{{ getPatientName(trip) }} • {{ formatDate(trip.departure_time || trip.scheduled_departure || trip.created_on) }}</span>
          </div>
          <!--end::Text-->

          <!--begin::Label-->
          <span :class="`badge badge-light-${getStatusColor(trip.status)} fs-7 fw-bold ms-auto`">{{ trip.status }}</span>
          <!--end::Label-->
        </div>
        <!--end::Item-->
      </template>

      <!-- Empty state -->
      <div v-if="upcomingTrips.length === 0" class="text-center text-muted py-10">
        <KTIcon icon-name="airplane" icon-class="fs-3x text-muted mb-3" />
        <div class="fw-semibold">No upcoming trips</div>
        <div class="fs-7">Scheduled trips will appear here</div>
      </div>
    </div>
    <!--end::Body-->
  </div>
  <!--end::Upcoming Trips Widget-->
</template>

<script setup lang="ts">
import { ref, onMounted, defineProps } from "vue";
import { useRouter } from "vue-router";
import ApiService from "@/core/services/ApiService";

interface Props {
  className?: string;
}

const props = defineProps<Props>();
const router = useRouter();

const upcomingTrips = ref<any[]>([]);
const loading = ref(false);

const widgetClasses = props.className;

const fetchUpcomingTrips = async () => {
  try {
    loading.value = true;
    const response = await ApiService.get("/trips/?page_size=5");
    const allTrips = response.data.results || response.data || [];
    
    // Filter for upcoming/pending trips
    upcomingTrips.value = allTrips
      .filter((trip: any) => ['pending', 'active', 'in_progress', 'scheduled'].includes(trip.status?.toLowerCase()))
      .sort((a: any, b: any) => {
        const aDate = new Date(a.departure_time || a.scheduled_departure || a.created_on);
        const bDate = new Date(b.departure_time || b.scheduled_departure || b.created_on);
        return aDate.getTime() - bDate.getTime();
      })
      .slice(0, 5);
  } catch (error) {
    console.error("Error fetching upcoming trips:", error);
  } finally {
    loading.value = false;
  }
};

const viewTrip = (trip: any) => {
  router.push(`/admin/trips/${trip.id}`);
};

const viewAllTrips = () => {
  router.push('/admin/trips');
};

const getStatusColor = (status: string): string => {
  switch (status?.toLowerCase()) {
    case 'pending': return 'warning';
    case 'active': case 'in_progress': return 'primary';
    case 'scheduled': return 'info';
    default: return 'secondary';
  }
};

const getPatientName = (trip: any): string => {
  if (trip.patient?.info) {
    const first = trip.patient.info.first_name || '';
    const last = trip.patient.info.last_name || '';
    const name = `${first} ${last}`.trim();
    return name || trip.patient.info.email || 'Patient';
  }
  if (trip.quote?.contact) {
    const first = trip.quote.contact.first_name || '';
    const last = trip.quote.contact.last_name || '';
    const name = `${first} ${last}`.trim();
    return name || trip.quote.contact.email || 'Contact';
  }
  return 'Unknown';
};

const formatDate = (dateString?: string): string => {
  if (!dateString) return 'TBD';
  return new Date(dateString).toLocaleDateString('en-US', {
    month: 'short',
    day: 'numeric',
    hour: 'numeric',
    minute: '2-digit',
  });
};

const getAircraftImage = (trip: any): string => {
  const aircraft = trip?.aircraft;
  if (!aircraft) return '/media/aircraft/Learjet35A.jpg';
  
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

const getAircraftModel = (trip: any): string => {
  const aircraft = trip?.aircraft;
  if (!aircraft) return 'Aircraft';
  return `${aircraft.make} ${aircraft.model}` || 'Aircraft';
};

onMounted(() => {
  fetchUpcomingTrips();
});
</script>