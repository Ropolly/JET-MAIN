<template>
  <!--begin::Financials Content-->
  <div>
    <!--begin::Header-->
    <div class="d-flex justify-content-between align-items-center mb-6">
      <!--begin::Title-->
      <div>
        <h2 class="fw-bold">Financial Overview</h2>
      </div>
      <!--end::Title-->

      <!--begin::Toolbar-->
      <div v-if="trip?.quote">
        <button class="btn btn-light-primary btn-sm">
          <KTIcon icon-name="dollar" icon-class="fs-6" />
          Add Payment
        </button>
      </div>
      <!--end::Toolbar-->
    </div>
    <!--end::Header-->

    <!--begin::Content-->
    <div>
      <!--begin::Loading-->
      <div v-if="loading" class="d-flex justify-content-center py-5">
        <div class="spinner-border" role="status">
          <span class="visually-hidden">Loading...</span>
        </div>
      </div>
      <!--end::Loading-->

      <!--begin::Financial Summary-->
      <div v-if="!loading && trip?.quote" class="mb-8">
        <div class="row g-6">
          <!--begin::Total Cost-->
          <div class="col-md-3">
            <div class="card text-center py-4 px-3">
              <div class="d-flex justify-content-center mb-3">
                <KTIcon icon-name="dollar" icon-class="fs-2x text-primary" />
              </div>
              <div class="fs-6 fw-semibold text-gray-700 mb-1">Total Cost</div>
              <div class="fs-2 fw-bold text-gray-900">${{ getTotalCost() }}</div>
            </div>
          </div>
          <!--end::Total Cost-->
          <!--begin::Paid Amount-->
          <div class="col-md-3">
            <div class="card text-center py-4 px-3">
              <div class="d-flex justify-content-center mb-3">
                <KTIcon icon-name="check-circle" icon-class="fs-2x text-success" />
              </div>
              <div class="fs-6 fw-semibold text-gray-700 mb-1">Paid</div>
              <div class="fs-2 fw-bold text-success">${{ getPaidAmount() }}</div>
            </div>
          </div>
          <!--end::Paid Amount-->
          <!--begin::Outstanding-->
          <div class="col-md-3">
            <div class="card text-center py-4 px-3">
              <div class="d-flex justify-content-center mb-3">
                <KTIcon icon-name="time" icon-class="fs-2x text-warning" />
              </div>
              <div class="fs-6 fw-semibold text-gray-700 mb-1">Outstanding</div>
              <div class="fs-2 fw-bold text-warning">${{ getOutstandingAmount() }}</div>
            </div>
          </div>
          <!--end::Outstanding-->
          <!--begin::Payment Status-->
          <div class="col-md-3">
            <div class="card text-center py-4 px-3">
              <div class="d-flex justify-content-center mb-3">
                <KTIcon :icon-name="getPaymentStatusIcon()" :icon-class="`fs-2x ${getPaymentStatusColor()}`" />
              </div>
              <div class="fs-6 fw-semibold text-gray-700 mb-1">Status</div>
              <div class="fs-4 fw-bold">{{ getPaymentStatus() }}</div>
            </div>
          </div>
          <!--end::Payment Status-->
        </div>
      </div>
      <!--end::Financial Summary-->

      <!--begin::Quote Details Card-->
      <div v-if="!loading && trip?.quote" class="card mb-8">
        <div class="card-body">
          <!--begin::Header-->
          <div class="d-flex justify-content-between align-items-center mb-8">
            <div class="fw-bold fs-3 text-gray-800">
              Quote #{{ trip.quote.id?.slice(0, 8) }}
            </div>
            <select
              v-if="trip.quote.status"
              :value="trip.quote.status"
              @change="updateQuoteStatus(($event.target as HTMLSelectElement).value)"
              class="form-select form-select-sm"
              :class="`text-${getQuoteStatusColor()}`"
              style="max-width: 150px;"
            >
              <option value="pending">Pending</option>
              <option value="active">Active</option>
              <option value="completed">Completed</option>
              <option value="lost">Lost</option>
            </select>
          </div>
          <!--end::Header-->

          <!--begin::Quote Details Row-->
          <div class="row g-5 mb-11">
            <!--begin::Issue Date-->
            <div class="col-sm-6">
              <div class="fw-semibold fs-7 text-gray-600 mb-1">Issue Date:</div>
              <div class="fw-bold fs-6 text-gray-800">{{ formatDate(trip.quote.created_on) }}</div>
            </div>
            <!--end::Issue Date-->

            <!--begin::Valid Until-->
            <div class="col-sm-6">
              <div class="fw-semibold fs-7 text-gray-600 mb-1">Valid Until:</div>
              <div class="fw-bold fs-6 text-gray-800 d-flex align-items-center flex-wrap">
                <span class="pe-2">{{ getValidUntilDate() }}</span>
                <span v-if="isExpiringSoon()" class="fs-7 text-warning d-flex align-items-center">
                  <span class="bullet bullet-dot bg-warning me-2"></span>
                  Expires soon
                </span>
                <span v-else-if="isExpired()" class="fs-7 text-danger d-flex align-items-center">
                  <span class="bullet bullet-dot bg-danger me-2"></span>
                  Expired
                </span>
              </div>
            </div>
            <!--end::Valid Until-->
          </div>
          <!--end::Quote Details Row-->

          <!--begin::Customer & Company Info Row-->
          <div class="row g-5 mb-12">
            <!--begin::Customer Info-->
            <div class="col-sm-6">
              <div class="fw-semibold fs-7 text-gray-600 mb-1">Quote For:</div>
              <div class="fw-bold fs-6 text-gray-800">{{ getCustomerName() }}</div>
              <div class="fw-semibold fs-7 text-gray-600">{{ getCustomerAddress() }}</div>
              <div class="fw-semibold fs-7 text-gray-600 mt-2">
                <div v-if="getCustomerEmail()">Email: {{ getCustomerEmail() }}</div>
                <div v-if="getCustomerPhone()">Phone: {{ getCustomerPhone() }}</div>
              </div>
            </div>
            <!--end::Customer Info-->

            <!--begin::Company Info-->
            <div class="col-sm-6">
              <div class="fw-semibold fs-7 text-gray-600 mb-1">Issued By:</div>
              <div class="fw-bold fs-6 text-gray-800">JET ICU Medical Transport</div>
              <div class="fw-semibold fs-7 text-gray-600">
                1511 N Westshore Blvd #650<br>
                Tampa, FL 33607<br>
                Phone: (352) 796-2540<br>
                Email: info@jeticu.com
              </div>
            </div>
            <!--end::Company Info-->
          </div>
          <!--end::Customer & Company Info Row-->

          <!--begin::Line Items Table-->
          <div class="table-responsive border-bottom mb-9">
            <table class="table mb-3">
              <thead>
                <tr class="border-bottom fs-6 fw-bold text-muted">
                  <th class="min-w-175px pb-2 text-start">Item</th>
                  <th class="min-w-200px pb-2 text-start">Description</th>
                  <th class="min-w-70px text-end pb-2">Price</th>
                </tr>
              </thead>
              <tbody>
                <tr class="fw-bold text-gray-700 fs-5">
                  <td class="pt-6 text-start">
                    <div class="d-flex align-items-center">
                      <KTIcon icon-name="airplane" icon-class="fs-2 me-2 text-primary" />
                      Flight Cost
                    </div>
                  </td>
                  <td class="pt-6 text-start">
                    <div class="fs-7 fw-normal text-gray-600">{{ getRouteDescriptionSimple() }}</div>
                  </td>
                  <td class="pt-6 text-end">${{ formatAmount(trip.quote.quoted_amount) }}</td>
                </tr>
              </tbody>
            </table>
          </div>
          <!--end::Line Items Table-->

          <!--begin::Route Info-->
          <div v-if="getRouteDescription()" class="mb-5">
            <div class="fw-semibold fs-7 text-gray-600 mb-1">Route:</div>
            <div class="fw-bold fs-6 text-gray-800">{{ getRouteDescription() }}</div>
          </div>
          <!--end::Route Info-->

          <!--begin::Notes-->
          <div class="d-flex flex-stack">
            <div class="fw-semibold pe-10 text-gray-600 fs-7">
              <div v-if="trip?.quote?.aircraft_type">Aircraft Type: {{ trip.quote.aircraft_type }}</div>
              <div v-if="trip?.quote?.medical_team">Medical Team: {{ trip.quote.medical_team }}</div>
              <div v-if="trip?.quote?.estimated_flight_time">Estimated Flight Time: {{ formatDuration(trip.quote.estimated_flight_time) }}</div>
            </div>
            <div class="text-end">
              <div class="fs-5 fw-bold text-gray-800">Quoted Amount</div>
              <div class="fs-3 fw-bolder text-primary">${{ getTotalCost() }}</div>
            </div>
          </div>
          <!--end::Notes-->
        </div>
      </div>
      <!--end::Quote Details Card-->

      <!--begin::Payment History-->
      <div v-if="!loading && trip?.quote" class="mb-8">
        <h3 class="fw-bold text-gray-900 mb-5">
          <KTIcon icon-name="calendar" icon-class="fs-3 text-primary me-2" />
          Payment History
        </h3>

        <!--begin::Payments List-->
        <div v-if="hasPayments()" class="card border border-dashed border-gray-300">
          <div class="card-body">
            <div class="table-responsive">
              <table class="table table-row-bordered">
                <thead>
                  <tr class="fw-bold fs-6 text-gray-800 border-bottom-2 border-gray-200">
                    <th>Date</th>
                    <th>Payment Method</th>
                    <th>Reference</th>
                    <th class="text-end">Amount</th>
                    <th>Status</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="(payment, index) in getPayments()" :key="payment.id || index">
                    <td class="text-gray-800">{{ formatDate(payment.date) }}</td>
                    <td class="text-gray-800">{{ payment.method || 'Credit Card' }}</td>
                    <td class="text-gray-600">{{ payment.reference || 'N/A' }}</td>
                    <td class="text-end fw-bold text-gray-900">${{ formatAmount(payment.amount) }}</td>
                    <td>
                      <span :class="`badge badge-light-${getPaymentStatusBadgeColor(payment.status)}`">
                        {{ payment.status || 'Completed' }}
                      </span>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>
        <!--end::Payments List-->

        <!--begin::No Payments-->
        <div v-else class="alert alert-light-info">
          <div class="d-flex align-items-center">
            <KTIcon icon-name="information" icon-class="fs-2 text-info me-3" />
            <div>
              <h5 class="text-info mb-1">No Payments Recorded</h5>
              <span class="text-gray-700">No payments have been recorded for this trip yet.</span>
            </div>
          </div>
        </div>
        <!--end::No Payments-->
      </div>
      <!--end::Payment History-->

      <!--begin::No Quote-->
      <div v-if="!loading && !trip?.quote" class="text-center py-10">
        <i class="fas fa-file-invoice-dollar fs-3x text-muted mb-4"></i>
        <p class="text-muted">No quote assigned to this trip yet</p>
        <button @click="showQuoteModal" type="button" class="btn btn-primary">
          <i class="fas fa-plus fs-4 me-2"></i>
          Add Quote
        </button>
      </div>
      <!--end::No Quote-->
    </div>
    <!--end::Content-->
  </div>
  <!--end::Financials Content-->

  <!--begin::Quote Modal-->
  <CreateQuoteForTripModal
    :trip="trip"
    :show="showQuoteModalRef"
    @close="onQuoteModalClose"
    @quote-created="onQuoteCreated"
  />
  <!--end::Quote Modal-->

  <!-- Lost Reason Modal -->
  <LostReasonModal
    ref="lostReasonModalRef"
    @confirmed="onLostReasonConfirmed"
  />
