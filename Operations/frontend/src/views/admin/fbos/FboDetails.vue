<template>
  <!--begin::Layout-->
  <div class="d-flex flex-column flex-xl-row">
    <!--begin::Sidebar-->
    <div class="flex-column flex-lg-row-auto w-100 w-xl-350px mb-10">
      <!--begin::Card-->
      <div class="card mb-5 mb-xl-8">
        <!--begin::Card body-->
        <div class="card-body pt-15">
          <!--begin::Summary-->
          <div class="d-flex flex-center flex-column mb-5">
            <!--begin::Avatar-->
            <div class="symbol symbol-100px symbol-circle mb-7">
              <div class="symbol-label bg-light-info">
                <i class="ki-duotone ki-home-2 fs-2x text-info">
                  <span class="path1"></span>
                  <span class="path2"></span>
                </i>
              </div>
            </div>
            <!--end::Avatar-->

            <!--begin::Name-->
            <a
              href="#"
              class="fs-3 text-gray-800 text-hover-primary fw-bold mb-1"
            >
              {{ getFboName() }}
            </a>
            <!--end::Name-->

            <!--begin::Position-->
            <div class="fs-5 fw-semibold text-muted mb-6">{{ getFboLocation() }}</div>
            <!--end::Position-->

            <!--begin::Airport Badges-->
            <div class="d-flex flex-wrap justify-content-center mb-6" v-if="fbo?.airport_codes && fbo.airport_codes.length > 0">
              <span
                v-for="code in fbo.airport_codes"
                :key="code"
                class="badge badge-light-primary fs-8 fw-bold me-2 mb-2"
              >
                <i class="ki-duotone ki-airplane fs-7 me-1">
                  <span class="path1"></span>
                  <span class="path2"></span>
                </i>
                {{ code }}
              </span>
            </div>
            <!--end::Airport Badges-->

            <!--begin::Info-->
            <div class="d-flex flex-wrap flex-center">
              <!--begin::Stats-->
              <div
                class="border border-gray-300 border-dashed rounded py-3 px-3 mb-3"
              >
                <div class="fs-4 fw-bold text-gray-700">
                  <span class="w-75px">{{ getTotalTrips() }}</span>
                  <KTIcon icon-name="arrow-up" icon-class="fs-3 text-success" />
                </div>
                <div class="fw-semibold text-muted">Total Trips</div>
              </div>
              <!--end::Stats-->

              <!--begin::Stats-->
              <div
                class="border border-gray-300 border-dashed rounded py-3 px-3 mx-4 mb-3"
              >
                <div class="fs-4 fw-bold text-gray-700">
                  <span class="w-50px">{{ getStatus() }}</span>
                </div>
                <div class="fw-semibold text-muted">Status</div>
              </div>
              <!--end::Stats-->

              <!--begin::Stats-->
              <div
                class="border border-gray-300 border-dashed rounded py-3 px-3 mb-3"
              >
                <div class="fs-4 fw-bold text-gray-700">
                  <span class="w-75px">{{ getLastServiceDate() }}</span>
                </div>
                <div class="fw-semibold text-muted">Last Service</div>
              </div>
              <!--end::Stats-->
            </div>
            <!--end::Info-->
          </div>
          <!--end::Summary-->

          <!--begin::Details toggle-->
          <div class="d-flex flex-stack fs-4 py-3">
            <div
              class="fw-bold rotate collapsible"
              data-bs-toggle="collapse"
              href="#kt_fbo_view_details"
              role="button"
              aria-expanded="false"
              aria-controls="kt_fbo_view_details"
            >
              Details
              <span class="ms-2 rotate-180">
                <KTIcon icon-name="down" icon-class="fs-3" />
              </span>
            </div>

            <span
              data-bs-toggle="tooltip"
              data-bs-trigger="hover"
              title="Edit FBO details"
            >
              <button class="btn btn-sm btn-light-primary" @click="handleEdit">
                Edit
              </button>
            </span>
          </div>
          <!--end::Details toggle-->

          <div class="separator separator-dashed my-3"></div>

          <!--begin::Details content-->
          <div id="kt_fbo_view_details" class="collapse show">
            <div class="py-5 fs-6">              
              <!--begin::Details item-->
              <div class="fw-bold mt-5">FBO ID</div>
              <div class="text-gray-600">{{ fbo?.id || '-' }}</div>
              <!--end::Details item-->
              
              <!--begin::Details item-->
              <div class="fw-bold mt-5">Primary Phone</div>
              <div class="text-gray-600">
                <a :href="`tel:${fbo?.phone}`" class="text-gray-600 text-hover-primary" v-if="fbo?.phone">
                  {{ fbo.phone }}
                </a>
                <span v-else>Not provided</span>
              </div>
              <!--end::Details item-->
              
              <!--begin::Details item-->
              <div class="fw-bold mt-5">Secondary Phone</div>
              <div class="text-gray-600">
                <a :href="`tel:${fbo?.phone_secondary}`" class="text-gray-600 text-hover-primary" v-if="fbo?.phone_secondary">
                  {{ fbo.phone_secondary }}
                </a>
                <span v-else>Not provided</span>
              </div>
              <!--end::Details item-->
              
              <!--begin::Details item-->
              <div class="fw-bold mt-5">Email</div>
              <div class="text-gray-600">
                <a :href="`mailto:${fbo?.email}`" class="text-gray-600 text-hover-primary" v-if="fbo?.email">
                  {{ fbo.email }}
                </a>
                <span v-else>Not provided</span>
              </div>
              <!--end::Details item-->
              
              <!--begin::Details item-->
              <div class="fw-bold mt-5">Full Address</div>
              <div class="text-gray-600">{{ getFullAddress() }}</div>
              <!--end::Details item-->
              
              <!--begin::Details item-->
              <div class="fw-bold mt-5">Notes</div>
              <div class="text-gray-600">{{ fbo?.notes || 'No notes' }}</div>
              <!--end::Details item-->
              
              <!--begin::Details item-->
              <div class="fw-bold mt-5">Created</div>
              <div class="text-gray-600">{{ formatDate(fbo?.created_on) }}</div>
              <!--end::Details item-->
            </div>
          </div>
          <!--end::Details content-->
        </div>
        <!--end::Card body-->
      </div>
      <!--end::Card-->

      <!--begin::Connected Airports-->
      <div class="card mb-5 mb-xl-8" v-if="fbo?.airport_names && fbo.airport_names.length > 0">
        <!--begin::Card header-->
        <div class="card-header border-0">
          <div class="card-title">
            <h3 class="fw-bold m-0">Airports Served</h3>
          </div>
        </div>
        <!--end::Card header-->

        <!--begin::Card body-->
        <div class="card-body pt-2">
          <div class="py-2">
            <div
              v-for="(airport, index) in fbo.airport_names"
              :key="index"
              class="d-flex align-items-center py-2"
            >
              <div class="symbol symbol-35px me-3">
                <div class="symbol-label bg-light-primary">
                  <i class="ki-duotone ki-airplane fs-6 text-primary">
                    <span class="path1"></span>
                    <span class="path2"></span>
                  </i>
                </div>
              </div>
              <div class="d-flex flex-column flex-grow-1">
                <span class="fw-bold text-gray-800">{{ fbo.airport_codes[index] }}</span>
                <span class="text-muted fs-7">{{ airport }}</span>
              </div>
            </div>
          </div>
        </div>
        <!--end::Card body-->
      </div>
      <!--end::Connected Airports-->
    </div>
    <!--end::Sidebar-->

    <!--begin::Content-->
    <div class="flex-lg-row-fluid ms-lg-15">
      <!--begin:::Tabs-->
      <ul
        class="nav nav-custom nav-tabs nav-line-tabs nav-line-tabs-2x border-0 fs-4 fw-semibold mb-8"
      >
        <!--begin:::Tab item-->
        <li class="nav-item">
          <a
            class="nav-link text-active-primary pb-4 active"
            data-bs-toggle="tab"
            href="#kt_fbo_view_overview_tab"
          >
            Overview
          </a>
        </li>
        <!--end:::Tab item-->

        <!--begin:::Tab item-->
        <li class="nav-item">
          <a
            class="nav-link text-active-primary pb-4"
            data-bs-toggle="tab"
            href="#kt_fbo_view_trips_tab"
          >
            Trip History
          </a>
        </li>
        <!--end:::Tab item-->

        <!--begin:::Tab item-->
        <li class="nav-item">
          <a
            class="nav-link text-active-primary pb-4"
            data-bs-toggle="tab"
            href="#kt_fbo_view_contacts_tab"
          >
            Contacts
          </a>
        </li>
        <!--end:::Tab item-->
      </ul>
      <!--end:::Tabs-->

      <!--begin:::Tab content-->
      <div class="tab-content" id="myTabContent">
        <!--begin:::Tab pane-->
        <div
          class="tab-pane fade show active"
          id="kt_fbo_view_overview_tab"
          role="tabpanel"
        >
          <!--begin::Card-->
          <div class="card">
            <!--begin::Card header-->
            <div class="card-header border-0 pt-6">
              <div class="card-title">
                <h3 class="fw-bold m-0">Services & Amenities</h3>
              </div>
            </div>
            <!--end::Card header-->

            <!--begin::Card body-->
            <div class="card-body pt-2">
              <div class="py-5">
                <div class="notice d-flex bg-light-info rounded border-info border border-dashed p-6">
                  <i class="ki-duotone ki-information fs-2tx text-info me-4">
                    <span class="path1"></span>
                    <span class="path2"></span>
                    <span class="path3"></span>
                  </i>
                  <div class="d-flex flex-stack flex-grow-1">
                    <div class="fw-semibold">
                      <h4 class="text-gray-900 fw-bold">FBO Services</h4>
                      <div class="fs-6 text-gray-700">
                        Standard FBO services include fuel services, hangar space, ground support equipment, 
                        passenger amenities, crew facilities, and aircraft maintenance coordination.
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
            <!--end::Card body-->
          </div>
          <!--end::Card-->
        </div>
        <!--end:::Tab pane-->

        <!--begin:::Tab pane-->
        <div
          class="tab-pane fade"
          id="kt_fbo_view_trips_tab"
          role="tabpanel"
        >
          <!--begin::Card-->
          <div class="card">
            <!--begin::Card header-->
            <div class="card-header border-0 pt-6">
              <div class="card-title">
                <h3 class="fw-bold m-0">Recent Trips</h3>
              </div>
            </div>
            <!--end::Card header-->

            <!--begin::Card body-->
            <div class="card-body pt-2">
              <div v-if="recentTrips.length === 0" class="text-center py-10">
                <div class="text-muted fs-6">No trips found for this FBO</div>
              </div>
              <div v-else>
                <div
                  v-for="trip in recentTrips"
                  :key="trip.id"
                  class="d-flex align-items-center border-bottom border-gray-300 pb-4 mb-4"
                >
                  <div class="symbol symbol-50px me-5">
                    <div class="symbol-label bg-light-primary">
                      <i class="ki-duotone ki-airplane fs-2x text-primary">
                        <span class="path1"></span>
                        <span class="path2"></span>
                      </i>
                    </div>
                  </div>
                  <div class="flex-grow-1">
                    <a
                      @click.prevent="navigateToTrip(trip.id)"
                      href="#"
                      class="text-gray-800 text-hover-primary fs-6 fw-bold"
                    >
                      {{ trip.trip_number }}
                    </a>
                    <div class="text-muted fs-7">
                      Status: {{ trip.status || 'Unknown' }}
                    </div>
                  </div>
                  <div class="text-end">
                    <span class="text-muted fs-7">{{ formatDate(trip.created_on) }}</span>
                  </div>
                </div>
              </div>
            </div>
            <!--end::Card body-->
          </div>
          <!--end::Card-->
        </div>
        <!--end:::Tab pane-->

        <!--begin:::Tab pane-->
        <div
          class="tab-pane fade"
          id="kt_fbo_view_contacts_tab"
          role="tabpanel"
        >
          <!--begin::Card-->
          <div class="card">
            <!--begin::Card header-->
            <div class="card-header border-0 pt-6">
              <div class="card-title">
                <h3 class="fw-bold m-0">Associated Contacts</h3>
              </div>
            </div>
            <!--end::Card header-->

            <!--begin::Card body-->
            <div class="card-body pt-2">
              <div v-if="!fbo?.contacts || fbo.contacts.length === 0" class="text-center py-10">
                <div class="text-muted fs-6">No contacts associated with this FBO</div>
              </div>
              <div v-else>
                <div
                  v-for="contact in fbo.contacts"
                  :key="contact"
                  class="d-flex align-items-center border-bottom border-gray-300 pb-4 mb-4"
                >
                  <div class="symbol symbol-50px me-5">
                    <div class="symbol-label bg-light-success">
                      <i class="ki-duotone ki-profile-user fs-2x text-success">
                        <span class="path1"></span>
                        <span class="path2"></span>
                        <span class="path3"></span>
                        <span class="path4"></span>
                      </i>
                    </div>
                  </div>
                  <div class="flex-grow-1">
                    <span class="text-gray-800 fs-6 fw-bold">Contact ID: {{ contact }}</span>
                    <div class="text-muted fs-7">
                      View full contact details
                    </div>
                  </div>
                </div>
              </div>
            </div>
            <!--end::Card body-->
          </div>
          <!--end::Card-->
        </div>
        <!--end:::Tab pane-->
      </div>
      <!--end:::Tab content-->
    </div>
    <!--end::Content-->
  </div>
  <!--end::Layout-->
