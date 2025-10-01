<template>
  <div class="mb-4">
    <!--begin::Heading-->
    <div class="d-flex flex-stack fw-semibold mb-4">
      <!--begin::Label-->
      <span class="text-muted fs-6 me-2">Recently Searched:</span>
      <!--end::Label-->

      <!--begin::Clear button-->
      <button
        v-if="recentSearches.length > 0"
        @click="clearRecentSearches"
        class="btn btn-sm btn-light-danger"
      >
        Clear History
      </button>
      <!--end::Clear button-->
    </div>
    <!--end::Heading-->

    <!--begin::Items-->
    <div class="scroll-y mh-200px mh-lg-325px">
      <!--begin::No recent searches-->
      <div v-if="recentSearches.length === 0" class="text-center py-10">
        <KTIcon icon-name="time" icon-class="fs-5x text-muted mb-4" />
        <div class="fs-6 fw-semibold text-gray-600 mb-2">No recent searches</div>
        <div class="fs-7 text-muted">
          Start searching for trips to see your history here
        </div>
      </div>
      <!--end::No recent searches-->

      <!--begin::Item-->
      <router-link
        v-for="trip in recentSearches"
        :key="trip.trip_id"
        :to="`/admin/trips/${trip.trip_id}/complete`"
        class="d-flex align-items-center mb-5 text-decoration-none text-gray-800 text-hover-primary"
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
          <span class="fs-7 text-muted">
            {{ trip.patient_name || 'No patient' }}
          </span>
          <!--end::Patient-->
        </div>
        <!--end::Content-->
      </router-link>
      <!--end::Item-->
    </div>
    <!--end::Items-->
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, onMounted } from "vue";

interface Trip {
  trip_id: string;
  trip_number: string;
  trip_type: string;
  trip_status: string;
  patient_name?: string;
  route?: string;
}

const RECENT_SEARCHES_KEY = "jet_icu_recent_searches";

export default defineComponent({
  name: "kt-main",
  components: {},
  setup() {
    const recentSearches = ref<Trip[]>([]);

    const loadRecentSearches = () => {
      try {
        const stored = localStorage.getItem(RECENT_SEARCHES_KEY);
        if (stored) {
          recentSearches.value = JSON.parse(stored);
        }
      } catch (error) {
        console.error("Error loading recent searches:", error);
        recentSearches.value = [];
      }
    };

    const clearRecentSearches = () => {
      recentSearches.value = [];
      localStorage.removeItem(RECENT_SEARCHES_KEY);
    };

    onMounted(() => {
      loadRecentSearches();
    });

    return {
      recentSearches,
      clearRecentSearches,
    };
  },
});
</script>
