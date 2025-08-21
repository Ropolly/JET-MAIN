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
            placeholder="Search Patients"
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
            @click="exportPatients"
          >
            <KTIcon icon-name="exit-up" icon-class="fs-2" />
            Export
          </button>
          <!--end::Export-->

          <!--begin::Add patient-->
          <button
            type="button"
            class="btn btn-primary"
            @click="handleCreate"
          >
            <KTIcon icon-name="plus" icon-class="fs-2" />
            Add Patient
          </button>
          <!--end::Add patient-->
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
            @click="deleteFewPatients()"
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
        :data="patients"
        :header="headerConfig"
        :checkbox-enabled="true"
        :loading="loading"
      >
        <template v-slot:patient="{ row: patient }">
          <div class="d-flex align-items-center">
            <div class="symbol symbol-circle symbol-50px overflow-hidden me-3">
              <div class="symbol-label bg-light-success">
                <i class="ki-duotone ki-profile-user fs-2x text-success">
                  <span class="path1"></span>
                  <span class="path2"></span>
                  <span class="path3"></span>
                  <span class="path4"></span>
                </i>
              </div>
            </div>
            <div class="d-flex flex-column">
              <a href="#" class="text-gray-800 text-hover-primary mb-1 fs-6 fw-bold">
                {{ getPatientName(patient) }}
              </a>
              <span class="text-muted fs-7">{{ patient.date_of_birth || 'DOB not set' }}</span>
            </div>
          </div>
        </template>

        <template v-slot:medical="{ row: patient }">
          <div class="d-flex flex-column">
            <span class="text-dark fw-semibold fs-6">
              {{ patient.medical_conditions || 'None specified' }}
            </span>
            <span class="text-muted fs-7">{{ patient.weight ? `${patient.weight} lbs` : 'Weight not set' }}</span>
          </div>
        </template>

        <template v-slot:mobility="{ row: patient }">
          <span :class="`badge badge-light-${patient.mobility_assistance ? 'warning' : 'success'} fs-7 fw-bold`">
            {{ patient.mobility_assistance ? 'Required' : 'Not Required' }}
          </span>
        </template>

        <template v-slot:created="{ row: patient }">
          {{ formatDate(patient.created_on) }}
        </template>

        <template v-slot:actions="{ row: patient }">
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
              <a @click="handleView(patient)" class="menu-link px-3"
                >View</a
              >
            </div>
            <!--end::Menu item-->
            <!--begin::Menu item-->
            <div class="menu-item px-3">
              <a @click="handleEdit(patient)" class="menu-link px-3"
                >Edit</a
              >
            </div>
            <!--end::Menu item-->
            <!--begin::Menu item-->
            <div class="menu-item px-3">
              <a @click="handleDelete(patient)" class="menu-link px-3"
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
import ApiService from "@/core/services/ApiService";
import KTDatatable from "@/components/kt-datatable/KTDataTable.vue";
import type { Sort } from "@/components/kt-datatable/table-partials/models";
import arraySort from "array-sort";
import { MenuComponent } from "@/assets/ts/components";
import Swal from "sweetalert2";

interface Patient {
  id: string;
  first_name: string;
  last_name: string;
  date_of_birth: string;
  weight: number;
  medical_conditions: string;
  mobility_assistance: boolean;
  created_on: string;
  updated_on: string;
}

