<template>
  <FullCalendar
    ref="calendarRef"
    class="demo-app-calendar"
    :options="calendarOptions"
  ></FullCalendar>
</template>

<script lang="ts">
import { getAssetPath } from "@/core/helpers/assets";
import { defineComponent, nextTick, onMounted, ref, type Ref } from "vue";
import FullCalendar from "@fullcalendar/vue3";
import dayGridPlugin from "@fullcalendar/daygrid";
import timeGridPlugin from "@fullcalendar/timegrid";
import listPlugin from "@fullcalendar/list";
import interactionPlugin from "@fullcalendar/interaction";
import { TODAY } from "@/core/data/events";
import NewEventModal from "@/components/modals/forms/NewEventModal.vue";
import { Modal } from "bootstrap";
import ApiService from "@/core/services/ApiService";
import type { EventInput } from "@fullcalendar/core";
import moment from "moment";

export default defineComponent({
  name: "calendar-app-1",
  components: {
    FullCalendar,
  },
  setup() {
    const calendarRef: Ref<null | typeof FullCalendar> = ref(null);
    const calendarEvents = ref<EventInput[]>([]);

    const newEvent = () => {
      const modal = new Modal(
        document.getElementById("kt_modal_add_event") as Element
      );
      modal.show();
    };

    const fetchTripsAndEvents = async () => {
      try {
        console.log("Fetching trips and events...");

        // Fetch trips with trip lines
        const tripsResponse = await ApiService.get("/trips/");
        const trips = tripsResponse.data.results || tripsResponse.data;

        console.log("Fetched trips:", trips);

        const calendarData: EventInput[] = [];

        // Add trip legs to calendar
        trips.forEach((trip: any) => {
          console.log("Processing trip:", trip.trip_number, trip);

          if (trip.trip_lines && trip.trip_lines.length > 0) {
            trip.trip_lines.forEach((line: any) => {
              console.log("Processing trip line:", line);

              // Add flight as a single event spanning departure to arrival
              if (line.departure_time_local && line.arrival_time_local) {
                calendarData.push({
                  id: `trip-${trip.id}-leg-${line.id}`,
                  title: `✈️ ${trip.trip_number}: ${line.origin_airport?.ident || 'UNK'} → ${line.destination_airport?.ident || 'UNK'}`,
                  start: line.departure_time_local,
                  end: line.arrival_time_local,
                  className: "fc-event-primary",
                  extendedProps: {
                    type: "trip-leg",
                    trip: trip,
                    tripLine: line,
                    description: `Flight from ${line.origin_airport?.name || 'Unknown Airport'} to ${line.destination_airport?.name || 'Unknown Airport'}`,
                    aircraft: trip.aircraft?.tail_number || 'Unknown Aircraft',
                    patient: trip.patient?.info?.first_name && trip.patient?.info?.last_name
                      ? `${trip.patient.info.first_name} ${trip.patient.info.last_name}`
                      : 'No patient assigned',
                    distance: line.distance || 'Unknown',
                    flightTime: line.flight_time || 'Unknown'
                  }
                });
              }
            });
          }

          // Add trip events if they exist
          if (trip.events && trip.events.length > 0) {
            trip.events.forEach((event: any) => {
              let eventClass = "fc-event-warning";
              let eventIcon = "📅";

              if (event.event_type === "CREW_CHANGE") {
                eventClass = "fc-event-info";
                eventIcon = "👥";
              } else if (event.event_type === "OVERNIGHT") {
                eventClass = "fc-event-dark";
                eventIcon = "🏨";
              }

              calendarData.push({
                id: `event-${event.id}`,
                title: `${eventIcon} ${event.event_type.replace('_', ' ')}`,
                start: event.start_time_local,
                end: event.end_time_local || event.start_time_local,
                className: eventClass,
                extendedProps: {
                  type: "trip-event",
                  event: event,
                  description: event.notes || `${event.event_type} at ${event.airport?.name || 'Unknown Airport'}`,
                  airport: event.airport?.ident || 'Unknown Airport'
                }
              });
            });
          }
        });

        console.log("Generated calendar data:", calendarData);
        calendarEvents.value = calendarData;

        // Update calendar if it's already initialized
        if (calendarRef.value) {
          const calendarApi = calendarRef.value.getApi();
          calendarApi.removeAllEvents();
          calendarApi.addEventSource(calendarEvents.value);
        }

      } catch (error) {
        console.error("Error fetching trips and events:", error);

        // Fallback: Create some test events to verify calendar is working
        calendarEvents.value = [
          {
            id: 'test-1',
            title: '✈️ Test Flight: LAX → JFK',
            start: moment().add(1, 'day').format('YYYY-MM-DD HH:mm'),
            end: moment().add(1, 'day').add(5, 'hours').format('YYYY-MM-DD HH:mm'),
            className: 'fc-event-primary'
          },
          {
            id: 'test-2',
            title: '🛬 Test Arrival',
            start: moment().add(2, 'days').format('YYYY-MM-DD HH:mm'),
            className: 'fc-event-success'
          }
        ];

        console.log("Using fallback test events:", calendarEvents.value);
      }
    };

    const handleEventClick = (info: any) => {
      const { event } = info;
      const props = event.extendedProps;

      let modalContent = "";

      if (props.type === "trip-leg") {
        modalContent = `
          <div class="text-start">
            <p><strong>Trip:</strong> ${props.trip.trip_number}</p>
            <p><strong>Aircraft:</strong> ${props.aircraft}</p>
            <p><strong>Route:</strong> ${props.tripLine.origin_airport?.ident || 'Unknown'} → ${props.tripLine.destination_airport?.ident || 'Unknown'}</p>
            <p><strong>Patient:</strong> ${props.patient}</p>
            <p><strong>Departure:</strong> ${moment(event.start).format('MMMM Do YYYY, h:mm A')}</p>
            <p><strong>Arrival:</strong> ${moment(event.end).format('MMMM Do YYYY, h:mm A')}</p>
            <p><strong>Distance:</strong> ${props.distance}</p>
            <p><strong>Flight Time:</strong> ${props.flightTime}</p>
            <p><strong>Status:</strong> ${props.trip.status}</p>
          </div>
        `;
      } else if (props.type === "trip-event") {
        modalContent = `
          <div class="text-start">
            <p><strong>Event Type:</strong> ${props.event.event_type.replace('_', ' ')}</p>
            <p><strong>Airport:</strong> ${props.airport}</p>
            <p><strong>Start:</strong> ${moment(event.start).format('MMMM Do YYYY, h:mm A')}</p>
            ${event.end ? `<p><strong>End:</strong> ${moment(event.end).format('MMMM Do YYYY, h:mm A')}</p>` : ''}
            ${props.event.notes ? `<p><strong>Notes:</strong> ${props.event.notes}</p>` : ''}
          </div>
        `;
      }

      // Show event details in a SweetAlert modal
      import('sweetalert2').then((Swal) => {
        Swal.default.fire({
          title: event.title,
          html: modalContent,
          icon: "info",
          showCancelButton: true,
          confirmButtonText: "View Trip Details",
          cancelButtonText: "Close"
        }).then((result) => {
          if (result.isConfirmed && props.trip) {
            // Navigate to trip details if confirmed
            window.location.href = `/admin/trips/${props.trip.id}`;
          }
        });
      });
    };

    onMounted(async () => {
      await fetchTripsAndEvents();
      nextTick(function () {
        window.dispatchEvent(new Event("resize"));
      });
    });

    const calendarOptions = {
      plugins: [dayGridPlugin, timeGridPlugin, listPlugin, interactionPlugin],
      headerToolbar: {
        left: "prev,next today",
        center: "title",
        right: "dayGridMonth,timeGridWeek,timeGridDay",
      },
      initialDate: TODAY,
      navLinks: true, // can click day/week names to navigate views
      selectable: true,
      selectMirror: true,

      views: {
        dayGridMonth: { buttonText: "month" },
        timeGridWeek: { buttonText: "week" },
        timeGridDay: { buttonText: "day" },
      },

      editable: false, // Disable editing for trip events
      dayMaxEvents: true, // allow "more" link when too many events
      events: calendarEvents,
      dateClick: newEvent,
      eventClick: handleEventClick,
    };

    return {
      calendarOptions,
      newEvent,
      getAssetPath,
      calendarRef,
      fetchTripsAndEvents,
    };
  },
});
</script>

