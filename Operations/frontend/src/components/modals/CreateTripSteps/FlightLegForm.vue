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
        <label class="required fs-6 fw-semibold mb-2">
          Departure Time
          <span v-if="originTimezoneInfo" class="text-muted ms-1">
            ({{ originTimezoneInfo.abbreviation }})
          </span>
        </label>
        <input
          v-model="legData.departure_time"
          type="time"
          class="form-control form-control-solid"
          @change="emitCrewChange"
        />
        <div class="form-text">
          <span v-if="originTimezoneInfo">
            {{ originTimezoneInfo.timezone }}
            <span v-if="originTimezoneInfo.is_dst" class="text-warning">(DST Active)</span>
          </span>
          <span v-else class="text-muted">Select departure airport to see timezone</span>
        </div>
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
        <label class="fs-6 fw-semibold mb-2">
          Arrival Time
          <span v-if="destinationTimezoneInfo" class="text-muted ms-1">
            ({{ destinationTimezoneInfo.abbreviation }})
          </span>
        </label>
        <input
          v-model="legData.arrival_time"
          type="time"
          class="form-control form-control-solid"
          readonly
        />
        <div class="form-text">
          <span v-if="destinationTimezoneInfo">
            {{ destinationTimezoneInfo.timezone }}
            <span v-if="destinationTimezoneInfo.is_dst" class="text-warning">(DST Active)</span>
            <br>
          </span>
          <span v-else class="text-muted">Select arrival airport to see timezone<br></span>
          Auto-calculated from departure time + flight time
        </div>
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
      <Multiselect
        v-model="legData.medical_staff_ids"
        @change="emitCrewChange"
        :options="medicalStaffOptions"
        mode="tags"
        :searchable="true"
        :close-on-select="false"
        placeholder="Select medical crew members..."
        :class="'multiselect-solid'"
      />
      <div class="form-text">Search and select multiple medical crew members. Only staff with medical roles (RN, MD, Paramedic, RT) are shown.</div>
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
import { ref, computed, watch, nextTick } from 'vue';
import Multiselect from '@vueform/multiselect';
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

// Store timezone information for airports
const originTimezoneInfo = ref<any>(null);
const destinationTimezoneInfo = ref<any>(null);

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

const medicalStaffOptions = computed(() => {
  return medicalStaff.value.map(staff => {
    const displayName = getStaffDisplayName(staff);
    const roles = getMedicalRoles(staff);
    const label = roles.length > 0
      ? `${displayName} (${roles.join(', ')})`
      : displayName;

    return {
      value: staff.id,
      label: label
    };
  });
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

// Timezone loading functions
const loadOriginTimezoneInfo = async (airportId: string) => {
  if (!airportId) {
    originTimezoneInfo.value = null;
    return;
  }
  
  try {
    console.log(`🕐 Loading origin timezone info for airport: ${airportId}`);
    const response = await ApiService.get(`/airports/${airportId}/timezone-info/`);
    originTimezoneInfo.value = response.data;
    console.log('✓ Origin timezone loaded:', response.data);
  } catch (error) {
    console.error('❌ Error loading origin timezone info:', error);
    if (error.response?.status === 400) {
      console.warn('Airport may not have timezone data, will use UTC fallback');
    } else {
      console.error('Response:', error.response?.data);
    }
    originTimezoneInfo.value = null;
  }
};

const loadDestinationTimezoneInfo = async (airportId: string) => {
  if (!airportId) {
    destinationTimezoneInfo.value = null;
    return;
  }
  
  try {
    console.log(`🕐 Loading destination timezone info for airport: ${airportId}`);
    const response = await ApiService.get(`/airports/${airportId}/timezone-info/`);
    destinationTimezoneInfo.value = response.data;
    console.log('✓ Destination timezone loaded:', response.data);
  } catch (error) {
    console.error('❌ Error loading destination timezone info:', error);
    if (error.response?.status === 400) {
      console.warn('Airport may not have timezone data, will use UTC fallback');
    } else {
      console.error('Response:', error.response?.data);
    }
    destinationTimezoneInfo.value = null;
  }
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
      
      // Load timezone information for departure airport
      await loadOriginTimezoneInfo(airport.id);
    } catch (error) {
      console.error('Error loading departure FBOs:', error);
      departureFbos.value = [];
    }
  } else {
    departureFbos.value = [];
    legData.departure_fbo_id = '';
    originTimezoneInfo.value = null;
  }
  await calculateFlightTimeFromDistance();
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
      
      // Load timezone information for arrival airport
      await loadDestinationTimezoneInfo(airport.id);
    } catch (error) {
      console.error('Error loading arrival FBOs:', error);
      arrivalFbos.value = [];
    }
  } else {
    arrivalFbos.value = [];
    legData.arrival_fbo_id = '';
    destinationTimezoneInfo.value = null;
  }
  await calculateFlightTimeFromDistance();
  emitCrewChange();
};