</template>

<script setup lang="ts">
import { computed, ref, nextTick } from 'vue';
import CreateQuoteForTripModal from '@/components/modals/CreateQuoteForTripModal.vue';
import LostReasonModal from '@/components/modals/LostReasonModal.vue';
import { showModal } from '@/core/helpers/modal';
import ApiService from '@/core/services/ApiService';
import Swal from 'sweetalert2';

interface Props {
  trip: any;
  loading: boolean;
}

const props = defineProps<Props>();
const emit = defineEmits(['trip-updated']);

// Modal state
const showQuoteModalRef = ref(false);
const lostReasonModalRef = ref<any>(null);

// Quote helper functions
const getQuoteStatusColor = (): string => {
  const status = props.trip?.quote?.status?.toLowerCase();
  switch (status) {
    case 'confirmed': case 'paid': return 'success';
    case 'pending': return 'warning';
    case 'cancelled': return 'danger';
    case 'active': return 'primary';
    default: return 'secondary';
  }
};

const hasQuoteBreakdown = (): boolean => {
  return !!(props.trip?.quote?.aircraft_type || props.trip?.quote?.medical_team || props.trip?.quote?.estimated_flight_time);
};

// Financial calculation functions
const getTotalCost = (): string => {
  if (props.trip?.quote?.quoted_amount) {
    return formatAmount(props.trip.quote.quoted_amount);
  }
  return '0.00';
};

