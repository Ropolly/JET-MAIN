<template>
  <div class="airport-search-select">
    <label v-if="label" :class="`fs-6 fw-semibold mb-2 ${required ? 'required' : ''}`">
      {{ label }}
    </label>
    
    <div class="position-relative">
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
        :class="`form-control form-control-solid ${dropdownVisible ? 'dropdown-open' : ''}`"
        :placeholder="placeholder"
        :disabled="disabled"
        autocomplete="off"
      />
      
      <!-- Loading Spinner -->
      <div v-if="loading" class="position-absolute top-50 end-0 translate-middle-y me-3">
        <span class="spinner-border spinner-border-sm" role="status"></span>
      </div>
      
      <!-- Clear Button -->
      <div v-if="selectedAirport && !loading" class="position-absolute top-50 end-0 translate-middle-y me-3">
        <button
          type="button" 
          @click="clearSelection"
          class="btn btn-sm btn-icon btn-active-light-primary"
        >
          <KTIcon icon-name="cross" icon-class="fs-4" />
        </button>
      </div>
      
      <!-- Search Icon -->
      <div v-if="!selectedAirport && !loading" class="position-absolute top-50 end-0 translate-middle-y me-3">
        <KTIcon icon-name="magnifier" icon-class="fs-4 text-muted" />
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
        <KTIcon icon-name="geolocation" icon-class="fs-2 text-muted mb-2" />
        <div>No airports found for "{{ searchTerm }}"</div>
        <small>Try searching by airport name, code, or city</small>
      </div>
      
      <!-- Search Prompt -->
      <div v-if="searchTerm.length < 2 && !selectedAirport" class="p-3 text-muted text-center">
        <KTIcon icon-name="magnifier" icon-class="fs-2 text-muted mb-2" />
        <div>Type at least 2 characters to search</div>
        <small>Search by name, IATA/ICAO code, or municipality</small>
      </div>
      
      <!-- Search Results -->
      <div v-for="(airport, index) in searchResults" 
           :key="airport.id" 
           :class="`airport-option p-3 border-bottom border-gray-200 cursor-pointer ${index === highlightedIndex ? 'bg-light-primary' : ''}`"
           @click="selectAirport(airport)"
           @mouseenter="highlightedIndex = index">
        
        <div class="d-flex align-items-center">
          <div class="symbol symbol-40px me-3">
            <div class="symbol-label bg-light-info">
              <KTIcon icon-name="geolocation" icon-class="fs-4 text-info" />
            </div>
          </div>
          
          <div class="flex-grow-1">
            <div class="d-flex align-items-center">
              <span class="fw-bold text-gray-800 me-2">{{ airport.name }}</span>
              <span class="badge badge-light-primary fs-8 me-1" v-if="airport.iata_code">{{ airport.iata_code }}</span>
              <span class="badge badge-light-secondary fs-8" v-if="airport.icao_code">{{ airport.icao_code }}</span>
              <span class="badge badge-light-info fs-8" v-if="airport.ident && !airport.iata_code && !airport.icao_code">{{ airport.ident }}</span>
            </div>
            <div class="text-muted fs-7">
              {{ formatLocation(airport) }} · {{ formatAirportType(airport.airport_type) }}
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
    
    <!-- Selected Airport Display (when not focused) -->
    <div v-if="selectedAirport && !dropdownVisible" class="mt-2 p-2 bg-light-success border border-success rounded">
      <div class="d-flex align-items-center">
        <KTIcon icon-name="geolocation" icon-class="fs-4 text-success me-2" />
        <div class="flex-grow-1">
          <span class="fw-bold text-success">{{ selectedAirport.name }}</span>
          <span class="badge badge-success fs-8 ms-2" v-if="getAirportCode(selectedAirport)">
            {{ getAirportCode(selectedAirport) }}
          </span>
          <div class="text-muted fs-8">{{ formatLocation(selectedAirport) }}</div>
        </div>
      </div>
    </div>
    
    <!-- Help Text -->
    <div v-if="helpText" class="form-text">{{ helpText }}</div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, watch, nextTick } from 'vue';
import ApiService from '@/core/services/ApiService';

interface Airport {
  id: string;
  ident: string;
  name: string;
  latitude: number;
  longitude: number;
  elevation?: number;
  iso_country: string;
  iso_region?: string;
  municipality?: string;
  icao_code?: string;
  iata_code?: string;
  local_code?: string;
  gps_code?: string;
  airport_type: string;
  timezone: string;
  fbos_count: number;
  grounds_count: number;
  created_on: string;
}

interface Props {
  modelValue?: string;
  label?: string;
  placeholder?: string;
  required?: boolean;
  disabled?: boolean;
  helpText?: string;
}

interface Emits {
  (event: 'update:modelValue', value: string | undefined): void;
  (event: 'airportSelected', airport: Airport | null): void;
}

const props = withDefaults(defineProps<Props>(), {
  placeholder: 'Search airports by name, code, or city...',
  required: false,
  disabled: false
});

const emit = defineEmits<Emits>();

// Reactive state
const searchInput = ref<HTMLInputElement | null>(null);
const searchTerm = ref('');
const searchResults = ref<Airport[]>([]);
const selectedAirport = ref<Airport | null>(null);
const loading = ref(false);
const dropdownVisible = ref(false);
const highlightedIndex = ref(-1);
const currentPage = ref(1);
const hasMore = ref(false);
const searchTimeout = ref<NodeJS.Timeout | null>(null);

// Computed
const displayValue = computed(() => {
  if (selectedAirport.value) {
    const airport = selectedAirport.value;
    const code = getAirportCode(airport);
    return `${airport.name}${code ? ` (${code})` : ''}`;
  }
  return searchTerm.value;
});

