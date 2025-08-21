<template>
  <!--begin::Card-->
  <div class="card">
    <!--begin::Card header-->
    <div class="card-header border-0 pt-6">
      <!--begin::Card title-->
      <div class="card-title">
        <!--begin::Search-->
        <div class="d-flex align-items-center position-relative my-1">
          <KTIcon
            icon-name="magnifier"
            icon-class="fs-1 position-absolute ms-6"
          />
          <input
            v-model="search"
            @input="searchItems()"
            type="text"
            class="form-control form-control-solid w-250px ps-14"
            placeholder="Search Quotes"
          />
        </div>
        <!--end::Search-->
      </div>
      <!--begin::Card title-->

      <!--begin::Card toolbar-->
      <div class="card-toolbar">
        <!--begin::Toolbar-->
        <div
          v-if="selectedIds.length === 0"
          class="d-flex justify-content-end"
        >
          <!--begin::Export-->
          <button
            type="button"
            class="btn btn-light-primary me-3"
            @click="exportQuotes"
          >
            <KTIcon icon-name="exit-up" icon-class="fs-2" />
            Export
          </button>
          <!--end::Export-->

          <!--begin::Add quote-->
          <button
            type="button"
            class="btn btn-primary"
            @click="handleCreate"
          >
            <KTIcon icon-name="plus" icon-class="fs-2" />
            Add Quote
          </button>
          <!--end::Add quote-->
        </div>
        <!--end::Toolbar-->

        <!--begin::Group actions-->
        <div v-else class="d-flex justify-content-end align-items-center">
          <div class="fw-bold me-5">
            <span class="me-2">{{ selectedIds.length }}</span
            >Selected
          </div>
          <button
            type="button"
            class="btn btn-danger"
            @click="deleteFewQuotes()"
          >
            Delete Selected
          </button>
        </div>
        <!--end::Group actions-->
      </div>
      <!--end::Card toolbar-->
    </div>
    <!--end::Card header-->

    <!--begin::Card body-->
    <div class="card-body pt-0">
      <KTDatatable
        @on-sort="sort"
        @on-items-select="onItemSelect"
        @on-items-per-page-change="onItemsPerPageChange"
        :data="quotes"
        :header="headerConfig"
        :checkbox-enabled="true"
        :loading="loading"
      >
        <template v-slot:quote="{ row: quote }">
          <div class="d-flex align-items-center">
            <div class="symbol symbol-circle symbol-50px overflow-hidden me-3">
              <div class="symbol-label bg-light-warning">
                <i class="ki-duotone ki-price-tag fs-2x text-warning">
                  <span class="path1"></span>
                  <span class="path2"></span>
                  <span class="path3"></span>
                </i>
              </div>
            </div>
            <div class="d-flex flex-column">
              <a href="#" @click="navigateToQuote(quote.id)" class="text-gray-800 text-hover-primary mb-1 fs-6 fw-bold">
                #{{ quote.quote_number || quote.id.slice(0, 8) }}
              </a>
              <span class="text-muted fs-7">{{ formatDate(quote.created_on) }}</span>
            </div>
          </div>
        </template>

        <template v-slot:patient="{ row: quote }">
          <div class="d-flex flex-column">
            <a v-if="quote.patient_id || quote.customer_id" 
               @click="navigateToContact(quote)" 
               href="#" 
               class="text-dark fw-bold text-hover-primary fs-6">
              {{ getPatientName(quote) }}
            </a>
            <span v-else class="text-dark fw-bold fs-6">
              {{ getPatientName(quote) }}
            </span>
            <span class="text-muted fs-7">{{ quote.medical_team }}</span>
          </div>
        </template>

        <template v-slot:route="{ row: quote }">
          <div class="d-flex flex-column">
            <span class="text-dark fw-semibold fs-6">
              {{ getAirportCode(quote.pickup_airport_id) }} → {{ getAirportCode(quote.dropoff_airport_id) }}
            </span>
            <span class="text-muted fs-7">{{ quote.aircraft_type }}</span>
          </div>
        </template>

        <template v-slot:amount="{ row: quote }">
          <span class="text-dark fw-bold fs-6">
            {{ formatCurrency(quote.quoted_amount) }}
          </span>
        </template>

        <template v-slot:status="{ row: quote }">
          <span :class="`badge badge-light-${getStatusColor(quote.status)} fs-7 fw-bold`">
            {{ quote.status }}
          </span>
        </template>

        <template v-slot:pdf_status="{ row: quote }">
          <span :class="`badge badge-light-${getPdfStatusColor(quote.quote_pdf_status)} fs-8 fw-bold`">
            {{ quote.quote_pdf_status }}
          </span>
        </template>

        <template v-slot:actions="{ row: quote }">
          <a
            href="#"
            class="btn btn-sm btn-light btn-active-light-primary"
            data-kt-menu-trigger="click"
            data-kt-menu-placement="bottom-end"
            data-kt-menu-flip="top-end"
            >Actions
            <KTIcon icon-name="down" icon-class="fs-5 m-0" />
          </a>
          <!--begin::Menu-->
          <div
            class="menu menu-sub menu-sub-dropdown menu-column menu-rounded menu-gray-600 menu-state-bg-light-primary fw-semibold fs-7 w-125px py-4"
            data-kt-menu="true"
          >
            <!--begin::Menu item-->
            <div class="menu-item px-3">
              <a @click="handleView(quote)" class="menu-link px-3"
                >View</a
              >
            </div>
            <!--end::Menu item-->
            <!--begin::Menu item-->
            <div class="menu-item px-3">
              <a @click="handleEdit(quote)" class="menu-link px-3"
                >Edit</a
              >
            </div>
            <!--end::Menu item-->
            <!--begin::Menu item-->
            <div class="menu-item px-3">
              <a @click="handleDelete(quote)" class="menu-link px-3"
                >Delete</a
              >
            </div>
            <!--end::Menu item-->
          </div>
          <!--end::Menu-->
        </template>
      </KTDatatable>
    </div>
    <!--end::Card body-->
  </div>
  <!--end::Card-->
