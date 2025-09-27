<template>
        <!--begin::Loading-->
        <div v-if="loading" class="d-flex justify-content-center py-20">
          <div class="spinner-border" role="status">
            <span class="visually-hidden">Loading...</span>
          </div>
        </div>
        <!--end::Loading-->

        <!--begin::Trip Header Card-->
        <div v-if="!loading && trip" class="card mb-6 mb-xl-9">
          <div class="card-body pt-9 pb-0">
            <!--begin::Details-->
            <div class="d-flex flex-wrap flex-sm-nowrap mb-6">
              <!--begin::Image-->
              <div class="d-flex flex-center flex-shrink-0 bg-light rounded w-100px h-100px w-lg-150px h-lg-150px me-7 mb-4">
                <img
                  v-if="getAircraftImage()"
                  :src="getAircraftImage()"
                  :alt="getAircraftName()"
                  class="w-100 h-100 rounded object-fit-cover"
                />
                <KTIcon
                  v-else
                  icon-name="airplane"
                  icon-class="fs-2x text-primary"
                />
              </div>
              <!--end::Image-->

              <!--begin::Wrapper-->
              <div class="flex-grow-1">
                <!--begin::Head-->
                <div class="d-flex justify-content-between align-items-start flex-wrap mb-2">
                  <!--begin::Details-->
                  <div class="d-flex flex-column">
                    <!--begin::Trip Title & Status-->
                    <div class="d-flex align-items-center mb-1">
                      <h2 class="text-gray-800 text-hover-primary fs-2 fw-bold me-3">
                        {{ getTripTitle() }}
                      </h2>
                      <span :class="`badge badge-light-${getStatusColor()}`">
                        {{ trip.status }}
                      </span>
                    </div>
                    <!--end::Trip Title & Status-->

                    <!--begin::Description-->
                    <div class="d-flex flex-wrap fw-semibold mb-4 fs-5 text-gray-500">
                      {{ getTripDescription() }}
                    </div>
                    <!--end::Description-->
                  </div>
                  <!--end::Details-->

                  <!--begin::Actions-->
                  <div class="d-flex mb-4">
                    <button @click="handleEditTrip" class="btn btn-sm btn-bg-light btn-active-color-primary me-3">
                      Edit Trip
                    </button>

                    <!--begin::Menu-->
                    <div class="me-0">
                      <button class="btn btn-sm btn-icon btn-bg-light btn-active-color-primary" data-kt-menu-trigger="click" data-kt-menu-placement="bottom-end">
                        <KTIcon icon-name="dots-horizontal" icon-class="fs-2x" />
                      </button>

                      <!--begin::Menu-->
                      <div class="menu menu-sub menu-sub-dropdown menu-column menu-rounded menu-gray-800 menu-state-bg-light-primary fw-semibold w-200px py-3" data-kt-menu="true">
                        <!--begin::Menu item-->
                        <div class="menu-item px-3">
                          <a href="#" @click="handleEditTrip" class="menu-link px-3">
                            Edit Trip
                          </a>
                        </div>
                        <!--end::Menu item-->

                        <!--begin::Menu item-->
                        <div class="menu-item px-3">
                          <a href="#" @click="duplicateTrip" class="menu-link px-3">
                            Duplicate Trip
                          </a>
                        </div>
                        <!--end::Menu item-->

                        <!--begin::Menu item-->
                        <div class="menu-item px-3 my-1">
                          <a href="#" @click="handleDeleteTrip" class="menu-link px-3 text-danger">
                            Delete Trip
                          </a>
                        </div>
                        <!--end::Menu item-->
                      </div>
                      <!--end::Menu-->
                    </div>
                    <!--end::Menu-->
                  </div>
                  <!--end::Actions-->
                </div>
                <!--end::Head-->

                <!--begin::Info-->
                <div class="d-flex flex-wrap justify-content-start">
                  <!--begin::Stats-->
                  <div class="d-flex flex-wrap">
                    <!--begin::Stat-->
                    <div class="border border-gray-300 border-dashed rounded min-w-125px py-3 px-4 me-6 mb-3">
                      <!--begin::Number-->
                      <div class="d-flex align-items-center">
                        <div class="fs-4 fw-bold">{{ getTripDate() }}</div>
                      </div>
                      <!--end::Number-->
                      <!--begin::Label-->
                      <div class="fw-semibold fs-6 text-gray-500">Trip Date</div>
                      <!--end::Label-->
                    </div>
                    <!--end::Stat-->

                    <!--begin::Stat-->
                    <div class="border border-gray-300 border-dashed rounded min-w-125px py-3 px-4 me-6 mb-3">
                      <!--begin::Number-->
                      <div class="d-flex align-items-center">
                        <div class="fs-4 fw-bold">{{ getTotalDistance() }}</div>
                      </div>
                      <!--end::Number-->
                      <!--begin::Label-->
                      <div class="fw-semibold fs-6 text-gray-500">Distance</div>
                      <!--end::Label-->
                    </div>
                    <!--end::Stat-->

                    <!--begin::Stat-->
                    <div class="border border-gray-300 border-dashed rounded min-w-125px py-3 px-4 me-6 mb-3">
                      <!--begin::Number-->
                      <div class="d-flex align-items-center">
                        <div class="fs-4 fw-bold">{{ getTotalFlightTime() }}</div>
                      </div>
                      <!--end::Number-->
                      <!--begin::Label-->
                      <div class="fw-semibold fs-6 text-gray-500">Flight Time</div>
                      <!--end::Label-->
                    </div>
                    <!--end::Stat-->
                  </div>
                  <!--end::Stats-->

                </div>
                <!--end::Info-->
              </div>
              <!--end::Wrapper-->
            </div>
            <!--end::Details-->

            <div class="separator"></div>

            <!--begin::Nav-->
            <ul class="nav nav-stretch nav-line-tabs nav-line-tabs-2x border-transparent fs-5 fw-bold">
              <!--begin::Nav item-->
              <li class="nav-item">
                <a class="nav-link text-active-primary py-5 me-6"
                   :class="{ active: activeTab === 'itinerary' }"
                   @click="activeTab = 'itinerary'"
                   href="#">
                  Itinerary
                </a>
              </li>
              <!--end::Nav item-->

              <!--begin::Nav item-->
              <li class="nav-item">
                <a class="nav-link text-active-primary py-5 me-6"
                   :class="{ active: activeTab === 'patients' }"
                   @click="activeTab = 'patients'"
                   href="#">
                  Patients/PAX
                </a>
              </li>
              <!--end::Nav item-->

              <!--begin::Nav item-->
              <li class="nav-item">
                <a class="nav-link text-active-primary py-5 me-6"
                   :class="{ active: activeTab === 'financials' }"
                   @click="activeTab = 'financials'"
                   href="#">
                  Financials
                </a>
              </li>
              <!--end::Nav item-->

              <!--begin::Nav item-->
              <li class="nav-item">
                <a class="nav-link text-active-primary py-5 me-6"
                   :class="{ active: activeTab === 'crew' }"
                   @click="activeTab = 'crew'"
                   href="#">
                  Crew
                </a>
              </li>
              <!--end::Nav item-->

              <!--begin::Nav item-->
              <li class="nav-item">
                <a class="nav-link text-active-primary py-5 me-6"
                   :class="{ active: activeTab === 'documents' }"
                   @click="activeTab = 'documents'"
                   href="#">
                  Documents
                </a>
              </li>
              <!--end::Nav item-->

              <!--begin::Nav item-->
              <li class="nav-item">
                <a class="nav-link text-active-primary py-5 me-6"
                   :class="{ active: activeTab === 'activity' }"
                   @click="activeTab = 'activity'"
                   href="#">
                  Activity
                </a>
              </li>
              <!--end::Nav item-->

            </ul>
            <!--end::Nav-->
          </div>
        </div>
        <!--end::Trip Header Card-->

        <!--begin::Tab Content-->
        <div class="tab-content">
          <!--begin::Itinerary Tab-->
          <div v-if="activeTab === 'itinerary'">
            <TripItinerary :trip="trip" :loading="loading" @trip-updated="handleTripUpdated" />
          </div>
          <!--end::Itinerary Tab-->

          <!--begin::Patients/PAX Tab-->
          <div v-if="activeTab === 'patients'">
            <TripPatients :trip="trip" :loading="loading" @trip-updated="handleTripUpdated" />
          </div>
          <!--end::Patients/PAX Tab-->

          <!--begin::Financials Tab-->
          <div v-if="activeTab === 'financials'">
            <TripFinancials :trip="trip" :loading="loading" />
          </div>
          <!--end::Financials Tab-->

          <!--begin::Crew Tab-->
          <div v-if="activeTab === 'crew'">
            <TripCrew :trip="trip" :loading="loading" />
          </div>
          <!--end::Crew Tab-->

          <!--begin::Documents Tab-->
          <div v-if="activeTab === 'documents'">
            <TripDocuments v-if="trip?.id" :trip-id="trip.id" :trip="trip" />
          </div>
          <!--end::Documents Tab-->

          <!--begin::Activity Tab-->
          <div v-if="activeTab === 'activity'">
            <TripActivity :trip="trip" :loading="loading" />
          </div>
          <!--end::Activity Tab-->

        </div>
        <!--end::Tab Content-->
