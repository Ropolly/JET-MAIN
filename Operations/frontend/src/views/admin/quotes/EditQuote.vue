<template>
  <div class="container">
    <!--begin::Card-->
    <div class="card">
      <!--begin::Card header-->
      <div class="card-header border-0 pt-6">
        <div class="card-title">
          <h2>Edit Quote #{{ quoteNumber }}</h2>
        </div>
        <!--begin::Card toolbar-->
        <div class="card-toolbar">
          <button @click="goBack" class="btn btn-light me-3">
            <KTIcon icon-name="arrow-left" icon-class="fs-3" />
            Cancel
          </button>
          <button @click="submitForm" class="btn btn-primary" :disabled="isSubmitting || !isFormValid">
            <KTIcon icon-name="check" icon-class="fs-3" />
            Save Changes
          </button>
        </div>
        <!--end::Card toolbar-->
      </div>
      <!--end::Card header-->

      <!--begin::Card body-->
      <div class="card-body pt-0">
        <!--begin::Loading-->
        <div v-if="loading" class="d-flex justify-content-center py-10">
          <div class="spinner-border text-primary" role="status">
            <span class="visually-hidden">Loading...</span>
          </div>
        </div>
        <!--end::Loading-->

        <!--begin::Form-->
        <form v-if="!loading" @submit.prevent="submitForm" class="form">
          <!--begin::Basic Information-->
          <div class="separator separator-content my-14">
            <span class="w-250px fw-bold text-gray-600">Basic Information</span>
          </div>

          <!--begin::Contact and Amount-->
          <div class="row g-9 mb-8">
            <div class="col-md-6 fv-row">
              <label class="required fs-6 fw-semibold mb-2">Contact</label>
              <select
                class="form-select form-select-solid"
                v-model="formData.contact_id"
                :disabled="isSubmitting"
              >
                <option value="">Select Contact</option>
                <option v-for="contact in contacts" :key="contact.id" :value="contact.id">
                  {{ getContactDisplayName(contact) }}
                </option>
              </select>
            </div>
            <div class="col-md-6 fv-row">
              <label class="required fs-6 fw-semibold mb-2">Quote Amount</label>
              <input
                type="number"
                class="form-control form-control-solid"
                placeholder="Enter amount"
                v-model="formData.quoted_amount"
                step="0.01"
                min="0"
                :disabled="isSubmitting"
              />
            </div>
          </div>
          <!--end::Contact and Amount-->

          <!--begin::Patient-->
          <div class="row g-9 mb-8">
            <div class="col-md-6 fv-row">
              <label class="fs-6 fw-semibold mb-2">Patient</label>
              <select
                class="form-select form-select-solid"
                v-model="formData.patient_id"
                :disabled="isSubmitting"
              >
                <option value="">No Patient Assigned</option>
                <option v-for="patient in patients" :key="patient.id" :value="patient.id">
                  {{ getPatientDisplayName(patient) }}
                </option>
              </select>
            </div>
            <div class="col-md-6 fv-row">
              <label class="required fs-6 fw-semibold mb-2">Status</label>
              <select
                class="form-select form-select-solid"
                v-model="formData.status"
                :disabled="isSubmitting"
              >
                <option value="pending">Pending</option>
                <option value="active">Active</option>
                <option value="completed">Completed</option>
                <option value="cancelled">Cancelled</option>
              </select>
            </div>
          </div>
          <!--end::Patient-->
          
          <!--begin::Payment Status-->
          <div class="row g-9 mb-8">
            <div class="col-md-6 fv-row">
              <label class="required fs-6 fw-semibold mb-2">Payment Status</label>
              <select
                class="form-select form-select-solid"
                v-model="formData.payment_status"
                :disabled="isSubmitting"
              >
                <option value="pending">Payment Pending</option>
                <option value="partial">Partial Paid</option>
                <option value="paid">Paid</option>
              </select>
            </div>
          </div>
          <!--end::Payment Status-->

          <!--begin::Travel Information-->
          <div class="separator separator-content my-14">
            <span class="w-250px fw-bold text-gray-600">Travel Information</span>
          </div>

          <!--begin::Airports-->
          <div class="row g-9 mb-8">
            <div class="col-md-6 fv-row">
              <label class="required fs-6 fw-semibold mb-2">Pickup Airport</label>
              <AirportSearchSelect 
                v-model="formData.pickup_airport_id" 
                placeholder="Search pickup airport..."
                @airport-selected="handlePickupAirportSelected"
                :disabled="isSubmitting"
              />
            </div>
            <div class="col-md-6 fv-row">
              <label class="required fs-6 fw-semibold mb-2">Dropoff Airport</label>
              <AirportSearchSelect 
                v-model="formData.dropoff_airport_id" 
                placeholder="Search dropoff airport..."
                @airport-selected="handleDropoffAirportSelected"
                :disabled="isSubmitting"
              />
            </div>
          </div>
          <!--end::Airports-->

          <!--begin::Aircraft and Medical Team-->
          <div class="row g-9 mb-8">
            <div class="col-md-6 fv-row">
              <label class="required fs-6 fw-semibold mb-2">Aircraft</label>
              <select
                class="form-select form-select-solid"
                v-model="formData.aircraft_type"
                :disabled="isSubmitting"
              >
                <option value="">Select Aircraft</option>
                <option value="60">Learjet 60</option>
                <option value="30">Learjet 30</option>
                <option value="TBD">To Be Determined</option>
              </select>
            </div>
            <div class="col-md-6 fv-row">
              <label class="required fs-6 fw-semibold mb-2">Medical Team</label>
              <select
                class="form-select form-select-solid"
                v-model="formData.medical_team"
                :disabled="isSubmitting"
              >
                <option value="">Select Medical Team</option>
                <option value="RN/RN">RN/RN</option>
                <option value="RN/Paramedic">RN/Paramedic</option>
                <option value="RN/MD">RN/MD</option>
                <option value="RN/RT">RN/RT</option>
                <option value="standard">Standard</option>
                <option value="full">Full</option>
              </select>
            </div>
          </div>
          <!--end::Aircraft and Medical Team-->

          <!--begin::Flight Details-->
          <div class="row g-9 mb-8">
            <div class="col-md-4 fv-row">
              <label class="required fs-6 fw-semibold mb-2">Estimated Flight Hours</label>
              <div class="input-group">
                <input
                  type="number"
                  class="form-control form-control-solid"
                  placeholder="Enter hours"
                  v-model="formData.estimated_flight_hours"
                  step="0.5"
                  min="0"
                  :disabled="isSubmitting"
                  @input="userEditedFlightTime = true"
                />
                <button 
                  class="btn btn-secondary" 
                  type="button"
                  @click="recalculateFlightTime"
                  :disabled="!canCalculateFlightTime"
                  title="Recalculate based on airports and aircraft"
                >
                  <KTIcon icon-name="calculator" icon-class="fs-3" />
                </button>
              </div>
            </div>
            <div class="col-md-4 fv-row">
              <label class="fs-6 fw-semibold mb-2">Number of Stops</label>
              <input
                type="number"
                class="form-control form-control-solid"
                placeholder="0"
                v-model.number="formData.number_of_stops"
                min="0"
                :disabled="isSubmitting"
              />
            </div>
            <div class="col-md-4 fv-row">
              <label class="fs-6 fw-semibold mb-2">Ground Transportation</label>
              <div class="form-check form-switch form-check-custom form-check-solid">
                <input
                  class="form-check-input"
                  type="checkbox"
                  v-model="formData.includes_grounds"
                  id="includesGrounds"
                  :disabled="isSubmitting"
                />
                <label class="form-check-label fw-semibold text-gray-600" for="includesGrounds">
                  Includes Ground Transportation
                </label>
              </div>
            </div>
          </div>
          <!--end::Flight Details-->

          <!--begin::Cruise Information (Optional)-->
          <div class="separator separator-content my-14">
            <span class="w-250px fw-bold text-gray-600">Cruise Information (Optional)</span>
          </div>

          <div class="row g-9 mb-8">
            <div class="col-md-6 fv-row">
              <label class="fs-6 fw-semibold mb-2">Cruise Line</label>
              <input
                type="text"
                class="form-control form-control-solid"
                placeholder="Enter cruise line"
                v-model="formData.cruise_line"
                :disabled="isSubmitting"
              />
            </div>
            <div class="col-md-6 fv-row">
              <label class="fs-6 fw-semibold mb-2">Cruise Ship</label>
              <input
                type="text"
                class="form-control form-control-solid"
                placeholder="Enter ship name"
                v-model="formData.cruise_ship"
                :disabled="isSubmitting"
              />
            </div>
          </div>

          <div class="row g-9 mb-8">
            <div class="col-md-6 fv-row">
              <label class="fs-6 fw-semibold mb-2">Cruise Doctor First Name</label>
              <input
                type="text"
                class="form-control form-control-solid"
                placeholder="Enter first name"
                v-model="formData.cruise_doctor_first_name"
                :disabled="isSubmitting"
              />
            </div>
            <div class="col-md-6 fv-row">
              <label class="fs-6 fw-semibold mb-2">Cruise Doctor Last Name</label>
              <input
                type="text"
                class="form-control form-control-solid"
                placeholder="Enter last name"
                v-model="formData.cruise_doctor_last_name"
                :disabled="isSubmitting"
              />
            </div>
          </div>
          <!--end::Cruise Information-->

          <!--begin::Communication-->
          <div class="separator separator-content my-14">
            <span class="w-250px fw-bold text-gray-600">Communication</span>
          </div>

          <div class="row g-9 mb-8">
            <div class="col-md-6 fv-row">
              <label class="required fs-6 fw-semibold mb-2">Quote PDF Email</label>
              <input
                type="email"
                class="form-control form-control-solid"
                placeholder="Enter email for PDF delivery"
                v-model="formData.quote_pdf_email"
                :disabled="isSubmitting"
              />
            </div>
          </div>
          <!--end::Communication-->

        </form>
        <!--end::Form-->
      </div>
      <!--end::Card body-->
    </div>
    <!--end::Card-->
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, computed, onMounted, watch } from "vue";
import { useRoute, useRouter } from "vue-router";
import ApiService from "@/core/services/ApiService";
import Swal from "sweetalert2/dist/sweetalert2.js";
import AirportSearchSelect from "@/components/form-controls/AirportSearchSelect.vue";

