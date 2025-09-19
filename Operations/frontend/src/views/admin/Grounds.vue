<template>
  <div class="card">
    <div class="card-header border-0 pt-6">
      <div class="card-title">
        <div class="d-flex align-items-center position-relative my-1">
          <KTIcon icon-name="magnifier" icon-class="fs-1 position-absolute ms-6" />
          <input v-model="search" @input="searchItems()" type="text" class="form-control form-control-solid w-250px ps-14" placeholder="Search Ground Transportation" />
        </div>
      </div>
      <div class="card-toolbar" v-if="selectedIds.length > 0">
        <div class="d-flex justify-content-end align-items-center">
          <div class="fw-bold me-5"><span class="me-2">{{ selectedIds.length }}</span>Selected</div>
          <button type="button" class="btn btn-danger" @click="deleteFewGrounds()">Delete Selected</button>
        </div>
      </div>
    </div>
    <div class="card-body pt-0">
      <KTDatatable @on-sort="sort" @on-items-select="onItemSelect" @on-items-per-page-change="onItemsPerPageChange" :data="grounds" :header="headerConfig" :checkbox-enabled="true" :loading="loading">
        <template v-slot:ground="{ row: ground }">
          <div class="d-flex align-items-center">
            <div class="symbol symbol-circle symbol-50px overflow-hidden me-3">
              <div class="symbol-label bg-light-success"><i class="ki-duotone ki-car fs-2x text-success"><span class="path1"></span><span class="path2"></span><span class="path3"></span></i></div>
            </div>
            <div class="d-flex flex-column">
              <a href="#" @click="handleView(ground)" class="text-gray-800 text-hover-primary mb-1 fs-6 fw-bold">{{ ground.name || 'Unnamed Ground Service' }}</a>
              <span class="text-muted fs-7">{{ ground.service_type || 'Unknown type' }}</span>
            </div>
          </div>
        </template>
        <template v-slot:contact="{ row: ground }"><span class="text-dark fw-semibold">{{ ground.contact_info || 'No contact' }}</span></template>
        <template v-slot:coverage="{ row: ground }"><span class="text-dark fw-semibold">{{ ground.coverage_area || 'Not specified' }}</span></template>
        <template v-slot:actions="{ row: ground }">
          <a href="#" class="btn btn-sm btn-light btn-active-light-primary" data-kt-menu-trigger="click" data-kt-menu-placement="bottom-end">Actions <KTIcon icon-name="down" icon-class="fs-5 m-0" /></a>
          <div class="menu menu-sub menu-sub-dropdown menu-column menu-rounded menu-gray-600 menu-state-bg-light-primary fw-semibold fs-7 w-200px py-4" data-kt-menu="true">
            <div class="menu-item px-3"><a @click="handleEdit(ground)" class="menu-link px-3">Edit Ground Service</a></div>
            <div class="separator mt-3 opacity-75"></div>
            <div class="menu-item px-3"><a @click="handleDelete(ground)" class="menu-link px-3 text-danger">Delete</a></div>
          </div>
        </template>
      </KTDatatable>
    </div>
  </div>

  <!-- Create Ground Modal -->
  <CreateGroundModal @ground-created="onGroundCreated" />
</template>

<script lang="ts">
import { defineComponent, ref, onMounted, onUnmounted, nextTick } from "vue";
import { useRouter } from "vue-router";
import ApiService from "@/core/services/ApiService";
import KTDatatable from "@/components/kt-datatable/KTDataTable.vue";
import CreateGroundModal from "@/components/modals/CreateGroundModal.vue";
import type { Sort } from "@/components/kt-datatable/table-partials/models";
import arraySort from "array-sort";
import { MenuComponent } from "@/assets/ts/components";
import { Modal } from "bootstrap";
import Swal from "sweetalert2";
import { useToolbarStore } from "@/stores/toolbar";

