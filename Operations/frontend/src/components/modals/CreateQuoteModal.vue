<template>
  <!--begin::Modal - Create quote-->
  <div
    class="modal fade"
    id="kt_modal_create_quote"
    ref="modalRef"
    tabindex="-1"
    aria-hidden="true"
  >
    <!--begin::Modal dialog-->
    <div class="modal-dialog modal-xl">
      <!--begin::Modal content-->
      <div class="modal-content">
        <!--begin::Modal header-->
        <div class="modal-header">
          <!--begin::Title-->
          <h2>Create New Quote</h2>
          <!--end::Title-->

          <!--begin::Close-->
          <div
            class="btn btn-sm btn-icon btn-active-color-primary"
            data-bs-dismiss="modal"
            @click="resetForm"
          >
            <KTIcon icon-name="cross" icon-class="fs-1" />
          </div>
          <!--end::Close-->
        </div>
        <!--end::Modal header-->

        <!--begin::Modal body-->
        <div class="modal-body scroll-y mx-5 my-7">
          <!--begin::Form-->
          <form id="kt_modal_create_quote_form" class="form" @submit.prevent="submitForm">
            
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
                  <option v-for="contact in availableContacts" :key="contact.id" :value="contact.id">
                    {{ getContactDisplayName(contact) }}
                  </option>
                </select>
              </div>
              <div class="col-md-6 fv-row">
                <label class="required fs-6 fw-semibold mb-2">Quoted Amount</label>
                <div class="input-group input-group-solid">
                  <span class="input-group-text">$</span>
                  <input
                    type="number"
                    step="0.01"
                    min="0"
                    class="form-control form-control-solid"
                    placeholder="0.00"
                    v-model="formData.quoted_amount"
                    :disabled="isSubmitting"
                  />
                </div>
              </div>
            </div>
            <!--end::Contact and Amount-->

            <!--begin::Patient (Optional)-->
            <div class="fv-row mb-8">
              <PatientSearchSelect
                v-model="formData.patient_id"
                label="Patient (Optional)"
                placeholder="Search patients..."
                :disabled="isSubmitting"
                @patientSelected="onPatientSelected"
              />
            </div>
            <!--end::Patient-->

            <!--begin::Flight Information-->
            <div class="separator separator-content my-14">
              <span class="w-250px fw-bold text-gray-600">Flight Information</span>
            </div>

            <!--begin::Airports-->
            <div class="row g-9 mb-8">
              <div class="col-md-6 fv-row">
                <AirportSearchSelect
                  v-model="formData.pickup_airport_id"
                  label="Pickup Airport"
                  placeholder="Search pickup airport..."
                  help-text="Search by airport name, IATA/ICAO code, or city"
                  required
                  :disabled="isSubmitting"
                  @airport-selected="onPickupAirportSelected"
                />
              </div>
              <div class="col-md-6 fv-row">
                <AirportSearchSelect
                  v-model="formData.dropoff_airport_id"
                  label="Dropoff Airport"
                  placeholder="Search dropoff airport..."
                  help-text="Search by airport name, IATA/ICAO code, or city"
                  required
                  :disabled="isSubmitting"
                  @airport-selected="onDropoffAirportSelected"
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
                  <option value="65">Learjet 65</option>
                  <option value="35">Learjet 35</option>
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
                <label class="required fs-6 fw-semibold mb-2">Estimated Flight Time (Hours)</label>
                <div class="input-group input-group-solid">
                  <input
                    type="number"
                    step="0.5"
                    min="0"
                    class="form-control form-control-solid"
                    placeholder="5.5"
                    v-model="formData.estimated_flight_hours"
                    :disabled="isSubmitting"
                  />
                  <button
                    class="btn btn-secondary"
                    type="button"
                    @click="recalculateFlightTime"
                    :disabled="isSubmitting"
                    title="Recalculate based on selected airports and aircraft"
                  >
                    <KTIcon icon-name="reload" icon-class="fs-6" />
                  </button>
                </div>
                <div class="form-text">Auto-calculated based on distance and aircraft speed</div>
              </div>
              <div class="col-md-4 fv-row">
                <label class="fs-6 fw-semibold mb-2">Number of Stops</label>
                <input
                  type="number"
                  min="0"
                  class="form-control form-control-solid"
                  placeholder="0"
                  v-model="formData.number_of_stops"
                  :disabled="isSubmitting"
                />
              </div>
              <div class="col-md-4 fv-row">
                <label class="fs-6 fw-semibold mb-2">Options</label>
                <div class="form-check form-check-custom form-check-solid mt-3">
                  <input 
                    class="form-check-input" 
                    type="checkbox" 
                    v-model="formData.includes_grounds"
                    id="includesGrounds"
                    :disabled="isSubmitting"
                  />
                  <label class="form-check-label" for="includesGrounds">
                    Includes Ground Transportation
                  </label>
                </div>
              </div>
            </div>
            <!--end::Flight Details-->

            <!--begin::Additional Information-->
            <div class="separator separator-content my-14">
              <span class="w-250px fw-bold text-gray-600">Additional Information</span>
            </div>

            <!--begin::Cruise Information-->
            <div class="row g-9 mb-8">
              <div class="col-md-6 fv-row">
                <label class="fs-6 fw-semibold mb-2">Cruise Line (Optional)</label>
                <input
                  type="text"
                  class="form-control form-control-solid"
                  placeholder="Enter cruise line"
                  v-model="formData.cruise_line"
                  :disabled="isSubmitting"
                />
              </div>
              <div class="col-md-6 fv-row">
                <label class="fs-6 fw-semibold mb-2">Cruise Ship (Optional)</label>
                <input
                  type="text"
                  class="form-control form-control-solid"
                  placeholder="Enter cruise ship name"
                  v-model="formData.cruise_ship"
                  :disabled="isSubmitting"
                />
              </div>
            </div>
            <!--end::Cruise Information-->

            <!--begin::Cruise Doctor-->
            <div class="row g-9 mb-8">
              <div class="col-md-6 fv-row">
                <label class="fs-6 fw-semibold mb-2">Cruise Doctor First Name (Optional)</label>
                <input
                  type="text"
                  class="form-control form-control-solid"
                  placeholder="First name"
                  v-model="formData.cruise_doctor_first_name"
                  :disabled="isSubmitting"
                />
              </div>
              <div class="col-md-6 fv-row">
                <label class="fs-6 fw-semibold mb-2">Cruise Doctor Last Name (Optional)</label>
                <input
                  type="text"
                  class="form-control form-control-solid"
                  placeholder="Last name"
                  v-model="formData.cruise_doctor_last_name"
                  :disabled="isSubmitting"
                />
              </div>
            </div>
            <!--end::Cruise Doctor-->

            <!--begin::Email and Status-->
            <div class="row g-9 mb-8">
              <div class="col-md-6 fv-row">
                <label class="required fs-6 fw-semibold mb-2">Quote PDF Email</label>
                <input
                  type="email"
                  class="form-control form-control-solid"
                  placeholder="email@example.com"
                  v-model="formData.quote_pdf_email"
                  :disabled="isSubmitting"
                />
              </div>
              <div class="col-md-6 fv-row">
                <label class="required fs-6 fw-semibold mb-2">Status</label>
                <select
                  class="form-select form-select-solid"
                  v-model="formData.status"
                  :disabled="isSubmitting"
                >
                  <option value="pending">Pending</option>
                  <option value="confirmed">Confirmed</option>
                  <option value="active">Active</option>
                  <option value="completed">Completed</option>
                  <option value="cancelled">Cancelled</option>
                  <option value="paid">Paid</option>
                </select>
              </div>
            </div>
            <!--end::Email and Status-->
          </form>
          <!--end::Form-->
        </div>
        <!--end::Modal body-->

        <!--begin::Modal footer-->
        <div class="modal-footer flex-center">
          <!--begin::Button-->
          <button
            type="reset"
            class="btn btn-light me-3"
            data-bs-dismiss="modal"
            :disabled="isSubmitting"
          >
            Cancel
          </button>
          <!--end::Button-->

          <!--begin::Button-->
          <button
            type="submit"
            class="btn btn-primary"
            @click="submitForm"
            :disabled="isSubmitting || !isFormValid"
          >
            <span v-if="!isSubmitting" class="indicator-label">Create Quote</span>
            <span v-else class="indicator-progress">
              Creating...
              <span class="spinner-border spinner-border-sm align-middle ms-2"></span>
            </span>
          </button>
          <!--end::Button-->
        </div>
        <!--end::Modal footer-->
      </div>
      <!--end::Modal content-->
    </div>
    <!--end::Modal dialog-->
  </div>
  <!--end::Modal - Create quote-->
