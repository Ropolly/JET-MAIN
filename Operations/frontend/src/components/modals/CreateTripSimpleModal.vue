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
                  <option value="medical">Medical Transport</option>
                  <option value="charter">Charter Flight</option>
                  <option value="part91">Part 91 Flight</option>
                  <option value="maintenance">Maintenance Flight</option>
                </select>
              </div>
            </div>
            <!--end::Input group-->

            <!--begin::Input group-->
            <div class="row g-9 mb-8">
              <div class="col-md-6 fv-row">
                <label class="fs-6 fw-semibold mb-2">Departure Airport</label>
                <select name="departure_airport" class="form-select form-select-solid" v-model="formData.departure_airport">
                  <option value="">Select departure...</option>
                  <option value="KORD">Chicago O'Hare (KORD)</option>
                  <option value="KMDW">Chicago Midway (KMDW)</option>
                  <option value="KLAX">Los Angeles (KLAX)</option>
                  <option value="KJFK">JFK New York (KJFK)</option>
                </select>
              </div>
              <div class="col-md-6 fv-row">
                <label class="fs-6 fw-semibold mb-2">Arrival Airport</label>
                <select name="arrival_airport" class="form-select form-select-solid" v-model="formData.arrival_airport">
                  <option value="">Select arrival...</option>
                  <option value="KORD">Chicago O'Hare (KORD)</option>
                  <option value="KMDW">Chicago Midway (KMDW)</option>
                  <option value="KLAX">Los Angeles (KLAX)</option>
                  <option value="KJFK">JFK New York (KJFK)</option>
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
                  {{ patient.first_name }} {{ patient.last_name }} 
                  <span v-if="patient.date_of_birth">(DOB: {{ patient.date_of_birth }})</span>
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
                  {{ plane.registration || plane.tail_number }} - {{ plane.model || plane.aircraft_type || 'Unknown Model' }}
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

// Emit event to parent to refresh trips list
const emit = defineEmits(['tripCreated']);

// Fetch patients and aircraft for dropdowns
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
};

onMounted(() => {
  fetchDropdownData();
});

const handleSubmit = async (e: Event) => {
  e.preventDefault();
  
  // Basic validation
  if (!formData.trip_number || !formData.type) {
    Swal.fire({
      title: "Validation Error",
      text: "Please fill in all required fields (Trip Number and Type)",
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
    
    // Only include patient_id and aircraft_id if they have values
    if (formData.patient_id) {
      tripData.patient_id = formData.patient_id;
    }
    
    if (formData.aircraft_id) {
      tripData.aircraft_id = formData.aircraft_id;
    }
    
    console.log('Creating trip with data:', tripData);
    
    // Make actual API call
    const response = await ApiService.post('/trips/', tripData);
    console.log('Trip created successfully:', response.data);
    
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