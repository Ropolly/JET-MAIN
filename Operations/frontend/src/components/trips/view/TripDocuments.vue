<template>
  <div>
    <!--begin::Header-->
    <div class="d-flex justify-content-between align-items-center mb-6">
      <!--begin::Title-->
      <div>
        <h2 class="fw-bold">Trip Documents</h2>
      </div>
      <!--end::Title-->

    </div>
    <!--end::Header-->

    <!-- Loading State -->
    <div v-if="isLoading" class="d-flex justify-content-center py-10">
      <div class="spinner-border text-primary" role="status">
        <span class="visually-hidden">Loading...</span>
      </div>
    </div>

    <!-- Documents Grid -->
    <div v-else class="row g-6 g-xl-9 mb-6 mb-xl-9">
      <!-- Add Document Card -->
      <div class="col-md-6 col-lg-4 col-xl-3">
        <!--begin::Card-->
        <div
          class="card h-100 flex-center border border-dashed p-8 bg-light-primary border-primary"
        >
          <!--begin::Image-->
          <img
            src="/media/svg/files/upload.svg"
            class="mb-5"
            alt=""
          >
          <!--end::Image-->

          <!--begin::Link-->
          <div class="dropdown">
            <a href="#" class="text-hover-primary fs-5 fw-bold mb-2 dropdown-toggle" data-bs-toggle="dropdown">
              Add Document
            </a>
            <ul class="dropdown-menu">
              <!-- Generate Documents Section -->
              <li v-if="availableDocTypes.length > 0">
                <h6 class="dropdown-header"><i class="fas fa-file-plus me-2"></i>Generate</h6>
              </li>
              <li v-for="docType in availableDocTypes" :key="'gen-' + docType.value">
                <a class="dropdown-item" href="#" @click.prevent="generateDocument(docType.value)">
                  <i class="fas fa-file me-2"></i>{{ docType.label }}
                </a>
              </li>

              <!-- Upload Documents Section -->
              <li v-if="availableUploadTypes.length > 0 && trip?.type === 'medical' && trip?.patient">
                <hr class="dropdown-divider" v-if="availableDocTypes.length > 0">
                <h6 class="dropdown-header"><i class="fas fa-upload me-2"></i>Upload</h6>
              </li>
              <li v-for="uploadType in availableUploadTypes" :key="'upload-' + uploadType.value" v-if="trip?.type === 'medical' && trip?.patient">
                <a class="dropdown-item" href="#" @click.prevent="handleDocumentAction({ type: 'upload', value: uploadType.value })">
                  <i :class="`fas fa-${uploadType.icon} me-2`"></i>{{ uploadType.label }}
                </a>
              </li>
            </ul>
          </div>
          <!--end::Link-->

          <!--begin::Description-->
          <div class="fs-7 fw-semibold text-gray-500">
            Generate or upload documents
          </div>
          <!--end::Description-->
        </div>
        <!--end::Card-->
      </div>
      <!--end::Add Document Card-->

      <!-- Generate Agreements Card -->
      <div class="col-md-6 col-lg-4 col-xl-3" v-if="availableContractTypes.length > 0 || hasAnyContracts">
        <!--begin::Card-->
        <div
          class="card h-100 flex-center border border-dashed p-8"
          :class="{
            'bg-light-warning border-warning': hasQuote,
            'bg-light-muted border-muted': !hasQuote
          }"
        >
          <!--begin::Image-->
          <img
            src="data:image/svg+xml,%3csvg%20width='67'%20height='67'%20viewBox='0%200%2067%2067'%20fill='none'%20xmlns='http://www.w3.org/2000/svg'%3e%3cpath%20opacity='0.25'%20d='M8.375%2011.167C8.375%206.54161%2012.1246%202.79199%2016.75%202.79199H43.9893C46.2105%202.79199%2048.3407%203.67436%2049.9113%205.24497L56.172%2011.5057C57.7426%2013.0763%2058.625%2015.2065%2058.625%2017.4277V55.8337C58.625%2060.459%2054.8754%2064.2087%2050.25%2064.2087H16.75C12.1246%2064.2087%208.375%2060.459%208.375%2055.8337V11.167Z'%20fill='%23FFC700'/%3e%3cpath%20d='M41.875%205.28162C41.875%203.90663%2042.9896%202.79199%2044.3646%202.79199V2.79199C46.3455%202.79199%2048.2452%203.57889%2049.6459%204.97957L56.4374%2011.7711C57.8381%2013.1718%2058.625%2015.0715%2058.625%2017.0524V17.0524C58.625%2018.4274%2057.5104%2019.542%2056.1354%2019.542H44.6667C43.1249%2019.542%2041.875%2018.2921%2041.875%2016.7503V5.28162Z'%20fill='%23FFC700'/%3e%3cpath%20d='M32.4311%2025.3368C32.1018%2025.4731%2031.7933%2025.675%2031.5257%2025.9427L23.1507%2034.3177C22.0605%2035.4079%2022.0605%2037.1755%2023.1507%2038.2657C24.2409%2039.3559%2026.0085%2039.3559%2027.0987%2038.2657L30.708%2034.6563V47.4583C30.708%2049.0001%2031.9579%2050.25%2033.4997%2050.25C35.0415%2050.25%2036.2913%2049.0001%2036.2913%2047.4583V34.6563L39.9007%2038.2657C40.9909%2039.3559%2042.7585%2039.3559%2043.8487%2038.2657C44.9389%2037.1755%2044.9389%2035.4079%2043.8487%2034.3177L35.4737%2025.9427C34.6511%2025.1201%2033.443%2024.9182%2032.4311%2025.3368Z'%20fill='%23FFC700'/%3e%3c/svg%3e"
            class="mb-5"
            alt=""
            :class="{ 'opacity-50': !hasQuote }"
          >
          <!--end::Image-->

          <!--begin::Link-->
          <div class="dropdown" v-if="hasQuote && availableContractTypes.length > 0">
            <a href="#" class="text-warning text-hover-warning fs-5 fw-bold mb-2 dropdown-toggle" data-bs-toggle="dropdown">
              Generate Agreements
            </a>
            <ul class="dropdown-menu">
              <!-- Generate All Option -->
              <li v-if="availableContractTypes.length > 1">
                <a class="dropdown-item" href="#" @click.prevent="generateAllContracts">
                  <i class="fas fa-plus-circle me-2 text-success"></i><strong>Generate All Agreements</strong>
                </a>
              </li>
              <li v-if="availableContractTypes.length > 1"><hr class="dropdown-divider"></li>

              <!-- Individual Contract Types -->
              <li v-for="contractType in contractTypes" :key="contractType.value">
                <a
                  class="dropdown-item"
                  href="#"
                  @click.prevent="generateContract(contractType.value)"
                  :class="{ 'disabled text-muted': !availableContractTypes.some(act => act.value === contractType.value) }"
                >
                  <i
                    :class="availableContractTypes.some(act => act.value === contractType.value)
                      ? 'fas fa-file-contract me-2'
                      : 'fas fa-check-circle me-2 text-success'"
                  ></i>
                  {{ contractType.label }}
                  <span
                    v-if="!availableContractTypes.some(act => act.value === contractType.value)"
                    class="badge badge-light-success ms-2"
                  >
                    Generated
                  </span>
                </a>
              </li>
            </ul>
          </div>
          <div v-else-if="hasQuote && availableContractTypes.length === 0">
            <span class="text-warning fs-5 fw-bold mb-2">
              All Agreements Generated
            </span>
          </div>
          <div v-else>
            <span class="fs-5 fw-bold mb-2 text-muted">
              Generate Agreements
            </span>
          </div>
          <!--end::Link-->

          <!--begin::Description-->
          <div class="fs-7 fw-semibold" :class="{
            'text-gray-500': hasQuote,
            'text-muted': !hasQuote
          }">
            {{
              !hasQuote
                ? 'Create a quote first'
                : availableContractTypes.length > 0
                ? 'Generate legal agreements'
                : 'All agreements completed'
            }}
          </div>
          <!--end::Description-->
        </div>
        <!--end::Card-->
      </div>
      <!--end::Generate Agreements Card-->

      <!--begin::Document Cards-->
      <div v-for="doc in documents" :key="doc.id" class="col-md-6 col-lg-4 col-xl-3">
        <!--begin::Card-->
        <div class="card h-100 position-relative">
          <!--begin::Delete Button-->
          <button
            type="button"
            class="position-absolute top-0 end-0 m-2 p-1 border-0 bg-transparent text-danger"
            @click="deleteDocument(doc)"
            title="Delete"
            style="z-index: 10; font-size: 18px; line-height: 1;"
          >
            <i class="fas fa-times"></i>
          </button>
          <!--end::Delete Button-->

          <!--begin::Card body-->
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
                {{ doc.document_type_display || formatDocType(doc.document_type) || 'Document' }}
              </div>
              <!--end::Title-->
            </a>
            <!--end::Name-->

            <!--begin::Description-->
            <div class="fs-7 fw-semibold text-gray-500">
              {{ formatDate(doc.created_on) }}
            </div>
            <!--end::Description-->
          </div>
          <!--end::Card body-->
        </div>
        <!--end::Card-->
      </div>
      <!--end::Document Cards-->
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
  document_type?: string;
  document_type_display?: string;
  file_path: string;
  created_on: string;
  created_by?: string;
  isContract?: boolean;
  contract_id?: string;
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
  { value: 'gendec', label: 'General Declaration', endpoint: 'generate_gen_dec' },
  { value: 'internal_itinerary', label: 'Internal Itinerary', endpoint: 'generate_documents' },
  { value: 'payment_agreement', label: 'Payment Agreement', endpoint: 'generate_contract', contract_type: 'payment_agreement' },
  { value: 'consent_transport', label: 'Consent for Transport', endpoint: 'generate_contract', contract_type: 'consent_transport' },
  { value: 'psa', label: 'Patient Service Agreement', endpoint: 'generate_contract', contract_type: 'psa' }
];

