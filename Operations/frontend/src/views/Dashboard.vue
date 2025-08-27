<template>
  <!--begin::Row-->
  <div class="row g-5 g-xl-10 mb-5 mb-xl-10">
    <!--begin::Col-->
    <div class="col-md-6 col-lg-6 col-xl-6 col-xxl-3 mb-md-5 mb-xl-10">
      <TripsWidget
        className="h-md-50 mb-5 mb-xl-10"
        bgColor="#1B84FF"
        :bgImage="getAssetPath('media/patterns/vector-1.png')"
      />

      <StatsWidget
        className="h-md-50 mb-5 mb-xl-10"
        title="Active Patients"
        :value="dashboardStore.stats?.patient_stats.active || 0"
        icon="ki-heart"
        iconColor="danger"
        :showProgress="true"
        :progressLabel="`${dashboardStore.stats?.patient_stats.total || 0} Total`"
        :progressValue="patientActivityPercentage"
      />
    </div>
    <!--end::Col-->

    <!--begin::Col-->
    <div class="col-md-6 col-lg-6 col-xl-6 col-xxl-3 mb-md-5 mb-xl-10">
      <QuotesWidget
        className="h-md-50 mb-5 mb-xl-10"
        bgColor="#F1416C"
        :bgImage="getAssetPath('media/patterns/vector-1.png')"
      />

      <StatsWidget
        className="h-md-50 mb-5 mb-xl-10"
        title="Aircraft Fleet"
        :value="dashboardStore.stats?.aircraft_stats.total || 0"
        icon="ki-airplane"
        iconColor="success"
      />
    </div>
    <!--end::Col-->

    <!--begin::Col-->
    <div class="col-xxl-6">
      <UpcomingTripsWidget className="h-md-100" />
    </div>
    <!--end::Col-->
  </div>
  <!--end::Row-->

  <!--begin::Row-->
  <div class="row gx-5 gx-xl-10">
    <!--begin::Col-->
    <div class="col-xxl-6 mb-5 mb-xl-10">
      <RecentActivityWidget className="h-xl-100" />
    </div>
    <!--end::Col-->

    <!--begin::Col-->
    <div class="col-xl-6 mb-5 mb-xl-10">
      <QuoteStatusChart className="h-xl-100" />
    </div>
    <!--end::Col-->
  </div>
  <!--end::Row-->

  <!--begin::Row-->
  <div class="row g-5 g-xl-10 mb-5 mb-xl-10">
    <!--begin::Col-->
    <div class="col-12">
      <RecentQuotesWidget className="h-xl-100" />
    </div>
    <!--end::Col-->
  </div>
  <!--end::Row-->
</template>

<script lang="ts">
import { getAssetPath } from "@/core/helpers/assets";
import { defineComponent, onMounted, computed } from "vue";
import { useDashboardStore } from "@/stores/dashboard";

// Import our custom widgets
import TripsWidget from "@/components/dashboard-default-widgets/TripsWidget.vue";
import QuotesWidget from "@/components/dashboard-default-widgets/QuotesWidget.vue";
import UpcomingTripsWidget from "@/components/dashboard-default-widgets/UpcomingTripsWidget.vue";
import RecentQuotesWidget from "@/components/dashboard-default-widgets/RecentQuotesWidget.vue";
import RecentActivityWidget from "@/components/dashboard-default-widgets/RecentActivityWidget.vue";
import StatsWidget from "@/components/dashboard-default-widgets/StatsWidget.vue";

// Import placeholder chart components (we'll keep these)
import QuoteStatusChart from "@/components/dashboard-default-widgets/QuoteStatusChart.vue";

export default defineComponent({
  name: "jet-operations-dashboard",
  components: {
    TripsWidget,
    QuotesWidget,
    UpcomingTripsWidget,
    RecentQuotesWidget,
    RecentActivityWidget,
    StatsWidget,
    QuoteStatusChart,
  },
  setup() {
    const dashboardStore = useDashboardStore();

    const patientActivityPercentage = computed(() => {
      const stats = dashboardStore.stats;
      if (!stats?.patient_stats) return 0;
      
      const { active, total } = stats.patient_stats;
      return total > 0 ? Math.round((active / total) * 100) : 0;
    });

    // Fetch dashboard data on component mount
    onMounted(async () => {
      try {
        await dashboardStore.fetchStats();
      } catch (error) {
        console.error("Failed to load dashboard data:", error);
      }
    });

    return {
      dashboardStore,
      patientActivityPercentage,
      getAssetPath,
    };
  },
});
</script>