<template>
  <!--begin::Modal dialog-->
  <div class="modal fade" id="create-user-modal" tabindex="-1" aria-hidden="true">
    <div class="modal-dialog modal-dialog-centered mw-900px">
      <div class="modal-content">
        <div class="modal-header" id="create-user-modal-header">
          <h2 class="fw-bold">Add New User</h2>
          <div 
            id="create-user-modal-close" 
            data-bs-dismiss="modal" 
            class="btn btn-icon btn-sm btn-active-icon-primary"
          >
            <KTIcon icon-name="cross" icon-class="fs-1" />
          </div>
        </div>

        <div class="modal-body scroll-y mx-5 mx-xl-15 my-7">
          <form 
            @submit.prevent="handleSubmit" 
            id="create-user-modal-form" 
            class="form"
          >
            <!--begin::Scroll-->
            <div class="d-flex flex-column scroll-y me-n7 pe-7">
              
              <!--begin::User Account Section-->
              <div class="mb-10">
                <h3 class="mb-5">User Account</h3>
                
                <div class="row">
                  <div class="col-md-6 mb-7">
                    <label class="required fw-semibold fs-6 mb-2">Username</label>
                    <input
                      type="text"
                      v-model="formData.username"
                      class="form-control form-control-solid"
                      :class="{'is-invalid': errors.username}"
                      placeholder="Enter username"
                      required
                    />
                    <div v-if="errors.username" class="invalid-feedback">
                      {{ errors.username }}
                    </div>
                  </div>

                  <div class="col-md-6 mb-7">
                    <label class="required fw-semibold fs-6 mb-2">Password</label>
                    <div class="position-relative">
                      <input
                        :type="showPassword ? 'text' : 'password'"
                        v-model="formData.password"
                        class="form-control form-control-solid"
                        :class="{'is-invalid': errors.password}"
                        placeholder="Enter password"
                        required
                      />
                      <button
                        type="button"
                        @click="showPassword = !showPassword"
                        class="btn btn-sm btn-icon position-absolute translate-middle top-50 end-0 me-n2"
                      >
                        <i :class="showPassword ? 'fas fa-eye-slash' : 'fas fa-eye'"></i>
                      </button>
                    </div>
                    <div v-if="errors.password" class="invalid-feedback">
                      {{ errors.password }}
                    </div>
                  </div>
                </div>

                <div class="row">
                  <div class="col-md-12 mb-7">
                    <div class="form-check">
                      <input 
                        class="form-check-input" 
                        type="checkbox" 
                        v-model="formData.is_staff"
                        id="is_staff_checkbox"
                      />
                      <label class="form-check-label" for="is_staff_checkbox">
                        Grant staff access (allows login to admin panel)
                      </label>
                    </div>
                  </div>
                </div>
              </div>

              <!--begin::Personal Information Section-->
              <div class="separator border-gray-300 my-10"></div>
              <div class="mb-10">
                <h3 class="mb-5">Personal Information</h3>
                
                <div class="row">
                  <div class="col-md-6 mb-7">
                    <label class="required fw-semibold fs-6 mb-2">First Name</label>
                    <input
                      type="text"
                      v-model="formData.first_name"
                      class="form-control form-control-solid"
                      :class="{'is-invalid': errors.first_name}"
                      placeholder="Enter first name"
                      required
                    />
                    <div v-if="errors.first_name" class="invalid-feedback">
                      {{ errors.first_name }}
                    </div>
                  </div>

                  <div class="col-md-6 mb-7">
                    <label class="required fw-semibold fs-6 mb-2">Last Name</label>
                    <input
                      type="text"
                      v-model="formData.last_name"
                      class="form-control form-control-solid"
                      :class="{'is-invalid': errors.last_name}"
                      placeholder="Enter last name"
                      required
                    />
                    <div v-if="errors.last_name" class="invalid-feedback">
                      {{ errors.last_name }}
                    </div>
                  </div>
                </div>

                <div class="row">
                  <div class="col-md-6 mb-7">
                    <label class="required fw-semibold fs-6 mb-2">Email</label>
                    <input
                      type="email"
                      v-model="formData.email"
                      class="form-control form-control-solid"
                      :class="{'is-invalid': errors.email}"
                      placeholder="Enter email address"
                      required
                    />
                    <div v-if="errors.email" class="invalid-feedback">
                      {{ errors.email }}
                    </div>
                  </div>

                  <div class="col-md-6 mb-7">
                    <label class="fw-semibold fs-6 mb-2">Phone</label>
                    <input
                      type="tel"
                      v-model="formData.phone"
                      class="form-control form-control-solid"
                      :class="{'is-invalid': errors.phone}"
                      placeholder="Enter phone number"
                    />
                    <div v-if="errors.phone" class="invalid-feedback">
                      {{ errors.phone }}
                    </div>
                  </div>
                </div>
              </div>

              <!--begin::Address Information Section-->
              <div class="separator border-gray-300 my-10"></div>
              <div class="mb-10">
                <h3 class="mb-5">Address Information <span class="text-muted fs-7">(Optional)</span></h3>
                
                <div class="row">
                  <div class="col-md-12 mb-7">
                    <label class="fw-semibold fs-6 mb-2">Address Line 1</label>
                    <input
                      type="text"
                      v-model="formData.address_line1"
                      class="form-control form-control-solid"
                      :class="{'is-invalid': errors.address_line1}"
                      placeholder="Enter street address"
                    />
                    <div v-if="errors.address_line1" class="invalid-feedback">
                      {{ errors.address_line1 }}
                    </div>
                  </div>
                </div>

                <div class="row">
                  <div class="col-md-12 mb-7">
                    <label class="fw-semibold fs-6 mb-2">Address Line 2</label>
                    <input
                      type="text"
                      v-model="formData.address_line2"
                      class="form-control form-control-solid"
                      :class="{'is-invalid': errors.address_line2}"
                      placeholder="Apartment, suite, etc. (optional)"
                    />
                    <div v-if="errors.address_line2" class="invalid-feedback">
                      {{ errors.address_line2 }}
                    </div>
                  </div>
                </div>

                <div class="row">
                  <div class="col-md-4 mb-7">
                    <label class="fw-semibold fs-6 mb-2">City</label>
                    <input
                      type="text"
                      v-model="formData.city"
                      class="form-control form-control-solid"
                      :class="{'is-invalid': errors.city}"
                      placeholder="Enter city"
                    />
                    <div v-if="errors.city" class="invalid-feedback">
                      {{ errors.city }}
                    </div>
                  </div>

                  <div class="col-md-4 mb-7">
                    <label class="fw-semibold fs-6 mb-2">State</label>
                    <input
                      type="text"
                      v-model="formData.state"
                      class="form-control form-control-solid"
                      :class="{'is-invalid': errors.state}"
                      placeholder="Enter state"
                    />
                    <div v-if="errors.state" class="invalid-feedback">
                      {{ errors.state }}
                    </div>
                  </div>

                  <div class="col-md-4 mb-7">
                    <label class="fw-semibold fs-6 mb-2">ZIP Code</label>
                    <input
                      type="text"
                      v-model="formData.zip"
                      class="form-control form-control-solid"
                      :class="{'is-invalid': errors.zip}"
                      placeholder="Enter ZIP code"
                    />
                    <div v-if="errors.zip" class="invalid-feedback">
                      {{ errors.zip }}
                    </div>
                  </div>
                </div>

                <div class="row">
                  <div class="col-md-6 mb-7">
                    <label class="fw-semibold fs-6 mb-2">Country</label>
                    <input
                      type="text"
                      v-model="formData.country"
                      class="form-control form-control-solid"
                      :class="{'is-invalid': errors.country}"
                      placeholder="Enter country"
                    />
                    <div v-if="errors.country" class="invalid-feedback">
                      {{ errors.country }}
                    </div>
                  </div>
                </div>
              </div>
            </div>
            <!--end::Scroll-->
          </form>
        </div>

        <div class="modal-footer flex-center">
          <button 
            type="button" 
            class="btn btn-light me-3"
            data-bs-dismiss="modal"
          >
            Cancel
          </button>
          <button 
            type="submit" 
            @click="handleSubmit"
            :disabled="isSubmitting"
            class="btn btn-primary"
          >
            <span v-if="isSubmitting" class="spinner-border spinner-border-sm me-2"></span>
            {{ isSubmitting ? 'Creating...' : 'Create User' }}
          </button>
        </div>
      </div>
    </div>
  </div>
  <!--end::Modal dialog-->
