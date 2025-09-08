<template>
  <div class="modal fade show d-block" tabindex="-1" role="dialog">
    <div class="modal-dialog modal-dialog-centered modal-lg">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title">Generate Agreements</h5>
          <button type="button" class="btn-close" @click="close"></button>
        </div>
        <div class="modal-body">
          <!-- Contract Types Selection -->
          <div class="mb-6">
            <label class="form-label required">Select Agreement Types</label>
            <div class="row">
              <div class="col-12 mb-3" v-for="contractType in contractTypes" :key="contractType.value">
                <div class="form-check form-check-custom form-check-solid">
                  <input 
                    class="form-check-input" 
                    type="checkbox" 
                    :id="`contract-${contractType.value}`"
                    :value="contractType.value"
                    v-model="selectedTypes"
                  />
                  <label class="form-check-label" :for="`contract-${contractType.value}`">
                    <div class="fw-bold text-gray-800">{{ contractType.label }}</div>
                    <div class="text-gray-600 fs-7">{{ contractType.description }}</div>
                  </label>
                </div>
              </div>
            </div>
          </div>

          <!-- Signer Information -->
          <div class="separator separator-dashed my-6"></div>
          <h6 class="mb-4">Signer Information</h6>
          
          <div v-if="hasCustomerContact" class="row">
            <div class="col-md-6 mb-4">
              <label class="form-label">Use Customer Contact</label>
              <div class="form-check form-switch form-check-custom form-check-solid">
                <input 
                  class="form-check-input" 
                  type="checkbox" 
                  id="useCustomerContact"
                  v-model="useCustomerContact"
                />
                <label class="form-check-label" for="useCustomerContact">
                  Use {{ tripData?.quote?.contact?.email }} from quote
                </label>
              </div>
            </div>
          </div>
          
          <div v-if="!hasCustomerContact" class="alert alert-info">
            <i class="fas fa-info-circle me-2"></i>
            <strong>No customer contact found in quote.</strong> Please provide signer information below.
          </div>

          <div v-if="!useCustomerContact" class="row">
            <div class="col-md-6 mb-4">
              <label class="form-label required">Signer Email</label>
              <input 
                type="email" 
                class="form-control" 
                v-model="customSignerEmail"
                placeholder="Enter signer email"
                :class="{ 'is-invalid': errors.email }"
              />
              <div v-if="errors.email" class="invalid-feedback">
                {{ errors.email }}
              </div>
            </div>
            <div class="col-md-6 mb-4">
              <label class="form-label">Signer Name</label>
              <input 
                type="text" 
                class="form-control" 
                v-model="customSignerName"
                placeholder="Enter signer name"
              />
            </div>
          </div>

          <!-- Send Options -->
          <div class="separator separator-dashed my-6"></div>
          <div class="row">
            <div class="col-12">
              <div class="form-check form-check-custom form-check-solid">
                <input 
                  class="form-check-input" 
                  type="checkbox" 
                  id="sendImmediately"
                  v-model="sendImmediately"
                />
                <label class="form-check-label" for="sendImmediately">
                  <div class="fw-bold text-gray-800">Send for signature immediately</div>
                  <div class="text-gray-600 fs-7">Contracts will be sent to DocuSeal right after generation</div>
                </label>
              </div>
            </div>
          </div>

          <!-- Info Alert -->
          <div class="alert alert-info d-flex align-items-center mt-6" v-if="selectedTypes.length > 0">
            <i class="fas fa-info-circle fs-2 me-3"></i>
            <div>
              <strong>{{ selectedTypes.length }} agreement(s) selected</strong><br>
              <span class="fs-7">
                These agreements will be generated using DocuSeal templates and populated with trip, patient, and customer data.
              </span>
            </div>
          </div>
        </div>
        <div class="modal-footer">
          <button type="button" class="btn btn-light" @click="close">Cancel</button>
          <button 
            type="button" 
            class="btn btn-primary" 
            @click="generateContracts"
            :disabled="isGenerating || selectedTypes.length === 0 || (!useCustomerContact && !customSignerEmail)"
          >
            <span v-if="!isGenerating">
              <i class="fas fa-file-contract me-2"></i>
              Generate {{ selectedTypes.length }} Agreement(s)
            </span>
            <span v-else>
              <span class="spinner-border spinner-border-sm me-2" role="status"></span>
              Generating...
            </span>
          </button>
        </div>
      </div>
    </div>
  </div>
  <div class="modal-backdrop fade show"></div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue';