</template>

<script setup lang="ts">
import { ref, reactive, computed, onMounted, watch } from "vue";
import Swal from "sweetalert2";
import ApiService from "@/core/services/ApiService";
import { Modal } from "bootstrap";
import AirportSearchSelect from "@/components/form-controls/AirportSearchSelect.vue";
import PatientSearchSelect from "@/components/form-controls/PatientSearchSelect.vue";

const emit = defineEmits(['quoteCreated']);

const modalRef = ref<HTMLElement | null>(null);
const isSubmitting = ref(false);

// Data arrays
const contacts = ref<any[]>([]);
const availableContacts = ref<any[]>([]);
const selectedPatient = ref<any>(null);

// Selected airports for additional data and flight calculations
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

// Methods
const resetForm = () => {
  Object.assign(formData, {
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
  });
  
  // Reset tracking variables and selected airports/patient
  userEditedFlightTime.value = false;
  selectedPickupAirport.value = null;
  selectedDropoffAirport.value = null;
  selectedPatient.value = null;
};

const fetchContacts = async () => {
  try {
    // Fetch all contacts
    const contactsResponse = await ApiService.get("/contacts/?page_size=100");
    contacts.value = contactsResponse.data.results || contactsResponse.data || [];
    
    // Fetch staff members to filter out their contacts
    const staffResponse = await ApiService.get("/staff/?page_size=100");
    const staffMembers = staffResponse.data.results || staffResponse.data || [];
    const staffContactIds = staffMembers.map((staff: any) => staff.contact_id);
    
    // Filter out contacts that are staff members
    availableContacts.value = contacts.value.filter(contact => 
      !staffContactIds.includes(contact.id)
    );
    
    console.log(`Loaded ${contacts.value.length} total contacts, ${availableContacts.value.length} available for quotes (${staffContactIds.length} staff filtered out)`);
  } catch (error) {
    console.error("Error fetching contacts:", error);
  }
};

