<template>
  <div class="card card-flush" :class="className">
    <!--begin::Header-->
    <div class="card-header pt-5">
      <!--begin::Title-->
      <div class="card-title d-flex flex-column">
        <!--begin::Amount-->
        <span class="fs-2hx fw-bold text-gray-800 me-2 lh-1 ls-n2">
          {{ value }}
        </span>
        <!--end::Amount-->

        <!--begin::Subtitle-->
        <span class="text-gray-500 pt-1 fw-semibold fs-6">{{ title }}</span>
        <!--end::Subtitle-->
      </div>
      <!--end::Title-->
    </div>
    <!--end::Header-->

    <!--begin::Card body-->
    <div class="card-body d-flex align-items-end pt-0">
      <!--begin::Progress-->
      <div class="d-flex align-items-center flex-column mt-3 w-100" v-if="showProgress">
        <div
          class="d-flex justify-content-between fw-bold fs-6 text-gray-500 w-100 mt-auto mb-2"
        >
          <span>{{ progressLabel }}</span>
          <span>{{ progressValue }}%</span>
        </div>

        <div class="h-8px mx-3 w-100 bg-light-primary rounded">
          <div
            class="bg-primary rounded h-8px"
            role="progressbar"
            :style="`width: ${progressValue}%`"
            :aria-valuenow="progressValue"
            aria-valuemin="0"
            aria-valuemax="100"
          ></div>
        </div>
      </div>
      <!--end::Progress-->

      <!--begin::Icon-->
      <div v-else class="d-flex align-items-center">
        <i :class="`ki-duotone ${icon} fs-2x text-${iconColor}`">
          <span class="path1"></span>
          <span class="path2"></span>
        </i>
      </div>
      <!--end::Icon-->
    </div>
    <!--end::Card body-->
  </div>
</template>

<script lang="ts">
import { defineComponent } from "vue";

export default defineComponent({
  name: "stats-widget",
  props: {
    className: {
      type: String,
      default: "",
    },
    title: {
      type: String,
      required: true,
    },
    value: {
      type: [String, Number],
      required: true,
    },
    icon: {
      type: String,
      default: "ki-abstract-39",
    },
    iconColor: {
      type: String,
      default: "primary",
    },
    showProgress: {
      type: Boolean,
      default: false,
    },
    progressLabel: {
      type: String,
      default: "",
    },
    progressValue: {
      type: Number,
      default: 0,
    },
  },
});
</script>