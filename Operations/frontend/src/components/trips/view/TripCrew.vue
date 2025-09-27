<template>
  <!--begin::Crew Content-->
  <div>
    <!--begin::Header-->
    <div class="d-flex justify-content-between align-items-center mb-6">
      <!--begin::Title-->
      <div>
        <h2 class="fw-bold">Crew Management</h2>
      </div>
      <!--end::Title-->
    </div>
    <!--end::Header-->

    <!--begin::Content-->
    <div>
      <!--begin::Loading-->
      <div v-if="loading" class="d-flex justify-content-center py-5">
        <div class="spinner-border" role="status">
          <span class="visually-hidden">Loading...</span>
        </div>
      </div>
      <!--end::Loading-->

      <!--begin::Crew Summary-->
      <div v-if="!loading && getTripLines().length > 0 && (hasFlightCrew() || hasMedicalCrew())" class="mb-8">
        <div class="row g-6">
          <!--begin::Total Crew-->
          <div class="col-md-3">
            <div class="card text-center py-4 px-3">
              <div class="d-flex justify-content-center mb-3">
                <KTIcon icon-name="people" icon-class="fs-2x text-info" />
              </div>
              <div class="fs-6 fw-semibold text-gray-700 mb-1">Total Crew</div>
              <div class="fs-2 fw-bold text-info">{{ getTotalCrewCount() }}</div>
            </div>
          </div>
          <!--end::Total Crew-->
          <!--begin::Flight Crew-->
          <div class="col-md-3">
            <div class="card text-center py-4 px-3">
              <div class="d-flex justify-content-center mb-3">
                <KTIcon icon-name="airplane" icon-class="fs-2x text-primary" />
              </div>
              <div class="fs-6 fw-semibold text-gray-700 mb-1">Flight Crew</div>
              <div class="fs-2 fw-bold text-primary">{{ getFlightCrewCount() }}</div>
            </div>
          </div>
          <!--end::Flight Crew-->
          <!--begin::Medical Crew-->
          <div class="col-md-3">
            <div class="card text-center py-4 px-3">
              <div class="d-flex justify-content-center mb-3">
                <KTIcon icon-name="heart" icon-class="fs-2x text-danger" />
              </div>
              <div class="fs-6 fw-semibold text-gray-700 mb-1">Medical Crew</div>
              <div class="fs-2 fw-bold text-danger">{{ getMedicalCrewCount() }}</div>
            </div>
          </div>
          <!--end::Medical Crew-->
          <!--begin::Total Duty Hours-->
          <div class="col-md-3">
            <div class="card text-center py-4 px-3">
              <div class="d-flex justify-content-center mb-3">
                <KTIcon icon-name="time" icon-class="fs-2x text-success" />
              </div>
              <div class="fs-6 fw-semibold text-gray-700 mb-1">Total Duty</div>
              <div class="fs-2 fw-bold text-success">{{ getTotalDutyHours() }}h</div>
            </div>
          </div>
          <!--end::Total Duty Hours-->
        </div>
      </div>
      <!--end::Crew Summary-->

      <!--begin::Flight Crew Section-->
      <div v-if="!loading && getTripLines().length > 0" class="mb-8">
        <h3 class="fw-bold text-gray-900 mb-5">
          <KTIcon icon-name="airplane" icon-class="fs-3 text-primary me-2" />
          Flight Crew
        </h3>

        <!--begin::Flight Legs-->
        <div v-if="hasFlightCrew()" class="row g-4">
          <div v-for="(tripLine, index) in getTripLines()" :key="tripLine.id || index" class="col-12">
            <div class="card border border-dashed border-gray-300">
              <div class="card-body">
                <div class="d-flex align-items-center justify-content-between mb-4">
                  <h4 class="fw-bold text-gray-800 mb-0">
                    <KTIcon icon-name="airplane" icon-class="fs-5 text-primary me-2" />
                    Leg {{ index + 1 }}: {{ getLegRoute(tripLine) }}
                  </h4>
                  <span class="text-muted fs-7">{{ formatDateTime(tripLine.departure_time_local) }}</span>
                </div>

                <div class="row g-6">
                  <!--begin::PIC-->
                  <div class="col-md-6">
                    <div class="d-flex align-items-start">
                      <div class="symbol symbol-50px symbol-circle me-4">
                        <span v-if="tripLine.crew_line?.primary_in_command"
                              class="symbol-label bg-light-primary text-primary fw-bold">
                          {{ getContactInitials(tripLine.crew_line.primary_in_command) }}
                        </span>
                        <span v-else class="symbol-label bg-light-secondary text-secondary fw-bold">
                          ?
                        </span>
                      </div>
                      <div class="flex-grow-1">
                        <div class="d-flex align-items-center mb-2">
                          <h5 class="text-gray-900 fw-bold me-3 mb-0">
                            {{ getContactName(tripLine.crew_line?.primary_in_command) || 'Not Assigned' }}
                          </h5>
                          <span class="badge badge-light-primary">PIC</span>
                        </div>
                        <div v-if="tripLine.crew_line?.primary_in_command" class="text-gray-600 fs-7">
                          <div v-if="tripLine.crew_line.primary_in_command.email" class="mb-1">
                            <KTIcon icon-name="sms" icon-class="fs-7 me-1" />
                            {{ tripLine.crew_line.primary_in_command.email }}
                          </div>
                          <div v-if="tripLine.crew_line.primary_in_command.phone">
                            <KTIcon icon-name="phone" icon-class="fs-7 me-1" />
                            {{ tripLine.crew_line.primary_in_command.phone }}
                          </div>
                        </div>
                        <div v-else class="text-muted fs-7">
                          Pilot in Command not assigned
                        </div>
                      </div>
                    </div>
                  </div>
                  <!--end::PIC-->

                  <!--begin::SIC-->
                  <div class="col-md-6">
                    <div class="d-flex align-items-start">
                      <div class="symbol symbol-50px symbol-circle me-4">
                        <span v-if="tripLine.crew_line?.secondary_in_command"
                              class="symbol-label bg-light-info text-info fw-bold">
                          {{ getContactInitials(tripLine.crew_line.secondary_in_command) }}
                        </span>
                        <span v-else class="symbol-label bg-light-secondary text-secondary fw-bold">
                          ?
                        </span>
                      </div>
                      <div class="flex-grow-1">
                        <div class="d-flex align-items-center mb-2">
                          <h5 class="text-gray-900 fw-bold me-3 mb-0">
                            {{ getContactName(tripLine.crew_line?.secondary_in_command) || 'Not Assigned' }}
                          </h5>
                          <span class="badge badge-light-info">SIC</span>
                        </div>
                        <div v-if="tripLine.crew_line?.secondary_in_command" class="text-gray-600 fs-7">
                          <div v-if="tripLine.crew_line.secondary_in_command.email" class="mb-1">
                            <KTIcon icon-name="sms" icon-class="fs-7 me-1" />
                            {{ tripLine.crew_line.secondary_in_command.email }}
                          </div>
                          <div v-if="tripLine.crew_line.secondary_in_command.phone">
                            <KTIcon icon-name="phone" icon-class="fs-7 me-1" />
                            {{ tripLine.crew_line.secondary_in_command.phone }}
                          </div>
                        </div>
                        <div v-else class="text-muted fs-7">
                          Second in Command not assigned
                        </div>
                      </div>
                    </div>
                  </div>
                  <!--end::SIC-->
                </div>

              </div>
            </div>
          </div>
        </div>
        <!--end::Flight Legs-->

        <!--begin::No Flight Crew-->
        <div v-else class="alert alert-light-info">
          <div class="d-flex align-items-center">
            <KTIcon icon-name="information" icon-class="fs-2 text-info me-3" />
            <div>
              <h5 class="text-info mb-1">No Flight Crew Assigned</h5>
              <span class="text-gray-700">Flight crew has not been assigned to this trip yet.</span>
            </div>
          </div>
        </div>
        <!--end::No Flight Crew-->
      </div>
      <!--end::Flight Crew Section-->

      <!--begin::Medical Crew Section-->
      <div v-if="!loading && getTripLines().length > 0" class="mb-8">
        <h3 class="fw-bold text-gray-900 mb-5">
          <KTIcon icon-name="heart" icon-class="fs-3 text-danger me-2" />
          Medical Crew
        </h3>

        <!--begin::Medical Staff-->
        <div v-if="hasMedicalCrew()" class="row g-4">
          <div v-for="(medic, index) in getAllMedicalCrew()" :key="medic.id || index" class="col-md-6">
            <div class="card border border-dashed border-gray-300">
              <div class="card-body">
                <div class="d-flex align-items-start">
                  <div class="symbol symbol-50px symbol-circle me-4">
                    <span class="symbol-label bg-light-danger text-danger fw-bold">
                      {{ getContactInitials(medic) }}
                    </span>
                  </div>
                  <div class="flex-grow-1">
                    <div class="d-flex align-items-center mb-2">
                      <h5 class="text-gray-900 fw-bold me-3 mb-0">
                        {{ getContactName(medic) }}
                      </h5>
                      <span class="badge badge-light-danger">{{ getMedicRole(medic) }}</span>
                    </div>
                    <div class="text-gray-600 fs-7">
                      <div v-if="medic.email" class="mb-1">
                        <KTIcon icon-name="sms" icon-class="fs-7 me-1" />
                        {{ medic.email }}
                      </div>
                      <div v-if="medic.phone" class="mb-1">
                        <KTIcon icon-name="phone" icon-class="fs-7 me-1" />
                        {{ medic.phone }}
                      </div>
                      <div v-if="getMedicSpecialty(medic)" class="text-muted fs-8">
                        Specialty: {{ getMedicSpecialty(medic) }}
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
        <!--end::Medical Staff-->

        <!--begin::No Medical Crew-->
        <div v-else class="alert alert-light-warning">
          <div class="d-flex align-items-center">
            <KTIcon icon-name="warning" icon-class="fs-2 text-warning me-3" />
            <div>
              <h5 class="text-warning mb-1">No Medical Crew Assigned</h5>
              <span class="text-gray-700">Medical crew has not been assigned to this trip yet.</span>
            </div>
          </div>
        </div>
        <!--end::No Medical Crew-->
      </div>
      <!--end::Medical Crew Section-->

      <!--begin::No Trip Lines-->
      <div v-if="!loading && getTripLines().length === 0" class="text-center py-10">
        <i class="fas fa-users fs-3x text-muted mb-4"></i>
        <p class="text-muted">Add flight legs to assign crew members</p>
      </div>
      <!--end::No Trip Lines-->

    </div>
    <!--end::Content-->
  </div>
  <!--end::Crew Content-->
