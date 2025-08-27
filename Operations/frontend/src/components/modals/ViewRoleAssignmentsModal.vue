<template>
  <!--begin::Modal - View role assignments-->
  <div
    class="modal fade show"
    id="kt_modal_view_role_assignments"
    ref="modalRef"
    tabindex="-1"
    aria-hidden="false"
    style="display: block;"
  >
    <!--begin::Modal dialog-->
    <div class="modal-dialog modal-xl">
      <!--begin::Modal content-->
      <div class="modal-content">
        <!--begin::Modal header-->
        <div class="modal-header">
          <!--begin::Title-->
          <div>
            <h2>Role Assignments</h2>
            <div class="text-muted fs-6">
              <span 
                :class="`badge badge-light-${getRoleColor(role.code)} me-2`"
              >
                {{ role.code }}
              </span>
              {{ role.name }}
            </div>
          </div>
          <!--end::Title-->

          <!--begin::Close-->
          <div
            class="btn btn-sm btn-icon btn-active-color-primary"
            @click="closeModal"
          >
            <KTIcon icon-name="cross" icon-class="fs-1" />
          </div>
          <!--end::Close-->
        </div>
        <!--end::Modal header-->

        <!--begin::Modal body-->
        <div class="modal-body scroll-y mx-5 my-7">
          <!--begin::Stats Cards-->
          <div class="row g-6 mb-8">
            <div class="col-xl-3">
              <div class="card card-flush">
                <div class="card-body text-center">
                  <div class="fs-2hx fw-bold text-gray-800 mb-2">{{ getTotalAssignments() }}</div>
                  <div class="fs-7 fw-semibold text-gray-500">Total Assignments</div>
                </div>
              </div>
            </div>
            <div class="col-xl-3">
              <div class="card card-flush">
                <div class="card-body text-center">
                  <div class="fs-2hx fw-bold text-success mb-2">{{ getActiveAssignments() }}</div>
                  <div class="fs-7 fw-semibold text-gray-500">Active Now</div>
                </div>
              </div>
            </div>
            <div class="col-xl-3">
              <div class="card card-flush">
                <div class="card-body text-center">
                  <div class="fs-2hx fw-bold text-warning mb-2">{{ getFutureAssignments() }}</div>
                  <div class="fs-7 fw-semibold text-gray-500">Future Assignments</div>
                </div>
              </div>
            </div>
            <div class="col-xl-3">
              <div class="card card-flush">
                <div class="card-body text-center">
                  <div class="fs-2hx fw-bold text-secondary mb-2">{{ getExpiredAssignments() }}</div>
                  <div class="fs-7 fw-semibold text-gray-500">Expired</div>
                </div>
              </div>
            </div>
          </div>
          <!--end::Stats Cards-->

          <!--begin::Filter Tabs-->
          <ul class="nav nav-tabs nav-line-tabs nav-line-tabs-2x mb-8 fs-6">
            <li class="nav-item">
              <a
                class="nav-link"
                :class="{ active: activeFilter === 'all' }"
                @click="activeFilter = 'all'"
                href="#"
              >
                All Assignments ({{ getTotalAssignments() }})
              </a>
            </li>
            <li class="nav-item">
              <a
                class="nav-link"
                :class="{ active: activeFilter === 'active' }"
                @click="activeFilter = 'active'"
                href="#"
              >
                Active ({{ getActiveAssignments() }})
              </a>
            </li>
            <li class="nav-item">
              <a
                class="nav-link"
                :class="{ active: activeFilter === 'future' }"
                @click="activeFilter = 'future'"
                href="#"
              >
                Future ({{ getFutureAssignments() }})
              </a>
            </li>
            <li class="nav-item">
              <a
                class="nav-link"
                :class="{ active: activeFilter === 'expired' }"
                @click="activeFilter = 'expired'"
                href="#"
              >
                Expired ({{ getExpiredAssignments() }})
              </a>
            </li>
          </ul>
          <!--end::Filter Tabs-->

          <!--begin::Assignments Table-->
          <div v-if="loading" class="text-center py-10">
            <div class="spinner-border text-primary" role="status">
              <span class="visually-hidden">Loading...</span>
            </div>
          </div>

          <div v-else-if="filteredAssignments.length === 0" class="text-center py-10">
            <div class="text-muted fs-4 mb-5">
              No {{ activeFilter === 'all' ? '' : activeFilter }} assignments found
            </div>
            <div class="text-gray-600">
              {{ getEmptyStateMessage() }}
            </div>
          </div>

          <div v-else class="table-responsive">
            <table class="table table-row-dashed table-row-gray-300 gy-7">
              <thead>
                <tr class="fw-bold fs-6 text-gray-800">
                  <th>Staff Member</th>
                  <th>Start Date</th>
                  <th>End Date</th>
                  <th>Duration</th>
                  <th>Status</th>
                  <th>Created</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="assignment in filteredAssignments" :key="assignment.id">
                  <td>
                    <div class="d-flex align-items-center">
                      <div class="symbol symbol-circle symbol-40px overflow-hidden me-3">
                        <div class="symbol-label bg-light-info">
                          <i class="ki-duotone ki-user fs-2x text-info">
                            <span class="path1"></span>
                            <span class="path2"></span>
                          </i>
                        </div>
                      </div>
                      <div>
                        <a 
                          @click="navigateToStaff(assignment.staff_id)" 
                          class="text-gray-800 text-hover-primary mb-1 fs-6 fw-bold cursor-pointer"
                        >
                          {{ getStaffName(assignment) }}
                        </a>
                        <div class="text-muted fs-7">{{ getStaffContact(assignment) }}</div>
                      </div>
                    </div>
                  </td>
                  <td>
                    <span v-if="assignment.start_on" class="text-gray-600">
                      {{ formatDate(assignment.start_on) }}
                    </span>
                    <span v-else class="text-muted">Not set</span>
                  </td>
                  <td>
                    <span v-if="assignment.end_on" class="text-gray-600">
                      {{ formatDate(assignment.end_on) }}
                    </span>
                    <span v-else class="text-success fw-bold">Ongoing</span>
                  </td>
                  <td>
                    {{ getAssignmentDuration(assignment) }}
                  </td>
                  <td>
                    <span :class="`badge badge-light-${getAssignmentStatusColor(assignment)}`">
                      {{ getAssignmentStatus(assignment) }}
                    </span>
                  </td>
                  <td>
                    <span class="text-muted">{{ formatDate(assignment.created_on) }}</span>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
          <!--end::Assignments Table-->
        </div>
        <!--end::Modal body-->

        <!--begin::Modal footer-->
        <div class="modal-footer flex-center">
          <button
            type="button"
            class="btn btn-light"
            @click="closeModal"
          >
            Close
          </button>
        </div>
        <!--end::Modal footer-->
      </div>
      <!--end::Modal content-->
    </div>
    <!--end::Modal dialog-->
  </div>
  <!--begin::Modal backdrop-->
  <div class="modal-backdrop fade show"></div>
  <!--end::Modal backdrop-->
  <!--end::Modal - View role assignments-->
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from "vue";
import ApiService from "@/core/services/ApiService";
import { useRouter } from "vue-router";

