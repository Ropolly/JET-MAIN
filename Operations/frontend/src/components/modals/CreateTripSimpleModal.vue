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
              <div class="col-md-6 fv-row">
                <label class="fs-6 fw-semibold mb-2">Aircraft</label>
                <select name="aircraft_id" class="form-select form-select-solid" v-model="formData.aircraft_id">
                  <option value="">Select aircraft...</option>
                  <option v-for="plane in aircraft" :key="plane.id" :value="plane.id">
                    {{ plane.tail_number }} - {{ plane.make }} {{ plane.model }}
                  </option>
                </select>
              </div>
            </div>
            <!--end::Input group-->

            <!--begin::Trip Number (Auto-generated)-->
            <div class="fv-row mb-8">
              <label class="required fs-6 fw-semibold mb-2">Trip Number (Auto-generated)</label>
              <input
                type="text"
                class="form-control form-control-solid"
                placeholder="Will be generated automatically..."
                name="trip_number"
                v-model="formData.trip_number"
                readonly
              />
              <div class="form-text">Trip number will be automatically assigned as the next sequential number</div>
            </div>
            <!--end::Trip Number-->

            <!--begin::Input group-->
            <div class="row g-9 mb-8">
              <div class="col-md-6 fv-row">
                <AirportSearchSelect
                  v-model="formData.departure_airport"
                  label="Departure Airport"
                  placeholder="Search departure airport..."
                  help-text="Search by airport name, IATA/ICAO code, or city"
                  required
                  @airport-selected="onDepartureAirportSelected"
                />
              </div>
              <div class="col-md-6 fv-row">
                <AirportSearchSelect
                  v-model="formData.arrival_airport"
                  label="Arrival Airport"
                  placeholder="Search arrival airport..."
                  help-text="Search by airport name, IATA/ICAO code, or city"
                  required
                  @airport-selected="onArrivalAirportSelected"
                />
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

            <!--begin::Duty Time Section-->
            <div class="row g-9 mb-8">
              <div class="col-md-6 fv-row">
                <label class="fs-6 fw-semibold mb-2">Pre-flight Duty Time (hours)</label>
                <input
                  type="number"
                  class="form-control form-control-solid"
                  name="pre_flight_duty_hours"
                  v-model="formData.pre_flight_duty_hours"
                  min="0"
                  max="24"
                  step="0.5"
                  placeholder="1.0"
                />
                <div class="form-text">Time required for pre-flight preparation (default: 1 hour)</div>
              </div>
              <div class="col-md-6 fv-row">
                <label class="fs-6 fw-semibold mb-2">Post-flight Duty Time (hours)</label>
                <input
                  type="number"
                  class="form-control form-control-solid"
                  name="post_flight_duty_hours"
                  v-model="formData.post_flight_duty_hours"
                  min="0"
                  max="24"
                  step="0.5"
                  placeholder="1.0"
                />
                <div class="form-text">Time required for post-flight activities (default: 1 hour)</div>
              </div>
            </div>
            <!--end::Duty Time Section-->

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


            <!--begin::Crew Section-->
            <div class="row g-9 mb-8">
              <div class="col-md-12 mb-3">
                <div class="alert alert-info d-flex align-items-center">
                  <KTIcon icon-name="information-5" icon-class="fs-2hx text-info me-4" />
                  <div class="d-flex flex-column">
                    <h4 class="mb-1 text-info">Crew Assignment</h4>
                    <span>Both PIC and SIC must be selected to create crew assignments. Medical crew is optional for medical trips.</span>
                  </div>
                </div>
              </div>
              <div class="col-md-6 fv-row">
                <label class="required fs-6 fw-semibold mb-2">Pilot in Command (PIC)</label>
                <select name="pic_staff_id" class="form-select form-select-solid" v-model="formData.pic_staff_id">
                  <option value="">Select pilot...</option>
                  <option v-for="staff in picEligibleStaff" :key="staff.id" :value="staff.id">
                    {{ getStaffDisplayName(staff) }} <span class="text-muted">(PIC)</span>
                  </option>
                </select>
                <div class="form-text">Only staff with active PIC role membership are shown</div>
              </div>
              <div class="col-md-6 fv-row">
                <label class="required fs-6 fw-semibold mb-2">Second in Command (SIC)</label>
                <select name="sic_staff_id" class="form-select form-select-solid" v-model="formData.sic_staff_id">
                  <option value="">Select co-pilot...</option>
                  <option v-for="staff in sicEligibleStaff" :key="staff.id" :value="staff.id">
                    {{ getStaffDisplayName(staff) }} <span class="text-muted">(SIC)</span>
                  </option>
                </select>
                <div class="form-text">Only staff with active SIC role membership are shown</div>
              </div>
            </div>
            <!--end::Crew Section-->

            <!--begin::Medical Crew Section-->
            <div class="fv-row mb-8" v-if="formData.type === 'medical'">
              <label class="fs-6 fw-semibold mb-2">Medical Crew</label>
              <select name="medical_staff_ids" class="form-select form-select-solid" v-model="formData.medical_staff_ids" multiple>
                <option v-for="staff in medicalStaff" :key="staff.id" :value="staff.id">
                  {{ getStaffDisplayName(staff) }} 
                  <span class="text-muted">({{ getMedicalRoles(staff).join(', ') }})</span>
                </option>
              </select>
              <div class="form-text">Hold Ctrl/Cmd to select multiple medical crew members. Only staff with medical roles (RN, MD, Paramedic, RT) are shown.</div>
            </div>
            <!--end::Medical Crew Section-->

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
import { ref, reactive, onMounted, onUnmounted } from "vue";
import { hideModal } from "@/core/helpers/modal";
import Swal from "sweetalert2";
import ApiService from "@/core/services/ApiService";
import AirportSearchSelect from "@/components/form-controls/AirportSearchSelect.vue";

