<template>
  <AdminTemplate
    title="Departments"
    subtitle="Manage organizational departments"
    endpoint="/departments/"
    :columns="columns"
  >
    <template v-slot:department="{ row: dept }">
      <div class="d-flex align-items-center">
        <div class="symbol symbol-circle symbol-50px overflow-hidden me-3">
          <div class="symbol-label bg-light-success">
            <i class="ki-duotone ki-office-bag fs-2x text-success">
              <span class="path1"></span>
              <span class="path2"></span>
            </i>
          </div>
        </div>
        <div class="d-flex flex-column">
          <a href="#" class="text-gray-800 text-hover-primary mb-1 fs-6 fw-bold">
            {{ dept.name || 'Unnamed Department' }}
          </a>
          <span class="text-muted fs-7">{{ dept.description || 'No description' }}</span>
        </div>
      </div>
    </template>
    
    <template v-slot:head="{ row: dept }">
      <span class="text-dark fw-semibold">
        {{ dept.head_of_department || 'No head assigned' }}
      </span>
    </template>
    
    <template v-slot:status="{ row: dept }">
      <span :class="`badge badge-light-${getStatusColor(dept.status)} fs-7 fw-bold`">
        {{ dept.status || 'Active' }}
      </span>
    </template>
  </AdminTemplate>
</template>

<script lang="ts">
import { defineComponent } from "vue";
import AdminTemplate from "./AdminTemplate.vue";

export default defineComponent({
  name: "departments-management",
  components: {
    AdminTemplate,
  },
  setup() {
    const columns = [
      {
        columnName: "Department",
        columnLabel: "department",
        sortEnabled: true,
      },
      {
        columnName: "Head",
        columnLabel: "head",
        sortEnabled: false,
      },
      {
        columnName: "Status",
        columnLabel: "status",
        sortEnabled: true,
      },
    ];

    const getStatusColor = (status: string): string => {
      const colors: Record<string, string> = {
        'active': 'success',
        'inactive': 'danger',
        'restructuring': 'warning',
      };
      return colors[status?.toLowerCase()] || 'success';
    };

    return {
      columns,
      getStatusColor,
    };
  },
});
</script>