interface Props {
  role: {
    id: string;
    code: string;
    name: string;
  };
}

const props = defineProps<Props>();
const emit = defineEmits(['close']);
const router = useRouter();

const loading = ref(false);
const assignments = ref<any[]>([]);
const activeFilter = ref('all');

// Methods
const fetchAssignments = async () => {
  try {
    loading.value = true;
    const response = await ApiService.get(`/staff-role-memberships/?role_id=${props.role.id}`);
    assignments.value = response.data.results || response.data || [];
    console.log('Role assignments loaded:', assignments.value.length);
  } catch (error) {
    console.error('Error fetching role assignments:', error);
  } finally {
    loading.value = false;
  }
};

const getRoleColor = (roleCode: string): string => {
  const colors: Record<string, string> = {
    PIC: 'primary',
    SIC: 'info',
    RN: 'success',
    PARAMEDIC: 'warning',
    MD: 'danger',
    RT: 'secondary',
    EMT: 'dark',
    DISPATCHER: 'info',
  };
  return colors[roleCode] || 'secondary';
};

const getAssignmentStatus = (assignment: any): string => {
  const today = new Date().toISOString().split('T')[0];
  
  if (assignment.start_on && assignment.start_on > today) {
    return 'Future';
  }
  
  if (assignment.end_on && assignment.end_on < today) {
    return 'Expired';
  }
  
  return 'Active';
};

