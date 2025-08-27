<template>
  <div class="card">
    <!--begin::Card header-->
    <div class="card-header border-0 pt-5">
      <h3 class="card-title align-items-start flex-column">
        <span class="card-label fw-bold fs-3 mb-1">Trip History</span>
        <span class="text-muted mt-1 fw-semibold fs-7">All trips for this aircraft</span>
      </h3>
      <div class="card-toolbar">
        <button class="btn btn-sm btn-light-primary">
          <KTIcon icon-name="plus" icon-class="fs-3" />
          Schedule Trip
        </button>
      </div>
    </div>
    <!--end::Card header-->

    <!--begin::Card body-->
    <div class="card-body py-3">
      <div v-if="loading" class="d-flex justify-content-center">
        <div class="spinner-border" role="status">
          <span class="visually-hidden">Loading...</span>
        </div>
      </div>

      <div v-else-if="trips && trips.length > 0">
        <!--begin::Table container-->
        <div class="table-responsive">
          <!--begin::Table-->
          <table class="table table-row-dashed table-row-gray-300 align-middle gs-0 gy-4">
            <!--begin::Table head-->
            <thead>
              <tr class="fw-bold text-muted">
                <th class="min-w-150px">Trip ID</th>
                <th class="min-w-140px">Date</th>
                <th class="min-w-120px">From</th>
                <th class="min-w-120px">To</th>
                <th class="min-w-100px">Duration</th>
                <th class="min-w-100px">Status</th>
                <th class="min-w-100px text-end">Actions</th>
              </tr>
            </thead>
            <!--end::Table head-->
            <!--begin::Table body-->
            <tbody>
              <tr v-for="trip in trips" :key="trip.id">
                <td>
                  <div class="d-flex align-items-center">
                    <div class="d-flex justify-content-start flex-column">
                      <a @click="navigateToTrip(trip.id)" href="#" class="text-dark fw-bold text-hover-primary fs-6">
                        #{{ trip.trip_number || trip.id }}
                      </a>
                    </div>
                  </div>
                </td>
                <td>
                  <div class="text-dark fw-bold fs-6">{{ formatDate(trip.date) }}</div>
                </td>
                <td>
                  <div class="text-dark fw-bold fs-6">{{ trip.from_airport || 'N/A' }}</div>
                </td>
                <td>
                  <div class="text-dark fw-bold fs-6">{{ trip.to_airport || 'N/A' }}</div>
                </td>
                <td>
                  <div class="text-dark fw-bold fs-6">{{ trip.duration || 'N/A' }}</div>
                </td>
                <td>
                  <span :class="`badge badge-light-${getStatusColor(trip.status)}`">
                    {{ trip.status || 'Unknown' }}
                  </span>
                </td>
                <td>
                  <div class="d-flex justify-content-end flex-shrink-0">
                    <a href="#" class="btn btn-icon btn-bg-light btn-active-color-primary btn-sm me-1">
                      <KTIcon icon-name="switch" icon-class="fs-3" />
                    </a>
                    <a href="#" class="btn btn-icon btn-bg-light btn-active-color-primary btn-sm">
                      <KTIcon icon-name="pencil" icon-class="fs-3" />
                    </a>
                  </div>
                </td>
              </tr>
            </tbody>
            <!--end::Table body-->
          </table>
          <!--end::Table-->
        </div>
        <!--end::Table container-->
      </div>

      <div v-else class="text-center py-10">
        <div class="text-gray-400">No trips found for this aircraft</div>
        <button class="btn btn-primary mt-3">
          Schedule First Trip
        </button>
      </div>
    </div>
    <!--end::Card body-->
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, watch, onMounted } from "vue";
import ApiService from "@/core/services/ApiService";

export default defineComponent({
  name: "AircraftTrips",
  props: {
    aircraft: {
      type: Object,
      default: null,
    },
    loading: {
      type: Boolean,
      default: false,
    },
  },
  setup(props) {
    const trips = ref<any[]>([]);
    const tripsLoading = ref(false);

    const fetchTrips = async () => {
      if (!props.aircraft?.id) return;
      
      try {
        tripsLoading.value = true;
        const response = await ApiService.get(`/trips/?aircraft=${props.aircraft.id}`);
        trips.value = response.data.results || response.data || [];
      } catch (error) {
        console.error("Error fetching aircraft trips:", error);
        trips.value = [];
      } finally {
        tripsLoading.value = false;
      }
    };

    const formatDate = (dateString?: string): string => {
      if (!dateString) return 'N/A';
      return new Date(dateString).toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
      });
    };

    const getStatusColor = (status?: string): string => {
      switch (status?.toLowerCase()) {
        case 'completed': return 'success';
        case 'in_progress': return 'primary';
        case 'cancelled': return 'danger';
        case 'scheduled': return 'warning';
        default: return 'secondary';
      }
    };

    const navigateToTrip = (tripId: string) => {
      const url = `/admin/trips/${tripId}`;
      window.open(url, '_blank');
    };

    watch(() => props.aircraft, fetchTrips, { immediate: true });

    return {
      trips,
      tripsLoading,
      formatDate,
      getStatusColor,
      navigateToTrip,
    };
  },
});
</script>