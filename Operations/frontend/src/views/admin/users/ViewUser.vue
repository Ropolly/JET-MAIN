<template>
  <!--begin::Layout-->
  <div class="d-flex flex-column flex-lg-row align-items-lg-start">
    <!--begin::Content-->
    <div class="flex-lg-row-fluid me-lg-5 order-2 order-lg-1 mb-10 mb-lg-0">
      
      <!-- User Profile Card -->
      <div class="card mb-5 mb-xxl-8">
        <!--begin::Card body-->
        <div class="card-body pt-9 pb-0">
          <!--begin::Details-->
          <div class="d-flex flex-wrap flex-sm-nowrap">
            <!--begin::Image-->
            <div class="me-7 mb-4">
              <div class="symbol symbol-100px symbol-lg-160px symbol-fixed position-relative">
                <div class="symbol-label bg-light-primary">
                  <i class="ki-duotone ki-profile-circle fs-2x text-primary">
                    <span class="path1"></span>
                    <span class="path2"></span>
                    <span class="path3"></span>
                  </i>
                </div>
              </div>
            </div>
            <!--end::Image-->

            <!--begin::Info-->
            <div class="flex-grow-1">
              <!--begin::Title-->
              <div class="d-flex justify-content-between align-items-start flex-wrap mb-2">
                <!--begin::User-->
                <div class="d-flex flex-column">
                  <!--begin::Name-->
                  <div class="d-flex align-items-center mb-2">
                    <a href="#" class="text-gray-900 text-hover-primary fs-2 fw-bold me-1">
                      {{ getUserName() }}
                    </a>
                    <span 
                      :class="`badge badge-light-${getStatusColor()} fs-8 fw-bold`"
                    >
                      {{ userProfile?.status === 'active' ? 'Active' : 'Inactive' }}
                    </span>
                  </div>
                  <!--end::Name-->

                  <!--begin::Info-->
                  <div class="d-flex flex-wrap fw-semibold fs-6 mb-4 pe-2">
                    <a href="#" class="d-flex align-items-center text-gray-500 text-hover-primary me-5 mb-2">
                      <i class="ki-duotone ki-profile-circle fs-4 me-1">
                        <span class="path1"></span>
                        <span class="path2"></span>
                        <span class="path3"></span>
                      </i>
                      {{ userProfile?.user?.username }}
                    </a>
                    <a href="#" class="d-flex align-items-center text-gray-500 text-hover-primary me-5 mb-2">
                      <i class="ki-duotone ki-sms fs-4 me-1">
                        <span class="path1"></span>
                        <span class="path2"></span>
                      </i>
                      {{ userProfile?.email || 'No email' }}
                    </a>
                    <a href="#" v-if="userProfile?.phone" class="d-flex align-items-center text-gray-500 text-hover-primary mb-2">
                      <i class="ki-duotone ki-phone fs-4 me-1">
                        <span class="path1"></span>
                        <span class="path2"></span>
                      </i>
                      {{ userProfile.phone }}
                    </a>
                  </div>
                  <!--end::Info-->
                </div>
                <!--end::User-->
              </div>
              <!--end::Title-->

              <!--begin::Stats-->
              <div class="d-flex flex-wrap flex-stack">
                <!--begin::Wrapper-->
                <div class="d-flex flex-column flex-grow-1 pe-8">
                  <!--begin::Stats-->
                  <div class="d-flex flex-wrap">
                    <!--begin::Stat-->
                    <div class="border border-gray-300 border-dashed rounded min-w-125px py-3 px-4 me-6 mb-3">
                      <!--begin::Number-->
                      <div class="d-flex align-items-center">
                        <div class="fs-2 fw-bold text-gray-900 me-2 lh-1 ls-n2">
                          {{ userProfile?.roles?.length || 0 }}
                        </div>
                      </div>
                      <!--end::Number-->
                      <!--begin::Label-->
                      <div class="fs-7 fw-semibold text-gray-500">Roles</div>
                      <!--end::Label-->
                    </div>
                    <!--end::Stat-->

                    <!--begin::Stat-->
                    <div class="border border-gray-300 border-dashed rounded min-w-125px py-3 px-4 me-6 mb-3">
                      <!--begin::Number-->
                      <div class="d-flex align-items-center">
                        <div class="fs-2 fw-bold text-gray-900 me-2 lh-1 ls-n2">
                          {{ userProfile?.departments?.length || 0 }}
                        </div>
                      </div>
                      <!--end::Number-->
                      <!--begin::Label-->
                      <div class="fs-7 fw-semibold text-gray-500">Departments</div>
                      <!--end::Label-->
                    </div>
                    <!--end::Stat-->

                    <!--begin::Stat-->
                    <div class="border border-gray-300 border-dashed rounded min-w-125px py-3 px-4 me-6 mb-3">
                      <!--begin::Number-->
                      <div class="d-flex align-items-center">
                        <div class="fs-2 fw-bold text-gray-900 me-2 lh-1 ls-n2">
                          {{ formatDate(userProfile?.created_on) }}
                        </div>
                      </div>
                      <!--end::Number-->
                      <!--begin::Label-->
                      <div class="fs-7 fw-semibold text-gray-500">Member Since</div>
                      <!--end::Label-->
                    </div>
                    <!--end::Stat-->
                  </div>
                  <!--end::Stats-->
                </div>
                <!--end::Wrapper-->
              </div>
              <!--end::Stats-->
            </div>
            <!--end::Info-->
          </div>
          <!--end::Details-->
        </div>
      </div>

      <!-- User Details Card -->
      <div class="card mb-5 mb-xxl-8">
        <!--begin::Header-->
        <div class="card-header border-0 pt-5">
          <h3 class="card-title align-items-start flex-column">
            <span class="card-label fw-bold fs-3 mb-1">User Details</span>
            <span class="text-muted mt-1 fw-semibold fs-7">Personal and contact information</span>
          </h3>
        </div>
        <!--end::Header-->

        <!--begin::Body-->
        <div class="card-body py-3">
          <div class="row">
            <div class="col-lg-6">
              <div class="mb-7">
                <label class="fw-semibold fs-6 text-gray-600">First Name</label>
                <div class="fw-bold fs-6 text-gray-900">{{ userProfile?.first_name || 'Not set' }}</div>
              </div>
              <div class="mb-7">
                <label class="fw-semibold fs-6 text-gray-600">Email</label>
                <div class="fw-bold fs-6 text-gray-900">{{ userProfile?.email || 'Not set' }}</div>
              </div>
              <div class="mb-7">
                <label class="fw-semibold fs-6 text-gray-600">Address Line 1</label>
                <div class="fw-bold fs-6 text-gray-900">{{ userProfile?.address_line1 || 'Not set' }}</div>
              </div>
              <div class="mb-7">
                <label class="fw-semibold fs-6 text-gray-600">City</label>
                <div class="fw-bold fs-6 text-gray-900">{{ userProfile?.city || 'Not set' }}</div>
              </div>
            </div>
            <div class="col-lg-6">
              <div class="mb-7">
                <label class="fw-semibold fs-6 text-gray-600">Last Name</label>
                <div class="fw-bold fs-6 text-gray-900">{{ userProfile?.last_name || 'Not set' }}</div>
              </div>
              <div class="mb-7">
                <label class="fw-semibold fs-6 text-gray-600">Phone</label>
                <div class="fw-bold fs-6 text-gray-900">{{ userProfile?.phone || 'Not set' }}</div>
              </div>
              <div class="mb-7">
                <label class="fw-semibold fs-6 text-gray-600">Address Line 2</label>
                <div class="fw-bold fs-6 text-gray-900">{{ userProfile?.address_line2 || 'Not set' }}</div>
              </div>
              <div class="mb-7">
                <label class="fw-semibold fs-6 text-gray-600">State / ZIP</label>
                <div class="fw-bold fs-6 text-gray-900">
                  {{ formatStateZip() }}
                </div>
              </div>
            </div>
          </div>
        </div>
        <!--end::Body-->
      </div>

      <!-- User Roles Card -->
      <div class="card mb-5 mb-xxl-8">
        <!--begin::Header-->
        <div class="card-header border-0 pt-5">
          <h3 class="card-title align-items-start flex-column">
            <span class="card-label fw-bold fs-3 mb-1">Assigned Roles</span>
            <span class="text-muted mt-1 fw-semibold fs-7">User permissions and access levels</span>
          </h3>
          <div class="card-toolbar">
            <button
              type="button"
              @click="manageRoles"
              class="btn btn-sm btn-light-primary"
            >
              <i class="fas fa-cog me-2"></i>
              Manage Roles
            </button>
          </div>
        </div>
        <!--end::Header-->

        <!--begin::Body-->
        <div class="card-body py-3">
          <div v-if="userProfile?.roles && userProfile.roles.length > 0" class="row">
            <div 
              v-for="role in userProfile.roles" 
              :key="role.id"
              class="col-lg-6 mb-5"
            >
              <div class="d-flex align-items-center border border-gray-300 rounded p-5">
                <div class="symbol symbol-40px me-4">
                  <div class="symbol-label bg-light-primary">
                    <i class="fas fa-user-tag text-primary fs-6"></i>
                  </div>
                </div>
                <div class="flex-grow-1">
                  <div class="fw-bold text-gray-900 fs-6">{{ role.name }}</div>
                  <div class="text-muted fs-7">{{ role.code }}</div>
                  <div v-if="role.description" class="text-muted fs-8 mt-1">
                    {{ role.description }}
                  </div>
                </div>
              </div>
            </div>
          </div>
          <div v-else class="text-center py-10">
            <i class="fas fa-user-tag fs-3x text-muted mb-4"></i>
            <div class="text-muted fs-6 mb-4">No roles assigned to this user</div>
            <button
              type="button"
              @click="manageRoles"
              class="btn btn-primary"
            >
              <i class="fas fa-plus me-2"></i>
              Assign Roles
            </button>
          </div>
        </div>
        <!--end::Body-->
      </div>
    </div>
    <!--end::Content-->

    <!--begin::Sidebar-->
    <div class="flex-column flex-lg-row-auto w-lg-350px w-xl-400px mb-10 order-1 order-lg-2">
      <!-- Quick Actions Card -->
      <div class="card mb-5 mb-xxl-8">
        <!--begin::Header-->
        <div class="card-header border-0 pt-5">
          <h3 class="card-title align-items-start flex-column">
            <span class="card-label fw-bold fs-3 mb-1">Quick Actions</span>
          </h3>
        </div>
        <!--end::Header-->

        <!--begin::Body-->
        <div class="card-body py-3">
          <div class="d-grid gap-2">
            <button
              type="button"
              @click="editUser"
              class="btn btn-light-primary"
            >
              <i class="fas fa-edit me-2"></i>
              Edit User
            </button>
            <button
              type="button"
              @click="manageRoles"
              class="btn btn-light-info"
            >
              <i class="fas fa-user-tag me-2"></i>
              Manage Roles
            </button>
            <button
              type="button"
              @click="resetPassword"
              class="btn btn-light-warning"
            >
              <i class="fas fa-key me-2"></i>
              Reset Password
            </button>
            <div class="separator my-3"></div>
            <button
              type="button"
              @click="toggleStatus"
              :class="`btn btn-light-${userProfile?.status === 'active' ? 'warning' : 'success'}`"
            >
              <i class="fas fa-power-off me-2"></i>
              {{ userProfile?.status === 'active' ? 'Deactivate' : 'Activate' }}
            </button>
            <button
              type="button"
              @click="deleteUser"
              class="btn btn-light-danger"
            >
              <i class="fas fa-trash me-2"></i>
              Delete User
            </button>
          </div>
        </div>
        <!--end::Body-->
      </div>
    </div>
    <!--end::Sidebar-->
  </div>
  <!--end::Layout-->
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
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
const loading = ref(true);

