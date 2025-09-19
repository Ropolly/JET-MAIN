<template>
  <div
    class="modal fade"
    id="kt_modal_create_fbo"
    ref="modalRef"
    tabindex="-1"
    aria-hidden="true"
  >
    <div class="modal-dialog modal-lg">
      <div class="modal-content">
        <div class="modal-header">
          <h2>Add New FBO</h2>
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
              <div class="col-lg-12">
                <!-- FBO Name -->
                <div class="fv-row mb-7">
                  <label class="fs-6 fw-semibold form-label mt-3">
                    <span class="required">FBO Name</span>
                  </label>
                  <input
                    v-model="formData.name"
                    type="text"
                    class="form-control form-control-solid"
                    placeholder="Enter FBO name"
                    required
                  />
                </div>

                <!-- Airport Search -->
                <div class="fv-row mb-7">
                  <label class="fs-6 fw-semibold form-label mt-3">
                    <span>Airports</span>
                  </label>
                  <div class="position-relative">
                    <input
                      v-model="airportSearchQuery"
                      @input="searchAirports"
                      @focus="showAirportDropdown = true"
                      type="text"
                      class="form-control form-control-solid"
                      placeholder="Search for airports..."
                    />
                    <div
                      v-if="showAirportDropdown && (airportSearchResults.length > 0 || airportSearchQuery.length >= 2)"
                      class="dropdown-menu show w-100 mt-1"
                      style="max-height: 200px; overflow-y: auto;"
                    >
                      <div v-if="airportSearchLoading" class="dropdown-item text-center">
                        <span class="spinner-border spinner-border-sm me-2"></span>
                        Searching...
                      </div>
                      <div v-else-if="airportSearchResults.length === 0 && airportSearchQuery.length >= 2" class="dropdown-item text-muted">
                        No airports found
                      </div>
                      <div
                        v-else
                        v-for="airport in airportSearchResults"
                        :key="airport.id"
                        @click="addAirport(airport)"
                        class="dropdown-item cursor-pointer"
                      >
                        <strong>{{ airport.ident }}</strong> - {{ airport.name }}
                        <br>
                        <small class="text-muted">{{ airport.municipality }}, {{ airport.iso_country }}</small>
                      </div>
                    </div>
                  </div>

                  <!-- Selected Airports -->
                  <div v-if="selectedAirports.length > 0" class="mt-3">
                    <label class="fs-7 fw-semibold text-muted">Selected Airports:</label>
                    <div class="d-flex flex-wrap gap-2 mt-2">
                      <span
                        v-for="airport in selectedAirports"
                        :key="airport.id"
                        class="badge badge-light-primary d-flex align-items-center"
                      >
                        {{ airport.ident }} - {{ airport.name }}
                        <button
                          @click="removeAirport(airport.id)"
                          type="button"
                          class="btn btn-sm btn-icon ms-2"
                          style="width: 16px; height: 16px;"
                        >
                          <i class="ki-duotone ki-cross fs-7"></i>
                        </button>
                      </span>
                    </div>
                  </div>
                </div>

                <!-- Email -->
                <div class="fv-row mb-7">
                  <label class="fs-6 fw-semibold form-label mt-3">
                    <span>Email</span>
                  </label>
                  <input
                    v-model="formData.email"
                    type="email"
                    class="form-control form-control-solid"
                    placeholder="Enter email address"
                  />
                </div>

                <!-- Phone Numbers -->
                <div class="row">
                  <div class="col-md-6">
                    <div class="fv-row mb-7">
                      <label class="fs-6 fw-semibold form-label mt-3">
                        <span>Primary Phone</span>
                      </label>
                      <input
                        v-model="formData.phone"
                        type="text"
                        class="form-control form-control-solid"
                        placeholder="Enter primary phone"
                      />
                    </div>
                  </div>
                  <div class="col-md-6">
                    <div class="fv-row mb-7">
                      <label class="fs-6 fw-semibold form-label mt-3">
                        <span>Secondary Phone</span>
                      </label>
                      <input
                        v-model="formData.phone_secondary"
                        type="text"
                        class="form-control form-control-solid"
                        placeholder="Enter secondary phone"
                      />
                    </div>
                  </div>
                </div>

                <!-- Address -->
                <div class="fv-row mb-7">
                  <label class="fs-6 fw-semibold form-label mt-3">
                    <span>Address Line 1</span>
                  </label>
                  <input
                    v-model="formData.address_line1"
                    type="text"
                    class="form-control form-control-solid"
                    placeholder="Enter street address"
                  />
                </div>

                <div class="fv-row mb-7">
                  <label class="fs-6 fw-semibold form-label mt-3">
                    <span>Address Line 2</span>
                  </label>
                  <input
                    v-model="formData.address_line2"
                    type="text"
                    class="form-control form-control-solid"
                    placeholder="Enter suite, building, etc."
                  />
                </div>

                <!-- City, State, ZIP -->
                <div class="row">
                  <div class="col-md-4">
                    <div class="fv-row mb-7">
                      <label class="fs-6 fw-semibold form-label mt-3">
                        <span>City</span>
                      </label>
                      <input
                        v-model="formData.city"
                        type="text"
                        class="form-control form-control-solid"
                        placeholder="Enter city"
                      />
                    </div>
                  </div>
                  <div class="col-md-4">
                    <div class="fv-row mb-7">
                      <label class="fs-6 fw-semibold form-label mt-3">
                        <span>State/Province</span>
                      </label>
                      <input
                        v-model="formData.state"
                        type="text"
                        class="form-control form-control-solid"
                        placeholder="Enter state"
                      />
                    </div>
                  </div>
                  <div class="col-md-4">
                    <div class="fv-row mb-7">
                      <label class="fs-6 fw-semibold form-label mt-3">
                        <span>ZIP/Postal Code</span>
                      </label>
                      <input
                        v-model="formData.zip"
                        type="text"
                        class="form-control form-control-solid"
                        placeholder="Enter ZIP code"
                      />
                    </div>
                  </div>
                </div>

                <!-- Country -->
                <div class="fv-row mb-7">
                  <label class="fs-6 fw-semibold form-label mt-3">
                    <span>Country</span>
                  </label>
                  <input
                    v-model="formData.country"
                    type="text"
                    class="form-control form-control-solid"
                    placeholder="Enter country"
                  />
                </div>

                <!-- Notes -->
                <div class="fv-row mb-15">
                  <label class="fs-6 fw-semibold form-label mt-3">
                    <span>Notes</span>
                  </label>
                  <textarea
                    v-model="formData.notes"
                    class="form-control form-control-solid"
                    rows="3"
                    placeholder="Enter additional notes or comments"
                  ></textarea>
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
            <span v-if="!loading">Create FBO</span>
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
import { defineComponent, ref, onMounted, onUnmounted } from "vue";
import ApiService from "@/core/services/ApiService";
import { Modal } from "bootstrap";
import Swal from "sweetalert2";

