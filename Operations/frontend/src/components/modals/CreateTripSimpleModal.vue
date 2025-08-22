<template>
  <!--begin::Modal - Create trip-->
  <div
    class="modal fade"
    id="kt_modal_create_trip_simple"
    ref="modalRef"
    tabindex="-1"
    aria-hidden="true"
  >
    <!--begin::Modal dialog-->
    <div class="modal-dialog modal-lg">
      <!--begin::Modal content-->
      <div class="modal-content">
        <!--begin::Modal header-->
        <div class="modal-header">
          <!--begin::Title-->
          <h2>Create New Trip</h2>
          <!--end::Title-->

          <!--begin::Close-->
          <div
            class="btn btn-sm btn-icon btn-active-color-primary"
            data-bs-dismiss="modal"
          >
            <KTIcon icon-name="cross" icon-class="fs-1" />
          </div>
          <!--end::Close-->
        </div>
        <!--end::Modal header-->

        <!--begin::Modal body-->
        <div class="modal-body scroll-y mx-5 my-7">
          <!--begin::Form-->
          <form id="kt_modal_create_trip_form" class="form">
            <!--begin::Input group-->
            <div class="row g-9 mb-8">
              <div class="col-md-6 fv-row">
                <label class="required fs-6 fw-semibold mb-2">Trip Number</label>
                <input
                  type="text"
                  class="form-control form-control-solid"
                  placeholder="JM-2025-001"
                  name="trip_number"
                  v-model="formData.trip_number"
                />
              </div>
              <div class="col-md-6 fv-row">
                <label class="required fs-6 fw-semibold mb-2">Trip Type</label>
                <select name="trip_type" class="form-select form-select-solid" v-model="formData.type">
                  <option value="">Select trip type...</option>
                  <option value="medical">Medical</option>
                  <option value="charter">Charter</option>
                  <option value="part 91">Part 91</option>
                  <option value="maintenance">Maintenance</option>
                  <option value="other">Other</option>
                </select>
              </div>
            </div>
            <!--end::Input group-->

            <!--begin::Input group-->
            <div class="row g-9 mb-8">
              <div class="col-md-6 fv-row">
                <label class="required fs-6 fw-semibold mb-2">Departure Airport</label>
                <select name="departure_airport" class="form-select form-select-solid" v-model="formData.departure_airport">
                  <option value="">Select departure...</option>
                  <option v-for="airport in airports" :key="airport.id" :value="airport.id">
                    {{ airport.name }} ({{ airport.icao_code }}{{ airport.iata_code ? '/' + airport.iata_code : '' }})
                  </option>
                </select>
              </div>
              <div class="col-md-6 fv-row">
                <label class="required fs-6 fw-semibold mb-2">Arrival Airport</label>
                <select name="arrival_airport" class="form-select form-select-solid" v-model="formData.arrival_airport">
                  <option value="">Select arrival...</option>
                  <option v-for="airport in airports" :key="airport.id" :value="airport.id">
                    {{ airport.name }} ({{ airport.icao_code }}{{ airport.iata_code ? '/' + airport.iata_code : '' }})
                  </option>
                </select>
              </div>
            </div>
            <!--end::Input group-->

            <!--begin::Input group-->
            <div class="row g-9 mb-8">
              <div class="col-md-6 fv-row">
                <label class="required fs-6 fw-semibold mb-2">Departure Date</label>
                <input
                  type="date"
                  class="form-control form-control-solid"
                  name="departure_date"
                  v-model="formData.departure_date"
                />
              </div>
              <div class="col-md-6 fv-row">
                <label class="required fs-6 fw-semibold mb-2">Departure Time</label>
                <input
                  type="time"
                  class="form-control form-control-solid"
                  name="departure_time"
                  v-model="formData.departure_time"
                />
              </div>
            </div>
            <!--end::Input group-->

            <!--begin::Input group-->
            <div class="fv-row mb-8">
              <label class="fs-6 fw-semibold mb-2">Patient</label>
              <select name="patient_id" class="form-select form-select-solid" v-model="formData.patient_id">
                <option value="">Select patient...</option>
                <option v-for="patient in patients" :key="patient.id" :value="patient.id">
                  {{ patient.info.first_name }} {{ patient.info.last_name }}
                  <span v-if="patient.info.email"> - {{ patient.info.email }}</span>
                </option>
              </select>
            </div>
            <!--end::Input group-->

            <!--begin::Input group-->
            <div class="fv-row mb-8">
              <label class="fs-6 fw-semibold mb-2">Aircraft</label>
              <select name="aircraft_id" class="form-select form-select-solid" v-model="formData.aircraft_id">
                <option value="">Select aircraft...</option>
                <option v-for="plane in aircraft" :key="plane.id" :value="plane.id">
                  {{ plane.tail_number }} - {{ plane.make }} {{ plane.model }}
                </option>
              </select>
            </div>
            <!--end::Input group-->

            <!--begin::Input group-->
            <div class="fv-row mb-8">
              <label class="fs-6 fw-semibold mb-2">Notes</label>
              <textarea
                class="form-control form-control-solid"
                rows="3"
                name="notes"
                placeholder="Additional trip notes or special requirements..."
                v-model="formData.notes"
              ></textarea>
            </div>
            <!--end::Input group-->
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
          >
            Cancel
          </button>
          <!--end::Button-->

          <!--begin::Button-->
          <button
            type="submit"
            class="btn btn-primary"
            @click="handleSubmit"
            :disabled="isSubmitting"
          >
            <span v-if="!isSubmitting" class="indicator-label">Create Trip</span>
            <span v-else class="indicator-progress">
              Please wait...
              <span
                class="spinner-border spinner-border-sm align-middle ms-2"
              ></span>
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
  <!--end::Modal - Create trip-->
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from "vue";
import { hideModal } from "@/core/helpers/modal";
import Swal from "sweetalert2";
import ApiService from "@/core/services/ApiService";

