<template>
  <AdminTemplate
    title="Ground Transportation"
    subtitle="Manage ground transportation services"
    endpoint="/grounds/"
    :columns="columns"
  >
    <template v-slot:provider="{ row: ground }">
      <div class="d-flex align-items-center">
        <div class="symbol symbol-circle symbol-50px overflow-hidden me-3">
          <div class="symbol-label bg-light-info">
            <i class="ki-duotone ki-delivery fs-2x text-info">
              <span class="path1"></span>
              <span class="path2"></span>
            </i>
          </div>
        </div>
        <div class="d-flex flex-column">
          <a href="#" class="text-gray-800 text-hover-primary mb-1 fs-6 fw-bold">
            {{ ground.provider_name || 'Unnamed Provider' }}
          </a>
          <span class="text-muted fs-7">{{ ground.vehicle_type || 'Standard vehicle' }}</span>
        </div>
      </div>
    </template>

    <template v-slot:route="{ row: ground }">
      <div class="d-flex flex-column">
        <span class="text-dark fw-semibold fs-6">
          {{ ground.pickup_location || 'TBD' }} → {{ ground.dropoff_location || 'TBD' }}
        </span>
      </div>
    </template>

    <template v-slot:cost="{ row: ground }">
      <span class="text-dark fw-bold fs-6">
        {{ formatCurrency(ground.cost) }}
      </span>
    </template>

    <template v-slot:status="{ row: ground }">
      <span :class="`badge badge-light-${getStatusColor(ground.status)} fs-7 fw-bold`">
        {{ ground.status || 'Available' }}
      </span>
    </template>
  </AdminTemplate>
</template>

<script lang="ts">
import { defineComponent } from "vue";
import AdminTemplate from "./AdminTemplate.vue";

export default defineComponent({
  name: "grounds-management",
  components: {
    AdminTemplate,
  },
  setup() {
    const columns = [
      {
        columnName: "Provider",
        columnLabel: "provider",
        sortEnabled: true,
      },
      {
        columnName: "Route",
        columnLabel: "route",
        sortEnabled: false,
      },
      {
        columnName: "Cost",
        columnLabel: "cost",
        sortEnabled: true,
      },
      {
        columnName: "Status",
        columnLabel: "status",
        sortEnabled: true,
      },
    ];

    const formatCurrency = (amount: number): string => {
      if (!amount) return 'TBD';
      return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD',
      }).format(amount);
    };

    const getStatusColor = (status: string): string => {
      const colors: Record<string, string> = {
        'available': 'success',
        'booked': 'primary',
        'in_transit': 'warning',
        'completed': 'info',
        'cancelled': 'danger',
      };
      return colors[status?.toLowerCase()] || 'success';
    };

    return {
      columns,
      formatCurrency,
      getStatusColor,
    };
  },
});
</script>