</template>

<script setup lang="ts">
import { ref, reactive, watch } from 'vue';
import ApiService from '@/core/services/ApiService';
import Swal from 'sweetalert2';

interface Props {
  show: boolean;
}

interface Emits {
  (e: 'close'): void;
  (e: 'user-created', user: any): void;
}

const props = defineProps<Props>();
const emit = defineEmits<Emits>();

const isSubmitting = ref(false);
const showPassword = ref(false);
const errors = ref<Record<string, string>>({});

const formData = reactive({
  username: '',
  password: '',
  is_staff: false,
  first_name: '',
  last_name: '',
  email: '',
  phone: '',
  address_line1: '',
  address_line2: '',
  city: '',
  state: '',
  country: '',
  zip: ''
});

const resetForm = () => {
  Object.assign(formData, {
    username: '',
    password: '',
    is_staff: false,
    first_name: '',
    last_name: '',
    email: '',
    phone: '',
    address_line1: '',
    address_line2: '',
    city: '',
    state: '',
    country: '',
    zip: ''
  });
  errors.value = {};
  showPassword.value = false;
};

const validateForm = (): boolean => {
  errors.value = {};
  
  if (!formData.username.trim()) {
    errors.value.username = 'Username is required';
  }
  if (!formData.password.trim()) {
    errors.value.password = 'Password is required';
  } else if (formData.password.length < 6) {
    errors.value.password = 'Password must be at least 6 characters';
  }
  if (!formData.first_name.trim()) {
    errors.value.first_name = 'First name is required';
  }
  if (!formData.last_name.trim()) {
    errors.value.last_name = 'Last name is required';
  }
  if (!formData.email.trim()) {
    errors.value.email = 'Email is required';
  } else if (!/\S+@\S+\.\S+/.test(formData.email)) {
    errors.value.email = 'Email format is invalid';
  }
  
  return Object.keys(errors.value).length === 0;
};

