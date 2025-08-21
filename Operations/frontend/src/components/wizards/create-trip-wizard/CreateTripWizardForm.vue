<template>
  <!--begin::Form-->
  <form class="form" id="kt_create_trip_form">
    <!--begin::Step 1-->
    <div class="current" data-kt-stepper-element="content">
      <CreateTripStep1 />
    </div>
    <!--end::Step 1-->

    <!--begin::Step 2-->
    <div data-kt-stepper-element="content">
      <CreateTripStep2 />
    </div>
    <!--end::Step 2-->

    <!--begin::Step 3-->
    <div data-kt-stepper-element="content">
      <CreateTripStep3 />
    </div>
    <!--end::Step 3-->

    <!--begin::Step 4-->
    <div data-kt-stepper-element="content">
      <CreateTripStep4 />
    </div>
    <!--end::Step 4-->

    <!--begin::Step 5-->
    <div data-kt-stepper-element="content">
      <CreateTripStep5 />
    </div>
    <!--end::Step 5-->

    <!--begin::Actions-->
    <div class="d-flex flex-stack pt-10">
      <!--begin::Wrapper-->
      <div class="me-2">
        <button
          type="button"
          class="btn btn-lg btn-light-primary me-3"
          data-kt-stepper-action="previous"
          @click="previousStep"
        >
          <KTIcon icon-name="arrow-left" icon-class="fs-4 me-1" />
          Back
        </button>
      </div>
      <!--end::Wrapper-->

      <!--begin::Wrapper-->
      <div>
        <button
          type="button"
          class="btn btn-lg btn-primary me-3"
          data-kt-stepper-action="submit"
          @click="handleSubmit"
          :disabled="isSubmitting"
        >
          <span v-if="!isSubmitting" class="indicator-label">
            Submit
            <KTIcon icon-name="arrow-right" icon-class="fs-4 ms-1" />
          </span>
          <span v-else class="indicator-progress">
            Please wait...
            <span
              class="spinner-border spinner-border-sm align-middle ms-2"
            ></span>
          </span>
        </button>

        <button
          type="button"
          class="btn btn-lg btn-primary"
          data-kt-stepper-action="next"
          @click="nextStep"
        >
          Continue
          <KTIcon icon-name="arrow-right" icon-class="fs-4 ms-1" />
        </button>
      </div>
      <!--end::Wrapper-->
    </div>
    <!--end::Actions-->
  </form>
  <!--end::Form-->
</template>

<script setup lang="ts">
import { onMounted, ref } from "vue";
import { StepperComponent } from "@/assets/ts/components";
import CreateTripStep1 from "./steps/CreateTripStep1.vue";
import CreateTripStep2 from "./steps/CreateTripStep2.vue";
import CreateTripStep3 from "./steps/CreateTripStep3.vue";
import CreateTripStep4 from "./steps/CreateTripStep4.vue";
import CreateTripStep5 from "./steps/CreateTripStep5.vue";
import Swal from "sweetalert2";

const props = defineProps<{
  stepperEl: HTMLElement | null;
  closeHandler: () => void;
}>();

const isSubmitting = ref(false);
let stepper: StepperComponent | null = null;

const nextStep = () => {
  if (!stepper) return;
  
  // Validate current step before proceeding
  if (stepper.getCurrentStepIndex() === 1) {
    if (!validateStep1()) return;
  } else if (stepper.getCurrentStepIndex() === 2) {
    if (!validateStep2()) return;
  } else if (stepper.getCurrentStepIndex() === 3) {
    if (!validateStep3()) return;
  } else if (stepper.getCurrentStepIndex() === 4) {
    if (!validateStep4()) return;
  }
  
  stepper.goNext();
};

const previousStep = () => {
  if (!stepper) return;
  stepper.goPrev();
};

const handleSubmit = async () => {
  if (!validateStep5()) return;
  
  isSubmitting.value = true;
  
  try {
    // Simulate API call
    await new Promise(resolve => setTimeout(resolve, 2000));
    
    Swal.fire({
      title: "Success!",
      text: "Trip has been created successfully.",
      icon: "success",
      confirmButtonText: "OK"
    }).then(() => {
      props.closeHandler();
    });
  } catch (error) {
    Swal.fire({
      title: "Error!",
      text: "Failed to create trip. Please try again.",
      icon: "error",
      confirmButtonText: "OK"
    });
  } finally {
    isSubmitting.value = false;
  }
};

// Validation functions
const validateStep1 = (): boolean => {
  // Add validation for trip type step
  return true;
};

const validateStep2 = (): boolean => {
  // Add validation for patient info step
  return true;
};

const validateStep3 = (): boolean => {
  // Add validation for flight details step
  return true;
};

const validateStep4 = (): boolean => {
  // Add validation for aircraft & crew step
  return true;
};

const validateStep5 = (): boolean => {
  // Add validation for review step
  return true;
};

onMounted(() => {
  if (props.stepperEl) {
    stepper = StepperComponent.createInsance(props.stepperEl);
  }
});
</script>