const route = useRoute();
const router = useRouter();

// Refs
const loading = ref(true);
const isSubmitting = ref(false);
const quoteNumber = ref("");
const userEditedFlightTime = ref(false);

// Data arrays
const contacts = ref<any[]>([]);
const patients = ref<any[]>([]);

// Selected airports for calculations
const selectedPickupAirport = ref<any>(null);
const selectedDropoffAirport = ref<any>(null);

// Form data
const formData = reactive({
  contact_id: '',
  quoted_amount: '',
  patient_id: '',
  pickup_airport_id: '',
  dropoff_airport_id: '',
  aircraft_type: '',
  medical_team: '',
  estimated_flight_hours: '',
  number_of_stops: 0,
  includes_grounds: false,
  cruise_line: '',
  cruise_ship: '',
  cruise_doctor_first_name: '',
  cruise_doctor_last_name: '',
  quote_pdf_email: '',
  status: 'pending',
  payment_status: 'pending',
});

// Computed
const isFormValid = computed(() => {
  return !!(
    formData.contact_id &&
    formData.quoted_amount &&
    formData.pickup_airport_id &&
    formData.dropoff_airport_id &&
    formData.aircraft_type &&
    formData.medical_team &&
    formData.estimated_flight_hours &&
    formData.quote_pdf_email &&
    formData.status
  );
});

