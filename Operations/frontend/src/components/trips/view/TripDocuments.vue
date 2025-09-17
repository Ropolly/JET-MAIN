<template>
  <div class="card">
    <div class="card-header">
      <h3 class="card-title">Trip Documents</h3>
      <div class="card-toolbar">
        <div class="dropdown">
          <button
            class="btn btn-sm btn-light-primary dropdown-toggle"
            type="button"
            data-bs-toggle="dropdown"
            :disabled="isGenerating"
          >
            <span v-if="!isGenerating">
              <i class="fas fa-cogs fs-4 me-2"></i>
              Actions
            </span>
            <span v-else>
              <span class="spinner-border spinner-border-sm me-2" role="status"></span>
              Processing...
            </span>
          </button>
          <ul class="dropdown-menu">
            <li>
              <a class="dropdown-item" href="#" @click.prevent="generateAllDocuments">
                <i class="fas fa-file-plus me-2"></i>
                Generate All Documents
              </a>
            </li>
            <div v-if="trip?.type === 'medical' && trip?.patient" class="dropdown-divider"></div>
            <li v-if="trip?.type === 'medical' && trip?.patient">
              <a class="dropdown-item" href="#" @click.prevent="triggerInsuranceCardUpload">
                <i class="fas fa-id-card me-2"></i>
                Upload Insurance Card
              </a>
            </li>
            <li v-if="trip?.type === 'medical' && trip?.patient">
              <a class="dropdown-item" href="#" @click.prevent="triggerMedicalLetterUpload">
                <i class="fas fa-file-medical me-2"></i>
                Upload Medical Letter
              </a>
            </li>
          </ul>
        </div>
      </div>
    </div>
    <div class="card-body">
      <!-- Loading State -->
      <div v-if="isLoading" class="d-flex justify-content-center py-10">
        <div class="spinner-border text-primary" role="status">
          <span class="visually-hidden">Loading...</span>
        </div>
      </div>

      <!-- No Documents State -->
      <div v-else-if="documents.length === 0" class="text-center py-10">
        <i class="fas fa-folder-open fs-3x text-muted mb-4"></i>
        <p class="text-muted">No documents generated yet</p>
        <button
          type="button"
          class="btn btn-primary"
          @click="generateAllDocuments"
          :disabled="isGenerating"
        >
          <i class="fas fa-file-plus fs-4 me-2"></i>
          Generate Documents
        </button>
      </div>

      <!-- Documents Grid -->
      <div v-else class="row g-5 g-xl-8">
        <div v-for="doc in documents" :key="doc.id" class="col-xl-6 col-lg-6 col-md-6 col-sm-12">
          <div class="card">
            <div class="card-body d-flex justify-content-center text-center flex-column p-8">
              <!--begin::Name-->
              <a href="#" @click.prevent="downloadDocument(doc)" class="text-gray-800 text-hover-primary d-flex flex-column">
                <!--begin::Image-->
                <div class="symbol symbol-60px mb-5">
                  <img :src="getDocumentImage(doc)" class="theme-light-show" :alt="doc.document_type">
                  <img :src="getDocumentImageDark(doc)" class="theme-dark-show" :alt="doc.document_type">
                </div>
                <!--end::Image-->

                <!--begin::Title-->
                <div class="fs-5 fw-bold mb-2">
                  {{ doc.document_type_display || formatDocType(doc.document_type) }}
                </div>
                <!--end::Title-->
              </a>
              <!--end::Name-->

              <!--begin::Filename-->
              <div class="fs-6 fw-semibold text-gray-600 mb-2 text-truncate" :title="doc.filename">
                {{ doc.filename }}
              </div>
              <!--end::Filename-->

              <!--begin::Description-->
              <div class="fs-7 fw-semibold text-gray-500 mb-4">
                {{ formatDate(doc.created_on) }}
              </div>
              <!--end::Description-->

              <!--begin::Actions-->
              <div class="d-flex justify-content-center gap-2">
                <button
                  type="button"
                  class="btn btn-sm btn-light-warning"
                  @click="regenerateDocument(doc.document_type)"
                  :disabled="isGenerating"
                  title="Regenerate"
                >
                  <i class="fas fa-sync-alt"></i>
                </button>
                <button
                  type="button"
                  class="btn btn-sm btn-light-danger"
                  @click="deleteDocument(doc)"
                  title="Delete"
                >
                  <i class="fas fa-trash"></i>
                </button>
              </div>
              <!--end::Actions-->
            </div>
          </div>
        </div>

        <!-- Add Document Card -->
        <div class="col-xl-6 col-lg-6 col-md-6 col-sm-12">
          <div class="card border-2 border-dashed border-primary bg-light-primary">
            <div class="card-body d-flex justify-content-center text-center flex-column p-8">
              <!--begin::Image-->
              <div class="symbol symbol-60px mb-5">
                <i class="fas fa-plus-circle fs-3x text-primary"></i>
              </div>
              <!--end::Image-->

              <!--begin::Title-->
              <div class="fs-5 fw-bold text-primary mb-2">Generate Document</div>
              <!--end::Title-->

              <!--begin::Description-->
              <div class="fs-7 fw-semibold text-gray-500 mb-4">
                Select document type
              </div>
              <!--end::Description-->

              <!--begin::Actions-->
              <div class="dropdown">
                <button
                  class="btn btn-sm btn-primary dropdown-toggle"
                  type="button"
                  data-bs-toggle="dropdown"
                  :disabled="isGenerating"
                >
                  Select Type
                </button>
                <ul class="dropdown-menu">
                  <li v-for="docType in availableDocTypes" :key="docType.value">
                    <a class="dropdown-item" href="#" @click.prevent="generateDocument(docType.value)">
                      {{ docType.label }}
                    </a>
                  </li>
                </ul>
              </div>
              <!--end::Actions-->
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Hidden file inputs for patient document uploads -->
    <input
      type="file"
      ref="insuranceCardInput"
      @change="handleInsuranceCardUpload"
      class="d-none"
      accept=".pdf,.jpg,.jpeg,.png"
    />
    <input
      type="file"
      ref="medicalLetterInput"
      @change="handleMedicalLetterUpload"
      class="d-none"
      accept=".pdf,.jpg,.jpeg,.png"
    />
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue';
import ApiService from '@/core/services/ApiService';
import Swal from 'sweetalert2';
import { formatDistanceToNow } from 'date-fns';

