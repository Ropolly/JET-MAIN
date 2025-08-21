<template>
  <AdminTemplate
    title="Modifications"
    subtitle="Manage trip modifications and changes"
    endpoint="/modifications/"
    :columns="columns"
  >
    <template v-slot:modification="{ row: modification }">
      <div class="d-flex align-items-center">
        <div class="symbol symbol-circle symbol-50px overflow-hidden me-3">
          <div class="symbol-label bg-light-warning">
            <i class="ki-duotone ki-pencil fs-2x text-warning">
              <span class="path1"></span>
              <span class="path2"></span>
            </i>
          </div>
        </div>
        <div class="d-flex flex-column">
          <a href="#" class="text-gray-800 text-hover-primary mb-1 fs-6 fw-bold">
            {{ modification.modification_id || 'No ID' }}
          </a>
          <span class="text-muted fs-7">{{ formatDate(modification.created_on) }}</span>
        </div>
      </div>
    </template>
    
    <template v-slot:type="{ row: modification }">
      <span :class="`badge badge-light-${getTypeColor(modification.modification_type)} fs-7 fw-bold`">
        {{ modification.modification_type || 'General' }}
      </span>
    </template>
    
    <template v-slot:description="{ row: modification }">
      <span class="text-dark fw-semibold">
        {{ modification.description || 'No description' }}
      </span>
    </template>
    
    <template v-slot:cost_impact="{ row: modification }">
      <span :class="`text-${getCostColor(modification.cost_impact)} fw-bold fs-6`">
        {{ formatCurrency(modification.cost_impact) }}
      </span>
    </template>
    
    <template v-slot:status="{ row: modification }">
      <span :class="`badge badge-light-${getStatusColor(modification.status)} fs-7 fw-bold`">
        {{ modification.status || 'Pending' }}
      </span>
    </template>
  </AdminTemplate>
</template>

<script lang="ts">
import { defineComponent } from "vue";
import AdminTemplate from "./AdminTemplate.vue";

export default defineComponent({
  name: "modifications-management",
  components: {
    AdminTemplate,
  },
  setup() {
    const columns = [
      {
        columnName: "Modification",
        columnLabel: "modification",
        sortEnabled: true,
      },
      {
        columnName: "Type",
        columnLabel: "type",
        sortEnabled: true,
      },
      {
        columnName: "Description",
        columnLabel: "description",
        sortEnabled: false,
      },
      {
        columnName: "Cost Impact",
        columnLabel: "cost_impact",
        sortEnabled: true,
      },
      {
        columnName: "Status",
        columnLabel: "status",
        sortEnabled: true,
      },
    ];

    const formatCurrency = (amount: number): string => {
      if (!amount) return '$0.00';
      return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD',
      }).format(amount);
    };

    const formatDate = (dateString: string): string => {
      if (!dateString) return 'Not set';
      return new Date(dateString).toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
      });
    };

    const getCostColor = (amount: number): string => {
      if (!amount || amount === 0) return 'muted';
      return amount > 0 ? 'danger' : 'success';
    };

    const getTypeColor = (type: string): string => {
      const colors: Record<string, string> = {
        'schedule': 'warning',
        'route': 'info',
        'passenger': 'primary',
        'aircraft': 'success',
        'service': 'secondary',
      };
      return colors[type?.toLowerCase()] || 'secondary';
    };

    const getStatusColor = (status: string): string => {
      const colors: Record<string, string> = {
        'approved': 'success',
        'pending': 'warning',
        'rejected': 'danger',
        'implemented': 'info',
      };
      return colors[status?.toLowerCase()] || 'warning';
    };

    return {
      columns,
      formatCurrency,
      formatDate,
      getCostColor,
      getTypeColor,
      getStatusColor,
    };
  },
});
</script>