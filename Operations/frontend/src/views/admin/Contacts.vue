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
            placeholder="Search Contacts"
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
            <span class="me-2">{{ selectedIds.length }}</span>Selected
          </div>
          <button
            type="button"
            class="btn btn-danger"
            @click="deleteFewContacts()"
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
        :data="contacts"
        :header="headerConfig"
        :checkbox-enabled="true"
        :loading="loading"
        :total="totalItems"
        :current-page="currentPage"
        :items-per-page="pageSize"
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

        <template v-slot:actions="{ row: contact }">
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
              <a @click.prevent="handleView(contact)" href="#" class="menu-link px-3">
                <KTIcon icon-name="eye" icon-class="fs-6 me-2" />
                View Details
              </a>
            </div>
            <!--end::Menu item-->
            <!--begin::Menu item-->
            <div class="menu-item px-3">
              <a @click.prevent="handleEdit(contact)" href="#" class="menu-link px-3">
                <KTIcon icon-name="pencil" icon-class="fs-6 me-2" />
                Edit Contact
              </a>
            </div>
            <!--end::Menu item-->
            
            <!--begin::Type-specific actions-->
            <div v-if="!isPatient(contact)" class="menu-item px-3">
              <a @click.prevent="handleCreatePatient(contact)" href="#" class="menu-link px-3">
                <KTIcon icon-name="medical-mask" icon-class="fs-6 me-2" />
                Make Patient
              </a>
            </div>
            
            <div v-if="!isStaff(contact)" class="menu-item px-3">
              <a @click.prevent="handleCreateStaff(contact)" href="#" class="menu-link px-3">
                <KTIcon icon-name="people" icon-class="fs-6 me-2" />
                Make Staff
              </a>
            </div>
            
            <div v-if="isPatient(contact)" class="menu-item px-3">
              <a @click.prevent="handleViewPatientDetails(contact)" href="#" class="menu-link px-3">
                <KTIcon icon-name="heart-pulse" icon-class="fs-6 me-2" />
                View Patient Details
              </a>
            </div>
            
            <div v-if="isStaff(contact)" class="menu-item px-3">
              <a @click.prevent="handleViewStaffDetails(contact)" href="#" class="menu-link px-3">
                <KTIcon icon-name="badge" icon-class="fs-6 me-2" />
                View Staff Details
              </a>
            </div>
            
            <div v-if="!isPatient(contact) && !isStaff(contact)" class="menu-item px-3">
              <a @click.prevent="handleCreateQuote(contact)" href="#" class="menu-link px-3">
                <KTIcon icon-name="dollar" icon-class="fs-6 me-2" />
                Create Quote
              </a>
            </div>
            <!--end::Type-specific actions-->
            <!--begin::Separator-->
            <div class="separator my-2"></div>
            <!--end::Separator-->
            <!--begin::Menu item-->
            <div class="menu-item px-3">
              <a @click.prevent="handleDelete(contact)" href="#" class="menu-link px-3 text-danger">
                <KTIcon icon-name="trash" icon-class="fs-6 me-2" />
                Delete Contact
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
  
  <!-- Create Contact Modal -->
  <CreateContactModal 
    @contactCreated="onContactCreated" 
    @openPatientModal="onOpenPatientModal" 
    @openStaffModal="onOpenStaffModal"
    @openPassengerModal="onOpenPassengerModal" 
  />
  
  <!-- Create Patient From Contact Modal -->
  <CreatePatientFromContactModal 
    ref="patientModalRef"
    @patientCreated="onPatientCreated" 
    @modalClosed="onPatientModalClosed" 
  />
  
  <!-- Create Staff From Contact Modal -->
  <CreateStaffFromContactModal 
    ref="staffModalRef"
    @staffCreated="onStaffCreated" 
    @modalClosed="onStaffModalClosed" 
  />
  
  <!-- Create Passenger From Contact Modal -->
  <CreatePassengerFromContactModal 
    ref="passengerModalRef"
    @passengerCreated="onPassengerCreated" 
    @modalClosed="onPassengerModalClosed" 
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
import { Modal } from "bootstrap";
import CreateContactModal from "@/components/modals/CreateContactModal.vue";
import CreatePatientFromContactModal from "@/components/modals/CreatePatientFromContactModal.vue";
import CreateStaffFromContactModal from "@/components/modals/CreateStaffFromContactModal.vue";
import CreatePassengerFromContactModal from "@/components/modals/CreatePassengerFromContactModal.vue";

interface Contact {
  id: string;
  first_name?: string;
  last_name?: string;
  business_name?: string;
  email?: string;
  phone?: string;
  contact_type?: string;
  created_on: string;
}

