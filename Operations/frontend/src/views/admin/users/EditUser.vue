<template>
  <div class="d-flex flex-column flex-lg-row">
    <!--begin::Content-->
    <div class="flex-lg-row-fluid me-lg-7 me-xl-10">
      <!--begin::Form-->
      <form
        @submit.prevent="handleSubmit"
        id="edit-user-form"
        class="form"
        novalidate="novalidate"
      >
        <!--begin::Card-->
        <div class="card card-flush py-4">
          <!--begin::Card header-->
          <div class="card-header">
            <div class="card-title">
              <h2>Edit User</h2>
            </div>
          </div>
          <!--end::Card header-->

          <!--begin::Card body-->
          <div class="card-body pt-0">
            <div class="row">
              <!--begin::Basic Information-->
              <div class="col-xl-6">
                <div class="mb-10">
                  <label class="required form-label">First Name</label>
                  <input
                    type="text"
                    v-model="formData.first_name"
                    class="form-control mb-2"
                    :class="{'is-invalid': errors.first_name}"
                    placeholder="Enter first name"
                    required
                  />
                  <div v-if="errors.first_name" class="invalid-feedback">
                    {{ errors.first_name }}
                  </div>
                </div>
              </div>

              <div class="col-xl-6">
                <div class="mb-10">
                  <label class="required form-label">Last Name</label>
                  <input
                    type="text"
                    v-model="formData.last_name"
                    class="form-control mb-2"
                    :class="{'is-invalid': errors.last_name}"
                    placeholder="Enter last name"
                    required
                  />
                  <div v-if="errors.last_name" class="invalid-feedback">
                    {{ errors.last_name }}
                  </div>
                </div>
              </div>

              <div class="col-xl-6">
                <div class="mb-10">
                  <label class="required form-label">Email</label>
                  <input
                    type="email"
                    v-model="formData.email"
                    class="form-control mb-2"
                    :class="{'is-invalid': errors.email}"
                    placeholder="Enter email address"
                    required
                  />
                  <div v-if="errors.email" class="invalid-feedback">
                    {{ errors.email }}
                  </div>
                </div>
              </div>

              <div class="col-xl-6">
                <div class="mb-10">
                  <label class="form-label">Phone</label>
                  <input
                    type="tel"
                    v-model="formData.phone"
                    class="form-control mb-2"
                    :class="{'is-invalid': errors.phone}"
                    placeholder="Enter phone number"
                  />
                  <div v-if="errors.phone" class="invalid-feedback">
                    {{ errors.phone }}
                  </div>
                </div>
              </div>

              <!--begin::Username (Read-only)-->
              <div class="col-xl-6">
                <div class="mb-10">
                  <label class="form-label">Username</label>
                  <input
                    type="text"
                    :value="userProfile?.user?.username"
                    class="form-control mb-2"
                    placeholder="Username"
                    readonly
                    disabled
                  />
                  <div class="form-text">Username cannot be changed</div>
                </div>
              </div>

              <!--begin::Status-->
              <div class="col-xl-6">
                <div class="mb-10">
                  <label class="form-label">Status</label>
                  <select 
                    v-model="formData.status"
                    class="form-select"
                    :class="{'is-invalid': errors.status}"
                  >
                    <option value="active">Active</option>
                    <option value="inactive">Inactive</option>
                  </select>
                  <div v-if="errors.status" class="invalid-feedback">
                    {{ errors.status }}
                  </div>
                </div>
              </div>
            </div>

            <!--begin::Address Section-->
            <div class="separator my-10"></div>
            <h3 class="mb-5">Address Information</h3>
            
            <div class="row">
              <div class="col-xl-12">
                <div class="mb-10">
                  <label class="form-label">Address Line 1</label>
                  <input
                    type="text"
                    v-model="formData.address_line1"
                    class="form-control mb-2"
                    :class="{'is-invalid': errors.address_line1}"
                    placeholder="Enter address line 1"
                  />
                  <div v-if="errors.address_line1" class="invalid-feedback">
                    {{ errors.address_line1 }}
                  </div>
                </div>
              </div>

              <div class="col-xl-12">
                <div class="mb-10">
                  <label class="form-label">Address Line 2</label>
                  <input
                    type="text"
                    v-model="formData.address_line2"
                    class="form-control mb-2"
                    :class="{'is-invalid': errors.address_line2}"
                    placeholder="Enter address line 2 (optional)"
                  />
                  <div v-if="errors.address_line2" class="invalid-feedback">
                    {{ errors.address_line2 }}
                  </div>
                </div>
              </div>

              <div class="col-xl-4">
                <div class="mb-10">
                  <label class="form-label">City</label>
                  <input
                    type="text"
                    v-model="formData.city"
                    class="form-control mb-2"
                    :class="{'is-invalid': errors.city}"
                    placeholder="Enter city"
                  />
                  <div v-if="errors.city" class="invalid-feedback">
                    {{ errors.city }}
                  </div>
                </div>
              </div>

              <div class="col-xl-4">
                <div class="mb-10">
                  <label class="form-label">State</label>
                  <input
                    type="text"
                    v-model="formData.state"
                    class="form-control mb-2"
                    :class="{'is-invalid': errors.state}"
                    placeholder="Enter state"
                  />
                  <div v-if="errors.state" class="invalid-feedback">
                    {{ errors.state }}
                  </div>
                </div>
              </div>

              <div class="col-xl-4">
                <div class="mb-10">
                  <label class="form-label">ZIP Code</label>
                  <input
                    type="text"
                    v-model="formData.zip"
                    class="form-control mb-2"
                    :class="{'is-invalid': errors.zip}"
                    placeholder="Enter ZIP code"
                  />
                  <div v-if="errors.zip" class="invalid-feedback">
                    {{ errors.zip }}
                  </div>
                </div>
              </div>

              <div class="col-xl-6">
                <div class="mb-10">
                  <label class="form-label">Country</label>
                  <input
                    type="text"
                    v-model="formData.country"
                    class="form-control mb-2"
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
          <!--end::Card body-->

          <!--begin::Actions-->
          <div class="card-footer d-flex justify-content-end py-6 px-9">
            <button type="button" @click="goBack" class="btn btn-light btn-active-light-primary me-2">
              Cancel
            </button>
            <button 
              type="submit" 
              :disabled="isSubmitting"
              class="btn btn-primary"
            >
              <span v-if="isSubmitting" class="spinner-border spinner-border-sm me-2"></span>
              {{ isSubmitting ? 'Updating...' : 'Update User' }}
            </button>
          </div>
          <!--end::Actions-->
        </div>
        <!--end::Card-->
      </form>
      <!--end::Form-->
    </div>
    <!--end::Content-->

    <!--begin::Sidebar-->
    <div class="w-lg-300px">
      <!--begin::Card-->
      <div class="card card-flush py-4">
        <!--begin::Card header-->
        <div class="card-header">
          <div class="card-title">
            <h2>User Roles</h2>
          </div>
        </div>
        <!--end::Card header-->

        <!--begin::Card body-->
        <div class="card-body pt-0">
          <div v-if="userProfile?.roles && userProfile.roles.length > 0">
            <div 
              v-for="role in userProfile.roles" 
              :key="role.id"
              class="d-flex align-items-center border border-gray-300 rounded p-3 mb-3"
            >
              <div class="flex-grow-1">
                <div class="fw-bold">{{ role.name }}</div>
                <div class="text-muted fs-7">{{ role.code }}</div>
              </div>
            </div>
          </div>
          <div v-else class="text-center py-5 text-muted">
            <i class="fas fa-user-tag fs-3x mb-3"></i>
            <div>No roles assigned</div>
          </div>

          <div class="mt-5">
            <button
              type="button"
              @click="openManageRoles"
              class="btn btn-sm btn-light-primary w-100"
            >
              <i class="fas fa-cog me-2"></i>
              Manage Roles
            </button>
          </div>
        </div>
        <!--end::Card body-->
      </div>
      <!--end::Card-->
    </div>
    <!--end::Sidebar-->
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, reactive } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import ApiService from '@/core/services/ApiService';
import Swal from 'sweetalert2';