const canCalculateFlightTime = computed(() => {
  return !!(
    selectedPickupAirport.value &&
    selectedDropoffAirport.value &&
    formData.aircraft_type
  );
});

// Methods
const goBack = () => {
  router.push('/admin/quotes');
};

const fetchQuote = async () => {
  try {
    loading.value = true;
    const quoteId = route.params.id as string;
    const response = await ApiService.get(`/quotes/${quoteId}/`);
    const quote = response.data;
    
    // Set quote number
    quoteNumber.value = quote.id.slice(0, 8);
    
    // Populate form data
    formData.contact_id = quote.contact?.id || '';
    formData.quoted_amount = quote.quoted_amount || '';
    formData.patient_id = quote.patient?.id || '';
    formData.pickup_airport_id = quote.pickup_airport?.id || '';
    formData.dropoff_airport_id = quote.dropoff_airport?.id || '';
    formData.aircraft_type = quote.aircraft_type || '';
    formData.medical_team = quote.medical_team || '';
    formData.number_of_stops = quote.number_of_stops ?? 0;
    formData.includes_grounds = quote.includes_grounds ?? false; // Use ?? for boolean to handle false value
    formData.cruise_line = quote.cruise_line || '';
    formData.cruise_ship = quote.cruise_ship || '';
    formData.cruise_doctor_first_name = quote.cruise_doctor_first_name || '';
    formData.cruise_doctor_last_name = quote.cruise_doctor_last_name || '';
    formData.quote_pdf_email = quote.quote_pdf_email || '';
    formData.status = quote.status || 'pending';
    formData.payment_status = quote.payment_status || 'pending';
    
    // Parse and set flight hours
    if (quote.estimated_flight_time) {
      const hours = parseFlightTime(quote.estimated_flight_time);
      formData.estimated_flight_hours = hours.toString();
    }
    
    // Store selected airports for calculations
    selectedPickupAirport.value = quote.pickup_airport;
    selectedDropoffAirport.value = quote.dropoff_airport;
    
  } catch (error: any) {
    console.error("Error fetching quote:", error);
    Swal.fire({
      title: "Error",
      text: error.response?.data?.detail || "Failed to load quote",
      icon: "error",
      confirmButtonText: "OK"
    }).then(() => {
      router.push('/admin/quotes');
    });
  } finally {
    loading.value = false;
  }
};

