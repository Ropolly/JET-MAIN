<template>
  <div class="modal fade" id="paymentModal" tabindex="-1" aria-hidden="true">
    <div class="modal-dialog modal-dialog-centered mw-650px">
      <div class="modal-content">
        <form class="form" action="#" @submit.prevent="handlePayment">
          <div class="modal-header" id="payment-modal-header">
            <h2 class="fw-bold">Receive Payment</h2>
            <div class="btn btn-icon btn-sm btn-active-icon-primary" data-bs-dismiss="modal">
              <i class="fas fa-times fs-1"></i>
            </div>
          </div>

          <div class="modal-body py-10 px-lg-17">
            <!-- Quote Information -->
            <div class="card card-flush mb-8" v-if="quote">
              <div class="card-body py-5">
                <div class="d-flex align-items-center justify-content-between mb-2">
                  <h6 class="fw-semibold text-gray-600 mb-0">
                    Quote #{{ quote.id?.slice(0, 8) }}
                  </h6>
                  <span :class="PaymentService.getPaymentStatusClass(quote.payment_status || 'pending')" class="fs-7 fw-bold">
                    {{ quote.payment_status?.toUpperCase() || 'PENDING' }}
                  </span>
                </div>
                
                <div class="row g-6">
                  <div class="col-4">
                    <div class="text-gray-800 fw-bold fs-6">{{ PaymentService.formatAmount(quote.quoted_amount || 0) }}</div>
                    <div class="text-gray-400 fs-7">Quote Total</div>
                  </div>
                  <div class="col-4">
                    <div class="text-success fw-bold fs-6">{{ PaymentService.formatAmount(quote.total_paid || 0) }}</div>
                    <div class="text-gray-400 fs-7">Total Paid</div>
                  </div>
                  <div class="col-4">
                    <div class="text-primary fw-bold fs-6">{{ PaymentService.formatAmount(quote.remaining_balance || quote.quoted_amount || 0) }}</div>
                    <div class="text-gray-400 fs-7">Remaining</div>
                  </div>
                </div>
              </div>
            </div>

            <!-- Payment Method Tabs -->
            <ul class="nav nav-tabs nav-line-tabs nav-line-tabs-2x border-transparent fs-4 fw-semibold w-100 mb-8" role="tablist">
              <li class="nav-item" role="presentation">
                <a 
                  class="nav-link text-active-primary d-flex align-items-center pb-5"
                  :class="{ active: activeTab === 'creditCard' }"
                  data-bs-toggle="tab" 
                  href="#creditCardTab" 
                  role="tab"
                  @click="activeTab = 'creditCard'"
                >
                  <i class="fas fa-credit-card fs-2 me-2"></i>
                  Credit Card
                </a>
              </li>
              <li class="nav-item" role="presentation">
                <a 
                  class="nav-link text-active-primary d-flex align-items-center pb-5"
                  :class="{ active: activeTab === 'ach' }"
                  data-bs-toggle="tab" 
                  href="#achTab" 
                  role="tab"
                  @click="activeTab = 'ach'"
                >
                  <i class="fas fa-university fs-2 me-2"></i>
                  Bank Transfer (ACH)
                </a>
              </li>
            </ul>

            <div class="tab-content">
              <!-- Credit Card Tab -->
              <div 
                class="tab-pane fade" 
                :class="{ 'show active': activeTab === 'creditCard' }" 
                id="creditCardTab" 
                role="tabpanel"
              >
                <CreditCardForm
                  :quote-id="quote?.id || ''"
                  :default-amount="defaultAmount"
                  :customer-info="customerInfo"
                  :processing="processing"
                  @submit="handleCardPayment"
                />
              </div>

              <!-- ACH Tab -->
              <div 
                class="tab-pane fade" 
                :class="{ 'show active': activeTab === 'ach' }" 
                id="achTab" 
                role="tabpanel"
              >
                <ACHForm
                  :quote-id="quote?.id || ''"
                  :default-amount="defaultAmount"
                  :customer-info="customerInfo"
                  :processing="processing"
                  @submit="handleACHPayment"
                />
              </div>
            </div>

            <!-- Error Display -->
            <div v-if="errorMessage" class="alert alert-danger d-flex align-items-center mt-5">
              <i class="fas fa-exclamation-triangle fs-2hx text-danger me-4"></i>
              <div class="d-flex flex-column">
                <h4 class="mb-1 text-danger">Payment Failed</h4>
                <span>{{ errorMessage }}</span>
              </div>
            </div>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue';
import CreditCardForm from './forms/CreditCardForm.vue';
import ACHForm from './forms/ACHForm.vue';
import PaymentService, { type CardPaymentData, type ACHPaymentData, type AuthorizeNetResponse } from '@/core/services/PaymentService';
import Swal from 'sweetalert2';

interface Props {
  quote?: any;
  customerInfo?: any;
}

const props = defineProps<Props>();

const emit = defineEmits<{
  paymentSuccess: [response: AuthorizeNetResponse];
  paymentError: [error: string];
}>();

// Component state
const activeTab = ref('creditCard');
const processing = ref(false);
const errorMessage = ref('');

