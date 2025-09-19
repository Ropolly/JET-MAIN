<template>
  <div
    class="modal fade"
    id="kt_modal_create_airport"
    ref="modalRef"
    tabindex="-1"
    aria-hidden="true"
  >
    <div class="modal-dialog modal-xl">
      <div class="modal-content">
        <div class="modal-header">
          <h2>Add New Airport</h2>
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
                <h5 class="mb-4">Basic Information</h5>

                <!-- Airport Name -->
                <div class="fv-row mb-7">
                  <label class="fs-6 fw-semibold form-label mt-3">
                    <span class="required">Airport Name</span>
                  </label>
                  <input
                    v-model="formData.name"
                    type="text"
                    class="form-control form-control-solid"
                    placeholder="Enter airport name"
                    required
                  />
                </div>

                <!-- Airport Identifier -->
                <div class="fv-row mb-7">
                  <label class="fs-6 fw-semibold form-label mt-3">
                    <span class="required">Airport Identifier</span>
                  </label>
                  <input
                    v-model="formData.ident"
                    type="text"
                    class="form-control form-control-solid"
                    placeholder="Enter airport identifier"
                    maxlength="10"
                    required
                  />
                </div>

                <!-- Airport Type -->
                <div class="fv-row mb-7">
                  <label class="fs-6 fw-semibold form-label mt-3">
                    <span class="required">Airport Type</span>
                  </label>
                  <select
                    v-model="formData.airport_type"
                    class="form-select form-select-solid"
                    required
                  >
                    <option value="">Select airport type</option>
                    <option value="large_airport">Large Airport</option>
                    <option value="medium_airport">Medium Airport</option>
                    <option value="small_airport">Small Airport</option>
                  </select>
                </div>

                <!-- Timezone -->
                <div class="fv-row mb-7">
                  <label class="fs-6 fw-semibold form-label mt-3">
                    <span class="required">Timezone</span>
                  </label>
                  <input
                    v-model="formData.timezone"
                    type="text"
                    class="form-control form-control-solid"
                    placeholder="e.g., America/New_York"
                    required
                  />
                </div>
              </div>

              <!-- Location Information -->
              <div class="col-lg-6">
                <h5 class="mb-4">Location Information</h5>

                <!-- Coordinates -->
                <div class="row">
                  <div class="col-md-6">
                    <div class="fv-row mb-7">
                      <label class="fs-6 fw-semibold form-label mt-3">
                        <span class="required">Latitude</span>
                      </label>
                      <input
                        v-model="formData.latitude"
                        type="number"
                        step="0.000001"
                        class="form-control form-control-solid"
                        placeholder="Enter latitude"
                        required
                      />
                    </div>
                  </div>
                  <div class="col-md-6">
                    <div class="fv-row mb-7">
                      <label class="fs-6 fw-semibold form-label mt-3">
                        <span class="required">Longitude</span>
                      </label>
                      <input
                        v-model="formData.longitude"
                        type="number"
                        step="0.000001"
                        class="form-control form-control-solid"
                        placeholder="Enter longitude"
                        required
                      />
                    </div>
                  </div>
                </div>

                <!-- Elevation -->
                <div class="fv-row mb-7">
                  <label class="fs-6 fw-semibold form-label mt-3">
                    <span>Elevation (ft)</span>
                  </label>
                  <input
                    v-model="formData.elevation"
                    type="number"
                    class="form-control form-control-solid"
                    placeholder="Enter elevation in feet"
                  />
                </div>

                <!-- Country -->
                <div class="fv-row mb-7">
                  <label class="fs-6 fw-semibold form-label mt-3">
                    <span class="required">Country</span>
                  </label>
                  <input
                    v-model="formData.iso_country"
                    type="text"
                    class="form-control form-control-solid"
                    placeholder="Enter country code (e.g., US)"
                    required
                  />
                </div>

                <!-- Region/State -->
                <div class="fv-row mb-7">
                  <label class="fs-6 fw-semibold form-label mt-3">
                    <span>Region/State</span>
                  </label>
                  <input
                    v-model="formData.iso_region"
                    type="text"
                    class="form-control form-control-solid"
                    placeholder="Enter region/state code"
                  />
                </div>

                <!-- Municipality -->
                <div class="fv-row mb-7">
                  <label class="fs-6 fw-semibold form-label mt-3">
                    <span>Municipality/City</span>
                  </label>
                  <input
                    v-model="formData.municipality"
                    type="text"
                    class="form-control form-control-solid"
                    placeholder="Enter city/municipality"
                  />
                </div>
              </div>
            </div>

            <!-- Airport Codes -->
            <div class="row mt-4">
              <div class="col-lg-12">
                <h5 class="mb-4">Airport Codes</h5>
              </div>
              <div class="col-md-3">
                <div class="fv-row mb-7">
                  <label class="fs-6 fw-semibold form-label mt-3">
                    <span>ICAO Code</span>
                  </label>
                  <input
                    v-model="formData.icao_code"
                    type="text"
                    class="form-control form-control-solid"
                    placeholder="4-letter ICAO"
                    maxlength="4"
                  />
                </div>
              </div>
              <div class="col-md-3">
                <div class="fv-row mb-7">
                  <label class="fs-6 fw-semibold form-label mt-3">
                    <span>IATA Code</span>
                  </label>
                  <input
                    v-model="formData.iata_code"
                    type="text"
                    class="form-control form-control-solid"
                    placeholder="3-letter IATA"
                    maxlength="3"
                  />
                </div>
              </div>
              <div class="col-md-3">
                <div class="fv-row mb-7">
                  <label class="fs-6 fw-semibold form-label mt-3">
                    <span>Local Code</span>
                  </label>
                  <input
                    v-model="formData.local_code"
                    type="text"
                    class="form-control form-control-solid"
                    placeholder="Local identifier"
                    maxlength="10"
                  />
                </div>
              </div>
              <div class="col-md-3">
                <div class="fv-row mb-7">
                  <label class="fs-6 fw-semibold form-label mt-3">
                    <span>GPS Code</span>
                  </label>
                  <input
                    v-model="formData.gps_code"
                    type="text"
                    class="form-control form-control-solid"
                    placeholder="GPS identifier"
                    maxlength="20"
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
            <span v-if="!loading">Create Airport</span>
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
  name: "create-airport-modal",
  emits: ["airport-created"],
  setup(_, { emit }) {
    const modalRef = ref<HTMLElement | null>(null);
    const modal = ref<Modal | null>(null);
    const loading = ref(false);

    const formData = ref({
      name: "",
      ident: "",
      latitude: null,
      longitude: null,
      elevation: null,
      iso_country: "",
      iso_region: "",
      municipality: "",
      icao_code: "",
      iata_code: "",
      local_code: "",
      gps_code: "",
      airport_type: "",
      timezone: "",
    });

    const resetForm = () => {
      formData.value = {
        name: "",
        ident: "",
        latitude: null,
        longitude: null,
        elevation: null,
        iso_country: "",
        iso_region: "",
        municipality: "",
        icao_code: "",
        iata_code: "",
        local_code: "",
        gps_code: "",
        airport_type: "",
        timezone: "",
      };
      loading.value = false;
    };

    const handleSubmit = async () => {
      // Validate required fields
      if (!formData.value.name || !formData.value.ident || !formData.value.latitude ||
          !formData.value.longitude || !formData.value.iso_country || !formData.value.airport_type ||
          !formData.value.timezone) {
        Swal.fire("Error", "Please fill in all required fields", "error");
        return;
      }

      try {
        loading.value = true;

        // Prepare data for submission
        const submitData = { ...formData.value };

        // Convert empty strings to null for optional fields
        Object.keys(submitData).forEach(key => {
          if (submitData[key] === "") {
            submitData[key] = null;
          }
        });

        const response = await ApiService.post("/airports/", submitData);

        // Close modal
        const modalElement = document.getElementById('kt_modal_create_airport');
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
        emit("airport-created", response.data);

        // Show success message
        setTimeout(async () => {
          await Swal.fire({
            title: "Success!",
            text: "Airport created successfully",
            icon: "success",
            confirmButtonText: "OK"
          });
        }, 100);

      } catch (error: any) {
        console.error("Error creating airport:", error);
        Swal.fire({
          title: "Error!",
          text: error.response?.data?.detail || "Failed to create airport",
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