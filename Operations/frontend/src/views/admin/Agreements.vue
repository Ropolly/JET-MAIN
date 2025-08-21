<template>
  <AdminTemplate
    title="Agreements"
    subtitle="Manage contracts and service agreements"
    endpoint="/agreements/"
    :columns="columns"
  >
    <template v-slot:agreement="{ row: agreement }">
      <div class="d-flex align-items-center">
        <div class="symbol symbol-circle symbol-50px overflow-hidden me-3">
          <div class="symbol-label bg-light-primary">
            <i class="ki-duotone ki-document fs-2x text-primary">
              <span class="path1"></span>
              <span class="path2"></span>
            </i>
          </div>
        </div>
        <div class="d-flex flex-column">
          <a href="#" class="text-gray-800 text-hover-primary mb-1 fs-6 fw-bold">
            {{ agreement.agreement_number || 'No number' }}
          </a>
          <span class="text-muted fs-7">{{ agreement.client_name || 'No client' }}</span>
        </div>
      </div>
    </template>
    
    <template v-slot:type="{ row: agreement }">
      <span :class="`badge badge-light-${getTypeColor(agreement.agreement_type)} fs-7 fw-bold`">
        {{ agreement.agreement_type || 'Service' }}
      </span>
    </template>
    
    <template v-slot:dates="{ row: agreement }">
      <div class="d-flex flex-column">
        <span class="text-dark fw-semibold fs-6">
          {{ formatDate(agreement.start_date) }}
        </span>
        <span class="text-muted fs-7">to {{ formatDate(agreement.end_date) }}</span>
      </div>
    </template>
    
    <template v-slot:status="{ row: agreement }">
      <span :class="`badge badge-light-${getStatusColor(agreement.status)} fs-7 fw-bold`">
        {{ agreement.status || 'Active' }}
      </span>
    </template>
  </AdminTemplate>
</template>

<script lang="ts">
import { defineComponent } from "vue";
import AdminTemplate from "./AdminTemplate.vue";

export default defineComponent({
  name: "agreements-management",
  components: {
    AdminTemplate,
  },
  setup() {
    const columns = [
      {
        columnName: "Agreement",
        columnLabel: "agreement",
        sortEnabled: true,
      },
      {
        columnName: "Type",
        columnLabel: "type",
        sortEnabled: true,
      },
      {
        columnName: "Duration",
        columnLabel: "dates",
        sortEnabled: false,
      },
      {
        columnName: "Status",
        columnLabel: "status",
        sortEnabled: true,
      },
    ];

    const formatDate = (dateString: string): string => {
      if (!dateString) return 'Not set';
      return new Date(dateString).toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
      });
    };

    const getTypeColor = (type: string): string => {
      const colors: Record<string, string> = {
        'service': 'primary',
        'maintenance': 'warning',
        'charter': 'info',
        'lease': 'success',
        'insurance': 'secondary',
      };
      return colors[type?.toLowerCase()] || 'primary';
    };

    const getStatusColor = (status: string): string => {
      const colors: Record<string, string> = {
        'active': 'success',
        'expired': 'danger',
        'pending': 'warning',
        'cancelled': 'secondary',
        'renewed': 'info',
      };
      return colors[status?.toLowerCase()] || 'success';
    };

    return {
      columns,
      formatDate,
      getTypeColor,
      getStatusColor,
    };
  },
});
</script>