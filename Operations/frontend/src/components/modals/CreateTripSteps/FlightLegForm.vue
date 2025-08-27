<template>
  <div>
    <!--begin::Crew Change Warning-->
    <div v-if="showCrewChangeWarning" class="alert alert-info d-flex align-items-center mb-5">
      <KTIcon icon-name="information" icon-class="fs-2x text-info me-3" />
      <div>
        <h6 class="mb-1 text-info">Crew Change Detected</h6>
        <div class="text-gray-700 fs-7">
          The crew for this leg differs from the previous leg. You may want to add an overnight event between legs if needed.
        </div>
      </div>
    </div>
    <!--end::Crew Change Warning-->

    <!--begin::Route Section-->
    <div class="row g-9 mb-6">
      <div class="col-md-6 fv-row">
        <AirportSearchSelect
          v-model="legData.origin_airport"
          label="Departure Airport"
          placeholder="Search departure airport..."
          help-text="Search by airport name, IATA/ICAO code, or city"
          required
          @airport-selected="onOriginAirportSelected"
        />
      </div>
      <div class="col-md-6 fv-row">
        <AirportSearchSelect
          v-model="legData.destination_airport"
          label="Arrival Airport"
          placeholder="Search arrival airport..."
          help-text="Search by airport name, IATA/ICAO code, or city"
          required
          @airport-selected="onDestinationAirportSelected"
        />
      </div>
    </div>
    <!--end::Route Section-->

    <!--begin::Timing Section-->
    <div class="row g-9 mb-6">
      <div class="col-md-4 fv-row">
        <label class="required fs-6 fw-semibold mb-2">Departure Date</label>
        <input
          v-model="legData.departure_date"
          type="date"
          class="form-control form-control-solid"
          :min="today"
          @change="emitCrewChange"
        />
      </div>
      <div class="col-md-4 fv-row">
        <label class="required fs-6 fw-semibold mb-2">Departure Time</label>
        <input
          v-model="legData.departure_time"
          type="time"
          class="form-control form-control-solid"
          @change="emitCrewChange"
        />
      </div>
      <div class="col-md-4 fv-row">
        <label class="fs-6 fw-semibold mb-2">Flight Time (hours)</label>
        <input
          v-model.number="legData.flight_time_hours"
          type="number"
          class="form-control form-control-solid"
          min="0"
          max="24"
          step="0.1"
          placeholder="Auto-calculated"
          @input="calculateArrivalTime"
        />
        <div class="form-text">You can override.</div>
      </div>
    </div>

    <!--begin::Arrival Time Section---->
    <div class="row g-9 mb-6">
      <div class="col-md-6 fv-row">
        <label class="fs-6 fw-semibold mb-2">Arrival Date</label>
        <input
          v-model="legData.arrival_date"
          type="date"
          class="form-control form-control-solid"
          readonly
        />
        <div class="form-text">Auto-calculated from departure time + flight time</div>
      </div>
      <div class="col-md-6 fv-row">
        <label class="fs-6 fw-semibold mb-2">Arrival Time</label>
        <input
          v-model="legData.arrival_time"
          type="time"
          class="form-control form-control-solid"
          readonly
        />
        <div class="form-text">Auto-calculated from departure time + flight time</div>
      </div>
    </div>
    <!--end::Arrival Time Section---->
    <!--end::Timing Section-->

    <!--begin::Duty Time Section-->
    <div class="row g-9 mb-6">
      <div class="col-md-6 fv-row">
        <label class="fs-6 fw-semibold mb-2">Pre-flight Duty Time (hours)</label>
        <input
          v-model.number="legData.pre_flight_duty_hours"
          type="number"
          class="form-control form-control-solid"
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
          v-model.number="legData.post_flight_duty_hours"
          type="number"
          class="form-control form-control-solid"
          min="0"
          max="24"
          step="0.5"
          placeholder="1.0"
        />
        <div class="form-text">Time required for post-flight activities (default: 1 hour)</div>
      </div>
    </div>
    <!--end::Duty Time Section-->

    <!--begin::Crew Section-->
    <div class="separator separator-dashed my-6"></div>
    <h6 class="fw-bold text-gray-900 mb-4">Crew Assignment</h6>
    
    <div class="row g-9 mb-6">
      <div class="col-md-6 fv-row">
        <label class="required fs-6 fw-semibold mb-2">Pilot in Command (PIC)</label>
        <select 
          v-model="legData.pic_staff_id" 
          @change="emitCrewChange"
          class="form-select form-select-solid"
        >
          <option value="">Select pilot...</option>
          <option v-for="staff in picEligibleStaff" :key="staff.id" :value="staff.id">
            {{ getStaffDisplayName(staff) }} <span class="text-muted">(PIC)</span>
          </option>
        </select>
        <div class="form-text">Only staff with active PIC role membership are shown</div>
      </div>
      <div class="col-md-6 fv-row">
        <label class="required fs-6 fw-semibold mb-2">Second in Command (SIC)</label>
        <select 
          v-model="legData.sic_staff_id" 
          @change="emitCrewChange"
          class="form-select form-select-solid"
        >
          <option value="">Select co-pilot...</option>
          <option v-for="staff in sicEligibleStaff" :key="staff.id" :value="staff.id">
            {{ getStaffDisplayName(staff) }} <span class="text-muted">(SIC)</span>
          </option>
        </select>
        <div class="form-text">Only staff with active SIC role membership are shown</div>
      </div>
    </div>

    <!--begin::Medical Crew Section-->
    <div class="fv-row mb-6">
      <label class="fs-6 fw-semibold mb-2">Medical Crew</label>
      <select 
        v-model="legData.medical_staff_ids" 
        @change="emitCrewChange"
        class="form-select form-select-solid" 
        multiple
      >
        <option v-for="staff in medicalStaff" :key="staff.id" :value="staff.id">
          {{ getStaffDisplayName(staff) }} 
          <span class="text-muted">({{ getMedicalRoles(staff).join(', ') }})</span>
        </option>
      </select>
      <div class="form-text">Hold Ctrl/Cmd to select multiple medical crew members. Only staff with medical roles (RN, MD, Paramedic, RT) are shown.</div>
    </div>
    <!--end::Medical Crew Section-->

    <!--begin::FBO Section-->
    <div class="separator separator-dashed my-6"></div>
    <h6 class="fw-bold text-gray-900 mb-4">Fixed Base Operators (FBOs)</h6>
    
    <div class="row g-9 mb-6">
      <div class="col-md-6 fv-row">
        <label class="fs-6 fw-semibold mb-2">Departure FBO</label>
        <select v-model="legData.departure_fbo_id" class="form-select form-select-solid">
          <option value="">No FBO selected...</option>
          <option v-for="fbo in departureFbos" :key="fbo.id" :value="fbo.id">
            {{ fbo.name }}
          </option>
        </select>
        <div class="form-text">Available FBOs at departure airport</div>
      </div>
      <div class="col-md-6 fv-row">
        <label class="fs-6 fw-semibold mb-2">Arrival FBO</label>
        <select v-model="legData.arrival_fbo_id" class="form-select form-select-solid">
          <option value="">No FBO selected...</option>
          <option v-for="fbo in arrivalFbos" :key="fbo.id" :value="fbo.id">
            {{ fbo.name }}
          </option>
        </select>
        <div class="form-text">Available FBOs at arrival airport</div>
      </div>
    </div>
    <!--end::FBO Section-->

    <!--begin::Notes-->
    <div class="fv-row">
      <label class="fs-6 fw-semibold mb-2">Leg Notes</label>
      <textarea
        v-model="legData.notes"
        class="form-control form-control-solid"
        rows="2"
        placeholder="Additional notes for this flight leg..."
      ></textarea>
    </div>
    <!--end::Notes-->
  </div>
