<template>
  <AdminTemplate
    title="Roles"
    subtitle="Manage user roles and permissions"
    endpoint="/roles/"
    :columns="columns"
  >
    <template v-slot:role="{ row: role }">
      <div class="d-flex align-items-center">
        <div class="symbol symbol-circle symbol-50px overflow-hidden me-3">
          <div class="symbol-label bg-light-info">
            <i class="ki-duotone ki-security-user fs-2x text-info">
              <span class="path1"></span>
              <span class="path2"></span>
              <span class="path3"></span>
            </i>
          </div>
        </div>
        <div class="d-flex flex-column">
          <a href="#" class="text-gray-800 text-hover-primary mb-1 fs-6 fw-bold">
            {{ role.name || 'Unnamed Role' }}
          </a>
          <span class="text-muted fs-7">{{ role.description || 'No description' }}</span>
        </div>
      </div>
    </template>

    <template v-slot:status="{ row: role }">
      <span :class="`badge badge-light-${getStatusColor(role.status)} fs-7 fw-bold`">
        {{ role.status || 'Active' }}
      </span>
    </template>

    <template v-slot:created="{ row: role }">
      {{ formatDate(role.created_on) }}
    </template>
  </AdminTemplate>
</template>

<script lang="ts">
import { defineComponent } from "vue";
import AdminTemplate from "./AdminTemplate.vue";

export default defineComponent({
  name: "roles-management",
  components: {
    AdminTemplate,
  },
  setup() {
    const columns = [
      {
        columnName: "Role",
        columnLabel: "role",
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
        'active': 'success',
        'inactive': 'danger',
        'deprecated': 'warning',
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