</template>

<script setup lang="ts">
import { computed } from 'vue';

interface Props {
  trip: any;
  loading: boolean;
}

const props = defineProps<Props>();

// Trip lines and crew data
const getTripLines = (): any[] => {
  return props.trip?.trip_lines || [];
};

const hasFlightCrew = (): boolean => {
  return getTripLines().some(line =>
    line.crew_line?.primary_in_command || line.crew_line?.secondary_in_command
  );
};

const hasMedicalCrew = (): boolean => {
  return getAllMedicalCrew().length > 0;
};

// Helper functions for crew information
const getContactName = (contact: any): string => {
  if (!contact) return '';
  const first = contact.first_name || '';
  const last = contact.last_name || '';
  const business = contact.business_name || '';

  if (business) return business;
  return `${first} ${last}`.trim();
};

const getContactInitials = (contact: any): string => {
  if (!contact) return '?';
  const first = contact.first_name || '';
  const last = contact.last_name || '';
  const business = contact.business_name || '';

  if (business) return business.charAt(0).toUpperCase();
  return `${first.charAt(0)}${last.charAt(0)}`.toUpperCase() || '?';
};

const getLegRoute = (tripLine: any): string => {
  const origin = tripLine.origin_airport?.icao_code || tripLine.origin_airport?.iata_code || 'UNK';
  const destination = tripLine.destination_airport?.icao_code || tripLine.destination_airport?.iata_code || 'UNK';
  return `${origin} → ${destination}`;
};