const getPaidAmount = (): string => {
  // TODO: Calculate from actual payments
  return '0.00';
};

const getOutstandingAmount = (): string => {
  const total = parseFloat(getTotalCost().replace(/,/g, ''));
  const paid = parseFloat(getPaidAmount().replace(/,/g, ''));
  return formatAmount(total - paid);
};

const getPaymentStatus = (): string => {
  const outstanding = parseFloat(getOutstandingAmount().replace(/,/g, ''));
  if (outstanding <= 0) return 'Paid';
  if (outstanding < parseFloat(getTotalCost().replace(/,/g, ''))) return 'Partial';
  return 'Unpaid';
};

const getPaymentStatusIcon = (): string => {
  const status = getPaymentStatus();
  switch (status) {
    case 'Paid': return 'check-circle';
    case 'Partial': return 'time';
    case 'Unpaid': return 'cross-circle';
    default: return 'information';
  }
};

const getPaymentStatusColor = (): string => {
  const status = getPaymentStatus();
  switch (status) {
    case 'Paid': return 'text-success';
    case 'Partial': return 'text-warning';
    case 'Unpaid': return 'text-danger';
    default: return 'text-gray-600';
  }
};

// Cost breakdown functions
const getFlightDescription = (): string => {
  const lines = props.trip?.trip_lines || [];
  if (lines.length === 0) return 'Flight services';

  if (lines.length === 1) {
    const line = lines[0];
    const origin = line.origin_airport?.icao_code || line.origin_airport?.iata_code || 'UNK';
    const destination = line.destination_airport?.icao_code || line.destination_airport?.iata_code || 'UNK';
    return `${origin} → ${destination}`;
  }

  return `Multi-leg flight (${lines.length} segments)`;
};

