<template>
  <!--begin::Stepper-->
  <div
    class="stepper stepper-links d-flex flex-column"
    id="kt_create_trip_stepper"
    ref="createTripStepperRef"
  >
    <!--begin::Nav-->
    <div class="stepper-nav py-5 mt-5">
      <!--begin::Step 1-->
      <div class="stepper-item current" data-kt-stepper-element="nav">
        <h3 class="stepper-title">Trip Type</h3>
      </div>
      <!--end::Step 1-->

      <!--begin::Step 2-->
      <div class="stepper-item" data-kt-stepper-element="nav">
        <h3 class="stepper-title">Patient Info</h3>
      </div>
      <!--end::Step 2-->

      <!--begin::Step 3-->
      <div class="stepper-item" data-kt-stepper-element="nav">
        <h3 class="stepper-title">Flight Details</h3>
      </div>
      <!--end::Step 3-->

      <!--begin::Step 4-->
      <div class="stepper-item" data-kt-stepper-element="nav">
        <h3 class="stepper-title">Aircraft & Crew</h3>
      </div>
      <!--end::Step 4-->

      <!--begin::Step 5-->
      <div class="stepper-item" data-kt-stepper-element="nav">
        <h3 class="stepper-title">Review & Create</h3>
      </div>
      <!--end::Step 5-->
    </div>
    <!--end::Nav-->

    <CreateTripWizardForm
      :stepper-el="createTripStepperRef"
      :close-handler="props.closeHandler"
    />
  </div>
  <!--end::Stepper-->
</template>

<script setup lang="ts">
import CreateTripWizardForm from "@/components/wizards/create-trip-wizard/CreateTripWizardForm.vue";
import { ref } from "vue";

const props = defineProps<{
  closeHandler: () => void;
}>();

const createTripStepperRef = ref<HTMLElement | null>(null);
</script>