</template>

<script setup lang="ts">
import { ref, onMounted, computed, watch, nextTick } from "vue";
import { useRoute, useRouter } from "vue-router";
import ApiService from "@/core/services/ApiService";
import Swal from "sweetalert2";
import { calculateTripDistance, formatDistance } from '@/core/helpers/distanceCalculator';

// Import existing components
import TripItinerary from "@/components/trips/view/TripItinerary.vue";
import TripDocuments from "@/components/trips/view/TripDocuments.vue";

// Import new tab components (to be created)
import TripPatients from "@/components/trips/view/TripPatients.vue";
import TripFinancials from "@/components/trips/view/TripFinancials.vue";
import TripCrew from "@/components/trips/view/TripCrew.vue";
import TripActivity from "@/components/trips/view/TripActivity.vue";

interface Trip {
  id: string;
  trip_number: string;
  type: string;
  status: string;
  patient_id?: string;
  patient?: any;
  aircraft_id?: string;
  aircraft?: any;
  quote_id?: string;
  quote?: any;
  trip_lines?: any[];
  estimated_departure_time?: string;
  notes?: string;
  created_on?: string;
  modified_on?: string;
}

const route = useRoute();
const router = useRouter();
const trip = ref<Trip | null>(null);
const loading = ref(true);
const error = ref<string | null>(null);
const activeTab = ref('itinerary');

