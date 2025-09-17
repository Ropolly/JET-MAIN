<template>
  <!--begin::Modal - Create user (multi-step)-->
  <div
    class="modal fade"
    id="kt_modal_create_user_wizard"
    ref="modalRef"
    tabindex="-1"
    aria-hidden="true"
  >
    <!--begin::Modal dialog-->
    <div class="modal-dialog modal-xl">
      <!--begin::Modal content-->
      <div class="modal-content">
        <!--begin::Modal header-->
        <div class="modal-header">
          <!--begin::Title-->
          <h2>Create New User - Step {{ currentStep }} of {{ totalSteps }}</h2>
          <!--end::Title-->

          <!--begin::Close-->
          <div
            class="btn btn-sm btn-icon btn-active-color-primary"
            @click="handleClose"
          >
            <KTIcon icon-name="cross" icon-class="fs-1" />
          </div>
          <!--end::Close-->
        </div>
        <!--end::Modal header-->

        <!--begin::Modal body-->
        <div class="modal-body">
          <!--begin::Stepper-->
          <div class="stepper stepper-pills stepper-column d-flex flex-column flex-xl-row flex-row-fluid gap-10" id="kt_create_user_stepper">
            <!--begin::Aside-->
            <div class="card d-flex justify-content-center justify-content-xl-start flex-row-auto w-100 w-xl-300px w-xxl-400px me-9">
              <!--begin::Wrapper-->
              <div class="card-body px-6 px-lg-10 px-xxl-15 py-20">
                <!--begin::Nav-->
                <div class="stepper-nav">
                  <!--begin::Step 1-->
                  <div class="stepper-item" :class="{ current: currentStep === 1, completed: currentStep > 1 }">
                    <!--begin::Wrapper-->
                    <div class="stepper-wrapper">
                      <!--begin::Icon-->
                      <div class="stepper-icon">
                        <i class="stepper-check fas fa-check"></i>
                        <span class="stepper-number">1</span>
                      </div>
                      <!--end::Icon-->

                      <!--begin::Label-->
                      <div class="stepper-label">
                        <h3 class="stepper-title">Basic Information</h3>
                        <div class="stepper-desc fw-semibold">Name, email, and role assignment</div>
                      </div>
                      <!--end::Label-->
                    </div>
                    <!--end::Wrapper-->
                  </div>
                  <!--end::Step 1-->

                  <!--begin::Step 2-->
                  <div class="stepper-item" :class="{ current: currentStep === 2, completed: currentStep > 2 }">
                    <!--begin::Wrapper-->
                    <div class="stepper-wrapper">
                      <!--begin::Icon-->
                      <div class="stepper-icon">
                        <i class="stepper-check fas fa-check"></i>
                        <span class="stepper-number">2</span>
                      </div>
                      <!--end::Icon-->

                      <!--begin::Label-->
                      <div class="stepper-label">
                        <h3 class="stepper-title">Confirmation</h3>
                        <div class="stepper-desc fw-semibold">Review and send activation email</div>
                      </div>
                      <!--end::Label-->
                    </div>
                    <!--end::Wrapper-->
                  </div>
                  <!--end::Step 2-->
                </div>
                <!--end::Nav-->
              </div>
              <!--end::Wrapper-->
            </div>
            <!--begin::Aside-->

            <!--begin::Content-->
            <div class="card d-flex flex-row-fluid flex-center">
              <!--begin::Form-->
              <form class="card-body py-20 w-100 mw-xl-700px px-9" id="kt_create_user_form">
                <!--begin::Step 1-->
                <div v-if="currentStep === 1" class="current">
                  <BasicInfoStep
                    :model-value="userData"
                    @update:model-value="handleUserDataUpdate"
                    :roles="roles"
                    :errors="validationErrors"
                    @step-validated="handleStepValidated"
                  />
                </div>
                <!--end::Step 1-->

                <!--begin::Step 2-->
                <div v-if="currentStep === 2" class="current">
                  <ConfirmationStep
                    :user-data="userData"
                    :roles="roles"
                    :is-submitting="isSubmitting"
                    @step-validated="handleStepValidated"
                  />
                </div>
                <!--end::Step 2-->

                <!--begin::Actions-->
                <div class="d-flex flex-stack pt-15">
                  <!--begin::Wrapper-->
                  <div class="mr-2">
                    <button
                      v-if="currentStep > 1"
                      type="button"
                      class="btn btn-lg btn-light-primary me-3"
                      @click="prevStep"
                      :disabled="isSubmitting"
                    >
                      <KTIcon icon-name="arrow-left" icon-class="fs-4 me-1" />
                      Previous
                    </button>
                  </div>
                  <!--end::Wrapper-->

                  <!--begin::Wrapper-->
                  <div>
                    <button
                      v-if="currentStep < totalSteps"
                      type="button"
                      class="btn btn-lg btn-primary"
                      @click="nextStep"
                      :disabled="!isCurrentStepValid"
                    >
                      Continue
                      <KTIcon icon-name="arrow-right" icon-class="fs-4 ms-1" />
                    </button>

                    <button
                      v-if="currentStep === totalSteps"
                      type="button"
                      class="btn btn-lg btn-primary"
                      @click="handleSubmit"
                      :disabled="isSubmitting || !isCurrentStepValid"
                    >
                      <span v-if="!isSubmitting" class="indicator-label">
                        Create User & Send Email
                        <KTIcon icon-name="arrow-right" icon-class="fs-4 ms-1" />
                      </span>
                      <span v-else class="indicator-progress">
                        Please wait...
                        <span class="spinner-border spinner-border-sm align-middle ms-2"></span>
                      </span>
                    </button>
                  </div>
                  <!--end::Wrapper-->
                </div>
                <!--end::Actions-->
              </form>
              <!--end::Form-->
            </div>
            <!--end::Content-->
          </div>
          <!--end::Stepper-->
        </div>
        <!--end::Modal body-->
      </div>
      <!--end::Modal content-->
    </div>
    <!--end::Modal dialog-->
  </div>
  <!--end::Modal - Create user-->
