<template>
  <!--begin::Card-->
  <div class="card">
    <!--begin::Card header-->
    <div class="card-header border-0 pt-6">
      <!--begin::Card title-->
      <div class="card-title">
        <!--begin::Search-->
        <div class="d-flex align-items-center position-relative my-1">
          <KTIcon icon-name="magnifier" icon-class="fs-1 position-absolute ms-6" />
          <input
            v-model="search"
            @input="searchItems()"
            type="text"
            class="form-control form-control-solid w-250px ps-14"
            placeholder="Search by passenger name"
          />
        </div>
        <!--end::Search-->
      </div>

      <!--begin::Card toolbar-->
      <div class="card-toolbar" v-if="selectedIds.length > 0">
        <div class="d-flex justify-content-end align-items-center">
          <div class="fw-bold me-5">
            <span class="me-2">{{ selectedIds.length }}</span>Selected
          </div>
          <button type="button" class="btn btn-danger" @click="deleteFewPassengers()">
            Delete Selected
          </button>
        </div>
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
        :data="passengers"
        :header="headerConfig"
        :checkbox-enabled="true"
        :loading="loading"
      >
        <template v-slot:passenger="{ row: passenger }">
          <div class="d-flex align-items-center">
            <div class="symbol symbol-circle symbol-50px overflow-hidden me-3">
              <div class="symbol-label bg-light-warning">
                <i class="ki-duotone ki-profile-user fs-2x text-warning">
                  <span class="path1"></span>
                  <span class="path2"></span>
                  <span class="path3"></span>
                  <span class="path4"></span>
                </i>
              </div>
            </div>
            <div class="d-flex flex-column">
              <a href="#" @click="handleView(passenger)" class="text-gray-800 text-hover-primary mb-1 fs-6 fw-bold">
                {{ getPassengerName(passenger) }}
              </a>
              <span class="text-muted fs-7">{{ passenger.info?.email || 'No email' }}</span>
            </div>
          </div>
        </template>


        <template v-slot:contact="{ row: passenger }">
          <span class="text-dark fw-semibold">{{ passenger.contact_number || 'No contact' }}</span>
        </template>

        <template v-slot:trips="{ row: passenger }">
          <div v-if="passenger.trips && passenger.trips.length > 0">
            <a 
              @click.prevent="navigateToTrip(passenger.trips[0].id)" 
              href="#" 
              class="text-primary text-hover-primary fw-bold">
              {{ passenger.trips[0].trip_number }}
            </a>
            <span v-if="passenger.trips.length > 1" class="text-muted ms-1">
              +{{ passenger.trips.length - 1 }}
            </span>
          </div>
          <span v-else class="text-muted fs-7">No trips</span>
        </template>

        <template v-slot:status="{ row: passenger }">
          <select 
            :value="passenger.status || 'active'"
            @change="updatePassengerStatus(passenger, ($event.target as HTMLSelectElement).value)"
            class="form-select form-select-sm"
            :class="`text-${getStatusColor(passenger.status || 'active')}`"
          >
            <option value="active">Active</option>
            <option value="inactive">Inactive</option>
            <option value="pending">Pending</option>
          </select>
        </template>

        <template v-slot:actions="{ row: passenger }">
          <a
            href="#"
            class="btn btn-sm btn-light btn-active-light-primary"
            data-kt-menu-trigger="click"
            data-kt-menu-placement="bottom-end"
            data-kt-menu-flip="top-end"
            >Actions
            <KTIcon icon-name="down" icon-class="fs-5 m-0" />
          </a>
          <div class="menu menu-sub menu-sub-dropdown menu-column menu-rounded menu-gray-600 menu-state-bg-light-primary fw-semibold fs-7 w-200px py-4" data-kt-menu="true">
            <div class="menu-item px-3"><a @click.prevent="handleEdit(passenger)" href="#" class="menu-link px-3">Edit Passenger</a></div>
            <div class="separator mt-3 opacity-75"></div>
            <div class="menu-item px-3"><a @click.prevent="handleDelete(passenger)" href="#" class="menu-link px-3 text-danger">Delete</a></div>
          </div>
        </template>
      </KTDatatable>
    </div>
    <!--end::Card body-->
  </div>
  <!--end::Card-->
  
  <!-- Create Contact Modal -->
  <CreateContactModal 
    :skipRoleSelection="true"
    @contactCreated="onContactCreated" 
    @openPassengerModal="onOpenPassengerModal" 
  />
  
  <!-- Create Passenger From Contact Modal -->
  <CreatePassengerFromContactModal 
    ref="passengerModalRef"
    @passengerCreated="onPassengerCreated" 
    @modalClosed="onPassengerModalClosed" 
  />
  
  <!-- Edit Passenger Modal -->
  <EditPassengerModal 
    ref="editPassengerModalRef"
    @passengerUpdated="onPassengerUpdated" 
  />