</template>

<script setup lang="ts">
import { ref, computed, watch } from 'vue';
import AirportSearchSelect from '@/components/form-controls/AirportSearchSelect.vue';
import ApiService from '@/core/services/ApiService';
import { calculateAirportDistance, calculateFlightTime } from '@/core/helpers/distanceCalculator';

const props = defineProps({
  modelValue: {
    type: Object,
    required: true
  },
  staffMembers: {
    type: Array,
    default: () => []
  },
  showCrewChangeWarning: {
    type: Boolean,
    default: false
  }
});

const emit = defineEmits(['update:modelValue', 'crew-changed']);

const legData = props.modelValue;
const departureFbos = ref<any[]>([]);
const arrivalFbos = ref<any[]>([]);

// Store full airport objects for distance calculation
const originAirportObject = ref<any>(null);
const destinationAirportObject = ref<any>(null);

// Filter staff by roles
const today = new Date().toISOString().split('T')[0];

const picEligibleStaff = computed(() => {
  return props.staffMembers.filter(staff => hasActiveRole(staff, 'PIC', today));
});

const sicEligibleStaff = computed(() => {
  return props.staffMembers.filter(staff => hasActiveRole(staff, 'SIC', today));
});

const medicalStaff = computed(() => {
  return props.staffMembers.filter(staff => hasAnyMedicalRole(staff, today));
});

// Role checking functions
const hasActiveRole = (staff: any, roleCode: string, today: string): boolean => {
  if (!staff.role_memberships || staff.role_memberships.length === 0) return false;
  
  return staff.role_memberships.some((membership: any) => {
    if (membership.role?.code !== roleCode) return false;
    
    const startDate = membership.start_on;
    const endDate = membership.end_on;
    
    const startValid = !startDate || startDate <= today;
    const endValid = !endDate || endDate >= today;
    
    return startValid && endValid;
  });
};