// Medical crew functions
const getAllMedicalCrew = (): any[] => {
  const medics: any[] = [];

  getTripLines().forEach(line => {
    if (line.crew_line?.medics) {
      if (Array.isArray(line.crew_line.medics)) {
        medics.push(...line.crew_line.medics);
      } else {
        medics.push(line.crew_line.medics);
      }
    }
  });

  // Remove duplicates based on id or name
  return medics.filter((medic, index, self) =>
    index === self.findIndex(m =>
      (m.id && medic.id && m.id === medic.id) ||
      (!m.id && !medic.id && getContactName(m) === getContactName(medic))
    )
  );
};

const getMedicRole = (medic: any): string => {
  // TODO: Determine role based on staff role or qualifications
  return medic.role || 'RN';
};

const getMedicSpecialty = (medic: any): string => {
  // TODO: Get specialty from medic data
  return medic.specialty || '';
};

// Duration and time calculations
const formatDuration = (duration?: string | number): string => {
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
};

const calculateTotalDuty = (tripLine: any): string => {
  let totalMinutes = 0;

  // Pre-flight duty
  if (tripLine.pre_flight_duty_time) {
    totalMinutes += parseDurationToMinutes(tripLine.pre_flight_duty_time);
  }

  // Flight time
  if (tripLine.flight_time) {
    totalMinutes += parseDurationToMinutes(tripLine.flight_time);
  }

  // Post-flight duty
  if (tripLine.post_flight_duty_time) {
    totalMinutes += parseDurationToMinutes(tripLine.post_flight_duty_time);
  }

  return formatDuration(totalMinutes);
};

