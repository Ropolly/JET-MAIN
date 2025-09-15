<template>
  <div class="d-flex flex-column flex-lg-row">
    <!--begin::Content-->
    <div class="flex-lg-row-fluid me-lg-7 me-xl-10">
      <!--begin::Form-->
      <form @submit.prevent="handleSubmit" id="manage-roles-form" class="form">
        <!--begin::Card-->
        <div class="card card-flush py-4">
          <!--begin::Card header-->
          <div class="card-header">
            <div class="card-title">
              <h2>Manage User Roles</h2>
              <div class="text-muted fs-7 mt-1">
                Assign or remove roles for {{ getUserName() }}
              </div>
            </div>
          </div>
          <!--end::Card header-->

          <!--begin::Card body-->
          <div class="card-body pt-0">
            <!--begin::Loading state-->
            <div v-if="loading" class="d-flex justify-content-center py-10">
              <div class="spinner-border text-primary" role="status">
                <span class="visually-hidden">Loading...</span>
              </div>
            </div>

            <!--begin::Available Roles-->
            <div v-else>
              <div class="mb-10">
                <h3 class="mb-5">Available Roles</h3>
                <div class="text-muted fs-7 mb-7">
                  Select the roles you want to assign to this user. Changes will be saved when you click "Update Roles".
                </div>

                <div v-if="availableRoles.length === 0" class="text-center py-10">
                  <i class="fas fa-user-tag fs-3x text-muted mb-4"></i>
                  <div class="text-muted">No roles available</div>
                </div>

                <div v-else class="row">
                  <div 
                    v-for="role in availableRoles" 
                    :key="role.id"
                    class="col-lg-6 mb-5"
                  >
                    <div class="d-flex align-items-start border border-gray-300 rounded p-5">
                      <div class="form-check form-check-custom form-check-solid me-4 mt-1">
                        <input
                          class="form-check-input"
                          type="checkbox"
                          :id="`role-${role.id}`"
                          v-model="selectedRoleIds"
                          :value="role.id"
                        />
                        <label class="form-check-label" :for="`role-${role.id}`"></label>
                      </div>
                      
                      <div class="flex-grow-1">
                        <div class="d-flex align-items-center mb-2">
                          <div class="symbol symbol-30px me-3">
                            <div class="symbol-label bg-light-primary">
                              <i class="fas fa-user-tag text-primary fs-7"></i>
                            </div>
                          </div>
                          <div>
                            <div class="fw-bold text-gray-900 fs-6">{{ role.name }}</div>
                            <div class="text-muted fs-7">{{ role.code }}</div>
                          </div>
                        </div>
                        
                        <div v-if="role.description" class="text-muted fs-8">
                          {{ role.description }}
                        </div>
                        
                        <!-- Show permissions if available -->
                        <div v-if="role.permissions && role.permissions.length > 0" class="mt-3">
                          <div class="text-muted fs-8 fw-semibold mb-2">Permissions:</div>
                          <div class="d-flex flex-wrap">
                            <span 
                              v-for="permission in role.permissions.slice(0, 3)" 
                              :key="permission.id"
                              class="badge badge-light-info me-1 mb-1 fs-8"
                            >
                              {{ permission.name }}
                            </span>
                            <span 
                              v-if="role.permissions.length > 3"
                              class="badge badge-light-secondary me-1 mb-1 fs-8"
                            >
                              +{{ role.permissions.length - 3 }} more
                            </span>
                          </div>
                        </div>
                      </div>
                    </div>
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
              :disabled="isSubmitting || loading"
              class="btn btn-primary"
            >
              <span v-if="isSubmitting" class="spinner-border spinner-border-sm me-2"></span>
              {{ isSubmitting ? 'Updating...' : 'Update Roles' }}
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
      <!--begin::User Info Card-->
      <div class="card card-flush py-4 mb-5">
        <!--begin::Card header-->
        <div class="card-header">
          <div class="card-title">
            <h2>User Info</h2>
          </div>
        </div>
        <!--end::Card header-->

        <!--begin::Card body-->
        <div class="card-body pt-0">
          <div v-if="userProfile" class="d-flex align-items-center">
            <div class="symbol symbol-60px me-4">
              <div class="symbol-label bg-light-primary">
                <i class="ki-duotone ki-profile-circle fs-2x text-primary">
                  <span class="path1"></span>
                  <span class="path2"></span>
                  <span class="path3"></span>
                </i>
              </div>
            </div>
            <div>
              <div class="fw-bold fs-6 text-gray-900 mb-1">{{ getUserName() }}</div>
              <div class="text-muted fs-7">{{ userProfile.user.username }}</div>
              <div class="text-muted fs-8">{{ userProfile.email }}</div>
            </div>
          </div>
        </div>
        <!--end::Card body-->
      </div>
      <!--end::User Info Card-->

      <!--begin::Current Roles Card-->
      <div class="card card-flush py-4">
        <!--begin::Card header-->
        <div class="card-header">
          <div class="card-title">
            <h2>Current Roles</h2>
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
              <div class="symbol symbol-30px me-3">
                <div class="symbol-label bg-light-success">
                  <i class="fas fa-check text-success fs-7"></i>
                </div>
              </div>
              <div class="flex-grow-1">
                <div class="fw-bold fs-7">{{ role.name }}</div>
                <div class="text-muted fs-8">{{ role.code }}</div>
              </div>
            </div>
          </div>
          <div v-else class="text-center py-5 text-muted">
            <i class="fas fa-user-tag fs-2x mb-3"></i>
            <div class="fs-7">No roles assigned</div>
          </div>

          <!--begin::Summary-->
          <div class="separator my-5"></div>
          <div class="d-flex justify-content-between align-items-center">
            <span class="text-muted fs-7">Selected roles:</span>
            <span class="badge badge-light-primary">{{ selectedRoleIds.length }}</span>
          </div>
        </div>
        <!--end::Card body-->
      </div>
      <!--end::Current Roles Card-->
    </div>
    <!--end::Sidebar-->
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import ApiService from '@/core/services/ApiService';
import Swal from 'sweetalert2';