// Flight time calculation
const calculateFlightTimeFromDistance = async () => {
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
      
      // Wait for timezone info to be available before calculating arrival time
      await calculateArrivalTime();
    }
  }
};

// Calculate arrival time based on departure time and flight time (accounting for timezones)
const calculateArrivalTime = async (retryCount = 0) => {
  // Always require all basic fields
  if (!legData.departure_date || !legData.departure_time || !legData.flight_time_hours) {
    console.log('🚫 Missing required fields for arrival time calculation:', {
      departure_date: !!legData.departure_date,
      departure_time: !!legData.departure_time,
      flight_time_hours: !!legData.flight_time_hours
    });
    return;
  }
  
  console.log('⏰ calculateArrivalTime called with:', {
    departure_date: legData.departure_date,
    departure_time: legData.departure_time,
    flight_time_hours: legData.flight_time_hours,
    has_origin_timezone: !!originTimezoneInfo.value,
    has_destination_timezone: !!destinationTimezoneInfo.value
  });
  
  // Try timezone-aware calculation first if we have timezone info
  if (originTimezoneInfo.value && destinationTimezoneInfo.value) {
    try {
      console.log('Attempting timezone-aware calculation with:', {
        departure_date: legData.departure_date,
        departure_time: legData.departure_time,
        flight_time_hours: legData.flight_time_hours,
        origin_timezone: originTimezoneInfo.value.timezone,
        destination_timezone: destinationTimezoneInfo.value.timezone
      });
      
      // Use backend timezone conversion API for accurate calculations
      const conversionData = {
        departure_date: legData.departure_date,
        departure_time: legData.departure_time,
        flight_time_hours: legData.flight_time_hours,
        origin_timezone: originTimezoneInfo.value.timezone,
        destination_timezone: destinationTimezoneInfo.value.timezone
      };
      
      const response = await ApiService.post('/timezone/convert/', conversionData);
      const result = response.data;
      
      console.log('📡 Backend timezone conversion response:', result);
      
      if (result.arrival_date && result.arrival_time) {
        legData.arrival_date = result.arrival_date;
        legData.arrival_time = result.arrival_time;
        
        console.log('✓ Timezone-aware calculation successful:');
        console.log(`  Departure: ${legData.departure_date} ${legData.departure_time} ${originTimezoneInfo.value.abbreviation}`);
        console.log(`  Flight time: ${legData.flight_time_hours} hours`);
        console.log(`  Arrival: ${result.arrival_date} ${result.arrival_time} ${destinationTimezoneInfo.value.abbreviation}`);
        console.log(`  Set arrival_time to: ${legData.arrival_time}`);
        return; // Success - exit early
      } else {
        console.error('❌ Backend response missing arrival_date or arrival_time:', result);
      }
    } catch (error) {
      console.error('❌ Error with timezone-aware calculation:', error);
      console.error('Response details:', error.response?.data);
      console.log('Falling back to simple UTC calculation...');
    }
  } else {
    console.log('⚠️ Timezone info not available - waiting briefly before fallback...');
    
    // Wait a short time for timezone info to potentially load
    await new Promise(resolve => setTimeout(resolve, 500));
    
    // Try again with timezone info if it's now available (prevent infinite recursion)
    if (originTimezoneInfo.value && destinationTimezoneInfo.value && retryCount < 1) {
      console.log('🔄 Timezone info now available, retrying timezone-aware calculation...');
      return await calculateArrivalTime(retryCount + 1); // Recursive retry with counter
    }
    
    console.log('⚠️ Timezone info still not available, proceeding with UTC calculation');
  }
  
  // Fallback: Simple UTC calculation (treats all times as UTC)
  console.warn('⚠️ Using fallback UTC calculation - arrival time may not account for timezone differences');
  try {
    const departureDateTime = new Date(`${legData.departure_date}T${legData.departure_time}:00Z`); // Explicitly UTC
    const flightTimeMilliseconds = legData.flight_time_hours * 60 * 60 * 1000;
    const arrivalDateTime = new Date(departureDateTime.getTime() + flightTimeMilliseconds);
    
    legData.arrival_date = arrivalDateTime.getFullYear() + '-' +
                      String(arrivalDateTime.getMonth() + 1).padStart(2, '0') + '-' +
                      String(arrivalDateTime.getDate()).padStart(2, '0');
    legData.arrival_time = String(arrivalDateTime.getHours()).padStart(2, '0') + ':' +
                          String(arrivalDateTime.getMinutes()).padStart(2, '0');
    
    console.log('📅 Fallback calculation result:');
    console.log(`  Departure: ${legData.departure_date} ${legData.departure_time}`);
    console.log(`  Flight time: ${legData.flight_time_hours} hours`);
    console.log(`  Arrival: ${legData.arrival_date} ${legData.arrival_time} (local time)`);
  } catch (fallbackError) {
    console.error('❌ Even fallback calculation failed:', fallbackError);
  }
};