const fetchUser = async () => {
  try {
    loading.value = true;
    const response = await ApiService.get(`/users/${userId}/`);
    userProfile.value = response.data;
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
  } finally {
    loading.value = false;
  }
};

const getUserName = (): string => {
  if (!userProfile.value) return 'Loading...';
  const fullName = `${userProfile.value.first_name || ''} ${userProfile.value.last_name || ''}`.trim();
  return fullName || userProfile.value.user.username;
};

const getStatusColor = (): string => {
  return userProfile.value?.status === 'active' ? 'success' : 'danger';
};

const formatDate = (dateString?: string): string => {
  if (!dateString) return 'Unknown';
  return new Date(dateString).toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric'
  });
};

const formatStateZip = (): string => {
  const state = userProfile.value?.state;
  const zip = userProfile.value?.zip;
  
  if (state && zip) return `${state} ${zip}`;
  if (state) return state;
  if (zip) return zip;
  return 'Not set';
};

const editUser = () => {
  router.push(`/admin/users/${userId}/edit`);
};

const manageRoles = () => {
  router.push(`/admin/users/${userId}/roles`);
};

const resetPassword = () => {
  Swal.fire({
    title: 'Reset Password',
    text: `Send password reset email to ${getUserName()}?`,
    icon: 'question',
    showCancelButton: true,
    confirmButtonText: 'Yes, send reset email',
    cancelButtonText: 'Cancel'
  }).then((result) => {
    if (result.isConfirmed) {
      Swal.fire('Email Sent!', 'Password reset email has been sent.', 'success');
    }
  });
};