const modalRef = ref<HTMLElement | null>(null);
const isSubmitting = ref(false);
const quoteId = ref<string | null>(null);

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
  pic_staff_id: '',
  sic_staff_id: '',
  medical_staff_ids: [] as string[],
  notes: '',
  status: 'pending',
  priority: 'routine',
  pre_flight_duty_hours: 1.0,  // Default 1 hour
  post_flight_duty_hours: 1.0, // Default 1 hour
});

// Handle pre-population from quote conversion
const handlePrepopulateForm = async (event: any) => {
  const data = event.detail;
  console.log('Received pre-populate data:', data);
  if (data) {
    quoteId.value = data.quoteId;
    console.log('Set quote ID to:', quoteId.value);
    if (data.tripType) formData.type = data.tripType;
    if (data.patientId) formData.patient_id = data.patientId;
    if (data.departureAirport) {
      formData.departure_airport = data.departureAirport;
      // The AirportSearchSelect will handle loading airport details by ID
    }
    if (data.arrivalAirport) {
      formData.arrival_airport = data.arrivalAirport;
      // The AirportSearchSelect will handle loading airport details by ID
    }
    if (data.notes) formData.notes = data.notes;
    
    // Generate trip number automatically
    await generateTripNumber();
  }
};

// Dropdown data
const patients = ref<any[]>([]);
const aircraft = ref<any[]>([]);
const staffMembers = ref<any[]>([]);

// Selected airports for additional data
const selectedDepartureAirport = ref<any>(null);
const selectedArrivalAirport = ref<any>(null);
const picEligibleStaff = ref<any[]>([]);
const sicEligibleStaff = ref<any[]>([]);
const medicalStaff = ref<any[]>([]);

// Emit event to parent to refresh trips list
const emit = defineEmits(['tripCreated']);

