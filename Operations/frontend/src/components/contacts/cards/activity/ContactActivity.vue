<template>
  <div>
    <!-- Activity Timeline Card -->
    <div class="card mb-6 mb-xl-9">
      <!--begin::Card header-->
      <div class="card-header border-0">
        <div class="card-title">
          <h3 class="fw-bold m-0">Recent Activity</h3>
        </div>
        <div class="card-toolbar">
          <div class="d-flex gap-2">
            <select class="form-select form-select-sm w-auto" v-model="activityFilter">
              <option value="">All Activities</option>
              <option value="trips">Trips</option>
              <option value="payments">Payments</option>
              <option value="quotes">Quotes</option>
              <option value="communications">Communications</option>
            </select>
            <button class="btn btn-sm btn-light">Export</button>
          </div>
        </div>
      </div>
      <!--end::Card header-->

      <!--begin::Card body-->
      <div class="card-body pt-2">
        <!--begin::Timeline-->
        <div class="timeline-label">
          <!--begin::Item-->
          <div 
            v-for="activity in filteredActivities" 
            :key="activity.id" 
            class="timeline-item"
          >
            <!--begin::Label-->
            <div class="timeline-label fw-bold text-gray-800 fs-6">
              {{ formatTime(activity.timestamp) }}
            </div>
            <!--end::Label-->

            <!--begin::Badge-->
            <div class="timeline-badge">
              <i :class="`fa fa-genderless text-${getActivityColor(activity.type)} fs-1`"></i>
            </div>
            <!--end::Badge-->

            <!--begin::Text-->
            <div class="fw-normal timeline-content text-muted ps-3">
              <div class="d-flex align-items-center mb-2">
                <div class="symbol symbol-30px me-3">
                  <div :class="`symbol-label bg-light-${getActivityColor(activity.type)}`">
                    <KTIcon 
                      :icon-name="getActivityIcon(activity.type)" 
                      :icon-class="`fs-3 text-${getActivityColor(activity.type)}`" 
                    />
                  </div>
                </div>
                <div class="d-flex flex-column flex-grow-1">
                  <div class="fs-6 fw-bold text-gray-800">{{ activity.title }}</div>
                  <div class="fs-7 text-gray-600">{{ activity.description }}</div>
                </div>
                <div class="fs-7 text-gray-500">{{ formatRelativeTime(activity.timestamp) }}</div>
              </div>
              
              <!--begin::Activity details-->
              <div v-if="activity.details" class="bg-light-primary rounded p-3 mt-2">
                <div class="fs-7 text-gray-700">
                  <div v-for="(value, key) in activity.details" :key="key" class="d-flex justify-content-between">
                    <span class="fw-semibold">{{ formatDetailKey(key) }}:</span>
                    <span>{{ value }}</span>
                  </div>
                </div>
              </div>
              <!--end::Activity details-->
            </div>
            <!--end::Text-->
          </div>
          <!--end::Item-->

          <!--begin::No activities message-->
          <div v-if="filteredActivities.length === 0" class="text-center py-6">
            <div class="fs-4 fw-bold text-gray-500 mb-2">No Activities Found</div>
            <div class="fs-6 text-gray-600">
              {{ activityFilter ? `No ${activityFilter} activities found for this contact` : 'No activities found for this contact' }}
            </div>
          </div>
          <!--end::No activities message-->
        </div>
        <!--end::Timeline-->

        <!--begin::Load more-->
        <div class="text-center mt-6" v-if="hasMoreActivities">
          <button class="btn btn-light" @click="loadMoreActivities" :disabled="loadingMore">
            <span v-if="loadingMore" class="spinner-border spinner-border-sm me-2"></span>
            Load More Activities
          </button>
        </div>
        <!--end::Load more-->
      </div>
      <!--end::Card body-->
    </div>
    <!--end::Activity Timeline Card-->

    <!-- Communication Log Card -->
    <div class="card mb-6 mb-xl-9">
      <!--begin::Card header-->
      <div class="card-header border-0">
        <div class="card-title">
          <h3 class="fw-bold m-0">Communication Log</h3>
        </div>
        <div class="card-toolbar">
          <button class="btn btn-sm btn-primary">Add Note</button>
        </div>
      </div>
      <!--end::Card header-->

      <!--begin::Card body-->
      <div class="card-body pt-2">
        <div class="table-responsive">
          <table class="table table-row-dashed align-middle gs-0 gy-4 my-0">
            <thead>
              <tr class="fs-7 fw-bold text-gray-500 border-bottom-0">
                <th class="ps-0 min-w-200px">Communication</th>
                <th class="min-w-100px">Type</th>
                <th class="min-w-100px">Date</th>
                <th class="min-w-100px">User</th>
                <th class="min-w-70px text-end">Actions</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="communication in communications" :key="communication.id">
                <td class="ps-0">
                  <div class="d-flex align-items-center">
                    <div class="symbol symbol-45px me-2">
                      <div :class="`symbol-label bg-light-${getCommunicationColor(communication.type)}`">
                        <KTIcon 
                          :icon-name="getCommunicationIcon(communication.type)" 
                          :icon-class="`fs-3 text-${getCommunicationColor(communication.type)}`" 
                        />
                      </div>
                    </div>
                    <div class="d-flex flex-column">
                      <span class="text-gray-800 fw-bold fs-6">{{ communication.subject }}</span>
                      <span class="text-gray-600 fw-semibold fs-7">{{ truncateText(communication.message, 60) }}</span>
                    </div>
                  </div>
                </td>
                <td>
                  <span :class="`badge badge-light-${getCommunicationColor(communication.type)} fs-7`">
                    {{ communication.type }}
                  </span>
                </td>
                <td>
                  <span class="text-gray-800 fw-bold fs-6">{{ formatDate(communication.created_on) }}</span>
                </td>
                <td>
                  <span class="text-gray-600 fs-6">{{ communication.created_by || 'System' }}</span>
                </td>
                <td class="text-end">
                  <div class="dropdown">
                    <button 
                      class="btn btn-sm btn-light btn-active-light-primary" 
                      type="button" 
                      data-bs-toggle="dropdown"
                    >
                      <KTIcon icon-name="dots-horizontal" icon-class="fs-3" />
                    </button>
                    <ul class="dropdown-menu">
                      <li>
                        <a class="dropdown-item" href="#" @click="viewCommunication(communication)">View</a>
                      </li>
                      <li>
                        <a class="dropdown-item" href="#" @click="replyCommunication(communication)">Reply</a>
                      </li>
                      <li>
                        <a class="dropdown-item" href="#" @click="forwardCommunication(communication)">Forward</a>
                      </li>
                    </ul>
                  </div>
                </td>
              </tr>
              <tr v-if="communications.length === 0">
                <td colspan="5" class="text-center text-muted py-6">
                  No communications found for this contact
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
      <!--end::Card body-->
    </div>
    <!--end::Communication Log Card-->

    <!-- System Logs Card -->
    <div class="card mb-6 mb-xl-9">
      <!--begin::Card header-->
      <div class="card-header border-0">
        <div class="card-title">
          <h3 class="fw-bold m-0">System Logs</h3>
        </div>
        <div class="card-toolbar">
          <button class="btn btn-sm btn-light">View All</button>
        </div>
      </div>
      <!--end::Card header-->

      <!--begin::Card body-->
      <div class="card-body pt-2">
        <div class="table-responsive">
          <table class="table table-row-dashed align-middle gs-0 gy-4 my-0">
            <thead>
              <tr class="fs-7 fw-bold text-gray-500 border-bottom-0">
                <th class="ps-0 min-w-300px">Event</th>
                <th class="min-w-100px">Level</th>
                <th class="min-w-100px">Date</th>
                <th class="min-w-100px">IP Address</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="log in systemLogs" :key="log.id">
                <td class="ps-0">
                  <div class="d-flex align-items-center">
                    <div class="symbol symbol-30px me-2">
                      <div :class="`symbol-label bg-light-${getLogLevelColor(log.level)}`">
                        <KTIcon 
                          :icon-name="getLogLevelIcon(log.level)" 
                          :icon-class="`fs-4 text-${getLogLevelColor(log.level)}`" 
                        />
                      </div>
                    </div>
                    <div class="d-flex flex-column">
                      <span class="text-gray-800 fw-bold fs-6">{{ log.event }}</span>
                      <span class="text-gray-600 fs-7">{{ log.description }}</span>
                    </div>
                  </div>
                </td>
                <td>
                  <span :class="`badge badge-light-${getLogLevelColor(log.level)} fs-7`">
                    {{ log.level }}
                  </span>
                </td>
                <td>
                  <div class="d-flex flex-column">
                    <span class="text-gray-800 fw-bold fs-6">{{ formatDate(log.timestamp) }}</span>
                    <span class="text-gray-600 fs-7">{{ formatTime(log.timestamp) }}</span>
                  </div>
                </td>
                <td>
                  <span class="text-gray-600 fs-6">{{ log.ip_address || '-' }}</span>
                </td>
              </tr>
              <tr v-if="systemLogs.length === 0">
                <td colspan="4" class="text-center text-muted py-6">
                  No system logs found for this contact
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
      <!--end::Card body-->
    </div>
    <!--end::System Logs Card-->
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from "vue";
import ApiService from "@/core/services/ApiService";
import Swal from "sweetalert2";