</template>

<script setup lang="ts">
import { ref, reactive, onMounted, onUnmounted, watch } from "vue";
import { hideModal, showModal } from "@/core/helpers/modal";
import Swal from "sweetalert2";
import ApiService from "@/core/services/ApiService";
import BasicInfoStep from "./CreateUserSteps/BasicInfoStep.vue";
import ConfirmationStep from "./CreateUserSteps/ConfirmationStep.vue";

// Props
interface Props {
  show?: boolean;
}

const props = withDefaults(defineProps<Props>(), {
  show: false
});

// Emits
const emit = defineEmits<{
  close: [];
  'user-created': [user: any];
}>();

interface UserData {
  first_name: string;
  last_name: string;
  email: string;
  role_ids: string[];
  send_activation_email: boolean;
}

interface Role {
  id: string;
  name: string;
  description?: string;
}

const modalRef = ref<HTMLElement | null>(null);
const currentStep = ref(1);
const totalSteps = 2;
const isSubmitting = ref(false);
const validationErrors = ref<Record<string, string>>({});

const stepValidation = ref<Record<number, boolean>>({
  1: false,
  2: true // Step 2 is always valid (just confirmation)
});

// Main user data structure
const userData = reactive<UserData>({
  first_name: '',
  last_name: '',
  email: '',
  role_ids: [],
  send_activation_email: true
});

// Dropdown data
const roles = ref<Role[]>([]);

// Modal visibility watcher
watch(() => props.show, (newVal) => {
  if (newVal) {
    showModal(modalRef.value);
  } else {
    hideModal(modalRef.value);
  }
});

// Handle close modal
const handleClose = () => {
  emit('close');
};

// Step validation
const isCurrentStepValid = ref(false);

const handleStepValidated = (isValid: boolean) => {
  stepValidation.value[currentStep.value] = isValid;
  isCurrentStepValid.value = isValid;
};

// Handle user data updates from BasicInfoStep
const handleUserDataUpdate = (newData: UserData) => {
  console.log('CreateUserWizardModal - received data update:', newData);
  Object.assign(userData, newData);
  console.log('CreateUserWizardModal - updated userData:', userData);
};

// Navigation
const nextStep = () => {
  if (currentStep.value < totalSteps && stepValidation.value[currentStep.value]) {
    currentStep.value++;
    isCurrentStepValid.value = stepValidation.value[currentStep.value];
  }
};

