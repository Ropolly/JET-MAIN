<template>
  <!--begin::Layout-->
  <div class="d-flex flex-column flex-xl-row">
    <!--begin::Sidebar-->
    <div class="flex-column flex-lg-row-auto w-100 w-xl-350px mb-10">
      <!--begin::Card-->
      <div class="card mb-5 mb-xl-8">
        <!--begin::Card body-->
        <div class="card-body pt-15">
          <!--begin::Summary-->
          <div class="d-flex flex-center flex-column mb-5">
            <!--begin::Avatar-->
            <div class="symbol symbol-100px symbol-circle mb-7">
              <img :src="getAircraftImage()" :alt="getAircraftType()" class="symbol-label object-fit-cover" style="width: 100px; height: 100px; border-radius: 50%;" />
            </div>
            <!--end::Avatar-->

            <!--begin::Name-->
            <a
              href="#"
              class="fs-3 text-gray-800 text-hover-primary fw-bold mb-1"
            >
              {{ getAircraftName() }}
            </a>
            <!--end::Name-->

            <!--begin::Position-->
            <div class="fs-5 fw-semibold text-muted mb-6">{{ getAircraftType() }}</div>
            <!--end::Position-->

            <!--begin::Info-->
            <div class="d-flex flex-wrap flex-center">
              <!--begin::Stats-->
              <div
                class="border border-gray-300 border-dashed rounded py-3 px-3 mb-3"
              >
                <div class="fs-4 fw-bold text-gray-700">
                  <span class="w-75px">{{ getTotalTrips() }}</span>
                  <KTIcon icon-name="arrow-up" icon-class="fs-3 text-success" />
                </div>
                <div class="fw-semibold text-muted">Total Trips</div>
              </div>
              <!--end::Stats-->

              <!--begin::Stats-->
              <div
                class="border border-gray-300 border-dashed rounded py-3 px-3 mx-4 mb-3"
              >
                <div class="fs-4 fw-bold text-gray-700">
                  <span class="w-50px">{{ getTotalFlightHours() }}</span>
                </div>
                <div class="fw-semibold text-muted">Flight Hours</div>
              </div>
              <!--end::Stats-->

              <!--begin::Stats-->
              <div
                class="border border-gray-300 border-dashed rounded py-3 px-3 mb-3"
              >
                <div class="fs-4 fw-bold text-gray-700">
                  <span class="w-50px">{{ getLastFlightDate() }}</span>
                </div>
                <div class="fw-semibold text-muted">Last Flight</div>
              </div>
              <!--end::Stats-->
            </div>
            <!--end::Info-->
          </div>
          <!--end::Summary-->

          <!--begin::Details toggle-->
          <div class="d-flex flex-stack fs-4 py-3">
            <div
              class="fw-bold rotate collapsible"
              data-bs-toggle="collapse"
              href="#kt_aircraft_view_details"
              role="button"
              aria-expanded="false"
              aria-controls="kt_aircraft_view_details"
            >
              Details
              <span class="ms-2 rotate-180">
                <KTIcon icon-name="down" icon-class="fs-3" />
              </span>
            </div>

            <span
              data-bs-toggle="tooltip"
              data-bs-trigger="hover"
              title="Edit aircraft details"
            >
              <button class="btn btn-sm btn-light-primary">
                Edit
              </button>
            </span>
          </div>
          <!--end::Details toggle-->

          <div class="separator separator-dashed my-3"></div>

          <!--begin::Details content-->
          <div id="kt_aircraft_view_details" class="collapse show">
            <div class="py-5 fs-6">
              <!--begin::Badge-->
              <div :class="`badge badge-light-${getStatusColor()} d-inline`">{{ aircraft?.status || 'Active' }}</div>
              <!--end::Badge-->
              
              <!--begin::Details item-->
              <div class="fw-bold mt-5">Aircraft ID</div>
              <div class="text-gray-600">{{ aircraft?.id || '-' }}</div>
              <!--end::Details item-->
              
              <!--begin::Details item-->
              <div class="fw-bold mt-5">Tail Number</div>
              <div class="text-gray-600">{{ aircraft?.tail_number || 'Not provided' }}</div>
              <!--end::Details item-->
              
              <!--begin::Details item-->
              <div class="fw-bold mt-5">Company</div>
              <div class="text-gray-600">{{ aircraft?.company || 'Not provided' }}</div>
              <!--end::Details item-->
              
              <!--begin::Details item-->
              <div class="fw-bold mt-5">Make & Model</div>
              <div class="text-gray-600">{{ getAircraftType() }}</div>
              <!--end::Details item-->
              
              <!--begin::Details item-->
              <div class="fw-bold mt-5">Serial Number</div>
              <div class="text-gray-600">{{ aircraft?.serial_number || 'Not provided' }}</div>
              <!--end::Details item-->
              
              <!--begin::Details item-->
              <div class="fw-bold mt-5">MGTOW</div>
              <div class="text-gray-600">{{ formatWeight(aircraft?.mgtow) }}</div>
              <!--end::Details item-->
              
              <!--begin::Details item-->
              <div class="fw-bold mt-5">Created</div>
              <div class="text-gray-600">{{ formatDate(aircraft?.created_on) }}</div>
              <!--end::Details item-->
            </div>
          </div>
          <!--end::Details content-->
        </div>
        <!--end::Card body-->
      </div>
      <!--end::Card-->
    </div>
    <!--end::Sidebar-->

    <!--begin::Content-->
    <div class="flex-lg-row-fluid ms-lg-15">
      <!--begin:::Tabs-->
      <ul
        class="nav nav-custom nav-tabs nav-line-tabs nav-line-tabs-2x border-0 fs-4 fw-semibold mb-8"
      >
        <!--begin:::Tab item-->
        <li class="nav-item">
          <a
            class="nav-link text-active-primary pb-4 active"
            data-bs-toggle="tab"
            href="#kt_aircraft_view_overview_tab"
          >
            Overview
          </a>
        </li>
        <!--end:::Tab item-->

        <!--begin:::Tab item-->
        <li class="nav-item">
          <a
            class="nav-link text-active-primary pb-4"
            data-bs-toggle="tab"
            href="#kt_aircraft_view_trips_tab"
          >
            All Trips
          </a>
        </li>
        <!--end:::Tab item-->


        <!--begin:::Tab item-->
        <li class="nav-item ms-auto">
          <!--begin::Action menu-->
          <a
            href="#"
            class="btn btn-primary ps-7"
            data-kt-menu-trigger="click"
            data-kt-menu-attach="parent"
            data-kt-menu-placement="bottom-end"
          >
            Actions
            <KTIcon icon-name="down" icon-class="fs-2 me-0" />
          </a>
          <!--begin::Menu-->
          <div
            class="menu menu-sub menu-sub-dropdown menu-column menu-rounded menu-gray-600 menu-state-bg-light-primary fw-semibold fs-7 w-200px py-4"
            data-kt-menu="true"
          >
            <div class="menu-item px-3">
              <a href="#" class="menu-link px-3">Edit Aircraft</a>
            </div>
            <div class="menu-item px-3">
              <a href="#" class="menu-link px-3">Schedule Trip</a>
            </div>
            <div class="menu-item px-3">
              <a href="#" class="menu-link px-3">View All Trips</a>
            </div>
            <div class="separator my-2"></div>
            <div class="menu-item px-3">
              <a href="#" class="menu-link px-3 text-warning">Mark Inactive</a>
            </div>
          </div>
          <!--end::Menu-->
        </li>
        <!--end:::Tab item-->
      </ul>
      <!--end:::Tabs-->

      <!--begin:::Tab content-->
      <div class="tab-content" id="myTabContent">
        <!--begin:::Tab pane-->
        <div
          class="tab-pane fade show active"
          id="kt_aircraft_view_overview_tab"
          role="tabpanel"
        >
          <AircraftOverview :aircraft="aircraft" :loading="loading" />
        </div>
        <!--end:::Tab pane-->

        <!--begin:::Tab pane-->
        <div
          class="tab-pane fade"
          id="kt_aircraft_view_trips_tab"
          role="tabpanel"
        >
          <AircraftTrips :aircraft="aircraft" :loading="loading" />
        </div>
        <!--end:::Tab pane-->

      </div>
      <!--end:::Tab content-->
    </div>
    <!--end::Content-->
  </div>
  <!--end::Layout-->
