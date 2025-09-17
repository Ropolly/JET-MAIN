<template>
  <!--begin::Wrapper-->
  <div class="w-lg-500px p-10">
    <!--begin::Form-->
    <VForm
      class="form w-100"
      id="kt_login_signin_form"
      @submit="onSubmitLogin"
      :validation-schema="currentSchema"
    >
      <!--begin::Heading-->
      <div class="text-center mb-10">
        <!--begin::Title-->
        <h1 class="text-gray-900 mb-3">
          {{ showMfaStep ? 'Enter Verification Code' : 'Sign In' }}
        </h1>
        <!--end::Title-->

        <!-- MFA Step Description -->
        <div v-if="showMfaStep" class="text-muted mb-3">
          <p class="mb-2">We've sent a verification code to</p>
          <strong>{{ maskedPhoneNumber }}</strong>
        </div>
      </div>
      <!--begin::Heading-->

      <!-- Step 1: Username & Password -->
      <div v-if="!showMfaStep">
        <!--begin::Username Input group-->
        <div class="fv-row mb-10">
          <!--begin::Label-->
          <label class="form-label fs-6 fw-bold text-gray-900">Username</label>
          <!--end::Label-->

          <!--begin::Input-->
          <Field
            tabindex="1"
            class="form-control form-control-lg form-control-solid"
            type="text"
            name="username"
            autocomplete="off"
            ref="usernameField"
          />
          <!--end::Input-->
          <div class="fv-plugins-message-container">
            <div class="fv-help-block">
              <ErrorMessage name="username" />
            </div>
          </div>
        </div>
        <!--end::Username Input group-->

        <!--begin::Password Input group-->
        <div class="fv-row mb-10">
          <!--begin::Wrapper-->
          <div class="d-flex flex-stack mb-2">
            <!--begin::Label-->
            <label class="form-label fw-bold text-gray-900 fs-6 mb-0">Password</label>
            <!--end::Label-->

            <!--begin::Link-->
            <router-link to="/password-reset" class="link-primary fs-6 fw-bold">
              Forgot Password ?
            </router-link>
            <!--end::Link-->
          </div>
          <!--end::Wrapper-->

          <!--begin::Input-->
          <Field
            tabindex="2"
            class="form-control form-control-lg form-control-solid"
            type="password"
            name="password"
            autocomplete="off"
          />
          <!--end::Input-->
          <div class="fv-plugins-message-container">
            <div class="fv-help-block">
              <ErrorMessage name="password" />
            </div>
          </div>
        </div>
        <!--end::Password Input group-->
      </div>

      <!-- Step 2: MFA Code -->
      <div v-else>
        <!--begin::MFA Code Input group-->
        <div class="fv-row mb-10">
          <!--begin::Label-->
          <label class="form-label fs-6 fw-bold text-gray-900">Verification Code</label>
          <!--end::Label-->

          <!--begin::Input-->
          <Field
            tabindex="1"
            class="form-control form-control-lg form-control-solid text-center fs-2"
            type="text"
            name="sms_code"
            autocomplete="one-time-code"
            placeholder="000000"
            maxlength="6"
            ref="mfaCodeField"
            style="font-family: monospace; letter-spacing: 0.5rem;"
          />
          <!--end::Input-->
          <div class="fv-plugins-message-container">
            <div class="fv-help-block">
              <ErrorMessage name="sms_code" />
            </div>
          </div>
        </div>
        <!--end::MFA Code Input group-->

        <!-- Resend Code Section -->
        <div class="text-center mb-6">
          <div v-if="resendCountdown > 0" class="text-muted">
            <i class="fas fa-clock me-2"></i>
            Resend code in {{ resendCountdown }}s
          </div>
          <div v-else>
            <button
              type="button"
              class="btn btn-link text-primary p-0"
              @click="resendMfaCode"
              :disabled="isResending"
            >
              <i class="fas fa-redo me-2" :class="{ 'fa-spin': isResending }"></i>
              {{ isResending ? 'Sending...' : 'Send Another Code' }}
            </button>
          </div>
        </div>

        <!-- Back to Login -->
        <div class="text-center mb-6">
          <button
            type="button"
            class="btn btn-link text-muted p-0"
            @click="backToLogin"
          >
            <i class="fas fa-arrow-left me-2"></i>
            Back to login
          </button>
        </div>
      </div>

      <!--begin::Actions-->
      <div class="text-center">
        <!--begin::Submit button-->
        <button
          :tabindex="showMfaStep ? 2 : 3"
          type="submit"
          ref="submitButton"
          id="kt_sign_in_submit"
          class="btn btn-lg btn-primary w-100 mb-5"
        >
          <span class="indicator-label">
            {{ showMfaStep ? 'Verify Code' : 'Continue' }}
          </span>

          <span class="indicator-progress">
            Please wait...
            <span
              class="spinner-border spinner-border-sm align-middle ms-2"
            ></span>
          </span>
        </button>
        <!--end::Submit button-->
      </div>
      <!--end::Actions-->
    </VForm>
    <!--end::Form-->
  </div>
  <!--end::Wrapper-->
