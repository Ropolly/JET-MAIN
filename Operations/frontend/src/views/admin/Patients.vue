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
          <!-- Toolbar actions now handled by main toolbar -->
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
              <a @click.prevent="handleViewPatientDetails(patient)" href="#" class="text-gray-800 text-hover-primary mb-1 fs-6 fw-bold">
                {{ getPatientName(patient) }}
              </a>
              <span class="text-muted fs-7">{{ patient.info?.email || 'No email' }}</span>
            </div>
          </div>
        </template>

        <template v-slot:phone="{ row: patient }">
          <span class="text-dark fs-7">{{ patient.info?.phone || 'N/A' }}</span>
        </template>


        <template v-slot:trips="{ row: patient }">
          <div v-if="patient.trips && patient.trips.length > 0">
            <a 
              @click.prevent="navigateToTrip(patient.trips[0].id)" 
              href="#" 
              class="text-primary text-hover-primary fw-bold">
              {{ patient.trips[0].trip_number }}
            </a>
            <span v-if="patient.trips.length > 1" class="text-muted ms-1">
              +{{ patient.trips.length - 1 }}
            </span>
          </div>
          <span v-else class="text-muted fs-7">No trips</span>
        </template>

        <template v-slot:quotes="{ row: patient }">
          <div v-if="patient.quotes && patient.quotes.length > 0">
            <a 
              @click.prevent="navigateToQuote(patient.quotes[0].id)" 
              href="#" 
              class="text-primary text-hover-primary fw-bold">
              #{{ patient.quotes[0].id.slice(0, 8) }}
            </a>
            <span v-if="patient.quotes.length > 1" class="text-muted ms-1">
              +{{ patient.quotes.length - 1 }}
            </span>
          </div>
          <span v-else class="text-muted fs-7">No quotes</span>
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
            class="menu menu-sub menu-sub-dropdown menu-column menu-rounded menu-gray-600 menu-state-bg-light-primary fw-semibold fs-7 w-200px py-4"
            data-kt-menu="true"
          >
            <!--begin::Menu item-->
            <div class="menu-item px-3">
              <a @click.prevent="handleEdit(patient)" href="#" class="menu-link px-3">
                <KTIcon icon-name="pencil" icon-class="fs-6 me-2" />
                Edit Patient
              </a>
            </div>
            <!--end::Menu item-->
            <!--begin::Separator-->
            <div class="separator my-2"></div>
            <!--end::Separator-->
            <!--begin::Menu item-->
            <div class="menu-item px-3">
              <a @click.prevent="handleDelete(patient)" href="#" class="menu-link px-3 text-danger">
                <KTIcon icon-name="trash" icon-class="fs-6 me-2" />
                Delete Patient
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
  
  <!-- CreatePatientModal removed - now using direct contact modal workflow -->
  
  <!-- Create Contact Modal for Direct Patient Creation -->
  <CreateContactModal 
    ref="contactModalRef"
    :skipRoleSelection="true"
    @contactCreated="onContactCreatedForPatient" 
  />
  
  <!-- Create Patient From Contact Modal -->
  <CreatePatientFromContactModal 
    ref="patientFromContactModalRef"
    @patientCreated="onPatientFromContactCreated" 
    @modalClosed="onPatientFromContactModalClosed" 
  />
  
  <!-- Edit Patient Modal -->
  <EditPatientModal 
    ref="editPatientModalRef"
    @patientUpdated="onPatientUpdated" 
  />
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
// CreatePatientModal removed - using direct contact modal workflow
import CreateContactModal from "@/components/modals/CreateContactModal.vue";
import CreatePatientFromContactModal from "@/components/modals/CreatePatientFromContactModal.vue";
import EditPatientModal from "@/components/modals/EditPatientModal.vue";
import { Modal } from "bootstrap";

interface Patient {
  id: string;
  info: {
    id: string;
    first_name: string;
    last_name: string;
    business_name?: string;
    email?: string;
    phone?: string;
    address_line1?: string;
    city?: string;
    state?: string;
    country?: string;
  };
  date_of_birth: string;
  nationality: string;
  passport_number: string;
  passport_expiration_date: string;
  special_instructions?: string;
  status: string;
  bed_at_origin: boolean;
  bed_at_destination: boolean;
  created_on: string;
  trips: Array<{id: string, trip_number: string}>;
  quotes: Array<{id: string}>;
}