const uploadTypes = [
  { value: 'insurance_card', label: 'Insurance Card', icon: 'id-card' },
  { value: 'letter_of_medical_necessity', label: 'Medical Letter', icon: 'file-medical' }
];

const availableDocTypes = computed(() => {
  const existingTypes = documents.value.map(d => d.document_type);
  return documentTypes.filter(dt => !existingTypes.includes(dt.value));
});

const availableUploadTypes = computed(() => {
  const existingTypes = documents.value.map(d => d.document_type);
  return uploadTypes.filter(ut => !existingTypes.includes(ut.value));
});

const allAvailableActions = computed(() => {
  return [
    ...availableDocTypes.value.map(dt => ({ ...dt, type: 'generate' })),
    ...availableUploadTypes.value.map(ut => ({ ...ut, type: 'upload' }))
  ];
});

const contractTypes = [
  { value: 'payment_agreement', label: 'Payment Agreement' },
  { value: 'consent_transport', label: 'Consent for Transport' },
  { value: 'psa', label: 'Patient Service Agreement' }
];

const availableContractTypes = computed(() => {
  const existingTypes = documents.value
    .filter(d => d.isContract)
    .map(d => d.document_type);
  return contractTypes.filter(ct => !existingTypes.includes(ct.value));
});

const hasAnyContracts = computed(() => {
  return documents.value.some(d => d.isContract);
});