interface Role {
  id: string;
  name: string;
  code: string;
  description?: string;
  permissions?: Array<{
    id: string;
    name: string;
    codename: string;
  }>;
}

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
  roles: Role[];
  departments: Array<{
    id: string;
    name: string;
    code: string;
  }>;
  status: string;
  created_on: string;
}

const route = useRoute();
const router = useRouter();
const userId = route.params.id as string;

const userProfile = ref<UserProfile | null>(null);
const availableRoles = ref<Role[]>([]);
const selectedRoleIds = ref<string[]>([]);
const loading = ref(true);
const isSubmitting = ref(false);

const fetchUserAndRoles = async () => {
  try {
    loading.value = true;
    
    // Fetch user profile and available roles in parallel
    const [userResponse, rolesResponse] = await Promise.all([
      ApiService.get(`/users/${userId}/`),
      ApiService.get('/roles/')
    ]);
    
    userProfile.value = userResponse.data;
    availableRoles.value = rolesResponse.data.results || rolesResponse.data;
    
    // Pre-select user's current roles
    selectedRoleIds.value = userProfile.value?.roles?.map(role => role.id) || [];
    
  } catch (error: any) {
    console.error('Error fetching data:', error);
    Swal.fire({
      title: 'Error',
      text: 'Failed to load user and roles data',
      icon: 'error',
      confirmButtonText: 'OK'
    }).then(() => {
      router.push('/admin/users');
    });
  } finally {
    loading.value = false;
  }
};

const getUserName = (): string => {
  if (!userProfile.value) return 'Loading...';
  const fullName = `${userProfile.value.first_name || ''} ${userProfile.value.last_name || ''}`.trim();
  return fullName || userProfile.value.user.username;
};

const handleSubmit = async () => {
  if (isSubmitting.value || loading.value) return;
  
  isSubmitting.value = true;
  
  try {
    // Update user roles
    await ApiService.patch(`/users/${userId}/`, {
      role_ids: selectedRoleIds.value
    });
    
    Swal.fire({
      title: 'Success!',
      text: 'User roles have been updated successfully.',
      icon: 'success',
      confirmButtonText: 'OK'
    }).then(() => {
      router.push(`/admin/users/${userId}`);
    });
    
  } catch (error: any) {
    console.error('Error updating user roles:', error);
    
    let errorMessage = 'Failed to update user roles. Please try again.';
    if (error.response?.data?.detail) {
      errorMessage = error.response.data.detail;
    } else if (error.response?.data?.message) {
      errorMessage = error.response.data.message;
    }
    
    Swal.fire({
      title: 'Error',
      text: errorMessage,
      icon: 'error',
      confirmButtonText: 'OK'
    });
  } finally {
    isSubmitting.value = false;
  }
};

const goBack = () => {
  router.push(`/admin/users/${userId}`);
};

onMounted(() => {
  fetchUserAndRoles();
});
</script>