const fetchTrip = async () => {
  try {
    loading.value = true;
    error.value = null;
    const tripId = route.params.id as string;

    const response = await ApiService.get(`/trips/${tripId}/`);
    trip.value = response.data;

    console.log('Trip data received:', response.data);
  } catch (err: any) {
    error.value = err.response?.data?.detail || "Failed to fetch trip details";
    console.error("Error fetching trip:", err);
  } finally {
    loading.value = false;
  }
};

const handleEditTrip = () => {
  if (trip.value?.id) {
    sessionStorage.setItem('editTripData', JSON.stringify({
      mode: 'edit',
      tripId: trip.value.id,
      tripData: trip.value
    }));

    router.push('/admin/trips?edit=' + trip.value.id);
  }
};


const handleDeleteTrip = () => {
  if (!trip.value) return;

  Swal.fire({
    title: 'Delete Trip',
    text: 'Are you sure you want to delete this trip? This action cannot be undone.',
    icon: 'warning',
    showCancelButton: true,
    confirmButtonText: 'Yes, Delete',
    cancelButtonText: 'Cancel',
    confirmButtonColor: '#d33'
  }).then(async (result) => {
    if (result.isConfirmed) {
      try {
        await ApiService.delete(`/trips/${trip.value!.id}/`);

        Swal.fire({
          title: 'Deleted!',
          text: 'Trip has been deleted successfully.',
          icon: 'success',
          confirmButtonText: 'OK'
        }).then(() => {
          router.push('/admin/trips');
        });
      } catch (error) {
        console.error('Error deleting trip:', error);
        Swal.fire({
          title: 'Error!',
          text: 'Failed to delete the trip. Please try again.',
          icon: 'error',
          confirmButtonText: 'OK'
        });
      }
    }
  });
};

