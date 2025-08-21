<template>
  <div>
    <!-- Recent Trips Card -->
    <div class="card mb-6 mb-xl-9">
      <!--begin::Card header-->
      <div class="card-header border-0">
        <div class="card-title">
          <h3 class="fw-bold m-0">Recent Trips</h3>
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
                <th class="ps-0 min-w-200px">Trip</th>
                <th class="min-w-100px">Date</th>
                <th class="min-w-100px">Route</th>
                <th class="min-w-100px">Status</th>
                <th class="min-w-100px text-end">Amount</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="trip in recentTrips" :key="trip.id">
                <td class="ps-0">
                  <div class="d-flex align-items-center">
                    <div class="symbol symbol-45px me-2">
                      <div class="symbol-label bg-light-primary">
                        <KTIcon icon-name="airplane" icon-class="fs-3 text-primary" />
                      </div>
                    </div>
                    <div class="d-flex flex-column">
                      <a href="#" class="text-gray-800 text-hover-primary fw-bold fs-6">
                        {{ trip.trip_number }}
                      </a>
                      <span class="text-gray-600 fw-semibold fs-7">{{ trip.type }}</span>
                    </div>
                  </div>
                </td>
                <td>
                  <span class="text-gray-800 fw-bold fs-6">{{ formatDate(trip.created_on) }}</span>
                </td>
                <td>
                  <span class="text-gray-800 fw-bold fs-6">{{ getRoute(trip) }}</span>
                </td>
                <td>
                  <span :class="`badge badge-light-${getStatusColor(trip.status)} fs-7`">
                    {{ trip.status }}
                  </span>
                </td>
                <td class="text-end">
                  <span class="text-gray-800 fw-bold fs-6">${{ trip.total_amount || '0' }}</span>
                </td>
              </tr>
              <tr v-if="recentTrips.length === 0">
                <td colspan="5" class="text-center text-muted py-6">
                  No trips found for this contact
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
      <!--end::Card body-->
    </div>
    <!--end::Recent Trips Card-->

    <!-- Payment Summary Card -->
    <div class="card mb-6 mb-xl-9">
      <!--begin::Card header-->
      <div class="card-header border-0">
        <div class="card-title">
          <h3 class="fw-bold m-0">Payment Summary</h3>
        </div>
      </div>
      <!--end::Card header-->

      <!--begin::Card body-->
      <div class="card-body pt-2">
        <div class="row g-6">
          <!--begin::Col-->
          <div class="col-sm-6 col-xl-3">
            <div class="border border-dashed border-gray-300 text-center min-w-125px rounded py-4 px-3">
              <span class="fs-6 fw-semibold text-gray-700 d-block mb-2">Total Paid</span>
              <div class="fs-2 fw-bold text-gray-800">${{ getTotalPaid() }}</div>
            </div>
          </div>
          <!--end::Col-->

          <!--begin::Col-->
          <div class="col-sm-6 col-xl-3">
            <div class="border border-dashed border-gray-300 text-center min-w-125px rounded py-4 px-3">
              <span class="fs-6 fw-semibold text-gray-700 d-block mb-2">Outstanding</span>
              <div class="fs-2 fw-bold text-danger">${{ getOutstanding() }}</div>
            </div>
          </div>
          <!--end::Col-->

          <!--begin::Col-->
          <div class="col-sm-6 col-xl-3">
            <div class="border border-dashed border-gray-300 text-center min-w-125px rounded py-4 px-3">
              <span class="fs-6 fw-semibold text-gray-700 d-block mb-2">Last Payment</span>
              <div class="fs-2 fw-bold text-gray-800">${{ getLastPayment() }}</div>
            </div>
          </div>
          <!--end::Col-->

          <!--begin::Col-->
          <div class="col-sm-6 col-xl-3">
            <div class="border border-dashed border-gray-300 text-center min-w-125px rounded py-4 px-3">
              <span class="fs-6 fw-semibold text-gray-700 d-block mb-2">Avg Trip Cost</span>
              <div class="fs-2 fw-bold text-gray-800">${{ getAvgTripCost() }}</div>
            </div>
          </div>
          <!--end::Col-->
        </div>
      </div>
      <!--end::Card body-->
    </div>
    <!--end::Payment Summary Card-->

    <!-- Contact Information Card -->
    <div class="card mb-6 mb-xl-9">
      <!--begin::Card header-->
      <div class="card-header border-0">
        <div class="card-title">
          <h3 class="fw-bold m-0">Contact Information</h3>
        </div>
        <div class="card-toolbar">
          <button class="btn btn-sm btn-light-primary">Edit</button>
        </div>
      </div>
      <!--end::Card header-->

      <!--begin::Card body-->
      <div class="card-body pt-2">
        <div class="row g-6">
          <!--begin::Col-->
          <div class="col-md-6">
            <div class="d-flex flex-column">
              <!--begin::Contact Details-->
              <div class="mb-6">
                <label class="fw-semibold fs-6 mb-2">Primary Contact</label>
                <div class="d-flex align-items-center">
                  <KTIcon icon-name="phone" icon-class="fs-3 text-primary me-3" />
                  <div>
                    <div class="fw-bold text-gray-800">{{ contact?.phone || 'Not provided' }}</div>
                    <div class="text-gray-600 fs-7">Mobile</div>
                  </div>
                </div>
              </div>

              <div class="mb-6">
                <label class="fw-semibold fs-6 mb-2">Email Address</label>
                <div class="d-flex align-items-center">
                  <KTIcon icon-name="sms" icon-class="fs-3 text-success me-3" />
                  <div>
                    <div class="fw-bold text-gray-800">{{ contact?.email || 'Not provided' }}</div>
                    <div class="text-gray-600 fs-7">Primary</div>
                  </div>
                </div>
              </div>

              <div class="mb-6">
                <label class="fw-semibold fs-6 mb-2">Emergency Contact</label>
                <div class="d-flex align-items-center">
                  <KTIcon icon-name="add-item" icon-class="fs-3 text-warning me-3" />
                  <div>
                    <div class="fw-bold text-gray-800">{{ contact?.emergency_contact || 'Not provided' }}</div>
                    <div class="text-gray-600 fs-7">Emergency</div>
                  </div>
                </div>
              </div>
              <!--end::Contact Details-->
            </div>
          </div>
          <!--end::Col-->

          <!--begin::Col-->
          <div class="col-md-6">
            <div class="d-flex flex-column">
              <!--begin::Address Details-->
              <div class="mb-6">
                <label class="fw-semibold fs-6 mb-2">Address</label>
                <div class="d-flex align-items-start">
                  <KTIcon icon-name="geolocation" icon-class="fs-3 text-info me-3 mt-1" />
                  <div>
                    <div class="fw-bold text-gray-800">{{ getFormattedAddress() }}</div>
                    <div class="text-gray-600 fs-7">Primary Address</div>
                  </div>
                </div>
              </div>

              <div class="mb-6" v-if="contact?.date_of_birth">
                <label class="fw-semibold fs-6 mb-2">Date of Birth</label>
                <div class="d-flex align-items-center">
                  <KTIcon icon-name="calendar" icon-class="fs-3 text-danger me-3" />
                  <div>
                    <div class="fw-bold text-gray-800">{{ formatDate(contact?.date_of_birth) }}</div>
                    <div class="text-gray-600 fs-7">Age: {{ calculateAge() }}</div>
                  </div>
                </div>
              </div>

              <div class="mb-6">
                <label class="fw-semibold fs-6 mb-2">Member Since</label>
                <div class="d-flex align-items-center">
                  <KTIcon icon-name="time" icon-class="fs-3 text-secondary me-3" />
                  <div>
                    <div class="fw-bold text-gray-800">{{ formatDate(contact?.created_on) }}</div>
                    <div class="text-gray-600 fs-7">{{ getMembershipDuration() }}</div>
                  </div>
                </div>
              </div>
              <!--end::Address Details-->
            </div>
          </div>
          <!--end::Col-->
        </div>
      </div>
      <!--end::Card body-->
    </div>
    <!--end::Contact Information Card-->
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from "vue";
import ApiService from "@/core/services/ApiService";

