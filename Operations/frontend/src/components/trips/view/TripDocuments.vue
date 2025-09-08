<template>
  <div class="card">
    <div class="card-header">
      <h3 class="card-title">Trip Documents</h3>
      <div class="card-toolbar">
        <button
          type="button"
          class="btn btn-sm btn-light-primary"
          @click="generateAllDocuments"
          :disabled="isGenerating"
        >
          <span v-if="!isGenerating">
            <i class="fas fa-file-plus fs-4 me-2"></i>
            Generate All Documents
          </span>
          <span v-else>
            <span class="spinner-border spinner-border-sm me-2" role="status"></span>
            Generating...
          </span>
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
}

const props = defineProps<Props>();

const documents = ref<Document[]>([]);
const isLoading = ref(false);
const isGenerating = ref(false);

const documentTypes = [
  { value: 'gendec', label: 'General Declaration' },
  { value: 'quote', label: 'Quote Form' },
  { value: 'customer_itinerary', label: 'Customer Itinerary' },
  { value: 'internal_itinerary', label: 'Internal Itinerary' },
  { value: 'payment_agreement', label: 'Payment Agreement' },
  { value: 'consent_transport', label: 'Consent for Transport' },
  { value: 'psa', label: 'Patient Service Agreement' },
  { value: 'handling_request', label: 'Handling Request' }
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
  isGenerating.value = true;
  try {
    await ApiService.post(`trips/${props.tripId}/generate_documents/`, {
      document_type: documentType
    });
    
    await loadDocuments();
    
    Swal.fire({
      icon: 'success',
      title: 'Success',
      text: 'Document generated successfully',
      timer: 2000,
      showConfirmButton: false
    });
  } catch (error) {
    console.error('Error generating document:', error);
    Swal.fire({
      icon: 'error',
      title: 'Error',
      text: 'Failed to generate document'
    });
  } finally {
    isGenerating.value = false;
  }
};

const generateAllDocuments = async () => {
  isGenerating.value = true;
  try {
    await ApiService.post(`trips/${props.tripId}/generate_documents/`);
    
    await loadDocuments();
    
    Swal.fire({
      icon: 'success',
      title: 'Success',
      text: 'All documents generated successfully',
      timer: 2000,
      showConfirmButton: false
    });
  } catch (error) {
    console.error('Error generating documents:', error);
    Swal.fire({
      icon: 'error',
      title: 'Error',
      text: 'Failed to generate documents'
    });
  } finally {
    isGenerating.value = false;
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

onMounted(() => {
  loadDocuments();
});
</script>