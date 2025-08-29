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
                <i class="ki-duotone ki-people fs-2x text-info">
                  <span class="path1"></span>
                  <span class="path2"></span>
                  <span class="path3"></span>
                  <span class="path4"></span>
                  <span class="path5"></span>
                </i>
              </div>
            </div>
            <!--end::Avatar-->

            <!--begin::Name-->
            <a
              href="#"
              class="fs-3 text-gray-800 text-hover-primary fw-bold mb-1"
            >
              {{ getPassengerName() }}
            </a>
            <!--end::Name-->

            <!--begin::Position-->
            <div class="fs-5 fw-semibold text-muted mb-6">Passenger</div>
            <!--end::Position-->

            <!--begin::Status Badge-->
            <div class="mb-6">
              <span :class="`badge badge-light-${getStatusColor()} fs-8 fw-bold`">
                {{ passenger?.status || 'Active' }}
              </span>
            </div>
            <!--end::Status Badge-->

            <!--begin::Stats-->
            <div class="d-flex flex-wrap flex-center">
              <!--begin::Trips-->
              <div class="border border-gray-300 border-dashed rounded py-3 px-3 mb-3">
                <div class="fs-4 fw-bold text-gray-700">
                  <span class="w-75px">{{ getTotalTrips() }}</span>
                  <KTIcon icon-name="airplane" icon-class="fs-3 text-info" />
                </div>
                <div class="fw-semibold text-muted">Total Trips</div>
              </div>
              <!--end::Trips-->

              <!--begin::Age-->
              <div class="border border-gray-300 border-dashed rounded py-3 px-3 mx-4 mb-3">
                <div class="fs-4 fw-bold text-gray-700">
                  <span class="w-50px">{{ getPassengerAge() }}</span>
                </div>
                <div class="fw-semibold text-muted">Age</div>
              </div>
              <!--end::Age-->

              <!--begin::Registered-->
              <div class="border border-gray-300 border-dashed rounded py-3 px-3 mb-3">
                <div class="fs-4 fw-bold text-gray-700">
                  <span class="w-75px">{{ formatDate(passenger?.created_on).split(',')[0] }}</span>
                </div>
                <div class="fw-semibold text-muted">Registered</div>
              </div>
              <!--end::Registered-->
            </div>
            <!--end::Stats-->
          </div>
          <!--end::Summary-->

          <!--begin::Details toggle-->
          <div class="d-flex flex-stack fs-4 py-3">
            <div
              class="fw-bold rotate collapsible"
              data-bs-toggle="collapse"
              href="#kt_passenger_view_details"
              role="button"
              aria-expanded="false"
              aria-controls="kt_passenger_view_details"
            >
              Details
              <span class="ms-2 rotate-180">
                <KTIcon icon-name="down" icon-class="fs-3" />
              </span>
            </div>

            <span
              data-bs-toggle="tooltip"
              data-bs-trigger="hover"
              title="Edit passenger details"
            >
              <button class="btn btn-sm btn-light-primary" @click="handleEdit">
                Edit
              </button>
            </span>
          </div>
          <!--end::Details toggle-->

          <div class="separator separator-dashed my-3"></div>

          <!--begin::Details content-->
          <div id="kt_passenger_view_details" class="collapse show">
            <div class="py-5 fs-6">
              <!--begin::Details item-->
              <div class="fw-bold mt-5">Passenger ID</div>
              <div class="text-gray-600">{{ passenger?.id || '-' }}</div>
              <!--end::Details item-->
              
              <!--begin::Details item-->
              <div class="fw-bold mt-5">Email</div>
              <div class="text-gray-600">
                <a :href="`mailto:${passenger?.info?.email}`" class="text-gray-600 text-hover-primary" v-if="passenger?.info?.email">
                  {{ passenger.info.email }}
                </a>
                <span v-else>No email</span>
              </div>
              <!--end::Details item-->
              
              <!--begin::Details item-->
              <div class="fw-bold mt-5">Phone</div>
              <div class="text-gray-600">
                <a :href="`tel:${passenger?.info?.phone}`" class="text-gray-600 text-hover-primary" v-if="passenger?.info?.phone">
                  {{ passenger.info.phone }}
                </a>
                <span v-else>No phone</span>
              </div>
              <!--end::Details item-->
              
              <!--begin::Details item-->
              <div class="fw-bold mt-5">Date of Birth</div>
              <div class="text-gray-600">{{ formatDate(passenger?.date_of_birth) }}</div>
              <!--end::Details item-->
              
              <!--begin::Details item-->
              <div class="fw-bold mt-5">Nationality</div>
              <div class="text-gray-600">{{ passenger?.nationality || 'Not specified' }}</div>
              <!--end::Details item-->
              
              <!--begin::Details item-->
              <div class="fw-bold mt-5">Address</div>
              <div class="text-gray-600">
                {{ getFormattedAddress() }}
              </div>
              <!--end::Details item-->
              
              <!--begin::Details item-->
              <div class="fw-bold mt-5">Emergency Contact</div>
              <div class="text-gray-600">
                <a :href="`tel:${passenger?.contact_number}`" class="text-gray-600 text-hover-primary" v-if="passenger?.contact_number">
                  {{ passenger.contact_number }}
                </a>
                <span v-else>Not provided</span>
              </div>
              <!--end::Details item-->
              
              <!--begin::Details item-->
              <div class="fw-bold mt-5">Created</div>
              <div class="text-gray-600">{{ formatDate(passenger?.created_on) }}</div>
              <!--end::Details item-->
            </div>
          </div>
          <!--end::Details content-->
        </div>
        <!--end::Card body-->
      </div>
      <!--end::Card-->

      <!--begin::Travel Information-->
      <div class="card mb-5 mb-xl-8">
        <!--begin::Card header-->
        <div class="card-header border-0">
          <div class="card-title">
            <h3 class="fw-bold m-0">Travel Information</h3>
          </div>
        </div>
        <!--end::Card header-->

        <!--begin::Card body-->
        <div class="card-body pt-2">
          <div class="py-2">
            <!--begin::Travel Details-->
            <div class="fw-bold mt-3">Passport Number</div>
            <div class="text-gray-600">{{ passenger?.passport_number || 'Not provided' }}</div>
            
            <div class="fw-bold mt-5">Passport Expiration</div>
            <div class="text-gray-600">{{ formatDate(passenger?.passport_expiration_date) }}</div>
            
            <div class="fw-bold mt-5">Special Notes</div>
            <div class="text-gray-600">{{ passenger?.notes || 'None' }}</div>
            <!--end::Travel Details-->
          </div>
        </div>
        <!--end::Card body-->
      </div>
      <!--end::Travel Information-->
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
            href="#kt_passenger_view_trips_tab"
          >
            Trip History
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
          id="kt_passenger_view_trips_tab"
          role="tabpanel"
        >
          <!--begin::Card-->
          <div class="card">
            <!--begin::Card header-->
            <div class="card-header border-0 pt-6">
              <div class="card-title">
                <h3 class="fw-bold m-0">Trip History</h3>
              </div>
            </div>
            <!--end::Card header-->

            <!--begin::Card body-->
            <div class="card-body pt-2">
              <div v-if="passengerTrips.length === 0" class="text-center py-10">
                <div class="text-muted fs-6">No trips found for this passenger</div>
              </div>
              <div v-else>
                <div
                  v-for="trip in passengerTrips"
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
import { Modal } from "bootstrap";