import ApiService from '@/core/services/ApiService';
import Swal from 'sweetalert2';

interface Props {
  tripId: string;
  tripData?: any;
}

interface Emits {
  (e: 'close'): void;
  (e: 'contracts-generated', contracts: any[]): void;
}

const props = defineProps<Props>();
const emit = defineEmits<Emits>();

const contractTypes = [
  {
    value: 'consent_transport',
    label: 'Consent for Transport',
    description: 'Agreement for medical transport services with origin and destination airports'
  },
  {
    value: 'payment_agreement',
    label: 'Air Ambulance Payment Agreement',
    description: 'Payment terms including price with 2.5% processing fee, requires JET ICU signature'
  },
  {
    value: 'patient_service_agreement',
    label: 'Patient Service Agreement',
    description: 'Comprehensive patient service terms, requires JET ICU signature'
  }
];

const selectedTypes = ref<string[]>([]);
// Check if customer contact is available from trip quote
const hasCustomerContact = computed(() => {
  return props.tripData?.quote?.contact?.email;
});

const useCustomerContact = ref(false); // Will be set based on availability
const customSignerEmail = ref('');
const customSignerName = ref('');
const sendImmediately = ref(false);
const isGenerating = ref(false);
const errors = ref<Record<string, string>>({});

const validateEmail = (email: string) => {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return emailRegex.test(email);
};

const generateContracts = async () => {
  // Clear errors
  errors.value = {};

  // Validate
  if (!useCustomerContact.value) {
    if (!customSignerEmail.value) {
      errors.value.email = 'Email is required';
      return;
    }
    if (!validateEmail(customSignerEmail.value)) {
      errors.value.email = 'Please enter a valid email';
      return;
    }
  }

  if (selectedTypes.value.length === 0) {
    Swal.fire({
      icon: 'warning',
      title: 'No Agreements Selected',
      text: 'Please select at least one agreement type'
    });
    return;
  }

  isGenerating.value = true;
  try {
    const payload: any = {
      trip_id: props.tripId,
      contract_types: selectedTypes.value,
      send_immediately: sendImmediately.value
    };

    if (!useCustomerContact.value) {
      payload.custom_signer_email = customSignerEmail.value;
      if (customSignerName.value) {
        payload.custom_signer_name = customSignerName.value;
      }
    }

    const response = await ApiService.post('contracts/create_from_trip/', payload);
    
    const contractCount = response.data.contracts?.length || selectedTypes.value.length;
    const message = sendImmediately.value 
      ? `${contractCount} agreement(s) generated and sent for signature`
      : `${contractCount} agreement(s) generated successfully`;

    Swal.fire({
      icon: 'success',
      title: 'Success!',
      text: message,
      timer: 3000,
      showConfirmButton: false
    });

    emit('contracts-generated', response.data.contracts);
  } catch (error: any) {
    console.error('Error generating contracts:', error);
    const errorMessage = error.response?.data?.error || 
                        error.response?.data?.detail || 
                        'Failed to generate agreements';
    
    Swal.fire({
      icon: 'error',
      title: 'Error',
      text: errorMessage
    });
  } finally {
    isGenerating.value = false;
  }
};

const close = () => {
  emit('close');
};

// Set default value for useCustomerContact based on availability
onMounted(() => {
  useCustomerContact.value = hasCustomerContact.value;
});
</script>

<style scoped>
.modal {
  background-color: rgba(0, 0, 0, 0.5);
}
</style>