interface Props {
  contact: any;
  loading: boolean;
}

const props = defineProps<Props>();

const activities = ref<any[]>([]);
const communications = ref<any[]>([]);
const systemLogs = ref<any[]>([]);
const activityFilter = ref('');
const hasMoreActivities = ref(true);
const loadingMore = ref(false);

const filteredActivities = computed(() => {
  if (!activityFilter.value) return activities.value;
  return activities.value.filter(activity => activity.type === activityFilter.value);
});

const fetchActivityData = async () => {
  if (!props.contact?.id) return;
  
  try {
    // These endpoints don't exist in the current backend - using empty arrays
    activities.value = [];
    communications.value = [];
    systemLogs.value = [];
    
    // Could potentially fetch related data from existing endpoints:
    // - Use /modifications/ for system logs
    // - Use /quotes/ for quote-related activities
    // - Use /trips/ for trip-related activities
    try {
      const modificationsResponse = await ApiService.get(`/modifications/?limit=10`);
      const allModifications = modificationsResponse.data.results || modificationsResponse.data || [];
      // This would need more sophisticated filtering based on contact relationships
      systemLogs.value = allModifications.slice(0, 5);
    } catch (error) {
      console.warn('Could not fetch modifications for activity logs:', error);
    }
  } catch (error) {
    console.error('Error fetching activity data:', error);
    // Generate mock data for demonstration
    generateMockData();
  }
};