interface Document {
  id: string;
  filename: string;
  document_type: string;
  document_type_display?: string;
  file_path: string;
  created_on: string;
  created_by?: string;
}

interface Props {
  tripId: string;
  trip?: any; // Trip object with quote information
}

const props = defineProps<Props>();

const documents = ref<Document[]>([]);
const isLoading = ref(false);

// Patient document upload refs
const insuranceCardInput = ref<HTMLInputElement>();
const medicalLetterInput = ref<HTMLInputElement>();
const isUploadingInsuranceCard = ref(false);
const isUploadingMedicalLetter = ref(false);
const isGeneratingDocs = ref(false);

const documentTypes = [
  { value: 'quote', label: 'Quote Form', endpoint: 'generate_quote_document' },
  { value: 'customer_itinerary', label: 'Customer Itinerary', endpoint: 'generate_itineraries' },
  { value: 'handling_request', label: 'Handling Request', endpoint: 'generate_handling_requests' },
  { value: 'gendec', label: 'General Declaration', endpoint: 'generate_documents' },
  { value: 'internal_itinerary', label: 'Internal Itinerary', endpoint: 'generate_documents' }
];

const availableDocTypes = computed(() => {
  const existingTypes = documents.value.map(d => d.document_type);
  return documentTypes.filter(dt => !existingTypes.includes(dt.value));
});

const getDocumentIcon = (doc: Document) => {
  const filename = doc.filename.toLowerCase();
  if (filename.endsWith('.pdf')) {
    return 'fas fa-file-pdf text-danger';
  } else if (filename.endsWith('.docx') || filename.endsWith('.doc')) {
    return 'fas fa-file-word text-primary';
  } else {
    return 'fas fa-file text-muted';
  }
};

const getDocumentImage = (doc: Document) => {
  const filename = doc.filename.toLowerCase();
  if (filename.endsWith('.pdf')) {
    return '/media/svg/files/pdf.svg';
  } else if (filename.endsWith('.docx') || filename.endsWith('.doc')) {
    return '/media/svg/files/doc.svg';
  } else {
    return '/media/svg/files/blank-image.svg';
  }
};

const getDocumentImageDark = (doc: Document) => {
  const filename = doc.filename.toLowerCase();
  if (filename.endsWith('.pdf')) {
    return '/media/svg/files/pdf-dark.svg';
  } else if (filename.endsWith('.docx') || filename.endsWith('.doc')) {
    return '/media/svg/files/doc-dark.svg';
  } else {
    return '/media/svg/files/blank-image-dark.svg';
  }
};

const formatDocType = (type: string) => {
  const docType = documentTypes.find(dt => dt.value === type);
  return docType ? docType.label : type;
};

const formatDate = (date: string) => {
  if (!date) return '';
  return formatDistanceToNow(new Date(date), { addSuffix: true });
};