export default defineComponent({
  name: "passenger-details",
  setup() {
    const route = useRoute();
    const router = useRouter();
    const passenger = ref<any>(null);
    const loading = ref(true);
    const error = ref<string | null>(null);
    const passengerTrips = ref<any[]>([]);

    const fetchPassenger = async () => {
      try {
        loading.value = true;
        error.value = null;
        const passengerId = route.params.id as string;
        
        const response = await ApiService.get(`/passengers/${passengerId}/`);
        passenger.value = response.data;
        
        // Extract trips from passenger data
        passengerTrips.value = passenger.value.trips || [];
        
      } catch (err: any) {
        error.value = err.response?.data?.detail || "Failed to fetch passenger details";
        console.error("Error fetching passenger:", err);
      } finally {
        loading.value = false;
      }
    };

    const getPassengerName = (): string => {
      if (passenger.value?.info) {
        const firstName = passenger.value.info.first_name || '';
        const lastName = passenger.value.info.last_name || '';
        const fullName = `${firstName} ${lastName}`.trim();
        return fullName || passenger.value.info.business_name || passenger.value.info.email || 'Unknown Passenger';
      }
      return 'Loading...';
    };

    const getTotalTrips = (): string => {
      return passengerTrips.value.length.toString();
    };

    const getPassengerAge = (): string => {
      if (!passenger.value?.date_of_birth) return 'Unknown';
      
      const today = new Date();
      const birthDate = new Date(passenger.value.date_of_birth);
      let age = today.getFullYear() - birthDate.getFullYear();
      const monthDiff = today.getMonth() - birthDate.getMonth();
      
      if (monthDiff < 0 || (monthDiff === 0 && today.getDate() < birthDate.getDate())) {
        age--;
      }
      
      return `${age}y`;
    };

    const getStatusColor = (): string => {
      const status = passenger.value?.status?.toLowerCase();
      switch (status) {
        case 'active': return 'success';
        case 'inactive': return 'secondary';
        case 'pending': return 'warning';
        case 'confirmed': return 'primary';
        default: return 'success';
      }
    };

    const getFormattedAddress = (): string => {
      if (!passenger.value?.info) return 'No address provided';
      
      const addressData = passenger.value.info;
      const parts = [
        addressData.address_line1,
        addressData.city,
        addressData.state,
        addressData.country
      ].filter(Boolean);
      
      return parts.length > 0 ? parts.join(', ') : 'No address provided';
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
      // Navigate back to passengers page and trigger edit modal
      // This would require passing the passenger ID and opening the edit modal
      Swal.fire({
        title: "Edit Passenger",
        text: "Edit functionality will open the passenger edit form.",
        icon: "info",
        confirmButtonText: "OK"
      }).then(() => {
        router.push('/admin/passengers');
      });
    };

    const navigateToTrip = (tripId: string) => {
      router.push(`/admin/trips/${tripId}`);
    };

    onMounted(() => {
      fetchPassenger();
    });

    return {
      passenger,
      loading,
      error,
      passengerTrips,
      getPassengerName,
      getTotalTrips,
      getPassengerAge,
      getStatusColor,
      getFormattedAddress,
      formatDate,
      handleEdit,
      navigateToTrip,
    };
  },
});
</script>