// Watch display value for input updates (safe to define here)
watch(displayValue, (newValue) => {
  if (searchInput.value && document.activeElement !== searchInput.value) {
    searchTerm.value = newValue;
  }
});

// Methods
const handleSearch = () => {
  // Clear existing timeout
  if (searchTimeout.value) {
    clearTimeout(searchTimeout.value);
  }
  
  // If we have a selected airport and user is typing, clear it
  if (selectedAirport.value) {
    selectedAirport.value = null;
    emit('update:modelValue', undefined);
    emit('airportSelected', null);
  }
  
  // Show dropdown immediately
  dropdownVisible.value = true;
  
  // Debounce search
  searchTimeout.value = setTimeout(async () => {
    if (searchTerm.value.length >= 2) {
      await performSearch();
    } else {
      searchResults.value = [];
      hasMore.value = false;
    }
  }, 300);
};

const performSearch = async (page: number = 1) => {
  if (searchTerm.value.length < 2) return;
  
  try {
    loading.value = true;
    
    const params = new URLSearchParams();
    params.append('search', searchTerm.value.trim());
    params.append('page', page.toString());
    params.append('page_size', '20');
    
    const { data } = await ApiService.get(`/airports/?${params}`);
    
    if (page === 1) {
      searchResults.value = data.results || [];
    } else {
      searchResults.value = [...searchResults.value, ...(data.results || [])];
    }
    
    currentPage.value = page;
    hasMore.value = !!data.next;
    highlightedIndex.value = -1;
    
  } catch (error) {
    console.error('Error searching airports:', error);
    searchResults.value = [];
    hasMore.value = false;
  } finally {
    loading.value = false;
  }
};

const loadMore = async () => {
  if (!hasMore.value || loading.value) return;
  await performSearch(currentPage.value + 1);
};

const loadAirportById = async (airportId: string) => {
  try {
    const { data } = await ApiService.get(`/airports/${airportId}/`);
    selectedAirport.value = data;
    searchTerm.value = displayValue.value;
    emit('airportSelected', data);
  } catch (error) {
    console.error('Error loading airport by ID:', error);
    selectedAirport.value = null;
    searchTerm.value = '';
    emit('airportSelected', null);
  }
};

const selectAirport = (airport: Airport) => {
  selectedAirport.value = airport;
  searchTerm.value = displayValue.value;
  dropdownVisible.value = false;
  highlightedIndex.value = -1;
  
  emit('update:modelValue', airport.id);
  emit('airportSelected', airport);
  
  // Blur the input to hide dropdown
  searchInput.value?.blur();
};

const clearSelection = () => {
  selectedAirport.value = null;
  searchTerm.value = '';
  searchResults.value = [];
  dropdownVisible.value = false;
  highlightedIndex.value = -1;
  hasMore.value = false;
  
  emit('update:modelValue', undefined);
  emit('airportSelected', null);
  
  // Focus the input for new search
  nextTick(() => {
    searchInput.value?.focus();
  });
};

const handleFocus = () => {
  if (selectedAirport.value) {
    searchTerm.value = '';
  }
  dropdownVisible.value = true;
};

const handleBlur = () => {
  // Delay hiding dropdown to allow for click events
  setTimeout(() => {
    dropdownVisible.value = false;
    if (selectedAirport.value) {
      searchTerm.value = displayValue.value;
    }
  }, 200);
};

const navigateDown = () => {
  if (searchResults.value.length === 0) return;
  highlightedIndex.value = Math.min(highlightedIndex.value + 1, searchResults.value.length - 1);
};

const navigateUp = () => {
  if (searchResults.value.length === 0) return;
  highlightedIndex.value = Math.max(highlightedIndex.value - 1, 0);
};

const selectHighlighted = () => {
  if (highlightedIndex.value >= 0 && searchResults.value[highlightedIndex.value]) {
    selectAirport(searchResults.value[highlightedIndex.value]);
  }
};

const hideDropdown = () => {
  dropdownVisible.value = false;
  if (selectedAirport.value) {
    searchTerm.value = displayValue.value;
  }
  searchInput.value?.blur();
};

// Helper functions
const getAirportCode = (airport: Airport): string => {
  return airport.iata_code || airport.icao_code || airport.ident || '';
};

const formatLocation = (airport: Airport): string => {
  const parts = [];
  if (airport.municipality) parts.push(airport.municipality);
  if (airport.iso_region) parts.push(airport.iso_region);
  if (airport.iso_country) parts.push(airport.iso_country);
  return parts.length > 0 ? parts.join(', ') : 'Unknown location';
};

const formatAirportType = (type: string): string => {
  const typeMap: Record<string, string> = {
    'large_airport': 'Large Airport',
    'medium_airport': 'Medium Airport', 
    'small_airport': 'Small Airport'
  };
  return typeMap[type] || type || 'Airport';
};

// Watch for external value changes (moved here after loadAirportById is defined)
watch(() => props.modelValue, async (newValue) => {
  if (newValue && (!selectedAirport.value || selectedAirport.value.id !== newValue)) {
    await loadAirportById(newValue);
  } else if (!newValue) {
    clearSelection();
  }
}, { immediate: true });
</script>

<style scoped>
.airport-search-select {
  position: relative;
}

.dropdown-open {
  border-bottom-left-radius: 0;
  border-bottom-right-radius: 0;
}

.airport-option:hover {
  background-color: var(--bs-light-primary) !important;
}

.airport-option:last-child {
  border-bottom: none !important;
}

.cursor-pointer {
  cursor: pointer;
}
</style>