// Fetch patients, aircraft, and crew contacts for dropdowns
const fetchDropdownData = async () => {
  try {
    // Fetch patients
    const patientsResponse = await ApiService.get('/patients/?page_size=100');
    patients.value = patientsResponse.data.results || patientsResponse.data || [];
    console.log('Loaded patients:', patients.value);
  } catch (error) {
    console.error('Error fetching patients:', error);
  }
  
  try {
    // Fetch aircraft
    const aircraftResponse = await ApiService.get('/aircraft/?page_size=100');
    aircraft.value = aircraftResponse.data.results || aircraftResponse.data || [];
    console.log('Loaded aircraft:', aircraft.value);
  } catch (error) {
    console.error('Error fetching aircraft:', error);
  }
  
  // Note: Airports are now handled by the AirportSearchSelect components
  
  try {
    // Fetch staff for crew selection with role memberships (request large page size to get all staff)
    const staffResponse = await ApiService.get('/staff/?page_size=100');
    staffMembers.value = staffResponse.data.results || staffResponse.data || [];
    
    console.log('Loaded staff members:', staffMembers.value.length);
    
    // Filter staff by role memberships
    filterStaffByRoles();
    
  } catch (error) {
    console.error('Error fetching staff:', error);
  }
};

// Filter staff members by their role memberships
const filterStaffByRoles = () => {
  const today = new Date().toISOString().split('T')[0];
  
  // Filter for PIC-eligible staff (those with active PIC role membership)
  picEligibleStaff.value = staffMembers.value.filter(staff => {
    return hasActiveRole(staff, 'PIC', today);
  });
  
  // Filter for SIC-eligible staff (those with active SIC role membership)
  sicEligibleStaff.value = staffMembers.value.filter(staff => {
    return hasActiveRole(staff, 'SIC', today);
  });
  
  // Filter for medical staff (those with medical role memberships)
  medicalStaff.value = staffMembers.value.filter(staff => {
    return hasAnyMedicalRole(staff, today);
  });
  
  console.log('Filtered staff - PIC:', picEligibleStaff.value.length, 'SIC:', sicEligibleStaff.value.length, 'Medical:', medicalStaff.value.length);
};

// Check if staff has active role membership for a specific role code
const hasActiveRole = (staff: any, roleCode: string, today: string): boolean => {
  if (!staff.role_memberships || staff.role_memberships.length === 0) return false;
  
  return staff.role_memberships.some((membership: any) => {
    // Check if this membership is for the requested role
    if (membership.role?.code !== roleCode) return false;
    
    // Check if membership is currently active
    const startDate = membership.start_on;
    const endDate = membership.end_on;
    
    const startValid = !startDate || startDate <= today;
    const endValid = !endDate || endDate >= today;
    
    return startValid && endValid;
  });
};

// Check if staff has any active medical role membership
const hasAnyMedicalRole = (staff: any, today: string): boolean => {
  const medicalRoles = ['RN', 'MD', 'PARAMEDIC', 'RT'];
  return medicalRoles.some(roleCode => hasActiveRole(staff, roleCode, today));
};

// Airport selection handlers
const onDepartureAirportSelected = (airport: any) => {
  selectedDepartureAirport.value = airport;
  console.log('Departure airport selected:', airport);
};

const onArrivalAirportSelected = (airport: any) => {
  selectedArrivalAirport.value = airport;
  console.log('Arrival airport selected:', airport);
};