const handleSubmit = async () => {
  if (isSubmitting.value) return;
  
  if (!validateForm()) {
    return;
  }
  
  isSubmitting.value = true;
  
  try {
    // First create the Django User
    const userData = {
      username: formData.username,
      password: formData.password,
      email: formData.email,
      is_staff: formData.is_staff
    };
    
    const userResponse = await ApiService.post('/auth/register/', userData);
    const createdUser = userResponse.data;
    
    // Then create the UserProfile
    const profileData = {
      user_id: createdUser.id,
      first_name: formData.first_name,
      last_name: formData.last_name,
      email: formData.email,
      phone: formData.phone || null,
      address_line1: formData.address_line1 || null,
      address_line2: formData.address_line2 || null,
      city: formData.city || null,
      state: formData.state || null,
      country: formData.country || null,
      zip: formData.zip || null,
      status: 'active'
    };
    
    const profileResponse = await ApiService.post('/users/', profileData);
    
    emit('user-created', profileResponse.data);
    emit('close');
    
    Swal.fire({
      title: 'Success!',
      text: 'User has been created successfully.',
      icon: 'success',
      confirmButtonText: 'OK',
      timer: 3000
    });
    
    resetForm();
    
  } catch (error: any) {
    console.error('Error creating user:', error);
    
    // Handle validation errors from backend
    if (error.response?.data) {
      const backendErrors = error.response.data;
      if (typeof backendErrors === 'object') {
        // Map backend field names to frontend field names
        Object.keys(backendErrors).forEach(key => {
          errors.value[key] = Array.isArray(backendErrors[key]) 
            ? backendErrors[key][0] 
            : backendErrors[key];
        });
      }
    }
    
    if (Object.keys(errors.value).length === 0) {
      Swal.fire({
        title: 'Error',
        text: 'Failed to create user. Please try again.',
        icon: 'error',
        confirmButtonText: 'OK'
      });
    }
  } finally {
    isSubmitting.value = false;
  }
};

// Watch for modal show/hide
watch(() => props.show, (newShow) => {
  if (newShow) {
    resetForm();
  }
});
</script>