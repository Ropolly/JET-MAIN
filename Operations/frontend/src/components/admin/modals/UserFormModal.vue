<template>
  <div
    class="modal fade"
    :class="{ show: show }"
    :style="{ display: show ? 'block' : 'none' }"
    tabindex="-1"
    @click.self="$emit('close')"
  >
    <div class="modal-dialog modal-dialog-centered mw-650px">
      <div class="modal-content">
        <div class="modal-header">
          <h2 class="fw-bolder">{{ isEdit ? 'Edit' : 'Add' }} User</h2>
          <div
            class="btn btn-icon btn-sm btn-active-icon-primary"
            @click="$emit('close')"
          >
            <i class="ki-duotone ki-cross fs-1">
              <span class="path1"></span>
              <span class="path2"></span>
            </i>
          </div>
        </div>

        <div class="modal-body scroll-y mx-5 mx-xl-15 my-7">
          <VForm
            @submit="handleSubmit"
            :validation-schema="validationSchema"
            v-slot="{ errors }"
          >
            <!--begin::Scroll-->
            <div class="d-flex flex-column scroll-y me-n7 pe-7">
              <!--begin::Input group-->
              <div class="fv-row mb-7">
                <label class="required fw-semibold fs-6 mb-2">Username</label>
                <Field
                  name="username"
                  type="text"
                  class="form-control form-control-solid mb-3 mb-lg-0"
                  placeholder="Enter username"
                  :class="{ 'is-invalid': errors.username }"
                  v-model="formData.username"
                />
                <div class="invalid-feedback">{{ errors.username }}</div>
              </div>
              <!--end::Input group-->

              <!--begin::Input group-->
              <div class="row">
                <div class="col-md-6 fv-row mb-7">
                  <label class="required fw-semibold fs-6 mb-2">First Name</label>
                  <Field
                    name="first_name"
                    type="text"
                    class="form-control form-control-solid mb-3 mb-lg-0"
                    placeholder="First name"
                    :class="{ 'is-invalid': errors.first_name }"
                    v-model="formData.first_name"
                  />
                  <div class="invalid-feedback">{{ errors.first_name }}</div>
                </div>
                <div class="col-md-6 fv-row mb-7">
                  <label class="required fw-semibold fs-6 mb-2">Last Name</label>
                  <Field
                    name="last_name"
                    type="text"
                    class="form-control form-control-solid mb-3 mb-lg-0"
                    placeholder="Last name"
                    :class="{ 'is-invalid': errors.last_name }"
                    v-model="formData.last_name"
                  />
                  <div class="invalid-feedback">{{ errors.last_name }}</div>
                </div>
              </div>
              <!--end::Input group-->

              <!--begin::Input group-->
              <div class="fv-row mb-7">
                <label class="required fw-semibold fs-6 mb-2">Email</label>
                <Field
                  name="email"
                  type="email"
                  class="form-control form-control-solid mb-3 mb-lg-0"
                  placeholder="example@domain.com"
                  :class="{ 'is-invalid': errors.email }"
                  v-model="formData.email"
                />
                <div class="invalid-feedback">{{ errors.email }}</div>
              </div>
              <!--end::Input group-->

              <!--begin::Input group-->
              <div class="fv-row mb-7">
                <label class="fw-semibold fs-6 mb-2">Phone</label>
                <Field
                  name="phone"
                  type="text"
                  class="form-control form-control-solid mb-3 mb-lg-0"
                  placeholder="+1 (555) 000-0000"
                  v-model="formData.phone"
                />
              </div>
              <!--end::Input group-->

              <!--begin::Input group-->
              <div class="fv-row mb-7" v-if="!isEdit">
                <label class="required fw-semibold fs-6 mb-2">Password</label>
                <Field
                  name="password"
                  type="password"
                  class="form-control form-control-solid mb-3 mb-lg-0"
                  placeholder="Enter password"
                  :class="{ 'is-invalid': errors.password }"
                  v-model="formData.password"
                />
                <div class="invalid-feedback">{{ errors.password }}</div>
              </div>
              <!--end::Input group-->

              <!--begin::Input group-->
              <div class="fv-row mb-7">
                <label class="fw-semibold fs-6 mb-2">Address</label>
                <Field
                  name="address_line1"
                  type="text"
                  class="form-control form-control-solid mb-3"
                  placeholder="Address Line 1"
                  v-model="formData.address_line1"
                />
                <Field
                  name="address_line2"
                  type="text"
                  class="form-control form-control-solid mb-3"
                  placeholder="Address Line 2 (Optional)"
                  v-model="formData.address_line2"
                />
                <div class="row">
                  <div class="col-md-6">
                    <Field
                      name="city"
                      type="text"
                      class="form-control form-control-solid mb-3 mb-md-0"
                      placeholder="City"
                      v-model="formData.city"
                    />
                  </div>
                  <div class="col-md-3">
                    <Field
                      name="state"
                      type="text"
                      class="form-control form-control-solid mb-3 mb-md-0"
                      placeholder="State"
                      v-model="formData.state"
                    />
                  </div>
                  <div class="col-md-3">
                    <Field
                      name="zip"
                      type="text"
                      class="form-control form-control-solid"
                      placeholder="ZIP"
                      v-model="formData.zip"
                    />
                  </div>
                </div>
              </div>
              <!--end::Input group-->

              <!--begin::Input group-->
              <div class="fv-row mb-7">
                <label class="fw-semibold fs-6 mb-2">Status</label>
                <Field
                  as="select"
                  name="status"
                  class="form-select form-select-solid"
                  v-model="formData.status"
                >
                  <option value="active">Active</option>
                  <option value="inactive">Inactive</option>
                </Field>
              </div>
              <!--end::Input group-->

              <!--begin::Input group-->
              <div class="fv-row mb-7">
                <label class="fw-semibold fs-6 mb-2">Departments</label>
                <select
                  multiple
                  class="form-select form-select-solid"
                  v-model="formData.departments"
                >
                  <option
                    v-for="dept in availableDepartments"
                    :key="dept.id"
                    :value="dept.id"
                  >
                    {{ dept.name }}
                  </option>
                </select>
                <div class="form-text">Hold Ctrl/Cmd to select multiple departments</div>
              </div>
              <!--end::Input group-->

              <!--begin::Input group-->
              <div class="fv-row mb-7">
                <label class="fw-semibold fs-6 mb-2">Roles</label>
                <select
                  multiple
                  class="form-select form-select-solid"
                  v-model="formData.roles"
                >
                  <option
                    v-for="role in availableRoles"
                    :key="role.id"
                    :value="role.id"
                  >
                    {{ role.name }}
                  </option>
                </select>
                <div class="form-text">Hold Ctrl/Cmd to select multiple roles</div>
              </div>
              <!--end::Input group-->
            </div>
            <!--end::Scroll-->

            <!--begin::Actions-->
            <div class="text-center pt-15">
              <button
                type="button"
                class="btn btn-light me-3"
                @click="$emit('close')"
              >
                Discard
              </button>
              <button
                type="submit"
                class="btn btn-primary"
                :disabled="loading"
              >
                <span v-if="!loading" class="indicator-label">
                  {{ isEdit ? 'Update' : 'Create' }} User
                </span>
                <span v-else class="indicator-progress">
                  Please wait...
                  <span
                    class="spinner-border spinner-border-sm align-middle ms-2"
                  ></span>
                </span>
              </button>
            </div>
            <!--end::Actions-->
          </VForm>
        </div>
      </div>
    </div>
  </div>
  <div
    v-if="show"
    class="modal-backdrop fade show"
  ></div>
