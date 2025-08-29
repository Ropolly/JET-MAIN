<template>
  <!--begin::Modal - Create trip (multi-step)-->
  <div
    class="modal fade"
    id="kt_modal_create_trip_multistep"
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
          <h2>{{ getModalTitle() }} - Step {{ currentStep }} of {{ totalSteps }}</h2>
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
        <div class="modal-body">
          <!--begin::Stepper-->
          <div class="stepper stepper-pills stepper-column d-flex flex-column flex-xl-row flex-row-fluid gap-10" id="kt_create_trip_stepper">
            <!--begin::Aside-->
            <div class="card d-flex justify-content-center justify-content-xl-start flex-row-auto w-100 w-xl-300px w-xxl-400px me-9">
              <!--begin::Wrapper-->
              <div class="card-body px-6 px-lg-10 px-xxl-15 py-20">
                <!--begin::Nav-->
                <div class="stepper-nav">
                  <!--begin::Step 1-->
                  <div class="stepper-item" :class="{ current: currentStep === 1, completed: currentStep > 1 }">
                    <!--begin::Wrapper-->
                    <div class="stepper-wrapper">
                      <!--begin::Icon-->
                      <div class="stepper-icon">
                        <i class="stepper-check fas fa-check"></i>
                        <span class="stepper-number">1</span>
                      </div>
                      <!--end::Icon-->

                      <!--begin::Label-->
                      <div class="stepper-label">
                        <h3 class="stepper-title">Trip Details</h3>
                        <div class="stepper-desc fw-semibold">Trip type, aircraft & number</div>
                      </div>
                      <!--end::Label-->
                    </div>
                    <!--end::Wrapper-->
                  </div>
                  <!--end::Step 1-->

                  <!--begin::Step 2-->
                  <div class="stepper-item" :class="{ current: currentStep === 2, completed: currentStep > 2 }">
                    <!--begin::Wrapper-->
                    <div class="stepper-wrapper">
                      <!--begin::Icon-->
                      <div class="stepper-icon">
                        <i class="stepper-check fas fa-check"></i>
                        <span class="stepper-number">2</span>
                      </div>
                      <!--end::Icon-->

                      <!--begin::Label-->
                      <div class="stepper-label">
                        <h3 class="stepper-title">Flight Legs & Events</h3>
                        <div class="stepper-desc fw-semibold">Add routes, crew & timeline events</div>
                      </div>
                      <!--end::Label-->
                    </div>
                    <!--end::Wrapper-->
                  </div>
                  <!--end::Step 2-->

                  <!--begin::Step 3-->
                  <div class="stepper-item" :class="{ current: currentStep === 3, completed: currentStep > 3 }">
                    <!--begin::Wrapper-->
                    <div class="stepper-wrapper">
                      <!--begin::Icon-->
                      <div class="stepper-icon">
                        <i class="stepper-check fas fa-check"></i>
                        <span class="stepper-number">3</span>
                      </div>
                      <!--end::Icon-->

                      <!--begin::Label-->
                      <div class="stepper-label">
                        <h3 class="stepper-title">Passengers & Patient</h3>
                        <div class="stepper-desc fw-semibold">Add patient & up to 8 passengers</div>
                      </div>
                      <!--end::Label-->
                    </div>
                    <!--end::Wrapper-->
                  </div>
                  <!--end::Step 3-->
                </div>
                <!--end::Nav-->
              </div>
              <!--end::Wrapper-->
            </div>
            <!--begin::Aside-->

            <!--begin::Content-->
            <div class="card d-flex flex-row-fluid flex-center">
              <!--begin::Form-->
              <form class="card-body py-20 w-100 mw-xl-700px px-9" id="kt_create_trip_form">
                <!--begin::Step 1-->
                <div v-if="currentStep === 1" class="current">
                  <TripDetailsStep 
                    v-model="tripData" 
                    :aircraft="aircraft"
                    @step-validated="handleStepValidated"
                  />
                </div>
                <!--end::Step 1-->

                <!--begin::Step 2-->
                <div v-if="currentStep === 2" class="current">
                  <FlightLegsStep 
                    v-model:legs="tripData.legs"
                    v-model:events="tripData.events"
                    :trip-data="tripData"
                    :staff-members="staffMembers"
                    @step-validated="handleStepValidated"
                  />
                </div>
                <!--end::Step 2-->

                <!--begin::Step 3-->
                <div v-if="currentStep === 3" class="current">
                  <PassengersStep 
                    v-model:patient="tripData.patient_id"
                    v-model:passengers="tripData.passengers"
                    :patients="patients"
                    @step-validated="handleStepValidated"
                  />
                </div>
                <!--end::Step 3-->

                <!--begin::Actions-->
                <div class="d-flex flex-stack pt-15">
                  <!--begin::Wrapper-->
                  <div class="mr-2">
                    <button
                      v-if="currentStep > 1"
                      type="button"
                      class="btn btn-lg btn-light-primary me-3"
                      @click="prevStep"
                    >
                      <KTIcon icon-name="arrow-left" icon-class="fs-4 me-1" />
                      Previous
                    </button>
                  </div>
                  <!--end::Wrapper-->

                  <!--begin::Wrapper-->
                  <div>
                    <button
                      v-if="currentStep < totalSteps"
                      type="button"
                      class="btn btn-lg btn-primary"
                      @click="nextStep"
                      :disabled="!isCurrentStepValid"
                    >
                      Continue
                      <KTIcon icon-name="arrow-right" icon-class="fs-4 ms-1" />
                    </button>

                    <button
                      v-if="currentStep === totalSteps"
                      type="button"
                      class="btn btn-lg btn-primary"
                      @click="handleSubmit"
                      :disabled="isSubmitting || !isCurrentStepValid"
                    >
                      <span v-if="!isSubmitting" class="indicator-label">
                        {{ editMode ? 'Update Trip' : 'Create Trip' }}
                        <KTIcon icon-name="arrow-right" icon-class="fs-4 ms-1" />
                      </span>
                      <span v-else class="indicator-progress">
                        Please wait...
                        <span class="spinner-border spinner-border-sm align-middle ms-2"></span>
                      </span>
                    </button>
                  </div>
                  <!--end::Wrapper-->
                </div>
                <!--end::Actions-->
              </form>
              <!--end::Form-->
            </div>
            <!--end::Content-->
          </div>
          <!--end::Stepper-->
        </div>
        <!--end::Modal body-->
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
import TripDetailsStep from "./CreateTripSteps/TripDetailsStep.vue";
import FlightLegsStep from "./CreateTripSteps/FlightLegsStep.vue"; 
import PassengersStep from "./CreateTripSteps/PassengersStep.vue";

