<template>
  <div class="card mb-5">
    <div class="card-header">
      <h3 class="card-title">Trip Timeline</h3>
    </div>
    <div class="card-body">
      <div v-if="loading" class="d-flex justify-content-center py-5">
        <div class="spinner-border" role="status">
          <span class="visually-hidden">Loading...</span>
        </div>
      </div>
      
      <div v-else-if="error" class="alert alert-danger">
        <KTIcon icon-name="warning" icon-class="fs-2x text-danger me-3" />
        {{ error }}
      </div>
      
      <div v-else-if="timelineItems.length === 0" class="text-center text-muted py-5">
        <KTIcon icon-name="time" icon-class="fs-2x text-muted mb-3" />
        <p class="mb-0">No timeline events found</p>
      </div>
      
      <div v-else class="timeline">
        <div 
          v-for="(item, index) in timelineItems" 
          :key="`${item.timeline_type}-${item.id}`"
          class="timeline-item"
        >
          <div class="timeline-line" v-if="index !== timelineItems.length - 1"></div>
          
          <!-- Flight Leg -->
          <div v-if="item.timeline_type === 'LEG'" class="timeline-content">
            <div class="timeline-icon bg-primary">
              <KTIcon icon-name="airplane" icon-class="text-white fs-6" />
            </div>
            <div class="timeline-details">
              <div class="d-flex align-items-center justify-content-between mb-2">
                <h6 class="mb-0 fw-bold">Flight Leg</h6>
                <span class="badge badge-primary fs-8">{{ item.timeline_type }}</span>
              </div>
              <div class="text-gray-700 mb-2">
                <strong>{{ item.origin_airport?.name }}</strong> ({{ item.origin_airport?.ident }})
                <KTIcon icon-name="arrow-right" icon-class="fs-7 mx-2" />
                <strong>{{ item.destination_airport?.name }}</strong> ({{ item.destination_airport?.ident }})
              </div>
              <div class="row text-gray-600 fs-7">
                <div class="col-md-6">
                  <div><strong>Departure:</strong> {{ formatDateTime(item.departure_time_local) }}</div>
                  <div><strong>Distance:</strong> {{ formatDistance(item.distance) }}</div>
                </div>
                <div class="col-md-6">
                  <div><strong>Arrival:</strong> {{ formatDateTime(item.arrival_time_local) }}</div>
                  <div><strong>Flight Time:</strong> {{ formatDuration(item.flight_time) }}</div>
                </div>
              </div>
              <div v-if="item.crew_line" class="mt-2">
                <span class="text-gray-600 fs-7">
                  <strong>Crew:</strong> 
                  {{ item.crew_line.primary_in_command?.first_name }} {{ item.crew_line.primary_in_command?.last_name }}
                  <span v-if="item.crew_line.secondary_in_command">, 
                    {{ item.crew_line.secondary_in_command.first_name }} {{ item.crew_line.secondary_in_command.last_name }}
                  </span>
                </span>
              </div>
            </div>
          </div>
          
          <!-- Trip Event -->
          <div v-else class="timeline-content">
            <div 
              class="timeline-icon"
              :class="{
                'bg-warning': item.event_type === 'OVERNIGHT',
                'bg-info': item.event_type === 'CREW_CHANGE'
              }"
            >
              <KTIcon 
                :icon-name="getEventIcon(item.event_type)" 
                icon-class="text-white fs-6" 
              />
            </div>
            <div class="timeline-details">
              <div class="d-flex align-items-center justify-content-between mb-2">
                <h6 class="mb-0 fw-bold">{{ getEventTitle(item.event_type) }}</h6>
                <span 
                  class="badge fs-8"
                  :class="{
                    'badge-warning': item.event_type === 'OVERNIGHT',
                    'badge-info': item.event_type === 'CREW_CHANGE'
                  }"
                >
                  {{ item.event_type }}
                </span>
              </div>
              <div class="text-gray-700 mb-2">
                <KTIcon icon-name="geolocation" icon-class="fs-7 me-1" />
                <strong>Location:</strong> {{ getAirportName(item.airport_id) }}
              </div>
              <div class="row text-gray-600 fs-7">
                <div class="col-md-6">
                  <div><strong>Start:</strong> {{ formatDateTime(item.start_time_local) }}</div>
                </div>
                <div class="col-md-6" v-if="item.end_time_local">
                  <div><strong>End:</strong> {{ formatDateTime(item.end_time_local) }}</div>
                  <div><strong>Duration:</strong> {{ calculateEventDuration(item.start_time_utc, item.end_time_utc) }}</div>
                </div>
              </div>
              <div v-if="item.notes" class="mt-2">
                <span class="text-gray-600 fs-7">
                  <strong>Notes:</strong> {{ item.notes }}
                </span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, computed, watch } from "vue";
import ApiService from "@/core/services/ApiService";

interface TimelineItem {
  id: string;
  timeline_type: 'LEG' | 'EVENT';
  sort_at: string;
  // Flight Leg fields
  origin_airport?: any;
  destination_airport?: any;
  departure_time_local?: string;
  departure_time_utc?: string;
  arrival_time_local?: string;
  arrival_time_utc?: string;
  distance?: string;
  flight_time?: string;
  crew_line?: any;
  // Event fields
  event_type?: 'OVERNIGHT' | 'CREW_CHANGE';
  airport_id?: string;
  start_time_local?: string;
  start_time_utc?: string;
  end_time_local?: string;
  end_time_utc?: string;
  notes?: string;
}