const duplicateTrip = () => {
  // TODO: Implement trip duplication
  Swal.fire({
    title: 'Feature Coming Soon',
    text: 'Trip duplication will be available in a future update.',
    icon: 'info',
    confirmButtonText: 'OK'
  });
};

// Handle trip updates from child components (e.g., when flight legs are added)
const handleTripUpdated = async () => {
  console.log('Trip updated, refreshing data...');
  await fetchTrip();
  await updatePageTitle();
};

// Computed properties for trip data
const getTripTitle = (): string => {
  if (!trip.value?.trip_number) return 'Trip';
  return `Trip ${trip.value.trip_number}`;
};

const getTripDescription = (): string => {
  if (!trip.value) return '';

  let description = trip.value.type?.charAt(0).toUpperCase() + trip.value.type?.slice(1) || 'Medical Transport';

  if (trip.value.trip_lines && trip.value.trip_lines.length > 0) {
    const firstLeg = trip.value.trip_lines[0];
    const lastLeg = trip.value.trip_lines[trip.value.trip_lines.length - 1];

    if (firstLeg.origin_airport && lastLeg.destination_airport) {
      const origin = firstLeg.origin_airport.icao_code || firstLeg.origin_airport.iata_code || 'UNK';
      const destination = lastLeg.destination_airport.icao_code || lastLeg.destination_airport.iata_code || 'UNK';
      description += ` • ${origin} → ${destination}`;
    }
  }

  return description;
};

const getTripDate = (): string => {
  // First try estimated_departure_time
  if (trip.value?.estimated_departure_time) {
    try {
      const date = new Date(trip.value.estimated_departure_time);
      return date.toLocaleDateString('en-US', {
        month: 'short',
        day: 'numeric',
        year: 'numeric'
      });
    } catch (error) {
      // Continue to trip lines fallback
    }
  }

  // Fallback to first trip line departure time
  if (trip.value?.trip_lines && trip.value.trip_lines.length > 0) {
    const firstLeg = trip.value.trip_lines[0];
    const departureTime = firstLeg.departure_time_local || firstLeg.departure_time_utc;

    if (departureTime) {
      try {
        const date = new Date(departureTime);
        return date.toLocaleDateString('en-US', {
          month: 'short',
          day: 'numeric',
          year: 'numeric'
        });
      } catch (error) {
        // Continue to TBD
      }
    }
  }

  return 'TBD';
};

const getTotalDistance = (): string => {
  if (!trip.value?.trip_lines) return 'TBD';

  const totalDistance = calculateTripDistance(trip.value.trip_lines);
  return formatDistance(totalDistance, false) + ' nm';
};

