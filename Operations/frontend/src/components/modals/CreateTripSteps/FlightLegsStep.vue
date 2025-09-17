<template>
  <div class="w-100">

    <!--begin::Summary-->
    <div v-if="legs.length > 0" class="alert alert-info d-flex align-items-center mb-6">
      <KTIcon icon-name="information-5" icon-class="fs-2x text-info me-4" />
      <div>
        <h5 class="mb-1 text-info">Trip Summary</h5>
        <div class="text-gray-700">
          <strong>{{ legs.length }}</strong> flight leg{{ legs.length > 1 ? 's' : '' }}
          <span v-if="events.length > 0">
            and <strong>{{ events.length }}</strong> timeline event{{ events.length > 1 ? 's' : '' }}
          </span>
          planned for this trip.
        </div>
      </div>
    </div>
    <!--end::Summary-->

    <!--begin::Empty State-->
    <div v-if="combinedItems.length === 0" class="text-center text-muted py-10">
      <KTIcon icon-name="airplane" icon-class="fs-2x text-muted mb-3" />
      <h5 class="text-gray-600 fw-semibold mb-2">No flight legs added yet</h5>
      <p class="mb-0">Click "Add Flight Leg" below to get started with your trip planning.</p>
    </div>
    <!--end::Empty State-->

    <!--begin::Accordion-->
    <div v-if="combinedItems.length > 0" class="mb-6">
      <draggable 
        v-model="combinedItemsArray"
        class="accordion" 
        id="trip-accordion"
        item-key="id"
        handle=".drag-handle"
        :move="onMove"
        @change="onDragChange"
        ghost-class="sortable-ghost"
        chosen-class="sortable-chosen"
        drag-class="sortable-drag"
      >
        <template #item="{ element: item, index }">
          <div 
            class="accordion-item"
            :data-type="item.type"
          >
            <h2 class="accordion-header">
              <div class="d-flex align-items-center w-100">
                <div class="drag-handle me-2" style="cursor: grab;">
                  <KTIcon icon-name="menu" icon-class="fs-5 text-muted" />
                </div>
                <button 
                  class="accordion-button fw-bold flex-grow-1"
                  :class="{ collapsed: activeAccordion !== index }"
                  type="button"
                  @click="toggleAccordion(index)"
                >
                  <KTIcon 
                    :icon-name="item.type === 'leg' ? 'airplane' : getEventIcon(item.data.event_type)" 
                    icon-class="fs-5 me-3"
                  />
                  <div class="d-flex align-items-center justify-content-between w-100 me-3">
                    <div>
                      <span v-if="item.type === 'leg'">
                        Flight Leg {{ getLegNumber(index) }}
                        <span v-if="item.data.origin_airport && item.data.destination_airport" class="text-muted fs-6 ms-2">
                          {{ getAirportDisplay(item.data.origin_airport) }} → {{ getAirportDisplay(item.data.destination_airport) }}
                        </span>
                      </span>
                      <span v-else>
                        {{ getEventTitle(item.data.event_type) }}
                        <span v-if="item.data.airport_id" class="text-muted fs-6 ms-2">
                          at {{ getAirportDisplay(item.data.airport_id) }}
                        </span>
                      </span>
                    </div>
                    <div class="d-flex align-items-center">
                      <span v-if="item.type === 'leg' && shouldShowCrewChangeWarning(getLegNumber(index) - 1)" class="badge badge-warning me-2">
                        Crew Change
                      </span>
                      <button
                        type="button"
                        class="btn btn-sm btn-icon btn-light-danger ms-2"
                        @click.stop="removeItem(index)"
                      >
                        <KTIcon icon-name="trash" icon-class="fs-6" />
                      </button>
                    </div>
                  </div>
                </button>
              </div>
            </h2>
            <div 
              class="accordion-collapse collapse"
              :class="{ show: activeAccordion === index }"
            >
              <div class="accordion-body">
                <FlightLegForm 
                  v-if="item.type === 'leg'"
                  v-model="item.data"
                  :staff-members="staffMembers"
                  :show-crew-change-warning="shouldShowCrewChangeWarning(getLegNumber(index) - 1)"
                  @crew-changed="handleCrewChange(getLegNumber(index) - 1, $event)"
                />
                <TripEventForm 
                  v-else
                  v-model="item.data"
                  :staff-members="staffMembers"
                  :default-airport-id="getDefaultAirportForEvent(combinedItems.findIndex(i => i.id === item.id))"
                  :arrival-date="getArrivalDateForEvent(combinedItems.findIndex(i => i.id === item.id))"
                  :arrival-time="getArrivalTimeForEvent(combinedItems.findIndex(i => i.id === item.id))"
                />
              </div>
            </div>
          </div>
        </template>
      </draggable>
    </div>
    <!--end::Accordion-->

    <!--begin::Add Buttons-->
    <div class="row g-3 mb-6">
      <div class="col-6">
        <button 
          type="button" 
          class="btn btn-primary w-100"
          @click="addLeg"
        >
          <KTIcon icon-name="plus" icon-class="fs-4 me-1" />
          Add Flight Leg
        </button>
      </div>
      <div class="col-6">
        <button 
          type="button" 
          class="btn btn-secondary w-100"
          @click="addEvent"
        >
          <KTIcon icon-name="time" icon-class="fs-4 me-1" />
          Add Overnight Event
        </button>
      </div>
    </div>
    <!--end::Add Buttons-->

  </div>
