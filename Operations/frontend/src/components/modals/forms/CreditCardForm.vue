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

    <!-- Card Number -->
    <div class="d-flex flex-column mb-7 fv-row">
      <label class="d-flex align-items-center fs-6 fw-semibold form-label mb-2">
        <span class="required">Card Number</span>
        <i class="fas fa-credit-card ms-2 fs-7" data-bs-toggle="tooltip" 
           title="Enter your credit card number"></i>
      </label>
      <Field
        name="cardNumber"
        type="text"
        class="form-control form-control-solid"
        placeholder="1234 5678 9012 3456"
        v-model="formData.cardNumber"
        @input="formatCardNumber"
        maxlength="19"
      />
      <div class="fv-plugins-message-container">
        <div class="fv-help-block">
          <ErrorMessage name="cardNumber" />
        </div>
      </div>
    </div>

    <!-- Expiry Date and CVV Row -->
    <div class="row g-9 mb-7">
      <div class="col-md-6 fv-row">
        <label class="d-flex align-items-center fs-6 fw-semibold form-label mb-2">
          <span class="required">Expiry Date</span>
          <i class="fas fa-calendar ms-2 fs-7" data-bs-toggle="tooltip" 
             title="Enter MM/YY format"></i>
        </label>
        <Field
          name="expirationDate"
          type="text"
          class="form-control form-control-solid"
          placeholder="MM/YY"
          v-model="formData.expirationDate"
          @input="formatExpiryDate"
          maxlength="5"
        />
        <div class="fv-plugins-message-container">
          <div class="fv-help-block">
            <ErrorMessage name="expirationDate" />
          </div>
        </div>
      </div>
      <div class="col-md-6 fv-row">
        <label class="d-flex align-items-center fs-6 fw-semibold form-label mb-2">
          <span class="required">CVV</span>
          <i class="fas fa-lock ms-2 fs-7" data-bs-toggle="tooltip" 
             title="3-4 digit security code on back of card"></i>
        </label>
        <Field
          name="cardCode"
          type="text"
          class="form-control form-control-solid"
          placeholder="123"
          v-model="formData.cardCode"
          maxlength="4"
        />
        <div class="fv-plugins-message-container">
          <div class="fv-help-block">
            <ErrorMessage name="cardCode" />
          </div>
        </div>
      </div>
    </div>

    <!-- Cardholder Name -->
    <div class="d-flex flex-column mb-7 fv-row">
      <label class="d-flex align-items-center fs-6 fw-semibold form-label mb-2">
        <span class="required">Cardholder Name</span>
      </label>
      <Field
        name="cardholderName"
        type="text"
        class="form-control form-control-solid"
        placeholder="Full name as on card"
        v-model="formData.cardholderName"
      />
      <div class="fv-plugins-message-container">
        <div class="fv-help-block">
          <ErrorMessage name="cardholderName" />
        </div>
      </div>
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
        @click="onButtonClick"
      >
        <span v-if="!processing" class="indicator-label">
          <i class="fas fa-credit-card fs-4 me-2"></i>
          Process Payment of {{ formattedAmount }}
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
import PaymentService, { type CardPaymentData, type BillingAddress } from '@/core/services/PaymentService';

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
  submit: [data: CardPaymentData];
}>();

// Form data
const formData = ref({
  amount: '',
  cardNumber: '',
  expirationDate: '',
  cardCode: '',
  cardholderName: '',
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
  cardNumber: yup.string()
    .required('Card number is required')
    .test('card-number', 'Invalid card number', (value) => {
      return PaymentService.validateCardNumber(value || '');
    }),
  expirationDate: yup.string()
    .required('Expiry date is required')
    .matches(/^(0[1-9]|1[0-2])\/\d{2}$/, 'Enter valid MM/YY format')
    .test('not-expired', 'Card is expired', (value) => {
      if (!value) return true;
      const [month, year] = value.split('/');
      const expiry = new Date(2000 + parseInt(year), parseInt(month) - 1);
      return expiry > new Date();
    }),
  cardCode: yup.string()
    .required('CVV is required')
    .matches(/^\d{3,4}$/, 'CVV must be 3-4 digits'),
  cardholderName: yup.string()
    .required('Cardholder name is required')
    .min(2, 'Name must be at least 2 characters'),
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

// Format card number with spaces
const formatCardNumber = (event: Event) => {
  const target = event.target as HTMLInputElement;
  const formatted = PaymentService.formatCardNumber(target.value);
  formData.value.cardNumber = formatted;
};

// Format expiry date
const formatExpiryDate = (event: Event) => {
  const target = event.target as HTMLInputElement;
  let value = target.value.replace(/\D/g, '');
  
  if (value.length >= 2) {
    value = value.substring(0, 2) + '/' + value.substring(2, 4);
  }
  
  formData.value.expirationDate = value;
};

// Button click handler - manually trigger form submission since validation is disabled
const onButtonClick = (event: Event) => {
  event.preventDefault();
  handleSubmit(null, null);
};

// Handle form submission
const handleSubmit = (values: any, actions: any) => {
  console.log('Form submission triggered!', { values, formData: formData.value });
  
  // Parse name into first/last
  const nameParts = formData.value.cardholderName.trim().split(' ');
  const firstName = nameParts[0] || '';
  const lastName = nameParts.slice(1).join(' ') || '';

  // Convert MM/YY to MMYY format for Authorize.Net
  const expiryParts = formData.value.expirationDate.split('/');
  const mmyyFormat = expiryParts[0] + expiryParts[1];

  const paymentData: CardPaymentData = {
    amount: formData.value.amount,
    cardNumber: formData.value.cardNumber.replace(/\s/g, ''), // Remove spaces
    expirationDate: mmyyFormat,
    cardCode: formData.value.cardCode,
    quote_id: props.quoteId,
    refId: `quote_${props.quoteId}`,
    billTo: {
      ...formData.value.billTo,
      firstName,
      lastName
    }
  };

  console.log('Emitting payment data:', paymentData);
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
    
    // Pre-fill cardholder name
    const fullName = `${props.customerInfo.first_name || ''} ${props.customerInfo.last_name || ''}`.trim();
    if (fullName) {
      formData.value.cardholderName = fullName;
    }
  }
});

// Watch for changes to defaultAmount prop
watch(() => props.defaultAmount, (newAmount) => {
  formData.value.amount = newAmount.toString();
});
</script>