// Computed values
const defaultAmount = computed(() => {
  if (!props.quote) return '0.00';
  const remaining = props.quote.remaining_balance || props.quote.quoted_amount || 0;
  return remaining.toString();
});

// Payment handlers
const handleCardPayment = async (paymentData: CardPaymentData) => {
  console.log('handleCardPayment called!', paymentData);
  
  // Close payment modal immediately
  const modalElement = document.getElementById('paymentModal');
  if (modalElement) {
    const bootstrapModal = (window as any).bootstrap?.Modal?.getInstance(modalElement);
    if (bootstrapModal) {
      console.log('Closing modal...');
      bootstrapModal.hide();
    }
  }
  
  await processPayment(() => PaymentService.processCardPayment(paymentData), 'Credit Card', paymentData.amount);
};

const handleACHPayment = async (paymentData: ACHPaymentData) => {
  // Close payment modal immediately
  const modalElement = document.getElementById('paymentModal');
  if (modalElement) {
    const bootstrapModal = (window as any).bootstrap?.Modal?.getInstance(modalElement);
    if (bootstrapModal) {
      bootstrapModal.hide();
    }
  }
  
  await processPayment(() => PaymentService.processACHPayment(paymentData), 'ACH', paymentData.amount);
};

const processPayment = async (paymentFunction: () => Promise<AuthorizeNetResponse>, paymentType: string, paymentAmount?: string) => {
  processing.value = true;
  errorMessage.value = '';

  // Small delay to ensure modal has closed
  await new Promise(resolve => setTimeout(resolve, 100));
  
  // Show processing SweetAlert
  Swal.fire({
    title: 'Processing Payment',
    html: `
      <div class="text-center">
        <div class="spinner-border text-primary mb-3" role="status" aria-hidden="true"></div>
        <p class="mb-2">Processing your ${paymentType} payment...</p>
        <p class="text-muted fs-7">Amount: ${PaymentService.formatAmount(paymentAmount || '0')}</p>
      </div>
    `,
    allowOutsideClick: false,
    allowEscapeKey: false,
    showConfirmButton: false,
    didOpen: () => {
      Swal.showLoading();
    }
  });

  try {
    const response = await paymentFunction();
    const result = PaymentService.parsePaymentResponse(response);

    if (result.success) {
      // Payment successful - update SweetAlert to success
      const transactionId = response.transactionResponse?.transId || 'N/A';
      
      await Swal.fire({
        title: 'Payment Successful!',
        html: `
          <div class="text-start">
            <p class="mb-2">Your payment has been processed successfully.</p>
            <hr class="my-3">
            <p class="mb-2"><strong>Payment Method:</strong> ${paymentType}</p>
            <p class="mb-2"><strong>Amount Paid:</strong> ${PaymentService.formatAmount(paymentAmount || '0')}</p>
            <p class="mb-0"><strong>Transaction ID:</strong> ${transactionId}</p>
          </div>
        `,
        icon: 'success',
        confirmButtonText: 'Continue',
        customClass: {
          popup: 'swal2-popup-large'
        }
      });
      
      // Emit success event with amount information
      emit('paymentSuccess', { ...response, paymentAmount });
    } else {
      // Payment failed - update SweetAlert to error
      const errorMsg = result.message || 'Payment was declined. Please check your payment information and try again.';
      
      await Swal.fire({
        title: 'Payment Failed',
        text: errorMsg,
        icon: 'error',
        confirmButtonText: 'OK'
      });

      emit('paymentError', errorMsg);
    }
  } catch (error: any) {
    const errorMsg = error.message || 'An unexpected error occurred. Please try again.';

    await Swal.fire({
      title: 'Payment Error',
      text: errorMsg,
      icon: 'error',
      confirmButtonText: 'OK'
    });

    emit('paymentError', errorMsg);
  } finally {
    processing.value = false;
  }
};

// Prevent modal from closing during processing
const handlePayment = (event: Event) => {
  if (processing.value) {
    event.preventDefault();
    event.stopPropagation();
    return false;
  }
};

// Reset form when modal is hidden
onMounted(() => {
  const modal = document.getElementById('paymentModal');
  if (modal) {
    modal.addEventListener('hidden.bs.modal', () => {
      activeTab.value = 'creditCard';
      errorMessage.value = '';
      processing.value = false;
    });
  }
});
</script>

<style scoped>
/* Custom styles for payment modal */
.nav-line-tabs .nav-link {
  border: 0;
  border-bottom: 2px solid transparent;
  padding: 1rem 1.5rem;
}

.nav-line-tabs .nav-link.active {
  color: var(--bs-primary) !important;
  border-bottom-color: var(--bs-primary);
}

.card-flush {
  border: 0;
  box-shadow: 0 0 50px 0 rgba(82, 63, 105, 0.15);
}

.swal2-popup-large {
  width: 32em !important;
}

/* Disable modal dismiss during processing */
.modal.processing .modal-header [data-bs-dismiss],
.modal.processing .modal-backdrop {
  pointer-events: none;
}
</style>