</template>

<script setup lang="ts">
import { watch, onMounted, computed, ref } from 'vue';
import { v4 as uuidv4 } from 'uuid';
import FlightLegForm from './FlightLegForm.vue';
import TripEventForm from './TripEventForm.vue';
import ApiService from '@/core/services/ApiService';
import draggable from 'vuedraggable';

interface TripLeg {
  id: string;
  origin_airport: string;
  destination_airport: string;
  departure_date: string;
  departure_time: string;
  arrival_date?: string;
  arrival_time?: string;
  flight_time_hours?: number;
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
  before_leg_id?: string;
}

const props = defineProps({
  legs: {
    type: Array as () => TripLeg[],
    default: () => []
  },
  events: {
    type: Array as () => TripEvent[],
    default: () => []
  },
  tripData: {
    type: Object,
    required: true
  },
  staffMembers: {
    type: Array,
    default: () => []
  }
});

const emit = defineEmits(['update:legs', 'update:events', 'stepValidated']);

const legs = props.legs;
const events = props.events;

// Accordion state
const activeAccordion = ref(0); // Start with first item open

// Airport cache for display
const airportCache = ref<Map<string, any>>(new Map());

// Maintain chronological order of items
const chronologicalOrder = ref<string[]>([]);

// Combine legs and events for unified display
const combinedItems = computed(() => {
  const legItems = legs.map(leg => ({ id: leg.id, type: 'leg' as const, data: leg }));
  const eventItems = events.map(event => ({ id: event.id, type: 'event' as const, data: event }));
  const allItems = [...legItems, ...eventItems];
  
  // If we have a chronological order, use it
  if (chronologicalOrder.value.length > 0) {
    const orderedItems = [];
    for (const id of chronologicalOrder.value) {
      const item = allItems.find(item => item.id === id);
      if (item) {
        orderedItems.push(item);
      }
    }
    // Add any new items that aren't in the order yet
    for (const item of allItems) {
      if (!chronologicalOrder.value.includes(item.id)) {
        orderedItems.push(item);
      }
    }
    return orderedItems;
  }
  
  // Default: legs first, then events (initial state)
  return allItems;
});

// Draggable array that syncs with combinedItems
const combinedItemsArray = computed({
  get: () => combinedItems.value,
  set: (newOrder) => {
    // Validate chronological order - events can only be between legs
    const validOrder = validateChronologicalOrder(newOrder);
    if (!validOrder.isValid) {
      // If invalid order, revert to previous state
      console.warn('Invalid chronological order detected:', validOrder.reason);
      return;
    }
    
    // Update chronological order
    chronologicalOrder.value = newOrder.map(item => item.id);
    
    // Update legs and events arrays based on new order
    const newLegs: TripLeg[] = [];
    const newEvents: TripEvent[] = [];
    
    newOrder.forEach(item => {
      if (item.type === 'leg') {
        newLegs.push(item.data);
      } else {
        newEvents.push(item.data);
      }
    });
    
    // Clear and repopulate arrays
    legs.splice(0, legs.length, ...newLegs);
    events.splice(0, events.length, ...newEvents);
    
    emit('update:legs', legs);
    emit('update:events', events);
  }
});


// Accordion controls
const toggleAccordion = (index: number) => {
  activeAccordion.value = activeAccordion.value === index ? -1 : index;
};