// Generate unique five-digit auto-incrementing trip number
const generateTripNumber = async () => {
  try {
    // Fetch existing trips ordered by trip_number descending to get the highest
    // We only need a small page size since we're just looking for the max
    const response = await ApiService.get('/trips/?ordering=-created_on&page_size=200');
    const existingTrips = response.data.results || response.data || [];
    
    console.log('Fetched trips for number generation:', existingTrips.length);
    
    // Find the highest numeric trip number
    let maxTripNumber = 0;
    
    for (const trip of existingTrips) {
      if (trip.trip_number) {
        // Try to parse the trip number as an integer
        const numberOnly = parseInt(trip.trip_number, 10);
        if (!isNaN(numberOnly) && numberOnly > maxTripNumber) {
          maxTripNumber = numberOnly;
        }
      }
    }
    
    console.log('Current highest trip number:', maxTripNumber);
    
    // If no trips exist or all have non-numeric trip numbers, start from 10000
    if (maxTripNumber < 10000) {
      maxTripNumber = 9999; // Will be incremented to 10000
    }
    
    // Increment to get the next number
    let nextTripNumber = maxTripNumber + 1;
    
    // Ensure we don't exceed 5 digits
    if (nextTripNumber > 99999) {
      console.warn('Trip number would exceed 5 digits, wrapping around');
      nextTripNumber = 10000; // Wrap around to start of 5-digit range
    }
    
    // Format as 5-digit number (pad with zeros if needed)
    const tripNumber = String(nextTripNumber).padStart(5, '0');
    
    // Double-check uniqueness
    const checkResponse = await ApiService.get(`/trips/?trip_number=${tripNumber}`);
    const conflictingTrips = checkResponse.data.results || checkResponse.data || [];
    
    if (conflictingTrips.length > 0) {
      // If there's a conflict, try incrementing until we find an available number
      console.warn(`Trip number ${tripNumber} already exists, finding next available...`);
      
      let attemptNumber = nextTripNumber;
      let found = false;
      const maxAttempts = 100; // Prevent infinite loop
      
      for (let i = 0; i < maxAttempts; i++) {
        attemptNumber++;
        if (attemptNumber > 99999) {
          attemptNumber = 10000; // Wrap around
        }
        
        const testNumber = String(attemptNumber).padStart(5, '0');
        const testResponse = await ApiService.get(`/trips/?trip_number=${testNumber}`);
        const testConflicts = testResponse.data.results || testResponse.data || [];
        
        if (testConflicts.length === 0) {
          formData.trip_number = testNumber;
          found = true;
          break;
        }
      }
      
      if (!found) {
        throw new Error('Could not find available trip number after 100 attempts');
      }
    } else {
      formData.trip_number = tripNumber;
    }
    
    console.log('Generated trip number:', formData.trip_number);
    
  } catch (error) {
    console.error('Error generating trip number:', error);
    
    // Fallback: use timestamp-based 5-digit number
    const timestamp = Date.now();
    const fallbackNumber = String((timestamp % 90000) + 10000); // Ensures 5-digit number between 10000-99999
    formData.trip_number = fallbackNumber;
    
    console.log('Using fallback trip number:', formData.trip_number);
  }
};

// Get medical roles for a staff member
const getMedicalRoles = (staff: any): string[] => {
  const today = new Date().toISOString().split('T')[0];
  const medicalRoles = ['RN', 'MD', 'PARAMEDIC', 'RT'];
  
  if (!staff.role_memberships || staff.role_memberships.length === 0) return [];
  
  return staff.role_memberships
    .filter((membership: any) => {
      // Check if this is a medical role and is currently active
      if (!medicalRoles.includes(membership.role?.code)) return false;
      
      const startDate = membership.start_on;
      const endDate = membership.end_on;
      
      const startValid = !startDate || startDate <= today;
      const endValid = !endDate || endDate >= today;
      
      return startValid && endValid;
    })
    .map((membership: any) => membership.role?.code)
    .filter(Boolean);
};

onMounted(() => {
  fetchDropdownData();
  
  // Generate trip number when modal opens
  generateTripNumber();
  
  // Add event listener for form pre-population
  if (modalRef.value) {
    modalRef.value.addEventListener('prepopulate-trip-form', handlePrepopulateForm);
  }
});

onUnmounted(() => {
  // Clean up event listener
  if (modalRef.value) {
    modalRef.value.removeEventListener('prepopulate-trip-form', handlePrepopulateForm);
  }
});

