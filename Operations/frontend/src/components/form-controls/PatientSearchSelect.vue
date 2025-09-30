<template>
  <div class="patient-search-select">
    <label v-if="label" :class="`fs-6 fw-semibold mb-2 ${required ? 'required' : ''}`">
      {{ label }}
    </label>
    
    <div class="d-flex">
      <div class="position-relative flex-grow-1">
        <!-- Search Input -->
        <input
          ref="searchInput"
          v-model="searchTerm"
          @input="handleSearch"
          @focus="handleFocus"
          @blur="handleBlur"
          @keydown.down.prevent="navigateDown"
          @keydown.up.prevent="navigateUp"
          @keydown.enter.prevent="selectHighlighted"
          @keydown.escape="hideDropdown"
          type="text"
          :class="`form-control form-control-solid me-2 ${dropdownVisible ? 'dropdown-open' : ''}`"
          :placeholder="placeholder"
          :disabled="disabled"
          autocomplete="off"
        />
      
      <!-- Loading Spinner -->
      <div v-if="loading" class="position-absolute top-50 end-0 translate-middle-y me-3">
        <span class="spinner-border spinner-border-sm" role="status"></span>
      </div>
      
      <!-- Clear Button -->
      <div v-if="selectedPatient && !loading" class="position-absolute top-50 end-0 translate-middle-y me-3">
        <button
          type="button" 
          @click="clearSelection"
          class="btn btn-sm btn-icon btn-active-light-primary"
        >
          <KTIcon icon-name="cross" icon-class="fs-4" />
        </button>
      </div>
      
      <!-- Search Icon -->
      <div v-if="!selectedPatient && !loading" class="position-absolute top-50 end-0 translate-middle-y me-5">
        <KTIcon icon-name="magnifier" icon-class="fs-4 text-muted" />
      </div>
      </div>

      <!-- Create New Patient Button -->
      <button
        type="button"
        class="btn btn-light-primary btn-sm"
        @click="createNewPatient"
        :disabled="disabled"
        title="Create New Patient"
      >
        <KTIcon icon-name="plus" icon-class="fs-6" />
      </button>
    </div>
    
    <!-- Selected Patient Display -->
    <div v-if="selectedPatient" class="mt-3 p-3 bg-light-success rounded border border-success border-dashed">
      <div class="d-flex align-items-center">
        <div class="symbol symbol-40px me-3">
          <div class="symbol-label bg-light-success">
            <i class="ki-duotone ki-people fs-4 text-success">
              <span class="path1"></span>
              <span class="path2"></span>
              <span class="path3"></span>
              <span class="path4"></span>
              <span class="path5"></span>
            </i>
          </div>
        </div>
        
        <div class="flex-grow-1">
          <div class="d-flex align-items-center">
            <a 
              href="#" 
              @click.prevent="openPatientDetails" 
              class="fw-bold text-success text-hover-success me-2 text-decoration-underline"
            >
              {{ getPatientDisplayName(selectedPatient) }}
            </a>
            <span class="badge badge-success fs-8">Patient</span>
          </div>
          <div class="text-muted fs-7" v-if="selectedPatient.info?.email">
            {{ selectedPatient.info.email }}
          </div>
        </div>
      </div>
    </div>
    
    <!-- Dropdown Results -->
    <div
      v-if="dropdownVisible"
      class="position-absolute w-100 bg-white border border-gray-300 rounded-bottom shadow-sm mt-1"
      style="z-index: 1050; max-height: 300px; overflow-y: auto;"
    >
      <!-- No Results -->
      <div v-if="searchResults.length === 0 && searchTerm.length >= 2 && !loading" class="p-3 text-muted text-center">
        <i class="ki-duotone ki-people fs-2 text-muted mb-2">
          <span class="path1"></span>
          <span class="path2"></span>
          <span class="path3"></span>
          <span class="path4"></span>
          <span class="path5"></span>
        </i>
        <div>No patients found for "{{ searchTerm }}"</div>
        <small>Try searching by name or email</small>
      </div>
      
      <!-- Search Prompt -->
      <div v-if="searchTerm.length < 2 && !selectedPatient" class="p-3 text-muted text-center">
        <KTIcon icon-name="magnifier" icon-class="fs-2 text-muted mb-2" />
        <div>Type at least 2 characters to search</div>
        <small>Search by name or email</small>
      </div>
      
      <!-- Search Results -->
      <div v-for="(patient, index) in searchResults" 
           :key="patient.id" 
           :class="`patient-option p-3 border-bottom border-gray-200 cursor-pointer ${index === highlightedIndex ? 'bg-light-primary' : ''}`"
           @click="selectPatient(patient)"
           @mouseenter="highlightedIndex = index">
        
        <div class="d-flex align-items-center">
          <div class="symbol symbol-40px me-3">
            <div class="symbol-label bg-light-info">
              <i class="ki-duotone ki-people fs-4 text-info">
                <span class="path1"></span>
                <span class="path2"></span>
                <span class="path3"></span>
                <span class="path4"></span>
                <span class="path5"></span>
              </i>
            </div>
          </div>
          
          <div class="flex-grow-1">
            <div class="d-flex align-items-center">
              <span class="fw-bold text-gray-800 me-2">{{ getPatientDisplayName(patient) }}</span>
              <span class="badge badge-info fs-8">Patient</span>
            </div>
            <div class="text-muted fs-7" v-if="patient.info?.email">
              {{ patient.info.email }}
            </div>
          </div>
        </div>
      </div>
      
      <!-- Load More -->
      <div v-if="hasMore && searchResults.length > 0" class="p-3 text-center border-top">
        <button @click="loadMore" :disabled="loading" class="btn btn-sm btn-light-primary">
          <span v-if="!loading">Load More Results</span>
          <span v-else class="d-flex align-items-center">
            <span class="spinner-border spinner-border-sm me-2"></span>
            Loading...
          </span>
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, watch, nextTick } from 'vue';
import ApiService from '@/core/services/ApiService';

