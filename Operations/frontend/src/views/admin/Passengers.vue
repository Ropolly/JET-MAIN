<template>
  <AdminTemplate
    title="Passengers"
    subtitle="Manage trip passengers and accompanying persons"
    endpoint="/passengers/"
    :columns="columns"
  >
    <template v-slot:passenger="{ row: passenger }">
      <div class="d-flex align-items-center">
        <div class="symbol symbol-circle symbol-50px overflow-hidden me-3">
          <div class="symbol-label bg-light-info">
            <i class="ki-duotone ki-profile-circle fs-2x text-info">
              <span class="path1"></span>
              <span class="path2"></span>
              <span class="path3"></span>
            </i>
          </div>
        </div>
        <div class="d-flex flex-column">
          <a href="#" class="text-gray-800 text-hover-primary mb-1 fs-6 fw-bold">
            {{ getPassengerName(passenger) }}
          </a>
          <span class="text-muted fs-7">{{ passenger.passenger_type || 'Standard' }}</span>
        </div>
      </div>
    </template>

    <template v-slot:type="{ row: passenger }">
      <span :class="`badge badge-light-${getTypeColor(passenger.passenger_type)} fs-7 fw-bold`">
        {{ passenger.passenger_type || 'Standard' }}
      </span>
    </template>

    <template v-slot:seat="{ row: passenger }">
      <span class="text-dark fw-semibold">
        {{ passenger.seat_preference || 'No preference' }}
      </span>
    </template>

    <template v-slot:created="{ row: passenger }">
      {{ formatDate(passenger.created_on) }}
    </template>
  </AdminTemplate>
</template>

<script lang="ts">
import { defineComponent } from "vue";
import AdminTemplate from "./AdminTemplate.vue";

export default defineComponent({
  name: "passengers-management",
  components: {
    AdminTemplate,
  },
  setup() {
    const columns = [
      {
        columnName: "Passenger",
        columnLabel: "passenger",
        sortEnabled: true,
      },
      {
        columnName: "Type",
        columnLabel: "type",
        sortEnabled: true,
      },
      {
        columnName: "Seat Preference",
        columnLabel: "seat",
        sortEnabled: false,
      },
      {
        columnName: "Created",
        columnLabel: "created",
        sortEnabled: true,
      },
    ];

    const getPassengerName = (passenger: any): string => {
      if (passenger.first_name || passenger.last_name) {
        return `${passenger.first_name || ''} ${passenger.last_name || ''}`.trim();
      }
      return 'Unnamed Passenger';
    };

    const getTypeColor = (type: string): string => {
      const colors: Record<string, string> = {
        'patient': 'danger',
        'medical': 'warning', 
        'family': 'info',
        'companion': 'primary',
        'crew': 'secondary',
        'standard': 'success',
      };
      return colors[type?.toLowerCase()] || 'success';
    };

    const formatDate = (dateString: string): string => {
      if (!dateString) return 'Not set';
      return new Date(dateString).toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
      });
    };

    return {
      columns,
      getPassengerName,
      getTypeColor,
      formatDate,
    };
  },
});
</script>