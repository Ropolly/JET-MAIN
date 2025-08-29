<template>
  <!--begin::Card-->
  <div class="card card-flush pt-3 mb-5 mb-xl-10">
    <!--begin::Card header-->
    <div class="card-header">
      <!--begin::Card title-->
      <div class="card-title">
        <h2 class="fw-bold">Flight Itinerary & Timeline</h2>
      </div>
      <!--end::Card title-->

      <!--begin::Card toolbar-->
      <div class="card-toolbar">
        <button class="btn btn-light-secondary" disabled>
          <KTIcon icon-name="geolocation" icon-class="fs-3" />
          Track Flight
        </button>
      </div>
      <!--end::Card toolbar-->
    </div>
    <!--end::Card header-->

    <!--begin::Card body-->
    <div class="card-body pt-3">
      <!--begin::Loading-->
      <div v-if="loading" class="d-flex justify-content-center py-5">
        <div class="spinner-border" role="status">
          <span class="visually-hidden">Loading...</span>
        </div>
      </div>
      <!--end::Loading-->


      <!--begin::Timeline-->
      <div v-if="combinedTimelineItems && combinedTimelineItems.length > 0" class="timeline-wrapper">
        <div class="timeline">
          <div v-for="(item, index) in combinedTimelineItems" :key="item.id || index">
            
            <!-- Flight Leg Items -->
            <div v-if="!item.event_type">
              <!-- Leg Header with Crew, Flight Time and Ground Time -->
              <div class="mb-4 p-3 bg-light-primary rounded">
                <div class="d-flex flex-wrap align-items-center">
                  <!-- Leg Number -->
                  <div class="me-4">
                    <div class="d-flex align-items-center">
                      <KTIcon icon-name="airplane" icon-class="fs-5 text-primary me-2" />
                      <span class="text-primary fs-8 fw-bold">LEG {{ getLegNumber(index) }}</span>
                    </div>
                  </div>
                  
                  
                  <!-- Flight Time -->
                  <div class="me-4">
                    <span class="text-primary fs-8 fw-bold">Flight Time: {{ formatDuration(item.flight_time) }}</span>
                  </div>
                  
                  <!-- Ground Time -->
                  <div v-if="item.ground_time">
                    <span class="text-primary fs-8 fw-bold">Ground Time: {{ formatDuration(item.ground_time) }}</span>
                  </div>
                </div>
              </div>

              <!--begin::Departure Timeline item-->
              <div class="timeline-item align-items-center mb-5">
                <div class="timeline-icon" style="margin-left: 0px">
                  <div class="timeline-line-connector"></div>
                  <div class="d-flex align-items-center justify-content-center w-50px h-50px">
                    <KTIcon icon-name="geolocation" icon-class="fs-2 text-success" />
                  </div>
                </div>
                <div class="timeline-content m-0">
                  <div class="d-flex align-items-center mb-2">
                    <span class="fs-8 fw-bolder text-success text-uppercase me-3">Departure</span>
                    <!-- Badges -->
                    <span v-if="item.has_overnight" class="badge badge-warning me-2">
                      <KTIcon icon-name="moon" icon-class="fs-7 me-1" />
                      Overnight
                    </span>
                    <span v-if="item.has_crew_change" class="badge badge-info me-2">
                      <KTIcon icon-name="people" icon-class="fs-7 me-1" />
                      Crew Change
                    </span>
                  </div>
                  <div class="fs-6 fw-bold text-gray-800">
                    {{ getAirportName(item.origin_airport) }}
                    <span class="text-muted ms-2">({{ getAirportCode(item.origin_airport) }})</span>
                  </div>
                  <div class="fw-semibold text-gray-700 fs-7">
                    <div class="mb-3">
                      <div class="mb-2">
                        <strong>Scheduled Departure:</strong><br>
                        {{ formatDateTimeWithTimezone(item.departure_time_local, item.departure_timezone_info) }}
                      </div>
                      <div v-if="item.actual_departure_time" class="mb-2">
                        <strong>Actual Departure:</strong><br>
                        {{ formatDateTime(item.actual_departure_time) }}
                      </div>
                      <div class="mt-2">
                        <div v-if="item.pre_flight_duty_time || item.post_flight_duty_time" class="mb-2">
                          <span v-if="item.pre_flight_duty_time"><strong>Pre-Flight:</strong> {{ formatDuration(item.pre_flight_duty_time) }}</span>
                          <span v-if="item.post_flight_duty_time" :class="item.pre_flight_duty_time ? 'ms-3' : ''"><strong>Post-Flight:</strong> {{ formatDuration(item.post_flight_duty_time) }}</span>
                        </div>
                        <div v-if="getOriginFbo(item)" class="text-muted fs-8 fw-light">
                          <strong>FBO:</strong> {{ getOriginFbo(item) }}
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>

              <!--begin::Arrival Timeline item-->
              <div class="timeline-item align-items-center mb-5">
                <div class="timeline-icon" style="margin-left: 0px">
                  <div class="d-flex align-items-center justify-content-center w-50px h-50px">
                    <KTIcon icon-name="airplane" icon-class="fs-2 text-primary" />
                  </div>
                </div>
                <div class="timeline-content m-0">
                  <span class="fs-8 fw-bolder text-primary text-uppercase">Arrival</span>
                  <div class="fs-6 fw-bold text-gray-800">
                    {{ getAirportName(item.destination_airport) }}
                    <span class="text-muted ms-2">({{ getAirportCode(item.destination_airport) }})</span>
                  </div>
                  <div class="fw-semibold text-gray-700 fs-7">
                    <div class="mb-2">
                      <strong>Estimated Arrival:</strong><br>
                      {{ formatDateTimeWithTimezone(item.arrival_time_local, item.arrival_timezone_info) }}
                    </div>
                    <div v-if="item.actual_arrival_time" class="mb-2">
                      <strong>Actual Arrival:</strong><br>
                      {{ formatDateTime(item.actual_arrival_time) }}
                    </div>
                    <div v-if="getDestinationFbo(item)" class="text-muted fs-8 fw-light">
                      <strong>FBO:</strong> {{ getDestinationFbo(item) }}
                    </div>
                  </div>
                </div>
              </div>
              
              <!-- Crew Information -->
              <div v-if="item.crew_line" class="mt-3 mb-5">
                <!-- Flight Crew -->
                <div v-if="item.crew_line.primary_in_command || item.crew_line.secondary_in_command" class="mb-2">
                  <span class="text-muted fs-8 me-2">Flight Crew:</span>
                  <span v-if="item.crew_line.primary_in_command" class="text-gray-700 fs-8 me-3">
                    {{ getContactName(item.crew_line.primary_in_command) }} (PIC)
                  </span>
                  <span v-if="item.crew_line.secondary_in_command" class="text-gray-700 fs-8">
                    {{ getContactName(item.crew_line.secondary_in_command) }} (SIC)
                  </span>
                </div>
                
                <!-- Medical Crew -->
                <div v-if="getMedicalCrew(item.crew_line).length > 0" class="mb-4">
                  <span class="text-muted fs-8 me-2">Medical Crew:</span>
                  <span v-for="(medic, index) in getMedicalCrew(item.crew_line)" :key="medic.id || index" 
                        class="text-gray-700 fs-8">
                    {{ getContactName(medic) }}<span v-if="index < getMedicalCrew(item.crew_line).length - 1">, </span>
                  </span>
                </div>
                
              </div>
            </div>

            <!-- Event Items (Overnight, Crew Change) -->
            <div v-else>
              <!-- Overnight Event Header -->
              <div v-if="item.event_type === 'OVERNIGHT'" class="mb-5 p-3 bg-light-secondary rounded">
                <div class="d-flex align-items-center">
                  <KTIcon icon-name="moon" icon-class="fs-5 text-gray-800 me-2" />
                  <span class="text-gray-800 fs-8 fw-bold">Overnight stay at {{ getOvernightAirportCode(item) }}</span>
                </div>
              </div>
              
              <!-- Crew Change Events -->
              <div v-else-if="item.event_type === 'CREW_CHANGE'" class="mb-5 p-3 bg-light-info rounded">
                <div class="d-flex align-items-center">
                  <KTIcon icon-name="people" icon-class="fs-5 text-info me-2" />
                  <span class="text-info fs-8 fw-bold">Crew change at {{ getCrewChangeAirportCode(item) }}</span>
                </div>
              </div>
              
              <!-- Other Events -->
              <div v-else class="timeline-item align-items-center mb-5">
                <div class="timeline-icon" style="margin-left: 0px">
                  <div class="d-flex align-items-center justify-content-center w-50px h-50px bg-secondary">
                    <KTIcon icon-name="information" icon-class="fs-2 text-white" />
                  </div>
                </div>
                <div class="timeline-content m-0">
                  <span class="fs-8 fw-bolder text-secondary text-uppercase">{{ item.event_type }}</span>
                  <div class="fs-6 fw-bold text-gray-800">
                    {{ getEventAirportName(item) }}
                  </div>
                  <div class="fw-semibold text-gray-700 fs-7">
                    <div class="mb-2">
                      <strong>Time:</strong> {{ formatDateTime(item.start_time_local) }}
                    </div>
                    <div v-if="item.notes" class="mt-2 text-muted">
                      <strong>Notes:</strong> {{ item.notes }}
                    </div>
                  </div>
                </div>
              </div>
            </div>

          </div>
        </div>
      </div>
      <!--end::Timeline-->
      
      <!-- No itinerary message -->
      <div v-else class="alert alert-light-info">
        <div class="d-flex align-items-center">
          <KTIcon icon-name="information" icon-class="fs-2 text-info me-3" />
          <div>
            <h5 class="text-info mb-1">No Flight Itinerary</h5>
            <span class="text-gray-700">Flight legs have not been scheduled for this trip yet.</span>
          </div>
        </div>
      </div>
    </div>
    <!--end::Card body-->
  </div>
  <!--end::Card-->
