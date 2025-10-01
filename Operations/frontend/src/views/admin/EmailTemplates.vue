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
            placeholder="Search Email Templates"
          />
        </div>
        <!--end::Search-->
      </div>
      <!--begin::Card title-->

      <!--begin::Card toolbar-->
      <div class="card-toolbar">
        <!--begin::Group actions-->
        <div v-if="selectedIds.length > 0" class="d-flex justify-content-end align-items-center">
          <div class="fw-bold me-5">
            <span class="me-2">{{ selectedIds.length }}</span>Selected
          </div>
          <button
            type="button"
            class="btn btn-danger"
            @click="deleteFewTemplates()"
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
        @page-change="onPageChange"
        :data="templates"
        :header="headerConfig"
        :checkbox-enabled="true"
        :loading="loading"
        :total="totalItems"
        :current-page="currentPage"
        :items-per-page="pageSize"
      >
        <template v-slot:title="{ row: template }">
          <div class="d-flex align-items-center">
            <div class="symbol symbol-circle symbol-50px overflow-hidden me-3">
              <div class="symbol-label bg-light-info">
                <i class="ki-duotone ki-sms fs-2x text-info">
                  <span class="path1"></span>
                  <span class="path2"></span>
                </i>
              </div>
            </div>
            <div class="d-flex flex-column">
              <a @click.prevent="handleEdit(template)" href="#" class="text-gray-800 text-hover-primary mb-1 fs-6 fw-bold">
                {{ template.title }}
              </a>
              <span class="text-muted fs-7">{{ template.subject || 'No subject' }}</span>
            </div>
          </div>
        </template>

        <template v-slot:category="{ row: template }">
          <span :class="`badge badge-light-${getCategoryColor(template.category)} fs-7 fw-bold`">
            {{ formatCategory(template.category) }}
          </span>
        </template>

        <template v-slot:status="{ row: template }">
          <span :class="`badge badge-light-${template.is_published ? 'success' : 'warning'} fs-7 fw-bold`">
            {{ template.is_published ? 'Published' : 'Draft' }}
          </span>
        </template>

        <template v-slot:last_sent="{ row: template }">
          <span class="text-dark fw-semibold">
            {{ template.last_sent_at ? formatDate(template.last_sent_at) : 'Never sent' }}
          </span>
        </template>

        <template v-slot:send_count="{ row: template }">
          <span class="text-dark fw-semibold">
            {{ template.send_count || 0 }}
          </span>
        </template>

        <template v-slot:created_on="{ row: template }">
          <span class="text-dark fw-semibold">{{ formatDate(template.created_on) }}</span>
        </template>

        <template v-slot:created_by="{ row: template }">
          <span class="text-dark fw-semibold">{{ getCreatedBy(template) }}</span>
        </template>

        <template v-slot:actions="{ row: template }">
          <a
            href="#"
            class="btn btn-light btn-active-light-primary btn-flex btn-center btn-sm"
            data-kt-menu-trigger="click"
            data-kt-menu-placement="bottom-end"
          >
            Actions
            <KTIcon icon-name="down" icon-class="fs-5 ms-1" />
          </a>
          <!--begin::Menu-->
          <div
            class="menu menu-sub menu-sub-dropdown menu-column menu-rounded menu-gray-600 menu-state-bg-light-primary fw-semibold fs-7 w-125px py-4"
            data-kt-menu="true"
          >
            <!--begin::Menu item-->
            <div class="menu-item px-3">
              <a @click.prevent="handleEdit(template)" href="#" class="menu-link px-3">
                <KTIcon icon-name="pencil" icon-class="fs-6 me-2" />
                Edit Template
              </a>
            </div>
            <!--end::Menu item-->

            <!--begin::Separator-->
            <div class="separator my-2"></div>
            <!--end::Separator-->
            <!--begin::Menu item-->
            <div class="menu-item px-3">
              <a @click.prevent="handleDelete(template)" href="#" class="menu-link px-3 text-danger">
                <KTIcon icon-name="trash" icon-class="fs-6 me-2" />
                Delete Template
              </a>
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
import { defineComponent, ref, onMounted, nextTick } from "vue";
import { useRouter } from "vue-router";
import ApiService from "@/core/services/ApiService";
import KTDatatable from "@/components/kt-datatable/KTDataTable.vue";
import type { Sort } from "@/components/kt-datatable/table-partials/models";
import arraySort from "array-sort";
import { MenuComponent } from "@/assets/ts/components";
import Swal from "sweetalert2";
import { useToolbar, createToolbarActions } from "@/core/helpers/toolbar";

interface EmailTemplate {
  id: string;
  title: string;
  subject?: string;
  content: string;
  category: string;
  is_published: boolean;
  last_sent_at?: string;
  send_count: number;
  created_on: string;
  created_by?: string;
  variables: string[];
}