const getBaseCost = (): string => {
  // This would be calculated based on flight time, distance, aircraft type
  const total = parseFloat(getTotalCost().replace(/,/g, ''));
  return formatAmount(total * 0.7); // Assume 70% is base flight cost
};

const hasMedicalTeamCost = (): boolean => {
  return !!(props.trip?.quote?.medical_team);
};

const getMedicalTeamDescription = (): string => {
  return props.trip?.quote?.medical_team || 'Medical team services';
};

const getMedicalTeamCost = (): string => {
  const total = parseFloat(getTotalCost().replace(/,/g, ''));
  return formatAmount(total * 0.2); // Assume 20% is medical team cost
};

const hasGroundTransportCost = (): boolean => {
  return !!(props.trip?.quote?.includes_grounds);
};

const getGroundTransportCost = (): string => {
  const total = parseFloat(getTotalCost().replace(/,/g, ''));
  return formatAmount(total * 0.05); // Assume 5% is ground transport cost
};

const hasAdditionalCosts = (): boolean => {
  // Check if there are any additional services
  return false; // TODO: Implement based on actual data structure
};

const getAdditionalServicesDescription = (): string => {
  return 'Additional services and fees';
};

const getAdditionalCosts = (): string => {
  const total = parseFloat(getTotalCost().replace(/,/g, ''));
  return formatAmount(total * 0.05); // Assume 5% is additional costs
};

// Payment functions
const hasPayments = (): boolean => {
  return getPayments().length > 0;
};

const getPayments = (): any[] => {
  // TODO: Return actual payments from trip data
  return props.trip?.payments || [];
};

const getPaymentStatusBadgeColor = (status: string): string => {
  switch (status?.toLowerCase()) {
    case 'completed': case 'paid': return 'success';
    case 'pending': return 'warning';
    case 'failed': case 'cancelled': return 'danger';
    default: return 'secondary';
  }
};

// Utility functions
const formatAmount = (amount: string | number): string => {
  if (!amount) return '0.00';
  const numAmount = typeof amount === 'string' ? parseFloat(amount) : amount;
  return numAmount.toLocaleString('en-US', {
    minimumFractionDigits: 2,
    maximumFractionDigits: 2
  });
};

const formatDate = (dateString?: string): string => {
  if (!dateString) return 'N/A';

  try {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric'
    });
  } catch (error) {
    return 'Invalid date';
  }
};

