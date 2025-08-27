<template>
  <div class="card">
    <!--begin::Card header-->
    <div class="card-header border-0 pt-5">
      <h3 class="card-title align-items-start flex-column">
        <span class="card-label fw-bold fs-3 mb-1">Maintenance Records</span>
        <span class="text-muted mt-1 fw-semibold fs-7">Maintenance history and upcoming inspections</span>
      </h3>
      <div class="card-toolbar">
        <button class="btn btn-sm btn-light-primary">
          <KTIcon icon-name="plus" icon-class="fs-3" />
          Add Maintenance
        </button>
      </div>
    </div>
    <!--end::Card header-->

    <!--begin::Card body-->
    <div class="card-body py-3">
      <div v-if="loading" class="d-flex justify-content-center">
        <div class="spinner-border" role="status">
          <span class="visually-hidden">Loading...</span>
        </div>
      </div>

      <div v-else>
        <!--begin::Upcoming Maintenance-->
        <div class="mb-10">
          <h4 class="fw-bold text-dark mb-5">Upcoming Maintenance</h4>
          <div class="row">
            <div class="col-md-4 mb-5">
              <div class="card card-custom">
                <div class="card-body">
                  <div class="d-flex align-items-center">
                    <KTIcon icon-name="wrench" icon-class="fs-2x text-warning me-4" />
                    <div>
                      <div class="fw-bold text-dark fs-6">Annual Inspection</div>
                      <div class="text-muted fs-7">Due: March 15, 2024</div>
                      <div class="text-warning fs-8">Due in 45 days</div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
            
            <div class="col-md-4 mb-5">
              <div class="card card-custom">
                <div class="card-body">
                  <div class="d-flex align-items-center">
                    <KTIcon icon-name="oil" icon-class="fs-2x text-primary me-4" />
                    <div>
                      <div class="fw-bold text-dark fs-6">Oil Change</div>
                      <div class="text-muted fs-7">Due: Feb 1, 2024</div>
                      <div class="text-success fs-8">Due in 10 days</div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
            
            <div class="col-md-4 mb-5">
              <div class="card card-custom">
                <div class="card-body">
                  <div class="d-flex align-items-center">
                    <KTIcon icon-name="gear" icon-class="fs-2x text-info me-4" />
                    <div>
                      <div class="fw-bold text-dark fs-6">100-Hour Inspection</div>
                      <div class="text-muted fs-7">Due: Jan 30, 2024</div>
                      <div class="text-success fs-8">Due in 8 days</div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
        <!--end::Upcoming Maintenance-->

        <!--begin::Maintenance History-->
        <div class="mb-10">
          <h4 class="fw-bold text-dark mb-5">Maintenance History</h4>
          
          <div v-if="maintenanceRecords && maintenanceRecords.length > 0">
            <!--begin::Table container-->
            <div class="table-responsive">
              <!--begin::Table-->
              <table class="table table-row-dashed table-row-gray-300 align-middle gs-0 gy-4">
                <!--begin::Table head-->
                <thead>
                  <tr class="fw-bold text-muted">
                    <th class="min-w-150px">Date</th>
                    <th class="min-w-140px">Type</th>
                    <th class="min-w-120px">Description</th>
                    <th class="min-w-100px">Hours</th>
                    <th class="min-w-100px">Cost</th>
                    <th class="min-w-100px">Status</th>
                    <th class="min-w-100px text-end">Actions</th>
                  </tr>
                </thead>
                <!--end::Table head-->
                <!--begin::Table body-->
                <tbody>
                  <tr v-for="record in maintenanceRecords" :key="record.id">
                    <td>
                      <div class="text-dark fw-bold fs-6">{{ formatDate(record.date) }}</div>
                    </td>
                    <td>
                      <div class="text-dark fw-bold fs-6">{{ record.type }}</div>
                    </td>
                    <td>
                      <div class="text-dark fw-bold fs-6">{{ record.description }}</div>
                    </td>
                    <td>
                      <div class="text-dark fw-bold fs-6">{{ record.aircraft_hours }}h</div>
                    </td>
                    <td>
                      <div class="text-dark fw-bold fs-6">${{ record.cost }}</div>
                    </td>
                    <td>
                      <span :class="`badge badge-light-${getMaintenanceStatusColor(record.status)}`">
                        {{ record.status }}
                      </span>
                    </td>
                    <td>
                      <div class="d-flex justify-content-end flex-shrink-0">
                        <a href="#" class="btn btn-icon btn-bg-light btn-active-color-primary btn-sm me-1">
                          <KTIcon icon-name="eye" icon-class="fs-3" />
                        </a>
                        <a href="#" class="btn btn-icon btn-bg-light btn-active-color-primary btn-sm">
                          <KTIcon icon-name="pencil" icon-class="fs-3" />
                        </a>
                      </div>
                    </td>
                  </tr>
                </tbody>
                <!--end::Table body-->
              </table>
              <!--end::Table-->
            </div>
            <!--end::Table container-->
          </div>
          
          <div v-else class="text-center py-10">
            <div class="text-gray-400">No maintenance records found</div>
            <button class="btn btn-primary mt-3">
              Add First Record
            </button>
          </div>
        </div>
        <!--end::Maintenance History-->
      </div>
    </div>
    <!--end::Card body-->
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, watch } from "vue";
import ApiService from "@/core/services/ApiService";

export default defineComponent({
  name: "AircraftMaintenance",
  props: {
    aircraft: {
      type: Object,
      default: null,
    },
    loading: {
      type: Boolean,
      default: false,
    },
  },
  setup(props) {
    const maintenanceRecords = ref<any[]>([]);
    const maintenanceLoading = ref(false);

    const fetchMaintenanceRecords = async () => {
      if (!props.aircraft?.id) return;
      
      try {
        maintenanceLoading.value = true;
        // This would be the actual API call when maintenance endpoint exists
        // const response = await ApiService.get(`/maintenance/?aircraft=${props.aircraft.id}`);
        // maintenanceRecords.value = response.data.results || response.data || [];
        
        // For now, use mock data
        maintenanceRecords.value = [
          {
            id: 1,
            date: '2024-01-15',
            type: 'Annual Inspection',
            description: 'Complete annual inspection and certification',
            aircraft_hours: 1250,
            cost: 3500,
            status: 'Completed'
          },
          {
            id: 2,
            date: '2024-01-10',
            type: 'Oil Change',
            description: 'Engine oil and filter replacement',
            aircraft_hours: 1248,
            cost: 150,
            status: 'Completed'
          },
          {
            id: 3,
            date: '2023-12-20',
            type: '100-Hour Inspection',
            description: '100-hour inspection and maintenance',
            aircraft_hours: 1200,
            cost: 1200,
            status: 'Completed'
          }
        ];
      } catch (error) {
        console.error("Error fetching maintenance records:", error);
        maintenanceRecords.value = [];
      } finally {
        maintenanceLoading.value = false;
      }
    };

    const formatDate = (dateString?: string): string => {
      if (!dateString) return 'N/A';
      return new Date(dateString).toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
      });
    };

    const getMaintenanceStatusColor = (status?: string): string => {
      switch (status?.toLowerCase()) {
        case 'completed': return 'success';
        case 'in_progress': return 'primary';
        case 'scheduled': return 'warning';
        case 'overdue': return 'danger';
        default: return 'secondary';
      }
    };

    watch(() => props.aircraft, fetchMaintenanceRecords, { immediate: true });

    return {
      maintenanceRecords,
      maintenanceLoading,
      formatDate,
      getMaintenanceStatusColor,
    };
  },
});
</script>