</template>

<script lang="ts">
import { defineComponent, ref, onMounted } from "vue";
import { useRouter } from "vue-router";
import ApiService from "@/core/services/ApiService";
import KTDatatable from "@/components/kt-datatable/KTDataTable.vue";
import type { Sort } from "@/components/kt-datatable/table-partials/models";
import arraySort from "array-sort";
import { MenuComponent } from "@/assets/ts/components";
import Swal from "sweetalert2";

interface Quote {
  id: string;
  quoted_amount: number;
  patient_id?: string;
  contact_id?: string;  // Changed from customer_id to match backend
  patient_first_name: string;
  patient_last_name: string;
  medical_team: string;
  pickup_airport_id: any;
  dropoff_airport_id: any;
  aircraft_type: string;
  status: string;
  quote_pdf_status: string;
  created_on: string;
}

export default defineComponent({
  name: "quotes-management",
  components: {
    KTDatatable,
  },
  setup() {
    const router = useRouter();
    const quotes = ref<Quote[]>([]);
    const loading = ref(false);
    const error = ref<string | null>(null);

    const headerConfig = ref([
      {
        columnName: "Quote",
        columnLabel: "quote",
        sortEnabled: true,
      },
      {
        columnName: "Patient",
        columnLabel: "patient",
        sortEnabled: false,
      },
      {
        columnName: "Route",
        columnLabel: "route",
        sortEnabled: false,
      },
      {
        columnName: "Amount",
        columnLabel: "amount",
        sortEnabled: true,
      },
      {
        columnName: "Status",
        columnLabel: "status",
        sortEnabled: true,
      },
      {
        columnName: "PDF Status",
        columnLabel: "pdf_status",
        sortEnabled: true,
      },
      {
        columnName: "Actions",
        columnLabel: "actions",
      },
    ]);

    const initData = ref<Array<Quote>>([]);
    const selectedIds = ref<Array<number>>([]);
    const search = ref<string>("");

    // Methods
    const fetchQuotes = async () => {
      try {
        loading.value = true;
        error.value = null;
        const { data } = await ApiService.get("/quotes/");
        quotes.value = data.results || data;
        initData.value.splice(0, quotes.value.length, ...quotes.value);
      } catch (err: any) {
        error.value = err.response?.data?.detail || "Failed to fetch quotes";
        console.error("Error fetching quotes:", err);
      } finally {
        loading.value = false;
      }
    };

    const handleCreate = () => {
      Swal.fire({
        title: "Create Quote",
        text: "Quote creation form would open here",
        icon: "info",
        confirmButtonText: "OK"
      });
    };

    const handleEdit = (quote: Quote) => {
      Swal.fire({
        title: "Edit Quote",
        text: `Edit form for quote #${quote.id.slice(0, 8)} would open here`,
        icon: "info",
        confirmButtonText: "OK"
      });
    };

    const handleView = (quote: Quote) => {
      Swal.fire({
        title: "Quote Details",
        html: `
          <div class="text-start">
            <p><strong>Quote ID:</strong> #${quote.id.slice(0, 8)}</p>
            <p><strong>Patient:</strong> ${getPatientName(quote)}</p>
            <p><strong>Amount:</strong> ${formatCurrency(quote.quoted_amount)}</p>
            <p><strong>Status:</strong> ${quote.status}</p>
            <p><strong>Medical Team:</strong> ${quote.medical_team}</p>
          </div>
        `,
        icon: "info",
        confirmButtonText: "OK"
      });
    };

    const handleDelete = (quote: Quote) => {
      Swal.fire({
        title: "Delete Quote",
        text: `Are you sure you want to delete quote #${quote.id.slice(0, 8)}?`,
        icon: "warning",
        showCancelButton: true,
        confirmButtonText: "Yes, delete it!",
        cancelButtonText: "Cancel"
      }).then((result) => {
        if (result.isConfirmed) {
          Swal.fire("Deleted!", "Quote has been deleted.", "success");
        }
      });
    };

    const getPatientName = (quote: Quote): string => {
      if (quote.patient_first_name || quote.patient_last_name) {
        return `${quote.patient_first_name || ''} ${quote.patient_last_name || ''}`.trim();
      }
      return 'Not specified';
    };

    const navigateToContact = (quote: Quote) => {
      if (quote.patient_id) {
        router.push(`/admin/contacts/patients/${quote.patient_id}`);
      } else if (quote.customer_id) {
        router.push(`/admin/contacts/customers/${quote.customer_id}`);
      }
    };

    const navigateToQuote = (quoteId: string) => {
      router.push(`/admin/quotes/${quoteId}`);
    };

    const getAirportCode = (airportId: any): string => {
      return airportId ? `${String(airportId).slice(0, 4).toUpperCase()}` : 'TBD';
    };

    const formatCurrency = (amount: number): string => {
      return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD',
      }).format(amount);
    };

    const formatDate = (dateString: string): string => {
      return new Date(dateString).toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
      });
    };

    const getStatusColor = (status: string): string => {
      const colors: Record<string, string> = {
        pending: 'warning',
        confirmed: 'info',
        active: 'primary',
        completed: 'success',
        cancelled: 'danger',
        paid: 'success',
      };
      return colors[status] || 'secondary';
    };

    const getPdfStatusColor = (status: string): string => {
      const colors: Record<string, string> = {
        created: 'info',
        pending: 'warning',
        modified: 'primary',
        accepted: 'success',
        denied: 'danger',
      };
      return colors[status] || 'secondary';
    };

    const deleteFewQuotes = () => {
      selectedIds.value.forEach((item) => {
        deleteQuote(item);
      });
      selectedIds.value.length = 0;
    };

    const deleteQuote = (id: number) => {
      for (let i = 0; i < quotes.value.length; i++) {
        if (quotes.value[i].id === id.toString()) {
          quotes.value.splice(i, 1);
        }
      }
    };

    const sort = (sort: Sort) => {
      const reverse: boolean = sort.order === "asc";
      if (sort.label) {
        arraySort(quotes.value, sort.label, { reverse });
      }
    };

    const onItemSelect = (selectedItems: Array<number>) => {
      selectedIds.value = selectedItems;
    };

    const searchItems = () => {
      quotes.value.splice(0, quotes.value.length, ...initData.value);
      if (search.value !== "") {
        let results: Array<Quote> = [];
        for (let j = 0; j < initData.value.length; j++) {
          if (searchingFunc(initData.value[j], search.value)) {
            results.push(initData.value[j]);
          }
        }
        quotes.value.splice(0, quotes.value.length, ...results);
      }
      MenuComponent.reinitialization();
    };

    const searchingFunc = (obj: any, value: string): boolean => {
      for (let key in obj) {
        if (!Number.isInteger(obj[key]) && !(typeof obj[key] === "object")) {
          if (obj[key]?.toString().toLowerCase().indexOf(value.toLowerCase()) != -1) {
            return true;
          }
        }
      }
      return false;
    };

    const onItemsPerPageChange = () => {
      setTimeout(() => {
        MenuComponent.reinitialization();
      }, 0);
    };

    const exportQuotes = () => {
      Swal.fire({
        title: "Export Quotes",
        text: "Export functionality would be implemented here",
        icon: "info",
        confirmButtonText: "OK"
      });
    };

    onMounted(() => {
      fetchQuotes();
    });

    return {
      search,
      searchItems,
      quotes,
      headerConfig,
      loading,
      error,
      sort,
      onItemSelect,
      selectedIds,
      deleteFewQuotes,
      deleteQuote,
      onItemsPerPageChange,
      exportQuotes,
      handleCreate,
      handleEdit,
      handleView,
      handleDelete,
      getPatientName,
      navigateToContact,
      navigateToQuote,
      getAirportCode,
      formatCurrency,
      formatDate,
      getStatusColor,
      getPdfStatusColor,
    };
  },
});
</script>