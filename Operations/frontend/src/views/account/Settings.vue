<template>
  <!--begin::Account Settings-->
  <div class="card mb-5 mb-xl-10">
    <!--begin::Card header-->
    <div class="card-header border-0 cursor-pointer">
      <!--begin::Card title-->
      <div class="card-title m-0">
        <h3 class="fw-bold m-0">Account Settings</h3>
      </div>
      <!--end::Card title-->
    </div>
    <!--begin::Card header-->

    <!--begin::Content-->
    <div class="collapse show">
      <!--begin::Form-->
      <VForm
        id="kt_account_profile_details_form"
        class="form"
        novalidate
        @submit="saveChanges"
        :validation-schema="profileDetailsValidator"
      >
        <!--begin::Card body-->
        <div class="card-body border-top p-9">
          <!--begin::Input group-->
          <div class="row mb-6">
            <!--begin::Label-->
            <label class="col-lg-4 col-form-label required fw-semibold fs-6">
              Username
            </label>
            <!--end::Label-->

            <!--begin::Col-->
            <div class="col-lg-8">
              <!--begin::Row-->
              <div class="row">
                <!--begin::Col-->
                <div class="col-lg-6 fv-row">
                  <Field
                    name="username"
                    type="text"
                    class="form-control form-control-lg form-control-solid mb-3 mb-lg-0"
                    placeholder="Username"
                    v-model="formData.username"
                    readonly
                  />
                  <div class="text-muted fs-7">Username cannot be changed</div>
                  <ErrorMessage name="username" class="fv-plugins-message-container invalid-feedback" />
                </div>
                <!--end::Col-->
              </div>
              <!--end::Row-->
            </div>
            <!--end::Col-->
          </div>
          <!--end::Input group-->

          <!--begin::Input group-->
          <div class="row mb-6">
            <!--begin::Label-->
            <label class="col-lg-4 col-form-label required fw-semibold fs-6">
              Full Name
            </label>
            <!--end::Label-->

            <!--begin::Col-->
            <div class="col-lg-8">
              <!--begin::Row-->
              <div class="row">
                <!--begin::Col-->
                <div class="col-lg-6 fv-row">
                  <Field
                    name="first_name"
                    type="text"
                    class="form-control form-control-lg form-control-solid mb-3 mb-lg-0"
                    placeholder="First name"
                    v-model="formData.first_name"
                  />
                  <ErrorMessage name="first_name" class="fv-plugins-message-container invalid-feedback" />
                </div>
                <!--end::Col-->

                <!--begin::Col-->
                <div class="col-lg-6 fv-row">
                  <Field
                    name="last_name"
                    type="text"
                    class="form-control form-control-lg form-control-solid"
                    placeholder="Last name"
                    v-model="formData.last_name"
                  />
                  <ErrorMessage name="last_name" class="fv-plugins-message-container invalid-feedback" />
                </div>
                <!--end::Col-->
              </div>
              <!--end::Row-->
            </div>
            <!--end::Col-->
          </div>
          <!--end::Input group-->

          <!--begin::Input group-->
          <div class="row mb-6">
            <!--begin::Label-->
            <label class="col-lg-4 col-form-label required fw-semibold fs-6">
              Email
            </label>
            <!--end::Label-->

            <!--begin::Col-->
            <div class="col-lg-8 fv-row">
              <Field
                name="email"
                type="email"
                class="form-control form-control-lg form-control-solid"
                placeholder="Email"
                v-model="formData.email"
              />
              <ErrorMessage name="email" class="fv-plugins-message-container invalid-feedback" />
            </div>
            <!--end::Col-->
          </div>
          <!--end::Input group-->

          <!--begin::Input group-->
          <div class="row mb-6">
            <!--begin::Label-->
            <label class="col-lg-4 col-form-label fw-semibold fs-6">
              <span>Phone</span>
            </label>
            <!--end::Label-->

            <!--begin::Col-->
            <div class="col-lg-8 fv-row">
              <Field
                name="phone"
                type="text"
                class="form-control form-control-lg form-control-solid"
                placeholder="Phone number"
                v-model="formData.phone"
              />
              <ErrorMessage name="phone" class="fv-plugins-message-container invalid-feedback" />
            </div>
            <!--end::Col-->
          </div>
          <!--end::Input group-->

          <!--begin::Input group-->
          <div class="row mb-6">
            <!--begin::Label-->
            <label class="col-lg-4 col-form-label fw-semibold fs-6">Address</label>
            <!--end::Label-->

            <!--begin::Col-->
            <div class="col-lg-8 fv-row">
              <Field
                name="address_line1"
                type="text"
                class="form-control form-control-lg form-control-solid mb-3"
                placeholder="Address Line 1"
                v-model="formData.address_line1"
              />
              <ErrorMessage name="address_line1" class="fv-plugins-message-container invalid-feedback" />
              
              <Field
                name="address_line2"
                type="text"
                class="form-control form-control-lg form-control-solid"
                placeholder="Address Line 2 (Optional)"
                v-model="formData.address_line2"
              />
              <ErrorMessage name="address_line2" class="fv-plugins-message-container invalid-feedback" />
            </div>
            <!--end::Col-->
          </div>
          <!--end::Input group-->

          <!--begin::Input group-->
          <div class="row mb-6">
            <!--begin::Label-->
            <label class="col-lg-4 col-form-label fw-semibold fs-6">Location</label>
            <!--end::Label-->

            <!--begin::Col-->
            <div class="col-lg-8">
              <!--begin::Row-->
              <div class="row">
                <!--begin::Col-->
                <div class="col-lg-6 fv-row">
                  <Field
                    name="city"
                    type="text"
                    class="form-control form-control-lg form-control-solid mb-3 mb-lg-0"
                    placeholder="City"
                    v-model="formData.city"
                  />
                  <ErrorMessage name="city" class="fv-plugins-message-container invalid-feedback" />
                </div>
                <!--end::Col-->

                <!--begin::Col-->
                <div class="col-lg-6 fv-row">
                  <Field
                    name="state"
                    type="text"
                    class="form-control form-control-lg form-control-solid"
                    placeholder="State"
                    v-model="formData.state"
                  />
                  <ErrorMessage name="state" class="fv-plugins-message-container invalid-feedback" />
                </div>
                <!--end::Col-->
              </div>
              <!--end::Row-->
            </div>
            <!--end::Col-->
          </div>
          <!--end::Input group-->

          <!--begin::Input group-->
          <div class="row mb-6">
            <!--begin::Label-->
            <label class="col-lg-4 col-form-label fw-semibold fs-6"></label>
            <!--end::Label-->

            <!--begin::Col-->
            <div class="col-lg-8">
              <!--begin::Row-->
              <div class="row">
                <!--begin::Col-->
                <div class="col-lg-6 fv-row">
                  <Field
                    name="country"
                    type="text"
                    class="form-control form-control-lg form-control-solid mb-3 mb-lg-0"
                    placeholder="Country"
                    v-model="formData.country"
                  />
                  <ErrorMessage name="country" class="fv-plugins-message-container invalid-feedback" />
                </div>
                <!--end::Col-->

                <!--begin::Col-->
                <div class="col-lg-6 fv-row">
                  <Field
                    name="zip"
                    type="text"
                    class="form-control form-control-lg form-control-solid"
                    placeholder="Postal Code"
                    v-model="formData.zip"
                  />
                  <ErrorMessage name="zip" class="fv-plugins-message-container invalid-feedback" />
                </div>
                <!--end::Col-->
              </div>
              <!--end::Row-->
            </div>
            <!--end::Col-->
          </div>
          <!--end::Input group-->
        </div>
        <!--end::Card body-->

        <!--begin::Actions-->
        <div class="card-footer d-flex justify-content-end py-6 px-9">
          <button type="reset" class="btn btn-light btn-active-light-primary me-2" @click="discardChanges">
            Discard
          </button>
          <button
            type="submit"
            class="btn btn-primary"
            :class="{ 'please-wait': loading }"
            :disabled="loading"
          >
            <span v-if="!loading" class="indicator-label">Save Changes</span>
            <span v-if="loading" class="indicator-progress">
              Please wait...
              <span class="spinner-border spinner-border-sm align-middle ms-2"></span>
            </span>
          </button>
        </div>
        <!--end::Actions-->
      </VForm>
      <!--end::Form-->
    </div>
    <!--end::Content-->
  </div>
  <!--end::Account Settings-->
