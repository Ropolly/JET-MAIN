<template>
  <div class="card card-flush" :class="className">
    <!--begin::Header-->
    <div class="card-header pt-5">
      <!--begin::Title-->
      <h3 class="card-title text-gray-800 fw-bold">Trip Types Distribution</h3>
      <!--end::Title-->
    </div>
    <!--end::Header-->

    <!--begin::Body-->
    <div class="card-body pt-6">
      <!--begin::Chart container-->
      <div id="trip_types_chart" class="d-flex justify-content-center"></div>
      <!--end::Chart container-->

      <!--begin::Labels-->
      <div class="d-flex flex-wrap mt-5">
        <div
          v-for="(tripType, index) in typesBreakdown"
          :key="tripType.type"
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
            {{ tripType.type.charAt(0).toUpperCase() + tripType.type.slice(1) }}
            ({{ tripType.count }})
          </div>
          <!--end::Label-->
        </div>
      </div>
      <!--end::Labels-->

      <!--begin::Progress bars-->
      <div class="pt-5">
        <div
          v-for="(tripType, index) in typesBreakdown"
          :key="tripType.type"
          class="d-flex align-items-center mb-7"
        >
          <!--begin::Label-->
          <div class="flex-grow-1 me-4">
            <div class="fs-sm fw-bold text-gray-800 d-flex align-items-center">
              <i :class="`ki-duotone ${getTripIcon(tripType.type)} fs-2 me-3`" :style="`color: ${colors[index % colors.length]}`">
                <span class="path1"></span>
                <span class="path2"></span>
              </i>
              {{ tripType.type.charAt(0).toUpperCase() + tripType.type.slice(1) }}
            </div>
          </div>
          <!--end::Label-->

          <!--begin::Progress-->
          <div class="d-flex align-items-center w-200px">
            <span class="me-3 fw-semibold text-gray-400 fs-7">{{ tripType.count }}</span>
            <div class="progress h-6px w-100 bg-light-success">
              <div 
                class="progress-bar"
                :style="`width: ${getPercentage(tripType.count)}%; background-color: ${colors[index % colors.length]}`"
                role="progressbar"
              ></div>
            </div>
          </div>
          <!--end::Progress-->
        </div>
      </div>
      <!--end::Progress bars-->
    </div>
    <!--end::Body-->
  </div>
</template>

<script lang="ts">
import { defineComponent, computed, onMounted, nextTick } from "vue";
import { useDashboardStore } from "@/stores/dashboard";

export default defineComponent({
  name: "trip-types-chart",
  props: {
    className: {
      type: String,
      default: "",
    },
  },
  setup() {
    const dashboardStore = useDashboardStore();

    const stats = computed(() => dashboardStore.stats);

    const typesBreakdown = computed(() => 
      stats.value?.trip_stats.types_breakdown || []
    );

    const colors = [
      "#F1416C", // Medical - Red
      "#3E97FF", // Charter - Blue
      "#FFC700", // Part 91 - Yellow
      "#50CD89", // Other - Green
      "#7239EA"  // Maintenance - Purple
    ];

    const totalTrips = computed(() => 
      typesBreakdown.value.reduce((sum, item) => sum + item.count, 0)
    );

    const getTripIcon = (type: string): string => {
      const icons: Record<string, string> = {
        medical: "ki-heart",
        charter: "ki-airplane",
        "part 91": "ki-setting-2",
        other: "ki-abstract-39",
        maintenance: "ki-wrench"
      };
      return icons[type] || "ki-abstract-39";
    };

    const getPercentage = (count: number): number => {
      return totalTrips.value > 0 ? (count / totalTrips.value) * 100 : 0;
    };

    const initChart = () => {
      if (!stats.value || typesBreakdown.value.length === 0) return;

      const chartElement = document.getElementById("trip_types_chart");
      if (chartElement) {
        chartElement.innerHTML = `
          <div class="d-flex flex-column align-items-center">
            <div class="fs-2hx fw-bold text-gray-800 mb-2">${totalTrips.value}</div>
            <div class="fs-6 text-gray-500">Total Trips</div>
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
      typesBreakdown,
      colors,
      totalTrips,
      getTripIcon,
      getPercentage,
    };
  },
});
</script>