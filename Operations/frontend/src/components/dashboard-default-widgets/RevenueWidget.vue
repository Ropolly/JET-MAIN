<template>
  <div class="card card-flush" :class="className">
    <!--begin::Header-->
    <div class="card-header pt-5">
      <!--begin::Title-->
      <div class="card-title d-flex flex-column">
        <!--begin::Info-->
        <div class="d-flex align-items-center">
          <!--begin::Currency-->
          <span class="fs-4 fw-semibold text-gray-500 me-1 align-self-start">$</span>
          <!--end::Currency-->

          <!--begin::Amount-->
          <span class="fs-2hx fw-bold text-gray-800 me-2 lh-1 ls-n2">
            {{ formattedRevenue }}
          </span>
          <!--end::Amount-->

          <!--begin::Badge-->
          <span :class="`badge badge-light-${badgeColor} fs-base`">
            <i class="ki-duotone ki-arrow-up fs-5 text-success ms-n1">
              <span class="path1"></span>
              <span class="path2"></span>
            </i>
            {{ revenueGrowth }}%
          </span>
          <!--end::Badge-->
        </div>
        <!--end::Info-->

        <!--begin::Subtitle-->
        <span class="text-gray-500 pt-1 fw-semibold fs-6">Total Revenue</span>
        <!--end::Subtitle-->
      </div>
      <!--end::Title-->
    </div>
    <!--end::Header-->

    <!--begin::Card body-->
    <div class="card-body pt-2 pb-4 d-flex flex-wrap align-items-center">
      <!--begin::Chart-->
      <div class="d-flex flex-center me-5 pt-2">
        <div
          id="kt_card_widget_17_chart"
          style="min-width: 70px; min-height: 70px"
          :data-kt-size="size"
          :data-kt-color="chartColor"
        ></div>
      </div>
      <!--end::Chart-->

      <!--begin::Labels-->
      <div class="d-flex flex-column content-justify-center flex-row-fluid">
        <!--begin::Label-->
        <div class="d-flex fw-semibold align-items-center">
          <!--begin::Bullet-->
          <div class="bullet w-8px h-3px rounded-2 bg-success me-3"></div>
          <!--end::Bullet-->

          <!--begin::Label-->
          <div class="text-gray-500 flex-grow-1 me-4">Completed</div>
          <!--end::Label-->

          <!--begin::Stats-->
          <div class="fw-bolder text-gray-700 text-xxl-end">
            {{ formatCurrency(stats?.financial_stats.total_revenue || 0) }}
          </div>
          <!--end::Stats-->
        </div>
        <!--end::Label-->

        <!--begin::Label-->
        <div class="d-flex fw-semibold align-items-center my-3">
          <!--begin::Bullet-->
          <div class="bullet w-8px h-3px rounded-2 bg-primary me-3"></div>
          <!--end::Bullet-->

          <!--begin::Label-->
          <div class="text-gray-500 flex-grow-1 me-4">Pending</div>
          <!--end::Label-->

          <!--begin::Stats-->
          <div class="fw-bolder text-gray-700 text-xxl-end">
            {{ formatCurrency(stats?.financial_stats.pending_revenue || 0) }}
          </div>
          <!--end::Stats-->
        </div>
        <!--end::Label-->

        <!--begin::Label-->
        <div class="d-flex fw-semibold align-items-center">
          <!--begin::Bullet-->
          <div class="bullet w-8px h-3px rounded-2 bg-gray-300 me-3"></div>
          <!--end::Bullet-->

          <!--begin::Label-->
          <div class="text-gray-500 flex-grow-1 me-4">Patients</div>
          <!--end::Label-->

          <!--begin::Stats-->
          <div class="fw-bolder text-gray-700 text-xxl-end">
            {{ stats?.patient_stats.total || 0 }}
          </div>
          <!--end::Stats-->
        </div>
        <!--end::Label-->
      </div>
      <!--end::Labels-->
    </div>
    <!--end::Card body-->
  </div>
</template>

<script lang="ts">
import { defineComponent, computed, onMounted } from "vue";
import { useDashboardStore } from "@/stores/dashboard";

export default defineComponent({
  name: "revenue-widget",
  props: {
    className: {
      type: String,
      default: "",
    },
    chartColor: {
      type: String,
      default: "success",
    },
    size: {
      type: String,
      default: "70",
    },
  },
  setup() {
    const dashboardStore = useDashboardStore();

    const stats = computed(() => dashboardStore.stats);

    const formattedRevenue = computed(() => {
      const revenue = stats.value?.financial_stats.total_revenue || 0;
      if (revenue >= 1000000) {
        return (revenue / 1000000).toFixed(1) + "M";
      } else if (revenue >= 1000) {
        return (revenue / 1000).toFixed(0) + "K";
      }
      return revenue.toString();
    });

    const formatCurrency = (amount: number): string => {
      return dashboardStore.formatCurrency(amount);
    };

    const badgeColor = computed(() => "success");
    const revenueGrowth = computed(() => "8.2"); // This could be calculated from historical data

    onMounted(() => {
      // Initialize chart if needed
      // Chart initialization code would go here
    });

    return {
      stats,
      formattedRevenue,
      formatCurrency,
      badgeColor,
      revenueGrowth,
    };
  },
});
</script>