// Validate chronological order for drag operations
const validateChronologicalOrder = (items: any[]): { isValid: boolean; reason?: string } => {
  if (items.length === 0) return { isValid: true };
  
  // Single item is always valid
  if (items.length === 1) return { isValid: true };
  
  // First item must be a leg (if there are multiple items)
  if (items.length > 1 && items[0].type !== 'leg') {
    return { isValid: false, reason: 'Trip must start with a flight leg' };
  }
  
  // Last item must be a leg (if there are multiple items)
  if (items.length > 1 && items[items.length - 1].type !== 'leg') {
    return { isValid: false, reason: 'Trip must end with a flight leg' };
  }
  
  // Check for consecutive events (not allowed)
  for (let i = 0; i < items.length - 1; i++) {
    const currentItem = items[i];
    const nextItem = items[i + 1];
    
    if (currentItem.type === 'event' && nextItem.type === 'event') {
      return { isValid: false, reason: 'Overnight stays cannot be consecutive' };
    }
  }
  
  return { isValid: true };
};

// Real-time drag validation
const onMove = (evt: any) => {
  const { draggedContext, relatedContext } = evt;
  const draggedItem = draggedContext.element;
  const targetIndex = relatedContext.index;
  
  // Create a temporary array to test the move
  const testItems = [...combinedItems.value];
  const currentIndex = testItems.findIndex(item => item.id === draggedItem.id);
  
  // Remove item from current position
  testItems.splice(currentIndex, 1);
  
  // Insert at new position
  testItems.splice(targetIndex, 0, draggedItem);
  
  // Validate the new order
  const validation = validateChronologicalOrder(testItems);
  
  if (!validation.isValid) {
    console.log('Invalid move prevented:', validation.reason);
    return false; // Prevent the move
  }
  
  return true; // Allow the move
};

// Drag change handler
const onDragChange = (evt: any) => {
  // Close all accordions when dragging to avoid confusion
  activeAccordion.value = -1;
  
  // If an event was moved, update its default airport
  if (evt.moved && evt.moved.element.type === 'event') {
    const movedEvent = evt.moved.element;
    const newIndex = evt.moved.newIndex;
    updateEventAirportAfterDrag(movedEvent, newIndex);
  }
  
  validateStep();
};

// Helper functions for display
const getLegNumber = (combinedIndex: number): number => {
  let legCount = 0;
  for (let i = 0; i <= combinedIndex; i++) {
    if (combinedItems.value[i]?.type === 'leg') {
      legCount++;
    }
  }
  return legCount;
};

// Get default airport for event (arrival airport of preceding leg)
const getDefaultAirportForEvent = (eventIndex: number): string => {
  // Look for the most recent leg before this event
  for (let i = eventIndex - 1; i >= 0; i--) {
    const item = combinedItems.value[i];
    if (item?.type === 'leg' && item.data.destination_airport) {
      console.log(`FlightLegsStep: Default airport for event at index ${eventIndex} is ${item.data.destination_airport}`);
      return item.data.destination_airport;
    }
  }
  console.log(`FlightLegsStep: No default airport found for event at index ${eventIndex}`);
  return '';
};

const getArrivalDateForEvent = (eventIndex: number): string => {
  // Look for the most recent leg before this event
  for (let i = eventIndex - 1; i >= 0; i--) {
    const item = combinedItems.value[i];
    if (item?.type === 'leg' && item.data.arrival_date) {
      return item.data.arrival_date;
    }
  }
  return '';
};

const getArrivalTimeForEvent = (eventIndex: number): string => {
  // Look for the most recent leg before this event  
  for (let i = eventIndex - 1; i >= 0; i--) {
    const item = combinedItems.value[i];
    if (item?.type === 'leg' && item.data.arrival_time) {
      return item.data.arrival_time;
    }
  }
  return '';
};


// Update event airport when dragged between different legs
const updateEventAirportAfterDrag = (eventItem: any, newIndex: number) => {
  const defaultAirport = getDefaultAirportForEvent(newIndex);
  if (defaultAirport) {
    // Always update to the arrival airport of the preceding leg
    eventItem.data.airport_id = defaultAirport;
    console.log(`Updated overnight stay airport to ${defaultAirport} based on preceding leg`);
  }
};

// Load airport details for display
const loadAirportDetails = async (airportId: string) => {
  if (!airportId || airportCache.value.has(airportId)) return;
  
  try {
    const response = await ApiService.get(`/airports/${airportId}/`);
    airportCache.value.set(airportId, response.data);
  } catch (error) {
    console.error('Failed to load airport details:', error);
  }
};