export default defineComponent({
  name: "create-fbo-modal",
  emits: ["fbo-created"],
  setup(_, { emit }) {
    const modalRef = ref<HTMLElement | null>(null);
    const modal = ref<Modal | null>(null);
    const loading = ref(false);

    const formData = ref({
      name: "",
      email: "",
      phone: "",
      phone_secondary: "",
      address_line1: "",
      address_line2: "",
      city: "",
      state: "",
      zip: "",
      country: "",
      notes: "",
      airports: [] as string[],
    });

    // Airport search functionality
    const airportSearchQuery = ref("");
    const airportSearchResults = ref([]);
    const airportSearchLoading = ref(false);
    const showAirportDropdown = ref(false);
    const selectedAirports = ref([]);
    let searchTimeout: number | null = null;

    const resetForm = () => {
      formData.value = {
        name: "",
        email: "",
        phone: "",
        phone_secondary: "",
        address_line1: "",
        address_line2: "",
        city: "",
        state: "",
        zip: "",
        country: "",
        notes: "",
        airports: [],
      };
      // Reset airport search state
      airportSearchQuery.value = "";
      airportSearchResults.value = [];
      showAirportDropdown.value = false;
      selectedAirports.value = [];
      loading.value = false;
    };

    // Airport search methods
    const searchAirports = async () => {
      const query = airportSearchQuery.value.trim();

      if (query.length < 2) {
        airportSearchResults.value = [];
        return;
      }

      // Debounce search
      if (searchTimeout) {
        clearTimeout(searchTimeout);
      }

      searchTimeout = window.setTimeout(async () => {
        try {
          airportSearchLoading.value = true;
          const response = await ApiService.get(`/airports/search/?q=${encodeURIComponent(query)}`);
          // The search endpoint returns data directly, not in a results wrapper
          airportSearchResults.value = response.data || [];
        } catch (error) {
          console.error("Error searching airports:", error);
          airportSearchResults.value = [];
        } finally {
          airportSearchLoading.value = false;
        }
      }, 300);
    };

    const addAirport = (airport) => {
      // Check if airport is already selected
      if (!selectedAirports.value.find(a => a.id === airport.id)) {
        selectedAirports.value.push(airport);
        formData.value.airports = selectedAirports.value.map(a => a.id);
      }

      // Clear search
      airportSearchQuery.value = "";
      airportSearchResults.value = [];
      showAirportDropdown.value = false;
    };

    const removeAirport = (airportId) => {
      selectedAirports.value = selectedAirports.value.filter(a => a.id !== airportId);
      formData.value.airports = selectedAirports.value.map(a => a.id);
    };

    // Close dropdown when clicking outside
    const handleClickOutside = (event) => {
      if (!event.target.closest('.position-relative')) {
        showAirportDropdown.value = false;
      }
    };

    const handleSubmit = async () => {
      if (!formData.value.name) {
        Swal.fire("Error", "FBO name is required", "error");
        return;
      }

      try {
        loading.value = true;

        const response = await ApiService.post("/fbos/", formData.value);

        // Close modal using direct method
        const modalElement = document.getElementById('kt_modal_create_fbo');
        if (modalElement) {
          // Try multiple methods to ensure modal closes
          modalElement.classList.remove('show');
          modalElement.style.display = 'none';
          modalElement.setAttribute('aria-hidden', 'true');
          modalElement.removeAttribute('aria-modal');
          
          // Remove backdrop
          const backdrop = document.querySelector('.modal-backdrop');
          if (backdrop) {
            backdrop.remove();
          }
          
          // Remove modal-open class from body
          document.body.classList.remove('modal-open');
          document.body.style.paddingRight = '';
        }
        
        resetForm();
        emit("fbo-created", response.data);

        // Show success message after modal is closed
        setTimeout(async () => {
          await Swal.fire({
            title: "Success!",
            text: "FBO created successfully",
            icon: "success",
            confirmButtonText: "OK"
          });
        }, 100);

      } catch (error: any) {
        console.error("Error creating FBO:", error);
        Swal.fire({
          title: "Error!",
          text: error.response?.data?.detail || "Failed to create FBO",
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

      // Add click outside listener for airport dropdown
      document.addEventListener('click', handleClickOutside);
    });

    onUnmounted(() => {
      // Cleanup event listener
      document.removeEventListener('click', handleClickOutside);

      // Clear search timeout
      if (searchTimeout) {
        clearTimeout(searchTimeout);
      }
    });

    return {
      modalRef,
      formData,
      loading,
      resetForm,
      handleSubmit,
      // Airport search
      airportSearchQuery,
      airportSearchResults,
      airportSearchLoading,
      showAirportDropdown,
      selectedAirports,
      searchAirports,
      addAirport,
      removeAirport,
    };
  },
});
</script>