// Patient selection handler
const onPatientSelected = (patient: any) => {
  selectedPatient.value = patient;
  console.log('Patient selected:', patient);
};

// Note: Airport fetching is now handled by AirportSearchSelect components


const getContactDisplayName = (contact: any): string => {
  if (contact.business_name) {
    return `${contact.business_name} (Business)`;
  }
  if (contact.first_name || contact.last_name) {
    return `${contact.first_name || ''} ${contact.last_name || ''}`.trim();
  }
  return `Contact ${contact.id.slice(0, 8)}`;
};


// Airport selection handlers
const onPickupAirportSelected = (airport: any) => {
  selectedPickupAirport.value = airport;
  console.log('Pickup airport selected:', airport);
};

const onDropoffAirportSelected = (airport: any) => {
  selectedDropoffAirport.value = airport;
  console.log('Dropoff airport selected:', airport);
};


// Flight time calculation functions
const calculateDistance = (lat1: number, lon1: number, lat2: number, lon2: number): number => {
  const R = 3440.065; // Earth's radius in nautical miles
  const dLat = (lat2 - lat1) * Math.PI / 180;
  const dLon = (lon2 - lon1) * Math.PI / 180;
  const a = 
    Math.sin(dLat / 2) * Math.sin(dLat / 2) +
    Math.cos(lat1 * Math.PI / 180) * Math.cos(lat2 * Math.PI / 180) * 
    Math.sin(dLon / 2) * Math.sin(dLon / 2);
  const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
  return R * c; // Distance in nautical miles
};

