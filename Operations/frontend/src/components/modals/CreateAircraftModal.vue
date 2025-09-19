<template>
  <div
    class="modal fade"
    id="kt_modal_create_aircraft"
    ref="modalRef"
    tabindex="-1"
    aria-hidden="true"
  >
    <div class="modal-dialog modal-lg">
      <div class="modal-content">
        <div class="modal-header">
          <h2>Add New Aircraft</h2>
          <div
            class="btn btn-sm btn-icon btn-active-color-primary"
            data-bs-dismiss="modal"
            @click="resetForm"
          >
            <KTIcon icon-name="cross" icon-class="fs-1" />
          </div>
        </div>

        <div class="modal-body py-10 px-lg-17">
          <form @submit.prevent="handleSubmit">
            <div class="row">
              <!-- Basic Information -->
              <div class="col-lg-6">
                <h5 class="mb-4">Aircraft Information</h5>

                <!-- Tail Number -->
                <div class="fv-row mb-7">
                  <label class="fs-6 fw-semibold form-label mt-3">
                    <span class="required">Tail Number</span>
                  </label>
                  <input
                    v-model="formData.tail_number"
                    type="text"
                    class="form-control form-control-solid"
                    placeholder="Enter tail number (e.g., N123AB)"
                    required
                  />
                </div>

                <!-- Company -->
                <div class="fv-row mb-7">
                  <label class="fs-6 fw-semibold form-label mt-3">
                    <span class="required">Company</span>
                  </label>
                  <input
                    v-model="formData.company"
                    type="text"
                    class="form-control form-control-solid"
                    placeholder="Enter company name"
                    required
                  />
                </div>

                <!-- Make -->
                <div class="fv-row mb-7">
                  <label class="fs-6 fw-semibold form-label mt-3">
                    <span class="required">Make</span>
                  </label>
                  <input
                    v-model="formData.make"
                    type="text"
                    class="form-control form-control-solid"
                    placeholder="Enter aircraft make (e.g., Learjet)"
                    required
                  />
                </div>
              </div>

              <!-- Specifications -->
              <div class="col-lg-6">
                <h5 class="mb-4">Specifications</h5>

                <!-- Model -->
                <div class="fv-row mb-7">
                  <label class="fs-6 fw-semibold form-label mt-3">
                    <span class="required">Model</span>
                  </label>
                  <input
                    v-model="formData.model"
                    type="text"
                    class="form-control form-control-solid"
                    placeholder="Enter aircraft model (e.g., 35A)"
                    required
                  />
                </div>

                <!-- Serial Number -->
                <div class="fv-row mb-7">
                  <label class="fs-6 fw-semibold form-label mt-3">
                    <span class="required">Serial Number</span>
                  </label>
                  <input
                    v-model="formData.serial_number"
                    type="text"
                    class="form-control form-control-solid"
                    placeholder="Enter aircraft serial number"
                    required
                  />
                </div>

                <!-- MGTOW -->
                <div class="fv-row mb-7">
                  <label class="fs-6 fw-semibold form-label mt-3">
                    <span class="required">Maximum Gross Takeoff Weight (lbs)</span>
                  </label>
                  <input
                    v-model="formData.mgtow"
                    type="number"
                    step="0.01"
                    class="form-control form-control-solid"
                    placeholder="Enter MGTOW in pounds"
                    required
                  />
                </div>
              </div>
            </div>
          </form>
        </div>

        <div class="modal-footer flex-center">
          <button
            type="reset"
            class="btn btn-light me-3"
            data-bs-dismiss="modal"
            @click="resetForm"
          >
            Cancel
          </button>

          <button
            type="button"
            class="btn btn-primary"
            @click="handleSubmit"
            :disabled="loading"
          >
            <span v-if="!loading">Create Aircraft</span>
            <span v-else>
              Please wait...
              <span class="spinner-border spinner-border-sm align-middle ms-2"></span>
            </span>
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, onMounted } from "vue";
import ApiService from "@/core/services/ApiService";
import { Modal } from "bootstrap";
import Swal from "sweetalert2";

export default defineComponent({
  name: "create-aircraft-modal",
  emits: ["aircraft-created"],
  setup(_, { emit }) {
    const modalRef = ref<HTMLElement | null>(null);
    const modal = ref<Modal | null>(null);
    const loading = ref(false);

    const formData = ref({
      tail_number: "",
      company: "",
      make: "",
      model: "",
      serial_number: "",
      mgtow: null,
    });

    const resetForm = () => {
      formData.value = {
        tail_number: "",
        company: "",
        make: "",
        model: "",
        serial_number: "",
        mgtow: null,
      };
      loading.value = false;
    };

    const handleSubmit = async () => {
      // Validate required fields
      if (!formData.value.tail_number || !formData.value.company || !formData.value.make ||
          !formData.value.model || !formData.value.serial_number || !formData.value.mgtow) {
        Swal.fire("Error", "Please fill in all required fields", "error");
        return;
      }

      try {
        loading.value = true;

        // Prepare data for submission
        const submitData = { ...formData.value };

        const response = await ApiService.post("/aircraft/", submitData);

        // Close modal
        const modalElement = document.getElementById('kt_modal_create_aircraft');
        if (modalElement) {
          modalElement.classList.remove('show');
          modalElement.style.display = 'none';
          modalElement.setAttribute('aria-hidden', 'true');
          modalElement.removeAttribute('aria-modal');

          const backdrop = document.querySelector('.modal-backdrop');
          if (backdrop) {
            backdrop.remove();
          }

          document.body.classList.remove('modal-open');
          document.body.style.paddingRight = '';
        }

        resetForm();
        emit("aircraft-created", response.data);

        // Show success message
        setTimeout(async () => {
          await Swal.fire({
            title: "Success!",
            text: "Aircraft created successfully",
            icon: "success",
            confirmButtonText: "OK"
          });
        }, 100);

      } catch (error: any) {
        console.error("Error creating aircraft:", error);
        Swal.fire({
          title: "Error!",
          text: error.response?.data?.detail || "Failed to create aircraft",
          icon: "error",
          confirmButtonText: "OK"
        });
      } finally {
        loading.value = false;
      }
    };

    onMounted(() => {
      if (modalRef.value) {
        modal.value = new Modal(modalRef.value);
      }
    });

    return {
      modalRef,
      formData,
      loading,
      resetForm,
      handleSubmit,
    };
  },
});
</script>