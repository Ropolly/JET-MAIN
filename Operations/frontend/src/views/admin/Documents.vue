<template>
  <AdminTemplate
    title="Documents"
    subtitle="Manage system documents and files"
    endpoint="/documents/"
    :columns="columns"
  >
    <template v-slot:document="{ row: document }">
      <div class="d-flex align-items-center">
        <div class="symbol symbol-circle symbol-50px overflow-hidden me-3">
          <div class="symbol-label bg-light-info">
            <i class="ki-duotone ki-file fs-2x text-info">
              <span class="path1"></span>
              <span class="path2"></span>
            </i>
          </div>
        </div>
        <div class="d-flex flex-column">
          <a href="#" class="text-gray-800 text-hover-primary mb-1 fs-6 fw-bold">
            {{ document.document_type_display || document.filename || 'Unnamed Document' }}
          </a>
          <span class="text-muted fs-7">{{ formatFileSize(document.file_size) }}</span>
        </div>
      </div>
    </template>
    
    <template v-slot:type="{ row: document }">
      <span :class="`badge badge-light-${getTypeColor(document.document_type)} fs-7 fw-bold`">
        {{ document.document_type || 'General' }}
      </span>
    </template>
    
    <template v-slot:uploaded_by="{ row: document }">
      <span class="text-dark fw-semibold">
        {{ document.uploaded_by || 'System' }}
      </span>
    </template>
    
    <template v-slot:status="{ row: document }">
      <span :class="`badge badge-light-${getStatusColor(document.status)} fs-7 fw-bold`">
        {{ document.status || 'Active' }}
      </span>
    </template>
    
    <template v-slot:created="{ row: document }">
      {{ formatDate(document.created_on) }}
    </template>
  </AdminTemplate>
</template>

<script lang="ts">
import { defineComponent } from "vue";
import AdminTemplate from "./AdminTemplate.vue";

export default defineComponent({
  name: "documents-management",
  components: {
    AdminTemplate,
  },
  setup() {
    const columns = [
      {
        columnName: "Document",
        columnLabel: "document",
        sortEnabled: true,
      },
      {
        columnName: "Type",
        columnLabel: "type",
        sortEnabled: true,
      },
      {
        columnName: "Uploaded By",
        columnLabel: "uploaded_by",
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

    const formatFileSize = (bytes: number): string => {
      if (!bytes) return '0 B';
      const k = 1024;
      const sizes = ['B', 'KB', 'MB', 'GB'];
      const i = Math.floor(Math.log(bytes) / Math.log(k));
      return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
    };

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
        'pdf': 'danger',
        'image': 'success',
        'document': 'primary',
        'spreadsheet': 'info',
        'archive': 'warning',
        'general': 'secondary',
      };
      return colors[type?.toLowerCase()] || 'secondary';
    };

    const getStatusColor = (status: string): string => {
      const colors: Record<string, string> = {
        'active': 'success',
        'archived': 'secondary',
        'processing': 'warning',
        'error': 'danger',
      };
      return colors[status?.toLowerCase()] || 'success';
    };

    return {
      columns,
      formatFileSize,
      formatDate,
      getTypeColor,
      getStatusColor,
    };
  },
});
</script>