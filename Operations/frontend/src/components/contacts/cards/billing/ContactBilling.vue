<template>
  <div>
    <!-- Payment Overview Card -->
    <div class="card mb-6 mb-xl-9">
      <!--begin::Card header-->
      <div class="card-header border-0">
        <div class="card-title">
          <h3 class="fw-bold m-0">Payment Overview</h3>
        </div>
        <div class="card-toolbar">
          <button class="btn btn-sm btn-primary">Generate Invoice</button>
        </div>
      </div>
      <!--end::Card header-->

      <!--begin::Card body-->
      <div class="card-body pt-2">
        <div class="row g-6">
          <!--begin::Col-->
          <div class="col-lg-3 col-md-6">
            <div class="border border-dashed border-gray-300 text-center min-w-125px rounded py-4 px-3">
              <span class="fs-6 fw-semibold text-gray-700 d-block mb-2">Total Billed</span>
              <div class="fs-2 fw-bold text-gray-800">${{ getTotalBilled() }}</div>
            </div>
          </div>
          <!--end::Col-->

          <!--begin::Col-->
          <div class="col-lg-3 col-md-6">
            <div class="border border-dashed border-gray-300 text-center min-w-125px rounded py-4 px-3">
              <span class="fs-6 fw-semibold text-gray-700 d-block mb-2">Total Paid</span>
              <div class="fs-2 fw-bold text-success">${{ getTotalPaid() }}</div>
            </div>
          </div>
          <!--end::Col-->

          <!--begin::Col-->
          <div class="col-lg-3 col-md-6">
            <div class="border border-dashed border-gray-300 text-center min-w-125px rounded py-4 px-3">
              <span class="fs-6 fw-semibold text-gray-700 d-block mb-2">Outstanding</span>
              <div class="fs-2 fw-bold text-danger">${{ getOutstanding() }}</div>
            </div>
          </div>
          <!--end::Col-->

          <!--begin::Col-->
          <div class="col-lg-3 col-md-6">
            <div class="border border-dashed border-gray-300 text-center min-w-125px rounded py-4 px-3">
              <span class="fs-6 fw-semibold text-gray-700 d-block mb-2">Credit Balance</span>
              <div class="fs-2 fw-bold text-primary">${{ getCreditBalance() }}</div>
            </div>
          </div>
          <!--end::Col-->
        </div>
      </div>
      <!--end::Card body-->
    </div>
    <!--end::Payment Overview Card-->

    <!-- Recent Invoices Card -->
    <div class="card mb-6 mb-xl-9">
      <!--begin::Card header-->
      <div class="card-header border-0">
        <div class="card-title">
          <h3 class="fw-bold m-0">Recent Invoices</h3>
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
                <th class="ps-0 min-w-200px">Invoice</th>
                <th class="min-w-100px">Date</th>
                <th class="min-w-100px">Due Date</th>
                <th class="min-w-100px">Status</th>
                <th class="min-w-100px text-end">Amount</th>
                <th class="min-w-70px text-end">Actions</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="invoice in recentInvoices" :key="invoice.id">
                <td class="ps-0">
                  <div class="d-flex align-items-center">
                    <div class="symbol symbol-45px me-2">
                      <div class="symbol-label bg-light-primary">
                        <KTIcon icon-name="document" icon-class="fs-3 text-primary" />
                      </div>
                    </div>
                    <div class="d-flex flex-column">
                      <a href="#" class="text-gray-800 text-hover-primary fw-bold fs-6">
                        {{ invoice.invoice_number }}
                      </a>
                      <span class="text-gray-600 fw-semibold fs-7">{{ invoice.description || 'Medical Transport' }}</span>
                    </div>
                  </div>
                </td>
                <td>
                  <span class="text-gray-800 fw-bold fs-6">{{ formatDate(invoice.created_on) }}</span>
                </td>
                <td>
                  <span class="text-gray-800 fw-bold fs-6">{{ formatDate(invoice.due_date) }}</span>
                </td>
                <td>
                  <span :class="`badge badge-light-${getInvoiceStatusColor(invoice.status)} fs-7`">
                    {{ invoice.status }}
                  </span>
                </td>
                <td class="text-end">
                  <span class="text-gray-800 fw-bold fs-6">${{ formatAmount(invoice.total_amount) }}</span>
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
                        <a class="dropdown-item" href="#" @click="viewInvoice(invoice.id)">View</a>
                      </li>
                      <li>
                        <a class="dropdown-item" href="#" @click="downloadInvoice(invoice.id)">Download</a>
                      </li>
                      <li>
                        <a class="dropdown-item" href="#" @click="sendInvoice(invoice.id)">Send Email</a>
                      </li>
                      <li v-if="invoice.status === 'draft'">
                        <a class="dropdown-item" href="#" @click="editInvoice(invoice.id)">Edit</a>
                      </li>
                    </ul>
                  </div>
                </td>
              </tr>
              <tr v-if="recentInvoices.length === 0">
                <td colspan="6" class="text-center text-muted py-6">
                  No invoices found for this contact
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
      <!--end::Card body-->
    </div>
    <!--end::Recent Invoices Card-->

    <!-- Payment History Card -->
    <div class="card mb-6 mb-xl-9">
      <!--begin::Card header-->
      <div class="card-header border-0">
        <div class="card-title">
          <h3 class="fw-bold m-0">Payment History</h3>
        </div>
        <div class="card-toolbar">
          <button class="btn btn-sm btn-light">Export</button>
        </div>
      </div>
      <!--end::Card header-->

      <!--begin::Card body-->
      <div class="card-body pt-2">
        <div class="table-responsive">
          <table class="table table-row-dashed align-middle gs-0 gy-4 my-0">
            <thead>
              <tr class="fs-7 fw-bold text-gray-500 border-bottom-0">
                <th class="ps-0 min-w-200px">Payment</th>
                <th class="min-w-100px">Date</th>
                <th class="min-w-100px">Method</th>
                <th class="min-w-100px">Reference</th>
                <th class="min-w-100px text-end">Amount</th>
                <th class="min-w-70px text-end">Actions</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="payment in paymentHistory" :key="payment.id">
                <td class="ps-0">
                  <div class="d-flex align-items-center">
                    <div class="symbol symbol-45px me-2">
                      <div :class="`symbol-label bg-light-${getPaymentMethodColor(payment.method)}`">
                        <KTIcon 
                          :icon-name="getPaymentMethodIcon(payment.method)" 
                          :icon-class="`fs-3 text-${getPaymentMethodColor(payment.method)}`" 
                        />
                      </div>
                    </div>
                    <div class="d-flex flex-column">
                      <span class="text-gray-800 fw-bold fs-6">Payment #{{ payment.id }}</span>
                      <span class="text-gray-600 fw-semibold fs-7">{{ payment.description || 'Trip Payment' }}</span>
                    </div>
                  </div>
                </td>
                <td>
                  <span class="text-gray-800 fw-bold fs-6">{{ formatDate(payment.payment_date) }}</span>
                </td>
                <td>
                  <span class="text-gray-800 fw-bold fs-6">{{ payment.method || 'Credit Card' }}</span>
                </td>
                <td>
                  <span class="text-gray-600 fs-6">{{ payment.reference_number || '-' }}</span>
                </td>
                <td class="text-end">
                  <span class="text-gray-800 fw-bold fs-6">${{ formatAmount(payment.amount) }}</span>
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
                        <a class="dropdown-item" href="#" @click="viewPayment(payment.id)">View Receipt</a>
                      </li>
                      <li>
                        <a class="dropdown-item" href="#" @click="downloadReceipt(payment.id)">Download</a>
                      </li>
                      <li>
                        <a class="dropdown-item" href="#" @click="refundPayment(payment.id)">Refund</a>
                      </li>
                    </ul>
                  </div>
                </td>
              </tr>
              <tr v-if="paymentHistory.length === 0">
                <td colspan="6" class="text-center text-muted py-6">
                  No payments found for this contact
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
      <!--end::Card body-->
    </div>
    <!--end::Payment History Card-->

    <!-- Quotes Card -->
    <div class="card mb-6 mb-xl-9">
      <!--begin::Card header-->
      <div class="card-header border-0">
        <div class="card-title">
          <h3 class="fw-bold m-0">Quotes & Estimates</h3>
        </div>
        <div class="card-toolbar">
          <button class="btn btn-sm btn-primary">Create Quote</button>
        </div>
      </div>
      <!--end::Card header-->

      <!--begin::Card body-->
      <div class="card-body pt-2">
        <div class="table-responsive">
          <table class="table table-row-dashed align-middle gs-0 gy-4 my-0">
            <thead>
              <tr class="fs-7 fw-bold text-gray-500 border-bottom-0">
                <th class="ps-0 min-w-200px">Quote</th>
                <th class="min-w-100px">Date</th>
                <th class="min-w-100px">Valid Until</th>
                <th class="min-w-100px">Status</th>
                <th class="min-w-100px text-end">Amount</th>
                <th class="min-w-70px text-end">Actions</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="quote in quotes" :key="quote.id">
                <td class="ps-0">
                  <div class="d-flex align-items-center">
                    <div class="symbol symbol-45px me-2">
                      <div class="symbol-label bg-light-info">
                        <KTIcon icon-name="calculator" icon-class="fs-3 text-info" />
                      </div>
                    </div>
                    <div class="d-flex flex-column">
                      <a href="#" class="text-gray-800 text-hover-primary fw-bold fs-6">
                        {{ quote.quote_number }}
                      </a>
                      <span class="text-gray-600 fw-semibold fs-7">{{ quote.description || 'Medical Transport Quote' }}</span>
                    </div>
                  </div>
                </td>
                <td>
                  <span class="text-gray-800 fw-bold fs-6">{{ formatDate(quote.created_on) }}</span>
                </td>
                <td>
                  <span class="text-gray-800 fw-bold fs-6">{{ formatDate(quote.valid_until) }}</span>
                </td>
                <td>
                  <span :class="`badge badge-light-${getQuoteStatusColor(quote.status)} fs-7`">
                    {{ quote.status }}
                  </span>
                </td>
                <td class="text-end">
                  <span class="text-gray-800 fw-bold fs-6">${{ formatAmount(quote.total_amount) }}</span>
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
                        <a class="dropdown-item" href="#" @click="viewQuote(quote.id)">View</a>
                      </li>
                      <li>
                        <a class="dropdown-item" href="#" @click="sendQuote(quote.id)">Send</a>
                      </li>
                      <li>
                        <a class="dropdown-item" href="#" @click="convertToTrip(quote.id)">Convert to Trip</a>
                      </li>
                      <li v-if="quote.status === 'draft'">
                        <a class="dropdown-item" href="#" @click="editQuote(quote.id)">Edit</a>
                      </li>
                    </ul>
                  </div>
                </td>
              </tr>
              <tr v-if="quotes.length === 0">
                <td colspan="6" class="text-center text-muted py-6">
                  No quotes found for this contact
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
      <!--end::Card body-->
    </div>
    <!--end::Quotes Card-->
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from "vue";
import ApiService from "@/core/services/ApiService";
import Swal from "sweetalert2";

