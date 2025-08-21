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
            :placeholder="`Search ${title}`"
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
            @click="exportItems"
          >
            <KTIcon icon-name="exit-up" icon-class="fs-2" />
            Export
          </button>
          <!--end::Export-->

          <!--begin::Add item-->
          <button
            type="button"
            class="btn btn-primary"
            @click="handleCreate"
          >
            <KTIcon icon-name="plus" icon-class="fs-2" />
            Add {{ title.slice(0, -1) }}
          </button>
          <!--end::Add item-->
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
            @click="deleteFewItems()"
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
        :data="items"
        :header="headerConfig"
        :checkbox-enabled="true"
        :loading="loading"
      >
        <template v-for="(_, name) in $slots" v-slot:[name]="{ row: item }">
          <slot :name="name" :row="item" />
        </template>

        <template v-slot:actions="{ row: item }">
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
              <a @click="handleView(item)" class="menu-link px-3"
                >View</a
              >
            </div>
            <!--end::Menu item-->
            <!--begin::Menu item-->
            <div class="menu-item px-3">
              <a @click="handleEdit(item)" class="menu-link px-3"
                >Edit</a
              >
            </div>
            <!--end::Menu item-->
            <!--begin::Menu item-->
            <div class="menu-item px-3">
              <a @click="handleDelete(item)" class="menu-link px-3"
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
import { defineComponent, ref, onMounted, computed } from "vue";
import ApiService from "@/core/services/ApiService";
import KTDatatable from "@/components/kt-datatable/KTDataTable.vue";
import type { Sort } from "@/components/kt-datatable/table-partials/models";
import arraySort from "array-sort";
import { MenuComponent } from "@/assets/ts/components";
import Swal from "sweetalert2";

export default defineComponent({
  name: "admin-template",
  components: {
    KTDatatable,
  },
  props: {
    title: {
      type: String,
      required: true,
    },
    subtitle: {
      type: String,
      default: "",
    },
    endpoint: {
      type: String,
      required: true,
    },
    columns: {
      type: Array as () => Array<{
        columnName: string;
        columnLabel: string;
        sortEnabled?: boolean;
      }>,
      required: true,
    },
  },
  setup(props) {
    const items = ref([]);
    const loading = ref(false);
    const error = ref<string | null>(null);

    const headerConfig = computed(() => {
      return [
        ...props.columns,
        {
          columnName: "Actions",
          columnLabel: "actions",
        },
      ];
    });

    const initData = ref<Array<any>>([]);
    const selectedIds = ref<Array<number>>([]);
    const search = ref<string>("");

    const fetchItems = async () => {
      try {
        loading.value = true;
        error.value = null;
        const { data } = await ApiService.get(props.endpoint);
        items.value = data.results || data;
        initData.value.splice(0, items.value.length, ...items.value);
      } catch (err: any) {
        error.value = err.response?.data?.detail || `Failed to fetch ${props.title.toLowerCase()}`;
        console.error(`Error fetching ${props.title.toLowerCase()}:`, err);
      } finally {
        loading.value = false;
      }
    };

    const handleCreate = () => {
      Swal.fire({
        title: `Create ${props.title.slice(0, -1)}`,
        text: `${props.title.slice(0, -1)} creation form would open here`,
        icon: "info",
        confirmButtonText: "OK"
      });
    };

    const handleEdit = (item: any) => {
      Swal.fire({
        title: `Edit ${props.title.slice(0, -1)}`,
        text: `Edit form for ${props.title.toLowerCase().slice(0, -1)} would open here`,
        icon: "info",
        confirmButtonText: "OK"
      });
    };

    const handleView = (item: any) => {
      Swal.fire({
        title: `${props.title.slice(0, -1)} Details`,
        text: `Details view for ${props.title.toLowerCase().slice(0, -1)} would open here`,
        icon: "info",
        confirmButtonText: "OK"
      });
    };

    const handleDelete = (item: any) => {
      Swal.fire({
        title: `Delete ${props.title.slice(0, -1)}`,
        text: `Are you sure you want to delete this ${props.title.toLowerCase().slice(0, -1)}?`,
        icon: "warning",
        showCancelButton: true,
        confirmButtonText: "Yes, delete it!",
        cancelButtonText: "Cancel"
      }).then((result) => {
        if (result.isConfirmed) {
          Swal.fire("Deleted!", `${props.title.slice(0, -1)} has been deleted.`, "success");
        }
      });
    };

    const deleteFewItems = () => {
      selectedIds.value.forEach((item) => {
        deleteItem(item);
      });
      selectedIds.value.length = 0;
    };

    const deleteItem = (id: number) => {
      for (let i = 0; i < items.value.length; i++) {
        if (items.value[i].id === id.toString()) {
          items.value.splice(i, 1);
        }
      }
    };

    const sort = (sort: Sort) => {
      const reverse: boolean = sort.order === "asc";
      if (sort.label) {
        arraySort(items.value, sort.label, { reverse });
      }
    };

    const onItemSelect = (selectedItems: Array<number>) => {
      selectedIds.value = selectedItems;
    };

    const searchItems = () => {
      items.value.splice(0, items.value.length, ...initData.value);
      if (search.value !== "") {
        let results: Array<any> = [];
        for (let j = 0; j < initData.value.length; j++) {
          if (searchingFunc(initData.value[j], search.value)) {
            results.push(initData.value[j]);
          }
        }
        items.value.splice(0, items.value.length, ...results);
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

    const exportItems = () => {
      Swal.fire({
        title: `Export ${props.title}`,
        text: "Export functionality would be implemented here",
        icon: "info",
        confirmButtonText: "OK"
      });
    };

    onMounted(() => {
      fetchItems();
    });

    return {
      search,
      searchItems,
      items,
      headerConfig,
      loading,
      error,
      sort,
      onItemSelect,
      selectedIds,
      deleteFewItems,
      deleteItem,
      onItemsPerPageChange,
      exportItems,
      handleCreate,
      handleEdit,
      handleView,
      handleDelete,
    };
  },
});
</script>