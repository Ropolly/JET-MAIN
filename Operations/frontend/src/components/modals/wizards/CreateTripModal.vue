<template>
  <!--begin::Modal - Create trip-->
  <div
    class="modal fade"
    id="kt_modal_create_trip"
    ref="modalRef"
    tabindex="-1"
    aria-hidden="true"
  >
    <!--begin::Modal dialog-->
    <div class="modal-dialog mw-1000px">
      <!--begin::Modal content-->
      <div class="modal-content">
        <!--begin::Modal header-->
        <div class="modal-header">
          <!--begin::Title-->
          <h2>Create New Trip</h2>
          <!--end::Title-->

          <!--begin::Close-->
          <div
            class="btn btn-sm btn-icon btn-active-color-primary"
            data-bs-dismiss="modal"
          >
            <KTIcon icon-name="cross" icon-class="fs-1" />
          </div>
          <!--end::Close-->
        </div>
        <!--end::Modal header-->

        <!--begin::Modal body-->
        <div class="modal-body scroll-y m-5">
          <CreateTripHorizontalWizardStepper
            :close-handler="closeModal"
          ></CreateTripHorizontalWizardStepper>
        </div>
        <!--end::Modal body-->
      </div>
      <!--end::Modal content-->
    </div>
    <!--end::Modal dialog-->
  </div>
  <!--end::Modal - Create trip-->
</template>

<script setup lang="ts">
import CreateTripHorizontalWizardStepper from "@/components/wizards/create-trip-wizard/CreateTripHorizontalWizardStepper.vue";
import { hideModal } from "@/core/helpers/modal";

import { ref } from "vue";

const modalRef = ref<HTMLElement | null>(null);

const closeModal = () => {
  hideModal(modalRef.value);
};
</script>