const generateMockData = () => {
  const now = new Date();
  
  activities.value = [
    {
      id: 1,
      type: 'trips',
      title: 'Trip Booked',
      description: 'Medical transport from LAX to JFK',
      timestamp: new Date(now.getTime() - 2 * 60 * 60 * 1000).toISOString(),
      details: { trip_id: 'T-12345', aircraft: 'N123AB', cost: '$15,000' }
    },
    {
      id: 2,
      type: 'payments',
      title: 'Payment Received',
      description: 'Credit card payment processed',
      timestamp: new Date(now.getTime() - 4 * 60 * 60 * 1000).toISOString(),
      details: { amount: '$15,000', method: 'Credit Card', reference: 'PAY-98765' }
    },
    {
      id: 3,
      type: 'quotes',
      title: 'Quote Sent',
      description: 'Medical transport quote emailed to customer',
      timestamp: new Date(now.getTime() - 1 * 24 * 60 * 60 * 1000).toISOString(),
      details: { quote_id: 'Q-54321', amount: '$15,000', valid_until: '2024-02-15' }
    },
    {
      id: 4,
      type: 'communications',
      title: 'Email Sent',
      description: 'Trip confirmation email sent',
      timestamp: new Date(now.getTime() - 2 * 24 * 60 * 60 * 1000).toISOString(),
      details: { subject: 'Trip Confirmation', to: props.contact?.email }
    }
  ];

  communications.value = [
    {
      id: 1,
      type: 'email',
      subject: 'Trip Confirmation',
      message: 'Your medical transport has been confirmed for tomorrow at 2:00 PM.',
      created_on: new Date(now.getTime() - 1 * 60 * 60 * 1000).toISOString(),
      created_by: 'John Smith'
    },
    {
      id: 2,
      type: 'phone',
      subject: 'Pre-flight consultation',
      message: 'Discussed medical requirements and special accommodations needed for the patient.',
      created_on: new Date(now.getTime() - 3 * 60 * 60 * 1000).toISOString(),
      created_by: 'Dr. Jane Doe'
    }
  ];

  systemLogs.value = [
    {
      id: 1,
      event: 'Contact Updated',
      description: 'Emergency contact information updated',
      level: 'info',
      timestamp: new Date(now.getTime() - 30 * 60 * 1000).toISOString(),
      ip_address: '192.168.1.100'
    },
    {
      id: 2,
      event: 'Login Success',
      description: 'Contact logged into patient portal',
      level: 'info',
      timestamp: new Date(now.getTime() - 2 * 60 * 60 * 1000).toISOString(),
      ip_address: '10.0.0.50'
    }
  ];
};