const parseDurationToMinutes = (duration: string | number): number => {
  if (typeof duration === 'string' && duration.includes(':')) {
    const parts = duration.split(':');
    const hours = parseInt(parts[0]) || 0;
    const minutes = parseInt(parts[1]) || 0;
    return hours * 60 + minutes;
  }

  return parseFloat(String(duration)) || 0;
};

const formatDateTime = (dateString?: string): string => {
  if (!dateString) return 'Not scheduled';

  try {
    const date = new Date(dateString);
    return date.toLocaleString('en-US', {
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  } catch (error) {
    return 'Invalid date';
  }
};

// Summary calculations
const getTotalCrewCount = (): number => {
  return getFlightCrewCount() + getMedicalCrewCount();
};

const getFlightCrewCount = (): number => {
  const crew = new Set();

  getTripLines().forEach(line => {
    if (line.crew_line?.primary_in_command?.id) {
      crew.add(line.crew_line.primary_in_command.id);
    }
    if (line.crew_line?.secondary_in_command?.id) {
      crew.add(line.crew_line.secondary_in_command.id);
    }
  });

  return crew.size;
};

const getMedicalCrewCount = (): number => {
  return getAllMedicalCrew().length;
};

const getTotalDutyHours = (): string => {
  let totalMinutes = 0;

  getTripLines().forEach(line => {
    totalMinutes += parseDurationToMinutes(line.pre_flight_duty_time || 0);
    totalMinutes += parseDurationToMinutes(line.flight_time || 0);
    totalMinutes += parseDurationToMinutes(line.post_flight_duty_time || 0);
  });

  return formatDuration(totalMinutes);
};

// Crew events/changes
const hasCrewEvents = (): boolean => {
  return getCrewEvents().length > 0;
};

const getCrewEvents = (): any[] => {
  const events = props.trip?.trip_events || props.trip?.events || [];
  return events.filter((event: any) => event.event_type === 'CREW_CHANGE');
};

const getEventAirport = (event: any): string => {
  if (event.airport) {
    return event.airport.icao_code || event.airport.iata_code || event.airport.name || 'Unknown';
  }
  return 'Unknown Airport';
};
</script>

<style scoped>
.symbol-label {
  font-size: 0.875rem;
}
</style>