const handleSubmit = async (e: Event) => {
  e.preventDefault();
  
  // Basic validation
  if (!formData.type) {
    Swal.fire({
      title: "Validation Error",
      text: "Please select a Trip Type",
      icon: "warning",
      confirmButtonText: "OK"
    });
    return;
  }
  
  // Ensure trip number is generated
  if (!formData.trip_number) {
    await generateTripNumber();
  }
  
  // Validate airports are selected - this is now REQUIRED for trip creation
  if (!formData.departure_airport || !formData.arrival_airport) {
    Swal.fire({
      title: "Validation Error",
      text: "Please select both Departure and Arrival airports to create the trip",
      icon: "warning",
      confirmButtonText: "OK"
    });
    return;
  }
  
  // Additional validation to ensure we have valid airport IDs
  console.log('Form validation passed - Trip Number:', formData.trip_number, 'Type:', formData.type);
  console.log('Airports - Departure:', formData.departure_airport, 'Arrival:', formData.arrival_airport);
  
  isSubmitting.value = true;
  
  try {
    // Helper function to convert hours to ISO 8601 duration format
    const hoursToIsoDuration = (hours: number): string | null => {
      if (!hours || hours === 0) return null;
      // Convert to HH:MM:SS format for Django DurationField
      const wholeHours = Math.floor(hours);
      const minutes = Math.round((hours - wholeHours) * 60);
      return `${String(wholeHours).padStart(2, '0')}:${String(minutes).padStart(2, '0')}:00`;
    };
    
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
      email_chain: [],
      // Add duty time fields
      pre_flight_duty_time: hoursToIsoDuration(formData.pre_flight_duty_hours),
      post_flight_duty_time: hoursToIsoDuration(formData.post_flight_duty_hours)
    };
    
    // If this trip is converted from a quote, include the quote reference
    if (quoteId.value) {
      tripData.quote = quoteId.value;
      console.log('Including quote ID in trip:', quoteId.value);
    }
    
    // Only include patient and aircraft if they have values (using correct field names for TripWriteSerializer)
    if (formData.patient_id) {
      tripData.patient = formData.patient_id;
    }
    
    if (formData.aircraft_id) {
      tripData.aircraft = formData.aircraft_id;
    }
    
    console.log('Creating trip with data:', tripData);
    console.log('Duty times - Pre-flight:', formData.pre_flight_duty_hours, 'hours -> ', tripData.pre_flight_duty_time);
    console.log('Duty times - Post-flight:', formData.post_flight_duty_hours, 'hours -> ', tripData.post_flight_duty_time);
    
    // Make actual API call to create trip
    const response = await ApiService.post('/trips/', tripData);
    console.log('Trip created successfully:', response.data);
    console.log('Trip ID for trip lines:', response.data.id);
    
    console.log('Checking trip line creation - Departure airport:', formData.departure_airport, 'Arrival airport:', formData.arrival_airport);
    
    // If airports are selected, create a basic trip line
    if (formData.departure_airport && formData.arrival_airport) {
      try {
        // Check if response has the expected structure
        if (!response.data || !response.data.id) {
          console.error('Trip response missing ID:', response.data);
          throw new Error('Trip created but ID not returned from server');
        }
        
        const tripId = response.data.id;
        console.log('Using trip ID for trip line:', tripId, 'Type:', typeof tripId);
        
        if (!tripId) {
          throw new Error('Trip ID is missing from response');
        }
        
        if (!formData.departure_airport || !formData.arrival_airport) {
          throw new Error('Airport IDs are missing');
        }
        
        console.log('Airport IDs - Departure:', formData.departure_airport, 'Arrival:', formData.arrival_airport);
        
        // Create crew line FIRST if we have both required crew members
        let crewLineId: string | null = null;
        if (formData.pic_staff_id && formData.sic_staff_id) {
          try {
            crewLineId = await createCrewLineFirst();
            console.log('Crew line created first with ID:', crewLineId);
          } catch (crewLineError) {
            console.error('Error creating crew line:', crewLineError);
            // Continue without crew line
            console.log('Continuing trip line creation without crew assignment');
          }
        } else if (formData.pic_staff_id || formData.sic_staff_id) {
          console.log('Skipping crew line creation - both PIC and SIC are required, but only one was selected');
        }
        
        // Now create trip line with crew_line reference if we have it
        const tripLineData: any = {
          trip: tripId,
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
          distance: '500.00', // Default distance
          flight_time: '02:00:00', // Default 2 hour flight time
          ground_time: '00:30:00', // Default 30 min ground time
          passenger_leg: true,
          status: 'pending'
        };
        
        // Include crew_line if we created one
        if (crewLineId) {
          tripLineData.crew_line = crewLineId;
          console.log('Including crew line ID in trip line creation:', crewLineId);
        }
        
        console.log('Creating trip line with data:', tripLineData);
        const tripLineResponse = await ApiService.post('/trip-lines/', tripLineData);
        console.log('Trip line created successfully with crew line reference:', tripLineResponse.data);
      } catch (tripLineError) {
        console.error('Error creating trip line:', tripLineError);
        console.error('Trip line error details:', tripLineError.response?.data);
        if (typeof tripLineData !== 'undefined') {
          console.error('Trip line request data was:', tripLineData);
        }
        
        let errorMessage = tripLineError.message;
        if (tripLineError.response?.data) {
          // Try to extract the most useful error message
          if (typeof tripLineError.response.data === 'object') {
            errorMessage = JSON.stringify(tripLineError.response.data);
          } else {
            errorMessage = tripLineError.response.data.detail || tripLineError.response.data.toString();
          }
        }
        
        // Show user that trip line creation failed
        Swal.fire({
          title: "Warning",
          text: `Trip created but flight route could not be set up: ${errorMessage}`,
          icon: "warning",
          confirmButtonText: "OK"
        });
      }
    } else {
      console.log('No airports selected, skipping trip line creation');
    }
    
    const successText = quoteId.value 
      ? `Trip ${formData.trip_number} has been created successfully from quote conversion.`
      : `Trip ${formData.trip_number} has been created successfully.`;
    
    Swal.fire({
      title: "Success!",
      text: successText,
      icon: "success",
      confirmButtonText: "OK"
    }).then(() => {
      hideModal(modalRef.value);
      // Emit event to refresh trips list
      emit('tripCreated', response.data);
      // Reset form
      resetForm();
      
      // If converted from quote, optionally redirect to the trips page or refresh quote
      if (quoteId.value) {
        // You could emit a special event or navigate somewhere specific
        console.log('Trip created from quote:', quoteId.value);
      }
    });
  } catch (error: any) {
    console.error('Error creating trip:', error);
    console.error('Trip creation error details:', error.response?.data);
    if (typeof tripData !== 'undefined') {
      console.error('Trip request data was:', tripData);
    }
    
    let errorMessage = "Failed to create trip. Please try again.";
    if (error.response?.data) {
      // Try to extract the most useful error message
      if (typeof error.response.data === 'object') {
        errorMessage = JSON.stringify(error.response.data);
      } else {
        errorMessage = error.response.data.detail || error.response.data.message || error.response.data.toString();
      }
    } else if (error.message) {
      errorMessage = error.message;
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

// Helper function to display contact names
const getContactDisplayName = (contact: any): string => {
  if (!contact) return 'Unknown Contact';
  
  const firstName = contact.first_name || '';
  const lastName = contact.last_name || '';
  const fullName = `${firstName} ${lastName}`.trim();
  
  if (fullName) {
    return fullName;
  }
  
  return contact.business_name || contact.email || 'Contact';
};

// Helper function to display staff names
const getStaffDisplayName = (staff: any): string => {
  if (!staff || !staff.contact) return 'Unknown Staff';
  
  const contact = staff.contact;
  const firstName = contact.first_name || '';
  const lastName = contact.last_name || '';
  const businessName = contact.business_name || '';
  
  if (businessName) return businessName;
  if (firstName || lastName) {
    return `${firstName} ${lastName}`.trim();
  }
  
  return contact.email || 'Staff Member';
};

// Helper function to get contact ID from staff ID
const getContactIdFromStaffId = (staffId: string): string | null => {
  const staff = staffMembers.value.find(s => s.id === staffId);
  return staff ? staff.contact_id : null;
};

// Helper function to get multiple contact IDs from staff IDs
const getContactIdsFromStaffIds = (staffIds: string[]): string[] => {
  return staffIds.map(staffId => getContactIdFromStaffId(staffId)).filter(Boolean) as string[];
};

// Function to create crew line first (before trip line)
const createCrewLineFirst = async (): Promise<string> => {
  console.log('Creating crew line first (before trip line)');
  
  // Get contact IDs from staff IDs
  const picContactId = formData.pic_staff_id ? getContactIdFromStaffId(formData.pic_staff_id) : null;
  const sicContactId = formData.sic_staff_id ? getContactIdFromStaffId(formData.sic_staff_id) : null;
  const medicContactIds = formData.type === 'medical' && formData.medical_staff_ids.length > 0 
    ? getContactIdsFromStaffIds(formData.medical_staff_ids) 
    : [];
  
  // Both PIC and SIC are required
  if (!picContactId || !sicContactId) {
    throw new Error('Both Pilot in Command and Second in Command are required to create a crew line');
  }
  
  // Prepare crew line data
  const crewLineData: any = {
    primary_in_command: picContactId,
    secondary_in_command: sicContactId,
    status: 'pending'
  };
  
  // Add medical crew if we have them
  if (medicContactIds.length > 0) {
    crewLineData.medic_ids = medicContactIds;
    console.log('Including medical crew:', medicContactIds);
  }
  
  console.log('Creating crew line with data:', crewLineData);
  
  // Create the crew line
  const crewLineResponse = await ApiService.post('/crew-lines/', crewLineData);
  console.log('Crew line POST response:', crewLineResponse.data);
  
  // Extract the ID from the response
  let crewLineId: string;
  
  if (crewLineResponse.data.id) {
    crewLineId = crewLineResponse.data.id;
  } else {
    // Try Location header
    const locationHeader = crewLineResponse.headers?.location;
    if (locationHeader) {
      const idMatch = locationHeader.match(/([a-f\d-]+)\/?$/);
      if (idMatch) {
        crewLineId = idMatch[1];
      } else {
        throw new Error('Could not extract crew line ID from Location header');
      }
    } else {
      // Fallback: fetch the latest crew line
      console.log('No ID in response, fetching latest crew line');
      const crewLinesResponse = await ApiService.get('/crew-lines/?ordering=-created_on&limit=1');
      const crewLines = crewLinesResponse.data.results || crewLinesResponse.data || [];
      if (crewLines.length > 0) {
        crewLineId = crewLines[0].id;
      } else {
        throw new Error('Could not determine crew line ID after creation');
      }
    }
  }
  
  console.log('Crew line created with ID:', crewLineId);
  return crewLineId;
};

// [DEPRECATED - Not used anymore, keeping for reference]
// Function to create crew line for trips (old approach - created crew line after trip line)
const createCrewLineForTrip_OLD = async (tripLineId: string) => {
  console.log('Creating crew line for trip line:', tripLineId);
  
  try {
    // Get contact IDs from staff IDs
    const picContactId = formData.pic_staff_id ? getContactIdFromStaffId(formData.pic_staff_id) : null;
    const sicContactId = formData.sic_staff_id ? getContactIdFromStaffId(formData.sic_staff_id) : null;
    const medicContactIds = formData.type === 'medical' && formData.medical_staff_ids.length > 0 
      ? getContactIdsFromStaffIds(formData.medical_staff_ids) 
      : [];
    
    // Check if we have the minimum required crew (at least PIC and SIC are required by the model)
    if (!picContactId || !sicContactId) {
      console.warn('CrewLine requires both PIC and SIC, but only have:', {
        pic: picContactId, 
        sic: sicContactId
      });
      
      // For now, skip crew line creation if we don't have both required crew members
      // In a production system, you might want to handle this differently
      throw new Error('Both Pilot in Command and Second in Command are required to create a crew line');
    }
    
    // Prepare crew line data with selected crew members
    const crewLineData: any = {
      primary_in_command: picContactId,
      secondary_in_command: sicContactId,
      status: 'pending'
    };
    
    // Add medical crew if we have them (DRF will handle the many-to-many relationship)
    if (medicContactIds.length > 0) {
      crewLineData.medic_ids = medicContactIds;
      console.log('Including medical crew in crew line creation:', medicContactIds);
    }
    
    console.log('Creating crew line with complete data:', crewLineData);
    
    // Step 1: Create the crew line with all data in one request
    const crewLineResponse = await ApiService.post('/crew-lines/', crewLineData);
    console.log('Crew line POST response:', crewLineResponse.data);
    
    // The write serializer doesn't return the ID, so we need to get it
    let crewLineId: string;
    
    // Check if we have an ID in the response
    if (crewLineResponse.data.id) {
      crewLineId = crewLineResponse.data.id;
    } else {
      // Try to get ID from Location header if the backend sets it
      const locationHeader = crewLineResponse.headers?.location;
      if (locationHeader) {
        // Extract ID from location URL like /api/crew-lines/{id}/
        const idMatch = locationHeader.match(/([a-f\d-]+)\/?$/);
        crewLineId = idMatch ? idMatch[1] : '';
      } else {
        // As a last resort, fetch the latest crew line (this is not ideal but works)
        console.log('No ID in response, fetching crew lines to find the created one');
        const crewLinesResponse = await ApiService.get('/crew-lines/?ordering=-created_on&limit=1');
        const crewLines = crewLinesResponse.data.results || crewLinesResponse.data || [];
        if (crewLines.length > 0) {
          crewLineId = crewLines[0].id;
          console.log('Found crew line ID from GET request:', crewLineId);
        } else {
          throw new Error('Could not determine crew line ID after creation');
        }
      }
    }
    
    console.log('Crew line created with ID:', crewLineId);
    
    // Step 2: Update the trip line to reference the created crew line
    if (!tripLineId) {
      throw new Error('Cannot update trip line - trip line ID is missing');
    }
    
    if (!crewLineId) {
      throw new Error('Cannot update trip line - crew line ID is missing');
    }
    
    const updateTripLineData = {
      crew_line: crewLineId
    };
    
    console.log('Updating trip line', tripLineId, 'with crew line reference:', crewLineId);
    
    try {
      const patchResponse = await ApiService.patch(`/trip-lines/${tripLineId}/`, updateTripLineData);
      console.log('Trip line PATCH response:', patchResponse.data);
      console.log('Trip line updated successfully with crew line reference');
    } catch (patchError) {
      console.error('Failed to update trip line with crew line:', patchError);
      console.error('PATCH error details:', patchError.response?.data);
      
      // Try alternative approach - use PUT with all required fields
      console.log('Trying alternative approach - fetching trip line to update it');
      const tripLineGetResponse = await ApiService.get(`/trip-lines/${tripLineId}/`);
      const existingTripLine = tripLineGetResponse.data;
      
      // Prepare full update data
      const fullUpdateData = {
        trip: existingTripLine.trip.id || existingTripLine.trip,
        origin_airport: existingTripLine.origin_airport.id || existingTripLine.origin_airport,
        destination_airport: existingTripLine.destination_airport.id || existingTripLine.destination_airport,
        crew_line: crewLineId,
        departure_time_local: existingTripLine.departure_time_local,
        departure_time_utc: existingTripLine.departure_time_utc,
        arrival_time_local: existingTripLine.arrival_time_local,
        arrival_time_utc: existingTripLine.arrival_time_utc,
        distance: existingTripLine.distance,
        flight_time: existingTripLine.flight_time,
        ground_time: existingTripLine.ground_time,
        passenger_leg: existingTripLine.passenger_leg,
        status: existingTripLine.status
      };
      
      console.log('Attempting PUT with full data:', fullUpdateData);
      const putResponse = await ApiService.put(`/trip-lines/${tripLineId}/`, fullUpdateData);
      console.log('Trip line PUT response:', putResponse.data);
      console.log('Trip line updated successfully with crew line reference using PUT');
    }
    
    return crewLineResponse.data;
  } catch (error) {
    console.error('Failed to create crew line:', error);
    console.error('Error details:', error.response?.data);
    throw error;
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
  formData.pic_staff_id = '';
  formData.sic_staff_id = '';
  formData.medical_staff_ids = [];
  formData.notes = '';
  formData.status = 'pending';
  formData.priority = 'routine';
  formData.pre_flight_duty_hours = 1.0;
  formData.post_flight_duty_hours = 1.0;
  quoteId.value = null;
};
</script>