const getAirportDisplay = (airportId: string): string => {
  if (!airportId) return 'Select Airport';
  
  const airport = airportCache.value.get(airportId);
  if (airport) {
    // Show ICAO code if available, fallback to IATA, then name
    return airport.icao_code || airport.iata_code || airport.name || airportId;
  }
  
  // Load airport details asynchronously
  loadAirportDetails(airportId);
  
  // Return ID temporarily while loading
  return '...';
};

// Remove item (leg or event)
const removeItem = (combinedIndex: number) => {
  const item = combinedItems.value[combinedIndex];
  
  // Remove from chronological order
  const orderIndex = chronologicalOrder.value.indexOf(item.id);
  if (orderIndex !== -1) {
    chronologicalOrder.value.splice(orderIndex, 1);
  }
  
  if (item.type === 'leg') {
    const legIndex = legs.findIndex(leg => leg.id === item.id);
    if (legIndex !== -1) {
      removeLeg(legIndex);
    }
  } else {
    const eventIndex = events.findIndex(event => event.id === item.id);
    if (eventIndex !== -1) {
      removeEvent(eventIndex);
    }
  }
  
  // Adjust active accordion if needed
  if (activeAccordion.value === combinedIndex) {
    activeAccordion.value = combinedIndex > 0 ? combinedIndex - 1 : 0;
  } else if (activeAccordion.value > combinedIndex) {
    activeAccordion.value--;
  }
};

// Add new leg
const addLeg = () => {
  const newLeg: TripLeg = {
    id: uuidv4(),
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
  };

  // Always add legs at the end
  legs.push(newLeg);
  emit('update:legs', legs);
  
  // Add to chronological order at the end
  chronologicalOrder.value.push(newLeg.id);
  
  // Open the newly added leg accordion after Vue updates
  setTimeout(() => {
    // Find the index of the newly added leg in the combined items
    const newLegIndex = combinedItems.value.findIndex(item => item.id === newLeg.id);
    activeAccordion.value = newLegIndex;
  }, 0);
  
  validateStep();
};

// Remove leg
const removeLeg = (index: number) => {
  legs.splice(index, 1);
  emit('update:legs', legs);
  validateStep();
};

// Add new event
const addEvent = () => {
  // Find the default airport, date, and time based on the last leg
  let defaultAirport = '';
  let inheritedDate = '';
  let inheritedTime = '';
  
  if (legs.length > 0) {
    const lastLeg = legs[legs.length - 1];
    if (lastLeg.destination_airport) {
      defaultAirport = lastLeg.destination_airport;
      console.log(`Setting new overnight stay airport to ${defaultAirport} (arrival of last leg)`);
    }
    
    // Inherit arrival date/time from the last leg, or departure if no arrival
    if (lastLeg.arrival_date && lastLeg.arrival_time) {
      inheritedDate = lastLeg.arrival_date;
      inheritedTime = lastLeg.arrival_time;
    } else if (lastLeg.departure_date && lastLeg.departure_time) {
      inheritedDate = lastLeg.departure_date;
      inheritedTime = lastLeg.departure_time;
    } else if (lastLeg.departure_date) {
      inheritedDate = lastLeg.departure_date;
      inheritedTime = '18:00'; // Default to 6 PM if no time available
    }
    console.log(`Setting overnight stay date/time to ${inheritedDate} ${inheritedTime} (from last leg)`);
  }

  // Provide default values if nothing inherited
  if (!inheritedDate) {
    const today = new Date();
    inheritedDate = today.toISOString().split('T')[0];
  }
  if (!inheritedTime) {
    inheritedTime = '18:00'; // Default to 6 PM
  }

  // Calculate end time (8 hours after start time)
  let endDate = inheritedDate;
  let endTime = inheritedTime;
  
  if (inheritedDate && inheritedTime) {
    try {
      const startDateTime = new Date(`${inheritedDate}T${inheritedTime}:00`);
      const endDateTime = new Date(startDateTime.getTime() + (8 * 60 * 60 * 1000)); // +8 hours
      
      endDate = endDateTime.toISOString().split('T')[0];
      endTime = endDateTime.toTimeString().slice(0, 5);
    } catch (error) {
      console.error('Error calculating end time:', error);
      // Fallback to next day if calculation fails
      try {
        const nextDay = new Date(inheritedDate);
        nextDay.setDate(nextDay.getDate() + 1);
        endDate = nextDay.toISOString().split('T')[0];
        endTime = '08:00'; // 8 AM next day
      } catch (fallbackError) {
        console.error('Fallback calculation also failed:', fallbackError);
      }
    }
  }

  const newEvent: TripEvent = {
    id: uuidv4(),
    event_type: 'OVERNIGHT',
    airport_id: defaultAirport,
    start_date: inheritedDate,
    start_time: inheritedTime,
    end_date: endDate,
    end_time: endTime,
    notes: ''
  };

  // Add event to events array
  events.push(newEvent);
  emit('update:events', events);
  
  // Insert event in chronological order right after the last leg
  if (legs.length > 0) {
    const lastLegId = legs[legs.length - 1].id;
    const lastLegIndex = chronologicalOrder.value.indexOf(lastLegId);
    
    if (lastLegIndex !== -1) {
      // Insert right after the last leg
      chronologicalOrder.value.splice(lastLegIndex + 1, 0, newEvent.id);
    } else {
      // Fallback: add all leg IDs to chronological order first, then add event
      legs.forEach(leg => {
        if (!chronologicalOrder.value.includes(leg.id)) {
          chronologicalOrder.value.push(leg.id);
        }
      });
      chronologicalOrder.value.push(newEvent.id);
    }
  } else {
    // No legs exist, just add the event
    chronologicalOrder.value.push(newEvent.id);
  }
  
  // Open the newly added event accordion after Vue updates
  setTimeout(() => {
    // Find the index of the newly added event in the combined items
    const newEventIndex = combinedItems.value.findIndex(item => item.id === newEvent.id);
    activeAccordion.value = newEventIndex;
  }, 0);
};