</template>

<script lang="ts">
import { defineComponent, ref, watch, onMounted } from "vue";
import { Field, Form as VForm } from "vee-validate";
import * as Yup from "yup";
import ApiService from "@/core/services/ApiService";

export default defineComponent({
  name: "user-form-modal",
  components: {
    Field,
    VForm,
  },
  emits: ['close', 'save'],
  props: {
    show: {
      type: Boolean,
      required: true,
    },
    user: {
      type: Object,
      default: null,
    },
    isEdit: {
      type: Boolean,
      default: false,
    },
  },
  setup(props, { emit }) {
    const loading = ref(false);
    const availableDepartments = ref([]);
    const availableRoles = ref([]);

    const formData = ref({
      username: '',
      first_name: '',
      last_name: '',
      email: '',
      phone: '',
      password: '',
      address_line1: '',
      address_line2: '',
      city: '',
      state: '',
      zip: '',
      status: 'active',
      departments: [],
      roles: [],
    });

    const validationSchema = Yup.object().shape({
      username: Yup.string().required('Username is required'),
      first_name: Yup.string().required('First name is required'),
      last_name: Yup.string().required('Last name is required'),
      email: Yup.string().email('Invalid email format').required('Email is required'),
      password: props.isEdit ? Yup.string() : Yup.string().min(6, 'Password must be at least 6 characters').required('Password is required'),
    });

    // Watch for user prop changes
    watch(() => props.user, (newUser) => {
      if (newUser) {
        formData.value = {
          username: newUser.user.username,
          first_name: newUser.first_name,
          last_name: newUser.last_name,
          email: newUser.email,
          phone: newUser.phone || '',
          password: '',
          address_line1: newUser.address_line1 || '',
          address_line2: newUser.address_line2 || '',
          city: newUser.city || '',
          state: newUser.state || '',
          zip: newUser.zip || '',
          status: newUser.status,
          departments: newUser.departments.map((d: any) => d.id),
          roles: newUser.roles.map((r: any) => r.id),
        };
      } else {
        // Reset form for new user
        formData.value = {
          username: '',
          first_name: '',
          last_name: '',
          email: '',
          phone: '',
          password: '',
          address_line1: '',
          address_line2: '',
          city: '',
          state: '',
          zip: '',
          status: 'active',
          departments: [],
          roles: [],
        };
      }
    }, { immediate: true });

    const handleSubmit = async () => {
      loading.value = true;
      try {
        emit('save', formData.value);
      } finally {
        loading.value = false;
      }
    };

    const fetchDepartments = async () => {
      try {
        const { data } = await ApiService.get('/departments/');
        availableDepartments.value = data.results || data;
      } catch (error) {
        console.error('Error fetching departments:', error);
      }
    };

    const fetchRoles = async () => {
      try {
        const { data } = await ApiService.get('/roles/');
        availableRoles.value = data.results || data;
      } catch (error) {
        console.error('Error fetching roles:', error);
      }
    };

    onMounted(() => {
      fetchDepartments();
      fetchRoles();
    });

    return {
      loading,
      formData,
      validationSchema,
      availableDepartments,
      availableRoles,
      handleSubmit,
    };
  },
});
</script>