const modalRef = ref<HTMLElement | null>(null);
const isSubmitting = ref(false);

// Form data
const formData = reactive({
  trip_number: '',
  type: '',
  departure_airport: '',
  arrival_airport: '',
  departure_date: '',
  departure_time: '',
  patient_id: '',
  aircraft_id: '',
  notes: '',
  status: 'pending',
  priority: 'routine',
});

// Dropdown data
const patients = ref<any[]>([]);
const aircraft = ref<any[]>([]);
const airports = ref<any[]>([]);

// Emit event to parent to refresh trips list
const emit = defineEmits(['tripCreated']);

// Fetch patients, aircraft, and airports for dropdowns
const fetchDropdownData = async () => {
  try {
    // Fetch patients
    const patientsResponse = await ApiService.get('/patients/');
    patients.value = patientsResponse.data.results || patientsResponse.data || [];
    console.log('Loaded patients:', patients.value);
  } catch (error) {
    console.error('Error fetching patients:', error);
  }
  
  try {
    // Fetch aircraft
    const aircraftResponse = await ApiService.get('/aircraft/');
    aircraft.value = aircraftResponse.data.results || aircraftResponse.data || [];
    console.log('Loaded aircraft:', aircraft.value);
  } catch (error) {
    console.error('Error fetching aircraft:', error);
  }
  
  try {
    // Fetch airports
    const airportsResponse = await ApiService.get('/airports/');
    airports.value = airportsResponse.data.results || airportsResponse.data || [];
    console.log('Loaded airports:', airports.value);
  } catch (error) {
    console.error('Error fetching airports:', error);
  }
};

onMounted(() => {
  fetchDropdownData();
});