const formatDuration = (duration?: string | number): string => {
  if (!duration) return 'TBD';

  if (typeof duration === 'string' && duration.includes(':')) {
    const parts = duration.split(':');
    const hours = parseInt(parts[0]) || 0;
    const minutes = parseInt(parts[1]) || 0;
    return `${hours}h ${minutes}m`;
  }

  const totalMinutes = parseFloat(String(duration)) || 0;
  if (totalMinutes === 0) return 'TBD';

  const hours = Math.floor(totalMinutes / 60);
  const minutes = Math.round(totalMinutes % 60);
  return `${hours}h ${minutes}m`;
};

// Quote detail helper functions
const getRouteDescription = (): string => {
  const quote = props.trip?.quote;
  if (!quote) return '';

  const pickup = quote.pickup_airport;
  const dropoff = quote.dropoff_airport;

  if (!pickup || !dropoff) return '';

  const pickupCode = pickup.icao_code || pickup.iata_code || pickup.ident;
  const pickupName = pickup.name || '';
  const dropoffCode = dropoff.icao_code || dropoff.iata_code || dropoff.ident;
  const dropoffName = dropoff.name || '';

  return `${pickupCode} (${pickupName}) → ${dropoffCode} (${dropoffName})`;
};

const getRouteDescriptionSimple = (): string => {
  const quote = props.trip?.quote;
  if (!quote) return 'N/A';

  const pickup = quote.pickup_airport;
  const dropoff = quote.dropoff_airport;

  if (!pickup || !dropoff) return 'N/A';

  const pickupCode = pickup.icao_code || pickup.iata_code || pickup.ident || 'UNK';
  const dropoffCode = dropoff.icao_code || dropoff.iata_code || dropoff.ident || 'UNK';

  return `${pickupCode} → ${dropoffCode}`;
};

const getCustomerName = (): string => {
  // Use customer_contact if available, otherwise fall back to contact
  const contact = props.trip?.quote?.customer_contact || props.trip?.quote?.contact;
  if (!contact) return 'N/A';

  // Try decrypted fields first (get_*), then fall back to regular fields
  const business = contact.get_business_name || contact.business_name;
  if (business) {
    return business;
  }

  const firstName = contact.get_first_name || contact.first_name || '';
  const lastName = contact.get_last_name || contact.last_name || '';
  return `${firstName} ${lastName}`.trim() || 'N/A';
};

const getCustomerAddress = (): string => {
  // Use customer_contact if available, otherwise fall back to contact
  const contact = props.trip?.quote?.customer_contact || props.trip?.quote?.contact;
  if (!contact) return '';

  // Try decrypted address first, then fall back to regular address
  const address = contact.get_address || contact.address;
  if (!address) return '';

  return address;
};

const getCustomerEmail = (): string => {
  // Use customer_contact if available, otherwise fall back to contact
  const contact = props.trip?.quote?.customer_contact || props.trip?.quote?.contact;
  if (!contact) return '';

  // Try decrypted email first, then fall back to regular email
  return contact.get_email || contact.email || '';
};

const getCustomerPhone = (): string => {
  // Use customer_contact if available, otherwise fall back to contact
  const contact = props.trip?.quote?.customer_contact || props.trip?.quote?.contact;
  if (!contact) return '';

  // Try decrypted phone first, then fall back to regular phone
  return contact.get_phone || contact.phone || '';
};

const getValidUntilDate = (): string => {
  const createdOn = props.trip?.quote?.created_on;
  if (!createdOn) return 'N/A';

  try {
    const issueDate = new Date(createdOn);
    const validUntilDate = new Date(issueDate);
    validUntilDate.setDate(validUntilDate.getDate() + 10); // 10 days validity

    return validUntilDate.toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric'
    });
  } catch (error) {
    return 'N/A';
  }
};

const isExpiringSoon = (): boolean => {
  const createdOn = props.trip?.quote?.created_on;
  if (!createdOn) return false;

  try {
    const issueDate = new Date(createdOn);
    const validUntilDate = new Date(issueDate);
    validUntilDate.setDate(validUntilDate.getDate() + 10);

    const now = new Date();
    const daysUntilExpiration = Math.floor((validUntilDate.getTime() - now.getTime()) / (1000 * 60 * 60 * 24));

    return daysUntilExpiration > 0 && daysUntilExpiration <= 3;
  } catch (error) {
    return false;
  }
};