const getAssignmentStatusColor = (assignment: any): string => {
  const status = getAssignmentStatus(assignment);
  const colors: Record<string, string> = {
    Active: 'success',
    Future: 'warning',
    Expired: 'secondary',
  };
  return colors[status] || 'secondary';
};

const getAssignmentDuration = (assignment: any): string => {
  const startDate = assignment.start_on ? new Date(assignment.start_on) : null;
  const endDate = assignment.end_on ? new Date(assignment.end_on) : new Date();
  
  if (!startDate) return 'Unknown';
  
  const diffTime = endDate.getTime() - startDate.getTime();
  const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
  
  if (diffDays < 30) return `${diffDays} days`;
  if (diffDays < 365) return `${Math.floor(diffDays / 30)} months`;
  return `${Math.floor(diffDays / 365)} years`;
};

const getStaffName = (assignment: any): string => {
  if (!assignment.staff_info) return 'Unknown Staff';
  
  const { first_name, last_name, business_name } = assignment.staff_info;
  
  if (business_name) return business_name;
  if (first_name || last_name) {
    return `${first_name || ''} ${last_name || ''}`.trim();
  }
  return 'Unknown Staff';
};

const getStaffContact = (assignment: any): string => {
  if (!assignment.staff_info) return 'No contact info';
  
  const email = assignment.staff_info.email;
  const phone = assignment.staff_info.phone;
  
  if (email && phone) return `${email} • ${phone}`;
  if (email) return email;
  if (phone) return phone;
  return 'No contact details';
};

const formatDate = (dateString: string): string => {
  if (!dateString) return '';
  return new Date(dateString).toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
  });
};

const navigateToStaff = (staffId: string) => {
  router.push(`/admin/staff/${staffId}`);
  closeModal();
};

const closeModal = () => {
  emit('close');
};

// Computed
const filteredAssignments = computed(() => {
  if (activeFilter.value === 'all') {
    return assignments.value;
  }
  
  const today = new Date().toISOString().split('T')[0];
  
  return assignments.value.filter(assignment => {
    const status = getAssignmentStatus(assignment);
    return status.toLowerCase() === activeFilter.value;
  });
});

const getTotalAssignments = (): number => {
  return assignments.value.length;
};

const getActiveAssignments = (): number => {
  const today = new Date().toISOString().split('T')[0];
  return assignments.value.filter(assignment => {
    const startDate = assignment.start_on;
    const endDate = assignment.end_on;
    
    const startValid = !startDate || startDate <= today;
    const endValid = !endDate || endDate >= today;
    
    return startValid && endValid;
  }).length;
};

const getFutureAssignments = (): number => {
  const today = new Date().toISOString().split('T')[0];
  return assignments.value.filter(assignment => {
    return assignment.start_on && assignment.start_on > today;
  }).length;
};

const getExpiredAssignments = (): number => {
  const today = new Date().toISOString().split('T')[0];
  return assignments.value.filter(assignment => {
    return assignment.end_on && assignment.end_on < today;
  }).length;
};

const getEmptyStateMessage = (): string => {
  const messages: Record<string, string> = {
    all: 'This role has not been assigned to any staff members yet.',
    active: 'No staff members currently have this role assigned.',
    future: 'No future assignments scheduled for this role.',
    expired: 'No expired assignments found for this role.',
  };
  return messages[activeFilter.value] || '';
};

onMounted(() => {
  fetchAssignments();
  
  // Handle escape key
  const handleEscape = (e: KeyboardEvent) => {
    if (e.key === 'Escape') {
      closeModal();
    }
  };
  
  document.addEventListener('keydown', handleEscape);
  
  return () => {
    document.removeEventListener('keydown', handleEscape);
  };
});
</script>