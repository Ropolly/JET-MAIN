<template>
  <div class="card">
    <div class="card-header border-0 pt-6">
      <div class="card-title">
        <div class="d-flex align-items-center position-relative my-1">
          <KTIcon icon-name="magnifier" icon-class="fs-1 position-absolute ms-6" />
          <input v-model="search" @input="searchItems" type="text" class="form-control form-control-solid w-250px ps-14" placeholder="Search FBOs" />
        </div>
      </div>
      <div class="card-toolbar" v-if="selectedIds.length > 0">
        <div class="d-flex justify-content-end align-items-center">
          <div class="fw-bold me-5"><span class="me-2">{{ selectedIds.length }}</span>Selected</div>
          <button type="button" class="btn btn-danger" @click="deleteFewFbos">Delete Selected</button>
        </div>
      </div>
    </div>
    <div class="card-body pt-0">
      <KTDatatable 
        @on-sort="sort" 
        @on-items-select="onItemSelect" 
        @on-items-per-page-change="onItemsPerPageChange"
        @page-change="onPageChange"
        :data="fbos" 
        :header="headerConfig" 
        :checkbox-enabled="true" 
        :loading="loading"
        :total="totalItems"
        :current-page="currentPage"
        :items-per-page="fbos.length || pageSize"
        :items-per-page-dropdown-enabled="true"
      >
        <template v-slot:fbo="{ row: fbo }">
          <div class="d-flex align-items-center">
            <div class="symbol symbol-circle symbol-50px overflow-hidden me-3">
              <div class="symbol-label bg-light-info"><i class="ki-duotone ki-home-2 fs-2x text-info"><span class="path1"></span><span class="path2"></span></i></div>
            </div>
            <div class="d-flex flex-column">
              <a href="#" @click.prevent="navigateToFboDetails(fbo.id)" class="text-gray-800 text-hover-primary mb-1 fs-6 fw-bold">{{ fbo.name || 'Unnamed FBO' }}</a>
              <span class="text-muted fs-7">{{ getLocationText(fbo) }}</span>
            </div>
          </div>
        </template>
        <template v-slot:phone="{ row: fbo }">
          <div class="d-flex flex-column">
            <span class="text-dark fw-semibold">{{ fbo.phone || 'No phone' }}</span>
            <span class="text-muted fs-7" v-if="fbo.phone_secondary">{{ fbo.phone_secondary }}</span>
          </div>
        </template>
        <template v-slot:email="{ row: fbo }">
          <a :href="`mailto:${fbo.email}`" class="text-dark fw-semibold text-hover-primary" v-if="fbo.email">{{ fbo.email }}</a>
          <span v-else class="text-muted">No email</span>
        </template>
        <template v-slot:actions="{ row: fbo }">
          <a href="#" class="btn btn-sm btn-light btn-active-light-primary" data-kt-menu-trigger="click" data-kt-menu-placement="bottom-end">Actions <KTIcon icon-name="down" icon-class="fs-5 m-0" /></a>
          <div class="menu menu-sub menu-sub-dropdown menu-column menu-rounded menu-gray-600 menu-state-bg-light-primary fw-semibold fs-7 w-200px py-4" data-kt-menu="true">
            <div class="menu-item px-3"><a @click="handleView(fbo)" class="menu-link px-3">View Details</a></div>
            <div class="menu-item px-3"><a @click="handleEdit(fbo)" class="menu-link px-3">Edit FBO</a></div>
            <div class="separator mt-3 opacity-75"></div>
            <div class="menu-item px-3"><a @click="handleDelete(fbo)" class="menu-link px-3 text-danger">Delete</a></div>
          </div>
        </template>
      </KTDatatable>
    </div>
  </div>

  <!-- Create FBO Modal -->
  <CreateFboModal @fbo-created="onFboCreated" />
</template>

<script lang="ts">
import { defineComponent, ref, onMounted, onUnmounted } from "vue";
import { useRouter } from "vue-router";
import ApiService from "@/core/services/ApiService";
import KTDatatable from "@/components/kt-datatable/KTDataTable.vue";
import CreateFboModal from "@/components/modals/CreateFboModal.vue";
import type { Sort } from "@/components/kt-datatable/table-partials/models";
import arraySort from "array-sort";
import { MenuComponent } from "@/assets/ts/components";
import { Modal } from "bootstrap";
import Swal from "sweetalert2";
import { useToolbarStore } from "@/stores/toolbar";