export default defineComponent({
  name: "patients-management",
  components: {
    KTDatatable,
    // CreatePatientModal removed - using direct workflow
    CreateContactModal,
    CreatePatientFromContactModal,
    EditPatientModal,
  },
  setup() {
    const router = useRouter();
    const patients = ref<Patient[]>([]);
    const loading = ref(false);
    const error = ref<string | null>(null);
    const { setToolbarActions } = useToolbar();
    const contactModalRef = ref();
    const patientFromContactModalRef = ref();
    const editPatientModalRef = ref();
    const createPatientModalRef = ref();

    const headerConfig = ref([
      {
        columnName: "Patient",
        columnLabel: "patient",
        sortEnabled: true,
      },
      {
        columnName: "Phone",
        columnLabel: "phone",
        sortEnabled: false,
      },
      {
        columnName: "Trips",
        columnLabel: "trips",
        sortEnabled: false,
      },
      {
        columnName: "Quotes",
        columnLabel: "quotes",
        sortEnabled: false,
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
        // Reinitialize menu components after data loads
        nextTick(() => {
          setTimeout(() => {
            MenuComponent.reinitialization();
          }, 100);
        });
      }
    };

    const handleCreate = () => {
      // Directly open the contact creation modal for patient creation
      nextTick(() => {
        const contactModalElement = document.getElementById('kt_modal_create_contact');
        if (contactModalElement) {
          try {
            // Set skip role selection to true for patient workflow
            if (contactModalRef.value?.setSkipRoleSelection) {
              contactModalRef.value.setSkipRoleSelection(true);
            }
            
            const contactModal = new Modal(contactModalElement);
            contactModal.show();
          } catch (error) {
            console.error('Error opening contact creation modal:', error);
            Swal.fire({
              title: "Error",
              text: "Unable to open contact creation form. Please refresh and try again.",
              icon: "error",
              confirmButtonText: "OK"
            });
          }
        }
      });
    };

    const handleEdit = (patient: Patient) => {
      if (editPatientModalRef.value?.setPatient) {
        editPatientModalRef.value.setPatient(patient);
        
        // Open the edit modal
        const editModalElement = document.getElementById('kt_modal_edit_patient');
        if (editModalElement) {
          try {
            const editModal = new Modal(editModalElement);
            editModal.show();
          } catch (error) {
            console.error('Error opening edit patient modal:', error);
          }
        }
      }
    };

    const handleView = (patient: Patient) => {
      Swal.fire({
        title: "Patient Details",
        html: `
          <div class="text-start">
            <p><strong>Name:</strong> ${getPatientName(patient)}</p>
            <p><strong>Date of Birth:</strong> ${formatDateOfBirth(patient.date_of_birth)}</p>
            <p><strong>Nationality:</strong> ${patient.nationality || 'Not set'}</p>
            <p><strong>Passport:</strong> ${patient.passport_number || 'Not provided'}</p>
            <p><strong>Special Instructions:</strong> ${patient.special_instructions || 'None specified'}</p>
            <p><strong>Bed Requirements:</strong> ${getBedRequirements(patient)}</p>
            <p><strong>Status:</strong> ${patient.status}</p>
            ${patient.info?.email ? `<p><strong>Email:</strong> ${patient.info.email}</p>` : ''}
            ${patient.info?.phone ? `<p><strong>Phone:</strong> ${patient.info.phone}</p>` : ''}
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
        cancelButtonText: "Cancel",
        confirmButtonColor: "#d33"
      }).then(async (result) => {
        if (result.isConfirmed) {
          try {
            await ApiService.delete(`/patients/${patient.id}/`);
            
            Swal.fire({
              title: "Deleted!",
              text: "Patient has been deleted successfully.",
              icon: "success"
            }).then(() => {
              // Refresh the patients list
              fetchPatients();
            });
          } catch (error) {
            Swal.fire({
              title: "Error",
              text: "Failed to delete the patient. Please try again.",
              icon: "error"
            });
          }
        }
      });
    };

    const handleViewContact = (patient: Patient) => {
      if (patient.id) {
        // Navigate to patient details page using patient ID
        window.open(`/admin/contacts/patients/${patient.id}`, '_blank');
      } else {
        Swal.fire({
          title: "No Contact Information",
          text: "This patient doesn't have associated contact information.",
          icon: "warning",
          confirmButtonText: "OK"
        });
      }
    };

    const handleViewPatientDetails = (patient: Patient) => {
      if (patient.id) {
        // Navigate to patient details page using patient ID
        router.push(`/admin/contacts/patients/${patient.id}`);
      }
    };

    const navigateToTrip = (tripId: string) => {
      router.push(`/admin/trips/${tripId}`);
    };

    const navigateToQuote = (quoteId: string) => {
      router.push(`/admin/quotes/${quoteId}`);
    };

    const handleViewTrips = (patient: Patient) => {
      Swal.fire({
        title: "Patient Trips",
        text: `Viewing trips for ${getPatientName(patient)}. This feature would show all trips associated with this patient.`,
        icon: "info",
        confirmButtonText: "OK"
      });
    };

    const handleUpdateStatus = (patient: Patient) => {
      const statusOptions = [
        { value: 'pending', text: 'Pending' },
        { value: 'confirmed', text: 'Confirmed' },
        { value: 'active', text: 'Active' },
        { value: 'completed', text: 'Completed' },
        { value: 'cancelled', text: 'Cancelled' }
      ];

      const selectHtml = statusOptions.map(option => 
        `<option value="${option.value}" ${option.value === patient.status ? 'selected' : ''}>${option.text}</option>`
      ).join('');

      Swal.fire({
        title: "Update Patient Status",
        html: `
          <div class="text-start">
            <p><strong>Patient:</strong> ${getPatientName(patient)}</p>
            <p><strong>Current Status:</strong> ${patient.status}</p>
            <div class="mb-3">
              <label for="status-select" class="form-label">New Status:</label>
              <select id="status-select" class="form-select">
                ${selectHtml}
              </select>
            </div>
          </div>
        `,
        showCancelButton: true,
        confirmButtonText: "Update Status",
        cancelButtonText: "Cancel",
        preConfirm: () => {
          const select = document.getElementById('status-select') as HTMLSelectElement;
          return select.value;
        }
      }).then(async (result) => {
        if (result.isConfirmed && result.value !== patient.status) {
          try {
            await ApiService.patch(`/patients/${patient.id}/`, { status: result.value });
            
            Swal.fire({
              title: "Status Updated!",
              text: `Patient status has been updated to ${result.value}.`,
              icon: "success"
            }).then(() => {
              // Refresh the patients list
              fetchPatients();
            });
          } catch (error) {
            Swal.fire({
              title: "Error",
              text: "Failed to update patient status. Please try again.",
              icon: "error"
            });
          }
        }
      });
    };

    const getPatientName = (patient: Patient): string => {
      if (!patient.info) return 'Unnamed Patient';
      
      const { first_name, last_name, business_name } = patient.info;
      
      if (business_name) return business_name;
      if (first_name || last_name) {
        return `${first_name || ''} ${last_name || ''}`.trim();
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

    const formatDateOfBirth = (dateString: string): string => {
      if (!dateString) return 'DOB not set';
      return new Date(dateString).toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
      });
    };

    const getBedRequirements = (patient: Patient): string => {
      const requirements = [];
      if (patient.bed_at_origin) requirements.push('Origin');
      if (patient.bed_at_destination) requirements.push('Destination');
      
      if (requirements.length === 0) return 'None';
      return `Bed at: ${requirements.join(' & ')}`;
    };

    const onPatientCreated = (newPatient: Patient) => {
      console.log('New patient created:', newPatient);
      // Refresh the patients list
      fetchPatients();
    };

    const onContactCreatedForPatient = async (newContact: any) => {
      console.log('New contact created for patient:', newContact);
      
      // Automatically open the patient form modal with the new contact
      nextTick(() => {
        if (patientFromContactModalRef.value?.setContact) {
          patientFromContactModalRef.value.setContact(newContact);
          
          // Open the patient modal
          const patientModalElement = document.getElementById('kt_modal_create_patient_from_contact');
          if (patientModalElement) {
            try {
              const patientModal = new Modal(patientModalElement);
              patientModal.show();
            } catch (error) {
              console.error('Error opening patient from contact modal:', error);
            }
          }
        }
      });
    };

    const onPatientFromContactCreated = (newPatient: any) => {
      console.log('New patient created from contact on patients page:', newPatient);
      // Refresh the patients list
      fetchPatients();
    };

    const onPatientFromContactModalClosed = () => {
      console.log('Patient from contact modal closed');
    };

    const onPatientUpdated = (updatedPatient: any) => {
      console.log('Patient updated:', updatedPatient);
      // Refresh the patients list
      fetchPatients();
    };

    const openContactForPatientCreation = () => {
      console.log('Opening contact creation modal for patient');
      nextTick(() => {
        const contactModalElement = document.getElementById('kt_modal_create_contact');
        if (contactModalElement) {
          try {
            // Set skip role selection to true
            if (contactModalRef.value?.setSkipRoleSelection) {
              contactModalRef.value.setSkipRoleSelection(true);
            }
            
            const contactModal = new Modal(contactModalElement);
            contactModal.show();
          } catch (error) {
            console.error('Error opening contact creation modal:', error);
          }
        }
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
      const searchValue = value.toLowerCase();
      
      // Search through flat properties
      for (let key in obj) {
        if (obj[key] && typeof obj[key] === "string") {
          if (obj[key].toLowerCase().indexOf(searchValue) !== -1) {
            return true;
          }
        } else if (typeof obj[key] === "object" && obj[key] !== null) {
          // Recursively search nested objects (like patient.info)
          if (searchingFunc(obj[key], value)) {
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


    onMounted(() => {
      fetchPatients();
      
      // Setup toolbar actions
      setToolbarActions([
        createToolbarActions.primary('add-patient', 'Add Patient', handleCreate, 'plus')
      ]);

      // Initialize menu components after everything is mounted
      nextTick(() => {
        setTimeout(() => {
          MenuComponent.reinitialization();
        }, 200);
      });
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
      handleCreate,
      handleEdit,
      handleDelete,
      handleViewPatientDetails,
      navigateToTrip,
      navigateToQuote,
      getPatientName,
      formatDate,
      formatDateOfBirth,
      getBedRequirements,
      onPatientCreated,
      onContactCreatedForPatient,
      onPatientFromContactCreated,
      onPatientFromContactModalClosed,
      onPatientUpdated,
      openContactForPatientCreation,
      contactModalRef,
      patientFromContactModalRef,
      editPatientModalRef,
      createPatientModalRef,
    };
  },
});
</script>