<style lang="scss">
.fc .fc-button {
  padding: 0.75rem 1.25rem;
  box-shadow: none !important;
  border: 0 !important;
  border-radius: 0.475rem;
  vertical-align: middle;
  font-weight: 500;
  text-transform: capitalize;
}

// Custom styles for trip events
.fc-event {
  cursor: pointer;
  border-radius: 4px;
  border: 1px solid transparent;

  &.fc-event-primary {
    background-color: #009ef7;
    border-color: #009ef7;
    color: white;
  }

  &.fc-event-success {
    background-color: #50cd89;
    border-color: #50cd89;
    color: white;
  }

  &.fc-event-warning {
    background-color: #ffc700;
    border-color: #ffc700;
    color: #1e1e2d;
  }

  &.fc-event-info {
    background-color: #7239ea;
    border-color: #7239ea;
    color: white;
  }

  &.fc-event-dark {
    background-color: #181c32;
    border-color: #181c32;
    color: white;
  }

  // Trip departure/arrival events
  .fc-event-title {
    font-weight: 600;
    font-size: 0.875rem;
  }

  // Hover effects
  &:hover {
    opacity: 0.8;
    transform: translateY(-1px);
    transition: all 0.2s ease-in-out;
  }
}

// Month view adjustments
.fc-daygrid-event {
  font-size: 0.8rem;
  padding: 2px 4px;
  margin-bottom: 1px;

  .fc-event-title {
    font-weight: 500;
  }
}

// Week and day view adjustments
.fc-timegrid-event {
  .fc-event-title {
    font-weight: 600;
    line-height: 1.2;
  }
}

// More link styling
.fc-more-link {
  color: #009ef7;
  font-weight: 600;

  &:hover {
    color: #0d6efd;
  }
}
</style>