const fetchContacts = async () => {
  try {
    const response = await ApiService.get("/contacts/?page_size=1000");
    contacts.value = response.data.results || response.data || [];
  } catch (error) {
    console.error("Error fetching contacts:", error);
  }
};

const fetchPatients = async () => {
  try {
    const response = await ApiService.get("/patients/?page_size=1000");
    patients.value = response.data.results || response.data || [];
  } catch (error) {
    console.error("Error fetching patients:", error);
  }
};

const getContactDisplayName = (contact: any): string => {
  if (contact.business_name) {
    return `${contact.business_name} (Business)`;
  }
  if (contact.first_name || contact.last_name) {
    return `${contact.first_name || ''} ${contact.last_name || ''}`.trim();
  }
  return contact.email || 'Unknown Contact';
};

const getPatientDisplayName = (patient: any): string => {
  const info = patient.info || patient;
  if (info.first_name || info.last_name) {
    return `${info.first_name || ''} ${info.last_name || ''}`.trim();
  }
  return info.email || 'Unknown Patient';
};

const handlePickupAirportSelected = (airport: any) => {
  selectedPickupAirport.value = airport;
};

const handleDropoffAirportSelected = (airport: any) => {
  selectedDropoffAirport.value = airport;
};

// Flight time calculation functions
const calculateDistance = (lat1: number, lon1: number, lat2: number, lon2: number): number => {
  const R = 3440.065; // Earth's radius in nautical miles
  const dLat = (lat2 - lat1) * Math.PI / 180;
  const dLon = (lon2 - lon1) * Math.PI / 180;
  const a = Math.sin(dLat / 2) * Math.sin(dLat / 2) +
    Math.cos(lat1 * Math.PI / 180) * Math.cos(lat2 * Math.PI / 180) *
    Math.sin(dLon / 2) * Math.sin(dLon / 2);
  const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
  return R * c; // Distance in nautical miles
};

const getAircraftCruiseSpeed = (aircraftType: string): number => {
  // Cruise speeds in knots (nautical miles per hour)
  const speeds: Record<string, number> = {
    '30': 530, // Learjet 30 cruise speed
    '60': 457, // Learjet 60 cruise speed
    'TBD': 450, // Default estimate
  };
  return speeds[aircraftType] || 450;
};

const calculateFlightTime = (): number | null => {
  const pickupAirport = selectedPickupAirport.value;
  const dropoffAirport = selectedDropoffAirport.value;
  
  if (!pickupAirport || !dropoffAirport || !formData.aircraft_type) {
    return null;
  }
  
  // Get coordinates
  const lat1 = parseFloat(pickupAirport.latitude);
  const lon1 = parseFloat(pickupAirport.longitude);
  const lat2 = parseFloat(dropoffAirport.latitude);
  const lon2 = parseFloat(dropoffAirport.longitude);
  
  if (isNaN(lat1) || isNaN(lon1) || isNaN(lat2) || isNaN(lon2)) {
    return null;
  }
  
  // Calculate distance
  const distanceNM = calculateDistance(lat1, lon1, lat2, lon2);
  
  // Get aircraft speed
  const cruiseSpeed = getAircraftCruiseSpeed(formData.aircraft_type);
  
  // Calculate flight time in hours (add 15% for taxi, climb, descent)
  const baseFlightTime = distanceNM / cruiseSpeed;
  const totalFlightTime = baseFlightTime * 1.15;
  
  // Add time for stops (30 minutes per stop)
  const stopTime = (formData.number_of_stops || 0) * 0.5;
  
  return Math.round((totalFlightTime + stopTime) * 2) / 2; // Round to nearest 0.5 hour
};

const recalculateFlightTime = () => {
  const calculatedTime = calculateFlightTime();
  if (calculatedTime !== null) {
    userEditedFlightTime.value = false;
    formData.estimated_flight_hours = calculatedTime.toString();
  }
};

