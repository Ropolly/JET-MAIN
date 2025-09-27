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
      <div>
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

      <!--begin::Quote Info-->
      <div v-if="!loading && trip?.quote" class="mb-8">
        <h3 class="fw-bold text-gray-900 mb-5">
          <KTIcon icon-name="price-tag" icon-class="fs-3 text-warning me-2" />
          <span v-if="trip?.quote">
            Quote #{{ trip.quote.id?.slice(0, 8) }}
            <span :class="`badge badge-light-${getQuoteStatusColor()} ms-3`">{{ trip.quote.status }}</span>
          </span>
          <span v-else>Quote Info</span>
        </h3>

        <div class="card border border-dashed border-gray-300">
          <div class="card-body">
            <div class="table-responsive">
              <table class="table table-row-bordered">
                <thead>
                  <tr class="fw-bold fs-6 text-gray-800 border-bottom-2 border-gray-200">
                    <th>Item</th>
                    <th>Description</th>
                    <th class="text-end">Amount</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-if="trip?.quote?.created_on" class="border-bottom-2 border-gray-200">
                    <td class="fw-bold text-gray-600">Quote Date</td>
                    <td class="text-gray-600">{{ formatDate(trip.quote.created_on) }}</td>
                    <td class="text-end fw-bold">${{ formatAmount(trip.quote.quoted_amount) }}</td>
                  </tr>
                  <tr>
                    <td class="fw-bold text-gray-800">Base Flight Cost</td>
                    <td class="text-gray-600">{{ getFlightDescription() }}</td>
                    <td class="text-end fw-bold">${{ getBaseCost() }}</td>
                  </tr>
                  <tr v-if="hasMedicalTeamCost()">
                    <td class="fw-bold text-gray-800">Medical Team</td>
                    <td class="text-gray-600">{{ getMedicalTeamDescription() }}</td>
                    <td class="text-end fw-bold">${{ getMedicalTeamCost() }}</td>
                  </tr>
                  <tr v-if="hasGroundTransportCost()">
                    <td class="fw-bold text-gray-800">Ground Transportation</td>
                    <td class="text-gray-600">Airport transfers and ground support</td>
                    <td class="text-end fw-bold">${{ getGroundTransportCost() }}</td>
                  </tr>
                  <tr v-if="hasAdditionalCosts()">
                    <td class="fw-bold text-gray-800">Additional Services</td>
                    <td class="text-gray-600">{{ getAdditionalServicesDescription() }}</td>
                    <td class="text-end fw-bold">${{ getAdditionalCosts() }}</td>
                  </tr>
                  <tr class="border-top-2 border-gray-200">
                    <td colspan="2" class="fw-bold text-gray-900 fs-5">Total</td>
                    <td class="text-end fw-bold text-gray-900 fs-4">${{ getTotalCost() }}</td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </div>
      <!--end::Quote Info-->

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
        <button @click="addQuote" type="button" class="btn btn-primary">
          <i class="fas fa-plus fs-4 me-2"></i>
          Add Quote
        </button>
      </div>
      <!--end::No Quote-->
    </div>
    <!--end::Content-->
  </div>
  <!--end::Financials Content-->
</template>

<script setup lang="ts">
import { computed } from 'vue';

interface Props {
  trip: any;
  loading: boolean;
}

const props = defineProps<Props>();

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

// Function to handle adding a new quote
const addQuote = () => {
  // For now, just show an alert - this could be replaced with a modal or navigation
  alert('Add Quote functionality - this could open a modal or navigate to a quote creation form.');

  // TODO: Implement one of these approaches:
  // 1. Open a modal to create a quote
  // 2. Navigate to a dedicated quote creation page
  // 3. Emit an event to parent component to handle the action
};
</script>

<style scoped>
.table th,
.table td {
  padding: 0.75rem 1rem;
}
</style>