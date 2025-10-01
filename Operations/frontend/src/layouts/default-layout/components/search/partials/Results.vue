<template>
  <div>
    <!--begin::Items-->
    <div class="scroll-y mh-200px mh-lg-325px">
      <!--begin::Loading-->
      <div v-if="loading" class="text-center py-10">
        <span class="spinner-border spinner-border-lg text-primary"></span>
        <div class="text-muted mt-3">Searching trips...</div>
      </div>
      <!--end::Loading-->

      <!--begin::Results-->
      <div v-else-if="searchResults && searchResults.length > 0">
        <!--begin::Category title-->
        <h3 class="fs-5 text-muted m-0 pb-5">Trips</h3>
        <!--end::Category title-->

        <!--begin::Item-->
        <router-link
          v-for="trip in searchResults"
          :key="trip.trip_id"
          :to="`/admin/trips/${trip.trip_id}/complete`"
          @click="handleTripClick(trip)"
          class="d-flex text-gray-900 text-hover-primary align-items-center mb-5 text-decoration-none"
        >
          <!--begin::Symbol-->
          <div class="symbol symbol-40px symbol-circle me-4">
            <span class="symbol-label bg-light">
              <KTIcon icon-name="airplane" icon-class="fs-2 text-primary" />
            </span>
          </div>
          <!--end::Symbol-->

          <!--begin::Content-->
          <div class="d-flex flex-column flex-grow-1">
            <!--begin::Title row-->
            <div class="d-flex align-items-center justify-content-between mb-1">
              <span class="fs-6 fw-semibold">{{ trip.trip_number || 'N/A' }}</span>
              <span
                class="badge badge-sm ms-2"
                :class="{
                  'badge-light-primary': trip.trip_status === 'pending',
                  'badge-light-success': trip.trip_status === 'active',
                  'badge-light-info': trip.trip_status === 'completed',
                  'badge-light-danger': trip.trip_status === 'cancelled',
                }"
              >
                {{ trip.trip_status }}
              </span>
            </div>
            <!--end::Title row-->

            <!--begin::Patient-->
            <span class="fs-7 fw-semibold text-muted mb-1">
              Patient: {{ trip.patient_name || 'No patient' }}
            </span>
            <!--end::Patient-->

            <!--begin::Route-->
            <span class="fs-7 text-gray-600">
              {{ trip.route || 'No route info' }}
            </span>
            <!--end::Route-->
          </div>
          <!--end::Content-->
        </router-link>
        <!--end::Item-->
      </div>
      <!--end::Results-->

      <!--begin::No results-->
      <div v-else class="text-center py-10">
        <KTIcon icon-name="file-search" icon-class="fs-5x text-muted mb-4" />
        <div class="fs-5 fw-semibold text-gray-700 mb-2">No trips found</div>
        <div class="fs-7 text-muted">
          Try searching by trip number, patient name, customer name, or airport
        </div>
      </div>
      <!--end::No results-->
    </div>
    <!--end::Items-->
  </div>
</template>

<script lang="ts">
import { defineComponent, inject } from "vue";
import type { Ref } from "vue";

interface Trip {
  trip_id: string;
  trip_number: string;
  trip_type: string;
  trip_status: string;
  patient_name?: string;
  route?: string;
}

export default defineComponent({
  name: "kt-results",
  components: {},
  setup() {
    const searchResults = inject<Ref<Trip[]>>("searchResults");
    const loading = inject<Ref<boolean>>("loading");
    const saveRecentSearch = inject<(trip: Trip) => void>("saveRecentSearch");

    const handleTripClick = (trip: Trip) => {
      if (saveRecentSearch) {
        saveRecentSearch(trip);
      }
    };

    return {
      searchResults,
      loading,
      handleTripClick,
    };
  },
});
</script>