const hasAnyMedicalRole = (staff: any, today: string): boolean => {
  const medicalRoles = ['RN', 'MD', 'PARAMEDIC', 'RT'];
  return medicalRoles.some(roleCode => hasActiveRole(staff, roleCode, today));
};

const getMedicalRoles = (staff: any): string[] => {
  const medicalRoles = ['RN', 'MD', 'PARAMEDIC', 'RT'];
  
  if (!staff.role_memberships || staff.role_memberships.length === 0) return [];
  
  return staff.role_memberships
    .filter((membership: any) => {
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

// Airport selection handlers
const onOriginAirportSelected = async (airport: any) => {
  // Store full airport object for distance calculation
  originAirportObject.value = airport;
  
  // Load FBOs for departure airport
  if (airport) {
    try {
      const response = await ApiService.get(`/airports/${airport.id}/`);
      const airportDetails = response.data;
      departureFbos.value = airportDetails.fbos || [];
    } catch (error) {
      console.error('Error loading departure FBOs:', error);
      departureFbos.value = [];
    }
  } else {
    departureFbos.value = [];
    legData.departure_fbo_id = '';
  }
  calculateFlightTimeFromDistance();
  emitCrewChange();
};

const onDestinationAirportSelected = async (airport: any) => {
  // Store full airport object for distance calculation
  destinationAirportObject.value = airport;
  
  // Load FBOs for arrival airport
  if (airport) {
    try {
      const response = await ApiService.get(`/airports/${airport.id}/`);
      const airportDetails = response.data;
      arrivalFbos.value = airportDetails.fbos || [];
    } catch (error) {
      console.error('Error loading arrival FBOs:', error);
      arrivalFbos.value = [];
    }
  } else {
    arrivalFbos.value = [];
    legData.arrival_fbo_id = '';
  }
  calculateFlightTimeFromDistance();
  emitCrewChange();
};

// Flight time calculation
const calculateFlightTimeFromDistance = () => {
  console.log('calculateFlightTimeFromDistance called');
  console.log('Origin airport object:', originAirportObject.value);
  console.log('Destination airport object:', destinationAirportObject.value);
  
  if (originAirportObject.value && destinationAirportObject.value) {
    const distance = calculateAirportDistance(originAirportObject.value, destinationAirportObject.value);
    console.log('Calculated distance:', distance);
    
    if (distance !== null) {
      const flightTime = calculateFlightTime(distance);
      console.log('Calculated flight time:', flightTime);
      legData.flight_time_hours = flightTime;
      calculateArrivalTime();
    }
  }
};

// Calculate arrival time based on departure time and flight time
const calculateArrivalTime = () => {
  if (legData.departure_date && legData.departure_time && legData.flight_time_hours) {
    try {
      const departureDateTime = new Date(`${legData.departure_date}T${legData.departure_time}:00`);
      const flightTimeMilliseconds = legData.flight_time_hours * 60 * 60 * 1000;
      const arrivalDateTime = new Date(departureDateTime.getTime() + flightTimeMilliseconds);
      
      // Update arrival date and time
      legData.arrival_date = arrivalDateTime.toISOString().split('T')[0];
      legData.arrival_time = arrivalDateTime.toTimeString().slice(0, 5);
      
      console.log('Departure:', departureDateTime.toString());
      console.log('Flight time hours:', legData.flight_time_hours);
      console.log('Arrival:', arrivalDateTime.toString());
    } catch (error) {
      console.error('Error calculating arrival time:', error);
    }
  }
};

// Watch for airport changes to auto-calculate flight time
watch(() => [legData.origin_airport, legData.destination_airport], () => {
  calculateFlightTimeFromDistance();
}, { deep: true });

// Watch for departure time changes to recalculate arrival
watch(() => [legData.departure_date, legData.departure_time], () => {
  calculateArrivalTime();
});

// Emit crew change detection
const emitCrewChange = () => {
  // This will be handled by the parent component to detect crew changes
  emit('crew-changed', true);
};

// Watch for crew changes
let previousCrewSignature = '';

watch(() => [
  legData.pic_staff_id, 
  legData.sic_staff_id, 
  legData.medical_staff_ids
], () => {
  const currentCrewSignature = `${legData.pic_staff_id}:${legData.sic_staff_id}:${legData.medical_staff_ids.sort().join(',')}`;
  
  if (previousCrewSignature && previousCrewSignature !== currentCrewSignature) {
    emit('crew-changed', true);
  }
  
  previousCrewSignature = currentCrewSignature;
}, { deep: true });
</script>