// Parse flight time from HH:MM:SS or duration string
const parseFlightTime = (duration: string): number => {
  if (!duration) return 0;
  
  // If it's already a number, return it
  if (!isNaN(Number(duration))) {
    return Number(duration);
  }
  
  // Handle HH:MM:SS format
  if (duration.includes(':')) {
    const parts = duration.split(':');
    const hours = parseInt(parts[0]) || 0;
    const minutes = parseInt(parts[1]) || 0;
    return hours + (minutes / 60);
  }
  
  // Handle PT format (e.g., "PT5H30M")
  const match = duration.match(/PT(?:(\d+)H)?(?:(\d+)M)?/);
  if (match) {
    const hours = parseInt(match[1]) || 0;
    const minutes = parseInt(match[2]) || 0;
    return hours + (minutes / 60);
  }
  
  return 0;
};

// Format hours to HH:MM:SS for backend
const formatFlightTime = (hours: number): string => {
  const h = Math.floor(hours);
  const m = Math.round((hours - h) * 60);
  return `${h.toString().padStart(2, '0')}:${m.toString().padStart(2, '0')}:00`;
};

const submitForm = async () => {
  if (!isFormValid.value) {
    Swal.fire({
      title: "Validation Error",
      text: "Please fill in all required fields",
      icon: "warning",
      confirmButtonText: "OK"
    });
    return;
  }

  isSubmitting.value = true;
  
  try {
    const quoteId = route.params.id as string;
    
    // Format flight time for backend
    const estimated_flight_time = formData.estimated_flight_hours ? 
      formatFlightTime(parseFloat(formData.estimated_flight_hours)) : "00:00:00";
    
    const quoteData: any = {
      contact: formData.contact_id,
      quoted_amount: parseFloat(formData.quoted_amount),
      pickup_airport: formData.pickup_airport_id,
      dropoff_airport: formData.dropoff_airport_id,
      aircraft_type: formData.aircraft_type,
      medical_team: formData.medical_team,
      estimated_flight_time: estimated_flight_time,
      number_of_stops: formData.number_of_stops,
      includes_grounds: formData.includes_grounds,
      quote_pdf_email: formData.quote_pdf_email,
      status: formData.status,
    };
    
    // Add optional fields
    if (formData.patient_id) {
      quoteData.patient = formData.patient_id;
    }
    if (formData.cruise_line) {
      quoteData.cruise_line = formData.cruise_line;
    }
    if (formData.cruise_ship) {
      quoteData.cruise_ship = formData.cruise_ship;
    }
    if (formData.cruise_doctor_first_name) {
      quoteData.cruise_doctor_first_name = formData.cruise_doctor_first_name;
    }
    if (formData.cruise_doctor_last_name) {
      quoteData.cruise_doctor_last_name = formData.cruise_doctor_last_name;
    }
    
    const response = await ApiService.put(`/quotes/${quoteId}/`, quoteData);
    
    await Swal.fire({
      title: "Success!",
      text: `Quote #${quoteNumber.value} has been updated successfully`,
      icon: "success",
      confirmButtonText: "OK",
      timer: 2000
    });
    
    router.push(`/admin/quotes/${quoteId}`);
    
  } catch (error: any) {
    console.error("Error updating quote:", error);
    Swal.fire({
      title: "Error",
      text: error.response?.data?.detail || "Failed to update quote",
      icon: "error",
      confirmButtonText: "OK"
    });
  } finally {
    isSubmitting.value = false;
  }
};

// Watchers to auto-calculate flight time
watch([
  () => formData.pickup_airport_id,
  () => formData.dropoff_airport_id,
  () => formData.aircraft_type,
  () => formData.number_of_stops,
  selectedPickupAirport,
  selectedDropoffAirport
], () => {
  // Only auto-calculate if user hasn't manually edited the field
  if (!userEditedFlightTime.value) {
    const calculatedTime = calculateFlightTime();
    if (calculatedTime !== null) {
      formData.estimated_flight_hours = calculatedTime.toString();
    }
  }
}, { deep: true });

// Track manual edits to flight time
watch(() => formData.estimated_flight_hours, (newVal, oldVal) => {
  // Skip if this was triggered by auto-calculation
  if (oldVal !== undefined && newVal !== oldVal) {
    userEditedFlightTime.value = true;
  }
});

// Load data on mount
onMounted(async () => {
  await Promise.all([
    fetchContacts(),
    fetchPatients(),
    fetchQuote()
  ]);
});
</script>

<style scoped>
.separator-content {
  position: relative;
  z-index: 1;
}

.separator-content::before {
  content: "";
  position: absolute;
  left: 260px;
  right: 0;
  top: 50%;
  height: 1px;
  background-color: #e4e6ef;
  z-index: -1;
}
</style>