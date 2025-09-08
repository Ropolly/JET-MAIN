<template>
  <div class="card">
    <div class="card-header">
      <h3 class="card-title">Contracts & Agreements</h3>
      <div class="card-toolbar">
        <button
          type="button"
          class="btn btn-sm btn-light-primary"
          @click="openGenerateModal"
        >
          <i class="fas fa-file-contract fs-4 me-2"></i>
          Generate Agreements
        </button>
      </div>
    </div>
    <div class="card-body">
      <!-- Loading State -->
      <div v-if="isLoading" class="d-flex justify-content-center py-10">
        <div class="spinner-border text-primary" role="status">
          <span class="visually-hidden">Loading...</span>
        </div>
      </div>

      <!-- No Contracts State -->
      <div v-else-if="contracts.length === 0" class="text-center py-10">
        <i class="fas fa-file-signature fs-3x text-muted mb-4"></i>
        <p class="text-muted">No contracts generated yet</p>
        <button
          type="button"
          class="btn btn-primary"
          @click="openGenerateModal"
        >
          <i class="fas fa-file-contract fs-4 me-2"></i>
          Generate Agreements
        </button>
      </div>

      <!-- Contracts Grid -->
      <div v-else class="row g-5 g-xl-8">
        <div v-for="contract in contracts" :key="contract.id" class="col-xl-6 col-lg-6 col-md-6 col-sm-12">
          <div class="card">
            <div class="card-body d-flex justify-content-center text-center flex-column p-8">
              <!--begin::Name-->
              <a 
                :href="getContractLink(contract)" 
                target="_blank"
                class="text-gray-800 text-hover-primary d-flex flex-column"
              >
                <!--begin::Image-->
                <div class="symbol symbol-60px mb-5">
                  <img src="/media/svg/files/pdf.svg" class="theme-light-show" alt="Contract">
                  <img src="/media/svg/files/pdf-dark.svg" class="theme-dark-show" alt="Contract">
                </div>
                <!--end::Image-->

                <!--begin::Title-->
                <div class="fs-5 fw-bold mb-2">
                  {{ contract.contract_type_display }}
                </div>
                <!--end::Title-->
              </a>
              <!--end::Name-->

              <!--begin::Status Badge-->
              <div class="mb-2">
                <span :class="getStatusBadgeClass(contract.status)">
                  {{ contract.status_display }}
                </span>
              </div>
              <!--end::Status Badge-->

              <!--begin::Signer Info-->
              <div class="fs-7 fw-semibold text-gray-600 mb-2">
                <i class="fas fa-user me-1"></i>
                {{ contract.signer_name || contract.signer_email }}
              </div>
              <!--end::Signer Info-->

              <!--begin::Dates-->
              <div class="fs-7 fw-semibold text-gray-500 mb-4">
                <div v-if="contract.date_sent">
                  Sent: {{ formatDate(contract.date_sent) }}
                </div>
                <div v-if="contract.date_signed" class="text-success">
                  Signed: {{ formatDate(contract.date_signed) }}
                </div>
                <div v-else>
                  Created: {{ formatDate(contract.created_on) }}
                </div>
              </div>
              <!--end::Dates-->

              <!--begin::Actions-->
              <div class="d-flex justify-content-center gap-2">
                <button
                  v-if="contract.status === 'draft'"
                  type="button"
                  class="btn btn-sm btn-light-primary"
                  @click="sendForSignature(contract)"
                  :disabled="isSending"
                  title="Send for Signature"
                >
                  <i class="fas fa-paper-plane"></i>
                </button>
                <button
                  v-if="contract.status === 'pending'"
                  type="button"
                  class="btn btn-sm btn-light-warning"
                  @click="resendContract(contract)"
                  :disabled="isSending"
                  title="Resend"
                >
                  <i class="fas fa-redo"></i>
                </button>
                <a
                  v-if="contract.docuseal_submission_id"
                  :href="getContractLink(contract)"
                  target="_blank"
                  class="btn btn-sm btn-light-info"
                  title="View in DocuSeal"
                >
                  <i class="fas fa-external-link-alt"></i>
                </a>
                <button
                  v-if="contract.signed_document"
                  type="button"
                  class="btn btn-sm btn-light-success"
                  @click="downloadSignedDocument(contract)"
                  title="Download Signed"
                >
                  <i class="fas fa-download"></i>
                </button>
                <button
                  v-if="contract.status !== 'signed' && contract.status !== 'completed'"
                  type="button"
                  class="btn btn-sm btn-light-danger"
                  @click="cancelContract(contract)"
                  title="Cancel"
                >
                  <i class="fas fa-times"></i>
                </button>
              </div>
              <!--end::Actions-->
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>

  <!-- Generate Contracts Modal -->
  <GenerateContractsModal 
    v-if="showGenerateModal"
    :trip-id="tripId"
    :trip-data="tripData"
    @close="showGenerateModal = false"
    @contracts-generated="onContractsGenerated"
  />
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import ApiService from '@/core/services/ApiService';
import Swal from 'sweetalert2';
import { formatDistanceToNow } from 'date-fns';
import GenerateContractsModal from '@/components/modals/GenerateContractsModal.vue';

interface Contract {
  id: string;
  title: string;
  contract_type: string;
  contract_type_display: string;
  status: string;
  status_display: string;
  trip_id: string;
  customer_contact_id?: string;
  patient_id?: string;
  docuseal_template_id?: string;
  docuseal_submission_id?: string;
  signer_email: string;
  signer_name?: string;
  date_sent?: string;
  date_signed?: string;
  date_expired?: string;
  unsigned_document?: any;
  signed_document?: any;
  created_on: string;
  notes?: string;
}

interface Props {
  tripId: string;
  tripData?: any;
}