interface Props {
  contact: any;
  loading: boolean;
}

const props = defineProps<Props>();

const recentTrips = ref<any[]>([]);

const fetchRecentTrips = async () => {
  if (!props.contact?.id) return;
  
  try {
    const response = await ApiService.get(`/trips/?${getContactFilterParam()}=${props.contact.id}&limit=5`);
    recentTrips.value = response.data.results || response.data || [];
  } catch (error) {
    console.error('Error fetching recent trips:', error);
  }
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

const getRoute = (trip: any): string => {
  if (trip.departure_airport && trip.arrival_airport) {
    return `${trip.departure_airport} → ${trip.arrival_airport}`;
  }
  return 'TBD';
};

const getStatusColor = (status: string): string => {
  switch (status?.toLowerCase()) {
    case 'completed': return 'success';
    case 'active': case 'in_progress': return 'primary';
    case 'cancelled': return 'danger';
    case 'pending': return 'warning';
    default: return 'secondary';
  }
};

const getTotalPaid = (): string => {
  return (props.contact?.total_paid || 0).toLocaleString();
};

const getOutstanding = (): string => {
  return (props.contact?.outstanding_balance || 0).toLocaleString();
};

const getLastPayment = (): string => {
  return (props.contact?.last_payment_amount || 0).toLocaleString();
};

const getAvgTripCost = (): string => {
  const totalSpent = props.contact?.total_spent || 0;
  const totalTrips = props.contact?.total_trips || 1;
  return (totalSpent / totalTrips).toLocaleString();
};

const getFormattedAddress = (): string => {
  if (!props.contact) return 'No address provided';
  
  const parts = [
    props.contact.address,
    props.contact.city,
    props.contact.state,
    props.contact.zip_code,
    props.contact.country
  ].filter(Boolean);
  
  return parts.length > 0 ? parts.join(', ') : 'No address provided';
};

const calculateAge = (): string => {
  if (!props.contact?.date_of_birth) return 'Unknown';
  
  const today = new Date();
  const birthDate = new Date(props.contact.date_of_birth);
  let age = today.getFullYear() - birthDate.getFullYear();
  const monthDiff = today.getMonth() - birthDate.getMonth();
  
  if (monthDiff < 0 || (monthDiff === 0 && today.getDate() < birthDate.getDate())) {
    age--;
  }
  
  return `${age} years`;
};

const getMembershipDuration = (): string => {
  if (!props.contact?.created_on) return 'Unknown';
  
  const created = new Date(props.contact.created_on);
  const now = new Date();
  const diffTime = Math.abs(now.getTime() - created.getTime());
  const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
  
  if (diffDays < 30) {
    return `${diffDays} days`;
  } else if (diffDays < 365) {
    const months = Math.floor(diffDays / 30);
    return `${months} months`;
  } else {
    const years = Math.floor(diffDays / 365);
    return `${years} years`;
  }
};

onMounted(() => {
  if (props.contact?.id) {
    fetchRecentTrips();
  }
});
</script>