const loadDocuments = async () => {
  isLoading.value = true;
  try {
    const response = await ApiService.get(`trips/${props.tripId}/documents/`);
    documents.value = response.data;
  } catch (error) {
    console.error('Error loading documents:', error);
    Swal.fire({
      icon: 'error',
      title: 'Error',
      text: 'Failed to load documents'
    });
  } finally {
    isLoading.value = false;
  }
};

const generateDocument = async (documentType: string) => {
  isGeneratingDocs.value = true;
  try {
    const docTypeConfig = documentTypes.find(dt => dt.value === documentType);
    if (!docTypeConfig) {
      throw new Error(`Unknown document type: ${documentType}`);
    }

    let endpoint = '';
    let requestData = {};
    
    // Determine the correct endpoint based on document type
    if (documentType === 'quote' && props.trip?.quote?.id) {
      // For quotes, use the quote endpoint
      endpoint = `quotes/${props.trip.quote.id}/${docTypeConfig.endpoint}/`;
    } else if (documentType === 'customer_itinerary' || documentType === 'handling_request') {
      // For legacy trip-based documents, use the specific endpoints
      endpoint = `trips/${props.tripId}/${docTypeConfig.endpoint}/`;
    } else if (documentType === 'gendec' || documentType === 'internal_itinerary') {
      // For new document types, use the generate_documents endpoint
      endpoint = `trips/${props.tripId}/generate_documents/`;
      requestData = { document_type: documentType };
    } else {
      throw new Error(`Cannot generate ${documentType}: ${documentType === 'quote' ? 'No quote found for this trip' : 'Invalid document type'}`);
    }

    await ApiService.post(endpoint, requestData);
    
    await loadDocuments();
    
    Swal.fire({
      icon: 'success',
      title: 'Success',
      text: 'Document generated successfully',
      timer: 2000,
      showConfirmButton: false
    });
  } catch (error: any) {
    console.error('Error generating document:', error);
    Swal.fire({
      icon: 'error',
      title: 'Error',
      text: error.message || 'Failed to generate document'
    });
  } finally {
    isGeneratingDocs.value = false;
  }
};

// Update the isGenerating computed to include upload states
const isGenerating = computed(() => {
  return isUploadingInsuranceCard.value || isUploadingMedicalLetter.value || isGeneratingDocs.value;
});

const generateAllDocuments = async () => {
  // Prevent multiple simultaneous generations
  if (isGenerating.value) {
    return;
  }

  isGeneratingDocs.value = true;
  try {
    // Use the comprehensive generate_documents endpoint for all documents
    // This single endpoint generates all applicable documents atomically
    const response = await ApiService.post(`trips/${props.tripId}/generate_documents/`);
    
    await loadDocuments();
    
    const documentCount = response.data?.documents?.length || 0;
    
    Swal.fire({
      icon: 'success',
      title: 'Success',
      text: `${documentCount} documents generated successfully`,
      timer: 2000,
      showConfirmButton: false
    });
  } catch (error: any) {
    console.error('Error generating documents:', error);
    
    // Fallback to individual document generation if the new endpoint fails
    if (error.response?.status === 404 || error.response?.status === 405) {
      await generateAllDocumentsLegacy();
    } else {
      Swal.fire({
        icon: 'error',
        title: 'Error',
        text: error.response?.data?.error || error.message || 'Failed to generate documents'
      });
    }
  } finally {
    isGeneratingDocs.value = false;
  }
};

// Legacy fallback method for individual document generation
const generateAllDocumentsLegacy = async () => {
  try {
    const promises = [];
    let generatedCount = 0;

    // Generate quote document if trip has a quote
    if (props.trip?.quote?.id) {
      promises.push(
        ApiService.post(`quotes/${props.trip.quote.id}/generate_quote_document/`)
          .then(() => generatedCount++)
          .catch(err => console.error('Error generating quote:', err))
      );
    }

    // Generate trip-based documents
    promises.push(
      ApiService.post(`trips/${props.tripId}/generate_itineraries/`)
        .then(() => generatedCount++)
        .catch(err => console.error('Error generating itineraries:', err))
    );

    promises.push(
      ApiService.post(`trips/${props.tripId}/generate_handling_requests/`)
        .then(() => generatedCount++)
        .catch(err => console.error('Error generating handling requests:', err))
    );

    // Wait for all document generation calls to complete
    await Promise.all(promises);
    
    await loadDocuments();
    
    Swal.fire({
      icon: 'success',
      title: 'Success',
      text: `${generatedCount} documents generated successfully`,
      timer: 2000,
      showConfirmButton: false
    });
  } catch (error) {
    console.error('Error generating documents (legacy):', error);
    Swal.fire({
      icon: 'error',
      title: 'Error',
      text: 'Failed to generate documents'
    });
  }
};

