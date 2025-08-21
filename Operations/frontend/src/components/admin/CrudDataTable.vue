<template>
  <div class="card">
    <!--begin::Card header-->
    <div class="card-header border-0 pt-6">
      <!--begin::Card title-->
      <div class="card-title">
        <!--begin::Search-->
        <div class="d-flex align-items-center position-relative my-1">
          <i class="ki-duotone ki-magnifier fs-1 position-absolute ms-6">
            <span class="path1"></span>
            <span class="path2"></span>
          </i>
          <input
            type="text"
            v-model="searchQuery"
            @input="handleSearch"
            :placeholder="`Search ${title.toLowerCase()}...`"
            class="form-control form-control-solid w-250px ps-15"
          />
        </div>
        <!--end::Search-->
      </div>
      <!--begin::Card title-->

      <!--begin::Card toolbar-->
      <div class="card-toolbar">
        <!--begin::Toolbar-->
        <div class="d-flex justify-content-end" data-kt-user-table-toolbar="base">
          <!--begin::Add user-->
          <button
            type="button"
            class="btn btn-primary"
            @click="$emit('create')"
          >
            <i class="ki-duotone ki-plus fs-2"></i>
            Add {{ title.slice(0, -1) }}
          </button>
          <!--end::Add user-->
        </div>
        <!--end::Toolbar-->
      </div>
      <!--end::Card toolbar-->
    </div>
    <!--end::Card header-->

    <!--begin::Card body-->
    <div class="card-body py-4">
      <!--begin::Loading-->
      <div v-if="loading" class="d-flex justify-content-center py-10">
        <div class="spinner-border text-primary" role="status">
          <span class="visually-hidden">Loading...</span>
        </div>
      </div>
      <!--end::Loading-->

      <!--begin::Error-->
      <div v-else-if="error" class="alert alert-danger">
        {{ error }}
      </div>
      <!--end::Error-->

      <!--begin::Table-->
      <div v-else-if="items.length > 0" class="table-responsive">
        <table class="table align-middle table-row-dashed fs-6 gy-5">
          <!--begin::Table head-->
          <thead>
            <tr class="text-start text-muted fw-bold fs-7 text-uppercase gs-0">
              <th
                v-for="column in columns"
                :key="column.key"
                :class="`min-w-${column.width || '125px'}`"
                :style="column.sortable !== false ? 'cursor: pointer;' : ''"
                @click="column.sortable !== false && handleSort(column.key)"
              >
                {{ column.title }}
                <span v-if="column.sortable !== false && sortBy === column.key">
                  <i :class="sortDirection === 'asc' ? 'ki-duotone ki-up' : 'ki-duotone ki-down'" class="fs-5"></i>
                </span>
              </th>
              <th class="text-end min-w-100px">Actions</th>
            </tr>
          </thead>
          <!--end::Table head-->

          <!--begin::Table body-->
          <tbody class="text-gray-600 fw-semibold">
            <tr v-for="item in paginatedItems" :key="item.id">
              <td v-for="column in columns" :key="`${item.id}-${column.key}`">
                <slot 
                  :name="`column-${column.key}`" 
                  :item="item" 
                  :value="getNestedValue(item, column.key)"
                >
                  <span v-if="column.type === 'badge'" 
                    :class="`badge badge-light-${getBadgeColor(getNestedValue(item, column.key))} fs-7 fw-bold`">
                    {{ formatValue(getNestedValue(item, column.key), column) }}
                  </span>
                  <span v-else-if="column.type === 'currency'">
                    {{ formatCurrency(getNestedValue(item, column.key)) }}
                  </span>
                  <span v-else-if="column.type === 'date'">
                    {{ formatDate(getNestedValue(item, column.key)) }}
                  </span>
                  <span v-else-if="column.type === 'boolean'">
                    <span :class="`badge badge-light-${getNestedValue(item, column.key) ? 'success' : 'danger'} fs-7`">
                      {{ getNestedValue(item, column.key) ? 'Yes' : 'No' }}
                    </span>
                  </span>
                  <span v-else>
                    {{ formatValue(getNestedValue(item, column.key), column) }}
                  </span>
                </slot>
              </td>
              <td class="text-end">
                <div class="d-flex justify-content-end flex-shrink-0">
                  <button
                    class="btn btn-icon btn-bg-light btn-active-color-primary btn-sm me-1"
                    @click="$emit('view', item)"
                    title="View"
                  >
                    <i class="ki-duotone ki-eye fs-2">
                      <span class="path1"></span>
                      <span class="path2"></span>
                      <span class="path3"></span>
                    </i>
                  </button>
                  <button
                    class="btn btn-icon btn-bg-light btn-active-color-primary btn-sm me-1"
                    @click="$emit('edit', item)"
                    title="Edit"
                  >
                    <i class="ki-duotone ki-pencil fs-2">
                      <span class="path1"></span>
                      <span class="path2"></span>
                    </i>
                  </button>
                  <button
                    class="btn btn-icon btn-bg-light btn-active-color-danger btn-sm"
                    @click="$emit('delete', item)"
                    title="Delete"
                  >
                    <i class="ki-duotone ki-trash fs-2">
                      <span class="path1"></span>
                      <span class="path2"></span>
                      <span class="path3"></span>
                      <span class="path4"></span>
                      <span class="path5"></span>
                    </i>
                  </button>
                </div>
              </td>
            </tr>
          </tbody>
          <!--end::Table body-->
        </table>
      </div>
      <!--end::Table-->

      <!--begin::Empty state-->
      <div v-else class="d-flex flex-column flex-center py-10">
        <img
          :src="getAssetPath('media/illustrations/sketchy-1/5.png')"
          alt=""
          class="mw-400px"
        />
        <div class="fs-1 fw-bolder text-dark mb-4">No {{ title.toLowerCase() }} found</div>
        <div class="fs-6">Start by creating your first {{ title.toLowerCase().slice(0, -1) }}</div>
      </div>
      <!--end::Empty state-->

      <!--begin::Pagination-->
      <div v-if="totalPages > 1" class="row">
        <div class="col-sm-12 col-md-5 d-flex align-items-center justify-content-center justify-content-md-start">
          <div class="dataTables_info">
            Showing {{ (currentPage - 1) * itemsPerPage + 1 }} to 
            {{ Math.min(currentPage * itemsPerPage, filteredItems.length) }} of 
            {{ filteredItems.length }} entries
          </div>
        </div>
        <div class="col-sm-12 col-md-7 d-flex align-items-center justify-content-center justify-content-md-end">
          <div class="dataTables_paginate paging_simple_numbers">
            <ul class="pagination">
              <li :class="['paginate_button', 'page-item', 'previous', { disabled: currentPage === 1 }]">
                <a href="#" @click.prevent="currentPage > 1 && (currentPage--)" class="page-link">
                  <i class="previous"></i>
                </a>
              </li>
              <li
                v-for="page in visiblePages"
                :key="page"
                :class="['paginate_button', 'page-item', { active: page === currentPage }]"
              >
                <a href="#" @click.prevent="currentPage = page" class="page-link">{{ page }}</a>
              </li>
              <li :class="['paginate_button', 'page-item', 'next', { disabled: currentPage === totalPages }]">
                <a href="#" @click.prevent="currentPage < totalPages && (currentPage++)" class="page-link">
                  <i class="next"></i>
                </a>
              </li>
            </ul>
          </div>
        </div>
      </div>
      <!--end::Pagination-->
    </div>
    <!--end::Card body-->
  </div>