</template>

<script setup lang="ts">
import { computed } from 'vue';

interface Props {
  trip: any;
  loading: boolean;
}

const props = defineProps<Props>();

// Get trip lines and combine with events for chronological timeline
const combinedTimelineItems = computed(() => {
  try {
    const tripLines = props.trip?.trip_lines || [];
    const events = props.trip?.trip_events || props.trip?.events || [];
    
    // Debug: Log event timestamps
    events.forEach(event => {
      console.log(`Event ${event.event_type}:`, {
        start_time_utc: event.start_time_utc,
        start_time_local: event.start_time_local,
        end_time_utc: event.end_time_utc,
        end_time_local: event.end_time_local,
        airport_id: event.airport_id
      });
    });
    
    // Add type indicators and extract sortable times
    const timelineItems = [
      ...tripLines.map(line => ({ 
        ...line, 
        timeline_type: 'LEG',
        sort_time: line.departure_time_utc || line.departure_time_local || 0
      })),
      ...events.map(event => ({ 
        ...event, 
        timeline_type: 'EVENT',
        sort_time: event.start_time_utc || event.start_time_local || 0
      }))
    ];
    
    // Sort chronologically by extracted time
    return timelineItems.sort((a, b) => {
      const timeA = new Date(a.sort_time);
      const timeB = new Date(b.sort_time);
      
      // Debug logging for event comparisons
      if (a.timeline_type === 'EVENT' && b.timeline_type === 'EVENT') {
        console.log(`Comparing events: ${a.event_type} vs ${b.event_type}`, {
          timeA: a.sort_time,
          timeB: b.sort_time,
          timeA_parsed: timeA,
          timeB_parsed: timeB,
          timeA_valid: !isNaN(timeA.getTime()),
          timeB_valid: !isNaN(timeB.getTime()),
          timeDiff: timeA.getTime() - timeB.getTime()
        });
      }
      
      // Handle invalid dates
      if (isNaN(timeA.getTime()) && isNaN(timeB.getTime())) {
        // If both have invalid times, apply logical ordering for events
        if (a.timeline_type === 'EVENT' && b.timeline_type === 'EVENT') {
          // Overnight should come before crew change when times are equal/invalid
          if (a.event_type === 'OVERNIGHT' && b.event_type === 'CREW_CHANGE') {
            console.log('Applying overnight before crew change (invalid times)');
            return -1;
          }
          if (a.event_type === 'CREW_CHANGE' && b.event_type === 'OVERNIGHT') {
            console.log('Applying crew change after overnight (invalid times)');
            return 1;
          }
        }
        return 0;
      }
      if (isNaN(timeA.getTime())) return 1; // Put invalid dates at end
      if (isNaN(timeB.getTime())) return -1;
      
      const timeDiff = timeA.getTime() - timeB.getTime();
      
      // If times are exactly equal, apply secondary sorting for logical event order
      if (timeDiff === 0 && a.timeline_type === 'EVENT' && b.timeline_type === 'EVENT') {
        // Overnight should come before crew change when times are equal
        if (a.event_type === 'OVERNIGHT' && b.event_type === 'CREW_CHANGE') {
          console.log('Applying overnight before crew change (equal times)');
          return -1;
        }
        if (a.event_type === 'CREW_CHANGE' && b.event_type === 'OVERNIGHT') {
          console.log('Applying crew change after overnight (equal times)');
          return 1;
        }
      }
      
      return timeDiff;
    });
  } catch (error) {
    console.error('Error processing timeline items:', error);
    return props.trip?.trip_lines || [];
  }
});

