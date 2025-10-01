<template>
  <MenuComponent menu-selector="#kt-search-menu">
    <template v-slot:toggle>
      <!--begin::Search-->
      <div
        id="kt_header_search"
        class="header-search d-flex align-items-stretch"
        data-kt-menu-target="#kt-search-menu"
        data-kt-menu-trigger="click"
        data-kt-menu-attach="parent"
        data-kt-menu-placement="bottom-end"
        data-kt-menu-flip="bottom"
      >
        <!--begin::Search toggle-->
        <div class="d-flex align-items-center" id="kt_header_search_toggle">
          <div
            class="btn btn-icon btn-custom btn-icon-muted btn-active-light btn-active-color-primary w-35px h-35px"
          >
            <KTIcon icon-name="magnifier" icon-class="fs-2" />
          </div>
        </div>
        <!--end::Search toggle-->
      </div>
      <!--end::Search-->
    </template>
    <template v-slot:content>
      <!--begin::Menu-->
      <div
        class="menu menu-sub menu-sub-dropdown menu-column p-7 w-325px w-md-375px"
        data-kt-menu="true"
        id="kt-search-menu"
      >
        <!--begin::Wrapper-->
        <div>
          <!--begin::Form-->
          <form class="w-100 position-relative mb-3" autocomplete="off">
            <!--begin::Icon-->
            <KTIcon
              icon-name="magnifier"
              icon-class="fs-2 fs-lg-1 text-gray-500 position-absolute top-50 translate-middle-y ms-0"
            />
            <!--end::Icon-->

            <!--begin::Input-->
            <input
              ref="inputRef"
              v-model="search"
              @input="searching"
              type="text"
              class="form-control form-control-flush ps-10"
              name="search"
              placeholder="Search..."
            />
            <!--end::Input-->

            <!--begin::Spinner-->
            <span
              v-if="loading"
              class="position-absolute top-50 end-0 translate-middle-y lh-0 me-1"
            >
              <span
                class="spinner-border h-15px w-15px align-middle text-gray-500"
              ></span>
            </span>
            <!--end::Spinner-->

            <!--begin::Reset-->
            <span
              v-show="search.length && !loading"
              @click="reset()"
              class="btn btn-flush btn-active-color-primary position-absolute top-50 end-0 translate-middle-y lh-0"
            >
              <KTIcon icon-name="cross" icon-class="fs-2 fs-lg-1 me-0" />
            </span>
            <!--end::Reset-->
          </form>
          <!--end::Form-->

          <!--begin::Separator-->
          <div class="separator border-gray-200 mb-6"></div>
          <!--end::Separator-->
          <Results v-if="state === 'results'"></Results>
          <PartialMain v-else-if="state === 'main'"></PartialMain>
          <Empty v-else-if="state === 'empty'"></Empty>
        </div>
        <!--end::Wrapper-->
      </div>
      <!--end::Menu-->
    </template>
  </MenuComponent>
</template>

<script lang="ts">
import { getAssetPath } from "@/core/helpers/assets";
import { defineComponent, ref, provide } from "vue";
import Results from "@/layouts/default-layout/components/search/partials/Results.vue";
import PartialMain from "@/layouts/default-layout/components/search/partials/Main.vue";
import Empty from "@/layouts/default-layout/components/search/partials/Empty.vue";
import MenuComponent from "@/components/menu/MenuComponent.vue";
import ApiService from "@/core/services/ApiService";

interface Trip {
  trip_id: string;
  trip_number: string;
  trip_type: string;
  trip_status: string;
  patient_name?: string;
  route?: string;
}

const RECENT_SEARCHES_KEY = "jet_icu_recent_searches";
const MAX_RECENT_SEARCHES = 10;

export default defineComponent({
  name: "kt-search",
  components: {
    Results,
    PartialMain,
    Empty,
    MenuComponent,
  },
  setup() {
    const search = ref<string>("");
    const state = ref<"main" | "empty" | "results">("main");
    const loading = ref<boolean>(false);
    const inputRef = ref<HTMLInputElement | null>(null);
    const searchResults = ref<Trip[]>([]);
    const searchDebounceTimer = ref<number | null>(null);

    // Provide search results and recent searches to child components
    provide("searchResults", searchResults);
    provide("loading", loading);

    const saveRecentSearch = (trip: Trip) => {
      try {
        const recent = JSON.parse(localStorage.getItem(RECENT_SEARCHES_KEY) || "[]");

        // Remove if already exists (to move to top)
        const filtered = recent.filter((t: Trip) => t.trip_id !== trip.trip_id);

        // Add to beginning
        filtered.unshift({
          trip_id: trip.trip_id,
          trip_number: trip.trip_number,
          patient_name: trip.patient_name,
          route: trip.route,
          trip_type: trip.trip_type,
          trip_status: trip.trip_status
        });

        // Keep only last MAX_RECENT_SEARCHES
        const trimmed = filtered.slice(0, MAX_RECENT_SEARCHES);

        localStorage.setItem(RECENT_SEARCHES_KEY, JSON.stringify(trimmed));
      } catch (error) {
        console.error("Error saving recent search:", error);
      }
    };

    const performSearch = async (searchTerm: string) => {
      if (searchTerm.trim().length < 2) {
        state.value = "main";
        searchResults.value = [];
        return;
      }

      loading.value = true;

      try {
        const params = new URLSearchParams();
        params.append("search", searchTerm.trim());
        params.append("page_size", "10"); // Limit to 10 results for dropdown

        const url = `/workflows?${params}`;
        const { data } = await ApiService.get(url);

        searchResults.value = data.results || [];

        if (searchResults.value.length === 0) {
          state.value = "empty";
        } else {
          state.value = "results";
        }
      } catch (error) {
        console.error("Search error:", error);
        searchResults.value = [];
        state.value = "empty";
      } finally {
        loading.value = false;
      }
    };

    const searching = (e: Event) => {
      const target = e.target as HTMLInputElement;

      // Clear previous timer
      if (searchDebounceTimer.value) {
        clearTimeout(searchDebounceTimer.value);
      }

      // Show loading state immediately
      if (target.value.trim().length >= 2) {
        loading.value = true;
      }

      // Debounce search
      searchDebounceTimer.value = setTimeout(() => {
        performSearch(target.value);
      }, 300) as unknown as number;
    };

    const reset = () => {
      search.value = "";
      state.value = "main";
      searchResults.value = [];

      if (searchDebounceTimer.value) {
        clearTimeout(searchDebounceTimer.value);
      }
    };

    // Expose saveRecentSearch to child components
    provide("saveRecentSearch", saveRecentSearch);

    return {
      search,
      state,
      loading,
      searching,
      reset,
      inputRef,
      getAssetPath,
      searchResults,
    };
  },
});
</script>