const handleSubmit = async (e: Event) => {
  e.preventDefault();
  
  // Basic validation
  if (!formData.trip_number || !formData.type || !formData.departure_airport || !formData.arrival_airport) {
    Swal.fire({
      title: "Validation Error",
      text: "Please fill in all required fields (Trip Number, Type, Departure and Arrival Airports)",
      icon: "warning",
      confirmButtonText: "OK"
    });
    return;
  }
  
  isSubmitting.value = true;
  
  try {
    // Prepare data for API - match TripWriteSerializer fields
    const tripData: any = {
      trip_number: formData.trip_number,
      type: formData.type,
      status: formData.status,
      // Combine date and time for departure
      estimated_departure_time: formData.departure_date && formData.departure_time 
        ? `${formData.departure_date}T${formData.departure_time}:00` 
        : null,
      // Initialize empty email_chain array
      email_chain: []
    };
    
    // Only include patient and aircraft if they have values (using correct field names for TripWriteSerializer)
    if (formData.patient_id) {
      tripData.patient = formData.patient_id;
    }
    
    if (formData.aircraft_id) {
      tripData.aircraft = formData.aircraft_id;
    }
    
    console.log('Creating trip with data:', tripData);
    
    // Make actual API call to create trip
    const response = await ApiService.post('/trips/', tripData);
    console.log('Trip created successfully:', response.data);
    
    // If airports are selected, create a basic trip line
    if (formData.departure_airport && formData.arrival_airport) {
      try {
        const tripLineData = {
          trip: response.data.id,
          origin_airport: formData.departure_airport,
          destination_airport: formData.arrival_airport,
          // Set basic departure/arrival times if date/time provided
          departure_time_local: formData.departure_date && formData.departure_time 
            ? `${formData.departure_date}T${formData.departure_time}:00` 
            : `${formData.departure_date || new Date().toISOString().split('T')[0]}T08:00:00`,
          departure_time_utc: formData.departure_date && formData.departure_time 
            ? `${formData.departure_date}T${formData.departure_time}:00` 
            : `${formData.departure_date || new Date().toISOString().split('T')[0]}T08:00:00`,
          // Set arrival time 2 hours after departure as default
          arrival_time_local: formData.departure_date && formData.departure_time 
            ? `${formData.departure_date}T${String(parseInt(formData.departure_time.split(':')[0]) + 2).padStart(2, '0')}:${formData.departure_time.split(':')[1]}:00`
            : `${formData.departure_date || new Date().toISOString().split('T')[0]}T10:00:00`,
          arrival_time_utc: formData.departure_date && formData.departure_time 
            ? `${formData.departure_date}T${String(parseInt(formData.departure_time.split(':')[0]) + 2).padStart(2, '0')}:${formData.departure_time.split(':')[1]}:00`
            : `${formData.departure_date || new Date().toISOString().split('T')[0]}T10:00:00`,
          distance: '0.00', // Default distance
          flight_time: '02:00:00', // Default 2 hour flight time
          ground_time: '00:30:00', // Default 30 min ground time
          passenger_leg: true,
          status: 'pending'
        };
        
        console.log('Creating trip line with data:', tripLineData);
        const tripLineResponse = await ApiService.post('/trip-lines/', tripLineData);
        console.log('Trip line created successfully:', tripLineResponse.data);
      } catch (tripLineError) {
        console.error('Error creating trip line:', tripLineError);
        // Don't fail the whole operation if trip line creation fails
      }
    }
    
    Swal.fire({
      title: "Success!",
      text: `Trip ${formData.trip_number} has been created successfully.`,
      icon: "success",
      confirmButtonText: "OK"
    }).then(() => {
      hideModal(modalRef.value);
      // Emit event to refresh trips list
      emit('tripCreated', response.data);
      // Reset form
      resetForm();
    });
  } catch (error: any) {
    console.error('Error creating trip:', error);
    const errorMessage = error.response?.data?.detail || 
                        error.response?.data?.message || 
                        error.message || 
                        "Failed to create trip. Please try again.";
    
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

const resetForm = () => {
  formData.trip_number = '';
  formData.type = '';
  formData.departure_airport = '';
  formData.arrival_airport = '';
  formData.departure_date = '';
  formData.departure_time = '';
  formData.patient_id = '';
  formData.aircraft_id = '';
  formData.notes = '';
  formData.status = 'pending';
  formData.priority = 'routine';
};
</script>