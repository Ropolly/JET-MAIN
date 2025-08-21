<template>
  <div class="card card-flush" :class="className">
    <!--begin::Header-->
    <div class="card-header pt-5">
      <!--begin::Title-->
      <h3 class="card-title text-gray-800 fw-bold">Quote Status Overview</h3>
      <!--end::Title-->
    </div>
    <!--end::Header-->

    <!--begin::Body-->
    <div class="card-body pt-6">
      <!--begin::Chart container-->
      <div id="quote_status_chart" class="d-flex justify-content-center"></div>
      <!--end::Chart container-->

      <!--begin::Labels-->
      <div class="d-flex flex-wrap mt-5">
        <div
          v-for="(status, index) in statusBreakdown"
          :key="status.status"
          class="d-flex align-items-center me-7 mb-2"
        >
          <!--begin::Bullet-->
          <div 
            :class="`bullet bullet-dot w-8px h-6px rounded-2 me-2`"
            :style="`background-color: ${colors[index % colors.length]}`"
          ></div>
          <!--end::Bullet-->

          <!--begin::Label-->
          <div class="fs-sm fw-semibold text-gray-400">
            {{ status.status.charAt(0).toUpperCase() + status.status.slice(1) }}
            ({{ status.count }})
          </div>
          <!--end::Label-->
        </div>
      </div>
      <!--end::Labels-->
    </div>
    <!--end::Body-->
  </div>
</template>

<script lang="ts">
import { defineComponent, computed, onMounted, nextTick } from "vue";
import { useDashboardStore } from "@/stores/dashboard";

export default defineComponent({
  name: "quote-status-chart",
  props: {
    className: {
      type: String,
      default: "",
    },
  },
  setup() {
    const dashboardStore = useDashboardStore();

    const stats = computed(() => dashboardStore.stats);

    const statusBreakdown = computed(() => 
      stats.value?.quote_stats.statuses_breakdown || []
    );

    const colors = [
      "#3E97FF", 
      "#F1416C", 
      "#50CD89", 
      "#FFC700", 
      "#7239EA",
      "#FF6B35"
    ];

    const initChart = () => {
      if (!stats.value || statusBreakdown.value.length === 0) return;

      // Simple representation without ApexCharts for now
      // In a real implementation, you'd use ApexCharts or Chart.js here
      const chartElement = document.getElementById("quote_status_chart");
      if (chartElement) {
        const total = statusBreakdown.value.reduce((sum, item) => sum + item.count, 0);
        
        chartElement.innerHTML = `
          <div class="d-flex flex-column align-items-center">
            <div class="fs-2hx fw-bold text-gray-800 mb-2">${total}</div>
            <div class="fs-6 text-gray-500">Total Quotes</div>
          </div>
        `;
      }
    };

    onMounted(async () => {
      await nextTick();
      initChart();
    });

    return {
      stats,
      statusBreakdown,
      colors,
    };
  },
});
</script>