interface TripLeg {
  id: string;
  origin_airport: string;
  destination_airport: string;
  departure_date: string;
  departure_time: string;
  pre_flight_duty_hours: number;
  post_flight_duty_hours: number;
  crew_line_id?: string;
  pic_staff_id: string;
  sic_staff_id: string;
  medical_staff_ids: string[];
  departure_fbo_id?: string;
  arrival_fbo_id?: string;
  notes?: string;
}

interface TripEvent {
  id: string;
  event_type: 'OVERNIGHT' | 'CREW_CHANGE';
  airport_id: string;
  start_date: string;
  start_time: string;
  end_date?: string;
  end_time?: string;
  crew_line_id?: string;
  notes?: string;
  before_leg_id?: string; // Which leg this event occurs before
}

interface TripPassenger {
  id: string;
  contact_id: string;
  contact_name: string;
  contact_email?: string;
  contact_phone?: string;
}

const modalRef = ref<HTMLElement | null>(null);
const currentStep = ref(1);
const totalSteps = 3;
const isSubmitting = ref(false);
const quoteId = ref<string | null>(null);
const editMode = ref(false);
const editTripId = ref<string | null>(null);
const stepValidation = ref<Record<number, boolean>>({
  1: false,
  2: false,
  3: true // Step 3 is optional, so default to valid
});