const toggleStatus = async () => {
  if (!userProfile.value) return;
  
  const isActive = userProfile.value.status === 'active';
  const action = isActive ? 'deactivate' : 'activate';
  
  const result = await Swal.fire({
    title: `${action.charAt(0).toUpperCase() + action.slice(1)} User`,
    text: `Are you sure you want to ${action} ${getUserName()}?`,
    icon: 'question',
    showCancelButton: true,
    confirmButtonText: `Yes, ${action}!`,
    cancelButtonText: 'Cancel'
  });
  
  if (result.isConfirmed) {
    try {
      await ApiService.patch(`/users/${userId}/`, {
        status: isActive ? 'inactive' : 'active'
      });
      
      // Refresh user data
      await fetchUser();
      
      Swal.fire('Updated!', `User has been ${action}d.`, 'success');
    } catch (error: any) {
      console.error('Error updating user:', error);
      Swal.fire('Error!', 'Failed to update user. Please try again.', 'error');
    }
  }
};

const deleteUser = async () => {
  if (!userProfile.value) return;
  
  const result = await Swal.fire({
    title: 'Delete User',
    text: `Are you sure you want to delete ${getUserName()}? This action cannot be undone.`,
    icon: 'warning',
    showCancelButton: true,
    confirmButtonText: 'Yes, delete it!',
    cancelButtonText: 'Cancel',
    confirmButtonColor: '#d33'
  });
  
  if (result.isConfirmed) {
    try {
      await ApiService.delete(`/users/${userId}/`);
      
      Swal.fire('Deleted!', 'User has been deleted.', 'success').then(() => {
        router.push('/admin/users');
      });
    } catch (error: any) {
      console.error('Error deleting user:', error);
      Swal.fire('Error!', 'Failed to delete user. Please try again.', 'error');
    }
  }
};

onMounted(() => {
  fetchUser();
});
</script>