// Get airport information from airport object
const getAirportName = (airport: any): string => {
  try {
    if (!airport) return 'Unknown Airport';
    return airport.name || airport.airport_name || 'Unknown Airport';
  } catch (error) {
    return 'Unknown Airport';
  }
};

const getAirportCode = (airport: any): string => {
  try {
    if (!airport) return 'UNK';
    return airport.icao_code || airport.iata_code || airport.code || 'UNK';
  } catch (error) {
    return 'UNK';
  }
};

// Get contact name from Contact object
const getContactName = (contact: any): string => {
  try {
    if (!contact) return 'Unknown';
    const first = contact.first_name || '';
    const last = contact.last_name || '';
    const business = contact.business_name || '';
    
    // Prefer business name if available, otherwise use first/last
    if (business) return business;
    return `${first} ${last}`.trim() || 'Unknown';
  } catch (error) {
    return 'Unknown';
  }
};

// Get medical crew from crew line
const getMedicalCrew = (crewLine: any): any[] => {
  try {
    if (!crewLine) return [];
    
    // Check different possible structures
    if (Array.isArray(crewLine.medics)) {
      return crewLine.medics;
    }
    
    if (Array.isArray(crewLine.medic_ids)) {
      return crewLine.medic_ids;
    }
    
    // If it's a single medic object, wrap in array
    if (crewLine.medics && typeof crewLine.medics === 'object' && !Array.isArray(crewLine.medics)) {
      return [crewLine.medics];
    }
    
    if (crewLine.medic_ids && typeof crewLine.medic_ids === 'object' && !Array.isArray(crewLine.medic_ids)) {
      return [crewLine.medic_ids];
    }
    
    return [];
  } catch (error) {
    console.error('Error getting medical crew:', error);
    return [];
  }
};

