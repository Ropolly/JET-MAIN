<template>
  <div class="card card-flush" :class="className">
    <!--begin::Header-->
    <div class="card-header pt-5">
      <!--begin::Title-->
      <h3 class="card-title text-gray-800 fw-bold">Recent Activity</h3>
      <!--end::Title-->

      <!--begin::Toolbar-->
      <div class="card-toolbar">
        <!--begin::Tabs-->
        <ul class="nav nav-pills nav-pills-sm nav-light">
          <li class="nav-item">
            <a
              class="nav-link btn btn-sm btn-color-muted btn-active btn-active-light-primary fw-bold px-4 me-1"
              :class="{ active: activeTab === 'quotes' }"
              @click="activeTab = 'quotes'"
              href="#"
            >
              Quotes
            </a>
          </li>
          <li class="nav-item">
            <a
              class="nav-link btn btn-sm btn-color-muted btn-active btn-active-light-primary fw-bold px-4"
              :class="{ active: activeTab === 'trips' }"
              @click="activeTab = 'trips'"
              href="#"
            >
              Trips
            </a>
          </li>
        </ul>
        <!--end::Tabs-->
      </div>
      <!--end::Toolbar-->
    </div>
    <!--end::Header-->

    <!--begin::Body-->
    <div class="card-body pt-5">
      <!--begin::Tab Content-->
      <div v-if="activeTab === 'quotes'" class="tab-content">
        <!--begin::Quotes-->
        <div v-if="recentQuotes.length > 0">
          <div
            v-for="quote in recentQuotes"
            :key="quote.id"
            class="d-flex align-items-center bg-light-warning rounded p-5 mb-7"
          >
            <!--begin::Icon-->
            <span class="svg-icon svg-icon-warning me-5">
              <i class="ki-duotone ki-abstract-19 fs-1 text-warning">
                <span class="path1"></span>
                <span class="path2"></span>
              </i>
            </span>
            <!--end::Icon-->

            <!--begin::Content-->
            <div class="flex-grow-1 me-2">
              <!--begin::Title-->
              <a href="#" class="fw-bold text-gray-800 text-hover-primary fs-6">
                {{ quote.patient_name || 'Quote ' + quote.id.slice(0, 8) }}
              </a>
              <!--end::Title-->

              <!--begin::Desc-->
              <span class="text-muted fw-semibold d-block">
                {{ formatCurrency(quote.amount) }} - {{ formatDate(quote.created_on) }}
              </span>
              <!--end::Desc-->
            </div>
            <!--end::Content-->

            <!--begin::Status-->
            <span :class="`badge badge-light-${getStatusColor(quote.status)} fs-8 fw-bold`">
              {{ quote.status.charAt(0).toUpperCase() + quote.status.slice(1) }}
            </span>
            <!--end::Status-->
          </div>
        </div>
        <div v-else class="text-center text-muted py-10">
          No recent quotes found
        </div>
        <!--end::Quotes-->
      </div>

      <div v-if="activeTab === 'trips'" class="tab-content">
        <!--begin::Trips-->
        <div v-if="recentTrips.length > 0">
          <div
            v-for="trip in recentTrips"
            :key="trip.id"
            class="d-flex align-items-center bg-light-primary rounded p-5 mb-7"
          >
            <!--begin::Icon-->
            <span class="svg-icon svg-icon-primary me-5">
              <i class="ki-duotone ki-airplane fs-1 text-primary">
                <span class="path1"></span>
                <span class="path2"></span>
              </i>
            </span>
            <!--end::Icon-->

            <!--begin::Content-->
            <div class="flex-grow-1 me-2">
              <!--begin::Title-->
              <a href="#" class="fw-bold text-gray-800 text-hover-primary fs-6">
                {{ trip.trip_number }}
              </a>
              <!--end::Title-->

              <!--begin::Desc-->
              <span class="text-muted fw-semibold d-block">
                {{ trip.type.charAt(0).toUpperCase() + trip.type.slice(1) }} - 
                {{ formatDate(trip.created_on) }}
              </span>
              <!--end::Desc-->
            </div>
            <!--end::Content-->

            <!--begin::Status-->
            <span :class="`badge badge-light-${getStatusColor(trip.type)} fs-8 fw-bold`">
              {{ trip.type.charAt(0).toUpperCase() + trip.type.slice(1) }}
            </span>
            <!--end::Status-->
          </div>
        </div>
        <div v-else class="text-center text-muted py-10">
          No recent trips found
        </div>
        <!--end::Trips-->
      </div>
      <!--end::Tab Content-->
    </div>
    <!--end::Body-->
  </div>
</template>

<script lang="ts">
import { defineComponent, computed, ref } from "vue";
import { useDashboardStore } from "@/stores/dashboard";

export default defineComponent({
  name: "recent-activity-widget",
  props: {
    className: {
      type: String,
      default: "",
    },
  },
  setup() {
    const dashboardStore = useDashboardStore();
    const activeTab = ref("quotes");

    const stats = computed(() => dashboardStore.stats);

    const recentQuotes = computed(() => 
      stats.value?.recent_activity.quotes || []
    );

    const recentTrips = computed(() => 
      stats.value?.recent_activity.trips || []
    );

    const formatCurrency = (amount: number): string => {
      return dashboardStore.formatCurrency(amount);
    };

    const formatDate = (dateString: string): string => {
      return dashboardStore.formatDate(dateString);
    };

    const getStatusColor = (status: string): string => {
      return dashboardStore.getStatusColor(status);
    };

    return {
      activeTab,
      stats,
      recentQuotes,
      recentTrips,
      formatCurrency,
      formatDate,
      getStatusColor,
    };
  },
});
</script>