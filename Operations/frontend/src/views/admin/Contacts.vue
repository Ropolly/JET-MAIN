<template>
  <AdminTemplate
    title="Contacts"
    subtitle="Manage customer and business contacts"
    endpoint="/contacts/"
    :columns="columns"
  >
    <template v-slot:contact="{ row: contact }">
      <div class="d-flex align-items-center">
        <div class="symbol symbol-circle symbol-50px overflow-hidden me-3">
          <div class="symbol-label bg-light-primary">
            <i class="ki-duotone ki-profile-circle fs-2x text-primary">
              <span class="path1"></span>
              <span class="path2"></span>
              <span class="path3"></span>
            </i>
          </div>
        </div>
        <div class="d-flex flex-column">
          <a href="#" class="text-gray-800 text-hover-primary mb-1 fs-6 fw-bold">
            {{ getContactName(contact) }}
          </a>
          <span class="text-muted fs-7">{{ contact.email || 'No email' }}</span>
        </div>
      </div>
    </template>

    <template v-slot:phone="{ row: contact }">
      <span class="text-dark fw-semibold">
        {{ contact.phone || 'No phone' }}
      </span>
    </template>

    <template v-slot:type="{ row: contact }">
      <span :class="`badge badge-light-${getTypeColor(contact.contact_type)} fs-7 fw-bold`">
        {{ contact.contact_type || 'General' }}
      </span>
    </template>

    <template v-slot:created="{ row: contact }">
      {{ formatDate(contact.created_on) }}
    </template>
  </AdminTemplate>
</template>

<script lang="ts">
import { defineComponent } from "vue";
import AdminTemplate from "./AdminTemplate.vue";

export default defineComponent({
  name: "contacts-management",
  components: {
    AdminTemplate,
  },
  setup() {
    const columns = [
      {
        columnName: "Contact",
        columnLabel: "contact",
        sortEnabled: true,
      },
      {
        columnName: "Phone",
        columnLabel: "phone",
        sortEnabled: false,
      },
      {
        columnName: "Type",
        columnLabel: "type",
        sortEnabled: true,
      },
      {
        columnName: "Created",
        columnLabel: "created",
        sortEnabled: true,
      },
    ];

    const getContactName = (contact: any): string => {
      if (contact.first_name || contact.last_name) {
        return `${contact.first_name || ''} ${contact.last_name || ''}`.trim();
      }
      return contact.name || 'Unnamed Contact';
    };

    const getTypeColor = (type: string): string => {
      const colors: Record<string, string> = {
        'customer': 'primary',
        'vendor': 'info',
        'medical': 'success',
        'emergency': 'danger',
        'family': 'warning',
        'general': 'secondary',
      };
      return colors[type?.toLowerCase()] || 'secondary';
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
      getContactName,
      getTypeColor,
      formatDate,
    };
  },
});
</script>