// Get airport name for events
const getEventAirportName = (event: any): string => {
  try {
    if (!event.airport && !event.airport_id) return 'Unknown Location';
    
    // If airport object is populated
    if (event.airport) {
      return `${event.airport.name || 'Unknown'} (${event.airport.ident || event.airport.icao_code || event.airport.iata_code || ''})`;
    }
    
    return 'Location loading...';
  } catch (error) {
    return 'Unknown Location';
  }
};

// Format duration from HH:MM:SS or minutes
const formatDuration = (duration?: string | number): string => {
  try {
    if (!duration) return 'TBD';
    
    if (typeof duration === 'string' && duration.includes(':')) {
      const parts = duration.split(':');
      const hours = parseInt(parts[0]) || 0;
      const minutes = parseInt(parts[1]) || 0;
      return `${hours}h ${minutes}m`;
    }
    
    const totalMinutes = parseFloat(String(duration)) || 0;
    if (totalMinutes === 0) return 'TBD';
    
    const hours = Math.floor(totalMinutes / 60);
    const minutes = Math.round(totalMinutes % 60);
    return `${hours}h ${minutes}m`;
  } catch (error) {
    return 'TBD';
  }
};

const formatDateTime = (dateString?: string): string => {
  try {
    if (!dateString) return 'Not scheduled';
    
    // Handle the case where backend sends timezone-aware strings that should be treated as local
    let date;
    if (dateString.includes('+00') || dateString.includes('Z')) {
      // Strip timezone info and parse as local time
      const dateOnly = dateString.split('+')[0].split('Z')[0];
      date = new Date(dateOnly);
    } else {
      date = new Date(dateString);
    }
    
    return date.toLocaleString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
      timeZoneName: 'short'
    });
  } catch (error) {
    return 'Invalid date';
  }
};

