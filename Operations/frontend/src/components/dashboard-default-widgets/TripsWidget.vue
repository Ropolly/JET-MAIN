<template>
  <div
    class="card card-flush bgi-no-repeat bgi-size-contain bgi-position-x-end"
    :class="className"
    :style="{ backgroundColor: bgColor, backgroundImage: `url('${bgImage}')` }"
  >
    <!--begin::Header-->
    <div class="card-header pt-5">
      <!--begin::Title-->
      <div class="card-title d-flex flex-column">
        <!--begin::Amount-->
        <span class="fs-2hx fw-bold text-white me-2 lh-1 ls-n2">
          {{ stats?.trip_stats.total || 0 }}
        </span>
        <!--end::Amount-->

        <!--begin::Subtitle-->
        <span class="text-white opacity-50 pt-1 fw-semibold fs-6">
          Total Trips
        </span>
        <!--end::Subtitle-->
      </div>
      <!--end::Title-->
    </div>
    <!--end::Header-->

    <!--begin::Card body-->
    <div class="card-body d-flex align-items-end pt-0">
      <!--begin::Progress-->
      <div class="d-flex align-items-center flex-column mt-3 w-100">
        <div
          class="d-flex justify-content-between fw-bold fs-6 text-white opacity-50 w-100 mt-auto mb-2"
        >
          <span>{{ stats?.trip_stats.active || 0 }} Active</span>
          <span>{{ activityPercentage }}%</span>
        </div>

        <div class="h-8px mx-3 w-100 bg-white bg-opacity-50 rounded">
          <div
            class="bg-white rounded h-8px"
            role="progressbar"
            :style="`width: ${activityPercentage}%`"
            :aria-valuenow="activityPercentage"
            aria-valuemin="0"
            aria-valuemax="100"
          ></div>
        </div>
      </div>
      <!--end::Progress-->
    </div>
    <!--end::Card body-->
  </div>
</template>

<script lang="ts">
import { defineComponent, computed } from "vue";
import { useDashboardStore } from "@/stores/dashboard";

export default defineComponent({
  name: "trips-widget",
  props: {
    className: {
      type: String,
      default: "",
    },
    bgColor: {
      type: String,
      default: "#1B84FF",
    },
    bgImage: {
      type: String,
      default: "",
    },
  },
  setup() {
    const dashboardStore = useDashboardStore();

    const stats = computed(() => dashboardStore.stats);
    
    const activityPercentage = computed(() => {
      return dashboardStore.getTripActivityPercentage();
    });

    return {
      stats,
      activityPercentage,
    };
  },
});
</script>