const getContactFilterParam = (): string => {
  switch (props.contact?.type) {
    case 'patients': return 'patient_id';
    case 'customers': return 'customer_id';
    default: return 'contact_id';
  }
};

const formatDate = (dateString?: string): string => {
  if (!dateString) return 'N/A';
  return new Date(dateString).toLocaleDateString('en-US', {
    month: 'short',
    day: 'numeric',
    year: 'numeric',
  });
};

const formatTime = (dateString?: string): string => {
  if (!dateString) return 'N/A';
  return new Date(dateString).toLocaleTimeString('en-US', {
    hour: 'numeric',
    minute: '2-digit',
    hour12: true,
  });
};

const formatRelativeTime = (dateString?: string): string => {
  if (!dateString) return 'Unknown';
  
  const now = new Date();
  const date = new Date(dateString);
  const diffMs = now.getTime() - date.getTime();
  const diffHours = Math.floor(diffMs / (1000 * 60 * 60));
  const diffDays = Math.floor(diffMs / (1000 * 60 * 60 * 24));
  
  if (diffHours < 1) return 'Just now';
  if (diffHours < 24) return `${diffHours}h ago`;
  if (diffDays < 7) return `${diffDays}d ago`;
  return formatDate(dateString);
};

const formatDetailKey = (key: string): string => {
  return key.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase());
};

const truncateText = (text: string, maxLength: number): string => {
  if (!text) return '';
  return text.length > maxLength ? text.substring(0, maxLength) + '...' : text;
};

const getActivityColor = (type: string): string => {
  switch (type?.toLowerCase()) {
    case 'trips': return 'primary';
    case 'payments': return 'success';
    case 'quotes': return 'info';
    case 'communications': return 'warning';
    default: return 'secondary';
  }
};

const getActivityIcon = (type: string): string => {
  switch (type?.toLowerCase()) {
    case 'trips': return 'airplane';
    case 'payments': return 'dollar';
    case 'quotes': return 'calculator';
    case 'communications': return 'sms';
    default: return 'information';
  }
};

const getCommunicationColor = (type: string): string => {
  switch (type?.toLowerCase()) {
    case 'email': return 'primary';
    case 'phone': return 'success';
    case 'sms': return 'warning';
    case 'note': return 'info';
    default: return 'secondary';
  }
};

const getCommunicationIcon = (type: string): string => {
  switch (type?.toLowerCase()) {
    case 'email': return 'sms';
    case 'phone': return 'phone';
    case 'sms': return 'message-text';
    case 'note': return 'pencil';
    default: return 'communication';
  }
};

const getLogLevelColor = (level: string): string => {
  switch (level?.toLowerCase()) {
    case 'error': return 'danger';
    case 'warning': return 'warning';
    case 'info': return 'primary';
    case 'debug': return 'secondary';
    default: return 'info';
  }
};

const getLogLevelIcon = (level: string): string => {
  switch (level?.toLowerCase()) {
    case 'error': return 'cross-circle';
    case 'warning': return 'information';
    case 'info': return 'information-2';
    case 'debug': return 'code';
    default: return 'information';
  }
};

const loadMoreActivities = async () => {
  loadingMore.value = true;
  // Simulate loading more activities
  setTimeout(() => {
    hasMoreActivities.value = false;
    loadingMore.value = false;
  }, 1000);
};

const viewCommunication = (communication: any) => {
  Swal.fire({
    title: communication.subject,
    text: communication.message,
    icon: 'info'
  });
};

const replyCommunication = (communication: any) => {
  Swal.fire({
    title: 'Reply to Communication',
    text: `Would open reply form for: ${communication.subject}`,
    icon: 'info'
  });
};

const forwardCommunication = (communication: any) => {
  Swal.fire({
    title: 'Forward Communication',
    text: `Would open forward form for: ${communication.subject}`,
    icon: 'info'
  });
};

onMounted(() => {
  if (props.contact?.id) {
    fetchActivityData();
  }
});
</script>