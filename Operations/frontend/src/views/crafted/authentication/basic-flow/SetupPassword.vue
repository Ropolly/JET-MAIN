<template>
  <!--begin::Wrapper-->
  <div class="w-lg-500px p-10">
    <!--begin::Form-->
    <VForm
      class="form w-100"
      id="kt_setup_password_form"
      @submit="onSubmitSetupPassword"
      :validation-schema="setupPasswordSchema"
    >
      <!--begin::Heading-->
      <div class="text-center mb-10">
        <!--begin::Title-->
        <h1 class="text-gray-900 mb-3">Set Your Password</h1>
        <!--end::Title-->

        <!--begin::Link-->
        <div class="text-gray-500 fw-semibold fs-4">
          Welcome! Please set your password to continue.
        </div>
        <!--end::Link-->
      </div>
      <!--end::Heading-->

      <!-- Display token validation status -->
      <div v-if="tokenStatus === 'validating'" class="d-flex justify-content-center mb-10">
        <div class="text-center">
          <div class="spinner-border text-primary" role="status">
            <span class="visually-hidden">Loading...</span>
          </div>
          <div class="text-muted mt-3">Validating your token...</div>
        </div>
      </div>

      <div v-else-if="tokenStatus === 'invalid'" class="alert alert-danger mb-10">
        <h4 class="alert-heading">Invalid or Expired Token</h4>
        <p class="mb-0">
          The activation link you used is invalid or has expired. Please contact your administrator
          to request a new activation link.
        </p>
      </div>

      <div v-else-if="tokenStatus === 'valid'">
        <!--begin::User Info-->
        <div v-if="userData" class="d-flex flex-column mb-10">
          <div class="alert alert-info">
            <h5 class="alert-heading">Account Information</h5>
            <p class="mb-1"><strong>Name:</strong> {{ userData.first_name }} {{ userData.last_name }}</p>
            <p class="mb-0"><strong>Email:</strong> {{ userData.email }}</p>
          </div>
        </div>
        <!--end::User Info-->

        <!--begin::Input group - Password-->
        <div class="fv-row mb-10">
          <label class="form-label fs-6 fw-bold text-gray-900">Password</label>
          <div class="position-relative">
            <Field
              :type="showPassword ? 'text' : 'password'"
              class="form-control form-control-lg form-control-solid"
              name="password"
              autocomplete="new-password"
              placeholder="Enter your password"
            />
            <button
              type="button"
              @click="showPassword = !showPassword"
              class="btn btn-sm btn-icon position-absolute translate-middle top-50 end-0 me-n2"
            >
              <i :class="showPassword ? 'fas fa-eye-slash' : 'fas fa-eye'"></i>
            </button>
          </div>
          <div class="fv-plugins-message-container">
            <div class="fv-help-block">
              <ErrorMessage name="password" />
            </div>
          </div>
          <div class="text-muted fs-7">
            Password must be at least 8 characters long.
          </div>
        </div>
        <!--end::Input group-->

        <!--begin::Input group - Confirm Password-->
        <div class="fv-row mb-10">
          <label class="form-label fs-6 fw-bold text-gray-900">Confirm Password</label>
          <div class="position-relative">
            <Field
              :type="showConfirmPassword ? 'text' : 'password'"
              class="form-control form-control-lg form-control-solid"
              name="confirmPassword"
              autocomplete="new-password"
              placeholder="Confirm your password"
            />
            <button
              type="button"
              @click="showConfirmPassword = !showConfirmPassword"
              class="btn btn-sm btn-icon position-absolute translate-middle top-50 end-0 me-n2"
            >
              <i :class="showConfirmPassword ? 'fas fa-eye-slash' : 'fas fa-eye'"></i>
            </button>
          </div>
          <div class="fv-plugins-message-container">
            <div class="fv-help-block">
              <ErrorMessage name="confirmPassword" />
            </div>
          </div>
        </div>
        <!--end::Input group-->


        <!--begin::Actions-->
        <div class="text-center">
          <button
            type="submit"
            ref="submitButton"
            id="kt_setup_password_submit"
            class="btn btn-lg btn-primary w-100 mb-5"
            :disabled="isSubmitting"
          >
            <span v-if="!isSubmitting" class="indicator-label">
              Complete Setup
            </span>
            <span v-else class="indicator-progress">
              Please wait...
              <span class="spinner-border spinner-border-sm align-middle ms-2"></span>
            </span>
          </button>
        </div>
        <!--end::Actions-->
      </div>
    </VForm>
    <!--end::Form-->

  </div>
  <!--end::Wrapper-->
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from "vue";
import { useRoute, useRouter } from "vue-router";
import { ErrorMessage, Field, Form as VForm } from "vee-validate";
import * as Yup from "yup";
import Swal from "sweetalert2";
import ApiService from "@/core/services/ApiService";
import { useAuthStore } from "@/stores/auth";

const route = useRoute();
const router = useRouter();
const authStore = useAuthStore();

const submitButton = ref<HTMLButtonElement | null>(null);

const showPassword = ref(false);
const showConfirmPassword = ref(false);
const isSubmitting = ref(false);
const tokenStatus = ref<'validating' | 'valid' | 'invalid'>('validating');
const userData = ref<any>(null);


// Form validation schema
const setupPasswordSchema = Yup.object().shape({
  password: Yup.string()
    .min(8, "Password must be at least 8 characters")
    .required("Password is required"),
  confirmPassword: Yup.string()
    .oneOf([Yup.ref("password")], "Passwords must match")
    .required("Please confirm your password")
});


// Validate token on component mount
onMounted(async () => {
  const token = route.query.token as string;

  if (!token) {
    tokenStatus.value = 'invalid';
    return;
  }

  try {
    const response = await ApiService.post('/auth/verify-token/', { token });

    if (response.data.valid && response.data.token_type === 'activation') {
      tokenStatus.value = 'valid';
      userData.value = response.data.user_data;
    } else {
      tokenStatus.value = 'invalid';
    }
  } catch (error) {
    console.error('Token validation error:', error);
    tokenStatus.value = 'invalid';
  }
});

// Form submit function
const onSubmitSetupPassword = async (values: any) => {
  if (isSubmitting.value) return;

  const token = route.query.token as string;

  if (!token) {
    Swal.fire({
      title: "Error",
      text: "Invalid activation token",
      icon: "error",
      confirmButtonText: "OK"
    });
    return;
  }

  isSubmitting.value = true;

  try {
    const response = await ApiService.post('/auth/set-password/', {
      token: token,
      password: values.password
    });

    if (response.data.success) {
      Swal.fire({
        title: "Success!",
        text: "Your password has been set successfully. You can now sign in.",
        icon: "success",
        confirmButtonText: "Continue to Sign In"
      }).then(() => {
        router.push({ name: "sign-in" });
      });
    } else {
      throw new Error(response.data.error || "Failed to set password");
    }

  } catch (error: any) {
    console.error('Error setting password:', error);

    let errorMessage = "Failed to set password. Please try again.";
    if (error.response?.data?.error) {
      errorMessage = error.response.data.error;
    } else if (error.message) {
      errorMessage = error.message;
    }

    Swal.fire({
      title: "Error",
      text: errorMessage,
      icon: "error",
      confirmButtonText: "Try Again"
    });
  } finally {
    isSubmitting.value = false;
  }
};
</script>