// Watch for airport changes to auto-calculate flight time
watch(() => [legData.origin_airport, legData.destination_airport], () => {
  calculateFlightTimeFromDistance();
}, { deep: true });

// Watch for departure time and flight time changes to recalculate arrival
watch(() => [legData.departure_date, legData.departure_time, legData.flight_time_hours], () => {
  // Only calculate if we have all required fields
  if (legData.departure_date && legData.departure_time && legData.flight_time_hours) {
    calculateArrivalTime();
  } else {
    // Clear arrival time if we don't have required data
    legData.arrival_date = '';
    legData.arrival_time = '';
    console.log('⏸️ Cleared arrival time - missing required departure data');
  }
});

// Watch for timezone info changes to recalculate arrival with proper timezone data
watch(() => [originTimezoneInfo.value, destinationTimezoneInfo.value], () => {
  console.log('🌍 Timezone info changed, recalculating arrival time...', {
    origin: originTimezoneInfo.value?.timezone,
    destination: destinationTimezoneInfo.value?.timezone
  });
  if (originTimezoneInfo.value && destinationTimezoneInfo.value && 
      legData.departure_date && legData.departure_time && legData.flight_time_hours) {
    calculateArrivalTime();
  }
});

// Emit crew change notification to parent
// Called by @change handlers on crew selection fields
const emitCrewChange = () => {
  // Use nextTick to ensure v-model update completes before parent reads the data
  nextTick(() => {
    emit('crew-changed', true);
  });
};
</script>

<style scoped>
/* Style multiselect to match Bootstrap form-select-solid */
:deep(.multiselect-solid) {
  --ms-font-size: 1rem;
  --ms-line-height: 1.5;
  --ms-bg: #f5f8fa;
  --ms-bg-disabled: #e9ecef;
  --ms-border-color: #f5f8fa;
  --ms-border-width: 1px;
  --ms-radius: 0.475rem;
  --ms-py: 0.75rem;
  --ms-px: 1rem;
  --ms-ring-width: 0;
  --ms-ring-color: transparent;
  --ms-placeholder-color: #a1a5b7;
  --ms-max-height: 15rem;

  --ms-tag-bg: #009ef7;
  --ms-tag-color: #ffffff;
  --ms-tag-radius: 0.375rem;
  --ms-tag-font-size: 0.875rem;
  --ms-tag-line-height: 1.5;
  --ms-tag-font-weight: 500;
  --ms-tag-py: 0.25rem;
  --ms-tag-px: 0.65rem;
  --ms-tag-my: 0.25rem;

  --ms-option-bg-pointed: #f5f8fa;
  --ms-option-bg-selected: #009ef7;
  --ms-option-bg-selected-pointed: #0095e8;
  --ms-option-color-pointed: #181c32;
  --ms-option-color-selected: #ffffff;
  --ms-option-color-selected-pointed: #ffffff;
  --ms-option-font-size: 1rem;
  --ms-option-py: 0.5rem;
  --ms-option-px: 1rem;

  --ms-dropdown-bg: #ffffff;
  --ms-dropdown-border-color: #e4e6ef;
  --ms-dropdown-border-width: 1px;
  --ms-dropdown-radius: 0.475rem;
}

:deep(.multiselect-solid .multiselect-wrapper) {
  min-height: calc(1.5em + 1.5rem + 2px);
}

:deep(.multiselect-solid .multiselect-tags-search) {
  background: #f5f8fa;
}
</style>