interface UserProfile {
  id: string;
  user: {
    id: number;
    username: string;
    email: string;
    is_staff: boolean;
  };
  first_name: string;
  last_name: string;
  email: string;
  phone?: string;
  address_line1?: string;
  address_line2?: string;
  city?: string;
  state?: string;
  country?: string;
  zip?: string;
  roles: Array<{
    id: string;
    name: string;
    code: string;
    description?: string;
  }>;
  departments: Array<{
    id: string;
    name: string;
    code: string;
  }>;
  flags?: any;
  status: string;
  created_on: string;
}

const route = useRoute();
const router = useRouter();
const userId = route.params.id as string;

const userProfile = ref<UserProfile | null>(null);
const isSubmitting = ref(false);
const errors = ref<Record<string, string>>({});

const formData = reactive({
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
  status: 'active'
});

const fetchUser = async () => {
  try {
    const response = await ApiService.get(`/users/${userId}/`);
    userProfile.value = response.data;
    
    // Populate form data
    Object.assign(formData, {
      first_name: response.data.first_name || '',
      last_name: response.data.last_name || '',
      email: response.data.email || '',
      phone: response.data.phone || '',
      address_line1: response.data.address_line1 || '',
      address_line2: response.data.address_line2 || '',
      city: response.data.city || '',
      state: response.data.state || '',
      country: response.data.country || '',
      zip: response.data.zip || '',
      status: response.data.status || 'active'
    });
  } catch (error: any) {
    console.error('Error fetching user:', error);
    Swal.fire({
      title: 'Error',
      text: 'Failed to load user details',
      icon: 'error',
      confirmButtonText: 'OK'
    }).then(() => {
      router.push('/admin/users');
    });
  }
};

const handleSubmit = async () => {
  if (isSubmitting.value) return;
  
  errors.value = {};
  
  // Basic validation
  if (!formData.first_name.trim()) {
    errors.value.first_name = 'First name is required';
  }
  if (!formData.last_name.trim()) {
    errors.value.last_name = 'Last name is required';
  }
  if (!formData.email.trim()) {
    errors.value.email = 'Email is required';
  }
  
  if (Object.keys(errors.value).length > 0) {
    return;
  }
  
  isSubmitting.value = true;
  
  try {
    await ApiService.patch(`/users/${userId}/`, formData);
    
    Swal.fire({
      title: 'Success!',
      text: 'User has been updated successfully.',
      icon: 'success',
      confirmButtonText: 'OK'
    }).then(() => {
      router.push('/admin/users');
    });
  } catch (error: any) {
    console.error('Error updating user:', error);
    
    // Handle validation errors from backend
    if (error.response?.data) {
      const backendErrors = error.response.data;
      if (typeof backendErrors === 'object') {
        errors.value = { ...backendErrors };
      }
    }
    
    Swal.fire({
      title: 'Error',
      text: 'Failed to update user. Please check the form and try again.',
      icon: 'error',
      confirmButtonText: 'OK'
    });
  } finally {
    isSubmitting.value = false;
  }
};

const openManageRoles = () => {
  router.push(`/admin/users/${userId}/roles`);
};

const goBack = () => {
  router.push('/admin/users');
};

onMounted(() => {
  fetchUser();
});
</script>