</template>

<script lang="ts">
import { defineComponent, ref, onMounted } from "vue";
import { useRoute, useRouter } from "vue-router";
import ApiService from "@/core/services/ApiService";
import Swal from "sweetalert2";

export default defineComponent({
  name: "fbo-details",
  setup() {
    const route = useRoute();
    const router = useRouter();
    const fbo = ref<any>(null);
    const loading = ref(true);
    const error = ref<string | null>(null);
    const recentTrips = ref<any[]>([]);

    const fetchFbo = async () => {
      try {
        loading.value = true;
        error.value = null;
        const fboId = route.params.id as string;
        
        const response = await ApiService.get(`/fbos/${fboId}/`);
        fbo.value = response.data;
        
        // TODO: Fetch trips associated with this FBO
        // This would require a backend endpoint to get trips by FBO
        recentTrips.value = [];
        
      } catch (err: any) {
        error.value = err.response?.data?.detail || "Failed to fetch FBO details";
        console.error("Error fetching FBO:", err);
      } finally {
        loading.value = false;
      }
    };

    const getFboName = (): string => {
      return fbo.value?.name || 'Loading...';
    };

    const getFboLocation = (): string => {
      if (!fbo.value) return '';
      
      // Priority: Show airport codes if available
      if (fbo.value.airport_codes && fbo.value.airport_codes.length > 0) {
        return fbo.value.airport_codes.join(', ');
      }
      
      // Fallback to city, state
      const parts = [fbo.value.city, fbo.value.state].filter(Boolean);
      return parts.length > 0 ? parts.join(', ') : 'Location not specified';
    };

    const getFullAddress = (): string => {
      if (!fbo.value) return 'No address provided';
      
      const parts = [
        fbo.value.address_line1,
        fbo.value.address_line2,
        fbo.value.city,
        fbo.value.state,
        fbo.value.zip,
        fbo.value.country
      ].filter(Boolean);
      
      return parts.length > 0 ? parts.join(', ') : 'No address provided';
    };

    const getTotalTrips = (): string => {
      // This would need to be calculated from backend data
      return '0';
    };

    const getStatus = (): string => {
      return 'Active';
    };

    const getLastServiceDate = (): string => {
      // This would need to come from backend data
      return 'N/A';
    };

    const formatDate = (dateString?: string): string => {
      if (!dateString) return 'Not provided';
      return new Date(dateString).toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'long',
        day: 'numeric',
      });
    };

    const handleEdit = () => {
      Swal.fire({
        title: "Edit FBO",
        text: "Edit functionality will be implemented soon.",
        icon: "info",
        confirmButtonText: "OK"
      });
    };

    const navigateToTrip = (tripId: string) => {
      router.push(`/admin/trips/${tripId}`);
    };

    onMounted(() => {
      fetchFbo();
    });

    return {
      fbo,
      loading,
      error,
      recentTrips,
      getFboName,
      getFboLocation,
      getFullAddress,
      getTotalTrips,
      getStatus,
      getLastServiceDate,
      formatDate,
      handleEdit,
      navigateToTrip,
    };
  },
});
</script>