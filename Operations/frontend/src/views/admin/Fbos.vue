<template>
  <AdminTemplate
    title="FBOs"
    subtitle="Manage Fixed Base Operations facilities"
    endpoint="/fbos/"
    :columns="columns"
  >
    <template v-slot:fbo="{ row: fbo }">
      <div class="d-flex align-items-center">
        <div class="symbol symbol-circle symbol-50px overflow-hidden me-3">
          <div class="symbol-label bg-light-warning">
            <i class="ki-duotone ki-geolocation fs-2x text-warning">
              <span class="path1"></span>
              <span class="path2"></span>
            </i>
          </div>
        </div>
        <div class="d-flex flex-column">
          <a href="#" class="text-gray-800 text-hover-primary mb-1 fs-6 fw-bold">
            {{ fbo.name || 'Unnamed FBO' }}
          </a>
          <span class="text-muted fs-7">{{ fbo.airport_code || 'No airport code' }}</span>
        </div>
      </div>
    </template>

    <template v-slot:contact="{ row: fbo }">
      <div class="d-flex flex-column">
        <span class="text-dark fw-semibold fs-6">
          {{ fbo.phone || 'No phone' }}
        </span>
        <span class="text-muted fs-7">{{ fbo.email || 'No email' }}</span>
      </div>
    </template>

    <template v-slot:services="{ row: fbo }">
      <span class="text-dark fw-semibold">
        {{ fbo.services || 'Standard services' }}
      </span>
    </template>

    <template v-slot:status="{ row: fbo }">
      <span :class="`badge badge-light-${getStatusColor(fbo.status)} fs-7 fw-bold`">
        {{ fbo.status || 'Active' }}
      </span>
    </template>

    <template v-slot:created="{ row: fbo }">
      {{ formatDate(fbo.created_on) }}
    </template>
  </AdminTemplate>
</template>

<script lang="ts">
import { defineComponent } from "vue";
import AdminTemplate from "./AdminTemplate.vue";

export default defineComponent({
  name: "fbos-management",
  components: {
    AdminTemplate,
  },
  setup() {
    const columns = [
      {
        columnName: "FBO",
        columnLabel: "fbo",
        sortEnabled: true,
      },
      {
        columnName: "Contact",
        columnLabel: "contact",
        sortEnabled: false,
      },
      {
        columnName: "Services",
        columnLabel: "services",
        sortEnabled: false,
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
        'active': 'success',
        'inactive': 'danger',
        'pending': 'warning',
        'suspended': 'secondary',
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