const getAircraftCruiseSpeed = (aircraftType: string): number => {
  // Cruise speeds in knots (nautical miles per hour)
  const speeds: Record<string, number> = {
    '35': 464, // Learjet 35 cruise speed
    '65': 459, // Learjet 65 cruise speed
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
    // Reset the tracking so auto-calculation can work again
    userEditedFlightTime.value = false;
    formData.estimated_flight_hours = calculatedTime.toString();
    
    // Show brief feedback
    const pickupAirport = selectedPickupAirport.value;
    const dropoffAirport = selectedDropoffAirport.value;
    
    if (pickupAirport && dropoffAirport) {
      const distanceNM = calculateDistance(
        parseFloat(pickupAirport.latitude),
        parseFloat(pickupAirport.longitude),
        parseFloat(dropoffAirport.latitude),
        parseFloat(dropoffAirport.longitude)
      );
      
      console.log(`Calculated flight time: ${calculatedTime} hours for ${Math.round(distanceNM)} NM`);
    }
  } else {
    Swal.fire({
      title: "Cannot Calculate",
      text: "Please select pickup airport, dropoff airport, and aircraft to calculate flight time.",
      icon: "info",
      timer: 2000,
      showConfirmButton: false
    });
  }
};

const submitForm = async () => {
  if (!isFormValid.value || isSubmitting.value) return;
  
  isSubmitting.value = true;
  
  try {
    // Convert flight hours to Django duration format (HH:MM:SS)
    const hours = Math.floor(parseFloat(formData.estimated_flight_hours));
    const minutes = Math.round((parseFloat(formData.estimated_flight_hours) - hours) * 60);
    const estimated_flight_time = `${hours.toString().padStart(2, '0')}:${minutes.toString().padStart(2, '0')}:00`;
    
    // Prepare quote data
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
    
    console.log('Creating quote:', quoteData);
    
    // Create the quote
    const response = await ApiService.post("/quotes/", quoteData);
    const newQuote = response.data;
    
    Swal.fire({
      title: "Success!",
      text: "Quote created successfully!",
      icon: "success",
      timer: 2000,
      showConfirmButton: false
    });
    
    emit('quoteCreated', newQuote);
    resetForm();
    
    // Close modal
    const modalElement = document.getElementById('kt_modal_create_quote');
    if (modalElement) {
      try {
        const modal = Modal.getInstance(modalElement);
        if (modal) {
          modal.hide();
        }
      } catch (error) {
        console.error('Error closing modal:', error);
      }
    }
    
  } catch (error: any) {
    console.error('Error creating quote:', error);
    console.error('Error response:', error.response?.data);
    
    let errorMessage = "Failed to create quote. Please try again.";
    
    if (error.response?.data?.detail) {
      errorMessage = error.response.data.detail;
    } else if (error.response?.data) {
      // Handle field-specific errors
      const errors = error.response.data;
      const errorMessages = [];
      
      for (const field in errors) {
        if (Array.isArray(errors[field])) {
          errorMessages.push(`${field}: ${errors[field].join(', ')}`);
        } else {
          errorMessages.push(`${field}: ${errors[field]}`);
        }
      }
      
      if (errorMessages.length > 0) {
        errorMessage = errorMessages.join('\n');
      }
    }
    
    Swal.fire({
      title: "Error!",
      text: errorMessage,
      icon: "error",
      confirmButtonText: "OK"
    });
  } finally {
    isSubmitting.value = false;
  }
};

// Track if user has manually edited flight time
const userEditedFlightTime = ref(false);

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
  // Mark as manually edited if user types in the field
  if (oldVal !== undefined && newVal !== oldVal && newVal !== '') {
    userEditedFlightTime.value = true;
  }
});

// Load data on component mount
onMounted(async () => {
  await fetchContacts();
  // Note: Airports and Patients are now handled by respective SearchSelect components
});
</script>

<style scoped>
.separator-content {
  position: relative;
  z-index: 1;
}

.separator-content span {
  background: var(--bs-body-bg);
  padding: 0 1rem;
}
</style>