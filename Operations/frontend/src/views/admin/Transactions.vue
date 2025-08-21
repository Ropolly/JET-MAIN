<template>
  <AdminTemplate
    title="Transactions"
    subtitle="Manage financial transactions and payments"
    endpoint="/transactions/"
    :columns="columns"
  >
    <template v-slot:transaction="{ row: transaction }">
      <div class="d-flex align-items-center">
        <div class="symbol symbol-circle symbol-50px overflow-hidden me-3">
          <div class="symbol-label bg-light-success">
            <i class="ki-duotone ki-dollar fs-2x text-success">
              <span class="path1"></span>
              <span class="path2"></span>
              <span class="path3"></span>
            </i>
          </div>
        </div>
        <div class="d-flex flex-column">
          <a href="#" class="text-gray-800 text-hover-primary mb-1 fs-6 fw-bold">
            {{ transaction.transaction_id || 'No ID' }}
          </a>
          <span class="text-muted fs-7">{{ formatDate(transaction.created_on) }}</span>
        </div>
      </div>
    </template>
    
    <template v-slot:amount="{ row: transaction }">
      <span class="text-dark fw-bold fs-6">
        {{ formatCurrency(transaction.amount) }}
      </span>
    </template>
    
    <template v-slot:type="{ row: transaction }">
      <span :class="`badge badge-light-${getTypeColor(transaction.transaction_type)} fs-7 fw-bold`">
        {{ transaction.transaction_type || 'Payment' }}
      </span>
    </template>
    
    <template v-slot:method="{ row: transaction }">
      <span class="text-dark fw-semibold">
        {{ transaction.payment_method || 'Unknown' }}
      </span>
    </template>
    
    <template v-slot:status="{ row: transaction }">
      <span :class="`badge badge-light-${getStatusColor(transaction.status)} fs-7 fw-bold`">
        {{ transaction.status || 'Pending' }}
      </span>
    </template>
  </AdminTemplate>
</template>

<script lang="ts">
import { defineComponent } from "vue";
import AdminTemplate from "./AdminTemplate.vue";

export default defineComponent({
  name: "transactions-management",
  components: {
    AdminTemplate,
  },
  setup() {
    const columns = [
      {
        columnName: "Transaction",
        columnLabel: "transaction",
        sortEnabled: true,
      },
      {
        columnName: "Amount",
        columnLabel: "amount",
        sortEnabled: true,
      },
      {
        columnName: "Type",
        columnLabel: "type",
        sortEnabled: true,
      },
      {
        columnName: "Method",
        columnLabel: "method",
        sortEnabled: false,
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

    const getTypeColor = (type: string): string => {
      const colors: Record<string, string> = {
        'payment': 'success',
        'refund': 'warning',
        'charge': 'primary',
        'fee': 'info',
        'adjustment': 'secondary',
      };
      return colors[type?.toLowerCase()] || 'primary';
    };

    const getStatusColor = (status: string): string => {
      const colors: Record<string, string> = {
        'completed': 'success',
        'pending': 'warning',
        'failed': 'danger',
        'cancelled': 'secondary',
        'processing': 'info',
      };
      return colors[status?.toLowerCase()] || 'warning';
    };

    return {
      columns,
      formatCurrency,
      formatDate,
      getTypeColor,
      getStatusColor,
    };
  },
});
</script>