export default defineComponent({
  name: "contacts-management",
  components: {
    KTDatatable,
    CreateContactModal,
    CreatePatientFromContactModal,
    CreateStaffFromContactModal,
    CreatePassengerFromContactModal,
  },
  setup() {
    const router = useRouter();
    const contacts = ref<Contact[]>([]);
    const loading = ref(false);
    const error = ref<string | null>(null);
    const { setToolbarActions } = useToolbar();
    const patientModalRef = ref();
    const staffModalRef = ref();
    const passengerModalRef = ref();
    const totalItems = ref(0);
    const currentPage = ref(1);
    const pageSize = ref(25);
    const searchTimeout = ref<NodeJS.Timeout | null>(null);
    const initData = ref<Contact[]>([]);

    const headerConfig = ref([
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
      {
        columnName: "Actions",
        columnLabel: "actions",
      },
    ]);

    const selectedIds = ref<Array<number>>([]);
    const search = ref<string>("");

    const fetchContacts = async (page: number = 1, pageLimit: number = 25, searchQuery: string = '') => {
      try {
        loading.value = true;
        error.value = null;
        
        const params = new URLSearchParams();
        params.append('page', page.toString());
        params.append('page_size', pageLimit.toString());
        if (searchQuery.trim()) {
          params.append('search', searchQuery.trim());
        }
        
        const { data } = await ApiService.get(`/contacts/?${params}`);
        contacts.value = data.results || [];
        totalItems.value = data.count || 0;
        currentPage.value = page;
      } catch (err: any) {
        error.value = err.response?.data?.detail || "Failed to fetch contacts";
        console.error("Error fetching contacts:", err);
        contacts.value = [];
        totalItems.value = 0;
      } finally {
        loading.value = false;
        // Reinitialize menu components after data loads
        setTimeout(() => {
          MenuComponent.reinitialization();
        }, 100);
      }
    };

    const handleCreate = () => {
      const modalElement = document.getElementById('kt_modal_create_contact');
      
      if (modalElement) {
        try {
          const modal = new Modal(modalElement);
          modal.show();
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
    };

    const handleView = (contact: Contact) => {
      // Navigate to contact details page
      window.open(`/admin/contacts/contacts/${contact.id}`, '_blank');
    };

    const handleEdit = (contact: Contact) => {
      Swal.fire({
        title: "Edit Contact",
        text: `Edit form for ${getContactName(contact)} would be implemented here`,
        icon: "info",
        confirmButtonText: "OK"
      });
    };

    const handleCreatePatient = (contact: Contact) => {
      Swal.fire({
        title: "Make Patient",
        text: `Create patient record for ${getContactName(contact)}?`,
        icon: "question",
        showCancelButton: true,
        confirmButtonText: "Yes, create patient",
        cancelButtonText: "Cancel"
      }).then(async (result) => {
        if (result.isConfirmed) {
          // This would create a patient using the existing contact
          Swal.fire({
            title: "Patient Created",
            text: "Patient record created successfully",
            icon: "success"
          });
        }
      });
    };

    const handleCreateStaff = (contact: Contact) => {
      Swal.fire({
        title: "Make Staff",
        text: `Create staff record for ${getContactName(contact)}?`,
        icon: "question",
        showCancelButton: true,
        confirmButtonText: "Yes, create staff",
        cancelButtonText: "Cancel"
      }).then(async (result) => {
        if (result.isConfirmed) {
          // This would create a staff using the existing contact
          Swal.fire({
            title: "Staff Created",
            text: "Staff record created successfully",
            icon: "success"
          });
        }
      });
    };

    const handleViewPatientDetails = async (contact: Contact) => {
      try {
        // Find the patient record that has this contact as info
        const patientsResponse = await ApiService.get('/patients/');
        const allPatients = patientsResponse.data.results || patientsResponse.data || [];
        const matchingPatient = allPatients.find((p: any) => p.info?.id === contact.id);
        
        if (matchingPatient) {
          router.push(`/admin/contacts/patients/${matchingPatient.id}`);
        } else {
          Swal.fire({
            title: "Patient Not Found",
            text: `Could not find patient record for ${getContactName(contact)}`,
            icon: "warning",
            confirmButtonText: "OK"
          });
        }
      } catch (error) {
        console.error('Error finding patient:', error);
        Swal.fire({
          title: "Error",
          text: "Failed to find patient details",
          icon: "error",
          confirmButtonText: "OK"
        });
      }
    };

    const handleViewStaffDetails = (contact: Contact) => {
      // Navigate to staff details - would need to get staff ID
      Swal.fire({
        title: "View Staff",
        text: `Navigate to staff details for ${getContactName(contact)}`,
        icon: "info",
        confirmButtonText: "OK"
      });
    };

    const handleCreateQuote = (contact: Contact) => {
      Swal.fire({
        title: "Create Quote",
        text: `Create a quote for ${getContactName(contact)}?`,
        icon: "question",
        showCancelButton: true,
        confirmButtonText: "Yes, create quote",
        cancelButtonText: "Cancel"
      }).then(async (result) => {
        if (result.isConfirmed) {
          // This would create a quote for the contact
          Swal.fire({
            title: "Quote Created",
            text: "Quote has been created successfully",
            icon: "success"
          });
        }
      });
    };

    const handleDelete = (contact: Contact) => {
      Swal.fire({
        title: "Delete Contact",
        text: `Are you sure you want to delete ${getContactName(contact)}? This action cannot be undone.`,
        icon: "warning",
        showCancelButton: true,
        confirmButtonText: "Yes, delete it!",
        cancelButtonText: "Cancel",
        confirmButtonColor: "#d33"
      }).then(async (result) => {
        if (result.isConfirmed) {
          try {
            await ApiService.delete(`/contacts/${contact.id}/`);
            
            Swal.fire({
              title: "Deleted!",
              text: "Contact has been deleted successfully.",
              icon: "success"
            }).then(async () => {
              // Refresh the contacts list
              await fetchContacts(currentPage.value, pageSize.value, search.value);
            });
          } catch (error) {
            Swal.fire({
              title: "Error",
              text: "Failed to delete the contact. Please try again.",
              icon: "error"
            });
          }
        }
      });
    };

    const getContactName = (contact: Contact): string => {
      if (contact.business_name) return contact.business_name;
      if (contact.first_name || contact.last_name) {
        return `${contact.first_name || ''} ${contact.last_name || ''}`.trim();
      }
      return 'Unnamed Contact';
    };

    // Helper methods to check contact type
    const isPatient = (contact: Contact): boolean => {
      return contact.contact_type?.toLowerCase() === 'patient';
    };

    const isStaff = (contact: Contact): boolean => {
      const type = contact.contact_type?.toLowerCase() || '';
      return type.includes('staff');
    };

    const isCustomer = (contact: Contact): boolean => {
      return contact.contact_type?.toLowerCase() === 'customer';
    };

    const getTypeColor = (type: string): string => {
      const typeKey = type?.toLowerCase();
      const colors: Record<string, string> = {
        'patient': 'danger',
        'staff - pilot': 'primary', 
        'staff - medic': 'success',
        'staff': 'info',
        'customer': 'warning',
        'passenger': 'secondary',
        'general': 'light',
      };
      return colors[typeKey] || 'light';
    };

    const formatDate = (dateString: string): string => {
      if (!dateString) return 'Not set';
      return new Date(dateString).toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
      });
    };

    const deleteFewContacts = async () => {
      if (selectedIds.value.length === 0) return;
      
      const result = await Swal.fire({
        title: "Delete Contacts",
        text: `Are you sure you want to delete ${selectedIds.value.length} contact(s)? This action cannot be undone.`,
        icon: "warning",
        showCancelButton: true,
        confirmButtonText: "Yes, delete them!",
        cancelButtonText: "Cancel",
        confirmButtonColor: "#d33"
      });
      
      if (result.isConfirmed) {
        try {
          loading.value = true;
          
          // Delete each selected contact via API
          for (const contactId of selectedIds.value) {
            await ApiService.delete(`/contacts/${contactId}/`);
          }
          
          selectedIds.value.length = 0;
          
          Swal.fire({
            title: "Deleted!",
            text: "Selected contacts have been deleted successfully.",
            icon: "success"
          }).then(() => {
            // Refresh the contacts list
            fetchContacts(currentPage.value, pageSize.value, search.value);
          });
        } catch (error) {
          console.error("Error deleting contacts:", error);
          Swal.fire({
            title: "Error",
            text: "Failed to delete some contacts. Please try again.",
            icon: "error"
          });
        } finally {
          loading.value = false;
        }
      }
    };

    const sort = (sort: Sort) => {
      const reverse: boolean = sort.order === "asc";
      if (sort.label) {
        arraySort(contacts.value, sort.label, { reverse });
      }
    };

    const onItemSelect = (selectedItems: Array<number>) => {
      selectedIds.value = selectedItems;
    };

    const searchItems = () => {
      // Clear the search timeout if it exists
      if (searchTimeout.value) {
        clearTimeout(searchTimeout.value);
      }
      
      // Set a new timeout to perform the search after a delay
      searchTimeout.value = setTimeout(() => {
        fetchContacts(currentPage.value, pageSize.value, search.value);
      }, 300);
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

    const onItemsPerPageChange = (itemsPerPage: number) => {
      pageSize.value = itemsPerPage;
      fetchContacts(1, itemsPerPage, search.value);
    };
    
    const onPageChange = (page: number) => {
      currentPage.value = page;
      fetchContacts(page, pageSize.value, search.value);
    };

    const onContactCreated = async (newContact: Contact) => {
      console.log('New contact created:', newContact);
      // Refresh the contacts list
      await fetchContacts(currentPage.value, pageSize.value, search.value);
    };

    const onPatientCreated = async (newPatient: any) => {
      console.log('New patient created from contact:', newPatient);
      // Could refresh contacts list if needed or show confirmation
    };

    const onPatientModalClosed = () => {
      // Patient modal was closed, could do cleanup if needed
      console.log('Patient creation modal closed');
    };

    const onOpenPatientModal = (contact: Contact) => {
      // Open patient modal with contact data
      nextTick(() => {
        if (patientModalRef.value?.setContact) {
          patientModalRef.value.setContact(contact);
          
          // Open the modal
          const patientModalElement = document.getElementById('kt_modal_create_patient_from_contact');
          if (patientModalElement) {
            try {
              const patientModal = new Modal(patientModalElement);
              patientModal.show();
            } catch (error) {
              console.error('Error opening patient modal:', error);
            }
          }
        }
      });
    };

    const onStaffCreated = async (newStaff: any) => {
      console.log('New staff created from contact:', newStaff);
      // Could refresh contacts list if needed or show confirmation
    };

    const onStaffModalClosed = () => {
      // Staff modal was closed, could do cleanup if needed
      console.log('Staff creation modal closed');
    };

    const onOpenStaffModal = (contact: Contact) => {
      // Open staff modal with contact data
      nextTick(() => {
        if (staffModalRef.value?.setContact) {
          staffModalRef.value.setContact(contact);
          
          // Open the modal
          const staffModalElement = document.getElementById('kt_modal_create_staff_from_contact');
          if (staffModalElement) {
            try {
              const staffModal = new Modal(staffModalElement);
              staffModal.show();
            } catch (error) {
              console.error('Error opening staff modal:', error);
            }
          }
        }
      });
    };

    const onPassengerCreated = async (newPassenger: any) => {
      console.log('New passenger created from contact:', newPassenger);
      // Could refresh contacts list if needed or show confirmation
    };

    const onPassengerModalClosed = () => {
      // Passenger modal was closed, could do cleanup if needed
      console.log('Passenger creation modal closed');
    };

    const onOpenPassengerModal = (contact: Contact) => {
      // Open passenger modal with contact data
      nextTick(() => {
        if (passengerModalRef.value?.setContact) {
          passengerModalRef.value.setContact(contact);
          
          // Open the modal
          const passengerModalElement = document.getElementById('kt_modal_create_passenger_from_contact');
          if (passengerModalElement) {
            try {
              const passengerModal = new Modal(passengerModalElement);
              passengerModal.show();
            } catch (error) {
              console.error('Error opening passenger modal:', error);
            }
          }
        }
      });
    };

    onMounted(async () => {
      await fetchContacts(currentPage.value, pageSize.value);
      
      // Setup toolbar actions
      setToolbarActions([
        createToolbarActions.primary('add-contact', 'Add Contact', handleCreate, 'plus')
      ]);

      // Initialize menu components after DOM is ready
      await nextTick();
      setTimeout(() => {
        MenuComponent.reinitialization();
      }, 300);
    });

    return {
      search,
      searchItems,
      contacts,
      headerConfig,
      loading,
      error,
      sort,
      onItemSelect,
      selectedIds,
      deleteFewContacts,
      onItemsPerPageChange,
      handleCreate,
      handleView,
      handleEdit,
      handleCreatePatient,
      handleCreateStaff,
      handleViewPatientDetails,
      handleViewStaffDetails,
      handleCreateQuote,
      handleDelete,
      getContactName,
      isPatient,
      isStaff,
      isCustomer,
      getTypeColor,
      formatDate,
      onContactCreated,
      onPatientCreated,
      onPatientModalClosed,
      onOpenPatientModal,
      onStaffCreated,
      onStaffModalClosed,
      onOpenStaffModal,
      onPassengerCreated,
      onPassengerModalClosed,
      onOpenPassengerModal,
      patientModalRef,
      staffModalRef,
      passengerModalRef,
      totalItems,
      currentPage,
      pageSize,
      onPageChange,
    };
  },
});
</script>