export default defineComponent({
  name: "grounds-management",
  components: { KTDatatable, CreateGroundModal },
  setup() {
    const router = useRouter();
    const toolbarStore = useToolbarStore();
    const grounds = ref([]);
    const loading = ref(false);
    const selectedIds = ref([]);
    const search = ref("");
    const initData = ref([]);

    const headerConfig = ref([
      { columnName: "Ground Service", columnLabel: "ground", sortEnabled: true },
      { columnName: "Contact", columnLabel: "contact", sortEnabled: false },
      { columnName: "Coverage Area", columnLabel: "coverage", sortEnabled: false },
      { columnName: "Actions", columnLabel: "actions" }
    ]);

    const fetchGrounds = async () => {
      try {
        loading.value = true;
        const { data } = await ApiService.get("/grounds/");
        grounds.value = data.results || data;
        initData.value.splice(0, grounds.value.length, ...grounds.value);
      } catch (error) {
        console.error("Error fetching grounds:", error);
      } finally {
        loading.value = false;
      }
    };

    const handleCreate = () => {
      const modalElement = document.getElementById('kt_modal_create_ground');
      if (modalElement) {
        const modal = new Modal(modalElement);
        modal.show();
      }
    };

    const handleEdit = (ground) => {
      console.log('Edit clicked for Ground:', ground);

      Swal.fire({
        title: `Edit Ground Service: ${ground.name}`,
        html: `
          <div class="text-start">
            <div class="mb-3">
              <label class="form-label fw-bold">Service Name <span class="text-danger">*</span></label>
              <input id="edit-name" class="form-control" value="${ground.name || ''}" required>
            </div>
            <div class="mb-3">
              <label class="form-label fw-bold">Address Line 1</label>
              <input id="edit-address1" class="form-control" value="${ground.address_line1 || ''}">
            </div>
            <div class="mb-3">
              <label class="form-label fw-bold">Address Line 2</label>
              <input id="edit-address2" class="form-control" value="${ground.address_line2 || ''}">
            </div>
            <div class="row mb-3">
              <div class="col-4">
                <label class="form-label fw-bold">City</label>
                <input id="edit-city" class="form-control" value="${ground.city || ''}">
              </div>
              <div class="col-4">
                <label class="form-label fw-bold">State</label>
                <input id="edit-state" class="form-control" value="${ground.state || ''}">
              </div>
              <div class="col-4">
                <label class="form-label fw-bold">ZIP</label>
                <input id="edit-zip" class="form-control" value="${ground.zip || ''}">
              </div>
            </div>
            <div class="mb-3">
              <label class="form-label fw-bold">Country</label>
              <input id="edit-country" class="form-control" value="${ground.country || ''}">
            </div>
            <div class="mb-3">
              <label class="form-label fw-bold">Notes</label>
              <textarea id="edit-notes" class="form-control" rows="3">${ground.notes || ''}</textarea>
            </div>
          </div>
        `,
        width: '500px',
        showCancelButton: true,
        confirmButtonText: 'Save Changes',
        cancelButtonText: 'Cancel',
        allowOutsideClick: false,
        allowEscapeKey: false,
        focusConfirm: false,
        preConfirm: () => {
          const name = (document.getElementById('edit-name') as HTMLInputElement)?.value?.trim();
          if (!name) {
            Swal.showValidationMessage('Service name is required');
            return false;
          }

          return {
            name: name,
            address_line1: (document.getElementById('edit-address1') as HTMLInputElement)?.value || '',
            address_line2: (document.getElementById('edit-address2') as HTMLInputElement)?.value || '',
            city: (document.getElementById('edit-city') as HTMLInputElement)?.value || '',
            state: (document.getElementById('edit-state') as HTMLInputElement)?.value || '',
            zip: (document.getElementById('edit-zip') as HTMLInputElement)?.value || '',
            country: (document.getElementById('edit-country') as HTMLInputElement)?.value || '',
            notes: (document.getElementById('edit-notes') as HTMLTextAreaElement)?.value || ''
          };
        }
      }).then(async (result) => {
        if (result.isConfirmed && result.value) {
          console.log('Saving Ground with data:', result.value);

          try {
            await ApiService.put(`/grounds/${ground.id}/`, result.value);

            Swal.fire({
              icon: 'success',
              title: 'Success!',
              text: 'Ground service updated successfully.',
              timer: 2000,
              showConfirmButton: false
            });

            // Refresh the list
            await fetchGrounds();
          } catch (error) {
            console.error('Error updating ground service:', error);
            Swal.fire({
              icon: 'error',
              title: 'Error',
              text: 'Failed to update ground service.'
            });
          }
        }
      });
    };

    const handleDelete = async (ground) => {
      const result = await Swal.fire({
        title: "Delete Ground Service",
        text: `Delete ${ground.name}?`,
        icon: "warning",
        showCancelButton: true,
        confirmButtonText: "Yes, delete!"
      });

      if (result.isConfirmed) {
        try {
          await ApiService.delete(`/grounds/${ground.id}/`);
          await fetchGrounds();
          Swal.fire("Deleted!", "Ground service deleted.", "success");
        } catch (error) {
          Swal.fire("Error!", "Failed to delete ground service.", "error");
        }
      }
    };

    const deleteFewGrounds = () => {
      selectedIds.value.forEach(id => grounds.value = grounds.value.filter(g => g.id !== id));
      selectedIds.value = [];
    };

    const sort = (sort) => {
      if (sort.label) {
        arraySort(grounds.value, sort.label, { reverse: sort.order === "asc" });
      }
    };

    const onItemSelect = (items) => selectedIds.value = items;

    const searchItems = () => {
      grounds.value.splice(0, grounds.value.length, ...initData.value);
      if (search.value) {
        const results = initData.value.filter(item =>
          Object.values(item).some(val =>
            val?.toString().toLowerCase().includes(search.value.toLowerCase())
          )
        );
        grounds.value.splice(0, grounds.value.length, ...results);
      }
      MenuComponent.reinitialization();
    };

    const onItemsPerPageChange = () => {
      setTimeout(() => MenuComponent.reinitialization(), 0);
    };

    const onGroundCreated = () => {
      // Refresh the grounds list after creating a new one
      fetchGrounds();
    };

    onMounted(async () => {
      await fetchGrounds();
      await nextTick();
      setTimeout(() => MenuComponent.reinitialization(), 100);

      toolbarStore.setActions([{
        id: 'add-ground',
        label: 'Add Ground Service',
        icon: 'plus',
        variant: 'primary',
        handler: handleCreate
      }]);
    });

    onUnmounted(() => toolbarStore.clearActions());

    return {
      search,
      searchItems,
      grounds,
      headerConfig,
      loading,
      sort,
      onItemSelect,
      selectedIds,
      deleteFewGrounds,
      onItemsPerPageChange,
      handleCreate,
      handleEdit,
      handleDelete,
      onGroundCreated
    };
  },
});
</script>