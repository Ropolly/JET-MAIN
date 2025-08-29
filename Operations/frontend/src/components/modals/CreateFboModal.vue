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
import { defineComponent, ref, onMounted } from "vue";
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
    });

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
      };
      loading.value = false;
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