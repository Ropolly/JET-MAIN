<template>
  <!--begin::Floating Create Trip Button-->
  <div class="position-fixed" style="top: 100px; right: 30px; z-index: 1000;">
    <button
      @click="showTripTypeModal"
      class="btn btn-primary btn-sm"
      :disabled="creatingTrip"
    >
      <span v-if="creatingTrip" class="spinner-border spinner-border-sm me-2"></span>
      <KTIcon icon-name="plus" icon-class="fs-6 me-1" />
      Create Trip
    </button>
  </div>
  <!--end::Floating Create Trip Button-->

  <!--begin::Trip Type Selection Modal-->
  <TripTypeSelectionModal
    :show="showTripTypeSelection"
    @close="onModalClose"
    @trip-type-selected="onTripTypeSelected"
  />
  <!--end::Trip Type Selection Modal-->

  <!--begin::Row-->
  <div class="row g-5 g-xl-10 mb-5 mb-xl-10">
    <!--begin::Col-->
    <div class="col-md-6 col-lg-6 col-xl-6 col-xxl-3 mb-md-5 mb-xl-10">
      <TripsWidget
        className="h-md-50 mb-5 mb-xl-10"
        bgColor="#1B84FF"
        :bgImage="getAssetPath('media/patterns/vector-1.png')"
      />

      <StatsWidget
        className="h-md-50 mb-5 mb-xl-10"
        title="Active Patients"
        :value="dashboardStore.stats?.patient_stats.active || 0"
        icon="ki-heart"
        iconColor="danger"
        :showProgress="true"
        :progressLabel="`${dashboardStore.stats?.patient_stats.total || 0} Total`"
        :progressValue="patientActivityPercentage"
      />
    </div>
    <!--end::Col-->

    <!--begin::Col-->
    <div class="col-md-6 col-lg-6 col-xl-6 col-xxl-3 mb-md-5 mb-xl-10">
      <QuotesWidget
        className="h-md-50 mb-5 mb-xl-10"
        bgColor="#F1416C"
        :bgImage="getAssetPath('media/patterns/vector-1.png')"
      />

      <StatsWidget
        className="h-md-50 mb-5 mb-xl-10"
        title="Aircraft Fleet"
        :value="dashboardStore.stats?.aircraft_stats.total || 0"
        icon="ki-airplane"
        iconColor="success"
      />
    </div>
    <!--end::Col-->

    <!--begin::Col-->
    <div class="col-xxl-6">
      <UpcomingTripsWidget className="h-md-100" />
    </div>
    <!--end::Col-->
  </div>
  <!--end::Row-->

  <!--begin::Row-->
  <div class="row gx-5 gx-xl-10">
    <!--begin::Col-->
    <div class="col-xxl-6 mb-5 mb-xl-10">
      <RecentActivityWidget className="h-xl-100" />
    </div>
    <!--end::Col-->

    <!--begin::Col-->
    <div class="col-xl-6 mb-5 mb-xl-10">
      <QuoteStatusChart className="h-xl-100" />
    </div>
    <!--end::Col-->
  </div>
  <!--end::Row-->

  <!--begin::Row-->
  <div class="row g-5 g-xl-10 mb-5 mb-xl-10">
    <!--begin::Col-->
    <div class="col-12">
      <RecentQuotesWidget className="h-xl-100" />
    </div>
    <!--end::Col-->
  </div>
  <!--end::Row-->
</template>

<script setup lang="ts">
import { getAssetPath } from "@/core/helpers/assets";
import { onMounted, computed, ref } from "vue";
import { useRouter } from "vue-router";
import { useDashboardStore } from "@/stores/dashboard";
import ApiService from "@/core/services/ApiService";
import Swal from "sweetalert2/dist/sweetalert2.js";

// Import our custom widgets
import TripsWidget from "@/components/dashboard-default-widgets/TripsWidget.vue";
import QuotesWidget from "@/components/dashboard-default-widgets/QuotesWidget.vue";
import UpcomingTripsWidget from "@/components/dashboard-default-widgets/UpcomingTripsWidget.vue";
import RecentQuotesWidget from "@/components/dashboard-default-widgets/RecentQuotesWidget.vue";
import RecentActivityWidget from "@/components/dashboard-default-widgets/RecentActivityWidget.vue";
import StatsWidget from "@/components/dashboard-default-widgets/StatsWidget.vue";

// Import placeholder chart components (we'll keep these)
import QuoteStatusChart from "@/components/dashboard-default-widgets/QuoteStatusChart.vue";

// Import modal components
import TripTypeSelectionModal from "@/components/modals/TripTypeSelectionModal.vue";

const router = useRouter();
const dashboardStore = useDashboardStore();
const creatingTrip = ref(false);
const showTripTypeSelection = ref(false);

const patientActivityPercentage = computed(() => {
  const stats = dashboardStore.stats;
  if (!stats?.patient_stats) return 0;

  const { active, total } = stats.patient_stats;
  return total > 0 ? Math.round((active / total) * 100) : 0;
});

// Show trip type selection modal
const showTripTypeModal = async () => {
  showTripTypeSelection.value = true;
  // Use showModal helper to show the modal
  const modalElement = document.getElementById('kt_modal_select_trip_type');
  if (modalElement) {
    const { showModal } = await import('@/core/helpers/modal');
    showModal(modalElement);
  }
};

// Handle modal close
const onModalClose = () => {
  showTripTypeSelection.value = false;
};

// Create trip with selected type
const onTripTypeSelected = async (tripType: string) => {
  if (creatingTrip.value) return;

  creatingTrip.value = true;
  showTripTypeSelection.value = false;

  // Ensure modal overlay is removed
  const modalElement = document.getElementById('kt_modal_select_trip_type');
  if (modalElement) {
    const { hideModal } = await import('@/core/helpers/modal');
    hideModal(modalElement);
  }

  // Clean up any lingering modal backdrops and restore body scroll
  const backdrops = document.querySelectorAll('.modal-backdrop');
  backdrops.forEach(backdrop => backdrop.remove());
  document.body.classList.remove('modal-open');
  document.body.style.overflow = '';
  document.body.style.paddingRight = '';

  try {
    // Create a unique draft trip number using timestamp
    const timestamp = Date.now();
    const draftNumber = `DRAFT-${timestamp}`;

    // Create a basic trip with selected type
    const tripData = {
      type: tripType,
      status: 'pending',
      trip_number: draftNumber // Unique draft number that can be updated later
    };

    console.log('Sending trip data:', tripData);
    const response = await ApiService.post('/trips/', tripData);
    console.log('Trip created successfully:', response.data);

    // Navigate to the complete trip view
    if (response.data?.id) {
      await router.push(`/admin/trips/${response.data.id}/complete`);
    } else {
      throw new Error('Trip created but no ID returned');
    }

  } catch (error) {
    console.error('Error creating trip:', error);

    let errorMessage = "Failed to create trip. Please try again.";
    if (error.response?.data) {
      if (typeof error.response.data === 'object') {
        errorMessage = JSON.stringify(error.response.data);
      } else {
        errorMessage = error.response.data.detail || error.response.data.message || error.response.data.toString();
      }
    } else if (error.message) {
      errorMessage = error.message;
    }

    await Swal.fire({
      title: "Error",
      text: errorMessage,
      icon: "error",
      confirmButtonText: "OK"
    });
  } finally {
    creatingTrip.value = false;
  }
};

// Fetch dashboard data on component mount
onMounted(async () => {
  try {
    await dashboardStore.fetchStats();
  } catch (error) {
    console.error("Failed to load dashboard data:", error);
  }
});
</script>