// Main trip data structure
const tripData = reactive({
  // Step 1: Trip Details
  trip_number: '',
  type: '',
  aircraft_id: '',
  notes: '',
  
  // Step 2: Flight Legs and Events  
  legs: [] as TripLeg[],
  events: [] as TripEvent[],
  
  // Step 3: Passengers and Patient
  patient_id: '',
  passengers: [] as TripPassenger[]
});

// Dropdown data
const aircraft = ref<any[]>([]);
const patients = ref<any[]>([]);
const staffMembers = ref<any[]>([]);

const emit = defineEmits(['tripCreated', 'tripUpdated']);

// Step validation
const isCurrentStepValid = ref(false);

// Modal title helper
const getModalTitle = () => {
  if (editMode.value) {
    return 'Edit Trip';
  }
  return quoteId.value ? 'Convert Quote to Trip' : 'Create New Trip';
};

const handleStepValidated = (isValid: boolean) => {
  stepValidation.value[currentStep.value] = isValid;
  isCurrentStepValid.value = isValid;
};

// Navigation
const nextStep = () => {
  if (currentStep.value < totalSteps && stepValidation.value[currentStep.value]) {
    currentStep.value++;
    isCurrentStepValid.value = stepValidation.value[currentStep.value];
  }
};

const prevStep = () => {
  if (currentStep.value > 1) {
    currentStep.value--;
    isCurrentStepValid.value = stepValidation.value[currentStep.value];
  }
};

// Load dropdown data
const fetchDropdownData = async () => {
  try {
    // Fetch aircraft
    const aircraftResponse = await ApiService.get('/aircraft/?page_size=100');
    aircraft.value = aircraftResponse.data.results || aircraftResponse.data || [];
    
    // Fetch patients  
    const patientsResponse = await ApiService.get('/patients/?page_size=100');
    patients.value = patientsResponse.data.results || patientsResponse.data || [];
    
    // Fetch staff for crew selection
    const staffResponse = await ApiService.get('/staff/?page_size=100');
    staffMembers.value = staffResponse.data.results || staffResponse.data || [];
    console.log('Loaded staff members:', staffMembers.value.length);
    if (staffMembers.value.length > 0) {
      console.log('Sample staff member:', staffMembers.value[0]);
    }
    
  } catch (error) {
    console.error('Error fetching dropdown data:', error);
  }
};

// Generate unique trip number
const generateTripNumber = async () => {
  try {
    const response = await ApiService.get('/trips/?ordering=-created_on&page_size=200');
    const existingTrips = response.data.results || response.data || [];
    
    let maxTripNumber = 0;
    for (const trip of existingTrips) {
      if (trip.trip_number) {
        const numberOnly = parseInt(trip.trip_number, 10);
        if (!isNaN(numberOnly) && numberOnly > maxTripNumber) {
          maxTripNumber = numberOnly;
        }
      }
    }
    
    if (maxTripNumber < 10000) {
      maxTripNumber = 9999;
    }
    
    let nextTripNumber = maxTripNumber + 1;
    if (nextTripNumber > 99999) {
      nextTripNumber = 10000;
    }
    
    const tripNumber = String(nextTripNumber).padStart(5, '0');
    
    // Check uniqueness
    const checkResponse = await ApiService.get(`/trips/?trip_number=${tripNumber}`);
    const conflictingTrips = checkResponse.data.results || checkResponse.data || [];
    
    if (conflictingTrips.length > 0) {
      // Find next available
      let attemptNumber = nextTripNumber;
      for (let i = 0; i < 100; i++) {
        attemptNumber++;
        if (attemptNumber > 99999) attemptNumber = 10000;
        
        const testNumber = String(attemptNumber).padStart(5, '0');
        const testResponse = await ApiService.get(`/trips/?trip_number=${testNumber}`);
        const testConflicts = testResponse.data.results || testResponse.data || [];
        
        if (testConflicts.length === 0) {
          tripData.trip_number = testNumber;
          return;
        }
      }
      throw new Error('Could not find available trip number');
    } else {
      tripData.trip_number = tripNumber;
    }
    
  } catch (error) {
    console.error('Error generating trip number:', error);
    const fallbackNumber = String((Date.now() % 90000) + 10000);
    tripData.trip_number = fallbackNumber;
  }
};