// Remove event
const removeEvent = (index: number) => {
  events.splice(index, 1);
  emit('update:events', events);
};

// Check if crew change warning should be shown
const shouldShowCrewChangeWarning = (legIndex: number): boolean => {
  if (legIndex === 0) return false;
  
  const currentLeg = legs[legIndex];
  const previousLeg = legs[legIndex - 1];
  
  if (!currentLeg || !previousLeg) return false;
  
  // Check if crew changed between legs
  const crewChanged = 
    currentLeg.pic_staff_id !== previousLeg.pic_staff_id ||
    currentLeg.sic_staff_id !== previousLeg.sic_staff_id ||
    JSON.stringify(currentLeg.medical_staff_ids.sort()) !== JSON.stringify(previousLeg.medical_staff_ids.sort());
    
  return crewChanged;
};

// Handle crew change
const handleCrewChange = (legIndex: number, crewChanged: boolean) => {
  const leg = legs[legIndex];
  const previousLeg = legs[legIndex - 1];
  
  if (!leg || !previousLeg || legIndex === 0) return;
  
  // Check if crew change event already exists for this transition
  const existingEventIndex = events.findIndex(e => 
    e.event_type === 'CREW_CHANGE' && 
    e.before_leg_id === leg.id
  );
  
  if (crewChanged) {
    // Crew is different from previous leg, create crew change event if it doesn't exist
    if (existingEventIndex === -1) {
      // Get the best available date/time for the crew change event
      const eventDate = leg.departure_date || previousLeg.departure_date || '';
      const eventTime = leg.departure_time || previousLeg.departure_time || '';
      
      // Only create crew change event if we have valid date/time
      if (eventDate && eventTime) {
        const crewChangeEvent: TripEvent = {
          id: uuidv4(),
          event_type: 'CREW_CHANGE',
          airport_id: leg.origin_airport || previousLeg.destination_airport || '',
          start_date: eventDate,
          start_time: eventTime,
          before_leg_id: leg.id,
          notes: 'Automatic crew change event'
        };
        
        events.push(crewChangeEvent);
        emit('update:events', events);
        
        // Add to chronological order right before the leg that has the crew change
        const legOrderIndex = chronologicalOrder.value.indexOf(leg.id);
        if (legOrderIndex !== -1) {
          chronologicalOrder.value.splice(legOrderIndex, 0, crewChangeEvent.id);
        } else {
          // Fallback: add at the end
          chronologicalOrder.value.push(crewChangeEvent.id);
        }
        
        console.log('Auto-created crew change event for crew difference');
      } else {
        console.warn('Cannot create crew change event - missing date/time data');
      }
    }
  } else {
    // Crew is the same as previous leg, remove crew change event if it exists
    if (existingEventIndex !== -1) {
      const eventToRemove = events[existingEventIndex];
      
      // Remove from events array
      events.splice(existingEventIndex, 1);
      emit('update:events', events);
      
      // Remove from chronological order
      const orderIndex = chronologicalOrder.value.indexOf(eventToRemove.id);
      if (orderIndex !== -1) {
        chronologicalOrder.value.splice(orderIndex, 1);
      }
      
      console.log('Removed crew change event - crew matches previous leg');
    }
  }
};