const allRequiredAgreementsGenerated = computed(() => {
  // Check if all contract types have been generated (no available contract types remaining)
  return availableContractTypes.value.length === 0 && hasAnyContracts.value;
});

const hasQuote = computed(() => {
  return !!(props.trip?.quote?.id);
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
  // Check if it's a contract first
  if (doc.isContract || (doc.document_type && ['payment_agreement', 'consent_transport', 'psa'].includes(doc.document_type))) {
    return '/media/svg/files/dcs.svg';
  }

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
  // Check if it's a contract first
  if (doc.isContract || (doc.document_type && ['payment_agreement', 'consent_transport', 'psa'].includes(doc.document_type))) {
    return '/media/svg/files/dcs-dark.svg';
  }

  const filename = doc.filename.toLowerCase();
  if (filename.endsWith('.pdf')) {
    return '/media/svg/files/pdf-dark.svg';
  } else if (filename.endsWith('.docx') || filename.endsWith('.doc')) {
    return '/media/svg/files/doc-dark.svg';
  } else {
    return '/media/svg/files/blank-image-dark.svg';
  }
};

const formatDocType = (type: string | undefined) => {
  if (!type) return 'Document';

  const docType = documentTypes.find(dt => dt.value === type);
  if (docType) {
    return docType.label;
  }

  // Fallback mapping for document types not in documentTypes array
  const typeMap: Record<string, string> = {
    'quote': 'Quote',
    'gendec': 'General Declaration',
    'customer_itinerary': 'Customer Itinerary',
    'internal_itinerary': 'Internal Itinerary',
    'payment_agreement': 'Payment Agreement',
    'consent_transport': 'Consent for Transport',
    'psa': 'Patient Service Agreement',
    'handling_request': 'Handling Request',
    'letter_of_medical_necessity': 'Letter of Medical Necessity',
    'insurance_card': 'Insurance Card'
  };

  return typeMap[type] || type.charAt(0).toUpperCase() + type.slice(1).replace(/_/g, ' ');
};

const formatDate = (date: string) => {
  if (!date) return '';
  return formatDistanceToNow(new Date(date), { addSuffix: true });
};

const loadDocuments = async () => {
  isLoading.value = true;
  try {
    // Load documents first
    const documentsResponse = await ApiService.get(`trips/${props.tripId}/documents/`);
    let allDocuments = [...documentsResponse.data];

    // Patient documents are now included in the trip's documents endpoint
    // No need to load them separately from the patient object
    // The backend creates trip-specific patient documents that will be loaded above

    // Try to load contracts with proper error handling
    let contractsData = [];
    try {
      const contractsResponse = await ApiService.get(`contracts/?trip=${props.tripId}`);
      console.log('Contracts response:', contractsResponse); // Debug logging

      // Handle both paginated and non-paginated responses
      if (contractsResponse.data && Array.isArray(contractsResponse.data.results)) {
        contractsData = contractsResponse.data.results;
      } else if (contractsResponse.data && Array.isArray(contractsResponse.data)) {
        contractsData = contractsResponse.data;
      } else {
        console.log('No contracts found or unexpected response format:', contractsResponse.data);
        contractsData = [];
      }
    } catch (contractError) {
      console.log('Error loading contracts (continuing without them):', contractError);
      contractsData = [];
    }

    // Add contracts to documents
    allDocuments = [
      ...allDocuments,
      ...contractsData.map((contract: any) => ({
        id: contract.id,
        filename: contract.signed_document?.filename || contract.unsigned_document?.filename || 'contract.pdf',
        document_type: contract.contract_type,
        document_type_display: contract.contract_type_display || formatDocType(contract.contract_type),
        created_on: contract.created_on,
        created_by: contract.created_by,
        file_path: contract.signed_document?.file_path || contract.unsigned_document?.file_path,
        isContract: true,
        contract_id: contract.id
      }))
    ];

    // Remove duplicates by ID (in case same document appears from multiple sources)
    const uniqueDocuments = allDocuments.filter((doc, index, self) =>
      index === self.findIndex(d => d.id === doc.id)
    );

    documents.value = uniqueDocuments;
    console.log('All documents loaded:', allDocuments); // Debug logging
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
    } else if (documentType === 'customer_itinerary' || documentType === 'handling_request' || documentType === 'gendec') {
      // For trip-based documents with dedicated endpoints
      endpoint = `trips/${props.tripId}/${docTypeConfig.endpoint}/`;
    } else if (documentType === 'internal_itinerary') {
      // For new document types that use the generic generate_documents endpoint
      endpoint = `trips/${props.tripId}/generate_documents/`;
      requestData = { document_type: documentType };
    } else if (docTypeConfig.contract_type) {
      // For contracts, use the generate_contract endpoint
      endpoint = `trips/${props.tripId}/generate_contract/`;
      requestData = { contract_type: docTypeConfig.contract_type };
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

const handleDocumentAction = async (action: any) => {
  if (action.type === 'generate') {
    await generateDocument(action.value);
  } else if (action.type === 'upload') {
    if (action.value === 'insurance_card') {
      triggerInsuranceCardUpload();
    } else if (action.value === 'letter_of_medical_necessity') {
      triggerMedicalLetterUpload();
    }
  }
};

const generateContract = async (contractType: string) => {
  isGeneratingDocs.value = true;
  try {
    // Use the trip's generate_contract endpoint
    await ApiService.post(`trips/${props.tripId}/generate_contract/`, {
      contract_type: contractType
    });

    await loadDocuments();

    Swal.fire({
      icon: 'success',
      title: 'Success',
      text: 'Agreement generated successfully',
      timer: 2000,
      showConfirmButton: false
    });
  } catch (error: any) {
    console.error('Error generating agreement:', error);
    Swal.fire({
      icon: 'error',
      title: 'Error',
      text: error.message || 'Failed to generate agreement'
    });
  } finally {
    isGeneratingDocs.value = false;
  }
};

const generateAllContracts = async () => {
  if (availableContractTypes.value.length === 0) {
    Swal.fire({
      icon: 'info',
      title: 'Info',
      text: 'All agreements have already been generated'
    });
    return;
  }

  isGeneratingDocs.value = true;
  try {
    let generatedCount = 0;
    const errors = [];

    // Generate each available contract type
    for (const contractType of availableContractTypes.value) {
      try {
        await ApiService.post(`trips/${props.tripId}/generate_contract/`, {
          contract_type: contractType.value
        });
        generatedCount++;
      } catch (error: any) {
        console.error(`Error generating ${contractType.label}:`, error);
        errors.push(`${contractType.label}: ${error.message || 'Unknown error'}`);
      }
    }

    await loadDocuments();

    if (errors.length === 0) {
      Swal.fire({
        icon: 'success',
        title: 'Success',
        text: `${generatedCount} agreements generated successfully`,
        timer: 2000,
        showConfirmButton: false
      });
    } else {
      Swal.fire({
        icon: 'warning',
        title: 'Partial Success',
        html: `${generatedCount} agreements generated successfully.<br><br>Errors:<br>${errors.join('<br>')}`
      });
    }
  } catch (error: any) {
    console.error('Error generating agreements:', error);
    Swal.fire({
      icon: 'error',
      title: 'Error',
      text: 'Failed to generate agreements'
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
    // Try to use the comprehensive generate_documents endpoint first
    // Note: The backend's generate_documents endpoint may not include gen_dec,
    // so we'll use the legacy approach for now to ensure all documents are generated
    await generateAllDocumentsLegacy();
  } catch (error: any) {
    console.error('Error generating documents:', error);
    Swal.fire({
      icon: 'error',
      title: 'Error',
      text: error.response?.data?.error || error.message || 'Failed to generate documents'
    });
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

    // Generate general declaration document
    promises.push(
      ApiService.post(`trips/${props.tripId}/generate_gen_dec/`)
        .then(() => generatedCount++)
        .catch(err => console.error('Error generating general declaration:', err))
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
    // Handle patient documents (insurance card and medical letter)
    if (doc.document_type === 'insurance_card' || doc.document_type === 'letter_of_medical_necessity') {
      // Construct media URL from file_path for patient documents
      if (doc.file_path) {
        const mediaUrl = `http://localhost:8001/media/${doc.file_path.startsWith('patient_documents/') ? doc.file_path : `patient_documents/${doc.file_path}`}`;
        window.open(mediaUrl, '_blank');
        return;
      }
    }

    // Handle contracts differently - they use DocuSeal for signing
    if (doc.isContract) {
      try {
        // For contracts, we need to open the signing URL from DocuSeal
        // Check if there's a signing URL in the response data
        const contractResponse = await ApiService.get(`contracts/${doc.contract_id}/`);
        const contract = contractResponse.data;

        console.log('Contract data:', contract);

        // Check for DocuSeal signing URL in response data (look for submitters, not signers)
        if (contract.docuseal_response_data && contract.docuseal_response_data.submitters && contract.docuseal_response_data.submitters.length > 0) {
          const submitters = contract.docuseal_response_data.submitters;

          // First, try to find JET ICU submitter (contracts@jeticu.com)
          const jetIcuSubmitter = submitters.find((submitter: any) =>
            submitter.email === 'contracts@jeticu.com'
          );

          if (jetIcuSubmitter?.embed_src) {
            window.open(jetIcuSubmitter.embed_src, '_blank');
            return;
          }

          // Fallback to first submitter with embed_src
          const firstSubmitterWithLink = submitters.find((submitter: any) => submitter.embed_src);
          if (firstSubmitterWithLink?.embed_src) {
            window.open(firstSubmitterWithLink.embed_src, '_blank');
            return;
          }
        }

        // Additional fallback: construct link from submission ID if available
        if (contract.docuseal_submission_id) {
          window.open(`https://docuseal.com/submissions/${contract.docuseal_submission_id}`, '_blank');
          return;
        }

        // Fallback to document download if no signing URL
        if (contract.signed_document?.id) {
          // Use signed document if available
          console.log('Opening signed document:', contract.signed_document.id);
          await downloadDocumentFile(contract.signed_document.id);
        } else if (contract.unsigned_document?.id) {
          // Use unsigned document as fallback
          console.log('Opening unsigned document:', contract.unsigned_document.id);
          await downloadDocumentFile(contract.unsigned_document.id);
        } else {
          // No document or signing URL available
          Swal.fire({
            icon: 'info',
            title: 'Contract Not Available',
            text: 'This contract has not been generated yet or is not available for viewing.'
          });
          return;
        }
      } catch (contractError) {
        console.error('Error fetching contract details:', contractError);
        Swal.fire({
          icon: 'error',
          title: 'Error',
          text: 'Failed to access contract details'
        });
        return;
      }
    } else {
      // Handle regular documents
      await downloadDocumentFile(doc.id);
    }
  } catch (error) {
    console.error('Error opening document:', error);
    let errorMessage = 'Failed to open document';

    if (error.response && error.response.status === 404) {
      errorMessage = 'Document file not found. It may have been moved or deleted.';
    } else if (error.response && error.response.status === 403) {
      errorMessage = 'You do not have permission to access this document.';
    }

    Swal.fire({
      icon: 'error',
      title: 'Error',
      text: errorMessage
    });
  }
};

const downloadDocumentFile = async (documentId: string) => {
  try {
    // Use the new view endpoint that doesn't force download
    const response = await ApiService.vueInstance.axios({
      method: 'GET',
      url: `documents/${documentId}/view/`,
      responseType: 'blob'
    });

    // Determine the correct MIME type based on the response
    const contentType = response.headers['content-type'] || 'application/octet-stream';

    // Create object URL from blob with correct type
    const blob = new Blob([response.data], { type: contentType });
    const url = window.URL.createObjectURL(blob);

    // Open in new tab
    window.open(url, '_blank');

    // Clean up object URL after a short delay to allow the browser to load it
    setTimeout(() => {
      window.URL.revokeObjectURL(url);
    }, 1000);
  } catch (error) {
    console.error('Error viewing document file:', error);
    throw error;
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