// Submit the complete trip
const handleSubmit = async () => {
  if (!stepValidation.value[1] || !stepValidation.value[2]) {
    Swal.fire({
      title: "Validation Error",
      text: "Please complete all required steps",
      icon: "warning",
      confirmButtonText: "OK"
    });
    return;
  }

  isSubmitting.value = true;

  try {
    let tripResponse;
    let createdTrip;
    
    if (editMode.value && editTripId.value) {
      // Update existing trip
      const tripApiData = {
        type: tripData.type,
        aircraft: tripData.aircraft_id || null,
        patient: tripData.patient_id || null,
        notes: tripData.notes
      };
      
      console.log('Updating trip with data:', tripApiData);
      tripResponse = await ApiService.patch(`/trips/${editTripId.value}/`, tripApiData);
      createdTrip = tripResponse.data;
      
    } else {
      // Create new trip
      const tripApiData = {
        trip_number: tripData.trip_number,
        type: tripData.type,
        aircraft: tripData.aircraft_id || null,
        patient: tripData.patient_id || null,
        quote: quoteId.value || null,
        notes: tripData.notes,
        status: 'pending',
        email_chain: []
      };

      console.log('Creating trip with data:', tripApiData);
      tripResponse = await ApiService.post('/trips/', tripApiData);
      createdTrip = tripResponse.data;
    }
    
    console.log('Trip created:', createdTrip);

    // Create trip legs and events
    await createTripLegsAndEvents(createdTrip.id);

    // Add passengers
    if (tripData.passengers.length > 0) {
      await addPassengersToTrip(createdTrip.id);
    }

    const tripNumber = tripResponse.data.trip_number;
    const actionText = editMode.value ? 'updated' : 'created';
    const eventName = editMode.value ? 'tripUpdated' : 'tripCreated';
    
    Swal.fire({
      title: "Success!",
      text: `Trip ${tripNumber} has been ${actionText} successfully.`,
      icon: "success",
      confirmButtonText: "OK"
    }).then(() => {
      hideModal(modalRef.value);
      emit(eventName, createdTrip);
      resetForm();
    });

  } catch (error: any) {
    const actionText = editMode.value ? 'updating' : 'creating';
    console.error(`Error ${actionText} trip:`, error);
    
    let errorMessage = `Failed to ${editMode.value ? 'update' : 'create'} trip. Please try again.`;
    if (error.response?.data) {
      errorMessage = typeof error.response.data === 'object' 
        ? JSON.stringify(error.response.data) 
        : error.response.data.detail || error.response.data.toString();
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

// Create trip legs and events
const createTripLegsAndEvents = async (tripId: string) => {
  // Sort legs and events by date/time
  const timeline = [];
  
  // Add legs to timeline
  for (const leg of tripData.legs) {
    timeline.push({
      type: 'leg',
      data: leg,
      datetime: `${leg.departure_date}T${leg.departure_time}`
    });
  }
  
  // Add events to timeline  
  for (const event of tripData.events) {
    timeline.push({
      type: 'event',
      data: event,
      datetime: `${event.start_date}T${event.start_time}`
    });
  }
  
  // Sort chronologically
  timeline.sort((a, b) => new Date(a.datetime).getTime() - new Date(b.datetime).getTime());
  
  // Track crew changes
  let currentCrewLineId: string | null = null;
  const createdCrewLines = new Map<string, string>(); // Key format: "pic_id:sic_id:medic_ids"
  
  // Process timeline in order
  for (let i = 0; i < timeline.length; i++) {
    const item = timeline[i];
    
    if (item.type === 'leg') {
      const leg = item.data as TripLeg;
      
      // Check if crew is assigned
      const hasCrewAssigned = leg.pic_staff_id && leg.sic_staff_id;
      
      if (hasCrewAssigned) {
        // Check if crew changed
        const crewKey = `${leg.pic_staff_id}:${leg.sic_staff_id}:${leg.medical_staff_ids.sort().join(',')}`;
        
        console.log('Processing leg with crew key:', crewKey);
        
        try {
          if (!createdCrewLines.has(crewKey)) {
            // Create new crew line
            console.log('Creating new crew line for crew key:', crewKey);
            currentCrewLineId = await createCrewLine(leg);
            
            // Verify we got a valid ID
            if (!currentCrewLineId) {
              console.error('ERROR: createCrewLine returned falsy value:', currentCrewLineId);
              throw new Error('Crew line creation returned invalid ID');
            }
            
            createdCrewLines.set(crewKey, currentCrewLineId);
            console.log('Crew line stored in map with ID:', currentCrewLineId);
            console.log('CrewLines map now contains:', Object.fromEntries(createdCrewLines));
          } else {
            currentCrewLineId = createdCrewLines.get(crewKey)!;
            console.log('Using existing crew line ID from map:', currentCrewLineId);
          }
        } catch (error) {
          console.error('Failed to create crew line:', error);
          // Continue without crew line if creation fails
          currentCrewLineId = null;
        }
      } else {
        console.log('No crew assigned for this leg, skipping crew line creation');
        currentCrewLineId = null;
      }
      
      // Create trip line (with or without crew line)
      console.log('About to create trip line with crew line ID:', currentCrewLineId);
      console.log('Crew line ID type:', typeof currentCrewLineId);
      console.log('Crew line ID value:', JSON.stringify(currentCrewLineId));
      
      const tripLineResult = await createTripLine(tripId, leg, currentCrewLineId);
      console.log('Trip line creation completed:', tripLineResult);
      
    } else if (item.type === 'event') {
      const event = item.data as TripEvent;
      
      // If it's a crew change event, find the crew line for the next leg
      let eventCrewLineId = null;
      if (event.event_type === 'CREW_CHANGE') {
        // Find the next leg after this event to get the new crew line
        const nextLegIndex = i + 1;
        
        if (nextLegIndex < timeline.length && timeline[nextLegIndex].type === 'leg') {
          const nextLeg = timeline[nextLegIndex].data as TripLeg;
          const nextCrewKey = `${nextLeg.pic_staff_id}:${nextLeg.sic_staff_id}:${nextLeg.medical_staff_ids.sort().join(',')}`;
          
          // Create the crew line for the next leg if it doesn't exist
          if (!createdCrewLines.has(nextCrewKey)) {
            const newCrewLineId = await createCrewLine(nextLeg);
            createdCrewLines.set(nextCrewKey, newCrewLineId);
            eventCrewLineId = newCrewLineId;
          } else {
            eventCrewLineId = createdCrewLines.get(nextCrewKey)!;
          }
        } else {
          // If no next leg found, use the current crew line
          eventCrewLineId = currentCrewLineId;
        }
        
        // If we still don't have a crew line ID, this is an error
        if (!eventCrewLineId) {
          console.error('CREW_CHANGE event requires a crew_line_id but none could be determined');
          console.error('Skipping CREW_CHANGE event due to missing crew_line_id');
          continue; // Skip this event
        }
        
        // Create the crew change event with the crew line ID
        await createTripEvent(tripId, event, eventCrewLineId);
      } else {
        // For non-CREW_CHANGE events, crew_line_id is optional
        await createTripEvent(tripId, event, eventCrewLineId);
      }
    }
  }
};

// Helper functions for creating trip components
const createCrewLine = async (leg: TripLeg): Promise<string> => {
  console.log('Leg data for crew line creation:', leg);
  console.log('Available staff members:', staffMembers.value);
  
  const picContactId = getContactIdFromStaffId(leg.pic_staff_id);
  const sicContactId = getContactIdFromStaffId(leg.sic_staff_id);
  const medicContactIds = leg.medical_staff_ids.map(id => getContactIdFromStaffId(id)).filter(Boolean);

  console.log('Creating crew line with:', {
    pic_staff_id: leg.pic_staff_id,
    sic_staff_id: leg.sic_staff_id,
    picContactId,
    sicContactId,
    medicContactIds
  });
  
  // Validate we have required IDs
  if (!picContactId || !sicContactId) {
    console.error('Missing required contact IDs for crew line:', {
      picContactId,
      sicContactId,
      pic_staff_id: leg.pic_staff_id,
      sic_staff_id: leg.sic_staff_id
    });
    throw new Error('Cannot create crew line without PIC and SIC contact IDs');
  }

  const crewLineData = {
    primary_in_command: picContactId,
    secondary_in_command: sicContactId,
    medic_ids: medicContactIds,
    status: 'pending'
  };

  const response = await ApiService.post('/crew-lines/', crewLineData);
  console.log('Crew line created successfully:', response.data);
  
  // Validate the crew line ID
  if (!response.data.id) {
    console.error('ERROR: Crew line was created but no ID returned:', response.data);
    throw new Error('Crew line creation failed - no ID returned');
  }
  
  console.log('Returning crew line ID:', response.data.id);
  return response.data.id;
};

const createTripLine = async (tripId: string, leg: TripLeg, crewLineId: string | null) => {
  const hoursToIsoDuration = (hours: number): string => {
    const wholeHours = Math.floor(hours);
    const minutes = Math.round((hours - wholeHours) * 60);
    return `${String(wholeHours).padStart(2, '0')}:${String(minutes).padStart(2, '0')}:00`;
  };

  const departureDateTime = `${leg.departure_date}T${leg.departure_time}:00`;
  
  // Get flight time in hours for backend calculation
  const flightTimeHours = leg.flight_time_hours || 2;

  const tripLineData: any = {
    trip: tripId,
    origin_airport: leg.origin_airport,
    destination_airport: leg.destination_airport,
    departure_fbo: leg.departure_fbo_id || null,
    arrival_fbo: leg.arrival_fbo_id || null,
    departure_time_local: departureDateTime,
    // Let backend calculate departure_time_utc from airport timezone
    // Don't send arrival times - let backend calculate from departure + flight_time
    distance: '500.00',
    flight_time: hoursToIsoDuration(flightTimeHours),
    ground_time: hoursToIsoDuration(leg.pre_flight_duty_hours + leg.post_flight_duty_hours),
    passenger_leg: true,
    status: 'pending'
  };
  
  // Only add crew_line if it exists
  if (crewLineId) {
    console.log('Adding crew_line to trip line data:', crewLineId);
    tripLineData.crew_line = crewLineId;
  } else {
    console.log('No crew line ID, creating trip line without crew assignment');
  }

  console.log('Creating trip line with data:', JSON.stringify(tripLineData, null, 2));
  
  try {
    const response = await ApiService.post('/trip-lines/', tripLineData);
    console.log('Trip line created successfully:', response.data);
    
    // Log all returned fields to see what the write serializer returns
    console.log('All fields returned by trip line creation:', Object.keys(response.data));
    
    // Note: Write serializers typically don't return related object data
    // We'll verify the crew_line was saved by checking the database separately if needed
    if (crewLineId) {
      console.log('Crew line was provided for this trip line:', {
        provided_crew_line: crewLineId,
        trip_line_id: response.data.id
      });
    }
    
    return response.data;
  } catch (error) {
    console.error('Failed to create trip line:', error);
    if (error.response) {
      console.error('Error response data:', error.response.data);
      console.error('Error response status:', error.response.status);
    }
    throw error;
  }
};

const createTripEvent = async (tripId: string, event: TripEvent, crewLineId: string | null = null) => {
  // Skip creating events with empty date/time
  if (!event.start_date || !event.start_time) {
    console.warn('Skipping trip event creation - missing start date/time:', event);
    return;
  }

  // Format datetime properly for Django (ISO format with timezone)
  const startDateTime = `${event.start_date}T${event.start_time}:00Z`;
  const endDateTime = event.end_date && event.end_time 
    ? `${event.end_date}T${event.end_time}:00Z` 
    : null;

  const eventData: any = {
    trip_id: tripId,
    airport_id: event.airport_id,
    event_type: event.event_type,
    start_time_local: startDateTime,
    start_time_utc: startDateTime,
    notes: event.notes || ''
  };

  if (endDateTime) {
    eventData.end_time_local = endDateTime;
    eventData.end_time_utc = endDateTime;
  }

  if (event.event_type === 'CREW_CHANGE') {
    if (!crewLineId) {
      console.error('CREW_CHANGE event requires crew_line_id but it is null/undefined');
      throw new Error('crew_line_id required for crew change');
    }
    eventData.crew_line_id = crewLineId;
  } else if (crewLineId) {
    // For other event types, crew_line_id is optional
    eventData.crew_line_id = crewLineId;
  }

  console.log('Creating trip event with data:', JSON.stringify(eventData, null, 2));
  await ApiService.post('/trip-events/', eventData);
};

const addPassengersToTrip = async (tripId: string) => {
  // This would depend on how passengers are linked to trips in your system
  // You might need to update the trip with passenger references or create separate passenger-trip relationships
  console.log('Adding passengers to trip:', tripId, tripData.passengers);
};

const getContactIdFromStaffId = (staffId: string): string => {
  const staff = staffMembers.value.find(s => s.id === staffId);
  // Staff object has contact nested, so we need to get the contact.id
  return staff?.contact?.id || staff?.contact_id || '';
};

const getStaffIdFromContactId = (contactId: string): string => {
  if (!contactId) return '';
  const staff = staffMembers.value.find(s => s.contact?.id === contactId || s.contact_id === contactId);
  return staff?.id || '';
};

const resetForm = () => {
  tripData.trip_number = '';
  tripData.type = '';
  tripData.aircraft_id = '';
  tripData.notes = '';
  tripData.legs = [];
  tripData.events = [];
  tripData.patient_id = '';
  tripData.passengers = [];
  quoteId.value = null;
  
  // Reset edit mode state
  editMode.value = false;
  editTripId.value = null;
  
  currentStep.value = 1;
  stepValidation.value = { 1: false, 2: false, 3: true };
  isCurrentStepValid.value = false;
};

// Handle pre-population from quote conversion
const handlePrepopulateForm = async (event: any) => {
  const data = event.detail;
  console.log('Received pre-populate data:', data);
  
  if (data) {
    // Check if this is edit mode
    if (data.mode === 'edit' && data.tripId && data.tripData) {
      editMode.value = true;
      editTripId.value = data.tripId;
      
      // Populate with existing trip data
      const trip = data.tripData;
      
      // Step 1: Trip Details
      tripData.type = trip.type || '';
      tripData.aircraft_id = trip.aircraft?.id || '';
      tripData.patient_id = trip.patient?.id || '';
      tripData.notes = trip.notes || '';
      
      // Step 2: Flight Legs - populate from trip_lines
      if (trip.trip_lines && trip.trip_lines.length > 0) {
        try {
          tripData.legs = trip.trip_lines.map((line: any, index: number) => ({
            id: `edit-leg-${index + 1}`,
            origin_airport: line.origin_airport?.id || '',
            destination_airport: line.destination_airport?.id || '',
            departure_date: line.departure_time_local ? line.departure_time_local.split('T')[0] : '',
            departure_time: line.departure_time_local ? line.departure_time_local.split('T')[1]?.substring(0, 5) : '',
            pre_flight_duty_hours: line.pre_flight_duty_hours || 1.0,
            post_flight_duty_hours: line.post_flight_duty_hours || 1.0,
            pic_staff_id: getStaffIdFromContactId(line.crew_line?.primary_in_command?.id),
            sic_staff_id: getStaffIdFromContactId(line.crew_line?.secondary_in_command?.id),
            medical_staff_ids: (line.crew_line?.medics || []).map((medic: any) => getStaffIdFromContactId(medic.id)).filter((id: string) => id),
            departure_fbo_id: line.departure_fbo?.id || '',
            arrival_fbo_id: line.arrival_fbo?.id || '',
            notes: line.notes || ''
          }));
          console.log('Populated legs from trip_lines:', tripData.legs);
        } catch (error) {
          console.error('Error processing trip lines for edit:', error);
          // Create a default leg if processing fails
          tripData.legs = [{
            id: 'edit-leg-1',
            origin_airport: '',
            destination_airport: '',
            departure_date: '',
            departure_time: '',
            pre_flight_duty_hours: 1.0,
            post_flight_duty_hours: 1.0,
            pic_staff_id: '',
            sic_staff_id: '',
            medical_staff_ids: [],
            departure_fbo_id: '',
            arrival_fbo_id: '',
            notes: ''
          }];
        }
      } else {
        // Create a default leg if no trip_lines exist
        tripData.legs = [{
          id: 'edit-leg-1',
          origin_airport: '',
          destination_airport: '',
          departure_date: '',
          departure_time: '',
          pre_flight_duty_hours: 1.0,
          post_flight_duty_hours: 1.0,
          pic_staff_id: '',
          sic_staff_id: '',
          medical_staff_ids: [],
          departure_fbo_id: '',
          arrival_fbo_id: '',
          notes: ''
        }];
      }
      
      // Set passengers if they exist
      tripData.passengers = trip.passengers_data || [];
      
      return; // Exit early for edit mode
    }
    
    // Quote conversion mode (existing logic)
    quoteId.value = data.quoteId;
    
    // Populate Step 1: Trip Details
    if (data.tripType) tripData.type = data.tripType;
    if (data.patientId) tripData.patient_id = data.patientId;
    if (data.notes) tripData.notes = data.notes;
    
    // Pre-configure first leg with quote data
    if (data.departureAirport && data.arrivalAirport) {
      // Set default departure date to today
      const today = new Date();
      const year = today.getFullYear();
      const month = String(today.getMonth() + 1).padStart(2, '0');
      const day = String(today.getDate()).padStart(2, '0');
      
      // Create initial leg from quote data
      const initialLeg: TripLeg = {
        id: `leg_${Date.now()}`,
        origin_airport: data.departureAirport,
        destination_airport: data.arrivalAirport,
        departure_date: `${year}-${month}-${day}`,
        departure_time: '09:00',
        pre_flight_duty_hours: 1.0,
        post_flight_duty_hours: 1.0,
        pic_staff_id: '',
        sic_staff_id: '',
        medical_staff_ids: [],
        departure_fbo_id: '',
        arrival_fbo_id: '',
        notes: ''
      };
      
      tripData.legs = [initialLeg];
    }
    
    // Generate trip number automatically
    await generateTripNumber();
  }
};

onMounted(() => {
  fetchDropdownData();
  generateTripNumber();
  
  // Add event listener for form pre-population
  if (modalRef.value) {
    modalRef.value.addEventListener('prepopulate-trip-form', handlePrepopulateForm);
    // Add event listener for modal close to reset form
    modalRef.value.addEventListener('hidden.bs.modal', resetForm);
  }
});

onUnmounted(() => {
  // Clean up event listeners
  if (modalRef.value) {
    modalRef.value.removeEventListener('prepopulate-trip-form', handlePrepopulateForm);
    modalRef.value.removeEventListener('hidden.bs.modal', resetForm);
  }
});
</script>

<style scoped>
.stepper-item.completed .stepper-icon {
  background-color: var(--bs-success);
  color: white;
}

.stepper-item.current .stepper-icon {
  background-color: var(--bs-primary);
  color: white;
}
</style>