const getTotalFlightTime = (): string => {
  if (!trip.value?.trip_lines) return 'TBD';

  let totalMinutes = 0;

  trip.value.trip_lines.forEach(line => {
    if (line.flight_time) {
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

const getStatusColor = (): string => {
  const status = trip.value?.status?.toLowerCase();
  switch (status) {
    case 'completed': return 'success';
    case 'active': case 'in_progress': return 'primary';
    case 'cancelled': return 'danger';
    case 'pending': return 'warning';
    default: return 'secondary';
  }
};

const getCrewMembers = (): any[] => {
  // TODO: Extract crew members from trip lines
  const crew: any[] = [];

  if (trip.value?.trip_lines) {
    trip.value.trip_lines.forEach(line => {
      if (line.crew_line) {
        if (line.crew_line.primary_in_command) {
          crew.push({
            name: getContactName(line.crew_line.primary_in_command) + ' (PIC)',
            initials: getContactInitials(line.crew_line.primary_in_command),
            avatar: null
          });
        }
        if (line.crew_line.secondary_in_command) {
          crew.push({
            name: getContactName(line.crew_line.secondary_in_command) + ' (SIC)',
            initials: getContactInitials(line.crew_line.secondary_in_command),
            avatar: null
          });
        }
      }
    });
  }

  // Remove duplicates based on name
  return crew.filter((member, index, self) =>
    index === self.findIndex(m => m.name === member.name)
  ).slice(0, 7); // Limit to 7 for display
};

const getContactName = (contact: any): string => {
  if (!contact) return 'Unknown';
  const first = contact.first_name || '';
  const last = contact.last_name || '';
  const business = contact.business_name || '';

  if (business) return business;
  return `${first} ${last}`.trim() || 'Unknown';
};

const getContactInitials = (contact: any): string => {
  if (!contact) return '?';
  const first = contact.first_name || '';
  const last = contact.last_name || '';
  const business = contact.business_name || '';

  if (business) return business.charAt(0).toUpperCase();
  return `${first.charAt(0)}${last.charAt(0)}`.toUpperCase() || '?';
};

const getAircraftImage = (): string | null => {
  if (!trip.value?.aircraft) return null;

  // Check if aircraft has an image URL
  if (trip.value.aircraft.image_url) {
    return trip.value.aircraft.image_url;
  }

  // Check if aircraft has a photo field
  if (trip.value.aircraft.photo) {
    return trip.value.aircraft.photo;
  }

  // Fallback to a generic aircraft image based on make/model if available
  if (trip.value.aircraft.make && trip.value.aircraft.model) {
    const makeModel = `${trip.value.aircraft.make}${trip.value.aircraft.model}`.replace(/\s+/g, '');
    return `/media/aircraft/${makeModel}.jpg`;
  }

  return null;
};

const getAircraftName = (): string => {
  if (!trip.value?.aircraft) return 'Aircraft';

  const tail = trip.value.aircraft.tail_number || '';
  const make = trip.value.aircraft.make || '';
  const model = trip.value.aircraft.model || '';

  if (tail && make && model) {
    return `${tail} - ${make} ${model}`;
  } else if (tail) {
    return tail;
  } else if (make && model) {
    return `${make} ${model}`;
  }

  return 'Aircraft';
};

onMounted(() => {
  fetchTrip();
});

// Watch for trip changes to update the page title and breadcrumbs
const updatePageTitle = async () => {
  const tripTitle = getTripTitle();
  console.log('Updating page title:', tripTitle, 'Trip data:', trip.value);

  // Update route meta using router.replace to ensure reactivity
  await router.replace({
    ...route,
    meta: {
      ...route.meta,
      pageTitle: tripTitle,
      breadcrumbs: ["Trips", tripTitle]
    }
  });

  console.log('Page title updated to:', route.meta.pageTitle);
};

// Watch trip changes to update title and breadcrumbs
watch(trip, (newTrip) => {
  if (newTrip) {
    updatePageTitle();
  }
}, { immediate: true });
</script>

<style scoped>
.nav-line-tabs .nav-link.active {
  border-bottom: 2px solid var(--kt-primary);
}

.symbol-group .symbol {
  margin-right: -0.5rem;
}

.symbol-group .symbol:last-child {
  margin-right: 0;
}
</style>