// New function to format datetime with specific airport timezone
const formatDateTimeWithTimezone = (dateString?: string, timezoneInfo?: any): string => {
  try {
    if (!dateString) return 'Not scheduled';
    
    // Debug logging
    console.log('formatDateTimeWithTimezone called with:', { dateString, timezoneInfo });
    
    // Parse the date as local time (strip any timezone info)
    let localDate;
    if (dateString.includes('+00') || dateString.includes('Z')) {
      const dateOnly = dateString.split('+')[0].split('Z')[0];
      localDate = new Date(dateOnly);
    } else {
      localDate = new Date(dateString);
    }
    
    const dateFormat = localDate.toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric'
    });
    
    // If we have timezone info from the backend, use the formatted time
    if (timezoneInfo?.formatted_time) {
      console.log('Using timezone info formatted_time:', timezoneInfo.formatted_time);
      return `${dateFormat}, ${timezoneInfo.formatted_time}`;
    }
    
    // Fallback: Show time with timezone abbreviation if available
    if (timezoneInfo?.abbreviation) {
      console.log('Using timezone abbreviation:', timezoneInfo.abbreviation);
      const timeFormat = localDate.toLocaleTimeString('en-US', {
        hour: '2-digit',
        minute: '2-digit',
        hour12: true
      });
      return `${dateFormat}, ${timeFormat} ${timezoneInfo.abbreviation}`;
    }
    
    console.log('No timezone info available, showing time as local without timezone label');
    // Final fallback: Show time without timezone label to avoid confusion
    const timeFormat = localDate.toLocaleTimeString('en-US', {
      hour: '2-digit',
      minute: '2-digit',
      hour12: true
    });
    return `${dateFormat}, ${timeFormat}`;
  } catch (error) {
    console.error('Error in formatDateTimeWithTimezone:', error);
    return 'Invalid date';
  }
};

// Get leg number (only count flight legs, not events)
const getLegNumber = (index: number): number => {
  try {
    let legCount = 0;
    for (let i = 0; i <= index; i++) {
      if (!combinedTimelineItems.value[i]?.event_type) {
        legCount++;
      }
    }
    return legCount;
  } catch (error) {
    return 1;
  }
};

// Calculate overnight duration
const calculateOvernightDuration = (event: any): string => {
  try {
    if (!event.start_time_local || !event.end_time_local) {
      return 'TBD';
    }
    
    const start = new Date(event.start_time_local);
    const end = new Date(event.end_time_local);
    const diffMs = end.getTime() - start.getTime();
    
    if (diffMs <= 0) return 'TBD';
    
    const hours = Math.floor(diffMs / (1000 * 60 * 60));
    const minutes = Math.floor((diffMs % (1000 * 60 * 60)) / (1000 * 60));
    
    return `${hours}h ${minutes}m`;
  } catch (error) {
    return 'TBD';
  }
};

// Get airport code for crew change events
const getCrewChangeAirportCode = (event: any): string => {
  try {
    // If airport object exists, use it
    if (event.airport) {
      return getAirportCode(event.airport);
    }
    
    // If we only have airport_id, try to find the airport in trip lines
    if (event.airport_id) {
      const tripLines = props.trip?.trip_lines || [];
      for (const line of tripLines) {
        if (line.origin_airport?.id === event.airport_id) {
          return getAirportCode(line.origin_airport);
        }
        if (line.destination_airport?.id === event.airport_id) {
          return getAirportCode(line.destination_airport);
        }
      }
    }
    
    return 'UNK';
  } catch (error) {
    return 'UNK';
  }
};

// Get airport code for overnight events
const getOvernightAirportCode = (event: any): string => {
  try {
    // If airport object exists, use it
    if (event.airport) {
      return getAirportCode(event.airport);
    }
    
    // If we only have airport_id, try to find the airport in trip lines
    if (event.airport_id) {
      const tripLines = props.trip?.trip_lines || [];
      for (const line of tripLines) {
        if (line.origin_airport?.id === event.airport_id) {
          return getAirportCode(line.origin_airport);
        }
        if (line.destination_airport?.id === event.airport_id) {
          return getAirportCode(line.destination_airport);
        }
      }
    }
    
    return 'UNK';
  } catch (error) {
    return 'UNK';
  }
};

// Get FBO information for origin airport
const getOriginFbo = (tripLine: any): string => {
  try {
    if (tripLine?.departure_fbo?.name) {
      return tripLine.departure_fbo.name;
    }
    if (tripLine?.departure_fbo?.business_name) {
      return tripLine.departure_fbo.business_name;
    }
    return '';
  } catch (error) {
    return '';
  }
};

// Get FBO information for destination airport
const getDestinationFbo = (tripLine: any): string => {
  try {
    if (tripLine?.arrival_fbo?.name) {
      return tripLine.arrival_fbo.name;
    }
    if (tripLine?.arrival_fbo?.business_name) {
      return tripLine.arrival_fbo.business_name;
    }
    return '';
  } catch (error) {
    return '';
  }
};



</script>

<style scoped>
  .timeline-line-connector {
    position: absolute;
    left: 17px;
    top: 53px;
    width: 2px;
    height: 100%;
    border-left: 2px dashed #e4e6ef;
    z-index: 1;
  }
  
  .timeline-icon {
    position: relative;
  }
</style>