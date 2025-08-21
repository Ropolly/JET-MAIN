<template>
  <AdminTemplate
    title="Airports"
    subtitle="Manage airport information and operations"
    endpoint="/airports/"
    :columns="columns"
  >
    <template v-slot:airport="{ row: airport }">
      <div class="d-flex align-items-center">
        <div class="symbol symbol-circle symbol-50px overflow-hidden me-3">
          <div class="symbol-label bg-light-primary">
            <i class="ki-duotone ki-geolocation fs-2x text-primary">
              <span class="path1"></span>
              <span class="path2"></span>
            </i>
          </div>
        </div>
        <div class="d-flex flex-column">
          <a href="#" class="text-gray-800 text-hover-primary mb-1 fs-6 fw-bold">
            {{ airport.name || 'Unnamed Airport' }}
          </a>
          <span class="text-muted fs-7">{{ airport.iata_code || airport.icao_code || 'No code' }}</span>
        </div>
      </div>
    </template>

    <template v-slot:codes="{ row: airport }">
      <div class="d-flex flex-column">
        <span class="text-dark fw-semibold fs-6">
          IATA: {{ airport.iata_code || 'N/A' }}
        </span>
        <span class="text-muted fs-7">ICAO: {{ airport.icao_code || 'N/A' }}</span>
      </div>
    </template>

    <template v-slot:location="{ row: airport }">
      <div class="d-flex flex-column">
        <span class="text-dark fw-semibold fs-6">
          {{ airport.city || 'Unknown City' }}
        </span>
        <span class="text-muted fs-7">{{ airport.country || 'Unknown Country' }}</span>
      </div>
    </template>

    <template v-slot:timezone="{ row: airport }">
      <span class="text-dark fw-semibold">
        {{ airport.timezone || 'UTC' }}
      </span>
    </template>
  </AdminTemplate>
</template>

<script lang="ts">
import { defineComponent } from "vue";
import AdminTemplate from "./AdminTemplate.vue";

export default defineComponent({
  name: "airports-management",
  components: {
    AdminTemplate,
  },
  setup() {
    const columns = [
      {
        columnName: "Airport",
        columnLabel: "airport",
        sortEnabled: true,
      },
      {
        columnName: "Codes",
        columnLabel: "codes",
        sortEnabled: false,
      },
      {
        columnName: "Location",
        columnLabel: "location",
        sortEnabled: true,
      },
      {
        columnName: "Timezone",
        columnLabel: "timezone",
        sortEnabled: false,
      },
    ];

    return {
      columns,
    };
  },
});
</script>