const regenerateDocument = async (documentType: string) => {
  const result = await Swal.fire({
    icon: 'warning',
    title: 'Regenerate Document?',
    text: 'This will replace the existing document',
    showCancelButton: true,
    confirmButtonText: 'Yes, regenerate',
    cancelButtonText: 'Cancel'
  });

  if (result.isConfirmed) {
    await generateDocument(documentType);
  }
};

const downloadDocument = async (doc: Document) => {
  try {
    // Use axios with proper blob configuration and authorization
    const response = await ApiService.vueInstance.axios({
      method: 'GET',
      url: `documents/${doc.id}/download/`,
      responseType: 'blob'
    });
    
    // Create download link from blob
    const blob = new Blob([response.data]);
    const url = window.URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.setAttribute('download', doc.filename);
    link.style.display = 'none';
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    window.URL.revokeObjectURL(url);
  } catch (error) {
    console.error('Error downloading document:', error);
    Swal.fire({
      icon: 'error',
      title: 'Error',
      text: 'Failed to download document'
    });
  }
};

const deleteDocument = async (doc: Document) => {
  const result = await Swal.fire({
    icon: 'warning',
    title: 'Delete Document?',
    text: 'This action cannot be undone',
    showCancelButton: true,
    confirmButtonColor: '#d33',
    confirmButtonText: 'Yes, delete',
    cancelButtonText: 'Cancel'
  });

  if (result.isConfirmed) {
    try {
      await ApiService.delete(`documents/${doc.id}/`);
      await loadDocuments();
      
      Swal.fire({
        icon: 'success',
        title: 'Deleted',
        text: 'Document has been deleted',
        timer: 2000,
        showConfirmButton: false
      });
    } catch (error) {
      console.error('Error deleting document:', error);
      Swal.fire({
        icon: 'error',
        title: 'Error',
        text: 'Failed to delete document'
      });
    }
  }
};

// Patient document upload trigger methods
const triggerInsuranceCardUpload = () => {
  if (insuranceCardInput.value) {
    insuranceCardInput.value.click();
  }
};

const triggerMedicalLetterUpload = () => {
  if (medicalLetterInput.value) {
    medicalLetterInput.value.click();
  }
};

// Patient document upload handlers
const handleInsuranceCardUpload = async (event: Event) => {
  const target = event.target as HTMLInputElement;
  const file = target.files?.[0];

  if (!file || !props.trip?.patient) return;

  try {
    isUploadingInsuranceCard.value = true;

    const formData = new FormData();
    formData.append('file', file);
    formData.append('document_type', 'insurance_card');
    formData.append('trip_id', props.tripId);

    await ApiService.upload(`/patients/${props.trip.patient.id}/upload_document/`, formData);

    Swal.fire({
      title: "Success!",
      text: "Insurance card uploaded successfully.",
      icon: "success",
      confirmButtonText: "OK"
    });

    // Refresh documents to include the new upload
    await loadDocuments();

    // Clear the file input
    if (insuranceCardInput.value) {
      insuranceCardInput.value.value = '';
    }

  } catch (error: any) {
    console.error('Error uploading insurance card:', error);
    Swal.fire({
      title: "Error",
      text: error.response?.data?.error || "Failed to upload insurance card. Please try again.",
      icon: "error",
      confirmButtonText: "OK"
    });
  } finally {
    isUploadingInsuranceCard.value = false;
  }
};

const handleMedicalLetterUpload = async (event: Event) => {
  const target = event.target as HTMLInputElement;
  const file = target.files?.[0];

  if (!file || !props.trip?.patient) return;

  try {
    isUploadingMedicalLetter.value = true;

    const formData = new FormData();
    formData.append('file', file);
    formData.append('document_type', 'letter_of_medical_necessity');
    formData.append('trip_id', props.tripId);

    await ApiService.upload(`/patients/${props.trip.patient.id}/upload_document/`, formData);

    Swal.fire({
      title: "Success!",
      text: "Letter of medical necessity uploaded successfully.",
      icon: "success",
      confirmButtonText: "OK"
    });

    // Refresh documents to include the new upload
    await loadDocuments();

    // Clear the file input
    if (medicalLetterInput.value) {
      medicalLetterInput.value.value = '';
    }

  } catch (error: any) {
    console.error('Error uploading medical letter:', error);
    Swal.fire({
      title: "Error",
      text: error.response?.data?.error || "Failed to upload letter of medical necessity. Please try again.",
      icon: "error",
      confirmButtonText: "OK"
    });
  } finally {
    isUploadingMedicalLetter.value = false;
  }
};

onMounted(() => {
  loadDocuments();
});
</script>