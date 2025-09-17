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

        <!--begin::Input group - Phone Number-->
        <div class="fv-row mb-10">
          <PhoneNumberInput
            v-model="phoneNumber"
            label="Phone Number"
            :required="true"
            :auto-format="true"
            :validate-on-input="true"
            placeholder="(555) 123-4567"
            help-text="Please provide your phone number for account security."
            @validation-change="handlePhoneValidation"
            ref="phoneInputRef"
          />


          <!-- Hidden field for form validation -->
          <Field
            type="hidden"
            name="phone"
            :value="phoneNumber"
          />
          <div class="fv-plugins-message-container">
            <div class="fv-help-block">
              <ErrorMessage name="phone" />
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

    <!-- SMS Verification Modal -->
    <SMSVerificationModal
      ref="smsModalRef"
      title="Verify Phone Number"
      phone-input-message="We'll send a verification code to confirm your phone number"
      :initial-phone-number="phoneNumber"
      :allow-phone-edit="false"
      @phone-verified="handlePhoneVerified"
    />
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
import PhoneNumberInput from "@/components/forms/PhoneNumberInput.vue";
import SMSVerificationModal from "@/components/modals/SMSVerificationModal.vue";
import { useAuthStore } from "@/stores/auth";

const route = useRoute();
const router = useRouter();
const authStore = useAuthStore();

const submitButton = ref<HTMLButtonElement | null>(null);
const phoneInputRef = ref<InstanceType<typeof PhoneNumberInput> | null>(null);
const smsModalRef = ref<InstanceType<typeof SMSVerificationModal> | null>(null);

const showPassword = ref(false);
const showConfirmPassword = ref(false);
const isSubmitting = ref(false);
const tokenStatus = ref<'validating' | 'valid' | 'invalid'>('validating');
const userData = ref<any>(null);
const formValues = ref<any>({}); // Store form values for SMS verification completion

// Phone verification state
const phoneNumber = ref(""); // Raw digits from v-model
const validatedPhoneNumber = ref(""); // E.164 format from validation
const isPhoneValid = ref(false);
const isPhoneVerified = ref(false);
const isSendingCode = ref(false);

// Computed properties
const maskedPhone = computed(() => {
  if (!validatedPhoneNumber.value) return "";

  const cleaned = validatedPhoneNumber.value.replace(/\D/g, "");
  if (cleaned.length === 11 && cleaned.startsWith("1")) {
    const areaCode = cleaned.slice(1, 4);
    const last = cleaned.slice(7, 11);
    return `+1 (${areaCode}) ***-${last}`;
  } else if (cleaned.length === 10) {
    const areaCode = cleaned.slice(0, 3);
    const last = cleaned.slice(6, 10);
    return `(${areaCode}) ***-${last}`;
  }
  return validatedPhoneNumber.value;
});

// Form validation schema
const setupPasswordSchema = Yup.object().shape({
  password: Yup.string()
    .min(8, "Password must be at least 8 characters")
    .required("Password is required"),
  confirmPassword: Yup.string()
    .oneOf([Yup.ref("password")], "Passwords must match")
    .required("Please confirm your password"),
  phone: Yup.string()
    .required("Phone number is required")
});

// Phone verification methods
function handlePhoneValidation(isValid: boolean, formattedNumber: string) {
  console.log('Phone validation:', { isValid, formattedNumber, rawPhone: phoneNumber.value });
  isPhoneValid.value = isValid;
  if (isValid && formattedNumber) {
    validatedPhoneNumber.value = formattedNumber; // Store the E.164 format
  }

  // Reset verification status if phone changes
  if (isPhoneVerified.value && validatedPhoneNumber.value !== formattedNumber) {
    isPhoneVerified.value = false;
  }
}


async function handlePhoneVerified(data: { phoneNumber: string, verificationCode: string }) {
  isPhoneVerified.value = true;
  validatedPhoneNumber.value = data.phoneNumber;

  // Now complete the password setup process
  const token = route.query.token as string;

  try {
    const response = await ApiService.post('/auth/set-password/', {
      token: token,
      password: formValues.value.password,
      phone: validatedPhoneNumber.value
    });

    // Show success message
    await Swal.fire({
      title: "Welcome!",
      text: "Your account has been activated successfully with phone verification. You can now sign in.",
      icon: "success",
      confirmButtonText: "Continue to Sign In"
    });

    // Redirect to sign-in page
    router.push('/sign-in');

  } catch (error: any) {
    console.error('Setup password error:', error);

    let errorMessage = "Failed to set up your password. Please try again.";

    if (error.response?.data) {
      if (typeof error.response.data === 'string') {
        errorMessage = error.response.data;
      } else if (error.response.data.detail) {
        errorMessage = error.response.data.detail;
      } else if (error.response.data.error) {
        errorMessage = error.response.data.error;
      }
    }

    Swal.fire({
      title: "Error",
      text: errorMessage,
      icon: "error",
      confirmButtonText: "Try Again"
    });
  }
}

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

  // Validate phone number is provided and valid
  if (!isPhoneValid.value || !validatedPhoneNumber.value) {
    Swal.fire({
      title: "Invalid Phone Number",
      text: "Please enter a valid phone number.",
      icon: "warning",
      confirmButtonText: "OK"
    });
    return;
  }

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
    // Store form values for completion after SMS verification
    formValues.value = values;

    // Step 1: Send SMS verification code
    console.log('Sending SMS to:', validatedPhoneNumber.value);
    const smsResult = await authStore.sendSmsCode(validatedPhoneNumber.value);

    if (!smsResult.success) {
      throw new Error(smsResult.error || "Failed to send verification code");
    }

    // Step 2: Show SMS verification modal
    if (smsModalRef.value) {
      smsModalRef.value.show();
    }

    Swal.fire({
      text: "Verification code sent to your phone!",
      icon: "info",
      buttonsStyling: false,
      timer: 2000,
      showConfirmButton: false,
      heightAuto: false,
    });

  } catch (error: any) {
    console.error('Error sending SMS code:', error);

    let errorMessage = "Failed to send verification code. Please try again.";
    if (error.message) {
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