</template>

<script lang="ts">
import { defineComponent, computed, ref, watch } from "vue";
import { getAssetPath } from "@/core/helpers/assets";

export interface TableColumn {
  key: string;
  title: string;
  type?: 'text' | 'badge' | 'currency' | 'date' | 'boolean';
  width?: string;
  sortable?: boolean;
}

export default defineComponent({
  name: "crud-data-table",
  emits: ['create', 'edit', 'view', 'delete'],
  props: {
    title: {
      type: String,
      required: true,
    },
    items: {
      type: Array,
      default: () => [],
    },
    columns: {
      type: Array as () => TableColumn[],
      required: true,
    },
    loading: {
      type: Boolean,
      default: false,
    },
    error: {
      type: String,
      default: null,
    },
    itemsPerPage: {
      type: Number,
      default: 10,
    },
  },
  setup(props) {
    const searchQuery = ref("");
    const sortBy = ref("");
    const sortDirection = ref<'asc' | 'desc'>('asc');
    const currentPage = ref(1);

    // Computed properties
    const filteredItems = computed(() => {
      if (!searchQuery.value) return props.items;
      
      const query = searchQuery.value.toLowerCase();
      return props.items.filter((item: any) =>
        props.columns.some(column =>
          String(getNestedValue(item, column.key)).toLowerCase().includes(query)
        )
      );
    });

    const sortedItems = computed(() => {
      if (!sortBy.value) return filteredItems.value;
      
      return [...filteredItems.value].sort((a: any, b: any) => {
        const aVal = getNestedValue(a, sortBy.value);
        const bVal = getNestedValue(b, sortBy.value);
        
        if (sortDirection.value === 'asc') {
          return aVal > bVal ? 1 : -1;
        } else {
          return aVal < bVal ? 1 : -1;
        }
      });
    });

    const paginatedItems = computed(() => {
      const start = (currentPage.value - 1) * props.itemsPerPage;
      const end = start + props.itemsPerPage;
      return sortedItems.value.slice(start, end);
    });

    const totalPages = computed(() =>
      Math.ceil(filteredItems.value.length / props.itemsPerPage)
    );

    const visiblePages = computed(() => {
      const pages = [];
      const start = Math.max(1, currentPage.value - 2);
      const end = Math.min(totalPages.value, currentPage.value + 2);
      
      for (let i = start; i <= end; i++) {
        pages.push(i);
      }
      return pages;
    });

    // Watch for search changes to reset pagination
    watch(searchQuery, () => {
      currentPage.value = 1;
    });

    // Methods
    const getNestedValue = (obj: any, path: string) => {
      return path.split('.').reduce((o, p) => (o && o[p]) || '', obj);
    };

    const handleSearch = () => {
      // Search is reactive through computed property
    };

    const handleSort = (column: string) => {
      if (sortBy.value === column) {
        sortDirection.value = sortDirection.value === 'asc' ? 'desc' : 'asc';
      } else {
        sortBy.value = column;
        sortDirection.value = 'asc';
      }
    };

    const formatValue = (value: any, column: TableColumn): string => {
      if (value === null || value === undefined) return '-';
      return String(value);
    };

    const formatCurrency = (value: number): string => {
      return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD',
      }).format(value || 0);
    };

    const formatDate = (value: string): string => {
      if (!value) return '-';
      return new Date(value).toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
      });
    };

    const getBadgeColor = (value: string): string => {
      const colorMap: Record<string, string> = {
        active: 'success',
        pending: 'warning',
        completed: 'success',
        cancelled: 'danger',
        paid: 'success',
        confirmed: 'info',
        medical: 'danger',
        charter: 'primary',
        maintenance: 'secondary',
      };
      return colorMap[String(value).toLowerCase()] || 'secondary';
    };

    return {
      searchQuery,
      sortBy,
      sortDirection,
      currentPage,
      filteredItems,
      paginatedItems,
      totalPages,
      visiblePages,
      getNestedValue,
      handleSearch,
      handleSort,
      formatValue,
      formatCurrency,
      formatDate,
      getBadgeColor,
      getAssetPath,
    };
  },
});
</script>