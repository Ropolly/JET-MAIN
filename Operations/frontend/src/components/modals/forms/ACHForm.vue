<template>
  <VForm @submit="handleSubmit">
    <!-- Payment Amount -->
    <div class="d-flex flex-column mb-7 fv-row">
      <label class="d-flex align-items-center fs-6 fw-semibold form-label mb-2">
        <span class="required">Payment Amount</span>
        <i class="fas fa-exclamation-circle ms-2 fs-7" data-bs-toggle="tooltip" 
           title="Enter the amount to charge (can be partial payment)"></i>
      </label>
      <Field
        name="amount"
        type="text"
        class="form-control form-control-solid"
        placeholder="$0.00"
        v-model="formData.amount"
        @input="formatAmountInput"
      />
      <div class="fv-plugins-message-container">
        <div class="fv-help-block">
          <ErrorMessage name="amount" />
        </div>
      </div>
    </div>

    <!-- Account Type -->
    <div class="d-flex flex-column mb-7 fv-row">
      <label class="d-flex align-items-center fs-6 fw-semibold form-label mb-2">
        <span class="required">Account Type</span>
        <i class="fas fa-university ms-2 fs-7" data-bs-toggle="tooltip" 
           title="Select checking or savings account"></i>
      </label>
      <div class="row">
        <div class="col-6">
          <Field name="accountType" v-model="formData.accountType" type="radio" value="checking" />
          <label class="form-check-label ms-2">
            <i class="fas fa-check-circle text-primary me-2"></i>
            Checking
          </label>
        </div>
        <div class="col-6">
          <Field name="accountType" v-model="formData.accountType" type="radio" value="savings" />
          <label class="form-check-label ms-2">
            <i class="fas fa-piggy-bank text-success me-2"></i>
            Savings
          </label>
        </div>
      </div>
      <div class="fv-plugins-message-container">
        <div class="fv-help-block">
          <ErrorMessage name="accountType" />
        </div>
      </div>
    </div>

    <!-- Routing Number and Account Number Row -->
    <div class="row g-9 mb-7">
      <div class="col-md-6 fv-row">
        <label class="d-flex align-items-center fs-6 fw-semibold form-label mb-2">
          <span class="required">Routing Number</span>
          <i class="fas fa-code-branch ms-2 fs-7" data-bs-toggle="tooltip" 
             title="9-digit bank routing number"></i>
        </label>
        <Field
          name="routingNumber"
          type="text"
          class="form-control form-control-solid"
          placeholder="123456789"
          v-model="formData.routingNumber"
          @input="formatRoutingNumber"
          maxlength="9"
        />
        <div class="fv-plugins-message-container">
          <div class="fv-help-block">
            <ErrorMessage name="routingNumber" />
          </div>
        </div>
      </div>
      <div class="col-md-6 fv-row">
        <label class="d-flex align-items-center fs-6 fw-semibold form-label mb-2">
          <span class="required">Account Number</span>
          <i class="fas fa-hashtag ms-2 fs-7" data-bs-toggle="tooltip" 
             title="Your bank account number"></i>
        </label>
        <Field
          name="accountNumber"
          type="text"
          class="form-control form-control-solid"
          placeholder="Account number"
          v-model="formData.accountNumber"
          maxlength="20"
        />
        <div class="fv-plugins-message-container">
          <div class="fv-help-block">
            <ErrorMessage name="accountNumber" />
          </div>
        </div>
      </div>
    </div>

    <!-- Account Holder Name -->
    <div class="d-flex flex-column mb-7 fv-row">
      <label class="d-flex align-items-center fs-6 fw-semibold form-label mb-2">
        <span class="required">Name on Account</span>
        <i class="fas fa-user ms-2 fs-7" data-bs-toggle="tooltip" 
           title="Name exactly as it appears on the bank account"></i>
      </label>
      <Field
        name="nameOnAccount"
        type="text"
        class="form-control form-control-solid"
        placeholder="Full name as on bank account"
        v-model="formData.nameOnAccount"
      />
      <div class="fv-plugins-message-container">
        <div class="fv-help-block">
          <ErrorMessage name="nameOnAccount" />
        </div>
      </div>
    </div>

    <!-- Bank Name (Optional) -->
    <div class="d-flex flex-column mb-7 fv-row">
      <label class="fs-6 fw-semibold form-label mb-2">
        <span>Bank Name</span>
        <span class="text-muted ms-1">(Optional)</span>
      </label>
      <Field
        name="bankName"
        type="text"
        class="form-control form-control-solid"
        placeholder="Bank name"
        v-model="formData.bankName"
      />
    </div>

    <!-- Billing Address -->
    <div class="separator separator-dashed my-5"></div>
    <h5 class="fw-bold text-gray-800 mb-7">Billing Address</h5>

    <!-- Address Line -->
    <div class="d-flex flex-column mb-7 fv-row">
      <label class="fs-6 fw-semibold form-label mb-2">
        <span class="required">Address</span>
      </label>
      <Field
        name="billTo.address"
        type="text"
        class="form-control form-control-solid"
        placeholder="123 Main Street"
        v-model="formData.billTo.address"
      />
      <div class="fv-plugins-message-container">
        <div class="fv-help-block">
          <ErrorMessage name="billTo.address" />
        </div>
      </div>
    </div>

    <!-- City, State, ZIP Row -->
    <div class="row g-9 mb-7">
      <div class="col-md-4 fv-row">
        <label class="fs-6 fw-semibold form-label mb-2">
          <span class="required">City</span>
        </label>
        <Field
          name="billTo.city"
          type="text"
          class="form-control form-control-solid"
          placeholder="City"
          v-model="formData.billTo.city"
        />
        <div class="fv-plugins-message-container">
          <div class="fv-help-block">
            <ErrorMessage name="billTo.city" />
          </div>
        </div>
      </div>
      <div class="col-md-4 fv-row">
        <label class="fs-6 fw-semibold form-label mb-2">
          <span class="required">State</span>
        </label>
        <Field
          name="billTo.state"
          type="text"
          class="form-control form-control-solid"
          placeholder="CA"
          v-model="formData.billTo.state"
          maxlength="2"
        />
        <div class="fv-plugins-message-container">
          <div class="fv-help-block">
            <ErrorMessage name="billTo.state" />
          </div>
        </div>
      </div>
      <div class="col-md-4 fv-row">
        <label class="fs-6 fw-semibold form-label mb-2">
          <span class="required">ZIP Code</span>
        </label>
        <Field
          name="billTo.zip"
          type="text"
          class="form-control form-control-solid"
          placeholder="12345"
          v-model="formData.billTo.zip"
          maxlength="10"
        />
        <div class="fv-plugins-message-container">
          <div class="fv-help-block">
            <ErrorMessage name="billTo.zip" />
          </div>
        </div>
      </div>
    </div>

    <!-- Email -->
    <div class="d-flex flex-column mb-7 fv-row">
      <label class="fs-6 fw-semibold form-label mb-2">
        <span class="required">Email</span>
      </label>
      <Field
        name="billTo.email"
        type="email"
        class="form-control form-control-solid"
        placeholder="customer@example.com"
        v-model="formData.billTo.email"
      />
      <div class="fv-plugins-message-container">
        <div class="fv-help-block">
          <ErrorMessage name="billTo.email" />
        </div>
      </div>
    </div>

    <!-- Submit Button -->
    <div class="text-center">
      <button
        type="submit"
        class="btn btn-lg btn-primary w-100"
        :disabled="processing"
      >
        <span v-if="!processing" class="indicator-label">
          <i class="fas fa-university fs-4 me-2"></i>
          Process ACH Payment of {{ formattedAmount }}
        </span>
        <span v-else class="indicator-progress">
          Processing...
          <span class="spinner-border spinner-border-sm align-middle ms-2"></span>
        </span>
      </button>
    </div>
  </VForm>