const prevStep = () => {
  if (currentStep.value > 1) {
    currentStep.value--;
    isCurrentStepValid.value = stepValidation.value[currentStep.value];
  }
};

// Load dropdown data
const fetchDropdownData = async () => {
  try {
    // Fetch roles
    const rolesResponse = await ApiService.get('/roles/?page_size=100');
    roles.value = rolesResponse.data.results || rolesResponse.data || [];
    console.log('Loaded roles:', roles.value.length);

  } catch (error) {
    console.error('Error fetching dropdown data:', error);
  }
};

// Submit the user creation request
const handleSubmit = async () => {
  if (!stepValidation.value[1]) {
    Swal.fire({
      title: "Validation Error",
      text: "Please complete all required fields",
      icon: "warning",
      confirmButtonText: "OK"
    });
    return;
  }

  isSubmitting.value = true;
  validationErrors.value = {};

  try {
    console.log('Creating user with data:', userData);
    console.log('Reactive userData object:', JSON.stringify(userData));

    const response = await ApiService.post('/auth/create-user-with-token/', {
      first_name: userData.first_name,
      last_name: userData.last_name,
      email: userData.email,
      role_ids: userData.role_ids,
      send_activation_email: userData.send_activation_email
    });

    console.log('User created successfully:', response.data);

    Swal.fire({
      title: "Success!",
      text: response.data.message || `User has been created and activation email sent to ${userData.email}`,
      icon: "success",
      confirmButtonText: "OK"
    }).then(() => {
      // Emit the profile data if available, otherwise emit the full response
      const profileData = response.data.profile || response.data;
      emit('user-created', profileData);
      emit('close');
      resetForm();
    });

  } catch (error: any) {
    console.error('Error creating user:', error);

    // Handle authentication errors
    if (error.response?.status === 401) {
      Swal.fire({
        title: "Authentication Required",
        text: "You need to be logged in to create users. Please sign in and try again.",
        icon: "warning",
        confirmButtonText: "OK"
      }).then(() => {
        // Redirect to login or emit close event
        emit('close');
      });
      return;
    }

    // Handle validation errors from backend
    if (error.response?.data) {
      const backendErrors = error.response.data;
      if (typeof backendErrors === 'object') {
        // Map backend errors to validation errors
        Object.keys(backendErrors).forEach(key => {
          validationErrors.value[key] = Array.isArray(backendErrors[key])
            ? backendErrors[key][0]
            : backendErrors[key];
        });

        // If there are validation errors, go back to step 1
        if (Object.keys(validationErrors.value).length > 0) {
          currentStep.value = 1;
          isCurrentStepValid.value = false;
          stepValidation.value[1] = false;
        }
      }
    }

    // Show generic error if no specific field errors
    if (Object.keys(validationErrors.value).length === 0) {
      let errorMessage = "Failed to create user. Please try again.";
      if (error.response?.data?.detail) {
        errorMessage = error.response.data.detail;
      } else if (typeof error.response?.data === 'string') {
        errorMessage = error.response.data;
      }

      Swal.fire({
        title: "Error!",
        text: errorMessage,
        icon: "error",
        confirmButtonText: "OK"
      });
    }
  } finally {
    isSubmitting.value = false;
  }
};

const resetForm = () => {
  userData.first_name = '';
  userData.last_name = '';
  userData.email = '';
  userData.role_ids = [];
  userData.send_activation_email = true;

  currentStep.value = 1;
  stepValidation.value = { 1: false, 2: true };
  isCurrentStepValid.value = false;
  validationErrors.value = {};
};

onMounted(() => {
  fetchDropdownData();

  // Add event listener for modal close to reset form
  if (modalRef.value) {
    modalRef.value.addEventListener('hidden.bs.modal', resetForm);
  }
});

onUnmounted(() => {
  // Clean up event listeners
  if (modalRef.value) {
    modalRef.value.removeEventListener('hidden.bs.modal', resetForm);
  }
});
</script>

<style scoped>
.stepper-item.completed .stepper-icon {
  background-color: var(--bs-success);
  color: white;
}

.stepper-item.current .stepper-icon {
  background-color: var(--bs-primary);
  color: white;
}
</style>