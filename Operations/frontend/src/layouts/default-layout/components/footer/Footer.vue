<template>
  <!--begin::Footer-->
  <div v-if="footerDisplay" id="kt_app_footer" class="app-footer">
    <!--begin::Footer container-->
    <div
      class="app-container d-flex flex-column flex-md-row flex-center flex-md-stack py-3"
      :class="{
        'container-fluid': footerWidthFluid,
        'container-xxl': !footerWidthFluid,
      }"
    >
      <!--begin::Copyright-->
      <div class="text-gray-900 order-2 order-md-1">
        <span class="text-muted fw-semibold me-1">{{ currentYear }}©</span>
        <span class="text-gray-800">JET Med</span>
      </div>
      <!--end::Copyright-->
    </div>
    <!--end::Footer container-->
  </div>
  <!--end::Footer-->
</template>

<script lang="ts">
import { defineComponent, computed } from "vue";
import { footerDisplay, footerWidthFluid } from "@/layouts/default-layout/config/helper";

export default defineComponent({
  name: "theme-footer",
  components: {},
  setup() {
    const currentYear = computed(() => new Date().getFullYear());

    return {
      footerWidthFluid,
      footerDisplay,
      currentYear,
    };
  },
});
</script>