</template>

<script lang="ts">
import { defineComponent, ref, onMounted, watch } from "vue";
import { ErrorMessage, Field, Form as VForm } from "vee-validate";
import * as Yup from "yup";
import { useAuthStore } from "@/stores/auth";
import Swal from "sweetalert2";

export default defineComponent({
  name: "account-settings",
  components: {
    Field,
    VForm,
    ErrorMessage,
  },
  setup() {
    const authStore = useAuthStore();
    const loading = ref(false);
    const formData = ref({
      username: '',
      first_name: '',
      last_name: '',
      email: '',
      phone: '',
      address_line1: '',
      address_line2: '',
      city: '',
      state: '',
      country: '',
      zip: '',
    });

    // Form validation schema
    const profileDetailsValidator = Yup.object().shape({
      first_name: Yup.string().required("First name is required"),
      last_name: Yup.string().required("Last name is required"),
      email: Yup.string()
        .email("Please enter a valid email address")
        .required("Email is required"),
      phone: Yup.string(),
      address_line1: Yup.string(),
      address_line2: Yup.string(),
      city: Yup.string(),
      state: Yup.string(),
      country: Yup.string(),
      zip: Yup.string(),
    });

    // Load user data
    const loadUserData = async () => {
      try {
        await authStore.getUserProfile();
        if (authStore.user) {
          formData.value = {
            username: authStore.user.username || '',
            first_name: authStore.user.first_name || '',
            last_name: authStore.user.last_name || '',
            email: authStore.user.email || '',
            phone: authStore.user.phone || '',
            address_line1: authStore.user.address_line1 || '',
            address_line2: authStore.user.address_line2 || '',
            city: authStore.user.city || '',
            state: authStore.user.state || '',
            country: authStore.user.country || '',
            zip: authStore.user.zip || '',
          };
        }
      } catch (error) {
        console.error("Failed to load user profile:", error);
        Swal.fire({
          title: "Error!",
          text: "Failed to load user profile",
          icon: "error",
          confirmButtonText: "OK"
        });
      }
    };

    // Save changes
    const saveChanges = async () => {
      if (!authStore.user) {
        Swal.fire({
          title: "Error!",
          text: "User not loaded",
          icon: "error",
          confirmButtonText: "OK"
        });
        return;
      }

      loading.value = true;
      try {
        await authStore.updateProfile({
          first_name: formData.value.first_name,
          last_name: formData.value.last_name,
          email: formData.value.email,
          phone: formData.value.phone,
          address_line1: formData.value.address_line1,
          address_line2: formData.value.address_line2,
          city: formData.value.city,
          state: formData.value.state,
          country: formData.value.country,
          zip: formData.value.zip,
        });

        Swal.fire({
          title: "Success!",
          text: "Profile updated successfully",
          icon: "success",
          confirmButtonText: "OK"
        });
      } catch (error) {
        console.error("Failed to update profile:", error);
        Swal.fire({
          title: "Error!",
          text: "Failed to update profile",
          icon: "error",
          confirmButtonText: "OK"
        });
      } finally {
        loading.value = false;
      }
    };

    // Discard changes
    const discardChanges = () => {
      loadUserData();
    };

    // Load data on mount
    onMounted(() => {
      loadUserData();
    });

    return {
      formData,
      loading,
      profileDetailsValidator,
      saveChanges,
      discardChanges,
    };
  },
});
</script>