</template>

<script lang="ts">
import { getAssetPath } from "@/core/helpers/assets";
import { defineComponent, ref, computed, nextTick, onUnmounted } from "vue";
import { ErrorMessage, Field, Form as VForm } from "vee-validate";
import { useAuthStore, type LoginCredentials } from "@/stores/auth";
import { useRouter } from "vue-router";
import Swal from "sweetalert2/dist/sweetalert2.js";
import * as Yup from "yup";

export default defineComponent({
  name: "sign-in",
  components: {
    Field,
    VForm,
    ErrorMessage,
  },
  setup() {
    const store = useAuthStore();
    const router = useRouter();

    const submitButton = ref<HTMLButtonElement | null>(null);
    const usernameField = ref<HTMLInputElement | null>(null);
    const mfaCodeField = ref<HTMLInputElement | null>(null);

    // MFA state
    const showMfaStep = ref(false);
    const mfaPhoneNumber = ref("");
    const savedCredentials = ref<LoginCredentials | null>(null);
    const resendCountdown = ref(0);
    const isResending = ref(false);
    let countdownInterval: NodeJS.Timeout | null = null;

    // Computed properties
    const maskedPhoneNumber = computed(() => {
      if (!mfaPhoneNumber.value) return "";

      // Format for display - mask middle digits
      const cleaned = mfaPhoneNumber.value.replace(/\D/g, "");
      if (cleaned.length === 11 && cleaned.startsWith("1")) {
        const areaCode = cleaned.slice(1, 4);
        const last = cleaned.slice(7, 11);
        return `+1 (${areaCode}) ***-${last}`;
      } else if (cleaned.length === 10) {
        const areaCode = cleaned.slice(0, 3);
        const last = cleaned.slice(6, 10);
        return `(${areaCode}) ***-${last}`;
      }
      return mfaPhoneNumber.value;
    });

    // Form validation schemas
    const loginSchema = Yup.object().shape({
      username: Yup.string().required().label("Username"),
      password: Yup.string().min(4).required().label("Password"),
    });

    const mfaSchema = Yup.object().shape({
      sms_code: Yup.string()
        .required()
        .matches(/^\d{6}$/, "Verification code must be 6 digits")
        .label("Verification Code"),
    });

    const currentSchema = computed(() => {
      return showMfaStep.value ? mfaSchema : loginSchema;
    });

    // Start countdown timer
    function startCountdown() {
      resendCountdown.value = 30;
      countdownInterval = setInterval(() => {
        resendCountdown.value--;
        if (resendCountdown.value <= 0) {
          stopCountdown();
        }
      }, 1000);
    }

    function stopCountdown() {
      if (countdownInterval) {
        clearInterval(countdownInterval);
        countdownInterval = null;
      }
      resendCountdown.value = 0;
    }

    // Form submit function
    const onSubmitLogin = async (values: any) => {
      if (submitButton.value) {
        submitButton.value.disabled = true;
        submitButton.value.setAttribute("data-kt-indicator", "on");
      }

      try {
        if (!showMfaStep.value) {
          // Step 1: Username and Password
          const credentials = values as LoginCredentials;
          const result = await store.login(credentials);

          if (result.mfa_required) {
            // MFA is required, show SMS step
            savedCredentials.value = credentials;
            mfaPhoneNumber.value = result.phone_number || "";
            showMfaStep.value = true;
            startCountdown();

            // Focus MFA code field
            nextTick(() => {
              mfaCodeField.value?.focus();
            });

            Swal.fire({
              text: result.message || "Verification code sent to your phone",
              icon: "info",
              buttonsStyling: false,
              confirmButtonText: "Ok",
              heightAuto: false,
              timer: 2000,
              customClass: {
                confirmButton: "btn fw-semibold btn-light-primary",
              },
            });
          } else {
            // Login successful without MFA
            await handleSuccessfulLogin();
          }
        } else {
          // Step 2: MFA Verification
          if (!savedCredentials.value) {
            throw new Error("Login session expired. Please try again.");
          }

          const mfaCredentials = {
            ...savedCredentials.value,
            sms_code: values.sms_code,
          };

          await store.login(mfaCredentials);
          await handleSuccessfulLogin();
        }
      } catch (error: any) {
        const errorMessage = store.errors.general ||
                           error.message ||
                           "Login failed. Please try again.";

        Swal.fire({
          text: errorMessage,
          icon: "error",
          buttonsStyling: false,
          confirmButtonText: "Try again!",
          heightAuto: false,
          customClass: {
            confirmButton: "btn fw-semibold btn-light-danger",
          },
        });
      } finally {
        if (submitButton.value) {
          submitButton.value.removeAttribute("data-kt-indicator");
          submitButton.value.disabled = false;
        }
      }
    };

    async function handleSuccessfulLogin() {
      stopCountdown();

      Swal.fire({
        text: "You have successfully logged in!",
        icon: "success",
        buttonsStyling: false,
        confirmButtonText: "Ok, got it!",
        heightAuto: false,
        customClass: {
          confirmButton: "btn fw-semibold btn-light-primary",
        },
      }).then(() => {
        router.push({ name: "dashboard" });
      });
    }

    async function resendMfaCode() {
      if (!savedCredentials.value || isResending.value) return;

      isResending.value = true;

      try {
        const result = await store.login(savedCredentials.value);

        if (result.mfa_required) {
          startCountdown();
          Swal.fire({
            text: "Verification code sent!",
            icon: "success",
            buttonsStyling: false,
            timer: 2000,
            showConfirmButton: false,
            heightAuto: false,
          });
        }
      } catch (error) {
        Swal.fire({
          text: "Failed to resend code. Please try again.",
          icon: "error",
          buttonsStyling: false,
          confirmButtonText: "Ok",
          heightAuto: false,
          customClass: {
            confirmButton: "btn fw-semibold btn-light-danger",
          },
        });
      } finally {
        isResending.value = false;
      }
    }

    function backToLogin() {
      showMfaStep.value = false;
      savedCredentials.value = null;
      mfaPhoneNumber.value = "";
      stopCountdown();

      // Clear any errors
      store.setError({});

      // Focus username field
      nextTick(() => {
        usernameField.value?.focus();
      });
    }

    // Cleanup on unmount
    onUnmounted(() => {
      stopCountdown();
    });

    return {
      onSubmitLogin,
      currentSchema,
      submitButton,
      usernameField,
      mfaCodeField,
      getAssetPath,
      // MFA state
      showMfaStep,
      maskedPhoneNumber,
      resendCountdown,
      isResending,
      resendMfaCode,
      backToLogin,
    };
  },
});
</script>