<template>
  <AdminTemplate
    title="Permissions"
    subtitle="Manage user permissions and access control"
    endpoint="/permissions/"
    :columns="columns"
  >
    <template v-slot:permission="{ row: permission }">
      <div class="d-flex align-items-center">
        <div class="symbol symbol-circle symbol-50px overflow-hidden me-3">
          <div class="symbol-label bg-light-warning">
            <i class="ki-duotone ki-shield-tick fs-2x text-warning">
              <span class="path1"></span>
              <span class="path2"></span>
              <span class="path3"></span>
            </i>
          </div>
        </div>
        <div class="d-flex flex-column">
          <a href="#" class="text-gray-800 text-hover-primary mb-1 fs-6 fw-bold">
            {{ permission.name || 'Unnamed Permission' }}
          </a>
          <span class="text-muted fs-7">{{ permission.codename || 'No codename' }}</span>
        </div>
      </div>
    </template>
    
    <template v-slot:content_type="{ row: permission }">
      <span class="badge badge-light-info fs-7 fw-bold">
        {{ permission.content_type || 'General' }}
      </span>
    </template>
    
    <template v-slot:description="{ row: permission }">
      <span class="text-dark fw-semibold">
        {{ permission.description || 'No description' }}
      </span>
    </template>
  </AdminTemplate>
</template>

<script lang="ts">
import { defineComponent } from "vue";
import AdminTemplate from "./AdminTemplate.vue";

export default defineComponent({
  name: "permissions-management",
  components: {
    AdminTemplate,
  },
  setup() {
    const columns = [
      {
        columnName: "Permission",
        columnLabel: "permission",
        sortEnabled: true,
      },
      {
        columnName: "Content Type",
        columnLabel: "content_type",
        sortEnabled: true,
      },
      {
        columnName: "Description",
        columnLabel: "description",
        sortEnabled: false,
      },
    ];

    return {
      columns,
    };
  },
});
</script>