const props = defineProps<Props>();

const contracts = ref<Contract[]>([]);
const isLoading = ref(false);
const isSending = ref(false);
const showGenerateModal = ref(false);

const getStatusBadgeClass = (status: string) => {
  const statusClasses: Record<string, string> = {
    'draft': 'badge badge-light-secondary',
    'pending': 'badge badge-light-warning',
    'signed': 'badge badge-light-success',
    'completed': 'badge badge-light-success',
    'expired': 'badge badge-light-danger',
    'cancelled': 'badge badge-light-danger',
    'failed': 'badge badge-light-danger'
  };
  return statusClasses[status] || 'badge badge-light-secondary';
};

const getContractLink = (contract: Contract) => {
  // Try to get embed_src from the first submitter in the response data
  if (contract.docuseal_response_data?.submitters && contract.docuseal_response_data.submitters.length > 0) {
    const firstSubmitter = contract.docuseal_response_data.submitters[0];
    if (firstSubmitter.embed_src) {
      return firstSubmitter.embed_src;
    }
  }
  
  // Fallback: construct link from submission ID if available
  if (contract.docuseal_submission_id) {
    return `https://docuseal.com/submissions/${contract.docuseal_submission_id}`;
  }
  
  return '#';
};

const formatDate = (date: string) => {
  if (!date) return '';
  return formatDistanceToNow(new Date(date), { addSuffix: true });
};

const loadContracts = async () => {
  isLoading.value = true;
  try {
    const response = await ApiService.get(`contracts/?trip=${props.tripId}`);
    contracts.value = response.data.results || response.data;
  } catch (error) {
    console.error('Error loading contracts:', error);
    Swal.fire({
      icon: 'error',
      title: 'Error',
      text: 'Failed to load contracts'
    });
  } finally {
    isLoading.value = false;
  }
};

const openGenerateModal = () => {
  showGenerateModal.value = true;
};

const onContractsGenerated = () => {
  showGenerateModal.value = false;
  loadContracts();
};

const sendForSignature = async (contract: Contract) => {
  const result = await Swal.fire({
    icon: 'question',
    title: 'Send for Signature?',
    text: `Send ${contract.contract_type_display} to ${contract.signer_email} for signature?`,
    showCancelButton: true,
    confirmButtonText: 'Yes, send',
    cancelButtonText: 'Cancel'
  });

  if (result.isConfirmed) {
    isSending.value = true;
    try {
      await ApiService.post(`contracts/${contract.id}/send_for_signature/`);
      await loadContracts();
      
      Swal.fire({
        icon: 'success',
        title: 'Sent!',
        text: 'Contract has been sent for signature',
        timer: 2000,
        showConfirmButton: false
      });
    } catch (error) {
      console.error('Error sending contract:', error);
      Swal.fire({
        icon: 'error',
        title: 'Error',
        text: 'Failed to send contract for signature'
      });
    } finally {
      isSending.value = false;
    }
  }
};

const resendContract = async (contract: Contract) => {
  const result = await Swal.fire({
    icon: 'question',
    title: 'Resend Contract?',
    text: `Resend ${contract.contract_type_display} to ${contract.signer_email}?`,
    showCancelButton: true,
    confirmButtonText: 'Yes, resend',
    cancelButtonText: 'Cancel'
  });

  if (result.isConfirmed) {
    isSending.value = true;
    try {
      await ApiService.post(`contracts/${contract.id}/docuseal_action/`, {
        action: 'resend'
      });
      await loadContracts();
      
      Swal.fire({
        icon: 'success',
        title: 'Resent!',
        text: 'Contract has been resent',
        timer: 2000,
        showConfirmButton: false
      });
    } catch (error) {
      console.error('Error resending contract:', error);
      Swal.fire({
        icon: 'error',
        title: 'Error',
        text: 'Failed to resend contract'
      });
    } finally {
      isSending.value = false;
    }
  }
};

const cancelContract = async (contract: Contract) => {
  const result = await Swal.fire({
    icon: 'warning',
    title: 'Cancel Contract?',
    text: 'This action cannot be undone',
    showCancelButton: true,
    confirmButtonColor: '#d33',
    confirmButtonText: 'Yes, cancel',
    cancelButtonText: 'Keep it'
  });

  if (result.isConfirmed) {
    try {
      await ApiService.post(`contracts/${contract.id}/docuseal_action/`, {
        action: 'cancel'
      });
      await loadContracts();
      
      Swal.fire({
        icon: 'success',
        title: 'Cancelled',
        text: 'Contract has been cancelled',
        timer: 2000,
        showConfirmButton: false
      });
    } catch (error) {
      console.error('Error cancelling contract:', error);
      Swal.fire({
        icon: 'error',
        title: 'Error',
        text: 'Failed to cancel contract'
      });
    }
  }
};

const downloadSignedDocument = async (contract: Contract) => {
  try {
    if (!contract.signed_document?.id) {
      Swal.fire({
        icon: 'warning',
        title: 'Not Available',
        text: 'Signed document is not available yet'
      });
      return;
    }

    // Download the signed document
    const response = await ApiService.vueInstance.axios({
      method: 'GET',
      url: `documents/${contract.signed_document.id}/download/`,
      responseType: 'blob'
    });
    
    // Create download link from blob
    const blob = new Blob([response.data], { type: 'application/pdf' });
    const url = window.URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.setAttribute('download', `${contract.title}_signed.pdf`);
    link.style.display = 'none';
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    window.URL.revokeObjectURL(url);
  } catch (error) {
    console.error('Error downloading signed document:', error);
    Swal.fire({
      icon: 'error',
      title: 'Error',
      text: 'Failed to download signed document'
    });
  }
};

onMounted(() => {
  loadContracts();
});
</script>