export default defineComponent({
  name: "patients-management",
  components: {
    KTDatatable,
  },
  setup() {
    const patients = ref<Patient[]>([]);
    const loading = ref(false);
    const error = ref<string | null>(null);

    const headerConfig = ref([
      {
        columnName: "Patient",
        columnLabel: "patient",
        sortEnabled: true,
      },
      {
        columnName: "Medical Info",
        columnLabel: "medical",
        sortEnabled: false,
      },
      {
        columnName: "Mobility",
        columnLabel: "mobility",
        sortEnabled: true,
      },
      {
        columnName: "Created",
        columnLabel: "created",
        sortEnabled: true,
      },
      {
        columnName: "Actions",
        columnLabel: "actions",
      },
    ]);

    const initData = ref<Array<Patient>>([]);
    const selectedIds = ref<Array<number>>([]);
    const search = ref<string>("");

    const fetchPatients = async () => {
      try {
        loading.value = true;
        error.value = null;
        const { data } = await ApiService.get("/patients/");
        patients.value = data.results || data;
        initData.value.splice(0, patients.value.length, ...patients.value);
      } catch (err: any) {
        error.value = err.response?.data?.detail || "Failed to fetch patients";
        console.error("Error fetching patients:", err);
      } finally {
        loading.value = false;
      }
    };

    const handleCreate = () => {
      Swal.fire({
        title: "Create Patient",
        text: "Patient creation form would open here",
        icon: "info",
        confirmButtonText: "OK"
      });
    };

    const handleEdit = (patient: Patient) => {
      Swal.fire({
        title: "Edit Patient",
        text: `Edit form for ${getPatientName(patient)} would open here`,
        icon: "info",
        confirmButtonText: "OK"
      });
    };

    const handleView = (patient: Patient) => {
      Swal.fire({
        title: "Patient Details",
        html: `
          <div class="text-start">
            <p><strong>Name:</strong> ${getPatientName(patient)}</p>
            <p><strong>Date of Birth:</strong> ${patient.date_of_birth || 'Not set'}</p>
            <p><strong>Weight:</strong> ${patient.weight ? `${patient.weight} lbs` : 'Not set'}</p>
            <p><strong>Medical Conditions:</strong> ${patient.medical_conditions || 'None specified'}</p>
            <p><strong>Mobility Assistance:</strong> ${patient.mobility_assistance ? 'Required' : 'Not required'}</p>
          </div>
        `,
        icon: "info",
        confirmButtonText: "OK"
      });
    };

    const handleDelete = (patient: Patient) => {
      Swal.fire({
        title: "Delete Patient",
        text: `Are you sure you want to delete ${getPatientName(patient)}?`,
        icon: "warning",
        showCancelButton: true,
        confirmButtonText: "Yes, delete it!",
        cancelButtonText: "Cancel"
      }).then((result) => {
        if (result.isConfirmed) {
          Swal.fire("Deleted!", "Patient has been deleted.", "success");
        }
      });
    };

    const getPatientName = (patient: Patient): string => {
      if (patient.first_name || patient.last_name) {
        return `${patient.first_name || ''} ${patient.last_name || ''}`.trim();
      }
      return 'Unnamed Patient';
    };

    const formatDate = (dateString: string): string => {
      if (!dateString) return 'Not set';
      return new Date(dateString).toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
      });
    };

    const deleteFewPatients = () => {
      selectedIds.value.forEach((item) => {
        deletePatient(item);
      });
      selectedIds.value.length = 0;
    };

    const deletePatient = (id: number) => {
      for (let i = 0; i < patients.value.length; i++) {
        if (patients.value[i].id === id.toString()) {
          patients.value.splice(i, 1);
        }
      }
    };

    const sort = (sort: Sort) => {
      const reverse: boolean = sort.order === "asc";
      if (sort.label) {
        arraySort(patients.value, sort.label, { reverse });
      }
    };

    const onItemSelect = (selectedItems: Array<number>) => {
      selectedIds.value = selectedItems;
    };

    const searchItems = () => {
      patients.value.splice(0, patients.value.length, ...initData.value);
      if (search.value !== "") {
        let results: Array<Patient> = [];
        for (let j = 0; j < initData.value.length; j++) {
          if (searchingFunc(initData.value[j], search.value)) {
            results.push(initData.value[j]);
          }
        }
        patients.value.splice(0, patients.value.length, ...results);
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

    const exportPatients = () => {
      Swal.fire({
        title: "Export Patients",
        text: "Export functionality would be implemented here",
        icon: "info",
        confirmButtonText: "OK"
      });
    };

    onMounted(() => {
      fetchPatients();
    });

    return {
      search,
      searchItems,
      patients,
      headerConfig,
      loading,
      error,
      sort,
      onItemSelect,
      selectedIds,
      deleteFewPatients,
      deletePatient,
      onItemsPerPageChange,
      exportPatients,
      handleCreate,
      handleEdit,
      handleView,
      handleDelete,
      getPatientName,
      formatDate,
    };
  },
});
</script>