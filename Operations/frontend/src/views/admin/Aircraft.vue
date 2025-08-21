<template>
  <AdminTemplate
    title="Aircraft"
    subtitle="Manage fleet and aircraft information"
    endpoint="/aircraft/"
    :columns="columns"
  >
    <template v-slot:aircraft="{ row: aircraft }">
      <div class="d-flex align-items-center">
        <div class="symbol symbol-circle symbol-50px overflow-hidden me-3">
          <div class="symbol-label bg-light-primary">
            <i class="ki-duotone ki-airplane fs-2x text-primary">
              <span class="path1"></span>
              <span class="path2"></span>
            </i>
          </div>
        </div>
        <div class="d-flex flex-column">
          <a href="#" class="text-gray-800 text-hover-primary mb-1 fs-6 fw-bold">
            {{ aircraft.tail_number || 'No tail number' }}
          </a>
          <span class="text-muted fs-7">{{ aircraft.make_model || 'Unknown model' }}</span>
        </div>
      </div>
    </template>

    <template v-slot:specs="{ row: aircraft }">
      <div class="d-flex flex-column">
        <span class="text-dark fw-semibold fs-6">
          {{ aircraft.aircraft_type || 'Unknown type' }}
        </span>
        <span class="text-muted fs-7">Max: {{ aircraft.max_passengers || 'N/A' }} passengers</span>
      </div>
    </template>

    <template v-slot:range="{ row: aircraft }">
      <span class="text-dark fw-semibold">
        {{ aircraft.range_nm ? `${aircraft.range_nm} nm` : 'Unknown range' }}
      </span>
    </template>

    <template v-slot:status="{ row: aircraft }">
      <span :class="`badge badge-light-${getStatusColor(aircraft.status)} fs-7 fw-bold`">
        {{ aircraft.status || 'Available' }}
      </span>
    </template>

    <template v-slot:created="{ row: aircraft }">
      {{ formatDate(aircraft.created_on) }}
    </template>
  </AdminTemplate>
</template>

<script lang="ts">
import { defineComponent } from "vue";
import AdminTemplate from "./AdminTemplate.vue";

export default defineComponent({
  name: "aircraft-management",
  components: {
    AdminTemplate,
  },
  setup() {
    const columns = [
      {
        columnName: "Aircraft",
        columnLabel: "aircraft",
        sortEnabled: true,
      },
      {
        columnName: "Specifications",
        columnLabel: "specs",
        sortEnabled: false,
      },
      {
        columnName: "Range",
        columnLabel: "range",
        sortEnabled: true,
      },
      {
        columnName: "Status",
        columnLabel: "status",
        sortEnabled: true,
      },
      {
        columnName: "Created",
        columnLabel: "created",
        sortEnabled: true,
      },
    ];

    const getStatusColor = (status: string): string => {
      const colors: Record<string, string> = {
        'available': 'success',
        'in_use': 'primary',
        'maintenance': 'warning',
        'out_of_service': 'danger',
        'retired': 'secondary',
      };
      return colors[status?.toLowerCase()] || 'success';
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
      getStatusColor,
      formatDate,
    };
  },
});
</script>