export default defineComponent({
  name: "fbos-management",
  components: { KTDatatable, CreateFboModal },
  setup() {
    const router = useRouter();
    const toolbarStore = useToolbarStore();
    const fbos = ref([]);
    const loading = ref(false);
    const selectedIds = ref([]);
    const search = ref("");
    const totalItems = ref(0);
    const currentPage = ref(1);
    const pageSize = ref(25);

    const headerConfig = ref([
      { columnName: "FBO", columnLabel: "fbo", sortEnabled: true },
      { columnName: "Phone", columnLabel: "phone", sortEnabled: false },
      { columnName: "Email", columnLabel: "email", sortEnabled: false },
      { columnName: "Actions", columnLabel: "actions" }
    ]);

    const fetchFbos = async (page: number = 1, pageLimit: number = 25, searchQuery: string = '') => {
      try {
        loading.value = true;
        
        const params = new URLSearchParams();
        params.append('page', page.toString());
        params.append('page_size', pageLimit.toString());
        if (searchQuery.trim()) {
          params.append('search', searchQuery.trim());
        }
        
        const { data } = await ApiService.get(`/fbos/?${params}`);
        fbos.value = data.results || [];
        totalItems.value = data.count || 0;
        currentPage.value = page;
        pageSize.value = pageLimit;
        
        // Debug pagination info
        console.log('FBO Pagination:', {
          page,
          pageSize: pageLimit,
          totalItems: data.count,
          resultsCount: data.results?.length,
          totalPages: Math.ceil((data.count || 0) / pageLimit),
          currentPageState: currentPage.value,
          fbosLength: fbos.value.length
        });
        
      } catch (error) {
        console.error("Error fetching FBOs:", error);
      } finally {
        loading.value = false;
        setTimeout(() => MenuComponent.reinitialization(), 100);
      }
    };

    const handleCreate = () => {
      const modalElement = document.getElementById('kt_modal_create_fbo');
      if (modalElement) {
        const modal = new Modal(modalElement);
        modal.show();
      }
    };

    const handleEdit = (fbo) => {
      console.log('Edit clicked for FBO:', fbo);

      Swal.fire({
        title: `Edit FBO: ${fbo.name}`,
        html: `
          <div class="text-start">
            <div class="mb-3">
              <label class="form-label fw-bold">FBO Name <span class="text-danger">*</span></label>
              <input id="edit-name" class="form-control" value="${fbo.name || ''}" required>
            </div>
            <div class="mb-3">
              <label class="form-label fw-bold">Email</label>
              <input id="edit-email" type="email" class="form-control" value="${fbo.email || ''}">
            </div>
            <div class="row mb-3">
              <div class="col-6">
                <label class="form-label fw-bold">Primary Phone</label>
                <input id="edit-phone" class="form-control" value="${fbo.phone || ''}">
              </div>
              <div class="col-6">
                <label class="form-label fw-bold">Secondary Phone</label>
                <input id="edit-phone-secondary" class="form-control" value="${fbo.phone_secondary || ''}">
              </div>
            </div>
            <div class="row mb-3">
              <div class="col-6">
                <label class="form-label fw-bold">City</label>
                <input id="edit-city" class="form-control" value="${fbo.city || ''}">
              </div>
              <div class="col-6">
                <label class="form-label fw-bold">Country</label>
                <input id="edit-country" class="form-control" value="${fbo.country || ''}">
              </div>
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
            Swal.showValidationMessage('FBO Name is required');
            return false;
          }

          return {
            name: name,
            email: (document.getElementById('edit-email') as HTMLInputElement)?.value || '',
            phone: (document.getElementById('edit-phone') as HTMLInputElement)?.value || '',
            phone_secondary: (document.getElementById('edit-phone-secondary') as HTMLInputElement)?.value || '',
            city: (document.getElementById('edit-city') as HTMLInputElement)?.value || '',
            country: (document.getElementById('edit-country') as HTMLInputElement)?.value || ''
          };
        }
      }).then(async (result) => {
        if (result.isConfirmed && result.value) {
          console.log('Saving FBO with data:', result.value);

          try {
            await ApiService.put(`/fbos/${fbo.id}/`, result.value);

            Swal.fire({
              icon: 'success',
              title: 'Success!',
              text: 'FBO updated successfully.',
              timer: 2000,
              showConfirmButton: false
            });

            // Refresh the list
            await fetchFbos(currentPage.value, pageSize.value, search.value);
          } catch (error) {
            console.error('Error updating FBO:', error);
            Swal.fire({
              icon: 'error',
              title: 'Error',
              text: 'Failed to update FBO.'
            });
          }
        }
      });
    };

    const handleView = (fbo) => {
      const locationText = getLocationText(fbo);
      const phoneText = fbo.phone || 'No phone';
      const emailText = fbo.email || 'No email';
      
      Swal.fire({
        title: "FBO Details",
        html: `<div class="text-start">
          <p><strong>Name:</strong> ${fbo.name}</p>
          <p><strong>Location:</strong> ${locationText}</p>
          <p><strong>Phone:</strong> ${phoneText}</p>
          <p><strong>Email:</strong> ${emailText}</p>
        </div>`,
        icon: "info"
      });
    };


    const navigateToFboDetails = (fboId: string) => {
      router.push(`/admin/fbos/${fboId}`);
    };

    const handleDelete = async (fbo) => {
      const result = await Swal.fire({
        title: "Delete FBO",
        text: `Delete ${fbo.name}?`,
        icon: "warning",
        showCancelButton: true,
        confirmButtonText: "Yes, delete!"
      });
      
      if (result.isConfirmed) {
        try {
          await ApiService.delete(`/fbos/${fbo.id}/`);
          await fetchFbos(currentPage.value, pageSize.value, search.value);
          Swal.fire("Deleted!", "FBO deleted.", "success");
        } catch (error) {
          Swal.fire("Error!", "Failed to delete FBO.", "error");
        }
      }
    };

    const deleteFewFbos = () => {
      selectedIds.value.forEach(id => fbos.value = fbos.value.filter(f => f.id !== id));
      selectedIds.value = [];
    };

    const getLocationText = (fbo) => {
      // Priority: Show airport codes if available
      if (fbo.airport_codes && fbo.airport_codes.length > 0) {
        return fbo.airport_codes.join(', ');
      }
      
      // Fallback: Show city, state, country if no airport codes
      const parts = [fbo.city, fbo.state, fbo.country].filter(Boolean);
      return parts.length > 0 ? parts.join(', ') : 'Location not specified';
    };

    const sort = (sortData) => {
      // For server-side pagination, we should implement server-side sorting
      // For now, disable client-side sorting to avoid pagination conflicts
      console.log('Sort requested:', sortData);
      // TODO: Implement server-side sorting
    };

    const onItemSelect = (items) => selectedIds.value = items;

    const searchItems = () => {
      fetchFbos(1, pageSize.value, search.value);
    };

    const onItemsPerPageChange = (newPageSize: number) => {
      pageSize.value = newPageSize;
      fetchFbos(1, newPageSize, search.value);
    };

    const onPageChange = (page: number) => {
      console.log('Page change requested:', page);
      fetchFbos(page, pageSize.value, search.value);
    };

    const onFboCreated = () => {
      // Refresh the FBOs list after creating a new one
      fetchFbos(currentPage.value, pageSize.value, search.value);
    };

    onMounted(async () => {
      await fetchFbos();
      toolbarStore.setActions([{
        id: 'add-fbo',
        label: 'Add FBO',
        icon: 'plus',
        variant: 'primary',
        handler: handleCreate
      }]);
    });

    onUnmounted(() => toolbarStore.clearActions());

    return {
      search,
      searchItems,
      fbos,
      headerConfig,
      loading,
      totalItems,
      currentPage,
      pageSize,
      sort,
      onItemSelect,
      selectedIds,
      deleteFewFbos,
      onItemsPerPageChange,
      onPageChange,
      handleCreate,
      handleEdit,
      handleView,
      handleDelete,
      getLocationText,
      navigateToFboDetails,
      onFboCreated
    };
  },
});
</script>