interface Props {
  contact: any;
  loading: boolean;
}

const props = defineProps<Props>();

const recentInvoices = ref<any[]>([]);
const paymentHistory = ref<any[]>([]);
const quotes = ref<any[]>([]);

const fetchBillingData = async () => {
  if (!props.contact?.id) return;
  
  try {
    // Fetch quotes (this endpoint exists)
    const quotesResponse = await ApiService.get(`/quotes/?contact_id=${props.contact.id}&limit=10`);
    quotes.value = quotesResponse.data.results || quotesResponse.data || [];
    
    // Fetch transactions related to quotes for this contact
    try {
      const transactionsResponse = await ApiService.get(`/transactions/?limit=10`);
      const allTransactions = transactionsResponse.data.results || transactionsResponse.data || [];
      // Filter transactions by contact through quotes
      paymentHistory.value = allTransactions.filter(transaction => 
        quotes.value.some(quote => 
          quote.transactions && quote.transactions.some(t => t.id === transaction.id)
        )
      );
    } catch (error) {
      console.warn('Could not fetch transactions:', error);
      paymentHistory.value = [];
    }
    
    // Invoices endpoint doesn't exist - use empty array
    recentInvoices.value = [];
  } catch (error) {
    console.error('Error fetching billing data:', error);
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

const formatAmount = (amount?: number): string => {
  if (!amount) return '0';
  return amount.toLocaleString();
};

const getTotalBilled = (): string => {
  return (props.contact?.total_billed || 0).toLocaleString();
};

const getTotalPaid = (): string => {
  return (props.contact?.total_paid || 0).toLocaleString();
};

const getOutstanding = (): string => {
  return (props.contact?.outstanding_balance || 0).toLocaleString();
};

const getCreditBalance = (): string => {
  return (props.contact?.credit_balance || 0).toLocaleString();
};

const getInvoiceStatusColor = (status: string): string => {
  switch (status?.toLowerCase()) {
    case 'paid': return 'success';
    case 'pending': return 'warning';
    case 'overdue': return 'danger';
    case 'draft': return 'secondary';
    default: return 'primary';
  }
};

const getPaymentMethodColor = (method: string): string => {
  switch (method?.toLowerCase()) {
    case 'credit card': return 'primary';
    case 'bank transfer': return 'success';
    case 'cash': return 'warning';
    case 'check': return 'info';
    default: return 'secondary';
  }
};

const getPaymentMethodIcon = (method: string): string => {
  switch (method?.toLowerCase()) {
    case 'credit card': return 'credit-card';
    case 'bank transfer': return 'bank';
    case 'cash': return 'dollar';
    case 'check': return 'document';
    default: return 'wallet';
  }
};

const getQuoteStatusColor = (status: string): string => {
  switch (status?.toLowerCase()) {
    case 'accepted': return 'success';
    case 'pending': return 'warning';
    case 'expired': return 'danger';
    case 'draft': return 'secondary';
    case 'sent': return 'primary';
    default: return 'secondary';
  }
};

const viewInvoice = (invoiceId: string) => {
  Swal.fire({
    title: 'View Invoice',
    text: `Would open invoice details for ID: ${invoiceId}`,
    icon: 'info'
  });
};

const downloadInvoice = (invoiceId: string) => {
  Swal.fire({
    title: 'Download Invoice',
    text: `Would download invoice PDF for ID: ${invoiceId}`,
    icon: 'info'
  });
};

const sendInvoice = (invoiceId: string) => {
  Swal.fire({
    title: 'Send Invoice',
    text: `Would send invoice via email for ID: ${invoiceId}`,
    icon: 'info'
  });
};

const editInvoice = (invoiceId: string) => {
  Swal.fire({
    title: 'Edit Invoice',
    text: `Would open invoice editor for ID: ${invoiceId}`,
    icon: 'info'
  });
};

const viewPayment = (paymentId: string) => {
  Swal.fire({
    title: 'View Payment',
    text: `Would show payment receipt for ID: ${paymentId}`,
    icon: 'info'
  });
};

const downloadReceipt = (paymentId: string) => {
  Swal.fire({
    title: 'Download Receipt',
    text: `Would download payment receipt for ID: ${paymentId}`,
    icon: 'info'
  });
};

const refundPayment = (paymentId: string) => {
  Swal.fire({
    title: 'Refund Payment',
    text: `Are you sure you want to refund payment ID: ${paymentId}?`,
    icon: 'warning',
    showCancelButton: true,
    confirmButtonText: 'Yes, refund it!'
  }).then((result) => {
    if (result.isConfirmed) {
      Swal.fire('Refunded!', 'The payment has been refunded.', 'success');
    }
  });
};

const viewQuote = (quoteId: string) => {
  Swal.fire({
    title: 'View Quote',
    text: `Would open quote details for ID: ${quoteId}`,
    icon: 'info'
  });
};

const sendQuote = (quoteId: string) => {
  Swal.fire({
    title: 'Send Quote',
    text: `Would send quote via email for ID: ${quoteId}`,
    icon: 'info'
  });
};

const convertToTrip = (quoteId: string) => {
  Swal.fire({
    title: 'Convert to Trip',
    text: `Would convert quote ID: ${quoteId} to a trip booking`,
    icon: 'info'
  });
};

const editQuote = (quoteId: string) => {
  Swal.fire({
    title: 'Edit Quote',
    text: `Would open quote editor for ID: ${quoteId}`,
    icon: 'info'
  });
};

onMounted(() => {
  if (props.contact?.id) {
    fetchBillingData();
  }
});
</script>