</template>

<script lang="ts">
import { defineComponent, ref, onMounted, onUnmounted, nextTick } from "vue";
import { useRouter } from "vue-router";
import ApiService from "@/core/services/ApiService";
import KTDatatable from "@/components/kt-datatable/KTDataTable.vue";
import type { Sort } from "@/components/kt-datatable/table-partials/models";
import arraySort from "array-sort";
import { MenuComponent } from "@/assets/ts/components";
import Swal from "sweetalert2";
import { useToolbarStore } from "@/stores/toolbar";
import CreateContactModal from "@/components/modals/CreateContactModal.vue";
import CreatePassengerFromContactModal from "@/components/modals/CreatePassengerFromContactModal.vue";
import EditPassengerModal from "@/components/modals/EditPassengerModal.vue";
import { Modal } from "bootstrap";

export default defineComponent({
  name: "passengers-management",
  components: { 
    KTDatatable,
    CreateContactModal,
    CreatePassengerFromContactModal,
    EditPassengerModal,
  },
  setup() {
    const router = useRouter();
    const toolbarStore = useToolbarStore();
    const passengers = ref([]);
    const loading = ref(false);
    const selectedIds = ref([]);
    const search = ref("");
    const initData = ref([]);
    const passengerModalRef = ref();
    const editPassengerModalRef = ref();

    const headerConfig = ref([
      { columnName: "Passenger", columnLabel: "passenger", sortEnabled: true },
      { columnName: "Contact", columnLabel: "contact", sortEnabled: false },
      { columnName: "Trips", columnLabel: "trips", sortEnabled: false },
      { columnName: "Status", columnLabel: "status", sortEnabled: true },
      { columnName: "Actions", columnLabel: "actions" },
    ]);

    const fetchPassengers = async () => {
      try {
        loading.value = true;
        const { data } = await ApiService.get("/passengers/");
        passengers.value = data.results || data;
        initData.value.splice(0, passengers.value.length, ...passengers.value);
      } catch (error) {
        console.error("Error fetching passengers:", error);
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
    
    const onPassengerCreated = async (newPassenger: any) => {
      console.log('New passenger created:', newPassenger);
      // Refresh the passengers list
      await fetchPassengers();
    };

    const onPassengerUpdated = async (updatedPassenger: any) => {
      console.log('Passenger updated:', updatedPassenger);
      // Refresh the passengers list to get the latest data
      await fetchPassengers();
    };

    const onContactCreated = async (newContact: any) => {
      console.log('New contact created:', newContact);
      // Automatically trigger passenger creation for this contact
      nextTick(() => {
        onOpenPassengerModal(newContact);
      });
    };

    const onPassengerModalClosed = () => {
      console.log('Passenger creation modal closed');
    };

    const onOpenPassengerModal = (contact: any) => {
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
    const handleEdit = (passenger) => {
      if (editPassengerModalRef.value?.setPassenger) {
        editPassengerModalRef.value.setPassenger(passenger);
        
        // Open the modal
        const modalElement = document.getElementById('kt_modal_edit_passenger');
        if (modalElement) {
          try {
            const modal = new Modal(modalElement);
            modal.show();
          } catch (error) {
            console.error('Error opening edit passenger modal:', error);
            Swal.fire({
              title: "Error",
              text: "Unable to open edit form. Please refresh and try again.",
              icon: "error",
              confirmButtonText: "OK"
            });
          }
        }
      }
    };

    const updatePassengerStatus = async (passenger, newStatus) => {
      if (passenger.status === newStatus) return;
      
      try {
        await ApiService.patch(`/passengers/${passenger.id}/`, { status: newStatus });
        
        // Update local passenger status
        const passengerIndex = passengers.value.findIndex(p => p.id === passenger.id);
        if (passengerIndex !== -1) {
          passengers.value[passengerIndex].status = newStatus;
        }
        
        Swal.fire({
          title: "Status Updated!",
          text: `Passenger status changed to ${newStatus}`,
          icon: "success",
          timer: 2000,
          showConfirmButton: false
        });
        
      } catch (error) {
        console.error('Error updating passenger status:', error);
        Swal.fire({
          title: "Error!",
          text: "Failed to update passenger status. Please try again.",
          icon: "error"
        });
        
        // Refresh passengers to revert the change
        await fetchPassengers();
      }
    };
    const handleView = (passenger) => {
      router.push(`/admin/passengers/${passenger.id}`);
    };
    const handleViewTrips = (passenger) => router.push(`/admin/trips?passenger=${passenger.id}`);
    
    const navigateToTrip = (tripId) => {
      router.push(`/admin/trips/${tripId}`);
    };
    const handleDelete = async (passenger) => {
      const result = await Swal.fire({ title: "Delete Passenger", text: `Delete ${getPassengerName(passenger)}?`, icon: "warning", showCancelButton: true, confirmButtonText: "Yes, delete!" });
      if (result.isConfirmed) {
        try { await ApiService.delete(`/passengers/${passenger.id}/`); await fetchPassengers(); Swal.fire("Deleted!", "Passenger deleted.", "success"); }
        catch (error) { Swal.fire("Error!", "Failed to delete passenger.", "error"); }
      }
    };

    const formatDate = (date) => date ? new Date(date).toLocaleDateString() : 'N/A';
    const getStatusColor = (status) => ({ active: 'success', inactive: 'secondary' }[status?.toLowerCase()] || 'primary');
    
    const getPassengerName = (passenger) => {
      if (passenger?.info) {
        const first = passenger.info.first_name || '';
        const last = passenger.info.last_name || '';
        const fullName = `${first} ${last}`.trim();
        return fullName || passenger.info.business_name || passenger.info.email || 'Unnamed Passenger';
      }
      return 'Unnamed Passenger';
    };
    const deleteFewPassengers = () => { selectedIds.value.forEach(id => passengers.value = passengers.value.filter(p => p.id !== id)); selectedIds.value = []; };

    const sort = (sort) => { if (sort.label) arraySort(passengers.value, sort.label, { reverse: sort.order === "asc" }); };
    const onItemSelect = (items) => selectedIds.value = items;
    const searchItems = () => {
      passengers.value.splice(0, passengers.value.length, ...initData.value);
      if (search.value) {
        const searchTerm = search.value.toLowerCase();
        const results = initData.value.filter(passenger => {
          const name = getPassengerName(passenger).toLowerCase();
          const email = passenger.info?.email?.toLowerCase() || '';
          return name.includes(searchTerm) || email.includes(searchTerm);
        });
        passengers.value.splice(0, passengers.value.length, ...results);
      }
      MenuComponent.reinitialization();
    };
    const onItemsPerPageChange = () => setTimeout(() => MenuComponent.reinitialization(), 0);

    onMounted(async () => {
      await fetchPassengers();
      await nextTick();
      setTimeout(() => MenuComponent.reinitialization(), 100);
      toolbarStore.setActions([{ id: 'add-passenger', label: 'Add Passenger', icon: 'plus', variant: 'primary', handler: handleCreate }]);
    });

    onUnmounted(() => toolbarStore.clearActions());

    return {
      search, searchItems, passengers, headerConfig, loading, sort, onItemSelect, selectedIds, deleteFewPassengers, onItemsPerPageChange,
      handleCreate, onPassengerCreated, onPassengerUpdated, onContactCreated, onPassengerModalClosed, onOpenPassengerModal, passengerModalRef,
      handleEdit, handleView, handleDelete, formatDate, getStatusColor, getPassengerName, updatePassengerStatus, navigateToTrip, editPassengerModalRef,
    };
  },
});
</script>