</template>

<script setup lang="ts">
import { ref, computed, watch, onMounted } from 'vue';
import { Field, Form as VForm, ErrorMessage } from 'vee-validate';
import * as yup from 'yup';
import PaymentService, { type ACHPaymentData, type BillingAddress } from '@/core/services/PaymentService';

interface Props {
  quoteId: string;
  defaultAmount: string | number;
  customerInfo?: any;
  processing?: boolean;
}

const props = withDefaults(defineProps<Props>(), {
  processing: false
});

const emit = defineEmits<{
  submit: [data: ACHPaymentData];
}>();

// Form data
const formData = ref({
  amount: '',
  accountType: 'checking' as 'checking' | 'savings',
  routingNumber: '',
  accountNumber: '',
  nameOnAccount: '',
  bankName: '',
  billTo: {
    firstName: '',
    lastName: '',
    address: '',
    city: '',
    state: '',
    zip: '',
    country: 'US',
    email: '',
    phone: ''
  } as BillingAddress
});

// Validation schema
const validationSchema = yup.object({
  amount: yup.string()
    .required('Amount is required')
    .test('is-number', 'Amount must be a valid number', (value) => {
      const num = parseFloat(value || '0');
      return !isNaN(num) && num > 0;
    })
    .test('min-amount', 'Amount must be greater than $0.00', (value) => {
      const num = parseFloat(value || '0');
      return num >= 0.01;
    })
    .test('max-amount', 'Amount cannot exceed $999,999.99', (value) => {
      const num = parseFloat(value || '0');
      return num <= 999999.99;
    }),
  accountType: yup.string()
    .required('Account type is required')
    .oneOf(['checking', 'savings'], 'Must select checking or savings'),
  routingNumber: yup.string()
    .required('Routing number is required')
    .matches(/^\d{9}$/, 'Routing number must be 9 digits')
    .test('routing-number', 'Invalid routing number', (value) => {
      return PaymentService.validateRoutingNumber(value || '');
    }),
  accountNumber: yup.string()
    .required('Account number is required')
    .min(4, 'Account number must be at least 4 digits')
    .max(20, 'Account number cannot exceed 20 digits')
    .matches(/^\d+$/, 'Account number must contain only numbers'),
  nameOnAccount: yup.string()
    .required('Name on account is required')
    .min(2, 'Name must be at least 2 characters'),
  bankName: yup.string()
    .optional(),
  'billTo.address': yup.string()
    .required('Address is required'),
  'billTo.city': yup.string()
    .required('City is required'),
  'billTo.state': yup.string()
    .required('State is required')
    .length(2, 'Enter 2-letter state code'),
  'billTo.zip': yup.string()
    .required('ZIP code is required')
    .matches(/^\d{5}(-\d{4})?$/, 'Enter valid ZIP code'),
  'billTo.email': yup.string()
    .required('Email is required')
    .email('Enter valid email address')
});