const isExpired = (): boolean => {
  const createdOn = props.trip?.quote?.created_on;
  if (!createdOn) return false;

  try {
    const issueDate = new Date(createdOn);
    const validUntilDate = new Date(issueDate);
    validUntilDate.setDate(validUntilDate.getDate() + 10);

    const now = new Date();
    return now > validUntilDate;
  } catch (error) {
    return false;
  }
};

// Modal functions
const showQuoteModal = async () => {
  showQuoteModalRef.value = true;
  // Use showModal helper to show the modal
  const modalElement = document.getElementById('kt_modal_create_quote_for_trip');
  if (modalElement) {
    showModal(modalElement);
  }
};

const onQuoteModalClose = () => {
  showQuoteModalRef.value = false;
};

const onQuoteCreated = (quote: any) => {
  console.log('Quote created and connected to trip:', quote);
  showQuoteModalRef.value = false;
  // Emit event to parent to refresh trip data
  emit('trip-updated');
};

// Quote status update functions
const updateQuoteStatus = async (newStatus: string) => {
  if (!props.trip?.quote || props.trip.quote.status === newStatus) return;

  // If changing to lost, show the lost reason modal
  if (newStatus === 'lost') {
    // Reset dropdown to current status while modal is shown
    const currentStatus = props.trip.quote.status;
    props.trip.quote.status = '';
    nextTick(() => {
      props.trip.quote.status = currentStatus;
    });

    // Show the lost reason modal
    if (lostReasonModalRef.value) {
      lostReasonModalRef.value.show();
    }
    return;
  }

  try {
    await ApiService.patch(`/quotes/${props.trip.quote.id}/`, { status: newStatus });

    // Update the local quote status
    props.trip.quote.status = newStatus;

    // Show success notification
    Swal.fire({
      title: "Status Updated!",
      text: `Quote status changed to ${newStatus}`,
      icon: "success",
      timer: 2000,
      showConfirmButton: false
    });

    // Emit event to parent to refresh trip data
    emit('trip-updated');

  } catch (error: any) {
    console.error('Error updating quote status:', error);
    Swal.fire({
      title: 'Error!',
      text: error.response?.data?.detail || 'Failed to update status. Please try again.',
      icon: 'error',
      confirmButtonText: 'OK'
    });
  }
};

const onLostReasonConfirmed = async (reasonId: string, comment: string) => {
  if (!props.trip?.quote) return;

  try {
    // Update quote with lost reason and status
    await ApiService.patch(`/quotes/${props.trip.quote.id}/`, {
      status: 'lost',
      lost_reason: reasonId
    });

    // Update local quote object
    props.trip.quote.status = 'lost';

    // Update associated trip status to cancelled
    try {
      await ApiService.patch(`/trips/${props.trip.id}/`, {
        status: 'cancelled'
      });

      // Update local trip object
      props.trip.status = 'cancelled';
    } catch (tripError) {
      console.error('Error updating trip status:', tripError);
      // Continue even if trip update fails - quote is still marked as lost
    }

    // If there's a comment, save it
    if (comment.trim()) {
      try {
        await ApiService.post('/comments/', {
          content_type: 'quote',
          object_id: props.trip.quote.id,
          text: `Quote marked as lost: ${comment.trim()}`
        });
      } catch (commentError) {
        console.error('Error saving lost reason comment:', commentError);
        // Continue even if comment fails
      }
    }

    // Show success notification
    Swal.fire({
      title: "Quote Marked as Lost!",
      text: "Quote status updated to Lost and Trip status updated to Cancelled",
      icon: "success",
      timer: 2000,
      showConfirmButton: false
    });

    // Emit event to parent to refresh trip data
    emit('trip-updated');

  } catch (error: any) {
    console.error('Error updating quote status:', error);
    Swal.fire({
      title: 'Error!',
      text: error.response?.data?.detail || 'Failed to update quote status. Please try again.',
      icon: 'error',
      confirmButtonText: 'OK'
    });

    // Reset dropdown back to current status
    const currentStatus = props.trip.quote.status;
    props.trip.quote.status = '';
    nextTick(() => {
      props.trip.quote.status = currentStatus;
    });
  }
};
</script>

<style scoped>
.table th,
.table td {
  padding: 0.75rem 1rem;
}
</style>