export default defineComponent({
  name: "TripTimeline",
  props: {
    trip: {
      type: Object,
      default: null,
    },
    loading: {
      type: Boolean,
      default: false,
    },
  },
  setup(props) {
    const timelineItems = ref<TimelineItem[]>([]);
    const timelineLoading = ref(false);
    const error = ref<string | null>(null);
    const airports = ref<Record<string, any>>({});

    const fetchTimeline = async () => {
      if (!props.trip?.id) return;
      
      try {
        timelineLoading.value = true;
        error.value = null;
        
        const response = await ApiService.get(`/trips/${props.trip.id}/timeline/`);
        timelineItems.value = response.data;
        
        // Extract unique airport IDs from events that need additional data
        const airportIds = new Set<string>();
        timelineItems.value.forEach(item => {
          if (item.timeline_type === 'EVENT' && item.airport_id) {
            airportIds.add(item.airport_id);
          }
        });
        
        // Also populate airports from existing flight leg data
        timelineItems.value.forEach(item => {
          if (item.timeline_type === 'LEG') {
            if (item.origin_airport) {
              airports.value[item.origin_airport.id] = item.origin_airport;
            }
            if (item.destination_airport) {
              airports.value[item.destination_airport.id] = item.destination_airport;
            }
          }
        });
        
        // Fetch airport details for events (flight legs already have airport data)
        if (airportIds.size > 0) {
          const airportPromises = Array.from(airportIds).map(async (airportId) => {
            try {
              const airportResponse = await ApiService.get(`/airports/${airportId}/`);
              airports.value[airportId] = airportResponse.data;
            } catch (err) {
              console.error(`Error fetching airport ${airportId}:`, err);
            }
          });
          
          await Promise.all(airportPromises);
        }
        
      } catch (err: any) {
        error.value = err.response?.data?.detail || "Failed to fetch timeline";
        console.error("Error fetching timeline:", err);
      } finally {
        timelineLoading.value = false;
      }
    };

    const formatDateTime = (dateTimeString: string | undefined): string => {
      if (!dateTimeString) return 'TBD';
      try {
        const date = new Date(dateTimeString);
        return date.toLocaleString();
      } catch {
        return 'Invalid Date';
      }
    };

    const formatDistance = (distance: string | undefined): string => {
      if (!distance) return 'TBD';
      try {
        const distanceNum = parseFloat(distance);
        return `${distanceNum.toFixed(0)} nm`;
      } catch {
        return 'TBD';
      }
    };

    const formatDuration = (duration: string | undefined): string => {
      if (!duration) return 'TBD';
      // Duration comes in HH:MM:SS format
      return duration;
    };

    const calculateEventDuration = (startTime: string | undefined, endTime: string | undefined): string => {
      if (!startTime || !endTime) return '';
      
      try {
        const start = new Date(startTime);
        const end = new Date(endTime);
        const diffMs = end.getTime() - start.getTime();
        const hours = Math.floor(diffMs / (1000 * 60 * 60));
        const minutes = Math.floor((diffMs % (1000 * 60 * 60)) / (1000 * 60));
        return `${hours}h ${minutes}m`;
      } catch {
        return '';
      }
    };

    const getEventIcon = (eventType: string): string => {
      switch (eventType) {
        case 'OVERNIGHT': return 'moon';
        case 'CREW_CHANGE': return 'people';
        default: return 'time';
      }
    };

    const getEventTitle = (eventType: string): string => {
      switch (eventType) {
        case 'OVERNIGHT': return 'Overnight Stay';
        case 'CREW_CHANGE': return 'Crew Change';
        default: return 'Event';
      }
    };

    const getAirportName = (airportId: string | undefined): string => {
      if (!airportId) return 'Unknown Airport';
      const airport = airports.value[airportId];
      return airport ? `${airport.name} (${airport.ident})` : 'Loading...';
    };

    // Watch for trip changes
    watch(() => props.trip?.id, () => {
      if (props.trip?.id) {
        fetchTimeline();
      }
    }, { immediate: true });

    const loading = computed(() => props.loading || timelineLoading.value);

    return {
      timelineItems,
      loading,
      error,
      formatDateTime,
      formatDistance,
      formatDuration,
      calculateEventDuration,
      getEventIcon,
      getEventTitle,
      getAirportName,
    };
  },
});
</script>

<style scoped>
.timeline {
  position: relative;
  padding-left: 2rem;
}

.timeline-item {
  position: relative;
  margin-bottom: 2rem;
}

.timeline-line {
  position: absolute;
  left: -1.75rem;
  top: 2.5rem;
  width: 2px;
  height: calc(100% + 1rem);
  background-color: #e1e3ea;
}

.timeline-icon {
  position: absolute;
  left: -2rem;
  top: 0;
  width: 2.5rem;
  height: 2.5rem;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  border: 3px solid #fff;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.timeline-details {
  background: #f8f9fa;
  border: 1px solid #e1e3ea;
  border-radius: 0.475rem;
  padding: 1rem;
  margin-left: 1rem;
}

.timeline-content {
  position: relative;
}
</style>