// Computed values
const formattedAmount = computed(() => {
  const amount = parseFloat(formData.value.amount) || 0;
  return PaymentService.formatAmount(amount);
});

// Format amount input
const formatAmountInput = (event: Event) => {
  const target = event.target as HTMLInputElement;
  let value = target.value.replace(/[^\d.]/g, '');
  
  // Ensure only one decimal point
  const parts = value.split('.');
  if (parts.length > 2) {
    value = parts[0] + '.' + parts.slice(1).join('');
  }
  
  // Limit to 2 decimal places
  if (parts[1] && parts[1].length > 2) {
    value = parts[0] + '.' + parts[1].substring(0, 2);
  }
  
  formData.value.amount = value;
};

// Format routing number (numbers only)
const formatRoutingNumber = (event: Event) => {
  const target = event.target as HTMLInputElement;
  const value = target.value.replace(/\D/g, '');
  formData.value.routingNumber = value;
};

// Handle form submission
const handleSubmit = (values: any, actions: any) => {
  // Parse name into first/last
  const nameParts = formData.value.nameOnAccount.trim().split(' ');
  const firstName = nameParts[0] || '';
  const lastName = nameParts.slice(1).join(' ') || '';

  const paymentData: ACHPaymentData = {
    amount: formData.value.amount,
    accountType: formData.value.accountType,
    routingNumber: formData.value.routingNumber,
    accountNumber: formData.value.accountNumber,
    nameOnAccount: formData.value.nameOnAccount,
    quote_id: props.quoteId,
    echeckType: 'WEB',
    bankName: formData.value.bankName,
    refId: `quote_${props.quoteId}`,
    billTo: {
      ...formData.value.billTo,
      firstName,
      lastName
    }
  };

  emit('submit', paymentData);
};

// Initialize form with props
onMounted(() => {
  // Set default amount
  formData.value.amount = props.defaultAmount.toString();
  
  // Pre-fill customer info if available
  if (props.customerInfo) {
    formData.value.billTo.firstName = props.customerInfo.first_name || '';
    formData.value.billTo.lastName = props.customerInfo.last_name || '';
    formData.value.billTo.email = props.customerInfo.email || '';
    formData.value.billTo.phone = props.customerInfo.phone || '';
    formData.value.billTo.address = props.customerInfo.address_line1 || '';
    formData.value.billTo.city = props.customerInfo.city || '';
    formData.value.billTo.state = props.customerInfo.state || '';
    formData.value.billTo.zip = props.customerInfo.zip || '';
    
    // Pre-fill name on account
    const fullName = `${props.customerInfo.first_name || ''} ${props.customerInfo.last_name || ''}`.trim();
    if (fullName) {
      formData.value.nameOnAccount = fullName;
    }
  }
});

// Watch for changes to defaultAmount prop
watch(() => props.defaultAmount, (newAmount) => {
  formData.value.amount = newAmount.toString();
});
</script>