// Event helper functions
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

// Validation
const validateStep = () => {
  // At least one leg is required
  if (legs.length === 0) {
    emit('stepValidated', false);
    return false;
  }

  // All legs must be valid
  const allLegsValid = legs.every(leg => 
    leg.origin_airport &&
    leg.destination_airport &&
    leg.departure_date &&
    leg.departure_time &&
    leg.pic_staff_id &&
    leg.sic_staff_id
  );

  emit('stepValidated', allLegsValid);
  return allLegsValid;
};

// Initialize chronological order when legs are populated (e.g., in edit mode)
watch(() => legs, (newLegs) => {
  // If chronologicalOrder is empty but we have legs, initialize it
  if (chronologicalOrder.value.length === 0 && newLegs.length > 0) {
    console.log('Initializing chronological order for', newLegs.length, 'legs');
    chronologicalOrder.value = newLegs.map(leg => leg.id);
  }
}, { immediate: true });

// Watch for changes
watch(() => [legs, events], () => {
  validateStep();
  
  // Update overnight stay airports when leg destinations change
  updateOvernightAirportsBasedOnLegs();
  
  // Check for crew changes between all legs and update events accordingly
  legs.forEach((leg, index) => {
    if (index > 0) {
      const crewChanged = shouldShowCrewChangeWarning(index);
      handleCrewChange(index, crewChanged);
    }
  });
  
  // Preload airport details for display
  [...legs, ...events].forEach(item => {
    if ('origin_airport' in item && item.origin_airport) {
      loadAirportDetails(item.origin_airport);
    }
    if ('destination_airport' in item && item.destination_airport) {
      loadAirportDetails(item.destination_airport);
    }
    if ('airport_id' in item && item.airport_id) {
      loadAirportDetails(item.airport_id);
    }
  });
}, { deep: true });

// Update overnight stay airports based on preceding leg destinations
const updateOvernightAirportsBasedOnLegs = () => {
  combinedItems.value.forEach((item, index) => {
    if (item.type === 'event') {
      const defaultAirport = getDefaultAirportForEvent(index);
      if (defaultAirport && item.data.airport_id !== defaultAirport) {
        // Only update if the event doesn't have an airport set or if it matches the previous default
        // This respects user manual selections
        const shouldUpdate = !item.data.airport_id;
        
        if (shouldUpdate) {
          item.data.airport_id = defaultAirport;
          console.log(`Auto-updated overnight stay airport to ${defaultAirport}`);
        }
      }
    }
  });
};

onMounted(() => {
  // Start with no flight legs - user must add them manually
  // All accordions start closed
  activeAccordion.value = -1;
  
  validateStep();
});
</script>

<style scoped>
.card-bordered {
  border: 1px solid #e1e3ea;
}

.drag-handle {
  cursor: grab;
}

.drag-handle:active {
  cursor: grabbing;
}

.sortable-ghost {
  opacity: 0.5;
  background: #f8f9fa;
  border: 2px dashed #dee2e6;
}

.sortable-chosen {
  transform: scale(1.02);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  background: #fff;
  z-index: 1000;
}

.sortable-drag {
  transform: rotate(2deg);
  opacity: 0.9;
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.2);
}

.accordion-item {
  transition: all 0.2s ease;
}

.accordion-header {
  position: relative;
}

.accordion-button {
  border: none !important;
  box-shadow: none !important;
}

.accordion-button:focus {
  box-shadow: none !important;
}

/* Visual feedback for overnight stays */
.accordion-item[data-type="event"] {
  border-left: 4px solid #ffc107;
}

.accordion-item[data-type="leg"] {
  border-left: 4px solid #0d6efd;
}

/* Drag feedback */
.accordion-item.dragging-event {
  background: linear-gradient(90deg, #fff3cd 0%, #ffffff 100%);
}

.accordion-item.dragging-leg {
  background: linear-gradient(90deg, #cce7ff 0%, #ffffff 100%);
}
</style>