export default defineComponent({
  name: "email-templates-management",
  components: {
    KTDatatable,
  },
  setup() {
    const router = useRouter();
    const templates = ref<EmailTemplate[]>([]);
    const selectedIds = ref<string[]>([]);
    const currentPage = ref(1);
    const pageSize = ref(25);
    const totalItems = ref(0);
    const loading = ref(false);
    const search = ref("");
    const sortLabel = ref("");
    const sortOrder = ref<"asc" | "desc">("asc");
    const { setToolbarActions } = useToolbar();

    const headerConfig = ref([
      {
        columnName: "Title",
        columnLabel: "title",
        sortEnabled: true,
        columnWidth: 300,
      },
      {
        columnName: "Category",
        columnLabel: "category",
        sortEnabled: true,
        columnWidth: 120,
      },
      {
        columnName: "Status",
        columnLabel: "status",
        sortEnabled: false,
        columnWidth: 100,
      },
      {
        columnName: "Last Sent",
        columnLabel: "last_sent",
        sortEnabled: true,
        columnWidth: 150,
      },
      {
        columnName: "Send Count",
        columnLabel: "send_count",
        sortEnabled: true,
        columnWidth: 120,
      },
      {
        columnName: "Created On",
        columnLabel: "created_on",
        sortEnabled: true,
        columnWidth: 150,
      },
      {
        columnName: "Created By",
        columnLabel: "created_by",
        sortEnabled: true,
        columnWidth: 150,
      },
      {
        columnName: "Actions",
        columnLabel: "actions",
        sortEnabled: false,
        columnWidth: 120,
      },
    ]);


    const fetchTemplates = async () => {
      loading.value = true;
      try {
        const params = {
          page: currentPage.value,
          page_size: pageSize.value,
          search: search.value,
          ordering: sortLabel.value ? `${sortOrder.value === "desc" ? "-" : ""}${sortLabel.value}` : undefined,
        };

        const response = await ApiService.query("email-templates", { params });
        templates.value = response.data.results || response.data;
        totalItems.value = response.data.count || templates.value.length;
      } catch (error) {
        console.error("Error fetching email templates:", error);
        Swal.fire({
          title: "Error",
          text: "Failed to fetch email templates",
          icon: "error",
        });
      } finally {
        loading.value = false;
      }
    };

    const searchItems = () => {
      currentPage.value = 1;
      fetchTemplates();
    };

    const sort = (sort: Sort) => {
      const { order, column } = sort;
      if (order) {
        sortOrder.value = order;
        sortLabel.value = column;
        fetchTemplates();
      }
    };

    const onItemSelect = (selectedItems: Array<string>) => {
      selectedIds.value = selectedItems;
    };

    const onItemsPerPageChange = (size: number) => {
      pageSize.value = size;
      currentPage.value = 1;
      fetchTemplates();
    };

    const onPageChange = (page: number) => {
      currentPage.value = page;
      fetchTemplates();
    };

    const handleCreate = () => {
      router.push({ name: "email-template-create" });
    };

    const handleEdit = (template: EmailTemplate) => {
      router.push({ name: "email-template-edit", params: { id: template.id } });
    };

    const handleDelete = async (template: EmailTemplate) => {
      const result = await Swal.fire({
        title: "Are you sure?",
        text: `You won't be able to revert this! This will delete the email template "${template.title}".`,
        icon: "warning",
        showCancelButton: true,
        confirmButtonColor: "#3085d6",
        cancelButtonColor: "#d33",
        confirmButtonText: "Yes, delete it!",
      });

      if (result.isConfirmed) {
        try {
          await ApiService.delete("email-templates", template.id);
          Swal.fire("Deleted!", "Email template has been deleted.", "success");
          fetchTemplates();
        } catch (error) {
          console.error("Error deleting template:", error);
          Swal.fire("Error!", "Failed to delete email template.", "error");
        }
      }
    };

    const deleteFewTemplates = async () => {
      const result = await Swal.fire({
        title: "Are you sure?",
        text: `You won't be able to revert this! This will delete ${selectedIds.value.length} email template(s).`,
        icon: "warning",
        showCancelButton: true,
        confirmButtonColor: "#3085d6",
        cancelButtonColor: "#d33",
        confirmButtonText: "Yes, delete them!",
      });

      if (result.isConfirmed) {
        try {
          await Promise.all(
            selectedIds.value.map((id) => ApiService.delete("email-templates", id))
          );
          selectedIds.value = [];
          Swal.fire("Deleted!", "Email templates have been deleted.", "success");
          fetchTemplates();
        } catch (error) {
          console.error("Error deleting templates:", error);
          Swal.fire("Error!", "Failed to delete some email templates.", "error");
        }
      }
    };

    const formatDate = (dateString: string): string => {
      if (!dateString) return "";
      return new Date(dateString).toLocaleDateString("en-US", {
        year: "numeric",
        month: "short",
        day: "numeric",
      });
    };

    const formatCategory = (category: string): string => {
      return category.charAt(0).toUpperCase() + category.slice(1);
    };

    const getCategoryColor = (category: string): string => {
      const colors: { [key: string]: string } = {
        general: "primary",
        trip: "info",
        quote: "warning",
        patient: "success",
        notification: "secondary",
      };
      return colors[category] || "primary";
    };

    const getCreatedBy = (template: EmailTemplate): string => {
      return template.created_by || "System";
    };

    onMounted(async () => {
      await fetchTemplates();

      // Setup toolbar actions
      setToolbarActions([
        createToolbarActions.primary('add-template', 'Add Template', handleCreate, 'plus')
      ]);

      // Initialize menu components after DOM is ready
      await nextTick();
      setTimeout(() => {
        MenuComponent.reinitialization();
      }, 300);
    });

    return {
      templates,
      selectedIds,
      currentPage,
      pageSize,
      totalItems,
      loading,
      search,
      headerConfig,
      fetchTemplates,
      searchItems,
      sort,
      onItemSelect,
      onItemsPerPageChange,
      onPageChange,
      handleCreate,
      handleEdit,
      handleDelete,
      deleteFewTemplates,
      formatDate,
      formatCategory,
      getCategoryColor,
      getCreatedBy,
    };
  },
});
</script>