</template>

<script lang="ts">
import { defineComponent, ref, onMounted } from "vue";
import { useRoute } from "vue-router";
import ApiService from "@/core/services/ApiService";
import AircraftOverview from "@/components/aircraft/cards/overview/AircraftOverview.vue";
import AircraftTrips from "@/components/aircraft/cards/trips/AircraftTrips.vue";

export default defineComponent({
  name: "aircraft-details",
  components: {
    AircraftOverview,
    AircraftTrips,
  },
  setup() {
    const route = useRoute();
    const aircraft = ref<any>(null);
    const loading = ref(true);
    const error = ref<string | null>(null);

    const fetchAircraft = async () => {
      try {
        loading.value = true;
        error.value = null;
        const aircraftId = route.params.id as string;
        
        const response = await ApiService.get(`/aircraft/${aircraftId}/`);
        aircraft.value = response.data;
        
      } catch (err: any) {
        error.value = err.response?.data?.detail || "Failed to fetch aircraft details";
        console.error("Error fetching aircraft:", err);
      } finally {
        loading.value = false;
      }
    };

    const getAircraftName = (): string => {
      if (aircraft.value) {
        return aircraft.value.tail_number || 'Unknown Aircraft';
      }
      return 'Loading...';
    };

    const getAircraftType = (): string => {
      if (aircraft.value) {
        const make = aircraft.value.make || '';
        const model = aircraft.value.model || '';
        return `${make} ${model}`.trim() || 'Unknown Type';
      }
      return 'Loading...';
    };

    const getTotalTrips = (): string => {
      return aircraft.value?.total_trips?.toString() || '0';
    };

    const getTotalFlightHours = (): string => {
      const hours = aircraft.value?.total_flight_hours || 0;
      return `${hours.toLocaleString()}h`;
    };

    const getLastFlightDate = (): string => {
      if (!aircraft.value?.last_flight_date) return 'Never';
      return new Date(aircraft.value.last_flight_date).toLocaleDateString('en-US', {
        month: 'short',
        day: 'numeric',
      });
    };

    const getStatusColor = (): string => {
      const status = aircraft.value?.status?.toLowerCase();
      switch (status) {
        case 'active': return 'success';
        case 'maintenance': return 'warning';
        case 'grounded': return 'danger';
        case 'inactive': return 'secondary';
        default: return 'primary';
      }
    };

    const formatWeight = (weight?: string | number): string => {
      if (!weight) return 'Not specified';
      const numWeight = typeof weight === 'string' ? parseFloat(weight) : weight;
      return `${numWeight.toLocaleString()} lbs`;
    };

    const formatDate = (dateString?: string): string => {
      if (!dateString) return 'Not provided';
      return new Date(dateString).toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'long',
        day: 'numeric',
      });
    };

    const getAircraftImage = (): string => {
      if (!aircraft.value) return '/media/aircraft/Learjet35A.jpg';
      
      // Build full model name for matching image files
      const make = aircraft.value.make || '';
      const model = aircraft.value.model || '';
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

    onMounted(() => {
      fetchAircraft();
    });

    return {
      aircraft,
      loading,
      error,
      getAircraftName,
      getAircraftType,
      getTotalTrips,
      getTotalFlightHours,
      getLastFlightDate,
      getStatusColor,
      formatWeight,
      formatDate,
      getAircraftImage,
    };
  },
});
</script>