// Props
interface Props {
  modelValue?: string | null;
  label?: string;
  placeholder?: string;
  required?: boolean;
  disabled?: boolean;
}

const props = withDefaults(defineProps<Props>(), {
  modelValue: null,
  label: '',
  placeholder: 'Search patients...',
  required: false,
  disabled: false
});

// Emits
const emit = defineEmits<{
  'update:modelValue': [value: string | null];
  'patientSelected': [patient: any];
  'createPatient': [];
}>();

// Refs
const searchInput = ref<HTMLInputElement | null>(null);
const searchTerm = ref('');
const searchResults = ref<any[]>([]);
const selectedPatient = ref<any>(null);
const loading = ref(false);
const dropdownVisible = ref(false);
const highlightedIndex = ref(-1);
const currentPage = ref(1);
const hasMore = ref(false);
const searchTimeout = ref<NodeJS.Timeout | null>(null);

// Computed
const displayValue = computed(() => {
  if (selectedPatient.value) {
    return getPatientDisplayName(selectedPatient.value);
  }
  return '';
});

// Methods
const getPatientDisplayName = (patient: any): string => {
  if (patient?.info?.first_name || patient?.info?.last_name) {
    const firstName = patient.info?.first_name || '';
    const lastName = patient.info?.last_name || '';
    return `${firstName} ${lastName}`.trim();
  }
  if (patient?.info?.email) {
    return patient.info.email;
  }
  return `Patient ${patient?.id?.slice(0, 8) || 'Unknown'}`;
};

const performSearch = async (page: number = 1) => {
  if (searchTerm.value.length < 2) {
    searchResults.value = [];
    hasMore.value = false;
    return;
  }

  try {
    loading.value = true;
    
    const params = new URLSearchParams();
    params.append('search', searchTerm.value.trim());
    params.append('page', page.toString());
    params.append('page_size', '20');
    
    const { data } = await ApiService.get(`/patients/?${params}`);
    
    if (page === 1) {
      searchResults.value = data.results || [];
    } else {
      searchResults.value.push(...(data.results || []));
    }
    
    currentPage.value = page;
    hasMore.value = data.next != null;
    
  } catch (error) {
    console.error('Error searching patients:', error);
    searchResults.value = [];
  } finally {
    loading.value = false;
  }
};

const handleSearch = () => {
  if (searchTimeout.value) {
    clearTimeout(searchTimeout.value);
  }
  
  searchTimeout.value = setTimeout(() => {
    performSearch(1);
  }, 300);
};

const handleFocus = () => {
  dropdownVisible.value = true;
  if (searchTerm.value.length >= 2) {
    performSearch(1);
  }
};

const handleBlur = () => {
  // Delay hiding to allow clicks on dropdown items
  setTimeout(() => {
    dropdownVisible.value = false;
  }, 200);
};

const selectPatient = (patient: any) => {
  selectedPatient.value = patient;
  searchTerm.value = displayValue.value;
  dropdownVisible.value = false;
  highlightedIndex.value = -1;
  
  emit('update:modelValue', patient.id);
  emit('patientSelected', patient);
};

const clearSelection = () => {
  selectedPatient.value = null;
  searchTerm.value = '';
  searchResults.value = [];
  highlightedIndex.value = -1;
  
  emit('update:modelValue', null);
  emit('patientSelected', null);
  
  nextTick(() => {
    searchInput.value?.focus();
  });
};

const navigateDown = () => {
  if (searchResults.value.length === 0) return;
  highlightedIndex.value = Math.min(highlightedIndex.value + 1, searchResults.value.length - 1);
};

const navigateUp = () => {
  if (searchResults.value.length === 0) return;
  highlightedIndex.value = Math.max(highlightedIndex.value - 1, -1);
};

const selectHighlighted = () => {
  if (highlightedIndex.value >= 0 && searchResults.value[highlightedIndex.value]) {
    selectPatient(searchResults.value[highlightedIndex.value]);
  }
};

const hideDropdown = () => {
  dropdownVisible.value = false;
  highlightedIndex.value = -1;
};

const loadMore = async () => {
  if (!hasMore.value || loading.value) return;
  await performSearch(currentPage.value + 1);
};

const openPatientDetails = () => {
  if (selectedPatient.value) {
    // Navigate to the contact details page with patient type
    const url = `/admin/contacts/patients/${selectedPatient.value.id}`;
    window.open(url, '_blank');
  }
};

const createNewPatient = () => {
  emit('createPatient');
};

const loadPatientById = async (patientId: string) => {
  try {
    const { data } = await ApiService.get(`/patients/${patientId}/`);
    selectedPatient.value = data;
    searchTerm.value = displayValue.value;
  } catch (error) {
    console.error('Error loading patient by ID:', error);
    selectedPatient.value = null;
    searchTerm.value = '';
  }
};

// Watch for external value changes
watch(() => props.modelValue, async (newValue) => {
  if (newValue && newValue !== '' && (!selectedPatient.value || selectedPatient.value.id !== newValue)) {
    await loadPatientById(newValue);
  } else if (!newValue || newValue === '') {
    clearSelection();
  }
}, { immediate: true });
</script>

<style scoped>
.patient-search-select {
  position: relative;
}

.patient-option:hover {
  background-color: var(--bs-light-primary) !important;
}

.dropdown-open {
  border-bottom-left-radius: 0 !important;
  border-bottom-right-radius: 0 !important;
}

.cursor-pointer {
  cursor: pointer;
}
</style>